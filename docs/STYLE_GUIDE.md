# BHR Industrial Solutions — current style guide

Inspected 20 November 2026. This is a reference to the repository implementation, not a redesign or a declaration that every existing choice is intentional. **Not explicitly defined** means no explicit shared rule was found. Recommendations are kept in [DESIGN_AUDIT.md](DESIGN_AUDIT.md).

## Architecture and evidence

The application generates static HTML with Node ES modules, CSS and vanilla browser JavaScript. There is no framework runtime, Tailwind, CSS module system, SCSS, component package, or dependency installation. `app/build.mjs` writes routes to `app/dist/<route>/index.html`, a search index and sitemap. `app/components.mjs` provides HTML string helpers and the shared document shell. Page implementations live in `inner-pages.mjs`, `parity-pages.mjs`, `secondary-pages.mjs`, `secondary-components.mjs`, `secondary-projects.mjs` and `secondary-forms.mjs`.

The stylesheet order matters:

1. `app/public/theme.css`: base fonts, tokens, primitives, sections, and substantial later overrides.
2. `app/public/responsive.css`: shared icon refinements, fixed-header behavior, ≥1700px layouts and motion-reveal animations.
3. `app/public/inner-pages.css`: loaded on `.secondary` routes; flowing inner layouts.
4. `app/public/parity.css`: loaded on `.parity-page`; scoped reference reconstruction.
5. `app/public/secondary-parity.css`: loaded on `.secondary-parity`; further route-specific refinements.

`components.mjs:layout()` chooses these classes and styles. `secondary-pages.mjs:secondaryOptions()` assigns route classes and optional `.secondary-compact-tablet`. Later selectors, media queries and specificity must be considered together; the first declaration is often not the effective one. The appendix inventories all literal CSS colors and custom-property declarations, including historical overrides and decorative exceptions.

The interactive route is `/style-guide`. It uses the ordinary `.secondary` shell, real helpers (`brand`, `inline`, `img`, `secondaryContactForm`, `arrowIcon`), actual service/project data, and scoped `.parity-page` specimens. Its extra CSS and JavaScript are loaded only on this route. Layout wrappers and local demo messages belong to the documentation, not the production component API. The guide loads `parity.css` and `secondary-parity.css` for those scoped specimens; global `@font-face` declarations also become available. No existing production stylesheet is edited.

## Brand identity

The brand is BHR Industrial Solutions, with the “Your system integreator” tagline and blue emphasis on “great.” Observed personality: technical, precise, collaborative and industrial. This is an interpretation of the implementation, not an externally supplied brand strategy.

- Color logo: `app/public/logo.svg`; inverse: `logo-white.svg`. Both have a 187 × 123 viewBox. `components.mjs:brand(white, original)` emits the logo and linked tagline.
- Parity/original variants: `app/public/assets/images/bhr-brand.svg` and `bhr-brand-white.svg`. The shared layout chooses these when parity is enabled.
- Base header image: 100 × 66px; ordinary inner header: 110 × 73px, mobile 75 × 50px. At ≥1700px: 140 × 92px with vertical offset. Base footer: 150 × 99px. Parity rules supply additional route-specific dimensions.
- Color logo appears on white; white logo appears on navy. Preserve the packaged proportions. Minimum size, clear space, co-branding and prohibited usage: **Not explicitly defined**.
- Observed visual conventions: bold geometric headings, large photography, generous sections, white/pale/navy surfaces, yellow pill CTAs, horizontal blue stripes, restrained borders and shadows.
- No general illustration or icon package is installed. Industrial photos and decorative stripe SVGs are packaged locally.

## Color system

Values below are exact source values. Hex alpha is retained where used; it is not a new solid color.

| Role | Base token/value | Scope and source |
| --- | --- | --- |
| Primary navy | `--navy: #1a2e55` | Main dark surfaces, navigation, button hover; `theme.css :root` |
| Primary action/blue | `--blue: #0096cd` | Accents, link hover, focus, checkboxes |
| Secondary light blue | `--lightblue: #83d0f5` | Inverse eyebrows, footer accents, decoration |
| Pale surface | `--pale: #ecf6fc` | Base backgrounds |
| Yellow CTA | `--yellow: #fde74c` | Base primary buttons |
| Body ink | `--ink: #010e19` | Body text |
| Process section | `--how: #2d4e8b` initially; **#2c4d8d final** | Later `theme.css :root` wins |
| White | `#fff` / `white` | Surfaces and inverse text; no token |
| Black | `#000` | Base primary button text; no token |
| Parity pale | `--pale: #eaf5fc` | `.parity-page` and literal parity surfaces |
| Parity yellow | `#ffeb4c` | `.parity-page .button`; `parity.css`. `.secondary-parity .button:not(.outline)` later returns filled buttons to #fde74c |
| Parity cyan | `#00a3d9` | Parity eyebrow and checkbox accent |
| Secondary hero | `#2e518e` | Secondary utility/hero/job surfaces; `secondary-parity.css` |
| Base field border | `#b8c8d6` | `.static-form` and search inputs |
| Header circle border | `#b2bfd2` | Base; parity uses `#aabbd0` |
| Branch border | `#b6cedd` | Base branch cards |
| FAQ divider | `#b9c6cf` | Base FAQ |
| Footer muted | `#a8b5cc` | Base footer legal text |
| Parity field/card border | `#0000001a` | 10% black |
| Parity divider/shadow | `#0002` | Expanded #00000022; about 13.33% black |
| WhatsApp green | `#18cf6e` | One-off `.parity-whatsapp`, not a success token |

