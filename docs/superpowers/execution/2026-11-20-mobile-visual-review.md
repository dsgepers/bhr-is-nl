# BHR mobile visual review — 20 November 2026

Implementation is available locally on `mobile-parity` at http://localhost:4173. The authored mobile navigation, responsive layouts and device-specific media are implemented. **Strict mobile visual parity is OPEN:** no compared phone/tablet page currently meets every independent visual gate. This is not a claim of a pixel-identical clone. Current desktop pixels are preserved against the immutable local baseline. Six representative phone→desktop rotation captures also preserve those pixels exactly.

## Reference and method

Reference: https://www.bhr-is.nl, with the same path as each local route. Candidate: http://localhost:4173. The live CMS selects separate corporate mobile/tablet/desktop markup and CSS using device cookies and user-agent detection. A narrow desktop window is an invalid phone reference. Shared preview cannot set user agent, touch or screen emulation; the device-correct Playwright capture helper supplies these settings.

Phone uses Android UA, touch and mobile emulation; tablet uses iPad UA and touch; desktop uses desktop UA. Each has explicit corresponding device cookie, DPR1 and visualViewport.scale1. Source corporate-theme stylesheet and actual viewport width are asserted. No source templates, stylesheets or JavaScript were copied into product files; JSON metadata contains source copy, visible heading-break positions and original-media mappings only.

Cookies are denied. Fonts and lazy media settle; finite transitions settle; the first hero and partner slide is fixed. Full pages are assembled from viewport tiles to avoid the live site’s 3D compositor defects; only the first sticky header remains and sticky sidebars become static. Native menu/sticky screenshots are separately captured without full-page tiling; the first hero image is fixed on both sides for those comparisons. No page masks, geometric alignment, metric rescaling or score averaging. Refreshed source representatives retain their original measured heights.

Pixel threshold is 5 for mobile and 0 for desktop. The installed visual-diff comparer supplies mismatch percentage and global SSIM estimate. Strict mobile acceptance requires mismatch≤0.5%, SSIM≥0.985 and absolute page-height delta≤2px. Separate close-clone classification requires mismatch<5% and SSIM>0.93. Desktop acceptance requires byte-equivalent rendered pixels. Every page is independently scored.

Final candidate capture phase: `handoff`; source phase: `baseline` except 360/430px source `final`. Earlier `reviewed`, `review-fixed`, `final-mobile`, `accepted`, `final-N`, `promo-final` and palette captures are development evidence and are not the final acceptance results.

## Results

| Profile | Compared pages | PASS | OPEN | Source unavailable |
|---|---:|---:|---:|---:|
| Phone 390×844 | 76 | 0 | 73 | 3 |
| Phone 360×800 | 21 | 0 | 21 | 0 |
| Phone 430×932 | 21 | 0 | 21 | 0 |
| Tablet 768×1024 | 8 | 0 | 8 | 0 |
| Desktop 1920×1080 | 76 | 76 | 0 | 0 |
| Laptop 1440×900 | 16 | 16 | 0 | 0 |

Final capture build revision: `f8589742e345a3977a593167018759b27045aed156f1c901e15dac8c61269dc7`. All captures assert the frozen build revision while capturing; fetched HTML/styles/modules/JSON/fonts/images must match the served local bytes. Rendering JSON is included in build identity. Stale, incomplete, failed, wrong-theme, wrong-width and mismatched PNG/inventory evidence is rejected. Five older supplementary references failed that last check and were refreshed; capture retries require stable geometry before acceptance. Desktop preservation measures this phase’s effect; it does not certify pre-existing local-versus-live desktop likeness.

The source returned HTTP404 for `/branches/verpakkingsindustrie`, `/privacyverklaring` and `/bedankt`. Their local pages remain available; no invented visual scores are assigned.

## What changed

