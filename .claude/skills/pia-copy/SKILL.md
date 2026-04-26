# /pia-copy

Write or rewrite copy for the Prosper In America landing page. Enforces brand voice, audience fit, and faith-first tone.

## Trigger

User invokes `/pia-copy` with a section or element:
- `/pia-copy hero` — rewrite hero headline and subtext
- `/pia-copy cta` — rewrite a call-to-action button or section
- `/pia-copy [section name]` — rewrite copy for that section
- `/pia-copy [paste raw text]` — edit/tighten provided copy

## Audience

Brazilian immigrants in the United States. Primary tensions:
- They are skilled, educated, and ambitious — but feel invisible or dismissed in the US system
- They have tried to figure things out alone and hit walls (documentation, legal status, language)
- They trust people, not institutions
- They respond to story, warmth, and proof — not hype or promises
- Family protection is the deepest motivator, not personal gain

Language note: many speak both languages at home. The PT toggle is for the first-generation parent or recent arrival. The EN toggle is for the professional who wants to signal they've built roots here.

## Brand Voice

**Tone:** Warm authority. A trusted advisor who has walked this path himself — not a salesman, not a motivational coach.

**Rhythm:** Short declarative sentences. Fragments are fine. White space between ideas.

**Words to use:** build, protect, navigate, roots, path, clear, step-by-step, family, legal, real, possible

**Words to avoid:** unlock, leverage, transform, journey, hustle, skyrocket, passive income, freedom, game-changer, secrets, proven system

**Headlines:** Speak to the tension or the outcome. Never both. Never vague.
- Good: "Stop Surviving. Start Building."
- Bad: "Your Path to the American Dream Starts Here"

**CTAs:** Direct action, no pressure.
- Good: "Schedule a Free Call" / "Get the Free Guide"
- Bad: "Claim Your Spot Now" / "Limited Time" / "Don't Wait"

## Faith-first rule

Every piece of copy passes this test: "Would this message honor God and protect the relationship?"

If the copy creates urgency through fear, pushes hard on money, or feels manipulative — rewrite it. Conviction through truth. Never through pressure.

## Bilingual requirements

Every copy change to `public/index.html` requires both `data-en` and `data-pt` attributes. PT is not a direct translation — it should feel native to a Brazilian Portuguese speaker.

HTML tags inside attributes must be encoded: `<span>` → `&lt;span&gt;`, `<br>` → `&lt;br&gt;`

## Output format

Present EN and PT versions side by side:

```
EN: [copy]
PT: [copy]
```

If editing HTML, show the full attribute change:
```html
data-en="[EN copy]"
data-pt="[PT copy]"
```

## File to edit

`/Users/miriampalma/AI-OS/projects/prosper-landing/public/index.html`

## Vault reference

Brand voice details and full guide copy:
`~/Documents/OBSIDIAN/REINO DE DEUS/06 Prosper In America/`
