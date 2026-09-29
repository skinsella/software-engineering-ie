import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import shared as S
from elementor_lib import section
CALL='<a class="ise-btn ise-btn--ghost ise-btn--on-dark" href="https://outlook.office365.com/owa/calendar/ISERPCallBookingPage@ulcampus.onmicrosoft.com/bookings/" target="_blank" rel="noopener">Book a call</a>'
def sec(inner, klass=""): return section(S.band(inner, klass))

# ===================== GLOBAL FELLOWSHIPS (109) =====================
# NOTE: framing copy, confirm programme specifics with the ISE team before publishing.
fel_hero=S.hero("Global Fellowships","The Global Fellowships Programme",
  "A programme that extends the ISE model beyond Ireland, connecting exceptional students with leading engineering teams internationally.",
  S.BTN_APPLY+' '+CALL, max_title="18ch")
fel_body=sec(f'''
<div class="ise-container">
  <div style="max-width:52ch;margin-bottom:2.25rem;"><p class="ise-eyebrow">Overview</p><h2>Global reach, the same immersive model</h2></div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">
    {S.card("International residencies","Opportunities to reside with partner engineering teams beyond Ireland.")}
    {S.card("A global network","Build relationships with companies and mentors across borders.")}
    {S.card("The ISE approach","The same learn-by-doing model, applied on an international stage.")}
  </div>
  <p class="ise-lead" style="margin-top:1.75rem;max-width:60ch;">Programme details are being confirmed, talk to the team to find out more.</p>
</div>''', "ise-band")
fel_cta=section(S.cta("Interested in the Fellowships?","Get in touch to learn more about international opportunities.",
  '<a class="ise-btn ise-btn--on-dark" href="https://outlook.office365.com/owa/calendar/ISERPCallBookingPage@ulcampus.onmicrosoft.com/bookings/" target="_blank" rel="noopener">Book a call</a>'))
S.assemble(109,"Global Fellowships","global-fellowships",[fel_hero,fel_body,fel_cta],menu_order=10)

# ===================== EDI SCHOLARSHIPS (110) =====================
edi_hero=S.hero("Scholarships","€10,000 EDI Scholarships",
  "Equity, Diversity & Inclusion scholarships help widen who gets to take part in ISE, supporting talented students from under-represented backgrounds.",
  '<a class="ise-btn ise-btn--primary" href="https://www.ul.ie/study/undergraduate/immersive-software-engineering-bsc-or-msc" target="_blank" rel="noopener">How to apply</a> '+CALL, max_title="16ch")
edi_body=sec(f'''
<div class="ise-container">
  <div style="max-width:52ch;margin-bottom:2rem;"><p class="ise-eyebrow">The scholarships</p><h2>Support to help you take part</h2></div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">
    <div>{S.stat("€10k","per scholarship")}</div>
    <div>{S.stat("Each year","new awards")}</div>
    <div>{S.stat("EDI","widening participation")}</div>
  </div>
  <p class="ise-lead" style="margin-top:1.75rem;max-width:62ch;">Scholarships are awarded to help talented students from under-represented backgrounds join ISE. Eligibility and application details are confirmed each year, ask us if you think you may be eligible.</p>
</div>''', "ise-band")
edi_cta=section(S.cta("Apply for ISE","Add CAO code LM173 to your application, and talk to us about EDI support.",
  '<a class="ise-btn ise-btn--on-dark" href="https://www.ul.ie/study/undergraduate/immersive-software-engineering-bsc-or-msc" target="_blank" rel="noopener">Apply, LM173</a> '+CALL))
S.assemble(110,"EDI Scholarships","edi-scholarships",[edi_hero,edi_body,edi_cta],menu_order=11)

# ===================== SCHOOLS (111) =====================
sch_hero=S.hero("For Schools","Guidance counsellors & teachers",
  "Everything you need to tell students about Immersive Software Engineering, a new route into a software career through the University of Limerick.",
  '<a class="ise-btn ise-btn--primary" href="https://www.ul.ie/study/undergraduate/immersive-software-engineering-bsc-or-msc" target="_blank" rel="noopener">Book a school talk</a> '+CALL, max_title="18ch")
