#!/usr/bin/env python3
"""
Wire the DOWNLOAD SPECS CTA in all 20 EM-driver PDP React bundles (UUID 018e416e)
to the canonical per-SKU PDF path: /products/{slug}/assets/datasheets/{slug}.pdf

The React component has:
  <a className="alg-btn" href="#" ...>Download Specs</a>

We patch it to:
  <a className="alg-btn" href="/products/{slug}/assets/datasheets/{slug}.pdf" download ...>Download Specs</a>
"""
import re, json, gzip, base64, os

em_slugs = [
    'em07-cmb150dc', 'em07-cmb260dc', 'em08-amb48dc', 'em08-hmb170dc',
    'em08-mt150dc', 'em08-ytb60dc', 'em15-hmb170dc', 'em15-pmb120ac',
    'em20-cmb150dc', 'em20-cmb260dc', 'em20-hmb135ac', 'em25-hmb170dc',
    'em25-pmb120ac', 'em30-umb170dc', 'em40-rmb170dc', 'em60-gmb170dc',
    'em60-umb170dc', 'crc6-em24-jbs-b', 'crc6-em24-jbs-w', 'crcu-em24-jbm'
]

REACT_UUID = '018e416e-13bd-453c-9f45-73e593db329c'

patched = 0
skipped = 0

for slug in em_slugs:
    pdf_path = f'/products/{slug}/assets/datasheets/{slug}.pdf'
    html_path = f'public/products/{slug}/index.html'
    
    if not os.path.exists(html_path):
        print(f'SKIP {slug}: HTML not found')
        skipped += 1
        continue
    
    # Verify PDF exists
    local_pdf = f'public/products/{slug}/assets/datasheets/{slug}.pdf'
    if not os.path.exists(local_pdf):
        print(f'WARN {slug}: PDF not found at {local_pdf}')
    
    with open(html_path) as f:
        html = f.read()
    
    scripts = re.findall(r'<script[^>]*>([\s\S]*?)</script>', html)
    manifest = json.loads(scripts[1])
    
    if REACT_UUID not in manifest:
        print(f'SKIP {slug}: UUID {REACT_UUID} not found in manifest')
        skipped += 1
        continue
    
    entry = manifest[REACT_UUID]
    data = entry['data']
    compressed = entry.get('compressed', False)
    
    if compressed:
        decoded = gzip.decompress(base64.b64decode(data)).decode('utf-8')
    else:
        decoded = base64.b64decode(data).decode('utf-8')
    
    # Find and patch the Download Specs href
    # Current pattern: href="#" style={{ background: 'transparent'...}}>Download Specs</a>
    # We need to replace href="#" with href="/products/{slug}/assets/datasheets/{slug}.pdf"
    # in the context of the Download Specs button
    
    # The exact pattern from find_download_cta.py:
    # <a className="alg-btn" href="#" style={{ background: 'transparent', borderColor: darkHero ? 'rgba(255,255,255,.45)' : 'var(--ink)', color: darkHero ? '#fff' : 'var(--ink)' }}>Download Specs</a>
    
    old_pattern = r'''<a className="alg-btn" href="#" style=\{\{ background: 'transparent', borderColor: darkHero \? 'rgba\(255,255,255,\.45\)' : 'var\(--ink\)', color: darkHero \? '#fff' : 'var\(--ink\)' \}\}>Download Specs</a>'''
    new_str = f'''<a className="alg-btn" href="{pdf_path}" download style={{{{ background: 'transparent', borderColor: darkHero ? 'rgba(255,255,255,.45)' : 'var(--ink)', color: darkHero ? '#fff' : 'var(--ink)' }}}}>Download Specs</a>'''
    
    new_decoded = re.sub(old_pattern, new_str, decoded)
    
    if new_decoded == decoded:
        # Try a simpler approach - just find the href="#" near Download Specs
        # Look for the specific context
        m = re.search(r'(href="#"[^>]*>Download Specs)', decoded)
        if m:
            old_href = m.group(0)
            new_href = old_href.replace('href="#"', f'href="{pdf_path}" download')
            new_decoded = decoded.replace(old_href, new_href)
            if new_decoded == decoded:
                print(f'FAIL {slug}: Could not patch href')
                skipped += 1
                continue
        else:
            print(f'FAIL {slug}: Pattern not found')
            skipped += 1
            continue
    
    # Verify the patch
    if pdf_path not in new_decoded:
        print(f'FAIL {slug}: PDF path not in patched bundle')
        skipped += 1
        continue
    
    # Re-encode
    if compressed:
        new_data = base64.b64encode(gzip.compress(new_decoded.encode('utf-8'))).decode('ascii')
    else:
        new_data = base64.b64encode(new_decoded.encode('utf-8')).decode('ascii')
    
    manifest[REACT_UUID]['data'] = new_data
    
    # Rebuild the HTML
    new_manifest_json = json.dumps(manifest, separators=(',', ':'))
    
    # Replace the manifest script in the HTML
    # The manifest is scripts[1] - find and replace it
    # Pattern: second <script> tag content
    script_pattern = r'(<script[^>]*>)([\s\S]*?)(</script>)'
    script_matches = list(re.finditer(script_pattern, html))
    
    if len(script_matches) < 2:
        print(f'FAIL {slug}: Could not find script tags')
        skipped += 1
        continue
    
    # Replace the second script tag's content
    second_script = script_matches[1]
    new_html = html[:second_script.start(2)] + new_manifest_json + html[second_script.end(2):]
    
    with open(html_path, 'w') as f:
        f.write(new_html)
    
    print(f'OK   {slug}: Wired to {pdf_path}')
    patched += 1

print(f'\nDone: {patched} patched, {skipped} skipped')
