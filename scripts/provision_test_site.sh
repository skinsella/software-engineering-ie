#!/usr/bin/env bash
# Root-run, ONE-TIME infra setup for the skinsella-test.software-engineering.ie
# test site: a brand-new MySQL DB/user, a fully separate copy of WordPress
# core (NOT a shared docroot — see notes below), and a new Apache vhost.
#
# Usage: sudo bash scripts/provision_test_site.sh
#
# Safety:
#  - Every resource created here is NEW and independently named; nothing
#    that already exists (config-default.php, wp.conf, the `wordpress` DB,
#    /var/lib/wordpress, /usr/share/wordpress) is written to. Core files are
#    only ever READ from /usr/share/wordpress, then copied elsewhere.
#  - We deliberately do NOT point the new vhost's DocumentRoot at
#    /usr/share/wordpress. That directory's .htaccess is a symlink to
#    /etc/wordpress/htaccess, a hand-edited file shared by every vhost that
#    uses it (it also auto-prepends the production AIOWPSEC firewall
#    bootstrap). Writing rewrite rules there via wp-cli, or having the
#    production firewall bootstrap run against the test DB, is exactly the
#    kind of shared-state risk to avoid. So the test site gets its own full
#    copy of WordPress core instead.
#  - Refuses to run if any target resource already exists, and aborts
#    before restarting Apache if `apache2ctl configtest` fails.
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "Run with: sudo bash $0" >&2
  exit 1
fi

TEST_DOMAIN="skinsella-test.software-engineering.ie"
DOCROOT="/var/www/html/skinsella-test"
DB_NAME="wp_skinsella_test"
DB_USER="wp_skinsella_test"
DB_PASS="$(openssl rand -base64 24 | tr -dc 'A-Za-z0-9' | head -c 24)"
VHOST_NAME="skinsella-test"
VHOST_FILE="/etc/apache2/sites-available/${VHOST_NAME}.conf"
SRC_WP="/usr/share/wordpress"

echo "==> Checking nothing we're about to create already exists"
for f in "$DOCROOT" "$VHOST_FILE"; do
  if [ -e "$f" ]; then
    echo "Refusing to continue: $f already exists." >&2
    exit 1
  fi
done
if mysql -N -e "SHOW DATABASES LIKE '${DB_NAME}';" | grep -q "${DB_NAME}"; then
  echo "Refusing to continue: MySQL database ${DB_NAME} already exists." >&2
  exit 1
fi

echo "==> Creating MySQL database + user (${DB_NAME})"
mysql <<SQL
CREATE DATABASE \`${DB_NAME}\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASS}';
GRANT ALL PRIVILEGES ON \`${DB_NAME}\`.* TO '${DB_USER}'@'localhost';
FLUSH PRIVILEGES;
SQL

echo "==> Copying WordPress core from ${SRC_WP} (read-only) into ${DOCROOT}"
mkdir -p "${DOCROOT}"
rsync -a \
  --exclude 'wp-config.php' \
  --exclude 'wp-content' \
  --exclude '.htaccess' \
  --exclude 'aios-bootstrap.php' \
  "${SRC_WP}/" "${DOCROOT}/"
mkdir -p "${DOCROOT}/wp-content"/{themes,plugins,uploads,upgrade}

echo "==> Fetching WordPress secret keys"
SALTS="$(curl -sL https://api.wordpress.org/secret-key/1.1/salt/ || true)"
if [ -z "$SALTS" ]; then
  echo "   (offline — generating local random salts instead)"
  SALTS=""
  for k in AUTH_KEY SECURE_AUTH_KEY LOGGED_IN_KEY NONCE_KEY AUTH_SALT SECURE_AUTH_SALT LOGGED_IN_SALT NONCE_SALT; do
    v="$(openssl rand -base64 48 | tr -d '\n')"
    SALTS="${SALTS}define('${k}', '${v}');
"
  done
fi

echo "==> Writing ${DOCROOT}/wp-config.php"
cat > "${DOCROOT}/wp-config.php" <<PHP
<?php
define('DB_NAME', '${DB_NAME}');
define('DB_USER', '${DB_USER}');
define('DB_PASSWORD', '${DB_PASS}');
define('DB_HOST', 'localhost');
define('DB_CHARSET', 'utf8mb4');
define('DB_COLLATE', '');

${SALTS}
\$table_prefix = 'wp_';

define('WP_AUTO_UPDATE_CORE', false);
define('FS_METHOD', 'direct');
define('WP_DEBUG', false);

if ( ! defined('ABSPATH') ) {
    define('ABSPATH', __DIR__ . '/');
}
require_once ABSPATH . 'wp-settings.php';
PHP

echo "==> Locking down + group-enabling ${DOCROOT} (www-data owns it; www-data group can write, so 'mark' can too via group membership)"
chown -R www-data:www-data "${DOCROOT}"
chmod -R u+rwX,g+rwX,o-w "${DOCROOT}"
find "${DOCROOT}" -type d -exec chmod g+s {} +
chmod 640 "${DOCROOT}/wp-config.php"

echo "==> Writing ${VHOST_FILE}"
cat > "${VHOST_FILE}" <<APACHE
<VirtualHost *:80>
        ServerName ${TEST_DOMAIN}
        ServerAdmin mark@burkley.net
        DocumentRoot ${DOCROOT}

        <Directory ${DOCROOT}>
            Options FollowSymLinks
            AllowOverride All
            DirectoryIndex index.php
            Require all granted
        </Directory>

        ErrorLog \${APACHE_LOG_DIR}/${VHOST_NAME}-error.log
        CustomLog \${APACHE_LOG_DIR}/${VHOST_NAME}-access.log combined
</VirtualHost>
APACHE

echo "==> Enabling site"
a2ensite "${VHOST_NAME}" >/dev/null

echo "==> Testing Apache config (aborting here if this fails — nothing reloaded)"
apache2ctl configtest

echo "==> Restarting Apache"
systemctl restart apache2

echo "==> Smoke test: existing live site"
curl -s -o /dev/null -w "www.software-engineering.ie -> HTTP %{http_code}\n" \
  -H "Host: www.software-engineering.ie" http://localhost/

echo "==> Smoke test: new test site (expect the WP install wizard, HTTP 200)"
curl -s -o /dev/null -w "${TEST_DOMAIN} -> HTTP %{http_code}\n" \
  -H "Host: ${TEST_DOMAIN}" http://localhost/

echo
echo "Done. Next: run scripts/build_test_site.sh as mark (no sudo) to install"
echo "WordPress + the theme/plugin/pages."
