"""Audit public SVG media, downloadable Office/PDF content, and release hashes."""
from pathlib import Path
from zipfile import ZipFile
from hashlib import sha256
from io import BytesIO
import argparse
import json
import re
from lxml import etree as E
from PIL import Image
import fitz

parser=argparse.ArgumentParser()
parser.add_argument('--record', action='store_true', help='Record hashes after completing visual review')
args=parser.parse_args()
ROOT=Path(__file__).resolve().parents[1]
ledger=json.loads((ROOT/'artwork/photo-sources.json').read_text())
allowed={photo['sha256'] for photo in ledger['photographs']}
assert len(allowed)==7
for photo in ledger['photographs']:
    assert photo['license']=='CC0-1.0' and photo.get('visual_review')
    assert sha256((ROOT/photo['file']).read_bytes()).hexdigest()==photo['sha256']
    assert not Image.open(ROOT/photo['file']).getexif(), f"EXIF remains: {photo['id']}"

for path in sorted((ROOT/'artwork/templates').glob('*.svg')):
    root=E.parse(str(path))
    for image in root.findall('.//{http://www.w3.org/2000/svg}image'):
        href=image.get('href','')
        assert href.startswith('../images/')
        assert sha256((path.parent/href).resolve().read_bytes()).hexdigest() in allowed, path.name

private=re.compile(r'/Users/|/private/|file:///|YLMUN|CHIANG MAI|supplied brochure|grain_clouds', re.I)
decks=[]
for path in sorted((ROOT/'public/downloads').glob('*.pptx')):
    approved=neutral=0
    with ZipFile(path) as z:
        assert z.testzip() is None
        for name in z.namelist():
            data=z.read(name)
            if name.endswith(('.xml','.rels')):
                assert not private.search(data.decode('utf-8',errors='ignore')), f'{path.name}: stale/private content in {name}'
                assert b'TargetMode="External"' not in data or b'https://' in data, f'{path.name}: local external relationship'
            if name.startswith('ppt/media/'):
                if sha256(data).hexdigest() in allowed: approved+=1
                else:
                    im=Image.open(BytesIO(data))
                    assert im.size==(1,1), f'{path.name}: unlisted image {name} ({im.size})'
                    neutral+=1
    decks.append({'file':path.name,'approved_landscape_media':approved,'neutral_pixels':neutral})
pdf=ROOT/'public/downloads/A4_Editorial_Examples.pdf'
doc=fitz.open(pdf)
assert len(doc)==24
for page in doc:
    assert abs(page.rect.width*25.4/72-210)<.1 and abs(page.rect.height*25.4/72-297)<.1
    assert not private.search(page.get_text())
assert 'CC0 PHOTOGRAPHY' in doc[-1].get_text()
files={}
for folder in ['public/layouts/rendered','public/layouts/structure','public/layouts/themes',
               'public/layouts/169/structure','public/layouts/169/themes','public/downloads']:
    for path in sorted((ROOT/folder).rglob('*')):
        if path.is_file(): files[path.relative_to(ROOT/'public').as_posix()]=sha256(path.read_bytes()).hexdigest()
record={'reviewed_on':'2026-10-24','scope':'Publication examples, downloads, homepage theme spreads, and theme showcases on the A4 and 16:9 layouts',
    'manual_visual_review':'Seven CC0 source landscapes; all 33 published layout previews and their structure previews; the eight-page fictional OSTRA brand study; the 24-page exported native PDF contact sheet; the four homepage theme spreads; the 24 A4 and 26 16:9 theme showcase renderings; and the 17 neutral 16:9 structure previews inspected. NatGeo, Brand Geometry and Boardroom showcases reuse only the seven CC0 landscapes. Landscape layouts contain no visible people. The Fashion theme spread and Fashion showcases use licensed Unsplash portraits (not CC0) and is labeled as such on the credits page and footer.',
    'automated_checks':{'only_approved_landscapes_or_neutral_pixels':True,'source_images_no_exif':True,'no_stale_or_private_strings_in_office_xml_or_pdf_text':True,'pdf_pages':len(doc),'pdf_size_mm':[210,297]},
    'decks':decks,'files':files}
if args.record:
    (ROOT/'artwork/release-review.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'decks':decks,'pdf_pages':len(doc),'public_artifact_files':len(files),'status':'passed'},ensure_ascii=False))
