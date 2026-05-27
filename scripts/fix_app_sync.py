#!/usr/bin/env python3
"""
fix_app_sync.py — Synchronize mega-menu application links with collection page application filters.

Changes:
1. planoARCH data: slug fixes (panels→panel, commercial-downlight→downlight, etc.)
   + add missing: stairwell-passageway, general-purpose-strips
   + add missing from collection: track-light, wraparound, retrofit-panel, retrofit-troffer
   Mega-menu: fix slugs to match data file slugs

2. lamparARCH data: replace market-vertical apps with application-name apps
   (Linear High Bay, Round High Bay, Linear Strip, Retrofit Linear Strip, Vapor-Tight)
   Mega-menu: replace washdown with Linear Strip, Retrofit Linear Strip, Vapor-Tight

3. luxoARCH data: add decorative application
   Mega-menu: add cylinder, dock-light, string-light

4. cityARCH data: add street-sign; fix traffic-control-lamp slug to traffic-control-lamps
   Mega-menu: add pole; fix traffic-control-lamps slug

5. All mega-menu planoARCH links: fix ?application= slugs to match data file slugs
"""

import re

# ============================================================
# 1. planoARCH data — the collection page already has the right slugs.
#    We need to add stairwell-passageway and general-purpose-strips.
# ============================================================
planoarch_path = '/home/ubuntu/alg-website/src/data/collections/planoarch.ts'
with open(planoarch_path) as f:
    content = f.read()

# Add stairwell-passageway and general-purpose-strips after wraparound
new_apps = """    {
      name: 'Stairwell & Passageway',
      slug: 'stairwell-passageway',
      skuCount: 8,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h4v-4h4v-4h4v-4h4V3"/><path d="M3 21V3"/></svg>',
    },
    {
      name: 'General Purpose Strips',
      slug: 'general-purpose-strips',
      skuCount: 12,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="10" width="20" height="4" rx="1"/><line x1="6" y1="10" x2="6" y2="14"/><line x1="10" y1="10" x2="10" y2="14"/><line x1="14" y1="10" x2="14" y2="14"/><line x1="18" y1="10" x2="18" y2="14"/></svg>',
    },
  ],"""

# Replace the closing of the applications array
content = content.replace(
    """    {
      name: 'Wraparound',
      slug: 'wraparound',
      skuCount: 17,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V8a2 2 0 012-2z"/><path d="M4 6c0-1.1.9-2 2-2h12a2 2 0 012 2"/></svg>',
    },
  ],""",
    """    {
      name: 'Wraparound',
      slug: 'wraparound',
      skuCount: 17,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V8a2 2 0 012-2z"/><path d="M4 6c0-1.1.9-2 2-2h12a2 2 0 012 2"/></svg>',
    },
""" + new_apps
)

with open(planoarch_path, 'w') as f:
    f.write(content)
print("✅ planoarch.ts: added stairwell-passageway, general-purpose-strips")

# ============================================================
# 2. lamparARCH data — replace 3 market apps with 5 application apps
# ============================================================
lampararch_path = '/home/ubuntu/alg-website/src/data/collections/lampararch.ts'
with open(lampararch_path) as f:
    content = f.read()

old_apps = """  applications: [
    {
      name: 'Warehouse & Distribution',
      slug: 'warehouse-distribution',
      skuCount: 56,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="10" r="4"/><path d="M12 2v2M12 18v4M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M2 10h2M20 10h2M4.22 15.78l1.42-1.42M18.36 5.64l1.42-1.42"/><path d="M8 14l-2 6h12l-2-6"/></svg>',
    },
    {
      name: 'Manufacturing',
      slug: 'manufacturing',
      skuCount: 46,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="8" width="20" height="8" rx="1"/><line x1="6" y1="8" x2="6" y2="16"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="18" y1="8" x2="18" y2="16"/></svg>',
    },
    {
      name: 'Big-box retail / commercial',
      slug: 'big-box-retail',
      skuCount: 15,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="3" y1="15" x2="21" y2="15"/><line x1="9" y1="3" x2="9" y2="21"/><line x1="15" y1="3" x2="15" y2="21"/></svg>',
    },
  ],"""