- Authored compact phone header, hamburger, full-screen phone drawer, submenu drill-down/Back, scroll locking/restoration, keyboard focus handling, native modal close/Escape and reduced-motion behavior. Tablet uses its observed half-width right drawer, backdrop and inline accordions.
- Phone/tablet family layouts across the 76 routes: images, stacked articles, expertise rows, galleries, project cards, step sliders, footers, contact/appointment/application forms and utility pages. Mobile enhancements restore original nodes, order and media on return to desktop.
- Original device-specific image derivatives, visible heading-break metadata, legacy branch strip and region/map content, with source provenance in the asset manifest. Generation guards cover delayed media/content during rotation.
- Native form field mapping, validation, consent, upload size limit and local-only submission contracts are retained. Browser checks abort outgoing delivery requests; none are sent.

## Remaining visual differences

Every OPEN row needs further refinement before calling the site nearly identical. Direct inspection of all 73 primary pairs in 13 contact sheets and representative heatmaps/overlays identified these residual groups:

- Residual hero raster, crop and decorative-band differences on some pages, even where the packaged source image bytes have been verified. No image alignment or masks hide those differences.
- Section heights, article inset/padding and accumulated vertical offsets; branch-strip/card spacing and FAQ controls.
- Quote question wording/options and portions of widget presentation differ from the live CMS widget. Existing payload, validation and local-only behavior are preserved. The measured legacy photo/intro and Service photo-strip/FAQ geometry have been corrected.
- Job header metadata, search vertical placement, cookie preferences and some native input appearance. The compact rounded search and empty/populated clear states are implemented.
- Tablet body typography/section geometry and small drawer spacing differences; phone menu intentionally decodes the source’s malformed Industries label.
- Source content/media availability and local existing content differences remain unmasked.

Contact and appointment page heights match the source exactly, but their remaining pixel/typography/control differences still fail the strict gate. Do not infer acceptance from matching heights.

## Verification

- Node test suite: 132/132 pass (`final-mobile-node.log`).
- Build verifier: 76 routes, 3543 local links and 1655 image/script references (`final-mobile-verify.log`).
- Native browser suite: 14 methods invoked in phone mode and 14 in tablet mode; mode-specific methods deliberately return when inapplicable. Both invocations pass (`handoff-all-browser.log`, `handoff-tablet-browser.log`).
- All 76 phone routes pass layout/overflow/visible field checks (`handoff-all-browser.log`). 360/430px family checks and 767/768/1199/1200 boundary, touch, delayed-resource, teardown and reduced-motion cases pass.
- Sole final reviewer raised11 Important findings; the executor’s12-case review regression suite is GREEN after observed RED cases (`final-mobile-review-browser.log`). See [review and response](2026-11-20-mobile-code-review.md). There was no second review or post-fix reviewer approval.
- Eleven-route native form/control sweep passes with zero deliveries; every legacy wizard step is also exercised by the review suite.
- Six phone→1920 rotation comparisons pass with zero changed pixels (`rotation-report/desktop/report.md`).
- Mobile/tablet JSON asset-reference audit: all referenced originals resolve. `git diff --check` passes.

## Artifacts and direct inspection

Artifacts are under [checks/mobile-parity-2026-11-20](../../../checks/mobile-parity-2026-11-20). They are ignored local evidence, preserved on disk.

- [Complete phone report](../../../checks/mobile-parity-2026-11-20/accepted-report/mobile/report.html) and [metrics JSON](../../../checks/mobile-parity-2026-11-20/accepted-report/mobile/report.json).
- [Standalone comparison gallery](../../../checks/mobile-parity-2026-11-20/gallery/gallery-standalone.html); previewed with html_preview and rendered inline.
- [Desktop preservation report](../../../checks/mobile-parity-2026-11-20/accepted-report/desktop/report.md), [1440px](../../../checks/mobile-parity-2026-11-20/accepted-report/laptop/report.md), [tablet](../../../checks/mobile-parity-2026-11-20/accepted-report/tablet/report.html), [360px](../../../checks/mobile-parity-2026-11-20/accepted-report/phone-small/report.html), [430px](../../../checks/mobile-parity-2026-11-20/accepted-report/phone-large/report.html).
- [Native state metrics](../../../checks/mobile-parity-2026-11-20/accepted-report/states/report.json). Phone and tablet closed/root/about/industries/scrolled frames have independent unmasked comparisons.
- Primary contact sheets `accepted-report/mobile/contact-sheet-01.jpg` through `13.jpg` were directly viewed. Representative appointment and final Service overlays, phone menu pair/heatmap and tablet accordion pair/overlay were directly viewed. Final13 contact sheets were directly inspected after the fix pass.
- Global visual-diff skill unchanged. Repo-local helpers add device-theme assertions, normalized tiling, source heading visibility/media packaging, native flow checks, per-page reports and gallery generation.

