import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import shared as S
from elementor_lib import section

CALL = '<a class="ise-btn ise-btn--ghost ise-btn--on-dark" href="https://outlook.office365.com/owa/calendar/ISERPCallBookingPage@ulcampus.onmicrosoft.com/bookings/" target="_blank" rel="noopener">Book a call</a>'
def sec(inner, klass=""): return section(S.band(inner, klass))

# ============================== APPLY (103) ==============================
apply_hero = S.hero("Apply", "Apply to ISE, CAO&nbsp;LM173",
  "Applications for 2027 entry are made through the CAO. Here is what you need to know to join the next cohort.",
  '<a class="ise-btn ise-btn--primary" href="https://www.ul.ie/study/undergraduate/immersive-software-engineering-bsc-or-msc" rel="noopener">Apply on CAO</a> ' + CALL,
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
    <div>{S.stat("4 yrs","to an MSc")}</div>
    <div>{S.stat("€10k","EDI scholarships available")}</div>
  </div>
  <p class="ise-lead" style="margin-top:1.75rem;max-width:60ch;">A number of €10,000 Equity, Diversity &amp; Inclusion scholarships are available each year to widen participation. Ask us if you think you may be eligible.</p>
</div>''')
apply_cta = section(S.cta("Ready to apply?","Add CAO code LM173 to your application, or talk to our team first.",
  '<a class="ise-btn ise-btn--on-dark" href="https://www.ul.ie/study/undergraduate/immersive-software-engineering-bsc-or-msc" rel="noopener">Apply on CAO</a> ' + CALL))
S.assemble(103, "Apply", "apply", [apply_hero, apply_how, apply_facts, apply_cta], menu_order=5)

# ============================== COURSE (104) ==============================
# Content sourced from the live UL/ISE course page (/what-you-need-to-know/).
course_hero = S.hero("The Course","Four years. Five paid residencies. An integrated MSc.",
  "ISE is a computer science degree where you learn by doing. You graduate with an integrated BSc and MSc, with the option to exit after three years with a BSc (Hons).",
  S.BTN_APPLY + ' ' + CALL, max_title="22ch")

course_intro = sec('''
<div class="ise-container ise-prose" style="max-width:64ch;">
  <p class="ise-eyebrow">Course details</p>
  <h2>You learn software engineering by doing it</h2>
  <p>ISE is a computer science degree where you learn by doing, and you graduate with an integrated bachelor's and master's qualification. You spend half your time learning on campus under continuous assessment, and the other half getting paid to solve real problems on residencies in leading companies.</p>
  <p>Over your four years you complete five paid residencies, spending more than 40 weeks each year learning in a personalised, highly interactive environment, working in small groups with your peers and mentors.</p>
  <p style="font-family:var(--font-serif);font-size:1.3rem;color:var(--ul-green-heritage);margin-top:1.5rem;">Award codes: LM173 BSc and LK315 MSc in Immersive Software Engineering.</p>
</div>''')

# ---- themed course-structure graphic (4 years, 5 residencies) ----
_struct = [
  ("Year 1","BSc, LM173",[("Sem 1","On campus",0),("Sem 2","On campus",0),("Sem 3","Residency 1",1)]),
  ("Year 2","BSc, LM173",[("Sem 1","Residency 2",1),("Sem 2","On campus",0),("Sem 3","Residency 3",1)]),
  ("Year 3","BSc, LM173",[("Sem 1","On campus",0),("Sem 2","Residency 4",1)]),
  ("Year 4","MSc, LK315",[("Sem 1","On campus",0),("Sem 2","Residency 5",1)]),
]
_sv = ['<svg viewBox="0 0 980 300" role="img" aria-label="ISE course structure: four years with five paid residencies, a BSc after Year 3 or an integrated MSc after Year 4" style="width:100%;height:auto;max-width:980px;display:block;margin:0 auto;font-family:Inter,sans-serif;">']
for _i,(_yr,_aw,_blocks) in enumerate(_struct):
    _x = 12 + _i*239
    _cw = 215
    _sv.append(f'<text x="{_x}" y="22" font-size="17" font-weight="700" fill="#003726">{_yr}</text>')
    _sv.append(f'<text x="{_x}" y="42" font-size="12" fill="#4a5a52" letter-spacing=".04em">{_aw}</text>')
    for _j,(_sem,_label,_res) in enumerate(_blocks):
        _by = 60 + _j*76
        _fill = "#00B140" if _res else "#e8f1ec"
        _tc   = "#ffffff" if _res else "#0a3f2c"
        _sc   = "#eafff2" if _res else "#4a5a52"
        _sub  = "paid residency" if _res else "continuously assessed"
        _mid  = _x + _cw//2
        _sv.append(f'<rect x="{_x}" y="{_by}" width="{_cw}" height="64" rx="12" fill="{_fill}"></rect>')
        _sv.append(f'<text x="{_x+14}" y="{_by+21}" font-size="11" fill="{_sc}" letter-spacing=".04em">{_sem}</text>')
        _sv.append(f'<text x="{_mid}" y="{_by+40}" text-anchor="middle" font-size="16" font-weight="700" fill="{_tc}">{_label}</text>')
        _sv.append(f'<text x="{_mid}" y="{_by+55}" text-anchor="middle" font-size="11" fill="{_sc}">{_sub}</text>')
_sv.append('</svg>')
course_struct = sec(f'''
<div class="ise-container">
  <div style="max-width:54ch;margin-bottom:1.75rem;"><p class="ise-eyebrow">The shape of the degree</p><h2>Four years, five paid residencies</h2></div>
  {''.join(_sv)}
  <p style="margin:1.5rem auto 0;max-width:72ch;text-align:center;color:var(--ink-70);">Roughly half the degree is spent on paid residency. Exit with a BSc (Hons) after Year 3, or continue to the integrated MSc in Year 4.</p>
</div>''', "ise-band")

# ---- full curriculum, year by year (from the live course page) ----
_curr = [
  ("Year 1","BSc, LM173",[
    ("Semester 1",["CS4421 Problem Solving with Computers","CS4431 Effectively Building Software with Others"]),
    ("Semester 2",["CS4422 Data Centric Computing","CS4431 Computation and Architecture Part 1"]),
    ("Semester 3",["CS4443 Computation and Architecture Part 2","CS4453 Residency 1: Software Systems / Dev Part 1"]),
  ]),
  ("Year 2","BSc, LM173",[
    ("Semester 1",["CS4444 Residency 2: Software Systems / Dev Part 2"]),
    ("Semester 2",["CS4445 Human Centric Computing","CS4455 Ethical Hacking and Security Part 1","CS4436 Ethical Hacking and Security Part 2"]),
    ("Semester 3",["CS4446 Residency 3: User Interaction in Practice"]),
  ]),
  ("Year 3","BSc, LM173",[
    ("Semester 1",["CS4437 Scaling for Reliability and Performance","CS4447 Computational Thinking"]),
    ("Semester 2",["CS4448 Residency 4: Immersive Software Project"]),
  ]),
  ("Year 4","MSc, LK315",[
    ("From Year 3, Semester 3",["CS6513 Research Methods"]),
    ("Semester 1",["CS6514 Artificial Intelligence and Machine Learning","CS6524 Software meets World"]),
    ("Semester 2",["CS6515 Residency 5a: ISE Research Project Part 1","CS6525 Residency 5b: ISE Research Project Part 2"]),
  ]),
]
def _mods(ms):
    out = ''
    for m in ms:
        style = 'font-weight:600;color:var(--ul-green);' if 'Residency' in m else 'color:var(--ink-70);'
        out += f'<li style="margin:0 0 .4rem;{style}">{m}</li>'
    return out
_curr_cards = ''
for _yr,_aw,_sems in _curr:
    _inner = f'<p class="ise-eyebrow" style="margin:0 0 .15rem;">{_yr}</p><h3 style="margin:0;font-size:1.05rem;color:var(--ul-green-heritage);">{_aw}</h3>'
    for _sem,_ms in _sems:
        _inner += (f'<p style="font-weight:700;font-size:.72rem;text-transform:uppercase;letter-spacing:.05em;color:#77857e;margin:1rem 0 .4rem;">{_sem}</p>'
                   f'<ul style="margin:0;padding-left:1.1rem;font-size:.9rem;line-height:1.35;">{_mods(_ms)}</ul>')
    _curr_cards += f'<div class="ise-card">{_inner}</div>'
course_curriculum = sec(f'''
<div class="ise-container">
  <div style="max-width:54ch;margin-bottom:2rem;"><p class="ise-eyebrow">What you will study</p><h2>Blocks, year by year</h2></div>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1.25rem;align-items:start;">{_curr_cards}</div>
</div>''')

# ---- entry + key facts (from the live course page) ----
_facts = [
  ("Award","LM173 BSc and LK315 MSc in Immersive Software Engineering."),
  ("Duration","Four years, an integrated BSc/MSc at level 9 on the NFQ, with an exit opportunity after Year 3 with a BSc (Hons) at level 8."),
  ("Subject area","Engineering and Science."),
  ("CAO points","Entry in 2025 required 651 points. Points combine the Leaving Certificate (up to 625) with the Entrance Submission (up to 200)."),
  ("Leaving Certificate","A Leaving Certificate, or an approved equivalent, with at least two H5 grades and four O6 grades, or four H7 grades."),
  ("Subjects","A minimum grade H4 in Mathematics, plus Irish or another language, and English. Contact UL admissions for full details."),
  ("Course fees","ISE fees are the same as for any other BSc in the UL Faculty of Science and Engineering."),
]
_facts_html = ''
for _lab,_val in _facts:
    _facts_html += f'<div class="ise-card"><p class="ise-eyebrow" style="margin:0 0 .35rem;">{_lab}</p><p style="margin:0;color:var(--ink-70);">{_val}</p></div>'
course_facts = sec(f'''
<div class="ise-container">
  <div style="max-width:54ch;margin-bottom:2rem;"><p class="ise-eyebrow">What you need to know</p><h2>Entry and key facts</h2></div>
  <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:1.25rem;">{_facts_html}</div>
</div>''', "ise-band")

course_entry = sec(f'''
<div class="ise-container">
  <div style="max-width:54ch;margin-bottom:2rem;"><p class="ise-eyebrow">Applying</p><h2>Entrance submission and routes in</h2></div>
  <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:1.25rem;">
    {S.card("Entrance submission","Applicants submit either Route A or Route B. You may also be invited to an interview to discuss your submission.")}
    {S.card("Special Mathematics Examination","A Special Mathematics Examination is offered at UL after the Leaving Certificate results if you did not meet the Mathematics requirement.")}
    {S.card("Mature students","Applications from mature students are welcome, through the CAO. See UL's Mature Student Guide and the Mature Student Office.")}
    {S.card("International applicants","Details for international applicants are available through the University of Limerick International Students pages.")}
  </div>
  <div style="margin-top:1.75rem;"><a class="ise-btn ise-btn--ghost" href="/entrance-submission">Entrance submission details →</a></div>
</div>''')

course_teach = sec(f'''
<div class="ise-container">
  <div style="max-width:52ch;margin-bottom:2.25rem;"><p class="ise-eyebrow">How you're taught</p><h2>Learning by doing</h2></div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">
    {S.card("Studio-based","Small teams in a studio, closer to a real engineering floor than a classroom.")}
    {S.card("Project-driven","Every block is anchored in building something real.")}
    {S.card("Continuously assessed","Progress is measured through the work itself, not end-of-year exams alone.")}
  </div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;margin-top:2rem;">
    <div>{S.stat("50%","of the degree in industry")}</div>
    <div>{S.stat("5","paid residencies")}</div>
    <div>{S.stat("MSc","or BSc after 3 years")}</div>
  </div>
</div>''', "ise-band")
course_cta = section(S.cta("Apply for 2027","Add CAO code LM173 to your application.",
  '<a class="ise-btn ise-btn--on-dark" href="https://www.ul.ie/study/undergraduate/immersive-software-engineering-bsc-or-msc" target="_blank" rel="noopener">Apply, LM173</a> ' + CALL))
course_split = S.split("course-teach.jpg", "Inside ISE",
  "Where the learning happens",
  "<p class=\"ise-lead\">Studios, whiteboards and real projects, students work through problems together, closer to an engineering floor than a classroom.</p>")

S.assemble(104, "Course", "course",
  [course_hero, course_intro, course_struct, course_curriculum, course_facts, course_entry, course_split, course_teach, course_cta],
  menu_order=3)

# ============================== WHY ISE (105) ==============================
why_hero = S.hero("Why ISE","A different kind of computer science degree",
  "Most degrees teach you about software. ISE has you building it, for real companies, for pay, from first year.",
  S.BTN_APPLY + ' ' + CALL, max_title="20ch")
why_cards = sec(f'''
<div class="ise-container">
  <div style="max-width:52ch;margin-bottom:2.25rem;"><p class="ise-eyebrow">Why choose ISE</p><h2>What makes it different</h2></div>
  <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:1.5rem;">
    {S.card("Learn by doing","Studios and real projects instead of lecture-hall-only terms, you build from week one.")}
    {S.card("Paid residencies","Spend half the degree contributing inside real engineering teams, and get paid for it.")}
    {S.card("Graduate with a master's","Four years to a master's (MSc), a faster route to a postgraduate qualification.")}
    {S.card("Work with the best","Residencies with world-leading companies and Ireland's fastest-growing startups.")}
  </div>
</div>''', "ise-band")
why_cta = section(S.cta("See if ISE is for you","Applications for 2027 are open through the CAO with code LM173.",
  '<a class="ise-btn ise-btn--on-dark" href="https://www.ul.ie/study/undergraduate/immersive-software-engineering-bsc-or-msc" target="_blank" rel="noopener">Apply, LM173</a> ' + CALL))
why_split = S.split("why-feature.jpg", "In practice",
  "You build from week one",
  "<p class=\"ise-lead\">Real projects in small teams from the first weeks, the fastest way to become a genuinely capable software engineer.</p>",
  reverse=True)

S.assemble(105, "Why ISE", "why-ise", [why_hero, why_cards, why_split, why_cta], menu_order=4)

# ============================== ABOUT (106) ==============================
about_hero = S.hero("About","Immersive Software Engineering at UL",
  "ISE is a radically practical computer science degree at the University of Limerick, built with industry to change how software engineers are trained.",
  S.BTN_APPLY + ' ' + CALL, max_title="20ch")
about_why = sec('''
<div class="ise-container ise-prose" style="max-width:64ch;">
  <p class="ise-eyebrow">Our story</p>
  <h2>Why ISE exists</h2>
  <p>Software runs the modern economy, but the way we train software engineers has barely changed in decades. Ireland's technology companies consistently say they cannot hire enough skilled engineers, and that the gap holds them back. More than three quarters of Irish tech firms report that the shortage costs them money. Immersive Software Engineering was built to close that gap.</p>
  <p>ISE started from a simple conviction. The best way to become a great software engineer is to do the work, supported by great teaching. So instead of four years of lectures and then a first job, ISE students spend about half the degree inside real engineering teams, on paid residencies, from first year. The idea is borrowed from medicine, where residencies have long turned students into practitioners, and brought to computer science.</p>
  <p>The programme was designed at the University of Limerick together with the companies that go on to hire its students, Stripe among them as a founding partner, so that what students learn and what industry needs are the same thing. It was also built to widen who sees software engineering as a path for them, and to bring more students, and more young women, into the field.</p>
  <p>The result is a degree built around real-world complexity rather than the lecture hall, and graduates who reach industry already knowing how to build.</p>
</div>''')

about_industry = sec(f'''
<div class="ise-container">
  <div style="max-width:58ch;margin-bottom:2rem;"><p class="ise-eyebrow">The coalition</p><h2>Built with industry, not just for it</h2>
  <p class="ise-lead">ISE was created with the companies that hire its graduates, not at a distance from them. Stripe helped shape the curriculum and the residency model from the start, and Analog Devices was there at the launch.</p></div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">
    {S.card("More than 70 partners","From global platforms to Ireland's fastest growing startups, including four of the country's nine unicorns.")}
    {S.card("Real residencies","Partners host students on paid residencies and mentor them on real engineering work.")}
    {S.card("Industry scholarships","Partners fund scholarships that widen access to the programme, including an equity, diversity and inclusion award.")}
  </div>
</div>''', "ise-band")

_milestones = [
  ("2021","The idea","UL, Stripe and Analog Devices set out to build a new kind of computer science degree, designed around paid residencies in industry."),
  ("2022","First cohort","The first ISE students start at UL, and AWS funds a Global Fellowships programme for the course."),
  ("2023","Recognised","ISE wins the Technology Ireland Outstanding Academic Achievement award."),
  ("2026","First MSc class","Sixteen students graduate with an integrated master's and move into roles at companies like Stripe, Fin, Analog Devices and AWS."),
]
_ms_cards = ''.join(
  f'<div class="ise-card"><p class="ise-eyebrow" style="margin:0 0 .3rem;color:var(--ul-green-modern);">{y}</p>'
  f'<h3 style="margin:0 0 .5rem;font-size:1.05rem;">{t}</h3><p style="margin:0;color:var(--ink-70);">{b}</p></div>'
  for y,t,b in _milestones)
about_story = sec(f'''
<div class="ise-container">
  <div style="max-width:52ch;margin-bottom:2rem;"><p class="ise-eyebrow">Milestones</p><h2>The story so far</h2></div>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1.25rem;">{_ms_cards}</div>
</div>''')

about_scale = sec(f'''
<div class="ise-container">
  <div style="max-width:52ch;margin-bottom:2rem;"><p class="ise-eyebrow">Where it stands now</p><h2>A growing programme</h2></div>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1.5rem;">
    <div>{S.stat("~60","students a year")}</div>
    <div>{S.stat("70+","partner organisations")}</div>
    <div>{S.stat("5","paid residencies")}</div>
    <div>{S.stat("16","first MSc graduates in 2026")}</div>
  </div>
</div>''', "ise-band")

about_quote = sec('''
<div class="ise-container" style="text-align:center;max-width:760px;">
  <blockquote style="margin:0;padding:0;border:0;">
    <p class="ise-serif" style="font-size:clamp(1.5rem,3vw,2.1rem);color:#fff;line-height:1.35;margin:0;">“Working with the staff and students of ISE over the past two years has been an incredibly rewarding journey. Seeing our first MSc graduating class preparing to cross the stage is the ultimate validation of our curriculum, proving the immersive teaching model delivers exactly what we set out to achieve.”</p>
    <footer style="font-family:var(--font-sans);font-size:1rem;color:#8fe3b0;margin-top:1.25rem;">Dr Mark Burkley · Course Director, Immersive Software Engineering</footer>
  </blockquote>
</div>''', "ise-band--heritage")
about_follow = sec('''
<div class="ise-container" style="text-align:center;max-width:720px;">
  <p class="ise-eyebrow">Follow ISE</p>
  <h2>See it for yourself</h2>
  <p class="ise-lead" style="margin-left:auto;margin-right:auto;">The everyday of ISE, from residencies to student projects, lives on our channels.</p>
  <div style="display:flex;gap:.9rem;justify-content:center;flex-wrap:wrap;margin-top:1.5rem;">
    <a class="ise-btn ise-btn--ghost" href="https://www.instagram.com/immersivesoftwareengineering/" target="_blank" rel="noopener">Instagram →</a>
    <a class="ise-btn ise-btn--ghost" href="https://www.tiktok.com/@immersivesoftwareeng" target="_blank" rel="noopener">TikTok →</a>
    <a class="ise-btn ise-btn--ghost" href="https://www.youtube.com/@immersiveSE" target="_blank" rel="noopener">YouTube →</a>
    <a class="ise-btn ise-btn--ghost" href="https://www.linkedin.com/company/ise-ul/" target="_blank" rel="noopener">LinkedIn →</a>
  </div>
</div>''')

about_cta = section(S.cta("Join the next cohort","Applications for 2027 are open through the CAO with code LM173.",
  '<a class="ise-btn ise-btn--on-dark" href="https://www.ul.ie/study/undergraduate/immersive-software-engineering-bsc-or-msc" target="_blank" rel="noopener">Apply, LM173</a> ' + CALL))
S.assemble(106, "About", "about",
  [about_hero, about_why, about_industry, about_story, about_scale, about_quote, about_follow, about_cta],
  menu_order=6)

# ============================== FAQ (107) ==============================
faqs = [
  ("What is ISE?","Immersive Software Engineering is a four-year MSc in software engineering at the University of Limerick (with a BSc exit option after three years), where you learn by doing, in studios and inside real companies."),
  ("How long is the programme?","Four years, graduating with a master's (MSc). Students may exit after three years with a BSc instead."),
  ("Do I get paid during residencies?","Yes. Residencies are paid, students join partner engineering teams as paid contributors, typically for three to six months at a time."),
  ("How many residencies are there?","Up to five residencies across the programme, making up roughly 50% of your time."),
  ("What is the CAO code?","LM173. List it on your CAO application to apply."),
  ("Which companies take part?","A network of world-leading technology companies and Ireland's fastest-growing start-ups across fintech, medtech, robotics, quantum and more."),
  ("Are there scholarships?","Yes, a number of €10,000 Equity, Diversity &amp; Inclusion scholarships are available each year."),
  ("Where is it based?","At the University of Limerick, Ireland."),
]
faq_items = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs)
faq_hero = S.hero("FAQ","Frequently asked questions",
  "Everything you might want to know about applying to and studying ISE.", S.BTN_APPLY + ' ' + CALL, max_title="18ch")
faq_body = sec(f'<div class="ise-container ise-faq" style="max-width:820px;">{faq_items}</div>')
faq_cta = section(S.cta("Still have a question?","Book a call with our team and we'll help.",
  '<a class="ise-btn ise-btn--on-dark" href="https://outlook.office365.com/owa/calendar/ISERPCallBookingPage@ulcampus.onmicrosoft.com/bookings/" target="_blank" rel="noopener">Book a call</a>'))
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
careers_cta = section(S.cta("Start your ISE journey","Applications for 2027 are open through the CAO with code LM173.",
  '<a class="ise-btn ise-btn--on-dark" href="https://www.ul.ie/study/undergraduate/immersive-software-engineering-bsc-or-msc" target="_blank" rel="noopener">Apply, LM173</a> ' + CALL))
S.assemble(108, "Careers", "careers", [careers_hero, careers_out, careers_wall, careers_cta], menu_order=7)

print("secondary pages built: apply, course, why-ise, about, faq, careers")
