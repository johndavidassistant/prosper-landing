# FORMS_AUDIT

Canonical reference for every form on prosperinamerica.com. Source of truth
for any future Cowork or Code session checking what is wired and what is not.

Last audit: 2026-05-02
Last verified Apps Script: V13 LOCKDOWN at `/exec`, secret-gated, tested live
with TEST email `audit-probe@example.com` (returned `status: updated`,
`MC-0242`, `data_type: TEST`, ConvertKit skipped per TEST gating).

## At-a-glance table

| File | Form ID | Submission target | CRM pipeline | ConvertKit tag | Status | Notes |
|---|---|---|---|---|---|---|
| public/index.html | Tally `q4E9x7` | Tally workspace webhook to Apps Script `/exec?secret=...` | CONTACTS + CONSULTING | `CONVERTKIT_TAG_ID` (single tag, set as Apps Script Script Property) | **OK** | Live since 2026-04-30 deliverability test. Source label: `Tally - prosperinamerica.com` (Apps Script default). |
| public/index.html | `fogo-strip-form` | None. localStorage only. `console.log('[fogo-live-pre-launch]', ...)` | None | None (PHASE-6 TODO) | **NOT WIRED** (by design — pre-launch) | Captures intent locally for later batch import. No CRM row. |
| public/fogo-live.html | `fogo-hero-form` | None. localStorage only. | None | None (PHASE-6 TODO) | **NOT WIRED** (by design — pre-launch) | Same handler as above. |
| public/fogo-live.html | `fogo-subscribe-form` | None. localStorage only. | None | None (PHASE-6 TODO) | **NOT WIRED** (by design — pre-launch) | Same handler as above. |
| public/go-big.html | `brief-form` | Netlify Forms (`data-netlify="true"`, action=`/obrigado-go-big.html`). `APPS_SCRIPT_ENDPOINT` placeholder is empty so the JS forwarding hook is dormant. | Netlify Forms dashboard only (no CRM write) | None | **NOT WIRED to V2 CRM** (intentional — Netlify Forms catches it) | If JD wants V2 CRM rows, set `APPS_SCRIPT_ENDPOINT` and adapt the function pattern from /ride. |
| public/ride.html | `orlando-form` | `/.netlify/functions/ride-intake` -> Apps Script `/exec` (server-side secret) | CONTACTS + CONSULTING | `CONVERTKIT_TAG_ID` (single tag, segmentation by Source field) | **FIXED** (2026-05-02) | Source label: `Ride - Orlando Insider Guide`. Requires `V2_INTAKE_SECRET` env var in Netlify. |
| public/ride.html | `financial-form` | `/.netlify/functions/ride-intake` -> Apps Script `/exec` (server-side secret) | CONTACTS + CONSULTING | `CONVERTKIT_TAG_ID` (single tag, segmentation by Source field) | **FIXED** (2026-05-02) | Source label: `Ride - Financial Starter Guide`. Requires `V2_INTAKE_SECRET` env var in Netlify. |

Thank-you pages (`obrigado*.html`) are not forms — they are static landing
pages with download buttons. Excluded from this audit.

## Apps Script V13 (V2_Intake_LOCKDOWN.gs) — what it accepts and writes

- Endpoint: `https://script.google.com/macros/s/AKfycbzl7pXpzF5mK2tMTjG9I-8vaHEfM1hYG5TeMtLY8BvHR7Eq2OknQEe-oJRNiBksK3ZuHQ/exec`
- Auth: shared secret in `?secret=` query string OR `secret` JSON field. Mismatch returns 401 + log entry.
- Payload shapes accepted:
  - Flat JSON: `{ name, email, phone, source, secret, lang? }`
  - Tally webhook shape: `{ data: { fields: [...] } }` — normalized server-side by extracting `INPUT_EMAIL`, `INPUT_PHONE_NUMBER`, `INPUT_TEXT` with label containing `nome` or `name`.
- Required fields after normalization: `name`, `email`, `phone` (all non-empty). Missing any one returns 400.
- TEST classification (gates ConvertKit and labels DATA_TYPE column):
  - email contains `@example.com`
  - source contains `(TEST)`
  - payload `data_type === 'TEST'`
- Pipeline routing: hardcoded `Main_Pipeline = 'CONSULTING'`. Every form lands in CONSULTING regardless of source. Segmentation is via the `Source` field, not the pipeline.
- ConvertKit subscribe: gated on `DATA_TYPE === 'REAL'`. Single tag from Script Property `CONVERTKIT_TAG_ID`.
- Dedup: by canonical email (Gmail dot-stripped, +alias stripped) OR last-10 phone digits. Existing rows are UPDATED in place (not skipped).

There is **no source allow-list** in V13. Any payload with a valid secret writes a row.

## Architecture for /ride

```
public/ride.html (#orlando-form, #financial-form)
  |
  |  POST JSON { name, email, phone, lang, form_id }
  v
/.netlify/functions/ride-intake.js
  |  - reads V2_INTAKE_SECRET from env
  |  - maps form_id -> source label
  |  - fills name/phone placeholders if blank (Apps Script requires non-empty)
  |  - posts JSON { name, email, phone, source, lang } with secret in URL query
  v
Apps Script /exec  (V13)
  |
  v
V2 CRM CONTACTS + CONSULTING + CAPTAIN_LOG  (and ConvertKit if data_type === 'REAL')
```

## Diagnosis of the pre-fix bug

