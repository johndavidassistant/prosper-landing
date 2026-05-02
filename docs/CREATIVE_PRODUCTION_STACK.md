# Creative Production Stack

**Permanent operating standard.** Governs all future work involving websites, landing pages, logos, social media posts, brand systems, marketing assets, and client deliverables.

If a build pass departs from this standard, the deviation must be justified in writing in the project task or PR description before merge.

This document is the contract. Read it before starting.

> **Premium Quality Bar (locked, non-negotiable).** Section 11 below is the binding pre-deploy contract for every page and asset shipped under this standard. A page that fails any of those requirements does not ship. The rest of this document explains how to meet that bar.

---

## 1. Core principle

> Premium work is not more effects.
> Premium work is controlled clarity, hierarchy, restraint, speed, and proof.

Every decision is judged against five questions:

1. **Clarity.** Can a stranger understand what we are selling in 15 seconds?
2. **Hierarchy.** Does the eye know where to land first, second, third?
3. **Restraint.** What can we remove without losing meaning?
4. **Speed.** Does the page load and feel fast on a mid-tier mobile device?
5. **Proof.** Can a real claim, quote, photo, or number replace a generic adjective?

A page that fails any of these is not ready.

The work is finished when nothing more can be removed without breaking the meaning, not when nothing more can be added.

---

## 2. Approved website stack

### Runtime

| Layer | Choice | Notes |
|---|---|---|
| Foundation | **Static HTML / CSS / JS** | Hand-authored. No framework unless the brand or scale demands it. |
| Animation | **GSAP 3 + ScrollTrigger** (CDN) | Free since 2024. The only motion library used. |
| Smooth scroll | **Lenis** (CDN) | Desktop only at `>=1024px`. Mobile keeps native scroll. |
| Forms | **Native HTML form + Netlify Forms** as V1 capture, **Apps Script webhook** for routing | Email notification with subject prefix `[BRAND-BRIEF]`, lands in `johndavid.assistant@gmail.com`. Phone push via Gmail mobile. |
| Hosting | **Netlify** | Auto-deploy from `main` branch of GitHub. |

### Build-time

| Tool | Use |
|---|---|
| **Sharp** | Image optimization. Re-encode JPGs at quality 82, mozjpeg, progressive. PNG compression level 9, palette mode. |
| **SVGO** | SVG optimization. Strip metadata, comments, unused defs. |
| **Puppeteer-core** | Screenshot QA. Uses system Chrome (no Chromium download). |
| **Lighthouse** | Pre-deploy audit. Performance, Accessibility, Best Practices, SEO. |
| **Prettier** | HTML / CSS / JS formatting consistency. |

### Already on the system, no install

- `@google/clasp` for Apps Script deploys
- ImageMagick for quick CLI image work
- Python 3 + reportlab + pillow for PDF generation
- Chrome.app as Puppeteer target
- Google Workspace MCP (Gmail / Drive / Calendar)
- Notion MCP, Obsidian MCP
- Claude skills: `ui-ux-pro-max`, `web-design-guidelines`, `frontend-design`, `impeccable`, `figma-implement-design`, `gsd-map-codebase`, `gsd-graphify`, `claude-api`

### Banned from the stack

| Tool | Reason |
|---|---|
| Webflow / Wix / Squarespace | We do not deliver template-built sites. |
| Bootstrap / Bulma / Foundation / Tailwind | We hand-author CSS for premium typographic control. |
| jQuery | Modern vanilla JS is enough. |
| Three.js | Aesthetic does not call for 3D. |
| Framer Motion | React-only. Our stack is HTML-first. |
| Vite / Webpack / Rollup as default | No build pipeline unless the brand or scale demands it. |
| Remotion (for websites) | Heavy. Reserved for Instagram reels and intro videos when those become a deliverable. |
| Playwright | Puppeteer-core covers our QA needs at lower install cost. |
| ESLint | Overkill for our static surface. Prettier covers formatting. |

### Performance targets (Lighthouse mobile, simulated 4G)

| Metric | Target |
|---|---|
| Performance | 90+ |
| Accessibility | 90+ |
| Best Practices | 90+ |
| SEO | 90+ on indexed pages. Thank-you / no-index pages exempt. |
| Largest Contentful Paint | under 2.5s |
| Cumulative Layout Shift | under 0.10 |
| Total Blocking Time | under 200ms |
| Page weight (excluding fonts) | under 250 KB |

