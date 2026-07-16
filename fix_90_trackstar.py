#!/usr/bin/env python3
"""
hotfix #90 — Trackstar: 4 defect groups
1. Remove false TAA COMPLIANT chip from hero feature-chips row
2. Remove leaked internal notes from rendered copy (spec-table footnote NOTE:, photometrics CFG-RBT-2, configurator compliance row)
3. Delete stray Solstice section (lines 4674-4785, including the preceding comment)
4. Rewrite orphaned -tier fragments, truncated family-card nouns, tier badge ECO→PRO
"""

import re

with open('public/products/trackstar/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = []

# ============================================================
# FIX 1: Remove TAA COMPLIANT feature chip
# The chip is a <div class="feature-chip">...</div> block ending with "TAA COMPLIANT"
# ============================================================
taa_chip = '''<div class="feature-chip">
 <div class="feature-chip-icon">
 <svg viewBox="0 0 60 60" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
 <circle cx="30" cy="30" r="26" stroke-width="1.4" opacity="0.35"/>
 <line x1="20" y1="14" x2="20" y2="46"/>
 <path d="M20 16 Q30 18 40 16 Q40 22 40 28 Q30 30 20 28 Z" fill="#F32740" stroke="#F32740"/>
 <circle cx="26" cy="22" r="0.9" fill="#ffffff" stroke="none"/>
 <circle cx="32" cy="22" r="0.9" fill="#ffffff" stroke="none"/>
 <circle cx="38" cy="22" r="0.9" fill="#ffffff" stroke="none"/>
 </svg>
 </div>
 <div class="feature-chip-label">TAA COMPLIANT</div>
 </div>'''

if taa_chip in content:
    content = content.replace(taa_chip, '', 1)
    changes.append('✅ FIX 1: TAA COMPLIANT hero chip removed')
else:
    changes.append('❌ FIX 1: TAA chip not found — check manually')

# ============================================================
# FIX 2a: Spec-table footnote — remove NOTE: sentence
# Keep everything before "NOTE:" and drop the rest of that sentence
# ============================================================
old_footnote = 'Voltage 120V · &gt;0.9 PF · TRIAC + Phase Dim. NOTE: datasheet pg 1 prose says "120-277V" but pg 2 spec list canonical = 120V — pg 2 spec list wins per CFG-RBT-2 datasheet hierarchy.'
new_footnote = 'Voltage 120V · &gt;0.9 PF · TRIAC + Phase Dim.'

if old_footnote in content:
    content = content.replace(old_footnote, new_footnote, 1)
    changes.append('✅ FIX 2a: Spec-table NOTE: footnote removed')
else:
    changes.append('❌ FIX 2a: Spec-table NOTE not found — check manually')

# ============================================================
# FIX 2b: Photometrics stat sub — remove "(per Rebate Center · CFG-RBT-2)"
# ============================================================
old_photo = '<strong>DLC Listed</strong> (per Rebate Center · CFG-RBT-2).'
new_photo = '<strong>DLC Listed</strong>.'

if old_photo in content:
    content = content.replace(old_photo, new_photo, 1)
    changes.append('✅ FIX 2b: Photometrics CFG-RBT-2 parenthetical removed')
else:
    changes.append('❌ FIX 2b: Photometrics CFG-RBT-2 not found — check manually')

# ============================================================
# FIX 2c: Configurator compliance row — remove "(heads up: no TAA · no Made-in-USA)"
# ============================================================
old_cfg = 'Made in China (heads up: no TAA · no Made-in-USA)'
new_cfg = 'Made in China'

if old_cfg in content:
    content = content.replace(old_cfg, new_cfg, 1)
    changes.append('✅ FIX 2c: Configurator compliance parenthetical removed')
else:
    changes.append('❌ FIX 2c: Configurator compliance not found — check manually')

# ============================================================
# FIX 3: Delete stray Solstice section (lines 4673-4785 in original)
# The section is preceded by a comment and starts with spotlight-section
# Delete from the comment through the closing </section>
# ============================================================
# Find the comment + section block
solstice_comment = '<!-- (legacy Solstice §3 below — preserved as reference, hidden in render) -->'
# Find start of comment
comment_idx = content.find(solstice_comment)
if comment_idx != -1:
    # Find the closing </section> of the spotlight-section
    section_start = content.find('<section class="spotlight-section"', comment_idx)
    if section_start != -1:
        # Find the matching </section>
        depth = 0
        i = section_start
        end_idx = -1
        while i < len(content):
            if content[i:i+8] == '<section':
                depth += 1
            elif content[i:i+10] == '</section>':
                depth -= 1
                if depth == 0:
                    end_idx = i + 10  # include </section>
                    break
            i += 1
        
        if end_idx != -1:
            # Delete from comment to end of section (include trailing newline)
            block_to_delete = content[comment_idx:end_idx]
            # Also consume the newline after </section> if present
            if end_idx < len(content) and content[end_idx] == '\n':
                end_idx += 1
            content = content[:comment_idx] + content[end_idx:]
            changes.append(f'✅ FIX 3: Solstice section deleted ({len(block_to_delete)} chars, ~111 lines)')
        else:
            changes.append('❌ FIX 3: Could not find closing </section> for Solstice block')
    else:
        changes.append('❌ FIX 3: spotlight-section not found after comment')
else:
    changes.append('❌ FIX 3: Solstice comment not found')

# ============================================================
# FIX 4a: Tier badge — H1 reads ECO, page-majority says PRO → fix H1
# ============================================================
old_h1 = '<span class="tier-badge tier-eco">ECO</span>'
new_h1 = '<span class="tier-badge tier-pro">PRO</span>'

if old_h1 in content:
    content = content.replace(old_h1, new_h1, 1)
    changes.append('✅ FIX 4a: Tier badge ECO → PRO in H1 (TBD-VERIFY against datasheet)')
else:
    changes.append('⚠️  FIX 4a: ECO tier badge not found — may already be PRO')

# ============================================================
# FIX 4b: Orphaned "-tier " fragments in closing section
# ============================================================

# "Track + -tier networked lighting control. One planoⒶRCH spec."
old_h2 = 'Track + -tier networked lighting control. One plano<span class="aa">Ⓐ</span>RCH spec.'
new_h2 = 'Track + ambient. One plano<span class="aa">Ⓐ</span>RCH spec.'
if old_h2 in content:
    content = content.replace(old_h2, new_h2, 1)
    changes.append('✅ FIX 4b: Closing H2 orphaned -tier fragment rewritten')
else:
    changes.append('❌ FIX 4b: Closing H2 not found')

# "LCDL -tier networked lighting control family" in closing sub-para
old_sub = 'the <strong>LCDL -tier networked lighting control family</strong>'
new_sub = 'the <strong>LCDL plano<span class="aa">Ⓐ</span>RCH downlight family</strong>'
if old_sub in content:
    content = content.replace(old_sub, new_sub, 1)
    changes.append('✅ FIX 4b: Closing sub-para LCDL -tier rewritten')
else:
    changes.append('❌ FIX 4b: Closing sub-para not found')

# "-tier networked lighting control cousin" in Spectra family card
old_spectra = 'The high-output -tier networked lighting control cousin for spaces requiring'
new_spectra = 'The high-output plano<span class="aa">Ⓐ</span>RCH downlight cousin for spaces requiring'
if old_spectra in content:
    content = content.replace(old_spectra, new_spectra, 1)
    changes.append('✅ FIX 4b: Spectra family card -tier fragment rewritten')
else:
    changes.append('❌ FIX 4b: Spectra family card not found')

# "The ambient -tier networked lighting control companion to Trackstar" in Astra card
old_astra = 'The ambient -tier networked lighting control companion to Trackstar'
new_astra = 'The ambient plano<span class="aa">Ⓐ</span>RCH downlight companion to Trackstar'
if old_astra in content:
    content = content.replace(old_astra, new_astra, 1)
    changes.append('✅ FIX 4b: Astra family card -tier fragment rewritten')
else:
    changes.append('❌ FIX 4b: Astra family card not found')

# alt text "-tier networked lighting control family"
old_alt = 'the planoⒶRCH track-light cousin to the LCDL -tier networked lighting control family'
new_alt = 'the planoⒶRCH track-light cousin to the LCDL planoⒶRCH downlight family'
if old_alt in content:
    content = content.replace(old_alt, new_alt, 1)
    changes.append('✅ FIX 4b: Alt text -tier fragment rewritten')
else:
    changes.append('⚠️  FIX 4b: Alt text -tier not found (may use different encoding)')

# JS comment position 4 = Solstice (ECO -tier networked lighting control cousin)
old_js4 = 'Position 4 = Solstice (ECO -tier networked lighting control cousin)'
new_js4 = 'Position 4 = Solstice (ECO planoⒶRCH downlight cousin)'
if old_js4 in content:
    content = content.replace(old_js4, new_js4, 1)
    changes.append('✅ FIX 4b: JS comment position 4 -tier rewritten')
else:
    changes.append('⚠️  FIX 4b: JS comment position 4 not found')

# "on track infrastructure; the LCDL -tier networked lighting control family handles ambient"
old_js_lcdl = 'on track infrastructure; the LCDL -tier networked lighting control family handles ambient'
new_js_lcdl = 'on track infrastructure; the LCDL planoⒶRCH downlight family handles ambient'
if old_js_lcdl in content:
    content = content.replace(old_js_lcdl, new_js_lcdl, 1)
    changes.append('✅ FIX 4b: JS comment LCDL -tier rewritten')
else:
    changes.append('⚠️  FIX 4b: JS comment LCDL -tier not found')

# ============================================================
# FIX 4c: Truncated family card nouns — "Commercial ." → "Commercial Downlight."
# ============================================================
# Solstice card
old_solstice_card = 'Affordable Can-Less Commercial . 4 sizes'
new_solstice_card = 'Affordable Can-Less Commercial Downlight. 4 sizes'
if old_solstice_card in content:
    content = content.replace(old_solstice_card, new_solstice_card, 1)
    changes.append('✅ FIX 4c: Solstice family card truncated noun restored')
else:
    changes.append('❌ FIX 4c: Solstice family card truncated noun not found')

# Astra card
old_astra_card = 'Spec-Grade Adjustable Architectural Commercial . CRI 90+'
new_astra_card = 'Spec-Grade Adjustable Architectural Commercial Downlight. CRI 90+'
if old_astra_card in content:
    content = content.replace(old_astra_card, new_astra_card, 1)
    changes.append('✅ FIX 4c: Astra family card truncated noun restored')
else:
    changes.append('❌ FIX 4c: Astra family card truncated noun not found')

# Spectra card
old_spectra_card = 'Spec-Grade High-Output Integrated-J-Box Commercial . 10/15/20W'
new_spectra_card = 'Spec-Grade High-Output Integrated-J-Box Commercial Downlight. 10/15/20W'
if old_spectra_card in content:
    content = content.replace(old_spectra_card, new_spectra_card, 1)
    changes.append('✅ FIX 4c: Spectra family card truncated noun restored')
else:
    changes.append('❌ FIX 4c: Spectra family card truncated noun not found')

# ============================================================
# Write file
# ============================================================
with open('public/products/trackstar/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('\n'.join(changes))

# ============================================================
# Verification sweep
# ============================================================
print('\n=== VERIFICATION ===')
checks = [
    ('TAA COMPLIANT', 'feature-chip-label'),
    ('NOTE: datasheet pg', 'spec-table footnote NOTE'),
    ('per Rebate Center · CFG-RBT-2', 'CFG-RBT-2 in rendered copy'),
    ('heads up: no TAA', 'heads up in configurator'),
    ('spotlight-section', 'Solstice section'),
    ('tier-eco', 'ECO tier badge'),
    ('-tier networked lighting control', '-tier orphan fragments'),
    ('Commercial .', 'truncated Commercial noun'),
]

for pattern, label in checks:
    # Only check rendered copy (not CSS/JS comments)
    # Simple check — count occurrences outside of <!--
    count = content.count(pattern)
    if count == 0:
        print(f'  ✅ CLEAN: {label}')
    else:
        print(f'  ❌ STILL PRESENT ({count}x): {label}')
        # Show first occurrence context
        idx = content.find(pattern)
        print(f'     context: {repr(content[max(0,idx-40):idx+80])}')
