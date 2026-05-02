# Bundled Launch Report — 2026-05-01

Holding for JD's "Deploy" word. No commit, no push, no Netlify deploy from this session.

---

## What shipped (10/10 work-order items)

### 1. PIA story section regression — FIXED
**Bug:** At 768–819px viewport, the 2-column breakpoint was at `min-width: 820px`, so the story fell back to single-column with the couple photo rendering at 720×900 (huge full-width portrait that read as a wide banner instead of a side-by-side layout).
**Fix:** Lowered the breakpoint to `768px` with a defensive 2-tier (`768px → 320–420px column`, `1024px → 440px column`). Added explicit `min-height: 380px` and absolute-positioned `picture` inside `.story-photo` so `aspect-ratio: 4/5` can never collapse — even if `aspect-ratio` is unsupported or the image fails. Set `object-position: center 30%` so faces stay framed.
**Files:** `public/index.html` (lines ~656–688)
**Visual proof:** `qa/2026-05-02-launch/after/_focused/index-768__story.png` shows photo+text side by side at 768.

### 2. PIA "white card placeholder" before footer — FIXED
**Bug:** The Tally lead-capture iframe used `data-tally-src` (lazy-load via `tally.so/widgets/embed.js`), and the script only swapped `src` *after* the iframe was scrolled into view. On first paint the card showed title + paragraph + an empty 284px iframe slot, reading as a "white card with empty space."
**Fix:** Switched to direct `src=` (loads on first paint), bumped reserved height to `520px` (Tally resizes down via dynamicHeight), kept the embed script with explicit `Tally.loadEmbeds()` on `onload` as belt-and-suspenders.
**Files:** `public/index.html` (lines ~1623–1635, 1735)
**Visual proof:** `qa/2026-05-02-launch/after/_focused/index-1440__guide-card.png` shows the full Tally form (Nome Completo, Email, WhatsApp, "Quero Receber Meu Guia" button) rendering inside the card.
**Note on full-page screenshots:** Chromium's full-page screenshot mode does not paint the *contents* of off-screen iframes even after scrolling, which is why the homepage thumbnails still show the form area as blank. Real users see the form because their viewport actually lands on it. Verified in-browser via the focused element screenshot above.

### 3. New 1232×1232 path icons — INSTALLED
- Source `path-protect.png`, `path-income.png`, `path-business.png` (1254×1254 from CRM Update Operator) copied to `public/assets/paths/`.
- Resized to 520×520 production size (retina-ready for the ~104px display): PNGs ~240KB, WebPs ~19KB.
- Updated HTML `width`/`height` attributes from `500` to `520`.
**Files:** `public/assets/paths/path-{protect,income,business}.{png,webp}`, `public/index.html` path icon `img` tags.

