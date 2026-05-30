#!/usr/bin/env python3
"""
CFG-COPY-4 unconditional brand scrub — all competitor mentions in PDP body copy.
Applies to source files (Astro wrappers and static HTML).
"""
import re
from pathlib import Path

ROOT = Path('/home/ubuntu/alg-website-src')

# Brand → generic replacement map (order matters — longer patterns first)
REPLACEMENTS = [
    # Product-specific patterns (most specific first)
    (r'Lithonia DSX1 LED', 'category-leading area light'),
    (r'Lithonia DSX1', 'category-leading area light'),
    (r'Cooper Galleon', 'premium-tier competitor fixture'),
    (r'McGraw-Edison Galleon', 'premium-tier competitor fixture'),
    (r'Galleon', 'premium-tier competitor fixture'),
    (r'Cree XSP', 'PRO-tier competitor'),
    (r'XSP', 'PRO-tier competitor'),
    (r'RAB ALED 5S', 'competing post-top'),
    (r'RAB ALED', 'competing area light'),
    (r'ALED\b', 'competing area light'),
    (r'Cooper Belmont', 'competing post-top'),
    (r'Lithonia VCPGX nLight', 'category-leading area light'),
    (r'Lithonia VCPGX', 'category-leading area light'),
    (r'VCPGX\b', 'category-leading area light'),
    (r'Lithonia DPT D', 'category-leading post-top'),
    (r'DSX1 LED', 'category-leading area light'),
    (r'DSX1\b', 'category-leading area light'),
    (r'WaveLinx', 'competing controls platform'),
    (r'nLight AIR', 'competing controls platform'),
    (r'nLight\b', 'competing controls platform'),
    # Brand names alone
    (r'Lithonia\b', 'category-leading'),
    (r'Acuity\b', 'category-leading'),
    (r'Sternberg\b', 'category-leading'),
    (r'Lumec\b', 'category-leading'),
    (r'\bRAB\b', 'competing'),
    (r'\bCree\b', 'competing'),
    (r'\bCooper\b', 'competing'),
    # Other brands from the full list
    (r'NICOR\b', 'competing'),
    (r'Halo HLB\b', 'competing'),
    (r'Halo HLCE\b', 'competing'),
    (r'Halo\b', 'competing'),
    (r'\bLotus\b', 'competing'),
    (r'DMF DRD2\b', 'competing'),
    (r'DMF\b', 'competing'),
    (r'Keystone\b', 'competing'),
    (r'Parmida\b', 'competing'),
    (r'Signify\b', 'category-leading'),
    (r'Holophane\b', 'category-leading'),
    (r'Kim Archetype\b', 'competing'),
]

# Files to scrub (source files, not dist)
TARGET_FILES = [
    # Static HTML PDPs
    ROOT / 'public/products/lptp-symmetry-post-top/index.html',
    ROOT / 'public/products/liberty/index.html',
    ROOT / 'public/products/navigator/index.html',
    ROOT / 'public/products/radius-ii/index.html',
    ROOT / 'public/products/ecrescent/index.html',
    # Astro wrappers (luxoARCH)
    ROOT / 'src/pages/products/anaheim/index.astro',
    ROOT / 'src/pages/products/atlanta/index.astro',
    ROOT / 'src/pages/products/heritage/index.astro',
    ROOT / 'src/pages/products/nightwatch/index.astro',
    ROOT / 'src/pages/products/watchtower/index.astro',
    ROOT / 'src/pages/products/pathfinder/index.astro',
    ROOT / 'src/pages/products/ramparts/index.astro',
    ROOT / 'src/pages/products/guardian/index.astro',
    ROOT / 'src/pages/products/illuminator/index.astro',
    ROOT / 'src/pages/products/aura/index.astro',
    ROOT / 'src/pages/products/sentinel/index.astro',
    ROOT / 'src/pages/products/radiator/index.astro',
    ROOT / 'src/pages/products/everest/index.astro',
    ROOT / 'src/pages/products/luna/index.astro',
    ROOT / 'src/pages/products/lara/index.astro',
    ROOT / 'src/pages/products/waymark/index.astro',
    ROOT / 'src/pages/products/trackstar/index.astro',
    # Multi-family Astro wrappers
    ROOT / 'src/pages/products/multi-family/eclipse-ii/index.astro',
    ROOT / 'src/pages/products/multi-family/gehry/index.astro',
    ROOT / 'src/pages/products/multi-family/nebula-ii/index.astro',
    ROOT / 'src/pages/products/multi-family/orbit-i/index.astro',
    ROOT / 'src/pages/products/multi-family/radius-safezone/index.astro',
    ROOT / 'src/pages/products/multi-family/ecrescent/index.astro',
    ROOT / 'src/pages/products/multi-family/lunar-eclipse/index.astro',
    ROOT / 'src/pages/products/multi-family/radius-ii/index.astro',
    # planoARCH static HTML
    ROOT / 'public/products/astra/index.html',
    ROOT / 'public/products/spectra/index.html',
    ROOT / 'public/products/solstice/index.html',
    ROOT / 'public/products/solstice-safezone/index.html',
    ROOT / 'public/products/lara/index.html',
    ROOT / 'public/products/luna/index.html',
    ROOT / 'public/products/waymark/index.html',
    ROOT / 'public/products/trackstar/index.html',
    ROOT / 'public/products/luxmark/index.html',
    ROOT / 'public/products/proarch-t/index.html',
    ROOT / 'public/products/retroarch-p1/index.html',
    ROOT / 'public/products/retroarch-t1/index.html',
]