No structured neutral ramp or semantic success/warning/error/information palette is defined. Status text uses `.form-status` navy. Native validation and browser disabled controls supply some states. Do not relabel brand blue as an information token or WhatsApp green as global success.

### State colors

Base links inherit text; hover uses `--blue`. Base buttons are yellow/black; hover navy/white. `.outline` starts transparent/currentColor and hovers yellow/ink with yellow border. `.button.white` supplies white text on inverse backgrounds. Parity `.button` and `.button:hover` override the outline hover background too, so parity outline hovers navy/white. Secondary parity restores filled button background to #fde74c with a later, more specific selector; that selector also wins over the earlier hover background, while hover text remains white. Active and disabled colors: **Not explicitly defined**. Disabled buttons get `cursor:wait` without a separate palette. Selected project-filter pills use `#83d0f5` fill and navy text; unchecked pills have a light-blue border. See `secondary-parity.css .secondary-project-filters`.

## Typography

Fonts are local WOFF2, `font-display:swap`:

| Family | Files and declared weights | Fallbacks |
| --- | --- | --- |
| `roboto` | `roboto-regular.woff2` 400; `roboto-medium.woff2` declared 500–900 | Arial, helvetica, sans-serif |
| `oxanium` | `oxanium-medium.woff2` 500; `oxanium-semibold.woff2` declared 600–900 | Arial, helvetica, sans-serif |
| `bhr-roboto` | Same Roboto regular 400 and medium 500 | Arial, Helvetica, sans-serif |
| `bhr-oxanium` | Oxanium medium 500 and `bhr-oxanium-semibold.woff2` 600 | Arial, Helvetica, sans-serif |

`theme.css` provides `--body-font`, `--heading-font`; parity overrides these. Declared 700 headings can resolve to the available semibold face; packaged files do not include a separate bold font. Additional hashed font files exist but the active CSS URLs above govern rendering.

| Specimen / role | Size / line-height / weight | Notes |
| --- | --- | --- |
| Base H1, H2 | 50px / 1.1 (55px) / 700 | Oxanium; both share a rule |
| Base H3 | 23px / 1.1 (25.3px) / 700 | Cards and subheadings |
| Base H4 | Inherited body size; browser bold unless scoped | Footer explicitly 18px, weight 400, light blue |
| H5, H6 | **Not explicitly defined** | Browser defaults; not an established design hierarchy |
| Homepage hero display | 100px / .9 / 500 | `.hero-title` is a div, not H1 |
| Process H3 | 50px / 1.1 / 700 | `.how-copy h3` exception |
| Base body | 18px / 1.6 / 400 | Paragraphs use 1.7 and 30px vertical margins |
| Eyebrow | 18px / 1 / 500 | 1px letter-spacing, 20px bottom margin |
| Button | 17px / 1 / 500 | Footer, cookie and parity form overrides exist |
| Inline action | 17px / 1.3 / 500 | 14px gap to outlined arrow |
| Base labels | 18px / 1.5 | Field font 18px |
| Parity body | 16px / 1.6 / 400 | `.secondary-parity` changes inherited line-height to 2 |
| Parity hero H1 | 65px / .88 (57.2px) / 700 | Not interchangeable with ordinary H1 |
| Parity form label/input | 14px / 17.5px | Labels later set weight 500; inputs 400 |
| Secondary prose | 18px / 30.6px | 24px paragraph bottom margin initially; later scoped rules vary |
| Secondary prose H3 / H4 | 30/33px; 24/26.4px | 32px top margins; H3 15px bottom, H4 0 |
| Footer body / legal | 16px / 1.6; legal 14px | Base helper text 16px |

Responsive inner headings: 50px desktop → 42px at ≤900px → 34px / 1.15 at ≤600px (`inner-pages.css`, which overrides earlier theme 36px). Parity and secondary compact-tablet rules have separate values, including 48.3333px utility H1, 38.3333px section headings, 20.3333px card headings and 17px body. These are captured-route exceptions, not a fluid global type scale. Letter spacing outside eyebrows is generally normal unless a selector says otherwise.

Actual specimen structure:

```html
<div class="eyebrow">Schakel in elk proces</div>
<h1>Industriële automatisering</h1>
<h2>Samen maken we het <span class="accent">great</span></h2>
<h3>Software engineering</h3>
<p>Betrouwbare techniek begint bij een helder proces.</p>
<a class="button" href="/afspraak-maken">Afspraak maken</a>
```

Heading level follows content hierarchy even where H1 and H2 share appearance. H4–H6 should not be presented as an established six-level branded scale.

## Layout and spacing

No named spacing ramp exists. Common measurements: 5, 10, 15, 20, 25, 30, 38, 40, 60, 80, 100 and 120px. These are observed values, not mandated multiples. Fractions such as 14.5px and geometry-specific values are retained in source.

