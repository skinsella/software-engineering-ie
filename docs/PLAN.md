# Plan: Rebuild www.software-engineering.ie (ISE) on WordPress + Elementor, UL-brand-compliant

## Context

`www.software-engineering.ie` is the marketing site for **Immersive Software Engineering (ISE)** at the
University of Limerick — a 4-year combined BSc/MSc where students spend ~45% of their time in paid company
residencies (partners include Stripe, AWS, Intercom, OpenAI, Mastercard, Analog Devices).

The user wants a **new site** that (1) is built on the **same technology as the current site**, (2) is **close
to and brand-compliant with the new UL.ie design**, and (3) is **centred on two quality pillars: the quality of
the students, and the quality of the companies they gain access to**. Scope agreed: **full rebuild** of all
pages. Build location agreed: a **fresh local WordPress**, then hand off an exportable package for the live host.

### Stack detected on the live site (must be reused)
- **WordPress 6.8.1**, **Hello Elementor** theme, **Elementor + Elementor Pro 3.35.3** (page builder)
- Add-ons: Essential Addons for Elementor Lite, The Pack Addon, Addon Elements
- **MailOptin** (forms/opt-ins), Burst Statistics + Google Analytics (MonsterInsights), **Cloudflare** CDN
- => The rebuild is an **Elementor build**, not hand-authored source files. Deliverables are a child theme +
  an Elementor global kit + page templates, assembled visually in the Elementor editor.

### UL brand system (target for compliance)
- **Colours:** UL Green `#005335` (core) · UL Modern Green `#00B140` · UL Heritage Green `#003726`
  (source lists a close core variant `#005844`; use `#005335` as canonical, confirm against the official kit).
- **Type:** Saol (serif) · Inter (sans) · Formula Condensed (display). Free UL-sanctioned fallbacks:
  **Cormorant Garamond · Inter · Roboto Condensed** (all Google Fonts, self-hostable).
- **Positioning voice:** "Become a Changemaker"; clean, institutional, image-led, sans-serif nav, mega-menu.

### Current page inventory (from sitemap — all to be rebuilt)
Home · Why Immersive Software Engineering · What You Need To Know (course) · About the ISE Entrance Submission ·
Careers · Global Fellowships Programme · Become a Residency Partner · Become a Partner Company · €10,000 EDI
Scholarships · FAQ · Schools · About Us · Screens · Privacy Policy.

---

## Approach

### 1. Local environment (Node-only, agent-scriptable)
No Docker/PHP/LocalWP present; Node 26 is. Use **WordPress Playground / `wp-now`** (PHP-WASM, no Docker) as the
local runtime so the build can be driven from the terminal and previewed in the browser tools.
- Scaffold under `ISESIte/` (empty additional working dir):
  `npx @wp-now/wp-now start` (or `npx @wp-playground/cli server --mount ...` for persistence).
- Install **Elementor (free)** from the WP.org repo. **Elementor Pro is a licensed dependency** — the live site
  uses Pro (Theme Builder header/footer, forms, global widgets), so the user must supply the **Elementor Pro
  plugin zip + license key** from their Elementor account to reproduce it faithfully. (Fallback if unavailable:
  build with free Elementor + Essential Addons; note the feature gaps in header/footer/forms.)
- Alternative if the user prefers a GUI / more production-faithful stack: **LocalWP** (real PHP/MySQL, one-click
  export). Documented as the fallback; `wp-now` is primary because it is installable and driveable with only Node.

### 2. Brand foundation — child theme + Elementor Global Kit
- Create **`hello-elementor-child`** theme (`ISESIte/.../wp-content/themes/hello-elementor-child/`) containing:
  - `style.css` + `functions.css` enqueue: self-hosted Google Fonts (Cormorant Garamond, Inter, Roboto
    Condensed) and a **`:root` design-token block** — UL greens, neutrals, spacing, radius, shadows.
  - Brand utility CSS classes used by Elementor sections (buttons, eyebrow labels, stat counters, logo grid).
- Configure **Elementor Site Settings → Global Colors / Global Fonts** to the UL tokens so every widget inherits
  brand values. This is the single source of truth for colour/type across all pages.
- Deliverable form of the brand system: an **Elementor Kit export (.zip)** (Tools → Import/Export Kit) — this
  packages global colours, fonts, theme-style defaults, headers/footers and templates in a **DB-agnostic** way,
  so it imports cleanly onto the live MySQL host regardless of the local SQLite runtime.

### 3. Information architecture, reorganised around the two pillars
Keep all existing pages but restructure the primary nav and homepage narrative around **Students** and
**Companies**:
- **Global header (Elementor Theme Builder):** logo · *Why ISE* · **The Students** · **The Companies** ·
  *Course* · *Apply* (primary button, CAO LM173) · secondary: About, FAQ, News.