new_apps_lampar = """  applications: [
    {
      name: 'Linear High Bay',
      slug: 'linear-high-bay',
      skuCount: 20,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="9" width="20" height="6" rx="1"/><line x1="12" y1="2" x2="12" y2="9"/><line x1="8" y1="4" x2="8" y2="9"/><line x1="16" y1="4" x2="16" y2="9"/></svg>',
    },
    {
      name: 'Round High Bay',
      slug: 'round-high-bay',
      skuCount: 24,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="10" r="6"/><line x1="12" y1="16" x2="12" y2="22"/><line x1="8" y1="19" x2="16" y2="19"/></svg>',
    },
    {
      name: 'Linear Strip',
      slug: 'linear-strip',
      skuCount: 8,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="10" width="20" height="4" rx="1"/><line x1="6" y1="10" x2="6" y2="14"/><line x1="12" y1="10" x2="12" y2="14"/><line x1="18" y1="10" x2="18" y2="14"/></svg>',
    },
    {
      name: 'Retrofit Linear Strip',
      slug: 'retrofit-linear-strip',
      skuCount: 6,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="10" width="20" height="4" rx="1"/><path d="M9 10l-2-4M15 10l2-4"/><path d="M7 14l-2 4M17 14l2 4"/></svg>',
    },
    {
      name: 'Vapor-Tight',
      slug: 'vapor-tight',
      skuCount: 12,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="8" width="20" height="8" rx="3"/><line x1="6" y1="8" x2="6" y2="16"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="18" y1="8" x2="18" y2="16"/></svg>',
    },
  ],"""

content = content.replace(old_apps, new_apps_lampar)
# Also update the redBanner Applications count
content = content.replace("{ value: '2',   label: 'Applications' }", "{ value: '5',   label: 'Applications' }")

with open(lampararch_path, 'w') as f:
    f.write(content)
print("✅ lampararch.ts: replaced market apps with 5 application-name apps")

# ============================================================
# 3. luxoARCH data — add decorative application
# ============================================================
luxoarch_path = '/home/ubuntu/alg-website/src/data/collections/luxoarch.ts'
with open(luxoarch_path) as f:
    content = f.read()

# Add decorative after wall-pack
content = content.replace(
    """    {
      name: 'Wall Pack',
      slug: 'wall-pack',
      skuCount: 46,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 9h6M9 12h6M9 15h4"/></svg>',
    },
  ],""",
    """    {
      name: 'Wall Pack',
      slug: 'wall-pack',
      skuCount: 46,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 9h6M9 12h6M9 15h4"/></svg>',
    },
    {
      name: 'Decorative',
      slug: 'decorative',
      skuCount: 4,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
    },
  ],"""
)

with open(luxoarch_path, 'w') as f:
    f.write(content)
print("✅ luxoarch.ts: added decorative application")

# ============================================================
# 4. cityARCH data — add street-sign; fix traffic-control-lamp slug
# ============================================================
cityarch_path = '/home/ubuntu/alg-website/src/data/collections/cityarch.ts'
with open(cityarch_path) as f:
    content = f.read()

# Fix traffic-control-lamp slug to traffic-control-lamps
content = content.replace(
    "      slug: 'traffic-control-lamp',",
    "      slug: 'traffic-control-lamps',"
)
content = content.replace(
    "      name: 'Traffic Control Lamp',",
    "      name: 'Traffic Control Lamps',"
)

# Add street-sign after roadway
content = content.replace(
    """    {
      name: 'Traffic Control Lamps',
      slug: 'traffic-control-lamps',""",
    """    {
      name: 'Street Sign',
      slug: 'street-sign',
      skuCount: 5,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="8" width="20" height="8" rx="1"/><line x1="12" y1="2" x2="12" y2="8"/><line x1="12" y1="16" x2="12" y2="22"/></svg>',
    },
    {
      name: 'Traffic Control Lamps',
      slug: 'traffic-control-lamps',"""
)

with open(cityarch_path, 'w') as f:
    f.write(content)
print("✅ cityarch.ts: added street-sign, fixed traffic-control-lamp slug")

# ============================================================
# 5. Header.astro — fix all mega-menu application slugs
# ============================================================
header_path = '/home/ubuntu/alg-website/src/components/Header.astro'
with open(header_path) as f:
    content = f.read()

