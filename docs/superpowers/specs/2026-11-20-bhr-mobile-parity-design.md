# BHR mobile parity design

The user explicitly preapproved both planning and execution and will be away. Continue without another approval pause. This approval supersedes this phase's normal design/plan handoff. Existing slider fixes are checkpointed on local branch `mobile-parity` at `31188e8`; remote main is unchanged.

## Intent and observed cause

Reproduce the actual live phone experience, including JavaScript-driven navigation and changing mobile compositions, while preserving the current desktop rendering. A390px desktop browser is NOT a valid live phone reference: the CMS chooses corporate-desktop, corporate-tablet or corporate-mobile CSS and server markup from device detection and its `device` cookie. The live source's inline portrait handler explicitly uses that cookie. A real phone context produces corporate-mobile and a96px fixed header instead of the old394px desktop navigation. The prior viewport-only mobile captures are superseded for this phase.

## Approach and authority

Keep the static Node20+/HTML/CSS/ES-module stack and original local media. Considered: changing the existing large stylesheets globally (too much desktop risk); rebuilding each route separately (duplicates76 pages and navigation); one authored mobile layer with family-specific overrides and a shared mobile runtime (chosen by the implementer). Use responsive CSS and matchMedia locally; no server or user-agent dependency is necessary. Reference HTML/CSS/JS are evidence only, never product source. Do not copy source templates or use screenshot backgrounds.

Scope is all76 current local routes, with live-source dispositions where a public counterpart fails. Inventory each path and group implementation by its shared renderer. Check every route at390×844. Check360×800,430×932 and768×1024 on representative families and menu states. Phone is≤767px, tablet768–1199px, desktop≥1200px; verify the transition edges and retain the1920px primary desktop and1440px regression. Real phone contexts use a mobile UA, touch, matching screen dimensions, DPR1 and scale1. Tablet references use the tablet theme and touch. Shared preview cannot emulate UA/screen/touch, so the visual-diff Playwright harness is required for device-correct capture; shared preview remains useful for showing and inspecting the observed theme via the CMS cookie.

## Product boundaries

Add app/public/mobile-parity.css, loaded last with media="(max-width:1199px)". Every declaration stays inside that range; use a separate phone media block at767px. Add app/public/mobile.mjs, which does nothing at desktop widths and enters/tears down mobile enhancements through matchMedia. It injects an authored compact header and drill-down drawer only while active. Hide the original header only after the replacement is ready. Clone only our own brand/control artwork. The simple appointment header has its observed Back/logo/phone composition and no invented full navigation.

The menu has a root list, Industries and Over BHR child panels, a Back control, close control, phone action, appointment CTA and original social destinations. Reproduce the source's slide-in transition, spacing, color and sticky state. Retain desktop nav links and handlers. Trap focus while open, support Escape/backdrop, restore focus and scroll position, release body lock and inert state on close or desktop resize. Keep Dutch labels readable instead of reproducing a double-encoded CMS entity.

Use mobile-only layout rules for page containers, hero crops/stripes/typography, vertical article sequences, horizontal expertise rows, card strips, step/photo relationships, forms, job sidebars, maps, locations and footer. Add mobile-only content only when confirmed by the reference (the observed homepage has eight expertise rows; the index has ten); remove it when leaving mobile mode. Maintain real images, text, native controls, existing form subjects/field names, required unchecked consent,4MB upload limit and local-only newsletter/test behavior. Do not send forms or publish.

Avoid stale previews: version the new stylesheet/module URLs by content. Extend existing asset fingerprinting without altering desktop presentation. Existing approved desktop HTML may gain those two inert resource references; protect its prior markup after stripping only these additions, and verify their media guard and runtime no-op separately. Functional hash fixtures must not be silently regenerated for all routes.

## Evidence and acceptance

Evidence root: checks/mobile-parity-2026-11-20. Preserve baseline source and candidate captures; candidate overflow is a recorded baseline defect, not a fabricated same-width score. Keep immutable local1920px before captures for all76 routes and1440px for representative families before building product changes. Freeze homepage/banner/partners on their same original first frame for comparison. Capture actual viewport tiles; retain one header and suppress only repeated floating chrome. Compare sticky/menu states separately without that normalization. No masks.

Mobile target per page/width: mismatch≤0.5%, SSIM≥0.985 and absolute full-page height delta≤2px. A failing gate remains OPEN. Separately classify close clones with mismatch<5% and SSIM>0.93; no averaging or Craft score. Desktop acceptance is stricter for this phase: no visible pixel/geometry change from this phase's local baseline at1920px and1440px. Existing source-vs-local desktop differences are not certified or silently changed. Finish includes a report with every page's mobile result, each desktop regression result, actual device/theme metadata, scoped interaction tests and any residual gates.

## Review focus

1. Menu opened from a scrolled page, submenu Back/Escape/backdrop, keyboard focus, body lock and viewport rotation must never strand navigation or scrolling.
2. A phone request must load the mobile theme in the reference, and a local mobile viewport must never use old426px overflow or a cached desktop bundle.
3. Leaving mobile mode must restore the desktop header, content order, hidden cards, carousel geometry and focus without changing desktop screenshots.
4. Phone forms, uploads, date selectors, consent and local-only flows must remain usable without accidental delivery or hidden validation targets.
5. Delayed mobile JS, failed media, reduced motion, touch dragging and sticky job/project controls must preserve access and never cover focused content.

A fresh builder review checks this design before execution; one whole-change code review occurs at the end, with one tested fix pass for Important/Critical findings. Keep the local branch and evidence for handoff; no remote push, merge or deployment is required by this request.
