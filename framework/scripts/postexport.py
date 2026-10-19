#!/usr/bin/env python3
"""Theme post-export for a ppt-master PPTX (runs AFTER ppt-master Step 7.3; never edits ppt-master output in place).

1. embed the theme's fonts (static instances → EOT-wrapped ppt/fonts/*.fntdata + p:embeddedFontLst)
2. verify original non-font package parts are unchanged and write a separate receipt
3. optional: render with LibreOffice → PDF + contact sheet

  postexport.py --theme <theme_dir> --pptx <ppt-master export> [--out <file>] [--render <dir>]

Default output: <export stem>_themed.pptx next to the input.
"""
import argparse, hashlib, json, re, struct, subprocess, sys, zipfile, tempfile, shutil
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from theme_fonts import build
from fontTools.ttLib import TTFont

def eot(path):
    """Uncompressed EOT v2.1 wrapper (format PowerPoint uses for .fntdata)."""
    data = Path(path).read_bytes(); f = TTFont(path); os2 = f['OS/2']; nm = f['name']
    if os2.fsType & 0x0206:
        raise ValueError(f'font embedding permission does not allow this editable variant: {path}')
    g = lambda i: (nm.getDebugName(i) or '').encode('utf-16-le')
    p = os2.panose
    panose = bytes([p.bFamilyType, p.bSerifStyle, p.bWeight, p.bProportion, p.bContrast,
                    p.bStrokeVariation, p.bArmStyle, p.bLetterForm, p.bMidline, p.bXHeight])
    hdr = struct.pack('<III', len(data), 0x00020001, 0) + panose
    hdr += struct.pack('<BBIHH', 1, 1 if os2.fsSelection & 1 else 0, os2.usWeightClass, os2.fsType, 0x504C)
    hdr += struct.pack('<IIII', os2.ulUnicodeRange1, os2.ulUnicodeRange2, os2.ulUnicodeRange3, os2.ulUnicodeRange4)
    hdr += struct.pack('<II', os2.ulCodePageRange1, os2.ulCodePageRange2)
    hdr += struct.pack('<I', f['head'].checkSumAdjustment) + b'\0' * 16
    for s in (g(1), g(2), g(5), g(4)):
        hdr += struct.pack('<HH', 0, len(s)) + s
    hdr += struct.pack('<HH', 0, 0)
    return struct.pack('<I', 4 + len(hdr) + len(data)) + hdr + data

FONT_EDITS = {'ppt/presentation.xml', 'ppt/_rels/presentation.xml.rels', '[Content_Types].xml'}

def verify_preserved(src, dst):
    """Font insertion may edit three metadata parts; all other input parts stay exact."""
    with zipfile.ZipFile(src) as before, zipfile.ZipFile(dst) as after:
        if after.testzip() is not None:
            raise ValueError('font variant failed ZIP integrity validation')
        missing = set(before.namelist()) - set(after.namelist())
        if missing:
            raise ValueError(f'original package parts missing: {sorted(missing)}')
        changed = [name for name in before.namelist()
                   if name not in FONT_EDITS and before.read(name) != after.read(name)]
        if changed:
            raise ValueError(f'font-only processing changed original content: {changed}')
        return len([name for name in before.namelist() if name not in FONT_EDITS])

