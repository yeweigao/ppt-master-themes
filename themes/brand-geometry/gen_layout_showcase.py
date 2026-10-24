#!/usr/bin/env python3
"""Brand Geometry on the shared a4-editorial Layout.

Writes examples/a4-editorial/<prototype>.svg. Each page is the Layout prototype
restyled with the Brand Geometry Theme DNA, using the fictional OSTRA identity:
the measured open-frame mark (6u field, 2u arm, 1u thickness) as the single
primitive family, one exposure move per page (complete, offset, parallel,
cropped, outline, matrix), the 1.0 / 0.58 / 0.34 overlap ladder, blue for
identity, gold for measurement, Georgia display with Arial reading and apparatus.
OSTRA is fictional; copy and figures are demonstration content.

    python3 themes/brand-geometry/gen_layout_showcase.py [--check]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "framework" / "scripts"))
from layout_showcase import Page, fit_report, text_markup  # noqa: E402

IMG = "../images/"
TOTAL = 8

PAPER, WARM, INK, BLUE, DEEP = "#FFFFFF", "#F7F5EE", "#14191C", "#14228F", "#0E1530"
GOLD, MUTED, LINE, PALE, BLUE_PALE, WHITE = "#A98B28", "#667077", "#D8D5CC", "#EEF0F4", "#E4E8F2", "#FFFFFF"
SERIF = "Georgia, 'Times New Roman', serif"
SANS = "Arial, Helvetica, sans-serif"


def mark(x, y, u, fill=BLUE, opacity=1.0, outline=False):
    """The OSTRA open frame at measure u (field 6u). Never redrawn, only scaled."""
    paths = [(0, 0, 2, 0, 2, 1, 1, 1, 1, 2, 0, 2), (6, 0, 6, 2, 5, 2, 5, 1, 4, 1, 4, 0),
             (6, 6, 4, 6, 4, 5, 5, 5, 5, 4, 6, 4), (0, 6, 0, 4, 1, 4, 1, 5, 2, 5, 2, 6)]
    d = " ".join("M " + " L ".join(f"{x + pts[i] * u:g} {y + pts[i + 1] * u:g}" for i in range(0, 12, 2)) + " Z"
                 for pts in paths)
    paint = (f'fill="none" stroke="{fill}" stroke-width="1.5" stroke-opacity="{opacity}"' if outline
             else f'fill="{fill}" fill-opacity="{opacity}"')
    return f'<path d="{d}" {paint}/>'


def offset_mark(x, y, u, step, fill=BLUE):
    """Offset move: three registrations on the 1.0 / 0.58 / 0.34 ladder."""
    return (mark(x + 2 * step, y + 2 * step, u, fill, 0.34) + mark(x + step, y + step, u, fill, 0.58)
            + mark(x, y, u, fill, 1.0))


def caps(p, id_, lines, x, y, fill=INK, anchor=None, lh=1.6, size=15):
    """Arial bold tracked capitals: the apparatus voice (15 px floor on A4)."""
    p.text(id_, lines, x=x, y=y, size=size, fill=fill, family=SANS, weight="bold", ls=2.6, anchor=anchor, lh=lh)


def caps_deco(text, x, y, fill=INK, anchor=None, lh=1.6):
    return text_markup(text, x=x, y=y, size=15, fill=fill, family=SANS, weight="bold", ls=2.6, anchor=anchor, lh=lh)


def header(p, label, dark=False):
    """Running header: the mark at u = 7 behaves like a folio, not a logo stamp."""
    fill = WHITE if dark else BLUE
    p.add(mark(100, 96, 7, fill), after="master-bg")
    caps(p, "kicker", label, 160, 124, WHITE if dark else INK)


def folio(p, n, dark=False):
    caps(p, "folio", f"{n:02d} / {TOTAL:02d}", 1140, 1668, WHITE if dark else MUTED, anchor="end")


def dimension(x1, x2, y, label):
    """Gold surveyor's dimension line with end ticks and a centred label."""
    return (f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{GOLD}" stroke-width="1.5"/>'
            f'<line x1="{x1}" y1="{y - 8}" x2="{x1}" y2="{y + 8}" stroke="{GOLD}" stroke-width="1.5"/>'
            f'<line x1="{x2}" y1="{y - 8}" x2="{x2}" y2="{y + 8}" stroke="{GOLD}" stroke-width="1.5"/>'
            + caps_deco(label, (x1 + x2) / 2, y - 14, GOLD, anchor="middle"))


