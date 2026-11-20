# BHR six-page visual parity design and evidence contract

Date: 2026-11-19. Status: proposed implementation design; planning only.

## Intent and scope

Match the current live renders of these six routes, including their Dutch copy, assets, section sequence, responsive layouts and visible interactions:

1. `/expertises`
2. `/voor-machinebouwers/voor-machinebouwers`
3. `/voor-machinebouwers/proces-productie`
4. `/service-en-onderhoud`
5. `/over-ons/partners`
6. `/over-ons/werken-bij`

The request authorizes investigation, plans and review evidence. Implementation remains a subsequent task. This design preserves the existing custom Node static generator and browser modules.

## Proposed approach

Use shared, measured primitives for the six pages' typography, header, hero variants, articles, CTA, form shell and footer, then explicit page compositions. Scope changes with route classes so the captured homepage and other routes do not inherit unreviewed changes.

Alternatives considered: independent markup/CSS per page is initially simple but duplicates fixes and drifts across widths; global overrides are smaller but the homepage already relies on many fixed-height and breakpoint overrides. Shared primitives with explicit route variants fit the existing code best. This is the planner's recommendation, not a recorded user choice.

## Global constraints

- Keep Node.js >=20, ES modules and the existing static build; add no application framework or runtime dependency.
- Modify source under `app/`; regenerate `app/dist/` with `npm run build`; never hand-edit generated HTML or CSS.
- Package exact original image/font assets locally; do not substitute a differently cropped derivative merely because the photograph matches.
- Preserve Dutch copy, heading emphasis, meaningful line breaks, link destinations, accessible controls and configured form-delivery behavior.
- Limit visual changes to the six requested routes and deliberately reviewed shared primitives; regression-check the homepage and other affected consumers.
- Review each route separately at primary 1920x1080 and secondary 1440x900, 768x1024 and 390x844 CSS pixels, DPR 1, light scheme, nl-NL locale and Europe/Amsterdam timezone.
- Do not use a homepage score, another page's score or an average across widths to pass a route.
- Preserve baseline evidence; save implementation comparisons in a new run directory.

## Evidence and capture method

Baseline lives in `checks/visual-planning-2026-11-19/<page-key>/`. Every route has reference/candidate full-page PNGs, side-by-side PNGs, heatmaps, overlays, content inventories, rendered HTML and computed DOM audits for all three widths. See `report.md`, `report.json` and `report.html` in each directory. The root README indexes all six runs.

The shared T3 preview browser returned stale 1280x800 images while its DOM reported other viewport sizes; those images are excluded. Standard Chromium full-page screenshots also dropped the live site's composited hero text and included off-canvas slider content. `compare-normalized.py` adapts the visual-diff skill to capture actual viewport tiles at native size and join them at their real scroll positions. It includes the header in the first tile and hides repeated sticky headers in later tiles, then restores the page for DOM auditing. Both origins use this identical method. Screenshot width equals the requested viewport; full document height is preserved. Off-canvas horizontal overflow remains visible in DOM `scrollWidth` diagnostics.

Cookie consent is dismissed using `button.cc-allow` on the reference and `[data-consent="accepted"]` locally. No content regions are masked. CSS animations are allowed to settle instead of globally disabling them, because the live site has layered and scroll-driven effects. Carousels remain a source of run-to-run variance; baseline metrics are diagnostic, not proof of exactness.

## Acceptance proposal for implementation

For each route at each width, target pixel mismatch <=0.5% and SSIM estimate >=0.985, plus full-page height within 2 CSS pixels once images and fonts settle. These are proposed near-exact gates from the visual-diff skill, not a promise that the current build passes. Inspect top, middle, form and footer manually; reject wrong copy, missing sections, incorrect photos, broken controls or text clipping regardless of score.

Before strict final metrics, choose and freeze matching carousel slides and hover/FAQ/form states through controls. Keep tracks, container sizes and spacing in the scored image. If an unavoidable third-party or moving region needs a mask, document the smallest mask and review unmasked images separately. Never mask a whole incorrect section to achieve a score. Repeat unstable captures once to establish variance before changing CSS.

The current Craft `verify:likeness` consumes Craft journal evidence, not these visual-diff reports. Do not present it as passing or invent Craft entries. A later implementation may add a separate visual-diff gate, or obtain genuine Craft-compatible evidence. The older 90% requirement is insufficient for the proposed near-exact target.

## Existing functional baseline

On 2026-11-19, `npm test` passed all 33 tests. `npm run verify` checked 44 routes, 2116 local links and 532 image/script references. Those checks do not establish visual likeness. Existing tests that require a separate panoramic document image will need intentional updates against the newly captured live hero, rather than preservation of an inaccurate layout.

## Execution and review order

Shared primitives first, then expertises, machinebouwers, proces-productie, service-en-onderhoud, partners and werken-bij. Each page has a separate implementation plan with source ownership and review criteria. Inspect intermediate page screenshots before moving to the next page; repeat all six after any shared CSS change.

Application runtime code was not changed during planning. Comparison helpers and evidence were added. This workspace is not a Git repository, so no commits or worktrees were created.

## Execution authorization and steering

The user authorized execution after these plans were presented, and subsequently selected 1920px as the primary comparison width. Preserve the original planning evidence and use fresh 1920×1080 references plus the original three regression widths. The local form service’s existing combined 4 MB upload limit remains binding; show that truthful limit even though the live careers copy says 10 MB.
