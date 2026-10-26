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
    # `active` is the current page's href (e.g. "/students") so the matching
    # nav item highlights regardless of its label.
    def link(href, label):
        cur = ' style="text-decoration:none;font-weight:700;"' if href == active else ' style="text-decoration:none;"'
        return f'<a href="{href}"{cur}>{label}</a>'
    inner = f'''
<div class="ise-container" style="display:flex;align-items:center;justify-content:space-between;padding-block:1.1rem;gap:1rem;flex-wrap:wrap;">
  <a href="/" style="display:inline-flex;align-items:center;"><img src="{ASSET}/ise-ul-logo.png" alt="Immersive Software Engineering · University of Limerick" style="height:40px;width:auto;"></a>
  <nav style="display:flex;gap:1.6rem;align-items:center;font-weight:500;flex-wrap:wrap;">
    {link("/course","The Course")}{link("/students","For Students")}{link("/companies","For Companies")}{link("/schools","For Schools")}{link("/about","About")}
    <a class="ise-btn ise-btn--primary" href="https://www.ul.ie/study/undergraduate/immersive-software-engineering-bsc-or-msc" target="_blank" rel="noopener" style="padding:.55rem 1.05rem;background:var(--ul-green-modern);color:#04231a;">Apply · LM173</a>
  </nav>
</div>'''
    return section(band(inner, "ise-nav", pad=False))

# Official ISE social channels (name, url, 24x24 SVG path).
SOCIALS = [
    ("Instagram", "https://www.instagram.com/immersivesoftwareengineering/",
     "M12 2.16c3.2 0 3.58.01 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41a3.72 3.72 0 0 1-1.38-.9 3.72 3.72 0 0 1-.9-1.38c-.16-.42-.36-1.06-.41-2.23C2.17 15.58 2.16 15.2 2.16 12s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.16 1.06-.36 2.23-.41C8.42 2.17 8.8 2.16 12 2.16zM12 0C8.74 0 8.33.01 7.05.07 5.78.13 4.9.33 4.14.63c-.79.3-1.46.72-2.12 1.38A5.86 5.86 0 0 0 .63 4.14c-.3.76-.5 1.64-.56 2.91C.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.06 1.27.26 2.15.56 2.91.3.79.72 1.46 1.38 2.12.66.66 1.33 1.08 2.12 1.38.76.3 1.64.5 2.91.56C8.33 23.99 8.74 24 12 24s3.67-.01 4.95-.07c1.27-.06 2.15-.26 2.91-.56a5.86 5.86 0 0 0 2.12-1.38 5.86 5.86 0 0 0 1.38-2.12c.3-.76.5-1.64.56-2.91.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95c-.06-1.27-.26-2.15-.56-2.91a5.86 5.86 0 0 0-1.38-2.12A5.86 5.86 0 0 0 19.86.63c-.76-.3-1.64-.5-2.91-.56C15.67.01 15.26 0 12 0zm0 5.84A6.16 6.16 0 1 0 18.16 12 6.16 6.16 0 0 0 12 5.84zm0 10.16A4 4 0 1 1 16 12a4 4 0 0 1-4 4zm6.4-11.85a1.44 1.44 0 1 0 1.44 1.44 1.44 1.44 0 0 0-1.44-1.44z"),
    ("TikTok", "https://www.tiktok.com/@immersivesoftwareeng",
     "M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1.04-.1z"),
    ("YouTube", "https://www.youtube.com/@immersiveSE",
     "M23.5 6.2a3.02 3.02 0 0 0-2.12-2.14C19.5 3.55 12 3.55 12 3.55s-7.5 0-9.38.51A3.02 3.02 0 0 0 .5 6.2 31.6 31.6 0 0 0 0 12a31.6 31.6 0 0 0 .5 5.8 3.02 3.02 0 0 0 2.12 2.14c1.88.51 9.38.51 9.38.51s7.5 0 9.38-.51a3.02 3.02 0 0 0 2.12-2.14A31.6 31.6 0 0 0 24 12a31.6 31.6 0 0 0-.5-5.8zM9.55 15.57V8.43L15.82 12l-6.27 3.57z"),
    ("LinkedIn", "https://www.linkedin.com/company/ise-ul/",
     "M20.45 20.45h-3.56v-5.57c0-1.33-.03-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.47-.9 1.63-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.07 2.07 0 1 1 0-4.14 2.07 2.07 0 0 1 0 4.14zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .78 0 1.73v20.54C0 23.22.79 24 1.77 24h20.45c.98 0 1.78-.78 1.78-1.73V1.73C24 .78 23.2 0 22.22 0z"),
]

def social_links():
    out = ''
    for name, url, path in SOCIALS:
        out += (f'<a class="ise-social" href="{url}" target="_blank" rel="noopener" aria-label="ISE on {name}">'
                f'<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" aria-hidden="true" focusable="false">'
                f'<path d="{path}"></path></svg></a>')
    return f'<div style="display:flex;gap:1rem;margin-top:1.1rem;">{out}</div>'

def footer_html():
    inner = f'''
<div class="ise-container" style="display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:2rem;padding-block:3.5rem 2rem;">
  <div>
    <img src="{ASSET}/ise-ul-logo.png" alt="ISE · University of Limerick" style="height:40px;width:auto;margin-bottom:.35rem;">
    <p style="max-width:34ch;margin:.75rem 0 0;color:#a9c9bb;">Immersive Software Engineering, University of Limerick. A radically practical computer science degree.</p>
    {social_links()}
  </div>
  <div><h3 style="color:#fff;font-size:1rem;">Explore</h3><p style="line-height:2;margin:.5rem 0 0;"><a href="/students">The Students</a><br><a href="/companies">The Companies</a><br><a href="/course">Course</a></p></div>
  <div><h3 style="color:#fff;font-size:1rem;">Apply</h3><p style="line-height:2;margin:.5rem 0 0;"><a href="https://www.ul.ie/study/undergraduate/immersive-software-engineering-bsc-or-msc" target="_blank" rel="noopener">How to apply</a><br><a href="/why-ise">Why ISE</a><br><a href="/entrance-submission">Entrance submission</a><br><a href="/faq">FAQ</a></p></div>
  <div><h3 style="color:#fff;font-size:1rem;">Connect</h3><p style="line-height:2;margin:.5rem 0 0;"><a href="/about">About us</a><br><a href="/become-a-partner">Partner with us</a><br><a href="/careers">Careers</a><br><a href="/team">Team</a><br><a href="/schools">For schools</a></p></div>
</div>
<div style="border-top:1px solid rgba(255,255,255,.12);"><div class="ise-container" style="display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;padding-block:1.25rem;color:#a9c9bb;font-size:.9rem;"><span>© 2026 University of Limerick</span><span><a href="/privacy">Privacy</a> · CAO code LM173 · software-engineering.ie</span></div></div>'''
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
    sections = [nav(active="/" + slug)] \
               + content_sections + [footer()]
    upsert_page(page_id, title, slug, sections, front=front, menu_order=menu_order)
