# BHR remaining-page foundations Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for native execution, or superpowers:subagent-driven-development if explicitly selected. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Supply isolated, tested route/rendering and behavior interfaces for the 64 page plans without changing the 12 protected pages.

**Architecture:** Exact-route opt-in manifest, focused family renderers, a stylesheet and optional browser module loaded only in the new scope. Existing data arrays and default helpers retain their output.

**Tech Stack:** Node.js >=20, ES modules, generated HTML, CSS, vanilla browser JavaScript; Python/Playwright visual-diff tooling for development only.

**Spec:** [Remaining-pages design](../specs/2026-11-20-bhr-remaining-pages-design.md)

## Global Constraints

- Node.js >=20; no additional application runtime dependencies.
- 1920×1080 primary; 1440×900, 768×1024 and 390×844 regression views; DPR 1 and zoom 1.
- Preserve Dutch source copy, original locally packaged media and the 12 protected route hashes.
- Author application HTML/CSS/JS; do not import reference application source or use screenshots as page backgrounds.
- No real form submissions; preserve delivery names/subjects and combined 4 MB uploads; consent initially unchecked.
- Strict visual target ≤0.5% mismatch, ≥0.985 SSIM estimate and ≤2px height delta, separately per page/width. No averaged acceptance.
- No Git repository currently exists. Use local source checkpoints and a durable ledger; do not invent commits or initialize Git.

## Review Focus

1. Exact routing must not swallow protected routes, emit duplicates, or confuse two equal-looking URLs with an observed redirect.
2. `media()` silently accepts other derivatives; new pages must fail rather than render a substitute photo.
3. Styles, scripts, branch taxonomy and project images must not leak into the homepage or previous pages.
4. A configured generic form key must not activate newsletter or `/test` delivery.
5. Floating headers/filters, carousel positions and cached PNG metadata must not create false comparison results.

---

## Task 1: Opt-in routing, strict media and protected consumers

**Files:** Create `app/secondary-assets.json`, `app/secondary-data.mjs`, `app/secondary-content.json`, `app/secondary-pages.mjs`, `app/secondary-components.mjs`, `app/secondary-projects.mjs`, `app/secondary-forms.mjs`, `app/public/secondary-parity.css`; modify `app/build.mjs` and `app/components.mjs`; test `app/tests/secondary-pages.test.mjs`, `app/tests/secondary-helpers.mjs`, `app/tests/fixtures/secondary-pages.json`, `app/tests/fixtures/secondary-protected-hashes.json`.

**Interfaces:** Consume the spec's `SecondaryPageSpec`. Export `secondaryContent`, `secondaryMedia(url: string) -> string`, `secondaryPage(route: string) -> string` and `secondaryOptions(route: string) -> {title,classes,simple,documentTitle,canonical}`. `secondaryMedia` requires an exact manifest key and returns its local path; no basename fallback. The body classes are `secondary parity-page secondary-parity secondary-<kind> secondary-route-<key>`. Family renderer signatures are defined in the spec. Test helpers export `readBody(route) -> string`, `plainText(html) -> string` and `assertInOrder(html,texts) -> void`; read only the `#page-content` body, excluding head/footer text.

- [ ] Add tests for unknown secondary routes, duplicate manifest paths, a same-photo/different-URL media lookup that must throw, isolated CSS/script loading, and all 12 protected generated-HTML hashes. Seed the protected fixture from `checks/visual-planning-2026-11-20/protected-route-hashes.json`. Do not seed it from output after editing.
- [ ] Run `npm --prefix app run build && node --test app/tests/secondary-pages.test.mjs`; expect failure for absent new exports/guards, with the existing 45 tests still the baseline.
- [ ] Implement strict lookup and dispatch, retaining existing `add()` callers and intercepting only exact manifest keys. Emit absent manifest routes once after existing routes. Begin with an empty manifest; individual page plans author their data. Preserve metadata and requested 200 URLs for the two reuse aliases; do not turn them into redirects.
- [ ] Load `/secondary-parity.css` after `/parity.css` and `/secondary.mjs` only for `secondary-parity`. Extend `layout` with optional fifth metadata argument `{documentTitle,canonical}` for new opted-in calls only, leaving old four-argument output unchanged. Extend `header(simple=false,parity=false,options={})` with `backHref` default `/`; the appointment scope supplies `/pagina-niet-gevonden`. Extend `footer(parity=false,options={})` with `privacyHref` default `/privacyverklaring`; only the new scope supplies `/privacy`. New CSS selectors start with `.secondary-parity` or its route class. Reuse the packaged `bhr-roboto` / `bhr-oxanium` fonts and original SVG media.
- [ ] Run build, the complete suite and `npm --prefix app run verify`; expect all current 44 routes and protected hashes unchanged with an empty manifest. Record the checkpoint locally.

## Task 2: Shared behavior contracts and content fixtures

**Files:** Create `app/public/secondary.mjs`, `app/public/secondary-behavior.mjs`, `app/tests/secondary-behavior.test.mjs`, `app/tools/check-secondary-browser.py`; extend the focused fixtures and family renderers above. Change existing `site.mjs` only if a narrowly scoped adapter cannot reuse its current contracts.

