# Voor machinebouwers Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for native implementation, or superpowers:subagent-driven-development if the user selects delegation. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Match the five alternating article blocks, live hero and personal contact section of the nested machine-builders route.

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

Reference: `https://www.bhr-is.nl/voor-machinebouwers/voor-machinebouwers`. Candidate: `http://127.0.0.1:4173/voor-machinebouwers/voor-machinebouwers`.

Artifacts: [report](../../../checks/visual-planning-2026-11-19/machinebouwers/report.md), [screenshots and DOM/content inventories](../../../checks/visual-planning-2026-11-19/machinebouwers/).

Widths: desktop 1440x900, tablet 768x1024, mobile 390x844, DPR 1. Cookie consent dismissed; no content masks. Full page height is retained; repeated sticky headers are suppressed after the first viewport. See the spec for capture limitations and carousel variance.

| Viewport | Reference size | Local size | Pixel mismatch | SSIM estimate |
| --- | --- | --- | ---: | ---: |
| desktop | 1440×7292 | 1440×7521 | 76.35% | 0.4168 |
| tablet | 768×10050 | 768×9552 | 77.00% | 0.0647 |
| mobile | 390×16070 | 390×9885 | 82.25% | -0.0894 |

These are diagnostic mismatch measurements, not a percentage of likeness. Cumulative vertical offsets can make pixel mismatch very high.

**Dependency:** Complete [2026-11-19-bhr-00-shared-primitives.md](2026-11-19-bhr-00-shared-primitives.md) first.

### Confirmed differences

This route uses the local `standardPage` renderer with the base `/voor-machinebouwers` record; the requested nested path is an alias. The source copy largely exists, but the hero composition, intentional title breaks, repeated article spacing, photo shapes and lower contact section differ. The phone baseline is thousands of pixels shorter locally, so a desktop-only correction will not cover it.

### Task 1: Bind the exact nested route and restore the hero/articles

**Files:** `app/build.mjs` nested route registration, `app/data.mjs:standard, observedPage, pageImage`, `app/inner-pages.mjs:standardPage`, `app/public/parity.css`, `app/tests/inner-pages.test.mjs`.

**Interfaces:** Keep `standardPage(page) -> string`. Give the nested route explicit parity presentation data while deliberately sourcing the base route's observed copy; preserve direct visits to both URLs.

- [x] Add a route test asserting the nested URL contains each of the five live article headings exactly once and in order, with the correct local image paths. Confirm it catches any current image fallback or missing section.
- [x] Render the exact `851_dsc01712.webp` hero with the overlay title. Preserve “Machinebouw-”, “ondersteuning” and the subsequent text's live line breaks and emphasis rather than relying on a normalized JSON heading to reproduce them.
- [x] Restore the separate dark “Voor machinebouwers” introduction band immediately below the hero: title at left, lead copy at right. The current small white lead is not equivalent. Then match the five alternating article compositions, lists and spacing in the saved reference order. Source photographs, in order: `783_dsc01720.webp`, `779_dsc02362.webp`, `777_dsc00987.webp`, `775_dsc02204.webp`, `781_dsc02826.webp`.
- [x] Match clipped corners, 940×740 source aspect ratios, image/text widths, vertical centering and background changes. Use the reference mobile/tablet stacking and large gutters; do not impose the local generic 600px stacking rule.
- [x] Build and run the route/asset audit. Inspect the first and last article at each width before moving to the contact area.

### Task 2: Match the CTA and personal contact form

**Files:** `app/inner-pages.mjs:standardPage`, `app/components.mjs:cta, contactForm`, `app/public/parity.css`; use shared opt-in presentation options.

- [x] Reproduce the striped CTA immediately after the fifth article, retaining the captured action texts and destinations.
- [x] Match “Kunnen we u helpen met uw proces?”, Henk Rutten's circular 100×100 portrait, compact role/name/phone/WhatsApp row and the white form card; replace the current large rectangular portrait. Use the reference field order, required indicators, checkboxes, control dimensions and submit alignment from the saved HTML/content inventory.
- [x] Exercise an invalid form and an unconfigured submission locally without contacting the live form service. Keep usable keyboard focus and error feedback.
- [x] Run the full functional checks and route review. Inspect all five image/text transitions, CTA/contact boundary and footer; verify the long phone layout and final document height rather than copying desktop offsets.

## Per-page review and completion

- [x] From `app`, run `npm run build`, `npm test` and `npm run verify`; all must pass.
- [x] From the workspace root, with `app/dist` served on port 4173, run `python checks/visual-planning-2026-11-19/run-comparisons.py --route machinebouwers --out checks/visual-review-machinebouwers-<run-id>`.
- [x] Open every width's side-by-side, heatmap and overlay with the visual-diff skill. Review header, hero, each section transition, form and footer. Compare heading boxes, photo crops and page height with the DOM audits; do not rely on metrics alone.
- [ ] Match interactive states and stabilize moving regions before applying the spec's <=0.5% mismatch / >=0.985 SSIM targets. Keep raw unmasked evidence and record any remaining difference explicitly.
- [ ] Review the five failure modes in Review Focus, recheck the homepage and affected shared-template consumers, and record the page's individual result. A failure at one width leaves this page incomplete.
- [x] Record a local checkpoint; commit only if a Git repository has subsequently been initialized.

## Execution record

Implemented and functionally verified; final visual acceptance is tracked separately. The user selected **1920×1080** as primary, with 1440×900, 768×1024 and 390×844 retained. The normalized implementation capture helper supersedes the original planning command so both origins use native viewport tiles and the same settled carousel state.

See the [execution ledger](../execution/2026-11-19-progress.md) for architectural rulings and the [final comparison report](../../../checks/visual-implementation-2026-11-19/review/README.md) for individual results and remaining strict-target failures. Checked implementation/review steps do not declare an open numeric gate passed.
