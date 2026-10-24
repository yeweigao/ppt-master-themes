#!/usr/bin/env python3
"""NatGeo Editorial on the shared 16:9 Layout (ppt169-editorial).

The A4 showcase in examples/svg/ was authored by hand on a4-editorial; this
script adds the 16:9 pages in examples/ppt169-editorial/. Each page is the
Layout prototype restyled with the NatGeo Theme DNA: warm rice paper for
reading, near-black scrims for turns, lemon yellow as the single identity
accent, a bold serif for claims and numerals against condensed tracked
capitals and a neutral sans, and purposeful photography at trim-edge scale.
Copy is demonstration text; photographs are CC0 (see examples/PHOTOS.md).

    python3 themes/natgeo/gen_layout_showcase.py [--check]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "framework" / "scripts"))
from layout_showcase import Page, fit_report, text_markup  # noqa: E402

IMG = "../images/"
W169 = "ppt169-editorial"
TOTAL = 6

PAPER, INK, LEMON, DEEP_LEMON, MUTED, RULE, WHITE = "#F7F3E8", "#111111", "#FFE500", "#6E6000", "#5C5C5C", "#D9D9D9", "#FFFFFF"
SERIF = "Georgia, 'Times New Roman', serif"
NARROW = "'Arial Narrow', Arial, sans-serif"
SANS = "Arial, Helvetica, sans-serif"


def kicker(p, id_, lines, x, y, fill=INK, anchor=None, lh=1.6, weight="bold"):
    """Condensed tracked capitals: kickers, running heads, captions (14 px)."""
    p.text(id_, lines, x=x, y=y, size=14, fill=fill, family=NARROW, weight=weight, ls=2.4, anchor=anchor, lh=lh)


def folio(p, n, fill=INK):
    kicker(p, "folio", f"{n:02d} / {TOTAL:02d}", 1200, 676, fill, anchor="end")


def bar(x, y, w=56):
    return f'<rect x="{x}" y="{y}" width="{w}" height="6" fill="{LEMON}"/>'


def cover():
    p = Page(W169, "01_cover").lang("en").background(PAPER)
    p.image("hero", IMG + "dunes.jpg", par="xMidYMax slice")
    p.add(f'<rect x="80" y="50" width="430" height="34" fill="{LEMON}"/>' + bar(80, 586)
          + f'<rect x="6" y="6" width="1268" height="708" fill="none" stroke="{LEMON}" stroke-width="12"/>',
          after="photo-shade")
    kicker(p, "kicker", "THE FIELD JOURNAL  /  LANDSCAPE STUDY", 94, 72)
    p.text("title", ["Beyond", "the frame."], size=72, fill=WHITE, family=SERIF, weight="bold", lh=1.0, ls=-1.5, y=480)
    p.text("subtitle", "A field guide to light, landscape and attention.", size=22, fill=WHITE, family=SANS, y=622)
    kicker(p, "edition", "FIELD NOTES  /  AN EDITORIAL LAYOUT STUDY", 80, 678, WHITE)
    return p


def chapter():
    p = Page(W169, "02_chapter").lang("en").background(PAPER)
    p.image("hero", IMG + "lake.jpg")
    p.text("chapter-number", "02", x=80, y=176, size=132, fill=LEMON, family=SERIF, weight="bold")
    p.add(bar(80, 446), after="photo-shade")
    p.text("title", "Look closer. Ask better questions.", size=48, fill=WHITE, family=SERIF, weight="bold", ls=-1,
           y=540)
    p.text("description", "Every place has a story. Start by learning how to see it.", size=22, fill=WHITE,
           family=SANS, y=640)
    return p


def side_photo():
    p = Page(W169, "03h_content_side_photo").lang("en").background(PAPER)
    p.image("photo", IMG + "waterfall.jpg")
    p.add(bar(80, 92, 40), after="master-bg")
    kicker(p, "kicker", "04  /  NATURE, UP CLOSE", 80, 72, MUTED)
    p.text("title", ["Follow", "the water."], size=52, fill=INK, family=SERIF, weight="bold", lh=1.02, ls=-1, y=166)
    p.text("lead", ["A quiet detail can open a wider story."], size=20, fill=MUTED, family=SANS, y=308)
    p.text("main-copy", ["Water moves through the frame. A rock, a branch", "and a current create different points of entry.",
                         "Look before naming the scene.", "",
                         "Notice light and arrangement. Follow an edge or", "a reflection, and leave room for a closer view."],
           size=18, fill=INK, family=SANS, lh=1.5, y=392)
    kicker(p, "source", "PHOTO: WIKIMEDIA COMMONS, CC0", 80, 668, MUTED, weight=None)
    kicker(p, "folio", f"03 / {TOTAL:02d}", 608, 676, INK, anchor="end")
    return p


def gallery():
    p = Page(W169, "03i_content_gallery").lang("en").background(PAPER)
    p.image("photo-wide", IMG + "horizon.jpg").image("photo-mid", IMG + "autumn.jpg")
    p.image("photo-edge", IMG + "ocean.jpg")
    p.add(bar(80, 466, 40), after="photo-edge")
    p.text("title", "Many ways of seeing.", size=44, fill=INK, family=SERIF, weight="bold", ls=-1, y=522)
    p.text("lead", "Water, shorelines and horizons: three landscapes, three scales of attention.", size=20,
           fill=INK, family=SANS, y=586)
    kicker(p, "source", "PHOTOS: WIKIMEDIA COMMONS, CC0  ·  CROPPED FOR LAYOUT DEMONSTRATION", 80, 668, MUTED,
           weight=None)
    folio(p, 4)
    return p


def chronology():
    p = Page(W169, "03f_content_chronology").lang("en").background(PAPER)
    p.style("time-rule", stroke=INK).style("foot-rule", stroke=RULE)
    for i in range(1, 5):
        p.style(f"time-tick-{i}", stroke=INK)
    kicker(p, "kicker", "THE ROUTE  /  FOUR DAYS IN THE FIELD", 80, 72, MUTED)
    p.add("".join(bar(x, 312, 40) for x in (80, 368, 656, 944)), after="foot-rule")
    p.text("title", "Four days, four ways of looking.", size=44, fill=INK, family=SERIF, weight="bold", ls=-1, y=162)
    days = [("Day 1", ["The wider view.", "Arrive, walk the shoreline", "and sketch the whole place", "before any detail."]),
            ("Day 2", ["The small detail.", "One square metre of forest", "floor, recorded for an hour."]),
            ("Day 3", ["The shared question.", "Groups compare notes and", "choose one thing to explain."]),
            ("Day 4", ["The way home.", "Each student presents one", "photograph and one claim."])]
    for i, (d, ev) in enumerate(days):
        p.text(f"time-{i + 1}", d, size=32, fill=INK, family=SERIF, weight="bold", y=366)
        p.text(f"event-{i + 1}", ev, size=17, fill=INK, family=SANS, lh=1.5, y=420)
    kicker(p, "source", "ITINERARY IS ILLUSTRATIVE  ·  EQUAL SPACING IS ORDER, NOT DURATION", 80, 668, MUTED,
           weight=None)
    folio(p, 5)
    return p


def ending():
    p = Page(W169, "04_ending").lang("en").background(PAPER)
    p.image("hero", IMG + "autumn.jpg")
    p.style("closing-rule", stroke=RULE)
    p.add(bar(80, 412), after="closing-rule")
    p.text("title", "Take the questions with you.", size=52, fill=INK, family=SERIF, weight="bold", ls=-1, y=488)
    p.text("subtitle", "The journey continues in the way you see the world.", size=20, fill=MUTED, family=SANS,
           y=552)
    kicker(p, "contact", ["CC0 PHOTOGRAPHY", "WIKIMEDIA COMMONS"], 80, 610)
    kicker(p, "closing", ["SOURCES AND LICENCES", "LISTED IN EXAMPLES/PHOTOS.MD"], 656, 610, MUTED)
    folio(p, 6)
    return p


PAGES_169 = [cover, chapter, side_photo, gallery, chronology, ending]

if __name__ == "__main__":
    issues = []
    for build in PAGES_169:
        page = build()
        page.save(HERE / "examples" / page.layout / f"{page.prototype}.svg")
        issues += fit_report(page)
    print(f"wrote {len(PAGES_169)} pages to examples/{W169}")
    if "--check" in sys.argv:
        print("\n".join(issues) or "fit check: no issues")
