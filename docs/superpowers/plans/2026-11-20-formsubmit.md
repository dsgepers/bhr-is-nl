# FormSubmit implementation plan

**Goal:** Send every enquiry, application, quote and newsletter form to `dennis@schepe.rs` through FormSubmit, with tailored thank-you pages.

**Architecture:** Standard multipart POST uses FormSubmit's `_next` redirect, `_subject`, `_template=table` and `_honey`. Keep default CAPTCHA, browser validation, wizard progression and the site's 4 MB attachment limit. Resolve redirect URLs at runtime against the published site root, supporting GitHub Pages. Recipient lives in `app/public/config.js` and is shared by the build and browser.

**Design:** Reuse BHR's navy, pale blue, yellow accent, Oxanium headings, diagonal stripes and existing navigation/footer. Dedicated Dutch pages cover contact, quick contact, appointment, quote, application and newsletter. Describe the next step accurately: appointment requests still need confirmation and newsletter requests are emailed, not automatically subscribed. Existing layouts and photo edits remain intact.

**Tech stack:** Existing Node ES modules, static HTML, CSS, vanilla JavaScript. No new dependencies.

## Review focus

- Redirects must stay on the actual site origin and work under `/bhr-is-nl/`.
- Invalid wizard steps and invalid dates must never submit; final errors reveal the relevant step.
- CV attachments must reach the native multipart POST and oversized files must be blocked.
- No success message before FormSubmit accepts a submission; no real emails in verification.
- Newsletter and alternate quote forms must also be connected; search/filter/cookie forms remain local.

## Tasks

- [x] Replace old delivery tests with meaningful FormSubmit action, redirect, recipient and upload validation tests; observe expected failures.
- [x] Centralize form settings and markup, migrate all templates and native submission validation, and remove obsolete demo-only and StaticForms handlers.
- [x] Add six responsive thank-you pages with form-specific copy and useful onward links; keep `/bedankt` compatible.
- [x] Update setup documentation and affected form assertions. Verify protected HTML changed only in intended form/configuration markup before refreshing affected baselines.
- [x] Build, run all tests/link verification, and locally intercept browser submissions for each form type, wizard validation, CV upload and GitHub Pages redirects. Inspect thank-you pages at desktop/mobile widths.

## Execution notes

- User has authorized the FormSubmit migration and thank-you pages. Existing site design supplies the visual direction.
- Work in the active checkout to preserve the running local preview and existing uncommitted photo/header work. No commit, push or deployment is part of this request.
- Documentation: https://formsubmit.co/documentation and https://formsubmit.co/. First submission triggers recipient activation; inbox activation is an external manual step.

- Completed: 26 forms across six purposes; 82 routes built; 138 tests and all link/asset checks pass.
- Browser verification: 22 intercepted submissions at the root plus 22 under `/bhr-is-nl/`, at 1920×1080 and 430×932. Five delayed-startup cases pass. No form requests reached FormSubmit.
- Visual review corrected new-page stylesheet precedence and mobile header contrast. Existing 76 pages have identical HTML outside intended form/config markup and asset version tokens. Reviewed and refreshed the 12 protected hashes accordingly.
- Recipient and imported browser modules now use build content versions to prevent stale configuration after updates. Browser scripts remain dependency-free.
- External limitation: recipient activation and actual inbox delivery require the first real submission and confirmation in the recipient inbox.
