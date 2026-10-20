import { cp, mkdir, readdir, readFile, rm, stat, writeFile } from 'node:fs/promises';
import { dirname, join, relative, resolve, sep } from 'node:path';
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
await cp(join(website, 'src/index.html'), join(output, 'index.html'));
await writeCredits(website, output);
// Only pages and selected public assets enter dist. The skill repository stays outside it.
await checkSite(output);
async function bytesAt(directory) {
  let bytes = 0;
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    bytes += entry.isDirectory() ? await bytesAt(path) : (await stat(path)).size;
  }
  return bytes;
}
const manifest = JSON.parse(await readFile(join(output, 'layouts/manifest.json'), 'utf8'));
await writeFile(join(output, 'site-info.json'), JSON.stringify({
  name: 'Themes for PPT Master', type: 'static', layouts: manifest.items.length,
  routes: ['/', '/layouts/', '/image-credits'],
}, null, 2) + '\n');
console.log(`Built website/dist: ${manifest.items.length} layouts, ${(await bytesAt(output) / 1024 / 1024).toFixed(1)} MB. No runtime dependencies.`);
