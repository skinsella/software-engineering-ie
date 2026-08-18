import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import shared as S
from elementor_lib import section
CALL='<a class="ise-btn ise-btn--ghost ise-btn--on-dark" href="/apply">Book a call</a>'
def sec(inner, klass=""): return section(S.band(inner, klass))

# ===================== GLOBAL FELLOWSHIPS (109) =====================
# NOTE: framing copy — confirm programme specifics with the ISE team before publishing.
fel_hero=S.hero("Global Fellowships","The Global Fellowships Programme",
  "A programme that extends the ISE model beyond Ireland — connecting exceptional students with leading engineering teams internationally.",
  S.BTN_APPLY+' '+CALL, max_title="18ch")
fel_body=sec(f'''
<div class="ise-container">
  <div style="max-width:52ch;margin-bottom:2.25rem;"><p class="ise-eyebrow">Overview</p><h2>Global reach, the same immersive model</h2></div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">
    {S.card("International residencies","Opportunities to reside with partner engineering teams beyond Ireland.")}
    {S.card("A global network","Build relationships with companies and mentors across borders.")}
    {S.card("The ISE approach","The same learn-by-doing model, applied on an international stage.")}
  </div>
  <p class="ise-lead" style="margin-top:1.75rem;max-width:60ch;">Programme details are being confirmed — talk to the team to find out more.</p>
</div>''', "ise-band")
fel_cta=section(S.cta("Interested in the Fellowships?","Get in touch to learn more about international opportunities.",
  '<a class="ise-btn ise-btn--on-dark" href="/apply">Book a call</a>'))
S.assemble(109,"Global Fellowships","global-fellowships",[fel_hero,fel_body,fel_cta],menu_order=10)

# ===================== EDI SCHOLARSHIPS (110) =====================
edi_hero=S.hero("Scholarships","€10,000 EDI Scholarships",
  "Equity, Diversity & Inclusion scholarships help widen who gets to take part in ISE — supporting talented students from under-represented backgrounds.",
  '<a class="ise-btn ise-btn--primary" href="/apply">How to apply</a> '+CALL, max_title="16ch")
edi_body=sec(f'''
<div class="ise-container">
  <div style="max-width:52ch;margin-bottom:2rem;"><p class="ise-eyebrow">The scholarships</p><h2>Support to help you take part</h2></div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">
    <div>{S.stat("€10k","per scholarship")}</div>
    <div>{S.stat("Each year","new awards")}</div>
    <div>{S.stat("EDI","widening participation")}</div>
  </div>
  <p class="ise-lead" style="margin-top:1.75rem;max-width:62ch;">Scholarships are awarded to help talented students from under-represented backgrounds join ISE. Eligibility and application details are confirmed each year — ask us if you think you may be eligible.</p>
</div>''', "ise-band")
edi_cta=section(S.cta("Apply for ISE","Add CAO code LM173 to your application, and talk to us about EDI support.",
  '<a class="ise-btn ise-btn--on-dark" href="/apply">Apply — LM173</a> '+CALL))
S.assemble(110,"EDI Scholarships","edi-scholarships",[edi_hero,edi_body,edi_cta],menu_order=11)

# ===================== SCHOOLS (111) =====================
sch_hero=S.hero("For Schools","Guidance counsellors & teachers",
  "Everything you need to tell students about Immersive Software Engineering — a new route into a software career through the University of Limerick.",
  '<a class="ise-btn ise-btn--primary" href="/apply">Book a school talk</a> '+CALL, max_title="18ch")
sch_body=sec(f'''
<div class="ise-container">
  <div style="max-width:52ch;margin-bottom:2.25rem;"><p class="ise-eyebrow">For schools</p><h2>Help your students find ISE</h2></div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">
    {S.card("What ISE is","A four-year integrated BSc + MSc where students learn by doing, in studios and paid company residencies. CAO code LM173.")}
    {S.card("Who it suits","Curious, motivated students who like building things — not only those with the highest points.")}
    {S.card("Book a talk","We're happy to speak with your students, in person or online, about the programme and how to apply.")}
  </div>
</div>''', "ise-band")
sch_cta=section(S.cta("Invite us to your school","Get in touch to arrange a talk or request materials.",
  '<a class="ise-btn ise-btn--on-dark" href="/apply">Book a school talk</a>'))
S.assemble(111,"For Schools","schools",[sch_hero,sch_body,sch_cta],menu_order=12)

# ===================== BECOME A PARTNER (112) =====================
par_hero=S.hero("Partner with ISE","Become a residency partner",
  "Host ISE students as paid contributors on your engineering team, and meet exceptional talent years before the graduate market does.",
  '<a class="ise-btn ise-btn--primary" href="/apply">Book a call</a> <a class="ise-btn ise-btn--ghost ise-btn--on-dark" href="/companies">How residencies work</a>',
  max_title="18ch")
par_body=sec(f'''
<div class="ise-container">
  <div style="max-width:52ch;margin-bottom:2.25rem;"><p class="ise-eyebrow">Why partner</p><h2>The strongest route to great engineers</h2></div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">
    {S.card("Real contribution","Students join your team as paid contributors on real work for three to six months.")}
    {S.card("Fully supported","Academic mentors and a learning framework wrap around every placement.")}
    {S.card("Build your pipeline","Residencies are the strongest possible route to hiring — you've already worked together.")}
  </div>
</div>''', "ise-band")
par_wall=sec(f'''
<div class="ise-container">
  <div style="max-width:56ch;margin-bottom:1.5rem;"><p class="ise-eyebrow" style="color:#8fe3b0;">In good company</p><h2 style="color:#fff;">Join our network of partners</h2></div>
  {S.partner_wall()}
</div>''', "ise-band--heritage")
par_cta=section(S.cta("Talk to our residency team","Tell us about your team and we'll find the right fit.",
  '<a class="ise-btn ise-btn--on-dark" href="/apply">Book a call</a>'))
S.assemble(112,"Become a partner","become-a-partner",[par_hero,par_body,par_wall,par_cta],menu_order=13)

# ===================== PRIVACY (113) =====================
# NOTE: placeholder — replace with the approved UL/ISE privacy notice before publishing.
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
