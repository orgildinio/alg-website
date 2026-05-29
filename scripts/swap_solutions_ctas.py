#!/usr/bin/env python3
"""
Swap CTAs on the 5 stub solutions pages:
- Replace single "Contact Sales →" btn--primary with dual CTA block
- Add btn--ghost CSS if missing
"""
import re, pathlib

PAGES = {
    'government-military':    'ALG_Government_Military_Lighting.pdf',
    'healthcare':             'ALG_Healthcare_Lighting.pdf',
    'hospitality':            'ALG_Hospitality_Lighting.pdf',
    'industrial-manufacturing': 'ALG_Industrial_Manufacturing_Lighting.pdf',
    'warehouse-logistics':    'ALG_Warehouse_Logistics_Lighting.pdf',
}

BASE = pathlib.Path('/home/ubuntu/alg-website-src/src/pages/solutions')

GHOST_CSS = """.btn--ghost {
    background: transparent;
    color: var(--text-primary);
    border: 2px solid var(--line-strong);
  }
  .btn--ghost:hover { border-color: var(--text-secondary); }"""

for slug, pdf in PAGES.items():
    path = BASE / slug / 'index.astro'
    text = path.read_text()

    # 1. Add btn--ghost CSS if missing
    if 'btn--ghost' not in text:
        text = text.replace(
            '.btn--primary:hover { background: var(--brand-red-dark); border-color: var(--brand-red-dark); }',
            '.btn--primary:hover { background: var(--brand-red-dark); border-color: var(--brand-red-dark); }\n  ' + GHOST_CSS
        )

    # 2. Replace the single "Contact Sales →" CTA with dual block
    old_cta = '<a href="/contact" class="btn btn--primary">Contact Sales →</a>'
    new_cta = (
        '<div class="hero__cta-row" style="display:flex;gap:12px;flex-wrap:wrap;">\n'
        '          <a href="mailto:sales@archipelagolighting.com?subject=Photometric%20request" class="btn btn--primary">Request a Photometric <span class="arrow">→</span></a>\n'
        f'          <a href="/spec-packs/{pdf}" class="btn btn--ghost" target="_blank" rel="noopener" download>Download Spec Pack <span class="arrow">→</span></a>\n'
        '        </div>'
    )
    if old_cta in text:
        text = text.replace(old_cta, new_cta)
        print(f'✅ {slug}: CTA swapped')
    else:
        print(f'⚠️  {slug}: old CTA not found — check manually')

    path.write_text(text)

print('\nDone.')
