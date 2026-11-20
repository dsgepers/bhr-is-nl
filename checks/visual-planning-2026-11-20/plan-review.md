# Planning review — remaining BHR pages

This review concerns the design, implementation plans and planning evidence. It does not certify implemented pages: no application source was changed.

## Scope and coverage

- 83 original sitemap URL entries; eight malformed duplicated-origin timeline entries and four duplicate root/hash entries are documented rather than turned into pages.
- 71 unique valid paths, minus homepage and six previously targeted paths = **64 scoped page plans**.
- 32 existing local candidates, 32 absent local routes. Missing routes have source-only evidence and no fabricated similarity score.
- **97 live reference captures / 65 candidate comparisons**: all 64 at 1920×1080, with three additional widths for the 11 priority pages. The other 53 pages explicitly require responsive capture before implementation fine tuning.
- All 64 live primary requests returned 200 without redirects; all visible source images decoded. The two root reuse URLs remain 200 pages rather than invented redirects.
- The 12 existing routes outside scope are protected by saved generated-HTML hashes. All application source files are additionally hash-checked against the planning start.

## Fresh builder check and resolutions

One fresh static-site engineer reviewed the design and relevant source. It raised two substantive questions, resolved in the design and shared/page plans:

1. **Unsupported forms:** newsletter subscription and the alternate three-step test quote have no established local delivery integration. Both get visual/validation parity and truthful local-only feedback, excluded from `.static-form` even with a configured generic key. Established contact, appointment, application and real quote contracts retain their actual subjects/field names. Cost: the two unsupported flows cannot complete real requests until a dedicated integration is supplied.
2. **Broken or out-of-scope source destinations:** `/branches` was verified public 200 and remains an explicit public link. `/solliciteer` returned 404, while the vacancy’s actual data-scroll handler was observed scrolling to its inline form without navigation: use `#form_2`. Encoded CMS links labeled “elektrische besturingskasten” use the verified existing paneelbouw page; malformed phone links become tel:. Preserve visible labels. Cost: corrected hrefs differ from broken source literals, and the branch-index action leaves the local site.

The builder was not asked to certify visual metrics or production delivery. No second review was substituted for the planner’s own consistency check. Contact team clicking showed no profile dialog; the plans retain the observed WhatsApp hover/focus affordance instead of adding one.

## Self-review checklist and corrections

- **Spec coverage:** each normalized path maps to exactly one numbered plan, source fixture, baseline disposition and final all-width acceptance protocol. The project listing plus all eight project details are explicitly listed, followed by contact and appointment.
- **Concrete page differences:** every plan pins its own H1/box, section headings, original image filenames, optional FAQ/field inventory and baseline dimensions/metrics. Generic family helpers cannot silently add missing forms, CTAs, galleries or testimonials.
- **Interfaces:** the shared plan defines manifest/strict-media, renderer/options, metadata/header/footer overloads, CSS/module scopes, test helpers, delivery subjects and field names. Page plans consume those same interfaces. Existing project/branch arrays and protected defaults are not repurposed.
- **Behavior evidence:** project Paneelbouw selection produced `?filter_projectgroup%5B%5D=2` and four rows; source gallery Next indices were 0,1,2,3,4,4,4. The listing has original gallery cardinalities 1,1,1,5,7,1,2,2; clones are not records. Required fields are derived from CMS validation metadata, not false native booleans.
- **Dependency scan:** new footer Privacy and appointment Back destinations require support pages first; service pages require standalone quote and Productie-industrie; Bordenbouwer requires its two linked destinations; the HTML sitemap requires root careers. The location index/detail breadcrumb cycle is one ten-page functional batch with ten separate visual reviews. No placeholder routes or weakened link gate are proposed.
- **Review Focus coverage:** structural/asset tests cover source copy and exact derivatives; browser cases cover controls, optional/required/consent/startup and local-only delivery; four-width screenshots/boxes cover typography/composition; protected hashes and full route verification cover shared regressions. CSS is verified visually rather than mirrored by unit tests.
- **Step/proportion scan:** steps specify files, signatures, expected failures, expected passing commands and page-specific evidence. Rendering bodies are left to the implementer; saved reference HTML is never an application template. Shared implementation protocols are referenced by all page plans.
- **Acceptance honesty:** baseline differences are not completed fixes. Proposed strict target is ≤0.5% mismatch, ≥0.985 SSIM estimate, ≤2px height delta individually at every width. Other responsive states are not claimed audited. Earlier-phase open gates remain unchanged.

## Capture-tool corrections verified

The shared browser snapshot timed out twice, so the skill’s Playwright fallback was used after quoting the error to the user. Native tiled captures avoid off-screen composited-layer omissions. Initial project-filter/simple-header duplicates were corrected in the selected captures; original diagnostic files were retained. Partner positions, fonts, finite animations, pointer location, decoded imagery and viewport/DPR/zoom were normalized without masks.

The initial image-only skill invocation did not load DOM sidecars and therefore reported unavailable zoom metadata even though both live captures asserted DPR/scale 1. The accepted reports reattach the actual sidecars and enforce equality. The reusable `compare-cached.py` now attaches metadata **before** the skill checks zoom; a cached Contact comparison passed the real `--fail-on-zoom-mismatch` gate without warnings. Missing actual metadata still fails. The runner also preserves the planning baseline by default and rechecks current local-route existence after implementation.

Repo-local tools were added/refined; the global visual-diff skill and earlier-phase evidence were not changed. No contact, appointment, quote, application or newsletter request was sent.

Final file checks: 64 page plans plus shared foundations; all relative document links resolve; 180 tracked application source files and 12 protected generated routes retain their saved hashes. Coverage and helper-gate results are recorded in `verification.json`.