**Interfaces:** `selectedProjectGroup(search) -> null|'1'|'2'|'3'`; `projectGalleryIndex(index,delta,count) -> number` clamps to available indices. Real forms retain `.static-form`, existing delivery subjects and field mappings. Local-only newsletter/test forms use `data-local-only-form` and never `.static-form`. Browser checker accepts `--route /path`, blocks delivery requests and uses dummy keys for configured-path checks. Reuse `searchPages(pages,query)` and `cookiePreferences(saved)` from `public/behavior.mjs` rather than creating conflicting search/consent algorithms.

- [ ] Add failing behavior tests: group `2` parses from the encoded source query; unknown group is null; gallery sequence for five images ends at 4; previous at zero stays zero; zero images returns zero. Add local-only form cases with a dummy shared key and assert no delivery request can occur.
- [ ] Run `node --test app/tests/secondary-behavior.test.mjs`; expect the new helpers/guards to fail before implementation.
- [ ] Implement those pure helpers and optional secondary handlers. Match the observed project query `filter_projectgroup[]`, synchronize both filter presentations and support browser history. The default visible choices are Automatisering and Paneelbouw; do not expose the hidden Integratie radio as a new default choice.
- [ ] Add the shared browser checks for native keyboard controls, first/last gallery bounds, real-form invalid/optional/consent/unconfigured paths, local-only feedback under a configured dummy key, and no duplicate event handling and disabled/prevented submit before handlers are ready (including local-only forms). Preserve existing `site.mjs` form subjects and safe unconfigured feedback.
- [ ] Seed each implemented route's test fixture from its frozen entry in `checks/visual-planning-2026-11-20/expected-pages.json`. Author production page data separately; test the generated body against the external reference fixture, not by comparing a renderer with its own input. Keep each page's exact field options, question/answer pairs and original image URLs traceable to its inventory.
- [ ] Run all tests and the browser checker against the opted-in pages; expect zero real delivery requests and no protected-page regression. Record the checkpoint.

## Task 3: Dependency-aware page execution and visual acceptance

**Files:** Use the 64 linked page plans; preserve `checks/visual-planning-2026-11-20/`. Create fresh implementation evidence under `checks/visual-review-remaining-<run-id>/` and a durable execution ledger.

**Interfaces:** Page plans consume the exports above and own their manifest entry, family-specific composition/styles and browser case. The comparison runner accepts `--route KEY --all-widths --out NEW_DIR`. It records source-only evidence until a local page exists; actual DOM sidecars validate DPR/zoom equality before accepting cached comparisons.

- [ ] Start with the `/privacy` and `/pagina-niet-gevonden` support-page plans so new footer links and the appointment Back action have working local destinations. Then prioritize the 11 explicitly requested pages.
- [ ] Before service plans, implement `/offerteaanvraag` and `/branches/productie-industrie`. Before `/bordenbouwer`, implement `/bordenbouw-op-maat` and `/industriele-bordenbouw`. Before the HTML sitemap, implement `/werken-bij`. Follow `checks/visual-planning-2026-11-20/link-dependencies.json` for the full graph.
- [ ] Implement the location index and nine location details as one functional delivery batch: index cards and detail breadcrumbs form a cycle. Keep a separate visual plan/result for each page, but run the global link gate and record completion only after all ten routes exist. Do not introduce placeholder routes or weaken link verification to break the cycle.
- [ ] Serve the built `app/dist` at `http://127.0.0.1:4173`: reuse the existing server, or run `python -m http.server 4173 --bind 127.0.0.1 --directory app/dist` from the workspace root. This server is for the site under test, not for the standalone review gallery.
- [ ] For each page, run build/tests/verify, then `/tmp/bhr-visual-diff-venv/bin/python checks/visual-planning-2026-11-20/run-comparisons.py --route KEY --all-widths --out checks/visual-review-remaining-<run-id>`. Expect valid source/candidate screenshots at all four widths and equal DPR/scale. Missing-route scores or zoom warnings are failures, not likeness measurements.
- [ ] Inspect full side-by-side, heatmap and overlay, heading/photo/form boxes, native crops and document height. Review selected/expanded/hover/focus/error states applicable to the page. Capture scrolled header/filter states separately; the full-document tiler deliberately suppresses repeated sticky clones after their original appearance.
- [ ] Require ≤0.5% mismatch / ≥0.985 SSIM / ≤2px height delta separately at all four widths for each page's strict acceptance. Keep open results explicit and retain unmasked evidence. A close-clone benchmark cannot replace the strict gate.
- [ ] Run final build/full suite/route audit, the browser checks and all protected hashes. Refresh reachable public references before the final claim. Request one fresh whole-change review under the selected execution workflow; fix Important/Critical findings with regression evidence, recording any deferred minor. No deployment or real forms are part of this gate.

## Independent deliverable

The empty-manifest foundation leaves all existing output stable; every page can opt in through one defined route interface. Dependencies determine functional delivery batches, while all 64 pages retain independent visual acceptance. Final source totals and link/reference counts are recorded from actual verification rather than assuming the current 2116 links remain the final count.
