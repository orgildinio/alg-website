/**
 * Cloudflare Pages Function: /api/rma-submit
 *
 * Scaffold — receives the RMA JSON payload from the wizard,
 * forwards it to the warranty team email via a transactional
 * email provider (e.g. Resend, SendGrid, Postmark).
 *
 * Current state: mailto: flow in the wizard handles delivery.
 * This endpoint is wired for the future server-side upgrade.
 *
 * Environment variables required (set in CF Pages dashboard):
 *   RESEND_API_KEY   — Resend API key
 *   WARRANTY_EMAIL   — destination address (warranty@archipelagolighting.com)
 *   FROM_EMAIL       — verified sender (noreply@archipelagolighting.com)
 */

export async function onRequestPost(context) {
  const { request, env } = context;

  // CORS preflight handled by CF Pages automatically for same-origin.
  // For cross-origin dev, add headers as needed.

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
    .map(l => `  · ${l.sku || '—'} | qty ${l.qty || 0} | lot ${l.dateCode || '—'}`)
    .join('\n');

  const body = [
    `NEW RMA REQUEST — ${rma}`,
    `severity (auto): ${_sev || '—'}  ·  route: ${_route || '—'}`,
    '',
    'BUYER',
    `company: ${company}`,
    `contact: ${contact}`,
    `email: ${email}`,
    `phone: ${phone}`,
    `account: ${account || '—'}`,
    `po/inv: ${poRef || '—'}`,
    '',
    'PRODUCTS',
    lineRows,
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
    `received: ${receivedISO}`,
  ].join('\n');

  // Forward via Resend (swap for SendGrid/Postmark as needed)
  if (env.RESEND_API_KEY) {
    const res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${env.RESEND_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: env.FROM_EMAIL || 'noreply@archipelagolighting.com',
        to: [env.WARRANTY_EMAIL || 'warranty@archipelagolighting.com'],
        subject: `[${_sev || 'RMA'}] ${rma} — ${company || ''}`,
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
  } else {
    // No email provider configured — log to CF Workers logs for now
    console.log('rma-submit (no email provider):', JSON.stringify({ rma, company, _sev }));
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