## Per-page 390px acceptance

| Page | Status | Mismatch | SSIM | Height delta px |
|---|---|---:|---:|---:|
| `/` | OPEN | 23.791% | 0.83531 | -22 |
| `/expertises` | OPEN | 9.726% | 0.92799 | +38 |
| `/expertises/software-engineering` | OPEN | 32.218% | 0.60945 | +98 |
| `/expertises/hardware-engineering` | OPEN | 29.667% | 0.64617 | -160 |
| `/expertises/paneelbouw` | OPEN | 57.885% | 0.60907 | +34 |
| `/expertises/retrofit` | OPEN | 61.441% | 0.47208 | +157 |
| `/expertises/bekabeling-en-installatie` | OPEN | 48.641% | 0.41096 | +220 |
| `/expertises/machineveiligheid` | OPEN | 29.020% | 0.67795 | -68 |
| `/expertises/cybersecurity` | OPEN | 38.785% | 0.60256 | -93 |
| `/expertises/elektrocomponenten` | OPEN | 11.166% | 0.87727 | -28 |
| `/expertises/inbedrijfstelling` | OPEN | 29.142% | 0.68447 | -36 |
| `/expertises/industriele-automatisering` | OPEN | 26.391% | 0.65074 | -56 |
| `/voor-machinebouwers` | OPEN | 19.573% | 0.76467 | +137 |
| `/voor-machinebouwers/proces-productie` | OPEN | 4.035% | 0.95317 | +17 |
| `/service-en-onderhoud` | OPEN | 13.291% | 0.90191 | -12 |
| `/voor-machinebouwers/voor-machinebouwers` | OPEN | 19.573% | 0.76467 | +137 |
| `/over-ons` | OPEN | 42.688% | 0.56172 | +198 |
| `/over-ons/partners` | OPEN | 7.540% | 0.91371 | +17 |
| `/over-ons/werken-bij` | OPEN | 29.549% | 0.70857 | -112 |
| `/vacature` | OPEN | 18.511% | 0.52396 | +93 |
| `/projecten` | OPEN | 11.937% | 0.88359 | +57 |
| `/projecten/bierskid-besturing-zonder-plc` | OPEN | 21.920% | 0.77582 | -10 |
| `/projecten/sc100` | OPEN | 19.931% | 0.76852 | -10 |
| `/projecten/bouwen-daf-installatie-waterzuivering` | OPEN | 21.430% | 0.79380 | -10 |
| `/projecten/energiebesparing-door-frequentieregelaars` | OPEN | 21.034% | 0.78617 | -10 |
| `/projecten/bouwen-afdelingsinstallatie` | OPEN | 23.072% | 0.75317 | -10 |
| `/projecten/cummins` | OPEN | 21.788% | 0.78673 | -9 |
| `/projecten/retrofit-oplossingen-in-bestaande-machineframe` | OPEN | 21.422% | 0.78615 | -10 |
| `/projecten/kleine-verdelerbouw-tot-630-a` | OPEN | 1.356% | 0.99371 | +0 |
| `/branches/machinebouw` | OPEN | 34.981% | 0.60019 | -202 |
| `/branches/voedingsindustrie` | OPEN | 32.272% | 0.61927 | -191 |
| `/branches/watertechnologie` | OPEN | 23.543% | 0.74101 | -163 |
| `/branches/agro` | OPEN | 33.934% | 0.66534 | +44 |
| `/branches/verpakkingsindustrie` | REFERENCE UNAVAILABLE | — | — | — |
| `/branches/chemie-en-farmacie` | OPEN | 31.748% | 0.63097 | -215 |
| `/branches/energie-en-utiliteit` | OPEN | 34.059% | 0.63294 | -194 |
| `/contact` | OPEN | 11.817% | 0.98405 | +0 |
| `/afspraak-maken` | OPEN | 7.350% | 0.97876 | +0 |
| `/veelgestelde-vragen` | OPEN | 16.162% | 0.80132 | -18 |
| `/zoeken` | OPEN | 20.294% | 0.59964 | +10 |
| `/cookie-instellingen` | OPEN | 26.414% | 0.65591 | +135 |
| `/privacyverklaring` | REFERENCE UNAVAILABLE | — | — | — |
| `/algemene-voorwaarden` | OPEN | 8.581% | 0.91407 | +0 |
| `/bedankt` | REFERENCE UNAVAILABLE | — | — | — |
| `/privacy` | OPEN | 7.751% | 0.90259 | +0 |
| `/pagina-niet-gevonden` | OPEN | 25.308% | 0.42546 | +20 |
| `/offerteaanvraag` | OPEN | 20.016% | 0.81762 | +48 |
| `/branches/productie-industrie` | OPEN | 32.542% | 0.61323 | -263 |
| `/bordenbouw-op-maat` | OPEN | 34.285% | 0.65624 | -158 |
| `/industriele-bordenbouw` | OPEN | 30.959% | 0.68846 | -54 |
| `/bordenbouwer` | OPEN | 35.891% | 0.63561 | -262 |
| `/werken-bij` | OPEN | 28.800% | 0.71591 | -116 |
| `/betrouwbare-paneelbouw-etten-leur` | OPEN | 26.940% | 0.73003 | -78 |
| `/certificering` | OPEN | 32.146% | 0.64156 | +200 |
| `/de-mensen-achter-de-techniek` | OPEN | 26.508% | 0.70768 | -62 |
| `/locaties` | OPEN | 53.198% | 0.66098 | +52 |
| `/locaties/betrouwbare-paneelbouw-voor-industriele-installaties-in-etten-leur` | OPEN | 35.429% | 0.60930 | -96 |
| `/locaties/oisterwijk` | OPEN | 31.391% | 0.70966 | -60 |
| `/locaties/paneelbouw-automatisering-voor-industriele-installaties-in-breda` | OPEN | 43.747% | 0.54119 | -184 |
| `/locaties/paneelbouw-automatisering-voor-machineparken-in-tilburg` | OPEN | 32.983% | 0.63323 | -70 |
| `/locaties/paneelbouw-op-maat-voor-productiebedrijven-in-oosterhout` | OPEN | 26.251% | 0.32287 | +44 |
| `/locaties/paneelbouwer-in-de-regio-dongen` | OPEN | 25.597% | 0.70414 | +46 |
| `/locaties/raamsdonksveer` | OPEN | 36.283% | 0.54862 | +163 |
| `/locaties/s-hertogenbosch` | OPEN | 42.381% | 0.57733 | -143 |
| `/locaties/waalwijk` | OPEN | 32.205% | 0.70744 | -73 |
| `/nieuws` | OPEN | 43.320% | 0.42470 | +173 |
| `/paneelbouw-automatisering-tilburg` | OPEN | 25.039% | 0.73976 | -52 |
| `/paneelbouw-automatisering-voor-machineparken-in-tilburg` | OPEN | 31.197% | 0.67033 | -74 |
| `/paneelbouw-oosterhout` | OPEN | 22.214% | 0.78916 | +10 |
| `/paneelbouwer-dongen` | OPEN | 30.663% | 0.67176 | +97 |
| `/paneelbrouwer-breda` | OPEN | 38.165% | 0.58001 | -160 |
| `/referentie` | OPEN | 23.940% | 0.36908 | +45 |
| `/sitemap` | OPEN | 15.766% | 0.81384 | +20 |
| `/test` | OPEN | 18.042% | 0.81661 | +30 |
| `/vacature/junior-e-plan-engineer` | OPEN | 34.978% | 0.73461 | +17 |
| `/vacature/monteur-paneelbouw` | OPEN | 36.699% | 0.74319 | +25 |
