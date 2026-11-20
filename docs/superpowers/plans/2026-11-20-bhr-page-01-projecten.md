# BHR /projecten Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for native execution, or superpowers:subagent-driven-development if explicitly selected. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make local `/projecten` match its live equivalent, with independent visual acceptance.
**Architecture:** Opt in this exact route through the shared secondary manifest; use the `project-listing` composition and route-scoped styles. Preserve old default consumers.
**Tech Stack:** Node.js >=20, ES modules, static HTML/CSS, vanilla JavaScript, Python/Playwright visual-diff.
**Spec:** [Remaining-pages design](../specs/2026-11-20-bhr-remaining-pages-design.md) · **Prerequisite:** [Shared foundations](2026-11-20-bhr-remaining-00-shared.md)

## Global Constraints

- Node.js >=20; no new application runtime dependencies; author HTML/CSS/JS and package original media locally.
- Preserve Dutch copy and the 12 protected route hashes. No global theme/data-array edits or screenshot-backed page content.
- 1920×1080 primary; 1440×900, 768×1024, 390×844 regression views; DPR 1, zoom 1, light, nl-NL, Europe/Amsterdam.
- No real submissions; existing delivery names/subjects, initially unchecked consent, combined 4 MB uploads. Newsletter/test forms are local-only.
- Strict acceptance per width: mismatch ≤0.5%, SSIM estimate ≥0.985, height delta ≤2px. No averages or invented Craft scores.
- No Git currently exists: record a local checkpoint and ledger instead of inventing a commit.

## Review Focus

1. Long/emphasized “Projecten waar we trots op zijn” text must retain source wrapping at all four widths.
2. Exact source photo derivatives and original media must load; a same-photo fallback is not an acceptable substitution.
3. The full heading/section/FAQ inventory must remain ordered, including content below the first screen.
4. Select each visible radio category, assert URL filter_projectgroup[]=1/2 and exactly four matching rows, synchronize the sticky copy, restore all eight on reset/back, then exercise each gallery’s thumbnail and bounded first/last controls. Keep Integratie hidden in the default view and test an explicit empty-result state without fabricating project cards.
5. The new route must retain usable links/validation without changing any protected consumer or sending a live request.

---

## Observed baseline and source requirements

Current owner: `app/inner-pages.mjs:projectListing()`.
Replace the pale title and two-column card grid with the dark striped title area, category controls and eight horizontal image/text rows. At 1920px each main photo is 760×559.23 at x=200, while the first text column starts at x=1120 with width 600. Preserve category headings, full card copy and all eight detail links. Four rows have multi-image galleries; retain the source eight-slot thumbnail sizing, rather than stretching five thumbnails to fill the row. Render the observed sticky filter only as a scrolled control, not repeated body bands.

At 1920px the source H1 is `Projecten waar we trots op zijn`: 65px/57.2px, box x=200.00, y=208.67, 620.00×114.38. Use these as measurements, not blank spacer dimensions.
The current local H1 is `Projecten waar we trots op zijn` at 50px; its structure/photo/section geometry is visible in the linked comparison.

| Baseline viewport | Mismatch | SSIM estimate | Reference / local full image |
|---|---:|---:|---|
| wide | 76.334% | -0.1442 | 1920×8982 / 1920×6278 |
| desktop | 79.166% | -0.1559 | 1440×8024 / 1440×5932 |
| tablet | 78.129% | -0.2279 | 768×7395 / 768×5567 |
| mobile | 72.602% | -0.1883 | 390×12611 / 390×8050 |

[Full reference/candidate report or source evidence](../../../checks/visual-planning-2026-11-20/baseline/projecten/report.html)
 · [Measured inventory](../../../checks/visual-planning-2026-11-20/baseline/projecten/wide-reference-inventory.json)
 · [Text/media/link inventory](../../../checks/visual-planning-2026-11-20/baseline/projecten/wide-reference-content.json)

**Exact content/asset fixture:** this route’s entry in [expected-pages.json](../../../checks/visual-planning-2026-11-20/expected-pages.json). Its full source heading sequence, every original image filename, resolved action targets, FAQ pairs and CMS validation designations are binding. Do not copy the saved HTML into app code.

**Ordered own content blocks:**
1. Bierskid besturing zonder PLC
2. Seal automatisering
3. Bouwen DAF installatie waterzuivering
4. Energiebesparing door frequentieregelaars
5. Bouwen afdelingsinstallatie
6. Cummins
7. Retrofit oplossingen in bestaande machineframe
8. Verdelerbouw 630A
9. Van technisch innovatie naar concrete oplossingen
10. Wat kunnen wij voor jouw proces betekenen?

**Source image filenames (exact derivatives):** `1125_bierskid.webp`, `566_nieuwe-map-slimme-automatisering.webp`, `570_dsc01712.webp`, `532_nieuwe-map-energiebesparing-door-frequentieregelaars-4.webp`, `533_nieuwe-map-energiebesparing-door-frequentieregelaars-5.webp`, `534_nieuwe-map-energiebesparing-door-frequentieregelaars-6.webp`, `530_nieuwe-map-energiebesparing-door-frequentieregelaars-2.webp`, `531_nieuwe-map-energiebesparing-door-frequentieregelaars-3.webp`, `1103_20190805-100136.webp`, `1102_20190805-100104.webp`, `1104_20190805-100241.webp`, `508_nieuwe-map-bouwen-afdelingsinstallatie-4.webp`, `509_nieuwe-map-bouwen-afdelingsinstallatie-5.webp`, `510_nieuwe-map-bouwen-afdelingsinstallatie-6.webp`, `511_nieuwe-map-bouwen-afdelingsinstallatie-7.webp`, `578_dsc02289.webp`, `413_dsc02888.webp`, `582_dsc01013.webp`, `544_nieuwe-map-kleine-verdelerbouw-tot-630-a-2.webp`, `545_nieuwe-map-kleine-verdelerbouw-tot-630-a.webp`.

