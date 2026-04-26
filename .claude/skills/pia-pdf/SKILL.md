# /pia-pdf

Build and maintain the Prosper In America Starter Guide PDF delivery system. Covers content assembly, Canva brief output, and email delivery wiring.

## Trigger

- `/pia-pdf status` — audit current state of PDF + delivery pipeline, identify what's blocking
- `/pia-pdf canva` — output full Canva design brief (all pages, layout specs, copy, brand tokens)
- `/pia-pdf email-sequence` — draft the 3-email ConvertKit sequence for guide delivery
- `/pia-pdf wireframe` — text wireframe of all PDF pages (no design tool needed)
- `/pia-pdf tally-check` — verify Tally form `q4E9x7` → ConvertKit wiring and redirect

## System state (as of last known build)

| Component | Status |
|---|---|
| Guide copy | Complete in Obsidian vault |
| PDF file | Not built — no Canva file exists |
| Tally form | Live (`q4E9x7`), redirects to `obrigado.html` |
| ConvertKit | Not wired to Tally |
| Email sequence | Not written |
| PDF delivery URL | Does not exist yet |

## PDF spec

**Pages:** 12–16
**Size:** US Letter (8.5" × 11") or A4
**Brand colors:** Navy `#0F1B2D`, Gold `#C8952E`, Cream `#F6F1E9`, White `#FFFFFF`
**Fonts:** Montserrat 800 (headings), Inter 400/600 (body)
**Cover:** Full navy background, gold title, cream subtitle, PIA logo

**Page structure:**
1. Cover
2. Welcome letter (John David, personal, faith tone)
3. How to use this guide
4. Steps 1–7 (1–2 pages each)
5. Next step / CTA page (book a free call)
6. Back cover (logo, website, WhatsApp)

## ConvertKit email sequence (3 emails)

**Email 1 — Immediate delivery**
- Subject (EN): "Here's your free guide — 7 Steps to Build Your Life in America"
- Subject (PT): "Aqui está seu guia gratuito — 7 Passos Para Construir Sua Vida nos EUA"
- Body: Short warm intro + PDF download link
- Delay: Send immediately on form submit

**Email 2 — Day 3 follow-up**
- Subject: "Did you read Step 3? (Most people skip this one)"
- Body: Highlight Step 3 (Get Your Documents Right), soft CTA to book a call
- Delay: 3 days after Email 1

**Email 3 — Day 7 close**
- Subject: "One question before you decide"
- Body: Address the top objection ("I'll figure it out myself"), invite to a free call, no pressure
- Delay: 4 days after Email 2

## Tally → ConvertKit wiring

Tally form `q4E9x7` must:
1. Capture email field
2. POST to ConvertKit via Tally webhook integration
3. Add subscriber to ConvertKit tag: `pia-guide-download`
4. Trigger ConvertKit automation sequence on that tag

System email for all automations: `johndavid.assistant@gmail.com`

## Output format for `/pia-pdf canva`

```
PAGE [N]: [Name]
Background: [color]
Layout: [description]
Top element: [text + style]
Mid element: [text + style]
Bottom element: [text + style or CTA]
Image: [description or "none"]
Notes: [any special instruction]
```

## Vault reference

Guide content source: `~/Documents/OBSIDIAN/REINO DE DEUS/06 Prosper In America/`

Read vault files before writing any guide content. Do not fabricate legal or immigration information.
