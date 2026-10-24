#!/usr/bin/env python3
"""Composite a photograph inside a word and write a transparent PNG.

The type-mask hero is a picture, so it renders identically in PowerPoint,
Keynote, LibreOffice and browsers. Regenerate it at the target canvas scale.

Usage:
  make_type_mask.py --font SixCaps-Regular.ttf --text PORTRAITS \
    --photo portrait.jpg --out type.png --width 720 --height 340 \
    [--outline 4] [--scale 3]
"""
import argparse
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps


def cover(im, w, h):
    im = ImageOps.exif_transpose(im).convert('L')
    im = ImageOps.autocontrast(im, cutoff=0.5)
    scale = max(w / im.width, h / im.height)
    im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.LANCZOS)
    left = (im.width - w) // 2
    top = (im.height - h) // 2
    return im.crop((left, top, left + w, top + h))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--font', required=True)
    ap.add_argument('--text', required=True)
    ap.add_argument('--photo', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--width', type=int, required=True)
    ap.add_argument('--height', type=int, required=True)
    ap.add_argument('--outline', type=int, default=4)
    ap.add_argument('--scale', type=int, default=3)
    ap.add_argument('--invert', action='store_true', help='white type on dark ground')
    a = ap.parse_args()

    W, H = a.width * a.scale, a.height * a.scale
    # Draw at a size where the ink box is taller than the target, then fit.
    probe = ImageFont.truetype(a.font, 400)
    bbox = probe.getbbox(a.text)
    draw_w, draw_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    font = ImageFont.truetype(a.font, max(8, round(400 * H / draw_h)))
    bbox = font.getbbox(a.text)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]

    mask = Image.new('L', (text_w + a.outline * 2, text_h + a.outline * 2), 0)
    d = ImageDraw.Draw(mask)
    d.text((a.outline - bbox[0], a.outline - bbox[1]), a.text, font=font, fill=255)
    mask = mask.resize((W, H), Image.LANCZOS)

    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    photo = cover(Image.open(a.photo), W, H)
    if a.invert:
        photo = ImageOps.invert(photo)
    canvas.paste(Image.merge('RGB', (photo, photo, photo)), (0, 0), mask)

    if a.outline > 0:
        edge = mask.filter(ImageFilter.MaxFilter(a.outline * 2 + 1))
        edge = Image.composite(edge, Image.new('L', (W, H), 0), mask.point(lambda v: 255 if v == 0 else 0))
        outline = Image.new('RGBA', (W, H), (10, 10, 10, 255))
        outline.putalpha(edge)
        canvas = Image.alpha_composite(outline, canvas)

    canvas.save(a.out, optimize=True)
    print(f'{a.out}: {W}x{H}, ink {text_w}x{text_h}, outline {a.outline}px (final), rendered at {a.scale}x')


if __name__ == '__main__':
    main()
