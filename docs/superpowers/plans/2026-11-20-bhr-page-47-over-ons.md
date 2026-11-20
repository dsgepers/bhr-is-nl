# BHR /over-ons Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for native execution, or superpowers:subagent-driven-development if explicitly selected. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make local `/over-ons` match its live equivalent, with independent visual acceptance.
**Architecture:** Opt in this exact route through the shared secondary manifest; use the `company` composition and route-scoped styles. Preserve old default consumers.
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

1. Long/emphasized “Over BHR | Partner in industriële automatisering” text must retain source wrapping at all four widths.
2. Exact source photo derivatives and original media must load; a same-photo fallback is not an acceptable substitution.
3. The full heading/section/FAQ inventory must remain ordered, including content below the first screen.
4. Check the source section actions and any observed team WhatsApp/hover, partner controls or recruitment destinations. Keep source empty states and use original certificate/reference media where applicable.
5. The new route must retain usable links/validation without changing any protected consumer or sending a live request.

---

## Observed baseline and source requirements

Current owner: `app/inner-pages.mjs:aboutPage()`.
Reproduce this route’s observed company composition and source assets, preserving the exact section order and any team, values, testimonial, certificate or recruitment treatment. Replace generic existing compositions only on this opted-in route; do not add a shared company template’s extra sections to short pages.

Replace the current photo-only hero with the observed “Over ons” overlay and its exact photograph. Match mission/vision, photographed industry choices, partner strip, the dark striped GREAT letter section, testimonial, vacancies/team and recruitment CTA in the source order. The source capture contains no video/iframe requiring an invented video hero.
The current local H1 is `Gedreven door techniek en teamwork` at 50px; its structure/photo/section geometry is visible in the linked comparison.
Source heading text currently absent or different: “Onze geschiedenis”; “Onze roots in techniek”; “2017”; “Rutten industriele automatisering ingeschreven KVK”; “2018” (18 total; use the full fixture).

| Baseline viewport | Mismatch | SSIM estimate | Reference / local full image |
|---|---:|---:|---|
| wide | 82.487% | -0.1220 | 1920×8722 / 1920×7925 |

Planning captured 1920px only for this secondary page. **Capture the other three widths before implementation fine tuning; they are not audited/passed by this baseline.**

[Full reference/candidate report or source evidence](../../../checks/visual-planning-2026-11-20/baseline/over-ons/report.html)
 · [Measured inventory](../../../checks/visual-planning-2026-11-20/baseline/over-ons/wide-reference-inventory.json)
 · [Text/media/link inventory](../../../checks/visual-planning-2026-11-20/baseline/over-ons/wide-reference-content.json)

**Exact content/asset fixture:** this route’s entry in [expected-pages.json](../../../checks/visual-planning-2026-11-20/expected-pages.json). Its full source heading sequence, every original image filename, resolved action targets, FAQ pairs and CMS validation designations are binding. Do not copy the saved HTML into app code.

**Ordered own content blocks:**
1. Gedreven door techniek en teamwork
2. 2017 / Rutten industriele automatisering ingeschreven KVK
3. 2018 / Brekelmans automatisering ingeschreven KVK
4. 2023 / Eerste kleine gezamenlijke montage
5. 2023 / Gezamenlijke klus spinazie verwerking
6. 2023 / Gezamenlijke project gerealiseerd nieuwe fabriek A-Z
7. 2024 / BHR is officieel ingeschreven bij de KVK
8. 2025 / 1e medewerker in dienst
9. 2025 / E-plan engineer in dienst genomen
10. Voor machinebouwers / Voor proces & productie / Industriële automatisering die alles verbindt
11. Voor machinebouwers
12. Voor proces & productie
13. Garantie
14. Resultaat
15. Efficientie
16. Ambitie
17. Trots
18. ''Het bedrijf is goed bereikbaar, reageert snel en professioneel bij storingen en beschikt over deskundig en betrokken personeel''
19. Henk Rutten
20. Bouw mee aan jouw toekomst in de techniek

**Source image filenames (exact derivatives):** `1113_dsc02261.webp`, `1116_1493618a8e8e77f6d88bb54501e6ea1d35a356b9.webp`, `452_dsc02362.webp`, `826_dsc00946.webp`, `899_dsc00962.webp`, `828_dsc02710.webp`, `829_dsc01293.webp`, `898_dsc02475.webp`, `831_dsc00930.webp`, `832_dsc01525.webp`, `833_dsc01048.webp`, `892_dsc01712.webp`, `893_dsc01159.webp`, `1002_rittal.webp`, `1003_lappkabel-logo.webp`, `1194_abb.webp`, `1195_allen-bradley.webp`, `1196_phoenix-contacts.webp`, `1197_wago.webp`, `44_partner2.webp`, `45_partner3.webp`, `908_aqualab-zuid.webp`, `vacancybg.png`, `1147_dsc02542.webp`.

