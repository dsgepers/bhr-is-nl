# BHR remaining pages: visual parity design

This is a proposed design and planning deliverable, not authorization to implement. The user requested page-by-page plans and visual comparisons for projects, contact, appointment, and the remaining public sitemap pages. No application source is changed in this planning phase.

## Intent and boundaries

Make each scoped local page visually match its live BHR equivalent. Keep the static Node.js >=20 / ES modules / HTML / CSS / vanilla-browser-JavaScript stack and existing delivery configuration. Use original public images, fonts and SVG media locally; author application HTML, CSS and JavaScript ourselves. Reference HTML and computed styles are evidence only, never application source.

The user's existing preference persists: **1920×1080 is primary**. Review implementation at **1920×1080, 1440×900, 768×1024 and 390×844**, DPR 1, browser zoom 1, light scheme, nl-NL, Europe/Amsterdam. Preserve the reference's Dutch text, emphasis and unusually narrow responsive layouts. This task is neither an editorial rewrite nor a mobile redesign.

Scope is the 64 normalized paths in `checks/visual-planning-2026-11-20/routes.json`: project listing, all eight project details, contact, appointment, and 53 other sitemap pages. Exclude the homepage and the six explicitly addressed routes from the previous phase. Normalize duplicate root/hash entries and reject the eight malformed duplicated-origin timeline URLs; do not manufacture public routes for them. Their original strings remain in `sitemap-invalid.json`.

32 scoped paths already have local HTML; 32 do not. A missing local route is an implementation gap, **not a scored comparison against a 404 page**. Preserve existing local routes absent from the public sitemap. The 12 routes outside this phase are pinned in `protected-route-hashes.json`, including the homepage, the previous six parity pages, paneelbouw, retrofit, verpakkingsindustrie, privacyverklaring and bedankt. Their generated HTML must retain its baseline hash. Previous open visual gates remain open; this phase must not silently certify or overwrite them.

## Approaches considered

1. Extend generic `titleSection` / `articleSections` globally. Fewer files, but would change the homepage's consumers and the already reviewed routes; it cannot express the appointment composition, project galleries or page-specific empty states reliably.
2. Add a route-scoped second parity layer with explicit content and family renderers. **Recommended and used for these plans**, continuing the established architecture. Adds focused files but keeps existing defaults and lets every page ship independently.
3. Replace the static site with another framework or embed reference screenshots. Adds migration work or produces non-functional pages, so it does not meet the task.

This is the planner's architecture recommendation, not an additional user-selected platform. The existing project and requested visual task leave no useful platform decision unresolved.

## Evidence and review method

Read the original sitemap snapshot, not the generated local sitemap, to decide scope. Every path gets a fresh full-document 1920px live capture and page inventory. Existing local routes also get a candidate capture, side-by-side, heatmap, overlay and metrics. The 11 priority pages additionally get the other three widths. Other pages' responsive capture work is an explicit implementation prerequisite; an unaudited width is never marked passed.

Evidence lives under `checks/visual-planning-2026-11-20/baseline/<key>/`. `wide-reference-content.json` inventories public text, links and media; `wide-reference-inventory.json` records visible headings, article ordering, geometry, forms, options, imagery and media. Raw reference HTML remains available to verify rich emphasis and CMS required-field metadata. Interpret `data-validation="Y"` / a `.required` field wrapper as required even when the input's HTML `required` property is false. Do not transfer public CMS delivery identifiers or keys into the application.

Use the repo-local visual-diff runner and native viewport tiling, because off-screen composited layers can disappear in Chromium full-document captures. Dismiss cookies; park the pointer outside the viewport; let fonts, finite transitions and counters settle. Hold partner strips on the same logical first item. Suppress repeated floating headers and sticky filter clones after the first tile without removing their original in-flow presentation; both simple and standard headers must be handled. Compare normal header/filter behavior separately in scrolled viewport captures. Document any animated hero, map, video or remote content that cannot be made deterministic. No masks are used in the planning baseline.

Cached image comparison must reattach its actual DOM sidecars before enforcing DPR/zoom equality: the skill CLI does not infer those sidecars from PNGs. The runner asserts actual dimensions, DPR and scale during live capture; `finalize-evidence.py` restores measured metadata and rejects a real mismatch. This is a tooling correction, not permission to ignore zoom failures.

