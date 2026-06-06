// functions/api/packet.js — Cloudflare Pages Function
// POST { docs:[{fileId,label,type,family}], packetName? } -> streams a real .zip of the WorkDrive PDFs + a cover sheet.
// NO npm dependencies — a minimal store-mode ZIP is built inline (PDFs are already compressed, so "store" is ideal
// and avoids the CF Pages Functions bundler choking on a package import).
//
// Required env secrets (Cloudflare → Pages → Settings → Environment variables, set by James/dev):
//   ZOHO_WD_CLIENT_ID, ZOHO_WD_CLIENT_SECRET, ZOHO_WD_REFRESH_TOKEN   (OAuth scope: WorkDrive.files.READ)
//   ZOHO_ACCOUNTS_HOST (default https://accounts.zoho.com)            // .com / .eu / etc per the org's DC

// ---------- dependency-free ZIP (store / no compression) ----------
function crc32(bytes){
  let crc = ~0;
  for (let i = 0; i < bytes.length; i++){
    crc ^= bytes[i];
    for (let j = 0; j < 8; j++) crc = (crc >>> 1) ^ (0xEDB88320 & -(crc & 1));
  }
  return (~crc) >>> 0;
}
function zipStore(files){ // files: { name: Uint8Array }
  const enc = new TextEncoder();
  const u16 = n => [n & 255, (n >>> 8) & 255];
  const u32 = n => [n & 255, (n >>> 8) & 255, (n >>> 16) & 255, (n >>> 24) & 255];
  const locals = [], central = [];
  let offset = 0;
  for (const name in files){
    const data = files[name];
    const nb = enc.encode(name);
    const crc = crc32(data), size = data.length;
    const lh = [...u32(0x04034b50), ...u16(20), ...u16(0), ...u16(0), ...u16(0), ...u16(0),
                ...u32(crc), ...u32(size), ...u32(size), ...u16(nb.length), ...u16(0)];
    const lbuf = new Uint8Array(lh.length + nb.length + size);
    lbuf.set(lh, 0); lbuf.set(nb, lh.length); lbuf.set(data, lh.length + nb.length);
    locals.push(lbuf);
    const cd = [...u32(0x02014b50), ...u16(20), ...u16(20), ...u16(0), ...u16(0), ...u16(0), ...u16(0),
                ...u32(crc), ...u32(size), ...u32(size), ...u16(nb.length), ...u16(0), ...u16(0),
                ...u16(0), ...u16(0), ...u32(0), ...u32(offset)];
    const cbuf = new Uint8Array(cd.length + nb.length);
    cbuf.set(cd, 0); cbuf.set(nb, cd.length);
    central.push(cbuf);
    offset += lbuf.length;
  }
  const cSize = central.reduce((a, c) => a + c.length, 0);
  const eocd = new Uint8Array([...u32(0x06054b50), ...u16(0), ...u16(0),
    ...u16(central.length), ...u16(central.length), ...u32(cSize), ...u32(offset), ...u16(0)]);
  const total = locals.reduce((a, c) => a + c.length, 0) + cSize + eocd.length;
  const out = new Uint8Array(total);
  let p = 0;
  for (const c of locals){ out.set(c, p); p += c.length; }
  for (const c of central){ out.set(c, p); p += c.length; }
  out.set(eocd, p);
  return out;
}
const strU8 = s => new TextEncoder().encode(s);

// ---------- Zoho auth ----------
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
  return strU8([
    'ARCHIPELAGO LIGHTING GROUP — SPEC PACKET',
    packetName ? ('Packet: ' + packetName) : '',
    'Generated: ' + new Date().toISOString(),
    '(866) 912-3220 · spec@archipelagolighting.com',
    '',
    'CONTENTS (' + docs.length + ' documents):',
    ...docs.map((d, i) => `  ${i + 1}. ${d.family || ''} — ${d.type || ''}  (${safe(d.label || d.fileId)})`),
  ].filter(x => x !== '').join('\n'));
}

export async function onRequestPost({ request, env }){
  try {
    const { docs = [], packetName } = await request.json();
    if (!docs.length) return new Response('No documents selected', { status: 400 });

    const token = await getAccessToken(env);
    const files = { 'ALG-Spec-Packet/_COVER-SHEET.txt': coverSheet(docs, packetName) };
    const failed = [];

    for (const d of docs){
      const resp = await fetch('https://download-accl.zoho.com/v1/workdrive/download/' + encodeURIComponent(d.fileId), {
        headers: { Authorization: 'Zoho-oauthtoken ' + token },
      });
      if (!resp.ok){ failed.push(safe(d.label || d.fileId)); continue; }
      const bytes = new Uint8Array(await resp.arrayBuffer());
      files[`ALG-Spec-Packet/${safe(d.family)} — ${safe(d.type || 'doc')}.pdf`] = bytes;
    }
    if (failed.length) files['ALG-Spec-Packet/_UNAVAILABLE.txt'] = strU8('Could not include:\n' + failed.join('\n'));

    const zip = zipStore(files);
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