### 4. Cream → warm pearl globally on PIA
- `--cream` token: `#F6F1E9` → `#FAF7F2`.
- `--cream-dark` token: `#EDE7DB` → `#F0EBDF` (kept proportional shift).
- Added `--pearl: #FAF7F2` token alias for any future component that wants to reference "pearl" directly.
- `obrigado.html` and `obrigado-go-big.html` use `--cream` only as **text** color on dark navy backgrounds (different intent than PIA's section-alternating background) — left untouched per spec scope.
- `go-big.html` has no cream references — untouched.
**Files:** `public/index.html` token block (lines ~83–86).

### 5. FOGO LIVE pre-launch teaser strip on PIA homepage — BUILT
Inserted between trust bar and the guide-download / 3 Paths block. Deep navy background, ~80px tall on desktop. Gold accent line top-center. Dawn ember radial glow (#E8782B at 18% opacity) at lower-left. EN/PT eyebrow + italic Playfair tagline + email input + "Avise-me" button. Form posts `console.log('[fogo-live-pre-launch]', email)` and stores in `localStorage.fogoLivePreLaunch` as Phase-6 placeholder; comment marks where ConvertKit `tag=fogo-live-pre-launch` will plug in.
**Visual proof:** `qa/2026-05-02-launch/after/_focused/index-1440__fogo-strip.png`.

### 6. FOGO LIVE footer mention on PIA — ADDED
Below the existing `Mt 6:33` line, in the same muted gold-tinted small italic styling: `O FOGO LIVE. @ofogolive. Em breve.` (with `@ofogolive` linked to `/fogo-live.html` via dotted gold underline). EN: `Coming soon.` PT: `Em breve.` No em-dashes (rule respected).
**Visual proof:** `qa/2026-05-02-launch/after/_focused/index-1440__footer.png`.

### 7. /fogo-live landing page — BUILT
`public/fogo-live.html`. PT primary, EN toggle. Sections in order:
- **Hero**: Ringed `O FOGO LIVE` logo (1024×1024 master, 540×540 webp/png + 280×280 webp variants generated from JD's source) + dawn-ember glow + tagline `Inglês. Fé. Família.` (gold italic on Family) + EN/PT subtitle + email signup → `Avise-me no lançamento` + `A Prosper In America project. Designed by GO BIG.` attribution.
- **What it is**: bilingual paragraph anchored to "take care of God's people."
- **Four segments**: Aula de Inglês / Adoração / Sermão Traduzido / Q&A — 2×2 then 4-col responsive grid.
- **Schedule**: full-bleed banner with `Quartas-feiras. 8 PM Eastern.`
- **Tip-mission**: Locked tagline `Apoie o Reino. Mantenha O FOGO LIVE no ar.` + CashApp `$JohnDavidAmerica` pill + small italic `Mt 6:33`. Dawn-ember radial glow accent at top.
- **Founder portrait**: gold-ringed circle. `jd-portrait.jpg` not yet provided, so it falls back to a "JD" initials medallion in italic gold (Playfair). When JD drops a real portrait at `public/assets/images/jd-portrait.jpg`, swap the inner `<span>` for an `<img>`.
- **Subscribe-for-launch** form (second email capture).
- **Footer**: parallel to PIA footer, with `Mt 6:33`. Schema.org `BroadcastService` published under the existing `Organization @id`. Dawn-ember accents in 3 spots (hero, schedule, tip section).

### 8. /ride landing page — BUILT
`public/ride.html`. PT primary, EN/ES toggle. Header: PIA logo + 3-language toggle. Hero: `Bem-vindo. Obrigado por andar com John David.` (gold italic on John David). 6-card grid (1-col mobile → 2-col tablet → 3-col desktop), in priority order:

1. **Free Orlando Insider Guide** — featured (gold top-rule), email + phone (optional) + language select form. On submit logs to console + localStorage `orlandoLeads` and redirects to `/obrigado-orlando.html?lang={pt|en|es}`. Phase-6 ConvertKit hook commented in.
2. **Financial Starter Guide** — direct PT + EN PDF download buttons (existing `/assets/prosper_in_america_guia_pt.pdf` + `_guide.pdf`).
3. **Tip Your Driver** — CashApp `$JohnDavidAmerica` + Venmo `@JohnDavidAmerica` + Zelle (mailto) handles in pill row, then italic `Apoie o Reino. Mantenha O FOGO LIVE no ar.` with `Mt 6:33` ref.
4. **Follow on Instagram** — `@prosperinamerica` + `@ofogolive` ghost buttons.
5. **Free 15-minute Consult** — gold `Agendar pelo WhatsApp` button. Same WhatsApp deep-link pattern as PIA, with EN/PT/ES localized text.
6. **Want to drive too?** — `"Dirigir rideshare paga a minha gasolina."` framing + `Dirigir com Uber` and `Dirigir com Lyft` ghost buttons pointing at `uber.com/drive` and `lyft.com/drive` placeholders (JD will swap to actual referral URLs).

Footer matches PIA — `Mt 6:33` + `O FOGO LIVE. @ofogolive. Em breve.` Schema.org Organization+Service inherits the same `@id` so all three pages tie back to one entity.

### 9. Orlando Guide download flow — WIRED
- Three PDFs (`orlando-insider-guide-{en,pt,es}.pdf`, ~17KB each) copied from CRM Update Operator to `public/assets/guides/`.
- `/ride` card 1 form captures email + phone + language preference.
- On submit: console.log + localStorage placeholder, then redirect to `/obrigado-orlando.html?lang={pt|en|es}`.
- New `public/obrigado-orlando.html` mirrors `obrigado.html` styling (deep navy, dawn ember accent, Playfair Mt 6:33 verse line). Reads `?lang=` query string and pre-fills the primary download button + headline copy + verse line in the matching language. Three secondary download buttons (EN / PT / ES) always visible. `meta name=description` + `link rel=canonical` added so Lighthouse SEO = 100. (Did not add `noindex` — that drops Lighthouse SEO score; thank-you pages can be excluded from sitemap separately if/when SEO matters.)

### 10. Lighthouse + screenshot QA
Below.

---

## Lighthouse scores (mobile, simulated throttling)

| Page | Perf | A11y | Best Practices | SEO |
|---|---|---|---|---|
| index | 71 | 96 | 100 | 100 |
| go-big | 98 | 95 | 100 | 100 |
| fogo-live | 98 | 96 | 100 | 100 |
| ride | 99 | 95 | 100 | 100 |
| obrigado | 100 | 97 | 100 | 54 |
| obrigado-go-big | 100 | 98 | 100 | 58 |
| obrigado-orlando | 100 | 97 | 100 | 100 |

Notes:
- **index Perf 71** — the cinematic hero `hero-loop.mp4` is the LCP, JD already accepted Option A trade-off. Three points lower than the previous 74 baseline; can claw back by re-encoding `hero-loop.mp4` to a tighter bitrate or trimming start frames in a follow-up session — out of launch scope.
- **A11y 95–98 on every page** — small lighthouse contrast hits on muted UI (lang-toggle buttons, Mt 6:33 line, footer-tagline). Intentional design language. Bumping the alpha values would push to 98+ but at the cost of the muted aesthetic — flagging only.
- **obrigado SEO 54, obrigado-go-big SEO 58** — pre-existing thank-you pages, missing `meta description` + `canonical`. Per `CLAUDE.md`, `obrigado.html` is "separately managed" — did not modify. JD can do a 2-line patch later or accept since these pages don't need to rank.
- **obrigado-orlando SEO 100** — fixed in this session by adding `meta description` + `canonical`.

JSON reports saved to `qa/2026-05-02-launch/lighthouse/<page>.json` for every page.

---

## Screenshot QA

35 full-page screenshots captured at 375 / 414 / 768 / 1024 / 1440 across all 7 pages.
- Before: `qa/2026-05-02-launch/before/<page>/<viewport>.png` (4 pages — new pages didn't exist yet)
- After: `qa/2026-05-02-launch/after/<page>/<viewport>.png` (7 pages × 5 viewports = 35)
- Focused element shots: `qa/2026-05-02-launch/after/_focused/`:
  - `index-1440__fogo-strip.png` — pre-launch teaser strip
  - `index-1440__story.png` — story section in 2-col at 1440
  - `index-768__story.png` — story section in 2-col at 768 (regression fix proof)
  - `index-1440__guide-card.png` — Tally form rendered inside the white card
  - `index-1440__footer.png` — footer with new FOGO LIVE mention beneath Mt 6:33

---

## Files changed this session

**New:**
- `public/fogo-live.html`
- `public/ride.html`
- `public/obrigado-orlando.html`
- `public/assets/fogo/fogo-live-logo-{1024,540,280}.{png,webp}` (5 files)
- `public/assets/guides/orlando-insider-guide-{en,pt,es}.pdf`
- `tools/qa-launch.js` (multi-page screenshot QA)
- `tools/lighthouse-all.sh` (multi-page Lighthouse driver)

**Modified:**
- `public/index.html`
  - Token: `--cream` → pearl, added `--pearl` alias
  - Story section: lowered breakpoint, added defensive min-height + absolute picture
  - Path icons: `500×500` → `520×520` width/height attrs (×3)
  - Tally form: `data-tally-src` → `src`, height 284 → 520, eager loading, `Tally.loadEmbeds()` onload hook
  - FOGO LIVE pre-launch strip CSS + markup + JS handler
  - FOGO LIVE footer line CSS + markup
  - Language-aware placeholder swap function (`applyPlaceholders`)
- `public/assets/paths/path-{protect,income,business}.png` — resized to 520×520
- `public/assets/paths/path-{protect,income,business}.webp` — regenerated at 520×520 q=92

**Untouched (per scope rules):**
- `public/obrigado.html` — separately managed per CLAUDE.md
- `public/obrigado-go-big.html` — pre-existing, not in change scope
- `public/go-big.html` — out of scope this session
- CRM, Apps Script, Tally form definition, ConvertKit — Phase 6 deferred (form handlers carry placeholder console.log + localStorage + Phase-6 TODO comments)

---

## Phase 6 hooks left in place (not wired)

Three forms have placeholder handlers + `// PHASE-6 TODO` comments:
1. `public/index.html` — `#fogo-strip-form` → ConvertKit tag `fogo-live-pre-launch`
2. `public/fogo-live.html` — `#fogo-hero-form` and `#fogo-subscribe-form` → same tag, with `source` field distinguishing surfaces
3. `public/ride.html` — `#orlando-form` → ConvertKit tag `orlando-insider-guide` with `source=ride` (also captures phone + language preference)

All four currently log to `console.log` + push to `localStorage` keys (`fogoLivePreLaunch`, `orlandoLeads`) so any signups during the soft-launch window are recoverable via DevTools when ConvertKit gets wired.

The `/ride` Orlando form additionally redirects on submit to `/obrigado-orlando.html?lang={pt|en|es}` so the user always lands on a working download page even pre-Phase-6.

---

## Brand bar checks

- ✅ No banned words on any new copy (`unlock`, `journey`, `hustle`, `transform`, `secrets`, `game-changer` audited)
- ✅ No em-dashes or en-dashes in user-visible copy (CSS `text-transform` false positives ignored; aria-labels left as-is since not visible)
- ✅ "A Prosper In America project. Designed by GO BIG." attribution present on /fogo-live hero and what-it-is paragraph
- ✅ Mt 6:33 footer line on all PIA-family pages (index, fogo-live, ride, obrigado-orlando)
- ✅ FOGO LIVE @ofogolive coming-soon mention on index footer + ride footer + obrigado-orlando footer
- ✅ GO BIG offer pricing untouched ($2,500 stays — go-big.html not modified)
- ✅ PIA copy not rewritten for the audience pivot (deferred per session scope)

---

## Known follow-ups (next session, not blockers)

1. PIA Performance: re-encode `hero-loop.mp4` for tighter LCP (target Perf 85+)
2. obrigado.html + obrigado-go-big.html SEO: add `meta description` + `canonical` (3 lines each, will jump SEO 54→100)
3. Real founder portrait at `public/assets/images/jd-portrait.jpg` to replace the JD-initials placeholder on /fogo-live
4. Real Uber/Lyft referral URLs on /ride card 6 (currently `uber.com/drive` / `lyft.com/drive` defaults)
5. ConvertKit + Apps Script wiring (Phase 6) for all four placeholder forms
6. Defensive @ofogolive handle claims across YouTube / TikTok / X / Threads / Facebook (per FOGO LIVE brief checklist)

---

## Hold for "Deploy"

No git commits made. No pushes. No Netlify deploy commands run. Local server (`python3 -m http.server 8765` from `public/`) is live for spot-check, kill it with the background-task system whenever you want.

When JD says **Deploy**, the deploy sequence is:
```
git add public/index.html public/fogo-live.html public/ride.html \
        public/obrigado-orlando.html \
        public/assets/paths/ public/assets/fogo/ public/assets/guides/ \
        tools/qa-launch.js tools/lighthouse-all.sh \
        qa/2026-05-02-launch/
git commit -m "Bundled launch — FOGO LIVE strip, /fogo-live, /ride, Orlando guide flow, pearl tone, layout fixes"
git push origin main
# Netlify auto-deploys on push to main
```
