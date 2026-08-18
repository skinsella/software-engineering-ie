"""Emit a standalone HTML snapshot of the homepage (same child-theme CSS + same
section markup as the Elementor build) so it can be viewed without WordPress."""
import os, sys, shutil
sys.path.insert(0, os.path.dirname(__file__))
import build_home as H  # running import builds the WP page too (idempotent)

CSS = open(os.path.join(os.path.dirname(__file__), "..",
      "theme-src/hello-elementor-child/style.css")).read()

blocks = [
    H.band(H.nav, "ise-nav", pad=False),
    ('<div class="ise-hero" style="background:#0a3f2c;padding-block:var(--section-y);">'
     + H.hero + '</div>'),
    H.band(H.prop, "ise-band"),
    H.band(H.students, ""),
    H.band(H.companies, "ise-band--heritage"),
    H.band(H.how, "ise-band"),
    H.band(H.cta, "ise-band--green"),
    '<div class="ise-footer">' + H.footer + '</div>',
]

doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ISE — homepage preview</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Roboto+Condensed:wght@400;500;700&display=swap" rel="stylesheet">
<style>{CSS}
*{{box-sizing:border-box}} body{{margin:0}} img{{max-width:100%}}
</style></head><body>{''.join(blocks)}</body></html>"""


# bundle brand assets next to the snapshot and point the doc at them
_assets_src = os.path.join(os.path.dirname(__file__), "..", "theme-src/hello-elementor-child/assets")
_assets_dst = os.path.join(os.path.dirname(__file__), "..", "design", "assets")
if os.path.isdir(_assets_dst): shutil.rmtree(_assets_dst)
shutil.copytree(_assets_src, _assets_dst)
doc = doc.replace("/wp-content/themes/hello-elementor-child/assets", "assets")

out = os.path.join(os.path.dirname(__file__), "..", "design", "home_preview.html")
open(out, "w").write(doc)
print("wrote", os.path.abspath(out), len(doc), "bytes")
