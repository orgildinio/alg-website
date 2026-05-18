/**
 * src/data/collections/tubularch.ts
 * Static data for the tubulⒶRCH collection page.
 * Route: /collections/tubularch/
 * Typed against CollectionPageLayout.astro Props['collection'].
 */
const tubularchData = {
  slug: 'tubulararch',
  parentVertical: 'Lamps',
  parentSubVertical: '',
  name: 'tubul<span class="aa">Ⓐ</span>RCH',
  titleAscii: 'TUBULARCH',
  headlineLine: 'tubul<span class="aa">Ⓐ</span>RCH',
  description: 'Linear LED retrofit lamps in T5, T8, PL, PLL, and U-Bend form factors — UL Type A, Type B, and A+B hybrid. DLC-listed, ballast-compatible, and tested against 200+ ballast models.',
  pillRow: ['UL TYPE A+B', 'DLC LISTED', '200+ BALLASTS PROVEN', '50,000-HR L70', '5-YEAR WARRANTY'],
  statStrip: [
    { value: '5',       label: 'Form Factors'     },
    { value: '200+',    label: 'Ballasts Proven'  },
    { value: '50k-hr',  label: 'L70'              },
    { value: 'DLC',     label: 'SSL QPL Listed'   },
  ],
  redBanner: [
    { value: '5',       label: 'Families'         },
    { value: 'UL A+B',  label: 'Hybrid Type'      },
    { value: 'DLC',     label: 'QPL Listed'       },
    { value: '200+',    label: 'Ballasts Tested'  },
    { value: 'T5–T8',   label: 'Envelopes'        },
    { value: 'G13',     label: 'Base'             },
  ],
  applications: [
    {
      name: 'T8',
      slug: 't8',
      skuCount: 5,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="9" width="20" height="6" rx="1"/><line x1="6" y1="12" x2="18" y2="12"/></svg>',
    },
    {
      name: 'T5',
      slug: 't5',
      skuCount: 33,
      appMulti: 'T5HE,T5HO',
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="10" width="20" height="4" rx="1"/><line x1="5" y1="12" x2="19" y2="12"/></svg>',
    },
    {
      name: 'PL',
      slug: 'pl',
      skuCount: 6,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v10"/><path d="M8 3v10"/><path d="M7 13h10"/><path d="M12 13v8"/></svg>',
    },
    {
      name: 'PLL',
      slug: 'pll',
      skuCount: 3,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3v14"/><path d="M15 3v14"/><path d="M8 17h8"/><path d="M12 17v4"/></svg>',
    },
    {
      name: 'U6',
      slug: 'u6',
      skuCount: 3,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M7 3v10a5 5 0 0010 0V3"/></svg>',
    },
  ],
  featured: [
    {
      family: 'CW5 T8',
      subCategory: 'Workhorse T8',
      displayEchelon: 'PRO' as const,
      maxWattage: 18,
      skuCount: 5,
      dlc: true,
      lineDrawing: null,
    },
    {
      family: 'UVA T8',
      subCategory: 'Workhorse T8',
      displayEchelon: 'PRO' as const,
      maxWattage: 15,
      skuCount: 4,
      dlc: true,
      lineDrawing: null,
    },
    {
      family: 'EM5 T8',
      subCategory: 'Workhorse T8',
      displayEchelon: 'PRO' as const,
      maxWattage: 18,
      skuCount: 5,
      dlc: true,
      lineDrawing: null,
    },
  ],
  featuredHeadline: 'Five form factors from the tubulARCH collection.',
  familiesHeadline: 'Five form factors. One spec language.',
  familiesSubhead: 'T5, T8, PL, PLL, and U-Bend LED retrofit lamps — UL-certified, DLC-listed, ballast-tested.',
  legacy: {
    headline: 'Discontinued retrofit families.',
    body: 'Earlier tubul<span class="aa">Ⓐ</span>RCH families have been phased out. Replacement recommendations available — contact your rep.',
    notifyLink: '/contact',
  },
  getStarted: {
    layoutCopy: 'Submit your fixture schedule. Our team returns a retrofit recommendation with UL type and wattage for each row within 48 hours.',
    sampleCopy: 'Request a physical sample of any active tubul<span class="aa">Ⓐ</span>RCH family. Ships from a US warehouse within 3 business days.',
    distributorCopy: 'Find a stocking distributor near your project site.',
    repCopy: 'Connect with a local sales rep for specification support and project tracking.',
  },
  relatedCollections: [
    {
      slug: 'lampararch',
      name: 'lampar<span class="aa">Ⓐ</span>RCH',
      vertical: 'Industrial',
      description: 'High-bay and linear strip for warehouses and manufacturing.',
      status: 'live' as const,
    },
    {
      slug: 'planoarch',
      name: 'plano<span class="aa">Ⓐ</span>RCH',
      vertical: 'Indoor',
      description: 'Commercial LED troffers, panels, and downlights.',
      status: 'live' as const,
    },
    {
      slug: 'signature',
      name: 'sign<span class="aa">Ⓐ</span>TURE',
      vertical: 'Lamps',
      description: 'A-lamp, BR flood, PAR reflector, and HID retrofit.',
      status: 'live' as const,
    },
  ],
};
export default tubularchData;
