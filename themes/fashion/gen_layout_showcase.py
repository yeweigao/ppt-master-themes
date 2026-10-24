#!/usr/bin/env python3
"""Fashion Editorial on the shared a4-editorial Layout.

Writes examples/a4-editorial/<prototype>.svg. Each page is the Layout prototype
restyled with the Fashion Theme DNA: paper / ink / cobalt-as-interruption,
Didone + ultra-condensed capitals against a neutral grotesque, black-and-white
images that change state, and the four temperatures (bleed, paper, ink, cobalt).
MAISON 170 is a fictional house; copy is demonstration text.

    python3 themes/fashion/gen_layout_showcase.py [--check]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "framework" / "scripts"))
from layout_showcase import Page, fit_report, text_markup  # noqa: E402

IMG = "../images/"
TOTAL = 8

PAPER, INK, COBALT, GREY, RULE = "#F6F4EF", "#0A0A0A", "#1710CC", "#77736B", "#D9D5CB"
WHITE = "#FFFFFF"
DIDONE = "'Bodoni Moda', Didot, 'Times New Roman', serif"
CAPS = "'Six Caps', 'Oswald', 'Arial Narrow', sans-serif"
SANS = "Archivo, Arial, sans-serif"


def micro(p, id_, lines, x, y, fill=INK, anchor=None, weight="bold", lh=1.6):
    """Tracked uppercase microtext: the evidence voice (15 px, never smaller)."""
    p.text(id_, lines, x=x, y=y, size=15, fill=fill, family=SANS, weight=weight, ls=3.4, anchor=anchor, lh=lh)


def micro_deco(text, x, y, fill=WHITE, anchor=None):
    return text_markup(text, x=x, y=y, size=15, fill=fill, family=SANS, weight="bold", ls=3.4, anchor=anchor)


def folio(p, n, fill=INK):
    micro(p, "folio", f"{n:02d} / {TOTAL:02d}", 1140, 1668, fill, anchor="end")


def specimen(y, fill, opacity=1.0):
    ticks = "".join(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y + 14}" stroke="{fill}" stroke-opacity="{opacity}" '
                    f'stroke-width="1.5"/>' for x in (100, 370, 640, 910, 1140))
    return f'<line x1="100" y1="{y}" x2="1140" y2="{y}" stroke="{fill}" stroke-opacity="{opacity}" stroke-width="1"/>' + ticks


def cover():
    p = Page("a4-editorial", "01_cover").lang("en-GB").background(PAPER).ground(INK)
    p.image("hero", IMG + "_cover.jpg", par="xMidYMin slice")
    p.add(specimen(172, WHITE, 0.7), after="photo-shade")
    p.add(f'<rect x="820" y="880" width="320" height="460" fill="{COBALT}" fill-opacity="0.62"/>', after="photo-shade")
    p.add(text_markup(["A GLOBAL", "CAST"], x=1112, y=1040, size=150, fill=WHITE, family=CAPS, lh=0.95, anchor="end"), after="photo-shade")
    p.add(micro_deco("INTERLOCK / ALPHA 62%", 848, 1308), after="photo-shade")
    micro(p, "kicker", "MAISON 170  —  VOLUME TWO", 100, 132, WHITE)
    p.text("title", ["The House", "of Presence"], size=124, fill=WHITE, family=DIDONE, lh=1.02, ls=-2,
           x=100, y=1238)
    p.text("subtitle", ["Ten portraits, four cities", "and one attitude."], size=30, fill=WHITE, family=SANS,
           lh=1.45, y=1478)
    micro(p, "edition", "AUTUMN / WINTER 2026   ·   ISSUE 02", 100, 1662, WHITE)
    return p


def chapter():
    p = Page("a4-editorial", "02_chapter").lang("en-GB").background(PAPER).ground(INK)
    p.image("hero", IMG + "_coat.jpg", par="xMidYMid slice")
    p.add(f'<rect x="100" y="96" width="250" height="230" fill="{COBALT}" fill-opacity="0.72"/>', after="photo-shade")
    p.add(micro_deco("CHAPTER", 124, 132), after="photo-shade")
    p.text("chapter-number", "02", x=118, y=245, size=170, fill=WHITE, family=CAPS)
    p.text("title", "Tailoring", size=124, fill=WHITE, family=DIDONE, ls=-2, y=1330)
    p.text("description", ["A shoulder is a line drawn in cloth.", "The rest is posture."], size=30,
           fill=WHITE, family=SANS, lh=1.45, y=1520)
    return p


def typographic():
    p = Page("a4-editorial", "03u_content_typographic").lang("en-GB").background(PAPER)
    for i in ("top-rule", "tick-1", "tick-2", "tick-3", "tick-4", "bottom-rule"):
        p.style(i, stroke=INK)
    p.style("mid-rule", stroke=RULE).style("short-rule", stroke=COBALT)
    p.add(f'<rect x="740" y="400" width="400" height="330" fill="{COBALT}" fill-opacity="0.62"/>', after="short-rule")
    p.add(text_markup("NO. 03", x=1112, y=700, size=110, fill=WHITE, family=CAPS, anchor="end"), after="short-rule")
    micro(p, "kicker", "MAISON 170  /  METHOD", 100, 126, GREY)
    p.text("title", ["Edit,", "then", "frame."], size=160, fill=INK, family=DIDONE, lh=0.98, ls=-3, y=390)
    p.text("lead", ["Three rules for photographing a collection", "without letting the clothes",
                    "outshout the people."], size=30, fill=INK, family=SANS, lh=1.4, y=922)
    p.text("takeaway", ["The camera does not", "invent presence. It", "waits for it, then edits."],
           size=38, fill=INK, family=DIDONE, italic=True, lh=1.3, y=1214)
    p.text("main-copy", ["We shoot every look twice: once for the",
                         "garment, once for the person. Only the",
                         "second survives the edit.",
                         "",
                         "Colour is removed first, so that cut,",
                         "texture and posture have to carry the",
                         "picture on their own. Cobalt returns",
                         "later, as an interruption, never a filter."],
           size=21, fill=INK, family=SANS, lh=1.5, y=1190)
    folio(p, 3)
    return p


def atelier():
    p = Page("a4-editorial", "03y_content_atelier").lang("en-GB").background(PAPER)
    p.style("sliced-monolith-bars", fill=INK)
    p.style("counter-form-glaze", fill=COBALT, fill_opacity="0.34")
    p.style("counter-form-accent", fill=COBALT, fill_opacity="0.86")
    p.style("counter-form-cutout", fill=PAPER, fill_opacity="0.96")
    p.style("slice-seam-1", fill=PAPER, fill_opacity="0.94").style("slice-seam-2", fill=PAPER, fill_opacity="0.94")
    p.style("horizon-rule", stroke=RULE)
    p.style("photo-interlock-pane", fill=COBALT, fill_opacity="0.32").style("photo-frame", stroke=INK)
    p.image("photo", IMG + "_profile.jpg", par="xMidYMid slice")
    micro(p, "kicker", ["ATELIER", "04"], 100, 128)
    micro(p, "index-nav", ["I.   THE CUT", "II.  THE CLOTH", "III. THE CAST"], 880, 124, GREY, lh=1.7)
    p.text("title", ["Every silhouette", "begins as a decision", "about what to leave out."],
           size=58, fill=INK, family=DIDONE, lh=1.14, y=244)
    micro(p, "source", ["STUDIO, LONDON  ·  06:40", "PHOTOGRAPHY / UNSPLASH LICENSE"], 460, 690, GREY)
    p.text("display-figure", "THE  CUT", x=616, y=1013, size=70, fill=INK, family=CAPS, ls=10)
    micro(p, "main-copy", "LOOK 07  ·  WOOL, BONE, NOTHING ELSE", 616, 1464)
    folio(p, 4)
    return p


def matrix():
    p = Page("a4-editorial", "03v_content_matrix").lang("en-GB").background(PAPER)
    for i in ("specimen-rule", "specimen-tick-1", "specimen-tick-2", "specimen-tick-3", "specimen-tick-4",
              "specimen-tick-5"):
        p.style(i, stroke=INK)
    p.style("card-primary", fill=INK).style("card-secondary", fill=COBALT)
    p.style("card-watermark", stroke_opacity="0.22").style("footer-rule", stroke=RULE)
    p.style("interlock-tab-1", fill=COBALT, fill_opacity="0.62").style("interlock-tab-2", fill=COBALT, fill_opacity="0.32")
    p.style("photo-1-border", stroke=INK).style("photo-2-border", stroke=INK)
    p.image("photo-1", IMG + "_cast_shirt.jpg").image("photo-2", IMG + "_cast_updo.jpg")
    p.add(text_markup("01", x=394, y=1318, size=110, fill=WHITE, family=CAPS), after="stripe-5")
    p.add(text_markup("02", x=934, y=1318, size=110, fill=WHITE, family=CAPS), after="card-watermark-inner")
    micro(p, "kicker", "MAISON 170  /  SIGNATURES  /  FOUR SILHOUETTES", 100, 124, GREY)
    p.text("title", "Signatures", size=168, fill=INK, family=DIDONE, ls=-4, y=364)
    p.text("card-copy-1", ["STRIPE", "", "A line repeated", "until it becomes", "a portrait. Worn", "loose, never",
                           "pressed."], size=19, fill=WHITE, family=SANS, lh=1.5, y=574)
    p.text("card-copy-2", ["DENIM", "", "The jacket we", "kept from the", "archive and", "refused to", "restyle."],
           size=19, fill=WHITE, family=SANS, lh=1.5, y=574)
    p.text("takeaway", "Silhouettes are arguments made in cloth.", size=31, fill=INK, family=DIDONE, y=1494)
    micro(p, "source", ["PHOTOGRAPHY", "UNSPLASH LICENSE"], 1140, 1478, GREY, anchor="end")
    folio(p, 5)
    return p


def overlay():
    p = Page("a4-editorial", "03p_content_overlay").lang("en-GB").background(PAPER).ground(INK)
    p.image("hero", IMG + "_street.jpg", par="xMidYMin slice")
    p.style("overlay-glaze-upper", fill=COBALT, fill_opacity="0.32")
    p.style("overlay-glaze-lower", fill=COBALT, fill_opacity="0.72", y="1300", height="200")
    p.style("headline-ground", fill=PAPER, fill_opacity="0.95")
    p.style("plate-rule", stroke=INK, stroke_opacity="0.2")
    p.add(micro_deco("INTERLOCK / 02", 772, 1342), after="plate-rule")
    p.add(text_markup(["THE STREET", "IS THE STUDIO"], x=772, y=1412, size=52, fill=WHITE, family=CAPS, ls=1, lh=0.95),
          after="plate-rule")
    micro(p, "kicker", "MAISON 170  /  THE STREET CAST", 100, 122, INK)
    p.text("title", ["The city styles it", "faster than we do."], size=78, fill=INK, family=DIDONE, lh=1.08, ls=-1,
           y=740)
    p.text("main-copy", ["We stopped building sets. A car park at dawn, a court",
                         "with no net, a coat borrowed from the person wearing it:",
                         "the street supplies the context and the cast supplies",
                         "the attitude. Our job is to keep both in frame."],
           size=24, fill=INK, family=SANS, lh=1.55, y=990)
    micro(p, "source", "LOS ANGELES  ·  07:15   /   PHOTOGRAPHY: UNSPLASH LICENSE", 100, 1622, PAPER)
    folio(p, 6, PAPER)
    return p


def deconstruct():
    p = Page("a4-editorial", "03x_content_deconstruct").lang("en-GB").background(PAPER).ground(INK)
    p.image("hero", IMG + "_cast_bw.jpg", par="xMidYMin slice")
    for i in ("veil-upper-bridge", "veil-mid-left", "veil-lower-wave"):
        p.style(i, fill=COBALT, fill_opacity="0.34")
    for i in ("glass-upper", "glass-lower-left", "glass-lower-mid", "glass-corner-echo"):
        p.style(i, fill=COBALT, fill_opacity="0.58")
    for i in ("cell-top-left", "cell-headline", "cell-badge", "cell-top-right", "cell-mid-right",
              "cell-bottom-right", "cell-bottom-left", "cell-step-left", "cell-step-low"):
        p.style(i, fill=INK)
    p.add(text_markup("170", x=300, y=632, size=120, fill=WHITE, family=CAPS, anchor="middle"), after="cell-step-low")
    micro(p, "kicker", ["CAST", "07"], 36, 92, WHITE)
    p.text("brand-label", "MAISON 170", x=820, y=128, size=28, fill=WHITE, family=SANS, weight="bold", ls=5)
    p.text("title", ["A face is not", "a mood board."], size=46, fill=WHITE, family=DIDONE, lh=1.15, y=320)
    p.text("main-copy", ["Seventy faces were cast in",
                         "four cities. None was chosen",
                         "to match a reference. Each",
                         "was chosen because the",
                         "clothes looked different on",
                         "them than on anyone else.",
                         "",
                         "The grid crops; it does not",
                         "hide. The eyes stay clear."],
           size=21, fill="#E8E6F7", family=SANS, lh=1.5, y=566)
    p.text("source", ["“We cast people,", "then let the clothes", "catch up.”"], size=34, fill=WHITE,
           family=DIDONE, italic=True, lh=1.25, y=1466)
    folio(p, 7, WHITE)
    return p


def ending():
    p = Page("a4-editorial", "04_ending").lang("en-GB").background(PAPER)
    p.image("hero", IMG + "_cast_neutral.jpg", par="xMidYMin slice")
    p.style("closing-rule", stroke=RULE)
    p.add(f'<rect x="900" y="780" width="240" height="250" fill="{COBALT}" fill-opacity="0.86"/>', after="hero")
    p.add(text_markup("FIN", x=926, y=990, size=170, fill=WHITE, family=CAPS), after="hero")
    p.text("title", ["Presence is", "the collection."], size=92, fill=INK, family=DIDONE, lh=1.04, ls=-2,
           y=1082)
    p.text("subtitle", "Volume two of a global cast. Volume three begins in Lagos.", size=26, fill=GREY,
           family=SANS, y=1300)
    micro(p, "contact", ["MAISON 170", "STUDIO@MAISON170.EXAMPLE", "LONDON  ·  MILAN  ·  LOS ANGELES"], 100, 1492,
          lh=1.75)
    micro(p, "closing", ["MAISON 170 IS A FICTIONAL HOUSE.", "PHOTOGRAPHY: UNSPLASH LICENSE.",
                         "COPY IS DEMONSTRATION TEXT."], 640, 1492, GREY, weight=None, lh=1.75)
    folio(p, 8)
    return p


PAGES = [cover, chapter, typographic, atelier, matrix, overlay, deconstruct, ending]

# --- 16:9 (ppt169-editorial) ---------------------------------------------------
W169 = "ppt169-editorial"
TOTAL_169 = 6


def micro169(p, id_, lines, x, y, fill=INK, anchor=None, weight="bold", lh=1.6):
    p.text(id_, lines, x=x, y=y, size=14, fill=fill, family=SANS, weight=weight, ls=3, anchor=anchor, lh=lh)


def folio169(p, n, fill=INK):
    micro169(p, "folio", f"{n:02d} / {TOTAL_169:02d}", 1200, 676, fill, anchor="end")


def cover_169():
    p = Page(W169, "01_cover").lang("en-GB").background(PAPER).ground(INK)
    p.image("hero", IMG + "_cover.jpg")
    p.add(f'<rect x="944" y="96" width="256" height="300" fill="{COBALT}" fill-opacity="0.62"/>'
          + text_markup(["A GLOBAL", "CAST"], x=1176, y=226, size=110, fill=WHITE, family=CAPS, lh=0.95, anchor="end")
          + text_markup("INTERLOCK / 62%", x=968, y=372, size=14, fill=WHITE, family=SANS, weight="bold", ls=3),
          after="photo-shade")
    micro169(p, "kicker", "MAISON 170  —  VOLUME TWO", 80, 72, WHITE)
    p.text("title", ["The House", "of Presence"], size=68, fill=WHITE, family=DIDONE, lh=1.0, ls=-1, y=480)
    p.text("subtitle", "Ten portraits, four cities and one attitude.", size=22, fill=WHITE, family=SANS, y=620)
    micro169(p, "edition", "AUTUMN / WINTER 2026  ·  ISSUE 02", 80, 678, WHITE)
    return p


def statement_169():
    p = Page(W169, "03a_content_statement").lang("en-GB").background(PAPER)
    for i in ("top-rule", "tick-1", "tick-2", "tick-3", "tick-4"):
        p.style(i, stroke=INK)
    p.style("short-rule", stroke=COBALT)
    p.add(f'<rect x="880" y="150" width="320" height="250" fill="{COBALT}" fill-opacity="0.62"/>'
          + text_markup("NO. 03", x=1176, y=376, size=96, fill=WHITE, family=CAPS, anchor="end"), after="short-rule")
    micro169(p, "kicker", "MAISON 170  /  METHOD", 80, 72, GREY)
    p.text("title", ["Edit,", "then frame."], size=112, fill=INK, family=DIDONE, lh=0.98, ls=-3, y=236)
    p.text("lead", ["Photograph the collection without", "letting the clothes outshout", "the people."], size=22,
           fill=INK, family=SANS, weight="bold", lh=1.35, y=530)
    p.text("main-copy", ["We shoot every look twice: once for the", "garment, once for the person. Only the",
                         "second survives the edit. Colour returns", "later, as an interruption."],
           size=18, fill=INK, family=SANS, lh=1.45, y=522)
    folio169(p, 2)
    return p


def deconstruct_169():
    p = Page(W169, "03l_content_deconstruct").lang("en-GB").background(PAPER).ground(INK)
    p.image("hero", IMG + "_cast_dark.jpg", par="xMidYMin slice")
    for i in (1, 2, 3):
        p.style(f"veil-{i}", fill=COBALT, fill_opacity="0.34").style(f"glass-{i}", fill=COBALT, fill_opacity="0.58")
    for i in range(1, 7):
        p.style(f"cell-{i}", fill=INK)
    micro169(p, "kicker", ["CAST", "07"], 24, 66, WHITE)
    p.text("title", ["A face is not", "a mood board."], size=34, fill=WHITE, family=DIDONE, lh=1.15, y=210)
    p.text("main-copy", ["Seventy faces were cast", "in four cities. None was", "chosen to match a", "reference: each because",
                         "the clothes looked", "different on them.", "", "The grid crops; it does", "not hide the eyes."],
           size=16, fill="#E8E6F7", family=SANS, lh=1.45, y=72)
    p.text("source", ["“We cast people, then let", "the clothes catch up.”"], size=26, fill=WHITE, family=DIDONE,
           italic=True, lh=1.2, y=622)
    folio169(p, 3, WHITE)
    return p


def quote_169():
    p = Page(W169, "03n_content_quote").lang("en-GB").background(PAPER)
    p.image("photo", IMG + "_profile.jpg")
    p.style("quote-rule", stroke=COBALT)
    micro169(p, "kicker", "MAISON 170  /  ATELIER", 640, 72, GREY)
    p.text("quote", ["Every silhouette begins", "as a decision about", "what to leave out."], size=44, fill=INK,
           family=DIDONE, italic=True, lh=1.2, y=236)
    micro169(p, "attribution", ["THE ATELIER, LONDON", "LOOK 07  ·  WOOL, BONE, NOTHING ELSE"], 640, 532, GREY)
    micro169(p, "source", "PHOTOGRAPHY: UNSPLASH LICENSE", 640, 668, GREY, weight=None)
    folio169(p, 4)
    return p


def gallery_169():
    p = Page(W169, "03i_content_gallery").lang("en-GB").background(PAPER)
    p.image("photo-wide", IMG + "_cast_man.jpg", par="xMidYMin slice").image("photo-mid", IMG + "_cast_shirt.jpg")
    p.image("photo-edge", IMG + "_cast_neutral.jpg")
    p.add(f'<rect x="560" y="360" width="160" height="110" fill="{COBALT}" fill-opacity="0.62"/>'
          + text_markup("03 / 70", x=696, y=448, size=56, fill=WHITE, family=CAPS, anchor="end"), after="photo-edge")
    p.text("title", "Seventy faces, four cities.", size=44, fill=INK, family=DIDONE, ls=-1, y=522)
    p.text("lead", "Three of the cast, photographed without hierarchy.", size=20, fill=INK, family=SANS, y=586)
    micro169(p, "source", "PHOTOGRAPHY: UNSPLASH LICENSE", 80, 668, GREY, weight=None)
    folio169(p, 5)
    return p


def ending_169():
    p = Page(W169, "04_ending").lang("en-GB").background(PAPER)
    p.image("hero", IMG + "_coat.jpg", par="xMidYMin slice")
    p.style("closing-rule", stroke=RULE)
    p.add(f'<rect x="1000" y="300" width="200" height="190" fill="{COBALT}" fill-opacity="0.86"/>'
          + text_markup("FIN", x=1176, y=468, size=140, fill=WHITE, family=CAPS, anchor="end"), after="hero")
    p.text("title", "Presence is the collection.", size=52, fill=INK, family=DIDONE, ls=-1, y=488)
    p.text("subtitle", "Volume two of a global cast. Volume three begins in Lagos.", size=20, fill=GREY,
           family=SANS, y=552)
    micro169(p, "contact", ["MAISON 170", "STUDIO@MAISON170.EXAMPLE"], 80, 610)
    micro169(p, "closing", ["MAISON 170 IS A FICTIONAL HOUSE.", "PHOTOGRAPHY: UNSPLASH LICENSE."], 656, 610, GREY,
             weight=None)
    folio169(p, 6)
    return p


PAGES_169 = [cover_169, statement_169, deconstruct_169, quote_169, gallery_169, ending_169]


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
