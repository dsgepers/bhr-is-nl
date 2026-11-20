# Werken bij Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for native implementation, or superpowers:subagent-driven-development if the user selects delegation. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Match the careers hero, recruitment content, facts, values, location and full application form.

**Architecture:** Use shared route-scoped parity primitives with an explicit page composition and original assets. Keep application behavior in the existing browser modules.

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

Reference: `https://www.bhr-is.nl/over-ons/werken-bij`. Candidate: `http://127.0.0.1:4173/over-ons/werken-bij`.

Artifacts: [report](../../../checks/visual-planning-2026-11-19/werken-bij/report.md), [screenshots and DOM/content inventories](../../../checks/visual-planning-2026-11-19/werken-bij/).

Widths: desktop 1440x900, tablet 768x1024, mobile 390x844, DPR 1. Cookie consent dismissed; no content masks. Full page height is retained; repeated sticky headers are suppressed after the first viewport. See the spec for capture limitations and carousel variance.

| Viewport | Reference size | Local size | Pixel mismatch | SSIM estimate |
| --- | --- | --- | ---: | ---: |
| desktop | 1440×8202 | 1440×7242 | 85.28% | -0.1910 |
| tablet | 768×9501 | 768×10575 | 83.78% | -0.2174 |
| mobile | 390×14793 | 390×9782 | 78.83% | -0.1177 |

These are diagnostic mismatch measurements, not a percentage of likeness. Cumulative vertical offsets can make pixel mismatch very high.

**Dependency:** Complete [2026-11-19-bhr-00-shared-primitives.md](2026-11-19-bhr-00-shared-primitives.md) first.

### Confirmed differences

The local hero is a generic pale image/text block rather than the live full-width overlay with “Zo werkt / het bij BHR” treatment. Several article and fact images are substituted or repeated. Section order is broadly present, but the fact cards, values block, empty vacancies state, location block and blue CTA/application background differ. The current birth date uses one native date input; the live form has three selectors. The local vacancy option is “Open sollicitatie”, whereas the captured live options are “Junior E-Plan Engineer” and “Monteur Paneelbouw”. The live form has its own white card heading and consent statement.

### Task 1: Match hero and recruitment sections with exact imagery

**Files:** `app/inner-pages.mjs:careersPage`, `app/data.mjs`, `app/reference/image-map.json`, `app/assets-manifest.json`, `app/page-content.json`, `app/public/parity.css`, `app/tests/inner-pages.test.mjs`.

**Interfaces:** Keep `careersPage() -> string`. Store explicit facts `{value, suffix, title, image}` and vacancy choices as captured data, rather than reusing one hero photograph or hard-coded global defaults.

- [x] Strengthen the careers structural test for the full section order: hero, two recruitment articles, vacancies, facts, values, location, CTA, application. Assert the five distinct fact images and the two captured vacancy choices; expect current fallback data to fail where inaccurate.
- [x] Use exact hero `857_dsc02261.webp`, the live emphasized title, complete introductory text, `/vacature` action and the “Lees verder” anchor to the first recruitment content for the desktop variant. The tablet/phone references show an unusually collapsed/overlapping initial hero; confirm it in a fresh viewport capture and follow the measured page-specific responsive composition instead of blindly applying the desktop overlay or inventing a cleaner redesign.
- [x] Use `787_dsc02462.webp` and `785_dsc00930.webp` for the first two articles. Match alternating image/text positions, clipped corners, copy width, whitespace and background changes.
- [x] Reproduce the vacancies empty state as captured, including heading and “Bekijk meer vacatures”. Do not invent vacancy cards merely because the application select has vacancy options.
- [x] Render the five fact cards with `816_dsc01886.webp`, `819_dsc02091.webp`, `820_dsc02701.webp`, `822_dsc02552.webp`, `824_dsc01048.webp`. Rebuild the desktop facts as the reference's asymmetric photo mosaic on a dark workshop background, with white statistic panels over the photographs, not five equal columns with values beneath. Match value/suffix typography for the first greater-than-50 treatment, 20, 60+, 1 and 100%, plus each card's title, crop and responsive arrangement. Freeze counters at their completed values for comparisons.
- [x] Match “Wat ons drijft” as a dark blue striped section, with its four outlined icons and headings. Extend the existing SVG icon module for the reference icon shapes; do not keep the current pale background and thin top-border cards. Do not assume the current four thin top-bordered boxes match the live composition.
- [x] Restore location image `1120_dsc02091.webp`, contact/address lines and “Plan je route” action. Preserve the live copy as captured, including its differing place names; editorial correction is a separate decision.
- [x] Build, run structural/asset checks and visually review the fact/value/location boundaries at all widths.

### Task 2: Match the application card and field controls

**Files:** `app/inner-pages.mjs:careersPage`, `app/components.mjs:contactForm` or a dedicated `applicationForm() -> string`, `app/public/site.mjs`, `app/public/behavior.mjs` only as needed, `app/public/parity.css`, `app/tests/forms.test.mjs` when date serialization changes.

- [x] Match the striped “Bouw mee aan jouw toekomst in de techniek” CTA and the pale application section that follows, with its compact circular contact portrait and bordered white application card. The application section itself does not continue the CTA stripes. Render the live outer label and inner white-card heading without accidentally duplicating a semantic main heading.
- [x] Match first/last name, email, phone, date-of-birth day/month/year selectors, retention consent, two vacancy choices, CV upload and final privacy/terms statement. Use the saved HTML snapshot for placeholder and required-state details.
- [x] Keep the existing sending subject and delivery hooks. If three date selectors serialize to `birthdate`, add a meaningful test that a selected day/month/year produces the correct value and that an invalid/incomplete date cannot submit. Keep the combined 4 MB file limit and existing error feedback.
- [x] Match label weights, required stars, field heights, date selector columns, CV picker appearance, checkbox spacing and submit alignment. Validate empty, selected, file-chosen and error states locally; do not send an application.
- [x] Run the full suite and route review. Inspect the mobile fact cards, values block, full form (including below the upload control), CTA and footer. Recheck other forms if shared helpers changed.

## Per-page review and completion

- [x] From `app`, run `npm run build`, `npm test` and `npm run verify`; all must pass.
- [x] From the workspace root, with `app/dist` served on port 4173, run `python checks/visual-planning-2026-11-19/run-comparisons.py --route werken-bij --out checks/visual-review-werken-bij-<run-id>`.
- [x] Open all three widths' side-by-side, heatmap and overlay files with the visual-diff skill. Inspect every section and compare computed boxes, fonts, image crops and total page height.
- [ ] Match carousel, counter, hover/focus and form states as applicable before applying the spec's <=0.5% mismatch / >=0.985 SSIM targets. Retain unmasked evidence and document any unresolved difference.
- [ ] Check all five Review Focus failure modes and affected shared-template consumers. A failure at one width leaves this page incomplete.
- [x] Record a local checkpoint; commit only if this workspace later has Git configured.

## Execution record

Implemented and functionally verified; final visual acceptance is tracked separately. The user selected **1920×1080** as primary, with 1440×900, 768×1024 and 390×844 retained. The normalized implementation capture helper supersedes the original planning command so both origins use native viewport tiles and the same settled carousel state.

See the [execution ledger](../execution/2026-11-19-progress.md) for architectural rulings and the [final comparison report](../../../checks/visual-implementation-2026-11-19/review/README.md) for individual results and remaining strict-target failures. Checked implementation/review steps do not declare an open numeric gate passed.