Base root sizing variables: `--body-size:18px`, `--heading-size:50px`, `--card-title-size:23px`, `--gutter:100px`, `--content-width:1720px`, `--radius:30px`, `--section-pad:120px`, `--card-gap:38px`. Many declarations repeat literal equivalents rather than consuming these variables. Inner pages consume `--section-pad` (120/80/60px).

| Pattern | Current dimensions and alignment | Source |
| --- | --- | --- |
| Base container | width calc(100% - 200px), max 1720px, margin auto | `theme.css .container` |
| Inner container | max 1520px; width minus 200/100/60/40px | `inner-pages.css .secondary .container` |
| Parity container | width minus 200px, max 1720px; later exceptions | `parity.css .parity-container` |
| Secondary container | width minus 200px, max 1520px | `secondary-parity.css .secondary-container` |
| Section | Base commonly padding 120px vertically, fixed heights on homepage | `theme.css` section selectors |
| Split image/prose | Equal minmax columns, 100px gap; 50px then 40px gaps | `inner-pages.css .split` |
| Service grid | Four columns, 38px column gap, 60px row gap on inner pages | `inner-pages.css .service-grid` |
| Project grid | Three columns; featured reference uses 40fr/27fr/27fr | `inner-pages.css .project-grid` |
| Paragraph rhythm | 30px vertical base; copy blocks commonly max 425/480/620px | `theme.css`, `parity.css` |
| CTA actions | Flex, 20px gaps, wrapping; phone inner CTA stacks with 15px gap | `theme.css`, `inner-pages.css` |
| Footer | Multi-column, legal row split; inner responsive reflow | `components.mjs:footer`, `inner-pages.css` |

### Breakpoints and actual responsive conventions

- Base theme uses 1550, 1199, 600px maximum queries, 1200, 1600px minimum queries and the 601–1199px band. Later ≥1700px refinements govern wide layouts.
- Ordinary inner pages: navigation collapses at ≤1399px; gutters shrink to 50px. At ≤900px, gutters 30px, section padding 80px, split content stacks, service/project grids have two columns. At ≤600px: gutters 20px, sections 60px, 80px header, project cards stack; services retain two columns because the later inner stylesheet overrides base one-column rules.
- Parity pages primarily use ≤1199, ≤600 and ≥1700px. Some preserve narrow captured columns, vertical navigation, fixed widths and clipping rather than ordinary reflow. `.secondary-compact-tablet` adds a 601–1199px normalization for selected routes.
- Homepage mobile deliberately retains large fixed sections, a 999px-wide header and very narrow content columns; do not mistake this for an intended reusable mobile system. This is an audit finding.
- No centralized breakpoint tokens or universally consistent tablet mode exists.

## Component reference

The components are HTML-generating functions, not framework components. Use shared functions for production composition and preserve the appropriate body classes. All components inherit the focus rule unless a scope overrides it. Values below are established defaults; page-specific geometry stays in its scoped stylesheet.

