# BHR mobile visual review — 20 November 2026

Implementation is available locally on `mobile-parity` at http://localhost:4173. The authored mobile navigation, responsive layouts and device-specific media are implemented. **Strict mobile visual parity is OPEN:** no compared phone/tablet page currently meets every independent visual gate. This is not a claim of a pixel-identical clone. Current desktop pixels are preserved against the immutable local baseline.

## Reference and method

Reference: https://www.bhr-is.nl, with the same path as each local route. Candidate: http://localhost:4173. The live CMS selects separate corporate mobile/tablet/desktop markup and CSS using device cookies and user-agent detection. A narrow desktop window is an invalid phone reference. Shared preview cannot set user agent, touch or screen emulation; the device-correct Playwright capture helper supplies these settings.

Phone uses Android UA, touch and mobile emulation; tablet uses iPad UA and touch; desktop uses desktop UA. Each has explicit corresponding device cookie, DPR1 and visualViewport.scale1. Source corporate-theme stylesheet and actual viewport width are asserted. No source templates, stylesheets or JavaScript were copied into product files; JSON metadata contains source copy, visible heading-break positions and original-media mappings only.

Cookies are denied. Fonts and lazy media settle; finite transitions settle; the first hero and partner slide is fixed. Full pages are assembled from viewport tiles to avoid the live site’s 3D compositor defects; only the first sticky header remains and sticky sidebars become static. Native menu/sticky screenshots are separately captured without this full-page normalization. No page masks, geometric alignment, metric rescaling or score averaging. Refreshed source representatives retain their original measured heights.

Pixel threshold is 5 for mobile and 0 for desktop. The installed visual-diff comparer supplies mismatch percentage and global SSIM estimate. Strict mobile acceptance requires mismatch≤0.5%, SSIM≥0.985 and absolute page-height delta≤2px. Separate close-clone classification requires mismatch<5% and SSIM>0.93. Desktop acceptance requires byte-equivalent rendered pixels. Every page is independently scored.

Final candidate capture phase: `reviewed`; source phase: `baseline` except 360/430px source `final`. Earlier `accepted`, `final-N`, `promo-final` and palette captures are development evidence and are not the final acceptance results.

## Results

| Profile | Compared pages | PASS | OPEN | Source unavailable |
|---|---:|---:|---:|---:|
| Phone 390×844 | 76 | 0 | 73 | 3 |
| Phone 360×800 | 21 | 0 | 21 | 0 |
| Phone 430×932 | 21 | 0 | 21 | 0 |
| Tablet 768×1024 | 8 | 0 | 8 | 0 |
| Desktop 1920×1080 | 76 | 76 | 0 | 0 |
| Laptop 1440×900 | 16 | 16 | 0 | 0 |

Final capture build revision(s): `{'192a0e53692be60e470533b23faafebbaa5548698e6c8edd1f67a738dff92b6f': 215}`. All captures assert unchanged build revision while capturing. Desktop preservation measures this phase’s effect; it does not certify pre-existing local-versus-live desktop likeness.

The source returned HTTP404 for `/branches/verpakkingsindustrie`, `/privacyverklaring` and `/bedankt`. Their local pages remain available; no invented visual scores are assigned.

## What changed

- Authored compact phone header, hamburger, full-screen phone drawer, submenu drill-down/Back, scroll locking/restoration, keyboard focus handling, native modal close/Escape and reduced-motion behavior. Tablet uses its observed half-width right drawer, backdrop and inline accordions.
- Phone/tablet family layouts across the 76 routes: images, stacked articles, expertise rows, galleries, project cards, step sliders, footers, contact/appointment/application forms and utility pages. Mobile enhancements restore original nodes, order and media on return to desktop.
- Original device-specific image derivatives, visible heading-break metadata, legacy branch strip and region/map content, with source provenance in the asset manifest. Generation guards cover delayed media/content during rotation.
- Native form field mapping, validation, consent, upload size limit and local-only submission contracts are retained. Browser checks abort outgoing delivery requests; none are sent.

## Remaining visual differences

Every OPEN row needs further refinement before calling the site nearly identical. Direct inspection of all 73 primary pairs in 13 contact sheets and representative heatmaps/overlays identified these residual groups:

- Some hero image exposures/crops, gradient and decorative-band geometry.
- Section heights, article inset/padding and accumulated vertical offsets; branch-strip/card spacing and FAQ controls.
- Legacy hero/intro structure and the quote wizard’s visual treatment differ from the live CMS widget. Existing local form behavior is preserved.
- Job header metadata, search control shape, cookie preferences and some native input appearance.
- Tablet body typography/section geometry and small drawer spacing differences; phone menu intentionally decodes the source’s malformed Industries label.
- Source content/media availability and local existing content differences remain unmasked.

Contact and appointment page heights match the source exactly, but their remaining pixel/typography/control differences still fail the strict gate. Do not infer acceptance from matching heights.

## Verification

