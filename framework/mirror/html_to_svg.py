#!/usr/bin/env python3
"""Optional HTML adapter: layout JSON -> flat editable SVG pages at authoring time.

Usage:
  python3 html_to_svg.py --layout layout.json --project <ppt-master project> --theme theme.json \
      [--canvas 1240x1754] [--names-from-spec] [--roles 1=cover,2=toc,24=ending] [--bg-group 0]

- Text is rebuilt as editable <text>/<tspan> lines at the measured baselines (copy is
  never rewritten; whatever the HTML says is what the slide says).
- Fonts are mapped through theme.mirror.html_font_map -> theme.typography.svg_stacks.
- Photos: background-layer photos become a page-sized derivative crop bg_PNN.jpg;
  object-fit/background-size:cover photos become crop_PNN_k.jpg; others are referenced as-is
  (copied into <project>/images). Run register_images.py afterwards.
- CSS linear-gradients become native SVG linearGradient rects (editable, export as PPT gradients).
- Each top-level child of the HTML page becomes a <g> with data-pptx-bounds zones that do
  not overlap (so ppt-master grouping/animation stays sane).
"""
import argparse, json, re, os, html, shutil
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import url2pathname
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument('--layout', required=True); ap.add_argument('--project', required=True)
ap.add_argument('--theme', required=True); ap.add_argument('--canvas', default='1240x1754')
ap.add_argument('--names-from-spec', action='store_true', help='file names from "#### Slide N - Title" in design_spec.md')
ap.add_argument('--roles', default='', help='e.g. 1=cover,2=toc,4=section,24=ending')
ap.add_argument('--bg-group', type=int, default=0)
ap.add_argument('--header-class', default='rh'); ap.add_argument('--footer-class', default='fo')
a = ap.parse_args()

L = json.load(open(a.layout, encoding='utf-8')); T = json.load(open(a.theme, encoding='utf-8'))
PW, PH = L['page_w'], L['page_h']; W, H = map(int, a.canvas.split('x')); S = W / PW
SRC = Path(L['html']).parent; PROJ = Path(a.project)
(PROJ / 'svg_output').mkdir(parents=True, exist_ok=True); (PROJ / 'images').mkdir(exist_ok=True)
FMAP = T.get('mirror', {}).get('html_font_map', {}); STACK = T['typography']['svg_stacks']
ROLE = {int(k): v for k, v in (x.split('=') for x in a.roles.split(',') if x)}

def col(c):
    m = re.findall(r'[\d.]+', c); r, g, b = [int(float(x)) for x in m[:3]]; al = float(m[3]) if len(m) > 3 else 1
    return '#%02X%02X%02X' % (r, g, b), al
def fam(ff):
    first = ff.split(',')[0].strip().strip('"\'')
    for k, role in FMAP.items():
        if first == k or first.startswith(k):
            return STACK.get(role.replace('_italic', ''), STACK.get('body', 'Arial'))
    return STACK.get('body', 'Arial')
def esc(t): return html.escape(t, quote=False)
def n(v): return ('%.2f' % v).rstrip('0').rstrip('.')
def inter(x, y, w, h):
    x0, y0 = max(x, 0), max(y, 0); x1, y1 = min(x + w, PW), min(y + h, PH); return (x0, y0, x1 - x0, y1 - y0)
def crop_save(srcpath, box, frame, out, cover=None):
    im = Image.open(srcpath); iw, ih = im.size; x, y, w, h = box
    if cover:
        sc = max(w / iw, h / ih); dw, dh = iw * sc, ih * sc; px, py = cover; ox = x + (w - dw) * px; oy = y + (h - dh) * py
    else: dw, dh, ox, oy = w, h, x, y
    fx, fy, fw, fh = frame
    c = im.crop((round((fx - ox) / dw * iw), round((fy - oy) / dh * ih), round((fx + fw - ox) / dw * iw), round((fy + fh - oy) / dh * ih)))
    tw = round(fw * S); target = max(tw, min(c.size[0], tw * 2)); c = c.resize((target, max(1, round(target * fh / fw))), Image.LANCZOS)
    if c.mode in ('RGBA', 'LA', 'P'):
        out = out.rsplit('.', 1)[0] + '.png'; c.convert('RGBA').save(PROJ / 'images' / out)
    else:
        out = out.rsplit('.', 1)[0] + '.jpg'; c.convert('RGB').save(PROJ / 'images' / out, quality=90)
    return out
