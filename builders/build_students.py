import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import shared as S
from elementor_lib import section

hero = S.hero(
  "The Students",
  "A cohort companies compete for",
  "ISE takes a small, highly selective intake each year and teaches them to build. By their first residency, partner engineering teams describe them as performing well beyond their years.",
  S.BTN_APPLY + ' <a class="ise-btn ise-btn--ghost ise-btn--on-dark" href="/companies">Book a call</a>',
  max_title="18ch", bg_image="students-hero.jpg")

selective = section(S.band(f'''
<div class="ise-container">
  <div style="max-width:54ch;margin-bottom:2.5rem;">
    <p class="ise-eyebrow">Selective by design</p>
    <h2>A small intake, chosen for how they build</h2>
    <p class="ise-lead">Places are limited and demand is high. Students are selected for genuine ability and motivation — not points alone — and the cohort is kept deliberately small so every student takes on real responsibility early.</p>
  </div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">
    {S.card("A deliberately small cohort","Small numbers mean real projects, close mentoring and genuine ownership from the first weeks.")}
    {S.card("Chosen on ability","Selected for how candidates actually think and build, and for their drive to make things.")}
    {S.card("Diverse and supported","€10,000 EDI scholarships and a supportive studio culture help widen who gets to take part.")}
  </div>
</div>''', "ise-band" ))

learn = section(S.band(f'''
<div class="ise-container">
  <div style="max-width:54ch;margin-bottom:2.25rem;">
    <p class="ise-eyebrow">How they learn</p>
    <h2>Learning by doing, from week one</h2>
    <p class="ise-lead">No lecture-hall-only terms. Students learn in studios, on real projects, assessed continuously — then spend half the degree in paid company residencies.</p>
  </div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">
    {S.card("Studio-based","Small teams working in a studio, closer to a real engineering floor than a classroom.")}
    {S.card("Project-driven","Every module is anchored in building something real, not just sitting exams.")}
    {S.card("Continuously assessed","Progress is measured through the work itself, week after week.")}
  </div>
</div>'''))

partners_say = section(S.band(f'''
<div class="ise-container" style="display:grid;grid-template-columns:1.1fr 1fr;gap:clamp(2rem,5vw,4rem);align-items:center;">
  <div>
    <p class="ise-eyebrow" style="color:#8fe3b0;">What partners say</p>
    <h2 style="color:#fff;">Beyond their years</h2>
    <p style="color:#d7e8df;font-size:var(--fs-lead);">Residency partners consistently report ISE students contributing like engineers with far more experience — shipping real work inside their teams.</p>
  </div>
  <blockquote style="margin:0;padding:0;border:0;">
    <p class="ise-serif" style="font-size:clamp(1.4rem,2.6vw,2rem);color:#fff;max-width:34ch;margin:0;line-height:1.3;">“Software engineering is a wonderful career.”</p>
    <footer style="font-family:var(--font-sans);font-size:1rem;color:#8fe3b0;margin-top:.85rem;">John Collison · co-founder, Stripe</footer>
  </blockquote>
</div>''', "ise-band--heritage"))

where = section(S.band(f'''
<div class="ise-container">
  <div style="max-width:54ch;margin-bottom:2.25rem;">
    <p class="ise-eyebrow">Where they go</p>
    <h2>Two degrees, and a head start</h2>
    <p class="ise-lead">In four years students complete an integrated BSc and MSc — graduating with a master's, a portfolio of real work, and a network built across multiple residencies.</p>
  </div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;">
    <div>{S.stat("4 yrs","to an integrated master's")}</div>
    <div>{S.stat("5","company residencies")}</div>
    <div>{S.stat("50%","of the degree in industry")}</div>
  </div>
  <div style="margin-top:2rem;"><a class="ise-btn ise-btn--ghost" href="/careers">Explore graduate paths →</a></div>
</div>''', "ise-band"))

cta = section(S.cta("Think you could be one of them?",
  "Applications for 2026 are open through the CAO with code LM173.",
  '<a class="ise-btn ise-btn--on-dark" href="/apply">Apply — LM173</a> <a class="ise-btn ise-btn--ghost ise-btn--on-dark" href="/companies">Talk to us</a>'))

cohort = S.portrait_cards("Meet the cohort", "Real students, real projects",
  [("cohort-1.jpg", "Built from day one", "Studio to residency"),
   ("cohort-2.jpg", "Selected on substance", "Chosen for how they build"),
   ("cohort-3.jpg", "Ready for industry", "Beyond their years")], klass="")

S.assemble(101, "The Students", "students", [hero, selective, cohort, learn, partners_say, where, cta], menu_order=1)
