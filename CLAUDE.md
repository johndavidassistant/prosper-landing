# CLAUDE.md — Prosper In America Landing Page

Operating brief for Claude Code sessions on this project. Read before doing anything.

---

## Project Identity

**Site:** Prosper In America (PIA)
**Domain:** prosperinamerica.com
**Purpose:** Lead capture + brand positioning for John David and Wellen's immigrant consulting, life insurance, and income-building services.
**Primary audience:** Brazilian immigrants in the United States — people navigating finances, protection, and building a real life in America.
**Stack:** Pure HTML / CSS / JS — no framework, no build step. One file governs everything.

---

## File Structure

```
prosper-landing/
├── index.html                    — Main landing page (single file, all CSS inline)
├── obrigado.html                 — Thank-you page after guide form submission
├── generate_guide.py             — Generates EN guide PDF via reportlab
├── generate_guide_pt.py          — Generates PT guide PDF via reportlab
├── generate_guide_pt_docx.py     — Generates PT guide DOCX via python-docx
├── public/assets/
│   ├── prosper_in_america_guide.pdf       — EN Starter Guide (PDF)
│   ├── prosper_in_america_guide.docx      — EN Starter Guide (DOCX)
│   ├── prosper_in_america_guia_pt.pdf     — PT Starter Guide (PDF)
│   ├── prosper_in_america_guia_pt.docx    — PT Starter Guide (DOCX)
│   ├── logo-gold.png             — Gold logo (used on dark backgrounds: hero, footer)
│   ├── logo-navy.jpg             — Navy logo (used on light backgrounds: navbar)
│   └── images/
│       ├── hero.jpg              — Hero background photo (John David)
│       └── story.jpg             — Story section photo (John David and Wellen together)
```

---

## Selected Images

| Slot | File | Source | Dimensions |
|---|---|---|---|
| Hero background | `assets/images/hero.jpg` | `~/Documents/ARCHIVE/John David/WhatsApp Image 2026-04-17 at 16.39.13.jpeg` | 1350×1800px, 771KB |
| Story section | `assets/images/story.jpg` | `~/Documents/ARCHIVE/Casal John David & Wellen/WhatsApp Image 2026-04-14 at 18.24.37.jpeg` | 1200×800px, 424KB |

**Image archive root:** `~/Documents/ARCHIVE/`
Additional supporting images (for future sections) should be sourced from there.

---

## Site Sections (index.html, in order)

| Section | ID | Status | Notes |
|---|---|---|---|
| Navbar | — | Done | Sticky; logo + 3 links + CTA button |
| Hero | — | Done | Full-width photo + dark navy overlay; "Stop Surviving. Start Building." |
| Trust Bar | — | Done | 3 trust signals: Licensed · Immigrant Community · Faith/Family/Structure |
| 3 Paths (Services) | `#caminhos` | Done | Cards: Protect My Family / Increase My Income / Build My Business |
| Our Story | `#nossa-historia` | Done | 2-col: story.jpg left, narrative text right |
| How It Works | `#como-funciona` | Done | 3-step numbered grid |
| Free Guide (Lead Capture) | `#guia` | Done | Tally.so embed (form ID: `q4E9x7`) |
| Footer | — | Done | Logo, tagline, nav links, disclaimer |

**obrigado.html** — standalone thank-you page, written in Portuguese, shown after guide form completion. Uses Lora serif + Inter. Dark navy background.

---

## Design System

### Color Tokens (CSS custom properties)

```css
--navy-deep:  #0F1B2D   /* darkest — page base, hero bg, footer */
--navy:       #1A2942   /* primary navy */
--navy-mid:   #223354
--navy-soft:  #2A3F63
--white:      #FFFFFF
--cream:      #F6F1E9   /* section alternating background */
--cream-dark: #EDE7DB
--gold:       #C8952E   /* primary accent — CTAs, eyebrows, icons */
--gold-light: #DBA94A   /* gold hover state */
--red:        #B22234   /* reserved — do not use without a specific reason */
--text:       #1A2942
--muted:      #5B6E8A
--border:     rgba(26,41,66,0.10)
```

### Typography

| Role | Font | Weights |
|---|---|---|
| Display / headings | Montserrat | 700, 800 |
| Body / UI | Inter | 400, 500, 600, 700 |
| Serif (obrigado.html only) | Lora | 400, 700, italic |

### Layout