def cover():
    p = Page("a4-editorial", "01_cover").lang("en").background(PAPER).ground(DEEP)
    p.image("hero", IMG + "lake.jpg")
    p.add(f'<rect width="1240" height="1754" fill="{DEEP}" fill-opacity="0.28"/>', after="hero")
    p.add(mark(900, 260, 64, WHITE, 0.92) + mark(1086, 1586, 9, BLUE_PALE, 0.85, outline=True), after="photo-shade")
    caps(p, "kicker", "OSTRA  /  THE OPEN FRAME", 100, 128, WHITE)
    p.text("title", ["The shape", "of a place."], size=112, fill=WHITE, family=SERIF, weight="bold", lh=1.02, ls=-2,
           y=1240)
    p.text("subtitle", ["A study in one measure.", "Four landscapes, one frame."], size=30, fill=WHITE, family=SANS,
           lh=1.45, y=1476)
    caps(p, "edition", "SELECTED WORK 2021–2026  ·  ARCHITECTURE / LANDSCAPE / URBANISM", 100, 1662,
         BLUE_PALE)
    return p


def chapter():
    p = Page("a4-editorial", "02_chapter").lang("en").background(PAPER).ground(DEEP)
    p.image("hero", IMG + "woodland.jpg")
    p.add(f'<rect width="1240" height="1754" fill="{DEEP}" fill-opacity="0.5"/>', after="hero")
    gold = "".join(f'<path d="{d}" fill="none" stroke="{GOLD}" stroke-width="4"/>' for d in (
        "M 100 150 V 100 H 150", "M 340 100 H 390 V 150", "M 390 270 V 320 H 340", "M 150 320 H 100 V 270"))
    p.add(gold, after="photo-shade")
    p.text("chapter-number", "02", x=150, y=250, size=150, fill=WHITE, family=SERIF, weight="bold")
    p.text("title", ["Site logic"], size=96, fill=WHITE, family=SERIF, weight="bold", ls=-1, y=1320)
    p.text("description", ["The plan is not a smaller drawing of a building.",
                           "It is a proposal for attention."], size=28, fill=BLUE_PALE, family=SANS, lh=1.45,
           y=1504)
    return p


def geometry():
    p = Page("a4-editorial", "03q_content_geometry").lang("en").background(PAPER)
    p.style("stepped-field", fill=PALE, fill_opacity="1")
    p.style("counterweight", fill_opacity="0")  # the identity has no circle; withhold it
    p.style("accent-block", fill=BLUE, fill_opacity="1")
    p.style("top-axis", stroke=INK, stroke_width="1").style("caption-rule", stroke=GOLD)
    p.style("interlock-glaze", fill=BLUE, fill_opacity="0.58").style("interlock-glaze-light", fill=BLUE, fill_opacity="0.34")
    p.style("photo-main-border", stroke_width="0").style("photo-detail-border", stroke_width="0")
    p.image("photo-main", IMG + "waterfall.jpg").image("photo-detail", IMG + "autumn.jpg")
    header(p, "OSTRA  /  03  ·  FALLS LOOKOUT")
    p.add(offset_mark(980, 214, 18, 12), after="top-axis")
    p.add(dimension(820, 1140, 1010, "SITE 03  ·  6u"), after="caption-rule")
    p.text("title", ["A frame reveals", "the falls."], size=72, fill=INK, family=SERIF, weight="bold", lh=1.06,
           ls=-1, y=270)
    p.text("note", ["A platform above the water", "line, set back one arm's", "length from the edge.", "",
                    "The opening faces north", "so the falls arrive in the", "frame before the sound does."],
           size=19, fill=INK, family=SANS, lh=1.5, y=634)
    p.text("main-copy", ["Every project begins with the same frame, then adjusts",
                         "to light, ground and use. Here the frame is turned",
                         "toward the water and left open at the top."], size=22, fill=INK, family=SANS, lh=1.5,
           y=1444)
    folio(p, 3)
    return p


