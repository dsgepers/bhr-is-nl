# Service en onderhoud Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for native implementation, or superpowers:subagent-driven-development if the user selects delegation. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Match the service hero, two articles, five-question FAQ, CTA and compact contact form.

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

Reference: `https://www.bhr-is.nl/service-en-onderhoud`. Candidate: `http://127.0.0.1:4173/service-en-onderhoud`.

Artifacts: [report](../../../checks/visual-planning-2026-11-19/service-en-onderhoud/report.md), [screenshots and DOM/content inventories](../../../checks/visual-planning-2026-11-19/service-en-onderhoud/).

Widths: desktop 1440x900, tablet 768x1024, mobile 390x844, DPR 1. Cookie consent dismissed; no content masks. Full page height is retained; repeated sticky headers are suppressed after the first viewport. See the spec for capture limitations and carousel variance.

| Viewport | Reference size | Local size | Pixel mismatch | SSIM estimate |
| --- | --- | --- | ---: | ---: |
| desktop | 1440×5280 | 1440×5545 | 81.25% | 0.3068 |
| tablet | 768×7190 | 768×6315 | 90.35% | -0.2216 |
| mobile | 390×10994 | 390×6425 | 88.79% | 0.1694 |

These are diagnostic mismatch measurements, not a percentage of likeness. Cumulative vertical offsets can make pixel mismatch very high.

**Dependency:** Complete [2026-11-19-bhr-00-shared-primitives.md](2026-11-19-bhr-00-shared-primitives.md) first.

### Confirmed differences

The page reuses the document template but the live hero is an overlay, with its own service photograph. Local article imagery uses fallback assets. The live testimonial has emphasized text, and the FAQ, CTA and compact “Snel contact” area need matched sizing and composition. `quickContact()` currently removes fields with string/regular-expression replacements, making the rendered form depend on unrelated template formatting.

### Task 1: Match service hero, article photos and FAQ

**Files:** `app/inner-pages.mjs:standardPage`, `app/components.mjs:articleSections, faqSection`, `app/data.mjs`, `app/reference/image-map.json`, `app/assets-manifest.json`, `app/public/parity.css`, `app/tests/inner-pages.test.mjs`.

**Interfaces:** Keep `standardPage(page) -> string`. Preserve `faqSection(all=false, page={}) -> string`, using the five page-specific questions and answers; do not introduce generic FAQ content.

- [x] Add assertions that the service page includes its two captured article headings followed by the page-specific FAQ, CTA and “Snel contact”, and that its primary “Plan uw serviceafspraak” action still leads to `/afspraak-maken`.
- [x] Use exact hero `421_dsc01159.webp`, overlaid heading, intro and service action. Match the image's actual crop and the blue overlay treatment.
- [x] Use exact article images `444_dsc01886.webp` and `451_dsc02462.webp`. Render the separate dark “Service en onderhoud” lead band beneath the hero. Match the first article's direction, clipped image corners, paragraph/list styles and service button. The testimonial is a full-width building-photo background with a blue inset text panel, emphasized “écht” and “Solliciteer nu” button; replace the current generic alternating two-column article.
- [x] Match the FAQ as a two-column section: heading and “Bekijk meer veelgestelde vragen” on the left, the five disclosure rows on the right at desktop. Match separators, plus/minus icons, padding, pale background and responsive stacking. Capture the same closed initial state, then inspect one expanded answer. Preserve keyboard-operable disclosure and existing answer text.
- [x] Build and test the real section order and destination; compare article-to-FAQ and FAQ-to-CTA transitions at all widths.

### Task 2: Match the small contact form explicitly

**Files:** `app/inner-pages.mjs:quickContact`, `app/components.mjs` form helpers, `app/public/parity.css`; `app/public/behavior.mjs` only if a form interface changes.

- [x] Replace `quickContact()`'s destructive HTML string replacements with an explicit compact renderer using the existing form delivery/validation hooks and subject. Match only the two live fields, privacy/terms controls and submit button; omit the personal portrait panel on this variant.
- [x] Match the “Snel contact” heading, form width, white/pale surfaces, required stars, row/column layout and relationship to the striped CTA/footer from the saved reference.
- [x] Exercise both FAQ states, form validation, unconfigured submit feedback and keyboard focus locally; do not submit to the live service.
- [x] Run full functional checks and route review. Reject a score that hides a wrong answer, extra field, missing paragraph or incorrect photograph. Inspect footer placement as well as the first screen.

## Per-page review and completion

- [x] From `app`, run `npm run build`, `npm test` and `npm run verify`; all must pass.
- [x] From the workspace root, with `app/dist` served on port 4173, run `python checks/visual-planning-2026-11-19/run-comparisons.py --route service-en-onderhoud --out checks/visual-review-service-en-onderhoud-<run-id>`.
- [x] Open every width's side-by-side, heatmap and overlay with the visual-diff skill. Review header, hero, each section transition, form and footer. Compare heading boxes, photo crops and page height with the DOM audits; do not rely on metrics alone.
- [ ] Match interactive states and stabilize moving regions before applying the spec's <=0.5% mismatch / >=0.985 SSIM targets. Keep raw unmasked evidence and record any remaining difference explicitly.
- [ ] Review the five failure modes in Review Focus, recheck the homepage and affected shared-template consumers, and record the page's individual result. A failure at one width leaves this page incomplete.
- [x] Record a local checkpoint; commit only if a Git repository has subsequently been initialized.

## Execution record

Implemented and functionally verified; final visual acceptance is tracked separately. The user selected **1920×1080** as primary, with 1440×900, 768×1024 and 390×844 retained. The normalized implementation capture helper supersedes the original planning command so both origins use native viewport tiles and the same settled carousel state.

See the [execution ledger](../execution/2026-11-19-progress.md) for architectural rulings and the [final comparison report](../../../checks/visual-implementation-2026-11-19/review/README.md) for individual results and remaining strict-target failures. Checked implementation/review steps do not declare an open numeric gate passed.
