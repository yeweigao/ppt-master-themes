#!/usr/bin/env python3
"""Optional post-export helper; ppt-master owns all generation and export commands.

  theme_build.py --pptx <exact successful export> [--render <directory>]
  theme_build.py --pptx <export> --theme <theme_dir> --embed-fonts [--out <variant>]

No project scan, checker, compactor, notes toggle, or exporter is run here.
The old --pm/--project pipeline interface is intentionally unsupported.
"""
import argparse
import zipfile
from pathlib import Path
from postexport import render, run, write_receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pptx', required=True, help='exact successfully exported PPTX')
    parser.add_argument('--theme', help='theme assets used by this deck, for an approved font variant')
    parser.add_argument('--embed-fonts', action='store_true', help='explicit opt-in for a separate font variant')
    parser.add_argument('--out')
    parser.add_argument('--render')
    args = parser.parse_args()
    src = Path(args.pptx).expanduser().resolve()
    if not src.is_file():
        parser.error('PPTX missing; finish the selected ppt-master runtime first')
    with zipfile.ZipFile(src) as package:
        if package.testzip() is not None:
            parser.error('input PPTX failed ZIP integrity validation')
    dst = src
    if args.embed_fonts:
        if not args.theme:
            parser.error('--embed-fonts requires --theme')
        dst = Path(args.out).expanduser().resolve() if args.out else src.with_name(src.stem + '_themed.pptx')
        n, w = run(Path(args.theme).expanduser().resolve(), src, dst)
        receipt = write_receipt(src, dst, n)
        print(f'[font-variant] {dst} fonts_embedded={n} frames_widened={w} receipt={receipt}')
    elif args.out:
        parser.error('--out is only used with --embed-fonts; preview uses the original PPTX')
    else:
        print(f'[original-export] {src} (unchanged)')
    if args.render:
        pdf, sheet = render(dst, Path(args.render).expanduser().resolve())
        print(f'[preview] {pdf}\n[contact-sheet] {sheet}')


if __name__ == '__main__':
    main()
