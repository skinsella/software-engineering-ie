#!/usr/bin/env bash
# Run as `mark` (no sudo) after scripts/provision_test_site.sh has completed.
# Installs WordPress core, Hello Elementor + Elementor, this repo's child
# theme + ISE Residency Board plugin, imports the Elementor page templates,
# and sets pretty permalinks. Idempotent — safe to re-run.
#
# Usage:
#   bash scripts/build_test_site.sh
#
# Optional overrides:
#   WP_ADMIN_USER=admin WP_ADMIN_EMAIL=mark@burkley.net WP_ADMIN_PASS=... \
#     bash scripts/build_test_site.sh
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
TEST_DOMAIN="software-engineering.ie"
DOCROOT="/var/www/html/skinsella-test"
WP_BIN="$HOME/.local/bin/wp"

WP_ADMIN_USER="${WP_ADMIN_USER:-admin}"
WP_ADMIN_EMAIL="${WP_ADMIN_EMAIL:-mark@burkley.net}"

if [ ! -d "$DOCROOT" ]; then
  echo "Docroot ${DOCROOT} doesn't exist — run scripts/provision_test_site.sh first." >&2
  exit 1
fi
if [ ! -w "$DOCROOT" ]; then
  echo "Cannot write to ${DOCROOT} — is 'mark' in the www-data group? (id -nG)" >&2
  exit 1
fi

if [ ! -x "$WP_BIN" ]; then
  echo "-> installing wp-cli to ${WP_BIN}"
  mkdir -p "$(dirname "$WP_BIN")"
  curl -sL -o "$WP_BIN" https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
  chmod +x "$WP_BIN"
fi

WP() { "$WP_BIN" --path="$DOCROOT" --url="http://${TEST_DOMAIN}" "$@"; }

if ! WP core is-installed 2>/dev/null; then
  echo "-> running the WordPress installer"
  install_args=(core install
    --title="Immersive Software Engineering (test)"
    --admin_user="$WP_ADMIN_USER"
    --admin_email="$WP_ADMIN_EMAIL")
  [ -n "${WP_ADMIN_PASS:-}" ] && install_args+=(--admin_password="$WP_ADMIN_PASS")
  WP "${install_args[@]}"
else
  echo "-> WordPress already installed, skipping core install"
fi

echo "-> theme + plugin"
# Pinned to the last classic (pre-Atomic-Widgets) release: this repo's
# templates are the classic elType:section/column/widget JSON format, which
# Elementor 4.x's rewritten frontend renders as empty content. Bump this only
# after confirming the exported templates still render under whatever is
# current.
ELEMENTOR_VERSION="3.35.9"
WP theme is-installed hello-elementor || WP theme install hello-elementor
CURRENT_ELEMENTOR="$(WP plugin get elementor --field=version 2>/dev/null || true)"
if [ "$CURRENT_ELEMENTOR" != "$ELEMENTOR_VERSION" ]; then
  WP plugin install elementor --version="$ELEMENTOR_VERSION" --force
fi
WP plugin is-active elementor || WP plugin activate elementor

echo "-> syncing child theme from ${REPO}/theme-src/hello-elementor-child"
rsync -a --delete "$REPO/theme-src/hello-elementor-child/" "$DOCROOT/wp-content/themes/hello-elementor-child/"
WP theme activate hello-elementor-child

echo "-> syncing ISE Residency Board plugin"
rsync -a --delete "$REPO/plugin-src/ise-residency-board/" "$DOCROOT/wp-content/plugins/ise-residency-board/"
WP plugin is-active ise-residency-board || WP plugin activate ise-residency-board

echo "-> importing Elementor page templates"
WP eval-file "$REPO/scripts/import_elementor_pages.php"

echo "-> permalinks"
WP rewrite structure '/%postname%/'
WP rewrite flush
# wp-cli runs under the PHP CLI SAPI, where WP's got_url_rewrite() can't
# detect Apache, so `wp rewrite flush` often skips writing .htaccess. Write
# the standard block directly if it's still missing (safe: this docroot is
# private to this site, not shared with any other vhost).
if [ ! -f "$DOCROOT/.htaccess" ]; then
  echo "   .htaccess missing, writing it directly"
  cat > "$DOCROOT/.htaccess" <<'HTACCESS'
# BEGIN WordPress
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
RewriteBase /
RewriteRule ^index\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.php [L]
</IfModule>
# END WordPress
HTACCESS
fi

echo "-> ensuring custom redirects block in .htaccess (idempotent)"
# UL's own course page links to this old slug and can't be changed on their
# end; redirect it to the current entrance-submission page. Lives outside
# WordPress's own BEGIN/END markers so `wp rewrite flush` never touches it.
if ! grep -q '# BEGIN custom redirects' "$DOCROOT/.htaccess"; then
  REDIRECTS=$(cat <<'HTACCESS'
# BEGIN custom redirects
RedirectMatch 301 ^/about-the-ise-entrance-submission/?$ https://software-engineering.ie/entrance-submission/
# END custom redirects

HTACCESS
)
  printf '%s' "$REDIRECTS" | cat - "$DOCROOT/.htaccess" > "$DOCROOT/.htaccess.tmp" && mv "$DOCROOT/.htaccess.tmp" "$DOCROOT/.htaccess"
fi

echo "-> clearing stale Elementor caches (per-page CSS + per-element render cache) so content updates actually show"
# _elementor_element_cache holds rendered HTML fragments and is NOT
# invalidated just by updating _elementor_data, so a content-only upstream
# change (e.g. editing a quote) can silently keep serving the old text from
# here even though the DB's _elementor_data is correctly updated.
WP post list --post_type=page --field=ID 2>/dev/null | while read -r id; do
  WP post meta delete "$id" _elementor_css >/dev/null 2>&1 || true
  WP post meta delete "$id" _elementor_element_cache >/dev/null 2>&1 || true
done
rm -f "$DOCROOT/wp-content/uploads/elementor/css/"*.css 2>/dev/null || true

echo "-> warming Elementor's per-page CSS cache"
# Hit HTTPS directly via curl --resolve rather than plain HTTP: once
# certbot's --redirect is in place, port 80 always 301s to the real public
# hostname, and Python's urllib auto-follows that — which fails on this box
# (no NAT hairpin back to its own public IP). curl without -L doesn't
# auto-follow, and --resolve keeps it entirely local.
python3 - "$REPO/exports/elementor-templates/manifest.json" "$TEST_DOMAIN" <<'PY'
import json, sys, subprocess
manifest_path, host = sys.argv[1], sys.argv[2]
manifest = json.load(open(manifest_path))
for p in manifest["pages"]:
    path = "/" if p["front_page"] else f"/{p['slug']}/"
    url = f"https://{host}{path}"
    code = subprocess.run(
        ["curl", "-sk", "-o", "/dev/null", "-w", "%{http_code}",
         "--resolve", f"{host}:443:127.0.0.1", url],
        capture_output=True, text=True
    ).stdout
    print(f"  {code} {p['slug']}")
PY

echo
echo "Done. Visit http://${TEST_DOMAIN}/ once DNS points here, or test now with:"
echo "  curl -H \"Host: ${TEST_DOMAIN}\" http://localhost/"
echo
echo "Still manual (per docs/HANDOFF.md, cosmetic/low-risk — do via wp-admin):"
echo "  - Elementor Site Settings: Global Colors + Global Fonts"
echo "  - Primary menu (Students, Companies, Course, About, Apply)"
echo "  - Site icon (theme-src/hello-elementor-child/assets/favicon-192.png)"