# planoARCH: fix slug mismatches
# commercial-downlight → downlight
content = content.replace(
    'href="/collections/planoarch/index.html?application=commercial-downlight"',
    'href="/collections/planoarch/?application=downlight"'
)
content = content.replace(
    'data-preview-name="planoⒶRCH · Commercial Downlight"',
    'data-preview-name="planoⒶRCH · Downlight"'
)
content = content.replace(
    '>Commercial Downlight</a>',
    '>Downlight</a>'
)

# recessed-downlight-housing → downlight (same filter, housing is a sub-type of downlight)
# Actually keep as separate entry but fix the slug
content = content.replace(
    'href="/collections/planoarch/index.html?application=recessed-downlight-housing"',
    'href="/collections/planoarch/?application=downlight"'
)

# panels → panel
content = content.replace(
    'href="/collections/planoarch/index.html?application=panels"',
    'href="/collections/planoarch/?application=panel"'
)
content = content.replace(
    'data-preview-name="planoⒶRCH · Panels"',
    'data-preview-name="planoⒶRCH · Panel"'
)
content = content.replace(
    '>Panels</a>',
    '>Panel</a>'
)

# troffer — slug is already correct
content = content.replace(
    'href="/collections/planoarch/index.html?application=troffer"',
    'href="/collections/planoarch/?application=troffer"'
)

# retrofit-kits → retrofit-panel (primary retrofit) — keep label as "Retrofit"
content = content.replace(
    'href="/collections/planoarch/index.html?application=retrofit-kits"',
    'href="/collections/planoarch/?application=retrofit-panel"'
)
content = content.replace(
    'data-preview-name="planoⒶRCH · Retrofit Kits"',
    'data-preview-name="planoⒶRCH · Retrofit Panel"'
)
content = content.replace(
    '>Retrofit Kits</a>',
    '>Retrofit Panel</a>'
)

# stairwell-passageway — slug is correct, just fix path
content = content.replace(
    'href="/collections/planoarch/index.html?application=stairwell-passageway"',
    'href="/collections/planoarch/?application=stairwell-passageway"'
)

# general-purpose-strips — slug is correct, just fix path
content = content.replace(
    'href="/collections/planoarch/index.html?application=general-purpose-strips"',
    'href="/collections/planoarch/?application=general-purpose-strips"'
)

# architectural-linear — fix path
content = content.replace(
    'href="/collections/planoarch/index.html?application=architectural-linear"',
    'href="/collections/planoarch/?application=architectural-linear"'
)

# Add missing planoARCH apps: track-light, wraparound, retrofit-troffer
# Insert after the retrofit-panel line
content = content.replace(
    '''            <a href="/collections/planoarch/?application=retrofit-panel" class="mm-app-item" data-preview-tiers="1" data-tier-eco="" data-tier-pro="retroⒶRCH-P1" data-tier-proplus="" data-preview-name="planoⒶRCH · Retrofit Panel" data-preview-label="Indoor · Retrofit" data-preview-desc="Fluorescent-to-LED retrofit kits for existing troffer, strip, and wrap housings.">Retrofit Panel</a>''',
    '''            <a href="/collections/planoarch/?application=retrofit-panel" class="mm-app-item" data-preview-tiers="1" data-tier-eco="" data-tier-pro="retroⒶRCH-P1" data-tier-proplus="" data-preview-name="planoⒶRCH · Retrofit Panel" data-preview-label="Indoor · Retrofit" data-preview-desc="Fluorescent-to-LED retrofit kits for existing troffer, strip, and wrap housings.">Retrofit Panel</a>
            <a href="/collections/planoarch/?application=retrofit-troffer" class="mm-app-item" data-preview-tiers="1" data-tier-eco="" data-tier-pro="retroⒶRCH-T1" data-tier-proplus="" data-preview-name="planoⒶRCH · Retrofit Troffer" data-preview-label="Indoor · Retrofit Troffer" data-preview-desc="Fluorescent-to-LED retrofit kits for existing 2×2 and 2×4 troffer housings.">Retrofit Troffer</a>
            <a href="/collections/planoarch/?application=track-light" class="mm-app-item" data-preview-name="planoⒶRCH · Track Light" data-preview-label="Indoor · Track" data-preview-desc="Track lighting heads and systems for accent and display lighting.">Track Light</a>
            <a href="/collections/planoarch/?application=wraparound" class="mm-app-item" data-preview-name="planoⒶRCH · Wraparound" data-preview-label="Indoor · Wraparound" data-preview-desc="Wraparound fixtures for utility, stairwell, and back-of-house applications.">Wraparound</a>'''
)

