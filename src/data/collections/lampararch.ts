/**
 * src/data/collections/lampararch.ts
 * Static data for the lamparⒶRCH collection page.
 * Typed against CollectionPageLayout.astro Props['collection'].
 */
const lampararchData = {
  slug: 'lampararch',
  parentVertical: 'Indoor',
  parentSubVertical: 'Industrial',
  name: 'lamparⒶRCH',
  titleAscii: 'LAMPARARCH',
  headlineLine: 'lampar<span class="aa">Ⓐ</span>RCH',
  description: 'Linear high-bay, low-bay, vapor-tight, and linear strip — DLC Premium-listed across the catalog, project-specified for warehouse, manufacturing, and distribution-center installs where lumen efficiency and 80,000+ hours of L80 matter. lampar<span class="aa">Ⓐ</span>RCH is the ALG line that ships when the photometric layout is the conversation.',
  pillRow: ['DLC PREMIUM', 'HIGH LUMEN EFFICIENCY', 'LONG PHOTOMETRIC THROW', 'PROJECT-SPECIFIED', '80,000-HR L80'],
  statStrip: [
    { value: '88.5k',label: 'up to lm' },
    { value: '150', label: 'lm/W' },
    { value: '80k-hr',label: 'L80' },
    { value: '48-hr',label: 'Layouts' },
  ],
  redBanner: [
    { value: '10',  label: 'Families'     },
    { value: '104', label: 'Active SKUs'  },
    { value: '6',   label: 'Applications' },
    { value: 'DLC', label: 'Premium'      },
    { value: 'TAA', label: 'Available'    },
    { value: '5 US',label: 'Warehouses'   },
  ],
  applications: [
    {
      name: 'Dock Light',
      slug: 'dock-light',
      skuCount: 2,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 2v4M12 18v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M2 12h4M18 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/></svg>',
    },
    {
      name: 'Linear High Bay',
      slug: 'linear-high-bay',
      skuCount: 20,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="9" width="20" height="6" rx="1"/><line x1="12" y1="2" x2="12" y2="9"/><line x1="8" y1="4" x2="8" y2="9"/><line x1="16" y1="4" x2="16" y2="9"/></svg>',
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
      name: 'Round High Bay',
      slug: 'round-high-bay',
      skuCount: 24,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="10" r="6"/><line x1="12" y1="16" x2="12" y2="22"/><line x1="8" y1="19" x2="16" y2="19"/></svg>',
    },
    {
      name: 'Vapor-Tight',
      slug: 'vapor-tight',
      skuCount: 12,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="8" width="20" height="8" rx="3"/><line x1="6" y1="8" x2="6" y2="16"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="18" y1="8" x2="18" y2="16"/></svg>',
    },
  ],
  featured: [
    {
      family: 'Titan-II',
      subCategory: 'Linear High-Bay',
      displayEchelon: 'PRO+' as const,
      maxWattage: 600,
      skuCount: 20,
      dlc: true,
      lineDrawing: null,
    },
    {
      family: 'Jupiter-II',
      subCategory: 'Linear Low-Bay',
      displayEchelon: 'PRO' as const,
      maxWattage: 200,
      skuCount: 12,
      dlc: true,
      lineDrawing: null,
    },
    {
      family: 'Icarus-III',
      subCategory: 'Vapor Tight',
      displayEchelon: 'PRO' as const,
      maxWattage: 150,
      skuCount: 12,
      dlc: true,
      lineDrawing: null,
    },
  ],
  familiesHeadline: 'The PRO line that earns the warehouse.',
  familiesSubhead: 'Linear high-bay, low-bay, vapor-tight, and linear strip — DLC Premium-listed across the catalog, project-specified for warehouse, manufacturing, and distribution-center installs.',
  legacy: {
    headline: 'Discontinued families.',
    body: 'Some earlier LAMPARARCH families have been discontinued. Industrial linear high-bay and low-bay luminaires. Replacement recommendations are available — contact your rep or distributor for guidance.',
    notifyLink: '/contact',
  },
  getStarted: {
    layoutCopy: 'Submit a project address and fixture list. Our team returns a complete photometric layout within 48 hours.',
    sampleCopy: 'Request a physical sample of any active LAMPARARCH family. Ships from a US warehouse within 3 business days.',
    distributorCopy: 'Find a stocking distributor near your project site. All 5 US warehouses carry core LAMPARARCH SKUs.',
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
      slug: 'cityarch',
      name: 'city<span class="aa">Ⓐ</span>RCH',
      vertical: 'Municipal',
      description: 'Street and area lighting for municipal and utility applications.',
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
export default lampararchData;