# Full brand pattern for scanning
SCAN_PATTERN = re.compile(
    r'Lithonia|Acuity|Cooper|RAB\b|Cree|DSX1|Galleon|XSP\b|NICOR|Halo HLB|Halo HLCE|'
    r'Lotus\b|DMF DRD2|DMF\b|Lumec|Sternberg|Keystone|Parmida|Signify|WaveLinx|VCPGX|'
    r'ALED\b|nLight|Holophane|Kim Archetype|McGraw-Edison'
)

def scrub_file(filepath: Path) -> int:
    """Scrub brand mentions from a file. Returns number of replacements made."""
    if not filepath.exists():
        return 0
    
    content = filepath.read_text(encoding='utf-8')
    original = content
    total_replacements = 0
    
    # Apply each replacement
    for pattern, replacement in REPLACEMENTS:
        new_content, count = re.subn(pattern, replacement, content)
        if count > 0:
            content = new_content
            total_replacements += count
    
    if content != original:
        filepath.write_text(content, encoding='utf-8')
    
    return total_replacements

def scan_for_remaining(filepath: Path) -> list:
    """Scan for any remaining brand mentions in visible HTML (outside scripts/comments)."""
    if not filepath.exists():
        return []
    
    content = filepath.read_text(encoding='utf-8')
    # Remove script blocks
    no_scripts = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    # Remove comments
    no_comments = re.sub(r'<!--.*?-->', '', no_scripts, flags=re.DOTALL)
    
    matches = SCAN_PATTERN.findall(no_comments)
    return matches

print("=== CFG-COPY-4 Unconditional Brand Scrub ===\n")

total_files_changed = 0
total_replacements = 0

for filepath in TARGET_FILES:
    if not filepath.exists():
        continue
    
    count = scrub_file(filepath)
    if count > 0:
        total_files_changed += 1
        total_replacements += count
        print(f"  {filepath.relative_to(ROOT)}: {count} replacements")

print(f"\nTotal: {total_replacements} replacements across {total_files_changed} files")

print("\n=== Post-scrub scan for remaining brand mentions ===")
# Only scan the 5 PDPs that had issues
priority_files = [
    ROOT / 'public/products/lptp-symmetry-post-top/index.html',
    ROOT / 'public/products/liberty/index.html',
    ROOT / 'public/products/navigator/index.html',
    ROOT / 'public/products/radius-ii/index.html',
    ROOT / 'public/products/ecrescent/index.html',
]

for filepath in priority_files:
    remaining = scan_for_remaining(filepath)
    if remaining:
        print(f"  WARN {filepath.parent.name}: {len(remaining)} remaining: {remaining[:10]}")
    else:
        print(f"  OK {filepath.parent.name}: 0 brand mentions")
