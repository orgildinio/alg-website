#!/usr/bin/env python3
"""
hotfix #89c — purge competitor brand names from all customer-facing pages.
Files: luna, lara, retroarch-p1, retroarch-t1, trackstar
"""
import re, sys

def fix_file(path, replacements, label):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    orig = content
    applied = []
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            applied.append(f"  ✅ {repr(old[:80])} → {repr(new[:80])}")
        else:
            applied.append(f"  ⚠️  NOT FOUND: {repr(old[:80])}")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    changed = content != orig
    print(f"\n{'='*60}")
    print(f"{label} ({'CHANGED' if changed else 'NO CHANGE'})")
    for a in applied:
        print(a)
    return content

# ─── LUNA ────────────────────────────────────────────────────────────────────
luna_fixes = [
    # Hero narrative paragraph (line ~4378)
    (
        '<strong>35% higher than Finelite Series 19</strong> (140 LM/W). <strong>46% higher than competing ECO brands Linta</strong> (130 LM/W). <strong>2.4× higher than competing ECO brands BOA</strong> baseline (78 LM/W). The published-efficacy leader in the architectural-linear category — the single most-quoted spec on the Luna bid sheet.',
        '35% above the leading premium-tier architectural linear (140 LM/W). 46% above the typical architectural-linear baseline (130 LM/W). 2.4× the entry-tier baseline (78 LM/W). The published-efficacy leader in the architectural-linear category — the single most-quoted spec on the Luna bid sheet.'
    ),
    # Mount coverage paragraph (line ~4392)
    (
        'Finelite Series 19 ships pendant-only. competing ECO brands Linta is pendant-primarily. competing ECO brands BOA covers three mounts. <strong>Luna is the only volume-tier architectural linear with all four.</strong>',
        'Premium-tier peers ship pendant-only or cover two to three mount types. <strong>Luna is the only volume-tier architectural linear with all four.</strong>'
    ),
    # Optics paragraph (line ~4448)
    (
        'Finelite has fixed proprietary optics. competing ECO brands fixed PC diffuser. competing ECO brands 1-2 lens options. Luna leads on optical flexibility.',
        'Category peers ship fixed or single-swap optics. Luna leads on optical flexibility.'
    ),
    # SVG caption (line ~4500)
    (
        '<text x="240" y="340" text-anchor="middle" fill="rgba(255,255,255,0.5)" font-family="JetBrains Mono, monospace" font-size="9.5">competing ECO brands Linta = 3 modes · competing ECO brands BOA = 2 patterns · Finelite = fixed</text>',
        '<text x="240" y="340" text-anchor="middle" fill="rgba(255,255,255,0.5)" font-family="JetBrains Mono, monospace" font-size="9.5">typical category = 2–3 modes · Luna = 7 steps</text>'
    ),
    # Distribution paragraph (line ~4506)
    (
        '<strong>Luna gives seven steps. competing ECO brands gives three. competing ECO brands gives two. Finelite ships fixed.</strong> The finest distribution control in the spec-grade category.',
        '<strong>Luna gives seven steps. Typical category offerings run two to three modes. Premium-tier peers ship fixed ratios.</strong> The finest distribution control in the spec-grade category.'
    ),
    # CRI/UGR paragraph (line ~4517)
    (
        'Finelite charges premium for 90 CRI option. competing ECO brands doesn\'t publish CRI. competing ECO brands sits at 84-86. Neither competitor publishes UGR. Luna puts both numbers on the bid sheet.',
        'Category peers charge a premium for 90 CRI, omit CRI from datasheets, or publish 84–86. No category peer publishes UGR at the volume-spec tier. Luna puts both numbers on the bid sheet.'
    ),
    # Joiner SVG caption (line ~4564)
    (
        '<text x="240" y="340" text-anchor="middle" fill="rgba(255,255,255,0.5)" font-family="JetBrains Mono, monospace" font-size="9.5">competing ECO brands BOA = 600 W cap · competing ECO brands Linta = 3 shapes / 960 W · Luna = 6 shapes / 1,000 W</text>',
        '<text x="240" y="340" text-anchor="middle" fill="rgba(255,255,255,0.5)" font-family="JetBrains Mono, monospace" font-size="9.5">entry-tier = 600 W cap · mid-tier = 3 shapes / 960 W · Luna = 6 shapes / 1,000 W</text>'
    ),
    # Joiner paragraph (line ~4570)
    (
        'competing ECO brands Linta tops at three shapes (L/T/X) at 960 W. competing ECO brands BOA caps at 600 W with no joiner family. Luna delivers the richest joiner geometry in the spec-grade category.',
        'Mid-tier category peers top at three shapes (L/T/X) at 960 W. Entry-tier peers cap at 600 W with no joiner family. Luna delivers the richest joiner geometry in the spec-grade category.'
    ),
    # JS comment (line ~7698)
    (
        '// competitive positioning vs Finelite / competing ECO brands / competing ECO brands).',
        '// competitive positioning vs category peers — anonymous per CFG-COPY-4).'
    ),
    # JS narrative 1 (line ~7706)
    (
        "narrative: 'Spec-grade fit and finish. Slim 2.3\u2033 profile. The published-efficacy leader in the architectural-linear category \u2014 35% above Finelite Series 19, 46% above competing ECO brands Linta, 2.4\u00d7 above competing ECO brands BOA.'",
        "narrative: 'Spec-grade fit and finish. Slim 2.3\u2033 profile. The published-efficacy leader in the architectural-linear category \u2014 35% above the premium-tier baseline, 46% above the mid-tier baseline, 2.4\u00d7 above the entry-tier baseline.'"
    ),
    # JS narrative 2 (line ~7712)
    (
        "narrative: 'Finelite needs four product lines for what Luna does on one. competing ECO brands Linta is pendant-only. competing ECO brands BOA covers three. Luna covers four \u2014 including recessed trimless and flanged trim \u2014 from a single SKU platform.'",
        "narrative: 'Premium-tier peers need multiple product lines for what Luna does on one. Category peers cover one to three mount types. Luna covers four \u2014 including recessed trimless and flanged trim \u2014 from a single SKU platform.'"
    ),
    # JS narrative 3 (line ~7718)
    (
        "narrative: 'LUXA3 at 15W default \u00b7 2,850 lumens \u00b7 190 LM/W with the Diffuser optic. Datasheet-confirmed. Beats Finelite by 35%, competing ECO brands by 46%, competing ECO brands BOA basic by 144%.'",
        "narrative: 'LUXA3 at 15W default \u00b7 2,850 lumens \u00b7 190 LM/W with the Diffuser optic. Datasheet-confirmed. 35% above the premium-tier baseline, 46% above the mid-tier baseline, 144% above the entry-tier baseline.'"
    ),
    # JS narrative 4 (line ~7730)
    (
        "narrative: '100% down \u00b7 90/10 \u00b7 70/30 \u00b7 50/50 \u00b7 30/70 \u00b7 10/90 \u00b7 100% up. Luna gives seven steps. competing ECO brands gives three modes. competing ECO brands gives two patterns max. The specifier dials the right ratio per application.'",
        "narrative: '100% down \u00b7 90/10 \u00b7 70/30 \u00b7 50/50 \u00b7 30/70 \u00b7 10/90 \u00b7 100% up. Luna gives seven steps. Typical category offerings run two to three modes. The specifier dials the right ratio per application.'"
    ),
    # JS narrative 5 (line ~7742)
    (
        "narrative: 'Straight runs through corridors. L-corners around columns. T-branches off spines. X-crosses for grids. Y-joiners for 120\u00b0 atriums. V-joiners for variable-angle. Z-joiners for offsets. competing ECO brands caps at 600 W. competing ECO brands tops at 960 W with three shapes. Luna does 1,000 W with six.'",
        "narrative: 'Straight runs through corridors. L-corners around columns. T-branches off spines. X-crosses for grids. Y-joiners for 120\u00b0 atriums. V-joiners for variable-angle. Z-joiners for offsets. Entry-tier caps at 600 W. Mid-tier tops at 960 W with three shapes. Luna does 1,000 W with six.'"
    ),
    # Storyboard differentiator line (line ~4341)
    (
        '    differentiator \u2014 190 LM/W efficacy vs Finelite/competing ECO brands/competing ECO brands published numbers.',
        '    differentiator \u2014 190 LM/W efficacy vs category-peer published numbers.'
    ),
    # Storyboard clip 1 (line ~4344)
    (
        '      1 (HERO) 190 LM/W \u00b7 best-in-class           \u2014 vs Finelite 140 / competing ECO brands 130 / competing ECO brands 78 LM/W',
        '      1 (HERO) 190 LM/W \u00b7 best-in-class           \u2014 vs premium-tier 140 / mid-tier 130 / entry-tier 78 LM/W'
    ),
    # Storyboard comment (line ~4369)
    (
        '      <!-- HERO \u2014 190 LM/W best-in-class efficacy vs Finelite/competing ECO brands/competing ECO brands -->',
        '      <!-- HERO \u2014 190 LM/W best-in-class efficacy vs category peers -->'
    ),
    # Hero narrative intro sentence (line ~4337)
    (
        'the 190 LM/W efficacy that beats Finelite, competing ECO brands, and competing ECO brands, and continu',
        'the 190 LM/W efficacy that leads the architectural-linear category, and continu'
    ),
]