| Component | Appearance, variants, dimensions, states | Usage and accessibility | Source |
| --- | --- | --- | --- |
| Primary button/link | Inline flex; min-height 47px; 1px transparent border; radius 30px; padding ends as 14px 36px in theme; yellow/black. Parity radius 32px and 15px 36px; latest parity form button 17px/16px with 14.5px 36px padding | `<button>` for actions, `<a href>` for navigation; focus 3px blue with 5px offset. Disabled wait cursor; loading text plus disabled. No general size API | `components.mjs:link`, `theme.css .button`, `parity.css` |
| Outline/inverse button | `.button.outline`, optional `.white`; transparent with currentColor border. Base hover yellow; parity hover navy | Place white text on inverse backgrounds; avoid undocumented color combinations | Same sources |
| Inline action/arrow | 17px label, gap 14px; 46×30px outlined pill; SVG 20px. Parity arrow 48×30px | `inline(text,url)` provides linked text; decorative SVG hidden from AT | `components.mjs:inline`, `public/icons.mjs` |
| Header/nav/dropdown | White/fixed base header, navy links; submenu 250px wide and shadow; 48px base circle controls. Inner header 90px, 80px phone, 78px wide; parity differs | Hover, focus-within or `.open` exposes submenu; toggle uses aria-expanded. Escape closes menu; outside click closes dropdown. Mobile toggle aria-controls/expanded | `components.mjs:header`, `site.mjs`, all scoped styles |
| Text/email/tel/search | Base white square field, 1px #b8c8d6, padding 15px 20px, margin-top 10px, 18px type | Wrapped labels; required/autocomplete attributes. Native invalid UI; no custom error color. Search fetch errors appear as text | `components.mjs:contactForm`, `secondary-forms.mjs:secondaryField`, `theme.css`, `site.mjs` |
| Parity fields/form panel | White bordered panel; base padding 100px 60px 60px; two columns, 25px column gap, final 15px row gap. Inputs 49.5px high, radius 5px, 15px padding/top margin, 14px type. Textarea initially 57px; section-specific overrides | Shared `secondaryContactForm`; template starts submit disabled until JS initialized. Delivery via config or contact alternative; no fake success | `secondary-forms.mjs`, `parity.css .parity-form`, `site.mjs` |
| Select | Native dropdown, same field styling; birth date has three labeled selects | Preserve label or aria-label and prompt where present; wizard validates current step | `secondary-forms.mjs`, `components.mjs:quoteForm` |
| Checkbox/consent | Base 20×20px, blue accent, 15px label gap; parity 14×14px, cyan accent, 6px gap; further consent layout overrides | Wrapped label is larger than box; required privacy consent links underlined. Native disabled necessary-cookie option | `theme.css .checkbox`, `parity.css`, `secondaryConsent()` |
| Radio filter pills | Native input visually transparent, pill border light blue, padding ends at 14.5px 25px; selected light blue/navy | Named radio group and fieldset legend; visible focus on sibling span (2px white, offset 4px). Query-state synchronization | `secondary-projects.mjs`, `secondary-parity.css .secondary-project-filters`, `secondary.mjs` |
| File upload | Native file input under custom upload layout, icon, filename; accepts PDF/DOC/DOCX/JPG | Label/aria-label; helper text says max 4MB, validation checks total file size. Update filename on change | `secondary-forms.mjs:secondaryApplicationForm`, `parity.css`, `site.mjs` |
| Service card | Flat image/title/action, no panel shadow/radius; image 352:427, title margin 30px; base H3 23px. Inner phone 21px and 20px margin | Base action fades in hover/focus-within; ordinary inner actions visible; fine-pointer reference actions fade. Links have real destinations | `components.mjs:serviceCards`, `inner-pages.css`, `parity-pages.mjs` |
| Project card/row | Base image height 450px; inner aspect .9; grouped project aspect 1.27 and 30px title; secondary routes have alternating rows | Same focus-within action convention; category filters update results and URL | `components.mjs:projectCards`, `secondary-projects.mjs`, scoped styles |
| Partner/team/branch/value/fact cards | Logo contain at 90px (70px inner phone); team max 352px; branch 1px border/padding 40px 25px; values 100px letter, facts 65px metric | Decorative versus meaningful image alternatives depend on content. No unified Card primitive or size/variant API | `components.mjs:branchCards/partners`, `inner-pages.mjs`, `secondary-components.mjs`, `inner-pages.css` |
| Accordion/FAQ | Native details/summary. Base bottom border/padding 25px; plus rotates 45°. Final parity boxed #0002, 10px separation, summary 25px padding and Oxanium 18/19.8px; expanded minus | Native keyboard disclosure; summary focus outline. Secondary final plus positioned right 25px | `components.mjs:faqSection`, `secondary-components.mjs:secondaryFaq`, `parity.css`, `secondary-parity.css` |
| Search dialog | Native dialog max 1000px, width 90vw, padding 80px, backdrop #1a2e55d9; close icon 40px | showModal, focus search input, Escape native close, backdrop dismissal; result area aria-live. Trigger remains link fallback | `components.mjs:searchDialog`, `site.mjs`, `theme.css` |
| Lightbox/gallery | Native dialog padding 50px; max 95vw/95vh, image contain max 80vh. Secondary gallery has bounded previous/next index | Label dialog and image; keyboard dialog behavior; arrows disable at bounds where implemented | `components.mjs`, `secondary-projects.mjs`, `secondary.mjs`, `theme.css` |
| Cookie dialog | Fixed overlay z100, black 30% backdrop, white 557px panel right/bottom 30px, padding 30px; two-column actions; inner mobile width minus 40px | role=dialog/aria-modal label; localStorage choice. No focus trap or focus return in banner; see audit | `components.mjs:cookie`, `site.mjs`, styles |
| Form status | Navy paragraph, grid span all; role=status/aria-live polite | Loading, success, unavailable, file and generic failures are text. Status clears on edit. No separate alert component | `secondary-forms.mjs`, `site.mjs`, `behavior.mjs` |
| Wizard | Fieldsets/legends; hidden inactive steps; previous/next/submit controls; base step pills 8px 16px, current navy/white | Validate before advancing, focus first field of next step; final validation reveals invalid step. Enter advances except textarea | `components.mjs:quoteForm`, `secondary-forms.mjs:secondaryQuoteForm`, `site.mjs`, `secondary.mjs` |
| Hero/carousel/timeline | Image slides crossfade; dots 12px, active white; carousel controls 50×28px with 20px radius; track transforms | Inactive hero slides inert/aria-hidden; dots aria-pressed; hero auto 6s, partners 5s. Partners pause on hover/focus and hidden document, swipe threshold 35px. No hero pause button | `components.mjs:hero`, `site.mjs`, `secondary-components.mjs`, `secondary.mjs`, `parity.css` |
| Footer | Navy, white copy/light-blue links, white logo, contact icons, social links, legal row; no universal fixed height | Semantic footer/nav and named icon links; some social hrefs are placeholders. Inner footer flows, homepage has fixed heights | `components.mjs:footer`, theme/inner/parity CSS |

Reusable tables, tab widgets, tooltip components, generic badges/tags, toast notifications and numbered pagination: **not found**. Category pills are radio filters, step indicators belong to the wizard, and timeline year controls are carousel controls; they are not evidence for a general tab/badge/pagination system. Do not fabricate examples for absent components.

