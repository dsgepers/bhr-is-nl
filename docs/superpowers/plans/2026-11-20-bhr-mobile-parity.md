# BHR mobile parity implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans inline to implement this plan task-by-task. User preapproved execution and will be away; continue without another permission pause. A builder check found nothing important left.

**Goal:** Match the actual live phone/tablet theme and interactions while leaving current desktop pixels unchanged.

**Architecture:** An authored last-loaded mobile stylesheet, scoped to≤1199px, and an ES module which creates mobile navigation only at that breakpoint. Share family layouts across76 routes; mobile-only DOM enhancements are reversible on resize. Keep current renderers, media, form contracts and desktop assets.

**Tech Stack:** Node20+, static HTML/CSS, vanilla JS ES modules, Python Playwright/Pillow and the installed visual-diff comparer.

**Spec:** `docs/superpowers/specs/2026-11-20-bhr-mobile-parity-design.md`.

## Global constraints

- All76 routes retain working content and local destinations. Original assets only; no source templates/CSS/JS copied into product.
- Actual phone/mobile and tablet themes, DPR1/scale1;390×844 primary.360×800/430×932/768×1024 family checks. Desktop1920×1080 all76 and1440×900 family regressions.
- No product build until immutable current desktop/mobile baseline capture finishes. Record baseline overflow truthfully; no fake comparable score.
- CSS≤1199px only;phone≤767px. Desktop runtime no-op and complete responsive teardown. Preserve prior slider/image/cache fixes.
- No form delivery, source keys, publication or remote Git changes. Keep existing consent/4MB upload and local-only integration contracts.
- Every visual result is per page/width. Strict mobile:≤0.5% mismatch,SSIM≥.985,|height delta|≤2px; OPEN if not met. Separate close-clone classification<5%/.93. Desktop before/after pixels must match.

## Review focus

1. Scroll-position menu open, submenu Back/Escape/backdrop, focus and rotation never strand scrolling/navigation (Task2 browser cases).
2. Wrong source theme,426px overflow and stale bundles never masquerade as mobile evidence (Tasks1/4 capture assertions).
3. Mobile→desktop teardown restores original DOM/order/carousel geometry and1920px screenshots (Tasks2/5/6).
4. Phone form controls/validation/consent/file uploads/local-only behavior remain usable without delivery (Task4 browser cases).
5. Delayed JS, missing media, reduced motion and touch/sticky controls retain access without covering focus (Tasks2/4/5).

### Task 1: Baselines and mobile asset integration

**Files:** tools/audit-mobile.py;public/mobile-parity.css;public/mobile.mjs;components.mjs;build.mjs;tests/mobile.test.mjs;tests/secondary-pages.test.mjs.
**Consumes:** current76-route build and approved checkpoint31188e8. **Produces:** last-loaded media-guarded/versioned mobile resources; original desktop markup untouched except the two inert references; baseline manifest.
- [x] Record baseline130-unit-test result and immutable desktop/mobile frames. Recover any genuine capture failures; mark wrong-width candidates as baseline defects.
- [x] Write node tests proving the new stylesheet has a media guard, new assets are local/versioned, prior markup survives after removing only the two new references, and desktop CSS has no active mobile declarations. Run and observe RED.
- [x] Add resource references and mobile runtime initialization guard. Keep protected raw hash fixtures; normalize only the new asset tags in the comparison, with the new resource tests checking their actual behavior.
- [x] Build and run full node suite plus verifier. Expected:all routes/links/assets resolve and original protected markup still matches.
- [x] Commit this task's code and ledger its evidence.

### Task 2: Header and navigation

