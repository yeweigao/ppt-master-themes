// Mode B step 1: measure a paginated HTML handbook into layout JSON.
// Usage (install playwright beside this script or in the working directory):
//   node html_extract.js --html book.html --out layout.json [--theme theme.json]
//        [--page "section.page"] [--w 794] [--h 1122] [--ready "document.body.dataset.ready==='1'"]
//        [--after "fill()"] [--pdf reference.pdf] [--chromium <executable>]
// Each top-level child of a page element becomes a "group"; child 0 is treated as the
// full-bleed background layer by html_to_svg.py when it carries a photo.
const fs = require('fs'), path = require('path');
const { pathToFileURL } = require('url');
const A = {}; process.argv.slice(2).forEach((v, i, a) => { if (v.startsWith('--')) A[v.slice(2)] = a[i + 1]; });
if (!A.html || !A.out) { console.error('need --html and --out'); process.exit(2); }
let pw;
try { pw = require('playwright'); }
catch (e) {
  try { pw = require(require.resolve('playwright', { paths: [process.cwd()] })); }
  catch (e) { console.error('Playwright not found. Install playwright in the working directory and run npx playwright install chromium. See framework/RUNTIME.md.'); process.exit(2); }
}
const { chromium } = pw;
const W = +(A.w || 794), H = +(A.h || 1122), SEL = A.page || 'section.page';
let css = '';
if (A.theme) { const t = JSON.parse(fs.readFileSync(A.theme, 'utf8')); css = (t.mirror || {}).html_css_overrides || '';
  // resolve theme-relative font urls
  const tdir = path.dirname(path.resolve(A.theme));
  css = css.replace(/url\((?!["']?(?:https?:|file:|data:))["']?([^)"']+)["']?\)/g, (m, u) => `url("${pathToFileURL(path.resolve(tdir, u)).href}")`); }
(async () => {
  const b = await chromium.launch(A.chromium ? { executablePath: A.chromium } : {});
  const p = await b.newPage({ viewport: { width: W + 100, height: H + 100 } });
  await p.goto(pathToFileURL(path.resolve(A.html)).href);
  if (css) await p.addStyleTag({ content: css });
  if (A.ready) await p.waitForFunction(A.ready, { timeout: 20000 }).catch(() => console.error('ready timeout'));
  await p.evaluate(async (after) => { await document.fonts.ready; if (after) { try { eval(after); } catch (e) { console.error(e); } } }, A.after || '');
  await p.waitForTimeout(300);
  const base = pathToFileURL(path.dirname(path.resolve(A.html)) + path.sep).href;
  const data = await p.evaluate(({ SEL, base }) => {
    const asc = {};
    function ascent(cs) { const k = [cs.fontFamily, cs.fontWeight, cs.fontStyle, cs.fontSize].join('|'); if (asc[k] != null) return asc[k];
      const s = document.createElement('span'); s.style.cssText = `font-family:${cs.fontFamily};font-weight:${cs.fontWeight};font-style:${cs.fontStyle};font-size:${cs.fontSize};line-height:normal;position:absolute;left:0;top:0;white-space:nowrap`;
      s.textContent = 'Hxg'; const m = document.createElement('i'); m.style.cssText = 'display:inline-block;width:1px;height:0;vertical-align:baseline'; s.appendChild(m); document.body.appendChild(s);
      const r = document.createRange(); r.selectNodeContents(s.firstChild); const t = r.getBoundingClientRect().top; const bl = m.getBoundingClientRect().bottom; s.remove(); return asc[k] = (bl - t) / parseFloat(cs.fontSize); }
    function zoomOf(el) { let z = 1; for (let e = el; e && e.nodeType === 1; e = e.parentElement) { const v = parseFloat(getComputedStyle(e).zoom); if (v && v !== 1) z *= v; } return z; }
    const rel_src = u => u.startsWith(base) ? u.slice(base.length) : u;
    const pages = [];
    document.querySelectorAll(SEL).forEach((sec, pi) => {
      const P = sec.getBoundingClientRect(); const rel = r => ({ x: r.left - P.left, y: r.top - P.top, w: r.width, h: r.height });
      const out = { n: pi + 1, cls: sec.className, title: sec.dataset.title || '', role: sec.dataset.role || '', bg: getComputedStyle(sec).backgroundColor, imgs: [], borders: [], paras: [], groups: [] };
      [...sec.children].forEach((c, ci) => { c.dataset.gi = ci; out.groups.push({ gi: ci, tag: c.tagName, cls: c.className, ...rel(c.getBoundingClientRect()) }); });
      const gidx = el => { let e = el; while (e.parentElement !== sec) e = e.parentElement; return +e.dataset.gi; };
      sec.querySelectorAll('*').forEach(el => {
        const cs = getComputedStyle(el); const r = el.getBoundingClientRect(); if (r.width === 0 && r.height === 0) return;
        if (el.tagName === 'IMG') out.imgs.push({ src: rel_src(el.src), nw: el.naturalWidth, nh: el.naturalHeight, fit: cs.objectFit === 'cover' ? 'cover' : 'fill', pos: cs.objectPosition, ...rel(r), g: gidx(el) });
        const bi = cs.backgroundImage; if (bi && bi !== 'none') { const mm = bi.match(/url\("?(.*?)"?\)/); if (mm) out.imgs.push({ src: rel_src(mm[1]), fit: 'cover', pos: cs.backgroundPosition, ...rel(r), g: gidx(el) });
          if (/gradient/.test(bi)) out.borders.push({ ...rel(r), gradient: bi, sides: [], g: gidx(el) }); }
        const sides = ['Top', 'Right', 'Bottom', 'Left'].map(s => ({ s, w: parseFloat(cs['border' + s + 'Width']), st: cs['border' + s + 'Style'], c: cs['border' + s + 'Color'] })).filter(o => o.w > 0 && o.st !== 'none');
        if (sides.length) out.borders.push({ ...rel(r), sides, g: gidx(el), z: zoomOf(el) });
        if (cs.backgroundColor !== 'rgba(0, 0, 0, 0)' && el !== sec) out.borders.push({ ...rel(r), fill: cs.backgroundColor, sides: [], g: gidx(el) });
      });
      const paraMap = new Map(); const tw = document.createTreeWalker(sec, NodeFilter.SHOW_TEXT); let tn;
      while (tn = tw.nextNode()) {
        if (!tn.textContent.trim()) continue;
        const el = tn.parentElement; let blk = el; while (getComputedStyle(blk).display === 'inline') blk = blk.parentElement;
        if (!paraMap.has(blk)) paraMap.set(blk, { g: gidx(blk), align: getComputedStyle(blk).textAlign, box: rel(blk.getBoundingClientRect()), toks: [] });
        const para = paraMap.get(blk); const cs = getComputedStyle(el); const z = zoomOf(el);
        const st = { ff: cs.fontFamily, fw: cs.fontWeight, fs: parseFloat(cs.fontSize) * z, fst: cs.fontStyle, col: cs.color, ls: (cs.letterSpacing === 'normal' ? 0 : parseFloat(cs.letterSpacing)) * z, tt: cs.textTransform, asc: ascent(cs) };
        const re = /\S+\s*|\s+/g; let m; const txt = tn.textContent;
        while (m = re.exec(txt)) { const word = m[0]; const core = word.replace(/\s+$/, ''); if (!core) { if (para.toks.length) para.toks[para.toks.length - 1].t += ' '; continue; }
          const rg = document.createRange(); rg.setStart(tn, m.index); rg.setEnd(tn, m.index + core.length); const rs = [...rg.getClientRects()]; if (!rs.length) continue; const r = rs[0]; const r2 = rs[rs.length - 1];
          const push = (t0, a, b2, trail) => { let t = t0; if (st.tt === 'uppercase') t = t.toUpperCase(); para.toks.push({ t: t + (trail ? ' ' : ''), x: a.left - P.left, y: a.top - P.top, w: b2.right - a.left, h: a.height, base: a.top - P.top + st.asc * st.fs, st }); };
          if (rs.length === 1 || Math.abs(r2.top - r.top) < 2) push(core, r, r2, word.length > core.length);
          else { // word broken across lines (hyphenation / CJK): split per visual line
            let start = 0, prevTop = null, first = null, last = null;
            for (let ci = 0; ci < core.length; ci++) { const cr = document.createRange(); cr.setStart(tn, m.index + ci); cr.setEnd(tn, m.index + ci + 1); const rr = cr.getClientRects()[0]; if (!rr) continue;
              if (prevTop !== null && Math.abs(rr.top - prevTop) > 2) { push(core.slice(start, ci), first, last, false); start = ci; first = rr; }
              if (first === null) first = rr; last = rr; prevTop = rr.top; }
            push(core.slice(start), first, last, word.length > core.length); }
        }
      }
      out.paras = [...paraMap.values()]; pages.push(out);
    });
    return pages;
  }, { SEL, base });
  fs.writeFileSync(A.out, JSON.stringify({ page_w: W, page_h: H, html: path.resolve(A.html), pages: data }));
  if (A.pdf) await p.pdf({ path: A.pdf, width: W + 'px', height: H + 'px', printBackground: true });
  console.log('pages', data.length, 'paras', data.map(d => d.paras.length).join(','));
  await p.close(); await b.close(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
