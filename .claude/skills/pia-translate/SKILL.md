# /pia-translate

Translate Prosper In America content between English and Brazilian Portuguese. Handles both raw copy and HTML attribute pairs in `public/index.html`.

## Trigger

- `/pia-translate en-to-pt [text]` — translate English copy to Brazilian Portuguese
- `/pia-translate pt-to-en [text]` — translate Portuguese copy to English
- `/pia-translate sync` — scan `public/index.html` for elements with `data-en` but missing or empty `data-pt` and generate the PT versions
- `/pia-translate section [name]` — re-translate all copy in a named section

## Translation principles

**This is not literal translation.** The goal is native-sounding Brazilian Portuguese that preserves brand voice.

Rules:
1. Write as a native Brazilian speaker would say it — not as a dictionary would translate it
2. Preserve sentence rhythm and emotional weight; restructure if needed for natural flow
3. "Immigrant" context: use "imigrante" not "emigrante"; use "nos Estados Unidos" not "na América"
4. Formal enough to signal professionalism; warm enough to feel human
5. Avoid Europeanisms (pt-PT) — use pt-BR spelling, vocabulary, and idioms
6. Religious/faith language: translate precisely, don't soften or omit

**Specific vocabulary:**
| EN | PT |
|---|---|
| Build your life | Construir sua vida |
| Protect my family | Proteger minha família |
| Navigate | Navegar |
| Legal status | Situação legal / status legal |
| Free call | Ligação gratuita |
| Schedule | Agendar |
| Get the guide | Baixar o guia |
| Step-by-step | Passo a passo |
| Starter guide | Guia inicial |

## HTML attribute format

When writing translations for `public/index.html`, HTML tags inside attributes must be encoded:

| Tag | Encoded |
|---|---|
| `<span>` | `&lt;span&gt;` |
| `</span>` | `&lt;/span&gt;` |
| `<br>` | `&lt;br&gt;` |

Example:
```html
data-en="Stop Surviving. &lt;span&gt;Start Building.&lt;/span&gt;"
data-pt="Pare de Sobreviver. &lt;span&gt;Comece a Construir.&lt;/span&gt;"
```

## Output format

For each translated element, show:
```
[Section / element description]
EN: [English text]
PT: [Portuguese text]

HTML:
data-en="..."
data-pt="..."
```

For `/pia-translate sync`, output a numbered list of all missing PT translations found, then ask for confirmation before writing to the file.

## File to edit

`/Users/miriampalma/AI-OS/projects/prosper-landing/public/index.html`
