# Go-live runbook, software-engineering.ie

One sequence for both workstreams: the infra cutover (vhosts, DNS, DB) and the
site readiness (content, SEO, consent, email). It is built around the decisions
already made:

- **Two separate sites, no content merge.** The current production site (57 posts,
  19 pages, 797 media, all its plugins) is untouched and moves to a new hostname.
- **The new site serves the apex + www.** Done by swapping which vhost owns those
  names, never by copying or overwriting.
- **The portal launches closed.** The new site's residency portal (sign-up, board,
  profiles, directory, applications) auto-closes in production, so the public
  marketing site collects no personal data until legal clears. See `SECURITY.md`.

That split means launch has **two phases with different gates**: Phase 1 puts the
marketing site live (small gate); Phase 2 opens the data-collecting portal (legal
gate). Do not conflate them.

Related docs: `HANDOFF.md` (import steps), `SECURITY.md` (hardening + the
kill-switch), `CONTENT-REQUEST.md` (facts still owed).

---

## Phase 0, prep (before the cutover day)

Close the gaps that matter for a *public marketing* site. None of these touch
production yet.

- [ ] **Backups on the new site.** Install/activate UpdraftPlus (or the host's
      backup) on the new site and take one successful backup. Production already
      has this; the new site must too before it becomes the live page.
- [ ] **SEO.** Install an SEO plugin (Yoast, to match production) so the public
      pages get meta descriptions, Open Graph tags and an XML sitemap. The review
      flagged the new build has no meta/OG; without this the live domain loses
      them and its sitemap.
- [ ] **Cookies / GDPR on the public pages.** The pages load Google Fonts, which
      sends visitor IPs to Google. Either self-host the fonts (disable Elementor's
      `google_font_enabled`) **or** add a cookie-consent banner (production has
      one). At minimum, a real cookie/privacy notice must be live, see Phase 1.
- [ ] **Firewall.** AIOWPSEC on production has no equivalent on the new site. The
      code-level hardening (REST/user-enum off, XML-RPC off, security headers) plus
      Cloudflare's WAF at the edge covers the basics *if* Cloudflare is confirmed in
      front of the new vhost. Otherwise restore a firewall plugin. Backfillable.
- [ ] **Content facts.** Resolve the Phase-A/B blockers in `CONTENT-REQUEST.md`
      (award titles, entry requirements incl. maths grade, CAO dates, fees) or
      soften/remove unconfirmed claims. In particular confirm "applications for
      2027 are open" is accurate on the go-live date.
- [ ] **Decisions to confirm with the infra session:**
      - Old-site hostname (suggested `old.software-engineering.ie`).
      - Where `dagobah.software-engineering.ie` points (recommend: stays on the old
        site; it is not part of this rebuild).

> Note: transactional email (WP Mail SMTP) and the approved privacy notice are
> **not** Phase 1 blockers, because the portal is closed and sends no mail and
> collects no data. They move to Phase 2.

---

## Phase 1, cutover (marketing site live, portal closed)

Order matters. Steps 1-3 are the infra session; 4-6 the WordPress side.

1. [ ] **Fresh DB backup of production**, on top of the existing vzdump snapshot,
      immediately before any DB write: `wp db export prod-pre-cutover.sql`.
2. [ ] **DNS:** create the record for the old-site hostname
      (`old.software-engineering.ie`) and let it resolve.
3. [ ] **Apache + certs:**
      - Add a vhost for the old site at its new `ServerName`
        (same docroot + DB), then `certbot` once DNS resolves.
      - Repoint the current `wp.conf` / `wp-le-ssl.conf` off apex/www onto the old
        hostname only.
      - Repoint `skinsella-test.conf` / `skinsella-test-le-ssl.conf` to claim
        `software-engineering.ie` + `www.software-engineering.ie` (the existing cert
        already covers both, no new cert needed).
      - `apachectl configtest && systemctl reload apache2`.
4. [ ] **WordPress URLs + internal links**, each site pointed at its own domain:
      - Old site: `wp option update home https://old.software-engineering.ie` and
        the same for `siteurl`; then
        `wp search-replace 'https://www.software-engineering.ie' 'https://old.software-engineering.ie' --all-tables --precise --skip-columns=guid`.
      - New site: set `home`/`siteurl` to `https://www.software-engineering.ie`;
        `wp search-replace '<staging-domain>' 'https://www.software-engineering.ie' --all-tables --precise --skip-columns=guid`.
5. [ ] **Plugin + permalinks on the new site:** confirm `ise-residency-board` is
      active, then `wp rewrite flush` so the residency routes (`/residency/...`)
      resolve.
6. [ ] **Flip to production:** `wp option update ise_rb_production 1`.
      This does two things at once: removes the site-wide `noindex,nofollow`, and
      **auto-closes the portal**. Do **not** set `ise_rb_signup_open` yet.

### Phase 1 smoke tests
- [ ] Apex and www both load the new site over HTTPS; no mixed-content warnings.
- [ ] `old.software-engineering.ie` loads the old site, posts/media intact.
- [ ] View source on a new-site page: **no** `noindex` meta; Open Graph + meta
      description present (SEO plugin working).
- [ ] Visit `/join`, `/jobs`, `/profile`, `/students-directory`, `/my-applications`:
      each shows the "portal opening soon" notice, **not** a working form or data.
- [ ] Footer `/privacy` loads a real cookie/privacy notice (not the placeholder).
- [ ] `robots.txt` and the XML sitemap serve; submit the sitemap in Search Console.
- [ ] Spot-check internal links and images (no staging-domain URLs left).

### Rollback (Phase 1)
If apex/www misbehave, revert the three vhost files to their previous `ServerName`s
and `systemctl reload apache2`: the old site is back on apex/www within seconds,
because its DB and files were never touched. If a search-replace went wrong, restore
`prod-pre-cutover.sql`. DNS for `old.` can stay; it is additive.

---

## Phase 2, open the portal (after legal clears)

Do **not** start Phase 2 until all of these are true:

- [ ] UL-approved **privacy notice** is live at `/privacy` (replaces the placeholder),
      with the data-controller / DPO contact (`CONTENT-REQUEST.md`, D1/D3).
- [ ] **DPIA** completed for the student directory and sign-up (D2), including the
      under-18 consent basis.
- [ ] **Transactional email** configured (WP Mail SMTP or host SMTP) and test-sent,
      so the board's five `wp_mail` flows (partner approval, new-application alert,
      applicant digest, student welcome, admin notify) actually deliver.
- [ ] **Consent** on the registration forms reviewed against the approved notice
      (confirm-password, consent checkbox, 18+/guardian check are already in code).
- [ ] Decide student identity: open self-registration vs UL SSO / verified
      UL-email domain (recommended before collecting real student data).

Then open it:

- [ ] `wp option update ise_rb_signup_open 1` (or define `ISE_RB_SIGNUP_OPEN` true).
- [ ] Re-run the portal smoke test: `/join` and `/post-a-job` show real forms;
      create one test student + one test partner; submit a test application and
      confirm the notification email arrives; then remove the test accounts.
- [ ] Confirm gated pages (`/profile`, `/students-directory`, `/my-applicants`)
      enforce sign-in and that a signed-in user cannot read another user's data.

To pause the portal again at any time: `wp option update ise_rb_signup_open 0`.
