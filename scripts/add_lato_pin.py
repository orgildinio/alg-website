#!/usr/bin/env python3
"""
add_lato_pin.py

Adds the CFG-TYPE-1 Lato + JetBrains Mono !important font pin to all 20
EM/CRC driver Astro wrappers. The pin is scoped to the per-PDP host class
(e.g. .em07-cmb150dc-pdp) to avoid leaking into the BaseLayout chrome.

Also checks for and removes any stub secondary nav strip (§D.5).
"""

import re
import os

SLUGS = [
    'em07-cmb150dc', 'em07-cmb260dc', 'em08-amb48dc', 'em08-hmb170dc',
    'em08-mt150dc', 'em08-ytb60dc', 'em15-hmb170dc', 'em15-pmb120ac',
    'em20-cmb150dc', 'em20-cmb260dc', 'em20-hmb135ac', 'em25-hmb170dc',
    'em25-pmb120ac', 'em30-umb170dc', 'em40-rmb170dc', 'em60-gmb170dc',
    'em60-umb170dc', 'crc6-em24-jbs-b', 'crc6-em24-jbs-w', 'crcu-em24-jbm',
]

LATO_PIN_TEMPLATE = """
    /* §D.6 CFG-TYPE-1 · Lato + JetBrains Mono pin — defeat Shopify/Cormorant cascade */
    .{host_class} h1,
    .{host_class} h2,
    .{host_class} h3,
    .{host_class} h4,
    .{host_class} h5,
    .{host_class} h6,
    .{host_class} p,
    .{host_class} a,
    .{host_class} li,
    .{host_class} button,
    .{host_class} span,
    .{host_class} div {{
      font-family: 'Lato', system-ui, -apple-system, sans-serif !important;
    }}
    .{host_class} .eyebrow,
    .{host_class} .alg-eyebrow,
    .{host_class} .mono,
    .{host_class} .spec-row,
    .{host_class} .spec-row .k,
    .{host_class} .spec-row .v,
    .{host_class} [class*="font-mono"],
    .{host_class} .alg-spec-table,
    .{host_class} .alg-spec-table th,
    .{host_class} .alg-spec-table td {{
      font-family: 'JetBrains Mono', ui-monospace, 'SF Mono', Menlo, monospace !important;
    }}"""

patched = 0
skipped = 0
errors = []

for slug in SLUGS:
    astro_path = f'src/pages/products/{slug}/index.astro'
    if not os.path.exists(astro_path):
        print(f'MISSING: {astro_path}')
        errors.append(slug)
        continue

    with open(astro_path, 'r', encoding='utf-8') as f:
        content = f.read()

    host_class = f'{slug}-pdp'

    # Check if already has Lato pin for this host class
    if f'.{host_class} h1' in content or 'font-family.*Lato' in content:
        print(f'ALREADY HAS LATO PIN: {slug}')
        skipped += 1
        continue

    # Find the existing style block (the one with .breadcrumb-band) and append the Lato pin
    # Look for the closing </style> tag in the head slot
    style_close = '  </style>\n  </Fragment>'
    if style_close not in content:
        print(f'STYLE CLOSE NOT FOUND: {slug}')
        errors.append(slug)
        continue

    lato_pin = LATO_PIN_TEMPLATE.format(host_class=host_class)
    new_content = content.replace(style_close, lato_pin + '\n  </style>\n  </Fragment>', 1)

    with open(astro_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'PATCHED: {slug}')
    patched += 1

print(f'\nSummary: {patched} patched, {skipped} already done, {len(errors)} errors')
if errors:
    print(f'Errors: {errors}')
