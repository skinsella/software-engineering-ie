#!/usr/bin/env bash
# Root-run, one-time: issues a Let's Encrypt cert for the test site and sets
# up the port 80 -> 443 redirect.
#
# Usage: sudo bash scripts/setup_https.sh
#
# Scoped so it cannot touch the existing software-engineering.ie or
# abcd-project.ie certs/vhosts:
#  -d only names skinsella-test.software-engineering.ie
#  --cert-name forces a brand-new certificate (can't merge into an existing one)
#  --apache only edits sites-available/skinsella-test.conf
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "Run with: sudo bash $0" >&2
  exit 1
fi

certbot --apache \
  -d skinsella-test.software-engineering.ie \
  --cert-name skinsella-test.software-engineering.ie \
  --redirect \
  --agree-tos \
  -m mark@burkley.net
