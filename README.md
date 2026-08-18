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
- [ ] Student & Company pillar hub pages
- [ ] Remaining pages (Why ISE, Course, Apply, Careers, Fellowships, Partner,
      EDI, FAQ, Schools, About)
- [ ] Global header/footer via Elementor Pro Theme Builder
- [ ] Export as an Elementor kit for the production host

## Stack
- **WordPress** + **Elementor** (production also uses Elementor **Pro**)
- Theme: **Hello Elementor** + `hello-elementor-child` (this repo)
- Local runtime: **wp-now** / WordPress Playground (PHP-WASM via Node — no Docker)

## Repository layout
```
theme-src/hello-elementor-child/   Brand child theme (design tokens, fonts, assets, logos)
builders/                          Python scripts that author Elementor pages as data
  elementor_lib.py                 Helpers: build sections, upsert pages into the WP DB
  build_home.py                    Homepage definition (content + layout)
  build_preview.py                 Emits a standalone HTML snapshot of the homepage
design/home_preview.html           Standalone homepage snapshot (regenerated)
docs/PLAN.md                       The approved build plan
```

## Run it locally
Requires **Node** (no Docker/PHP needed).

```bash
# 1) Start a local WordPress (downloads WP + PHP-WASM on first run)
npx @wp-now/wp-now start --port 8881      # serves http://localhost:8881

# 2) Install into the wp-now content dir (~/.wp-now/wp-content/playground)
#    - Hello Elementor theme + Elementor plugin (from wordpress.org)
#    - copy theme-src/hello-elementor-child into themes/
#    See docs/PLAN.md for the exact steps; a bootstrap script will follow.

# 3) Build/refresh the pages
python3 builders/build_home.py            # writes the homepage into the WP DB
python3 builders/build_preview.py         # regenerates design/home_preview.html
```

> Note: `@wp-now/wp-now` is deprecated upstream in favour of
> `@wp-playground/cli`; either works for local preview.

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
