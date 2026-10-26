import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from elementor_lib import section, upsert_page
import shared as _S

ASSET = "/wp-content/themes/hello-elementor-child/assets"

# Partner logos come from the shared list (S.partner_wall) so the homepage and the
# rest of the site stay in sync; no local logo list to drift or misspell.


def band(inner_html, klass="", pad=True):
    """Full-bleed band wrapper carried INSIDE the HTML widget (Elementor section
    padding is zeroed in elementor_lib), so brand band backgrounds/padding apply
    reliably without depending on Elementor's own CSS-class field."""
    p = "padding-block:var(--section-y);" if pad else ""
    return f'<div class="{klass}" style="{p}">{inner_html}</div>'

def card(title, body, dark=False):
    tcol = "#fff" if dark else "var(--ul-green-heritage)"
    bcol = "#d7e8df" if dark else "var(--ink-70)"
    bg = "rgba(255,255,255,.06)" if dark else "#fff"
    bd = "rgba(255,255,255,.14)" if dark else "var(--line)"
    return (f'<div class="ise-card" style="background:{bg};border-color:{bd};">'
            f'<h3 style="color:{tcol};margin:0 0 .5rem;">{title}</h3>'
            f'<p style="margin:0;color:{bcol};">{body}</p></div>')

# ---- NAV (interim; becomes a Theme Builder global header under Pro) ----
nav = '''
<div class="ise-container" style="display:flex;align-items:center;justify-content:space-between;padding-block:1.15rem;gap:1rem;flex-wrap:wrap;">
  <a href="/" style="display:inline-flex;align-items:center;"><img src="/wp-content/themes/hello-elementor-child/assets/ise-ul-logo.png" alt="Immersive Software Engineering · University of Limerick" style="height:40px;width:auto;"></a>
  <nav style="display:flex;gap:1.6rem;align-items:center;font-weight:500;flex-wrap:wrap;">
    <a href="#course" style="text-decoration:none;">The Course</a>
    <a href="/students" style="text-decoration:none;">For Students</a>
    <a href="/companies" style="text-decoration:none;">For Companies</a>
    <a href="/schools" style="text-decoration:none;">For Schools</a>
    <a href="/about" style="text-decoration:none;">About</a>
    <a class="ise-btn ise-btn--primary" href="https://www.ul.ie/study/undergraduate/immersive-software-engineering-bsc-or-msc" target="_blank" rel="noopener" style="padding:.55rem 1.05rem;background:var(--ul-green-modern);color:#04231a;">Apply · LM173</a>
  </nav>
</div>'''

# ---- HERO ----
hero = '''
<div class="ise-container" style="min-height:clamp(560px,78vh,720px);display:flex;flex-direction:column;justify-content:center;padding-block:6rem 5rem;">
  <p class="ise-eyebrow" style="color:#8fe3b0;">Immersive Software Engineering · University of Limerick</p>
  <h1 style="color:#fff;font-size:var(--fs-hero);margin:.6rem 0 1.25rem;max-width:17ch;">Learn by building. Work with the best.</h1>
  <p style="font-size:var(--fs-lead);color:#e7f2ec;max-width:60ch;">A four-year integrated MSc, with the option to exit after three years with a BSc, where you learn by doing and spend half your degree in paid residencies with leading software companies.</p>
  <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-top:2rem;">
    <a class="ise-btn ise-btn--primary" href="https://www.ul.ie/study/undergraduate/immersive-software-engineering-bsc-or-msc" target="_blank" rel="noopener">Apply now, CAO LM173</a>
    <a class="ise-btn ise-btn--ghost ise-btn--on-dark" href="https://outlook.office365.com/owa/calendar/ISERPCallBookingPage@ulcampus.onmicrosoft.com/bookings/" target="_blank" rel="noopener">Book a call</a>
  </div>
</div>'''

# ---- PROPOSITION ----
prop = '''
<div class="ise-container" style="display:grid;grid-template-columns:1.3fr 1fr;gap:clamp(2rem,5vw,4rem);align-items:center;">
  <p class="ise-serif" style="font-size:clamp(1.4rem,2.6vw,2.05rem);color:var(--ul-green-heritage);line-height:1.35;margin:0;">ISE is a computer science degree where you learn by doing, not in lecture halls, but in studios and inside real companies, shipping real software from first year.</p>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.25rem;">
    <div><div class="ise-stat__num">50%</div><div class="ise-stat__label">in paid residency</div></div>
    <div><div class="ise-stat__num">4 yrs</div><div class="ise-stat__label">to an MSc</div></div>
    <div><div class="ise-stat__num">5</div><div class="ise-stat__label">residencies</div></div>
  </div>
</div>'''

# ---- PILLAR A: STUDENTS ----
students = f'''
<div class="ise-container">
  <div style="max-width:54ch;margin-bottom:2.5rem;">
    <p class="ise-eyebrow">The Students</p>
    <h2>A small, highly selective cohort</h2>
    <p class="ise-lead">ISE admits a small group each year, chosen for how they actually think and build. Students join partner engineering teams as paid contributors from early in the programme.</p>
  </div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">
    {card("Selected on substance","A highly selective intake focused on genuine ability, not points alone, we look for real builders.")}
    {card("Learning by shipping","Studio-based, project-driven and continuously assessed. Students build from week one.")}
    {card("Ready for industry","Students contribute to real engineering work from their very first residency, not shadowing from the sidelines.")}
  </div>
  <div style="margin-top:2rem;"><a class="ise-btn ise-btn--ghost" href="/students">Meet the students →</a></div>
</div>'''

