#!/usr/bin/env python3
"""
#90b sweeps:
1. Internal-note leak sweep: CFG-, heads up:, NOTE:, literal § in rendered copy
2. Cross-product SKU contamination matrix
"""

import os
import re
from pathlib import Path

PUBLIC = Path('public')
SRC = Path('src')

# All HTML files in public (rendered pages)
html_files = sorted(PUBLIC.rglob('*.html'))
# All Astro/TSX/JS files in src (source pages)
src_files = sorted(SRC.rglob('*.astro')) + sorted(SRC.rglob('*.tsx')) + sorted(SRC.rglob('*.ts'))

def is_in_comment(content, idx):
    """Check if position idx is inside an HTML comment <!-- ... -->"""
    # Find the last <!-- before idx
    last_open = content.rfind('<!--', 0, idx)
    if last_open == -1:
        return False
    # Find the next --> after that <!--
    next_close = content.find('-->', last_open)
    if next_close == -1:
        return True  # unclosed comment
    return next_close > idx

def is_in_script_or_style(content, idx):
    """Rough check: is position inside a <script> or <style> block?"""
    # Find last <script or <style before idx
    for tag in ['<script', '<style']:
        last_open = content.rfind(tag, 0, idx)
        if last_open != -1:
            close_tag = '</' + tag[1:]
            next_close = content.find(close_tag, last_open)
            if next_close > idx:
                return True
    return False

def get_context(lines, line_num, width=120):
    return lines[line_num].rstrip()[:width]

# ============================================================
# SWEEP 1: Internal-note leak patterns
# ============================================================
NOTE_PATTERNS = [
    (r'CFG-[A-Z]', 'CFG- internal ref'),
    (r'heads up:', 'heads up: note'),
    (r'\bNOTE:', 'NOTE: note'),
    (r'§\d+', 'literal §N section ref'),
]

print('=' * 80)
print('SWEEP 1: INTERNAL-NOTE LEAKS IN RENDERED COPY')
print('=' * 80)

sweep1_results = []

for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
        lines = content.splitlines()
    
    for pattern, label in NOTE_PATTERNS:
        for m in re.finditer(pattern, content):
            idx = m.start()
            in_comment = is_in_comment(content, idx)
            in_script = is_in_script_or_style(content, idx)
            line_num = content[:idx].count('\n')
            line_text = lines[line_num] if line_num < len(lines) else ''
            
            # Determine if rendered
            rendered = not in_comment and not in_script
            
            sweep1_results.append({
                'file': str(fpath),
                'line': line_num + 1,
                'pattern': label,
                'match': m.group(),
                'rendered': rendered,
                'context': line_text.strip()[:100],
            })

# Print results grouped by rendered status
rendered_leaks = [r for r in sweep1_results if r['rendered']]
comment_only = [r for r in sweep1_results if not r['rendered']]

print(f'\nRENDERED LEAKS (require fix): {len(rendered_leaks)}')
for r in rendered_leaks:
    print(f"  [{r['file']}:{r['line']}] {r['pattern']}: {r['context'][:100]}")

print(f'\nCOMMENT/SCRIPT ONLY (no fix needed): {len(comment_only)}')
# Group by file for brevity
from collections import defaultdict
by_file = defaultdict(list)
for r in comment_only:
    by_file[r['file']].append(r['pattern'])
for f, pats in sorted(by_file.items()):
    print(f"  {f}: {', '.join(set(pats))}")

# ============================================================
# SWEEP 2: Cross-product SKU contamination matrix
# ============================================================
print('\n' + '=' * 80)
print('SWEEP 2: CROSS-PRODUCT SKU CONTAMINATION MATRIX')
print('=' * 80)

# SKU prefix → owning product path
SKU_MAP = {
    'LTRK': 'trackstar',
    'LSPL': 'illuminator',
    'LCDL': 'solstice',
    'LCDL4': 'solstice',
    'LCDL6': 'solstice',
    'LCDL8': 'solstice',
    'LCDL10': 'solstice',
    'LLHB': 'titan',
    'LRHB': 'radiator',
    'LARA': 'lara',
    'LUNA': 'luna',
    'LTRK3W': 'trackstar',
    'LDRR': 'nebula-ii',
    'LMFP': 'gehry',
}

# Family name → owning product path
FAMILY_MAP = {
    'Trackstar': 'trackstar',
    'Illuminator': 'illuminator',
    'Solstice': 'solstice',
    'Titan': 'titan',
    'Radiator': 'radiator',
    'Lara': 'lara',
    'Luna': 'luna',
    'Nebula': 'nebula-ii',
    'Gehry': 'gehry',
    'Astra': 'astra',
    'Spectra': 'spectra',
    'Icarus': 'icarus',
    'Symmetry': 'symmetry',
    'retroⒶRCH': 'retroarch',
}

print('\nChecking each PDP for foreign SKU prefixes in body copy / spec / assets...')

contamination_hits = []

for fpath in html_files:
    # Determine owning product from path
    path_str = str(fpath)
    owner = None
    for sku, prod in SKU_MAP.items():
        if prod in path_str:
            owner = prod
            break
    if owner is None:
        # Try family map
        for name, prod in FAMILY_MAP.items():
            if prod in path_str:
                owner = prod
                break
    
    if owner is None:
        continue  # skip non-product pages
    
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
        lines = content.splitlines()
    
    # Check for foreign SKU prefixes
    for sku, prod in SKU_MAP.items():
        if prod == owner:
            continue  # skip own SKU
        
        pattern = r'\b' + re.escape(sku) + r'\d'
        for m in re.finditer(pattern, content):
            idx = m.start()
            in_comment = is_in_comment(content, idx)
            in_script = is_in_script_or_style(content, idx)
            line_num = content[:idx].count('\n')
            line_text = lines[line_num] if line_num < len(lines) else ''
            
            # Family/round-out cards are LEGIT — check if in family section
            in_family_section = 'family-card' in line_text or 'round-out' in line_text.lower() or 'family-section' in line_text
            
            contamination_hits.append({
                'file': str(fpath),
                'owner': owner,
                'foreign_sku': sku,
                'foreign_prod': prod,
                'line': line_num + 1,
                'rendered': not in_comment and not in_script,
                'in_family_card': in_family_section,
                'context': line_text.strip()[:100],
            })

# Report
actual_leaks = [h for h in contamination_hits if h['rendered'] and not h['in_family_card']]
legit_family = [h for h in contamination_hits if h['in_family_card']]
comment_hits = [h for h in contamination_hits if not h['rendered']]

print(f'\nACTUAL LEAKS (rendered, not in family cards): {len(actual_leaks)}')
for h in actual_leaks:
    print(f"  [{h['file']}:{h['line']}] {h['owner']} page has {h['foreign_sku']} ({h['foreign_prod']}): {h['context'][:90]}")

print(f'\nLEGIT family/round-out card references: {len(legit_family)}')
print(f'Comment-only hits: {len(comment_hits)}')

print('\nDone.')
