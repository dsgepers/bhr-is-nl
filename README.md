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