def write_receipt(src, dst, embedded):
    preserved = verify_preserved(src, dst)
    receipt = Path(dst).with_suffix('.postexport.json')
    receipt.write_text(json.dumps({
        'kind': 'theme-font-variant-preservation',
        'source': str(Path(src).resolve()), 'variant': str(Path(dst).resolve()),
        'source_sha256': hashlib.sha256(Path(src).read_bytes()).hexdigest(),
        'variant_sha256': hashlib.sha256(Path(dst).read_bytes()).hexdigest(),
        'preserved_original_parts': preserved, 'fonts_embedded': embedded,
        'frames_widened': 0,
        'scope': 'ZIP integrity and non-font part preservation only; not a ppt-master postflight or visual/PowerPoint validation',
    }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return receipt

def run(theme_dir, src, dst, widen=None):
    src, dst = Path(src).expanduser().resolve(), Path(dst).expanduser().resolve()
    if src == dst:
        raise ValueError('font variant must not overwrite the ppt-master export')
    if dst.exists():
        raise FileExistsError(f'font variant already exists: {dst}; choose a separate output path')
    if widen is not None and widen != 1:
        raise ValueError('post-export frame widening is unsupported; repair source SVG and re-export')
    with tempfile.TemporaryDirectory(prefix='theme-fonts-') as td, zipfile.ZipFile(src) as zin:
        th, made = build(theme_dir, Path(td) / 'fonts')
        if not made:
            raise ValueError('theme declares no embeddable font faces')
        pres = zin.read('ppt/presentation.xml').decode('utf-8')
        if 'embeddedFontLst' in pres or any(n.startswith('ppt/fonts/') for n in zin.namelist()):
            raise ValueError('input already contains embedded fonts; merging is unsupported')
        rels = zin.read('ppt/_rels/presentation.xml.rels').decode('utf-8')
        nid = max((int(x) for x in re.findall(r'Id="rId(\d+)"', rels)), default=0) + 1
        fams = {}
        for fam, face, path in made:
            fams.setdefault(fam, {})[face] = path
        meta = {f['family']: f for f in th['fonts']}
        lst, newrels, parts = '<p:embeddedFontLst>', '', {}
        k = 1
        from xml.sax.saxutils import quoteattr
        for fam, faces in fams.items():
            lst += f'<p:embeddedFont><p:font typeface={quoteattr(fam)} pitchFamily="{meta[fam].get("pitch_family", 0)}" charset="0"/>'
            for face in ('regular', 'bold', 'italic', 'boldItalic'):
                if face not in faces:
                    continue
                parts[f'ppt/fonts/font{k}.fntdata'] = eot(faces[face])
                newrels += f'<Relationship Id="rId{nid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/font" Target="fonts/font{k}.fntdata"/>'
                lst += f'<p:{face} r:id="rId{nid}"/>'
                nid += 1
                k += 1
            lst += '</p:embeddedFont>'
        lst += '</p:embeddedFontLst>'
        pres, count = re.subn(r'(<p:notesSz[^>]*/>)', lambda m: m.group(1) + lst, pres, count=1)
        if count != 1 or '</Relationships>' not in rels:
            raise ValueError('unsupported presentation metadata layout; retain original export')
        if 'embedTrueTypeFonts' not in pres:
            pres = pres.replace('<p:presentation ', '<p:presentation embedTrueTypeFonts="1" ', 1)
        replacements = {
            'ppt/presentation.xml': pres.encode('utf-8'),
            'ppt/_rels/presentation.xml.rels': rels.replace('</Relationships>', newrels + '</Relationships>').encode('utf-8'),
        }
        types = zin.read('[Content_Types].xml').decode('utf-8')
        if 'Extension="fntdata"' not in types:
            if '</Types>' not in types:
                raise ValueError('unsupported content-types metadata')
            types = types.replace('</Types>', '<Default Extension="fntdata" ContentType="application/x-fontdata" /></Types>')
        replacements['[Content_Types].xml'] = types.encode('utf-8')
        # Build and verify separately; only publish a complete checked variant.
        dst.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='.theme-variant-', dir=dst.parent) as staging:
            candidate = Path(staging) / 'variant.pptx'
            with zipfile.ZipFile(candidate, 'w', zipfile.ZIP_DEFLATED) as zout:
                for item in zin.infolist():
                    zout.writestr(item, replacements.get(item.filename, zin.read(item.filename)))
                for name, payload in parts.items():
                    zout.writestr(name, payload)
            verify_preserved(src, candidate)
            candidate.rename(dst)
    return len(parts), 0

def render(pptx, outdir):
    outdir = Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', str(outdir), str(pptx)],
                   check=True, capture_output=True)
    pdf = outdir / (Path(pptx).stem + '.pdf')
    for old in outdir.glob('pg-*.png'): old.unlink()
    subprocess.run(['pdftoppm', '-r', '30', '-png', str(pdf), str(outdir / 'pg')], check=True)
    pngs = sorted(outdir.glob('pg-*.png'))
    sheet = outdir / (Path(pptx).stem + '_sheet.jpg')
    subprocess.run(['magick', 'montage', *map(str, pngs), '-tile', f'{min(8, len(pngs))}x', '-geometry', '+4+4',
                    '-quality', '85', str(sheet)], check=True)
    return pdf, sheet

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--theme', required=True); ap.add_argument('--pptx', required=True)
    ap.add_argument('--out'); ap.add_argument('--render'); ap.add_argument('--widen', type=float)
    a = ap.parse_args()
    src = Path(a.pptx); dst = Path(a.out) if a.out else src.with_name(src.stem + '_themed.pptx')
    n, w = run(a.theme, src, dst, a.widen)
    receipt = write_receipt(src, dst, n)
    print(f'[postexport] {dst}  fonts_embedded={n} frames_widened={w} receipt={receipt}')
    if a.render:
        pdf, sheet = render(dst, a.render); print(f'[postexport] render {pdf}\n[postexport] sheet {sheet}')
