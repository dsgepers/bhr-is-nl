# BHR /branches/machinebouw Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for native execution, or superpowers:subagent-driven-development if explicitly selected. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make local `/branches/machinebouw` match its live equivalent, with independent visual acceptance.
**Architecture:** Opt in this exact route through the shared secondary manifest; use the `branch` composition and route-scoped styles. Preserve old default consumers.
**Tech Stack:** Node.js >=20, ES modules, static HTML/CSS, vanilla JavaScript, Python/Playwright visual-diff.
**Spec:** [Remaining-pages design](../specs/2026-11-20-bhr-remaining-pages-design.md) · **Prerequisite:** [Shared foundations](2026-11-20-bhr-remaining-00-shared.md)

## Global Constraints

- Node.js >=20; no new application runtime dependencies; author HTML/CSS/JS and package original media locally.
- Preserve Dutch copy and the 12 protected route hashes. No global theme/data-array edits or screenshot-backed page content.
- 1920×1080 primary; 1440×900, 768×1024, 390×844 regression views; DPR 1, zoom 1, light, nl-NL, Europe/Amsterdam.
- No real submissions; existing delivery names/subjects, initially unchecked consent, combined 4 MB uploads. Newsletter/test forms are local-only.
- Strict acceptance per width: mismatch ≤0.5%, SSIM estimate ≥0.985, height delta ≤2px. No averages or invented Craft scores.
- No Git currently exists: record a local checkpoint and ledger instead of inventing a commit.

## Review Focus

1. Long/emphasized “Betrouwbare paneelbouw en automatisering voor machinebouw” text must retain source wrapping at all four widths.
2. Exact source photo derivatives and original media must load; a same-photo fallback is not an acceptable substitution.
3. The full heading/section/FAQ inventory must remain ordered, including content below the first screen.
4. Exercise photographed service links, source process/partner controls where present and all captured FAQ disclosures. Do not let a generic service component replace this route’s actual section order or link taxonomy.
5. The new route must retain usable links/validation without changing any protected consumer or sending a live request.

---

## Observed baseline and source requirements

Current owner: the branch loop in `app/build.mjs`, using shared generic components.
Rebuild the overlaid branch hero and dark lead, then the original article/illustrated-service compositions in their observed order. Match the ten service cards, photographed testimonial or process block, partner strip, FAQ and CTA only when present here. Keep the source target /branches/productie-industrie in the new pages’ branch taxonomy; leave the protected local /branches/verpakkingsindustrie route and old shared array untouched.

At 1920px the source H1 is `Betrouwbare paneelbouw en automatisering voor machinebouw`: 65px/57.2px, box x=200.00, y=153.00, 620.00×228.75. Use these as measurements, not blank spacer dimensions.
The current local H1 is `Betrouwbare paneelbouw en automatisering voor machinebouw` at 50px; its structure/photo/section geometry is visible in the linked comparison.
Source heading text currently absent or different: “Inbedrijfstelling”; “Industriële automatisering”; “Vakmanschap van begin tot eind”; “Hoe BHR werkt”; “Stap 1” (14 total; use the full fixture).

| Baseline viewport | Mismatch | SSIM estimate | Reference / local full image |
|---|---:|---:|---|
| wide | 89.050% | -0.1399 | 1920×10122 / 1920×8821 |

Planning captured 1920px only for this secondary page. **Capture the other three widths before implementation fine tuning; they are not audited/passed by this baseline.**

[Full reference/candidate report or source evidence](../../../checks/visual-planning-2026-11-20/baseline/branches--machinebouw/report.html)
 · [Measured inventory](../../../checks/visual-planning-2026-11-20/baseline/branches--machinebouw/wide-reference-inventory.json)
 · [Text/media/link inventory](../../../checks/visual-planning-2026-11-20/baseline/branches--machinebouw/wide-reference-content.json)

**Exact content/asset fixture:** this route’s entry in [expected-pages.json](../../../checks/visual-planning-2026-11-20/expected-pages.json). Its full source heading sequence, every original image filename, resolved action targets, FAQ pairs and CMS validation designations are binding. Do not copy the saved HTML into app code.

**Ordered own content blocks:**
1. Geïntegreerde besturing en automatisering voor optimale machinebouwprestaties
2. Paneelbouw en besturingskasten die betrouwbaarheid in machinebouw garanderen
3. Slimme machinebouwautomatisering die efficiëntie verhoogt
4. De betrouwbare partner voor machinebouw
5. ‘Hier leer je pas écht de kneepjes van het vak’
6. Wat kunnen wij voor jouw proces betekenen?

