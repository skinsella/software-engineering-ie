#!/usr/bin/env bash
# One-shot local setup for the ISE site on wp-now (Node-only; no Docker).
#
#   Terminal 1:  npx @wp-now/wp-now start --port 8881
#   Terminal 2:  bash scripts/setup_local.sh
#
# Installs Hello Elementor + Elementor, activates the child theme, sets brand
# options + pretty permalinks, and builds all pages. Safe to re-run.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
WC="$HOME/.wp-now/wp-content/playground"
DB="$WC/database/.ht.sqlite"

[ -d "$WC" ] || { echo "wp-now not initialised yet — run 'npx @wp-now/wp-now start' first."; exit 1; }

echo "→ installing Hello Elementor theme + Elementor plugin (if missing)"
tmp="$(mktemp -d)"
[ -d "$WC/themes/hello-elementor" ] || { curl -sL -o "$tmp/t.zip" https://downloads.wordpress.org/theme/hello-elementor.zip && unzip -q -o "$tmp/t.zip" -d "$WC/themes/"; }
[ -d "$WC/plugins/elementor" ]      || { curl -sL -o "$tmp/p.zip" https://downloads.wordpress.org/plugin/elementor.zip && unzip -q -o "$tmp/p.zip" -d "$WC/plugins/"; }

echo "→ syncing child theme"
rm -rf "$WC/themes/hello-elementor-child"
cp -R "$REPO/theme-src/hello-elementor-child" "$WC/themes/hello-elementor-child"

echo "→ activating theme + plugin, setting brand options + permalinks"
sqlite3 "$DB" <<SQL
UPDATE wp_options SET option_value='hello-elementor'       WHERE option_name='template';
UPDATE wp_options SET option_value='hello-elementor-child' WHERE option_name='stylesheet';
UPDATE wp_options SET option_value='a:1:{i:0;s:23:"elementor/elementor.php";}' WHERE option_name='active_plugins';
UPDATE wp_options SET option_value='Immersive Software Engineering' WHERE option_name='blogname';
UPDATE wp_options SET option_value='Exceptional students. World-class companies.' WHERE option_name='blogdescription';
UPDATE wp_options SET option_value='/%postname%/' WHERE option_name='permalink_structure';
DELETE FROM wp_options WHERE option_name='rewrite_rules';
SQL

echo "→ warming Elementor + flushing rewrites"
for i in 1 2 3; do curl -s -o /dev/null http://localhost:8881/wp-admin/ || true; done

echo "→ building pages"
python3 "$REPO/builders/build_all.py"

echo "✓ done — open http://localhost:8881/"
