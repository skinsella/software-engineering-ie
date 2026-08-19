"""Reusable helpers to author Elementor pages by writing _elementor_data JSON
straight into the wp-now SQLite DB. Structure kept deliberately thin: each
page section is an Elementor <section> holding one HTML widget whose markup
reuses the child theme's ise-* brand classes. This maximises brand-CSS reuse,
keeps sections modular/editable in Elementor, and travels cleanly in the
export kit."""
import json, secrets, sqlite3, time, os

DB = os.path.expanduser("~/.wp-now/wp-content/playground/database/.ht.sqlite")

def eid():
    return secrets.token_hex(4)[:7]

def html_widget(html):
    return {"id": eid(), "elType": "widget", "widgetType": "html",
            "settings": {"html": html}, "elements": []}

def section(inner_html, css_classes="", settings=None):
    """One full-width Elementor section -> one 100% column -> one HTML widget."""
    col = {"id": eid(), "elType": "column",
           "settings": {"_column_size": 100, "_inline_size": None,
                        "padding": {"unit":"px","top":"0","right":"0","bottom":"0","left":"0","isLinked":True}, "margin": {"unit":"px","top":"0","right":"0","bottom":"0","left":"0","isLinked":True}},
           "elements": [html_widget(inner_html)]}
    st = {"content_width": "full", "gap": "no",
          "padding": {"unit":"px","top":"0","right":"0","bottom":"0","left":"0","isLinked":True}, "margin": {"unit":"px","top":"0","right":"0","bottom":"0","left":"0","isLinked":True},
          "structure": "10"}
    if settings:
        st.update(settings)
    if css_classes:
        st["_css_classes"] = css_classes
    return {"id": eid(), "elType": "section", "settings": st, "elements": [col]}

def upsert_page(page_id, title, slug, sections, template="elementor_canvas",
                front=False, menu_order=0):
    data = json.dumps(sections, ensure_ascii=False)
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    con = sqlite3.connect(DB); cur = con.cursor()
    cur.execute("DELETE FROM wp_posts WHERE ID=?", (page_id,))
    cur.execute("DELETE FROM wp_postmeta WHERE post_id=?", (page_id,))
    cur.execute("""INSERT INTO wp_posts
        (ID,post_author,post_date,post_date_gmt,post_content,post_title,post_excerpt,
         post_status,comment_status,ping_status,post_password,post_name,to_ping,pinged,
         post_modified,post_modified_gmt,post_content_filtered,post_parent,guid,menu_order,
         post_type,post_mime_type,comment_count)
        VALUES (?,?,?,?,?,?,?, 'publish','closed','closed','',?, '','', ?,?, '',0, ?, ?, 'page','',0)""",
        (page_id, 1, now, now, "", title, "", slug, now, now,
         f"http://localhost:8881/?page_id={page_id}", menu_order))
    meta = {
        "_elementor_edit_mode": "builder",
        "_elementor_template_type": "wp-page",
        "_elementor_version": "4.2.2",
        "_wp_page_template": template,
        "_elementor_data": data,
        "_elementor_page_settings": "a:0:{}",
    }
    for k, v in meta.items():
        cur.execute("INSERT INTO wp_postmeta (post_id,meta_key,meta_value) VALUES (?,?,?)",
                    (page_id, k, v))
    if front:
        for name, val in (("show_on_front", "page"), ("page_on_front", str(page_id))):
            cur.execute("UPDATE wp_options SET option_value=? WHERE option_name=?", (val, name))
    con.commit(); con.close()
    print(f"upserted page #{page_id} '{title}' ({len(sections)} sections, {len(data)} bytes data)")

def shortcode_widget(code):
    return {"id": eid(), "elType": "widget", "widgetType": "shortcode",
            "settings": {"shortcode": code}, "elements": []}

def section_of(widget, css_classes="", settings=None):
    """Full-width section wrapping a single arbitrary widget (e.g. a shortcode)."""
    zero = {"unit":"px","top":"0","right":"0","bottom":"0","left":"0","isLinked":True}
    col = {"id": eid(), "elType": "column",
           "settings": {"_column_size": 100, "_inline_size": None, "padding": zero, "margin": zero},
           "elements": [widget]}
    st = {"content_width": "full", "gap": "no", "padding": zero, "margin": zero, "structure": "10"}
    if settings: st.update(settings)
    if css_classes: st["_css_classes"] = css_classes
    return {"id": eid(), "elType": "section", "settings": st, "elements": [col]}
