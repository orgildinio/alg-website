#!/usr/bin/env python3
"""
Patch D: Brand mention scrub — parse Markdown table diffs and apply to source files.
"""
import re
from pathlib import Path

ROOT = Path('/home/ubuntu/alg-website-src')
BUNDLE = Path('/home/ubuntu/upload/cross_collection_sweep_v2.1')
diff_dir = BUNDLE / 'diffs'

def read(p): return p.read_text(encoding='utf-8')
def write(p, t): p.write_text(t, encoding='utf-8')

total_changes = 0

for diff_file in sorted(diff_dir.glob('*_brand_diff.md')):
    slug_name = diff_file.stem.replace('_brand_diff', '')
    diff_content = read(diff_file)
    
    # Parse Markdown table rows: | line | Before | After |
    # Skip header rows
    replacements = []
    for line in diff_content.split('\n'):
        line = line.strip()
        if not line.startswith('|') or '---' in line or 'Before' in line:
            continue
        parts = [p.strip() for p in line.split('|')]
        parts = [p for p in parts if p]  # remove empty
        if len(parts) >= 3:
            before = parts[1].strip('`')
            after = parts[2].strip('`')
            if before and after and before != after:
                replacements.append((before, after))
    
    if not replacements:
        print(f"  {slug_name}: no replacements parsed")
        continue
    
    print(f"  {slug_name}: {len(replacements)} replacements to apply")
    
    # Find the target file — try multiple locations
    target_file = None
    for search_path in [
        ROOT / f'src/pages/products/{slug_name}/index.astro',
        ROOT / f'src/pages/products/multi-family/{slug_name}/index.astro',
        ROOT / f'public/products/{slug_name}/index.html',
        ROOT / f'public/products/multi-family/{slug_name}/index.html',
        ROOT / f'public/products/lptp-symmetry-post-top/index.html',  # symmetry special case
    ]:
        if search_path.exists():
            target_file = search_path
            break
    
    # Special case for symmetry (slug in diff is 'symmetry' but file is lptp-symmetry-post-top)
    if slug_name == 'symmetry' and not target_file:
        target_file = ROOT / 'public/products/lptp-symmetry-post-top/index.html'
    
    if not target_file or not target_file.exists():
        print(f"    WARN: No file found for {slug_name}")
        continue
    
    content = read(target_file)
    new_content = content
    applied = 0
    skipped = 0
    
    for before, after in replacements:
        # The ║ prefix means this is inside an HTML comment block
        # Strip the ║ prefix for matching
        before_clean = before.lstrip('║ ').strip()
        after_clean = after.lstrip('║ ').strip()
        
        if before_clean in new_content:
            new_content = new_content.replace(before_clean, after_clean)
            applied += 1
        else:
            skipped += 1
            # Try with the ║ prefix intact
            if before in new_content:
                new_content = new_content.replace(before, after)
                applied += 1
                skipped -= 1
    
    if new_content != content:
        write(target_file, new_content)
        print(f"    Applied {applied}/{len(replacements)} to {target_file.relative_to(ROOT)}")
        total_changes += applied
    else:
        print(f"    No changes (applied={applied}, skipped={skipped})")
        # Show first few that didn't match
        for before, after in replacements[:3]:
            before_clean = before.lstrip('║ ').strip()
            print(f"      NOT FOUND: '{before_clean[:60]}...'")

print(f"\nTotal brand replacements applied: {total_changes}")
