# BHR website recreation

Static recreation of bhr-is.nl, originally created with Craft Anywhere. Built with Node.js ES modules, HTML, CSS and vanilla browser JavaScript. Original image and font assets are packaged locally.

Requires Node.js 20 or newer. No runtime dependencies or package installation are needed.

```sh
npm --prefix app run build
npm --prefix app test
npm --prefix app run verify
```

The build generates 76 routes in `app/dist/`. Serve that directory with a static web server, or upload its contents to a static host.

Form configuration is in `app/public/config.js`. Without a configured form key, deliverable forms display contact alternatives rather than sending a request. Newsletter and alternate test-quote forms are intentionally local-only.

Page plans, review decisions and execution notes are in `docs/superpowers/`. Visual parity remains open on some pages and responsive widths; passing the functional tests does not certify visual identity.

Generated builds, captured reference pages, screenshot evidence, local archives and Craft session metadata are excluded from Git and remain in the original workspace. The retained visual-planning scripts may require those local captures, Python browser/image dependencies and the visual-diff skill. The older `app/SETUP.txt` describes earlier project stages; the commands and route count above describe the current build.

The responsive layer is `app/public/mobile-parity.css` plus `mobile.mjs`. It activates below 1200px and restores the original desktop DOM/media on exit. Phones through 767px use a full-screen drill-down menu; tablets use a half-width drawer with inline submenus. Original device-specific photo mappings and heading breaks are stored in the accompanying JSON files. Form delivery and validation stay in the existing form modules.

The live CMS serves different phone, tablet and desktop markup/styles based on device selection. The mobile audit therefore sets matching device cookies, user agents, screen sizes, touch capability and DPR1; a narrow desktop-UA screenshot is not a mobile reference. `app/tools/audit-mobile.py`, `audit-mobile-states.py`, `check-mobile.py` and `report-mobile.py` reproduce the captures, interaction checks and per-page metrics. They need Python Playwright/Pillow/NumPy and the installed visual-diff comparer; the content packaging helpers also need BeautifulSoup. Desktop comparisons use immutable local before screenshots, while mobile comparisons use the live device theme. The reports never average page scores or treat unavailable live routes as passes.
