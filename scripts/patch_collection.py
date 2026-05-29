#!/usr/bin/env python3
"""
Apply all §B collection page fixes to src/pages/collections/constant/index.astro
"""
import re

path = 'src/pages/collections/constant/index.astro'
with open(path, 'r', encoding='utf-8') as f:
    src = f.read()

orig = src

# ── §B.1  SKU count: 11 → 20 everywhere ──────────────────────────────────────
src = src.replace(
    "* §D.8 SKU grid: ONLY 11 real SKUs. 5 invented SKUs removed.",
    "* §D.8 SKU grid: 20 real SKUs (v8 full set)."
)
src = src.replace(
    "* §D.16 Anchor rail: 11 dots.",
    "* §D.16 Anchor rail: 11 dots. (unchanged)"
)
src = src.replace(
    "  { value: '11',     label: 'Active Driver SKUs'    },",
    "  { value: '20',     label: 'Active Driver SKUs'    },"
)
src = src.replace(
    "  { value: '11',    label: 'Active Drivers'         },",
    "  { value: '20',    label: 'Active Drivers'         },"
)
src = src.replace(
    '  title="constANT — Emergency Drivers | Archipelago Lighting Group"',
    '  title="constⒶNT — Emergency Drivers · Archipelago Lighting Group"'
)
src = src.replace(
    '  description="constANT — ALG\'s emergency battery backup driver ecosystem. UL 924 listed. Universal 100–347Vac input. 11 active driver SKUs across 4 install tiers and 8 verticals."',
    '  description="constⒶNT — ALG\'s emergency battery backup driver ecosystem. UL 924 listed. Multi-input 120–347 VAC. 20 active driver SKUs across 3 install tiers and 8 verticals."'
)

# ── §B.2  Hero body copy: tech-truth ─────────────────────────────────────────
src = src.replace(
    'UL 924 listed. Universal 100–347Vac input. <strong>11 active driver SKUs across 3 install tiers and 8 verticals.</strong>',
    'UL 924 listed. Multi-input 120–347 VAC. <strong>20 active driver SKUs across 3 install tiers and 8 verticals.</strong>'
)
src = src.replace(
    '<span class="hero-pill">100–347VAC UNIVERSAL</span>',
    '<span class="hero-pill">120-347 VAC INPUT</span>'
)
src = src.replace(
    '<span class="hero-pill">TITLE 24 NLC-READY</span>',
    '<span class="hero-pill">NLC-READY VIA /CL</span>'
)

# ── §B.3  BROWSE BY INSTALL TIER — remove TIER n · prefix ────────────────────
src = src.replace(
    '<span class="btl-eyebrow">TIER 1 · FACTORY</span>',
    '<span class="btl-eyebrow">FACTORY</span>'
)
src = src.replace(
    '<span class="btl-eyebrow">TIER 2 · FIELD</span>',
    '<span class="btl-eyebrow">FIELD</span>'
)
src = src.replace(
    '<span class="btl-eyebrow">TIER 3 · QUICK</span>',
    '<span class="btl-eyebrow">QUICK</span>'
)
src = src.replace(
    '<span class="btl-eyebrow">TIER 4 · SAFETY</span>',
    '<span class="btl-eyebrow">SAFETY</span>'
)
src = src.replace(
    '<span class="btl-meta">Exit signs · combo · emergency lights · COMING SOON</span>',
    '<span class="btl-meta">Exit signs · combo · emergency lights</span>'
)
src = src.replace(
    '<span class="btl-meta">2 SKUs · Pre-installed in host fixture</span>',
    '<span class="btl-meta">2 SKUs · Pre-installed in host fixture</span>'
)
src = src.replace(
    '<span class="btl-meta">6 SKUs · Certified electrician on-site</span>',
    '<span class="btl-meta">6 SKUs · Certified electrician on-site</span>'
)
src = src.replace(
    '<span class="btl-meta">3 SKUs · J-Box remote mount</span>',
    '<span class="btl-meta">3 SKUs · J-Box remote mount</span>'
)