### Code conventions

Use existing helpers from `components.mjs`, escape dynamic text, and let the build's route class decide the styling family:

```js
import {link, inline, esc, img} from './components.mjs';
const action = link('Afspraak maken', '/afspraak-maken');
const secondaryAction = link('Neem contact op', '/contact', 'button outline');
const readMore = inline('Lees verder', '/projecten');
const heading = `<h3>${esc(title)}</h3>`;
const photograph = img(source, title); // resolves packaged media; escaped alt
```

```js
import {secondaryContactForm} from './secondary-forms.mjs';
const form = secondaryContactForm();
// Requires parity/secondary styles and the existing config/site scripts.
// Live forms use configured delivery; the style-guide route intercepts submission.
```

### Additional scoped patterns

- Share popover: native details/summary in job header; 14px/20px summary with 20px SVG, white menu min-width 200px, padding 15px, border #d9d9d9, shadow 0 5px 20px #0002; Escape closes and restores summary focus (`secondary-pages.mjs`, `secondary-parity.css .secondary-job-share`, `secondary.mjs`).
- Newsletter: email input and initially disabled submit; local-only demonstration behavior, polite status; button width 163px/min-height 49.5px (`secondary-forms.mjs:secondaryNewsletterForm`, `secondary.mjs`, `secondary-parity.css`). Do not imply a subscription was delivered.
- Cookie preferences: necessary/optional checkbox groups and explicit save status; more detailed secondary purpose descriptions use 18px controls (`secondary-pages.mjs`, `secondary.mjs`, `secondary-parity.css .secondary-cookie-panel`).
- Timeline: scroll/transform track, year buttons 50/55px Oxanium; inactive opacity .3, selected state and boundary buttons synchronized (`secondary-components.mjs:secondaryTimeline`, `secondary.mjs`, `secondary-parity.css`).
- Employee/contact aside, reference/testimonial block, location/map split, image/prose article and CTA are section-level compositions, not generic widgets. Their shared renderers are `secondaryEmployee`, `secondaryReference`, `secondaryMap`, `secondaryArticle`, `secondaryCta`; all live in `secondary-components.mjs` and use the scoped rules in `secondary-parity.css`. Location cards have #d9d9d9 borders and 40px content padding.

## Effects

- Radii: base fields/images/cards square; parity fields 5px; carousel/arrow exceptions 20px; base pill 30px; parity button 32px; circles 50%/100%. `--radius:30px` exists but is not a universal source of truth.
- Borders usually 1px; active navigation pseudo underline 2px in final parity rules; focus 3px with 5px offset.
- Overlay/menu shadow `0 0 30px #0002`; scrolled base header `0 3px 20px #1a2e5526`; final parity header `0 0 30px rgba(0,0,0,.15)`; share popover `0 5px 20px #0002`.
- Gradients: CTA `linear-gradient(90deg,#8cdbf6 40%,#2d4e8b)`; hero navy-to-transparent; reference intro combines navy-alpha gradients over bgmaincolumn.png. Secondary decorative stripes use per-stripe colors, widths and heights from `secondaryStripes(mode)` and scoped CSS. They are artwork parameters, not semantic tokens.
- Transitions: hero opacity 1.3s ease, action opacity .2s, fixed header shadow .3s ease; track transitions scoped in parity. Content entrance .8s and hero entrance .9s ease use opacity and translate.
- Reduced motion: no reveal observation on reduced-motion preference; animation only under no-preference; slide and parity track transitions disabled. Hero automatic cycling does not start under reduced motion. The scroll button explicitly requests smooth scrolling in JavaScript, independently of the CSS preference; see audit.
- There is no centralized elevation, animation or opacity token scale.

## Imagery and iconography

Sources: `app/assets-manifest.json`, `parity-assets.json`, `secondary-assets.json`, `app/public/assets/images/` and `app/public/icons.mjs`. Manifests map original URLs to local paths and hashes. `data.mjs:media()` handles alternate CMS image sizes. Preserve local packaging.

Photography: machinery, panels, wiring, industrial buildings, real staff, workshop scenes. Common ratios: 352:427 service, 940:740 split, 1920:700 document banner, .85 fact portrait, .9 inner project, 1.27 grouped project; base hero width factor .46875 and wide min-height 660px. Object-fit cover crops photographs; logos/partner marks use contain. Hero/inverse overlays improve text legibility but contrast varies with image and crop.

Icon conventions: inline shared arrow uses 24-unit viewBox, 20×20px output, stroke 1.5/currentColor, rounded caps/joins, aria-hidden/focusable=false. Header inline icons are 20px stroke 1; packaged SVGs include header-phone/search, footer-mail/phone/malfunction, checkmark, career-upload and social marks. Base fallback icons also use characters (⌂, ✉, ♧, ☰); parity uses original SVG assets. This is an inconsistency, not an installed icon library. Base circle actions are 48px; footer round icons 38px.

## Accessibility: current implementation

