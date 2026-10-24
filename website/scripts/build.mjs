import { cp, mkdir, readdir, readFile, rm, stat, writeFile } from 'node:fs/promises';
import { dirname, extname, join, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { checkSite } from './check.mjs';
import { writeCredits } from './credits.mjs';

const website = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const output = join(website, 'dist');
const publicRoot = join(website, 'public');
await rm(output, { recursive: true, force: true });
await mkdir(output, { recursive: true });
await cp(publicRoot, output, {
  recursive: true,
  filter: source => !relative(publicRoot, source).split(sep).some(part => part.startsWith('.')),
});
const manifest = JSON.parse(await readFile(join(output, 'layouts/manifest.json'), 'utf8'));
const familyLabels = { photography: 'PHOTOGRAPHY', reading: 'READING', information: 'INFORMATION' };
const layoutIndex = manifest.items.map((item, index) => {
  const number = String(index + 1).padStart(2, '0');
  const title = escapeHtml(item.title);
  const alt = escapeHtml(`${item.title}版式实景预览`);
  return `<a class="layout-index-card family-${item.family}" href="/layouts/?id=${encodeURIComponent(item.id)}" aria-label="查看版式 ${number} ${title}"><span class="layout-index-visual"><img src="${item.image}" width="620" height="877" loading="lazy" alt="${alt}"><span class="layout-index-no">${number}</span></span><span class="layout-index-caption"><strong>${title}</strong><small>${familyLabels[item.family] || 'EDITORIAL'}</small></span></a>`;
}).join('\n');
const homepage = await readFile(join(website, 'src/index.html'), 'utf8');
if (!homepage.includes('<!--LAYOUT_INDEX-->')) throw new Error('Homepage is missing the layout index placeholder.');
await writeFile(join(output, 'index.html'), homepage.replace('<!--LAYOUT_INDEX-->', layoutIndex));
await writeCredits(website, output);
// Only pages and selected public assets enter dist. The skill repository stays outside it.
await checkSite(output);
function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, character => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[character]));
}
async function bytesAt(directory) {
  let bytes = 0;
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    bytes += entry.isDirectory() ? await bytesAt(path) : (await stat(path)).size;
  }
  return bytes;
}
await writeFile(join(output, 'site-info.json'), JSON.stringify({
  name: 'Themes for PPT Master', type: 'static', layouts: manifest.items.length,
  routes: ['/', '/layouts/', '/image-credits'],
}, null, 2) + '\n');

// GitHub Pages serves project sites from /<repo>/, so root-absolute URLs need a prefix there.
// Vercel (and any root-domain host) leaves SITE_BASE unset and the output stays untouched.
const siteBase = normalizeBase(process.env.SITE_BASE);
if (siteBase) await applyBase(output, siteBase);

console.log(`Built website/dist: ${manifest.items.length} layouts, ${(await bytesAt(output) / 1024 / 1024).toFixed(1)} MB. No runtime dependencies.`);

function normalizeBase(raw) {
  const value = (raw ?? '').trim();
  if (!value || value === '/') return '';
  if (!value.startsWith('/') || value.startsWith('//')) {
    throw new Error(`SITE_BASE must be empty or a single leading slash path, got: ${value}`);
  }
  return value.replace(/\/+$/, '');
}

async function applyBase(root, base) {
  const files = [];
  const collect = async directory => {
    for (const entry of await readdir(directory, { withFileTypes: true })) {
      const path = join(directory, entry.name);
      if (entry.isDirectory()) await collect(path);
      else files.push(path);
    }
  };
  await collect(root);
  let rewritten = 0;
  for (const file of files) {
    if (!['.html', '.css', '.js', '.json'].includes(extname(file))) continue;
    const source = await readFile(file, 'utf8');
    const next = source.replace(/(["'])(\/(?!\/)[^"'<>\s\\]*)\1/g, (whole, quote, path) => {
      rewritten++;
      return `${quote}${base}${path}${quote}`;
    });
    if (next !== source) await writeFile(file, next);
  }
  console.log(`Applied SITE_BASE ${base}: ${rewritten} root-absolute URLs rewritten for a nested deploy.`);
}