- **Two pillar hubs** become the spine of the site:
  - **The Students / Outcomes** (new hub, absorbs quality-of-student proof): admissions selectivity, the
    entrance submission, student calibre, projects, testimonials, where graduates go.
  - **The Companies / Residencies** (rebuild of Partner Companies + Become a Partner): partner logo wall,
    company calibre, what a residency is, outcomes for partners, "Become a residency partner" CTA.

### 4. Homepage design (sections, top → bottom)
Brand-compliant, image-led, mirroring UL.ie's clean institutional layout:
1. **Hero** — full-bleed image, UL-green overlay, display headline on the dual promise
   ("Exceptional students. World-class companies."), primary CTA *Apply (LM173)* + secondary *Book a call*.
2. **The proposition** — one-line "learn by doing" statement + the 45%-in-residency stat.
3. **Pillar A — Quality of students**: stat band (applicant selectivity, cohort size), entrance-submission
   highlight, student voices. Links to Students hub.
4. **Pillar B — Quality of companies**: partner **logo wall** (Stripe, AWS, Intercom, OpenAI, Mastercard,
   Analog Devices…), short partner testimonial (e.g. John Collison quote), link to Companies hub.
5. **How it works** — the 4-year / 5-residency model as a horizontal timeline.
6. **Proof / outcomes** — counters + featured story.
7. **CTA band** — Apply + newsletter (MailOptin) + Book a call with the Residency Team.
8. **Footer (Theme Builder)** — UL-brand footer, nav columns, social, policies.

### 5. Remaining pages (rebuilt on shared section templates)
Why ISE · Course ("What you need to know") · Entrance Submission · Careers · Global Fellowships · Become a
Residency/Partner Company · EDI Scholarships · FAQ (accordion) · Schools · About Us · Privacy. Each assembled
from a small kit of **reusable Elementor section templates** (hero, stat band, logo wall, testimonial, CTA
band, FAQ accordion) so the design stays consistent and fast to build.

### 6. Content
Reuse factual content from the live site (partner list, course facts, testimonials, CAO code, EDI/fellowship
details) via targeted fetches during build; write **fresh hero + pillar framing copy** centred on the two
quality themes. Real partner logos and photography to be supplied by the user (placeholders until then).

### 7. Handoff to the live host
- Export **Elementor Kit (.zip)** + **child theme (.zip)** + **media library**.
- Provide an import runbook: install Hello Elementor + child theme + Elementor Pro on the (staging first) live
  host, import the kit, point the header/footer + homepage, then push live behind Cloudflare.
- Recommend building/importing on **staging** before production; never edit production directly.

---

## Critical files / locations
- `ISESIte/` — local WordPress root (scaffolded).
- `ISESIte/.../wp-content/themes/hello-elementor-child/{style.css,functions.php}` — brand tokens, fonts, utilities.
- Elementor **Site Settings** (Global Colors/Fonts) — brand source of truth.
- Export artefacts: `ISESIte/exports/ise-elementor-kit.zip`, `hello-elementor-child.zip`.

## Reused conventions / assets
- Elementor **Kit Import/Export** for DB-agnostic transport (no full SQLite→MySQL migration needed).
- Existing plugin set on live (Essential Addons, The Pack, MailOptin) reused rather than re-chosen.
- UL free-font fallbacks (Google Fonts) so the site is licence-clean and self-hostable.

## Verification (end-to-end)
1. `wp-now` serves locally; open in the browser preview tools — homepage renders, no console errors.
2. **Brand audit:** computed CSS shows UL greens and the three fonts on headings/body/display; check with the
   browser `javascript_tool` (getComputedStyle) and a screenshot at desktop + mobile (`resize_window`).
3. **Nav/IA:** header links resolve to the two pillar hubs + all rebuilt pages; footer + Theme Builder parts
   present (needs Elementor Pro).
4. **Content pass:** partner logo wall, stats, testimonials, CTAs (Apply LM173, Book a call) present and linked.
5. **Export round-trip:** import the Kit zip into a second clean `wp-now` instance to confirm the package is
   self-contained before handing to the host.
6. Screenshots of homepage + both pillar pages shared with the user as proof.

## Open dependencies to confirm before/at build start
- **Elementor Pro plugin zip + license** (required for header/footer/forms/global — the live site uses it).
- **Brand assets:** official UL colour confirmation (`#005335` vs `#005844`), any licensed Saol/Formula
  Condensed files (else free fallbacks), partner logos, photography.
- Whether to keep MailOptin + Burst/GA analytics as on live (assumed yes).
