#!/usr/bin/env python3
"""
Regenerate all 20 EM-driver PDP Astro wrappers.
Each wrapper:
  - Wraps in BaseLayout (SiteLayout chrome)
  - Injects 5-seg breadcrumb
  - Extracts <style> AND <script> blocks from v9 HTML <head>
  - Injects body content (data + JSX scripts)
  - Pins Lato + JetBrains Mono fonts
"""

SKUS = [
    {
        'slug': 'em07-cmb150dc',
        'name': 'EM07-CMB/150DC',
        'title': 'constⒶNT EM07-CMB/150DC · Low-Power Factory-Install Emergency Driver · Archipelago Lighting Group',
        'desc': 'Low-power 7W CMB emergency driver. Factory-install. 150Vdc output. UL 924 listed. Multi-family and commercial fixture compatible.',
    },
    {
        'slug': 'em07-cmb260dc',
        'name': 'EM07-CMB/260DC',
        'title': 'constⒶNT EM07-CMB/260DC · Low-Power Factory-Install Emergency Driver · Archipelago Lighting Group',
        'desc': 'Low-power 7W CMB emergency driver. Factory-install. 90–260Vdc wide-range output. /AG ArcticGuard ready. UL 924 listed.',
    },
    {
        'slug': 'em08-amb48dc',
        'name': 'EM08-AMB/48DC',
        'title': 'constⒶNT EM08-AMB/48DC · Low-Power Factory-Install Emergency Driver · Archipelago Lighting Group',
        'desc': 'Low-power 8W AMB emergency driver. Factory-install. 48Vdc output. UL 924 listed. cityARCH fixture compatible.',
    },
    {
        'slug': 'em08-hmb170dc',
        'name': 'EM08-HMB/170DC',
        'title': 'constⒶNT EM08-HMB/170DC · Low-Power Field-Install Emergency Driver · Archipelago Lighting Group',
        'desc': 'Low-power 8W HMB emergency driver. Field-install. 170Vdc output. UL 924 listed. planoARCH fixture compatible.',
    },
    {
        'slug': 'em08-mt150dc',
        'name': 'EM08-MT/150DC',
        'title': 'constⒶNT EM08-MT/150DC · Low-Power Field-Install Emergency Driver · Archipelago Lighting Group',
        'desc': 'Low-power 8W MT emergency driver. Field-install. 150Vdc output. UL 924 listed. Multi-family fixture compatible.',
    },
    {
        'slug': 'em08-ytb60dc',
        'name': 'EM08-YTB/60DC',
        'title': 'constⒶNT EM08-YTB/60DC · Low-Power Field-Install Emergency Driver · Archipelago Lighting Group',
        'desc': 'Low-power 8W YTB emergency driver. Field-install. 60Vdc output. UL 924 listed. Multi-family fixture compatible.',
    },
    {
        'slug': 'em15-hmb170dc',
        'name': 'EM15-HMB/170DC',
        'title': 'constⒶNT EM15-HMB/170DC · Mid-Power Field-Install Emergency Driver · Archipelago Lighting Group',
        'desc': 'Mid-power 15W HMB emergency driver. Field-install. 170Vdc output. UL 924 listed. planoARCH fixture compatible.',
    },
    {
        'slug': 'em15-pmb120ac',
        'name': 'EM15-PMB/120AC',
        'title': 'constⒶNT EM15-PMB/120AC · Mid-Power Field-Install Emergency Driver · Archipelago Lighting Group',
        'desc': 'Mid-power 15W PMB emergency driver. Field-install. 120Vac output. /CL constANTLink ready. UL 924 listed.',
    },
    {
        'slug': 'em20-cmb150dc',
        'name': 'EM20-CMB/150DC',
        'title': 'constⒶNT EM20-CMB/150DC · Mid-Power Quick-Install Emergency Driver · Archipelago Lighting Group',
        'desc': 'Mid-power 20W CMB emergency driver. Quick-install J-Box mount. 150Vdc output. UL 924 listed.',
    },
    {
        'slug': 'em20-cmb260dc',
        'name': 'EM20-CMB/260DC',
        'title': 'constⒶNT EM20-CMB/260DC · Mid-Power Factory-Install Emergency Driver · Archipelago Lighting Group',
        'desc': 'Mid-power 20W CMB emergency driver. Factory-install. 90–260Vdc wide-range output. /AG ArcticGuard ready. UL 924 listed.',
    },
    {
        'slug': 'em20-hmb135ac',
        'name': 'EM20-HMB/135AC',
        'title': 'constⒶNT EM20-HMB/135AC · Mid-Power Field-Install Emergency Driver · Archipelago Lighting Group',
        'desc': 'Mid-power 20W HMB emergency driver. Field-install. 135Vac tubular AC-output. /CL constANTLink ready. UL 924 listed.',
    },
    {
        'slug': 'em25-hmb170dc',
        'name': 'EM25-HMB/170DC',
        'title': 'constⒶNT EM25-HMB/170DC · Mid-Power Field-Install Emergency Driver · Archipelago Lighting Group',
        'desc': 'Mid-power 25W HMB emergency driver. Field-install. 170Vdc output. UL 924 listed. lamparARCH fixture compatible.',
    },
    {
        'slug': 'em25-pmb120ac',
        'name': 'EM25-PMB/120AC',
        'title': 'constⒶNT EM25-PMB/120AC · Mid-Power Field-Install Emergency Driver · Archipelago Lighting Group',
        'desc': 'Mid-power 25W PMB emergency driver. Field-install. 120Vac output. /CL constANTLink ready. UL 924 listed.',
    },
    {
        'slug': 'em30-umb170dc',
        'name': 'EM30-UMB/170DC',
        'title': 'constⒶNT EM30-UMB/170DC · High-Power Field-Install Emergency Driver · Archipelago Lighting Group',
        'desc': 'High-power 30W UMB emergency driver. Field-install. 170Vdc output. External /U chassis. UL 924 listed.',
    },
    {
        'slug': 'em40-rmb170dc',
        'name': 'EM40-RMB/170DC',
        'title': 'constⒶNT EM40-RMB/170DC · High-Power Field-Install Emergency Driver · Archipelago Lighting Group',
        'desc': 'High-power 40W RMB emergency driver. Field-install. 170Vdc output. /CL constANTLink ready. lamparARCH compatible. UL 924 listed.',
    },
    {
        'slug': 'em60-gmb170dc',
        'name': 'EM60-GMB/170DC',
        'title': 'constⒶNT EM60-GMB/170DC · High-Power Field-Install Emergency Driver · Archipelago Lighting Group',
        'desc': 'High-power 60W GMB emergency driver. Field-install. 170Vdc output. lamparARCH high-bay compatible. UL 924 listed.',
    },
    {
        'slug': 'em60-umb170dc',
        'name': 'EM60-UMB/170DC',
        'title': 'constⒶNT EM60-UMB/170DC · High-Power Field-Install Emergency Driver · Archipelago Lighting Group',
        'desc': 'High-power 60W UMB emergency driver. Field-install. 170Vdc output. External /U chassis. Warehouse/logistics compatible. UL 924 listed.',
    },
    {
        'slug': 'crc6-em24-jbs-b',
        'name': 'CRC6-EM24/JBS/B',
        'title': 'constⒶNT CRC6-EM24/JBS/B · Mid-Power Quick-Install Emergency Driver · Archipelago Lighting Group',
        'desc': 'Mid-power 24W CRC6 emergency driver. Quick-install J-Box surface mount. Black finish. 190Vdc output. UL 924 listed.',
    },
    {
        'slug': 'crc6-em24-jbs-w',
        'name': 'CRC6-EM24/JBS/W',
        'title': 'constⒶNT CRC6-EM24/JBS/W · Mid-Power Quick-Install Emergency Driver · Archipelago Lighting Group',
        'desc': 'Mid-power 24W CRC6 emergency driver. Quick-install J-Box surface mount. White finish. 190Vdc output. UL 924 listed.',
    },
    {
        'slug': 'crcu-em24-jbm',
        'name': 'CRCU-EM24/JBM',
        'title': 'constⒶNT CRCU-EM24/JBM · Mid-Power Quick-Install Emergency Driver · Archipelago Lighting Group',
        'desc': 'Mid-power 24W CRCU emergency driver. Quick-install J-Box mount. 190Vdc output. UL 924 listed.',
    },
]