---

## 3. Approved design behavior

### Precision Line System

One signature motion pattern. Applied identically across every page in the family.

Allowed motion moments:

- **Hero load reveal.** H1 lifts and fades. Gold rule expands from 0 to full width. Sub + CTA stagger in. Total under 1.2 seconds. Once per visit.
- **Section enter reveal.** Each section, on entering at 78 percent viewport: eyebrow micro-rule expands; content items stagger in with 70ms offsets. Once.
- **Climactic moment.** A pricing number, a key statistic, or a hero word may carry a vertical gold gradient for visual punctuation. One per page maximum.
- **Hover state.** Color and border shifts only. Maximum 200ms. No glow, no lift larger than 4px.
- **Smooth scroll.** Lenis on desktop only. Mobile native scroll preserved.

Banned motion:

- Looping animations after first scroll.
- Parallax over 8 percent of viewport height.
- Scroll-jacking that overrides native velocity.
- Auto-playing carousels.
- Animations longer than 800ms.
- Bounce, elastic, or back easings.
- Cursor-tied effects.
- Loading spinners on under-2-second pages.
- Splash screens or intro overlays.
- Number count-ups longer than 1.2 seconds.

Reduced motion is non-negotiable. Every animation must check `prefers-reduced-motion: reduce` and skip entirely.

### Visual restraint

| Banned | Reason |
|---|---|
| Stock photography | We use real photography or no photography. |
| Generic icon sets | Branded assets only. The wordmark is the icon. |
| Gradient meshes / orbs / glows | Atmosphere comes from layered radials, not decoration. |
| Background patterns | A 1.3 percent material grid texture is the only allowed overlay. |
| Drop shadows over 24px blur | Premium UI shadows are subtle. Heavy shadows are template tells. |
| Card grids with hover lifts greater than 4px | Cards are functional, not bouncy. |
| Bullet emoji | Use a 6px gold dot or a 1px gold dash. |
| Six or more colors per page | The palette is locked at four maximum. |

### Typography rules

- **Two families maximum.** A display family and a body family. Standard pair: Playfair Display (display) plus Inter (body).
- **Tracked uppercase eyebrows at 0.36em.** This is the architectural label signature.
- **Italic moments for emotional pivots.** One italic Playfair line near the close. Used sparingly.
- **No em-dashes, en-dashes, or hyphens used as connectors** in body copy. Wikilinks and proper-noun hyphens are exempt.
- **Mobile typography scales via `clamp()`** so display headlines never break at small viewports.

---

## 4. Logo standard

Every brand mark ships in a complete asset family.

### Required deliverables per brand

| Variant | Purpose |
|---|---|
| Horizontal SVG | Email signature, website header, letterhead, invoice |
| Horizontal PNG (1800px wide) | Fallback for SVG, social headers |
| Square SVG | Favicon, social profile picture, app icon |
| Square PNG (1080×1080) | Instagram avatar, WhatsApp Business avatar |
| Light-context variant | Transparent background or navy-on-light fill, for use on white pages |
| Dark-context variant | For use on deep navy or black surfaces |

### Folder structure (per brand)

```
assets/[brand]/
├── approved/      ← Source of truth. Locked production assets.
├── archive/       ← Past explorations. Do not use in production.
├── rejected/      ← Killed directions. Reference only.
└── README.md      ← States the locked version, usage rules, and what NOT to use.
```

### README contract

The brand's `assets/[brand]/README.md` must include:

1. The currently APPROVED version (e.g., V8).
2. The exact files in `approved/` and what each is for.
3. Hard rules (no exceptions).
4. What is in `archive/` and `rejected/` and why those folders are off-limits for production.

Example: `public/assets/gobig/README.md` already follows this pattern. Future brands must mirror it.

### Hard rules across all brands

- Never composite the wordmark with previous monogram or crest variants.
- Never tilt, rotate, or apply effects (drop shadow, glow, outline) to the mark.
- Never color-shift the gold (no green-gold, no rose-gold, no platinum).
- Never use the mark on a busy or textured background without a solid color block.
- Never scale below 64px on screen. Use the favicon variant if smaller.

---

