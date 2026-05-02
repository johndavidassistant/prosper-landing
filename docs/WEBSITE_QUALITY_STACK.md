# Website Quality Stack

> **This document is a website-specific extension of `docs/CREATIVE_PRODUCTION_STACK.md`** (the permanent operating standard governing websites, logos, social, marketing, and brand systems). When the two documents conflict, the Creative Production Stack wins.

Standard for premium static websites. Applies to `prosperinamerica.com` and to future client work.

This document is the source of truth for tooling decisions, animation discipline, SEO standards, QA workflow, and the client-ready bar. If a build pass departs from this stack, the deviation must be justified in the PR or task description.

---

## 1. Approved tools

### Runtime libraries (loaded via CDN, no install)

| Tool | Use | When to use | When NOT to use |
|---|---|---|---|
| GSAP 3 + ScrollTrigger | Premium scroll-triggered motion. Line reveals, fade-ins, parallax-lite. Free since 2024. | Hero entrance reveal. Section-enter accents (hairlines drawing). Pricing number on-enter. Submit-button subtle focus pulses. | Anything that animates more than three elements at once. Anything longer than 600ms. Hero-product carousels (use static instead). |
| Lenis (smooth scroll) | Physics-based scroll smoothing. ~3KB. Used by Apollo, Aman, Linear. | Desktop only. Adds expensive feel to long-scroll editorial pages. | Mobile (native scroll is better on touch). Pages where the user needs precise anchor-link jumping. |

CDN sources:
- GSAP: `https://cdn.jsdelivr.net/npm/gsap@3.12/dist/gsap.min.js`
- GSAP ScrollTrigger: `https://cdn.jsdelivr.net/npm/gsap@3.12/dist/ScrollTrigger.min.js`
- Lenis: `https://cdn.jsdelivr.net/npm/lenis@1.1/dist/lenis.min.js`

### Dev dependencies (installed in `package.json`)

| Tool | Version | Use | When NOT to use |
|---|---|---|---|
| `puppeteer-core` | 24.x | Screenshot QA across breakpoints. Uses system Chrome (no Chromium download). | Production runtime. Heavy automated user flows (use Playwright). |
| `lighthouse` | 13.x | Pre-deploy audit: performance, accessibility, SEO, best practices. | As a daily check (only on PRs and pre-deploy). |
| `sharp` | 0.34.x (libvips 8.17) | Image optimization: resize, WebP generation, quality targeting. | SVGs (use SVGO instead). |
| `svgo` | 4.x | SVG optimization. Strip metadata, comments, unused defs. | SVGs that contain handwritten gradients or IDs that other code references. Run with `--pretty` first to inspect. |
| `prettier` | 3.x | Format HTML/CSS/JS to a consistent style. | Generated files, third-party libs. |

### Already on the system (no install needed)

| Tool | What it is | Use it for |
|---|---|---|
| `@google/clasp` | Google Apps Script CLI (global) | Deploying the Apps Script webhook for the GO BIG brief |
| ImageMagick | Image manipulation (Homebrew) | Quick CLI image conversions when sharp is overkill |
| ReportLab + Pillow (Python) | PDF generation | The PIA guide PDF generation pipeline |
| Chrome.app | System browser | Puppeteer-core target |
| Google Workspace MCP | Gmail, Drive, Calendar | Workflow automation, lead followups |
| Obsidian MCP | Vault read/write | Vault-backed writes (use disk for content, MCP for queries only) |
| Notion MCP | Notion read/write | Notion sync if needed |
| Claude skill `ui-ux-pro-max` | Premium layout system reference | Color palette, font pairings, layout direction starting points |
| Claude skill `web-design-guidelines` | UI accessibility/UX audit | Pre-deploy review of new pages |
| Claude skill `frontend-design` | Distinctive frontend interface generation | First-pass landing page or component scaffolding |
| Claude skill `impeccable` | UI critique and polish | Mid-build art direction review |
| Claude skill `figma-implement-design` | Figma to code translation | When client provides a Figma file |
| Claude skill `gsd-map-codebase` | Codebase analysis | Onboarding to a new client repo |
| Claude skill `gsd-graphify` | Project knowledge graph | Cross-reference complex client docs |

### Explicitly NOT in the stack

