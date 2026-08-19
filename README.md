# software-engineering.ie — new site

A rebuild of the **Immersive Software Engineering (ISE)** website (University of
Limerick) — brand-aligned to the current UL identity and centred on two pillars:
the **quality of the students** and the **quality of the companies** they gain
access to through paid residencies.

Built on the **same stack as the production site**: WordPress + Elementor, using a
`hello-elementor` child theme for the brand system.

## Status
Work in progress.
- [x] Local WordPress build environment (Node-only, no Docker)
- [x] UL-brand child theme (design tokens, fonts, utility classes)
- [x] Homepage — hero, proposition, **The Students**, **The Companies**
      (full 33-logo partner wall), how-it-works, CTA, footer
- [x] Real ISE·UL logo + genuine partner logos wired in
- [x] Student & Company pillar hub pages
- [x] Core pages: Apply, Course, Why ISE, About, FAQ, Careers
- [x] Remaining pages: Fellowships, EDI scholarships, Schools, Partner sign-up, Privacy
- [x] Elementor template exports + child-theme zip + handoff runbook
- [x] Residency Job Board plugin (partner login + moderated job uploads)
- [ ] Global header/footer via Elementor Pro Theme Builder (production step — see docs/HANDOFF.md)
- [x] Export as importable Elementor templates for the production host

## Stack
- **WordPress** + **Elementor** (production also uses Elementor **Pro**)
- Theme: **Hello Elementor** + `hello-elementor-child` (this repo)
- Local runtime: **wp-now** / WordPress Playground (PHP-WASM via Node — no Docker)

## Repository layout
```
theme-src/hello-elementor-child/   Brand child theme (design tokens, fonts, assets, logos)
builders/                          Python scripts that author Elementor pages as data
  elementor_lib.py                 Helpers: build sections, upsert pages into the WP DB
  shared.py                        Nav, footer, brand helpers, partner wall, page assembly
  build_home.py                    Homepage
  build_students.py                The Students hub
  build_companies.py               The Companies hub
  build_all.py                     Build every page + snapshot
  build_preview.py                 Emits a standalone HTML snapshot of the homepage
design/home_preview.html           Standalone homepage snapshot (regenerated)
plugin-src/ise-residency-board/     Custom plugin: Residency Job Board (CPT + gated submit)
builders/export_kit.py             Emits importable Elementor template JSON per page
exports/elementor-templates/       Per-page Elementor templates + manifest.json
docs/PLAN.md                       The approved build plan
docs/HANDOFF.md                    Production import runbook
```

## Run it locally
Requires **Node** (no Docker/PHP needed).

```bash
# Terminal 1 — start a local WordPress (downloads WP + PHP-WASM on first run)
npx @wp-now/wp-now start --port 8881        # serves http://localhost:8881

# Terminal 2 — install theme/plugins, activate, set options, build all pages
bash scripts/setup_local.sh                  # idempotent; safe to re-run
```

Rebuild pages after editing a builder:

```bash
python3 builders/build_all.py                # all pages + design/home_preview.html
```

> `@wp-now/wp-now` is deprecated upstream in favour of `@wp-playground/cli`;
> either works for local preview.

## Brand system (UL)
- **Colours:** UL Green `#005335` · UL Modern Green `#00B140` · UL Heritage Green `#003726`
  (confirm the exact core green against the official UL brand kit).
- **Type:** licence-clean UL fallbacks — Roboto Condensed (display), Inter (body),
  Cormorant Garamond (serif accents). Exact brand faces (Saol / Formula Condensed)
  are licensed and can be swapped in.
- Tokens live in `theme-src/hello-elementor-child/style.css` (`:root`), mirrored
  into Elementor Site Settings for the production build.

## Assets & attribution
The ISE·UL logo lockup and partner logos are sourced from the existing
software-engineering.ie site (the project's own assets). Partner marks are the
trademarks of their respective owners and are used to represent residency
partners; confirm display permissions before publishing externally.