# ---- PILLAR B: COMPANIES ----
companies = f'''
<div class="ise-container">
  <div style="max-width:58ch;margin-bottom:2.5rem;">
    <p class="ise-eyebrow" style="color:#8fe3b0;">The Companies</p>
    <h2 style="color:#fff;">You will work inside real engineering teams</h2>
    <p style="color:#d7e8df;font-size:var(--fs-lead);">Residencies are not shadowing. Students join leading engineering teams as paid contributors, from global platforms to Ireland's fastest-growing startups in fintech, medtech, robotics and quantum.</p>
  </div>
  {_S.partner_wall()}
  <div style="margin-top:2.5rem;"><a class="ise-btn ise-btn--on-dark" href="/companies">See partner companies →</a></div>
</div>'''

# ---- HOW IT WORKS ----
years = [
  ("Year 1","Foundations and Residency 1","Studio-based fundamentals in programming, systems and maths, then your first paid residency in the summer."),
  ("Year 2","Residencies 2 and 3","Human-centric computing and security alongside two more paid residencies inside partner engineering teams."),
  ("Year 3","Specialism and Residency 4","Scaling, reliability and a larger immersive software-project residency. Exit here with a BSc (Hons), or continue."),
  ("Year 4","Integrated MSc","AI and machine learning, advanced modules and a research-project residency, completing the integrated MSc."),
]
timeline = ''.join(
  f'<div class="ise-card"><p class="ise-eyebrow" style="margin-bottom:.4rem;">{y}</p>'
  f'<h3 style="margin:0 0 .5rem;">{t}</h3><p style="margin:0;color:var(--ink-70);">{b}</p></div>'
  for y,t,b in years)
how = f'''
<div class="ise-container" id="course">
  <div style="max-width:52ch;margin-bottom:2.25rem;">
    <p class="ise-eyebrow">How it works</p>
    <h2 style="max-width:20ch;">Four years. One master's. Five residencies.</h2>
  </div>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1.25rem;">{timeline}</div>
</div>'''

# ---- CTA ----
cta = '''
<div class="ise-container" style="text-align:center;max-width:760px;">
  <h2 style="color:#fff;">Applications for 2027 are open</h2>
  <p style="color:#e7f2ec;font-size:var(--fs-lead);">Apply through the CAO with code LM173, or talk to our team about residencies and partnerships.</p>
  <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;margin-top:1.5rem;">
    <a class="ise-btn ise-btn--on-dark" href="https://www.ul.ie/study/undergraduate/immersive-software-engineering-bsc-or-msc" target="_blank" rel="noopener">Apply, LM173</a>
    <a class="ise-btn ise-btn--ghost ise-btn--on-dark" href="/become-a-partner">Become a partner</a>
  </div>
</div>'''

# ---- FOOTER ----
# Uses the shared footer so the homepage matches every subpage (Privacy link,
# spaced copyright line, no login-only portal links leaking into the public footer).


# ---- TWO PATHS: student flow vs partner flow ----
two_paths = '''
<div class="ise-container">
  <div style="max-width:54ch;margin-bottom:2rem;">
    <p class="ise-eyebrow">Two ways in</p>
    <h2>Whether you want to study, or to partner</h2>
  </div>
  <div class="ise-paths">
    <div class="ise-path">
      <p class="ise-eyebrow">Future students</p>
      <h3>Join the next cohort</h3>
      <p>Learn by doing, get paid to work with leading companies, and graduate with a master\'s in four years.</p>
      <div class="row"><a class="ise-btn ise-btn--primary" href="/students">Explore the programme →</a><a href="https://www.ul.ie/study/undergraduate/immersive-software-engineering-bsc-or-msc" target="_blank" rel="noopener" style="font-weight:600;">or apply now · LM173</a></div>
    </div>
    <div class="ise-path ise-path--dark">
      <p class="ise-eyebrow">Companies &amp; partners</p>
      <h3>Host an ISE resident</h3>
      <p>Meet ambitious engineers early, host paid residents on your team, and build your hiring pipeline.</p>
      <div class="row"><a class="ise-btn ise-btn--on-dark" href="/companies">How residencies work →</a><a href="/become-a-partner" style="color:#8fe3b0;font-weight:600;">or become a partner</a></div>
    </div>
  </div>
  <p style="margin-top:1.75rem;text-align:center;color:var(--ink-70);">Teacher or guidance counsellor? <a href="/schools" style="color:var(--ul-green);font-weight:600;">For schools →</a></p>
</div>'''

sections = [
  section(band(nav, "ise-nav", pad=False)),
  section(band(hero, "ise-hero").replace('class="ise-hero" style="', 'class="ise-hero" style="background:#0a3f2c url(/wp-content/themes/hello-elementor-child/assets/photos/home-hero.jpg) center/cover no-repeat;')),
  section(band(prop, "ise-band")),
  section(band(two_paths, "")),
  section(band(students, "")),
  section(band(companies, "ise-band--heritage")),
  section(band(how, "ise-band")),
  _S.testimonials("Student stories", "In their words", klass=""),
  section(band(cta, "ise-band--green")),
  _S.footer(),
]
upsert_page(100, "Home", "home", sections, template="elementor_canvas", front=True)