- Shared skip link targets `#page-content`; focus moves its position into view. Its destination is a div without tabindex; verify keyboard focus behavior manually.
- Native anchors/buttons/form controls, wrapped labels, required and autocomplete attributes, fieldsets and legends, details/summary, native dialogs, aria-expanded menu toggles and polite status regions are present.
- Global focus-visible: 3px solid `--blue`, 5px offset on links/buttons/summary/inputs/selects/textarea. Project radio pills have a dedicated visible sibling outline. No production focus rules were changed for this guide.
- Buttons generally meet a 44px height convention at 47px; header circles 48px (ordinary inner 42px). Slide dots 12px, arrows 46×30px and checkboxes 14/20px are smaller; actual linked label area and target spacing need inspection.
- Hero inactive content becomes inert; carousel clones are inert/aria-hidden. Native search/lightbox dialogs use showModal. Cookie banner only uses dialog semantics and lacks equivalent modal focus management.
- Reduced-motion support is partial as described above.

Approximate WCAG relative luminance contrast, calculated from exact solid sRGB values (not measured over photos):

| Foreground / background | Ratio | Normal text observation |
| --- | --- | --- |
| #010e19 / #ffffff | 19.48:1 | Above 4.5:1 |
| #1a2e55 / #ffffff | 13.41:1 | Above 4.5:1 |
| #0096cd / #ffffff | 3.36:1 | Below 4.5:1 |
| #0096cd / #ecf6fc | 3.07:1 | Below 4.5:1 |
| #83d0f5 / #1a2e55 | 7.86:1 | Above 4.5:1 |
| #000000 / #fde74c | 16.71:1 | Above 4.5:1 |

The validation script used for this task recalculates these values; figures are rounded. Passing a pair does not certify a component. See audit for focus contrast, moving content, clipped responsive layouts, placeholders and modal limitations. Manual assistive-technology and complete page-by-page contrast verification remain necessary.

## Validation and limitations

The initial clean-worktree build failed because `app/data.mjs` unconditionally reads ignored `app/reference/image-map.json`. For local checks, the existing file was copied from the original checkout, without editing tracked build code. A fresh clone still needs that input; this pre-existing reproducibility issue is recorded in the audit.

Commands: `npm --prefix app run build`, `npm --prefix app test`, `npm --prefix app run verify`. There is no configured lint or type-check script and no TypeScript; added JS modules can be syntax-checked with `node --check`. `verify:likeness` depends on external/local capture evidence and is not a general build check. Browser review uses representative homepage/contact/project and style-guide routes; it does not certify every route, browser or screen reader. No live form requests are needed or made.


## Source inventory appendix

This inventory retains every unique literal hex/RGB/HSL/named color and custom-property declaration found in the production CSS (excluding documentation CSS). It is evidence, not an endorsed palette. Initial values may be superseded; inspect the selector/media context in the linked source. Artwork colors are intentionally included.


### app/public/theme.css

| Literal color | Source lines |
| --- | --- |
| `#000` | 3, 8, 19 |
| `#0000004d` | 11 |
| `#0002` | 4, 11 |
| `#0096cd` | 2 |
| `#010e19` | 2 |
| `#1a2e55` | 2, 19 |
| `#1a2e5580` | 5 |
| `#1a2e5599` | 19 |
| `#1a2e55bb` | 9 |
| `#1a2e55cc` | 19 |
| `#1a2e55d9` | 12 |
| `#2c4d8d` | 22 |
| `#2d4e8b` | 2, 9 |
| `#5a96c344` | 8 |
| `#83d0f5` | 2 |
| `#83d0f530` | 9, 19 |
| `#8cdbf6` | 9 |
| `#a8b5cc` | 10 |
| `#b2bfd2` | 4 |
| `#b6cedd` | 12 |
| `#b8c8d6` | 12 |
| `#b9c6cf` | 12 |
| `#ccd4df` | 12 |
| `#ecf6fc` | 2 |
| `#fde74c` | 2 |
| `#fff` | 3, 4, 5, 6, 8, 9, 10, 11, 12, 22 |
| `#ffffff4d` | 10 |
| `currentColor` | 3, 4 |
| `transparent` | 3, 4, 5, 8, 9, 12, 16, 19 |

Custom properties (including component parameters):

| Property | Declared values |
| --- | --- |
| `--blue` | `#0096cd` |
| `--body-font` | `roboto,Arial,helvetica,sans-serif` |
| `--body-size` | `18px` |
| `--card-gap` | `38px` |
| `--card-title-size` | `23px` |
| `--content-width` | `1720px` |
| `--gutter` | `100px` |
| `--heading-font` | `oxanium,Arial,helvetica,sans-serif` |
| `--heading-size` | `50px` |
| `--how` | `#2c4d8d`; `#2d4e8b` |
| `--ink` | `#010e19` |
| `--lightblue` | `#83d0f5` |
| `--navy` | `#1a2e55` |
| `--pale` | `#ecf6fc` |
| `--radius` | `30px` |
| `--section-pad` | `120px` |
| `--yellow` | `#fde74c` |

### app/public/responsive.css

| Literal color | Source lines |
| --- | --- |
| `#000` | 116 |
| `#1a2e551a` | 104 |
| `#1a2e5526` | 7 |
| `#1a2e5544` | 111, 113 |
| `#1a2e5577` | 104 |
| `#83d0f52e` | 113, 114 |
| `#83d0f53d` | 112 |
| `#83d0f54d` | 112, 115 |
| `transparent` | 111, 114, 116 |

