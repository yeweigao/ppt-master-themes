#!/usr/bin/env python3
"""Legacy-named helper: emit theme planning hints; never write a project lock.

  theme_lock.py --theme <theme_dir> [--canvas a4] [--out <candidate.json>]

Use after a selected workspace is installed (or during explicit theme maintenance).
Strategist owns the confirmed Design Spec and lock; Quick owns transient anchors.
The former --project/--init/--size lock-overlay interface is intentionally unsupported.
"""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--theme', required=True)
    parser.add_argument('--canvas', help='choose a reference ladder, never change project canvas')
    parser.add_argument('--out', help='optional hints JSON outside the theme; no project lock output')
    args = parser.parse_args()
    theme_dir = Path(args.theme).expanduser().resolve()
    theme = json.loads((theme_dir / 'theme.json').read_text(encoding='utf-8'))
    hints = {
        'kind': 'theme-planning-hints',
        'authority': 'Reference defaults only; confirmed plan and workspace segment owners win',
        'theme_id': theme['id'],
        'design_defaults': theme.get('design_defaults', theme.get('user_rules', [])),
        'stage2_seeds': theme.get('stage2_seeds', {}),
        'fallback_colors': theme.get('colors', {}),
        'fallback_typography': theme.get('typography', {}),
        'contextual_paint': theme.get('contextual_paint', {}),
    }
    if args.canvas:
        hints['reference_ladder'] = theme.get('typography', {}).get('ladders', {}).get(args.canvas)
        if hints['reference_ladder'] is None:
            parser.error(f'no reference ladder for {args.canvas}; use the runtime canvas/type planning')
    data = json.dumps(hints, ensure_ascii=False, indent=2) + '\n'
    if args.out:
        out = Path(args.out).expanduser().resolve()
        if out.name in {'design_spec.md', 'spec_lock.md'} or out.suffix.lower() != '.json':
            parser.error('--out must be a candidate .json, never a Design Spec or lock')
        if out == theme_dir or theme_dir in out.parents:
            parser.error('--out must be outside the theme assets')
        if out.exists():
            parser.error('--out already exists; choose a new candidate path')
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(data, encoding='utf-8')
        print(out)
    else:
        print(data, end='')


if __name__ == '__main__':
    main()
