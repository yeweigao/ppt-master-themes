"""Create a publication copy of the approved, hand-authored sample SVGs.

This maintenance command receives its source explicitly. It replaces media and
sample copy without changing the neutral Layout package or the original demo.
"""
import argparse
import json
import shutil
from pathlib import Path
from lxml import etree as E
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('--source', type=Path, required=True, help='Existing sample workspace containing templates/')
args = parser.parse_args()
ROOT = Path(__file__).resolve().parents[1]
SRC = args.source.resolve() / 'templates'
DEST = ROOT / 'artwork' / 'templates'
DEST.mkdir(parents=True, exist_ok=True)
NS = 'http://www.w3.org/2000/svg'
MEDIA = {'image1.png':'dunes', 'image10.png':'lake', 'image11.png':'ocean',
         'image14.png':'autumn', 'image16.jpeg':'waterfall', 'image17.jpeg':'horizon', 'image18.jpeg':'woodland'}
COPY = {
 '01_cover': {'title':'Beyond the\nframe.', 'subtitle':'A field guide to light,\nlandscape and attention.', 'kicker':'PPT MASTER THEMES  /  LANDSCAPE STUDY'},
 '03c_content_bottom': {'caption':'PHOTO: ARCHBOB / CC0 1.0 / CROP FOR LAYOUT DEMONSTRATION'},
 '03d_content_side': {
  'kicker':'04 / NATURE, UP CLOSE', 'title':'Follow\nthe\nwater.',
  'lead':'A quiet detail can\nopen a wider story.',
  'main-copy':'Water moves through the frame.\nA rock, a branch and a current\ncreate different points of entry.\nLook before naming the scene.\n\nNotice light and arrangement.\nFollow an edge or a reflection.\nLeave room for a closer view\nto change what first seemed\nimportant in the landscape.',
  'caption':'PHOTO: MARTIN EKLUND / CC0\nFULL-HEIGHT PHOTOGRAPHIC CROP'},
 '03f_content_spread_right': {'caption':'BONNIE MORELAND / CC0 1.0 / ONE SHARED CROP ACROSS BOTH PAGES'},
 '03i_content_gallery': {'lead':'Water, shorelines and horizons.\nThree landscapes offer different scales of attention.',
  'source':'PHOTOS: BONNIE MORELAND / HOMMIE09 / MARTIN EKLUND. CC0 1.0.'},
 '03m_content_masonry': {'title':'A world, in fragments.',
  'source':'BY COLUMN, TOP TO BOTTOM: lake / autumn; waterfall / sunrise;\nwaves / dunes. CC0 1.0 photographs; full credits in the website source list.\nIndependent landscapes, not one location or event sequence.'},
 '03n_content_stagger': {
  'main-copy':'01 / THE SETTING\nBegin with the wider scene.\n\n03 / A DIFFERENT SCALE\nMove from water to land to horizon.\nDifferent image sizes create a route,\nwhile the shared edges hold it together.',
  'source':'CC0 1.0 LANDSCAPES\nSOURCES LISTED ON THE WEBSITE\nLAYOUT DEMONSTRATION'},
 '03o_content_contact': {'title':'One frame. Many worlds.',
  'source':'A panoramic anchor, followed by six supporting views.\nRead the smaller frames from left to right, then top to bottom.\nCC0 landscapes from different places; full credits in the source list.'},
 '03p_content_overlay': {'source':'PHOTO: BONNIE\nMORELAND / CC0\n\nPhotograph, reading plate\nand headline remain\nseparate objects.'},
 '03q_content_geometry': {'title':'A frame for\nthe natural world.'},
 '04_ending': {
  'contact':'CC0 PHOTOGRAPHY\nBonnie Moreland / Archbob / Martin Eklund\nBautsch / SpessiG / Hommie09\nAlabama Extension / Bruce Dupree',
  'closing':'SOURCES AND LICENSE\nSource list included with the examples:\nphoto-sources.json and image-credits.html\nAlso available on the website.'}
}

def set_lines(text, value):
    lines = value.split('\n')
    for child in list(text): text.remove(child)
    text.text = lines[0]
    size = float(text.get('font-size', '24'))
    gap = size * (1.16 if size >= 50 else 1.5)
    skipped = 0
    for line in lines[1:]:
        if not line: skipped += 1; continue
        span = E.SubElement(text, f'{{{NS}}}tspan', x=text.get('x'), dy=f'{gap*(skipped+1):.2f}'.rstrip('0').rstrip('.'))
        span.text = line
        skipped = 0

paths = sorted(SRC.glob('*.svg'))
assert len(paths) == 24, 'Expected the approved 24 examples'
source_records = json.loads((ROOT/'artwork/photo-sources.json').read_text())['photographs']
photos_by_id = {photo['id']:photo for photo in source_records}
uses = []
for number, path in enumerate(paths, 1):
    tree = E.parse(str(path))
    root = tree.getroot()
    for image in list(root.findall(f'.//{{{NS}}}image')):
        href = image.get('href', '')
        if href.endswith('grain_clouds.png'):
            image.getparent().remove(image)
            continue
        basename = Path(href).name
        if basename in MEDIA:
            key = MEDIA[basename]
            assert (ROOT/f'artwork/images/{key}.jpg').exists()
            image.set('href', f'../images/{key}.jpg')
            uses.append({'layout':path.stem, 'slot':image.getparent().get('id', 'panorama'), 'photo':key})
            parent = image.getparent()
            if parent.tag == f'{{{NS}}}svg' and parent.get('data-pptx-carrier') == 'true':
                # Both pages are windows onto one shared panorama crop.
                w, h = Image.open(ROOT/f'artwork/images/{key}.jpg').size
                visible_height = (w / 2) / h
                assert visible_height <= 1
                x = 0 if path.stem.endswith('left') else .5
                parent.set('viewBox', f'{x} {(1-visible_height)/2:.12f} 0.5 {visible_height:.12f}')
    for group in root.findall(f'{{{NS}}}g'):
        gid = group.get('id')
        text = group.find(f'{{{NS}}}text')
        if text is None: continue
        if path.stem == '04_ending' and gid in ['contact', 'closing']:
            text.set('font-size','20')
        if gid in COPY.get(path.stem, {}): set_lines(text, COPY[path.stem][gid])
        if gid == 'folio': set_lines(text, f'{number:02d}')
    tree.write(str(DEST/path.name), encoding='utf-8')
shutil.copy2(SRC/'design_spec.layout.a4-editorial.md', DEST/'design_spec.layout.a4-editorial.md')
(ROOT/'artwork/photo-uses.json').write_text(json.dumps(uses,ensure_ascii=False,indent=2)+'\n')
print('Prepared 24 publication SVGs using only the seven licensed landscape files.')
