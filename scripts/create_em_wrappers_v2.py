#!/usr/bin/env python3
"""
Regenerate Astro wrappers for all 20 EM-driver PDPs.
Includes:
- BaseLayout (SiteLayout chrome)
- breadcrumb-band nav (5-segment canonical) with inline CSS
- Head slot with style blocks + font links from public HTML
- Body content from public/products/{slug}/index.html
"""
import os

# Map: dir_slug -> (sku_display_name, title, description, body_class)
EM_PDPS = [
    ('em07-cmb150dc',   'EM07-CMB/150DC',  'constⒶNT EM07-CMB/150DC · Low-Power Factory-Install Emergency Driver · Archipelago Lighting Group',  'Low-power 7W CMB emergency driver. Factory-install. 150Vdc output. UL 924 listed. Multi-family and commercial fixture compatible.', 'em07-cmb150dc-pdp'),
    ('em07-cmb260dc',   'EM07-CMB/260DC',  'constⒶNT EM07-CMB/260DC · Low-Power Factory-Install Emergency Driver · Archipelago Lighting Group',  'Low-power 7W CMB emergency driver. Factory-install. 90–260Vdc wide-range output. /AG ⒶrcticGuard rated. UL 924 listed.', 'em07-cmb260dc-pdp'),
    ('em08-amb48dc',    'EM08-AMB/48DC',   'constⒶNT EM08-AMB/48DC · Low-Power Factory-Install Emergency Driver · Archipelago Lighting Group',   'Low-power 8W AMB emergency driver. Factory-install. 48Vdc output. cityⒶRCH compatible. UL 924 listed.', 'em08-amb48dc-pdp'),
    ('em08-hmb170dc',   'EM08-HMB/170DC',  'constⒶNT EM08-HMB/170DC · Low-Power Field-Install Emergency Driver · Archipelago Lighting Group',   'Low-power 8W HMB emergency driver. Field-install. 170Vdc output. planoⒶRCH compatible. UL 924 listed.', 'em08-hmb170dc-pdp'),
    ('em08-mt150dc',    'EM08-MT/150DC',   'constⒶNT EM08-MT/150DC · Low-Power Field-Install Emergency Driver · Archipelago Lighting Group',    'Low-power 8W MT emergency driver. Field-install. 150Vdc output. Multi-family compatible. UL 924 listed.', 'em08-mt150dc-pdp'),
    ('em08-ytb60dc',    'EM08-YTB/60DC',   'constⒶNT EM08-YTB/60DC · Low-Power Field-Install Emergency Driver · Archipelago Lighting Group',    'Low-power 8W YTB emergency driver. Field-install. 60Vdc output. Multi-family compatible. UL 924 listed.', 'em08-ytb60dc-pdp'),
    ('em15-hmb170dc',   'EM15-HMB/170DC',  'constⒶNT EM15-HMB/170DC · Mid-Power Field-Install Emergency Driver · Archipelago Lighting Group',   'Mid-power 15W HMB emergency driver. Field-install. 170Vdc output. planoⒶRCH compatible. UL 924 listed.', 'em15-hmb170dc-pdp'),
    ('em15-pmb120ac',   'EM15-PMB/120AC',  'constⒶNT EM15-PMB/120AC · Mid-Power Field-Install Emergency Driver · Archipelago Lighting Group',   'Mid-power 15W PMB emergency driver. Field-install. 120Vac output. /CL networked-test ready. lamparⒶRCH compatible. UL 924 listed.', 'em15-pmb120ac-pdp'),
    ('em20-cmb150dc',   'EM20-CMB/150DC',  'constⒶNT EM20-CMB/150DC · Mid-Power Quick-Install Emergency Driver · Archipelago Lighting Group',   'Mid-power 20W CMB emergency driver. Quick-install J-Box mount. 150Vdc output. Universal fixture compatible. UL 924 listed.', 'em20-cmb150dc-pdp'),
    ('em20-cmb260dc',   'EM20-CMB/260DC',  'constⒶNT EM20-CMB/260DC · Mid-Power Factory-Install Emergency Driver · Archipelago Lighting Group', 'Mid-power 20W CMB emergency driver. Factory-install. 90–260Vdc wide-range output. /AG ⒶrcticGuard rated. UL 924 listed.', 'em20-cmb260dc-pdp'),
    ('em20-hmb135ac',   'EM20-HMB/135AC',  'constⒶNT EM20-HMB/135AC · Mid-Power Field-Install Emergency Driver · Archipelago Lighting Group',   'Mid-power 20W HMB emergency driver. Field-install. 135Vac output. /CL networked-test ready. luxoⒶRCH compatible. UL 924 listed.', 'em20-hmb135ac-pdp'),
    ('em25-hmb170dc',   'EM25-HMB/170DC',  'constⒶNT EM25-HMB/170DC · Mid-Power Field-Install Emergency Driver · Archipelago Lighting Group',   'Mid-power 25W HMB emergency driver. Field-install. 170Vdc output. lamparⒶRCH compatible. UL 924 listed.', 'em25-hmb170dc-pdp'),
    ('em25-pmb120ac',   'EM25-PMB/120AC',  'constⒶNT EM25-PMB/120AC · Mid-Power Field-Install Emergency Driver · Archipelago Lighting Group',   'Mid-power 25W PMB emergency driver. Field-install. 120Vac output. /CL networked-test ready. lamparⒶRCH compatible. UL 924 listed.', 'em25-pmb120ac-pdp'),
    ('em30-umb170dc',   'EM30-UMB/170DC',  'constⒶNT EM30-UMB/170DC · High-Power Field-Install Emergency Driver · Archipelago Lighting Group',  'High-power 30W UMB emergency driver. Field-install. 170Vdc output. External /U chassis. Universal fixture compatible. UL 924 listed.', 'em30-umb170dc-pdp'),
    ('em40-rmb170dc',   'EM40-RMB/170DC',  'constⒶNT EM40-RMB/170DC · High-Power Field-Install Emergency Driver · Archipelago Lighting Group',  'High-power 40W RMB emergency driver. Field-install. 170Vdc output. /CL networked-test ready. lamparⒶRCH compatible. UL 924 listed.', 'em40-rmb170dc-pdp'),
    ('em60-gmb170dc',   'EM60-GMB/170DC',  'constⒶNT EM60-GMB/170DC · High-Power Field-Install Emergency Driver · Archipelago Lighting Group',  'High-power 60W GMB emergency driver. Field-install. 170Vdc output. lamparⒶRCH high-bay compatible. UL 924 listed.', 'em60-gmb170dc-pdp'),
    ('em60-umb170dc',   'EM60-UMB/170DC',  'constⒶNT EM60-UMB/170DC · High-Power Field-Install Emergency Driver · Archipelago Lighting Group',  'High-power 60W UMB emergency driver. Field-install. 170Vdc output. External /U chassis. Warehouse compatible. UL 924 listed.', 'em60-umb170dc-pdp'),
    ('crcu-em24-jbm',   'CRCU-EM24/JBM',   'constⒶNT CRCU-EM24/JBM · Mid-Power Quick-Install Emergency Driver · Archipelago Lighting Group',    'Mid-power 24W CRCU emergency driver. Quick-install J-Box mount. 190Vdc output. Universal fixture compatible. UL 924 listed.', 'crcu-em24-jbm-pdp'),
    ('crc6-em24-jbs-b', 'CRC6-EM24/JBS/B', 'constⒶNT CRC6-EM24/JBS/B · Mid-Power Quick-Install Emergency Driver · Archipelago Lighting Group',  'Mid-power 24W CRC6 emergency driver. Quick-install J-Box surface mount. Black finish. 190Vdc output. luxoⒶRCH compatible. UL 924 listed.', 'crc6-em24-jbs-b-pdp'),
    ('crc6-em24-jbs-w', 'CRC6-EM24/JBS/W', 'constⒶNT CRC6-EM24/JBS/W · Mid-Power Quick-Install Emergency Driver · Archipelago Lighting Group',  'Mid-power 24W CRC6 emergency driver. Quick-install J-Box surface mount. White finish. 190Vdc output. luxoⒶRCH compatible. UL 924 listed.', 'crc6-em24-jbs-w-pdp'),
]