**Source image filenames (exact derivatives):** `809_dsc01712.webp`, `649_dsc02916.webp`, `651_dsc01013.webp`, `653_dsc02826.webp`, `585_dsc02701.webp`, `588_dsc02665.webp`, `895_dsc01075.webp`, `596_dsc01103.webp`, `600_dsc01226.webp`, `604_dsc01010.webp`, `609_dsc02603.webp`, `613_dsc01030.webp`, `616_dsc00987.webp`, `549_nieuwe-map-slimme-automatisering.webp`, `647_dsc02231.webp`, `437_dsc02673.webp`, `451_dsc02462.webp`, `1002_rittal.webp`, `1003_lappkabel-logo.webp`, `1194_abb.webp`, `1195_allen-bradley.webp`, `1196_phoenix-contacts.webp`, `1197_wago.webp`, `44_partner2.webp`, `45_partner3.webp`.

**Linked-route prerequisites:** `/privacy`.

## Task 1: Source composition, exact assets and route ownership

**Files:** `app/secondary-content.json`, `app/secondary-data.mjs`, `app/secondary-pages.mjs`, `app/secondary-components.mjs`, `app/assets-manifest.json`, `app/public/assets/images/`; test `app/tests/secondary-pages.test.mjs` and its source fixture.
**Interfaces:** Consume `secondaryContent["/branches/machinebouw"]` and the shared renderer/strict-media interfaces. Produce one authored `branch` entry and generated `/branches/machinebouw/index.html`; no duplicate route emitter.

- [ ] Add the frozen `/branches/machinebouw` expectation and test `/branches/machinebouw source composition`: `const html=readBody("/branches/machinebouw"); assertInOrder(plainText(html),expected.headings); for(const src of expected.images) assert.ok(html.includes(src));` Assert the exact H1 “Betrouwbare paneelbouw en automatisering voor machinebouw”, resolved destinations, expected FAQ count and no unrelated generic section.
- [ ] Run `npm --prefix app run build && node --test --test-name-pattern="/branches/machinebouw source composition" app/tests/secondary-pages.test.mjs`; expect FAIL for the old composition/media or ENOENT for the missing route.
- [ ] Author the route’s complete source data and `branch` body in its designated renderer; package every missing exact media URL with bytes/SHA-256 and an exact manifest key. Opt this route in through `secondaryOptions`; preserve requested URL, metadata and observed header variant.
- [ ] Rebuild and rerun the targeted test; expect PASS for all frozen headings/assets/links and this route’s actual content. Record a local source checkpoint.

## Task 2: Measured layout and observed behavior

**Files:** `app/public/secondary-parity.css`, the designated family renderer, `app/secondary-forms.mjs` where this page has a form, `app/public/secondary.mjs` only for new controls; test `app/tools/check-secondary-browser.py` and meaningful pure behavior cases.
**Interfaces:** Use `.secondary-parity.secondary-route-branches--machinebouw` and the spec’s delivery/behavior contracts; do not change old global selectors.

- [ ] Capture any planning-unaudited widths and add the route-specific browser regression before its behavior implementation; verify that it fails against the old/missing controls. Use screenshot/box evidence for CSS rather than tests that mirror style declarations.
- [ ] Match the measured header, H1/emphasis, photo crop, source section surfaces, text widths, clipped corners, controls, form/card geometry and footer. Follow this page’s reference composition; do not impose a generic clean mobile stack or pad to the target document height.
- [ ] Implement and check: Exercise photographed service links, source process/partner controls where present and all captured FAQ disclosures. Do not let a generic service component replace this route’s actual section order or link taxonomy.
- [ ] Run `/tmp/bhr-visual-diff-venv/bin/python app/tools/check-secondary-browser.py --route /branches/machinebouw` with delivery blocked; expect its keyboard/state/validation assertions to pass and zero real submission requests. Run the complete unit suite after any behavior change.

## Task 3: Four-width page review and release gate

- [ ] Complete the listed route prerequisites (or the ten-location batch), then run `npm --prefix app run build`, `npm --prefix app test` and `npm --prefix app run verify`; expect all functional/asset/link checks and the 12 protected hashes to pass.
- [ ] From the workspace root run `/tmp/bhr-visual-diff-venv/bin/python checks/visual-planning-2026-11-20/run-comparisons.py --route branches--machinebouw --all-widths --out checks/visual-review-remaining-<run-id>`; expect four valid matched-zoom captures. Preserve the planning baseline.
- [ ] Open every width’s side-by-side, heatmap and overlay, and native crops of the title, photos, key control/form, section boundaries and footer. Compare actual boxes/fonts and document height. Review applicable expanded, selected, hover/focus and error views; scrolled sticky controls require separate viewport captures.
- [ ] Record each result separately. Require mismatch ≤0.5%, SSIM estimate ≥0.985 and height delta ≤2px at every width for strict acceptance; leave this page open if any fail. Never certify a missing candidate, unaudited state, averaged score or Craft score as a visual-diff pass.
- [ ] Record the source checkpoint, commands, browser results, individual metrics and any intentional difference in the execution ledger. No deployment or real delivery belongs to this page’s completion gate.
