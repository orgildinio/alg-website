#!/usr/bin/env python3
"""
hotfix #89e — authored sentence rewrites only.
No global find-replace. Each replacement is a specific, verified string
mapped to a clean English rewrite reviewed by a spec-writer.
"""
import re, sys

def apply(path, label, changes):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    orig = c
    for old, new, note in changes:
        if old in c:
            c = c.replace(old, new, 1)
            print(f"  ✅ {label}: {note}")
        else:
            print(f"  ⚠️  NOT FOUND in {label}: {note}")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    return c != orig


# ─── RETROARCH-P1 ────────────────────────────────────────────────────────────
# The lock-out block has THREE SVG text lines:
#   line 1: "Lock-out competitors:"                         ← label, keep
#   line 2: "China-direct category imports (BAA + TAA blocked)"  ← main value
#   line 3: "(China-direct · BAA + TAA blocked)"            ← orphaned duplicate, DELETE
#
# Fix: collapse to two clean lines.
#   line 1: "Lock-out:" (shorter label)
#   line 2: "China-direct imports · BAA + TAA blocked"
#   line 3: REMOVE entirely

p1_changes = [
    (
        '<text x="0" y="166" fill="rgba(255,255,255,0.55)" font-size="8">Lock-out competitors:</text>\n              <text x="0" y="180" fill="#ffc457" font-size="9" font-weight="700">China-direct category imports (BAA + TAA blocked)</text>\n              <text x="0" y="192" fill="rgba(255,255,255,0.4)" font-size="7.5">(China-direct · BAA + TAA blocked)</text>',
        '<text x="0" y="166" fill="rgba(255,255,255,0.55)" font-size="8">Lock-out:</text>\n              <text x="0" y="180" fill="#ffc457" font-size="9" font-weight="700">China-direct imports · BAA + TAA blocked</text>',
        'SVG lock-out caption: collapsed to 2 clean lines, removed doubled parenthetical'
    ),
]
apply('public/products/retroarch-p1/index.html', 'retroarch-p1', p1_changes)


# ─── RETROARCH-T1 ────────────────────────────────────────────────────────────
# Same shared panel pattern — same fix.
t1_changes = [
    (
        '<text x="0" y="166" fill="rgba(255,255,255,0.55)" font-size="8">Lock-out competitors:</text>\n              <text x="0" y="180" fill="#ffc457" font-size="9" font-weight="700">China-direct category imports (BAA + TAA blocked)</text>\n              <text x="0" y="192" fill="rgba(255,255,255,0.4)" font-size="7.5">(China-direct · BAA + TAA blocked)</text>',
        '<text x="0" y="166" fill="rgba(255,255,255,0.55)" font-size="8">Lock-out:</text>\n              <text x="0" y="180" fill="#ffc457" font-size="9" font-weight="700">China-direct imports · BAA + TAA blocked</text>',
        'SVG lock-out caption: collapsed to 2 clean lines, removed doubled parenthetical'
    ),
]
apply('public/products/retroarch-t1/index.html', 'retroarch-t1', t1_changes)


# ─── TRACKSTAR ───────────────────────────────────────────────────────────────
# Multiple damaged sentences. Each is rewritten as clean spec-writer English.

