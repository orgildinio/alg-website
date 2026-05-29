#!/usr/bin/env python3
"""
Re-import 13 patched mockup HTMLs from the regressions round 2 bundle.
For each slug:
  1. Read the patched mockup HTML from /tmp/regressions_r2/.../patched_mockups/{slug}/mockup_*_pdp_v2.html
  2. Copy it wholesale to public/products/{slug}/index.html
  3. Verify: 5 breadcrumb segments, CSS >= 100KB, CFG-TYPE-1 present
"""
import re
import os
import shutil
from pathlib import Path

MOCKUP_BASE = Path('/tmp/regressions_r2/planoarch_regressions_2026-05-29_round2/patched_mockups')
PUBLIC_BASE = Path('public/products')

# Map slug -> mockup filename
SLUG_MAP = {
    'astra':              'mockup_astra_pdp_v2.html',
    'solstice':           'mockup_solstice_pdp_v2.html',
    'solstice-safezone':  'mockup_solstice_safezone_pdp_v2.html',
    'spectra':            'mockup_spectra_pdp_v2.html',
    'luxmark':            'mockup_luxmark_pdp_v2.html',
    'proarch-t':          'mockup_proarch_t1t2_pdp_v2.html',
    'trackstar':          'mockup_trackstar_pdp_v2.html',
    'lara':               'mockup_lara_pdp_v2.html',
    'luna':               'mockup_luna_pdp_v2.html',
    'waymark':            'mockup_waymark_pdp_v2.html',
    'retroarch-p1':       'mockup_retroarch_p1_pdp_v2.html',
    'retroarch-t1':       'mockup_retroarch_t1_pdp_v2.html',
    'proarch':            'mockup_proarch_pdp_v2.html',
}

errors = []
for slug, fname in SLUG_MAP.items():
    src = MOCKUP_BASE / slug / fname
    dst = PUBLIC_BASE / slug / 'index.html'

    if not src.exists():
        print(f'ERROR: source not found: {src}')
        errors.append(slug)
        continue

    if not dst.parent.exists():
        print(f'ERROR: dest dir not found: {dst.parent}')
        errors.append(slug)
        continue

    # Read source
    html = src.read_text(encoding='utf-8')

    # Verify breadcrumb
    bc = re.search(r'<nav class="breadcrumb-band"[^>]*>([\s\S]*?)</nav>', html)
    bc_text = re.sub(r'<[^>]+>', ' ', bc.group(1)).strip() if bc else ''
    sep_count = bc_text.count('›')

    # Verify CSS
    blocks = re.findall(r'<style[^>]*>[\s\S]*?</style>', html)
    total_css = sum(len(b) for b in blocks)
    has_type1 = bool(re.search(r'body\.[\w-]+-pdp\s*h[12][^{}]*\{[^}]*Lato[^}]*!important', html))

    # Title
    title_m = re.search(r'<title>(.*?)</title>', html)
    title = title_m.group(1) if title_m else 'NONE'

    # Checks
    ok = True
    if sep_count != 4:
        print(f'  WARNING {slug}: breadcrumb has {sep_count+1} segs (expected 5)')
        ok = False
    if total_css < 100000:
        print(f'  WARNING {slug}: CSS only {total_css//1024}KB (expected >=100KB)')
        ok = False
    if not has_type1:
        print(f'  WARNING {slug}: CFG-TYPE-1 not found')
        ok = False

    # Write
    dst.write_text(html, encoding='utf-8')
    status = 'OK' if ok else 'WARN'
    print(f'[{status}] {slug:<22} css={total_css//1024:>3}KB segs={sep_count+1} title={title[:50]}')

if errors:
    print(f'\nERRORS: {errors}')
    exit(1)
else:
    print(f'\nAll {len(SLUG_MAP)} PDPs re-imported successfully.')
