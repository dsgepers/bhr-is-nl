# BHR website recreation

Static recreation of bhr-is.nl, originally created with Craft Anywhere. Built with Node.js ES modules, HTML, CSS and vanilla browser JavaScript. Original image and font assets are packaged locally.

Requires Node.js 20 or newer. No runtime dependencies or package installation are needed.

```sh
npm --prefix app run build
npm --prefix app test
npm --prefix app run verify
```

The build generates 76 routes in `app/dist/`. Serve that directory with a static web server, or upload its contents to a static host.

GitHub Pages deployment is configured in `.github/workflows/pages.yml`. In the GitHub repository, open **Settings → Pages → Build and deployment** and set **Source** to **GitHub Actions**. Push these changes to the default branch, or run **Deploy GitHub Pages** manually from the Actions tab on that branch. The workflow builds, tests and verifies the site before publishing `app/dist/`. Other branches do not deploy. No deployment secret or package installation is required.

The workflow reads the Pages base path automatically, supporting both `https://<owner>.github.io/bhr-is-nl/` and a custom domain configured in Pages settings. `app/prepare-pages.mjs` prefixes published HTML/CSS/JSON URLs; browser modules resolve runtime links and requests relative to their published root. To verify a repository deployment locally, run these commands on a fresh build:

```sh
npm --prefix app run build
PAGES_BASE_PATH=/bhr-is-nl node app/prepare-pages.mjs
PAGES_BASE_PATH=/bhr-is-nl npm --prefix app run verify
```

Run the normal build again before running the full test suite, which checks the original root URL output.

Form configuration is in `app/public/config.js`. Without a configured form key, deliverable forms display contact alternatives rather than sending a request. Newsletter and alternate test-quote forms are intentionally local-only.

Page plans, review decisions and execution notes are in `docs/superpowers/`. Visual parity remains open on some pages and responsive widths; passing the functional tests does not certify visual identity.

Generated builds, captured reference pages, screenshot evidence, local archives and Craft session metadata are excluded from Git and remain in the original workspace. The retained visual-planning scripts may require those local captures, Python browser/image dependencies and the visual-diff skill. The older `app/SETUP.txt` describes earlier project stages; the commands and route count above describe the current build.

The responsive layer is `app/public/mobile-parity.css` plus `mobile.mjs`. It activates below 1200px and restores the original desktop DOM/media on exit. Phones through 767px use a full-screen drill-down menu; tablets use a half-width drawer with inline submenus. Original device-specific photo mappings and heading breaks are stored in the accompanying JSON files. Form delivery and validation stay in the existing form modules.

The live CMS serves different phone, tablet and desktop markup/styles based on device selection. The mobile audit therefore sets matching device cookies, user agents, screen sizes, touch capability and DPR1; a narrow desktop-UA screenshot is not a mobile reference. `app/tools/audit-mobile.py`, `audit-mobile-states.py`, `check-mobile.py` and `report-mobile.py` reproduce the captures, interaction checks and per-page metrics. They need Python Playwright/Pillow/NumPy and the installed visual-diff comparer; the content packaging helpers also need BeautifulSoup. Desktop comparisons use immutable local before screenshots, while mobile comparisons use the live device theme. The reports never average page scores or treat unavailable live routes as passes.

The mobile review regressions are in `app/tools/check-mobile-review.py` (Playwright, Pillow). `app/tools/mobile_evidence.py` includes rendering JSON in the build identity and verifies browser-served resource bytes before visual frames are scored. Cached frames must have complete matching metadata and PNG dimensions. The per-page visual status and remaining OPEN gates are documented in `docs/superpowers/execution/2026-11-20-mobile-visual-review.md`; desktop preservation compares the saved local baseline.
