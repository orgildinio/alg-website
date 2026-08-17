import { readdir, readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { JSDOM } from 'jsdom';

const DIST_DIR = 'dist';

async function walk(dir) {
  const entries = await readdir(dir, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) files.push(...await walk(path));
    else if (entry.name.endsWith('.html')) files.push(path);
  }
  return files;
}

function isIgnoredTextNode(node) {
  for (let parent = node.parentElement; parent; parent = parent.parentElement) {
    const tag = parent.tagName?.toLowerCase();
    if (tag === 'script' || tag === 'style' || tag === 'svg' || tag === 'text' || tag === 'tspan') return true;
    if (parent.classList?.contains('aa')) return true;
  }
  return false;
}

let wrapped = 0;
let skippedCssParseFiles = 0;
for (const file of await walk(DIST_DIR)) {
  const html = await readFile(file, 'utf8');
  let dom;
  try {
    dom = new JSDOM(html);
  } catch (error) {
    skippedCssParseFiles++;
    console.warn(`⚠ Glyph normalization skipped ${file}: jsdom could not parse unsupported CSS without terminating the build: ${error.message}`);
    continue;
  }
  const { document, NodeFilter } = dom.window;
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const textNodes = [];
  let node;
  while ((node = walker.nextNode())) {
    if (node.textContent.includes('Ⓐ') && !isIgnoredTextNode(node)) textNodes.push(node);
  }
  for (const textNode of textNodes) {
    const parts = textNode.textContent.split('Ⓐ');
    const fragment = document.createDocumentFragment();
    parts.forEach((part, index) => {
      if (part) fragment.append(document.createTextNode(part));
      if (index < parts.length - 1) {
        const mark = document.createElement('span');
        mark.className = 'aa';
        mark.textContent = 'Ⓐ';
        fragment.append(mark);
        wrapped++;
      }
    });
    textNode.parentNode.replaceChild(fragment, textNode);
  }
  await writeFile(file, dom.serialize());
}

console.log(`Canonicalized ${wrapped} rendered Ⓐ mark(s) as <span class="aa">Ⓐ</span>.`);
if (skippedCssParseFiles > 0) {
  console.warn(`⚠ Glyph normalization completed with ${skippedCssParseFiles} CSS-parse warning(s).`);
}
