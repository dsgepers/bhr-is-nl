# Six-page visual baseline

Captured live references and the existing local build on 2026-11-19. Planning evidence; no application changes.

Settings: Chromium, DPR 1, light scheme, nl-NL, Europe/Amsterdam; desktop 1440×900, tablet 768×1024, phone 390×844. Cookie consent dismissed. No content masks. Native viewport tiles preserve layered heroes, with repeated sticky headers suppressed after the first tile. Full document height is retained; horizontal off-canvas carousel overflow is excluded from screenshot width and retained in DOM diagnostics.

Animations/carousels can vary. Metrics diagnose differences; they are not a likeness percentage or an acceptance result. Each full-page report includes side-by-side, heatmap, overlay, computed DOM, rendered text/HTML and image inventory.

| Page | Viewport | Pixel mismatch | SSIM estimate | Live dimensions | Local dimensions |
| --- | --- | ---: | ---: | --- | --- |
| [Expertises](expertises/report.md) | desktop | 88.97% | -0.1328 | 1440×8226 | 1440×7391 |
| [Expertises](expertises/report.md) | tablet | 87.11% | 0.1102 | 768×8659 | 768×9190 |
| [Expertises](expertises/report.md) | mobile | 89.70% | -0.1039 | 390×11176 | 390×9306 |
| [Machinebouwers](machinebouwers/report.md) | desktop | 76.35% | 0.4168 | 1440×7292 | 1440×7521 |
| [Machinebouwers](machinebouwers/report.md) | tablet | 77.00% | 0.0647 | 768×10050 | 768×9552 |
| [Machinebouwers](machinebouwers/report.md) | mobile | 82.25% | -0.0894 | 390×16070 | 390×9885 |
| [Proces & productie](proces-productie/report.md) | desktop | 82.83% | 0.4431 | 1440×5956 | 1440×6155 |
| [Proces & productie](proces-productie/report.md) | tablet | 84.78% | -0.1826 | 768×8483 | 768×7473 |
| [Proces & productie](proces-productie/report.md) | mobile | 79.58% | 0.0195 | 390×14008 | 390×8265 |
| [Service & onderhoud](service-en-onderhoud/report.md) | desktop | 81.25% | 0.3068 | 1440×5280 | 1440×5545 |
| [Service & onderhoud](service-en-onderhoud/report.md) | tablet | 90.35% | -0.2216 | 768×7190 | 768×6315 |
| [Service & onderhoud](service-en-onderhoud/report.md) | mobile | 88.79% | 0.1694 | 390×10994 | 390×6425 |
| [Partners](partners/report.md) | desktop | 87.36% | -0.1131 | 1440×3256 | 1440×3847 |
| [Partners](partners/report.md) | tablet | 90.30% | -0.3031 | 768×3935 | 768×4873 |
| [Partners](partners/report.md) | mobile | 84.98% | -0.0826 | 390×5431 | 390×4603 |
| [Werken bij](werken-bij/report.md) | desktop | 85.28% | -0.1910 | 1440×8202 | 1440×7242 |
| [Werken bij](werken-bij/report.md) | tablet | 83.78% | -0.2174 | 768×9501 | 768×10575 |
| [Werken bij](werken-bij/report.md) | mobile | 78.83% | -0.1177 | 390×14793 | 390×9782 |

All 18 comparisons have matched DPR/zoom diagnostics. Proposed future near-exact target: <=0.5% mismatch, >=0.985 SSIM, height delta <=2px, and manual review of every section and state. No current page passes this target.

## Reports and screenshots

- Expertises: [live page](https://www.bhr-is.nl/expertises), [report](expertises/report.html), [desktop comparison](expertises/desktop-side-by-side.png), [heatmap](expertises/desktop-heatmap.png), [overlay](expertises/desktop-overlay.png). Tablet and phone versions are beside them.
- Machinebouwers: [live page](https://www.bhr-is.nl/voor-machinebouwers/voor-machinebouwers), [report](machinebouwers/report.html), [desktop comparison](machinebouwers/desktop-side-by-side.png), [heatmap](machinebouwers/desktop-heatmap.png), [overlay](machinebouwers/desktop-overlay.png). Tablet and phone versions are beside them.
- Proces & productie: [live page](https://www.bhr-is.nl/voor-machinebouwers/proces-productie), [report](proces-productie/report.html), [desktop comparison](proces-productie/desktop-side-by-side.png), [heatmap](proces-productie/desktop-heatmap.png), [overlay](proces-productie/desktop-overlay.png). Tablet and phone versions are beside them.
- Service & onderhoud: [live page](https://www.bhr-is.nl/service-en-onderhoud), [report](service-en-onderhoud/report.html), [desktop comparison](service-en-onderhoud/desktop-side-by-side.png), [heatmap](service-en-onderhoud/desktop-heatmap.png), [overlay](service-en-onderhoud/desktop-overlay.png). Tablet and phone versions are beside them.
- Partners: [live page](https://www.bhr-is.nl/over-ons/partners), [report](partners/report.html), [desktop comparison](partners/desktop-side-by-side.png), [heatmap](partners/desktop-heatmap.png), [overlay](partners/desktop-overlay.png). Tablet and phone versions are beside them.
- Werken bij: [live page](https://www.bhr-is.nl/over-ons/werken-bij), [report](werken-bij/report.html), [desktop comparison](werken-bij/desktop-side-by-side.png), [heatmap](werken-bij/desktop-heatmap.png), [overlay](werken-bij/desktop-overlay.png). Tablet and phone versions are beside them.

## Assets and functional baseline

`asset-audit.json` records 59 unique-per-page source image references: 37 exact manifest entries, 10 other derivatives of the same photo, and 12 missing image sources. Exact derivatives must be packaged during implementation. Counts include the same asset when used on different pages.

Existing checks passed: 33 tests; 44 routes, 2116 local links and 532 image/script references verified. These checks establish functionality, not visual parity.

## Reproduce

From the project root, serve the current build with `python -m http.server 4173 --bind 127.0.0.1 --directory app/dist`. In another terminal run:

```bash
python checks/visual-planning-2026-11-19/run-comparisons.py --out checks/visual-review-<run-id>
# Add --route expertises (or another page key) for a single page.
```

The helper uses `/tmp/bhr-visual-diff-venv/bin/python` by default. For a persistent Python environment with `playwright`, `pillow` and `numpy`, set `VISUAL_DIFF_PYTHON`; install its Playwright Chromium browser. The skill is loaded from `~/.codex/skills/visual-diff/scripts/compare_page.py`. No application dependencies were installed.

Self-healing: added the repo-local capture adapter, runner and report builder. The global visual-diff skill was not modified. The stale shared-preview screenshots and superseded standard full-page captures are not part of this baseline.

See [plan index](../../docs/superpowers/plans/2026-11-19-bhr-visual-parity.md) and [review record](review.md).
