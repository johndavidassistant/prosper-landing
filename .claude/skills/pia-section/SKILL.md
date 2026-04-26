# /pia-section

Add, remove, or restructure sections in the Prosper In America landing page without breaking the bilingual system, design tokens, or WhatsApp CTAs.

## Trigger

- `/pia-section add [name]` — add a new section at a specified position
- `/pia-section remove [name]` — remove a section safely
- `/pia-section reorder` — propose a new section order and confirm before applying
- `/pia-section audit` — list all current sections with their purpose and conversion role

## Current section inventory

| Order | Section | ID | Purpose |
|---|---|---|---|
| 1 | Navbar | `nav` | Language toggle + CTA button |
| 2 | Hero | `hero` | Headline, subtext, primary CTA |
| 3 | Social proof strip | `social-proof` | Logos or trust indicators |
| 4 | Problem | `problem` | Name the pain (documentation, status, isolation) |
| 5 | Paths | `paths` | 4-tier consulting menu |
| 6 | Story | `story` | John David & Wellen — trust builder |
| 7 | Guide | `guide` | Free guide offer + Tally form embed |
| 8 | Testimonials | `testimonials` | 3 client stories |
| 9 | Footer | `footer` | Logo, nav links, legal |

## Rules for new sections

Every new section must:
1. Have alternating background (white or cream `#F6F1E9`) matching the surrounding sections
2. Include `data-en` and `data-pt` on every visible text element
3. Use brand tokens only — no new colors, no new fonts
4. Have a single conversion role (inform / build trust / capture email / drive call booking)
5. Not duplicate a role already served by an existing section

## Rules for removal

Before removing a section:
1. Confirm with user — sections are hard to recover from git if removed by mistake
2. Check if the section contains a CTA — if so, confirm the CTA is preserved elsewhere
3. Never remove the hero, guide form, or footer without explicit confirmation

## Output format for `/pia-section add`

Produce the complete HTML block with:
- Correct section id
- All text elements with `data-en` and `data-pt`
- Brand-consistent CSS (inline or in existing `<style>` block)
- Insertion point clearly labeled: `<!-- INSERT AFTER: [section id] -->`

Then ask for confirmation before writing to `public/index.html`.

## File to edit

`/Users/miriampalma/AI-OS/projects/prosper-landing/public/index.html`
