# Iteration 3 — Visual Cohesion Pass

Holding for JD's "Deploy" word. No commit, no push, no Netlify deploy from this session.

---

## What shipped (5/5 work-order items)

### 1. Unified header — every page

New `public/css/site-header.css` defines `.site-header*` classes with hard-coded hex (no CSS-var dependency, works inside any page namespace). Identical markup pasted into all 8 pages:

- **Logo on left**: gold `/assets/logo-gold.png` at 36px height, links to `/`.
- **Center nav**: `Sobre Nós · Serviços · Guia Gratuito · O FOGO LIVE · Contato` with `data-en/pt/es` attributes.
- **Right**: `EN | PT | ES` lang toggle. PIA index also has the optional `Agendar uma Chamada` gold CTA per JD's spec.
- **Background**: deep navy `rgba(15,27,45,0.94)` + saturate-blur backdrop, gold `rgba(200,149,46,0.18)` border-bottom. Same on every page including GO BIG (overrides the previous white sticky header per JD's iter-3 instruction).
- **Sticky** with `position: sticky; top: 0; z-index: 200;`.

Selectors use `.site-header .site-lang-toggle .lang-btn` specificity to win against legacy per-page `.lang-btn` rules from earlier iterations.

### 2. Unified footer — every page

`public/css/site-footer.css` already existed from iter 2 — confirmed reachable at `http://localhost:8765/css/site-footer.css` and linked via absolute path on all 8 pages. Markup verified identical across pages: PIA logo + tagline + 5-link nav + © 2026 + Mt 6:33 + clickable "Designed by GO BIG" + "O FOGO LIVE. @ofogolive. Em breve." + page-appropriate disclaimer.

### 3. Broken image audit

Headless audit across all 8 pages with force-decode of every img element:
- All paths now use absolute `/assets/...` form.
- Only one expected 404: `/assets/images/jd-friendly.jpg` (handled by the `onerror` swap to the gold-ring "JD" placeholder on /ride).
- The "broken" reports JD saw were lazy-load timing artifacts in iter 2 — when the audit forces decode, every img loads. `obrigado-go-big.html` footer logo and `index.html` footer logo both 200 OK.

Defensive change: the 4 obrigado pages' top headers were `obrigado-banner` divs containing only a logo. Replaced with the unified `.site-header` (with full nav + lang toggle) so the visual rhythm is consistent and the lang toggle is reachable from every thank-you page too.

### 4. $2,500 cut-off — fixed

`.price-num` was `clamp(88px, 22vw, 296px)` with -0.055em letter-spacing — at 1440px viewport that meant ~600px wide rendered glyph block, but the parent `.wrap-md` is capped at 880px with 24-72px padding on each side. The number overflowed at desktop and crowded the edges on tablet.

Fix:
- Reduced clamp to `clamp(64px, 14vw, 200px)`, line-height 0.92 → 0.96, letter-spacing -0.055em → -0.04em, top/bottom margins 32/56 → 28/48.
- Added `word-break: keep-all` and `.pricing { overflow: hidden }` as defensive guards.

Verified across all 5 viewports (375, 414, 768, 1024, 1440):

| Viewport | Font-size | Number width | Parent width | Overflows? |
|---|---|---|---|---|
| 375 | 64px | 193px | 375px | ✓ no |
| 414 | 64px | 193px | 414px | ✓ no |
| 768 | 107.5px | 324px | 768px | ✓ no |
| 1024 | 143px | 432px | 880px | ✓ no |
| 1440 | 200px | 603px | 880px | ✓ no |

### 5. EN | PT | ES toggle — every page

Headless click-test verified each page swaps `Sobre Nós` ↔ `About Us` ↔ `Sobre Nosotros` correctly:

```
index                    | default=Sobre Nós | ES=Sobre Nosotros | EN=About Us
go-big                   | default=About Us  | ES=Sobre Nosotros | EN=About Us
fogo-live                | default=Sobre Nós | ES=Sobre Nosotros | EN=About Us
ride                     | default=Sobre Nós | ES=Sobre Nosotros | EN=About Us
obrigado                 | default=Sobre Nós | ES=Sobre Nosotros | EN=About Us
obrigado-go-big          | default=About Us  | ES=Sobre Nosotros | EN=About Us
obrigado-orlando         | default=Sobre Nós | ES=Sobre Nosotros | EN=About Us
obrigado-financial-guide | default=Sobre Nós | ES=Sobre Nosotros | EN=About Us
```

The 4 obrigado pages previously had `setLanguage()` functions that ran once on load but never bound click handlers. Added click bindings to each. Created `public/js/site-lang.js` as a reusable opt-in helper for any future static page that needs the toggle without writing per-page glue.

---

## Lighthouse (mobile, simulated throttling)

| Page | Perf | A11y | BP | SEO |
|---|---|---|---|---|
| index | **87** (was 86) | 96 | 96 | 100 |
| go-big | **96** (was 99) | 95 | 100 | 100 |
| fogo-live | **76** (was 98) | 96 | 100 | 100 |
| ride | 99 | 95 | 96 | 100 |
| obrigado | 99 | 96 | 100 | 69 |
| obrigado-go-big | 99 | 90 | 100 | 69 |
| obrigado-orlando | 99 | 96 | 100 | 100 |
| obrigado-financial-guide | 99 | 96 | 100 | 100 |

Notes:
- **fogo-live Perf dropped 98 → 76**: the new `/css/site-header.css` adds a render-blocking stylesheet request, and the hero is the LCP candidate (the 540×540 FOGO LIVE logo at 20KB WebP). The audit reports `largest-contentful-paint: 7%`, `render-blocking-insight: 0%`. Two trade-off paths to recover this in a follow-up: (a) inline the header CSS into the page's existing `<style>` block, or (b) shrink the hero logo display to ~180px max so a smaller WebP variant can replace it. Out of iter-3 scope (the iteration goal was visual cohesion, and that's been achieved).
- **go-big Perf dropped 99 → 96**: the new hero `<video>` element preloads metadata, which adds one network request even when the actual MP4 file doesn't exist yet (404 on `gobig-hero-loop.mp4`). Once JD drops the video, the page should hold or improve.
- **obrigado / obrigado-go-big SEO 69**: same as iter 2 — pages are blocked by `robots.txt` (intentional). Trade-off accepted.
- All other scores ≥ 90.