**Linked-route prerequisites:** `/privacy`.

## Task 1: Source composition, exact assets and route ownership

**Files:** `app/secondary-content.json`, `app/secondary-data.mjs`, `app/secondary-pages.mjs`, `app/secondary-components.mjs`, `app/assets-manifest.json`, `app/public/assets/images/`; test `app/tests/secondary-pages.test.mjs` and its source fixture.
**Interfaces:** Consume `secondaryContent["/over-ons"]` and the shared renderer/strict-media interfaces. Produce one authored `company` entry and generated `/over-ons/index.html`; no duplicate route emitter.

- [ ] Add the frozen `/over-ons` expectation and test `/over-ons source composition`: `const html=readBody("/over-ons"); assertInOrder(plainText(html),expected.headings); for(const src of expected.images) assert.ok(html.includes(src));` Assert the exact H1 “Over BHR | Partner in industriële automatisering”, resolved destinations, expected FAQ count and no unrelated generic section.
- [ ] Run `npm --prefix app run build && node --test --test-name-pattern="/over-ons source composition" app/tests/secondary-pages.test.mjs`; expect FAIL for the old composition/media or ENOENT for the missing route.
- [ ] Author the route’s complete source data and `company` body in its designated renderer; package every missing exact media URL with bytes/SHA-256 and an exact manifest key. Opt this route in through `secondaryOptions`; preserve requested URL, metadata and observed header variant.
- [ ] Rebuild and rerun the targeted test; expect PASS for all frozen headings/assets/links and this route’s actual content. Record a local source checkpoint.

## Task 2: Measured layout and observed behavior

**Files:** `app/public/secondary-parity.css`, the designated family renderer, `app/secondary-forms.mjs` where this page has a form, `app/public/secondary.mjs` only for new controls; test `app/tools/check-secondary-browser.py` and meaningful pure behavior cases.
**Interfaces:** Use `.secondary-parity.secondary-route-over-ons` and the spec’s delivery/behavior contracts; do not change old global selectors.

- [ ] Capture any planning-unaudited widths and add the route-specific browser regression before its behavior implementation; verify that it fails against the old/missing controls. Use screenshot/box evidence for CSS rather than tests that mirror style declarations.
- [ ] Match the measured header, H1/emphasis, photo crop, source section surfaces, text widths, clipped corners, controls, form/card geometry and footer. Follow this page’s reference composition; do not impose a generic clean mobile stack or pad to the target document height.
- [ ] Implement and check: Check the source section actions and any observed team WhatsApp/hover, partner controls or recruitment destinations. Keep source empty states and use original certificate/reference media where applicable.
- [ ] Run `/tmp/bhr-visual-diff-venv/bin/python app/tools/check-secondary-browser.py --route /over-ons` with delivery blocked; expect its keyboard/state/validation assertions to pass and zero real submission requests. Run the complete unit suite after any behavior change.

## Task 3: Four-width page review and release gate

- [ ] Complete the listed route prerequisites (or the ten-location batch), then run `npm --prefix app run build`, `npm --prefix app test` and `npm --prefix app run verify`; expect all functional/asset/link checks and the 12 protected hashes to pass.
- [ ] From the workspace root run `/tmp/bhr-visual-diff-venv/bin/python checks/visual-planning-2026-11-20/run-comparisons.py --route over-ons --all-widths --out checks/visual-review-remaining-<run-id>`; expect four valid matched-zoom captures. Preserve the planning baseline.
- [ ] Open every width’s side-by-side, heatmap and overlay, and native crops of the title, photos, key control/form, section boundaries and footer. Compare actual boxes/fonts and document height. Review applicable expanded, selected, hover/focus and error views; scrolled sticky controls require separate viewport captures.
- [ ] Record each result separately. Require mismatch ≤0.5%, SSIM estimate ≥0.985 and height delta ≤2px at every width for strict acceptance; leave this page open if any fail. Never certify a missing candidate, unaudited state, averaged score or Craft score as a visual-diff pass.
- [ ] Record the source checkpoint, commands, browser results, individual metrics and any intentional difference in the execution ledger. No deployment or real delivery belongs to this page’s completion gate.
