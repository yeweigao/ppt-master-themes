#!/usr/bin/env python3
"""Scaffold a new theme from themes/_template.
  python3 new_theme.py --id minimal-mag --name "Minimal Magazine" --name-zh "极简杂志风" [--style-id minimal-magazine]
"""
import argparse, shutil
from pathlib import Path
ap = argparse.ArgumentParser(); ap.add_argument('--id', required=True); ap.add_argument('--name', required=True)
ap.add_argument('--name-zh', default=''); ap.add_argument('--style-id')
a = ap.parse_args(); root = Path(__file__).resolve().parents[2] / 'themes'
src, dst = root / '_template', root / a.id
if dst.exists(): raise SystemExit(f'{dst} exists')
sid = a.style_id or a.id
shutil.copytree(src, dst)
for f in dst.rglob('*'):
    if f.is_file() and f.suffix in ('.json', '.md'):
        t = f.read_text(encoding='utf-8').replace('__ID__', a.id).replace('__NAME__', a.name).replace('__中文名__', a.name_zh).replace('__STYLE_ID__', sid)
        f.write_text(t, encoding='utf-8')
    if '__STYLE_ID__' in f.name: f.rename(f.with_name(f.name.replace('__STYLE_ID__', sid)))
print(f'created draft {dst} — complete the reusable Style through ppt-master\'s Create Template contract; optional fonts/examples stay outside workspace. Maintenance check: compat_check.py --pm <provided-absolute-ppt-master-root> --theme {a.id}; this is not end-to-end acceptance.')