- Max width: `1100px` (`.wrap`), `700px` (`.wrap-sm`)
- Section padding: `96px 0` desktop, `72px 0` mobile
- Breakpoints: 480px (mobile), 580px (flex row), 700px (3-col grid), 720px (paths grid), 768px (nav links), 820px (story 2-col)

### Section Alternation

White and cream sections alternate: Paths (white) → Story (cream) → How It Works (white) → Guide (cream).

---

## Brand Principles

### 1. Faith-First Positioning

John David's operating foundation is Matthew 6:33 and Proverbs 1:7. Every message on this site must pass the question: "Would this honor God and protect the relationship?" The brand is not hustle culture. It is not urgency-manipulation. It leads with service, trust, and care.

**Copy tone:** Grounded, warm, direct. No hype. No fake scarcity. No pressure.

### 2. Premium, Not Flashy

The visual language is navy + gold + cream — inspired by financial services that communicate trust and authority. It should feel like a firm a family would trust with their money, not a landing page selling a course.

**What "premium" means here:** Generous whitespace. Clean type hierarchy. Real photography. Restraint in color use. No clutter.

**What to avoid:** Gradient overload, excessive animation, stock photography, generic motivational copy, the word "journey" used cheaply.

### 3. Built for Brazilian Immigrants in the US

The primary emotional context: someone who worked hard to come to America, feels behind, doesn't fully trust institutions, and needs a guide who understands both cultures. John David and Wellen together represent both sides — American-born with immigrant roots, and actual immigrant.

**Copy principles:**
- Speak to the real fear (falling behind, leaving family unprotected) without weaponizing it
- Use "we" not "I" — this is a couple, a partnership, a family approach
- English is the primary language but Portuguese is a first-language signal of trust
- Avoid immigration legal framing — this is financial and consulting, not legal

### 4. Trust, Clarity, Authority

Every section must answer: why trust these people? The answer is not credentials alone. It is shared experience, transparency about their own immigrant story, and the offer of a free, no-pressure conversation.

**Trust signals already on the page:** "Licensed Financial Professional" · shared story (born from both sides) · no-pressure positioning ("A free conversation. No agenda.") · faith anchor.

---

## Bilingual Strategy (EN/PT)

**Current state:** English primary. Portuguese present in the guide section headline ("Os 7 Passos...") and obrigado.html.

**Direction:** A language toggle (EN/PT) is a near-term priority. It should swap copy, not redesign the layout.

**Strategy:**
- All section text should be authored in English first, then translated to Brazilian Portuguese
- The Portuguese version is not a literal translation — it should sound native, not dubbed
- Key conversion moments (CTA buttons, guide headline, hero subtext) are highest priority for bilingual support
- The free guide headline is already in Portuguese as a trust signal for the Brazilian audience

**Skills being built to support this:** `pia-translate` (see below).

---

## Lead Capture

**Form:** Tally.so embed
**Form ID:** `q4E9x7`
**Embed URL:** `https://tally.so/embed/q4E9x7?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1`
**Thank-you page:** `obrigado.html` (Tally redirects here after submission)
**System email (receives leads):** `johndavid.assistant@gmail.com`

---

## Scheduling / CTA

All "Schedule a Free Call" buttons use a centralized JS variable:

```js
var SCHEDULE_URL = 'mailto:johndavid.assistant@gmail.com?subject=...';
```

To point to a real booking page (Calendly, Tally, etc.), update `SCHEDULE_URL` in the `<script>` block at the bottom of `index.html`. All buttons update automatically.

---

## Deployment Workflow

```
Local edits (index.html / assets)
  ↓
git add + git commit
  ↓
git push origin main
  ↓  (auto-deploy via Netlify CI)
prosperinamerica.com
```

**Git remote:** `https://github.com/johndavidassistant/prosper-landing.git`
**Git user:** `johndavidassistant`
**Netlify:** Connected to the GitHub repo. Any push to `main` triggers a deploy.