Custom properties (including component parameters):

| Property | Declared values |
| --- | --- |
| — | None |

### app/public/inner-pages.css

| Literal color | Source lines |
| --- | --- |
| `#1a2e55` | 120 |
| `#1a2e5526` | 182 |
| `#1a2e5566` | 90 |
| `#1a2e5599` | 120 |
| `#1a2e55cc` | 120 |
| `#fff` | 181 |
| `transparent` | 90, 120, 177 |
| `white` | 77, 119, 131 |

Custom properties (including component parameters):

| Property | Declared values |
| --- | --- |
| `--section-pad` | `120px`; `60px`; `80px` |

### app/public/parity.css

| Literal color | Source lines |
| --- | --- |
| `#0000001a` | 127, 130 |
| `#0001` | 159 |
| `#0002` | 36, 149, 163, 169, 477, 610 |
| `#006fb1` | 596 |
| `#009bd6` | 133 |
| `#00a3d9` | 14, 115, 135, 152, 183 |
| `#010e19` | 7, 15, 129, 130, 157, 182, 630 |
| `#010e191a` | 109 |
| `#015396` | 600 |
| `#044a8b` | 593 |
| `#047eb2` | 602 |
| `#0664a9` | 88 |
| `#0964a8` | 72 |
| `#0a518d` | 599 |
| `#0a5da8` | 609 |
| `#0f5897` | 598 |
| `#148cbd` | 603 |
| `#18cf6e` | 126 |
| `#1a2e55` | 7, 17, 29, 35, 111, 198, 518, 519, 591, 607, 735, 736, 741, 745, 753 |
| `#1a2e5529` | 518 |
| `#1a2e5599` | 52 |
| `#1a2e55cc` | 178 |
| `#1a2e55dd` | 178 |
| `#1a2e55f5` | 52 |
| `#1a4b86a8` | 40 |
| `#204079` | 284, 296 |
| `#20407c` | 547, 581 |
| `#204879` | 38 |
| `#234f8d` | 286, 295 |
| `#234f8e` | 48, 51, 285, 294 |
| `#235091` | 549, 583 |
| `#244076` | 573 |
| `#244178` | 554, 758 |
| `#245294` | 548, 559, 582 |
| `#245396` | 550, 584, 604 |
| `#25427b` | 576 |
| `#273060` | 597 |
| `#2a5f9f` | 289, 298 |
| `#2c4d8d` | 552 |
| `#2e518e` | 82, 191 |
| `#2f5190` | 555, 759 |
| `#305291` | 558 |
| `#315392` | 556, 760 |
| `#335695` | 572, 732 |
| `#345897` | 561 |
| `#3d6b9f` | 288, 297 |
| `#3e6ca1` | 551, 562, 585, 605 |
| `#436ba8` | 553, 574, 608, 757 |
| `#446ca9` | 560 |
| `#518daf` | 601 |
| `#618ac5` | 557 |
| `#6ac3e6` | 69 |
| `#6b95cf` | 575 |
| `#7dd1ee` | 69 |
| `#7fa6b3` | 149 |
| `#83d0f5` | 88, 89, 94, 113, 154, 195, 209, 212, 299, 456, 594, 651, 721, 790 |
| `#83d0f54d` | 720 |
| `#aabbd0` | 32 |
| `#eaf5fc` | 7, 20 |
| `#ecf6fc` | 579, 580 |
| `#fde74c` | 365 |
| `#ffeb4c` | 15 |
| `currentColor` | 16, 93, 616 |
| `rgba(0,0,0,.15)` | 748 |
| `rgba(26,46,85,0)` | 607, 745 |
| `transparent` | 15, 16, 40, 48, 51, 93, 155, 284, 285, 286, 288, 289, 294, 295, 296, 297, 298, 367, 547, 548, 549, 550, 551, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 572, 573, 574, 575, 576, 581, 582, 583, 584, 585, 591, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 608, 732, 736, 757, 758, 759, 760 |
| `white` | 7, 17, 23, 38, 42, 44, 52, 72, 82, 126, 127, 130, 159, 163, 178, 182, 191, 198, 381 |

Custom properties (including component parameters):

| Property | Declared values |
| --- | --- |
| `--body-font` | `bhr-roboto,Arial,Helvetica,sans-serif` |
| `--fact-top` | `614.22px`; `clamp(164.59px,calc(43.275vw - 73.6px),549.56px)` |
| `--heading-font` | `bhr-oxanium,Arial,Helvetica,sans-serif` |
| `--ink` | `#010e19` |
| `--lead-tail` | `30px` |
| `--navy` | `#1a2e55` |
| `--pale` | `#eaf5fc`; `#ecf6fc` |
| `--parity-gutter` | `calc((100vw - 1520px)/2)` |
| `--parity-header` | `116px`; `394px`; `78px` |

### app/public/secondary-parity.css