# lamparARCH: replace washdown with linear-strip, retrofit-linear-strip, vapor-tight
content = content.replace(
    '''            <a href="/collections/lamparch/?application=linear-high-bay" class="mm-app-item" data-preview-tiers="1" data-tier-eco="" data-tier-pro="Titan" data-tier-proplus="Valkyrie-II" data-preview-name="lamparⒶRCH · Linear High Bay" data-preview-label="Industrial · Linear HB" data-preview-desc="Linear high-bay fixtures for warehouses, manufacturing, and retail back-of-house.">Linear High Bay</a>
            <a href="/collections/lamparch/?application=round-high-bay" class="mm-app-item" data-preview-tiers="1" data-tier-eco="Icarus" data-tier-pro="Jupiter" data-tier-proplus="Millennium-I" data-preview-name="lamparⒶRCH · Round High Bay" data-preview-label="Industrial · Round HB" data-preview-desc="UFO-form round high bays for open-ceiling industrial spaces. Up to 60,000 lumens per fixture.">Round High Bay</a>
            <a href="/collections/lamparch/?application=washdown" class="mm-app-item" data-preview-tiers="1" data-tier-eco="Eureka-II" data-tier-pro="Eureka-I" data-tier-proplus="Poseidon-I" data-preview-name="lamparⒶRCH · Washdown" data-preview-label="Industrial · Washdown" data-preview-desc="IP69K-rated washdown fixtures for food-processing, commercial kitchen, and pharmaceutical environments.">Washdown</a>''',
    '''            <a href="/collections/lamparch/?application=linear-high-bay" class="mm-app-item" data-preview-tiers="1" data-tier-eco="" data-tier-pro="Titan" data-tier-proplus="" data-preview-name="lamparⒶRCH · Linear High Bay" data-preview-label="Industrial · Linear HB" data-preview-desc="Linear high-bay fixtures for warehouses, manufacturing, and retail back-of-house. Titan up to 155W.">Linear High Bay</a>
            <a href="/collections/lamparch/?application=round-high-bay" class="mm-app-item" data-preview-tiers="1" data-tier-eco="Icarus" data-tier-pro="Jupiter" data-tier-proplus="" data-preview-name="lamparⒶRCH · Round High Bay" data-preview-label="Industrial · Round HB" data-preview-desc="UFO-form round high bays for open-ceiling industrial spaces. Up to 60,000 lumens per fixture.">Round High Bay</a>
            <a href="/collections/lamparch/?application=linear-strip" class="mm-app-item" data-preview-tiers="1" data-tier-eco="Hallmark" data-tier-pro="" data-tier-proplus="" data-preview-name="lamparⒶRCH · Linear Strip" data-preview-label="Industrial · Strip" data-preview-desc="Surface and suspended linear strip fixtures for utility and back-of-house applications.">Linear Strip</a>
            <a href="/collections/lamparch/?application=retrofit-linear-strip" class="mm-app-item" data-preview-tiers="1" data-tier-eco="" data-tier-pro="retroⒶRCH-L1" data-tier-proplus="" data-preview-name="lamparⒶRCH · Retrofit Linear Strip" data-preview-label="Industrial · Retrofit Strip" data-preview-desc="Drop-in LED retrofit kits for existing fluorescent linear strip housings.">Retrofit Linear Strip</a>
            <a href="/collections/lamparch/?application=vapor-tight" class="mm-app-item" data-preview-tiers="1" data-tier-eco="Eureka-II" data-tier-pro="Eureka-I" data-tier-proplus="" data-preview-name="lamparⒶRCH · Vapor-Tight" data-preview-label="Industrial · Vapor-Tight" data-preview-desc="IP65/IP66 vapor-tight fixtures for wet, damp, and washdown environments.">Vapor-Tight</a>'''
)

