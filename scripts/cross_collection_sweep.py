#!/usr/bin/env python3
"""
cross_collection_sweep_v2.1 — Patches A through J
"""
import os, re, shutil
from pathlib import Path

ROOT = Path('/home/ubuntu/alg-website-src')
BUNDLE = Path('/home/ubuntu/upload/cross_collection_sweep_v2.1')

def read(p): return p.read_text(encoding='utf-8')
def write(p, t): p.write_text(t, encoding='utf-8')

changes = []

# ─── PATCH A: Abbey + OmniMax alias routes ──────────────────────────────────
# The PROMPT says lrdw-abbey-rectilinear-wall and lhmf-omnimax-i are broken.
# Repo has lrdw-abbey-roadway and lhmf-omnimax-high-mast (real content).
# Create redirect HTML pages for the old slugs.
print("=== Patch A: Abbey + OmniMax alias routes ===")

alias_pairs = [
    ('lrdw-abbey-rectilinear-wall', 'lrdw-abbey-roadway'),
    ('lhmf-omnimax-i', 'lhmf-omnimax-high-mast'),
]
for alias_slug, canonical_slug in alias_pairs:
    alias_dir = ROOT / 'public/products' / alias_slug
    alias_dir.mkdir(parents=True, exist_ok=True)
    alias_html = alias_dir / 'index.html'
    if not alias_html.exists():
        redirect_html = f'''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="0; url=/products/{canonical_slug}/">
  <link rel="canonical" href="/products/{canonical_slug}/">
  <title>Redirecting...</title>
</head>
<body>
  <p>Redirecting to <a href="/products/{canonical_slug}/">/products/{canonical_slug}/</a></p>
</body>
</html>
'''
        write(alias_html, redirect_html)
        print(f"  Created alias: {alias_slug} → {canonical_slug}")
        changes.append(f"Patch A: alias {alias_slug}")
    else:
        print(f"  Already exists: {alias_slug}")

# ─── PATCH B: Collection body class on all Astro wrappers ───────────────────
print("\n=== Patch B: Collection body class ===")

# Map: slug → collection prefix
COLLECTION_MAP = {
    # luxoARCH
    'heritage': 'luxoarch', 'anaheim': 'luxoarch', 'atlanta': 'luxoarch',
    'everest': 'luxoarch', 'guardian': 'luxoarch', 'liberty': 'luxoarch',
    'navigator': 'luxoarch', 'nightwatch': 'luxoarch', 'pathfinder': 'luxoarch',
    'radiator': 'luxoarch', 'ramparts': 'luxoarch', 'sentinel': 'luxoarch',
    'watchtower': 'luxoarch', 'wedge': 'luxoarch',
    # luxoARCH — with Astro wrappers
    'illuminator': 'luxoarch', 'aura': 'luxoarch',
    # planoARCH
    'astra': 'planoarch', 'spectra': 'planoarch', 'solstice': 'planoarch',
    'solstice-safezone': 'planoarch', 'lara': 'planoarch', 'luna': 'planoarch',
    'luxmark': 'planoarch', 'proarch-t': 'planoarch', 'trackstar': 'planoarch',
    'waymark': 'planoarch', 'retroarch-p1': 'planoarch', 'retroarch-t1': 'planoarch',
    'proarch': 'planoarch',
}

astro_products = ROOT / 'src/pages/products'
for slug, collection in COLLECTION_MAP.items():
    astro_file = astro_products / slug / 'index.astro'
    if not astro_file.exists():
        continue
    content = read(astro_file)
    # Find current bodyClass value
    m = re.search(r'bodyClass="([^"]*)"', content)
    if not m:
        print(f"  SKIP {slug}: no bodyClass found")
        continue
    current_class = m.group(1)
    collection_class = f'{collection}-pdp'
    if collection_class in current_class:
        print(f"  OK {slug}: already has {collection_class}")
        continue
    # Add collection class as prefix
    new_class = f'{collection_class} {current_class}'
    new_content = content.replace(f'bodyClass="{current_class}"', f'bodyClass="{new_class}"')
    if new_content != content:
        write(astro_file, new_content)
        print(f"  Fixed {slug}: '{current_class}' → '{new_class}'")
        changes.append(f"Patch B: {slug} bodyClass")
    else:
        print(f"  WARN {slug}: replace failed")