def pos_frac(pos):
    vals = []
    for v in (pos or '50% 50%').split()[:2]:
        v = {'left': '0%', 'top': '0%', 'center': '50%', 'right': '100%', 'bottom': '100%'}.get(v, v)
        vals.append(float(v.strip('%')) / 100 if v.endswith('%') else 0.5)
    return (vals + [0.5])[:2]
GRAD = []
def gradient(css, gid):
    m = re.search(r'linear-gradient\((.*)\)', css)
    if not m: return None
    parts = re.split(r',(?![^()]*\))', m.group(1)); ang = 180
    if re.match(r'\s*(-?[\d.]+)deg', parts[0]): ang = float(re.match(r'\s*(-?[\d.]+)deg', parts[0]).group(1)); parts = parts[1:]
    elif parts[0].strip().startswith('to '):
        ang = {'to bottom': 180, 'to top': 0, 'to right': 90, 'to left': 270}.get(parts[0].strip(), 180); parts = parts[1:]
    stops = []
    for i, p in enumerate(parts):
        cm = re.search(r'(rgba?\([^)]*\)|#[0-9a-fA-F]{3,8})', p)
        if not cm: continue
        c = cm.group(1); off = re.search(r'([\d.]+)%', p[cm.end():])
        hexc, al = col(c) if c.startswith('rgb') else (c.upper(), 1)
        stops.append((float(off.group(1)) if off else (100 * i / max(1, len(parts) - 1)), hexc, al))
    vec = {180: ('0', '0', '0', '1'), 0: ('0', '1', '0', '0'), 90: ('0', '0', '1', '0'), 270: ('1', '0', '0', '0')}.get(int(ang) % 360, ('0', '0', '0', '1'))
    s = ''.join(f'<stop offset="{n(o)}%" stop-color="{c}" stop-opacity="{n(al)}"/>' for o, c, al in stops)
    GRAD.append(f'<linearGradient id="{gid}" x1="{vec[0]}" y1="{vec[1]}" x2="{vec[2]}" y2="{vec[3]}">{s}</linearGradient>')
    return gid

names = {}
spec = PROJ / 'design_spec.md'
if a.names_from_spec and spec.exists():
    for i, t in enumerate(re.findall(r'#### Slide \d+ - (.+)', spec.read_text(encoding='utf-8')), 1):
        names[i] = re.sub(r'[^a-z0-9]+', '_', t.lower()).strip('_')
used = set()
def gid_(base):
    base = re.sub(r'[^a-z0-9]+', '-', base.lower()).strip('-')[:28] or 'group'; i, k = base, 2
    while i in used: i = f'{base}-{k}'; k += 1
    used.add(i); return i