# luxoARCH: add cylinder, dock-light, string-light to mega-menu
# Insert after sports-lighting
content = content.replace(
    '''            <a href="/collections/luxoarch/index.html?application=sports-lighting" class="mm-app-item" data-preview-tiers="1" data-tier-eco="Radiator-III" data-tier-pro="Illuminator-I" data-tier-proplus="" data-preview-name="luxoⒶRCH · Sports Lighters" data-preview-label="Outdoor · Sports" data-preview-desc="Sports lighters for outdoor athletic venues. Broadcast-grade visual comfort with precision optics.">Sports Lighters</a>''',
    '''            <a href="/collections/luxoarch/?application=sports-lighting" class="mm-app-item" data-preview-tiers="1" data-tier-eco="Radiator-III" data-tier-pro="Illuminator-I" data-tier-proplus="" data-preview-name="luxoⒶRCH · Sports Lighters" data-preview-label="Outdoor · Sports" data-preview-desc="Sports lighters for outdoor athletic venues. Broadcast-grade visual comfort with precision optics.">Sports Lighters</a>
            <a href="/collections/luxoarch/?application=cylinder" class="mm-app-item" data-preview-tiers="1" data-tier-eco="" data-tier-pro="Aura-I" data-tier-proplus="" data-preview-name="luxoⒶRCH · Cylinder" data-preview-label="Outdoor · Cylinder" data-preview-desc="Cylinder luminaires for architectural accent and façade lighting.">Cylinder</a>
            <a href="/collections/luxoarch/?application=dock-light" class="mm-app-item" data-preview-tiers="1" data-tier-eco="" data-tier-pro="Canadarm-I" data-tier-proplus="" data-preview-name="luxoⒶRCH · Dock Light" data-preview-label="Outdoor · Dock" data-preview-desc="Articulating dock lights for loading docks and freight handling areas.">Dock Light</a>
            <a href="/collections/luxoarch/?application=string-light" class="mm-app-item" data-preview-name="luxoⒶRCH · String Light" data-preview-label="Outdoor · String" data-preview-desc="Commercial-grade outdoor string lights for hospitality, events, and amenity areas.">String Light</a>'''
)

# Fix remaining luxoARCH links to use clean paths (remove index.html)
content = content.replace(
    'href="/collections/luxoarch/index.html?application=',
    'href="/collections/luxoarch/?application='
)

# cityARCH: add pole; fix traffic-control-lamps slug (already correct in mega-menu)
# Add pole after high-mast
content = content.replace(
    '''            <a href="/collections/cityarch/index.html?application=high-mast" class="mm-app-item" data-preview-tiers="1" data-tier-eco="" data-tier-pro="" data-tier-proplus="OmniMax-I" data-preview-name="cityⒶRCH · High-Mast" data-preview-label="Municipal · High-Mast" data-preview-desc="High-mast fixtures for roadway interchanges, seaports, and large open-area applications.">High-Mast</a>''',
    '''            <a href="/collections/cityarch/?application=high-mast" class="mm-app-item" data-preview-tiers="1" data-tier-eco="" data-tier-pro="" data-tier-proplus="OmniMax-I" data-preview-name="cityⒶRCH · High-Mast" data-preview-label="Municipal · High-Mast" data-preview-desc="High-mast fixtures for roadway interchanges, seaports, and large open-area applications.">High-Mast</a>
            <a href="/collections/cityarch/?application=pole" class="mm-app-item" data-preview-tiers="1" data-tier-eco="" data-tier-pro="" data-tier-proplus="" data-preview-name="cityⒶRCH · Pole" data-preview-label="Municipal · Pole" data-preview-desc="Pole-mount luminaires for parking lots, roadways, and commercial outdoor areas.">Pole</a>'''
)

# Fix remaining cityARCH links to use clean paths
content = content.replace(
    'href="/collections/cityarch/index.html?application=',
    'href="/collections/cityarch/?application='
)

with open(header_path, 'w') as f:
    f.write(content)
print("✅ Header.astro: all mega-menu application links fixed and synced")

print("\nDone. All application sync changes applied.")