def dual():
    p = Page("a4-editorial", "03a_content_dual").lang("en").background(PAPER).ground(WARM)
    p.style("header-rule", stroke=LINE).style("quote-rule", stroke=GOLD)
    header(p, "OSTRA  /  POSITION")
    bars = "".join(f'<rect x="{1140 - 12 - i * 24}" y="436" width="12" height="104" fill="{BLUE}" '
                   f'fill-opacity="{0.34 if i % 3 else 0.58}"/>' for i in range(8))
    p.add(bars, after="quote-rule")
    p.text("title", ["We design the", "space between."], size=76, fill=INK, family=SERIF, weight="bold", lh=1.06,
           ls=-1, y=280)
    p.text("lead", ["A building begins with a line. A place begins", "with the space that line leaves open."],
           size=28, fill=MUTED, family=SANS, lh=1.4, y=468)
    p.text("body-left", ["OSTRA works between structure and",
                         "ground: reading the site before",
                         "drawing the frame, and drawing the",
                         "frame before choosing a material.",
                         "",
                         "One measure keeps many voices in",
                         "the room. The width of a path, the",
                         "depth of a threshold and the interval",
                         "between trees are all set in the",
                         "same unit, so decisions made by",
                         "different people still agree."],
           size=22, fill=INK, family=SANS, lh=1.55, y=652)
    p.text("body-right", ["We are less interested in the object",
                          "than in what it frames. A good",
                          "opening shows you something you",
                          "had stopped looking at.",
                          "",
                          "That is why the mark is never",
                          "closed. Its centre is the work: a",
                          "lake, a ridge, a clearing, a street",
                          "corner. The four brackets only say",
                          "where to stand."],
           size=22, fill=INK, family=SANS, lh=1.55, y=652)
    p.text("takeaway", ["A frame is not a border.", "It is a decision about what to leave open."], size=38,
           fill=INK, family=SERIF, lh=1.3, y=1454)
    folio(p, 4)
    return p


def gallery():
    p = Page("a4-editorial", "03i_content_gallery").lang("en").background(PAPER)
    p.image("photo-wide", IMG + "horizon.jpg").image("photo-left", IMG + "dunes.jpg")
    p.image("photo-right", IMG + "ocean.jpg")
    corner = (f'<path d="M 0 0 H 240 V 120 H 120 V 240 H 0 Z" fill="{WHITE}" fill-opacity="0.92"/>'
              f'<path d="M 1240 740 H 1000 V 620 H 1120 V 500 H 1240 Z" fill="{WHITE}" fill-opacity="0.92"/>')
    p.add(corner, after="photo-wide")
    p.add(mark(100, 96, 7, BLUE), after="photo-wide")
    p.text("title", "Four sites. One measure.", size=60, fill=INK, family=SERIF, weight="bold", ls=-1, y=1405)
    p.text("lead", "Each project starts from the same frame, then adjusts to light, ground and use.", size=26,
           fill=MUTED, family=SANS, y=1502)
    caps(p, "source", "MOSS PAVILION  ·  DUNE CORRIDOR  ·  COAST STEP  —  FICTIONAL PROJECTS",
         100, 1636, MUTED)
    folio(p, 5)
    return p


def metrics():
    p = Page("a4-editorial", "03w_content_metrics_masonry").lang("en").background(PAPER)
    for i in range(1, 5):
        p.style(f"metric-rule-{i}", stroke=GOLD)
    p.style("canted-glaze", fill=BLUE, fill_opacity="0.34").style("canted-top-wedge", fill=PAPER)
    p.style("seam-interlock-1", fill=WHITE, fill_opacity="0.58").style("seam-interlock-2", fill=BLUE, fill_opacity="0.58")
    header(p, "OSTRA  /  THE SYSTEM IN NUMBERS")
    for i, (val, label) in enumerate([("6u", "FIELD"), ("2:1", "ARM : FRAME"), ("1u", "THICKNESS"), ("04", "SITES")]):
        p.text(f"metric-{i + 1}", val, size=96, fill=BLUE, family=SERIF, weight="bold", ls=-2, y=318)
        p.add(caps_deco(label, 100 + 270 * i, 390, MUTED), after="metric-rule-4")
    for i, (img, par) in enumerate([("lake.jpg", "xMidYMid slice"), ("dunes.jpg", "xMidYMid slice"),
                                    ("waterfall.jpg", "xMidYMid slice"), ("woodland.jpg", "xMidYMid slice"),
                                    ("autumn.jpg", "xMidYMid slice"), ("horizon.jpg", "xMinYMid slice"),
                                    ("ocean.jpg", "xMidYMid slice"), ("lake.jpg", "xMaxYMax slice")]):
        p.image(f"photo-{i + 1}", IMG + img, par=par)
    caps(p, "source", "ONE MEASURE, FOUR SITES  ·  PHOTOGRAPHY: WIKIMEDIA COMMONS, CC0", 100, 1626, MUTED)
    folio(p, 6)
    return p