# ── §B.4  BROWSE BY PRODUCT TYPE — flip COMING SOON tiles to LIVE ────────────
old_product_type_block = '''        <a class="browse-tile-link browse-tile-link--live" href="#all-drivers">
          <span class="btl-eyebrow">LIVE · 11 SKUS</span>
          <span class="btl-name">Emergency Battery Backup</span>
          <span class="btl-meta">EM &amp; CRC driver line · UL 924</span>
        </a>
        <a class="browse-tile-link browse-tile-link--soon" href="/collections/constant/em-batteries/">
          <span class="btl-eyebrow">COMING SOON</span>
          <span class="btl-name">const<span class="aa">Ⓐ</span>NTLink EM Batteries</span>
          <span class="btl-meta">Networked NLC battery line · notify me →</span>
        </a>
        <a class="browse-tile-link browse-tile-link--soon" href="/collections/constant/exit-signs/">
          <span class="btl-eyebrow">COMING SOON</span>
          <span class="btl-name">Exit Signs</span>
          <span class="btl-meta">UL 924 listed · notify me →</span>
        </a>
        <a class="browse-tile-link browse-tile-link--soon" href="/collections/constant/combo-signs/">
          <span class="btl-eyebrow">COMING SOON</span>
          <span class="btl-name">Combo Signs</span>
          <span class="btl-meta">Exit + emergency in one unit · notify me →</span>
        </a>
        <a class="browse-tile-link browse-tile-link--soon" href="/collections/constant/emergency-lights/">
          <span class="btl-eyebrow">COMING SOON</span>
          <span class="btl-name">Emergency Lights</span>
          <span class="btl-meta">2-head · 4-head · remote-capable · notify me →</span>
        </a>'''
new_product_type_block = '''        <a class="browse-tile-link browse-tile-link--live" href="/collections/constant/#all-drivers">
          <span class="btl-eyebrow">LIVE · 20 SKUS</span>
          <span class="btl-name">Emergency Battery Backup</span>
          <span class="btl-meta">EM &amp; CRC driver line · UL 924</span>
        </a>
        <a class="browse-tile-link browse-tile-link--live" href="/collections/constant/#all-drivers">
          <span class="btl-eyebrow">LIVE · 3 SKUS</span>
          <span class="btl-name">const<span class="aa">Ⓐ</span>NTLink EM Batteries</span>
          <span class="btl-meta">Networked NLC battery line · /CL adder</span>
        </a>
        <a class="browse-tile-link browse-tile-link--live" href="/collections/constant/exit/">
          <span class="btl-eyebrow">LIVE · 28 SKUS</span>
          <span class="btl-name">Exit Signs</span>
          <span class="btl-meta">UL 924 listed · LEMX family</span>
        </a>
        <a class="browse-tile-link browse-tile-link--live" href="/collections/constant/exit/">
          <span class="btl-eyebrow">LIVE · 8 SKUS</span>
          <span class="btl-name">Combo Signs</span>
          <span class="btl-meta">Exit + emergency in one unit</span>
        </a>
        <a class="browse-tile-link browse-tile-link--live" href="/collections/constant/exit/">
          <span class="btl-eyebrow">LIVE · 5 SKUS</span>
          <span class="btl-name">Emergency Lights</span>
          <span class="btl-meta">2-head · 4-head · remote-capable</span>
        </a>'''
src = src.replace(old_product_type_block, new_product_type_block)

# ── §B.5  Featured cards: pdpUrl → real PDP routes + cardImage ───────────────
src = src.replace(
    "    cardImage: null,\n    pdpUrl: '#sku-em20-cmb-260dc',",
    "    cardImage: '/products/em20-cmb260dc/assets/em20-cmb-260dc-001_white.png',\n    cardImageAlt: 'EM20-CMB/260DC emergency driver',\n    pdpUrl: '/products/em20-cmb260dc/',"
)
src = src.replace(
    "    cardImage: null,\n    pdpUrl: '#sku-em15-pmb-120ac',",
    "    cardImage: '/products/em15-pmb120ac/assets/em15-pmb-120ac-001_white.png',\n    cardImageAlt: 'EM15-PMB/120AC emergency driver',\n    pdpUrl: '/products/em15-pmb120ac/',"
)
src = src.replace(
    "    cardImage: null,\n    pdpUrl: '#sku-crcu-em24-jbm',",
    "    cardImage: '/products/crcu-em24-jbm/assets/crcu-em24-jbm-001_white.png',\n    cardImageAlt: 'CRCU-EM24/JBM emergency driver',\n    pdpUrl: '/products/crcu-em24-jbm/',"
)
src = src.replace(
    "    cardImage: null,\n    pdpUrl: '#sku-em60-umb-170dc',",
    "    cardImage: '/products/em60-umb170dc/assets/em60-umb-170dc-001_white.png',\n    cardImageAlt: 'EM60-UMB/170DC emergency driver',\n    pdpUrl: '/products/em60-umb170dc/',"
)

