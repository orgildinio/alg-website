/**
 * Build the structured catalog-search layer consumed by SearchModal.astro.
 *
 * Pagefind continues to crawl every HTML page after Astro builds, so normal
 * pages (including new blog posts) enter search automatically. This script
 * adds the product/application semantics that page-text search cannot infer.
 */
import { readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const DATA_PATH = join(ROOT, 'src', 'data', 'sku-index.json');
const HEADER_PATH = join(ROOT, 'src', 'components', 'Header.astro');
const BLOG_PATH = join(ROOT, 'src', 'content', 'blog');
const OUTPUT_PATH = join(ROOT, 'public', 'search-catalog.json');

const SITE = 'https://www.archipelagolighting.com';

const COLLECTION_META = {
  luxoarch: { title: 'luxoⒶRCH', url: '/collections/luxoarch/', aliases: ['outdoor lighting', 'commercial outdoor'] },
  cityarch: { title: 'cityⒶRCH', url: '/collections/cityarch/', aliases: ['municipal lighting', 'roadway lighting'] },
  planoarch: { title: 'planoⒶRCH', url: '/collections/planoarch/', aliases: ['commercial indoor lighting'] },
  lampararch: { title: 'lamparⒶRCH', url: '/collections/lamparch/', aliases: ['industrial lighting', 'high bay lighting'] },
  multifamily: { title: 'multi-fⒶMILY', url: '/collections/multi-family/', aliases: ['multi family lighting', 'residential lighting'] },
  tubulararch: { title: 'tubulⒶRCH', url: '/collections/tubulararch/', aliases: ['t8 retrofit', 't5 retrofit', 'led tube'] },
  'nostalgic-decor': { title: 'Nostalgic Décor', url: '/collections/nostalgic-decor/', aliases: ['decorative lamps', 'vintage lamps'] },
  'vintage-decor': { title: 'Vintage Décor', url: '/collections/vintage-decor/', aliases: ['decorative lamps', 'edison lamps'] },
  constant: { title: 'constⒶNT', url: '/collections/constant/', aliases: ['emergency lighting', 'exit signs', 'battery backup'] },
  controls: { title: 'contrⒶLS', url: '/collections/controls/', aliases: ['lighting controls', 'occupancy sensors'] },
};

const APPLICATION_SYNONYMS = {
  'area luminaire': ['area light', 'area lighting', 'shoebox light', 'parking lot light'],
  'canopy luminaire': ['canopy light', 'gas station light', 'drive thru light'],
  'cylinder': ['cylinder light', 'architectural cylinder'],
  'flood': ['flood light', 'floodlighting'],
  'sports lighters': ['sports light', 'sports lighting', 'stadium light'],
  'linear high bay': ['linear highbay', 'linear high-bay', 'warehouse light'],
  'round high bay': ['round highbay', 'ufo high bay', 'ufo light'],
  'roadway': ['roadway light', 'cobra head', 'street light'],
  'recessed downlights': ['recessed downlight', 'downlight'],
  'housing cans': ['recessed housing', 'can light'],
  'retrofit panel': ['panel retrofit', 'flat panel retrofit'],
  'retrofit troffer': ['troffer retrofit'],
};

const PRODUCT_OVERRIDES = [
  {
    title: 'Husk Series',
    url: '/collections/planoarch/husk/',
    aliases: ['Husk', 'Husk HID', 'HID retrofit', 'HID retrofit lamp'],
    breadcrumb: 'Products › Lamps › HID Retrofit',
  },
];

function cleanText(value = '') {
  return String(value)
    .replace(/<[^>]*>/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&#x27;/g, "'")
    .replace(/\s+/g, ' ')
    .trim();
}

function unique(values) {
  return [...new Set(values.filter(Boolean).map(value => cleanText(value)))];
}

function absolute(url) {
  return /^https?:\/\//.test(url) ? url : `${SITE}${url.startsWith('/') ? '' : '/'}${url}`;
}

function collectionTitle(key) {
  return COLLECTION_META[key]?.title || key.replace(/-/g, ' ').replace(/\b\w/g, char => char.toUpperCase());
}

function collectionUrl(key) {
  return COLLECTION_META[key]?.url || `/collections/${key}/`;
}

function extractApplications(header) {
  const records = [];
  const appRe = /<a\s+href="([^"]+)"\s+class="mm-app-item"([^>]*)>([\s\S]*?)<\/a>/g;
  let match;

  while ((match = appRe.exec(header))) {
    const [, href, attrs, inner] = match;
    const title = cleanText(inner).replace(/\s+(ECO|PRO\+|PRO)$/i, '').trim();
    const previewName = attrs.match(/data-preview-name="([^"]+)"/)?.[1] || '';
    const previewLabel = attrs.match(/data-preview-label="([^"]+)"/)?.[1] || '';
    const previewDesc = attrs.match(/data-preview-desc="([^"]+)"/)?.[1] || '';
    if (!title || !previewName) continue;

    const normalizedTitle = title.toLowerCase();
    const aliases = unique([
      title,
      previewName,
      previewLabel,
      previewDesc,
      ...(APPLICATION_SYNONYMS[normalizedTitle] || []),
    ]);
    const key = `${absolute(href)}|${title}`;
    if (!records.some(record => record.key === key)) {
      records.push({
        key,
        type: 'applications',
        title,
        url: absolute(href),
        aliases,
        breadcrumb: `Applications › ${cleanText(previewLabel || previewName)}`,
      });
    }
  }
  return records;
}

