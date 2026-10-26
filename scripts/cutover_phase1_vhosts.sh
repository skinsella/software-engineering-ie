#!/usr/bin/env bash
# Root-run, one-time: Phase 1 cutover, infra half.
#
# Repoints which vhost owns which hostname WITHOUT copying or overwriting any
# site's files/DB:
#   - wp.conf / wp-le-ssl.conf (currently www.software-engineering.ie +
#     ServerAlias software-engineering.ie, dagobah.software-engineering.ie,
#     docroot /usr/share/wordpress -- the CURRENT production site) is
#     repointed to ServerName old.software-engineering.ie, ServerAlias
#     dagobah.software-engineering.ie. Docroot/DB untouched.
#   - skinsella-test.conf / skinsella-test-le-ssl.conf (docroot
#     /var/www/html/skinsella-test -- the new site) is repointed to
#     ServerName software-engineering.ie, ServerAlias
#     www.software-engineering.ie, and its SSL vhost is repointed at the
#     existing software-engineering.ie certificate (already covers both
#     names -- no new cert needed for this one).
#
# Does NOT touch certs for the old site -- that cert doesn't cover
# "old.software-engineering.ie" yet, so wp-le-ssl.conf is left referencing
# the existing (soon-to-be-stale-for-this-vhost, but still valid) cert until
# the certbot command printed at the end is run separately.
#
# Backs up all four vhost files with a timestamp before editing.
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "Run with: sudo bash $0" >&2
  exit 1
fi

TS=$(date +%Y%m%d%H%M%S)
AVAIL=/etc/apache2/sites-available

for f in wp.conf wp-le-ssl.conf skinsella-test.conf skinsella-test-le-ssl.conf; do
  cp -p "$AVAIL/$f" "$AVAIL/$f.bak.$TS"
done

echo "==> Repointing wp.conf / wp-le-ssl.conf to old.software-engineering.ie"
for f in wp.conf wp-le-ssl.conf; do
  sed -i \
    -e 's/^\( *\)ServerName www\.software-engineering\.ie$/\1ServerName old.software-engineering.ie/' \
    -e '/^ *ServerAlias software-engineering\.ie$/d' \
    "$AVAIL/$f"
done
# wp-le-ssl.conf carries a second, redundant "ServerAlias www.software-engineering.ie"
# line (added after the Include line) left over from an earlier certbot run --
# drop it now that www belongs to the new site.
sed -i '/^ServerAlias www\.software-engineering\.ie$/d' "$AVAIL/wp-le-ssl.conf"
# the boilerplate http->https RewriteCond matched the old ServerName; update it
sed -i 's/RewriteCond %{SERVER_NAME} =software-engineering\.ie/RewriteCond %{SERVER_NAME} =old.software-engineering.ie/' "$AVAIL/wp.conf"

echo "==> Repointing skinsella-test.conf / skinsella-test-le-ssl.conf to software-engineering.ie + www"
for f in skinsella-test.conf skinsella-test-le-ssl.conf; do
  sed -i \
    -e 's/^\( *\)ServerName skinsella-test\.software-engineering\.ie$/\1ServerName software-engineering.ie\n\1ServerAlias www.software-engineering.ie/' \
    "$AVAIL/$f"
done
sed -i 's/RewriteCond %{SERVER_NAME} =skinsella-test\.software-engineering\.ie/RewriteCond %{SERVER_NAME} =software-engineering.ie/' "$AVAIL/skinsella-test.conf"
# reuse the existing software-engineering.ie cert (already covers apex + www); no new cert needed
sed -i \
  -e 's#SSLCertificateFile /etc/letsencrypt/live/skinsella-test\.software-engineering\.ie/fullchain\.pem#SSLCertificateFile /etc/letsencrypt/live/software-engineering.ie/fullchain.pem#' \
  -e 's#SSLCertificateKeyFile /etc/letsencrypt/live/skinsella-test\.software-engineering\.ie/privkey\.pem#SSLCertificateKeyFile /etc/letsencrypt/live/software-engineering.ie/privkey.pem#' \
  "$AVAIL/skinsella-test-le-ssl.conf"

echo "==> Diffs:"
for f in wp.conf wp-le-ssl.conf skinsella-test.conf skinsella-test-le-ssl.conf; do
  echo "--- $f ---"
  diff -u "$AVAIL/$f.bak.$TS" "$AVAIL/$f" || true
done

echo "==> Testing Apache config (aborting here if this fails -- nothing reloaded)"
apache2ctl configtest

echo "==> Reloading Apache"
systemctl reload apache2

echo
echo "==> Smoke tests (old.software-engineering.ie will show a cert mismatch until the certbot step below is run)"
for host in old.software-engineering.ie dagobah.software-engineering.ie software-engineering.ie www.software-engineering.ie; do
  code=$(curl -sk -o /dev/null -w "%{http_code}" --resolve "${host}:443:127.0.0.1" "https://${host}/")
  echo "  ${host} -> HTTP ${code}"
done

cat <<'EOF'

==> Next: issue a certificate for the old site (needs DNS for
    old.software-engineering.ie to already resolve -- it does):

    certbot --apache \
      -d old.software-engineering.ie -d dagobah.software-engineering.ie \
      --cert-name old-software-engineering-ie \
      --redirect --agree-tos -m mark@burkley.net

Rollback if anything looks wrong:
    for f in wp.conf wp-le-ssl.conf skinsella-test.conf skinsella-test-le-ssl.conf; do
      cp /etc/apache2/sites-available/$f.bak.TIMESTAMP /etc/apache2/sites-available/$f
    done
    apache2ctl configtest && systemctl reload apache2
EOF