BREADCRUMB_CSS = '''\
  <style>
    /* §D.1 breadcrumb-band — constⒶNT EM-driver PDPs */
    .breadcrumb-band {
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
    }
    .breadcrumb-band a { color: #666; text-decoration: none; }
    .breadcrumb-band a:hover { color: var(--color-alg-red, #F32740); }
    .bc-sep { color: #c8ccd3; }
    .bc-current { color: #000; font-weight: 600; }
    .bc-current .aa { color: var(--color-alg-red, #F32740); }
    .aa { color: var(--color-alg-red, #F32740); }
  </style>'''

WRAPPER_TEMPLATE = '''\
---
/**
 * {slug} PDP — constⒶNT · Astro wrapper
 * Route: /products/{slug}/
 *
 * CFG-CHROME-1: BaseLayout injects site header + footer.
 * CFG-TYPE-1: Lato + JetBrains Mono pinned via head slot style blocks.
 * §D.1: 5-segment canonical breadcrumb injected before React app body.
 * §D.4: SiteLayout chrome restored (was missing on all EM/CRC routes).
 */
import BaseLayout from '../../../../layouts/BaseLayout.astro';
import {{ readFileSync }} from 'node:fs';
import path from 'node:path';
const publicHtml = readFileSync(
  path.join(process.cwd(), 'public/products/{slug}/index.html'),
  'utf-8'
);
// Extract body content
const bodyMatch = publicHtml.match(/<body[^>]*>([\\s\\S]*)<\\/body>/i);
const bodyContent = bodyMatch ? bodyMatch[1] : publicHtml;
// Extract all <style> blocks from <head>
const headMatch = publicHtml.match(/<head[^>]*>([\\s\\S]*?)<\\/head>/i);
const headContent = headMatch ? headMatch[1] : '';
const styleBlocks = [...headContent.matchAll(/<style[^>]*>[\\s\\S]*?<\\/style>/gi)]
  .map(m => m[0]).join('\\n');
// Extract Google Fonts link tags
const fontLinks = [...headContent.matchAll(/<link[^>]*fonts\\.googleapis\\.com[^>]*>/gi)]
  .map(m => m[0]).join('\\n');
const fontPreconnects = [...headContent.matchAll(/<link[^>]*rel="preconnect"[^>]*>/gi)]
  .map(m => m[0]).join('\\n');
---
<BaseLayout
  title="{title}"
  description="{description}"
  bodyClass="{body_class}"
>
  <Fragment slot="head">
    <Fragment set:html={{fontPreconnects}} />
    <Fragment set:html={{fontLinks}} />
    <Fragment set:html={{styleBlocks}} />
{breadcrumb_css}
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
    <span class="bc-current">{sku_name}</span>
  </div>
  <div class="{body_class}">
    <Fragment set:html={{bodyContent}} />
  </div>
</BaseLayout>
'''

created = []
for slug, sku_name, title, description, body_class in EM_PDPS:
    wrapper_dir = f'src/pages/products/{slug}'
    os.makedirs(wrapper_dir, exist_ok=True)
    
    wrapper_path = f'{wrapper_dir}/index.astro'
    
    public_html = f'public/products/{slug}/index.html'
    if not os.path.exists(public_html):
        print(f'WARNING: {public_html} does not exist, skipping')
        continue
    
    content = WRAPPER_TEMPLATE.format(
        slug=slug,
        sku_name=sku_name,
        title=title,
        description=description,
        body_class=body_class,
        breadcrumb_css=BREADCRUMB_CSS,
    )
    
    with open(wrapper_path, 'w') as f:
        f.write(content)
    
    created.append(slug)
    print(f'Created: {wrapper_path}')

print(f'\nTotal: {len(created)} wrappers created')
