import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import shared as S
from elementor_lib import section

CALL = '<a class="ise-btn ise-btn--ghost ise-btn--on-dark" href="/apply">Book a call</a>'
def sec(inner, klass=""): return section(S.band(inner, klass))

# ============================== APPLY (103) ==============================
apply_hero = S.hero("Apply", "Apply to ISE — CAO&nbsp;LM173",
  "Applications for 2026 entry are made through the CAO. Here is what you need to know to join the next cohort.",
  '<a class="ise-btn ise-btn--primary" href="https://www.cao.ie" rel="noopener">Apply on CAO</a> ' + CALL,
  max_title="16ch")
apply_how = sec(f'''
<div class="ise-container">
  <div style="max-width:52ch;margin-bottom:2.25rem;"><p class="ise-eyebrow">How to apply</p><h2>Three steps to a place</h2></div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">
    {S.card("1 · Apply through the CAO","List Immersive Software Engineering (CAO code LM173) on your CAO application.")}
    {S.card("2 · Meet the requirements","Meet UL's entry requirements for the programme, including maths.")}
    {S.card("3 · Talk to us","Come to a webinar or open day, or book a call with the team to ask anything.")}
  </div>
</div>''', "ise-band")
apply_facts = sec(f'''
<div class="ise-container">
  <div style="max-width:52ch;margin-bottom:2rem;"><p class="ise-eyebrow">Key facts</p><h2>The essentials</h2></div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">
    <div>{S.stat("LM173","CAO course code")}</div>
    <div>{S.stat("4 yrs","integrated BSc + MSc")}</div>
    <div>{S.stat("€10k","EDI scholarships available")}</div>
  </div>
  <p class="ise-lead" style="margin-top:1.75rem;max-width:60ch;">A number of €10,000 Equity, Diversity &amp; Inclusion scholarships are available each year to widen participation. Ask us if you think you may be eligible.</p>
</div>''')
apply_cta = section(S.cta("Ready to apply?","Add CAO code LM173 to your application, or talk to our team first.",
  '<a class="ise-btn ise-btn--on-dark" href="https://www.cao.ie" rel="noopener">Apply on CAO</a> ' + CALL))
S.assemble(103, "Apply", "apply", [apply_hero, apply_how, apply_facts, apply_cta], menu_order=5)

# ============================== COURSE (104) ==============================
years = [
  ("Year 1","Foundations","Studio-based fundamentals — programming, systems and maths — building real projects in small teams."),
  ("Year 2","First residencies","Paid residencies begin. Students join partner engineering teams for three to six months at a time."),
  ("Year 3","Depth &amp; specialism","Deeper residencies paired with advanced coursework in a chosen area of software engineering."),
  ("Year 4","Master's project","A capstone master's project, often with an industry partner, completing the integrated MSc."),
]
timeline = ''.join(f'<div class="ise-card"><p class="ise-eyebrow" style="margin-bottom:.4rem;">{y}</p><h3 style="margin:0 0 .5rem;">{t}</h3><p style="margin:0;color:var(--ink-70);">{b}</p></div>' for y,t,b in years)
course_hero = S.hero("The Course","Four years. Two degrees. Five residencies.",
  "ISE is a four-year integrated BSc and MSc in software engineering where you learn by doing — in studios and inside real companies.",
  S.BTN_APPLY + ' ' + CALL, max_title="20ch")
course_tl = sec(f'''
<div class="ise-container">
  <div style="max-width:52ch;margin-bottom:2rem;"><p class="ise-eyebrow">Year by year</p><h2>How the four years fit together</h2></div>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1.25rem;">{timeline}</div>
</div>''', "ise-band")
course_teach = sec(f'''
<div class="ise-container">
  <div style="max-width:52ch;margin-bottom:2.25rem;"><p class="ise-eyebrow">How you're taught</p><h2>Learning by doing</h2></div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">
    {S.card("Studio-based","Small teams in a studio, closer to a real engineering floor than a classroom.")}
    {S.card("Project-driven","Every module is anchored in building something real.")}
    {S.card("Continuously assessed","Progress is measured through the work itself, not end-of-year exams alone.")}
  </div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;margin-top:2rem;">
    <div>{S.stat("50%","of the degree in industry")}</div>
    <div>{S.stat("5","paid residencies")}</div>
    <div>{S.stat("2","degrees (BSc + MSc)")}</div>
  </div>
</div>''')
course_cta = section(S.cta("Apply for 2026","Add CAO code LM173 to your application.",
  '<a class="ise-btn ise-btn--on-dark" href="/apply">Apply — LM173</a> ' + CALL))
S.assemble(104, "Course", "course", [course_hero, course_tl, course_teach, course_cta], menu_order=3)

# ============================== WHY ISE (105) ==============================
why_hero = S.hero("Why ISE","A different kind of computer science degree",
  "Most degrees teach you about software. ISE has you building it — for real companies, for pay, from first year.",
  S.BTN_APPLY + ' ' + CALL, max_title="20ch")