# ─── PATCH C1: Short slug refs in cityARCH static HTML ──────────────────────
print("\n=== Patch C1: Short slug refs in cityARCH PDPs ===")

SHORT_SLUG_MAP = {
    '/products/sentry/': '/products/lbol-sentry-bollard/',
    '/products/abbey/': '/products/lrdw-abbey-roadway/',
    '/products/omnimax/': '/products/lhmf-omnimax-high-mast/',
    '/products/symmetry/': '/products/lptp-symmetry-post-top/',
    '/products/unity/': '/products/lptp-unity-post-top/',
    '/products/lpar/': '/products/lpar-traffic-par38/',
    '/products/lyt10/': '/products/ly-t10-slimline-sign-lamp/',
    '/products/ly-t10/': '/products/ly-t10-slimline-sign-lamp/',
}

cityarch_slugs = [
    'lbol-sentry-bollard', 'lptp-symmetry-post-top', 'lptp-unity-post-top',
    'lpar-traffic-par38', 'ly-t10-slimline-sign-lamp', 'lrdw-abbey-roadway',
    'lhmf-omnimax-high-mast'
]
for slug in cityarch_slugs:
    html_file = ROOT / 'public/products' / slug / 'index.html'
    if not html_file.exists():
        continue
    content = read(html_file)
    new_content = content
    for short, canonical in SHORT_SLUG_MAP.items():
        new_content = new_content.replace(f'href="{short}"', f'href="{canonical}"')
    if new_content != content:
        write(html_file, new_content)
        print(f"  Fixed {slug}")
        changes.append(f"Patch C1: {slug}")
    else:
        print(f"  OK {slug}: no short slugs")

# ─── PATCH C2: proarch-t → proarch in cityARCH PDPs ─────────────────────────
print("\n=== Patch C2: proarch-t → proarch in cityARCH PDPs ===")

for slug in cityarch_slugs:
    html_file = ROOT / 'public/products' / slug / 'index.html'
    if not html_file.exists():
        continue
    content = read(html_file)
    new_content = content.replace('href="/products/proarch-t/"', 'href="/products/proarch/"')
    if new_content != content:
        write(html_file, new_content)
        count = content.count('href="/products/proarch-t/"')
        print(f"  Fixed {slug}: {count} refs")
        changes.append(f"Patch C2: {slug}")
    else:
        print(f"  OK {slug}: no proarch-t refs")

# ─── PATCH C3: Symmetry PRO → PRO+ fix in cityARCH PDPs ─────────────────────
# The PROMPT says Symmetry cards show PRO+ but should show PRO.
# Check the family card labels in cityARCH static HTML files.
print("\n=== Patch C3: Symmetry tier PRO+ → PRO in cityARCH PDPs ===")

