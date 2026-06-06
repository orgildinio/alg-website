// functions/api/packet.js — Cloudflare Pages Function
// POST { docs:[{fileId,label,type,family}], packetName? } -> streams a real .zip of the WorkDrive PDFs + a cover sheet.
// The browser CANNOT fetch WorkDrive (external links are viewer HTML + CORS) — this runs server-side with the Zoho API.
//
// Required env secrets (Cloudflare → Pages → Settings → Environment variables, set by James/dev):
//   ZOHO_WD_CLIENT_ID, ZOHO_WD_CLIENT_SECRET, ZOHO_WD_REFRESH_TOKEN   (OAuth scope: WorkDrive.files.READ)
//   ZOHO_ACCOUNTS_HOST (default https://accounts.zoho.com)            // .com / .eu / etc per the org's DC
//
// npm i fflate   (pure-JS zip, runs in Workers/Pages Functions)
import { zipSync, strToU8 } from 'fflate';

async function getAccessToken(env){
  const host = env.ZOHO_ACCOUNTS_HOST || 'https://accounts.zoho.com';
  const r = await fetch(host + '/oauth/v2/token', {
    method: 'POST',
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      refresh_token: env.ZOHO_WD_REFRESH_TOKEN,
      client_id:     env.ZOHO_WD_CLIENT_ID,
      client_secret: env.ZOHO_WD_CLIENT_SECRET,
      grant_type:    'refresh_token',
    }),
  });
  const j = await r.json();
  if (!j.access_token) throw new Error('token: ' + JSON.stringify(j));
  return j.access_token;
}

const safe = s => String(s || 'file').replace(/[^\w.\- ]+/g, '_').slice(0, 80);

function coverSheet(docs, packetName){
  const lines = [
    'ARCHIPELAGO LIGHTING GROUP — SPEC PACKET',
    packetName ? ('Packet: ' + packetName) : '',
    'Generated: ' + new Date().toISOString(),
    '(866) 912-3220 · spec@archipelagolighting.com',
    '',
    'CONTENTS (' + docs.length + ' documents):',
    ...docs.map((d,i) => `  ${i+1}. ${d.family || ''} — ${d.type || ''}  (${safe(d.label || d.fileId)})`),
  ];
  return strToU8(lines.filter(x => x !== null).join('\n'));
}

export async function onRequestPost({ request, env }){
  try {
    const { docs = [], packetName } = await request.json();
    if (!docs.length) return new Response('No documents selected', { status: 400 });

    const token = await getAccessToken(env);
    const files = { 'ALG-Spec-Packet/_COVER-SHEET.txt': coverSheet(docs, packetName) };
    const failed = [];

    for (const d of docs){
      // download the PDF bytes by WorkDrive file-ID
      const resp = await fetch('https://download-accl.zoho.com/v1/workdrive/download/' + encodeURIComponent(d.fileId), {
        headers: { Authorization: 'Zoho-oauthtoken ' + token },
      });
      if (!resp.ok){ failed.push(safe(d.label || d.fileId)); continue; }
      const bytes = new Uint8Array(await resp.arrayBuffer());
      const name = `ALG-Spec-Packet/${safe(d.family)} — ${safe(d.type || 'doc')}.pdf`;
      files[name] = bytes;
    }
    if (failed.length) files['ALG-Spec-Packet/_UNAVAILABLE.txt'] = strToU8('Could not include:\n' + failed.join('\n'));

    const zip = zipSync(files, { level: 0 }); // PDFs already compressed; level 0 = fast
    return new Response(zip, {
      headers: {
        'content-type': 'application/zip',
        'content-disposition': 'attachment; filename="ALG-Spec-Packet.zip"',
        'cache-control': 'no-store',
      },
    });
  } catch (e){
    return new Response('Packet build failed: ' + e.message, { status: 500 });
  }
}
