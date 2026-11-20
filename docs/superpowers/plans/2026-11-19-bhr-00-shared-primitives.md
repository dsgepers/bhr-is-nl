# BHR shared visual primitives Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for native implementation, or superpowers:subagent-driven-development if the user selects delegation. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Provide measured, route-scoped building blocks for the six page plans.

**Architecture:** Keep the existing generator and add opt-in page classes and a final scoped stylesheet. Reuse the existing templates with explicit variants; leave their default behavior intact.

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

## Files and interfaces

- Modify `app/build.mjs`: opt the six routes into `parity-page` plus `parity-<page-key>`, retaining existing secondary/reference classes. The machine-builders alias must keep functioning.
- Modify `app/components.mjs`: `layout(title, body, cls='', simple=false) -> string` loads `/parity.css` only when `cls` includes `parity-page`. Keep existing defaults for other routes.
- Modify `app/inner-pages.mjs`: `documentHeader(page, variant='overlay') -> string` renders image, overlay, title, intro and actions in one hero; renderers choose variants explicitly.
- Modify `app/components.mjs`: extend `contactForm(title, job=false, options={}) -> string` with an opt-in presentation variant while preserving field names, delivery, validation and existing callers.
- Create `app/public/parity.css`: all selectors begin with `.parity-page` or a page-specific parity class. Do not add another layer of unscoped homepage overrides.
- Modify `app/public/icons.mjs` only for reference-matched SVG icons needed by these variants; retain existing exports.
- Modify `app/data.mjs`, `app/assets-manifest.json` and `app/public/assets/` only where exact reference media is absent. `media(sourceUrl)` continues resolving local paths, but parity pages must not silently accept the differently sized same-photo fallback.
- Test `app/tests/inner-pages.test.mjs` for real structure/link changes; use screenshot comparisons for CSS.

## Measured shared discrepancies

At 1440px the live hero heading starts at x=100, y=191, with 65px Oxanium, 57.2px line height and a 620px text box. The local document header puts a 50px heading into a second block below the photograph. Its image derivative can also differ from the actual live 1920×700 asset.

The live desktop header is 116px tall in the captured 1440px view and wraps navigation onto two rows. The local secondary header is 90px with a different logo, navigation spacing and one-row arrangement. Active navigation underlines, home/search/phone controls and footer icons also need direct matching.

The live 768px and 390px captures retain a large header and 100px content inset. At 390px the hero text box is only 190px wide and hero text is still 65px. Preserve the actual captured layout for this parity task, including awkward mobile wrapping; do not silently redesign it into a more conventional mobile layout.

Body typography is 16px Roboto in the live audited content versus the local 18px default. Use each element's DOM audit for final sizes, weights and line heights; do not globally scale screenshots. Article images have clipped corners and intentional alternation rather than generic unshaped rectangles. CTA areas and the expertise quote section use the blue stripe background; local pale/white form sections and partner grids differ visibly.

## Task 1: Route-scoped layout, type and chrome

- [x] Add the opt-in classes and `/parity.css` loading through `build.mjs` and `layout`; no edits to generated files.
- [x] Use the three reference DOM inventories to implement header dimensions, logo treatment, navigation wrapping/active state, controls, body type, section gutters and footer layout in the new scope. Preserve hover and keyboard focus behavior.
- [x] Rebuild and visually compare the header/footer at each width before changing individual page bodies.
- [x] Run `npm test` and `npm run verify` from `app`. Verify the homepage, `/contact` and `/expertises/paneelbouw` retain the previous default templates and style loading. Fix shared regressions before proceeding.

## Task 2: Overlay hero, image treatment, CTA and form variants

- [x] Add the overlay `documentHeader` variant: image, tint/stripes, emphasized title, intro and actions share the reference hero area. Match each width's measured image positioning and text box. Keep explicit line breaks separate from escaped content.
- [x] Add scoped article image shapes, alternating compositions, CTA background and form presentation variants. Do not make every page use the same heading, copy, fields or CTA order.
- [x] Audit each requested page's image inventory against the manifest; use exact live derivatives and record hashes/sizes when packaging missing media. Do not copy the live site's JavaScript or stylesheets into the project.
- [x] Update the existing test that asserts a separate panoramic banner only where the new reference-backed hero invalidates it; keep assertions for correct source image, title and actions. Verify nested machine-builders route links and existing aliases.
- [x] Build, run the 33-test suite and route/asset audit, then follow each page plan for its own capture/review cycle. Do not mark a page complete merely because these shared tasks pass.

## Independent deliverable

All six pages have the scoped primitives available, other routes keep their defaults, and the functional audit passes. No page is yet declared visually complete. Record a local checkpoint; commit only if this workspace later has Git configured.

## Execution record

Implemented and functionally verified; final visual acceptance is tracked separately. The user selected **1920×1080** as primary, with 1440×900, 768×1024 and 390×844 retained. The normalized implementation capture helper supersedes the original planning command so both origins use native viewport tiles and the same settled carousel state.

See the [execution ledger](../execution/2026-11-19-progress.md) for architectural rulings and the [final comparison report](../../../checks/visual-implementation-2026-11-19/review/README.md) for individual results and remaining strict-target failures. Checked implementation/review steps do not declare an open numeric gate passed.