For implementation review, run each page at all four widths and inspect images directly. Proposed strict target: **pixel mismatch ≤0.5%, SSIM estimate ≥0.985, full-page height delta ≤2 CSS pixels**, individually for every page/width. A failure leaves that page's strict acceptance open. Never average across pages, call mismatch a likeness percentage, or equate the separate Craft score with these reports. Report a close clone separately if appropriate (<5% mismatch, SSIM >0.93); do not relabel it as a strict pass.

## Architecture and exact interfaces

Keep `app/data.mjs`, the default templates, and their shared project/branch arrays stable. The source branch taxonomy differs from the old local taxonomy; source photo derivatives also differ by use. A listing fix must not change the photographs on the homepage or previous Expertises page through a shared array.

Create `app/secondary-data.mjs` and `app/secondary-content.json`. Export `secondaryContent: Record<string, SecondaryPageSpec>`, keyed by the exact normalized route. Add only pages whose implementation is ready. `SecondaryPageSpec` has `route`, `title`, `documentTitle`, `canonical`, `kind`, `header: 'standard'|'simple'`, `headingParts`, `intro`, `hero`, `blocks`, `actions`, plus family-specific `projects`, `fields`, `faq`, `gallery`, `locations`, `formMode` or `aliasTarget` when used. Do not require a photo on a page without one. Author the data from the reviewed public inventory; do not render saved HTML snapshots.

Create `app/secondary-pages.mjs`:

- `secondaryPage(route: string) -> string`: returns the authored body for a known manifest entry; throws for an unknown route.
- `secondaryOptions(route: string) -> {title: string, classes: string, simple: boolean, documentTitle: string, canonical: string}`: returns `secondary parity-page secondary-parity secondary-<kind>` plus a route-specific class, and the measured header variant. Alias entries additionally retain their canonical composition’s `parity-machinebouwers` or `parity-werken-bij` class so its body styles work; their own canonical metadata still names the requested root URL.

Create focused family renderers:

- `app/secondary-projects.mjs`: `projectListingPage(spec) -> string` and `projectDetailPage(spec) -> string`.
- `app/secondary-forms.mjs`: `secondaryContactForm(spec) -> string` and `secondaryQuoteForm(spec) -> string`.
- `app/secondary-components.mjs`: `secondaryHero(spec) -> string`, `secondaryArticle(block,index) -> string`, `secondaryCta(spec) -> string`, `secondarySteps(spec) -> string`, `secondaryPartners(spec) -> string`, and `secondaryTeam(spec) -> string`.
- The `secondary-pages.mjs` dispatch composes editorial, service, branch, location, vacancy, listing, FAQ, quote and utility bodies from these helpers and their explicit ordered blocks. Do not append a generic CTA, contact form, FAQ or photo if absent from that route's source.

In `app/build.mjs`, the existing `add(url,title,body,cls,simple)` checks the secondary manifest only for exact route matches and replaces body/options for opted-in pages. After existing routes, add manifest routes that were not already emitted. Reject duplicate paths. Keep existing aliases functional. Routing an existing page and creating a missing page therefore use the same opt-in interface. If all 32 absent routes become ordinary static pages, the initial 44-route build becomes 76 routes; record actual totals after source redirect/error dispositions are implemented.

Add `app/public/secondary-parity.css`, loaded only when the class includes `secondary-parity`, after `parity.css`. Every rule is scoped to `.secondary-parity` or its route-specific descendant. Reuse existing exact font assets and SVG media. Use the already measured shared colors and stripe profiles where the source agrees; use the new page inventories for each new geometry. Avoid appending new broad `.parity-page` overrides that would change the previous six pages.

Extend `layout(title,body,cls='',simple=false,meta={})` with optional `meta.documentTitle` and `meta.canonical`; only opted-in calls supply the exact captured document title and canonical, avoiding a duplicated “| BHR” suffix. Its default four-argument output remains byte-identical. Extend `header(simple=false,parity=false,options={})` with `options.backHref`, default `/`; the new appointment scope supplies the captured `/pagina-niet-gevonden` destination. Extend `footer(parity=false, options={})` with `options.privacyHref`, defaulting to the existing `/privacyverklaring`. For the new secondary scope only, `layout` supplies `/privacy` to match the live routes. Its old call signature and output remain unchanged for protected consumers. New body links use the actual local destination once created; contact/quote pages must not keep routing their primary actions to a substitute flow when the exact route is now in scope.

