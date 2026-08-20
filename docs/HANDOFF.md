# Production handoff — importing the ISE site

This package moves the locally-built site onto the production WordPress host in an
**Elementor-native, database-independent** way. No SQLite→MySQL migration needed.

## What's in the package
```
exports/hello-elementor-child.zip        Brand child theme (installable zip)
exports/elementor-templates/*.json       One importable Elementor template per page
exports/elementor-templates/manifest.json  Page list + slugs + which is the front page
```
Regenerate any time: `python3 builders/export_kit.py` (templates) and re-zip
`theme-src/hello-elementor-child`.

## Prerequisites on the host
- WordPress (matching production, currently 6.8.x)
- **Hello Elementor** theme (from wordpress.org)
- **Elementor** (free is enough to import; production also runs **Elementor Pro**
  for the global Theme Builder header/footer and forms)
- **Work on staging first.** Never import directly onto the live page.

## Steps
1. **Theme** — Appearance → Themes: install *Hello Elementor*, then upload
   `hello-elementor-child.zip` and activate it.
2. **Plugins** — install/activate *Elementor* (and *Elementor Pro* if available).
3. **Global brand** — Elementor → Site Settings:
   - *Global Colors*: Primary `#005335`, Secondary `#00B140`, Text `#16211c`,
     Accent `#003726` (see brand values below).
   - *Global Fonts*: Primary **Inter**, Secondary **Roboto Condensed**,
     Text **Inter**, Accent **Cormorant Garamond**.
   (These mirror the CSS tokens in the child theme's `style.css`.)
4. **Import pages** — for each file in `elementor-templates/`:
   Templates → Saved Templates → *Import Templates* → choose the `.json`.
   Then create/assign a Page for it, or use *Elementor → My Templates* to apply
   the page template. Set each page's template to **Elementor Canvas** (until the
   Pro global header/footer exists), or **Elementor Full Width** afterwards.
5. **Front page** — Settings → Reading → *A static page* → Home
   (the `home` template; see `manifest.json.front_page`).
6. **Menus/permalinks** — Settings → Permalinks → *Post name* (`/%postname%/`).
   Build the primary menu to match: The Students, The Companies, Course, About,
   Apply. (Currently the nav/footer are in-page sections; see step 7.)
7. **Global header & footer (Elementor Pro)** — the current build renders the nav
   and footer as the first/last section of each page for a self-contained preview.
   In production, lift these into **Theme Builder → Header** and **→ Footer** as
   global templates, then remove the in-page copies. The markup/classes are in
   `builders/shared.py` (`nav()` / `footer()`).
8. **Site icon** — Appearance → Customize → Site Identity: upload
   `theme-src/hello-elementor-child/assets/favicon-192.png`.

## Brand values (reference)
| Token | Value |
|---|---|
| UL Green (core / primary) | `#005335` (confirm vs `#005844` on the official UL kit) |
| UL Modern Green (accent) | `#00B140` |
| UL Heritage Green (dark) | `#003726` |
| Ink (text) | `#16211c` |
| Display / headings | Roboto Condensed *(brand: Formula Condensed)* |
| Body / UI | Inter |
| Serif accents | Cormorant Garamond *(brand: Saol)* |

## Notes & things to confirm before publishing
- **Fonts** — the licensed UL faces *Saol* and *Formula Condensed* can replace the
  free fallbacks once the font files are supplied.
- **Partner logos** — shown as uniform white marks on the dark band; swap to the
  colour-on-white treatment if preferred. Confirm display permissions.
- **Placeholder copy** — *Global Fellowships*, *For Schools* and *Privacy* carry
  framing copy only; replace with confirmed content (Privacy should use UL's
  official data-protection notice).
- **Analytics/forms** — production also runs MailOptin + Burst/GA; re-add on the host.

## Residency Job Board (custom plugin — partner logins + job uploads)
The job board is a self-contained plugin: **`plugin-src/ise-residency-board/`**. No
paid plugins required.

**Install:** zip the folder (or copy it) into `wp-content/plugins/` and activate
*ISE Residency Board*. On first load it registers everything and seeds a few
sample roles.

**What it provides**
- A **Residency Job** post type (managed in wp-admin → Residency Jobs), with meta:
  round, company (logo slug), monthly salary, ISE champion email, application email.
- A **Partner** user role.
- Shortcodes (already placed on the pages by the builders):
  - `[ise_residency_board]` → the public board on **/jobs** (rounds, per-round
    search, four-field cards), rendered live from published posts.
  - `[ise_residency_submit]` → **/post-a-job**: gated form (partners/admins only)
    that creates a **pending** job for review.
  - `[ise_partner_register]` → company self-registration into the Partner role.

**Partner flow:** register/sign in on /post-a-job → submit a role → it is created
as *Pending* → ISE approves it in wp-admin (Residency Jobs) → it appears on /jobs.
Verified end-to-end locally (pending hidden, approved shown).

**Built-in moderation & approval**
- New partner registrations are created **pending approval** (not auto-logged-in).
  Approve them in **wp-admin → Users** (a "Partner status" column with a one-click
  Approve link). Only approved partners see the submission form.
- Submitting a role creates a **Pending** Residency Job for review under
  **wp-admin → Residency Jobs**.
- Job cards show the partner **logo** when the role's company slug matches a file
  in `assets/partners/`.
- **Email notifications** (via `wp_mail`): the ISE team is emailed on each new
  pending role and each new partner registration; partners are emailed on approval.
  The notification address defaults to the site admin email — override with the
  `ise_rb_notify_email` filter. Email needs a mail-capable host (SMTP) to deliver.

**Further hardening to consider**
- Add spam protection (honeypot/CAPTCHA) to the public register/submit forms.
- Optionally email the ISE team on each new pending submission.
- If you want members-only *viewing* of the board (like Softr), add a membership
  plugin or restrict the /jobs page; the board content itself is public by default.

### Employer tools + in-app applications
- **Skills:** residencies carry a Skills taxonomy; skills show as tags and drive a
  per-round filter on the board.
- **In-app apply:** signed-in students click **Apply in-app** on a residency, send a
  short note (AJAX), and the ISE champion is emailed. Duplicate applications are
  blocked. Students track status at **/my-applications**.
- **Applicants:** partners see applicants to their own roles at **/my-applicants**
  and can **Shortlist / Reject** (AJAX) or open the student's profile.
- **Favourites + search:** the student directory (**/students-directory**) has
  search + skill filter; partners can **♥ save** students and filter to *Saved only*.
- Data: an **Application** post type (wp-admin → Applications) records each apply;
  favourites are stored per partner as user meta. Emails need SMTP on the host.

### Bookmarks, CSV export, applicant digest
- **Student bookmarking:** students tap **☆ Save** on any residency card; a per-round
  **"Saved only"** filter shows just saved roles; saved roles are listed at
  **/my-applications** under "Saved residencies". Stored per student as user meta.
- **CSV export:** partners get a **Download CSV** button on **/my-applicants**
  (admin-post + nonce) exporting their applications (student, email, role, status,
  message, date). Admins export all.
- **Daily applicant digest:** a `wp_cron` event (`ise_rb_digest`) emails each partner a
  summary of new applications to their roles, plus an admin summary. Uses a
  `ise_rb_last_digest` marker. A **"Send digest now"** button appears on the
  wp-admin → Applications screen for manual/testing. Needs real cron + SMTP to deliver
  (wp_cron fires on traffic; use a real cron on the host for reliability).
