#!/usr/bin/env python3
"""
Deploy v9 EM-driver HTMLs to public/products/{slug}/index.html
Each v9 HTML is a self-contained file — copy as-is to replace the old bundle.
"""
import os
import shutil

V9_DIR = '/tmp/v9'
PUBLIC_DIR = '/home/ubuntu/alg-website-src/public/products'

SLUGS = [
    'em07-cmb150dc', 'em07-cmb260dc',
    'em08-amb48dc', 'em08-hmb170dc', 'em08-mt150dc', 'em08-ytb60dc',
    'em15-hmb170dc', 'em15-pmb120ac',
    'em20-cmb150dc', 'em20-cmb260dc', 'em20-hmb135ac',
    'em25-hmb170dc', 'em25-pmb120ac',
    'em30-umb170dc', 'em40-rmb170dc',
    'em60-gmb170dc', 'em60-umb170dc',
    'crc6-em24-jbs-b', 'crc6-em24-jbs-w', 'crcu-em24-jbm',
]

ok = 0
missing = []
for slug in SLUGS:
    src = os.path.join(V9_DIR, f'{slug}.html')
    dest_dir = os.path.join(PUBLIC_DIR, slug)
    dest = os.path.join(dest_dir, 'index.html')
    if not os.path.exists(src):
        missing.append(slug)
        continue
    os.makedirs(dest_dir, exist_ok=True)
    shutil.copy2(src, dest)
    size_kb = os.path.getsize(dest) // 1024
    print(f'  ✓ {slug}/index.html ({size_kb} KB)')
    ok += 1

print(f'\n{ok}/20 v9 HTMLs deployed.')
if missing:
    print(f'MISSING: {missing}')