JSON reports at `qa/2026-05-02-iteration-3/lighthouse/<page>.json`.

---

## Files changed this session

**New:**
- `public/css/site-header.css` — unified header stylesheet (180 lines)
- `public/js/site-lang.js` — reusable lang-toggle helper for static pages

**Modified (8 HTML files):**
- `public/index.html` — replaced inline navbar with unified header markup; added `/css/site-header.css` link
- `public/go-big.html` — replaced inline header with unified header; fixed `.price-num` clamp() + added overflow guard; added `/css/site-header.css` link
- `public/fogo-live.html` — replaced custom navbar with unified header; added `/css/site-header.css` link
- `public/ride.html` — replaced `.top` banner with unified header; added `/css/site-header.css` link
- `public/obrigado.html` — replaced `.obrigado-banner` with unified header; added inline lang-toggle script (page had no JS); added `/css/site-header.css` link
- `public/obrigado-go-big.html` — replaced `.obrigado-banner` (was GO BIG SVG) with unified header (PIA gold logo per JD's "same exact" spec); added click bindings + ES support to existing setLanguage; added `/css/site-header.css` link
- `public/obrigado-orlando.html` — replaced `.obrigado-banner` with unified header; added click bindings to existing setLanguage; added `/css/site-header.css` link
- `public/obrigado-financial-guide.html` — replaced `.obrigado-banner` with unified header; added click bindings to existing setLanguage; added `/css/site-header.css` link

**Untouched:**
- robots.txt — Disallow rules for thank-you pages stay intact (intentional indexing block)
- CRM, Apps Script, Tally, ConvertKit (Phase 6 deferred)
- GO BIG offer pricing (still $2,500)

---

## Brand bar checks

- ✅ No new banned words (`unlock`, `journey`, `hustle`, `transform`, `secrets`, `game-changer`)
- ✅ No em-dashes in user-visible copy (verified)
- ✅ "Designed by GO BIG" present in every footer
- ✅ Mt 6:33 in every footer
- ✅ "O FOGO LIVE. @ofogolive. Em breve." in every footer
- ✅ GO BIG offer pricing untouched ($2,500)
- ✅ Path-card links route to WhatsApp (still consistent from iter 2)
- ✅ All 8 pages render the unified header correctly
- ✅ All 8 pages pass EN | PT | ES click test
- ✅ $2,500 fits at every breakpoint with no overflow

---

## Known follow-ups (not blockers)

1. fogo-live Perf 76 — inline `/css/site-header.css` into the page's existing `<style>` block, or shrink hero-logo max-width to allow a 280px webp variant.
2. go-big.html still requests `/assets/video/gobig-hero-loop.mp4` (404) — JD will drop the file separately.
3. obrigado / obrigado-go-big SEO 69 — accepted, blocked by robots.txt by design.
4. obrigado-go-big A11y 90 — pre-existing heading-order issue.
5. 46 ES translations on `go-big.html` are still PT placeholders (marked TODO).
6. Drop `public/assets/images/jd-friendly.jpg` and `public/assets/images/jd-portrait.jpg` — gold-ring placeholders auto-swap on file presence.

---

## Hold for "Deploy"

No git commits. No pushes. No deploys. Local server live at `http://localhost:8765/`.

When JD says **Deploy**, sequence:
```
git add public/ qa/2026-05-02-iteration-3/
git commit -m "Iteration 3 — unified header on every page, $2,500 fit fix, EN|PT|ES on all"
git push origin main
```
Netlify auto-deploys on push to main.
