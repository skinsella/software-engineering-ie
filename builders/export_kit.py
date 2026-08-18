"""Export the built pages as importable Elementor template JSON files, plus a
manifest. Each file imports via WordPress → Templates → Import Templates (free
Elementor), or Elementor's Import Kit. Host-independent: no DB migration needed."""
import os, sys, json, sqlite3
sys.path.insert(0, os.path.dirname(__file__))
from elementor_lib import DB

OUT = os.path.join(os.path.dirname(__file__), "..", "exports", "elementor-templates")
os.makedirs(OUT, exist_ok=True)

con = sqlite3.connect(DB); cur = con.cursor()
cur.execute("""SELECT p.ID, p.post_title, p.post_name,
                      (SELECT meta_value FROM wp_postmeta m WHERE m.post_id=p.ID AND m.meta_key='_elementor_data')
               FROM wp_posts p
               WHERE p.post_type='page' AND p.post_status='publish' AND p.ID>=100
               ORDER BY p.ID""")
manifest = []
for pid, title, slug, data in cur.fetchall():
    if not data:
        continue
    tpl = {"version": "0.4", "title": title, "type": "page",
           "page_settings": [], "content": json.loads(data)}
    fn = f"{slug}.json"
    with open(os.path.join(OUT, fn), "w") as f:
        json.dump(tpl, f, ensure_ascii=False)
    manifest.append({"id": pid, "title": title, "slug": slug, "file": fn,
                     "front_page": slug == "home"})
    print(f"  exported {fn:28s} ({title})")
con.close()

with open(os.path.join(OUT, "manifest.json"), "w") as f:
    json.dump({"pages": manifest}, f, indent=2, ensure_ascii=False)
print(f"→ {len(manifest)} templates + manifest.json in exports/elementor-templates/")
