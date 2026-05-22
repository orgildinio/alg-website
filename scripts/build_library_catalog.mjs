#!/usr/bin/env node
/**
 * build_library_catalog.mjs
 *
 * Converts the raw WorkDrive URL Dashboard export (wd_url_dashboard.json)
 * into the normalized library_catalog.json consumed by src/pages/support/library.astro.
 *
 * EASY-UPDATE PATH (per v27x_LibraryPage prompt §5):
 *   1. In the WorkDrive URL Dashboard, add/edit document URLs and SKU counts.
 *   2. Click "Export JSON" → save as scripts/wd_url_dashboard.json
 *      (raw seedData shape: { collection: { "full | path | family": { sku_count, families, datasheet, install, quick, sell, ies } } })
 *   3. Run:  node scripts/build_library_catalog.mjs
 *   4. Commit the regenerated src/data/library_catalog.json
 *   5. Push → CF Pages rebuilds → page and all filter counts update automatically.
 *
 * No code edits needed. No hand-counting.
 *
 * Parsing rules (must match shipped library_catalog.json):
 *   - Collection = top-level JSON key (keep literal Ⓐ)
 *   - For each family entry, split full_path on '|', trim each segment
 *   - vertical  = segment[0]
 *   - application = segment[2] if present
 *   - tier = whichever segment ∈ {ECO, PRO, PRO+}
 *   - family = last segment
 *   - docs = each of {datasheet, install, quick, sell, ies} that is a non-empty string,
 *            mapped to { label: <canonical slot label>, url: <value> }
 *   - doc_count = number of populated slots
 *   - sku_count passes through
 *   - Facet counts: doc_type = families-with-that-slot; collection/vertical/tier = sum of doc_count
 */

import { readFileSync, writeFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const INPUT  = join(__dirname, 'wd_url_dashboard.json');
const OUTPUT = join(__dirname, '..', 'src', 'data', 'library_catalog.json');

const SLOT_LABELS = {
  datasheet: 'Datasheet',
  install:   'Install Guide',
  quick:     'Quick Sheet',
  sell:      'Sell Sheet',
  ies:       'IES Bundle',
};

const TIERS = new Set(['ECO', 'PRO', 'PRO+']);

function parseFamilyEntry(collection, fullPath, raw) {
  const segments = fullPath.split('|').map(s => s.trim());
  const vertical    = segments[0] || '';
  const application = segments[2] || '';
  const tier        = segments.find(s => TIERS.has(s)) || '';
  const family      = segments[segments.length - 1] || '';

  const docs = {};
  for (const slot of Object.keys(SLOT_LABELS)) {
    const url = raw[slot];
    if (url && typeof url === 'string' && url.trim() !== '') {
      docs[slot] = { label: SLOT_LABELS[slot], url: url.trim() };
    }
  }

  return {
    collection,
    vertical,
    application,
    tier,
    family,
    full_path: fullPath,
    sku_count: typeof raw.sku_count === 'number' ? raw.sku_count : (parseInt(raw.sku_count, 10) || 0),
    docs,
    doc_count: Object.keys(docs).length,
  };
}

function buildCatalog(rawData) {
  const catalog = [];

  for (const [collection, families] of Object.entries(rawData)) {
    for (const [fullPath, raw] of Object.entries(families)) {
      catalog.push(parseFamilyEntry(collection, fullPath, raw));
    }
  }

  return catalog;
}

function computeFacets(catalog) {
  // doc_type: families with that slot populated
  const docType = {};
  for (const slot of Object.keys(SLOT_LABELS)) {
    docType[SLOT_LABELS[slot]] = catalog.filter(e => slot in e.docs).length;
  }

  // collection/vertical/tier: sum of doc_count
  const collection = {};
  const vertical   = {};
  const tier       = {};

  for (const entry of catalog) {
    collection[entry.collection] = (collection[entry.collection] || 0) + entry.doc_count;
    vertical[entry.vertical]     = (vertical[entry.vertical]     || 0) + entry.doc_count;
    tier[entry.tier]             = (tier[entry.tier]             || 0) + entry.doc_count;
  }

  return { collection, vertical, tier, doc_type: docType };
}

// ── Main ──────────────────────────────────────────────────────────────────────

let rawData;
try {
  rawData = JSON.parse(readFileSync(INPUT, 'utf8'));
} catch (err) {
  console.error(`ERROR: Could not read ${INPUT}`);
  console.error('  Make sure wd_url_dashboard.json is in the scripts/ directory.');
  console.error('  Export it from the WorkDrive URL Dashboard using the "Export JSON" button.');
  process.exit(1);
}

const catalog = buildCatalog(rawData);
const facets  = computeFacets(catalog);

const totalDocUrls = catalog.reduce((sum, e) => sum + e.doc_count, 0);
const output = {
  generated_from: `wd_url_dashboard.json (converted by build_library_catalog.mjs on ${new Date().toISOString().slice(0, 10)})`,
  slot_labels: SLOT_LABELS,
  totals: {
    collections:   new Set(catalog.map(e => e.collection)).size,
    family_groups: catalog.length,
    sku_count_sum: catalog.reduce((sum, e) => sum + e.sku_count, 0),
    doc_urls_total: totalDocUrls,
  },
  facets,
  catalog,
};

writeFileSync(OUTPUT, JSON.stringify(output, null, 2) + '\n', 'utf8');
console.log(`✓ Written to ${OUTPUT}`);
console.log(`  ${catalog.length} families · ${totalDocUrls} doc URLs`);
console.log('  Doc type counts:', Object.entries(facets.doc_type).map(([k,v]) => `${k}: ${v}`).join(' · '));
