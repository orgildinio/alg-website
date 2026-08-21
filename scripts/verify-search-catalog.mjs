import { readFileSync, readdirSync } from 'node:fs';

const catalog = JSON.parse(readFileSync(new URL('../public/search-catalog.json', import.meta.url), 'utf8'));
if (!catalog.records.site?.some(record => record.url.endsWith('/blog/'))) throw new Error('Search catalog is missing the blog index record');

function requiredProduct(title) {
  const record = catalog.records.products.find(item => item.title === title);
  if (!record) throw new Error(`Missing required Product record: ${title}`);
  console.log(`${title} -> ${record.url} | ${record.aliases.join(', ')}`);
}

requiredProduct('Liberty Series');
requiredProduct('Heritage Series');
requiredProduct('Husk Series');

const areaLuminaire = catalog.records.applications.find(item => item.title === 'Area Luminaire');
if (!areaLuminaire) throw new Error('Missing required Application record: Area Luminaire');
console.log(`Area Luminaire -> ${areaLuminaire.url} | ${areaLuminaire.aliases.join(', ')}`);

function normalized(value) {
  return String(value || '').replace(/Ⓐ/g, 'a').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
}
function matches(record, query) {
  const q = normalized(query);
  const haystack = [record.title, ...(record.aliases || [])].map(normalized).join(' ');
  return q.split(' ').every(token => haystack.includes(token));
}
function requireMatch(group, query, title) {
  const record = catalog.records[group].find(item => item.title === title && matches(item, query));
  if (!record) throw new Error(`Query ${query} does not surface ${title} in ${group}`);
}

requireMatch('products', 'liberty', 'Liberty Series');
requireMatch('products', 'area light', 'Liberty Series');
requireMatch('products', 'area light', 'Heritage Series');
requireMatch('applications', 'area light', 'Area Luminaire');
requireMatch('products', 'husk', 'Husk Series');

const allowedExternalUrls = new Set(['https://careers.archipelagolighting.com/']);
for (const group of Object.values(catalog.records)) {
  for (const record of group) {
    if (!/^https:\/\/www\.archipelagolighting\.com\//.test(record.url) && !allowedExternalUrls.has(record.url)) {
      throw new Error(`Non-canonical URL in catalog: ${record.title} -> ${record.url}`);
    }
  }
}

const blogFiles = readdirSync(new URL('../src/content/blog/', import.meta.url))
  .filter(file => file.endsWith('.md'));
if (blogFiles.length < 6) throw new Error(`Expected at least six blog articles; found ${blogFiles.length}`);
if (catalog.records.site.filter(record => record.url.includes('/blog/')).length !== blogFiles.length + 1) {
  throw new Error('Search catalog does not include the blog index plus every current blog article');
}

const packageJson = JSON.parse(readFileSync(new URL('../package.json', import.meta.url), 'utf8'));
if (!packageJson.scripts?.['cf-build']?.includes('build-search-catalog.mjs')) {
  throw new Error('cf-build does not regenerate the catalog search data');
}
if (!packageJson.scripts?.['cf-build']?.includes('astro build')) {
  throw new Error('cf-build does not run Astro and its Pagefind integration');
}

console.log(`Verified ${blogFiles.length} blog articles plus the blog index are included in the generated and Pagefind production-build paths.`);
console.log(`Verified ${catalog.records.products.length} products, ${catalog.records.applications.length} applications, and ${catalog.records.collections.length} collections.`);
