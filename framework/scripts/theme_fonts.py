#!/usr/bin/env python3
"""Build static font instances declared in a theme (theme.json `fonts[].embed`).

PowerPoint maps every run to one of four faces per family (regular/bold/italic/boldItalic).
A theme may choose which variable-font weight backs each face (e.g. Playfair "bold" = wght 900).
Instances are written with consistent name/OS2 bits so Office, LibreOffice and fontconfig agree.

  theme_fonts.py --theme <theme_dir> --out <dir> [--install | --install-dir <dir>]
"""
import argparse, json, os, shutil, subprocess, sys
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

STYLE_NAME = {'regular': 'Regular', 'bold': 'Bold', 'italic': 'Italic', 'boldItalic': 'Bold Italic'}

def user_font_dir():
    if sys.platform == 'darwin':
        return Path.home() / 'Library' / 'Fonts'
    if sys.platform == 'win32':
        base = Path(os.environ.get('LOCALAPPDATA', str(Path.home() / 'AppData' / 'Local')))
        return base / 'Microsoft' / 'Windows' / 'Fonts'
    return Path(os.environ.get('XDG_DATA_HOME', str(Path.home() / '.local' / 'share'))) / 'fonts'

def install(made, directory=None):
    d = Path(directory).expanduser().resolve() if directory else user_font_dir()
    d.mkdir(parents=True, exist_ok=True)
    for _, _, p in made:
        if p.resolve() != (d / p.name).resolve():
            shutil.copy(p, d / p.name)
    if sys.platform == 'win32' and directory is None:
        import winreg
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                              r'Software\Microsoft\Windows NT\CurrentVersion\Fonts') as key:
            for fam, face, p in made:
                winreg.SetValueEx(key, f'{fam} {STYLE_NAME[face]} (TrueType)', 0,
                                 winreg.REG_SZ, str(d / p.name))
    cache = shutil.which('fc-cache')
    if cache:
        subprocess.run([cache, '-f'], check=False)
    return d

def build(theme_dir, out):
    th = json.loads((Path(theme_dir) / 'theme.json').read_text(encoding='utf-8'))
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    made = []
    for f in th.get('fonts', []):
        fam = f['family']
        for face, spec in f['embed'].items():
            src = Path(theme_dir) / spec['source']
            ft = TTFont(src)
            if 'fvar' in ft:
                ft = instancer.instantiateVariableFont(ft, {'wght': spec['wght']})
            if 'STAT' in ft: del ft['STAT']
            name = ft['name']
            for nid in (16, 17, 21, 22, 25): name.removeNames(nameID=nid)
            sty = STYLE_NAME[face]; ps = fam.replace(' ', '') + '-' + sty.replace(' ', '')
            full = fam if face == 'regular' else f'{fam} {sty}'
            for nid, val in [(1, fam), (2, sty), (3, ps + ';theme-static'), (4, full), (6, ps)]:
                name.setName(val, nid, 3, 1, 0x409); name.setName(val, nid, 1, 0, 0)
            italic = face in ('italic', 'boldItalic'); bold = face in ('bold', 'boldItalic')
            os2 = ft['OS/2']; os2.usWeightClass = 700 if bold else 400  # preserve source embedding permissions
            sel = (1 if italic else 0) | (32 if bold else 0) | (64 if not (italic or bold) else 0)
            os2.fsSelection = (os2.fsSelection & ~0b1100001) | sel
            ft['head'].macStyle = (2 if italic else 0) | (1 if bold else 0)
            p = out / f'{ps}.ttf'; ft.save(p); made.append((fam, face, p))
    return th, made

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--theme', required=True); ap.add_argument('--out', required=True)
    group = ap.add_mutually_exclusive_group()
    group.add_argument('--install', action='store_true')
    group.add_argument('--install-dir', help='copy fonts to a caller-managed font directory')
    a = ap.parse_args()
    th, made = build(a.theme, a.out)
    for fam, face, p in made: print(f'{fam:20s} {face:10s} {p}')
    if a.install or a.install_dir:
        d = install(made, a.install_dir)
        print(f'installed {len(made)} faces into {d}')
