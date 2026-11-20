# Plan review record

2026-11-19. Review type: native self-review of the plans against source code, live screenshots, rendered content and computed DOM inventories. No independent agent review was claimed or requested.

## Evidence inspected

- All six desktop full-page side-by-side comparisons and heatmaps; representative overlays for Expertises and Careers.
- All six phone and tablet first-screen reference/candidate pairs.
- Per-page heading sequences, image inventories, source renderers, CSS scopes and form templates.
- Existing functional tests: 33 passing. Route audit: 44 routes, 2116 local links and 532 image/script references verified.

## Findings incorporated into the plans

1. Shared document heroes must overlay text on imagery. The current split image/dark-intro template does not match. Preserve explicit page-specific responsive differences.
2. The machine-builders, process and service pages need an additional dark introductory band; replacing only their hero would omit it.
3. Expertises is missing the process slider, hides its final two services and uses the wrong lower-page article direction/image. Its quote form needs a compact white card rather than exposed step labels.
4. Service's second article is actually a full-width photo with a blue text panel. The FAQ is a two-column layout rather than the current full-width list.
5. Partners already gets its full introductory sentence through observed content. Corrected the draft's assumption that the rendered copy omitted it. The main hero difference is full-bleed/overlay treatment and derivative, not absence of any photo.
6. Contact portraits are circular 100×100 elements in a compact contact row, not large rectangular portraits. Surrounding section backgrounds vary by route.
7. Careers facts form a mosaic on a dark workshop background, with white statistic overlays. Values have a blue striped background and four outlined icons. The application section is pale, after the striped CTA; it does not continue the stripes.
8. Careers uses three birth-date selectors and two captured vacancy options, unlike the current native date input and generic option. Retain functioning local validation and file handling when matching presentation.
9. The live mobile/tablet navigation and text layout are unusual. Plans explicitly preserve captured behavior and require a fresh check of Careers' collapsed/overlapping hero before implementing those variants.
10. Rejected stale shared-browser screenshots, replaced standard full-page capture that omitted composited hero text, and hardened sticky-header suppression to include opacity. Only the final normalized six-route run is indexed as the baseline.

## Coverage check

- Six requested URLs map to six separate plans, each with source ownership and exact media identifiers.
- Shared work is a dependency rather than repeated conflicting global CSS edits.
- All plans include three viewport reviews, section/content checks, interactive-state checks and regression checks for shared consumers.
- The missing image/derivative audit is retained separately; no exactness is claimed while substitutes remain.
- The old Craft journal gate is explicitly distinguished from the new visual-diff reports.
- Baseline artifacts are preserved; implementation review commands write to a new directory.
- No application framework migration, live form submission, Git initialization or application runtime edits are part of this planning task.

## Remaining limits

Reference carousels and counters can vary with time; stabilize matching states before strict completion scoring. First-screen gallery images supplement full-page evidence and cannot pass a whole page. Thresholds are a proposed target, and all current pages remain visually incomplete. The final capture report records exact dimensions and matched zoom/DPR for each width.
