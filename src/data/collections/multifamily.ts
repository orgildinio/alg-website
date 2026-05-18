/**
 * src/data/collections/multifamily.ts
 * Static data for the multi-fⒶMILY collection page.
 * Typed against CollectionPageLayout.astro Props['collection'].
 *
 * §A1 canonical: 8 families · 59 SKUs · 4 applications.
 * Wally removed. Crescent removed. Radius-II kept (Recessed Downlights).
 * Gehry echelon: PRO. Orbit renamed to Orbit-I.
 * C5: Featured heading corrected to "Three flagship families".
 * C6: Browse-by-Application tiles wired via appMulti field.
 */
const multifamilyData = {
  slug: 'multifamily',
  searchKeywords: 'multi-family,apartment,condo,property management,low-glare,downlight,puck light,recess can,wall sconce,balcony lighting,corridor lighting,stairwell lighting,fixture-only,wireless control',
  parentVertical: 'Residential',
  parentSubVertical: 'Multi-Family',
  name: 'multi-fⒶMILY',
  titleAscii: 'MULTIFAMILY',
  headlineLine: 'multi-f<span class="aa">Ⓐ</span>MILY',
  description: 'Multifamily, garden-style, and mid-rise developments need lighting that works on a per-door budget — and still passes the code inspector on the first walk-through. multi-f<span class="aa">Ⓐ</span>MILY is the ALG line that ships value-engineered ECO and code-compliant PRO downlights, hallway fixtures, and unit basics with the per-door affordability developers run on.',
  pillRow: ['VALUE-ENGINEERED', 'CODE-COMPLIANT', 'JA8 / TITLE 24', '48-HR LAYOUTS', '5-YR WARRANTY'],
  statStrip: [
    { value: '~$12', label: '/ door' },
    { value: '5-yr', label: 'Warranty' },
    { value: 'JA8',  label: 'Title 24' },
    { value: '48-hr',label: 'Layouts' },
  ],
  // C1: Updated to 8 families · 59 SKUs · 4 applications (Wally removed, new taxonomy)
  redBanner: [
    { value: '8',   label: 'Families'     },
    { value: '59',  label: 'Active SKUs'  },
    { value: '4',   label: 'Applications' },
    { value: 'DLC', label: 'Premium'      },
    { value: 'TAA', label: 'Available'    },
    { value: '5 US',label: 'Warehouses'   },
  ],
  // C2: 4-bucket application taxonomy per §A2 (canonical)
  // appMulti maps to the sub_category values in sku-index.json (comma-separated)
  // C6: skuCount updated per §A2 canonical counts
  applications: [
    {
      name: 'Housing Cans',
      slug: 'housing-cans',
      skuCount: 8,
      appMulti: 'Housing Cans',
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>',
    },
    {
      name: 'Recessed Downlights',
      slug: 'recessed-downlights',
      skuCount: 22,
      appMulti: 'Recessed Downlights',
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/></svg>',
    },
    {
      name: 'SafeZone Downlights',
      slug: 'safezone-downlights',
      skuCount: 8,
      appMulti: 'SafeZone Downlights',
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>',
    },
    {
      name: 'Surface Mount',
      slug: 'surface-mount',
      skuCount: 21,
      appMulti: 'Surface Mount',
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
    },
  ],
  // C5: familiesHeadline updated to reflect 8 total families
  featured: [
    {
      family: 'Nebula-II',
      subCategory: 'Recessed Downlights',
      displayEchelon: 'ECO' as const,
      maxWattage: 20,
      skuCount: 12,
      dlc: true,
      lineDrawing: '/products/multi-family/card-images/nebula-ii-card.png',
      pdpUrl: '/products/multi-family/nebula-ii/',
    },
    {
      family: 'Eclipse-II',
      subCategory: 'Surface Mount',
      displayEchelon: 'PRO' as const,
      maxWattage: 18,
      skuCount: 13,
      dlc: true,
      lineDrawing: '/products/multi-family/card-images/eclipse-ii-card.png',
      pdpUrl: '/products/multi-family/eclipse-ii/',
    },
    {
      family: 'Radius SafeZone',
      subCategory: 'SafeZone Downlights',
      displayEchelon: 'PRO+' as const,
      maxWattage: 15,
      skuCount: 8,
      dlc: true,
      lineDrawing: '/products/multi-family/card-images/radius-safezone-card.png',
      pdpUrl: '/products/multi-family/radius-safezone/',
    },
  ],
  featuredHeadline: 'Three flagship families from the multi-fAMILY collection.',
  familiesHeadline: 'Eight families from the multi-fAMILY collection.',
  familiesSubhead: 'Multifamily, garden-style, and mid-rise developments need lighting that works on a per-door budget — and still passes the code inspector on the first walk-through.',
  legacy: {
    headline: 'Discontinued families.',
    body: 'Some earlier multi-fAMILY families have been discontinued. Replacement recommendations are available — contact your rep or distributor for guidance.',
    notifyLink: '/contact',
  },
  getStarted: {
    layoutCopy: 'Submit a project address and fixture list. Our team returns a complete photometric layout within 48 hours.',
    sampleCopy: 'Request a physical sample of any active multi-fAMILY family. Ships from a US warehouse within 3 business days.',
    distributorCopy: 'Find a stocking distributor near your project site. All 5 US warehouses carry core multi-fAMILY SKUs.',
    repCopy: 'Connect with a local sales rep for specification support, pricing, and project tracking.',
  },
  relatedCollections: [
    {
      slug: 'planoarch',
      name: 'plano<span class="aa">Ⓐ</span>RCH',
      vertical: 'Indoor',
      description: 'Commercial indoor lighting for offices, retail, and healthcare.',
      status: 'live' as const,
    },
    {
      slug: 'luxoarch',
      name: 'luxo<span class="aa">Ⓐ</span>RCH',
      vertical: 'Outdoor',
      description: 'Outdoor lighting for the commercial perimeter.',
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
      slug: 'cityarch',
      name: 'city<span class="aa">Ⓐ</span>RCH',
      vertical: 'Municipal',
      description: 'Street and area lighting for municipal and utility applications.',
      status: 'live' as const,
    },
  ],
};
export default multifamilyData;