for slug in cityarch_slugs:
    html_file = ROOT / 'public/products' / slug / 'index.html'
    if not html_file.exists():
        continue
    content = read(html_file)
    # Look for Symmetry card with PRO+ label
    # Pattern: near "symmetry" there's a tier-badge with PRO+
    new_content = re.sub(
        r'((?:SYMMETRY|symmetry)[^<]{0,200}?tier-badge[^>]*>)PRO\+',
        r'\1PRO',
        new_content if 'new_content' in dir() else content,
        flags=re.DOTALL
    )
    new_content = re.sub(
        r'(tier-badge[^>]*>[^<]{0,50}?(?:SYMMETRY|symmetry)[^<]{0,200}?)PRO\+',
        r'\1PRO',
        content,
        flags=re.DOTALL
    )
    # More targeted: find family card for symmetry and fix its tier text
    # The card structure: <a href="/products/lptp-symmetry-post-top/">...<span class="tier-badge...">PRO+</span>
    new_content = re.sub(
        r'(href="/products/lptp-symmetry-post-top/"[^<]{0,500}?<span[^>]*tier-badge[^>]*>)PRO\+',
        r'\1PRO',
        content,
        flags=re.DOTALL
    )
    if new_content != content:
        write(html_file, new_content)
        print(f"  Fixed {slug}: Symmetry PRO+ → PRO")
        changes.append(f"Patch C3: {slug}")
    else:
        print(f"  OK {slug}: no Symmetry PRO+ found")

# ─── PATCH D: Brand mention scrub from diff files ───────────────────────────
print("\n=== Patch D: Brand mention scrub ===")

diff_dir = BUNDLE / 'diffs'
scrubbed_dir = BUNDLE / 'source/mockups_scrubbed'

# Read each diff file and apply replacements
for diff_file in sorted(diff_dir.glob('*_brand_diff.md')):
    slug_name = diff_file.stem.replace('_brand_diff', '')
    print(f"  Processing diff: {slug_name}")
    diff_content = read(diff_file)
    
    # Parse the diff for find/replace pairs
    # Format: - old text (lines starting with -)
    #         + new text (lines starting with +)
    replacements = []
    lines = diff_content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('- ') and i + 1 < len(lines) and lines[i+1].startswith('+ '):
            old = line[2:].strip()
            new = lines[i+1][2:].strip()
            if old and new and old != new:
                replacements.append((old, new))
            i += 2
        else:
            i += 1
    
    if not replacements:
        print(f"    No replacements found in {diff_file.name}")
        continue
    
    # Find the target file
    # Try Astro wrapper first, then static HTML
    target_file = None
    for search_path in [
        ROOT / f'src/pages/products/{slug_name}/index.astro',
        ROOT / f'src/pages/products/multi-family/{slug_name}/index.astro',
        ROOT / f'public/products/{slug_name}/index.html',
        ROOT / f'public/products/multi-family/{slug_name}/index.html',
    ]:
        if search_path.exists():
            target_file = search_path
            break
    
    if not target_file:
        print(f"    WARN: No file found for {slug_name}")
        continue
    
    content = read(target_file)
    new_content = content
    applied = 0
    for old, new in replacements:
        if old in new_content:
            new_content = new_content.replace(old, new)
            applied += 1
    
    if new_content != content:
        write(target_file, new_content)
        print(f"    Applied {applied}/{len(replacements)} replacements to {target_file.name}")
        changes.append(f"Patch D: {slug_name}")
    else:
        print(f"    No changes needed for {slug_name} ({len(replacements)} pairs checked)")

# ─── PATCH E: submittal href fix in multi-family PDPs ───────────────────────
print("\n=== Patch E: submittal href fix in multi-family PDPs ===")

mf_slugs_abs = ['gehry', 'nebula-ii', 'radius-ii']  # orbit-i already has relative
for slug in mf_slugs_abs:
    astro_file = ROOT / f'src/pages/products/multi-family/{slug}/index.astro'
    if not astro_file.exists():
        continue
    content = read(astro_file)
    # Fix absolute CTA href to relative
    abs_pattern = f'href="/products/multi-family/{slug}/submittal/"'
    rel_pattern = 'href="submittal/"'
    new_content = content.replace(abs_pattern, rel_pattern)
    if new_content != content:
        write(astro_file, new_content)
        print(f"  Fixed {slug}: absolute → relative submittal href")
        changes.append(f"Patch E: {slug}")
    else:
        print(f"  OK {slug}: no absolute submittal href")

print(f"\n=== Patches A-E complete: {len(changes)} changes ===")
for c in changes:
    print(f"  {c}")