**Files:** public/mobile.mjs;public/mobile-parity.css;tools/check-mobile.py.
**Consumes:** mobile resource guard;existing own brand/media/destinations. **Produces:**≤767px compact96px phone header, tablet78px header, authored drawer, subpanels, simple header, state teardown.
- [x] Write/run browser cases for phone menu visibility, root/Industries/Over BHR, Back, close/Escape/backdrop, focus trap/restoration, scroll lock/restoration, resize teardown and JS delay. Observe missing mobile UI RED.
- [x] Implement accessible header/drawer using original local SVG media and Dutch labels. Match live measured spacing, slide transition and colors. Keep simple appointment header source-backed.
- [x] Compare native closed/open/submenu/scrolled states at390 and768; inspect pairs/heatmaps/overlays. Match desktop after resizing back to1920.
- [x] Run cases and full suite;commit and ledger.

### Task 3: Homepage and previous-phase families

**Files:** public/mobile-parity.css;public/mobile.mjs;public/mobile-data.json (only if source-backed mobile content is absent locally);tools/check-mobile.py.
**Consumes:** source device inventories;navigation layer. **Produces:**stacked home sections, eight homepage expertise rows and ten index rows, usable legacy hero/article/service/partner/career/form variants.
- [x] Run failing mobile layout cases for home/expertises/machine-builder/process/service/partners/careers plus paneelbouw/retrofit/verpakkingsindustrie. Pin no overflow, real image widths, section ordering, input widths and step photo/card stacking.
- [x] Implement phone-only family rules; remove old fixed heights/column gaps/transforms at phone widths. Retain the eight observed homepage expertise rows and ten index rows; do not add index-only cards to the homepage. Do not change desktop copy or card inventory.
- [x] Capture and inspect source/local at390 and small/large phone samples. Check sliders, native controls, cookies and footer.
- [x] Run tests;commit and ledger.

### Task 4: Remaining sitemap families

**Files:** public/mobile-parity.css;public/mobile.mjs;tools/check-mobile.py;page-plan-index.json.
**Consumes:** complete per-route source inventory and shared family classes. **Produces:**mobile editorial/branch/location/project/contact/appointment/job/about/utility compositions across all76 routes.
- [x] Write/run browser regressions for each family: no horizontal overflow, vertical article order,100%-width photo/form, horizontal expertise listing rows, source-backed branch strip/grid, usable job/sidebar/share/application, gallery/filter/FAQ/search/quote/cookie states. Include retained form field mappings and zero delivery checks.
- [x] Implement measured phone rules with route exceptions only where inventories differ. Scope all changes to the new mobile file/runtime.
- [x] Use the per-page plan table below to check every route's hero, image order, headings, sections, forms/cards/footer and links; record a source-error disposition instead of a fabricated score.
- [x] Run node/browser/route checks;commit and ledger.

### Task 5: Tablet and responsive boundaries

**Files:** public/mobile-parity.css;public/mobile.mjs;tools/check-mobile.py.
**Consumes:** actual tablet-theme inventories. **Produces:**768px tablet layout and reliable transitions at767/768/1199/1200.
- [x] Write/run tablet/rotation/touch/reduced-motion cases; observe wrong old desktop layouts RED.
- [x] Implement tablet containers/typography/card grids/header/menu and family-specific columns matching reference. Ensure desktop≥1200 remains unchanged.
- [x] Check360/390/430/768 plus breakpoint edges. Verify menu exit and carousel recalculation after rotation. Run suite;commit and ledger.

### Task 6: Visual acceptance and desktop preservation

**Files:** tools/audit-mobile.py;tools/report-mobile.py;checks/mobile-parity-2026-11-20/final;docs/superpowers/execution/2026-11-20-mobile-progress.md.
**Consumes:** frozen implementation. **Produces:**76 phone comparisons and76 desktop before/after records, representative extra widths and interaction states, gallery.
- [x] Capture all76 phone references/candidates with device metadata and all76 local1920 frames against immutable baseline. Capture1440 and extra phone/tablet widths on families.
- [x] Run visual-diff image comparisons, inspect every primary pair and representative heatmaps/overlays; refine observed differences before final review. No masks, score averaging or stale revision reuse.
- [x] Require zero desktop regressions or fix them;label every unresolved mobile gate OPEN and retain evidence.
- [x] Build a self-contained comparison gallery;check with html_preview then show with html_render. Record skill/helper changes.

