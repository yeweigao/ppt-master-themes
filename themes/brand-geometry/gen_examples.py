#!/usr/bin/env python3
"""Generate the OSTRA brand-geometry example suite (A4, 1240x1754)."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "examples" / "svg"
OUT.mkdir(parents=True, exist_ok=True)

WHITE = "#FFFFFF"
PAPER = "#F7F5EE"
INK = "#14191C"
BLUE = "#14228F"
DEEP = "#0E1530"
GOLD = "#A98B28"
MUTED = "#667077"
LINE = "#D8D5CC"
PALE = "#EEF0F4"
BLUE_PALE = "#E4E8F2"
W, H = 1240, 1754


def n(value):
    return str(int(value)) if float(value).is_integer() else f"{value:g}"


def text(x, y, content, size=18, fill=INK, family="Arial", weight="normal",
         ls=None, italic=False, anchor="start", leading=None, opacity=None):
    # A4 legibility floor: nothing below 14 px (about 6.7 pt in print). Labels that
    # were drawn at 9-11 px are raised to the floor and their tracking tightened in
    # proportion, so the line keeps roughly its old length.
    if size < 14:
        if ls is not None:
            ls = round(float(ls) * size / 14, 2)
        size = 14
    attrs = [f'x="{n(x)}"', f'y="{n(y)}"', f'fill="{fill}"', f'font-size="{n(size)}"']
    if family != "Arial":
        attrs.append(f'font-family="{family}"')
    if weight != "normal":
        attrs.append(f'font-weight="{weight}"')
    if ls is not None:
        attrs.append(f'letter-spacing="{ls}"')
    if italic:
        attrs.append('font-style="italic"')
    if anchor != "start":
        attrs.append(f'text-anchor="{anchor}"')
    if opacity is not None:
        attrs.append(f'fill-opacity="{opacity}"')
    lines = content if isinstance(content, (list, tuple)) else [content]
    body = escape(str(lines[0]))
    if len(lines) > 1:
        dy = leading if leading is not None else round(size * 1.3, 2)
        body += "".join(f'<tspan x="{n(x)}" dy="{n(dy)}">{escape(str(line))}</tspan>' for line in lines[1:])
    return f'<text {" ".join(attrs)}>{body}</text>'


def rect(x, y, width, height, fill="none", stroke=None, sw=1, opacity=None,
         role=None, dash=None):
    attrs = [f'x="{n(x)}"', f'y="{n(y)}"', f'width="{n(width)}"', f'height="{n(height)}"', f'fill="{fill}"']
    if stroke:
        attrs += [f'stroke="{stroke}"', f'stroke-width="{n(sw)}"']
    if opacity is not None:
        attrs.append(f'fill-opacity="{opacity}"')
    if dash:
        attrs.append(f'stroke-dasharray="{dash}"')
    if role:
        attrs.append(f'data-pptx-role="{role}"')
    return f'<rect {" ".join(attrs)}/>'


def line(x1, y1, x2, y2, stroke=INK, sw=1, opacity=None, role=None):
    attrs = [f'x1="{n(x1)}"', f'y1="{n(y1)}"', f'x2="{n(x2)}"', f'y2="{n(y2)}"',
             f'stroke="{stroke}"', f'stroke-width="{n(sw)}"']
    if opacity is not None:
        attrs.append(f'stroke-opacity="{opacity}"')
    if role:
        attrs.append(f'data-pptx-role="{role}"')
    return f'<line {" ".join(attrs)}/>'


def image(x, y, width, height, href):
    return (f'<image x="{n(x)}" y="{n(y)}" width="{n(width)}" height="{n(height)}" '
            f'preserveAspectRatio="xMidYMid slice" href="../images/{href}"/>')


def mark_polygons(u):
    return [
        [(0, 0), (2 * u, 0), (2 * u, u), (u, u), (u, 2 * u), (0, 2 * u)],
        [(6 * u, 0), (6 * u, 2 * u), (5 * u, 2 * u), (5 * u, u), (4 * u, u), (4 * u, 0)],
        [(6 * u, 6 * u), (4 * u, 6 * u), (4 * u, 5 * u), (5 * u, 5 * u), (5 * u, 4 * u), (6 * u, 4 * u)],
        [(0, 6 * u), (0, 4 * u), (u, 4 * u), (u, 5 * u), (2 * u, 5 * u), (2 * u, 6 * u)],
    ]


def _clip_polygon(points, bounds):
    """Sutherland–Hodgman clip so previews and PPTX never rely on clip-path."""
    x0, y0, x1, y1 = bounds

    def inside(point, edge):
        x, y = point
        return {"l": x >= x0, "r": x <= x1, "t": y >= y0, "b": y <= y1}[edge]

    def intersect(start, end, edge):
        sx, sy = start
        ex, ey = end
        if edge in "lr":
            x = x0 if edge == "l" else x1
            ratio = 0 if ex == sx else (x - sx) / (ex - sx)
            return x, sy + ratio * (ey - sy)
        y = y0 if edge == "t" else y1
        ratio = 0 if ey == sy else (y - sy) / (ey - sy)
        return sx + ratio * (ex - sx), y

    polygon = points
    for edge in ("l", "r", "t", "b"):
        if not polygon:
            break
        source, polygon = polygon, []
        start = source[-1]
        for end in source:
            if inside(end, edge):
                if not inside(start, edge):
                    polygon.append(intersect(start, end, edge))
                polygon.append(end)
            elif inside(start, edge):
                polygon.append(intersect(start, end, edge))
            start = end
    return polygon


def _path(points, x=0, y=0):
    if not points:
        return ""
    return "M" + "L".join(f"{n(x + px)} {n(y + py)}" for px, py in points) + "Z"


def mark(x, y, u, color=BLUE, opacity=1.0, indices=None, bounds=None):
    selected = indices if indices is not None else range(4)
    paths = []
    for index in selected:
        points = mark_polygons(u)[index]
        if bounds is not None:
            points = _clip_polygon([(x + px, y + py) for px, py in points], bounds)
            paths.append(_path(points))
        else:
            paths.append(_path(points, x, y))
    body = "".join(f'<path d="{d}"/>' for d in paths if d)
    return (f'<g fill="{color}" fill-opacity="{opacity}" '
            f'data-pptx-role="decoration">{body}</g>')


def mark_layers(x, y, u, color=BLUE, steps=((0, 1.0), (0.5, 0.58), (1.0, 0.34)),
                indices=None, bounds=None):
    return "".join(
        mark(x + offset * u, y + offset * u, u, color, opacity, indices, bounds)
        for offset, opacity in steps
    )


def outline_mark(x, y, u, color=WHITE, sw=2, opacity=0.4, indices=None):
    selected = indices if indices is not None else range(4)
    paths = "".join(
        f'<path d="{_path(mark_polygons(u)[index], x, y)}"/>' for index in selected
    )
    return (f'<g fill="none" stroke="{color}" stroke-width="{n(sw)}" '
            f'stroke-opacity="{opacity}">{paths}</g>')


def crop_corners(x, y, width, height, arm=52, thick=10, color=WHITE, opacity=1):
    a, t = arm, thick
    paths = [
        f"M{n(x)} {n(y)}H{n(x+a)}V{n(y+t)}H{n(x+t)}V{n(y+a)}H{n(x)}Z",
        f"M{n(x+width)} {n(y)}H{n(x+width-a)}V{n(y+t)}H{n(x+width-t)}V{n(y+a)}H{n(x+width)}Z",
        f"M{n(x+width)} {n(y+height)}H{n(x+width-a)}V{n(y+height-t)}H{n(x+width-t)}V{n(y+height-a)}H{n(x+width)}Z",
        f"M{n(x)} {n(y+height)}H{n(x+a)}V{n(y+height-t)}H{n(x+t)}V{n(y+height-a)}H{n(x)}Z",
    ]
    return (f'<g fill="{color}" fill-opacity="{opacity}" data-pptx-role="decoration">'
            + "".join(f'<path d="{d}"/>' for d in paths) + "</g>")


def header(page_no, section, dark=False):
    ink = WHITE if dark else INK
    brand = WHITE if dark else BLUE
    muted = "#B9C2D4" if dark else MUTED
    return "".join([
        mark(100, 64, 12, brand),
        text(180, 84, "OSTRA / THE OPEN FRAME", 10, ink, ls=3.4),
        text(180, 104, "ARCHITECTURE / LANDSCAPE / URBANISM", 9, muted, ls=2.6),
        text(1140, 84, section, 10, muted, ls=3, anchor="end"),
        text(1140, 104, f"{page_no:02d} / 08", 10, ink, ls=3, anchor="end"),
    ])


def footer(page_no, note="FICTIONAL IDENTITY STUDY / DEMONSTRATION ONLY", dark=False):
    ink = WHITE if dark else INK
    muted = "#AEB8CA" if dark else MUTED
    stroke = "#43506B" if dark else LINE
    return "".join([
        line(100, 1648, 1140, 1648, stroke, 1),
        text(100, 1680, "OSTRA", 10, ink, ls=3.6),
        text(160, 1680, note, 9, muted, ls=2.2),
        text(1140, 1680, f"{page_no:02d} / 08", 10, ink, ls=3, anchor="end"),
    ])


def page(name, body, bg=WHITE, title="", desc=""):
    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1240 1754" '
        'font-family="Arial" data-pptx-master="a4-editorial" data-pptx-master-name="A4 Editorial" '
        f'data-pptx-layout="ostra-{escape(name)}" data-pptx-layout-name="{escape(title)}">',
        f"<title>{escape(title)}</title><desc>{escape(desc)}</desc>",
        rect(0, 0, W, H, bg, role="background"),
        body,
        "</svg>",
    ]
    (OUT / f"{name}.svg").write_text("\n".join(svg) + "\n")
    return name


def page_cover():
    b = []
    b.append(header(1, "VOLUME 01 / SELECTED WORK"))
    for x in [278, 456, 634, 812, 990]:
        b.append(line(x, 150, x, 1600, INK, 1, 0.045))
    b.append(text(100, 326, "THE SHAPE", 158, INK, "Georgia", "bold", leading=180))
    b.append(text(100, 686, "OF A PLACE.", 158, INK, "Georgia", "bold"))
    b.append(line(100, 776, 560, 776, GOLD, 2))
    b.append(text(100, 832, "A study in one measure. Four landscapes, one frame.", 26, MUTED))
    b.append(text(100, 876, "An identity built from a frame, a void and a repeatable interval.", 18, MUTED, opacity=0.9))
    b.append(mark_layers(700, 900, 64, BLUE, indices=(0, 2)))
    b.append(text(700, 1380, "THE OPEN FRAME", 10, BLUE, ls=3.2))
    b.append(text(700, 1402, "4 × L / 6u FIELD / 2:1 ARM", 9, MUTED, ls=2.2))
    b.append(line(100, 1450, 1140, 1450, LINE, 1))
    b.append(text(100, 1508, "Selected work 2021—2026", 18, INK))
    b.append(text(1140, 1508, "FICTIONAL IDENTITY / NOT A REAL PRACTICE", 9, MUTED, ls=2.2, anchor="end"))
    b.append(text(100, 1546, "Architecture / Landscape / Urbanism", 15, MUTED))
    b.append(text(1140, 1546, "DEMONSTRATION PAGES", 9, MUTED, ls=2.2, anchor="end"))
    b.append(footer(1))
    return page("01_cover", "".join(b), WHITE, "The shape of a place", "OSTRA identity cover with the complete open-frame mark and layered construction offsets.")


def page_identity():
    b = []
    b.append(header(2, "IDENTITY / CONSTRUCTION"))
    b.append(text(100, 190, "01 / IDENTITY CONSTRUCTION", 11, BLUE, ls=3.2))
    b.append(text(100, 300, "A mark is a plan.", 88, INK, "Georgia", "bold"))
    b.append(text(100, 366, ["Four corner brackets, drawn on a six-unit field. Each arm is two units long, one unit thick.", "The opening is not empty; it is the subject."], 18, MUTED, leading=27))
    # construction drawing
    gx, gy, u = 100, 540, 56
    for i in range(7):
        b.append(line(gx + i * u, gy, gx + i * u, gy + 6 * u, LINE, 1))
        b.append(line(gx, gy + i * u, gx + 6 * u, gy + i * u, LINE, 1))
    b.append(mark(gx, gy, u))
    # dimension lines
    b.append(line(gx, gy - 44, gx + 6 * u, gy - 44, GOLD, 1))
    b.append(line(gx, gy - 52, gx, gy - 36, GOLD, 1))
    b.append(line(gx + 6 * u, gy - 52, gx + 6 * u, gy - 36, GOLD, 1))
    b.append(text(gx + 3 * u, gy - 54, "6u", 11, GOLD, ls=2, anchor="middle"))
    b.append(line(gx - 44, gy, gx - 44, gy + 6 * u, GOLD, 1))
    b.append(line(gx - 52, gy, gx - 36, gy, GOLD, 1))
    b.append(line(gx - 52, gy + 6 * u, gx - 36, gy + 6 * u, GOLD, 1))
    b.append(text(gx - 54, gy + 3 * u, "6u", 11, GOLD, ls=2, anchor="middle"))
    b.append(line(gx + 2 * u, gy + 6 * u + 34, gx + 4 * u, gy + 6 * u + 34, GOLD, 1))
    b.append(text(gx + 3 * u, gy + 6 * u + 58, "OPENING / 2u", 10, GOLD, ls=2, anchor="middle"))
    b.append(line(gx + 6 * u + 24, gy, gx + 6 * u + 24, gy + u, GOLD, 1))
    b.append(text(gx + 6 * u + 36, gy + 8, "FRAME / 1u", 10, GOLD, ls=1.8))
    b.append(text(gx + 6 * u + 36, gy + 30, "ARM / 2u", 10, GOLD, ls=1.8))
    b.append(text(gx + 6 * u + 36, gy + 52, "GAP / 2u", 10, GOLD, ls=1.8))
    # state panels
    px = 600
    b.append(text(px, 526, "THE MARK IN USE", 11, BLUE, ls=3))
    states = [
        (px, 548, 250, WHITE, BLUE, "PRIMARY / ON PAPER", MUTED),
        (880, 548, 260, BLUE, WHITE, "REVERSED / ON FIELD", WHITE),
    ]
    for x, y, width, bg, fg, label, label_fill in states:
        b.append(rect(x, y, width, 168, bg, stroke=LINE if bg == WHITE else None, sw=1))
        b.append(text(x + 20, y + 26, label, 9, label_fill, ls=1.9))
        b.append(mark(x + (width - 108) / 2, y + 44, 18, fg))
    # cropped state: real vector crop, no clip-path dependency
    b.append(rect(px, 750, 540, 190, BLUE_PALE))
    b.append(text(px + 20, 780, "CROPPED / AT THE EDGE", 9, BLUE, ls=1.9))
    b.append(mark(1020, 760, 28, BLUE, bounds=(px, 750, 1140, 940)))
    b.append(rect(px, 750, 540, 190, "none", stroke=LINE, sw=1))
    b.append(text(px, 968, "One frame, three registers. The crop is never an accident.", 12, MUTED))
    b.append(line(px, 1000, 1140, 1000, LINE, 1))
    b.append(text(px, 1054, "The rule", 26, INK, "Georgia", "bold"))
    rows = [("6u", "field. The same measure as the page's six tracks."),
            ("2:1", "arm. Long enough to carry a crop, short enough to read as a corner."),
            ("1u", "frame. The thickness never changes with scale.")]
    for i, (key, body) in enumerate(rows):
        y = 1102 + i * 60
        b.append(text(px, y, key, 24, BLUE, "Georgia", "bold"))
        b.append(text(px + 78, y, body, 14.5, MUTED))
        if i < 2:
            b.append(line(px, y + 28, 1140, y + 28, LINE, 1))
    b.append(text(px, 1268, ["The mark is never redrawn. It is measured, cropped,", "repeated and allowed to meet the site."], 17, INK, leading=26))
    b.append(line(100, 1040, 540, 1040, GOLD, 2))
    b.append(text(100, 1122, ["Construction", "is the identity."], 44, INK, "Georgia", "italic", leading=52))
    b.append(text(100, 1250, ["Every page keeps one measurable relationship to the", "frame; recognition comes from the interval, not", "the ornament."], 16, MUTED, leading=25))
    b.append(line(100, 1440, 1140, 1440, LINE, 1))
    b.append(text(100, 1512, "The frame is the argument. The opening is the work.", 38, INK, "Georgia", "italic"))
    b.append(footer(2))
    return page("02_identity", "".join(b), WHITE, "A mark is a plan", "Measured construction drawing and three states of the OSTRA mark.")


def page_position():
    b = []
    b.append(header(3, "POSITION / THE IN-BETWEEN"))
    b.append(text(100, 190, "02 / POSITION", 11, BLUE, ls=3.2))
    b.append(text(100, 400, ["We design", "the space", "between."], 112, INK, "Georgia", "bold", leading=118))
    # measured field: grid, one solid corner, three outlined registrations
    gx, gy, gu = 840, 180, 50
    for i in range(7):
        b.append(line(gx + i * gu, gy, gx + i * gu, gy + 6 * gu, LINE, 1))
        b.append(line(gx, gy + i * gu, gx + 6 * gu, gy + i * gu, LINE, 1))
    b.append(outline_mark(gx, gy, gu, BLUE, 1, 0.55))
    b.append(mark(gx, gy, gu, BLUE, 0.92, indices=(0,)))
    b.append(text(gx + 3 * gu, gy - 18, "6u FIELD / 1u FRAME", 9, BLUE, ls=2, anchor="middle"))
    b.append(line(100, 800, 620, 800, GOLD, 2))
    b.append(text(100, 872, ["A building begins with a line. A place begins", "with the space that line leaves open. OSTRA", "works between structure and ground — reading", "the site before drawing the frame."], 18, MUTED, leading=29))
    b.append(text(700, 872, ["Between architecture, landscape and urbanism.", "One measure keeps many voices in the room:", "the width of a path, the depth of a threshold,", "the interval between trees."], 18, MUTED, leading=29))
    b.append(text(100, 1092, "We are less interested in the object than in what it frames.", 20, INK))
    # the mark becomes an edge condition: two left corners, three registrations
    b.append(mark_layers(1020, 1040, 80, BLUE, steps=((0, 0.9), (0.5, 0.22), (1.0, 0.1)), indices=(0, 3)))
    b.append(line(100, 1270, 780, 1270, LINE, 1))
    b.append(text(100, 1360, ["A frame is not a border.", "It is a decision about what to leave open."], 38, INK, "Georgia", "italic", leading=52))
    b.append(text(100, 1490, "THE OPEN FRAME / NOTES ON PRACTICE", 9.5, MUTED, ls=2.6))
    b.append(footer(3))
    return page("03_position", "".join(b), WHITE, "We design the space between", "Manifesto page with a cropped brand fragment and a clear reading field.")


def page_window():
    b = []
    b.append(header(4, "SITE / THE OPENING"))
    b.append(text(100, 190, "03 / SITE", 11, BLUE, ls=3.2))
    b.append(text(100, 286, "The frame does not", 62, INK, "Georgia", "bold"))
    b.append(text(100, 356, "hold the view.", 62, INK, "Georgia", "bold"))
    b.append(text(100, 426, "It reveals it.", 62, BLUE, "Georgia", "italic"))
    b.append(text(100, 472, "A single opening, cut into a working landscape. The geometry does not cover the image; it gives the eye a place to begin.", 16, MUTED))
    b.append(image(100, 540, 1040, 860, "lake.jpg"))
    # the mark itself becomes the crop: 2u arms, 1u thickness at photo scale
    b.append(mark(100, 540, 110, WHITE, 0.88, indices=(0,)))
    b.append(mark(480, 740, 110, WHITE, 0.88, indices=(2,)))
    b.append(text(100, 1460, ["Moss Pavilion sits at the edge of a clearing. The frame opens north", "to the water; the reading bench follows the shade line."], 18, INK, leading=27))
    b.append(text(100, 1540, "PHOTO: BONNIE MORELAND / CC0 1.0", 9, MUTED, ls=2.2))
    b.append(text(1140, 1460, "SITE STUDY 01", 10, BLUE, ls=2.6, anchor="end"))
    b.append(text(1140, 1484, "LAKE / 2026", 9, MUTED, ls=2.2, anchor="end"))
    b.append(footer(4))
    return page("04_window", "".join(b), WHITE, "The frame reveals the view", "Full-bleed site photograph with white and blue crop geometry derived from the mark.")


def page_system():
    b = []
    b.append(header(5, "SYSTEM / SIX MOVES"))
    b.append(text(100, 190, "04 / THE SYSTEM", 11, BLUE, ls=3.2))
    b.append(text(100, 320, "One mark.", 96, INK, "Georgia", "bold"))
    b.append(text(100, 426, "Six moves.", 96, BLUE, "Georgia", "bold"))
    b.append(text(740, 332, ["The mark is not repeated as decoration.", "It is decomposed into a working vocabulary."], 16, MUTED, leading=25))
    tiles = [
        (100, 540, "01 / FRAME", "Complete. Measured. Never distorted."),
        (460, 540, "02 / OFFSET", "Three registrations reveal the construction."),
        (820, 540, "03 / RHYTHM", "The 1-unit arm becomes a repeatable interval."),
        (100, 1010, "04 / CROP", "Scale until the mark becomes a structure."),
        (460, 1010, "05 / WINDOW", "Let an image pass through the opening."),
        (820, 1010, "06 / FIELD", "Repeat at low contrast to build a ground."),
    ]
    for idx, (x, y, label, caption) in enumerate(tiles):
        w, h = 320, 410
        b.append(line(x, y, x + w, y, BLUE, 2))
        b.append(text(x, y + 28, label, 10, BLUE, ls=2.4))
        b.append(rect(x, y + 48, w, 270, BLUE if idx == 1 else PALE))
        if idx == 0:
            b.append(mark(x + 88, y + 103, 24, BLUE))
        elif idx == 1:
            b.append(mark_layers(x + 86, y + 103, 22, WHITE, steps=((0, 0.95), (0.5, 0.58), (1.0, 0.34))))
        elif idx == 2:
            for j in range(9):
                b.append(rect(x + 38 + j * 28, y + 88, 10, 174, BLUE, opacity=0.12 + j * 0.055))
        elif idx == 3:
            b.append(mark(x + 40, y + 60, 50, BLUE, bounds=(x, y + 48, x + w, y + 318)))
            b.append(rect(x, y + 48, w, 270, "none", stroke=LINE, sw=1))
        elif idx == 4:
            b.append(image(x + 30, y + 78, 260, 210, "waterfall.jpg"))
            b.append(mark(x + 30, y + 78, 26, WHITE, 0.94, indices=(0,)))
            b.append(outline_mark(x + 134, y + 132, 26, BLUE, 1.5, 0.8, indices=(2,)))
        else:
            for row in range(3):
                for col in range(3):
                    b.append(mark(x + 62 + col * 72, y + 85 + row * 72, 8, BLUE, 0.22))
        b.append(text(x, y + 350, caption, 15, MUTED))
        b.append(line(x, y + 374, x + w, y + 374, LINE, 1))
    b.append(text(100, 1530, ["The mark sets proportion. The page sets scale.", "Recognition comes from the interval, not from repetition."], 22, INK, "Georgia", leading=32))
    b.append(footer(5))
    return page("05_system", "".join(b), WHITE, "One mark, six moves", "Specimen page showing six derived composition moves from the OSTRA mark.")


def page_works():
    b = []
    b.append(header(6, "WORK / FOUR SITES"))
    b.append(text(100, 190, "05 / SELECTED WORK", 11, BLUE, ls=3.2))
    b.append(text(100, 302, ["Four sites.", "One measure."], 88, INK, "Georgia", "bold", leading=94))
    b.append(text(760, 322, ["Each project begins with the same frame,", "then adjusts to light, ground and use.", "Names and figures are illustrative."], 16, MUTED, leading=26))
    projects = [
        ("01", "Moss Pavilion", "A reading room in a clearing", "NORTH LAKE / 2025 / 240 m²", "lake.jpg"),
        ("02", "Dune Corridor", "A wind-shaped path across a ridge", "COASTAL RIDGE / 2024 / 1.8 km", "dunes.jpg"),
        ("03", "Falls Lookout", "A platform above the water line", "UPPER FALLS / 2023 / 180 m²", "waterfall.jpg"),
        ("04", "Understory Walk", "A raised walk through old forest", "WEST WOODLAND / 2022 / 2.4 km", "woodland.jpg"),
    ]
    for i, (num, name, desc, meta, img) in enumerate(projects):
        x = 100 if i % 2 == 0 else 630
        y = 540 if i < 2 else 1060
        b.append(image(x, y, 510, 340, img))
        b.append(mark(x, y, 42, WHITE, 0.92, indices=(0,)))
        b.append(outline_mark(x + 258, y + 88, 42, BLUE, 1.5, 0.85, indices=(2,)))
        b.append(text(x, y + 388, name, 34, INK, "Georgia", "bold"))
        b.append(text(x, y + 416, desc, 15, MUTED))
        b.append(text(x, y + 442, f"{num} / {meta}", 9.5, BLUE, ls=2.2))
    b.append(text(100, 1560, "Fictional projects for composition study; no client, site or outcome is represented.", 11, MUTED, ls=1.6))
    b.append(footer(6))
    return page("06_work", "".join(b), WHITE, "Four sites, one measure", "Four-project matrix with crop-mark geometry and clean captions.")


def page_insitu():
    b = []
    b.append(header(7, "IN SITU / SITE LOGIC", dark=True))
    b.append(text(100, 190, "06 / IN SITU", 11, GOLD, ls=3.2))
    b.append(text(100, 338, "The plan is", 92, WHITE, "Georgia", "bold"))
    b.append(text(100, 440, "a way of", 92, WHITE, "Georgia", "bold"))
    b.append(text(100, 542, "seeing.", 92, GOLD, "Georgia", "italic"))
    b.append(text(100, 640, ["A plan is not a smaller drawing of a building.", "It is a proposal for attention: what to keep,", "what to open, what to leave alone."], 19, "#D5DBE8", leading=30))
    b.append(image(640, 300, 500, 660, "horizon.jpg"))
    b.append(rect(640, 300, 500, 660, DEEP, opacity=0.28))
    b.append(crop_corners(640, 300, 500, 660, arm=48, thick=24, color=GOLD, opacity=0.95))
    b.append(text(640, 988, "EDGE CONDITION / 01", 9, WHITE, ls=2.4))
    b.append(line(100, 1040, 540, 1040, "#43506B", 1))
    b.append(text(100, 1102, ["What we build is a way of looking.", "The rest is maintenance."], 24, WHITE, "Georgia", leading=34))
    metrics = [("04", "SITES"), ("03", "CLIMATES"), ("01", "FRAME")]
    for i, (value, label) in enumerate(metrics):
        x = 100 + i * 160
        b.append(text(x, 1330, value, 58, GOLD, "Georgia", "bold"))
        b.append(text(x, 1358, label, 9, "#AEB8CA", ls=2.4))
    b.append(text(640, 1330, ["The mark is not applied to the site.", "It is calibrated to it."], 18, "#D5DBE8", leading=28))
    b.append(text(100, 1540, "SITE LOG / NORTH COAST / 2026", 9, "#AEB8CA", ls=2.4))
    b.append(text(1140, 1540, "THE OPEN FRAME / 6u", 9, "#AEB8CA", ls=2.4, anchor="end"))
    b.append(footer(7, dark=True))
    return page("07_insitu", "".join(b), DEEP, "The plan is a way of seeing", "Dark site-logic page with outlined mark, photograph and measured metrics.")


def page_closing():
    b = []
    b.append(header(8, "CLOSING / CONTACT"))
    b.append(text(100, 190, "07 / CLOSING", 11, BLUE, ls=3.2))
    b.append(text(100, 360, ["Build the frame.", "Let the place speak."], 94, INK, "Georgia", "bold", leading=102))
    b.append(text(100, 568, ["OSTRA is a fictional architecture and landscape practice made for this", "identity study. The mark, projects and figures are illustrative."], 17, MUTED, leading=26))
    b.append(mark_layers(760, 660, 58, BLUE, steps=((0, 1.0), (0.5, 0.34), (1.0, 0.12)), indices=(0, 2)))
    b.append(text(760, 1150, "THE OPEN FRAME / 4 × L / 6u FIELD", 10, BLUE, ls=2.8))
    b.append(rect(0, 1180, W, 574, BLUE))
    b.append(mark(100, 1268, 48, WHITE))
    b.append(text(540, 1392, "OSTRA", 116, WHITE, "Georgia", "bold", ls=6))
    b.append(line(540, 1424, 1140, 1424, GOLD, 2))
    b.append(text(540, 1474, "ARCHITECTURE / LANDSCAPE / URBANISM", 11, WHITE, ls=2.6))
    b.append(text(540, 1544, "studio@ostra.example", 18, WHITE))
    b.append(text(540, 1576, "Fictional identity study / no real practice or client", 10, "#C9D2E3", ls=1.6))
    b.append(text(1140, 1600, "08 / 08", 10, WHITE, ls=3, anchor="end"))
    return page("08_closing", "".join(b), WHITE, "Build the frame, let the place speak", "Closing page with the OSTRA lockup and an honest fictional-identity note.")


def main():
    pages = [page_cover(), page_identity(), page_position(), page_window(),
             page_system(), page_works(), page_insitu(), page_closing()]
    print(f"Wrote {len(pages)} SVG pages to {OUT}")


if __name__ == "__main__":
    main()