Keep common `site.mjs` delivery, cookie, search and lightbox behavior. Add `app/public/secondary.mjs` only for new opt-in project filter/gallery and local-only form behavior, loaded only in the new scope. Do not attach a second handler to controls already handled by `site.mjs`. New process/partner markup can reuse its existing `data-carousel` behavior after checking the geometry. Gallery controls use `data-project-gallery`; filter controls use `data-project-filter`; any repeated sticky filter uses `data-project-sticky`. Team cards expose their observed WhatsApp link on hover and keyboard focus; do not invent a profile dialog.

Add pure helpers in `app/public/secondary-behavior.mjs` only where needed by meaningful tests. `selectedProjectGroup(search: string) -> null|'1'|'2'|'3'` reads `filter_projectgroup[]`; no/unknown value returns null. `projectGalleryIndex(index: number,delta: number,count: number) -> number` clamps at 0 and count−1. The interaction audit observed source gallery indices 0,1,2,3,4,4,4 and a Paneelbouw URL of `?filter_projectgroup%5B%5D=2` with exactly four matching rows. Do not invent a third visible project category merely because its hidden radio exists in source HTML.

## Priority page requirements

### Project listing and eight details

The live listing uses a dark striped title area, two visible category choices, a scrolled sticky filter, category headings, and eight large horizontal image/text rows. Four rows expose multi-image galleries with thumbnails and previous/next controls. The current local card grid, substitute photographs, truncated copy and three visible checkbox categories are materially different. Capture and implement both the default view and selected category behavior. Preserve all eight detail destinations.

Each detail has its own panoramic derivative, overlaid title/intro, separate dark category/lead band and two alternating clipped photo/text articles, then the footer. Do not add a listing gallery or CTA indiscriminately to every detail. Pin the exact H1, lead and article text per route. In particular the live Cummins page has the surprising H1 “Energiebesparing door frequentieregelaars.”; copying it is intentional, not a request to rewrite it.

### Contact

Match the dark striped top composition, contact details and the original `459_dsc02204.webp` photo. At 1920px, the H1 is 65px at x=200/y=153 in a 620px box; the photo is x=960/y≈176.34, 760×≈615.66. Match the compact circular Henk contact panel beside the bordered white form, then the centered single-person team presentation and its observed WhatsApp hover/focus interaction. The current large rectangular portrait and left-aligned team block are not equivalent. The first four fields are required by CMS metadata; Bericht is optional. Consent stays unchecked and required under the local delivery contract.

### Appointment

Use the special simple header and one dark striped first section: a small photograph (`797_dsc00930.webp`) and 35px “Maak een afspraak” H1 on the left, the white appointment form on the right. At 1920px the photo is 470×≈220.31 at x=200/y=123; the H1 is x=200/y≈403.31. Do not apply the ordinary 65px overlay hero or put the form in a second full-width contact section. Restore the pale “Hoe BHR werkt” slider below with its exact `437_dsc02673.webp` photo, source step wording and controls. Do not add the Henk contact panel visibly when the live appointment composition hides it.

## Remaining sitemap pages

Write a separate plan per normalized path, even for shared families. Each plan pins its own headings, article sequence, image URLs, form/FAQ/CTA composition, current owner and missing-route status. Location and SEO landing pages must not be collapsed into one generic page with only a town name substituted. Service and branch pages differ in heading order, embedded branch/service lists, FAQ placement, process blocks and CTA wording. Empty or utility pages follow their actual source presentation without invented company/legal copy. Alias/redirect candidates require observed status, final URL and canonical evidence before choosing a redirect rather than an authored page. Malformed sitemap entries are documented instead of repaired into guessed routes.

## Behavior and delivery constraints

Preserve existing field delivery names, subjects and configured/unconfigured feedback. Map presentation labels to those local names explicitly; public CMS names such as `address.first_name` do not justify renaming the local company field. No real form submissions, applications, emails or booking requests during planning or verification. Block outgoing mutation requests in browser checks. Exercise invalid, optional, consent and safe unconfigured flows locally after implementation. Keep the established combined 4 MB upload limit and truthful 4 MB help where uploads exist, even if a public help line says 10 MB. Do not import production credentials.