**Source fields:** Automatisering; Integratie; Paneelbouw; Automatisering; Integratie; Paneelbouw. Use semantic CMS requiredness, not a false native required boolean. Keep exact option inventories from the fixture.

**Linked-route prerequisites:** `/privacy`.

## Task 1: Source composition, exact assets and route ownership

**Files:** `app/secondary-content.json`, `app/secondary-data.mjs`, `app/secondary-projects.mjs`, `app/secondary-components.mjs`, `app/assets-manifest.json`, `app/public/assets/images/`; test `app/tests/secondary-pages.test.mjs` and its source fixture.
**Interfaces:** Consume `secondaryContent["/projecten"]` and the shared renderer/strict-media interfaces. Produce one authored `project-listing` entry and generated `/projecten/index.html`; no duplicate route emitter.

- [ ] Add the frozen `/projecten` expectation and test `/projecten source composition`: `const html=readBody("/projecten"); assertInOrder(plainText(html),expected.headings); for(const src of expected.images) assert.ok(html.includes(src));` Assert the exact H1 “Projecten waar we trots op zijn”, resolved destinations, expected FAQ count and no unrelated generic section.
- [ ] Run `npm --prefix app run build && node --test --test-name-pattern="/projecten source composition" app/tests/secondary-pages.test.mjs`; expect FAIL for the old composition/media or ENOENT for the missing route.
- [ ] Author the route’s complete source data and `project-listing` body in its designated renderer; package every missing exact media URL with bytes/SHA-256 and an exact manifest key. Opt this route in through `secondaryOptions`; preserve requested URL, metadata and observed header variant.
- [ ] Rebuild and rerun the targeted test; expect PASS for all frozen headings/assets/links and this route’s actual content. Record a local source checkpoint.

## Task 2: Measured layout and observed behavior

**Files:** `app/public/secondary-parity.css`, the designated family renderer, `app/secondary-forms.mjs` where this page has a form, `app/public/secondary.mjs` only for new controls; test `app/tools/check-secondary-browser.py` and meaningful pure behavior cases.
**Interfaces:** Use `.secondary-parity.secondary-route-projecten` and the spec’s delivery/behavior contracts; do not change old global selectors.

- [ ] Capture any planning-unaudited widths and add the route-specific browser regression before its behavior implementation; verify that it fails against the old/missing controls. Use screenshot/box evidence for CSS rather than tests that mirror style declarations.
- [ ] Match the measured header, H1/emphasis, photo crop, source section surfaces, text widths, clipped corners, controls, form/card geometry and footer. Follow this page’s reference composition; do not impose a generic clean mobile stack or pad to the target document height.
- [ ] Implement and check: Select each visible radio category, assert URL filter_projectgroup[]=1/2 and exactly four matching rows, synchronize the sticky copy, restore all eight on reset/back, then exercise each gallery’s thumbnail and bounded first/last controls. Keep Integratie hidden in the default view and test an explicit empty-result state without fabricating project cards.
- [ ] Run `/tmp/bhr-visual-diff-venv/bin/python app/tools/check-secondary-browser.py --route /projecten` with delivery blocked; expect its keyboard/state/validation assertions to pass and zero real submission requests. Run the complete unit suite after any behavior change.

## Task 3: Four-width page review and release gate

- [ ] Complete the listed route prerequisites (or the ten-location batch), then run `npm --prefix app run build`, `npm --prefix app test` and `npm --prefix app run verify`; expect all functional/asset/link checks and the 12 protected hashes to pass.
- [ ] From the workspace root run `/tmp/bhr-visual-diff-venv/bin/python checks/visual-planning-2026-11-20/run-comparisons.py --route projecten --all-widths --out checks/visual-review-remaining-<run-id>`; expect four valid matched-zoom captures. Preserve the planning baseline.
- [ ] Open every width’s side-by-side, heatmap and overlay, and native crops of the title, photos, key control/form, section boundaries and footer. Compare actual boxes/fonts and document height. Review applicable expanded, selected, hover/focus and error views; scrolled sticky controls require separate viewport captures.
- [ ] Record each result separately. Require mismatch ≤0.5%, SSIM estimate ≥0.985 and height delta ≤2px at every width for strict acceptance; leave this page open if any fail. Never certify a missing candidate, unaudited state, averaged score or Craft score as a visual-diff pass.
- [ ] Record the source checkpoint, commands, browser results, individual metrics and any intentional difference in the execution ledger. No deployment or real delivery belongs to this page’s completion gate.

## Exact gallery cardinality

The frozen `projectGalleries` fixture requires 8 rows, with original slide counts **1, 1, 1, 5, 7, 1, 2, 2** in listing order. The four multi-image rows expose thumbnails/controls; single-image rows do not. Count originals, not Tiny Slider clones. The five-image gallery was observed bounded at its final index after repeated Next presses; use the shared clamped index helper.
