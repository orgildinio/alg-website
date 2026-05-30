"""
card_paths_sweep: Fix broken family-card image paths and broken href slugs
across all planoARCH PDPs.

Fixes:
1. Broken src paths: ../MOCKUP-FOLDER/assets/... → /products/{slug}/assets/...
2. Broken href slugs: /products/old-slug/ → /products/canonical-slug/
"""
import re, os

PLANO_SLUGS = ['astra', 'lara', 'luna', 'luxmark', 'proarch', 'proarch-t', 
               'solstice', 'solstice-safezone', 'spectra', 'trackstar', 'waymark']

# Mockup folder → canonical slug
FOLDER_TO_SLUG = {
    'LCDL-Solstice': 'solstice',
    'LCDL-SolsticeSafeZone': 'solstice-safezone',
    'LCDL-SpectraI': 'spectra',
    'LCDL-AstraI': 'astra',
    'LUXA-LUNA': 'luna',
    'LUXA-LARA': 'lara',
    'LPVT-proARCH': 'proarch-t',
    'LPVT-Luxmark': 'luxmark',
    'LTRK-Trackstar': 'trackstar',
    'LWRL-Waymark': 'waymark',
    'retroarch-p1': 'retroarch-p1',  # self-referential, keep as-is but fix path
}

# Broken href → canonical href
HREF_FIXES = {
    '/products/astra-i/': '/products/astra/',
    '/products/lcdl-astra-i/': '/products/astra/',
    '/products/lcdl-astra/': '/products/astra/',
    '/products/lcdl-solstice/': '/products/solstice/',
    '/products/lcdl-solstice-safezone/': '/products/solstice-safezone/',
    '/products/lcdl-spectra/': '/products/spectra/',
    '/products/lpvt-luxmark/': '/products/luxmark/',
    '/products/ltrk-trackstar/': '/products/trackstar/',
    '/products/luxa-lara/': '/products/lara/',
    '/products/luxa-luna/': '/products/luna/',
    '/products/lwrl-waymark/': '/products/waymark/',
    '/products/lbol-sentry/': '/products/lbol-sentry-bollard/',
    '/products/symmetry/': '/products/lptp-symmetry-post-top/',
}

BROKEN_SRC_PATTERN = re.compile(r'src="\.\./([^/]+)/assets/([^"]+)"')

total_src_fixes = 0
total_href_fixes = 0

for slug in PLANO_SLUGS:
    # Fix the public/products/{slug}/index.html file
    fpath = f'public/products/{slug}/index.html'
    if not os.path.exists(fpath):
        continue
    
    with open(fpath) as f:
        content = f.read()
    
    original = content
    src_fixes = 0
    href_fixes = 0
    
    # Fix broken src paths
    def replace_src(m):
        global src_fixes
        folder = m.group(1)
        subpath = m.group(2)
        if folder in FOLDER_TO_SLUG:
            target_slug = FOLDER_TO_SLUG[folder]
            new_path = f'/products/{target_slug}/assets/{subpath}'
            # Verify the file exists
            local_path = f'public/products/{target_slug}/assets/{subpath}'
            if os.path.exists(local_path):
                return f'src="{new_path}"'
            else:
                print(f"  WARNING: {slug}: target file missing: {local_path}")
                return m.group(0)  # keep original
        else:
            print(f"  WARNING: {slug}: unknown folder {folder}")
            return m.group(0)
    
    new_content = BROKEN_SRC_PATTERN.sub(replace_src, content)
    src_fixes = content.count('../') - new_content.count('../')  # rough count
    
    # Fix broken hrefs
    for old_href, new_href in HREF_FIXES.items():
        if old_href in new_content:
            count = new_content.count(old_href)
            new_content = new_content.replace(old_href, new_href)
            href_fixes += count
    
    if new_content != original:
        with open(fpath, 'w') as f:
            f.write(new_content)
        
        # Count actual changes
        actual_src = len(BROKEN_SRC_PATTERN.findall(original)) - len(BROKEN_SRC_PATTERN.findall(new_content))
        actual_href = sum(original.count(old) - new_content.count(old) for old in HREF_FIXES)
        
        print(f"✅ {slug}: {actual_src} src fixes, {actual_href} href fixes")
        total_src_fixes += actual_src
        total_href_fixes += actual_href
    else:
        print(f"   {slug}: no changes needed")

print(f"\nTotal: {total_src_fixes} src fixes, {total_href_fixes} href fixes")
