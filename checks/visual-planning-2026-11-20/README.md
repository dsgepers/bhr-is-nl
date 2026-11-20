# BHR remaining-pages visual planning evidence

Planning only; **no application source changed**. Primary **1920×1080**; regression **1440×900, 768×1024, 390×844**, DPR/zoom 1, light scheme, nl-NL, Europe/Amsterdam.

83 sitemap URL entries normalize to 71 unique valid paths: eight malformed duplicated-origin timeline entries and four duplicate root entries are documented separately. Exclude the homepage and six previously targeted paths: **64 pages remain, 32 existing locally and 32 absent**. Every scoped source returned 200 without redirects.

[Interactive baseline comparisons](comparison-gallery.html) · [Plan index](../../docs/superpowers/plans/2026-11-20-bhr-remaining-pages.md) · [Design](../../docs/superpowers/specs/2026-11-20-bhr-remaining-pages-design.md) · [Scope](routes.json) · [Asset audit](asset-audit.json) · [Link dependencies](link-dependencies.json)

There are **97 reference captures and 65 existing-candidate comparisons**: all 64 pages at 1920px, plus three additional widths for the 11 priority pages. Missing candidates have source-only evidence, never a fabricated 404 similarity score. Other 53 pages need their three responsive baselines during implementation.

Native viewport tiles retain composited imagery. Cookies are dismissed, the pointer is outside the viewport, fonts/images/counters/finite animations settle, and partner tracks are held on the first logical original item. Repeated floating headers and filter clones are suppressed after the original in-flow presentation; review their actual scrolled behavior separately. Both standard and simple headers are covered. **No masks. RGB mismatch threshold 5.** Every comparison reattaches actual DOM sidecars and enforces DPR/zoom equality; image-only CLI missing-metadata warnings from the initial attempt are retained as diagnostics, not accepted as zoom evidence.

The initial project/appointment sticky-header capture artifacts are preserved under `baseline-sticky-diagnostics/`; the selected canonical evidence uses the corrected normalizer. All visible source images have nonzero decoded natural dimensions.