# ── §B.6  Featured headline glyph ────────────────────────────────────────────
src = src.replace(
    'featuredHeadline="Four flagship drivers from the constANT line."',
    'featuredHeadline="Four flagship drivers from the const\u24b6NT line."'
)

# ── §B.7  All Drivers headline count ─────────────────────────────────────────
src = src.replace(
    '<h2 class="fam-headline">11 drivers. One ecosystem.</h2>',
    '<h2 class="fam-headline">20 drivers. One ecosystem.</h2>'
)
src = src.replace(
    '<!-- SKU GRID — 11 real SKUs -->',
    '<!-- SKU GRID — 20 real SKUs -->'
)
src = src.replace(
    '<span class="fam-count-label" id="skuCountLabel">Showing 11 drivers</span>',
    '<span class="fam-count-label" id="skuCountLabel">Showing 20 drivers</span>'
)

# ── §B.8  Filter rail: update INSTALL TIER counts ────────────────────────────
src = src.replace(
    '<label class="fg-item"><input type="checkbox" data-facet="tier" value="factory" /><span class="fg-name">Factory-Install</span><span class="fg-count">(2)</span></label>',
    '<label class="fg-item"><input type="checkbox" data-facet="tier" value="factory" /><span class="fg-name">Factory-Install</span><span class="fg-count">(4)</span></label>'
)
src = src.replace(
    '<label class="fg-item"><input type="checkbox" data-facet="tier" value="field" /><span class="fg-name">Field-Install</span><span class="fg-count">(6)</span></label>',
    '<label class="fg-item"><input type="checkbox" data-facet="tier" value="field" /><span class="fg-name">Field-Install</span><span class="fg-count">(10)</span></label>'
)
src = src.replace(
    '<label class="fg-item"><input type="checkbox" data-facet="tier" value="quick" /><span class="fg-name">Quick-Install</span><span class="fg-count">(3)</span></label>',
    '<label class="fg-item"><input type="checkbox" data-facet="tier" value="quick" /><span class="fg-name">Quick-Install</span><span class="fg-count">(6)</span></label>'
)

# ── §B.9  Filter rail: update POWER CLASS counts ─────────────────────────────
src = src.replace(
    '<label class="fg-item"><input type="checkbox" data-facet="power" value="low" /><span class="fg-name">Low 5–9W</span><span class="fg-count">(1)</span></label>',
    '<label class="fg-item"><input type="checkbox" data-facet="power" value="low" /><span class="fg-name">Low 5–9W</span><span class="fg-count">(2)</span></label>'
)
src = src.replace(
    '<label class="fg-item"><input type="checkbox" data-facet="power" value="mid" /><span class="fg-name">Mid 15–25W</span><span class="fg-count">(5)</span></label>',
    '<label class="fg-item"><input type="checkbox" data-facet="power" value="mid" /><span class="fg-name">Mid 15–25W</span><span class="fg-count">(10)</span></label>'
)
src = src.replace(
    '<label class="fg-item"><input type="checkbox" data-facet="power" value="high" /><span class="fg-name">High 30–60W</span><span class="fg-count">(5)</span></label>',
    '<label class="fg-item"><input type="checkbox" data-facet="power" value="high" /><span class="fg-name">High 30–60W</span><span class="fg-count">(8)</span></label>'
)

