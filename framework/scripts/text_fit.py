"""Copy fitting for SVG authoring with real font metrics (ppt-master-themes).

Families: "T" = theme title font, "K" = kicker font, "A" = body (Arial). Font files come from
THEME_FONTS (default themes/natgeo/fonts). CJK characters are measured at 1 em.

  from text_fit import wrap, bwrap, pwrap, fit_headline, log_fit, tl
  pwrap(text, "A", 26, 980)                   # body: "pretty" - no single-word / single-char last line
  bwrap(text, "T", 64, 1064, bold=True)       # headings: "balance" - lines of similar length
  plan = fit_headline(text, "T", 84, 1064, ladder=[84, 64, 42, 36, 20], bold=True)
  log_fit(project, "P03", text, plan)          # -> notes/copy_fit_log.md (deliver this table)
  tl(x, y, lines, dy, font_size=26)            # -> <text> with one <tspan> per line

Line-break rules built in: separators (· | — → / -) never start a line; CJK closing punctuation
never starts a line and opening punctuation never ends one (避头尾); words are never split.
See framework/COPY_FIT.md for the headline split ladder.
"""
import os, re, html, shutil, subprocess
from pathlib import Path
from PIL import ImageFont

F = os.environ.get('THEME_FONTS', str(Path(__file__).resolve().parents[2] / 'themes' / 'natgeo' / 'fonts')) + '/'
SEPS = {'·', '|', '—', '–', '→', '/', '-', '+'}
CLOSE = set('，。、；：！？）」』》〉】,.;:!?)]}%…') | {'”', '’'}
OPEN = set('（「『《〈【([{') | {'“', '‘'}
CJK = re.compile(r'[\u2e80-\u9fff\uf900-\ufaff\u3000-\u303f\uff00-\uffef]')
_c = {}

def body_font_path(bold=False, italic=False):
    face = ('BOLD_ITALIC' if italic else 'BOLD') if bold else ('ITALIC' if italic else '')
    env_key = 'THEME_BODY_FONT' + ('_' + face if face else '')
    if os.environ.get(env_key):
        p = Path(os.environ[env_key]).expanduser()
        if not p.is_file():
            raise FileNotFoundError(f'{env_key} does not point to a font file: {p}')
        return str(p)
    filename = ('arialbi.ttf' if italic else 'arialbd.ttf') if bold else ('ariali.ttf' if italic else 'arial.ttf')
    macname = ('Arial Bold Italic.ttf' if italic else 'Arial Bold.ttf') if bold else ('Arial Italic.ttf' if italic else 'Arial.ttf')
    roots = [Path.home() / 'Library' / 'Fonts', Path('/Library/Fonts'), Path('/Library/Fonts/Microsoft'),
             Path('/System/Library/Fonts/Supplemental'),
             Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts',
             Path(os.environ.get('LOCALAPPDATA', str(Path.home() / 'AppData' / 'Local'))) / 'Microsoft/Windows/Fonts',
             Path('/usr/share/fonts/msttcore'), Path('/usr/share/fonts/truetype/msttcorefonts'),
             Path.home() / '.fonts',
             Path(os.environ.get('XDG_DATA_HOME', str(Path.home() / '.local/share'))) / 'fonts']
    for root in roots:
        for name in (filename, macname):
            p = root / name
            if p.is_file():
                return str(p)
    matcher = shutil.which('fc-match')
    if matcher:
        style = ('Bold Italic' if italic else 'Bold') if bold else ('Italic' if italic else 'Regular')
        r = subprocess.run([matcher, '-f', '%{family}\n%{file}\n', f'Arial:style={style}'],
                           capture_output=True, text=True, check=False)
        lines = r.stdout.splitlines()
        if r.returncode == 0 and len(lines) >= 2 and 'arial' in [f.strip().lower() for f in lines[0].split(',')] and Path(lines[1]).is_file():
            return lines[1]
    raise FileNotFoundError(f'Arial {face or "REGULAR"} not found; set {env_key} to the matching body font file. See framework/RUNTIME.md.')