**To preview locally:** `open index.html` or run a local server:
```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

---

## Skills Being Built

These are reusable Claude Code skills for this project. When implemented, invoke with `/pia-*`.

| Skill | Purpose |
|---|---|
| `pia-copy` | Write or rewrite section copy in PIA brand voice — grounded, warm, no hype, faith-adjacent |
| `pia-translate` | Translate English copy to native Brazilian Portuguese (not literal — culturally fluent) |
| `pia-section` | Scaffold a new HTML section using the existing design system tokens and layout patterns |
| `pia-design` | Review a section for visual hierarchy, premium feel, and brand consistency; output specific fixes |

Until these skills exist, apply their principles manually using this file as context.

---

## Currently Implemented

- [x] Full landing page structure (8 sections)
- [x] Design system (tokens, typography, layout)
- [x] Hero: real photo with dark navy overlay (`object-fit: cover` via `background-size: cover`)
- [x] Story: real photo in 4:5 portrait container (`object-fit: cover`)
- [x] Tally form embed (lead capture)
- [x] Thank-you page (`obrigado.html`)
- [x] Centralized schedule CTA (JS variable)
- [x] Responsive layout (mobile-first)

---

## Next Priorities (in order)

### 1. Language Toggle (EN/PT)

Add a toggle in the navbar. On switch, swap copy in all sections using `data-en` / `data-pt` attributes or a JS-driven content map. Do not redesign — only swap text. CTA URLs stay the same.

### 2. Copy Upgrade (EN/PT)

Current copy is functional but generic in places. Priority sections for rewrite:
- Hero subtext (too long, too safe)
- 3 Paths card descriptions (need more specificity and emotional resonance)
- How It Works steps (currently flat — should feel inviting)

Apply `pia-copy` principles. Then translate to PT.

### 3. Visual Hierarchy Improvement

The page currently reads as a stack of equal-weight sections. Needs:
- Stronger contrast between hero and first content section
- More differentiation between section headings and body text
- The gold accent used more intentionally (currently slightly overused)

### 4. Remove "Cheap" Feel

Specific things that undermine the premium positioning:
- The hero overlay may be slightly too dark — the photo should show more
- Trust bar feels thin and unearned — consider removing or replacing with real social proof
- CTA button on navbar ("Schedule a Free Call") disappears on mobile — ensure it's always visible or replaced with a visible trigger
- Path card links use `mailto:` — these should route to a proper booking flow when the schedule URL is live

---

## What NOT to Do

- Do not use `alert()`, confetti, countdown timers, or fake urgency
- Do not write copy that sounds like a sales funnel — this brand leads with relationship
- Do not add sections without confirming against the next priorities above
- Do not use stock photos — all images must be real photos of John David and Wellen
- Do not add emojis to the page
- Do not redesign layout without explicit instruction — iteration is incremental
- Do not commit credentials, API keys, or Tally form IDs as sensitive — they are already public-facing
- Do not modify `obrigado.html` unless explicitly asked — it is separately managed

---

## PIA Communication Rules (permanent — corrected 2026-04-28)

These apply to every WhatsApp message, outreach sequence, testimonial request, and referral ask.

- No hyphens or dashes in client-facing messages — they make messages feel formatted, not human
- Write short natural sentences instead of dash-connected phrases
- Portuguese must sound like real Brazilian WhatsApp, not formal marketing copy
- Outreach is always staged — never combine asks:
  - Message 1: feedback only, one link, one easy question
  - Message 2: testimonial permission + short bio (after they respond)
  - Message 3: referral ask — minimum 1 week later, only after engagement
- Do NOT include referral ask in Message 2
- Do NOT overload Message 1

Full rules: `05 Prosper In America/PIA Communication Rules.md` in the vault

---

## PIA Conversion Rules (permanent — added 2026-04-28)

These apply to every PIA asset: PDF, website, emails, and client-facing copy.

**Rule 1 — First 15 seconds clarity (non-negotiable)**
Every asset must answer WHO, WHAT, and NEXT STEP within the first 15 seconds:
- WHO: Prosper In America — John David and Wellen
- WHAT: Consulting for Brazilian immigrants — finances, protection, income, business
- NEXT STEP: WhatsApp conversation, free, no pressure

**Rule 2 — Social proof (non-negotiable)**
- Real testimonials required at two positions: early (before middle) and near the CTA
- Format: name, profession, city, 2–3 sentence quote, optional photo
- Never fabricate, suggest, or publish without explicit written confirmation

**Rule 3 — Messaging simplicity (non-negotiable)**
- No hyphens or dashes as connectors — applies to PDF, website, and email copy, not only WhatsApp
- Short sentences. One idea per sentence.
- One objective per message or section.

**Checklist before delivering any PIA asset:**
- [ ] Answers WHO, WHAT, NEXT STEP in first 15 seconds?
- [ ] Real social proof in two positions?
- [ ] No dashes, short sentences, single objective per section?

Full rules: `05 Prosper In America/PIA Conversion Rules.md` in the vault
