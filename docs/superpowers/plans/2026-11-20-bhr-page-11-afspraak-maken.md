# BHR /afspraak-maken Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for native execution, or superpowers:subagent-driven-development if explicitly selected. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make local `/afspraak-maken` match its live equivalent, with independent visual acceptance.
**Architecture:** Opt in this exact route through the shared secondary manifest; use the `appointment` composition and route-scoped styles. Preserve old default consumers.
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

1. Long/emphasized “Maak een afspraak” text must retain source wrapping at all four widths.
2. Exact source photo derivatives and original media must load; a same-photo fallback is not an acceptable substitution.
3. The full heading/section/FAQ inventory must remain ordered, including content below the first screen.
4. Test the same contact field contract and safe submit, the captured Back/phone destinations, then next/previous process cards and visible progress. Assert the contact portrait remains absent from the visible first section.
5. The new route must retain usable links/validation without changing any protected consumer or sending a live request.

---

## Observed baseline and source requirements

Current owner: `app/inner-pages.mjs:appointmentPage()` plus the simple layout flag.
Build one dark striped first section under the measured simple header: 470×220.31 photo at x=200/y=123, 35px H1 on the left, white appointment form on the right. Remove the separate generic form section and visible large contact portrait. Restore the pale process section with its 760px-wide clipped photo, three source step cards and controls. The source third title is “Nog een stap”. Keep the captured Back destination /pagina-niet-gevonden and a working telephone action.

At 1920px the source H1 is `Maak een afspraak`: 35px/38.5px, box x=200.00, y=403.31, 470.00×38.50. Use these as measurements, not blank spacer dimensions.
The current local H1 is `Maak een afspraak` at 50px; its structure/photo/section geometry is visible in the linked comparison.
Source heading text currently absent or different: “Vakmanschap van begin tot eind”; “Hoe BHR werkt”; “Stap 1”; “Advies en Concept”; “Stap 2” (8 total; use the full fixture).

| Baseline viewport | Mismatch | SSIM estimate | Reference / local full image |
|---|---:|---:|---|
| wide | 54.665% | 0.5082 | 1920×2576 / 1920×2674 |
| desktop | 55.575% | 0.5289 | 1440×2504 / 1440×2564 |
| tablet | 72.479% | -0.0287 | 768×2859 / 768×3331 |
| mobile | 81.677% | -0.0022 | 390×4250 / 390×3470 |

[Full reference/candidate report or source evidence](../../../checks/visual-planning-2026-11-20/baseline/afspraak-maken/report.html)
 · [Measured inventory](../../../checks/visual-planning-2026-11-20/baseline/afspraak-maken/wide-reference-inventory.json)
 · [Text/media/link inventory](../../../checks/visual-planning-2026-11-20/baseline/afspraak-maken/wide-reference-content.json)

**Exact content/asset fixture:** this route’s entry in [expected-pages.json](../../../checks/visual-planning-2026-11-20/expected-pages.json). Its full source heading sequence, every original image filename, resolved action targets, FAQ pairs and CMS validation designations are binding. Do not copy the saved HTML into app code.

**Ordered own content blocks:**
1. Vul het afspraakformulier in / Henk Rutten

**Source image filenames (exact derivatives):** `797_dsc00930.webp`, `437_dsc02673.webp`.

**Source fields:** Bedrijfsnaam [required]; Naam [required]; E-mailadres [required]; Telefoonnummer [required]; Bericht; Ik ga akkoord met de privacyverklaring en voorwaarden. Use semantic CMS requiredness, not a false native required boolean. Keep exact option inventories from the fixture.

**Linked-route prerequisites:** `/pagina-niet-gevonden`, `/privacy`.

## Task 1: Source composition, exact assets and route ownership