| Literal color | Source lines |
| --- | --- |
| `#0000001a` | 441, 505 |
| `#0002` | 249, 251, 960 |
| `#006fb1` | 907 |
| `#0096cd` | 766, 777, 871 |
| `#00a3d9` | 41, 265 |
| `#010e19` | 115, 169, 243, 251, 253, 609, 960 |
| `#010e191a` | 214 |
| `#015396` | 911 |
| `#044a8b` | 467 |
| `#047eb2` | 913 |
| `#0964a8` | 177 |
| `#0a5da8` | 124 |
| `#0f5897` | 909 |
| `#148cbd` | 914 |
| `#1687ad` | 694 |
| `#18cf6e` | 702 |
| `#1a2e55` | 42, 62, 65, 73, 84, 110, 166, 256, 408, 422, 441, 615, 619, 885 |
| `#1a2e5529` | 42 |
| `#1a2e55b3` | 107 |
| `#1a2e55bb` | 273 |
| `#1a4b86a8` | 32 |
| `#204079` | 346 |
| `#20407c` | 349 |
| `#234f8d` | 345 |
| `#234f8e` | 344 |
| `#235091` | 351 |
| `#244178` | 9, 578, 897 |
| `#245294` | 14, 350, 902 |
| `#245396` | 352, 915 |
| `#273060` | 908 |
| `#2a5f9f` | 348 |
| `#2e518e` | 19, 28, 174, 202, 206, 219, 229, 237, 276, 321, 329, 385, 477, 572, 581, 601, 606, 630, 732, 895 |
| `#2f5190` | 10, 579, 898 |
| `#305291` | 13, 901 |
| `#315392` | 11, 580, 899 |
| `#345897` | 16, 514 |
| `#3d6b9f` | 347 |
| `#3e6ca1` | 17, 353, 916 |
| `#436ba8` | 8, 577 |
| `#446ca9` | 15, 513, 903 |
| `#518daf` | 912 |
| `#618ac5` | 12, 900 |
| `#6b95cf` | 910 |
| `#83d0f5` | 40, 60, 62, 79, 167, 209, 224, 368, 423, 469, 566, 609, 620, 637 |
| `#aabbd0` | 408 |
| `#d9d9d9` | 459, 472, 532, 677, 960 |
| `#d9e5ec` | 667 |
| `#ddd` | 243 |
| `#eaf5fc` | 27, 54, 272 |
| `#ecf6fc` | 358, 441, 477, 581, 592, 608, 625 |
| `#fde74c` | 531 |
| `#ffffff1a` | 364 |
| `#ffffff20` | 636 |
| `#ffffff4d` | 382, 384 |
| `#ffffff80` | 452 |
| `currentColor` | 656, 778, 883 |
| `rgba(26,46,85,0)` | 422, 619, 885 |
| `transparent` | 7, 32, 273, 343, 356, 376, 514, 577, 632, 737, 751, 890, 892 |
| `white` | 19, 28, 42, 57, 63, 73, 84, 107, 110, 124, 168, 174, 177, 197, 200, 202, 206, 219, 229, 237, 243, 249, 251, 253, 257, 273, 276, 286, 376, 378, 381, 408, 409, 452, 454, 455, 481, 572, 601, 606, 607, 619, 624, 630, 669, 732, 735, 763, 957, 960 |

Custom properties (including component parameters):

| Property | Declared values |
| --- | --- |
| `--parity-header` | `111px`; `78px`; `93px` |
| `--stripe-color` | `#006fb1`; `#015396`; `#047eb2`; `#0f5897`; `#148cbd`; `#204079`; `#20407c`; `#234f8d`; `#234f8e`; `#235091`; `#244178`; `#245294`; `#245396`; `#273060`; `#2a5f9f`; `#2f5190`; `#305291`; `#315392`; `#345897`; `#3d6b9f`; `#3e6ca1`; `#436ba8`; `#446ca9`; `#518daf`; `#618ac5`; `#6b95cf` |
| `--team-area` | `max(0px,min(660px,calc(50% - 100px)))` |

### Rendered validation observations

The homepage computed body is 18px/28.8px Roboto, H1 700 50px/55px Oxanium, button #fde74c and process surface #2c4d8d. Contact computes 16px/32px bhr-roboto, H1 65px/57.2px bhr-oxanium, visible parity fields 14px/17.5px with 5px radius and 49.5px height. Its hidden honeypot is excluded from the visible input specimens. The secondary filled-button override is #fde74c. Guide checks include local form interception, focus outline, image availability (excluding the intentionally empty hidden lightbox image), disclosure, navigation and responsive containment.

### Final check results

- Build: 77 routes generated successfully.
- Existing tests: 129 passed, 0 failed.
- Route verifier: 77 routes, 3524 local links and 1593 image/script references passed.
- Added/modified JS module syntax checks and `git diff --check`: passed. No lint/type-check script exists.
- Baseline comparison: all 77 pre-existing HTML files (76 routes plus 404) and existing assets remained byte-identical. Only the existing search index and sitemap changed to include the new route.
- Browser checks at 1280px, 768px and 390px: no guide-content horizontal overflow; all guide specimen images loaded. Local form interception, focus outline, button feedback and native disclosure were exercised. A hidden lightbox image without a source is part of the existing shell and excluded from image-load assertions.
- Production styles/components were not edited. The ignored reference input was copied only to make local verification possible.
