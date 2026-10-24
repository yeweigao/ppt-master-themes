import assert from 'node:assert/strict';
import { access, readFile, readdir, stat } from 'node:fs/promises';
import { dirname, extname, join, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';

const website = resolve(dirname(fileURLToPath(import.meta.url)), '..');
async function walk(directory) {
  const files = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) files.push(...await walk(path));
    else files.push(path);
  }
  return files;
}
export async function checkSite(root) {
  root = resolve(root);
  const files = await walk(root);
  const errors = [];
  let links = 0;
  for (const file of files) {
    if (!['.html', '.css', '.js', '.json'].includes(extname(file))) continue;
    const text = await readFile(file, 'utf8');
    if (/(?:127\.0\.0\.1|localhost|file:\/\/|\/Users\/|\/private\/)/.test(text)) errors.push(`${relative(root, file)}: local-machine path in public content`);
    if (['.html', '.css'].includes(extname(file))) {
      const refs = [...text.matchAll(/(?:src|href)\s*=\s*["']([^"']+)["']|url\(\s*["']?([^\s)'"\r\n]+)["']?\s*\)/g)];
      for (const match of refs) {
        const href = match[1] || match[2];
        if (/^(?:https?:|mailto:|tel:|data:|#)/.test(href)) continue;
        const url = new URL(href, `https://site.test/${relative(root, file).split(sep).join('/')}`);
        const path = resolve(root, '.' + decodeURIComponent(url.pathname));
        if (path !== root && !path.startsWith(root + sep)) { errors.push(`${href}: outside output`); continue; }
        try {
          const info = await stat(path);
          if (info.isDirectory()) await access(join(path, 'index.html'));
          links++;
        } catch { errors.push(`${relative(root, file)}: missing ${href}`); }
      }
    }
  }
  const manifest = JSON.parse(await readFile(join(root, 'layouts/manifest.json'), 'utf8'));
  assert.equal(manifest.items.length, 33, 'Expected the published 33-layout collection');
  assert.equal(new Set(manifest.items.map(item => item.id)).size, 33, 'Duplicate layout ids');
  for (const item of manifest.items) {
    for (const key of ['image', 'structure']) {
      assert.ok(item[key].startsWith('/layouts/'), `${item.id}: media must use a portable public URL`);
      try { await access(join(root, item[key])); } catch { errors.push(`${item.id}: missing ${item[key]}`); }
    }
  }
  const html = await readFile(join(root, 'index.html'), 'utf8');
  const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]);
  assert.equal(ids.length, new Set(ids).size, 'Duplicate home-page ids');
  for (const [, fragment] of html.matchAll(/href="#([^"]+)"/g)) {
    if (!ids.includes(fragment)) errors.push(`Missing home section #${fragment}`);
  }
  assert.ok(files.every(file => !relative(root, file).split(sep).some(part => part.startsWith('.'))), 'Unexpected hidden file');
  const release=JSON.parse(await readFile(join(website,'artwork/release-review.json'),'utf8'));
  const reviewedFiles=Object.keys(release.files).sort();
  const actualReviewFiles=files.map(file=>relative(root,file).split(sep).join('/'))
    .filter(file=>/^(layouts\/(rendered|structure)|downloads)\//.test(file)).sort();
  assert.deepEqual(actualReviewFiles,reviewedFiles,'Public asset roster differs from the reviewed release');
  for (const [file,wanted] of Object.entries(release.files)) {
    const actual=createHash('sha256').update(await readFile(join(root,file))).digest('hex');
    assert.equal(actual,wanted,`Reviewed public asset changed: ${file}`);
  }
  const sources=JSON.parse(await readFile(join(root,'downloads/photo-sources.json'),'utf8'));
  assert.equal(sources.photographs.length,7);
  assert.ok(sources.photographs.every(photo=>photo.license==='CC0-1.0'&&photo.visual_review));
  assert.equal(errors.length, 0, errors.join('\n'));
  console.log(`Site check passed: ${links} local links, 33 distinct layouts and 73 preview assets.`);
}
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) await checkSite(join(website, 'dist'));
