#!/usr/bin/env python3
"""
Fix all 20 EM-driver PDPs:
1. Create placeholder hero PNG assets (001_white.png + 002_white.png) in each PDP's assets/ dir
2. Fix breadcrumb: Indoor C&I · Emergency · constⒶNT · {sku}
   → HOME › PRODUCTS › SAFETY & CONTROLS › CONSTⒶNT › {sku}
"""

import os
import re
import json
import gzip
import base64
import struct
import zlib

# SKU mapping: (slug, display_name, filename_stem)
SKUS = [
    ('em07-cmb150dc',  'EM07-CMB/150DC', 'em07-cmb-150dc'),
    ('em07-cmb260dc',  'EM07-CMB/260DC', 'em07-cmb-260dc'),
    ('em08-amb48dc',   'EM08-AMB/48DC',  'em08-amb-48dc'),
    ('em08-hmb170dc',  'EM08-HMB/170DC', 'em08-hmb-170dc'),
    ('em08-mt150dc',   'EM08-MT/150DC',  'em08-mt-150dc'),
    ('em08-ytb60dc',   'EM08-YTB/60DC',  'em08-ytb-60dc'),
    ('em15-hmb170dc',  'EM15-HMB/170DC', 'em15-hmb-170dc'),
    ('em15-pmb120ac',  'EM15-PMB/120AC', 'em15-pmb-120ac'),
    ('em20-cmb150dc',  'EM20-CMB/150DC', 'em20-cmb-150dc'),
    ('em20-cmb260dc',  'EM20-CMB/260DC', 'em20-cmb-260dc'),
    ('em20-hmb135ac',  'EM20-HMB/135AC', 'em20-hmb-135ac'),
    ('em25-hmb170dc',  'EM25-HMB/170DC', 'em25-hmb-170dc'),
    ('em25-pmb120ac',  'EM25-PMB/120AC', 'em25-pmb-120ac'),
    ('em30-umb170dc',  'EM30-UMB/170DC', 'em30-umb-170dc'),
    ('em40-rmb170dc',  'EM40-RMB/170DC', 'em40-rmb-170dc'),
    ('em60-gmb170dc',  'EM60-GMB/170DC', 'em60-gmb-170dc'),
    ('em60-umb170dc',  'EM60-UMB/170DC', 'em60-umb-170dc'),
    ('crc6-em24-jbs-b','CRC6-EM24/JBS/B','crc6-em24-jbs-b'),
    ('crc6-em24-jbs-w','CRC6-EM24/JBS/W','crc6-em24-jbs-w'),
    ('crcu-em24-jbm',  'CRCU-EM24/JBM', 'crcu-em24-jbm'),
]

def make_minimal_png(width=800, height=600, r=26, g=29, b=35):
    """Create a minimal solid-color PNG."""
    def png_chunk(chunk_type, data):
        c = chunk_type + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    
    # PNG signature
    sig = b'\x89PNG\r\n\x1a\n'
    # IHDR
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr = png_chunk(b'IHDR', ihdr_data)
    # IDAT - solid color rows
    raw_row = bytes([0] + [r, g, b] * width)  # filter byte + RGB pixels
    raw_data = raw_row * height
    compressed = zlib.compress(raw_data, 9)
    idat = png_chunk(b'IDAT', compressed)
    # IEND
    iend = png_chunk(b'IEND', b'')
    return sig + ihdr + idat + iend


