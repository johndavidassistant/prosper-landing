// netlify/functions/gobig-intake.js
//
// Server-side proxy for the /go-big brief-form. Mirrors the architecture of
// ride-intake.js but extracts the richer brief fields (business, what,
// not_working, want, budget) and forwards them upstream so V14+ Apps Script
// can record them and email John David's system inbox on real submissions.
//
// Required env var (set in Netlify Site settings -> Environment variables):
//   V2_INTAKE_SECRET = <same value Apps Script Script Property holds>
//
// Optional env var:
//   APPS_SCRIPT_EXEC_URL = override the upstream /exec URL (default below)
//
// Request: POST application/json
//   { name?, email, whatsapp?, phone?, business?, what_do_you_do?,
//     not_working?, want?, budget?, lang? }
//
// Response: 200 with JSON from Apps Script, or 4xx/5xx with { status, message }.

const DEFAULT_EXEC_URL =
  'https://script.google.com/macros/s/AKfycbzl7pXpzF5mK2tMTjG9I-8vaHEfM1hYG5TeMtLY8BvHR7Eq2OknQEe-oJRNiBksK3ZuHQ/exec';

const SOURCE_LABEL = 'GO BIG Brief';

function jsonResponse(statusCode, body) {
  return {
    statusCode,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  };
}

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return jsonResponse(405, { status: 'error', message: 'POST required' });
  }

  const secret = process.env.V2_INTAKE_SECRET;
  if (!secret) {
    return jsonResponse(500, {
      status: 'error',
      message: 'Server misconfigured: V2_INTAKE_SECRET env var is missing.',
    });
  }
  const execUrl = process.env.APPS_SCRIPT_EXEC_URL || DEFAULT_EXEC_URL;

  let payload;
  try {
    payload = event.body ? JSON.parse(event.body) : {};
  } catch (err) {
    return jsonResponse(400, { status: 'error', message: 'Invalid JSON body.' });
  }

  const email = String(payload.email || '').trim();
  if (!email || email.indexOf('@') === -1) {
    return jsonResponse(400, { status: 'error', message: 'email required' });
  }

  // Apps Script V13 requires non-empty name and phone. Use safe placeholders
  // when /go-big leaves them blank so the row still lands in CRM.
  const rawName = String(payload.name || '').trim();
  const rawPhone = String(payload.whatsapp || payload.phone || '').trim();
  const name = rawName || email.split('@')[0];
  const phone = rawPhone || 'not-provided';

  const upstreamPayload = {
    name,
    email,
    phone,
    source: SOURCE_LABEL,
    lang: String(payload.lang || '').trim(),

    // Rich brief fields. V13 ignores unknown payload keys. V14 reads them
    // for the Quick_Note summary, the CAPTAIN_LOG entry, and the email
    // notification body.
    business: String(payload.business || '').trim(),
    what_do_you_do: String(payload.what_do_you_do || '').trim(),
    not_working: String(payload.not_working || '').trim(),
    want: String(payload.want || '').trim(),
    budget: String(payload.budget || '').trim(),
  };

  const upstreamUrl = `${execUrl}?secret=${encodeURIComponent(secret)}`;

  let upstreamResp;
  try {
    upstreamResp = await fetch(upstreamUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(upstreamPayload),
      redirect: 'follow',
    });
  } catch (err) {
    return jsonResponse(502, {
      status: 'error',
      message: 'Upstream Apps Script request failed: ' + err.message,
    });
  }

  const text = await upstreamResp.text();
  let parsed;
  try {
    parsed = JSON.parse(text);
  } catch (_err) {
    parsed = { status: 'unknown', message: 'Non-JSON upstream response', raw: text.slice(0, 200) };
  }

  const isOk = upstreamResp.ok && parsed && (parsed.status === 'ok' || parsed.status === 'updated');
  return jsonResponse(isOk ? 200 : 502, parsed);
};