def feature():
    p = Page("a4-editorial", "03ad_content_feature_panel").lang("en").background(PAPER)
    p.image("hero", IMG + "autumn.jpg", par="xMinYMid slice")
    p.style("photo-shade-bottom", fill="url(#feature-panel-bottom)")
    p.style("panel-rule", fill=BLUE).style("title-rule", fill=GOLD).style("quote-rule", fill=GOLD)
    p.add(mark(-120, 120, 40, WHITE, 0.92), after="photo-shade-bottom")
    caps(p, "kicker", "OSTRA  /  IN SITU", 780, 124, INK)
    p.text("title", ["The plan is", "a way of", "seeing."], size=56, fill=INK, family=SERIF, weight="bold", lh=1.05,
           ls=-1, y=256)
    p.text("lead", ["A proposal for what to keep,", "what to open and what to", "leave alone."], size=22,
           fill=MUTED, family=SANS, lh=1.45, y=446)
    p.text("body", ["Dune Corridor runs a raised walk",
                    "through a protected ridge. The frame",
                    "sets the walk's width at 2u and its",
                    "rest points at every 6u, so the path",
                    "reads as one measured line rather",
                    "than a string of viewpoints.",
                    "",
                    "Fences stay where the dune needs",
                    "them. The walk goes over, never",
                    "through."], size=20, fill=INK, family=SANS, lh=1.55, y=604)
    p.text("photo-quote", ["What we build", "is a way of looking."], size=46, fill=WHITE, family=SERIF,
           weight="bold", lh=1.15, y=1430)
    p.text("panel-note", ["The rest is", "maintenance."], size=30, fill=BLUE, family=SERIF, weight="bold", lh=1.2,
           y=1258)
    caps(p, "caption", ["SITE 02  ·  DUNE CORRIDOR", "PHOTOGRAPHY: WIKIMEDIA, CC0"], 780, 1592, MUTED)
    caps(p, "folio", f"07 / {TOTAL:02d}", 1140, 1716, MUTED, anchor="end")
    return p


def ending():
    p = Page("a4-editorial", "04_ending").lang("en").background(PAPER).ground(BLUE)
    p.image("hero", IMG + "ocean.jpg")
    p.style("closing-rule", stroke=WHITE, stroke_opacity="0.4")
    p.add(mark(940, 1000, 33, WHITE), after="closing-rule")
    p.text("title", ["Build the frame.", "Let the place speak."], size=72, fill=WHITE, family=SERIF, weight="bold",
           lh=1.12, ls=-1, y=1074)
    p.text("subtitle", "OSTRA  ·  Architecture, landscape and urbanism", size=28, fill=BLUE_PALE,
           family=SANS, y=1300)
    caps(p, "contact", ["STUDIO@OSTRA.EXAMPLE", "THE OPEN FRAME  ·  6u / 2u / 1u"], 100, 1494, WHITE, lh=1.75)
    caps(p, "closing", ["OSTRA IS A FICTIONAL IDENTITY.", "PROJECTS AND FIGURES ARE ILLUSTRATIVE."], 640, 1494,
         BLUE_PALE, lh=1.75)
    folio(p, 8, dark=True)
    return p


PAGES = [cover, chapter, geometry, dual, gallery, metrics, feature, ending]

# --- 16:9 (ppt169-editorial) ---------------------------------------------------
W169 = "ppt169-editorial"
TOTAL_169 = 6


def caps169(p, id_, lines, x, y, fill=INK, anchor=None, lh=1.6):
    p.text(id_, lines, x=x, y=y, size=14, fill=fill, family=SANS, weight="bold", ls=2.4, anchor=anchor, lh=lh)


