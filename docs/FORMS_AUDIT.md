# FORMS_AUDIT

Canonical reference for every form on prosperinamerica.com. Source of truth
for any future Cowork or Code session checking what is wired and what is not.

Last audit: 2026-05-02
Last code-side update: 2026-05-02 (GO BIG brief wiring + V14 Apps Script patch).
Last verified Apps Script: V13 LOCKDOWN at `/exec`, secret-gated, tested live
with TEST email `audit-probe@example.com` (returned `status: updated`,
`MC-0242`, `data_type: TEST`, ConvertKit skipped per TEST gating).
V14 patch is staged in `V2_Intake_LOCKDOWN.gs` but NOT yet redeployed —
manual paste + new web-app version required by John David before brief
emails fire.

## At-a-glance table

| File | Form ID | Submission target | CRM pipeline | ConvertKit tag | Status | Notes |
|---|---|---|---|---|---|---|
| public/index.html | Tally `q4E9x7` | Tally workspace webhook to Apps Script `/exec?secret=...` | CONTACTS + CONSULTING | `CONVERTKIT_TAG_ID` (single tag, set as Apps Script Script Property) | **OK** | Live since 2026-04-30 deliverability test. Source label: `Tally - prosperinamerica.com` (Apps Script default). |
| public/index.html | `fogo-strip-form` | None. localStorage only. `console.log('[fogo-live-pre-launch]', ...)` | None | None (PHASE-6 TODO) | **NOT WIRED** (by design — pre-launch) | Captures intent locally for later batch import. No CRM row. |
| public/fogo-live.html | `fogo-hero-form` | None. localStorage only. | None | None (PHASE-6 TODO) | **NOT WIRED** (by design — pre-launch) | Same handler as above. |
| public/fogo-live.html | `fogo-subscribe-form` | None. localStorage only. | None | None (PHASE-6 TODO) | **NOT WIRED** (by design — pre-launch) | Same handler as above. |
| public/go-big.html | `brief-form` | `/.netlify/functions/gobig-intake` -> Apps Script `/exec` (server-side secret). `data-netlify="true"` retained as no-JS fallback to Netlify Forms dashboard. | CONTACTS + CONSULTING | `CONVERTKIT_TAG_ID` (single tag, segmentation by Source field) | **FIXED** (2026-05-02, pending deploy) | Source label: `GO BIG Brief`. New required `email` input added. V14 Apps Script patch fires `MailApp.sendEmail()` to `johndavid.assistant@gmail.com` for non-TEST submissions and writes the full brief to CAPTAIN_LOG + a Quick_Note summary. Requires `V2_INTAKE_SECRET` env var in Netlify AND the V14 Apps Script redeploy. |
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

## Architecture for /go-big

```
public/go-big.html (#brief-form)
  |
  |  POST JSON { name, email, whatsapp, business, what_do_you_do,
  |              not_working, want, budget, lang }
  v
/.netlify/functions/gobig-intake.js
  |  - reads V2_INTAKE_SECRET from env
  |  - hardcodes source = "GO BIG Brief"
  |  - maps whatsapp -> phone (Apps Script V13 expects 'phone')
  |  - synthesises name placeholder if blank, phone placeholder 'not-provided'
  |  - posts JSON to /exec?secret=... including all rich brief fields
  v
Apps Script /exec  (V14 patch — pending redeploy)
  |  - writes CONTACTS + CONSULTING rows (Quick_Note carries a brief summary)
  |  - logs full brief to CAPTAIN_LOG (action_type 'gobig_brief_received')
  |  - if DATA_TYPE === 'REAL' AND source contains "GO BIG":
  |      MailApp.sendEmail({ to: V2_INTAKE_GOBIG_NOTIFY,
  |                          subject: '[GO BIG Brief] {name} - {email}',
  |                          body: full brief + CRM link })
  v
V2 CRM CONTACTS + CONSULTING + CAPTAIN_LOG
ConvertKit (if data_type === 'REAL')
johndavid.assistant@gmail.com inbox (if REAL + GO BIG source)
```