# ── §B.10 Filter rail: update ADDER counts ───────────────────────────────────
src = src.replace(
    '<label class="fg-item"><input type="checkbox" data-facet="adder" value="ag" /><span class="fg-name">/AG <span class="aa">Ⓐ</span>rcticGuard</span><span class="fg-count">(1)</span></label>',
    '<label class="fg-item"><input type="checkbox" data-facet="adder" value="ag" /><span class="fg-name">/AG <span class="aa">Ⓐ</span>rcticGuard</span><span class="fg-count">(2)</span></label>'
)
src = src.replace(
    '<label class="fg-item"><input type="checkbox" data-facet="adder" value="xd" /><span class="fg-name">/XD Extended Discharge</span><span class="fg-count">(0)</span></label>',
    '<label class="fg-item"><input type="checkbox" data-facet="adder" value="xd" /><span class="fg-name">/XD Extended Discharge</span><span class="fg-count">(0)</span></label>'
)
src = src.replace(
    '<label class="fg-item"><input type="checkbox" data-facet="adder" value="cl" /><span class="fg-name">/CL const<span class="aa">Ⓐ</span>NTLink</span><span class="fg-count">(3)</span></label>',
    '<label class="fg-item"><input type="checkbox" data-facet="adder" value="cl" /><span class="fg-name">/CL const<span class="aa">Ⓐ</span>NTLink</span><span class="fg-count">(5)</span></label>'
)

# ── §B.11 Filter rail: update OUTPUT TYPE counts ─────────────────────────────
src = src.replace(
    '<label class="fg-item"><input type="checkbox" data-facet="output" value="dc" /><span class="fg-name">DC Output · HMB·CMB·GMB·UMB·MT</span><span class="fg-count">(8)</span></label>',
    '<label class="fg-item"><input type="checkbox" data-facet="output" value="dc" /><span class="fg-name">DC Output</span><span class="fg-count">(16)</span></label>'
)
src = src.replace(
    '<label class="fg-item"><input type="checkbox" data-facet="output" value="ac" /><span class="fg-name">AC Output · PMB·HMB-AC</span><span class="fg-count">(2)</span></label>',
    '<label class="fg-item"><input type="checkbox" data-facet="output" value="ac" /><span class="fg-name">AC Output</span><span class="fg-count">(4)</span></label>'
)

# ── §B.12 Filter rail: update FIXTURE FAMILY counts ──────────────────────────
old_family_block = '''              <label class="fg-item"><input type="checkbox" data-facet="family" value="lamparch" /><span class="fg-name">lampar<span class="aa">Ⓐ</span>RCH</span><span class="fg-count">(4)</span></label>
              <label class="fg-item"><input type="checkbox" data-facet="family" value="luxoarch" /><span class="fg-name">luxo<span class="aa">Ⓐ</span>RCH</span><span class="fg-count">(1)</span></label>
              <label class="fg-item"><input type="checkbox" data-facet="family" value="planoarch" /><span class="fg-name">plano<span class="aa">Ⓐ</span>RCH</span><span class="fg-count">(4)</span></label>
              <label class="fg-item"><input type="checkbox" data-facet="family" value="universal" /><span class="fg-name">All universal</span><span class="fg-count">(0)</span></label>'''
new_family_block = '''              <label class="fg-item"><input type="checkbox" data-facet="family" value="cityarch" /><span class="fg-name">city<span class="aa">Ⓐ</span>RCH</span><span class="fg-count">(1)</span></label>
              <label class="fg-item"><input type="checkbox" data-facet="family" value="lamparch" /><span class="fg-name">lampar<span class="aa">Ⓐ</span>RCH</span><span class="fg-count">(4)</span></label>
              <label class="fg-item"><input type="checkbox" data-facet="family" value="luxoarch" /><span class="fg-name">luxo<span class="aa">Ⓐ</span>RCH</span><span class="fg-count">(2)</span></label>
              <label class="fg-item"><input type="checkbox" data-facet="family" value="multifamily" /><span class="fg-name">multi-f<span class="aa">Ⓐ</span>MILY</span><span class="fg-count">(4)</span></label>
              <label class="fg-item"><input type="checkbox" data-facet="family" value="planoarch" /><span class="fg-name">plano<span class="aa">Ⓐ</span>RCH</span><span class="fg-count">(2)</span></label>
              <label class="fg-item"><input type="checkbox" data-facet="family" value="universal" /><span class="fg-name">All universal</span><span class="fg-count">(7)</span></label>'''
src = src.replace(old_family_block, new_family_block)