**Files:** `app/secondary-content.json`, `app/secondary-data.mjs`, `app/secondary-pages.mjs`, `app/secondary-components.mjs`, `app/assets-manifest.json`, `app/public/assets/images/`; test `app/tests/secondary-pages.test.mjs` and its source fixture.
**Interfaces:** Consume `secondaryContent["/afspraak-maken"]` and the shared renderer/strict-media interfaces. Produce one authored `appointment` entry and generated `/afspraak-maken/index.html`; no duplicate route emitter.

- [ ] Add the frozen `/afspraak-maken` expectation and test `/afspraak-maken source composition`: `const html=readBody("/afspraak-maken"); assertInOrder(plainText(html),expected.headings); for(const src of expected.images) assert.ok(html.includes(src));` Assert the exact H1 “Maak een afspraak”, resolved destinations, expected FAQ count and no unrelated generic section.
- [ ] Run `npm --prefix app run build && node --test --test-name-pattern="/afspraak-maken source composition" app/tests/secondary-pages.test.mjs`; expect FAIL for the old composition/media or ENOENT for the missing route.
- [ ] Author the route’s complete source data and `appointment` body in its designated renderer; package every missing exact media URL with bytes/SHA-256 and an exact manifest key. Opt this route in through `secondaryOptions`; preserve requested URL, metadata and observed header variant.
- [ ] Rebuild and rerun the targeted test; expect PASS for all frozen headings/assets/links and this route’s actual content. Record a local source checkpoint.

## Task 2: Measured layout and observed behavior

**Files:** `app/public/secondary-parity.css`, the designated family renderer, `app/secondary-forms.mjs` where this page has a form, `app/public/secondary.mjs` only for new controls; test `app/tools/check-secondary-browser.py` and meaningful pure behavior cases.
**Interfaces:** Use `.secondary-parity.secondary-route-afspraak-maken` and the spec’s delivery/behavior contracts; do not change old global selectors.

- [ ] Capture any planning-unaudited widths and add the route-specific browser regression before its behavior implementation; verify that it fails against the old/missing controls. Use screenshot/box evidence for CSS rather than tests that mirror style declarations.
- [ ] Match the measured header, H1/emphasis, photo crop, source section surfaces, text widths, clipped corners, controls, form/card geometry and footer. Follow this page’s reference composition; do not impose a generic clean mobile stack or pad to the target document height.
- [ ] Implement and check: Test the same contact field contract and safe submit, the captured Back/phone destinations, then next/previous process cards and visible progress. Assert the contact portrait remains absent from the visible first section.
- [ ] Run `/tmp/bhr-visual-diff-venv/bin/python app/tools/check-secondary-browser.py --route /afspraak-maken` with delivery blocked; expect its keyboard/state/validation assertions to pass and zero real submission requests. Run the complete unit suite after any behavior change.

## Task 3: Four-width page review and release gate

- [ ] Complete the listed route prerequisites (or the ten-location batch), then run `npm --prefix app run build`, `npm --prefix app test` and `npm --prefix app run verify`; expect all functional/asset/link checks and the 12 protected hashes to pass.
- [ ] From the workspace root run `/tmp/bhr-visual-diff-venv/bin/python checks/visual-planning-2026-11-20/run-comparisons.py --route afspraak-maken --all-widths --out checks/visual-review-remaining-<run-id>`; expect four valid matched-zoom captures. Preserve the planning baseline.
- [ ] Open every width’s side-by-side, heatmap and overlay, and native crops of the title, photos, key control/form, section boundaries and footer. Compare actual boxes/fonts and document height. Review applicable expanded, selected, hover/focus and error views; scrolled sticky controls require separate viewport captures.
- [ ] Record each result separately. Require mismatch ≤0.5%, SSIM estimate ≥0.985 and height delta ≤2px at every width for strict acceptance; leave this page open if any fail. Never certify a missing candidate, unaudited state, averaged score or Craft score as a visual-diff pass.
- [ ] Record the source checkpoint, commands, browser results, individual metrics and any intentional difference in the execution ledger. No deployment or real delivery belongs to this page’s completion gate.
