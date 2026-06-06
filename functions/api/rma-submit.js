/**
 * Cloudflare Pages Function: /api/rma-submit
 *
 * Receives the RMA JSON payload from the wizard and forwards it to the
 * warranty team via Resend. reply_to is set to the customer's email so
 * the warranty team can reply directly.
 *
 * Environment variables (set in CF Pages → Settings → Environment variables):
 *   RMA_MAIL_TOKEN  — Resend API key
 *   RMA_TO          — destination address (default: warranty@archipelagolighting.com)
 *   RMA_FROM        — verified sender (e.g. no-reply@archipelagolighting.com)
 *
 * If RMA_MAIL_TOKEN is missing, returns 503 so the front-end falls back to mailto.
 */
export async function onRequestPost(context) {
  const { request, env } = context;

  let payload;
  try {
    payload = await request.json();
  } catch {
    return new Response(JSON.stringify({ ok: false, error: 'Invalid JSON' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const {
    rma, company, contact, email, phone, account, poRef,
    lines, reasons, description, installDate, siteAddress,
    safetyFlag, action, actionLabel, laborShield,
    evidenceCount, receivedISO,
    // Internal routing — included in warranty-team email only, never returned to client
    _sev, _route,
  } = payload;

  // Build plain-text email body for the warranty team
  const lineRows = (lines || [])
    .map(l => `  · ${l.sku || '—'} | qty ${l.qty || 0} | desc ${l.desc || '—'} | loc ${l.loc || '—'}`)
    .join('\n');

  const body = [
    `NEW RMA REQUEST — ${rma}`,
    `severity (auto): ${_sev || '—'}  ·  route: ${_route || '—'}`,
    '',
    'BUYER',
    `company: ${company}`,
    `contact: ${contact}`,
    `email: ${email}`,
    `phone: ${phone || '—'}`,
    `account: ${account || '—'}`,
    `po/inv: ${poRef || '—'}`,
    '',
    'PRODUCTS',
    lineRows || '  (none)',
    '',
    'FAILURE',
    `reasons: ${(reasons || []).join(', ')}`,
    `install: ${installDate || '—'}   site: ${siteAddress || '—'}`,
    `description: ${description || '—'}`,
    `safety_flag: ${safetyFlag ? 'YES' : 'no'}`,
    '',
    `ACTION REQUESTED: ${actionLabel || action || '—'}`,
    `laborShield: ${laborShield || '—'}`,
    `evidence: ${evidenceCount || 0} files (attached separately)`,
    '',
    `received: ${receivedISO || new Date().toISOString()}`,
  ].join('\n');

  // If token is missing, return non-2xx so the front-end falls back to mailto
  if (!env.RMA_MAIL_TOKEN) {
    console.log('rma-submit: RMA_MAIL_TOKEN not set — returning 503 for mailto fallback');
    return new Response(JSON.stringify({ ok: false, error: 'Email provider not configured' }), {
      status: 503,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${env.RMA_MAIL_TOKEN}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from: env.RMA_FROM || 'no-reply@archipelagolighting.com',
      to: [env.RMA_TO || 'warranty@archipelagolighting.com'],
      reply_to: email || undefined,
      subject: `[${_sev || 'RMA'}] ${rma} · ${company || ''} · ${(lines && lines[0] && lines[0].sku) || '—'} · qty ${(lines || []).reduce((s, l) => s + (parseInt(l.qty) || 0), 0)}`,
      text: body,
    }),
  });

  if (!res.ok) {
    const err = await res.text();
    console.error('Resend error:', err);
    return new Response(JSON.stringify({ ok: false, error: 'Email delivery failed' }), {
      status: 502,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  return new Response(JSON.stringify({ ok: true, rma }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  });
}

// Handle OPTIONS preflight
export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    },
  });
}