## 5. Social media standard

Every social asset is treated as a brand deliverable, not a casual post.

### Per-post requirements

| File | Purpose |
|---|---|
| Asset (PNG / JPG / MP4) | Correct platform dimensions. Export-ready. |
| `caption.txt` | The caption written to ship as-is. |
| Optional `hashtags.txt` | Hashtags relevant to platform and audience. Skip if account voice does not use them. |

### Platform dimensions

| Platform | Format | Size |
|---|---|---|
| Instagram feed | Square | 1080 × 1080 |
| Instagram feed | Portrait | 1080 × 1350 |
| Instagram Story | Vertical | 1080 × 1920 |
| Instagram Reel cover | Vertical | 1080 × 1920 |
| LinkedIn | Square | 1200 × 1200 |
| LinkedIn banner | Wide | 1584 × 396 |
| WhatsApp Business avatar | Square | 1080 × 1080 |
| Email signature | Horizontal PNG | 600 × 180 |

### Voice rules per account

- **One brand per account.** PIA Instagram does not post GO BIG content. GO BIG Instagram does not post PIA content.
- **Match account voice.** PIA voice is faith-anchored, warm, plural ("we"). GO BIG voice is authoritative, cold, agency ("we").
- **One job per post.** Educate, surface a quote, announce, or invite. Never two at once.
- **No template carousel formats.** Each carousel is purpose-built.
- **No emojis** on GO BIG. Emojis allowed sparingly on PIA.
- **No exclamation points** on GO BIG. PIA may use them when the voice genuinely requires.
- **Banned everywhere:** "dream big," "let's go," "amazing journey," "synergy," "leverage," "stack."

---

## 6. Marketing standard

Copy first. Design supports conversion, not ego.

### Order of operations for any marketing asset

1. **Audience clarity.** Who is this for, named in one sentence?
2. **Offer clarity.** What are we selling, named in one sentence?
3. **CTA clarity.** What is the one action we want them to take?
4. **Copy first.** Write the message before opening the design tool.
5. **Proof injection.** Where does a real quote, photo, number, or testimonial replace a generic claim?
6. **Design last.** Visuals frame the message; they do not invent it.

### First-15-second test

Every asset (page, PDF, email, post) must answer in the first 15 seconds:

- **WHO** is speaking? Name the brand and the people behind it.
- **WHAT** do they offer? In specific terms, not adjectives.
- **NEXT STEP** for the reader who wants to engage? One clear action.

Failing this test means the asset is not ready, regardless of how it looks.

### Banned marketing language

- "Best in class," "industry leader," "world-class," "cutting edge."
- "Trusted by thousands" without a real number and a real source.
- Urgency manipulation: "only X spots," "this week only," countdown timers without a real deadline.
- Discount language: we adjust scope, never price.
- Generic CTA verbs: "click here," "learn more." Use the actual outcome the reader wants.

### Required for every page or asset

- Real testimonials at two positions if conversion is the goal: early in the content, and adjacent to the CTA.
- Schema markup (JSON-LD) on every public page.
- Open Graph tags on every public page.
- A privacy / disclaimer line if the asset references financial, legal, or medical claims.

---

## 7. QA checklist

Pre-deploy. Every box must be checked. No exceptions.

### Visual

- [ ] Desktop screenshot at 1280 × 800 and 1440 × 900 reviewed.
- [ ] Mobile screenshot at 360 × 800 and 414 × 896 reviewed.
- [ ] Tablet screenshot at 768 × 1024 reviewed.
- [ ] No horizontal scroll at any breakpoint.
- [ ] All form fields fit on mobile without overflow.
- [ ] All tap targets minimum 44 × 44 px.
- [ ] Brand consistency: one display family, one body family, no accidental sixth color.

### Performance

- [ ] Lighthouse mobile run on every page.
- [ ] Performance, Accessibility, Best Practices, SEO all 90+ on indexed pages.
- [ ] LCP under 2.5s.
- [ ] CLS under 0.10.

### Assets

- [ ] All raster images optimized via Sharp.
- [ ] All SVGs optimized via SVGO.
- [ ] All approved logo files present in `assets/[brand]/approved/` and verified loaded by the page.
- [ ] No stock photography.
- [ ] No template icons.

### Links