Until V14 is redeployed, the function still writes the row to V2 CRM via
V13. The brief fields silently pass through without enriching Quick_Note
or triggering the email — V13 ignores unknown payload keys. Post-redeploy,
the Quick_Note becomes brief-aware and the email starts firing.

## Diagnosis of the pre-fix bug

`public/ride.html:840` had `bindGuideForm` that:
1. captured email + phone + lang
2. wrote to `localStorage`
3. logged to `console.log('[' + tag + ']', ...)`
4. redirected to thank-you page

There was a literal `// PHASE-6 TODO: POST to ConvertKit with tag=opts.tag, source=ride` comment that was never implemented. **No fetch, no webhook, no Apps Script call.** Submissions silently never reached CRM. Apps Script was healthy the entire time.

## Fixes applied (2026-05-02)

### Round 1 — /ride

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

### Round 2 — /go-big brief-form (2026-05-02 same day)

1. **public/go-big.html**
   - Added required `email` input between `name` and `business` (V13 requires non-empty email; brief-form previously collected only WhatsApp).
   - Replaced the dormant `APPS_SCRIPT_ENDPOINT` JS forwarding hook with a real submit handler mirroring /ride: POST JSON to `/.netlify/functions/gobig-intake`, redirect to `/obrigado-go-big.html?lang=<currentLang>`, 4-second safety timeout, localStorage backup under key `goBigBriefs`.
   - Kept `data-netlify="true"` + `form-name` hidden input + form `action` attribute so non-JS users still get captured by Netlify Forms as a fallback.
2. **netlify/functions/gobig-intake.js (NEW)**
   - Server-side proxy. Reads `V2_INTAKE_SECRET` from env. Hardcodes source = `GO BIG Brief`.
   - Maps `whatsapp` -> `phone`. Synthesises name from email local-part if blank; sends `phone = 'not-provided'` when blank.
   - Forwards every brief field upstream so V14 Apps Script can record them. V13 silently ignores unknown keys, so this is forward-compatible.
3. **V2_Intake_LOCKDOWN.gs (V14 patch, NOT redeployed yet)**
   - New constants `V2_INTAKE_GOBIG_NOTIFY` and `V2_INTAKE_GOBIG_SOURCE_KEY`.
   - `v2_intake()` now extracts brief fields, builds a one-line Quick_Note summary when present, logs the full brief to CAPTAIN_LOG under `gobig_brief_received`, and (when DATA_TYPE === 'REAL' AND source contains "GO BIG") calls `_v2intake_notifyGoBig_()` which fires `MailApp.sendEmail()` to `johndavid.assistant@gmail.com`.
   - Both new-create and duplicate-update paths trigger the email so resubmissions still reach John David's phone.
   - Mail failures are logged + swallowed; they never block the intake response.
   - New editor test `v2_intake_TEST_GOBIG()` for John David to verify the GO BIG path before the live web-app redeploy.

## Manual steps required (John David)

These cannot be done from code. Run them once before the relevant deploy lands.

1. **Set Netlify environment variable** (one-time, covers both /ride and /go-big).
   - Netlify dashboard -> the prosper-landing site -> Site configuration -> Environment variables -> Add a single variable.
   - Key: `V2_INTAKE_SECRET`
   - Value: the existing V2_INTAKE_SECRET (same value the Apps Script Script Property holds and the Tally webhook uses).
   - Scope: All deploy contexts.
   - Save. No redeploy needed for env var changes; the next deploy will pick it up automatically.

