#!/usr/bin/env python3
"""
import_round4_traversal_fix.py

For each of the 11 affected planoARCH PDPs:
1. Copies the patched mockup HTML as a drop-in replacement for public/products/{slug}/index.html
2. Merges the shared-lib assets into public/products/{slug}/assets/ (additive, no deletions)

HTML filename → slug mapping:
  mockup_astra_pdp_v2.html           → astra
  mockup_solstice_pdp_v2.html        → solstice
  mockup_solstice_safezone_pdp_v2.html → solstice-safezone
  mockup_spectra_pdp_v2.html         → spectra
  mockup_proarch_t1t2_pdp_v2.html    → proarch-t
  mockup_trackstar_pdp_v2.html       → trackstar
  mockup_lara_pdp_v2.html            → lara
  mockup_luna_pdp_v2.html            → luna
  mockup_waymark_pdp_v2.html         → waymark
  mockup_retroarch_p1_pdp_v2.html    → retroarch-p1
  mockup_retroarch_t1_pdp_v2.html    → retroarch-t1
"""

import os
import shutil
import glob

BASE = '/home/ubuntu/planoarch_round4/planoarch_round4_traversal_fix_2026-05-29/patched_pdps'
DEST_ROOT = '/home/ubuntu/alg-website-src/public/products'

SLUG_MAP = {
    'astra': 'mockup_astra_pdp_v2.html',
    'solstice': 'mockup_solstice_pdp_v2.html',
    'solstice-safezone': 'mockup_solstice_safezone_pdp_v2.html',
    'spectra': 'mockup_spectra_pdp_v2.html',
    'proarch-t': 'mockup_proarch_t1t2_pdp_v2.html',
    'trackstar': 'mockup_trackstar_pdp_v2.html',
    'lara': 'mockup_lara_pdp_v2.html',
    'luna': 'mockup_luna_pdp_v2.html',
    'waymark': 'mockup_waymark_pdp_v2.html',
    'retroarch-p1': 'mockup_retroarch_p1_pdp_v2.html',
    'retroarch-t1': 'mockup_retroarch_t1_pdp_v2.html',
}

html_copied = 0
assets_copied = 0
errors = []

for slug, html_filename in SLUG_MAP.items():
    src_dir = os.path.join(BASE, slug)
    dest_dir = os.path.join(DEST_ROOT, slug)

    # 1. Copy patched HTML → index.html
    src_html = os.path.join(src_dir, html_filename)
    dest_html = os.path.join(dest_dir, 'index.html')
    if not os.path.exists(src_html):
        print(f'MISSING HTML: {src_html}')
        errors.append(slug)
        continue
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)
    shutil.copy2(src_html, dest_html)
    print(f'HTML: {slug}/index.html ← {html_filename}')
    html_copied += 1

    # 2. Merge assets/ tree (additive)
    src_assets = os.path.join(src_dir, 'assets')
    if not os.path.exists(src_assets):
        print(f'  (no assets to merge for {slug})')
        continue
    for src_file in glob.glob(os.path.join(src_assets, '**', '*'), recursive=True):
        if not os.path.isfile(src_file):
            continue
        rel_path = os.path.relpath(src_file, src_assets)
        dest_file = os.path.join(dest_dir, 'assets', rel_path)
        os.makedirs(os.path.dirname(dest_file), exist_ok=True)
        shutil.copy2(src_file, dest_file)
        print(f'  ASSET: {slug}/assets/{rel_path}')
        assets_copied += 1

print(f'\nSummary: {html_copied} HTMLs copied, {assets_copied} assets merged, {len(errors)} errors')
if errors:
    print(f'Errors: {errors}')