def font(fam, bold=False, italic=False):
    k = (fam, bold, italic)
    if k in _c: return _c[k]
    if fam == 'T':
        f = ImageFont.truetype(F + ('PlayfairDisplay-Italic[wght].ttf' if italic else 'PlayfairDisplay[wght].ttf'), 100)
        f.set_variation_by_axes([700 if (italic and bold) else (900 if bold else 400)])
    elif fam == 'K':
        f = ImageFont.truetype(F + 'Oswald[wght].ttf', 100); f.set_variation_by_axes([600 if bold else 400])
    else:
        f = ImageFont.truetype(body_font_path(bold, italic), 100)
    _c[k] = f; return f

def width(t, fam, size, bold=False, italic=False, ls=0):
    n_cjk = len(CJK.findall(t)); rest = CJK.sub('', t)
    return font(fam, bold, italic).getlength(rest) * size / 100 + n_cjk * size + ls * len(t)

def _units(t):
    """unbreakable units: [text, space_before]"""
    toks = re.findall(r'\s+|' + CJK.pattern + r'|[^\s\u2e80-\u9fff\uf900-\ufaff\u3000-\u303f\uff00-\uffef]+', t)
    units, sp = [], False
    for tok in toks:
        if tok.isspace(): sp = True; continue
        glue_prev = units and (tok in CLOSE or tok[0] in CLOSE and CJK.match(tok[0] or '') or tok in SEPS
                               or units[-1][0][-1] in OPEN)
        if glue_prev:
            units[-1][0] += (' ' if sp else '') + tok
        else:
            units.append([tok, sp])
        sp = False
    return units

def _join(us):
    s = ''
    for i, (u, sp) in enumerate(us): s += (' ' if (sp and i) else '') + u
    return s

def wrap(t, fam, size, w, bold=False, italic=False, ls=0):
    """greedy wrap (what PowerPoint would do)"""
    us = _units(t); out, cur = [], []
    for u in us:
        c = cur + [u]
        if not cur or width(_join(c), fam, size, bold, italic, ls) <= w: cur = c
        else: out.append(_join(cur)); cur = [[u[0], False]]
    if cur: out.append(_join(cur))
    return out

def bwrap(t, fam, size, w, **k):
    """balance (like CSS text-wrap: balance): same line count as greedy, shortest longest line"""
    base = wrap(t, fam, size, w, **k); n = len(base)
    if n == 1: return base
    lo, hi, best = w * 0.4, w, base
    for _ in range(25):
        mid = (lo + hi) / 2; r = wrap(t, fam, size, mid, **k)
        if len(r) <= n: best, hi = r, mid
        else: lo = mid
    return best

def _short_last(lines, fam, size, w, **k):
    last = lines[-1]
    units = _units(last)
    return len(units) < 2 or width(last, fam, size, **k) < 0.2 * w

def pwrap(t, fam, size, w, **k):
    """pretty (like CSS text-wrap: pretty): greedy, but the last line never holds a single
    word / CJK char or less than ~20% of the measure; line count unchanged when possible"""
    base = wrap(t, fam, size, w, **k)
    if len(base) < 2 or not _short_last(base, fam, size, w, **k): return base
    tw = w
    while tw > w * 0.7:
        tw -= w * 0.01
        r = wrap(t, fam, size, tw, **k)
        if len(r) == len(base) and not _short_last(r, fam, size, w, **k): return r
    for tw in [w * f for f in (0.99, 0.97, 0.95, 0.93, 0.9, 0.87, 0.84, 0.8)]:   # accept one extra line
        r = wrap(t, fam, size, tw, **k)
        if len(r) == len(base) + 1 and not _short_last(r, fam, size, w, **k): return r
    return base

PREFIX = re.compile(r'^((?:chapter|part|section|highlight|highlights|day|module|unit|step|appendix|d)\s*[\w\d]+'
                    r'|第[^\s·|:：—]{1,6}[章节部分天课站]|[0-9]{1,2})\s*[·|:：—–-]\s*', re.I)
SPLITS = [' · ', ' — ', ' – ', ' | ', ': ', '：', ' - ']
PAREN = re.compile(r'^(.*?)\s*([（(][^（）()]+[）)])\s*$')