ts_changes = [
    # 1. Main trackADAPT body paragraph (line ~4922)
    # Damaged: "a leading H-track brand fits H-track only. a leading J-track brand fits J-track only.
    #           category peers ships separate part numbers per track standard (W / H / J / L).
    #           Trackstar's interchangeable trackⒶDAPT base mounts to H-Type (H-track 1-circuit)
    #           and J-Type (a leading J-track brand 1-circuit) infrastructure from a single catalog SKU."
    (
        '<strong>a leading H-track brand fits H-track only. a leading J-track brand fits J-track only.</strong> category peers ships separate part numbers per track standard (W / H / J / L). Trackstar\'s interchangeable track<span class="aa">\u24b6</span>DAPT base mounts to <strong>H-Type (H-track 1-circuit) and J-Type (a leading J-track brand 1-circuit)</strong> infrastructure from a single catalog SKU.',
        '<strong>Most track heads fit a single standard — H-track or J-track only — and category peers ship separate part numbers per standard (W / H / J / L).</strong> Trackstar\'s interchangeable track<span class="aa">\u24b6</span>DAPT base mounts to <strong>H-Type and J-Type single-circuit track infrastructure</strong> from a single catalog SKU.',
        'trackADAPT body paragraph: rewritten as clean spec English, removed orphaned brand fragments'
    ),
    # 2. SVG caption line ~4916
    # Damaged: "a leading H-track brand = H only · a leading J-track brand = J only · a volume-spec peer = separate SKUs per standard"
    (
        '<text x="240" y="328" text-anchor="middle" fill="rgba(255,255,255,0.55)" font-family="JetBrains Mono, monospace" font-size="9.5">a leading H-track brand = H only · a leading J-track brand = J only · a volume-spec peer = separate SKUs per standard</text>',
        '<text x="240" y="328" text-anchor="middle" fill="rgba(255,255,255,0.55)" font-family="JetBrains Mono, monospace" font-size="9.5">H-track heads = H only · J-track heads = J only · Trackstar = both from one SKU</text>',
        'SVG caption line 4916: rewritten to anonymous, clean, parallel structure'
    ),
    # 3. SVG aria-label (line ~4881) — "J-Type for a leading J-track brand 1-circuit infrastructure"
    (
        'J-Type for a leading J-track brand 1-circuit infrastructure on the bottom right',
        'J-Type for J-track 1-circuit infrastructure on the bottom right',
        'SVG aria-label line 4881: removed orphaned brand fragment'
    ),
    # 4. SVG text label line ~4913 — "a leading J-track brand · 1-circuit"
    (
        '<text x="0" y="40" text-anchor="middle" fill="rgba(255,255,255,0.7)" font-family="JetBrains Mono, monospace" font-size="9">a leading J-track brand · 1-circuit</text>',
        '<text x="0" y="40" text-anchor="middle" fill="rgba(255,255,255,0.7)" font-family="JetBrains Mono, monospace" font-size="9">J-Type · 1-circuit</text>',
        'SVG label line 4913: "a leading J-track brand · 1-circuit" → "J-Type · 1-circuit"'
    ),
    # 5. Unique-positioning paragraph (line ~4861)
    # Damaged: "a leading J-track brand forks single-CCT + fixed beam per part number.
    #           a leading H-track brand is 2-CCT (3000K + 4000K) + 3 fixed beams.
    #           category peers splits the three properties across separate families."
    (
        'a leading J-track brand forks single-CCT + fixed beam per part number. a leading H-track brand is 2-CCT (3000K + 4000K) + 3 fixed beams. category peers splits the three properties across separate families.',
        'J-track category peers fork single-CCT and fixed-beam options across separate part numbers. H-track category peers offer 2-CCT with 3 fixed beams. Volume-spec peers split the three properties across separate product families.',
        'Unique-positioning paragraph line 4861: rewritten, subjects agree with verbs, no orphaned brand fragments'
    ),
    # 6. CRI paragraph (line ~4875)
    # Damaged: "a leading J-track brand, a leading H-track brand, and category peers ship CRI 80..."
    (
        'a leading J-track brand, a leading H-track brand, and category peers ship <strong>CRI 80 at the volume-spec tier</strong>',
        'J-track and H-track category peers ship <strong>CRI 80 at the volume-spec tier</strong>',
        'CRI paragraph line 4875: rewritten, removed orphaned brand fragments'
    ),
    # 7. Damp-location paragraph (line ~5001)
    # Damaged: "a leading J-track brand, a leading H-track brand, and premium-tier track are dry-location only..."
    (
        '<strong>a leading J-track brand, a leading H-track brand, and premium-tier track are dry-location only at the spec-grade tier.</strong>',
        '<strong>J-track and H-track category peers, including premium-tier track, are dry-location only at the spec-grade tier.</strong>',
        'Damp-location paragraph line 5001: rewritten, removed orphaned brand fragments'
    ),
    # 8. SVG caption line ~4995
    # Damaged: "leading J-track brand · competing · Tech Element = dry location only at spec-grade tier"
    (
        '<text x="240" y="338" text-anchor="middle" fill="rgba(255,255,255,0.55)" font-family="JetBrains Mono, monospace" font-size="9">leading J-track brand · competing · Tech Element = dry location only at spec-grade tier</text>',
        '<text x="240" y="338" text-anchor="middle" fill="rgba(255,255,255,0.55)" font-family="JetBrains Mono, monospace" font-size="9">category peers = dry location only at spec-grade tier · Trackstar = damp rated standard</text>',
        'SVG caption line 4995: rewritten as clean parallel structure'
    ),
    # 9. JS hj narrative (line ~6784)
    # Damaged: "a leading H-track brand fits H only · a leading J-track brand fits J only · category peers ships separate part numbers per track standard"
    (
        'a leading H-track brand fits H only \u00b7 a leading J-track brand fits J only \u00b7 category peers ships separate part numbers per track standard',
        'H-track heads fit H only \u00b7 J-track heads fit J only \u00b7 category peers ship separate part numbers per standard',
        'JS hj narrative line 6784: rewritten, verb agreement fixed'
    ),
    # 10. JS hj narrative — "J-Type (a leading J-track brand 1-circuit) infrastructure"
    (
        'J-Type (a leading J-track brand 1-circuit) infrastructure on the same head SKU.',
        'J-Type (J-track 1-circuit) infrastructure on the same head SKU.',
        'JS hj narrative: removed orphaned brand fragment from J-Type parenthetical'
    ),
    # 11. Storyboard clip 02 text (line ~7589)
    # Damaged: "trackⒶDAPT mounts to H-Type (H-track) and J-Type (a leading J-track brand) infrastructure...
    #           H-track brand fits H only. a leading J-track brand fits J only.
    #           a volume-spec peer ships separate part numbers per track standard."
    (
        'trackⒶDAPT mounts to H-Type (H-track) and J-Type (a leading J-track brand) infrastructure from a single head SKU. H-track brand fits H only. a leading J-track brand fits J only. a volume-spec peer ships separate part numbers per track standard.',
        'trackⒶDAPT mounts to H-Type and J-Type single-circuit track infrastructure from a single head SKU. H-track heads fit H only; J-track heads fit J only. Category peers ship separate part numbers per track standard.',
        'Storyboard clip 02 text: rewritten as clean spec English, semicolon for parallel list'
    ),
    # 12. Second SVG aria-label (line ~5184)
    (
        'J-Type for a leading J-track brand infrastructure on the right',
        'J-Type for J-track infrastructure on the right',
        'Second SVG aria-label line 5184: removed orphaned brand fragment'
    ),
    # 13. Second SVG J-Type label (line ~5219)
    (
        '<text x="275" y="270" text-anchor="middle" fill="rgba(255,255,255,0.7)" font-family="JetBrains Mono, monospace" font-size="9">a leading J-track brand</text>',
        '<text x="275" y="270" text-anchor="middle" fill="rgba(255,255,255,0.7)" font-family="JetBrains Mono, monospace" font-size="9">J-Type · 1-circuit</text>',
        'Second SVG J-Type label line 5219: "a leading J-track brand" → "J-Type · 1-circuit"'
    ),
]
apply('public/products/trackstar/index.html', 'trackstar', ts_changes)