def fix_breadcrumb_in_bundle(bundle_json_str, display_name):
    """
    Decompress UUID 4b7bc02c, replace the breadcrumb text, recompress.
    Returns updated bundle JSON string.
    """
    bundle = json.loads(bundle_json_str)
    
    for uuid, entry in bundle.items():
        if not uuid.startswith('4b7bc02c'):
            continue
        
        if not entry.get('compressed'):
            # Uncompressed — do direct replacement
            old = "Indoor C&amp;I · Emergency · <b>const<span className=\"ag-a\">Ⓐ</span>NT</b> · {sku}"
            new = ("<a href=\"/\" style={{color:'inherit',textDecoration:'none'}}>HOME</a>"
                   " ›&nbsp;"
                   "<a href=\"/collections/\" style={{color:'inherit',textDecoration:'none'}}>PRODUCTS</a>"
                   " ›&nbsp;"
                   "<a href=\"/collections/safety-controls/\" style={{color:'inherit',textDecoration:'none'}}>SAFETY &amp; CONTROLS</a>"
                   " ›&nbsp;"
                   "<a href=\"/collections/constant/\" style={{color:'inherit',textDecoration:'none'}}>CONST<span className=\"ag-a\">Ⓐ</span>NT</a>"
                   " ›&nbsp;"
                   "<b>{sku}</b>")
            entry['data'] = entry['data'].replace(old, new)
            break
        
        # Compressed
        compressed = base64.b64decode(entry['data'])
        decompressed = gzip.decompress(compressed).decode('utf-8')
        
        # The old breadcrumb line
        old = "Indoor C&amp;I · Emergency · <b>const<span className=\"ag-a\">Ⓐ</span>NT</b> · {sku}"
        new = ("<a href=\"/\" style={{color:'inherit',textDecoration:'none'}}>HOME</a>"
               " ›\u00a0"
               "<a href=\"/collections/\" style={{color:'inherit',textDecoration:'none'}}>PRODUCTS</a>"
               " ›\u00a0"
               "<a href=\"/collections/safety-controls/\" style={{color:'inherit',textDecoration:'none'}}>SAFETY &amp; CONTROLS</a>"
               " ›\u00a0"
               "<a href=\"/collections/constant/\" style={{color:'inherit',textDecoration:'none'}}>CONST<span className=\"ag-a\">Ⓐ</span>NT</a>"
               " ›\u00a0"
               "<b>{sku}</b>")
        
        if old not in decompressed:
            print(f"  WARNING: breadcrumb pattern not found in {uuid[:8]}")
            # Try to find what's there
            idx = decompressed.find('Indoor C')
            if idx > -1:
                print(f"  Found 'Indoor C' at {idx}: {repr(decompressed[idx:idx+200])}")
            continue
        
        updated = decompressed.replace(old, new)
        
        # Recompress
        new_compressed = gzip.compress(updated.encode('utf-8'), compresslevel=9)
        entry['data'] = base64.b64encode(new_compressed).decode('ascii')
        print(f"  Breadcrumb patched in {uuid[:8]}")
        break
    
    return json.dumps(bundle, separators=(',', ':'))


def process_pdp(slug, display_name, filename_stem):
    """Process one EM-driver PDP: create assets + fix breadcrumb."""
    pdp_dir = f'public/products/{slug}'
    assets_dir = f'{pdp_dir}/assets'
    html_path = f'{pdp_dir}/index.html'
    
    print(f"\n--- {slug} ---")
    
    # Step 1: Create assets directory and placeholder PNGs
    os.makedirs(assets_dir, exist_ok=True)
    
    for suffix in ['001', '002']:
        png_path = f'{assets_dir}/{filename_stem}-{suffix}_white.png'
        if not os.path.exists(png_path):
            png_data = make_minimal_png(800, 600, r=245, g=245, b=245)  # light gray
            with open(png_path, 'wb') as f:
                f.write(png_data)
            print(f"  Created {png_path}")
        else:
            print(f"  Already exists: {png_path}")
    
    # Step 2: Fix breadcrumb in the HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Find the bundle script (script[1])
    # Use a regex to find the large bundle script
    # The bundle script starts with {"a38a1f88-...
    bundle_pattern = re.compile(
        r'(<script[^>]*>)({"a38a1f88-[^<]+)(</script>)',
        re.DOTALL
    )
    
    match = bundle_pattern.search(html)
    if not match:
        print(f"  ERROR: Could not find bundle script in {html_path}")
        return False
    
    open_tag = match.group(1)
    bundle_json = match.group(2)
    close_tag = match.group(3)
    
    # Fix the breadcrumb
    updated_bundle = fix_breadcrumb_in_bundle(bundle_json, display_name)
    
    # Replace in HTML
    new_html = html[:match.start()] + open_tag + updated_bundle + close_tag + html[match.end():]
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"  HTML updated: {html_path}")
    return True


def main():
    os.chdir('/home/ubuntu/alg-website-src')
    
    success = 0
    failed = 0
    
    for slug, display_name, filename_stem in SKUS:
        try:
            if process_pdp(slug, display_name, filename_stem):
                success += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  EXCEPTION for {slug}: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print(f"\n=== Done: {success} OK, {failed} failed ===")


if __name__ == '__main__':
    main()