TEMPLATE = '''---
/**
 * {slug} PDP — constⒶNT · Astro wrapper
 * Route: /products/{slug}/
 *
 * CFG-CHROME-1: BaseLayout injects site header + footer.
 * CFG-TYPE-1: Lato + JetBrains Mono pinned via head slot style blocks.
 * §D.1: 5-segment canonical breadcrumb injected before React app body.
 * §D.4: SiteLayout chrome restored (was missing on all EM/CRC routes).
 */
import BaseLayout from '../../../layouts/BaseLayout.astro';
import {{ readFileSync }} from 'node:fs';
import path from 'node:path';
const publicHtml = readFileSync(
  path.join(process.cwd(), 'public/products/{slug}/index.html'),
  'utf-8'
);
// Extract body content (data + JSX render scripts)
const bodyMatch = publicHtml.match(/<body[^>]*>([\s\S]*)<\\/body>/i);
const bodyContent = bodyMatch ? bodyMatch[1] : publicHtml;
// Extract all <style> and <script> blocks from <head>
const headMatch = publicHtml.match(/<head[^>]*>([\s\S]*?)<\\/head>/i);
const headContent = headMatch ? headMatch[1] : '';
const styleBlocks = [...headContent.matchAll(/<style[^>]*>[\\s\\S]*?<\\/style>/gi)]
  .map(m => m[0]).join('\\n');
const scriptBlocks = [...headContent.matchAll(/<script[^>]*>[\\s\\S]*?<\\/script>/gi)]
  .map(m => m[0]).join('\\n');
// Extract Google Fonts link tags
const fontLinks = [...headContent.matchAll(/<link[^>]*fonts\\.googleapis\\.com[^>]*>/gi)]
  .map(m => m[0]).join('\\n');
const fontPreconnects = [...headContent.matchAll(/<link[^>]*rel="preconnect"[^>]*>/gi)]
  .map(m => m[0]).join('\\n');
---
<BaseLayout
  title="{title}"
  description="{desc}"
  bodyClass="{slug}-pdp"
>
  <Fragment slot="head">
    <Fragment set:html={{fontPreconnects}} />
    <Fragment set:html={{fontLinks}} />
    <Fragment set:html={{styleBlocks}} />
    <Fragment set:html={{scriptBlocks}} />
  <style>
    /* §D.1 breadcrumb-band — constⒶNT EM-driver PDPs */
    .breadcrumb-band {{
      padding: 10px 32px;
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 0.75rem;
      letter-spacing: 0.08em;
      font-weight: 500;
      text-transform: uppercase;
      color: #666;
      background: var(--bg2, #f5f5f3);
      border-bottom: 1px solid rgba(0,0,0,0.06);
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }}
    .breadcrumb-band a {{ color: #666; text-decoration: none; }}
    .breadcrumb-band a:hover {{ color: var(--color-alg-red, #F32740); }}
    .bc-sep {{ color: #c8ccd3; }}
    .bc-current {{ color: #000; font-weight: 600; }}
    .bc-current .aa {{ color: var(--color-alg-red, #F32740); }}
    .aa {{ color: var(--color-alg-red, #F32740); }}
    /* §D.6 CFG-TYPE-1 · Lato + JetBrains Mono pin — defeat Shopify/Cormorant cascade */
    .{slug}-pdp h1,
    .{slug}-pdp h2,
    .{slug}-pdp h3,
    .{slug}-pdp h4,
    .{slug}-pdp h5,
    .{slug}-pdp h6,
    .{slug}-pdp p,
    .{slug}-pdp a,
    .{slug}-pdp li,
    .{slug}-pdp button,
    .{slug}-pdp span,
    .{slug}-pdp div {{
      font-family: 'Lato', system-ui, -apple-system, sans-serif !important;
    }}
    .{slug}-pdp .eyebrow,
    .{slug}-pdp .alg-eyebrow,
    .{slug}-pdp .mono,
    .{slug}-pdp .spec-row,
    .{slug}-pdp .spec-row .k,
    .{slug}-pdp .spec-row .v,
    .{slug}-pdp [class*="font-mono"],
    .{slug}-pdp .alg-spec-table,
    .{slug}-pdp .alg-spec-table th,
    .{slug}-pdp .alg-spec-table td {{
      font-family: 'JetBrains Mono', ui-monospace, 'SF Mono', Menlo, monospace !important;
    }}
  </style>
  </Fragment>
  <!-- §D.1 · 5-segment canonical breadcrumb -->
  <div class="breadcrumb-band">
    <a href="/">HOME</a>
    <span class="bc-sep">›</span>
    <a href="/collections">PRODUCTS</a>
    <span class="bc-sep">›</span>
    <a href="/solutions/safety-controls/">SAFETY &amp; CONTROLS</a>
    <span class="bc-sep">›</span>
    <a href="/collections/constant/">CONST<span class="aa">Ⓐ</span>NT</a>
    <span class="bc-sep">›</span>
    <span class="bc-current">{name}</span>
  </div>
  <div class="{slug}-pdp">
    <Fragment set:html={{bodyContent}} />
  </div>
</BaseLayout>
'''

import os

WRAPPERS_DIR = '/home/ubuntu/alg-website-src/src/pages/products'

for sku in SKUS:
    slug = sku['slug']
    wrapper_dir = os.path.join(WRAPPERS_DIR, slug)
    os.makedirs(wrapper_dir, exist_ok=True)
    wrapper_path = os.path.join(wrapper_dir, 'index.astro')
    content = TEMPLATE.format(
        slug=slug,
        name=sku['name'],
        title=sku['title'],
        desc=sku['desc'],
    )
    with open(wrapper_path, 'w') as f:
        f.write(content)
    print(f'  ✓ {slug}/index.astro')

print(f'\n{len(SKUS)}/20 wrappers regenerated.')