# ── §B.13 Filter rail: update CERTIFICATION counts ───────────────────────────
src = src.replace(
    '<label class="fg-item"><input type="checkbox" data-facet="cert" value="ul924" /><span class="fg-name">UL 924 Listed</span><span class="fg-count">(11)</span></label>',
    '<label class="fg-item"><input type="checkbox" data-facet="cert" value="ul924" /><span class="fg-name">UL 924 Listed</span><span class="fg-count">(20)</span></label>'
)
src = src.replace(
    '<label class="fg-item"><input type="checkbox" data-facet="cert" value="csa" /><span class="fg-name">CSA C22.2 No.141</span><span class="fg-count">(11)</span></label>',
    '<label class="fg-item"><input type="checkbox" data-facet="cert" value="csa" /><span class="fg-name">CSA C22.2 No.141</span><span class="fg-count">(20)</span></label>'
)
src = src.replace(
    '<label class="fg-item"><input type="checkbox" data-facet="cert" value="cec" /><span class="fg-name">CEC Title 20</span><span class="fg-count">(11)</span></label>',
    '<label class="fg-item"><input type="checkbox" data-facet="cert" value="cec" /><span class="fg-name">CEC Title 20</span><span class="fg-count">(20)</span></label>'
)

# ── §B.14 SKU data array: expand from 11 to 20 ───────────────────────────────
old_sku_array = '''// §D.8: 11 real SKUs (no invented SKUs)
const skus = [
  { id: 'sku-em07-cmb-150dc',   tier: 'factory', eyebrow: 'FACTORY · LOW-POWER · PRO',  name: 'EM07-CMB/150DC',    meta: '7W · 150Vdc · low-power CMB' },
  { id: 'sku-em20-cmb-260dc',   tier: 'factory', eyebrow: 'FACTORY · MID-POWER · PRO',  name: 'EM20-CMB/260DC',    meta: '20W · 90–260Vdc · /AG ready' },
  { id: 'sku-em15-pmb-120ac',   tier: 'field',   eyebrow: 'FIELD · MID-POWER · PRO',    name: 'EM15-PMB/120AC',    meta: '15W · 120Vac · /CL ready' },
  { id: 'sku-em25-pmb-120ac',   tier: 'field',   eyebrow: 'FIELD · MID-POWER · PRO',    name: 'EM25-PMB/120AC',    meta: '25W · 120Vac · /CL ready' },
  { id: 'sku-em30-umb-170dc',   tier: 'field',   eyebrow: 'FIELD · HIGH-POWER · PRO',   name: 'EM30-UMB/170DC',    meta: '30W · 170Vdc · external /U chassis' },
  { id: 'sku-em40-rmb-170dc',   tier: 'field',   eyebrow: 'FIELD · HIGH-POWER · PRO',   name: 'EM40-RMB/170DC',    meta: '40W · 170Vdc · /CL ready · lamparⒶRCH' },
  { id: 'sku-em60-gmb-170dc',   tier: 'field',   eyebrow: 'FIELD · HIGH-POWER · PRO',   name: 'EM60-GMB/170DC',    meta: '60W · 170Vdc · lamparⒶRCH high-bay' },
  { id: 'sku-em60-umb-170dc',   tier: 'field',   eyebrow: 'FIELD · HIGH-POWER · PRO',   name: 'EM60-UMB/170DC',    meta: '60W · 170Vdc · external /U · warehouse hero' },
  { id: 'sku-crcu-em24-jbm',    tier: 'quick',   eyebrow: 'QUICK · MID-POWER · PRO',    name: 'CRCU-EM24/JBM',     meta: '24W · 190Vdc · J-Box mount' },
  { id: 'sku-crc6-em24-jbs-b',  tier: 'quick',   eyebrow: 'QUICK · MID-POWER · PRO',    name: 'CRC6-EM24/JBS/B',   meta: '24W · 190Vdc · black finish · J-Box surface' },
  { id: 'sku-crc6-em24-jbs-w',  tier: 'quick',   eyebrow: 'QUICK · MID-POWER · PRO',    name: 'CRC6-EM24/JBS/W',   meta: '24W · 190Vdc · white finish · J-Box surface' },
];'''
new_sku_array = '''// §D.8: 20 real SKUs (v8 full set)
const skus = [
  // FACTORY-INSTALL (4)
  { id: 'sku-em07-cmb-150dc',   tier: 'factory', eyebrow: 'FACTORY · LOW-POWER · PRO',  name: 'EM07-CMB/150DC',    meta: '7W · 150Vdc · low-power CMB',            pdp: '/products/em07-cmb150dc/' },
  { id: 'sku-em07-cmb-260dc',   tier: 'factory', eyebrow: 'FACTORY · LOW-POWER · PRO',  name: 'EM07-CMB/260DC',    meta: '7W · 90–260Vdc · low-power CMB',         pdp: '/products/em07-cmb260dc/' },
  { id: 'sku-em08-amb-48dc',    tier: 'factory', eyebrow: 'FACTORY · LOW-POWER · PRO',  name: 'EM08-AMB/48DC',     meta: '8W · 48Vdc · low-power AMB',             pdp: '/products/em08-amb48dc/' },
  { id: 'sku-em20-cmb-260dc',   tier: 'factory', eyebrow: 'FACTORY · MID-POWER · PRO',  name: 'EM20-CMB/260DC',    meta: '20W · 90–260Vdc · /AG ready',            pdp: '/products/em20-cmb260dc/' },
  // FIELD-INSTALL (10)
  { id: 'sku-em08-hmb-170dc',   tier: 'field',   eyebrow: 'FIELD · LOW-POWER · PRO',    name: 'EM08-HMB/170DC',    meta: '8W · 170Vdc · low-power HMB',            pdp: '/products/em08-hmb170dc/' },
  { id: 'sku-em08-mt-150dc',    tier: 'field',   eyebrow: 'FIELD · LOW-POWER · PRO',    name: 'EM08-MT/150DC',     meta: '8W · 150Vdc · low-power MT',             pdp: '/products/em08-mt150dc/' },
  { id: 'sku-em08-ytb-60dc',    tier: 'field',   eyebrow: 'FIELD · LOW-POWER · PRO',    name: 'EM08-YTB/60DC',     meta: '8W · 60Vdc · low-power YTB',             pdp: '/products/em08-ytb60dc/' },
  { id: 'sku-em15-hmb-170dc',   tier: 'field',   eyebrow: 'FIELD · MID-POWER · PRO',    name: 'EM15-HMB/170DC',    meta: '15W · 170Vdc · mid-power HMB',           pdp: '/products/em15-hmb170dc/' },
  { id: 'sku-em15-pmb-120ac',   tier: 'field',   eyebrow: 'FIELD · MID-POWER · PRO',    name: 'EM15-PMB/120AC',    meta: '15W · 120Vac · /CL ready',               pdp: '/products/em15-pmb120ac/' },
  { id: 'sku-em20-hmb-135ac',   tier: 'field',   eyebrow: 'FIELD · MID-POWER · PRO',    name: 'EM20-HMB/135AC',    meta: '20W · 135Vac · tubular AC-output',        pdp: '/products/em20-hmb135ac/' },
  { id: 'sku-em25-hmb-170dc',   tier: 'field',   eyebrow: 'FIELD · MID-POWER · PRO',    name: 'EM25-HMB/170DC',    meta: '25W · 170Vdc · mid-power HMB',           pdp: '/products/em25-hmb170dc/' },
  { id: 'sku-em25-pmb-120ac',   tier: 'field',   eyebrow: 'FIELD · MID-POWER · PRO',    name: 'EM25-PMB/120AC',    meta: '25W · 120Vac · /CL ready',               pdp: '/products/em25-pmb120ac/' },
  { id: 'sku-em30-umb-170dc',   tier: 'field',   eyebrow: 'FIELD · HIGH-POWER · PRO',   name: 'EM30-UMB/170DC',    meta: '30W · 170Vdc · external /U chassis',     pdp: '/products/em30-umb170dc/' },
  { id: 'sku-em40-rmb-170dc',   tier: 'field',   eyebrow: 'FIELD · HIGH-POWER · PRO',   name: 'EM40-RMB/170DC',    meta: '40W · 170Vdc · /CL ready · lamparⒶRCH', pdp: '/products/em40-rmb170dc/' },
  { id: 'sku-em60-gmb-170dc',   tier: 'field',   eyebrow: 'FIELD · HIGH-POWER · PRO',   name: 'EM60-GMB/170DC',    meta: '60W · 170Vdc · lamparⒶRCH high-bay',    pdp: '/products/em60-gmb170dc/' },
  { id: 'sku-em60-umb-170dc',   tier: 'field',   eyebrow: 'FIELD · HIGH-POWER · PRO',   name: 'EM60-UMB/170DC',    meta: '60W · 170Vdc · external /U · warehouse', pdp: '/products/em60-umb170dc/' },
  // QUICK-INSTALL (6)
  { id: 'sku-em20-cmb-150dc',   tier: 'quick',   eyebrow: 'QUICK · MID-POWER · PRO',    name: 'EM20-CMB/150DC',    meta: '20W · 150Vdc · J-Box CMB',               pdp: '/products/em20-cmb150dc/' },
  { id: 'sku-em20-cmb-260dc-q', tier: 'quick',   eyebrow: 'QUICK · MID-POWER · PRO',    name: 'EM20-CMB/260DC',    meta: '20W · 90–260Vdc · J-Box CMB /AG',        pdp: '/products/em20-cmb260dc/' },
  { id: 'sku-crcu-em24-jbm',    tier: 'quick',   eyebrow: 'QUICK · MID-POWER · PRO',    name: 'CRCU-EM24/JBM',     meta: '24W · 190Vdc · J-Box mount',             pdp: '/products/crcu-em24-jbm/' },
  { id: 'sku-crc6-em24-jbs-b',  tier: 'quick',   eyebrow: 'QUICK · MID-POWER · PRO',    name: 'CRC6-EM24/JBS/B',   meta: '24W · 190Vdc · black · J-Box surface',   pdp: '/products/crc6-em24-jbs-b/' },
  { id: 'sku-crc6-em24-jbs-w',  tier: 'quick',   eyebrow: 'QUICK · MID-POWER · PRO',    name: 'CRC6-EM24/JBS/W',   meta: '24W · 190Vdc · white · J-Box surface',   pdp: '/products/crc6-em24-jbs-w/' },
];'''
src = src.replace(old_sku_array, new_sku_array)

