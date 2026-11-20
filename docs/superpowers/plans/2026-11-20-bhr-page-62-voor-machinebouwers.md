# BHR /voor-machinebouwers Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for native execution, or superpowers:subagent-driven-development if explicitly selected. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make local `/voor-machinebouwers` match its live equivalent, with independent visual acceptance.
**Architecture:** Opt in this exact route through the shared secondary manifest; use the `alias` composition and route-scoped styles. Preserve old default consumers.
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

1. Long/emphasized “Machinebouw- ondersteuning voor OEM’s en professionele machinebouwers” text must retain source wrapping at all four widths.
2. Exact source photo derivatives and original media must load; a same-photo fallback is not an acceptable substitution.
3. The full heading/section/FAQ inventory must remain ordered, including content below the first screen.
4. Verify the requested URL stays a 200 page with no redirect; then exercise its canonical composition’s contact/application and source actions using the same delivery guards. Preserve all protected route hashes.
5. The new route must retain usable links/validation without changing any protected consumer or sending a live request.

---

## Observed baseline and source requirements

Current owner: the explicit route in `app/build.mjs` and its current component helpers.
The source serves this requested URL with HTTP 200, not a redirect. Reuse the already authored machine-builders/careers composition as a starting point, retaining this route’s observed metadata, photo derivative and content. Apply any remaining layout corrections in the new alias scope only; the canonical route from the previous phase remains protected. Renderer reuse is not a 301/302 decision.

Reuse the canonical nested machine-builders composition without changing that protected route. The current root renderer still uses the old split document header; replace it with the observed overlay/lead, five original alternating articles, CTA and compact contact form.

At 1920px the source H1 is `Machinebouw- ondersteuning voor OEM’s en professionele machinebouwers`: 65px/57.2px, box x=200.00, y=175.84, 620.00×285.94. Use these as measurements, not blank spacer dimensions.
The current local H1 is `Machinebouw-ondersteuning voor OEM’s en professionele machinebouwers` at 50px; its structure/photo/section geometry is visible in the linked comparison.
Source heading text currently absent or different: “Machinebouw- ondersteuning voor OEM’s en professionele machinebouwers”.

| Baseline viewport | Mismatch | SSIM estimate | Reference / local full image |
|---|---:|---:|---|
| wide | 69.860% | 0.5666 | 1920×7523 / 1920×7698 |

Planning captured 1920px only for this secondary page. **Capture the other three widths before implementation fine tuning; they are not audited/passed by this baseline.**

[Full reference/candidate report or source evidence](../../../checks/visual-planning-2026-11-20/baseline/voor-machinebouwers/report.html)
 · [Measured inventory](../../../checks/visual-planning-2026-11-20/baseline/voor-machinebouwers/wide-reference-inventory.json)
 · [Text/media/link inventory](../../../checks/visual-planning-2026-11-20/baseline/voor-machinebouwers/wide-reference-content.json)

**Exact content/asset fixture:** this route’s entry in [expected-pages.json](../../../checks/visual-planning-2026-11-20/expected-pages.json). Its full source heading sequence, every original image filename, resolved action targets, FAQ pairs and CMS validation designations are binding. Do not copy the saved HTML into app code.

**Ordered own content blocks:**
1. Seriematige paneelbouw voor maximale efficiëntie
2. Efficiënte techniek die ontworpen is om te presteren
3. De kwaliteit van het proces gewaarborgd door testen en controle
4. BHR Industrial Solutions: een partner die uw machinebouw versterkt
5. Samen bouwen aan voorspelbare, efficiënte machinebouw
6. Wat kunnen wij voor jouw proces betekenen?
7. Kunnen we u helpen met uw proces? / Henk Rutten
8. Henk Rutten

**Source image filenames (exact derivatives):** `851_dsc01712.webp`, `783_dsc01720.webp`, `779_dsc02362.webp`, `777_dsc00987.webp`, `775_dsc02204.webp`, `781_dsc02826.webp`, `1147_dsc02542.webp`.

**Source fields:** Bedrijfsnaam [required]; Naam [required]; E-mailadres [required]; Telefoonnummer [required]; Bericht; Ik ga akkoord met de privacyverklaring en voorwaarden. Use semantic CMS requiredness, not a false native required boolean. Keep exact option inventories from the fixture.

