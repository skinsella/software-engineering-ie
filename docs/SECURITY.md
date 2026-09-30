# Pre-deployment security checklist

Response to the security review in the website feedback. Split into what is already
handled in code (the `ise-residency-board` plugin / child theme) and what must be
configured on the production host or by UL IT.

## Done in code (plugin `ise-residency-board`)

- **REST user enumeration blocked** for anonymous visitors (`/wp-json/wp/v2/users`
  and `/wp/v2/users/{id}` are removed via `rest_endpoints`). Logged-in access is
  unchanged.
- **`?author=N` enumeration** redirects to home for anonymous visitors.
- **XML-RPC disabled** (`xmlrpc_enabled` → false).
- **Head disclosure removed**: generator/version tag, RSD link, WLW manifest and
  oEmbed discovery links.
- **Baseline security headers** via `send_headers`: `X-Content-Type-Options: nosniff`,
  `X-Frame-Options: SAMEORIGIN`, `Referrer-Policy: strict-origin-when-cross-origin`,
  `Permissions-Policy` (geolocation/mic/camera off). HSTS is emitted only over HTTPS.
- **noindex until launch**: every page carries `noindex,nofollow` until the site is
  marked live. Flip it on for production by setting option `ise_rb_production = 1`
  **or** defining `ISE_RB_PRODUCTION` true in `wp-config.php`.
- **Registration forms hardened**: confirm-password field, a required consent
  checkbox linking the privacy notice, work-email (free-mail domain) rejection for
  partners, and an 18+/guardian-consent checkbox for students. (Honeypot, optional
  Cloudflare Turnstile CAPTCHA, per-IP throttling and partner admin-approval were
  already present.)
- **Upload validation**: CV (pdf/doc/docx, ≤8 MB) and profile photo
  (jpg/png/webp, ≤5 MB) are validated by real file contents (`wp_check_filetype_and_ext`),
  not the client-supplied MIME type, and `media_handle_upload` is restricted to those types.

## Must be configured on the host / by UL IT

- **HSTS at the edge** with a long max-age + preload once HTTPS is confirmed
  everywhere (the code header is a fallback, not a substitute).
- **Content-Security-Policy**: needs tuning against Elementor/Google Fonts; set at
  the edge/host. Not shipped in code to avoid breaking the Elementor editor.
- **Self-host Google Fonts**: disable `google_font_enabled` in Elementor
  (Settings → Advanced) and load fonts locally — Google Fonts sends visitor IPs to
  Google (EU/GDPR concern).
- **UL SSO / verified UL email domain** for student accounts (replace open
  self-registration). Strongly recommended before real student data is collected.
- **MFA** for partner and admin accounts.
- **Login rate-limiting / brute-force protection** on `wp-login.php` (plugin or WAF);
  optionally move/obscure the login URL.
- **Keep WordPress, Elementor and all plugins fully patched** on the day of launch
  and thereafter (Elementor XSS patches are frequent).
- **Restrict the pre-launch/test site** with HTTP auth or IP allow-listing in
  addition to the code-level noindex.
- **DPIA + lawful basis + consent records** for the student directory (it exposes
  photo, skills, CV and GitHub to signed-in users; some first-years may be under 18).
  A UL data-protection review is required before go-live.

## Not assessed (needs a live host)

Responsive/keyboard/contrast audit, a Lighthouse run, response-header verification,
and confirmation that gating is enforced server-side on `admin-ajax.php` actions and
direct `wp-content/uploads` URLs. Run these on staging before launch.