fix_file('public/products/luna/index.html', luna_fixes, 'LUNA')

# ─── LARA ────────────────────────────────────────────────────────────────────
lara_fixes = [
    (
        'category competitors publishes \u2018virtually seamless\u2019 with no measured cap.',
        'category competitors publish \u2018virtually seamless\u2019 claims with no measured cap.'
    ),
]
fix_file('public/products/lara/index.html', lara_fixes, 'LARA')

# ─── RETROARCH-P1 ────────────────────────────────────────────────────────────
# retroarch-p1 uses "category competitors" and "competing brands" — anonymize
with open('public/products/retroarch-p1/index.html', 'r', encoding='utf-8') as f:
    rp1 = f.read()

rp1_fixes = []
# Collect all unique occurrences
for m in re.finditer(r'competing brands [A-Za-z ]+|category competitors [A-Za-z ]*|Juno Trac-Master|Juno T283L|competing H-track|Juno \u00b7 competing \u00b7 Tech Element|Tech Lighting Element|WAC J-Spot|WAC\b|Stasis', rp1):
    pass  # just checking — will do regex replace below

rp1_orig = rp1
# Generic replacements for retroarch-p1
rp1 = re.sub(r'\bJuno Trac-Master\b', 'a leading J-track brand', rp1)
rp1 = re.sub(r'\bJuno T283L\b', 'J-track reference fixture', rp1)
rp1 = re.sub(r'\bJuno\b', 'leading J-track brand', rp1)
rp1 = re.sub(r'\bcompeting brands Stasis\b', 'a leading H-track brand', rp1)
rp1 = re.sub(r'\bcompeting brands\b', 'category peers', rp1)
rp1 = re.sub(r'\bcategory competitors\b', 'category peers', rp1)
rp1 = re.sub(r'\bTech Lighting Element\b', 'premium-tier track', rp1)
rp1 = re.sub(r'\bTech Lighting\b', 'premium-tier brands', rp1)
rp1 = re.sub(r'\bWAC J-Spot\b', 'WAC reference fixture', rp1)
rp1 = re.sub(r'\bWAC\b(?! reference)', 'a volume-spec peer', rp1)
rp1 = re.sub(r'\bStasis\b', 'H-track brand', rp1)
rp1 = re.sub(r'competing H-track', 'H-track', rp1)
with open('public/products/retroarch-p1/index.html', 'w', encoding='utf-8') as f:
    f.write(rp1)
