#!/usr/bin/env python3
"""
Patch C: CFG-COPY-4 unconditional brand scrub across all submittal HTML files.
Applies the same brand→generic mapping from cross_collection_sweep_v2.1.
"""
import re
from pathlib import Path

ROOT = Path('/home/ubuntu/alg-website-src')

# Brand → generic mapping (same as v2.1 Patch D)
REPLACEMENTS = [
    # Specific product names first (most specific → least specific)
    (r'Lithonia DSX1[-\s]?LED', 'category-leading area light'),
    (r'Lithonia DSX1', 'category-leading area light'),
    (r'DSX1[-\s]?LED', 'category-leading area light'),
    (r'DSX1\b', 'category-leading area light'),
    (r'Cooper Galleon', 'premium-tier competitor fixture'),
    (r'Cooper Navion', 'premium-tier competitor fixture'),
    (r'Cooper Belmont', 'premium-tier competitor fixture'),
    (r'Cooper\b', 'competing'),
    (r'Cree XSP', 'PRO-tier competitor'),
    (r'XSP\b', 'PRO-tier competitor'),
    (r'RAB ALED', 'competing area light'),
    (r'RAB WP3', 'competing wallpack'),
    (r'RAB TWR2', 'competing tower light'),
    (r'RAB\b', 'competing'),
    (r'ALED\b', 'competing area light'),
    (r'WaveLinx', 'competing controls platform'),
    (r'VCPGX\s*nLight', 'competing networked fixture'),
    (r'VCPGX', 'competing fixture'),
    (r'nLight\b', 'competing controls'),
    (r'Lithonia\b', 'category-leading'),
    (r'Acuity\b', 'category-leading'),
    (r'Lumec\b', 'category-leading'),
    (r'Sternberg\b', 'category-leading'),
    (r'Holophane\b', 'category-leading'),
    (r'McGraw-Edison\b', 'category-leading'),
    (r'Kim Archetype\b', 'category-leading'),
    (r'Cree\b', 'competing'),
    (r'Galleon\b', 'premium-tier competitor'),
    (r'NICOR\b', 'competing'),
    (r'Halo HLB\b', 'competing'),
    (r'Halo HLCE\b', 'competing'),
    (r'Lotus\b', 'competing'),
    (r'DMF DRD2\b', 'competing'),
    (r'DMF\b', 'competing'),
    (r'Keystone\b', 'competing'),
    (r'Parmida\b', 'competing'),
    (r'Signify\b', 'category-leading'),
    (r'Sylvania\b', 'competing'),
    (r'Philips\b', 'competing'),
    (r'Navion\b', 'premium-tier competitor'),
]

# Compile patterns
COMPILED = [(re.compile(pat), repl) for pat, repl in REPLACEMENTS]

# Scan pattern for verification
SCAN = re.compile(
    r'Lithonia|Acuity|Cooper|RAB\b|Cree|DSX1|Galleon|XSP\b|NICOR|Halo HLB|Halo HLCE|'
    r'Lotus\b|DMF DRD2|DMF\b|Lumec|Sternberg|Keystone|Parmida|Signify|WaveLinx|VCPGX|'
    r'ALED\b|nLight|Holophane|Kim Archetype|McGraw-Edison|Sylvania|Philips\b|Navion'
)

def scrub_html(content: str) -> tuple[str, int]:
    """Scrub brand mentions from visible HTML (not scripts or comments)."""
    # Split into segments: scripts, comments, and visible HTML
    # We need to scrub only visible HTML text, not JS data tables or HTML comments
    
    # Strategy: replace in full content but skip script blocks and HTML comments
    # Use a state machine approach
    result = []
    total_replacements = 0
    
    # Find all script blocks and HTML comments to preserve them
    preserve_ranges = []
    
    # HTML comments
    for m in re.finditer(r'<!--.*?-->', content, re.DOTALL):
        preserve_ranges.append((m.start(), m.end()))
    
    # Script blocks
    for m in re.finditer(r'<script[^>]*>.*?</script>', content, re.DOTALL):
        preserve_ranges.append((m.start(), m.end()))
    
    # Sort ranges
    preserve_ranges.sort()
    
    # Process content segment by segment
    pos = 0
    for start, end in preserve_ranges:
        # Process the segment before this preserved block
        segment = content[pos:start]
        for pattern, repl in COMPILED:
            new_segment, n = pattern.subn(repl, segment)
            total_replacements += n
            segment = new_segment
        result.append(segment)
        # Preserve the script/comment block unchanged
        result.append(content[start:end])
        pos = end
    
    # Process the remaining content after the last preserved block
    segment = content[pos:]
    for pattern, repl in COMPILED:
        new_segment, n = pattern.subn(repl, segment)
        total_replacements += n
        segment = new_segment
    result.append(segment)
    
    return ''.join(result), total_replacements


def main():
    submittal_files = sorted(ROOT.glob('public/products/*/submittal/index.html'))
    print(f"Found {len(submittal_files)} submittal files")
    
    total_files_changed = 0
    total_replacements = 0
    
    for f in submittal_files:
        slug = f.parts[-3]
        content = f.read_text(encoding='utf-8')
        
        # Quick check if any brands present
        no_scripts = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
        no_comments = re.sub(r'<!--.*?-->', '', no_scripts, flags=re.DOTALL)
        hits_before = len(SCAN.findall(no_comments))
        
        if hits_before == 0:
            continue
        
        new_content, n = scrub_html(content)
        
        if n > 0:
            f.write_text(new_content, encoding='utf-8')
            total_files_changed += 1
            total_replacements += n
            print(f"  Fixed {slug}: {n} replacements ({hits_before} brand hits)")
    
    print(f"\nTotal: {total_files_changed} files changed, {total_replacements} replacements")
    
    # Verify
    print("\n=== Verification ===")
    remaining = 0
    for f in submittal_files:
        slug = f.parts[-3]
        content = f.read_text(encoding='utf-8')
        no_scripts = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
        no_comments = re.sub(r'<!--.*?-->', '', no_scripts, flags=re.DOTALL)
        hits = SCAN.findall(no_comments)
        if hits:
            print(f"  WARN {slug}: {hits[:5]}")
            remaining += len(hits)
    if remaining == 0:
        print("  ✅ 0 brand mentions remaining in all submittal files")
    else:
        print(f"  ❌ {remaining} brand mentions still present")


if __name__ == '__main__':
    main()
