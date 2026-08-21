import { readFileSync } from 'node:fs';

const source = readFileSync(new URL('../src/components/SearchModal.astro', import.meta.url), 'utf8');
const match = source.match(/<script>([\s\S]*?)<\/script>/);
if (!match) throw new Error('SearchModal.astro contains no browser script');

try {
  // Parse only; do not execute DOM-dependent browser code in Node.
  new Function(match[1]);
} catch (error) {
  throw new Error(`Search modal browser-script syntax error: ${error.message}`);
}

const required = [
  "['products','applications','collections','site'",
  "GROUP_LABELS = { products:'Products', applications:'Applications', collections:'Collections'",
  "fetch('/search-catalog.json'",
  "pfInstance.options({ basePath: '/_pagefind/' })",
  'function searchCatalog',
  'function comparableUrl',
  'async function doSearch',
];
for (const token of required) {
  if (!source.includes(token)) throw new Error(`Search modal is missing required catalog-search hook: ${token}`);
}

console.log('Search modal browser script parses and includes Products → Applications → Collections catalog hooks.');