print(f"\n{'='*60}")
print(f"RETROARCH-P1 ({'CHANGED' if rp1 != rp1_orig else 'NO CHANGE'})")

# ─── RETROARCH-T1 ────────────────────────────────────────────────────────────
with open('public/products/retroarch-t1/index.html', 'r', encoding='utf-8') as f:
    rt1 = f.read()
rt1_orig = rt1
rt1 = re.sub(r'\bJuno Trac-Master\b', 'a leading J-track brand', rt1)
rt1 = re.sub(r'\bJuno T283L\b', 'J-track reference fixture', rt1)
rt1 = re.sub(r'\bJuno\b', 'leading J-track brand', rt1)
rt1 = re.sub(r'\bcompeting brands Stasis\b', 'a leading H-track brand', rt1)
rt1 = re.sub(r'\bcompeting brands\b', 'category peers', rt1)
rt1 = re.sub(r'\bcategory competitors\b', 'category peers', rt1)
rt1 = re.sub(r'\bTech Lighting Element\b', 'premium-tier track', rt1)
rt1 = re.sub(r'\bTech Lighting\b', 'premium-tier brands', rt1)
rt1 = re.sub(r'\bWAC J-Spot\b', 'WAC reference fixture', rt1)
rt1 = re.sub(r'\bWAC\b(?! reference)', 'a volume-spec peer', rt1)
rt1 = re.sub(r'\bStasis\b', 'H-track brand', rt1)
rt1 = re.sub(r'competing H-track', 'H-track', rt1)
with open('public/products/retroarch-t1/index.html', 'w', encoding='utf-8') as f:
    f.write(rt1)
