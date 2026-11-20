# Expertises Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for native implementation, or superpowers:subagent-driven-development if the user selects delegation. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restore the live overlay hero, all ten service cards, process slider, recommendations and quote presentation.

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

Reference: `https://www.bhr-is.nl/expertises`. Candidate: `http://127.0.0.1:4173/expertises`.

Artifacts: [report](../../../checks/visual-planning-2026-11-19/expertises/report.md), [screenshots and DOM/content inventories](../../../checks/visual-planning-2026-11-19/expertises/).

Widths: desktop 1440x900, tablet 768x1024, mobile 390x844, DPR 1. Cookie consent dismissed; no content masks. Full page height is retained; repeated sticky headers are suppressed after the first viewport. See the spec for capture limitations and carousel variance.

| Viewport | Reference size | Local size | Pixel mismatch | SSIM estimate |
| --- | --- | --- | ---: | ---: |
| desktop | 1440×8226 | 1440×7391 | 88.97% | -0.1328 |
| tablet | 768×8659 | 768×9190 | 87.11% | 0.1102 |
| mobile | 390×11176 | 390×9306 | 89.70% | -0.1039 |

These are diagnostic mismatch measurements, not a percentage of likeness. Cumulative vertical offsets can make pixel mismatch very high.

**Dependency:** Complete [2026-11-19-bhr-00-shared-primitives.md](2026-11-19-bhr-00-shared-primitives.md) first.

### Confirmed differences

The local template places a separate dark intro below a wrongly cropped banner. The reference overlays the title, introduction and two actions directly on the hero. The local service component emits ten cards but hides the final two behind “Toon meer”; the reference presents ten cards in its overview. The entire “Vakmanschap van begin tot eind / Hoe BHR werkt” step slider is missing locally. The following article has its image/text direction reversed, the partner display is a carousel rather than a four-column grid, and the quote form shows a large step-label list absent from the live initial state.

### Task 1: Restore overview structure and the missing process block

**Files:** `app/inner-pages.mjs:expertiseIndex`, `app/components.mjs:serviceCards`, `app/data.mjs`, `app/public/parity.css`, `app/public/site.mjs` if slider controls need a new handler; `app/tests/inner-pages.test.mjs`.

**Interfaces:** `expertiseIndex() -> string` retains its export. Extend `serviceCards(all=false, options={}) -> string` with an explicit visible-overview variant, preserving other callers. Add `expertiseSteps() -> string` in `inner-pages.mjs` and data for the three captured step cards; use page-scoped controls.

- [x] Add a structural test that the page renders all ten service destinations in the overview and places “Hoe BHR werkt” between the service overview and “Complete oplossingen voor elke installatie”. It must fail on the current build.
- [x] Use the shared overlay hero and exact `917_ecec51a39e5616038f86b048c77d7c2eec6b96f7.webp` image. Preserve “Bekijk onze expertises” scrolling to the overview and “Ontdek hoe wij werken” linking to `/over-ons`.
- [x] Remove the local overview's extra “Toon meer” presentation and reveal all ten cards on this page only. Match reference columns, row spacing, image ratio, card titles and hover/focus links at each width.
- [x] Insert the blue process block, the exact `437_dsc02673.webp` photograph, clipped corners, background stripes, three step cards and previous/next/progress controls. Capture the reference's initial card position and responsive overflow; do not reuse the homepage's unrelated three-row “how” section.
- [x] Build, run the structural test and verify both process controls and service links with mouse and keyboard. Inspect the service-to-process boundary at all widths.

### Task 2: Match lower-page composition and quote form

**Files:** `app/inner-pages.mjs:expertiseIndex`, `app/components.mjs:articleSections, projectCards, partners, quoteForm`, `app/public/parity.css` and `app/public/behavior.mjs` only if state behavior changes.

- [x] Render “Complete oplossingen…” with text left, photograph right, the five captured bullets, original clipped image and “Spreek met een specialist” action. Match pale background and padding.
- [x] Match the three project cards in their actual widths, 450px desktop image height, title wraps, margins and action states. Use exact photographed subjects.
- [x] Match the partner strip's centered heading, bordered logo cells, viewport clipping, sizes and initial order. Keep navigation usable if the reference exposes controls.
- [x] Match CTA stripes and emphasis. Present the initial quote step as the compact centered white card with company, email and phone fields and “Volgende stap”; suppress the local visible eight-item step list in this variant. Match subsequent steps and validation without sending any live submissions.
- [x] Run the full functional checks and the route-specific review command below. Inspect top, missing-process area, project/partner boundary, quote card and footer in side-by-side and overlay images. Check hover/focus and next/previous wizard states separately.

## Per-page review and completion

- [x] From `app`, run `npm run build`, `npm test` and `npm run verify`; all must pass.
- [x] From the workspace root, with `app/dist` served on port 4173, run `python checks/visual-planning-2026-11-19/run-comparisons.py --route expertises --out checks/visual-review-expertises-<run-id>`.
- [x] Open every width's side-by-side, heatmap and overlay with the visual-diff skill. Review header, hero, each section transition, form and footer. Compare heading boxes, photo crops and page height with the DOM audits; do not rely on metrics alone.
- [ ] Match interactive states and stabilize moving regions before applying the spec's <=0.5% mismatch / >=0.985 SSIM targets. Keep raw unmasked evidence and record any remaining difference explicitly.
- [ ] Review the five failure modes in Review Focus, recheck the homepage and affected shared-template consumers, and record the page's individual result. A failure at one width leaves this page incomplete.
- [x] Record a local checkpoint; commit only if a Git repository has subsequently been initialized.

## Execution record

Implemented and functionally verified; final visual acceptance is tracked separately. The user selected **1920×1080** as primary, with 1440×900, 768×1024 and 390×844 retained. The normalized implementation capture helper supersedes the original planning command so both origins use native viewport tiles and the same settled carousel state.

See the [execution ledger](../execution/2026-11-19-progress.md) for architectural rulings and the [final comparison report](../../../checks/visual-implementation-2026-11-19/review/README.md) for individual results and remaining strict-target failures. Checked implementation/review steps do not declare an open numeric gate passed.
