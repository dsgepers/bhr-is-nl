# Proces en productie Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for native implementation, or superpowers:subagent-driven-development if the user selects delegation. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reproduce the process/production hero, three specific articles, mid-page CTA and personal contact form.

**Architecture:** Use the shared opt-in parity primitives and preserve the existing exported page renderer. Apply page-specific structure, assets and responsive rules rather than global overrides.

**Tech Stack:** Node.js >=20, ES modules, generated HTML, custom CSS, browser JavaScript, Python/Playwright visual-diff tooling.

**Spec:** [../specs/2026-11-19-bhr-visual-parity-design.md](../specs/2026-11-19-bhr-visual-parity-design.md)

## Global Constraints

All exact constraints and capture settings in the spec apply. Keep the existing dependency-free application, edit source rather than `dist`, package original assets locally, preserve Dutch copy and functioning controls, scope CSS to reviewed routes, and preserve the baseline captures.

## Review Focus

1. Long Dutch headings and emphasis must wrap as on the reference at all three widths.
2. Every visible photo must use the correct source/crop, with fonts and images fully loaded.
3. Section order and full document height must match, including content below the first screen.
4. Initial, hover/focus and expanded interactive states must remain usable and match the reference.
5. Shared changes must not alter the homepage or unrelated routes without explicit review.

---

## Baseline evidence

Reference: `https://www.bhr-is.nl/voor-machinebouwers/proces-productie`. Candidate: `http://127.0.0.1:4173/voor-machinebouwers/proces-productie`.

Artifacts: [report](../../../checks/visual-planning-2026-11-19/proces-productie/report.md), [screenshots and DOM/content inventories](../../../checks/visual-planning-2026-11-19/proces-productie/).

Widths: desktop 1440x900, tablet 768x1024, mobile 390x844, DPR 1. Cookie consent dismissed; no content masks. Full page height is retained; repeated sticky headers are suppressed after the first viewport. See the spec for capture limitations and carousel variance.

| Viewport | Reference size | Local size | Pixel mismatch | SSIM estimate |
| --- | --- | --- | ---: | ---: |
| desktop | 1440×5956 | 1440×6155 | 82.83% | 0.4431 |
| tablet | 768×8483 | 768×7473 | 84.78% | -0.1826 |
| mobile | 390×14008 | 390×8265 | 79.58% | 0.0195 |

These are diagnostic mismatch measurements, not a percentage of likeness. Cumulative vertical offsets can make pixel mismatch very high.

**Dependency:** Complete [2026-11-19-bhr-00-shared-primitives.md](2026-11-19-bhr-00-shared-primitives.md) first.

### Confirmed differences

The current page already places the CTA before the final partner article, but its hero is split into an image and separate intro, the article photographs are substituted, the title wraps differently and the contact heading is replaced with “Neem contact met ons op”. The live contact heading is “Wij helpen u graag verder”. Structure must retain the mid-page CTA while correcting appearance and exact imagery.

### Task 1: Correct hero, original photographs and article layout

**Files:** `app/data.mjs`, `app/page-content.json` if independently verified copy differs, `app/reference/image-map.json`, `app/assets-manifest.json`, `app/inner-pages.mjs:standardPage`, `app/public/parity.css`, `app/tests/inner-pages.test.mjs`.

**Interfaces:** Keep `standardPage(page) -> string` and the observed three-article data. Add page-specific image mappings instead of changing global photo fallbacks.

- [x] Strengthen the existing process-page test using live evidence: first two articles, CTA, final partner article, then a single “Wij helpen u graag verder” contact section. Confirm the current forced contact-heading replacement fails this expectation.
- [x] Package the exact `848_dsc01159.webp` hero and render its overlay title, lead copy, “Offerte aanvraag” and “Praat met een expert” actions. Preserve working local destinations while matching their reference presentation.
- [x] Use exact article photographs `771_dsc01350.webp`, `773_dsc02153.webp`, `769_dsc02091.webp`; these are not interchangeable with the current generic process/production photos.
- [x] Restore the dark “Voor proces & productie” introduction band below the hero, with its two-column title/lead composition. Match article direction, clipped image corners, bullet treatment, paragraph widths and spacing. Keep the introductory lead exactly once and keep the CTA after the second article, before “BHR Industrial Solutions: partner voor uw proces en productiviteit”.
- [x] Build, run the structure test and inspect those three article boundaries at all widths.

### Task 2: Restore contact composition and review all states

**Files:** `app/inner-pages.mjs:standardPage`, `app/components.mjs:contactForm`, `app/public/parity.css`.

- [x] Remove the page's string replacement that forces “Neem contact met ons op”. Render “Wij helpen u graag verder” with the captured compact 100×100 circular portrait/contact panel, background and bordered white form card (the surrounding section is white on this route).
- [x] Match fields, labels, required indicators, privacy/terms controls and submit button from the reference form inventory. Keep configured Static Forms behavior and existing local validation.
- [x] Review CTA buttons, article lightbox/focus treatment and invalid/unconfigured form states without sending real requests.
- [x] Run functional checks and route-specific visual review. Inspect the hero, both CTA boundaries, final partner article, form and footer at each width. Ensure content is neither duplicated nor pushed into artificial blank spacers.

## Per-page review and completion

- [x] From `app`, run `npm run build`, `npm test` and `npm run verify`; all must pass.
- [x] From the workspace root, with `app/dist` served on port 4173, run `python checks/visual-planning-2026-11-19/run-comparisons.py --route proces-productie --out checks/visual-review-proces-productie-<run-id>`.
- [x] Open every width's side-by-side, heatmap and overlay with the visual-diff skill. Review header, hero, each section transition, form and footer. Compare heading boxes, photo crops and page height with the DOM audits; do not rely on metrics alone.
- [ ] Match interactive states and stabilize moving regions before applying the spec's <=0.5% mismatch / >=0.985 SSIM targets. Keep raw unmasked evidence and record any remaining difference explicitly.
- [ ] Review the five failure modes in Review Focus, recheck the homepage and affected shared-template consumers, and record the page's individual result. A failure at one width leaves this page incomplete.
- [x] Record a local checkpoint; commit only if a Git repository has subsequently been initialized.

## Execution record

Implemented and functionally verified; final visual acceptance is tracked separately. The user selected **1920×1080** as primary, with 1440×900, 768×1024 and 390×844 retained. The normalized implementation capture helper supersedes the original planning command so both origins use native viewport tiles and the same settled carousel state.

See the [execution ledger](../execution/2026-11-19-progress.md) for architectural rulings and the [final comparison report](../../../checks/visual-implementation-2026-11-19/review/README.md) for individual results and remaining strict-target failures. Checked implementation/review steps do not declare an open numeric gate passed.
