#!/usr/bin/env python3
import re

with open('public/products/trackstar/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    content = ''.join(lines)

def show_lines(label, pattern, context=2):
    print(f"\n=== {label} ===")
    for i, line in enumerate(lines):
        if re.search(pattern, line):
            start = max(0, i - context)
            end = min(len(lines), i + context + 1)
            for j in range(start, end):
                marker = ">>>" if j == i else "   "
                print(f"{marker} {j+1:5d}: {lines[j].rstrip()}")
            print()

# 1. TAA/BAA in rendered content (not in HTML/JS comments)
show_lines("TAA/BAA in rendered copy", r'TAA|BAA|Made.in.USA')

# 2. Internal notes
show_lines("Internal notes", r'CFG-|heads up:|NOTE:|datasheet pg|per Rebate Center')

# 3. Solstice section boundaries
show_lines("Solstice section start/end", r'SECTION.*Solstice|Solstice.*SECTION|15-in-1 Spotlight|spotlight-section|spotlight-picker')

# 4. Tier badge
show_lines("Tier badge", r'tier-badge|tier-eco|tier-pro')

# 5. Orphaned -tier fragments
show_lines("Orphaned -tier", r'\-tier ')

# 6. Family card truncated nouns
show_lines("Truncated family card nouns", r'Commercial \.')

# 7. Configurator compliance row
show_lines("Configurator compliance", r'compliance|Made in China|heads up')
