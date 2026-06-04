import { defineConfig } from 'astro/config';
import { execSync } from 'child_process';

// Astro config for ALG Website
// Output: static site
// Hosted by: Cloudflare Pages
// Source of truth: this repo on GitHub
//
// Per Playbook v2.0 §1: Manus generates Astro components, commits to GitHub,
// Cloudflare Pages auto-builds and deploys. There is no separate "publish" step.

// G1 BUILD HASH FIX (v2.7.13):
// Cloudflare Pages auto-injects CF_PAGES_COMMIT_SHA and CF_PAGES_BUILD_DATE as
// shell env vars during its own build, but they are NOT automatically available
// as import.meta.env.PUBLIC_* in Astro unless explicitly defined here via vite.define.
// By reading them at config-evaluation time and baking them into the static HTML
// via vite.define, the real SHA is embedded regardless of CF Pages env var propagation.
function resolveBuildHash() {
  if (process.env.CF_PAGES_COMMIT_SHA) return process.env.CF_PAGES_COMMIT_SHA;
  if (process.env.PUBLIC_BUILD_HASH) return process.env.PUBLIC_BUILD_HASH;
  try { return execSync('git rev-parse HEAD', { stdio: ['pipe','pipe','pipe'] }).toString().trim(); } catch { return 'dev'; }
}
function resolveBuildTime() {
  if (process.env.CF_PAGES_BUILD_DATE) return process.env.CF_PAGES_BUILD_DATE;
  if (process.env.PUBLIC_BUILD_TIME) return process.env.PUBLIC_BUILD_TIME;
  return new Date().toISOString();
}
const BUILD_HASH = resolveBuildHash();
const BUILD_TIME = resolveBuildTime();

// Pagefind integration: runs pagefind CLI after every static build.
// The index lands in dist/_pagefind/ and is served as part of the static site.
// Zero manual configuration — every new HTML file is indexed automatically.
function pagefindIntegration() {
  return {
    name: 'pagefind',
    hooks: {
      'astro:build:done': async ({ dir }) => {
        const { execSync: exec } = await import('node:child_process');
        const sitePath = dir.pathname.replace(/\/$/, '');
        console.log('[pagefind] Indexing', sitePath);
        exec(`node_modules/.bin/pagefind --site "${sitePath}" --output-path "${sitePath}/_pagefind"`, {
          stdio: 'inherit',
          cwd: process.cwd()
        });
      }
    }
  };
}

export default defineConfig({
  site: 'https://archipelagolighting.com',
  output: 'static',
  build: {
    format: 'directory'
  },
  trailingSlash: 'never',
  integrations: [pagefindIntegration()],
  // Compression handled by Cloudflare CDN — no in-build minification quirks
  vite: {
    server: {
      allowedHosts: true,
    },
    preview: {
      allowedHosts: true,
    },
    build: {
      rollupOptions: {
        // Pagefind is generated post-build and served as a static asset.
        // Externalizing prevents Vite from trying to resolve it at build time.
        external: ['/_pagefind/pagefind.js'],
      },
    },
    define: {
      // Bake the real SHA into static HTML at build time.
      // These override import.meta.env.PUBLIC_BUILD_HASH / PUBLIC_BUILD_TIME
      // so Footer.astro always gets the real value, not the 'dev' fallback.
      'import.meta.env.PUBLIC_BUILD_HASH': JSON.stringify(BUILD_HASH),
      'import.meta.env.PUBLIC_BUILD_TIME': JSON.stringify(BUILD_TIME),
      // Bake Clarity project ID at build time from CF Pages env var PUBLIC_CLARITY_ID.
      // Set PUBLIC_CLARITY_ID in CF Pages dashboard → Settings → Environment variables.
      'import.meta.env.PUBLIC_CLARITY_ID': JSON.stringify(process.env.PUBLIC_CLARITY_ID || ''),
    },
  },
});
