# BHR visual parity plan index

Planning and visual baseline review, 2026-11-19. No application files were changed.

The recommended implementation keeps the existing static stack, fixes shared visual primitives in an opt-in scope, then completes one page at a time. Each page plan includes observed differences, exact source files and image names, small implementation tasks, functional checks, and a separate visual-diff review loop at desktop, tablet and phone sizes.

## Design and shared work

- [Design, capture method, constraints and acceptance proposal](../specs/2026-11-19-bhr-visual-parity-design.md)
- [Shared primitives: typography, header, heroes, image shapes, form shell and footer](2026-11-19-bhr-00-shared-primitives.md)

## Individual plans, in execution order

| Page | Main work | Plan |
| --- | --- | --- |
| Expertises | Overlay hero; show all ten services; add the missing process slider; correct article, partner strip and quote card | [01 — Expertises](2026-11-19-bhr-01-expertises.md) |
| Voor machinebouwers | Overlay hero and dark lead band; five alternating articles; compact personal contact panel and form | [02 — Machinebouwers](2026-11-19-bhr-02-machinebouwers.md) |
| Proces & productie | Original photos; dark lead band; three articles with the CTA between articles two and three; correct contact heading/form | [03 — Proces & productie](2026-11-19-bhr-03-proces-productie.md) |
| Service en onderhoud | Original photos; lead band; full-width recruitment testimonial; two-column FAQ; compact contact form | [04 — Service](2026-11-19-bhr-04-service-en-onderhoud.md) |
| Partners | Full-bleed hero; sliding partner strip; single-action CTA; personal contact form | [05 — Partners](2026-11-19-bhr-05-partners.md) |
| Werken bij | Recruitment photos; facts mosaic; dark values section/icons; location; application card and matching field controls | [06 — Werken bij](2026-11-19-bhr-06-werken-bij.md) |

## Evidence and review

- [All 18 comparison results and complete artifact links](../../../checks/visual-planning-2026-11-19/README.md)
- [Interactive first-screen comparison gallery](../../../checks/visual-planning-2026-11-19/comparison-gallery.html)
- [Plan self-review and resolved findings](../../../checks/visual-planning-2026-11-19/review.md)
- [Exact-image audit](../../../checks/visual-planning-2026-11-19/asset-audit.json)

Execution steering from the user: use **1920×1080 as the primary desktop reference**, while retaining 1440×900, 768×1024 and 390×844 as regression widths, DPR 1. Proposed near-exact completion target: pixel mismatch <=0.5%, SSIM estimate >=0.985, full-page height within 2 CSS pixels, plus visual and functional review. No averaging across pages or widths. The existing 90% Craft gate does not demonstrate this standard.

The live tablet/phone layout has unusually large navigation and narrow content columns; Careers also has an unusual initial hero at these sizes. These plans follow the reference instead of silently redesigning mobile. Confirm unstable hero/carousel states in fresh captures before fine tuning.

Functional baseline: 33 tests passed; route/asset verification passed for 44 routes, 2116 local links and 532 image/script references. The image inventory found 12 missing original sources and 10 different derivatives of the same photo across the page-specific references.

These are implementation plans for review, not a report of completed visual fixes. Implementation should start only after the user requests it, preserving this baseline and using a new comparison output directory.

Implementation is authorized by the user’s “Execute these plans” request. Progress and rulings are recorded in [the execution ledger](../execution/2026-11-19-progress.md); the planning captures above remain unchanged.

## Execution result — 2026-11-20

All six page compositions and scoped shared primitives are implemented and functionally reviewed. The [final comparison report](../../../checks/visual-implementation-2026-11-19/review/README.md) contains 24 measurements and an interactive 1920px-first gallery. 45 automated tests and 19 browser checks pass. Strict visual acceptance remains open: 8/24 combinations pass the proposed target, including 5/6 at 1920px. Individual plan acceptance checkboxes stay open where their all-width condition is not met.
