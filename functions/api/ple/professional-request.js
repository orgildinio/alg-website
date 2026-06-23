/**
 * Cloudflare Pages Function: /api/ple/professional-request
 *
 * Server-side proxy: receives the Pro Layout form JSON from the browser and
 * forwards it to the ACC engine at /api/public/ple/professional-request.
 * Keeps the ACC origin out of the browser entirely — no CORS exposure, no
 * direct browser→onrender.com calls.
 *
 * Environment variables (set in CF Pages → Settings → Environment variables):
 *   ACC_BASE  — ACC origin, e.g. https://alg-command-center.onrender.com
 *               (defaults to the production ACC URL if not set)
 *
 * The function passes the JSON body through unchanged and returns the ACC
 * response (handle, status, message) directly to the browser.
 */

const ACC_DEFAULT = 'https://alg-command-center.onrender.com';

export async function onRequestPost(context) {
  const { request, env } = context;

  // Parse incoming JSON from the browser
  let payload;
  try {
    payload = await request.json();
  } catch {
    return jsonResponse({ ok: false, error: 'Invalid JSON' }, 400);
  }

  // Enforce 16 KB body bound (ACC limit)
  const bodyStr = JSON.stringify(payload);
  if (bodyStr.length > 16384) {
    return jsonResponse({ ok: false, error: 'BODY_BOUND', message: 'Payload exceeds 16 KB limit' }, 413);
  }

  const accBase = (env.ACC_BASE || ACC_DEFAULT).replace(/\/$/, '');
  const accUrl = `${accBase}/api/public/ple/professional-request`;

  let accResp;
  try {
    accResp = await fetch(accUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Origin': 'https://www.archipelagolighting.com',
      },
      body: bodyStr,
    });
  } catch (err) {
    console.error('[ple/professional-request] ACC fetch error:', err);
    return jsonResponse({ ok: false, error: 'ACC_UNAVAILABLE', message: 'Engine unreachable' }, 502);
  }

  const accBody = await accResp.json().catch(() => ({}));

  if (!accResp.ok) {
    console.error('[ple/professional-request] ACC error:', accResp.status, JSON.stringify(accBody));
    return jsonResponse(
      { ok: false, error: accBody?.code || 'ACC_ERROR', message: accBody?.error || 'Submission failed' },
      accResp.status
    );
  }

  // Forward the handle + message back to the browser
  return jsonResponse({ ok: true, handle: accBody.handle, message: accBody.message }, 200);
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

function jsonResponse(body, status) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}
