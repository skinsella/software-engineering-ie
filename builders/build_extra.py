import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import shared as S
from elementor_lib import section
CALL='<a class="ise-btn ise-btn--ghost ise-btn--on-dark" href="https://outlook.office365.com/owa/calendar/ISERPCallBookingPage@ulcampus.onmicrosoft.com/bookings/" target="_blank" rel="noopener">Book a call</a>'
def sec(inner, klass=""): return section(S.band(inner, klass))

# ===================== GLOBAL FELLOWSHIPS (109) =====================
# NOTE: framing copy, confirm programme specifics with the ISE team before publishing.
fel_hero=S.hero("Global Fellowships","The Global Fellowships Programme",
  "A programme that extends the ISE model beyond Ireland, connecting ambitious students with leading engineering teams internationally.",
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
  "Host ISE students as paid contributors on your engineering team, and meet ambitious talent years before the graduate market does.",
  '<a class="ise-btn ise-btn--primary" href="https://outlook.office365.com/owa/calendar/ISERPCallBookingPage@ulcampus.onmicrosoft.com/bookings/" target="_blank" rel="noopener">Book a call</a> <a class="ise-btn ise-btn--ghost ise-btn--on-dark" href="/companies">How residencies work</a>',
  max_title="18ch")
par_body=sec(f'''
<div class="ise-container">
  <div style="max-width:52ch;margin-bottom:2.25rem;"><p class="ise-eyebrow">Why partner</p><h2>A strong route to great engineers</h2></div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">
    {S.card("Real contribution","Students join your team as paid contributors on real work for three to six months.")}
    {S.card("Fully supported","Academic mentors and a learning framework wrap around every placement.")}
    {S.card("Build your pipeline","Residencies are one of the best ways to hire, because you've already worked together.")}
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
# Content from software-engineering.ie/about-the-ise-entrance-submission/,
# with the timeline graphic recreated in the site's own format.
es_hero=S.hero("Applying","The ISE entrance submission",
  "ISE looks beyond points. Alongside your CAO application you complete an entrance submission, worth up to 200 points, so we can see how you think and build. Please read this page carefully before you begin.",
  S.BTN_APPLY + ' <a class="ise-btn ise-btn--ghost ise-btn--on-dark" href="mailto:ISE@ul.ie">Email ISE@ul.ie</a>', max_title="18ch")

es_intro=sec('''
<div class="ise-container ise-prose" style="max-width:64ch;">
  <p class="ise-eyebrow">Please read carefully</p>
  <h2>Two options, both worth up to 200 points</h2>
  <p>The ISE entrance submission has two options, each worth a maximum of 200 points. It applies to CAO (Leaving Certificate), mature and international applicants to Immersive Software Engineering, CAO code LM173. We are interested in many kinds of students, so show us your skills and interests in science, technology, engineering, maths and innovation, in a way that connects with you.</p>
  <p>Once you select LM173 on the CAO you will receive an email with a link to the submission portal. International applicants apply directly to UL and receive the same link. If you have any questions, email <a href="mailto:ISE@ul.ie">ISE@ul.ie</a>.</p>
</div>''')

# route comparison table (Option A vs Option B)
_cmp = [
  ("Graded questions","One written report","Respond to three of four questions"),
  ("Word limit","Up to 800 words","Up to 400 words per response"),
  ("Question type","Essay","Shorter narrative"),
  ("Main focus","Creative use of technology","Personal characteristics and achievements"),
  ("Evidence","Yes","Yes"),
  ("Points","200","200"),
  ("Submission","Upload a single document to the portal","Enter responses in the portal"),
]
_rows = ''.join(
  f'<tr><td style="padding:.7rem 1rem;border-bottom:1px solid var(--line);font-weight:700;">{lab}</td>'
  f'<td style="padding:.7rem 1rem;border-bottom:1px solid var(--line);color:var(--ink-70);">{a}</td>'
  f'<td style="padding:.7rem 1rem;border-bottom:1px solid var(--line);color:var(--ink-70);">{b}</td></tr>'
  for lab,a,b in _cmp)
_table = (f'<table style="width:100%;border-collapse:collapse;font-size:.95rem;min-width:560px;background:#fff;">'
          f'<thead><tr>'
          f'<th style="text-align:left;padding:.75rem 1rem;border-bottom:2px solid var(--ul-green);"></th>'
          f'<th style="text-align:left;padding:.75rem 1rem;border-bottom:2px solid var(--ul-green);color:var(--ul-green-heritage);">Route A<br>Technology Project</th>'
          f'<th style="text-align:left;padding:.75rem 1rem;border-bottom:2px solid var(--ul-green);color:var(--ul-green-heritage);">Route B<br>Personal Profile</th>'
          f'</tr></thead><tbody>{_rows}</tbody></table>')
es_routes=sec(f'''
<div class="ise-container">
  <div style="max-width:58ch;margin-bottom:2rem;"><p class="ise-eyebrow">Choose one route</p><h2>Two routes, one submission</h2>
  <p class="ise-lead">Choose one of two routes. Both carry equal marks and are worth up to 200 points. Pick the one that lets you best show your skills and interests.</p></div>
  <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:1.5rem;margin-bottom:2rem;">
    {S.card("Route A · Technology Project","Up to 800 words on a project where you used technology to do something interesting. Tell us what you did and how you did it, with evidence.")}
    {S.card("Route B · Personal Profile","Respond to three of four questions, up to 400 words each. A shorter, narrative route that suits applicants with or without hands-on software experience.")}
  </div>
  <div style="overflow-x:auto;border-radius:var(--radius-lg);border:1px solid var(--line);">{_table}</div>
</div>''', "ise-band")

es_steps=sec(f'''
<div class="ise-container">
  <div style="max-width:56ch;margin-bottom:2rem;"><p class="ise-eyebrow">The submission</p><h2>Three steps</h2></div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">
    {S.card("1 · Personal details","Not graded. Your name, email, CAO number if applicable, and mobile number. Use the email from your original CAO or UL application, and give your mobile with the country code in 00 format, not +.")}
    {S.card("2 · Choose your route","Choose Route A or Route B. Both carry equal marks and are worth up to 200 points. Pick the one that best represents you.")}
    {S.card("3 · Final stage and submission","Not graded. Sign an honour pledge that the work is your own and that all sources are acknowledged. Your work can be part of a team project, but the submission must focus on your own contribution. Anything found not to be your own work leads to rejection of the whole submission.")}
  </div>
</div>''')

es_routeA=sec(f'''
<div class="ise-container">
  <div style="max-width:62ch;margin-bottom:2rem;"><p class="ise-eyebrow">Route A guidance</p><h2>The Technology Project</h2>
  <p class="ise-lead">Up to 800 words, submitted as a single document through the portal. Using technology does not have to mean writing a program; it can be any situation where you used technology to do something interesting. We want to know what you did, and just as much, how you did it.</p></div>
  <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:1.5rem;">
    {S.card("Overview of your work","What did you do? Include screenshots, photos and links to repositories, websites or other illustrations. If you wrote code, add short fragments with a brief explanation of what they do, and link to the full implementation.")}
    {S.card("Project impact","Why did you do it? Were you solving a problem or learning something new? What was the impact, and did anyone use it? What are you most proud of, and what would you do differently next time?")}
  </div>
  <div style="margin-top:1.5rem;">{S.card("A few notes","Team projects are fine, but be clear about the parts you did yourself. Leaving Certificate or other coursework projects are allowed if you improve on them and explain how. Always provide and explain your evidence. If you are unsure whether an idea fits, it probably does, but you can email ISE@ul.ie to check.")}</div>
</div>''', "ise-band")

# ---- timeline graphic, recreated in the site's format ----
_tl = [
  ("1","Apply by","1 February","Emailed early to mid March"),
  ("2","After 1 Feb,","up to 1 May","Emailed by mid May"),
  ("3","Change of Mind,","up to 1 July","Emailed by mid July"),
]
_cx = [160, 480, 800]
_svg = ['<svg viewBox="0 0 960 230" role="img" aria-label="Entrance submission timeline: when applicants hear from ISE based on when LM173 is selected on the CAO" style="width:100%;height:auto;max-width:960px;display:block;margin:0 auto;font-family:Inter,sans-serif;">']
_svg.append('<line x1="130" y1="112" x2="830" y2="112" stroke="#cfe0d6" stroke-width="3"></line>')
for _i,(_n,_l1,_l2,_note) in enumerate(_tl):
    _x = _cx[_i]
    _svg.append(f'<rect x="{_x-112}" y="20" width="224" height="64" rx="14" fill="#e8f1ec"></rect>')
    _svg.append(f'<text x="{_x}" y="48" text-anchor="middle" font-size="15" font-weight="700" fill="#0a3f2c">{_l1}</text>')
    _svg.append(f'<text x="{_x}" y="68" text-anchor="middle" font-size="15" font-weight="700" fill="#0a3f2c">{_l2}</text>')
    _svg.append(f'<circle cx="{_x}" cy="112" r="16" fill="#005335"></circle>')
    _svg.append(f'<text x="{_x}" y="117" text-anchor="middle" font-size="14" font-weight="700" fill="#ffffff">{_n}</text>')
    _svg.append(f'<text x="{_x}" y="158" text-anchor="middle" font-size="11" fill="#77857e" letter-spacing=".06em">THEN</text>')
    _svg.append(f'<text x="{_x}" y="180" text-anchor="middle" font-size="13" font-weight="600" fill="#0a6b3b">{_note}</text>')
_svg.append('</svg>')
es_timeline=sec(f'''
<div class="ise-container">
  <div style="max-width:56ch;margin-bottom:1.75rem;"><p class="ise-eyebrow">Timeline</p><h2>When you will hear from us</h2>
  <p class="ise-lead">When you hear from us depends on when you select LM173 on the CAO.</p></div>
  {''.join(_svg)}
  <p style="margin:1.25rem auto 0;max-width:70ch;text-align:center;color:var(--ink-70);">Dates may differ for international applicants; contact UL Admissions for details.</p>
</div>''', "ise-band")

es_additional=sec(f'''
<div class="ise-container">
  <div style="max-width:56ch;margin-bottom:2rem;"><p class="ise-eyebrow">Good to know</p><h2>Before you submit</h2></div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">
    {S.card("You may be invited to talk","You may be called for a short online discussion to clarify parts of your submission. You will hear more when you receive your portal link.")}
    {S.card("Everyone submits","Mature and international applicants complete the submission too. Mature applicants also send a short motivation letter; email ISE@ul.ie for instructions.")}
    {S.card("Watch the workshop","For a full walkthrough, watch the ISE Entrance Submission Workshop on the ISE YouTube channel.")}
  </div>
  <div style="margin-top:1.75rem;"><a class="ise-btn ise-btn--ghost" href="https://www.youtube.com/@immersiveSE" target="_blank" rel="noopener">ISE on YouTube →</a> <a class="ise-btn ise-btn--ghost" href="mailto:ISE@ul.ie">Email ISE@ul.ie</a></div>
</div>''')

_faqs = [
  ("What are the differences between the Technology Project and the Personal Profile?","Route A (Technology Project) is a single written report of up to 800 words focused on creative use of technology. Route B (Personal Profile) asks you to respond to three of four questions, up to 400 words each, as shorter narratives focused on your personal characteristics and achievements. Both carry 200 points and both require evidence. Route B opens the course to students who may not have an extensive technical background."),
  ("Can I gain a place on ISE without completing an entrance submission?","No. All applicants, through the CAO or by direct application to UL, must submit either Route A or Route B."),
  ("What are the minimum requirements aside from the entrance submission?","Full course entry requirements are on the University of Limerick website."),
  ("Can I make changes after I have submitted?","No, changes cannot be made once you send your submission through the portal. Email ISE@ul.ie with any queries."),
  ("I have not received the link to complete my submission. What should I do?","Check your spam or junk folder first. If you still cannot find the email, contact ISE@ul.ie."),
  ("I am a mature student. Do I need to complete an entrance submission?","Yes. Mature students also submit a short motivation letter outlining why they would like a place on ISE. Email ISE@ul.ie for instructions on submitting it."),
  ("I am an international student. Do I need to complete the entrance submission?","Yes. All applicants complete either Route A or Route B."),
  ("Can I choose both Route A and Route B?","No, choose only one. Pick the option that best represents you."),
  ("Is ISE a restricted course?","No. ISE can be selected in each of the three submission windows (normal CAO, late applications and Change of Mind), unlike restricted courses such as Medicine."),
  ("Can I use a Leaving Certificate project?","Yes, if it meets the criteria. Try to make it unique and add something to it, especially if other students may have similar projects."),
  ("Can I use a group project?","Yes, but clearly specify which parts you worked on, as you may be called for an interview to discuss it further."),
]
_faq_html = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in _faqs)
es_faq=sec(f'''
<div class="ise-container">
  <div style="max-width:56ch;margin-bottom:1.5rem;"><p class="ise-eyebrow">FAQ</p><h2>Frequently asked questions</h2></div>
  <div class="ise-faq" style="max-width:820px;">{_faq_html}</div>
</div>''')

es_cta=section(S.cta("Questions about the submission?",
  "Email the ISE admissions team, or apply through the CAO with code LM173.",
  S.BTN_APPLY + ' <a class="ise-btn ise-btn--ghost ise-btn--on-dark" href="mailto:ISE@ul.ie">Email ISE@ul.ie</a>'))

S.assemble(123,"Entrance submission","entrance-submission",
  [es_hero,es_intro,es_routes,es_steps,es_routeA,es_timeline,es_additional,es_faq,es_cta],menu_order=16)

print("team + entrance-submission pages added")