def caps169_deco(text, x, y, fill=INK, anchor=None):
    return text_markup(text, x=x, y=y, size=14, fill=fill, family=SANS, weight="bold", ls=2.4, anchor=anchor)


def header169(p, label, dark=False):
    p.add(mark(80, 54, 5, WHITE if dark else BLUE), after="master-bg")
    caps169(p, "kicker", label, 124, 72, WHITE if dark else INK)


def folio169(p, n, dark=False):
    caps169(p, "folio", f"{n:02d} / {TOTAL_169:02d}", 1200, 676, WHITE if dark else MUTED, anchor="end")


def cover_169():
    p = Page(W169, "01_cover").lang("en").background(PAPER).ground(DEEP)
    p.image("hero", IMG + "lake.jpg")
    p.add(f'<rect width="1280" height="720" fill="{DEEP}" fill-opacity="0.28"/>', after="hero")
    p.add(mark(1064, 110, 40, WHITE, 0.92) + mark(1152, 610, 8, BLUE_PALE, 0.85, outline=True), after="photo-shade")
    caps169(p, "kicker", "OSTRA  /  THE OPEN FRAME", 80, 72, WHITE)
    p.text("title", ["The shape", "of a place."], size=68, fill=WHITE, family=SERIF, weight="bold", lh=1.02, ls=-1,
           y=480)
    p.text("subtitle", "A study in one measure. Four landscapes, one frame.", size=22, fill=WHITE, family=SANS, y=620)
    caps169(p, "edition", "SELECTED WORK 2021–2026  ·  ARCHITECTURE / LANDSCAPE / URBANISM", 80, 678, BLUE_PALE)
    return p


def chapter_169():
    p = Page(W169, "02_chapter").lang("en").background(PAPER).ground(DEEP)
    p.image("hero", IMG + "woodland.jpg")
    p.add(f'<rect width="1280" height="720" fill="{DEEP}" fill-opacity="0.5"/>', after="hero")
    gold = "".join(f'<path d="{d}" fill="none" stroke="{GOLD}" stroke-width="3"/>' for d in (
        "M 80 92 V 56 H 116", "M 324 56 H 360 V 92", "M 360 196 V 232 H 324", "M 116 232 H 80 V 196"))
    p.add(gold, after="photo-shade")
    p.text("chapter-number", "02", x=120, y=188, size=120, fill=WHITE, family=SERIF, weight="bold")
    p.text("title", "Site logic", size=60, fill=WHITE, family=SERIF, weight="bold", ls=-1, y=548)
    p.text("description", "The plan is not a smaller drawing of a building. It is a proposal for attention.",
           size=20, fill=BLUE_PALE, family=SANS, y=640)
    return p


def dual_169():
    p = Page(W169, "03b_content_dual").lang("en").background(PAPER).ground(WARM)
    p.style("header-rule", stroke=LINE).style("foot-rule", stroke=LINE)
    header169(p, "OSTRA  /  POSITION")
    p.add("".join(f'<rect x="{1200 - 10 - i * 20}" y="128" width="10" height="64" fill="{BLUE}" '
                  f'fill-opacity="{0.34 if i % 3 else 0.58}"/>' for i in range(8)), after="foot-rule")
    p.text("title", "We design the space between.", size=44, fill=INK, family=SERIF, weight="bold", ls=-1, y=166)
    p.text("lead", "A building begins with a line. A place begins with the space that line leaves open.",
           size=20, fill=MUTED, family=SANS, y=258)
    p.text("body-left", ["OSTRA works between structure and ground:", "reading the site before drawing the frame,",
                         "and drawing the frame before choosing a", "material. One measure keeps many voices",
                         "in the room."], size=18, fill=INK, family=SANS, lh=1.5, y=334)
    p.text("body-right", ["We are less interested in the object than in", "what it frames. That is why the mark is never",
                          "closed: its centre is the work — a lake, a", "ridge, a clearing. The four brackets only",
                          "say where to stand."], size=18, fill=INK, family=SANS, lh=1.5, y=334)
    caps169(p, "source", "OSTRA IS A FICTIONAL PRACTICE  ·  DEMONSTRATION COPY", 80, 668, MUTED)
    folio169(p, 3)
    return p