- [ ] Every internal anchor link resolves.
- [ ] Every external link opens in a new tab with `rel="noopener"`.
- [ ] Every `mailto:` opens to the correct brand-face email.
- [ ] Every `tel:` resolves on mobile.

### Forms

- [ ] Submit a real test entry from a real device.
- [ ] Confirm CRM row written.
- [ ] Confirm email notification arrives at `johndavid.assistant@gmail.com` with subject prefix `[BRAND-BRIEF]`.
- [ ] Confirm thank-you redirect.
- [ ] Honeypot field traps a fake submission.

### Language toggle (if applicable)

- [ ] Default language matches the audience (PIA = PT, GO BIG = EN).
- [ ] Toggle swaps every text element including form labels and select options.
- [ ] No flash of wrong language on first paint (FOUC prevented).
- [ ] `<noscript>` fallback shows the source content.

### Accessibility

- [ ] AA contrast on all text.
- [ ] Keyboard tab order logical.
- [ ] All form fields have associated labels.
- [ ] aria-label on icon-only buttons.
- [ ] Headings sequential (no h1 → h3 jump).
- [ ] One h1 per page.

### Deploy

- [ ] No `console.error` on any page.
- [ ] No 404 on any asset request.
- [ ] netlify.toml correct, publish dir set to `public`.
- [ ] DNS verified, SSL active.

---

## 8. Rule for future client work

Before opening any design tool or writing any line of code, define in writing:

| Question | Lock before starting |
|---|---|
| **Audience** | Who is this for? Named in one sentence. |
| **Offer** | What are we selling? Named in one sentence with the price or pricing model. |
| **Visual direction** | Cinematic dark, white-first editorial, photographic warm, or other? Lock one direction. Do not mix mid-build. |
| **Conversion goal** | What is the one action a visitor should take? Form submit, WhatsApp message, calendar booking, PDF download, purchase. |
| **Proof needed** | Real testimonials, photographs, numbers, or named clients. List what is required and where it will come from. |
| **Signature behavior** | One motion pattern (Precision Line System is the default). Document if any deviation is approved. |

Document these answers at the top of the project task or in a `docs/[CLIENT]-BRIEF.md` file before kickoff.

If any of the six are undefined, the project is not ready to start. Fix that first.

---

## 9. Revisions and ownership

This document is owned by **John David Mathias-Mello (Maestro)** and is the source of truth for creative production decisions across all brands and all client work.

Revisions are tracked in git history. Update this document whenever:

- A new tool is added to or removed from the stack.
- A motion rule changes.
- A performance target changes.
- A new client-ready standard is enforced.
- A banned tool or pattern is reconsidered (justify in commit message).

Treat this file like a contract. Pages or assets that contradict this stack are revised, not shipped.

---

## 10. Quality bar enforcement

The quality bar (Section 11) replaces all earlier informal targets in this document. Where any other section in this document is less strict than Section 11, Section 11 wins.

---

## 11. Premium Quality Bar (locked, non-negotiable)

This is the pre-deploy contract for every page and asset.

### 11.1 Design

- Invoke the relevant Claude skills BEFORE editing: `figma-implement-design`, `frontend-design`, `web-design-guidelines`, `impeccable`, `ui-ux-pro-max`, Brand Guardian.
- **Premium typography.** Real font pairing (default: Inter sans + Playfair Display serif). No system fonts in production. **Self-host fonts** for performance — no third-party CDN font loading on production deploys.
- Restraint over flourish. PIA position is "premium not flashy."
- **Real photos only.** No stock people. Use actual John David and Wellen and family photos. For production assets, use a real photographer.

### 11.2 Copy

- **Banned characters.** No em-dashes (`—`), no en-dashes (`–`), no hyphens used as connectors in marketing copy. Periods and commas instead. Hyphenated proper-name compounds (e.g., "five-step", "step-by-step", "faith-first") and hyphens inside file or class names are exempt.
- **Banned words list.** Do not use: `unlock`, `journey`, `hustle`, `transform`, `secrets`, `game-changer`. These are AI-tells and template language.
- **Required tone words.** Reach for: `build`, `protect`, `family`, `step-by-step`, `clear`, `possible`. The voice is grounded, definite, helpful.
- **Faith-first test.** Every line passes the question: "Would this honor God and protect the relationship?" If unclear, default to relationship-only framing.
- **Real social proof.** When claiming social proof, use real testimonials with photo plus quote. Never fabricate, never use anonymous "a client in Florida" placeholders in production.