sch_body=sec(f'''
<div class="ise-container">
  <div style="max-width:52ch;margin-bottom:2.25rem;"><p class="ise-eyebrow">For schools</p><h2>Help your students find ISE</h2></div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">
    {S.card("What ISE is","A four-year MSc (or a three-year BSc) where students learn by doing, in studios and paid company residencies. CAO code LM173.")}
    {S.card("Who it suits","Curious, motivated students who like building things, not only those with the highest points.")}
    {S.card("Book a talk","We're happy to speak with your students, in person or online, about the programme and how to apply.")}
  </div>
</div>''', "ise-band")
sch_cta=section(S.cta("Invite us to your school","Get in touch to arrange a talk or request materials.",
  '<a class="ise-btn ise-btn--on-dark" href="https://www.ul.ie/study/undergraduate/immersive-software-engineering-bsc-or-msc" target="_blank" rel="noopener">Book a school talk</a>'))
S.assemble(111,"For Schools","schools",[sch_hero,sch_body,sch_cta],menu_order=12)

# ===================== BECOME A PARTNER (112) =====================
par_hero=S.hero("Partner with ISE","Become a residency partner",
  "Host ISE students as paid contributors on your engineering team, and meet exceptional talent years before the graduate market does.",
  '<a class="ise-btn ise-btn--primary" href="https://outlook.office365.com/owa/calendar/ISERPCallBookingPage@ulcampus.onmicrosoft.com/bookings/" target="_blank" rel="noopener">Book a call</a> <a class="ise-btn ise-btn--ghost ise-btn--on-dark" href="/companies">How residencies work</a>',
  max_title="18ch")
par_body=sec(f'''
<div class="ise-container">
  <div style="max-width:52ch;margin-bottom:2.25rem;"><p class="ise-eyebrow">Why partner</p><h2>The strongest route to great engineers</h2></div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">
    {S.card("Real contribution","Students join your team as paid contributors on real work for three to six months.")}
    {S.card("Fully supported","Academic mentors and a learning framework wrap around every placement.")}
    {S.card("Build your pipeline","Residencies are the strongest possible route to hiring, you've already worked together.")}
  </div>
</div>''', "ise-band")
par_wall=sec(f'''
<div class="ise-container">
  <div style="max-width:56ch;margin-bottom:1.5rem;"><p class="ise-eyebrow" style="color:#8fe3b0;">In good company</p><h2 style="color:#fff;">Join our network of partners</h2></div>
  {S.partner_wall()}
</div>''', "ise-band--heritage")
par_cta=section(S.cta("Talk to our residency team","Tell us about your team and we'll find the right fit.",
  '<a class="ise-btn ise-btn--on-dark" href="https://outlook.office365.com/owa/calendar/ISERPCallBookingPage@ulcampus.onmicrosoft.com/bookings/" target="_blank" rel="noopener">Book a call</a>'))
S.assemble(112,"Become a partner","become-a-partner",[par_hero,par_body,par_wall,par_cta],menu_order=13)

# ===================== PRIVACY (113) =====================
# NOTE: placeholder, replace with the approved UL/ISE privacy notice before publishing.
pri_hero=S.hero("Privacy","Privacy notice",
  "How we handle your information when you use this site or apply to ISE.", '', max_title="16ch")
pri_body=sec('''
<div class="ise-container ise-prose">
  <p>Immersive Software Engineering is part of the University of Limerick. Your personal data is processed in line with the University of Limerick's data protection policies and privacy notices.</p>
  <p>This page is a placeholder. The published site should link to, or reproduce, the University of Limerick's official data protection notice and any ISE-specific privacy statement approved by the University.</p>
  <p style="margin-top:1.25rem;"><a class="ise-btn ise-btn--ghost" href="https://www.ul.ie/corporatesecretary/data-protection" rel="noopener">UL data protection →</a></p>
</div>''', "ise-band")
S.assemble(113,"Privacy","privacy",[pri_hero,pri_body],menu_order=20)

print("extra pages built: global-fellowships, edi-scholarships, schools, become-a-partner, privacy")

# ===================== TEAM (122) =====================
# NOTE: placeholder, add real ISE team names, roles, photos and a booking/contact link.
team_hero=S.hero("The team","Meet the ISE team",
  "The people behind Immersive Software Engineering, teaching, mentoring and connecting students with residency partners.",
  '<a class="ise-btn ise-btn--primary" href="https://www.ul.ie/study/undergraduate/immersive-software-engineering-bsc-or-msc" target="_blank" rel="noopener">Programme details on ul.ie</a>', max_title="18ch")