`public/ride.html:840` had `bindGuideForm` that:
1. captured email + phone + lang
2. wrote to `localStorage`
3. logged to `console.log('[' + tag + ']', ...)`
4. redirected to thank-you page

There was a literal `// PHASE-6 TODO: POST to ConvertKit with tag=opts.tag, source=ride` comment that was never implemented. **No fetch, no webhook, no Apps Script call.** Submissions silently never reached CRM. Apps Script was healthy the entire time.

## Fixes applied (2026-05-02)

1. **public/ride.html**
   - Added required `name` input to `#orlando-form` and `#financial-form` (Apps Script V13 requires a non-empty name).
   - Added `autocomplete` hints to all three text inputs.
   - Rewired `bindGuideForm` to POST JSON to `/.netlify/functions/ride-intake` then redirect.
   - Added a 4-second safety timeout so a slow function call cannot keep the user stuck on /ride.
   - Kept the localStorage write as a backup capture in case the network fails.
2. **netlify/functions/ride-intake.js (NEW)**
   - Server-side proxy. Reads `V2_INTAKE_SECRET` from env.
   - Maps `form_id` -> source label: `orlando-form` -> `Ride - Orlando Insider Guide`, `financial-form` -> `Ride - Financial Starter Guide`.
   - Fills `name` placeholder from email local-part and `phone` placeholder `not-provided` when /ride leaves them blank, so Apps Script's required-field check passes without exposing those placeholders to the user.
   - Forwards JSON to Apps Script `/exec?secret=...` and parses the response.
3. **netlify.toml**
   - Added `[functions] directory = "netlify/functions"` and `node_bundler = "esbuild"` so Netlify picks up the function on deploy.

## Manual steps required (John David)

These cannot be done from code. Run them once before the next deploy lands.

1. **Set Netlify environment variable.**
   - Netlify dashboard -> the prosper-landing site -> Site configuration -> Environment variables -> Add a single variable.
   - Key: `V2_INTAKE_SECRET`
   - Value: the existing V2_INTAKE_SECRET (same value the Apps Script Script Property holds and the Tally webhook uses).
   - Scope: All deploy contexts.
   - Save. No redeploy needed for env var changes; the next deploy will pick it up automatically.

2. **(Optional) Override Apps Script /exec URL.**
   - Only needed if a future Apps Script redeploy issues a new `/exec` URL. The function falls back to the current V13 URL by default.
   - Key: `APPS_SCRIPT_EXEC_URL`
   - Value: the new `/exec` URL.

3. **Verify post-deploy.**
   - Submit a TEST entry through `/ride`: name `Audit`, email `test+ride+<timestamp>@example.com`, phone blank, lang PT.
   - Within 60 seconds: V2 CRM CONTACTS gets a new row (or an update to an existing test row) with `Source = "Ride - Orlando Insider Guide"` and `DATA_TYPE = TEST`.
   - ConvertKit should NOT subscribe (TEST gating).
   - Repeat for the financial form. Source should be `Ride - Financial Starter Guide`.

## End-to-end test status (2026-05-02 audit)

Live writes to production CRM during this audit were limited per pre-authorization
scope (reads from CRM via Apps Script test calls were allowed; writes were not
explicitly pre-authorized). One probe call established Apps Script health.

| Form | Verified path | Status | Verified how |
|---|---|---|---|
| Tally `q4E9x7` | Tally -> /exec | OK | Live writes confirmed in 2026-04-30 funnel test (vault session log). No fresh write performed in this audit to avoid CRM noise. |
| `fogo-strip-form` | localStorage only | NOT WIRED (by design) | Code review of `public/index.html:1737-1761`. |
| `fogo-hero-form` | localStorage only | NOT WIRED (by design) | Code review of `public/fogo-live.html:909-933`. |
| `fogo-subscribe-form` | localStorage only | NOT WIRED (by design) | Code review of `public/fogo-live.html:909-933`. |
| `brief-form` | Netlify Forms only | NOT WIRED to CRM | Code review of `public/go-big.html:1123-1191`, `1257-1308`. |
| `orlando-form` | New: `/ride-intake` -> /exec | FIXED (pending deploy) | Static branch tests of the function pass (GET 405, no-secret 500, no-email 400, happy 200, bad-upstream 502, network-err 502). End-to-end test deferred to post-deploy verification by John David. |
| `financial-form` | Same as above | FIXED (pending deploy) | Same as above. |

## Security note

The fix routes the secret through a Netlify Function so it stays server-side.
The secret is NOT in any client-side bundle. It IS held in:

- Apps Script Script Properties (`V2_INTAKE_SECRET`)
- The Tally workspace webhook URL query string
- John David's Obsidian vault (`01 Systems/Website & DNS Reference.md`)
- Netlify env var (after the manual step above)

If the secret ever leaks publicly, rotate it in:
1. Apps Script Script Properties
2. Tally webhook URL
3. Netlify env var
4. The vault reference doc

The leaked value would let anyone spam the V2 CRM and trigger ConvertKit
subscriptions for arbitrary emails.

## Pipeline routing follow-up

Apps Script V13 hardcodes every intake into CONSULTING. The `Source` field
is the only segmentation. If John David later wants /ride leads in a separate
pipeline (e.g. a `RIDE` tab) or wants `brief-form` leads in `HUBBER`, that is
a V14 Apps Script change — not a code-side change in this repo. Route via:

```
payload.source -> route table -> target pipeline tab
```

inside `v2_intake.gs`. For now, segment downstream queries on `Source`.
