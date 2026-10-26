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

# Human-readable partner names for accessible alt text (slug -> display name).
# Anything not listed falls back to title-casing the slug (stripe -> Stripe).
PARTNER_NAMES = {
    "aws": "AWS", "bd": "BD", "hse": "HSE", "ida": "IDA Ireland", "openai": "OpenAI",
    "ul-at-work": "UL@Work", "ei-electronics": "EI Electronics", "eli-lilly": "Eli Lilly",
    "jaguar-landrover": "Jaguar Land Rover", "johnson-johnson": "Johnson & Johnson",
    "first-derivatives": "First Derivatives", "general-motors": "General Motors",
    "keeper-solutions": "Keeper Solutions", "boston-scientific": "Boston Scientific",
    "enterprise-ireland": "Enterprise Ireland", "virtu-financial": "Virtu Financial",
    "protex-ai": "Protex AI", "carbon-copy": "Carbon Copy", "premium-power": "Premium Power",
    "equal1": "Equal1", "cubic3": "Cubic3", "wrxflo": "WRXFLO", "kinetikiq": "KinetiKiq",
    "openchip": "OpenChip", "cloudcards": "CloudCards", "fluidedge": "FluidEdge",
    "totalcare": "TotalCare", "avtrain": "AVTrain", "susquehanna": "Susquehanna",
}

def partner_name(slug):
    return PARTNER_NAMES.get(slug) or slug.replace("-", " ").title()