- Node test suite: 132/132 pass (`reviewed-final-node.log`).
- Build verifier: 76 routes, 3543 local links and 1655 image/script references (`reviewed-final-verify.log`).
- Native browser suite: 14 methods invoked in phone mode and 14 in tablet mode; mode-specific methods deliberately return when inapplicable. Both invocations pass (`reviewed-final-browser.log`, `reviewed-final-tablet-browser.log`).
- All 76 phone routes pass layout/overflow/visible field checks (`reviewed-all-routes-browser.log`). 360/430px family checks and 767/768/1199/1200 boundary, touch, delayed-resource, teardown and reduced-motion cases pass.
- Mobile/tablet JSON asset-reference audit: all referenced originals resolve. `git diff --check` passes.

## Artifacts and direct inspection

Artifacts are under [checks/mobile-parity-2026-11-20](../../../checks/mobile-parity-2026-11-20). They are ignored local evidence, preserved on disk.

- [Complete phone report](../../../checks/mobile-parity-2026-11-20/accepted-report/mobile/report.html) and [metrics JSON](../../../checks/mobile-parity-2026-11-20/accepted-report/mobile/report.json).
- [Standalone comparison gallery](../../../checks/mobile-parity-2026-11-20/gallery/gallery-standalone.html); previewed with html_preview and rendered inline.
- [Desktop preservation report](../../../checks/mobile-parity-2026-11-20/accepted-report/desktop/report.md), [1440px](../../../checks/mobile-parity-2026-11-20/accepted-report/laptop/report.md), [tablet](../../../checks/mobile-parity-2026-11-20/accepted-report/tablet/report.html), [360px](../../../checks/mobile-parity-2026-11-20/accepted-report/phone-small/report.html), [430px](../../../checks/mobile-parity-2026-11-20/accepted-report/phone-large/report.html).
- [Native state metrics](../../../checks/mobile-parity-2026-11-20/accepted-report/states/report.json). Phone and tablet closed/root/about/industries/scrolled frames have independent unmasked comparisons.
- Primary contact sheets `accepted-report/mobile/contact-sheet-01.jpg` through `13.jpg` were directly viewed. Representative appointment overlay, phone menu pair/heatmap and tablet accordion pair/heatmap were directly viewed.
- Global visual-diff skill unchanged. Repo-local helpers add device-theme assertions, normalized tiling, source heading visibility/media packaging, native flow checks, per-page reports and gallery generation.

## Per-page 390px acceptance

