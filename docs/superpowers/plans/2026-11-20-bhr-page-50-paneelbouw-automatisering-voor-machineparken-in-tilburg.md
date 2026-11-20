# BHR /paneelbouw-automatisering-voor-machineparken-in-tilburg Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for native execution, or superpowers:subagent-driven-development if explicitly selected. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make local `/paneelbouw-automatisering-voor-machineparken-in-tilburg` match its live equivalent, with independent visual acceptance.
**Architecture:** Opt in this exact route through the shared secondary manifest; use the `seo` composition and route-scoped styles. Preserve old default consumers.
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

1. Long/emphasized “Paneelbouw & automatisering in Tilburg” text must retain source wrapping at all four widths.
2. Exact source photo derivatives and original media must load; a same-photo fallback is not an acceptable substitution.
3. The full heading/section/FAQ inventory must remain ordered, including content below the first screen.
4. Check this page’s inline technical links, exact primary/secondary actions and any contact form with delivery blocked. Match only its captured FAQ/gallery/CTA states, without adding absent widgets.
5. The new route must retain usable links/validation without changing any protected consumer or sending a live request.

---

## Observed baseline and source requirements

No local route exists; create it through the shared manifest and route emitter.
Create this landing page from its own overlaid photographic hero, dark introduction and exact article sequence. Preserve source lists, inline links, blue/pale/white transitions, testimonial or full contact form and CTA only where this route contains them. These SEO pages use materially different photos and technical copy; a generic page with a city/product name substituted is not equivalent.

At 1920px the source H1 is `Paneelbouw & automatisering in Tilburg`: 65px/57.2px, box x=200.00, y=245.83, 620.00×171.56. Use these as measurements, not blank spacer dimensions.

| Baseline viewport | Mismatch | SSIM estimate | Reference / local full image |
|---|---:|---:|---|
| wide | Not scored: local route absent | — | 1920×5283 / missing |

Planning captured 1920px only for this secondary page. **Capture the other three widths before implementation fine tuning; they are not audited/passed by this baseline.**

[Full reference/candidate report or source evidence](../../../checks/visual-planning-2026-11-20/baseline/paneelbouw-automatisering-voor-machineparken-in-tilburg/wide-reference.png)
 · [Measured inventory](../../../checks/visual-planning-2026-11-20/baseline/paneelbouw-automatisering-voor-machineparken-in-tilburg/wide-reference-inventory.json)
 · [Text/media/link inventory](../../../checks/visual-planning-2026-11-20/baseline/paneelbouw-automatisering-voor-machineparken-in-tilburg/wide-reference-content.json)

**Exact content/asset fixture:** this route’s entry in [expected-pages.json](../../../checks/visual-planning-2026-11-20/expected-pages.json). Its full source heading sequence, every original image filename, resolved action targets, FAQ pairs and CMS validation designations are binding. Do not copy the saved HTML into app code.

**Ordered own content blocks:**
1. Van cruciale schakel naar knelpunt in het machinepark door uitstekende paneelbouw
2. Paneelbouw als integraal onderdeel van uw productieomgeving
3. Waarom technische diensten in Tilburg vertrouwen op BHR Industrial Solutions
4. Bespreek uw paneelbouw of automatiseringsvraag

**Source image filenames (exact derivatives):** `1016_dsc01103.webp`, `1018_dsc01226.webp`, `1020_dsc02552.webp`, `935_dsc02866.webp`.

**Linked-route prerequisites:** `/privacy`.

## Task 1: Source composition, exact assets and route ownership

**Files:** `app/secondary-content.json`, `app/secondary-data.mjs`, `app/secondary-pages.mjs`, `app/secondary-components.mjs`, `app/assets-manifest.json`, `app/public/assets/images/`; test `app/tests/secondary-pages.test.mjs` and its source fixture.
**Interfaces:** Consume `secondaryContent["/paneelbouw-automatisering-voor-machineparken-in-tilburg"]` and the shared renderer/strict-media interfaces. Produce one authored `seo` entry and generated `/paneelbouw-automatisering-voor-machineparken-in-tilburg/index.html`; no duplicate route emitter.