def partner_wall():
    cells = ''.join(
        f'<div class="ise-logo-cell">'
        f'<img src="{ASSET}/partners/{n}.png" alt="{partner_name(n)}" loading="lazy" decoding="async"></div>'
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
    <a class="ise-btn ise-btn--primary" href="https://www.ul.ie/study/undergraduate/immersive-software-engineering-bsc-or-msc" target="_blank" rel="noopener" style="padding:.55rem 1.05rem;background:var(--ul-green-modern);color:#04231a;">Apply · LM173</a>
  </nav>
</div>'''
    return section(band(inner, "ise-nav", pad=False))

def footer_html():
    inner = f'''
<div class="ise-container" style="display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:2rem;padding-block:3.5rem 2rem;">
  <div>
    <img src="{ASSET}/ise-ul-logo.png" alt="ISE · University of Limerick" style="height:40px;width:auto;margin-bottom:.35rem;">
    <p style="max-width:34ch;margin:.75rem 0 0;color:#a9c9bb;">Immersive Software Engineering, University of Limerick. A radically practical computer science degree.</p>
  </div>
  <div><h3 style="color:#fff;font-size:1rem;">Explore</h3><p style="line-height:2;margin:.5rem 0 0;"><a href="/students">The Students</a><br><a href="/companies">The Companies</a><br><a href="/course">Course</a></p></div>
  <div><h3 style="color:#fff;font-size:1rem;">Apply</h3><p style="line-height:2;margin:.5rem 0 0;"><a href="https://www.ul.ie/study/undergraduate/immersive-software-engineering-bsc-or-msc" target="_blank" rel="noopener">How to apply</a><br><a href="/why-ise">Why ISE</a><br><a href="/entrance-submission">Entrance submission</a><br><a href="/faq">FAQ</a></p></div>
  <div><h3 style="color:#fff;font-size:1rem;">Connect</h3><p style="line-height:2;margin:.5rem 0 0;"><a href="/about">About us</a><br><a href="/become-a-partner">Partner with us</a><br><a href="/careers">Careers</a><br><a href="/team">Team</a><br><a href="/schools">For schools</a></p></div>
</div>
<div style="border-top:1px solid rgba(255,255,255,.12);"><div class="ise-container" style="display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;padding-block:1.25rem;color:#a9c9bb;font-size:.9rem;"><span>© 2027 University of Limerick</span><span><a href="/privacy">Privacy</a> · CAO code LM173 · software-engineering.ie</span></div></div>'''
    return '<div class="ise-footer">' + inner + '</div>'

def footer():
    return section(footer_html())

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

BTN_APPLY = '<a class="ise-btn ise-btn--primary" href="https://www.ul.ie/study/undergraduate/immersive-software-engineering-bsc-or-msc" target="_blank" rel="noopener">Apply now, CAO LM173</a>'
BTN_CALL  = '<a class="ise-btn ise-btn--ghost ise-btn--on-dark" href="https://outlook.office365.com/owa/calendar/ISERPCallBookingPage@ulcampus.onmicrosoft.com/bookings/" target="_blank" rel="noopener">Book a call</a>'

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


# Illustrative student testimonials, PLACEHOLDER copy + names, to be replaced
# with real, approved student quotes before publishing.
# Real, approved student quotes from the ISE/Stripe graduation press pack
# ("Quotes for Stripe Press Release", approved) and Justyna's ISE reflection.
# Tuple shape: (quote, name, project_line, avatar_filename_or_None). Photos can be
# added later by dropping a file in assets/photos and setting the 4th field.
STUDENT_TESTIMONIALS = [
    ("When I first arrived in Ireland, I couldn't speak English. A few years later, I am graduating with first-class honours through a course that completely changed the direction of my career.",
     "Desiree Charles Dos Santos", "MSc, now a Software Engineer at Analog Devices", "student-desiree.jpg", "https://www.linkedin.com/in/desirèe-charles-b0a4b316b/"),
    ("I was the only one in my school year of 300 who went to UL. I feel so proud of the leap I took, and who I've become.",
     "Josh Sloggett", "BSc, residencies at AWS, Intercom and Stripe; returning to Stripe", "student-josh.jpg", "https://www.linkedin.com/in/joshsloggett/"),
    ("I'm adding 'researcher' to the list of things I never thought I'd achieve when I started ISE.",
     "Justyna Przyborska", "Residencies at Stripe, Analog Devices, AWS and Virtu; now at Stripe", "student-justyna.jpg", "https://www.linkedin.com/in/justyna-przy/"),
    ("I completed four residencies at a diverse range of companies, which is my favourite aspect of the course. It helped me develop both as a programmer and a team member.",
     "Ruairi Glackin", "BSc, residencies at Transact, AWS and BD; returning to AWS", "student-ruairi.jpg", "https://www.linkedin.com/in/ruairíglackin/"),
    ("The programme gave me exactly what I was looking for: the opportunity to learn by building, solve real engineering problems alongside industry, and graduate ready to make an impact from day one.",
     "Adam Byrne", "MSc, residencies at Analog Devices, Provizio and Johnson & Johnson", "student-adam.jpg", "https://www.linkedin.com/in/bxrne/"),
    ("We were taught the way students want to be taught: through assignments instead of big exams, with the freedom to build alongside companies and bring what we learned back to class.",
     "Michelle Vaz", "BSc, residencies at AWS and Fin; returning to AWS", "student-michelle.jpg", "https://www.linkedin.com/in/michelle-vaz/"),
]

def testimonials(eyebrow, title, items=None, klass="ise-band"):
    """Grid of student testimonial cards: quote + avatar + name + project line.
    A falsy avatar renders a neutral placeholder disc (no stock photo of a real person)."""
    items = items or STUDENT_TESTIMONIALS
    def avatar(av):
        # Photo when supplied; otherwise no avatar element at all (used for partner
        # quotes, which come without photos) so the card stays clean.
        if not av:
            return ''
        return f'<img src="{ASSET}/photos/{av}" alt="" loading="lazy" decoding="async">'
    _li_icon = ('<svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true" focusable="false" '
                'style="vertical-align:-2px;margin-left:.35rem;fill:currentColor;">'
                '<path d="M20.45 20.45h-3.56v-5.57c0-1.33-.03-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.47-.9 1.63-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.07 2.07 0 1 1 0-4.14 2.07 2.07 0 0 1 0 4.14zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .78 0 1.73v20.54C0 23.22.79 24 1.77 24h20.45c.98 0 1.78-.78 1.78-1.73V1.73C24 .78 23.2 0 22.22 0z"/></svg>')
    def who(name, li):
        if li:
            return (f'<a class="ise-tcard__name" href="{li}" target="_blank" rel="noopener" '
                    f'aria-label="{name} on LinkedIn">{name}{_li_icon}</a>')
        return f'<div class="ise-tcard__name">{name}</div>'
    cells = ''.join(
        f'<div class="ise-tcard"><p class="ise-tcard__quote">{item[0]}</p>'
        f'<div class="ise-tcard__who">{avatar(item[3])}'
        f'<div>{who(item[1], item[4] if len(item) > 4 else None)}'
        f'<div class="ise-tcard__proj">{item[2]}</div></div></div></div>'
        for item in items)
    inner = (f'<div class="ise-container"><div style="max-width:54ch;margin-bottom:2rem;">'
             f'<p class="ise-eyebrow">{eyebrow}</p><h2>{title}</h2></div>'
             f'<div class="ise-tcards">{cells}</div></div>')
    return section(band(inner, klass))

def assemble(page_id, title, slug, content_sections, menu_order=0, front=False):
    """Wrap page-specific sections between the global nav and footer, then upsert."""
    sections = [nav(active=title if title in ("The Students","The Companies") else "")] \
               + content_sections + [footer()]
    upsert_page(page_id, title, slug, sections, front=front, menu_order=menu_order)