function frontmatterValue(source, key) {
  const quoted = source.match(new RegExp(`^${key}:\\s*["']([^"']+)["']\\s*$`, 'm'));
  if (quoted) return quoted[1].trim();
  const bare = source.match(new RegExp(`^${key}:\\s*([^\\n]+)$`, 'm'));
  return bare ? bare[1].trim() : '';
}

function extractBlogRecords() {
  const posts = readdirSync(BLOG_PATH)
    .filter(file => file.endsWith('.md'))
    .map(file => {
      const source = readFileSync(join(BLOG_PATH, file), 'utf8');
      const slug = file.replace(/\.md$/, '');
      const title = frontmatterValue(source, 'title');
      const category = frontmatterValue(source, 'category');
      const excerpt = frontmatterValue(source, 'excerpt');
      const date = frontmatterValue(source, 'date');
      return {
        type: 'site',
        title,
        url: absolute(`/blog/${slug}/`),
        aliases: unique([title, category, excerpt, date, 'blog', 'article']),
        breadcrumb: `Blog › ${category || 'Article'}`,
      };
    })
    .filter(record => record.title);

  return [{
    type: 'site',
    title: 'ALG Blog',
    url: absolute('/blog/'),
    aliases: ['blog', 'articles', 'lighting insights', 'spec notes', 'product news'],
    breadcrumb: 'Blog',
  }, ...posts];
}

const skuIndex = JSON.parse(readFileSync(DATA_PATH, 'utf8'));
const header = readFileSync(HEADER_PATH, 'utf8');
const products = [];
const collections = [];

for (const [collectionKey, collection] of Object.entries(skuIndex.collections || {})) {
  const meta = COLLECTION_META[collectionKey];
  if (meta) {
    collections.push({
      type: 'collections',
      title: meta.title,
      url: absolute(meta.url),
      aliases: unique([meta.title, collectionKey, ...meta.aliases]),
      breadcrumb: 'Collections',
    });
  }

  for (const family of collection.families || []) {
    if (!family.pdpUrl || family.pdp_ready === false || family.linkType === 'datasheet') continue;
    const title = `${family.family} Series`;
    const application = family.sub_category || '';
    const aliases = unique([
      family.family,
      title,
      family.slug,
      family.tierKey,
      family.zoho_family,
      application,
      ...(APPLICATION_SYNONYMS[application.toLowerCase()] || []),
    ]);
    const record = {
      type: 'products',
      title,
      url: absolute(family.pdpUrl),
      aliases,
      breadcrumb: `Products › ${collectionTitle(collectionKey)}${application ? ` › ${application}` : ''}`,
      tier: family.display_echelon || '',
    };
    if (!products.some(existing => existing.url === record.url && existing.title === record.title)) products.push(record);
  }
}

for (const override of PRODUCT_OVERRIDES) {
  if (!products.some(record => record.url === absolute(override.url))) {
    products.push({ type: 'products', tier: '', ...override, url: absolute(override.url) });
  }
}

const applications = extractApplications(header);
const site = extractBlogRecords();
const sortByTitle = (a, b) => a.title.localeCompare(b.title, 'en');
products.sort(sortByTitle);
collections.sort(sortByTitle);
applications.sort(sortByTitle);
site.sort(sortByTitle);

const output = {
  generatedAt: new Date().toISOString(),
  source: 'sku-index.json + Header.astro + src/content/blog',
  records: { products, applications, collections, site },
};

writeFileSync(OUTPUT_PATH, `${JSON.stringify(output, null, 2)}\n`, 'utf8');
console.log(`[build-search-catalog] Wrote ${OUTPUT_PATH}: ${products.length} products, ${applications.length} applications, ${collections.length} collections, ${site.length} blog/site records.`);