# ─── FINAL VERIFICATION ───────────────────────────────────────────────────────
print('\n' + '='*60)
print('FINAL VERIFICATION SWEEP')
checks = {
    'retroarch-p1': 'public/products/retroarch-p1/index.html',
    'retroarch-t1': 'public/products/retroarch-t1/index.html',
    'trackstar':    'public/products/trackstar/index.html',
}
patterns = [
    (r'Forest', 'Forest'),
    (r'category peers \u00b7 ', 'category peers · (dup separator)'),
    (r'\)\s*\(', ')(  (doubled parenthetical)'),
    (r'a leading [A-Za-z-]+ brand [A-Za-z]', 'orphaned "a leading X brand" mid-sentence'),
    (r'Finelite|Linta|\bBOA\b|Juno|Stasis|Tech Lighting|\bWAC\b', 'competitor name'),
]
all_clean = True
for label, path in checks.items():
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    hits = []
    for pat, desc in patterns:
        ms = list(re.finditer(pat, c))
        if ms:
            hits.append(f"{desc}×{len(ms)}")
    if hits:
        print(f'  ❌ {label}: {", ".join(hits)}')
        all_clean = False
    else:
        print(f'  ✅ {label}: CLEAN')

if not all_clean:
    sys.exit(1)
print('\nALL CLEAN — ready to commit')
