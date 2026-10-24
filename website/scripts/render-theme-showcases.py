"""Render theme showcases and neutral 16:9 structure previews for the website.

Optional maintenance tool; the normal `npm run build` never runs it. Needs Python
Playwright with Chromium and Pillow. Install the theme fonts (Bodoni Moda, Six Caps,
Archivo) or metric-compatible substitutes (Georgia -> Gelasio, Arial -> Liberation Sans)
first, because Chromium renders whatever the system resolves.

Sources (read only):
  themes/<id>/examples/a4-editorial/*.svg      -> public/layouts/themes/<id>/*.jpg     (992 wide)
  themes/<id>/examples/ppt169-editorial/*.svg  -> public/layouts/169/themes/<id>/*.jpg (1600 wide)
  layouts/ppt169-editorial/workspace/templates -> public/layouts/169/structure/*.jpg   (placeholder
                                                  tokens replaced by readable neutral labels)

Afterwards: update the manifests if prototypes were added, inspect every image, then run
`python3 website/scripts/audit-release.py --record` and `npm run build`.
"""
import asyncio
import re
import tempfile
from pathlib import Path

from PIL import Image
from playwright.async_api import async_playwright

WEBSITE = Path(__file__).resolve().parents[1]
REPO = WEBSITE.parent
PUBLIC = WEBSITE / 'public' / 'layouts'
LABELS = {
    'TITLE': 'Cover title', 'SUBTITLE': 'Subtitle', 'DATE': 'Edition / date',
    'CHAPTER_NUM': '02', 'CHAPTER_TITLE': 'Chapter title', 'CHAPTER_DESC': 'Chapter description',
    'SECTION_NAME': 'SECTION / KICKER', 'PAGE_TITLE': 'Page title', 'PAGE_NUM': '00',
    'SOURCE': 'Caption / source', 'CONTENT_AREA': 'Content area', 'CONTENT_LEFT': 'Left column',
    'CONTENT_RIGHT': 'Right column', 'CONTEXT': 'Context note', 'SIDEBAR': 'Sidebar note',
    'KEY_MESSAGE': 'Key message', 'NOTE_1': 'Margin note', 'LABEL_LEFT': 'Option A',
    'LABEL_RIGHT': 'Option B', 'THANK_YOU': 'Closing line', 'ENDING_SUBTITLE': 'Closing subtitle',
    'CONTACT_INFO': 'Contact', 'CLOSING_MESSAGE': 'Next step',
}
for i, metric in enumerate(['15+', '24%', '99', '3.2'], 1):
    LABELS.update({f'METRIC_{i}': metric, f'LABEL_{i}': f'Metric label {i}', f'TIME_{i}': f'Stage {i}',
                   f'EVENT_{i}': f'Event {i}', f'STEP_{i}': f'Step {i}', f'LEFT_{i}': f'Left row {i}',
                   f'RIGHT_{i}': f'Right row {i}'})


async def render(browser, svgs, out_dir, width, height, out_width):
    out_dir.mkdir(parents=True, exist_ok=True)
    page = await browser.new_page(viewport={'width': width, 'height': height},
                                  device_scale_factor=max(1, out_width / width))
    for svg in svgs:
        await page.goto(svg.resolve().as_uri())
        await page.evaluate('document.fonts.ready')
        await page.wait_for_timeout(250)
        png = out_dir / f'{svg.stem}.png'
        await page.screenshot(path=str(png))
        image = Image.open(png).convert('RGB').resize((out_width, round(out_width * height / width)), Image.LANCZOS)
        image.save(out_dir / f'{svg.stem}.jpg', quality=88, optimize=True, progressive=True)
        png.unlink()
    await page.close()
    return len(svgs)


async def main():
    count = 0
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        for theme in sorted(p for p in (REPO / 'themes').iterdir() if p.is_dir() and not p.name.startswith('_')):
            a4 = sorted((theme / 'examples' / 'a4-editorial').glob('*.svg'))
            wide = sorted((theme / 'examples' / 'ppt169-editorial').glob('*.svg'))
            if a4:
                count += await render(browser, a4, PUBLIC / 'themes' / theme.name, 1240, 1754, 992)
            if wide:
                count += await render(browser, wide, PUBLIC / '169' / 'themes' / theme.name, 1280, 720, 1600)
        templates = REPO / 'layouts' / 'ppt169-editorial' / 'workspace' / 'templates'
        with tempfile.TemporaryDirectory() as tmp:
            labelled = []
            for svg in sorted(templates.glob('*.svg')):
                text = re.sub(r'\{\{([A-Z0-9_]+)\}\}', lambda m: LABELS.get(m.group(1), m.group(1).title()), svg.read_text('utf-8'))
                target = Path(tmp) / svg.name
                target.write_text(text, 'utf-8')
                labelled.append(target)
            count += await render(browser, labelled, PUBLIC / '169' / 'structure', 1280, 720, 1600)
        await browser.close()
    print(f'Rendered {count} images. Inspect them, then run audit-release.py --record and npm run build.')


asyncio.run(main())
