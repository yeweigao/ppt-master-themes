#!/usr/bin/env python3
"""Extract used PPTX colors as design evidence, never as an approved palette."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
from zipfile import ZipFile
import xml.etree.ElementTree as ET

A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'


def extract(source):
    counts = defaultdict(Counter)
    pages = defaultdict(set)
    slots = {}
    with ZipFile(source) as archive:
        theme = ET.fromstring(archive.read('ppt/theme/theme1.xml'))
        for slot in theme.find('.//' + A + 'clrScheme'):
            color = list(slot)[0]
            slots[slot.tag.split('}')[-1]] = '#' + (color.get('val') if color.tag == A+'srgbClr' else color.get('lastClr', '000000')).upper()
        slide_names = sorted((n for n in archive.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml', n)), key=lambda n: int(re.search(r'(\d+)\.xml', n)[1]))
        transformed = 0
        for name in slide_names:
            number = int(re.search(r'(\d+)\.xml', name)[1])
            root = ET.fromstring(archive.read(name))
            parents = {child: parent for parent in root.iter() for child in parent}
            for color in root.iter():
                if color.tag not in (A+'srgbClr', A+'schemeClr'):
                    continue
                # Modified colors are useful evidence, but a base token is not the rendered RGB.
                if any(child.tag != A+'alpha' for child in color):
                    transformed += 1
                    continue
                rgb = '#' + color.get('val', '').upper() if color.tag == A+'srgbClr' else slots.get(color.get('val'))
                if not rgb or not re.fullmatch(r'#[0-9A-F]{6}', rgb):
                    continue
                parent = parents.get(color)
                owner = parents.get(parent)
                tag = owner.tag.split('}')[-1] if owner is not None else ''
                role = 'text' if tag in ('rPr','defRPr','endParaRPr') else 'line' if tag == 'ln' else 'shape-or-other'
                counts[rgb][role] += 1
                pages[rgb].add(number)
    used = [{'hex': rgb, 'occurrences': sum(c.values()), 'roles': dict(c), 'pages': sorted(pages[rgb])} for rgb,c in sorted(counts.items(), key=lambda item: -sum(item[1].values()))]
    return {'schema': 'ppt-master-themes.source-palette.v1', 'source': str(Path(source).resolve()), 'method': 'Used DrawingML base RGB and scheme-color tokens, including opacity variants; occurrence counts, not visual area.', 'limitations': ['Default theme slots are separate evidence, not automatically a brand palette.', 'Photos, embedded logo pixels, master overrides and rendered color transforms require visual inspection.', 'A frequent color is not by itself a brand requirement.'], 'used_colors': used, 'default_theme_slots': slots, 'modified_tokens_not_resolved': transformed}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if args.source.suffix.lower() != '.pptx':
        parser.error('this helper handles PPTX only; use host document/image tools for other inputs')
    if args.out.resolve() == args.source.resolve():
        parser.error('output must not overwrite source')
    data = extract(args.source)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'output': str(args.out.resolve()), 'top_used_colors': data['used_colors'][:6]}, ensure_ascii=False))


if __name__ == '__main__':
    main()