Filters, galleries, lightboxes, FAQ disclosures, process/partner controls, search, cookie preferences, team contact links and wizard navigation must remain usable with keyboard and touch. Match the reference initial view, then review selected, expanded, hover/focus and error states. Honor reduced motion. Do not copy inaccessible source-only click behavior when a normal button or link can preserve the same appearance and supply keyboard access.

## Test and acceptance contracts

Baseline: 45/45 tests; 44 routes / 2116 local links / 590 image/script references. Run `npm --prefix app run build`, `npm --prefix app test` and `npm --prefix app run verify` after each independently implemented page/family. Add route-specific structural/asset/link tests in `app/tests/secondary-pages.test.mjs`; pure behavior tests in `app/tests/secondary-behavior.test.mjs`; form semantics/delivery tests in the existing form suite or a focused secondary form suite. Watch each new regression fail before implementing the feature. Do not write unit tests that merely restate CSS; visual-diff and measured browser boxes verify styles.

Every page's test pins its exact H1/content sequence and original image inventory from its plan, expected route creation when absent, destinations and relevant behavior. The shared regression test checks all 12 protected route hashes, manifest path uniqueness and isolation of CSS/script loading. Intentionally update old tests only where the new reference-backed layout invalidates their old visual structure; retain delivery, route and accessibility guarantees.

Implementation review command, from the workspace root:

`/tmp/bhr-visual-diff-venv/bin/python checks/visual-planning-2026-11-20/run-comparisons.py --route <key> --all-widths --out checks/visual-review-remaining-<run-id>`

After each capture, inspect full-page side-by-side, heatmap and overlay plus native crops of the header, title, gallery/form, section boundaries and footer. Verify actual H1/photo/form boxes and total height. Save all four results individually; do not reuse the planning output directory. Review scrolled sticky states separately so tiled normalization cannot conceal a broken sticky filter/header.

## Planning completion and implementation handoff

Planning is complete only when every scoped path has an inventory disposition, a page plan, visual evidence or an explicit live-capture error, and a review entry. The plan index links all pages and distinguishes the 11 four-width baselines from the other 53 primary-only baselines. Include missing local routes and any source error/redirect in that index. Run a fresh builder check of this design, resolve questions against the existing evidence, and self-review the final plans for scope, signatures, dependencies, tests and five Review Focus items. Application implementation waits for the user's next instruction.

This workspace has no Git repository. Keep a source snapshot/hash ledger for future implementation; do not invent commits/worktrees or initialize Git as part of this visual task. Publishing, production delivery, Git integration and Craft's independent likeness gate are outside this planning request.

## Builder-check resolutions and planner calls

One fresh builder review found two substantive contract questions; both are now decided here for review, without changing application files.

1. **Unsupported delivery:** `/nieuws` is an email-only newsletter form with no mailing-list integration; `/test` is a different three-step quote wizard with no existing local payload/subject contract. Set `formMode: 'local-only'` for both. Match initial appearance, options, step navigation, validation and unchecked consent, then show truthful “Dit formulier is nog niet aangesloten.” feedback after a valid submit. Never show a subscription/sending success. Do not give these forms the `.static-form` class: that is the actual selector the existing `site.mjs` delivery handler binds, and a shared configured contact key must not activate them accidentally. Test with a dummy configured key and assert zero delivery requests. Established contact, appointment, application and `/offerteaanvraag` flows remain `formMode: 'deliverable'` with their existing subjects/mappings. Cost of this call: newsletter and alternate test-quote requests cannot be completed until a dedicated integration is requested.
2. **Source link defects/out-of-scope targets:** preserve visible labels and styling, but use working verified destinations. `/branches` is a valid public 200 page outside this sitemap scope: the seven observed “Al onze diensten” actions remain explicit `https://www.bhr-is.nl/branches` links. `/solliciteer` is a 404, but the vacancy actions also have `data-scroll=".Form.Detail"`; activating that handler keeps the vacancy URL and scrolls to its inline `form_2`. Use local `#form_2` anchors for those actions. The encoded `{1:Document:16}` links titled “elektrische besturingskasten” resolve to a broken CMS token: route that label to the verified existing `/expertises/paneelbouw` page (public 200, local route already present), not a guessed numeric document URL. Convert `+31162238834` relative hrefs to `tel:+31162238834`; normalize WhatsApp phone query formatting to the same international number without changing displayed copy. Do not create guessed routes for bad tokens. Cost: some intentionally corrected targets differ from the broken literal source href, and the branch-index action leaves the local site.
3. **Alias presentation:** all 64 scoped source requests returned 200 without redirects. `/voor-machinebouwers` and `/werken-bij` can reuse the authored canonical compositions as a starting point, but must serve their own requested URLs with the observed metadata. `aliasTarget` means renderer reuse, not permission to introduce an HTTP redirect. Keep any refinements scoped to the new alias class; the previous six pages' hashes remain protected.
4. **Team interaction:** clicking the contact team card did not open a profile dialog. Its source markup contains a WhatsApp hover overlay. Match that observed affordance with hover/focus access; an extra dialog would be invented behavior.