why_cards = sec(f'''
<div class="ise-container">
  <div style="max-width:52ch;margin-bottom:2.25rem;"><p class="ise-eyebrow">Why choose ISE</p><h2>What makes it different</h2></div>
  <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:1.5rem;">
    {S.card("Learn by doing","Studios and real projects instead of lecture-hall-only terms — you build from week one.")}
    {S.card("Paid residencies","Spend half the degree contributing inside real engineering teams, and get paid for it.")}
    {S.card("Graduate with a master's","Four years to an integrated BSc and MSc — a faster route to a postgraduate qualification.")}
    {S.card("Work with the best","Residencies with world-leading companies and Ireland's fastest-growing startups.")}
  </div>
</div>''', "ise-band")
why_cta = section(S.cta("See if ISE is for you","Applications for 2026 are open through the CAO with code LM173.",
  '<a class="ise-btn ise-btn--on-dark" href="/apply">Apply — LM173</a> ' + CALL))
S.assemble(105, "Why ISE", "why-ise", [why_hero, why_cards, why_cta], menu_order=4)

# ============================== ABOUT (106) ==============================
about_hero = S.hero("About","Immersive Software Engineering at UL",
  "ISE is a radically practical computer science degree at the University of Limerick, built with industry to change how software engineers are trained.",
  S.BTN_APPLY + ' ' + CALL, max_title="20ch")
about_prose = sec('''
<div class="ise-container ise-prose">
  <div style="max-width:52ch;margin-bottom:1.5rem;"><p class="ise-eyebrow">Our approach</p><h2>Trained like engineers, not just taught about engineering</h2></div>
  <p>ISE was designed around a simple idea: the best way to become a great software engineer is to do the work, supported by great teaching. Students split their time between studio-based learning at UL and paid residencies inside real companies — building a portfolio, a network and a master's degree along the way.</p>
  <p>The programme is delivered in partnership with a network of leading technology companies and Irish start-ups, and is part of the University of Limerick.</p>
  <p style="margin-top:1.25rem;"><a class="ise-btn ise-btn--ghost" href="https://www.ul.ie" rel="noopener">University of Limerick →</a></p>
</div>''', "ise-band")
about_cta = section(S.cta("Join the next cohort","Applications for 2026 are open through the CAO with code LM173.",
  '<a class="ise-btn ise-btn--on-dark" href="/apply">Apply — LM173</a> ' + CALL))
S.assemble(106, "About", "about", [about_hero, about_prose, about_cta], menu_order=6)

# ============================== FAQ (107) ==============================
faqs = [
  ("What is ISE?","Immersive Software Engineering is a four-year integrated BSc and MSc in software engineering at the University of Limerick, where you learn by doing — in studios and inside real companies."),
  ("How long is the programme?","Four years, at the end of which you graduate with both a BSc and a master's (MSc)."),
  ("Do I get paid during residencies?","Yes. Residencies are paid — students join partner engineering teams as paid contributors, typically for three to six months at a time."),
  ("How many residencies are there?","Up to five residencies across the programme, making up roughly 50% of your time."),
  ("What is the CAO code?","LM173. List it on your CAO application to apply."),
  ("Which companies take part?","A network of world-leading technology companies and Ireland's fastest-growing start-ups across fintech, medtech, robotics, quantum and more."),
  ("Are there scholarships?","Yes — a number of €10,000 Equity, Diversity &amp; Inclusion scholarships are available each year."),
  ("Where is it based?","At the University of Limerick, Ireland."),
]
faq_items = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs)
faq_hero = S.hero("FAQ","Frequently asked questions",
  "Everything you might want to know about applying to and studying ISE.", S.BTN_APPLY + ' ' + CALL, max_title="18ch")
faq_body = sec(f'<div class="ise-container ise-faq" style="max-width:820px;">{faq_items}</div>')
faq_cta = section(S.cta("Still have a question?","Book a call with our team and we'll help.",
  '<a class="ise-btn ise-btn--on-dark" href="/apply">Book a call</a>'))
S.assemble(107, "FAQ", "faq", [faq_hero, faq_body, faq_cta], menu_order=8)

# ============================== CAREERS (108) ==============================
careers_hero = S.hero("Careers","Where an ISE degree takes you",
  "Graduates leave with a master's, a portfolio of real work, and relationships built across multiple company residencies.",
  S.BTN_APPLY + ' ' + CALL, max_title="18ch")
careers_out = sec(f'''
<div class="ise-container">
  <div style="max-width:52ch;margin-bottom:2.25rem;"><p class="ise-eyebrow">Outcomes</p><h2>A head start on a software career</h2></div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">
    {S.card("A proven track record","Multiple residencies mean graduates have already shipped real work in real teams.")}
    {S.card("A ready-made network","Students build relationships across every company they reside with.")}
    {S.card("A master's degree","Graduates leave with an integrated MSc, not just a bachelor's.")}
  </div>
</div>''', "ise-band")
careers_wall = sec(f'''
<div class="ise-container">
  <div style="max-width:56ch;margin-bottom:1.5rem;"><p class="ise-eyebrow" style="color:#8fe3b0;">Residency partners</p><h2 style="color:#fff;">Companies students have worked with</h2></div>
  {S.partner_wall()}
</div>''', "ise-band--heritage")
careers_cta = section(S.cta("Start your ISE journey","Applications for 2026 are open through the CAO with code LM173.",
  '<a class="ise-btn ise-btn--on-dark" href="/apply">Apply — LM173</a> ' + CALL))
S.assemble(108, "Careers", "careers", [careers_hero, careers_out, careers_wall, careers_cta], menu_order=7)

print("secondary pages built: apply, course, why-ise, about, faq, careers")