def overlay_169():
    p = Page(W169, "03k_content_overlay").lang("en").background(PAPER).ground(DEEP)
    p.image("hero", IMG + "waterfall.jpg")
    p.style("plate", fill=PAPER, fill_opacity="0.95").style("plate-rule", stroke=GOLD, stroke_opacity="1")
    p.add(offset_mark(1080, 178, 12, 8), after="plate-rule")
    caps169(p, "kicker", "OSTRA  /  SITE 03  ·  FALLS LOOKOUT", 80, 72, WHITE)
    p.text("title", ["A frame reveals", "the falls."], size=40, fill=INK, family=SERIF, weight="bold", lh=1.05, y=236)
    p.text("main-copy", ["A platform above the water line, set back one arm's length", "from the edge. The opening faces north, so the falls arrive",
                         "in the frame before the sound does."], size=18, fill=INK, family=SANS, lh=1.5, y=376)
    caps169(p, "source", "PHOTOGRAPHY: WIKIMEDIA COMMONS, CC0", 80, 668, WHITE)
    folio169(p, 4, dark=True)
    return p


def marginalia_169():
    p = Page(W169, "03g_content_marginalia").lang("en").background(PAPER)
    p.style("header-rule", stroke=LINE).style("margin-rule", stroke=GOLD).style("quote-rule", stroke=GOLD)
    header169(p, "OSTRA  /  THE SYSTEM")
    p.add(dimension(848, 1040, 222, "6u FIELD"), after="quote-rule")
    p.text("title", "One mark. Six moves.", size=44, fill=INK, family=SERIF, weight="bold", ls=-1, y=166)
    p.text("main-copy", ["The mark is not repeated as decoration. It is decomposed into a",
                         "working vocabulary: complete, offset, parallel, cropped, outline",
                         "and matrix. One move leads each page; a second may appear only",
                         "if it is quiet.", "",
                         "Every move keeps the same thickness of 1u, the same stepped",
                         "inner contour and the same open centre. Scale changes; the",
                         "proportions never do."], size=18, fill=INK, family=SANS, lh=1.5, y=262)
    p.text("note-1", ["The arm is 2u long, the", "frame 1u thick, the opening", "2u wide. Recognition comes",
                      "from the interval, not from", "repetition."], size=15, fill=MUTED, family=SANS, lh=1.5, y=262)
    p.text("pull-quote", ["The mark sets proportion.", "The page sets scale."], size=22, fill=BLUE, family=SERIF,
           weight="bold", lh=1.3, y=516)
    caps169(p, "source", "OSTRA IS A FICTIONAL IDENTITY", 80, 668, MUTED)
    folio169(p, 5)
    return p


def ending_169():
    p = Page(W169, "04_ending").lang("en").background(PAPER).ground(BLUE)
    p.image("hero", IMG + "ocean.jpg")
    p.style("closing-rule", stroke=WHITE, stroke_opacity="0.4")
    p.add(mark(1068, 420, 22, WHITE), after="closing-rule")
    p.text("title", "Build the frame. Let the place speak.", size=44, fill=WHITE, family=SERIF, weight="bold",
           ls=-1, y=484)
    p.text("subtitle", "OSTRA  ·  Architecture, landscape and urbanism", size=20, fill=BLUE_PALE, family=SANS,
           y=552)
    caps169(p, "contact", ["STUDIO@OSTRA.EXAMPLE", "6u / 2u / 1u"], 80, 610, WHITE)
    caps169(p, "closing", ["OSTRA IS A FICTIONAL IDENTITY.", "PROJECTS ARE ILLUSTRATIVE."], 656, 610, BLUE_PALE)
    folio169(p, 6, dark=True)
    return p


PAGES_169 = [cover_169, chapter_169, dual_169, overlay_169, marginalia_169, ending_169]


if __name__ == "__main__":
    issues, counts = [], {}
    for build in PAGES + PAGES_169:
        page = build()
        page.save(HERE / "examples" / page.layout / f"{page.prototype}.svg")
        counts[page.layout] = counts.get(page.layout, 0) + 1
        issues += fit_report(page)
    print("wrote " + ", ".join(f"{n} pages to examples/{k}" for k, n in counts.items()))
    if "--check" in sys.argv:
        print("\n".join(issues) or "fit check: no issues")
