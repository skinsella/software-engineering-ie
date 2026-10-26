import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import shared as S
from elementor_lib import section

BTN_PARTNER = '<a class="ise-btn ise-btn--primary" href="/become-a-partner">Become a residency partner</a>'
BTN_CALL    = '<a class="ise-btn ise-btn--ghost ise-btn--on-dark" href="https://outlook.office365.com/owa/calendar/ISERPCallBookingPage@ulcampus.onmicrosoft.com/bookings/" target="_blank" rel="noopener">Book a call</a>'

hero = S.hero(
  "The Companies",
  "Work with the best engineers, early",
  "Residencies place ISE students inside your engineering team as paid contributors for three to six months at a time, real work, real impact, with academic mentoring alongside.",
  BTN_PARTNER + ' ' + BTN_CALL,
  max_title="20ch", bg_image="companies-hero.jpg")

wall = section(S.band(f'''
<div class="ise-container">
  <div style="max-width:58ch;margin-bottom:1.5rem;">
    <p class="ise-eyebrow" style="color:#8fe3b0;">Where students reside</p>
    <h2 style="color:#fff;">From global platforms to Ireland's fastest-growing startups</h2>
    <p style="color:#d7e8df;font-size:var(--fs-lead);">ISE partners span fintech, medtech, robotics, quantum and more, the companies students join as paid contributors.</p>
  </div>
  {S.partner_wall()}
</div>''', "ise-band--heritage"))

what = section(S.band(f'''
<div class="ise-container">
  <div style="max-width:54ch;margin-bottom:2.25rem;">
    <p class="ise-eyebrow">What a residency is</p>
    <h2>Not an internship. A contribution.</h2>
    <p class="ise-lead">Students join your team as paid contributors on real work, supported by ISE's academic mentors and a structured learning framework around the placement.</p>
  </div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">
    {S.card("Paid contributors","Students are paid and expected to do real, shippable engineering work, not shadowing.")}
    {S.card("Three to six months","Long enough to onboard, take ownership and deliver, across up to five residencies per student.")}
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
    {S.card("Build your pipeline","Residencies are the strongest possible route to hiring, you have already worked together.")}
    {S.card("Fresh capability","Motivated students bring current skills, energy and new perspectives to your team.")}
  </div>
</div>''', "ise-band"))

# Partner and industry testimonials (same card format as the student testimonials).
# Tuple shape: (quote, name, role, avatar=None).
PARTNER_TESTIMONIALS = [
  ("Software engineering is a wonderful career. Immersive Software Engineering gets students writing code in the real world as quickly as possible, so they're ready to join today's leading companies or start Ireland's next breakout startup.",
   "John Collison", "Entrepreneur, co-founder of Stripe", None),
  ("We gave them something that we thought would take them three months and they finished in three weeks. That was the incredible nature of what they were able to achieve, because of the talent, because of the training they got and because of the immersion in industry.",
   "Mike Morrissey", "Catalyst Director, Analog Devices", None),
  ("Our ISE student was operating at a level that we would expect to see from a graduate, and he had only completed his first year.",
   "Professor Geraldine Boylan", "Director of the Irish Centre for Maternal & Child Health Research, University College Cork", None),
  ("We take ISE students because we see the attitude. They embrace the culture, they embrace the environment. We know that they are great technologists, but it's actually the ability and the trajectory that has completely changed the perception of interns at Intercom.",
   "Oisín Hurley", "Senior Engineering Manager, Intercom", None),
  ("The whole set-up has been second to none. The programme team communication was fantastic, and the students' organisation and ability to deliver is actually far superior to where they should be right now.",
   "Lorraine Curham", "NDRC Head of Operations, Dogpatch Labs", None),
  ("Some of our ISE students have worked on projects that are incredibly critical for us here in J&J, and they have delivered beyond all expectations.",
   "James Walsh", "Senior Software Development Manager, MLL Platforms, at Johnson & Johnson Technology Services", None),
  ("This is exactly what I wanted when I was in college.",
   "Marc Andreessen", "Inventor of the web browser", None),
  ("This is a phenomenal way to learn the skills you need to build the next Instagram.",
   "Mike Krieger", "Co-founder of Instagram", None),
]
voices = S.testimonials("What partners say", "Real-world, hands-on experience",
  items=PARTNER_TESTIMONIALS, klass="")

cta = section(S.cta("Become a residency partner",
  "Tell us about your engineering team and we'll find the right residency fit.",
  '<a class="ise-btn ise-btn--on-dark" href="https://outlook.office365.com/owa/calendar/ISERPCallBookingPage@ulcampus.onmicrosoft.com/bookings/" target="_blank" rel="noopener">Book a call with our team</a>'))

S.assemble(102, "The Companies", "companies", [hero, wall, what, why, voices, cta], menu_order=2)
