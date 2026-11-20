# Partners Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for native implementation, or superpowers:subagent-driven-development if the user selects delegation. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Match the partners hero, moving logo strip, single-action CTA and personal contact form.

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

Reference: `https://www.bhr-is.nl/over-ons/partners`. Candidate: `http://127.0.0.1:4173/over-ons/partners`.

Artifacts: [report](../../../checks/visual-planning-2026-11-19/partners/report.md), [screenshots and DOM/content inventories](../../../checks/visual-planning-2026-11-19/partners/).

Widths: desktop 1440x900, tablet 768x1024, mobile 390x844, DPR 1. Cookie consent dismissed; no content masks. Full page height is retained; repeated sticky headers are suppressed after the first viewport. See the spec for capture limitations and carousel variance.

| Viewport | Reference size | Local size | Pixel mismatch | SSIM estimate |
| --- | --- | --- | ---: | ---: |
| desktop | 1440×3256 | 1440×3847 | 87.36% | -0.1131 |
| tablet | 768×3935 | 768×4873 | 90.30% | -0.3031 |
| mobile | 390×5431 | 390×4603 | 84.98% | -0.0826 |

These are diagnostic mismatch measurements, not a percentage of likeness. Cumulative vertical offsets can make pixel mismatch very high.

**Dependency:** Complete [2026-11-19-bhr-00-shared-primitives.md](2026-11-19-bhr-00-shared-primitives.md) first.

### Confirmed differences

The local route is assembled directly in `build.mjs` with `titleSection(..., false)`, which uses an inset image/text layout instead of the live full-bleed photographic hero. Verify the full introductory copy through observedPage; the inline build fallback alone omits the final sentence, while the current built page already recovers it from observed content. `partners()` produces a four-column static grid, whereas the live page uses a horizontally sliding strip with repeated track items. The local CTA/form are generic; the live contact section has a page-specific eyebrow, portrait and white form layout.

### Task 1: Give partners a dedicated composition and exact hero

**Files:** `app/build.mjs` partners registration, `app/inner-pages.mjs`, `app/page-content.json`, `app/data.mjs`, `app/assets-manifest.json`, `app/public/parity.css`, `app/tests/inner-pages.test.mjs`.

**Interfaces:** Add `partnersPage() -> string` to `inner-pages.mjs`; import it in `build.mjs` and replace the inline partners assembly. Consume the shared overlay hero and retain the current route.

- [x] Add a structural test asserting the exact hero image, full observed introductory copy, logo section, single-action project CTA and “Samenwerken doen we graag!” contact section in that order. The missing overlay hero variant must make it fail on the current build.
- [x] Package the exact `866_dsc02204.webp` document image. Render the live title and complete introduction, including “Onderstaand ziet u de partners van BHR Industrial Solutions:”, as the captured overlay composition.
- [x] Match hero crop, text wrap, colors, whitespace and absence/presence of actions using the reference's three DOM audits. The observed introductory copy already restores the final partner-list sentence in the current build; preserve it rather than claiming it is missing.
- [x] Build and compare the hero/partner transition at all widths before proceeding.

### Task 2: Logo strip, CTA and contact presentation

**Files:** `app/components.mjs:partners`, `app/inner-pages.mjs:partnersPage`, `app/public/parity.css`, `app/public/site.mjs` for scoped carousel controls if required.

**Interfaces:** Extend `partners(options={}) -> string` with an opt-in strip variant. Keep the eight unique partner records distinct from any cloned track items. The expertises page can reuse this variant, but other consumers keep their default presentation until reviewed.

- [x] Match the eight logos, asset fit, bordered cells, gaps, centered heading and clipped track. Use the captured viewport's visible window; duplicated track images are carousel clones, not additional partner records. Do not hard-code a transient “slide 9 to 12 of 8” status string into site copy.
- [x] Exercise the strip's available controls/drag behavior and keyboard focus. Before strict scoring, set the same logical first slide on both pages or pause the same state; automatic timing is not a reliable reference state.
- [x] Match the striped “Klaar om uw project te bespreken?” CTA with its single “Neem contact op” action. Do not introduce the generic second expertise button.
- [x] Render the “Neem contact met ons op?” eyebrow and “Samenwerken doen we graag!” heading, compact Henk Rutten panel with a 100×100 circular portrait and phone/WhatsApp row, five captured contact fields and privacy/terms consent. Preserve validation and delivery behavior.
- [x] Run full functional checks and route review. Inspect initial and advanced strip states, narrow text wrapping, the CTA/form transition and footer. Recheck the expertises strip if its implementation is shared.

## Per-page review and completion

- [x] From `app`, run `npm run build`, `npm test` and `npm run verify`; all must pass.
- [x] From the workspace root, with `app/dist` served on port 4173, run `python checks/visual-planning-2026-11-19/run-comparisons.py --route partners --out checks/visual-review-partners-<run-id>`.
- [x] Open all three widths' side-by-side, heatmap and overlay files with the visual-diff skill. Inspect every section and compare computed boxes, fonts, image crops and total page height.
- [ ] Match carousel, counter, hover/focus and form states as applicable before applying the spec's <=0.5% mismatch / >=0.985 SSIM targets. Retain unmasked evidence and document any unresolved difference.
- [ ] Check all five Review Focus failure modes and affected shared-template consumers. A failure at one width leaves this page incomplete.
- [x] Record a local checkpoint; commit only if this workspace later has Git configured.

## Execution record

Implemented and functionally verified; final visual acceptance is tracked separately. The user selected **1920×1080** as primary, with 1440×900, 768×1024 and 390×844 retained. The normalized implementation capture helper supersedes the original planning command so both origins use native viewport tiles and the same settled carousel state.

See the [execution ledger](../execution/2026-11-19-progress.md) for architectural rulings and the [final comparison report](../../../checks/visual-implementation-2026-11-19/review/README.md) for individual results and remaining strict-target failures. Checked implementation/review steps do not declare an open numeric gate passed.