2. **Apps Script V14 redeploy** (required for the GO BIG email notification + Quick_Note enrichment).
   - Open the Apps Script project: `1FnsH_4BgN9sFtKeRQ5456CGkzByR-08DI9iTfPr7ydkLrYjsPaxRqda-`.
   - Open `V2_Intake.gs` in the Apps Script editor.
   - Replace its contents with the V14 file at `/Users/miriampalma/Documents/Claude/Projects/CRM Update Operator/V2_Intake_LOCKDOWN.gs`.
   - Save.
   - Run `v2_intake_TEST_GOBIG()` from the editor's Run menu once. Confirm CAPTAIN_LOG gets a `gobig_brief_received` entry. Because the test email is `@example.com`, DATA_TYPE will be TEST and no email will fire — that is correct.
   - Deploy -> Manage deployments -> select the existing web-app deployment -> Edit (pencil) -> Version: New version. Save.
   - Verify the `/exec` URL is unchanged: `AKfycbzl7pXpzF5mK2tMTjG9I-8vaHEfM1hYG5TeMtLY8BvHR7Eq2OknQEe-oJRNiBksK3ZuHQ`. If a new URL is issued, update Netlify env var `APPS_SCRIPT_EXEC_URL` (see step 3) AND the Tally webhook URL.

3. **(Optional) Override Apps Script /exec URL.**
   - Only needed if a future Apps Script redeploy issues a new `/exec` URL. The functions fall back to the current V13 URL by default.
   - Key: `APPS_SCRIPT_EXEC_URL`
   - Value: the new `/exec` URL.

4. **Verify post-deploy.**
   - **`/ride`** — submit a TEST entry: name `Audit`, email `test+ride+<timestamp>@example.com`, phone blank, lang PT. Within 60 seconds: V2 CRM CONTACTS gets a new or updated row with `Source = "Ride - Orlando Insider Guide"` and `DATA_TYPE = TEST`. ConvertKit should NOT subscribe. Repeat for the financial form (`Source = "Ride - Financial Starter Guide"`).
   - **`/go-big`** — submit a TEST entry: name `Audit`, email `test+gobig+<timestamp>@example.com`, business `Audit Co`, all four textareas with one-line answers, budget `not sure`, WhatsApp `+1 555 555 5555`. Within 60 seconds: V2 CRM CONTACTS gets a row with `Source = "GO BIG Brief"` and `DATA_TYPE = TEST`. CONSULTING `Quick_Note` should start with the date + `GO BIG Brief.` + `Business: Audit Co.`. CAPTAIN_LOG should have a `gobig_brief_received` row. ConvertKit should NOT subscribe. **No email** — TEST gating suppresses it. To test the email path, use a real address you control, run once, then delete the row from CONTACTS + CONSULTING and unsubscribe the address from ConvertKit.

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
| `orlando-form` | New: `/ride-intake` -> /exec | FIXED (live since prior deploy) | Static branch tests of the function pass. End-to-end test deferred to post-deploy verification. |
| `financial-form` | Same as above | FIXED (live since prior deploy) | Same as above. |
| `brief-form` | New: `/gobig-intake` -> /exec V14 | FIXED (pending deploy + V14 redeploy) | Static branch tests of `gobig-intake.js` pass (GET 405, no-secret 500, no-email 400, happy 200 with source `GO BIG Brief` and whatsapp -> phone mapping, bad-upstream 502, network-err 502). V14 syntax-checked with `node --check`. End-to-end test (TEST email) deferred to post-deploy verification by John David. |

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

V14 still hardcodes every intake into CONSULTING. The `Source` field is the
only segmentation. If John David later wants /ride leads in a separate
pipeline (e.g. a `RIDE` tab) or wants `brief-form` leads in `HUBBER`, that is
a V15 Apps Script change, not a code-side change in this repo. Route via:

```
payload.source -> route table -> target pipeline tab
```

inside `v2_intake.gs`. For now, segment downstream queries on `Source`:

- `Source = "Tally - prosperinamerica.com"` -> main lead capture (Tally form)
- `Source = "Ride - Orlando Insider Guide"` -> /ride orlando flow
- `Source = "Ride - Financial Starter Guide"` -> /ride financial flow
- `Source = "GO BIG Brief"` -> /go-big brief

CAPTAIN_LOG also carries `gobig_brief_received` rows with the full brief
content for any GO BIG intake (V14+).