for pg in L['pages']:
    N = pg['n']; used.clear(); GRAD.clear(); out = []
    bgc, _ = col(pg['bg'])
    out.append(f'<rect id="bg-fill" x="0" y="0" width="{W}" height="{H}" fill="{bgc}"/>')
    items = {g['gi']: [] for g in pg['groups']}; ext = {g['gi']: [g['x'], g['y'], g['x'] + g['w'], g['y'] + g['h']] for g in pg['groups']}
    def grow(gi, x, y, w, h):
        e = ext[gi]; e[0] = min(e[0], x); e[1] = min(e[1], y); e[2] = max(e[2], x + w); e[3] = max(e[3], y + h)
    ci = 0
    for im in pg['imgs']:
        fr = inter(im['x'], im['y'], im['w'], im['h'])
        if fr[2] <= 0 or fr[3] <= 0 or im['src'].startswith(('http:', 'https:', 'data:')): continue
        image_url = urlsplit(im['src'])
        image_path = url2pathname(image_url.path)
        if image_url.scheme == 'file' and image_url.netloc:
            image_path = '//' + image_url.netloc + image_path
        srcp = SRC / image_path
        if not srcp.exists(): print('missing image', srcp); continue
        name = srcp.name
        if im['g'] == a.bg_group:
            fn = crop_save(srcp, (im['x'], im['y'], im['w'], im['h']), fr, f'bg_P{N:02d}.jpg', cover=pos_frac(im.get('pos')) if im['fit'] == 'cover' else None)
            out.append(f'<image id="bg-photo" data-pptx-role="background" href="../images/{fn}" x="{n(fr[0]*S)}" y="{n(fr[1]*S)}" width="{n(fr[2]*S)}" height="{n(fr[3]*S)}" preserveAspectRatio="xMidYMid slice"/>'); continue
        if im['fit'] == 'cover':
            ci += 1; fn = crop_save(srcp, (im['x'], im['y'], im['w'], im['h']), fr, f'crop_P{N:02d}_{ci}.jpg', cover=pos_frac(im.get('pos')))
            items[im['g']].append(('i', f'<image href="../images/{fn}" x="{n(fr[0]*S)}" y="{n(fr[1]*S)}" width="{n(fr[2]*S)}" height="{n(fr[3]*S)}" preserveAspectRatio="xMidYMid slice"/>'))
        else:
            if not (PROJ / 'images' / name).exists(): shutil.copy(srcp, PROJ / 'images' / name)
            items[im['g']].append(('i', f'<image href="../images/{name}" x="{n(fr[0]*S)}" y="{n(fr[1]*S)}" width="{n(fr[2]*S)}" height="{n(fr[3]*S)}" preserveAspectRatio="xMidYMid meet"/>'))
        grow(im['g'], *fr)
    for bd in pg['borders']:
        x, y, w, h = bd['x'], bd['y'], bd['w'], bd['h']
        if 'gradient' in bd:
            g = gradient(bd['gradient'], f'grad-p{N}-{len(GRAD)+1}')
            if g:
                fr = inter(x, y, w, h)
                tgt = out if bd['g'] == a.bg_group else items[bd['g']]
                el = f'<rect x="{n(fr[0]*S)}" y="{n(fr[1]*S)}" width="{n(fr[2]*S)}" height="{n(fr[3]*S)}" fill="url(#{g})"/>'
                (tgt.append(el) if tgt is out else tgt.append(('r', el)))
            continue
        if 'fill' in bd:
            c, al = col(bd['fill'])
            items[bd['g']].append(('r', f'<rect x="{n(x*S)}" y="{n(y*S)}" width="{n(w*S)}" height="{n(h*S)}" fill="{c}"' + (f' fill-opacity="{n(al)}"' if al < 1 else '') + '/>')); grow(bd['g'], x, y, w, h); continue
        sd = bd['sides']
        if len(sd) == 4 and len({(s['w'], s['c']) for s in sd}) == 1:
            s = sd[0]; c, al = col(s['c']); sw = s['w'] * bd.get('z', 1)
            items[bd['g']].append(('r', f'<rect x="{n((x+sw/2)*S)}" y="{n((y+sw/2)*S)}" width="{n((w-sw)*S)}" height="{n((h-sw)*S)}" fill="none" stroke="{c}" stroke-width="{n(sw*S)}"/>'))
        else:
            for s in sd:
                c, al = col(s['c']); sw = s['w'] * bd.get('z', 1)
                x1, y1, x2, y2 = {'Bottom': (x, y+h-sw/2, x+w, y+h-sw/2), 'Top': (x, y+sw/2, x+w, y+sw/2),
                                  'Left': (x+sw/2, y, x+sw/2, y+h)}.get(s['s'], (x+w-sw/2, y, x+w-sw/2, y+h))
                items[bd['g']].append(('l', f'<line x1="{n(x1*S)}" y1="{n(y1*S)}" x2="{n(x2*S)}" y2="{n(y2*S)}" stroke="{c}" stroke-width="{n(sw*S)}"/>'))
        grow(bd['g'], x, y, w, h)
    first = {}
    for p in pg['paras']:
        toks = p['toks']
        if not toks: continue
        lines = []
        for t in sorted(toks, key=lambda t: (t['base'], t['x'])):
            if lines and abs(t['base'] - lines[-1][0]) < 0.35 * t['st']['fs']: lines[-1][1].append(t)
            else: lines.append([t['base'], [t]])
        key = lambda st: (fam(st['ff']), st['fst'], round(st['ls'], 2))
        bold = lambda fw: 'bold' if int(fw) >= 600 else 'normal'
        dom = Counter()
        for t in toks: dom[(key(t['st']), t['st']['fw'], round(t['st']['fs'], 2), col(t['st']['col'])[0])] += len(t['t'])
        (df, dst, dls), dfw, dfs, dcol = dom.most_common(1)[0][0]
        attrs = f'font-family="{df}" font-size="{n(dfs*S)}" fill="{dcol}"'
        if bold(dfw) != 'normal': attrs += ' font-weight="bold"'
        if dst == 'italic': attrs += ' font-style="italic"'
        if dls: attrs += f' letter-spacing="{n(dls*S)}"'
        parts, prevb = [], None
        for b, ts in lines:
            ts.sort(key=lambda t: t['x']); runs = []
            for t in ts:
                st = t['st']; sk = (key(st), bold(st['fw']), round(st['fs'], 2), col(st['col'])[0])
                if runs and runs[-1][0] == sk: runs[-1][1] += t['t']
                else: runs.append([sk, t['t']])
            runs[-1][1] = runs[-1][1].rstrip(); body = ''
            for ((f, fst, ls), fw, fs, c), txt in runs:
                at = []
                if f != df: at.append(f'font-family="{f}"')
                if fw != bold(dfw): at.append(f'font-weight="{fw}"')
                if fst != dst: at.append(f'font-style="{fst}"')
                if fs != round(dfs, 2): at.append(f'font-size="{n(fs*S)}"')
                if c != dcol: at.append(f'fill="{c}"')
                body += f'<tspan {" ".join(at)}>{esc(txt)}</tspan>' if at else esc(txt)
            parts.append(f'<tspan x="{n(ts[0]["x"]*S)}" dy="{n(0 if prevb is None else (b-prevb)*S)}">{body}</tspan>'); prevb = b
        items[p['g']].append(('t', f'<text x="{n(lines[0][1][0]["x"]*S)}" y="{n(lines[0][0]*S)}" {attrs}>' + ''.join(parts) + '</text>'))
        for t in toks: grow(p['g'], t['x'], t['y'], t['w'], t['h'])
        first.setdefault(p['g'], ''.join(t['t'] for t in toks)[:30])
    live = sorted([g['gi'] for g in pg['groups'] if g['gi'] != a.bg_group and items[g['gi']]], key=lambda gi: ext[gi][1])
    zone = {}
    for k, gi in enumerate(live):
        top = 0 if k == 0 else (ext[live[k-1]][3] + ext[gi][1]) / 2
        bot = PH if k == len(live) - 1 else (ext[gi][3] + ext[live[k+1]][1]) / 2
        zone[gi] = (0, max(top, 0), PW, min(bot, PH))
    for g in pg['groups']:
        gi = g['gi']
        if gi not in zone: continue
        x0, y0, x1, y1 = [v * S for v in zone[gi]]; cls = g['cls'].split()
        if a.header_class in cls: i = gid_('header'); role = ' data-pptx-role="header"'
        elif a.footer_class in cls: i = gid_('footer'); role = ' data-pptx-role="footer"'
        else: i = gid_(first.get(gi, 'group')); role = ''
        body = '\n  '.join(s for k, s in sorted(items[gi], key=lambda z: z[0] == 't'))
        out.append(f'<g id="{i}"{role} data-pptx-bounds="{n(x0)} {n(y0)} {n(x1-x0)} {n(y1-y0)}">\n  {body}\n</g>')
    defs = f'<defs>{"".join(GRAD)}</defs>\n' if GRAD else ''
    role = ROLE.get(N) or pg.get('role') or 'content'
    nm = names.get(N) or re.sub(r'[^a-z0-9]+', '_', (pg.get('title') or f'page_{N}').lower()).strip('_')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{STACK.get("body","Arial")}" data-pptx-page-role="{role}">\n'
           + defs + '\n'.join(out) + '\n</svg>\n')
    (PROJ / 'svg_output' / f'{N:02d}_{nm}.svg').write_text(svg, encoding='utf-8')
print('pages written:', len(L['pages']))