| Page | Viewport | Mismatch | SSIM | Live image / local image | Evidence |
|---|---|---:|---:|---|---|
| [/projecten](https://www.bhr-is.nl/projecten) | 1920 × 1080 | 76.334% | -0.1442 | 1920×8982 / 1920×6278 | [report](baseline/projecten/report.html) |
| [/projecten](https://www.bhr-is.nl/projecten) | 1440 × 900 | 79.166% | -0.1559 | 1440×8024 / 1440×5932 | [report](baseline/projecten/report.html) |
| [/projecten](https://www.bhr-is.nl/projecten) | 768 × 1024 | 78.129% | -0.2279 | 768×7395 / 768×5567 | [report](baseline/projecten/report.html) |
| [/projecten](https://www.bhr-is.nl/projecten) | 390 × 844 | 72.602% | -0.1883 | 390×12611 / 390×8050 | [report](baseline/projecten/report.html) |
| [/projecten/bierskid-besturing-zonder-plc](https://www.bhr-is.nl/projecten/bierskid-besturing-zonder-plc) | 1920 × 1080 | 81.841% | 0.1680 | 1920×4043 / 1920×3878 | [report](baseline/projecten--bierskid-besturing-zonder-plc/report.html) |
| [/projecten/bierskid-besturing-zonder-plc](https://www.bhr-is.nl/projecten/bierskid-besturing-zonder-plc) | 1440 × 900 | 80.829% | 0.0707 | 1440×3749 / 1440×3547 | [report](baseline/projecten--bierskid-besturing-zonder-plc/report.html) |
| [/projecten/bierskid-besturing-zonder-plc](https://www.bhr-is.nl/projecten/bierskid-besturing-zonder-plc) | 768 × 1024 | 95.479% | -0.2608 | 768×3362 / 768×4708 | [report](baseline/projecten--bierskid-besturing-zonder-plc/report.html) |
| [/projecten/bierskid-besturing-zonder-plc](https://www.bhr-is.nl/projecten/bierskid-besturing-zonder-plc) | 390 × 844 | 79.195% | -0.1414 | 390×8393 / 390×4644 | [report](baseline/projecten--bierskid-besturing-zonder-plc/report.html) |
| [/projecten/bouwen-afdelingsinstallatie](https://www.bhr-is.nl/projecten/bouwen-afdelingsinstallatie) | 1920 × 1080 | 85.789% | -0.0784 | 1920×3710 / 1920×3236 | [report](baseline/projecten--bouwen-afdelingsinstallatie/report.html) |
| [/projecten/bouwen-afdelingsinstallatie](https://www.bhr-is.nl/projecten/bouwen-afdelingsinstallatie) | 1440 × 900 | 82.510% | -0.0028 | 1440×3292 / 1440×2905 | [report](baseline/projecten--bouwen-afdelingsinstallatie/report.html) |
| [/projecten/bouwen-afdelingsinstallatie](https://www.bhr-is.nl/projecten/bouwen-afdelingsinstallatie) | 768 × 1024 | 87.739% | -0.1906 | 768×2903 / 768×3632 | [report](baseline/projecten--bouwen-afdelingsinstallatie/report.html) |
| [/projecten/bouwen-afdelingsinstallatie](https://www.bhr-is.nl/projecten/bouwen-afdelingsinstallatie) | 390 × 844 | 73.145% | 0.0226 | 390×6298 / 390×2975 | [report](baseline/projecten--bouwen-afdelingsinstallatie/report.html) |
| [/projecten/bouwen-daf-installatie-waterzuivering](https://www.bhr-is.nl/projecten/bouwen-daf-installatie-waterzuivering) | 1920 × 1080 | 78.149% | 0.4226 | 1920×3644 / 1920×3581 | [report](baseline/projecten--bouwen-daf-installatie-waterzuivering/report.html) |
| [/projecten/bouwen-daf-installatie-waterzuivering](https://www.bhr-is.nl/projecten/bouwen-daf-installatie-waterzuivering) | 1440 × 900 | 76.590% | 0.3998 | 1440×3309 / 1440×3250 | [report](baseline/projecten--bouwen-daf-installatie-waterzuivering/report.html) |
| [/projecten/bouwen-daf-installatie-waterzuivering](https://www.bhr-is.nl/projecten/bouwen-daf-installatie-waterzuivering) | 768 × 1024 | 81.534% | -0.0096 | 768×3782 / 768×4212 | [report](baseline/projecten--bouwen-daf-installatie-waterzuivering/report.html) |
| [/projecten/bouwen-daf-installatie-waterzuivering](https://www.bhr-is.nl/projecten/bouwen-daf-installatie-waterzuivering) | 390 × 844 | 79.141% | -0.3591 | 390×5799 / 390×3811 | [report](baseline/projecten--bouwen-daf-installatie-waterzuivering/report.html) |
| [/projecten/cummins](https://www.bhr-is.nl/projecten/cummins) | 1920 × 1080 | 79.588% | 0.4102 | 1920×3649 / 1920×3581 | [report](baseline/projecten--cummins/report.html) |
| [/projecten/cummins](https://www.bhr-is.nl/projecten/cummins) | 1440 × 900 | 74.219% | 0.4817 | 1440×3259 / 1440×3250 | [report](baseline/projecten--cummins/report.html) |
| [/projecten/cummins](https://www.bhr-is.nl/projecten/cummins) | 768 × 1024 | 93.333% | -0.1630 | 768×2787 / 768×4212 | [report](baseline/projecten--cummins/report.html) |
| [/projecten/cummins](https://www.bhr-is.nl/projecten/cummins) | 390 × 844 | 74.823% | -0.3169 | 390×6077 / 390×3786 | [report](baseline/projecten--cummins/report.html) |
| [/projecten/energiebesparing-door-frequentieregelaars](https://www.bhr-is.nl/projecten/energiebesparing-door-frequentieregelaars) | 1920 × 1080 | 84.164% | 0.0217 | 1920×3649 / 1920×3236 | [report](baseline/projecten--energiebesparing-door-frequentieregelaars/report.html) |
| [/projecten/energiebesparing-door-frequentieregelaars](https://www.bhr-is.nl/projecten/energiebesparing-door-frequentieregelaars) | 1440 × 900 | 81.663% | 0.0526 | 1440×3259 / 1440×2905 | [report](baseline/projecten--energiebesparing-door-frequentieregelaars/report.html) |
| [/projecten/energiebesparing-door-frequentieregelaars](https://www.bhr-is.nl/projecten/energiebesparing-door-frequentieregelaars) | 768 × 1024 | 74.668% | 0.2242 | 768×3848 / 768×3785 | [report](baseline/projecten--energiebesparing-door-frequentieregelaars/report.html) |
| [/projecten/energiebesparing-door-frequentieregelaars](https://www.bhr-is.nl/projecten/energiebesparing-door-frequentieregelaars) | 390 × 844 | 71.377% | -0.1723 | 390×6077 / 390×3176 | [report](baseline/projecten--energiebesparing-door-frequentieregelaars/report.html) |
| [/projecten/kleine-verdelerbouw-tot-630-a](https://www.bhr-is.nl/projecten/kleine-verdelerbouw-tot-630-a) | 1920 × 1080 | 70.033% | 0.6381 | 1920×3256 / 1920×3236 | [report](baseline/projecten--kleine-verdelerbouw-tot-630-a/report.html) |
| [/projecten/kleine-verdelerbouw-tot-630-a](https://www.bhr-is.nl/projecten/kleine-verdelerbouw-tot-630-a) | 1440 × 900 | 65.189% | 0.5771 | 1440×2854 / 1440×2905 | [report](baseline/projecten--kleine-verdelerbouw-tot-630-a/report.html) |
| [/projecten/kleine-verdelerbouw-tot-630-a](https://www.bhr-is.nl/projecten/kleine-verdelerbouw-tot-630-a) | 768 × 1024 | 75.798% | 0.1976 | 768×3696 / 768×4029 | [report](baseline/projecten--kleine-verdelerbouw-tot-630-a/report.html) |
| [/projecten/kleine-verdelerbouw-tot-630-a](https://www.bhr-is.nl/projecten/kleine-verdelerbouw-tot-630-a) | 390 × 844 | 68.794% | -0.2855 | 390×6367 / 390×3670 | [report](baseline/projecten--kleine-verdelerbouw-tot-630-a/report.html) |
| [/projecten/retrofit-oplossingen-in-bestaande-machineframe](https://www.bhr-is.nl/projecten/retrofit-oplossingen-in-bestaande-machineframe) | 1920 × 1080 | 78.827% | 0.4561 | 1920×3644 / 1920×3581 | [report](baseline/projecten--retrofit-oplossingen-in-bestaande-machineframe/report.html) |
| [/projecten/retrofit-oplossingen-in-bestaande-machineframe](https://www.bhr-is.nl/projecten/retrofit-oplossingen-in-bestaande-machineframe) | 1440 × 900 | 78.152% | 0.2855 | 1440×3392 / 1440×3250 | [report](baseline/projecten--retrofit-oplossingen-in-bestaande-machineframe/report.html) |
| [/projecten/retrofit-oplossingen-in-bestaande-machineframe](https://www.bhr-is.nl/projecten/retrofit-oplossingen-in-bestaande-machineframe) | 768 × 1024 | 79.192% | 0.2347 | 768×4195 / 768×4289 | [report](baseline/projecten--retrofit-oplossingen-in-bestaande-machineframe/report.html) |
| [/projecten/retrofit-oplossingen-in-bestaande-machineframe](https://www.bhr-is.nl/projecten/retrofit-oplossingen-in-bestaande-machineframe) | 390 × 844 | 76.763% | -0.3331 | 390×5950 / 390×3842 | [report](baseline/projecten--retrofit-oplossingen-in-bestaande-machineframe/report.html) |
| [/projecten/sc100](https://www.bhr-is.nl/projecten/sc100) | 1920 × 1080 | 83.065% | 0.0316 | 1920×3880 / 1920×3581 | [report](baseline/projecten--sc100/report.html) |
| [/projecten/sc100](https://www.bhr-is.nl/projecten/sc100) | 1440 × 900 | 84.437% | -0.0951 | 1440×3648 / 1440×3250 | [report](baseline/projecten--sc100/report.html) |
| [/projecten/sc100](https://www.bhr-is.nl/projecten/sc100) | 768 × 1024 | 95.069% | -0.3423 | 768×3054 / 768×4227 | [report](baseline/projecten--sc100/report.html) |
| [/projecten/sc100](https://www.bhr-is.nl/projecten/sc100) | 390 × 844 | 79.415% | -0.1947 | 390×6750 / 390×3908 | [report](baseline/projecten--sc100/report.html) |
| [/contact](https://www.bhr-is.nl/contact) | 1920 × 1080 | 52.294% | 0.2924 | 1920×3390 / 1920×3637 | [report](baseline/contact/report.html) |
| [/contact](https://www.bhr-is.nl/contact) | 1440 × 900 | 47.252% | 0.4058 | 1440×3474 / 1440×3612 | [report](baseline/contact/report.html) |
| [/contact](https://www.bhr-is.nl/contact) | 768 × 1024 | 59.868% | 0.4637 | 768×4398 / 768×4478 | [report](baseline/contact/report.html) |
| [/contact](https://www.bhr-is.nl/contact) | 390 × 844 | 92.818% | -0.4050 | 390×5808 / 390×4546 | [report](baseline/contact/report.html) |
| [/afspraak-maken](https://www.bhr-is.nl/afspraak-maken) | 1920 × 1080 | 54.665% | 0.5082 | 1920×2576 / 1920×2674 | [report](baseline/afspraak-maken/report.html) |
| [/afspraak-maken](https://www.bhr-is.nl/afspraak-maken) | 1440 × 900 | 55.575% | 0.5289 | 1440×2504 / 1440×2564 | [report](baseline/afspraak-maken/report.html) |
| [/afspraak-maken](https://www.bhr-is.nl/afspraak-maken) | 768 × 1024 | 72.479% | -0.0287 | 768×2859 / 768×3331 | [report](baseline/afspraak-maken/report.html) |
| [/afspraak-maken](https://www.bhr-is.nl/afspraak-maken) | 390 × 844 | 81.677% | -0.0022 | 390×4250 / 390×3470 | [report](baseline/afspraak-maken/report.html) |
| [/algemene-voorwaarden](https://www.bhr-is.nl/algemene-voorwaarden) | 1920 × 1080 | 48.545% | 0.2185 | 1920×1458 / 1920×1504 | [report](baseline/algemene-voorwaarden/report.html) |
| [/betrouwbare-paneelbouw-etten-leur](https://www.bhr-is.nl/betrouwbare-paneelbouw-etten-leur) | 1920 × 1080 | missing local | — | 1920×6068 / absent | [reference](baseline/betrouwbare-paneelbouw-etten-leur/wide-reference.png) |
| [/bordenbouw-op-maat](https://www.bhr-is.nl/bordenbouw-op-maat) | 1920 × 1080 | missing local | — | 1920×10331 / absent | [reference](baseline/bordenbouw-op-maat/wide-reference.png) |
| [/bordenbouwer](https://www.bhr-is.nl/bordenbouwer) | 1920 × 1080 | missing local | — | 1920×9966 / absent | [reference](baseline/bordenbouwer/wide-reference.png) |
| [/branches/agro](https://www.bhr-is.nl/branches/agro) | 1920 × 1080 | 82.261% | -0.2280 | 1920×9557 / 1920×11164 | [report](baseline/branches--agro/report.html) |
| [/branches/chemie-en-farmacie](https://www.bhr-is.nl/branches/chemie-en-farmacie) | 1920 × 1080 | 82.973% | -0.0027 | 1920×8553 / 1920×6924 | [report](baseline/branches--chemie-en-farmacie/report.html) |
| [/branches/energie-en-utiliteit](https://www.bhr-is.nl/branches/energie-en-utiliteit) | 1920 × 1080 | 93.104% | -0.2032 | 1920×7726 / 1920×6924 | [report](baseline/branches--energie-en-utiliteit/report.html) |
| [/branches/machinebouw](https://www.bhr-is.nl/branches/machinebouw) | 1920 × 1080 | 89.050% | -0.1399 | 1920×10122 / 1920×8821 | [report](baseline/branches--machinebouw/report.html) |
| [/branches/productie-industrie](https://www.bhr-is.nl/branches/productie-industrie) | 1920 × 1080 | missing local | — | 1920×8275 / absent | [reference](baseline/branches--productie-industrie/wide-reference.png) |
| [/branches/voedingsindustrie](https://www.bhr-is.nl/branches/voedingsindustrie) | 1920 × 1080 | 94.294% | -0.0531 | 1920×10566 / 1920×6924 | [report](baseline/branches--voedingsindustrie/report.html) |
| [/branches/watertechnologie](https://www.bhr-is.nl/branches/watertechnologie) | 1920 × 1080 | 92.330% | -0.1491 | 1920×9238 / 1920×8053 | [report](baseline/branches--watertechnologie/report.html) |
| [/certificering](https://www.bhr-is.nl/certificering) | 1920 × 1080 | missing local | — | 1920×3189 / absent | [reference](baseline/certificering/wide-reference.png) |
| [/cookie-instellingen](https://www.bhr-is.nl/cookie-instellingen) | 1920 × 1080 | 96.867% | -0.6246 | 1920×2560 / 1920×1795 | [report](baseline/cookie-instellingen/report.html) |
| [/de-mensen-achter-de-techniek](https://www.bhr-is.nl/de-mensen-achter-de-techniek) | 1920 × 1080 | missing local | — | 1920×4680 / absent | [reference](baseline/de-mensen-achter-de-techniek/wide-reference.png) |
| [/expertises/bekabeling-en-installatie](https://www.bhr-is.nl/expertises/bekabeling-en-installatie) | 1920 × 1080 | 88.197% | 0.2010 | 1920×8038 / 1920×6730 | [report](baseline/expertises--bekabeling-en-installatie/report.html) |
| [/expertises/cybersecurity](https://www.bhr-is.nl/expertises/cybersecurity) | 1920 × 1080 | 92.154% | 0.1599 | 1920×7159 / 1920×5978 | [report](baseline/expertises--cybersecurity/report.html) |
| [/expertises/elektrocomponenten](https://www.bhr-is.nl/expertises/elektrocomponenten) | 1920 × 1080 | 92.620% | -0.1246 | 1920×8401 / 1920×7481 | [report](baseline/expertises--elektrocomponenten/report.html) |
| [/expertises/hardware-engineering](https://www.bhr-is.nl/expertises/hardware-engineering) | 1920 × 1080 | 86.450% | -0.2292 | 1920×8609 / 1920×7333 | [report](baseline/expertises--hardware-engineering/report.html) |
| [/expertises/inbedrijfstelling](https://www.bhr-is.nl/expertises/inbedrijfstelling) | 1920 × 1080 | 85.908% | -0.0803 | 1920×10047 / 1920×4500 | [report](baseline/expertises--inbedrijfstelling/report.html) |
| [/expertises/industriele-automatisering](https://www.bhr-is.nl/expertises/industriele-automatisering) | 1920 × 1080 | 84.544% | -0.0697 | 1920×9788 / 1920×8871 | [report](baseline/expertises--industriele-automatisering/report.html) |
| [/expertises/machineveiligheid](https://www.bhr-is.nl/expertises/machineveiligheid) | 1920 × 1080 | 88.377% | 0.2001 | 1920×6784 / 1920×5626 | [report](baseline/expertises--machineveiligheid/report.html) |
| [/expertises/software-engineering](https://www.bhr-is.nl/expertises/software-engineering) | 1920 × 1080 | 80.991% | -0.0880 | 1920×9467 / 1920×8426 | [report](baseline/expertises--software-engineering/report.html) |
| [/industriele-bordenbouw](https://www.bhr-is.nl/industriele-bordenbouw) | 1920 × 1080 | missing local | — | 1920×10556 / absent | [reference](baseline/industriele-bordenbouw/wide-reference.png) |
| [/locaties](https://www.bhr-is.nl/locaties) | 1920 × 1080 | missing local | — | 1920×3702 / absent | [reference](baseline/locaties/wide-reference.png) |
| [/locaties/betrouwbare-paneelbouw-voor-industriele-installaties-in-etten-leur](https://www.bhr-is.nl/locaties/betrouwbare-paneelbouw-voor-industriele-installaties-in-etten-leur) | 1920 × 1080 | missing local | — | 1920×5419 / absent | [reference](baseline/locaties--betrouwbare-paneelbouw-voor-industriele-installaties-in-etten-leur/wide-reference.png) |
| [/locaties/oisterwijk](https://www.bhr-is.nl/locaties/oisterwijk) | 1920 × 1080 | missing local | — | 1920×6400 / absent | [reference](baseline/locaties--oisterwijk/wide-reference.png) |
| [/locaties/paneelbouw-automatisering-voor-industriele-installaties-in-breda](https://www.bhr-is.nl/locaties/paneelbouw-automatisering-voor-industriele-installaties-in-breda) | 1920 × 1080 | missing local | — | 1920×6417 / absent | [reference](baseline/locaties--paneelbouw-automatisering-voor-industriele-installaties-in-breda/wide-reference.png) |
| [/locaties/paneelbouw-automatisering-voor-machineparken-in-tilburg](https://www.bhr-is.nl/locaties/paneelbouw-automatisering-voor-machineparken-in-tilburg) | 1920 × 1080 | missing local | — | 1920×5039 / absent | [reference](baseline/locaties--paneelbouw-automatisering-voor-machineparken-in-tilburg/wide-reference.png) |
| [/locaties/paneelbouw-op-maat-voor-productiebedrijven-in-oosterhout](https://www.bhr-is.nl/locaties/paneelbouw-op-maat-voor-productiebedrijven-in-oosterhout) | 1920 × 1080 | missing local | — | 1920×2299 / absent | [reference](baseline/locaties--paneelbouw-op-maat-voor-productiebedrijven-in-oosterhout/wide-reference.png) |
| [/locaties/paneelbouwer-in-de-regio-dongen](https://www.bhr-is.nl/locaties/paneelbouwer-in-de-regio-dongen) | 1920 × 1080 | missing local | — | 1920×6544 / absent | [reference](baseline/locaties--paneelbouwer-in-de-regio-dongen/wide-reference.png) |
| [/locaties/raamsdonksveer](https://www.bhr-is.nl/locaties/raamsdonksveer) | 1920 × 1080 | missing local | — | 1920×6098 / absent | [reference](baseline/locaties--raamsdonksveer/wide-reference.png) |
| [/locaties/s-hertogenbosch](https://www.bhr-is.nl/locaties/s-hertogenbosch) | 1920 × 1080 | missing local | — | 1920×6322 / absent | [reference](baseline/locaties--s-hertogenbosch/wide-reference.png) |
| [/locaties/waalwijk](https://www.bhr-is.nl/locaties/waalwijk) | 1920 × 1080 | missing local | — | 1920×6322 / absent | [reference](baseline/locaties--waalwijk/wide-reference.png) |
| [/nieuws](https://www.bhr-is.nl/nieuws) | 1920 × 1080 | missing local | — | 1920×2269 / absent | [reference](baseline/nieuws/wide-reference.png) |
| [/offerteaanvraag](https://www.bhr-is.nl/offerteaanvraag) | 1920 × 1080 | missing local | — | 1920×2238 / absent | [reference](baseline/offerteaanvraag/wide-reference.png) |
| [/over-ons](https://www.bhr-is.nl/over-ons) | 1920 × 1080 | 82.487% | -0.1220 | 1920×8722 / 1920×7925 | [report](baseline/over-ons/report.html) |
| [/pagina-niet-gevonden](https://www.bhr-is.nl/pagina-niet-gevonden) | 1920 × 1080 | missing local | — | 1920×1598 / absent | [reference](baseline/pagina-niet-gevonden/wide-reference.png) |
| [/paneelbouw-automatisering-tilburg](https://www.bhr-is.nl/paneelbouw-automatisering-tilburg) | 1920 × 1080 | missing local | — | 1920×6051 / absent | [reference](baseline/paneelbouw-automatisering-tilburg/wide-reference.png) |
| [/paneelbouw-automatisering-voor-machineparken-in-tilburg](https://www.bhr-is.nl/paneelbouw-automatisering-voor-machineparken-in-tilburg) | 1920 × 1080 | missing local | — | 1920×5283 / absent | [reference](baseline/paneelbouw-automatisering-voor-machineparken-in-tilburg/wide-reference.png) |
| [/paneelbouw-oosterhout](https://www.bhr-is.nl/paneelbouw-oosterhout) | 1920 × 1080 | missing local | — | 1920×5497 / absent | [reference](baseline/paneelbouw-oosterhout/wide-reference.png) |
| [/paneelbouwer-dongen](https://www.bhr-is.nl/paneelbouwer-dongen) | 1920 × 1080 | missing local | — | 1920×8027 / absent | [reference](baseline/paneelbouwer-dongen/wide-reference.png) |
| [/paneelbrouwer-breda](https://www.bhr-is.nl/paneelbrouwer-breda) | 1920 × 1080 | missing local | — | 1920×5726 / absent | [reference](baseline/paneelbrouwer-breda/wide-reference.png) |
| [/privacy](https://www.bhr-is.nl/privacy) | 1920 × 1080 | missing local | — | 1920×1458 / absent | [reference](baseline/privacy/wide-reference.png) |
| [/referentie](https://www.bhr-is.nl/referentie) | 1920 × 1080 | missing local | — | 1920×3109 / absent | [reference](baseline/referentie/wide-reference.png) |
| [/sitemap](https://www.bhr-is.nl/sitemap) | 1920 × 1080 | missing local | — | 1920×2085 / absent | [reference](baseline/sitemap/wide-reference.png) |
| [/test](https://www.bhr-is.nl/test) | 1920 × 1080 | missing local | — | 1920×2141 / absent | [reference](baseline/test/wide-reference.png) |
| [/vacature](https://www.bhr-is.nl/vacature) | 1920 × 1080 | 63.897% | 0.1542 | 1920×1726 / 1920×1969 | [report](baseline/vacature/report.html) |
| [/vacature/junior-e-plan-engineer](https://www.bhr-is.nl/vacature/junior-e-plan-engineer) | 1920 × 1080 | missing local | — | 1920×6181 / absent | [reference](baseline/vacature--junior-e-plan-engineer/wide-reference.png) |
| [/vacature/monteur-paneelbouw](https://www.bhr-is.nl/vacature/monteur-paneelbouw) | 1920 × 1080 | missing local | — | 1920×5951 / absent | [reference](baseline/vacature--monteur-paneelbouw/wide-reference.png) |
| [/veelgestelde-vragen](https://www.bhr-is.nl/veelgestelde-vragen) | 1920 × 1080 | 34.416% | 0.3496 | 1920×3553 / 1920×3339 | [report](baseline/veelgestelde-vragen/report.html) |
| [/voor-machinebouwers](https://www.bhr-is.nl/voor-machinebouwers) | 1920 × 1080 | 69.860% | 0.5666 | 1920×7523 / 1920×7698 | [report](baseline/voor-machinebouwers/report.html) |
| [/werken-bij](https://www.bhr-is.nl/werken-bij) | 1920 × 1080 | missing local | — | 1920×8761 / absent | [reference](baseline/werken-bij/wide-reference.png) |
| [/zoeken](https://www.bhr-is.nl/zoeken) | 1920 × 1080 | 66.152% | -0.1483 | 1920×1698 / 1920×1466 | [report](baseline/zoeken/report.html) |

Baseline functional checks: 45/45 tests; 44 routes, 2116 local links and 590 image/script references. These establish the starting point, not completion of the proposed changes.

Strict implementation target: mismatch ≤0.5%, SSIM estimate ≥0.985, height delta ≤2px per page/width, plus direct visual and functional review. No averaged acceptance or substituted Craft score. No current baseline is certified as a completed fix.

The media audit finds 283 unique visible image URLs, 232 without an exact packaged entry (123 other derivatives of already available photographs and 109 URLs whose photo is absent from the manifest). Planning downloads no replacement application assets. The original images/JSON/text/DOM/HTML are evidence only.

Builder-check decisions: newsletter and `/test` keep local-only truthful feedback until dedicated integrations exist; real contact/appointment/application/quote contracts remain. Broken phone/CMS hrefs use verified local equivalents, `/solliciteer` actions scroll to the inline form, and the valid out-of-scope `/branches` destination stays an explicit public link. Team cards retain their observed WhatsApp affordance; no profile dialog is invented. Details and costs are in the design.

Repo-local capture/catalog/report helpers were added; the global visual-diff skill and all prior-phase evidence were left unchanged. No live form/subscription/application was submitted.
