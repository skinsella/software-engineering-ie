#!/usr/bin/env bash
# Root-run, one-time: repoints wp-le-ssl.conf at the correct Let's Encrypt
# certificate.
#
# Currently wp-le-ssl.conf (ServerName www.software-engineering.ie,
# ServerAlias software-engineering.ie + dagobah.software-engineering.ie)
# uses the "abcd-project.ie" certificate, whose SAN list is
# abcd-project.ie / www.abcd-project.ie / software-engineering.ie — it does
# NOT cover www.software-engineering.ie or dagobah.software-engineering.ie.
# `certbot certificates` (checked earlier) shows a correctly-scoped
# certificate already exists and is valid:
#   Certificate Name: software-engineering.ie
#   Domains: software-engineering.ie dagobah.software-engineering.ie www.software-engineering.ie
# This script only swaps the two SSLCertificateFile/SSLCertificateKeyFile
# paths in wp-le-ssl.conf to that certificate — no new cert is issued, no
# other file is touched, and a timestamped backup is kept.
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "Run with: sudo bash $0" >&2
  exit 1
fi

CONF="/etc/apache2/sites-available/wp-le-ssl.conf"
BACKUP="${CONF}.bak.$(date +%Y%m%d%H%M%S)"
NEW_CERT_DIR="/etc/letsencrypt/live/software-engineering.ie"

if [ ! -r "${NEW_CERT_DIR}/fullchain.pem" ] || [ ! -r "${NEW_CERT_DIR}/privkey.pem" ]; then
  echo "Refusing to continue: ${NEW_CERT_DIR}/fullchain.pem or privkey.pem missing/unreadable." >&2
  exit 1
fi

echo "==> Backing up ${CONF} to ${BACKUP}"
cp -p "${CONF}" "${BACKUP}"

echo "==> Updating SSLCertificateFile/SSLCertificateKeyFile"
sed -i \
  -e "s|^SSLCertificateFile .*|SSLCertificateFile ${NEW_CERT_DIR}/fullchain.pem|" \
  -e "s|^SSLCertificateKeyFile .*|SSLCertificateKeyFile ${NEW_CERT_DIR}/privkey.pem|" \
  "${CONF}"

echo "==> Diff:"
diff -u "${BACKUP}" "${CONF}" || true

echo "==> Testing Apache config (aborting here if this fails — nothing reloaded)"
apache2ctl configtest

echo "==> Restarting Apache"
systemctl restart apache2

echo "==> Smoke tests"
for host in www.software-engineering.ie software-engineering.ie dagobah.software-engineering.ie skinsella-test.software-engineering.ie; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --resolve "${host}:443:127.0.0.1" "https://${host}/")
  echo "  ${host} -> HTTP ${code}"
done

echo
echo "Done. Verify cert details manually with, e.g.:"
echo "  curl -v --resolve www.software-engineering.ie:443:127.0.0.1 https://www.software-engineering.ie/ 2>&1 | grep -i subject:"
echo "Backup kept at ${BACKUP} (restore with: cp ${BACKUP} ${CONF} && apache2ctl configtest && systemctl restart apache2)"