| Tool | Why we are not using it |
|---|---|
| Remotion | Heavy install (FFmpeg, Chrome). Out of scope for static website work. Reconsider if and when we ship motion-graphics deliverables (Instagram reels, intros). Until then, skip. |
| Three.js | Overkill for editorial sites. Adds 600KB+ minified. The aesthetic does not call for 3D. |
| Framer Motion | React-only. Our stack is pure HTML/CSS/JS, no React. |
| Vite, Webpack, Rollup | No build step. Site stays as static HTML. Adding a build pipeline is a tax we do not need to pay. |
| Next.js, Astro, Eleventy | Same reason. Static HTML deployed via Netlify is sufficient and faster than any framework for our scale. |
| Tailwind CSS | We hand-author CSS for premium typographic control. Tailwind is for fast component scaffolding, not for editorial restraint. |
| ESLint | Overkill for our static HTML/CSS with minimal JS. Prettier covers formatting. |
| Playwright | Puppeteer-core covers our QA needs at lower install cost. Playwright is better for cross-browser automation. Not yet justified. |
| jQuery | Banned. Modern vanilla JS is enough. |
| Bootstrap, Bulma, Foundation | Component frameworks. Banned. We hand-author every component. |
| Webflow, Wix, Squarespace | Client deliverables come from this stack only. Not from a no-code tool. |

---

## 2. Animation rules

The site moves with restraint. Motion is a luxury cue when used correctly and a template tell when used wrong.

### Allowed

- **Line-draw reveals.** Hairlines that animate from `stroke-dashoffset: 100%` to `0` on section enter. Duration `600ms`, easing `expo.out`, single occurrence per visit.
- **Subtle fade + lift.** `opacity: 0 → 1` and `translateY: 12px → 0` on section enter. Duration `500ms`, easing `power2.out`, no stagger longer than `80ms`.
- **Smooth scroll on desktop.** Lenis enabled at `>=1024px` viewport, disabled below.
- **Hover-state color shifts.** Links, buttons. `200ms` ease.
- **Form input focus underline.** Border-bottom color shift to gold on focus. `200ms` ease.

### Banned

- Parallax that moves more than 8% of viewport height.
- Auto-playing carousels.
- Scroll-jacked sections that override native scroll velocity.
- Looping animations after first scroll.
- Animations longer than 800ms.
- Bounce / elastic / back easings (cute, not premium).
- Number count-ups longer than 1.2s.
- Any animation triggered by mouse movement (cursor trails, tilt effects).
- Loading spinners (the site loads under 2s; a spinner is an admission of failure).
- Splash screens, intro overlays.

### Reduced motion

Every animation must check `prefers-reduced-motion: reduce` and skip the animation entirely. GSAP exposes `gsap.matchMedia()` for this. Use it.

### Mobile

- No Lenis on mobile. Native scroll wins.
- Reduce animation duration by 25% on `<768px`.
- Skip section-enter line-reveals below `<480px`. The viewport is too small for the gesture to register.

---

## 3. SEO rules

Pre-deploy SEO is non-negotiable. The site must score Lighthouse SEO 95+ before any client deliverable is signed off.

### Required on every page

- `<title>` 50–60 characters, includes brand and primary keyword.
- `<meta name="description">` 140–160 characters, written as a real sentence.
- `<meta property="og:title">` and `og:description` and `og:type` and `og:image` (when image is appropriate).
- `<html lang="...">` matches the page's language.
- `<link rel="canonical">` if multi-route.
- Heading order is sequential (no skipping h1 → h3).
- One `<h1>` per page.
- All `<img>` tags have `alt` attributes.
- All `<a>` tags either have descriptive text or `aria-label`.

### JSON-LD schema (hand-written)