- [ ] Add the frozen `/paneelbouw-automatisering-voor-machineparken-in-tilburg` expectation and test `/paneelbouw-automatisering-voor-machineparken-in-tilburg source composition`: `const html=readBody("/paneelbouw-automatisering-voor-machineparken-in-tilburg"); assertInOrder(plainText(html),expected.headings); for(const src of expected.images) assert.ok(html.includes(src));` Assert the exact H1 “Paneelbouw & automatisering in Tilburg”, resolved destinations, expected FAQ count and no unrelated generic section.
- [ ] Run `npm --prefix app run build && node --test --test-name-pattern="/paneelbouw-automatisering-voor-machineparken-in-tilburg source composition" app/tests/secondary-pages.test.mjs`; expect FAIL for the old composition/media or ENOENT for the missing route.
- [ ] Author the route’s complete source data and `seo` body in its designated renderer; package every missing exact media URL with bytes/SHA-256 and an exact manifest key. Opt this route in through `secondaryOptions`; preserve requested URL, metadata and observed header variant.
- [ ] Rebuild and rerun the targeted test; expect PASS for all frozen headings/assets/links and this route’s actual content. Record a local source checkpoint.

## Task 2: Measured layout and observed behavior

**Files:** `app/public/secondary-parity.css`, the designated family renderer, `app/secondary-forms.mjs` where this page has a form, `app/public/secondary.mjs` only for new controls; test `app/tools/check-secondary-browser.py` and meaningful pure behavior cases.
**Interfaces:** Use `.secondary-parity.secondary-route-paneelbouw-automatisering-voor-machineparken-in-tilburg` and the spec’s delivery/behavior contracts; do not change old global selectors.

- [ ] Capture any planning-unaudited widths and add the route-specific browser regression before its behavior implementation; verify that it fails against the old/missing controls. Use screenshot/box evidence for CSS rather than tests that mirror style declarations.
- [ ] Match the measured header, H1/emphasis, photo crop, source section surfaces, text widths, clipped corners, controls, form/card geometry and footer. Follow this page’s reference composition; do not impose a generic clean mobile stack or pad to the target document height.
- [ ] Implement and check: Check this page’s inline technical links, exact primary/secondary actions and any contact form with delivery blocked. Match only its captured FAQ/gallery/CTA states, without adding absent widgets.
- [ ] Run `/tmp/bhr-visual-diff-venv/bin/python app/tools/check-secondary-browser.py --route /paneelbouw-automatisering-voor-machineparken-in-tilburg` with delivery blocked; expect its keyboard/state/validation assertions to pass and zero real submission requests. Run the complete unit suite after any behavior change.

## Task 3: Four-width page review and release gate

- [ ] Complete the listed route prerequisites (or the ten-location batch), then run `npm --prefix app run build`, `npm --prefix app test` and `npm --prefix app run verify`; expect all functional/asset/link checks and the 12 protected hashes to pass.
- [ ] From the workspace root run `/tmp/bhr-visual-diff-venv/bin/python checks/visual-planning-2026-11-20/run-comparisons.py --route paneelbouw-automatisering-voor-machineparken-in-tilburg --all-widths --out checks/visual-review-remaining-<run-id>`; expect four valid matched-zoom captures. Preserve the planning baseline.
- [ ] Open every width’s side-by-side, heatmap and overlay, and native crops of the title, photos, key control/form, section boundaries and footer. Compare actual boxes/fonts and document height. Review applicable expanded, selected, hover/focus and error views; scrolled sticky controls require separate viewport captures.
- [ ] Record each result separately. Require mismatch ≤0.5%, SSIM estimate ≥0.985 and height delta ≤2px at every width for strict acceptance; leave this page open if any fail. Never certify a missing candidate, unaudited state, averaged score or Craft score as a visual-diff pass.
- [ ] Record the source checkpoint, commands, browser results, individual metrics and any intentional difference in the execution ledger. No deployment or real delivery belongs to this page’s completion gate.