### 11.3 Performance

- **Lighthouse all-green.** Performance, Accessibility, Best Practices, SEO each ≥ 90 on every indexed page.
- **PageSpeed Insights** mobile ≥ 90, desktop ≥ 95.
- **Core Web Vitals.** LCP under 2.0s, CLS under 0.1, INP under 200ms.
- **Self-hosted fonts.** Font files live in `public/assets/fonts/` and are loaded via `@font-face` with `font-display: swap` and `<link rel="preload" as="font" crossorigin>`.
- **Images.** Compressed via Sharp. WebP variants generated alongside JPGs. Responsive `srcset` on `<img>` tags ≥ 320px wide.
- **Critical CSS inlined** in `<head>`. Non-critical CSS deferred (loaded asynchronously via `<link rel="preload" as="style" onload="this.rel='stylesheet'">`).
- **No render-blocking JS.** All `<script>` tags must use `async` or `defer`, except small inline scripts that set the language or document state before paint.

### 11.4 Accessibility

- **Semantic HTML required.** Real `<header>`, `<main>`, `<section>`, `<article>`, `<footer>`, `<nav>` tags. No `<div>` soup.
- All `<img>` tags have `alt` attributes (decorative images get `alt=""`).
- Form labels associated with inputs via `for` and `id`, or wrapping `<label>`.
- **Color contrast AA minimum**, AAA where possible. Verify against gold-on-navy and white-on-navy combinations.
- **Keyboard navigation works** through every interactive element in logical tab order.
- **Focus states visible** and styled with `:focus-visible`.

### 11.5 Mobile

- Mobile-first design verified at **375px, 414px, 768px, 1024px, 1440px**.
- Touch targets ≥ 44 × 44 px on every interactive element.
- No horizontal scroll on any breakpoint.

### 11.6 Structure

- One `<h1>` per page. Heading hierarchy ordered, no skipping levels.
- **Meta tags required:**
  - `<title>` under 60 characters.
  - `<meta name="description">` under 160 characters.
  - `<link rel="canonical">` set on every page.
  - Open Graph tags: `og:title`, `og:description`, `og:type`, `og:image`, `og:url`.
  - Twitter card: `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`.
- **Favicon set:** `favicon.ico`, `favicon-32x32.png`, `favicon-16x16.png`, `apple-touch-icon.png` (180×180), `<link rel="manifest">` if PWA.
- **`robots.txt` and `sitemap.xml`** at site root.
- **Schema.org JSON-LD structured data** on every page:
  - GO BIG → `Organization` and `Service` types.
  - PIA → `Organization`, `Service`, optionally `LocalBusiness` if a physical address applies.

### 11.7 Pre-deploy gates

- **Lighthouse run** before every push. Block deploy if any score < 90.
- **Cross-browser test** in real Chrome, Safari, mobile Safari, Firefox before push.
- **Form submission smoke test.** Submit a real test entry from a real device. Verify CRM row written. Delete after.
- **Email deliverability test.** Re-test from a clean email address that the system has never seen. Verify Day 0 nurture email lands in inbox, not spam or promotions.
- **Visible verification of the dark/light rhythm.** Two screenshots side-by-side, mobile and desktop, signed off before push.

### 11.8 The bar in one line

A page that fails any of 11.1 through 11.7 does not ship. No exceptions.

---

## 12. Related documents

- `docs/WEBSITE_QUALITY_STACK.md` — website-specific implementation details, building on this stack
- `assets/gobig/README.md` — GO BIG logo locked-version contract
- Vault: `06 The Go Big Agency/GO BIG — Brand System.md` — GO BIG brand system V8
- Vault: `01 Systems/Brand Relationship — PIA × GO BIG.md` — cross-brand architecture lock
- Vault: `05 Prosper In America/Brand Bible.md` — PIA brand foundation
- Vault: `05 Prosper In America/PIA Communication Rules.md` — message formatting rules
- Vault: `05 Prosper In America/PIA Conversion Rules.md` — first-15-second clarity, social proof, simplicity

---

*Last updated: 2026-04-30. Locked as the permanent operating standard.*
