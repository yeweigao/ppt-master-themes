import { createServer } from 'node:http';
import { open, stat } from 'node:fs/promises';
import { dirname, extname, join, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../dist');
const port = Number(process.env.PORT || 6077);
const mime = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.json': 'application/json; charset=utf-8', '.jpg': 'image/jpeg', '.png': 'image/png', '.svg': 'image/svg+xml', '.ttf': 'font/ttf', '.txt': 'text/plain; charset=utf-8', '.pdf': 'application/pdf', '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation' };
const server = createServer(async (req, res) => {
  try {
    if (!['GET', 'HEAD'].includes(req.method)) { res.writeHead(405, { Allow: 'GET, HEAD' }).end(); return; }
    const path = decodeURIComponent(new URL(req.url, 'http://local.test').pathname);
    let file = resolve(root, '.' + path);
    if (file !== root && !file.startsWith(root + sep)) { res.writeHead(403).end(); return; }
    let code = 200;
    let info;
    try {
      info = await stat(file);
      if (info.isDirectory()) { file = join(file, 'index.html'); info = await stat(file); }
    } catch { file = join(root, '404.html'); info = await stat(file); code = 404; }
    res.writeHead(code, { 'Content-Type': mime[extname(file)] || 'application/octet-stream', 'Content-Length': info.size, 'Cache-Control': 'no-store' });
    if (req.method === 'HEAD') { res.end(); return; }
    const handle = await open(file);
    handle.createReadStream().on('error', () => res.destroy()).pipe(res);
  } catch { if (!res.headersSent) res.writeHead(500); res.end(); }
});
server.listen(port, '127.0.0.1', () => console.log(`PPT Master Themes: http://127.0.0.1:${port}/`));
for (const signal of ['SIGINT', 'SIGTERM']) process.on(signal, () => server.close(() => process.exit(0)));