team_body=sec(f'''
<div class="ise-container">
  <div style="max-width:54ch;margin-bottom:2rem;"><p class="ise-eyebrow">Placeholder</p><h2>Team profiles</h2>
  <p class="ise-lead">Team member names, roles and photos will appear here. Add them from the ISE team.</p></div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">
    {S.card("Programme Director","Name and bio to be added.")}
    {S.card("Residency Lead","Name and bio to be added.")}
    {S.card("Studio Faculty","Name and bio to be added.")}
  </div>
</div>''', "ise-band")
team_cta=section(S.cta("Talk to the ISE team","Book a call about the programme, residencies or partnerships.",
  '<a class="ise-btn ise-btn--on-dark" href="https://www.ul.ie/study/undergraduate/immersive-software-engineering-bsc-or-msc" target="_blank" rel="noopener">Contact via ul.ie</a>'))
S.assemble(122,"Team","team",[team_hero,team_body,team_cta],menu_order=15)

# ===================== ENTRANCE SUBMISSION (123) =====================
es_hero=S.hero("Applying","The ISE entrance submission",
  "ISE looks beyond points. Alongside your CAO application you complete an entrance submission, worth up to 200 points, so we can see how you think and build.",
  '<a class="ise-btn ise-btn--primary" href="https://www.software-engineering.ie/about-the-ise-entrance-submission/" target="_blank" rel="noopener">Read the full brief</a>', max_title="18ch")

es_routes=sec(f'''
<div class="ise-container">
  <div style="max-width:58ch;margin-bottom:2rem;"><p class="ise-eyebrow">How it works</p><h2>Two routes, one submission</h2>
  <p class="ise-lead">Choose one of two routes. Both carry equal marks and are worth up to 200 points. Pick the one that lets you best show your skills and interests in science, technology, engineering, maths and innovation.</p></div>
  <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:1.5rem;">
    {S.card("Route A · Technology Project","Up to 800 words on a project where you used technology to do something interesting. Tell us what you did and, just as important, how you did it. Add screenshots, links to repositories or sites, and short explained code fragments, plus the impact of the work and what you would do differently.")}
    {S.card("Route B · Personal Profile","Answer three of four set questions, up to 400 words each, with one optional supporting link per answer. This route suits applicants with or without hands-on software experience and lets you showcase achievements and identity beyond grades.")}
  </div>
</div>''', "ise-band")

es_process=sec(f'''
<div class="ise-container">
  <div style="max-width:56ch;margin-bottom:2rem;"><p class="ise-eyebrow">Who and how</p><h2>Applying and getting access</h2></div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">
    {S.card("Who it is for","CAO (Leaving Certificate), mature and international applicants to Immersive Software Engineering, CAO code LM173.")}
    {S.card("Getting the portal link","Select LM173 on your CAO application and you will be emailed a link to the submission portal. International applicants apply directly to UL and receive the same link.")}
    {S.card("Evidence is welcome","Screenshots, repositories, portfolios, website links and commented code all help, as long as you explain them in your writing.")}
  </div>
</div>''')

es_timeline=sec('''
<div class="ise-container">
  <div style="max-width:56ch;margin-bottom:1.5rem;"><p class="ise-eyebrow">Timeline</p><h2>When you will hear from us</h2></div>
  <div class="ise-faq" style="max-width:820px;">
    <details open><summary>CAO application by 1 February</summary><p>You will be emailed in early to mid March with details of the entrance submission process.</p></details>
    <details><summary>CAO application after 1 February, up to 1 May</summary><p>You will be emailed by mid May with the same details.</p></details>
    <details><summary>CAO Change of Mind up to 1 July</summary><p>If you add LM173 through Change of Mind, you will be emailed by mid July. Dates may differ for international applicants; contact UL Admissions.</p></details>
  </div>
</div>''', "ise-band")

es_cta=section(S.cta("Questions about the submission?",
  "Read the full brief, including the current questions and video guidance, or contact the ISE admissions team.",
  '<a class="ise-btn ise-btn--on-dark" href="https://www.software-engineering.ie/about-the-ise-entrance-submission/" target="_blank" rel="noopener">Entrance submission brief</a>'))

S.assemble(123,"Entrance submission","entrance-submission",[es_hero,es_routes,es_process,es_timeline,es_cta],menu_order=16)

print("team + entrance-submission pages added")
