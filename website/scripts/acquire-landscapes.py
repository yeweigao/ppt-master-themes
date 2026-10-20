"""Acquire the explicitly selected CC0 photographs; never runs during site builds."""
from pathlib import Path
from urllib.parse import quote, unquote, urljoin, urlsplit, urlunsplit
from datetime import date
from hashlib import sha256
import json
import subprocess
from io import BytesIO
from PIL import Image, ImageOps
from lxml import html

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'artwork' / 'images'
DEST.mkdir(parents=True, exist_ok=True)
SELECTED = [
    ('lake', 'Lake Mountain Landscape.jpg', 'Bonnie Moreland', '山湖'),
    ('autumn', 'Lateautumnforest.jpg', 'Archbob', '秋林'),
    ('waterfall', 'Waterfall in forest.jpg', 'Martin Eklund', '林间瀑布'),
    ('ocean', 'Meereswellen.Atlantik.P1180785.jpg', 'Bautsch', '大西洋海浪'),
    ('dunes', 'Sand Dunes at Sunset - 50134723536.jpg', 'Alabama Extension / Bruce Dupree', '日落沙丘'),
    ('woodland', 'Landscape of a wild forest.jpg', 'SpessiG', '林地光影'),
    ('horizon', 'Sunrise Over the Ocean.jpg', 'Hommie09', '海上日出'),
]

def get(url):
    return subprocess.run(['curl', '-fsSL', '--retry', '2', '--retry-delay', '1',
        '--connect-timeout', '15', '--max-time', '90', '-A',
        'PPTMasterThemes/1.0 (public website image provenance audit)', url],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout

ledger = ROOT / 'artwork' / 'photo-sources.json'
records = json.loads(ledger.read_text())['photographs'] if ledger.exists() else []
records = [record for record in records if record['id'] in {item[0] for item in SELECTED}]
for key, filename, author, title in SELECTED:
    previous = next((record for record in records if record['id'] == key), None)
    if previous and (ROOT / previous['file']).exists() and sha256((ROOT / previous['file']).read_bytes()).hexdigest() == previous['sha256']:
        print(f'{key}: retained verified acquisition', flush=True)
        continue
    page = 'https://commons.wikimedia.org/wiki/File:' + quote(filename.replace(' ', '_'), safe="()_-.")
    tree = html.fromstring(get(page))
    licenses = tree.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," licensetpl_short ")]/text()')
    if not any('CC0' in label for label in licenses):
        raise ValueError(f'{key}: exact file-license field is not CC0: {licenses}')
    original = list(dict.fromkeys(urlunsplit(urlsplit(urljoin(page, u))._replace(query='', fragment='')) for u in tree.xpath('//a/@href')
        if 'upload.wikimedia.org/wikipedia/commons/' in u and '/thumb/' not in u
        and unquote(urlsplit(u).path).endswith('/' + filename.replace(' ', '_'))))
    if len(original) != 1 or not original[0].startswith('https://upload.wikimedia.org/'):
        raise ValueError(f'{key}: unrecognised original file URL: {original}')
    payload = get(original[0])
    image = ImageOps.exif_transpose(Image.open(BytesIO(payload))).convert('RGB')
    original_size = list(image.size)
    image.thumbnail((2800, 2800), Image.Resampling.LANCZOS)
    path = DEST / f'{key}.jpg'
    image.save(path, 'JPEG', quality=92, subsampling=0, optimize=True)
    oldids = tree.xpath('//a[contains(@href,"oldid=") and contains(@href,"title=File")]/@href')
    oldid = next((u.split('oldid=')[1].split('&')[0] for u in oldids), None)
    records.append({
        'id': key, 'title': title, 'original_title': filename, 'author': author,
        'source_page': page, 'source_revision': oldid,
        'download_url': original[0], 'license': 'CC0-1.0',
        'license_url': 'https://creativecommons.org/publicdomain/zero/1.0/',
        'verified_on': date.today().isoformat(),
        'verification': 'Exact file description page and licensetpl_short field checked; visual review follows acquisition.',
        'original_sha256': sha256(payload).hexdigest(),
        'original_size_px': original_size, 'file': f'artwork/images/{key}.jpg',
        'sha256': sha256(path.read_bytes()).hexdigest(), 'size_px': list(image.size),
        'processing': 'Orientation normalised, resized, JPEG encoded; EXIF omitted. No semantic image editing.',
    })
    ledger.write_text(json.dumps({'collection':'Public landscape demonstration assets', 'photographs':records}, ensure_ascii=False, indent=2) + '\n')
    print(f'{key}: CC0 verified, saved {image.width}x{image.height}', flush=True)

(ROOT / 'artwork' / 'photo-sources.json').write_text(json.dumps({
    'collection': 'Public landscape demonstration assets', 'photographs': records,
}, ensure_ascii=False, indent=2) + '\n')