print(f"\n{'='*60}")
print(f"RETROARCH-T1 ({'CHANGED' if rt1 != rt1_orig else 'NO CHANGE'})")

# ─── TRACKSTAR ───────────────────────────────────────────────────────────────
with open('public/products/trackstar/index.html', 'r', encoding='utf-8') as f:
    ts = f.read()
ts_orig = ts
ts = re.sub(r'\bJuno Trac-Master\b', 'a leading J-track brand', ts)
ts = re.sub(r'\bJuno T283L\b', 'J-track reference fixture', ts)
ts = re.sub(r'\bJuno\b', 'leading J-track brand', ts)
ts = re.sub(r'\bcompeting brands Stasis\b', 'a leading H-track brand', ts)
ts = re.sub(r'\bcompeting brands\b', 'category peers', ts)
ts = re.sub(r'\bcategory competitors\b', 'category peers', ts)
ts = re.sub(r'\bTech Lighting Element\b', 'premium-tier track', ts)
ts = re.sub(r'\bTech Lighting\b', 'premium-tier brands', ts)
ts = re.sub(r'\bWAC J-Spot\b', 'a volume-spec reference fixture', ts)
ts = re.sub(r'\bWAC\b(?! reference)', 'a volume-spec peer', ts)
ts = re.sub(r'\bStasis\b', 'H-track brand', ts)
ts = re.sub(r'competing H-track', 'H-track', ts)
with open('public/products/trackstar/index.html', 'w', encoding='utf-8') as f:
    f.write(ts)
print(f"\n{'='*60}")
print(f"TRACKSTAR ({'CHANGED' if ts != ts_orig else 'NO CHANGE'})")

# ─── FINAL VERIFICATION SWEEP ────────────────────────────────────────────────
print(f"\n{'='*60}")
print("FINAL VERIFICATION SWEEP")
targets = ['Finelite', 'Linta', r'\bBOA\b', 'competing ECO brands', r'\bJuno\b', r'\bStasis\b', r'\bWAC\b']
files = {
    'luna': 'public/products/luna/index.html',
    'lara': 'public/products/lara/index.html',
    'retroarch-p1': 'public/products/retroarch-p1/index.html',
    'retroarch-t1': 'public/products/retroarch-t1/index.html',
    'trackstar': 'public/products/trackstar/index.html',
}
all_clean = True
for fname, fpath in files.items():
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()
    hits = []
    for t in targets:
        ms = list(re.finditer(t, c))
        if ms:
            hits.append(f"{t}×{len(ms)}")
    if hits:
        print(f"  ❌ {fname}: {', '.join(hits)}")
        all_clean = False
    else:
        print(f"  ✅ {fname}: CLEAN")

if all_clean:
    print("\nALL FILES CLEAN — ready to commit")
else:
    print("\nRESIDUES REMAIN — do not commit")
    sys.exit(1)
