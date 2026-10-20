// Optional artwork maintenance tool. The normal website build has no sharp dependency.
const fs = require('node:fs/promises');
const path = require('node:path');
const { createRequire } = require('node:module');
const req = process.env.PPT_THEMES_NODE_MODULES ? createRequire(path.join(process.env.PPT_THEMES_NODE_MODULES, '__resolver.cjs')) : require;
const sharp = req('sharp');
const root = path.resolve(__dirname, '..');
(async () => {
  const manifest = JSON.parse(await fs.readFile(path.join(root, 'public/layouts/manifest.json'), 'utf8'));
  for (const item of manifest.items) {
    const source = path.join(root, 'artwork/templates', item.id + '.svg');
    let svg = await fs.readFile(source, 'utf8');
    const refs = [...new Set([...svg.matchAll(/href="(\.\.\/images\/[^"]+)"/g)].map(match => match[1]))];
    for (const href of refs) {
      const bytes = await fs.readFile(path.resolve(path.dirname(source), href));
      svg = svg.replaceAll(`href="${href}"`, `href="data:image/jpeg;base64,${bytes.toString('base64')}"`);
    }
    await sharp(Buffer.from(svg), {density:96}).resize({width:992})
      .jpeg({quality:92,chromaSubsampling:'4:4:4'}).toFile(path.join(root, 'public/layouts/rendered', item.id + '.jpg'));
  }
  const folder = path.join(root, 'public/layouts/rendered');
  const left = path.join(folder,'03e_content_spread_left.jpg');
  const right = path.join(folder,'03f_content_spread_right.jpg');
  const meta = await sharp(left).metadata();
  await sharp({create:{width:meta.width*2,height:meta.height,channels:3,background:'#fff'}})
    .composite([{input:left,left:0,top:0},{input:right,left:meta.width,top:0}])
    .jpeg({quality:94}).toFile(path.join(folder,'spread.jpg'));
  console.log('Rendered 24 public examples and the continuous spread.');
})();
