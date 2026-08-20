"""Shared brand building blocks for every ISE page: asset base, nav + footer,
band/card helpers, the partner-logo wall, and a page-assembly helper that wraps
page-specific sections between the global nav and footer. Keeping these here
ensures every page (home + hubs + secondary) stays visually consistent and
lets the whole site export as one coherent Elementor kit."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from elementor_lib import section, upsert_page

ASSET = "/wp-content/themes/hello-elementor-child/assets"

PARTNER_LOGOS = [
    "stripe", "intercom", "analog-devices", "aws", "manna", "bd", "boston-scientific",
    "transact", "provizio", "tines", "johnson-johnson", "dell", "openai",
    "viotas", "first-derivatives", "dogpatch", "mbryonics", "fiserv", "general-motors",
    "deveire", "eli-lilly", "jaguar-landrover", "keeper-solutions", "mastercard", "ericsson",
    "kirby", "wayflyer", "shannonside", "teckro", "kneat", "macmarts",
    "equal1", "payslip", "workday", "cloudcards", "reasire", "intel",
    "frontline", "jentic", "avtrain", "hse", "fluidedge", "totalcare",
    "cashbook", "openchip", "virtu-financial", "susquehanna", "kinetikiq", "protex-ai",
    "deloitte", "ei-electronics", "qualcomm", "redfaire", "ailtire", "dairymaster",
    "carbon-copy", "cubic3", "wrxflo", "dezzai", "nant", "premium-power",
    "fexco", "fidelity", "ul-at-work", "enterprise-ireland", "ida"]

# ---------- generic helpers ----------
def band(inner_html, klass="", pad=True):
    p = "padding-block:var(--section-y);" if pad else ""
    return f'<div class="{klass}" style="{p}">{inner_html}</div>'

def card(title, body, dark=False):
    tcol = "#fff" if dark else "var(--ul-green-heritage)"
    bcol = "#d7e8df" if dark else "var(--ink-70)"
    bg   = "rgba(255,255,255,.06)" if dark else "#fff"
    bd   = "rgba(255,255,255,.14)" if dark else "var(--line)"
    return (f'<div class="ise-card" style="background:{bg};border-color:{bd};">'
            f'<h3 style="color:{tcol};margin:0 0 .5rem;">{title}</h3>'
            f'<p style="margin:0;color:{bcol};">{body}</p></div>')

def stat(num, label, on_dark=False):
    ncol = "#fff" if on_dark else "var(--ul-green)"
    lcol = "#8fe3b0" if on_dark else "var(--ink-70)"
    return (f'<div><div class="ise-stat__num" style="color:{ncol};">{num}</div>'
            f'<div class="ise-stat__label" style="color:{lcol};">{label}</div></div>')

def partner_wall():
    cells = ''.join(f'<div class="ise-logo-cell"><img src="{ASSET}/partners/{n}.png" alt="{n} logo"></div>'
                    for n in PARTNER_LOGOS)
    return f'<div class="ise-logo-wall ise-logo-wall--mono" style="gap:1rem;margin-top:.5rem;">{cells}</div>'

# ---------- global nav + footer ----------
def nav(active=""):
    def link(href, label):
        cur = ' style="text-decoration:none;font-weight:700;"' if label == active else ' style="text-decoration:none;"'
        return f'<a href="{href}"{cur}>{label}</a>'
    inner = f'''
<div class="ise-container" style="display:flex;align-items:center;justify-content:space-between;padding-block:1.1rem;gap:1rem;flex-wrap:wrap;">
  <a href="/" style="display:inline-flex;align-items:center;"><img src="{ASSET}/ise-ul-logo.png" alt="Immersive Software Engineering · University of Limerick" style="height:40px;width:auto;"></a>
  <nav style="display:flex;gap:1.6rem;align-items:center;font-weight:500;flex-wrap:wrap;">
    {link("/students","The Students")}{link("/companies","The Companies")}{link("/course","Course")}{link("/jobs","Jobs")}{link("/about","About")}<a href="/become-a-partner" style="text-decoration:none;">For partners</a>
    <a class="ise-btn ise-btn--primary" href="/apply" style="padding:.55rem 1.05rem;background:var(--ul-green-modern);color:#04231a;">Apply · LM173</a>
  </nav>
</div>'''
    return section(band(inner, "ise-nav", pad=False))

def footer():
    inner = f'''
<div class="ise-container" style="display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:2rem;padding-block:3.5rem 2rem;">
  <div>
    <img src="{ASSET}/ise-ul-logo.png" alt="ISE · University of Limerick" style="height:40px;width:auto;margin-bottom:.35rem;">
    <p style="max-width:34ch;margin:.75rem 0 0;color:#a9c9bb;">Immersive Software Engineering, University of Limerick. A radically practical computer science degree.</p>
  </div>
  <div><h3 style="color:#fff;font-size:1rem;">Explore</h3><p style="line-height:2;margin:.5rem 0 0;"><a href="/students">The Students</a><br><a href="/companies">The Companies</a><br><a href="/course">Course</a></p></div>
  <div><h3 style="color:#fff;font-size:1rem;">Apply</h3><p style="line-height:2;margin:.5rem 0 0;"><a href="/apply">How to apply</a><br><a href="/why-ise">Why ISE</a><br><a href="/faq">FAQ</a></p></div>
  <div><h3 style="color:#fff;font-size:1rem;">Connect</h3><p style="line-height:2;margin:.5rem 0 0;"><a href="/about">About us</a><br><a href="/companies">Partner with us</a><br><a href="/careers">Careers</a><br><a href="/profile">Student portal</a></p></div>
</div>
<div style="border-top:1px solid rgba(255,255,255,.12);"><div class="ise-container" style="display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;padding-block:1.25rem;color:#a9c9bb;font-size:.9rem;"><span>© 2026 University of Limerick</span><span><a href="/privacy">Privacy</a> · CAO code LM173 · software-engineering.ie</span></div></div>'''
    return section('<div class="ise-footer">' + inner + '</div>')

def hero(eyebrow, title, lead, buttons_html, max_title="17ch", bg_image=None):
    inner = f'''
<div class="ise-container" style="min-height:clamp(440px,58vh,560px);display:flex;flex-direction:column;justify-content:center;padding-block:5rem 4rem;">
  <p class="ise-eyebrow" style="color:#8fe3b0;">{eyebrow}</p>
  <h1 style="color:#fff;font-size:var(--fs-h1);margin:.5rem 0 1.1rem;max-width:{max_title};">{title}</h1>
  <p style="font-size:var(--fs-lead);color:#e7f2ec;max-width:60ch;">{lead}</p>
  <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-top:1.75rem;">{buttons_html}</div>
</div>'''
    bg = "#0a3f2c" + (f" url('{ASSET}/photos/{bg_image}') center/cover no-repeat" if bg_image else "")
    return section(f'<div class="ise-hero" style="background:{bg};padding-block:0;">' + inner + '</div>')

BTN_APPLY = '<a class="ise-btn ise-btn--primary" href="/apply">Apply now — CAO LM173</a>'
BTN_CALL  = '<a class="ise-btn ise-btn--ghost ise-btn--on-dark" href="/companies">Book a call</a>'

def cta(title, text, buttons_html):
    inner = f'''
<div class="ise-container" style="text-align:center;max-width:760px;">
  <h2 style="color:#fff;">{title}</h2>
  <p style="color:#e7f2ec;font-size:var(--fs-lead);">{text}</p>
  <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;margin-top:1.5rem;">{buttons_html}</div>
</div>'''
    return band(inner, "ise-band--green")


def split(img_file, eyebrow, title, body_html, reverse=False):
    """Full-width image + text row (Option B). reverse=True puts text on the left."""
    img = f'<img src="{ASSET}/photos/{img_file}" alt="">'
    text = (f'<div class="ise-split__text"><p class="ise-eyebrow">{eyebrow}</p>'
            f'<h2>{title}</h2>{body_html}</div>')
    inner = (text + img) if reverse else (img + text)
    cls = "ise-split ise-split--rev" if reverse else "ise-split"
    return section(f'<div class="{cls}">{inner}</div>')

def portrait_cards(eyebrow, title, items, klass="ise-band"):
    """Row of student portrait cards (Option D). items = [(img_file, name, sub)]."""
    cells = ''.join(
        f'<div class="ise-pcard"><img src="{ASSET}/photos/{img}" alt="">'
        f'<div class="ise-pcard__c"><h3>{name}</h3><p>{sub}</p></div></div>'
        for img, name, sub in items)
    inner = (f'<div class="ise-container"><div style="max-width:52ch;margin-bottom:2rem;">'
             f'<p class="ise-eyebrow">{eyebrow}</p><h2>{title}</h2></div>'
             f'<div class="ise-pcards">{cells}</div></div>')
    return section(band(inner, klass))


# Illustrative student testimonials — PLACEHOLDER copy + names, to be replaced
# with real, approved student quotes before publishing.
STUDENT_TESTIMONIALS = [
    ("In my first residency I was shipping code to production within weeks — real features used by real customers. I learned more in three months than I thought was possible.",
     "Aoife M.", "Residency at Stripe · payments dashboard", "avatar-2.jpg"),
    ("I went from writing my first real program to building a computer-vision pipeline for a medtech company. ISE throws you in — then makes sure you can swim.",
     "Cian D.", "Residency at Provizio · sensor data & ML", "avatar-1.jpg"),
    ("The studio changed how I work. We build together, review each other's code and ship real things. By second year I already felt like an engineer.",
     "Eoin R.", "Residency at Intercom · internal tooling", "avatar-3.jpg"),
]

def testimonials(eyebrow, title, items=None, klass="ise-band"):
    """Grid of student testimonial cards: quote + avatar + name + project line."""
    items = items or STUDENT_TESTIMONIALS
    cells = ''.join(
        f'<div class="ise-tcard"><p class="ise-tcard__quote">{q}</p>'
        f'<div class="ise-tcard__who"><img src="{ASSET}/photos/{av}" alt="">'
        f'<div><div class="ise-tcard__name">{name}</div>'
        f'<div class="ise-tcard__proj">{proj}</div></div></div></div>'
        for q, name, proj, av in items)
    inner = (f'<div class="ise-container"><div style="max-width:54ch;margin-bottom:2rem;">'
             f'<p class="ise-eyebrow">{eyebrow}</p><h2>{title}</h2></div>'
             f'<div class="ise-tcards">{cells}</div></div>')
    return section(band(inner, klass))

def assemble(page_id, title, slug, content_sections, menu_order=0, front=False):
    """Wrap page-specific sections between the global nav and footer, then upsert."""
    sections = [nav(active=title if title in ("The Students","The Companies") else "")] \
               + content_sections + [footer()]
    upsert_page(page_id, title, slug, sections, front=front, menu_order=menu_order)
