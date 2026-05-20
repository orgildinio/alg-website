/**
 * src/data/collections/cityarch.ts
 * Static data for the cityⒶRCH collection page.
 * Typed against CollectionPageLayout.astro Props['collection'].
 *
 * NOTE: 5 Pole-type families (Alpine, Centurion, Hyperion, Redwood, Sequoia)
 * have display_echelon: null per James direction. Their family cards render
 * with no echelon badge.
 */
const cityarchData = {
  slug: 'cityarch',
  searchKeywords: 'municipal,roadway,post top,bollard,high mast,traffic lamp,street sign,DOT,municipal lighting,roadway luminaire,decorative post top,Type III roadway,Type V roadway',
  parentVertical: 'Outdoor',
  parentSubVertical: 'Municipal',
  name: 'cityⒶRCH',
  titleAscii: 'CITYARCH',
  headlineLine: 'city<span class="aa">Ⓐ</span>RCH',
  description: 'Street and roadway luminaires for municipal and utility applications. 7 active families, 81 active SKUs.',
  pillRow: ['DLC PREMIUM', 'TAA AVAILABLE', '5 US WAREHOUSES', '3-DAY DELIVERY', '6 APPLICATIONS'],
  statStrip: [
    { value: '7',   label: 'Fixture Families' },
    { value: '81',  label: 'Active SKUs'       },
    { value: '6',   label: 'Applications'      },
    { value: 'DLC', label: 'Premium Listed'    },
  ],
  redBanner: [
    { value: '7',   label: 'Families'     },
    { value: '81',  label: 'Active SKUs'  },
    { value: '6',   label: 'Applications' },
    { value: 'DLC', label: 'Premium'      },
    { value: 'TAA', label: 'Available'    },
    { value: '5 US',label: 'Warehouses'   },
  ],
  applications: [
    {
      name: 'Bollard',
      slug: 'bollard',
      skuCount: 22,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="2" width="6" height="8" rx="1"/><path d="M7 10h10l1 12H6L7 10z"/></svg>',
    },
    {
      name: 'High Mast',
      slug: 'high-mast',
      skuCount: 10,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="2" x2="12" y2="22"/><path d="M12 6l-6 4h12L12 6z"/><path d="M6 10l-2 2h16l-2-2"/></svg>',
    },
    {
      name: 'Post Top',
      slug: 'post-top',
      skuCount: 31,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="7" r="4"/><line x1="12" y1="11" x2="12" y2="22"/></svg>',
    },
    {
      name: 'Roadway',
      slug: 'roadway',
      skuCount: 23,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17l4-10h10l4 10H3z"/><line x1="12" y1="7" x2="12" y2="2"/></svg>',
    },
    {
      name: 'Street Sign Lamp',
      slug: 'street-sign-lamp',
      skuCount: 4,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="8" width="20" height="8" rx="1"/><line x1="12" y1="2" x2="12" y2="8"/><line x1="12" y1="16" x2="12" y2="22"/></svg>',
    },
    {
      name: 'Traffic Control Lamps',
      slug: 'traffic-control-lamps',
      skuCount: 3,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="7" y="2" width="10" height="20" rx="2"/><circle cx="12" cy="7" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="12" cy="17" r="2"/></svg>',
    },
  ],
  featured: [
    {
      family: 'Symmetry',
      subCategory: 'Post Top',
      displayEchelon: 'PRO' as const,
      maxWattage: null,
      skuCount: 29,
      dlc: true,
      lineDrawing: null,
      pdpUrl: '/products/lptp-symmetry-post-top/',
    },
    {
      family: 'OmniMax',
      subCategory: 'High Mast',
      displayEchelon: 'PRO+' as const,
      maxWattage: null,
      skuCount: 10,
      dlc: true,
      lineDrawing: null,
      pdpUrl: '/products/lhmf-omnimax-high-mast/',
    },
    {
      family: 'Abbey',
      subCategory: 'Roadway',
      displayEchelon: 'PRO' as const,
      maxWattage: null,
      skuCount: 11,
      dlc: true,
      lineDrawing: null,
      pdpUrl: '/products/lrdw-abbey-roadway/',
    },
    {
      family: 'Sentry',
      subCategory: 'Bollard',
      displayEchelon: 'PRO' as const,
      maxWattage: null,
      skuCount: 4,
      dlc: true,
      lineDrawing: null,
      pdpUrl: '/products/lbol-sentry-bollard/',
    },
  ],
  featuredHeadline: 'Four flagship families from the cityARCH collection.',
  familiesHeadline: '7 families. One municipal portfolio.',
  familiesSubhead: 'Filter by application, echelon, wattage, CCT, and more.',
  legacy: {
    headline: 'Discontinued families.',
    body: 'Some earlier CITYARCH families have been discontinued. Replacement recommendations are available — contact your rep or distributor for guidance.',
    notifyLink: '/contact',
  },
  getStarted: {
    layoutCopy: 'Submit a project address and fixture list. Our team returns a complete photometric layout within 48 hours.',
    sampleCopy: 'Request a physical sample of any active CITYARCH family. Ships from a US warehouse within 3 business days.',
    distributorCopy: 'Find a stocking distributor near your project site. All 5 US warehouses carry core CITYARCH SKUs.',
    repCopy: 'Connect with a local sales rep for specification support, pricing, and project tracking.',
  },
  relatedCollections: [
    {
      slug: 'luxoarch',
      name: 'luxo<span class="aa">Ⓐ</span>RCH',
      vertical: 'Outdoor',
      description: 'Outdoor lighting for the commercial perimeter.',
      status: 'live' as const,
    },
    {
      slug: 'planoarch',
      name: 'plano<span class="aa">Ⓐ</span>RCH',
      vertical: 'Indoor',
      description: 'Commercial indoor lighting for offices, retail, and healthcare.',
      status: 'live' as const,
    },
    {
      slug: 'lampararch',
      name: 'lampar<span class="aa">Ⓐ</span>RCH',
      vertical: 'Industrial',
      description: 'Industrial lighting for warehouses and manufacturing.',
      status: 'live' as const,
    },
    {
      slug: 'tubulararch',
      name: 'tubul<span class="aa">Ⓐ</span>RCH',
      vertical: 'Industrial',
      description: 'High-bay and low-bay lighting for industrial and warehouse spaces.',
      status: 'coming-soon' as const,
    },
  ],
};
export default cityarchData;
