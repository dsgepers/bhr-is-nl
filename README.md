# BHR website recreation

Static recreation of bhr-is.nl, originally created with Craft Anywhere. Built with Node.js ES modules, HTML, CSS and vanilla browser JavaScript. Original image and font assets are packaged locally. The build uses the tracked `app/image-map.json` for page image selection; local reference captures are not required.

Requires Node.js 20 or newer. No runtime dependencies or package installation are needed.

```sh
npm --prefix app run build
npm --prefix app test
npm --prefix app run verify
```

The build generates 82 routes in `app/dist/`. Serve that directory with a static web server, or upload its contents to a static host.

GitHub Pages deployment is configured in `.github/workflows/pages.yml`. In the GitHub repository, open **Settings → Pages → Build and deployment** and set **Source** to **GitHub Actions**. Push these changes to the default branch, or run **Deploy GitHub Pages** manually from the Actions tab on that branch. The workflow builds, tests and verifies the site before publishing `app/dist/`. Other branches do not deploy. No deployment secret or package installation is required.

The workflow reads the Pages base path automatically, supporting both `https://<owner>.github.io/bhr-is-nl/` and a custom domain configured in Pages settings. `app/prepare-pages.mjs` prefixes published HTML/CSS/JSON URLs; browser modules resolve runtime links and requests relative to their published root. To verify a repository deployment locally, run these commands on a fresh build:

```sh
npm --prefix app run build
PAGES_BASE_PATH=/bhr-is-nl node app/prepare-pages.mjs
PAGES_BASE_PATH=/bhr-is-nl npm --prefix app run verify
```

Run the normal build again before running the full test suite, which checks the original root URL output.

All 26 enquiry, service, appointment, quote, job application and newsletter forms use [Web3Forms](https://docs.web3forms.com/getting-started/api-reference). Their shared public access key is `formAccessKey` in `app/public/config.js`; change it and rebuild to replace the destination.

Forms post natively to `https://api.web3forms.com/submit` with `access_key`, a purpose-specific `subject`, an absolute `redirect` and a hidden `botcheck` checkbox. The visitor's `email` supplies the reply address. Existing validation, wizard steps, privacy consent and the 4 MB combined attachment limit are preserved. CV uploads use `attachment` and require Web3Forms PRO. Newsletter requests are emailed for manual processing, with no automatic mailing-list integration.

Each purpose has a styled thank-you page: `/bedankt/contact/`, `/bedankt/service/`, `/bedankt/afspraak/`, `/bedankt/offerte/`, `/bedankt/sollicitatie/` and `/bedankt/nieuwsbrief/`. `redirect` is populated with the absolute URL for the current site, including a repository base path on GitHub Pages. JavaScript supplies that URL before enabling submit; without JavaScript visitors see an email alternative. Edit page copy in `app/thank-you.mjs` and styles in `app/public/thank-you.css`.

For browser verification, serve `app/dist` on port 4173 and run `app/tools/check-forms-browser.py` with a Python environment that has Playwright/Chromium. The tool intercepts every POST locally: it checks the payload and follows a simulated redirect without sending email. It also checks invalid fields, wizard validation, CV uploads, oversized attachments and mobile/desktop thank-you layouts. Actual Web3Forms acceptance and inbox delivery require a separate manual test after publishing; intercepted tests do not verify account entitlements or provider delivery.

Page plans, review decisions and execution notes are in `docs/superpowers/`. Visual parity remains open on some pages and responsive widths; passing the functional tests does not certify visual identity.

Generated builds, captured reference pages, screenshot evidence, local archives and Craft session metadata are excluded from Git and remain in the original workspace. The retained visual-planning scripts may require those local captures, Python browser/image dependencies and the visual-diff skill. The older `app/SETUP.txt` describes earlier project stages; the commands and route count above describe the current build.

The responsive layer is `app/public/mobile-parity.css` plus `mobile.mjs`. It activates below 1200px and restores the original desktop DOM/media on exit. Phones through 767px use a full-screen drill-down menu; tablets use a half-width drawer with inline submenus. Original device-specific photo mappings and heading breaks are stored in the accompanying JSON files. Form delivery and validation stay in the existing form modules.

The live CMS serves different phone, tablet and desktop markup/styles based on device selection. The mobile audit therefore sets matching device cookies, user agents, screen sizes, touch capability and DPR1; a narrow desktop-UA screenshot is not a mobile reference. `app/tools/audit-mobile.py`, `audit-mobile-states.py`, `check-mobile.py` and `report-mobile.py` reproduce the captures, interaction checks and per-page metrics. They need Python Playwright/Pillow/NumPy and the installed visual-diff comparer; the content packaging helpers also need BeautifulSoup. Desktop comparisons use immutable local before screenshots, while mobile comparisons use the live device theme. The reports never average page scores or treat unavailable live routes as passes.

The mobile review regressions are in `app/tools/check-mobile-review.py` (Playwright, Pillow). `app/tools/mobile_evidence.py` includes rendering JSON in the build identity and verifies browser-served resource bytes before visual frames are scored. Cached frames must have complete matching metadata and PNG dimensions. The per-page visual status and remaining OPEN gates are documented in `docs/superpowers/execution/2026-11-20-mobile-visual-review.md`; desktop preservation compares the saved local baseline.