| Page | Status | Mismatch | SSIM | Height delta px |
|---|---|---:|---:|---:|
| `/` | OPEN | 38.928% | 0.72953 | -69 |
| `/expertises` | OPEN | 15.227% | 0.92120 | +38 |
| `/expertises/software-engineering` | OPEN | 36.420% | 0.62270 | +59 |
| `/expertises/hardware-engineering` | OPEN | 36.090% | 0.63081 | -161 |
| `/expertises/paneelbouw` | OPEN | 58.131% | 0.54545 | -135 |
| `/expertises/retrofit` | OPEN | 66.080% | 0.43476 | +245 |
| `/expertises/bekabeling-en-installatie` | OPEN | 40.608% | 0.60671 | +152 |
| `/expertises/machineveiligheid` | OPEN | 27.402% | 0.75538 | -69 |
| `/expertises/cybersecurity` | OPEN | 41.450% | 0.58587 | -94 |
| `/expertises/elektrocomponenten` | OPEN | 35.041% | 0.65087 | -89 |
| `/expertises/inbedrijfstelling` | OPEN | 26.943% | 0.75873 | -97 |
| `/expertises/industriele-automatisering` | OPEN | 19.006% | 0.80579 | -117 |
| `/voor-machinebouwers` | OPEN | 36.732% | 0.62385 | +69 |
| `/voor-machinebouwers/proces-productie` | OPEN | 36.994% | 0.65318 | -51 |
| `/service-en-onderhoud` | OPEN | 54.431% | 0.43415 | -297 |
| `/voor-machinebouwers/voor-machinebouwers` | OPEN | 36.732% | 0.62385 | +69 |
| `/over-ons` | OPEN | 43.880% | 0.55309 | +198 |
| `/over-ons/partners` | OPEN | 19.523% | 0.90570 | +17 |
| `/over-ons/werken-bij` | OPEN | 33.198% | 0.70646 | -112 |
| `/vacature` | OPEN | 42.579% | 0.53078 | +93 |
| `/projecten` | OPEN | 11.937% | 0.88359 | +57 |
| `/projecten/bierskid-besturing-zonder-plc` | OPEN | 36.064% | 0.68725 | -37 |
| `/projecten/sc100` | OPEN | 36.924% | 0.65452 | -48 |
| `/projecten/bouwen-daf-installatie-waterzuivering` | OPEN | 39.952% | 0.67993 | -37 |
| `/projecten/energiebesparing-door-frequentieregelaars` | OPEN | 40.854% | 0.67052 | -37 |
| `/projecten/bouwen-afdelingsinstallatie` | OPEN | 41.606% | 0.63005 | -48 |
| `/projecten/cummins` | OPEN | 35.036% | 0.71564 | -58 |
| `/projecten/retrofit-oplossingen-in-bestaande-machineframe` | OPEN | 40.390% | 0.68548 | -26 |
| `/projecten/kleine-verdelerbouw-tot-630-a` | OPEN | 32.373% | 0.74284 | -60 |
| `/branches/machinebouw` | OPEN | 35.704% | 0.65541 | -262 |
| `/branches/voedingsindustrie` | OPEN | 39.965% | 0.60035 | -251 |
| `/branches/watertechnologie` | OPEN | 29.121% | 0.73670 | -163 |
| `/branches/agro` | OPEN | 39.365% | 0.61018 | -141 |
| `/branches/verpakkingsindustrie` | REFERENCE UNAVAILABLE | — | — | — |
| `/branches/chemie-en-farmacie` | OPEN | 41.628% | 0.59000 | -275 |
| `/branches/energie-en-utiliteit` | OPEN | 37.637% | 0.65336 | -254 |
| `/contact` | OPEN | 11.817% | 0.98405 | +0 |
| `/afspraak-maken` | OPEN | 7.350% | 0.97876 | +0 |
| `/veelgestelde-vragen` | OPEN | 16.162% | 0.80132 | -18 |
| `/zoeken` | OPEN | 26.315% | 0.40262 | +30 |
| `/cookie-instellingen` | OPEN | 26.414% | 0.65591 | +135 |
| `/privacyverklaring` | REFERENCE UNAVAILABLE | — | — | — |
| `/algemene-voorwaarden` | OPEN | 8.581% | 0.91407 | +0 |
| `/bedankt` | REFERENCE UNAVAILABLE | — | — | — |
| `/privacy` | OPEN | 7.751% | 0.90259 | +0 |
| `/pagina-niet-gevonden` | OPEN | 25.308% | 0.42546 | +20 |
| `/offerteaanvraag` | OPEN | 20.016% | 0.81762 | +48 |
| `/branches/productie-industrie` | OPEN | 39.844% | 0.60792 | -263 |
| `/bordenbouw-op-maat` | OPEN | 47.445% | 0.53968 | -316 |
| `/industriele-bordenbouw` | OPEN | 46.445% | 0.52612 | -272 |
| `/bordenbouwer` | OPEN | 48.681% | 0.52359 | -431 |
| `/werken-bij` | OPEN | 32.449% | 0.71384 | -116 |
| `/betrouwbare-paneelbouw-etten-leur` | OPEN | 40.434% | 0.64488 | -105 |
| `/certificering` | OPEN | 32.146% | 0.64156 | +200 |
| `/de-mensen-achter-de-techniek` | OPEN | 37.208% | 0.67721 | -29 |
| `/locaties` | OPEN | 53.198% | 0.66098 | +52 |
| `/locaties/betrouwbare-paneelbouw-voor-industriele-installaties-in-etten-leur` | OPEN | 40.109% | 0.52583 | -156 |
| `/locaties/oisterwijk` | OPEN | 37.145% | 0.62624 | -120 |
| `/locaties/paneelbouw-automatisering-voor-industriele-installaties-in-breda` | OPEN | 47.744% | 0.49675 | -244 |
| `/locaties/paneelbouw-automatisering-voor-machineparken-in-tilburg` | OPEN | 37.819% | 0.54648 | -130 |
| `/locaties/paneelbouw-op-maat-voor-productiebedrijven-in-oosterhout` | OPEN | 26.251% | 0.32287 | +44 |
| `/locaties/paneelbouwer-in-de-regio-dongen` | OPEN | 18.983% | 0.79063 | -14 |
| `/locaties/raamsdonksveer` | OPEN | 32.977% | 0.60015 | +103 |
| `/locaties/s-hertogenbosch` | OPEN | 46.673% | 0.51961 | -203 |
| `/locaties/waalwijk` | OPEN | 38.099% | 0.63569 | -133 |
| `/nieuws` | OPEN | 43.320% | 0.42470 | +173 |
| `/paneelbouw-automatisering-tilburg` | OPEN | 37.138% | 0.67461 | -24 |
| `/paneelbouw-automatisering-voor-machineparken-in-tilburg` | OPEN | 45.097% | 0.59371 | -24 |
| `/paneelbouw-oosterhout` | OPEN | 35.387% | 0.72803 | -28 |
| `/paneelbouwer-dongen` | OPEN | 30.711% | 0.72354 | -61 |
| `/paneelbrouwer-breda` | OPEN | 45.222% | 0.52007 | -220 |
| `/referentie` | OPEN | 23.940% | 0.36908 | +45 |
| `/sitemap` | OPEN | 15.766% | 0.81384 | +20 |
| `/test` | OPEN | 18.042% | 0.81661 | +30 |
| `/vacature/junior-e-plan-engineer` | OPEN | 34.978% | 0.73461 | +17 |
| `/vacature/monteur-paneelbouw` | OPEN | 36.699% | 0.74319 | +25 |