Place inside `<head>`. Minimum schema for a brand site:

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Prosper In America",
  "url": "https://prosperinamerica.com",
  "logo": "https://prosperinamerica.com/assets/logo-gold.png",
  "founder": [
    {"@type": "Person", "name": "John David"},
    {"@type": "Person", "name": "Wellen"}
  ],
  "areaServed": "US"
}
```

Add `WebSite` schema with `potentialAction` if there is a search box. Add `LocalBusiness` schema if the client has a physical location. Add `Service` schema for offered services.

### Sitemap and robots

- `sitemap.xml` at root. Generated by a small Node script (`tools/sitemap.js`) that walks `public/*.html` and writes the file. Update automatically pre-deploy.
- `robots.txt` at root. Allows everything. Points to sitemap.

### Performance targets (Lighthouse mobile, 4G)

| Metric | Target |
|---|---|
| Performance score | 90+ |
| Accessibility score | 95+ |
| Best Practices score | 95+ |
| SEO score | 95+ |
| Largest Contentful Paint | under 2.5s |
| Cumulative Layout Shift | under 0.10 |
| Total Blocking Time | under 200ms |
| Page weight (excluding fonts) | under 250 KB |

A page that misses any of these does not ship.

---

## 4. Screenshot QA process

Pre-deploy visual QA. Required for every page change.

### Standard breakpoints

- 360 × 800 (small mobile)
- 414 × 896 (large mobile)
- 768 × 1024 (tablet)
- 1280 × 800 (laptop)
- 1440 × 900 (desktop)

### Tool

`tools/screenshot-qa.js` — a Puppeteer-core script (to be added) that:
1. Launches system Chrome via `puppeteer-core`.
2. For each route in `public/*.html`, takes a full-page screenshot at each breakpoint.
3. Saves to `tools/screenshots/[route]/[breakpoint].png` with timestamps.
4. Optionally diffs against an approved baseline if one exists.

Run with: `npm run qa:screenshots`

Review every screenshot before deploy. Look for:
- Horizontal scroll
- Type that breaks at unexpected points
- Form fields that overflow
- Images that crop the wrong region
- Touch targets under 44 × 44px
- Text contrast that fails AA

### Pre-deploy checklist

- [ ] Lighthouse run on every page, scores recorded.
- [ ] Screenshot QA across all five breakpoints.
- [ ] Real device test on iPhone and Android if available.
- [ ] Form submission test (live test row in CRM, then delete).
- [ ] Email notification arrival test.
- [ ] All external links open in new tab with `rel="noopener"`.
- [ ] All `<a href="mailto:...">` and `<a href="tel:...">` work.
- [ ] No console errors in production build.
- [ ] Heading order audit (one `<h1>`, sequential h levels).

---

## 5. Client-ready website standard

A site is "client-ready" when ALL of these are true:

### Brand

- [ ] Brand system documented in vault (colors, typography, voice rules, logo usage).
- [ ] One Question Test passes on every section: which brand is speaking?
- [ ] No template tells: cards over-used, generic icon set, stock photography, Bootstrap classes, fake testimonials.
- [ ] Photography is real (or absent), never stock.
- [ ] Logo used at correct scale per brand system.
- [ ] Color palette consistent. No accidental sixth color.

### Copy

- [ ] No em-dashes, en-dashes, or hyphens used as connectors in body copy.
- [ ] No exclamation points in voice-controlled brands.
- [ ] First 15 seconds answer WHO, WHAT, NEXT STEP.
- [ ] One objective per section.
- [ ] No motivational filler ("dream big," "amazing journey").
- [ ] Read-aloud test: every sentence flows without a stumble.

### Engineering

- [ ] HTML validates (no broken tags).
- [ ] CSS is hand-authored, hand-organized, named for legibility.
- [ ] No build pipeline unless required by the brand or framework.
- [ ] All assets optimized (sharp for raster, svgo for vector).
- [ ] FOUC prevention if language toggle exists.
- [ ] `prefers-reduced-motion` honored.
- [ ] `prefers-color-scheme` respected if both modes are designed.

### Accessibility

- [ ] AA contrast on all text.
- [ ] Keyboard navigation reaches every interactive element in logical order.
- [ ] Form fields have labels.
- [ ] aria-label on icon-only buttons.
- [ ] Skip-to-content link if header has more than 4 nav items.

### SEO

- [ ] Title, meta description, OG tags on every page.
- [ ] JSON-LD schema present.
- [ ] Sitemap.xml + robots.txt at root.
- [ ] Lighthouse SEO 95+.

### Performance

- [ ] All Lighthouse scores 90+.
- [ ] Page weight target met.
- [ ] LCP target met.
- [ ] CLS target met.

### Deploy

- [ ] netlify.toml present and correct.
- [ ] Form notifications configured in dashboard.
- [ ] Custom domain wired with SSL.
- [ ] Branch protection on main (manual gate before deploy if revenue-critical).

---

## 6. Process map

```
Brief from client
       ↓
Brand system locked (vault)
       ↓
Visual direction approved (Apollo lens)
       ↓
Page structure approved (Architect lens)
       ↓
Copy locked (Copy Chief lens)
       ↓
Build (HTML/CSS, hand-authored)
       ↓
Asset optimization (sharp + svgo)
       ↓
Animation pass (GSAP + Lenis, if approved)
       ↓
Pre-deploy QA (puppeteer-core screenshots + lighthouse)
       ↓
Stakeholder review (review every screenshot)
       ↓
Deploy (Netlify)
       ↓
Post-deploy verification (live tests)
       ↓
Sign off
```

Every gate is enforceable. A failed gate sends the work back, never around.

---

## 7. Versioning this document

This file lives in the repo at `docs/WEBSITE_QUALITY_STACK.md`. Update it whenever:
- A new tool is added to or removed from the stack.
- An animation rule changes.
- A performance target changes.
- A new client-ready standard is enforced.

Treat it like a contract.

---

*Last updated: 2026-04-30. Maintained by John David.*