**Linked-route prerequisites:** `/privacy`.

## Task 1: Source composition, exact assets and route ownership

**Files:** `app/secondary-content.json`, `app/secondary-data.mjs`, `app/secondary-pages.mjs`, `app/secondary-components.mjs`, `app/assets-manifest.json`, `app/public/assets/images/`; test `app/tests/secondary-pages.test.mjs` and its source fixture.
**Interfaces:** Consume `secondaryContent["/voor-machinebouwers"]` and the shared renderer/strict-media interfaces. Produce one authored `alias` entry and generated `/voor-machinebouwers/index.html`; no duplicate route emitter.

- [ ] Add the frozen `/voor-machinebouwers` expectation and test `/voor-machinebouwers source composition`: `const html=readBody("/voor-machinebouwers"); assertInOrder(plainText(html),expected.headings); for(const src of expected.images) assert.ok(html.includes(src));` Assert the exact H1 “Machinebouw- ondersteuning voor OEM’s en professionele machinebouwers”, resolved destinations, expected FAQ count and no unrelated generic section.
- [ ] Run `npm --prefix app run build && node --test --test-name-pattern="/voor-machinebouwers source composition" app/tests/secondary-pages.test.mjs`; expect FAIL for the old composition/media or ENOENT for the missing route.
- [ ] Author the route’s complete source data and `alias` body in its designated renderer; package every missing exact media URL with bytes/SHA-256 and an exact manifest key. Opt this route in through `secondaryOptions`; preserve requested URL, metadata and observed header variant.
- [ ] Rebuild and rerun the targeted test; expect PASS for all frozen headings/assets/links and this route’s actual content. Record a local source checkpoint.

## Task 2: Measured layout and observed behavior

**Files:** `app/public/secondary-parity.css`, the designated family renderer, `app/secondary-forms.mjs` where this page has a form, `app/public/secondary.mjs` only for new controls; test `app/tools/check-secondary-browser.py` and meaningful pure behavior cases.
**Interfaces:** Use `.secondary-parity.secondary-route-voor-machinebouwers` and the spec’s delivery/behavior contracts; do not change old global selectors.

- [ ] Capture any planning-unaudited widths and add the route-specific browser regression before its behavior implementation; verify that it fails against the old/missing controls. Use screenshot/box evidence for CSS rather than tests that mirror style declarations.
- [ ] Match the measured header, H1/emphasis, photo crop, source section surfaces, text widths, clipped corners, controls, form/card geometry and footer. Follow this page’s reference composition; do not impose a generic clean mobile stack or pad to the target document height.
- [ ] Implement and check: Verify the requested URL stays a 200 page with no redirect; then exercise its canonical composition’s contact/application and source actions using the same delivery guards. Preserve all protected route hashes.
- [ ] Run `/tmp/bhr-visual-diff-venv/bin/python app/tools/check-secondary-browser.py --route /voor-machinebouwers` with delivery blocked; expect its keyboard/state/validation assertions to pass and zero real submission requests. Run the complete unit suite after any behavior change.

## Task 3: Four-width page review and release gate

- [ ] Complete the listed route prerequisites (or the ten-location batch), then run `npm --prefix app run build`, `npm --prefix app test` and `npm --prefix app run verify`; expect all functional/asset/link checks and the 12 protected hashes to pass.
- [ ] From the workspace root run `/tmp/bhr-visual-diff-venv/bin/python checks/visual-planning-2026-11-20/run-comparisons.py --route voor-machinebouwers --all-widths --out checks/visual-review-remaining-<run-id>`; expect four valid matched-zoom captures. Preserve the planning baseline.
- [ ] Open every width’s side-by-side, heatmap and overlay, and native crops of the title, photos, key control/form, section boundaries and footer. Compare actual boxes/fonts and document height. Review applicable expanded, selected, hover/focus and error views; scrolled sticky controls require separate viewport captures.
- [ ] Record each result separately. Require mismatch ≤0.5%, SSIM estimate ≥0.985 and height delta ≤2px at every width for strict acceptance; leave this page open if any fail. Never certify a missing candidate, unaudited state, averaged score or Craft score as a visual-diff pass.
- [ ] Record the source checkpoint, commands, browser results, individual metrics and any intentional difference in the execution ledger. No deployment or real delivery belongs to this page’s completion gate.
