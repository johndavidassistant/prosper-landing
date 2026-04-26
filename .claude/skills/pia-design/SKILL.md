# /pia-design

Audit and improve the visual quality of the Prosper In America landing page. Enforces the brand design system without restructuring sections or changing copy.

## Trigger

User invokes `/pia-design` with an optional focus area:
- `/pia-design` — full audit
- `/pia-design hero` — hero section only
- `/pia-design mobile` — mobile/responsive issues only
- `/pia-design spacing` — whitespace and rhythm only

## Brand Design System (do not deviate)

**Colors:**
- Navy dark: `#0F1B2D`
- Navy mid: `#1A2942`
- Gold: `#C8952E`
- Cream: `#F6F1E9`
- Text primary: `#0F1B2D`
- Text secondary: `#4A5568`

**Typography:**
- Display: Montserrat 800 — headings only
- Body: Inter 400/600/700 — all other text
- No other font families

**Spacing scale:** 4px base unit. Prefer multiples of 8 (8, 16, 24, 32, 48, 64, 80, 96)

**Card/surface style:** white background, `border-radius: 12px`, `box-shadow: 0 4px 24px rgba(0,0,0,0.08)`, `1px solid rgba(0,0,0,0.06)`

**Buttons:**
- Primary (gold): `background: #C8952E`, white text, `border-radius: 8px`, `font-weight: 700`
- Ghost: transparent, gold border, gold text
- Minimum tap target: 44px height on mobile

**Section backgrounds alternate:** white → cream `#F6F1E9` → white

## What to check

1. **Hierarchy** — h1 > h2 > h3 weight contrast is visible and consistent
2. **Color usage** — gold used sparingly as accent only (CTAs, borders, highlights); not decorative fill
3. **Typography sizing** — h1 ≥ 48px desktop / ≥ 36px mobile; body ≥ 16px; never below 14px
4. **Spacing rhythm** — sections have consistent vertical padding (80px desktop / 48px mobile)
5. **Mobile** — all CTAs visible at 375px; no horizontal overflow; font sizes readable
6. **Trust signals** — testimonials, authority indicators, and credentials are visually prominent
7. **Faith tone** — no flashy gradients, no neon colors, no casino-style urgency

## What NOT to do

- Do not change section order or structure
- Do not rewrite copy
- Do not add new sections
- Do not change the WhatsApp CTA URLs
- Do not touch JS logic

## Output format

For each issue found:
```
ISSUE: [short label]
Location: [section name or CSS selector]
Problem: [one sentence]
Fix: [specific CSS or HTML change]
```

Then apply fixes directly to `public/index.html` if user confirms.

## File to edit

`/Users/miriampalma/AI-OS/projects/prosper-landing/public/index.html`