### Task 7: One final review and handoff

**Files:**execution ledger/review package and relevant tested fixes.
**Consumes:** full task evidence and spec Review Focus. **Produces:**one fresh whole-change code review,one RED→GREEN Important/Critical fix pass,green suite, final report.
- [ ] Dispatch the required fresh reviewer on the most capable available model with plan/spec,full range and Review Focus. No per-task reviewers.
- [ ] Grade findings by user effect;fix Important/Critical once with observed regression tests. Ledger deferred Minors and any rulings.
- [ ] Repeat affected visual/desktop checks after fixes;run full tests and route/asset verifier. Keep local branch and evidence under the user's preapproved local execution scope;no publish/push/merge.

## Per-page plan

Each row inherits its family implementation task and the six exact checks in `checks/mobile-parity-2026-11-20/page-plan-index.json`. Evidence paths are relative to `checks/mobile-parity-2026-11-20/baseline`. The source inventory records measured section/header/field/image geometry; the final row records its independent acceptance gate.

| Page | Family | Live counterpart | Mobile evidence |
|---|---|---|---|
| `/` | homepage | [reference](https://www.bhr-is.nl/) | `home/mobile/reference.json` |
| `/expertises` | expertise-index | [reference](https://www.bhr-is.nl/expertises) | `expertises/mobile/reference.json` |
| `/expertises/software-engineering` | expertise | [reference](https://www.bhr-is.nl/expertises/software-engineering) | `expertises--software-engineering/mobile/reference.json` |
| `/expertises/hardware-engineering` | expertise | [reference](https://www.bhr-is.nl/expertises/hardware-engineering) | `expertises--hardware-engineering/mobile/reference.json` |
| `/expertises/paneelbouw` | legacy-article | [reference](https://www.bhr-is.nl/expertises/paneelbouw) | `expertises--paneelbouw/mobile/reference.json` |
| `/expertises/retrofit` | legacy-article | [reference](https://www.bhr-is.nl/expertises/retrofit) | `expertises--retrofit/mobile/reference.json` |
| `/expertises/bekabeling-en-installatie` | expertise | [reference](https://www.bhr-is.nl/expertises/bekabeling-en-installatie) | `expertises--bekabeling-en-installatie/mobile/reference.json` |
| `/expertises/machineveiligheid` | expertise | [reference](https://www.bhr-is.nl/expertises/machineveiligheid) | `expertises--machineveiligheid/mobile/reference.json` |
| `/expertises/cybersecurity` | expertise | [reference](https://www.bhr-is.nl/expertises/cybersecurity) | `expertises--cybersecurity/mobile/reference.json` |
| `/expertises/elektrocomponenten` | expertise | [reference](https://www.bhr-is.nl/expertises/elektrocomponenten) | `expertises--elektrocomponenten/mobile/reference.json` |
| `/expertises/inbedrijfstelling` | expertise | [reference](https://www.bhr-is.nl/expertises/inbedrijfstelling) | `expertises--inbedrijfstelling/mobile/reference.json` |
| `/expertises/industriele-automatisering` | expertise | [reference](https://www.bhr-is.nl/expertises/industriele-automatisering) | `expertises--industriele-automatisering/mobile/reference.json` |
| `/voor-machinebouwers` | alias | [reference](https://www.bhr-is.nl/voor-machinebouwers) | `voor-machinebouwers/mobile/reference.json` |
| `/voor-machinebouwers/proces-productie` | legacy-article | [reference](https://www.bhr-is.nl/voor-machinebouwers/proces-productie) | `voor-machinebouwers--proces-productie/mobile/reference.json` |
| `/service-en-onderhoud` | legacy-service | [reference](https://www.bhr-is.nl/service-en-onderhoud) | `service-en-onderhoud/mobile/reference.json` |
| `/voor-machinebouwers/voor-machinebouwers` | legacy-article | [reference](https://www.bhr-is.nl/voor-machinebouwers/voor-machinebouwers) | `voor-machinebouwers--voor-machinebouwers/mobile/reference.json` |
| `/over-ons` | company | [reference](https://www.bhr-is.nl/over-ons) | `over-ons/mobile/reference.json` |
| `/over-ons/partners` | legacy-partners | [reference](https://www.bhr-is.nl/over-ons/partners) | `over-ons--partners/mobile/reference.json` |
| `/over-ons/werken-bij` | legacy-careers | [reference](https://www.bhr-is.nl/over-ons/werken-bij) | `over-ons--werken-bij/mobile/reference.json` |
| `/vacature` | vacancy-listing | [reference](https://www.bhr-is.nl/vacature) | `vacature/mobile/reference.json` |
| `/projecten` | project-listing | [reference](https://www.bhr-is.nl/projecten) | `projecten/mobile/reference.json` |
| `/projecten/bierskid-besturing-zonder-plc` | project-detail | [reference](https://www.bhr-is.nl/projecten/bierskid-besturing-zonder-plc) | `projecten--bierskid-besturing-zonder-plc/mobile/reference.json` |
| `/projecten/sc100` | project-detail | [reference](https://www.bhr-is.nl/projecten/sc100) | `projecten--sc100/mobile/reference.json` |
| `/projecten/bouwen-daf-installatie-waterzuivering` | project-detail | [reference](https://www.bhr-is.nl/projecten/bouwen-daf-installatie-waterzuivering) | `projecten--bouwen-daf-installatie-waterzuivering/mobile/reference.json` |
| `/projecten/energiebesparing-door-frequentieregelaars` | project-detail | [reference](https://www.bhr-is.nl/projecten/energiebesparing-door-frequentieregelaars) | `projecten--energiebesparing-door-frequentieregelaars/mobile/reference.json` |
| `/projecten/bouwen-afdelingsinstallatie` | project-detail | [reference](https://www.bhr-is.nl/projecten/bouwen-afdelingsinstallatie) | `projecten--bouwen-afdelingsinstallatie/mobile/reference.json` |
| `/projecten/cummins` | project-detail | [reference](https://www.bhr-is.nl/projecten/cummins) | `projecten--cummins/mobile/reference.json` |
| `/projecten/retrofit-oplossingen-in-bestaande-machineframe` | project-detail | [reference](https://www.bhr-is.nl/projecten/retrofit-oplossingen-in-bestaande-machineframe) | `projecten--retrofit-oplossingen-in-bestaande-machineframe/mobile/reference.json` |
| `/projecten/kleine-verdelerbouw-tot-630-a` | project-detail | [reference](https://www.bhr-is.nl/projecten/kleine-verdelerbouw-tot-630-a) | `projecten--kleine-verdelerbouw-tot-630-a/mobile/reference.json` |
| `/branches/machinebouw` | branch | [reference](https://www.bhr-is.nl/branches/machinebouw) | `branches--machinebouw/mobile/reference.json` |
| `/branches/voedingsindustrie` | branch | [reference](https://www.bhr-is.nl/branches/voedingsindustrie) | `branches--voedingsindustrie/mobile/reference.json` |
| `/branches/watertechnologie` | branch | [reference](https://www.bhr-is.nl/branches/watertechnologie) | `branches--watertechnologie/mobile/reference.json` |
| `/branches/agro` | branch | [reference](https://www.bhr-is.nl/branches/agro) | `branches--agro/mobile/reference.json` |
| `/branches/verpakkingsindustrie` | legacy-article | [reference](https://www.bhr-is.nl/branches/verpakkingsindustrie) | `branches--verpakkingsindustrie/mobile/reference.json` |
| `/branches/chemie-en-farmacie` | branch | [reference](https://www.bhr-is.nl/branches/chemie-en-farmacie) | `branches--chemie-en-farmacie/mobile/reference.json` |
| `/branches/energie-en-utiliteit` | branch | [reference](https://www.bhr-is.nl/branches/energie-en-utiliteit) | `branches--energie-en-utiliteit/mobile/reference.json` |
| `/contact` | contact | [reference](https://www.bhr-is.nl/contact) | `contact/mobile/reference.json` |
| `/afspraak-maken` | appointment | [reference](https://www.bhr-is.nl/afspraak-maken) | `afspraak-maken/mobile/reference.json` |
| `/veelgestelde-vragen` | utility | [reference](https://www.bhr-is.nl/veelgestelde-vragen) | `veelgestelde-vragen/mobile/reference.json` |
| `/zoeken` | utility | [reference](https://www.bhr-is.nl/zoeken) | `zoeken/mobile/reference.json` |
| `/cookie-instellingen` | utility | [reference](https://www.bhr-is.nl/cookie-instellingen) | `cookie-instellingen/mobile/reference.json` |
| `/privacyverklaring` | legacy-article | [reference](https://www.bhr-is.nl/privacyverklaring) | `privacyverklaring/mobile/reference.json` |
| `/algemene-voorwaarden` | utility | [reference](https://www.bhr-is.nl/algemene-voorwaarden) | `algemene-voorwaarden/mobile/reference.json` |
| `/bedankt` | legacy-article | [reference](https://www.bhr-is.nl/bedankt) | `bedankt/mobile/reference.json` |
| `/privacy` | utility | [reference](https://www.bhr-is.nl/privacy) | `privacy/mobile/reference.json` |
| `/pagina-niet-gevonden` | utility | [reference](https://www.bhr-is.nl/pagina-niet-gevonden) | `pagina-niet-gevonden/mobile/reference.json` |
| `/offerteaanvraag` | quote | [reference](https://www.bhr-is.nl/offerteaanvraag) | `offerteaanvraag/mobile/reference.json` |
| `/branches/productie-industrie` | branch | [reference](https://www.bhr-is.nl/branches/productie-industrie) | `branches--productie-industrie/mobile/reference.json` |
| `/bordenbouw-op-maat` | seo | [reference](https://www.bhr-is.nl/bordenbouw-op-maat) | `bordenbouw-op-maat/mobile/reference.json` |
| `/industriele-bordenbouw` | seo | [reference](https://www.bhr-is.nl/industriele-bordenbouw) | `industriele-bordenbouw/mobile/reference.json` |
| `/bordenbouwer` | seo | [reference](https://www.bhr-is.nl/bordenbouwer) | `bordenbouwer/mobile/reference.json` |
| `/werken-bij` | alias | [reference](https://www.bhr-is.nl/werken-bij) | `werken-bij/mobile/reference.json` |
| `/betrouwbare-paneelbouw-etten-leur` | seo | [reference](https://www.bhr-is.nl/betrouwbare-paneelbouw-etten-leur) | `betrouwbare-paneelbouw-etten-leur/mobile/reference.json` |
| `/certificering` | company | [reference](https://www.bhr-is.nl/certificering) | `certificering/mobile/reference.json` |
| `/de-mensen-achter-de-techniek` | company | [reference](https://www.bhr-is.nl/de-mensen-achter-de-techniek) | `de-mensen-achter-de-techniek/mobile/reference.json` |
| `/locaties` | location-listing | [reference](https://www.bhr-is.nl/locaties) | `locaties/mobile/reference.json` |
| `/locaties/betrouwbare-paneelbouw-voor-industriele-installaties-in-etten-leur` | location-detail | [reference](https://www.bhr-is.nl/locaties/betrouwbare-paneelbouw-voor-industriele-installaties-in-etten-leur) | `locaties--betrouwbare-paneelbouw-voor-industriele-installaties-in-etten-leur/mobile/reference.json` |
| `/locaties/oisterwijk` | location-detail | [reference](https://www.bhr-is.nl/locaties/oisterwijk) | `locaties--oisterwijk/mobile/reference.json` |
| `/locaties/paneelbouw-automatisering-voor-industriele-installaties-in-breda` | location-detail | [reference](https://www.bhr-is.nl/locaties/paneelbouw-automatisering-voor-industriele-installaties-in-breda) | `locaties--paneelbouw-automatisering-voor-industriele-installaties-in-breda/mobile/reference.json` |
| `/locaties/paneelbouw-automatisering-voor-machineparken-in-tilburg` | location-detail | [reference](https://www.bhr-is.nl/locaties/paneelbouw-automatisering-voor-machineparken-in-tilburg) | `locaties--paneelbouw-automatisering-voor-machineparken-in-tilburg/mobile/reference.json` |
| `/locaties/paneelbouw-op-maat-voor-productiebedrijven-in-oosterhout` | location-detail | [reference](https://www.bhr-is.nl/locaties/paneelbouw-op-maat-voor-productiebedrijven-in-oosterhout) | `locaties--paneelbouw-op-maat-voor-productiebedrijven-in-oosterhout/mobile/reference.json` |
| `/locaties/paneelbouwer-in-de-regio-dongen` | location-detail | [reference](https://www.bhr-is.nl/locaties/paneelbouwer-in-de-regio-dongen) | `locaties--paneelbouwer-in-de-regio-dongen/mobile/reference.json` |
| `/locaties/raamsdonksveer` | location-detail | [reference](https://www.bhr-is.nl/locaties/raamsdonksveer) | `locaties--raamsdonksveer/mobile/reference.json` |
| `/locaties/s-hertogenbosch` | location-detail | [reference](https://www.bhr-is.nl/locaties/s-hertogenbosch) | `locaties--s-hertogenbosch/mobile/reference.json` |
| `/locaties/waalwijk` | location-detail | [reference](https://www.bhr-is.nl/locaties/waalwijk) | `locaties--waalwijk/mobile/reference.json` |
| `/nieuws` | news | [reference](https://www.bhr-is.nl/nieuws) | `nieuws/mobile/reference.json` |
| `/paneelbouw-automatisering-tilburg` | seo | [reference](https://www.bhr-is.nl/paneelbouw-automatisering-tilburg) | `paneelbouw-automatisering-tilburg/mobile/reference.json` |
| `/paneelbouw-automatisering-voor-machineparken-in-tilburg` | seo | [reference](https://www.bhr-is.nl/paneelbouw-automatisering-voor-machineparken-in-tilburg) | `paneelbouw-automatisering-voor-machineparken-in-tilburg/mobile/reference.json` |
| `/paneelbouw-oosterhout` | seo | [reference](https://www.bhr-is.nl/paneelbouw-oosterhout) | `paneelbouw-oosterhout/mobile/reference.json` |
| `/paneelbouwer-dongen` | seo | [reference](https://www.bhr-is.nl/paneelbouwer-dongen) | `paneelbouwer-dongen/mobile/reference.json` |
| `/paneelbrouwer-breda` | seo | [reference](https://www.bhr-is.nl/paneelbrouwer-breda) | `paneelbrouwer-breda/mobile/reference.json` |
| `/referentie` | company | [reference](https://www.bhr-is.nl/referentie) | `referentie/mobile/reference.json` |
| `/sitemap` | utility | [reference](https://www.bhr-is.nl/sitemap) | `sitemap/mobile/reference.json` |
| `/test` | quote | [reference](https://www.bhr-is.nl/test) | `test/mobile/reference.json` |
| `/vacature/junior-e-plan-engineer` | vacancy-detail | [reference](https://www.bhr-is.nl/vacature/junior-e-plan-engineer) | `vacature--junior-e-plan-engineer/mobile/reference.json` |
| `/vacature/monteur-paneelbouw` | vacancy-detail | [reference](https://www.bhr-is.nl/vacature/monteur-paneelbouw) | `vacature--monteur-paneelbouw/mobile/reference.json` |
