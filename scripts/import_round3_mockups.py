#!/usr/bin/env python3
"""
Import round 3 patched mockup HTMLs → public/products/{slug}/index.html
Maps mockup filename to canonical slug directory.
"""
import shutil, os

BASE = '/home/ubuntu/planoarch_round3/planoarch_round3_2026-05-29/patched_mockups'
DEST = '/home/ubuntu/alg-website-src/public/products'

# slug → mockup filename
SLUGS = {
    'astra':            'mockup_astra_pdp_v2.html',
    'solstice':         'mockup_solstice_pdp_v2.html',
    'solstice-safezone':'mockup_solstice_safezone_pdp_v2.html',
    'spectra':          'mockup_spectra_pdp_v2.html',
    'luxmark':          'mockup_luxmark_pdp_v2.html',
    'proarch-t':        'mockup_proarch_t_pdp_v2.html',
    'trackstar':        'mockup_trackstar_pdp_v2.html',
    'lara':             'mockup_lara_pdp_v2.html',
    'luna':             'mockup_luna_pdp_v2.html',
    'waymark':          'mockup_waymark_pdp_v2.html',
    'retroarch-p1':     'mockup_retroarch_p1_pdp_v2.html',
    'retroarch-t1':     'mockup_retroarch_t1_pdp_v2.html',
    'proarch':          'mockup_proarch_pdp_v2.html',
}

ok = 0
for slug, fname in SLUGS.items():
    src = os.path.join(BASE, slug, fname)
    dst = os.path.join(DEST, slug, 'index.html')
    if not os.path.exists(src):
        print(f'  MISSING  {slug} → {src}')
        continue
    if not os.path.exists(os.path.dirname(dst)):
        print(f'  NO DEST  {slug} → {dst}')
        continue
    shutil.copy2(src, dst)
    print(f'  ✅ {slug}')
    ok += 1

print(f'\n{ok}/{len(SLUGS)} imported')
