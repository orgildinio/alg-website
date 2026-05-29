#!/usr/bin/env python3
"""
patch_em_host_mount.py

Patches all 20 EM/CRC driver public HTML files to use host-mount strategy
instead of document.documentElement.replaceWith() when running inside the
Astro BaseLayout wrapper. This preserves the site header/footer chrome.

Strategy: find the unique anchor line and replace the surrounding block using
a regex that matches the actual content (including em-dashes and blank lines).
"""

import re
import os

SLUGS = [
    'em07-cmb150dc', 'em07-cmb260dc', 'em08-amb48dc', 'em08-hmb170dc',
    'em08-mt150dc', 'em08-ytb60dc', 'em15-hmb170dc', 'em15-pmb120ac',
    'em20-cmb150dc', 'em20-cmb260dc', 'em20-hmb135ac', 'em25-hmb170dc',
    'em25-pmb120ac', 'em30-umb170dc', 'em40-rmb170dc', 'em60-gmb170dc',
    'em60-umb170dc', 'crc6-em24-jbs-b', 'crc6-em24-jbs-w', 'crcu-em24-jbm',
]

# Regex to match the replaceWith block (from the comment before DOMParser to the headScripts/bodyScripts lines)
# We match from "// Parse the template and swap" to "const bodyScripts = ..."
PATTERN = re.compile(
    r'(    // Parse the template and swap the root element\..*?'
    r'    const bodyScripts = allScripts\.filter\(s => !s\.closest\(\'head\'\)\);)',
    re.DOTALL
)

NEW_BLOCK = """    // Parse the template. HOST MODE if .{slug}-pdp host div exists (Astro wrapper);
    // STANDALONE MODE (replaceWith) for file:// preview fallback.
    const doc = new DOMParser().parseFromString(template, 'text/html');
    const _hostEl = document.querySelector('[class*="-pdp"]');
    const _hostClass = _hostEl ? Array.from(_hostEl.classList).find(c => c.endsWith('-pdp')) : null;
    const host = _hostClass ? document.querySelector('.' + _hostClass) : null;
    if (host) {
      // ===== HOST MODE \u2014 preserve Astro BaseLayout chrome =====
      for (const styleEl of doc.head.querySelectorAll('style')) {
        const scoped = document.createElement('style');
        scoped.textContent = styleEl.textContent;
        scoped.setAttribute('data-bundler-scoped', '1');
        document.head.appendChild(scoped);
      }
      for (const linkEl of doc.head.querySelectorAll('link[rel="stylesheet"]')) {
        document.head.appendChild(linkEl.cloneNode(true));
      }
      const existingRoot = host.querySelector('#root');
      if (existingRoot) existingRoot.remove();
      async function appendScriptOrChild(child, dest) {
        if (child.tagName === 'SCRIPT') {
          const s = document.createElement('script');
          for (const a of child.attributes) s.setAttribute(a.name, a.value);
          s.textContent = child.textContent;
          if ((s.type === 'text/babel' || s.type === 'text/jsx') && s.src) {
            if (blobToText[s.src]) { s.textContent = blobToText[s.src]; }
            else { try { const r = await fetch(s.src); s.textContent = await r.text(); } catch(e) {} }
            s.removeAttribute('src');
          }
          const p = s.src ? new Promise(function(r) { s.onload = s.onerror = r; }) : null;
          dest.appendChild(s);
          if (p) await p;
        } else { dest.appendChild(child); }
      }
      const _headScripts = Array.from(doc.head.querySelectorAll('script'));
      for (const s of _headScripts) await appendScriptOrChild(s, host);
      const _bodyChildren = Array.from(doc.body.children);
      for (const child of _bodyChildren) await appendScriptOrChild(child, host);
      const _thumb = document.getElementById('__bundler_thumbnail');
      if (_thumb) _thumb.remove();
      const _load = document.getElementById('__bundler_loading');
      if (_load) _load.remove();
      return;
    }
    // ===== STANDALONE MODE (file:// preview) =====
    document.documentElement.replaceWith(doc.documentElement);
    const allScripts = Array.from(document.scripts);
    const headScripts = allScripts.filter(s => s.closest('head'));
    const bodyScripts = allScripts.filter(s => !s.closest('head'));"""

patched = 0
skipped = 0
errors = []

for slug in SLUGS:
    html_path = f'public/products/{slug}/index.html'
    if not os.path.exists(html_path):
        print(f'MISSING: {html_path}')
        errors.append(slug)
        continue

    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'HOST MODE \u2014 preserve Astro BaseLayout chrome' in content:
        print(f'ALREADY PATCHED: {slug}')
        skipped += 1
        continue

    m = PATTERN.search(content)
    if not m:
        print(f'PATTERN NOT FOUND: {slug}')
        errors.append(slug)
        continue

    new_content = content[:m.start()] + NEW_BLOCK + content[m.end():]
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'PATCHED: {slug}')
    patched += 1

print(f'\nSummary: {patched} patched, {skipped} already done, {len(errors)} errors')
if errors:
    print(f'Errors: {errors}')