Link and interaction evidence is in `checks/visual-planning-2026-11-20/interaction-audit/`. No subscription, quote, appointment or application was sent. The public GET-only category filter was exercised. Source field requiredness comes from CMS validation metadata, not guessed from a false HTML boolean.

## Delivery dependencies

Page numbers are identifiers, not a mandate to ignore link prerequisites. Run the privacy and not-found utility plans after the empty-manifest foundation and before the priority pages: new secondary footer links use `/privacy`, and the observed appointment Back href is `/pagina-niet-gevonden`. Preserve that captured Back destination rather than inventing history behavior. Establish `/offerteaanvraag` and `/branches/productie-industrie` before service pages; establish the two linked bordenbouw pages before `/bordenbouwer`, and the root careers path before the HTML sitemap.

The location index links all nine details, and every detail links the index. Those ten page plans form one functional delivery batch; author all ten routes before running the global link gate or claiming that batch complete. Each keeps its own data, tests, screenshots and visual acceptance. Do not invent placeholder redirects or skip broken-link verification to make an isolated location page appear complete. The full graph is `checks/visual-planning-2026-11-20/link-dependencies.json`.

For search, keep the source `search` query parameter on the new page and accept legacy `q` from the existing header dialog. The new page uses an opt-in handler rather than the old `.site-search` submit handler, which reads only `q`. Reuse the existing `searchPages` algorithm and the generated local index. Do not fake source result sets with precomputed screenshots/query responses; record result-membership differences caused by the local corpus separately from visual result-list styling. Cookie preferences reuse `cookiePreferences`, retaining necessary storage and honoring existing accepted/declined/JSON states.

## Existing local delivery names (binding)

The current generated forms were inspected, not inferred from their headings:

| Flow | Existing `subject` | Local delivery fields |
|---|---|---|
| Contact and appointment, plus analogous new contact forms | `Contact met BHR` | `company`, `name`, `email`, `phone`, `message`, `privacy` |
| Application | `Sollicitatieformulier` | `firstname`, `lastname`, `email`, `phone`, `birth_day`, `birth_month`, `birth_year`, serialized `birthdate`, `bewaren`, `vacature`, `cv`, `privacy` |
| Quote | `Offerteaanvraag BHR` | `company`, `email`, `phone`, `$specificatie_0` through `$specificatie_6`, `privacy` |

Retain `apiKey` and honeypot handling through the existing sender. Do not rename these fields to plausible English alternatives, derive a new subject from a page heading, or replace option labels with opaque CMS object IDs. Newsletter and test-quote forms have no delivery subject and are excluded from `.static-form` binding.

Inline SVG artwork/icons (including the error-page artwork) may be extracted as original vector media into `app/public/assets/images/secondary-*.svg`, with source page/role, bytes and SHA-256 in `app/secondary-assets.json`. This is separate from reusing application templates. External image URLs still require exact `assets-manifest.json` entries.

All new forms preserve startup safety: submits remain disabled/prevented until their validation and submit listeners are installed, following the existing form scaffold and its regression test. Local-only forms install their own listener before enabling submission and never enter the `.static-form` scanner. Include a delayed-module browser case proving a native submit cannot escape before readiness.
