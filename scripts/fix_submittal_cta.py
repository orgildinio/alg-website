"""
submittal_cta_sweep_v2 · Bug A
Replace all submittal_{slug}.html patterns with submittal/ in PDP source files.
Applies to both static href= attributes and JS template literals.
"""
import re, os

# Per-file edit table from PROMPT §C
EDITS = [
    ('public/products/trackstar/index.html', ['trackstar']),
    ('public/products/astra/index.html', ['astra']),
    ('public/products/spectra/index.html', ['spectra']),
    ('public/products/solstice/index.html', ['solstice']),
    ('public/products/solstice-safezone/index.html', ['solstice-safezone', 'safezone']),
    ('public/products/luxmark/index.html', ['luxmark']),
    ('public/products/proarch-t/index.html', ['proarch_t1_t2', 'proarch-t']),
    ('public/products/lara/index.html', ['lara']),
    ('public/products/luna/index.html', ['luna']),
    ('public/products/waymark/index.html', ['waymark']),
    ('public/products/retroarch-p1/index.html', ['retroarch_p1', 'retroarch-p1']),
    ('public/products/retroarch-t1/index.html', ['retroarch_t1', 'retroarch-t1']),
    # luxoARCH — these use submittal_template.html
    ('public/products/illuminator/index.html', ['illuminator', 'template']),
    ('public/products/anaheim/index.html', ['anaheim', 'template']),
    ('public/products/atlanta/index.html', ['atlanta', 'template']),
    ('public/products/aura/index.html', ['aura', 'template']),
    ('public/products/everest/index.html', ['everest', 'template']),
    ('public/products/guardian/index.html', ['guardian', 'template']),
    ('public/products/heritage/index.html', ['heritage', 'template']),
    ('public/products/liberty/index.html', ['liberty', 'template']),
    ('public/products/navigator/index.html', ['navigator', 'template']),
    ('public/products/nightwatch/index.html', ['nightwatch', 'template']),
    ('public/products/pathfinder/index.html', ['pathfinder', 'template']),
    ('public/products/radiator/index.html', ['radiator', 'template']),
    ('public/products/ramparts/index.html', ['ramparts', 'template']),
    ('public/products/sentinel/index.html', ['sentinel', 'template']),
    ('public/products/watchtower/index.html', ['watchtower', 'template']),
    ('public/products/wedge/index.html', ['wedge', 'template']),
    # cityARCH
    ('public/products/lbol-sentry-bollard/index.html', ['sentry']),
    ('public/products/lrdw-abbey-rectilinear-wall/index.html', ['abbey']),
    ('public/products/lhmf-omnimax-high-mast/index.html', ['omnimax']),
    ('public/products/lptp-symmetry-post-top/index.html', ['symmetry']),
    ('public/products/lptp-unity-post-top/index.html', ['unity']),
    ('public/products/lpar-traffic-par38/index.html', ['lpar']),
    ('public/products/ly-t10-slimline-sign-lamp/index.html', ['lyt10', 'ly-t10']),
    # multi-family
    ('public/products/multi-family/gehry/index.html', ['gehry']),
    ('public/products/multi-family/nebula-ii/index.html', ['nebula-ii']),
    ('public/products/multi-family/orbit-i/index.html', ['orbit']),
    ('public/products/multi-family/radius-ii/index.html', ['radius-ii']),
    ('public/products/multi-family/radius-safezone/index.html', ['radius-safezone']),
    ('public/products/multi-family/ecrescent/index.html', ['ecrescent']),
    ('public/products/multi-family/eclipse-ii/index.html', ['eclipse-ii']),
    ('public/products/multi-family/lunar-eclipse/index.html', ['lunar-eclipse']),
]

total_fixed = 0
not_found = []
skipped = []

for fpath, slugs in EDITS:
    if not os.path.exists(fpath):
        skipped.append(fpath)
        continue
    
    with open(fpath) as f:
        content = f.read()
    
    original = content
    file_fixes = 0
    
    for slug in slugs:
        pattern = f'submittal_{slug}.html'
        if pattern in content:
            count = content.count(pattern)
            content = content.replace(pattern, 'submittal/')
            file_fixes += count
    
    if content != original:
        with open(fpath, 'w') as f:
            f.write(content)
        print(f"  ✅ {fpath}: {file_fixes} replacement(s)")
        total_fixed += 1
    else:
        # Check if old pattern still exists
        old_hits = re.findall(r'submittal_[a-z0-9_-]+\.html', content)
        if old_hits:
            not_found.append((fpath, old_hits))
            print(f"  ⚠️  {fpath}: UNMATCHED old patterns: {old_hits}")
        else:
            print(f"  ✓  {fpath}: already clean (no old patterns)")

if skipped:
    print(f"\nSkipped (file not found):")
    for f in skipped:
        print(f"  {f}")

if not_found:
    print(f"\nFiles with unmatched old patterns (surface to James):")
    for f, hits in not_found:
        print(f"  {f}: {hits}")

print(f"\nTotal files modified: {total_fixed}")