def fit_headline(t, fam, size, w, ladder, max_lines=2, sub_lines=2, bold=True, italic=False):
    """Headline split ladder (COPY_FIT.md). Never rewrites, reorders or abbreviates words.
    ladder: role sizes from big to small, e.g. [display, title, heading_sm, subtitle, annotation].
    Tries steps 1-4 at the intended size, then once more one ladder step down (step 5).
    Returns dict(rule, kicker, title, title_size, subtitle, sub_size, note, dropped, changed)."""
    k = dict(bold=bold, italic=italic)
    smaller = [s for s in ladder if s < size]
    def attempt(sz):
        sm = [s for s in ladder if s < sz]
        sub = sm[1] if len(sm) > 1 else (sm[0] if sm else sz)          # subtitle = two ladder steps down
        r = dict(rule='', kicker='', title=[], title_size=sz, subtitle=[], sub_size=sub, note='', dropped='', changed=sz != size)
        L = bwrap(t, fam, sz, w, **k)                                      # 1 balance
        if len(L) <= max_lines: r.update(rule='1 balance', title=L); return r
        body = t
        m = PREFIX.match(body)                                             # 2 leading attribution -> kicker
        if m and len(body) > m.end():
            r.update(kicker=m.group(1), dropped=body[len(m.group(1)):m.end()].strip(), changed=True); body = body[m.end():]
            L = bwrap(body, fam, sz, w, **k)
            if len(L) <= max_lines: r.update(rule='2 prefix→kicker', title=L); return r
        for sep in SPLITS:                                                 # 3 first separator -> title + subtitle
            if sep in body:
                head, tail = body.split(sep, 1)
                Lh = bwrap(head, fam, sz, w, **k); Lt = bwrap(tail, fam, sub, w, **k)
                if len(Lh) <= max_lines and len(Lt) <= sub_lines:
                    r.update(rule='3 separator→subtitle', title=Lh, subtitle=Lt, changed=True,
                             dropped=(r['dropped'] + ' ' + sep.strip()).strip()); return r
        m = PAREN.match(body)                                              # 4 trailing parenthesis -> note
        if m:
            L = bwrap(m.group(1), fam, sz, w, **k)
            if len(L) <= max_lines: r.update(rule='4 parenthesis→note', title=L, note=m.group(2), changed=True); return r
        return None
    for sz in [size] + smaller[:1]:
        r = attempt(sz)
        if r:
            if sz != size: r['rule'] = '5 one size down + ' + r['rule']
            return r
    return dict(rule='6 NO FIT: reflow page / split page / ask user', kicker='', title=bwrap(t, fam, size, w, **k),
                title_size=size, subtitle=[], sub_size=size, note='', dropped='', changed=True)

def log_fit(project, page, source, plan):
    """append one row to <project>/notes/copy_fit_log.md when the hierarchy changed"""
    if not plan.get('changed'): return
    p = Path(project) / 'notes'; p.mkdir(parents=True, exist_ok=True); f = p / 'copy_fit_log.md'
    if not f.exists():
        f.write_text('# Copy fit log — hierarchy adjustments (wording unchanged)\n\n'
                     '| Page | Source text | Kicker | Title | Subtitle | Note | Size | Rule | Not printed |\n'
                     '|---|---|---|---|---|---|---|---|---|\n', encoding='utf-8')
    cell = lambda s: (s if isinstance(s, str) else ' / '.join(s)).replace('|', '\\|')
    with f.open('a', encoding='utf-8') as fh:
        fh.write(f"| {page} | {cell(source)} | {cell(plan['kicker'])} | {cell(plan['title'])} | {cell(plan['subtitle'])} | "
                 f"{cell(plan['note'])} | {plan['title_size']} | {plan['rule']} | {cell(plan['dropped'])} |\n")

def e(s): return html.escape(s, quote=False)

def tl(x, y, lines, dy, **a):
    at = ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in a.items())
    sp = ''.join(f'<tspan x="{x}" dy="{0 if i == 0 else dy}">{e(l)}</tspan>' for i, l in enumerate(lines))
    return f'<text x="{x}" y="{y}" {at}>{sp}</text>'
