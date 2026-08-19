import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import shared as S
from elementor_lib import section

BTN_PARTNER = '<a class="ise-btn ise-btn--primary" href="/apply">Become a residency partner</a>'
BTN_CALL    = '<a class="ise-btn ise-btn--ghost ise-btn--on-dark" href="/apply">Book a call</a>'

hero = S.hero(
  "The Companies",
  "Work with the best engineers, early",
  "Residencies place ISE students inside your engineering team as paid contributors for three to six months at a time — real work, real impact, with academic mentoring alongside.",
  BTN_PARTNER + ' ' + BTN_CALL,
  max_title="20ch", bg_image="companies-hero.jpg")

wall = section(S.band(f'''
<div class="ise-container">
  <div style="max-width:58ch;margin-bottom:1.5rem;">
    <p class="ise-eyebrow" style="color:#8fe3b0;">Where students reside</p>
    <h2 style="color:#fff;">From global platforms to Ireland's fastest-growing startups</h2>
    <p style="color:#d7e8df;font-size:var(--fs-lead);">ISE partners span fintech, medtech, robotics, quantum and more — the companies students join as paid contributors.</p>
  </div>
  {S.partner_wall()}
</div>''', "ise-band--heritage"))

what = section(S.band(f'''
<div class="ise-container">
  <div style="max-width:54ch;margin-bottom:2.25rem;">
    <p class="ise-eyebrow">What a residency is</p>
    <h2>Not an internship. A contribution.</h2>
    <p class="ise-lead">Students join your team as paid contributors on real work — supported by ISE's academic mentors and a structured learning framework around the placement.</p>
  </div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">
    {S.card("Paid contributors","Students are paid and expected to do real, shippable engineering work — not shadowing.")}
    {S.card("Three to six months","Long enough to onboard, take ownership and deliver — across up to five residencies per student.")}
    {S.card("Fully supported","Academic mentors and a learning framework wrap around every placement, sharing the load with your team.")}
  </div>
</div>'''))

why = section(S.band(f'''
<div class="ise-container">
  <div style="max-width:54ch;margin-bottom:2.25rem;">
    <p class="ise-eyebrow">Why partner with ISE</p>
    <h2>Meet exceptional engineers before anyone else</h2>
  </div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">
    {S.card("Access talent early","Work with a highly selective cohort years before they reach the graduate market.")}
    {S.card("Build your pipeline","Residencies are the strongest possible route to hiring — you have already worked together.")}
    {S.card("Fresh capability","Motivated students bring current skills, energy and new perspectives to your team.")}
  </div>
  <blockquote style="margin:2.5rem 0 0;padding:0;border:0;">
    <p class="ise-serif" style="font-size:clamp(1.3rem,2.4vw,1.9rem);color:var(--ul-green-heritage);max-width:40ch;margin:0;line-height:1.3;">“Software engineering is a wonderful career.”</p>
    <footer style="font-family:var(--font-sans);font-size:1rem;color:var(--ink-70);margin-top:.75rem;">John Collison · co-founder, Stripe</footer>
  </blockquote>
</div>''', "ise-band"))

cta = section(S.cta("Become a residency partner",
  "Tell us about your engineering team and we'll find the right residency fit.",
  '<a class="ise-btn ise-btn--on-dark" href="/apply">Book a call with our team</a>'))

S.assemble(102, "The Companies", "companies", [hero, wall, what, why, cta], menu_order=2)