# ── §B.15 SKU card VIEW → links: #id → real PDP ──────────────────────────────
# Replace the card template to use sku.pdp for the VIEW link
old_card_view = '                  <a href={`#${sku.id}`} class="fc-view">VIEW →</a>'
new_card_view = '                  <a href={sku.pdp} class="fc-view">VIEW →</a>'
src = src.replace(old_card_view, new_card_view)

# ── §B.16 SKU card image: add hero photo ─────────────────────────────────────
old_fc_img = '''                <div class="fc-img">
                  <span class="fc-watermark">{sku.name}</span>
                </div>'''
new_fc_img = '''                <div class="fc-img">
                  <img
                    src={`/products/${sku.id.replace('sku-','').replace(/-q$/,'').replace(/-/g,'').replace(/\//g,'')}/assets/${sku.id.replace('sku-','').replace(/-q$/,'')}-001_white.png`}
                    alt={sku.name}
                    loading="lazy"
                    style="max-width:100%;max-height:100%;object-fit:contain;opacity:0.85;"
                    onerror="this.style.display='none';this.nextElementSibling.style.display='block';"
                  />
                  <span class="fc-watermark" style="display:none;">{sku.name}</span>
                </div>'''
src = src.replace(old_fc_img, new_fc_img)

# ── §B.17 Remove the duplicate sku-em20-cmb-260dc-q id issue ─────────────────
# The id 'sku-em20-cmb-260dc-q' is a duplicate entry for the quick tier — keep it distinct
# No further action needed since we already gave it a unique id

# ── Verify changes ────────────────────────────────────────────────────────────
if src == orig:
    print("WARNING: No changes made!")
else:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(src)
    
    # Count replacements
    changes = 0
    for old, new in [
        ('20 active driver SKUs', '20 active driver SKUs'),
    ]:
        if new in src:
            changes += 1
    
    print(f"OK: File updated. Spot-check:")
    print(f"  '20 active driver SKUs' in src: {'20 active driver SKUs' in src}")
    print(f"  '20 drivers. One ecosystem.' in src: {'20 drivers. One ecosystem.' in src}")
    print(f"  'LIVE · 20 SKUS' in src: {'LIVE · 20 SKUS' in src}")
    print(f"  '/products/em20-cmb260dc/' in src: {'/products/em20-cmb260dc/' in src}")
    print(f"  'EM07-CMB/260DC' in src: {'EM07-CMB/260DC' in src}")
    print(f"  'EM20-HMB/135AC' in src: {'EM20-HMB/135AC' in src}")
    print(f"  'EM08-AMB/48DC' in src: {'EM08-AMB/48DC' in src}")
    print(f"  'sku.pdp' in src: {'sku.pdp' in src}")
