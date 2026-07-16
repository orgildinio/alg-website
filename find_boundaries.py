#!/usr/bin/env python3
import re

with open('public/products/trackstar/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find Solstice section start and end
print("=== Solstice section boundaries ===")
for i, line in enumerate(lines):
    if re.search(r'spotlight-section|15-in-1 Spotlight|SECTION.*Solstice|Solstice.*SECTION', line):
        print(f"  {i+1}: {line.rstrip()}")

# Find tier badge
print("\n=== Tier badge ===")
for i, line in enumerate(lines):
    if re.search(r'tier-badge|tier-eco|tier-pro', line):
        for j in range(max(0,i-1), min(len(lines),i+3)):
            print(f"  {j+1}: {lines[j].rstrip()}")
        print()

# Find spec-table footnote with NOTE:
print("\n=== Spec-table NOTE footnote ===")
for i, line in enumerate(lines):
    if 'NOTE:' in line and 'datasheet pg' in line:
        for j in range(max(0,i-2), min(len(lines),i+4)):
            print(f"  {j+1}: {lines[j].rstrip()}")
        print()

# Find "per Rebate Center · CFG-RBT-2" in rendered copy
print("\n=== per Rebate Center CFG-RBT-2 in rendered copy ===")
for i, line in enumerate(lines):
    if 'per Rebate Center' in line and 'CFG-RBT' in line:
        for j in range(max(0,i-1), min(len(lines),i+3)):
            print(f"  {j+1}: {lines[j].rstrip()}")
        print()

# Find TAA in rendered copy (not in comments)
print("\n=== TAA in rendered copy (not comments) ===")
for i, line in enumerate(lines):
    stripped = line.strip()
    if 'TAA' in line and not stripped.startswith('<!--') and not stripped.startswith('//') and not stripped.startswith('/*') and not stripped.startswith('*'):
        print(f"  {i+1}: {line.rstrip()}")

# Find hero chip row to locate TAA chip
print("\n=== Hero compliance row / cert badges ===")
for i, line in enumerate(lines):
    if re.search(r'hero-compliance|cert-badge|taa.*chip|TAA.*COMPLIANT', line, re.I):
        for j in range(max(0,i-1), min(len(lines),i+5)):
            print(f"  {j+1}: {lines[j].rstrip()}")
        print()

# Find the closing section H2 and family card nouns
print("\n=== Closing section H2 and family card descriptions ===")
for i, line in enumerate(lines):
    if re.search(r'closing-title|family-card-desc', line):
        for j in range(max(0,i-1), min(len(lines),i+5)):
            print(f"  {j+1}: {lines[j].rstrip()}")
        print()
