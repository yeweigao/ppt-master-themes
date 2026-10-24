#!/usr/bin/env python3
"""Build one SVG path outlining a word, for clipping a picture to the letters.

Usage: type_mask.py FONT TEXT X Y WIDTH HEIGHT [--xscale N] [--tracking N]
Prints JSON with the path data and the exact box the picture should occupy.
"""
import argparse, json
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform


def draw_word(font, text, sx, sy, x0, baseline, tracking):
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    pen = SVGPathPen(glyphs, ntos=lambda v: f"{v:.3f}")
    x = x0
    for ch in text:
        name = cmap.get(ord(ch))
        if name is None:
            raise SystemExit(f"missing glyph: {ch!r}")
        glyph = glyphs[name]
        glyph.draw(TransformPen(pen, Transform(sx, 0, 0, -sy, x, baseline)))
        x += glyph.width * sx + tracking
    return pen.getCommands(), x - x0 - tracking


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('font'); ap.add_argument('text')
    ap.add_argument('x', type=float); ap.add_argument('y', type=float)
    ap.add_argument('width', type=float); ap.add_argument('height', type=float)
    ap.add_argument('--xscale', type=float, default=0.4)
    ap.add_argument('--tracking', type=float, default=-6)
    a = ap.parse_args()

    font = TTFont(a.font)
    glyphs = font.getGlyphSet(); cmap = font.getBestCmap()
    upem = font['head'].unitsPerEm
    # Measure cap height at 1 em.
    bp = BoundsPen(glyphs)
    for ch in a.text:
        glyphs[cmap[ord(ch)]].draw(bp)
    cap_units = bp.bounds[3] - bp.bounds[1]
    sy = a.height / cap_units
    natural = sum(glyphs[cmap[ord(ch)]].width for ch in a.text) * sy
    sx = (a.width / natural) * sy
    d, _ = draw_word(font, a.text, sx, sy, a.x, a.y + a.height, a.tracking)
    bbox = BoundsPen(glyphs)
    x = a.x
    for ch in a.text:
        g = glyphs[cmap[ord(ch)]]
        g.draw(TransformPen(bbox, Transform(sx, 0, 0, -sy, x, a.y + a.height)))
        x += g.width * sx + a.tracking
    print(json.dumps({
        'd': d, 'x': a.x, 'y': a.y, 'width': a.width, 'height': a.height,
        'natural_width': round(natural, 1), 'xscale': round(sx / sy, 4),
    }))


if __name__ == '__main__':
    main()
