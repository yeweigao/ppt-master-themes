#!/usr/bin/env python3
"""Build the ppt169-editorial Layout prototypes (maintainer tool).

Writes workspace/templates/*.svg and the frontmatter placeholder map used by
design_spec.layout.ppt169-editorial.md. The geometry is the 16:9 translation of
a4-editorial: 80-unit outer margins, six 160-unit tracks with 32-unit gutters
(x = 80, 272, 464, 656, 848, 1040), a symmetric four-module division
(x = 80, 368, 656, 944, width 256), a kicker line at y = 72, a title band from
y = 104 and a running foot at y = 640-684. Colours, faces and sizes are neutral
preview values; identity and the final type scale come from the applied Style
and Brand. No prototype is a card wall, KPI tile row or dashboard module.

    python3 layouts/ppt169-editorial/build_prototypes.py
"""
from __future__ import annotations

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "workspace" / "templates"

INK, MUTED, RULE, DARK, WHITE, PALE, LIGHT = "#20262A", "#62696D", "#C8CCCF", "#18202C", "#FFFFFF", "#F1F2F3", "#DCE2EA"
PNG = ("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGO4cfsuAAUfApHcJOEkAAAAAElFTkSuQmCC")
COLS4 = (80, 368, 656, 944)


class Proto:
    def __init__(self, stem, key, name):
        self.stem, self.key, self.name = stem, key, name
        self.defs, self.layers, self.parts, self.idx, self.tokens = [], [], [], 0, []

    def layer(self, markup):
        """Layout-owned fixed element(s); each needs an id."""
        # Paint order: layout shapes always precede slide content and placeholders.
        self.layers.append(markup.replace("/>", ' data-pptx-layer="layout" data-pptx-editable="false"/>', 1)
                           if "data-pptx-layer" not in markup else markup)
        return self

    def deco(self, markup):
        self.parts.append(markup.replace("/>", ' data-pptx-role="decoration"/>', 1))
        return self

    def text(self, id_, kind, bounds, x, y, token, size=18, fill=INK, bold=False, ls=None, italic=False):
        self.idx += 1
        attrs = f'x="{x}" y="{y}" fill="{fill}"' + (f' font-size="{size}"' if size != 24 else "")
        if bold:
            attrs += ' font-weight="bold"'
        if ls:
            attrs += f' letter-spacing="{ls}"'
        if italic:
            attrs += ' font-style="italic"'
        self.parts.append(f'<g id="{id_}" data-pptx-placeholder="{kind}" data-pptx-idx="{self.idx}" '
                          f'data-pptx-bounds="{bounds}"><text data-pptx-carrier="true" {attrs}>{{{{{token}}}}}</text></g>')
        self.tokens.append("{{" + token + "}}")
        return self

    def picture(self, id_, x, y, w, h):
        self.idx += 1
        self.parts.append(f'<g id="{id_}" data-pptx-placeholder="picture" data-pptx-idx="{self.idx}" '
                          f'data-pptx-bounds="{x} {y} {w} {h}"><image data-pptx-carrier="true" x="{x}" y="{y}" '
                          f'width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice" href="{PNG}"/></g>')
        return self

    def proxy(self, id_, bounds, inner, token="CONTENT_AREA"):
        self.idx += 1
        self.parts.append(f'<g id="{id_}" data-pptx-placeholder="object" data-pptx-binding="proxy" '
                          f'data-pptx-idx="{self.idx}" data-pptx-bounds="{bounds}">{inner}</g>')
        self.tokens.append("{{" + token + "}}")
        return self

    # common furniture -------------------------------------------------------
    def kicker(self, fill=MUTED, bounds="80 48 1120 36", x=80, y=72):
        return self.text("kicker", "body", bounds, x, y, "SECTION_NAME", 14, fill, ls=2)

    def folio(self, fill=MUTED, bounds="1100 652 100 32", x=1100, y=676):
        return self.text("folio", "slide-number", bounds, x, y, "PAGE_NUM", 14, fill)

    def svg(self):
        defs = f"<defs>{''.join(self.defs)}</defs>\n  " if self.defs else ""
        body = "\n  ".join(self.layers + self.parts)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" font-family="Arial" font-size="24" '
                f'data-pptx-master="ppt169-editorial" data-pptx-master-name="16:9 Editorial" '
                f'data-pptx-layout="{self.key}" data-pptx-layout-name="{self.name}">\n  {defs}'
                f'<rect id="master-bg" data-pptx-layer="master" data-pptx-editable="false" width="1280" height="720" '
                f'fill="{WHITE}"/>\n  {body}\n</svg>\n')


def shade(id_, top=0.0, bottom=0.8):
    return (f'<linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000000" '
            f'stop-opacity="{top}"/><stop offset="1" stop-color="#000000" stop-opacity="{bottom}"/></linearGradient>')


def ticks(prefix, y, xs, h=12, w=2):
    return "".join(f'<line id="{prefix}-{i + 1}" x1="{x}" y1="{y}" x2="{x}" y2="{y + h}" stroke="{INK}" '
                   f'stroke-width="{w}" data-pptx-layer="layout" data-pptx-editable="false"/>' for i, x in enumerate(xs))


def build():
    P = []

    p = Proto("01_cover", "w-cover", "Full-bleed cover")
    p.defs.append(shade("cover-shade", 0, 0.78))
    p.picture("hero", 0, 0, 1280, 720)
    p.deco('<rect id="photo-shade" x="0" y="300" width="1280" height="420" fill="url(#cover-shade)"/>')
    p.kicker(WHITE, "80 48 800 36")
    p.text("title", "title", "80 410 960 170", 80, 490, "TITLE", 64, WHITE, bold=True)
    p.text("subtitle", "subtitle", "80 590 760 50", 80, 620, "SUBTITLE", 22, WHITE)
    p.text("edition", "date", "80 656 760 30", 80, 678, "DATE", 14, WHITE, ls=2)
    P.append(p)

    p = Proto("02_chapter", "w-chapter", "Photographic chapter")
    p.defs.append(shade("chapter-shade", 0.05, 0.8))
    p.picture("hero", 0, 0, 1280, 720)
    p.deco('<rect id="photo-shade" x="0" y="260" width="1280" height="460" fill="url(#chapter-shade)"/>')
    p.text("chapter-number", "body", "80 52 400 180", 80, 180, "CHAPTER_NUM", 140, WHITE)
    p.text("title", "title", "80 470 960 130", 80, 540, "CHAPTER_TITLE", 56, WHITE, bold=True)
    p.text("description", "body", "80 610 760 70", 80, 638, "CHAPTER_DESC", 22, WHITE)
    P.append(p)

    p = Proto("03a_content_statement", "w-statement", "Typographic statement and counterpoint")
    p.layer(f'<line id="top-rule" x1="80" y1="96" x2="1200" y2="96" stroke="{INK}" stroke-width="3"/>')
    p.layers.append(ticks("tick", 96, (80, 464, 848, 1200)))
    p.layer(f'<line id="short-rule" x1="656" y1="472" x2="1200" y2="472" stroke="{INK}" stroke-width="4"/>')
    p.kicker()
    p.text("title", "title", "80 124 1120 320", 80, 230, "PAGE_TITLE", 96, INK, bold=True, ls=-2)
    p.text("lead", "subtitle", "656 496 544 120", 656, 528, "SUBTITLE", 22, INK, bold=True)
    p.text("main-copy", "body", "80 496 544 136", 80, 522, "CONTENT_AREA", 18, MUTED)
    p.folio()
    P.append(p)

    p = Proto("03b_content_dual", "w-dual", "Two-column reading")
    p.layer(f'<line id="header-rule" x1="80" y1="96" x2="1200" y2="96" stroke="{RULE}" stroke-width="1"/>')
    p.layer(f'<line id="foot-rule" x1="80" y1="628" x2="1200" y2="628" stroke="{RULE}" stroke-width="1"/>')
    p.kicker()
    p.text("title", "title", "80 108 1120 110", 80, 166, "PAGE_TITLE", 44, INK, bold=True)
    p.text("lead", "subtitle", "80 226 1120 64", 80, 256, "SUBTITLE", 22, MUTED)
    p.text("body-left", "body", "80 306 544 306", 80, 332, "CONTENT_LEFT", 18, INK)
    p.text("body-right", "body", "656 306 544 306", 656, 332, "CONTENT_RIGHT", 18, INK)
    p.text("source", "body", "80 644 900 32", 80, 666, "SOURCE", 14, MUTED)
    p.folio()
    P.append(p)

    p = Proto("03c_content_evidence", "w-evidence", "Statement and annotated evidence")
    p.layer(f'<line id="exhibit-rule" x1="80" y1="290" x2="1200" y2="290" stroke="{INK}" stroke-width="2"/>')
    p.layer(f'<line id="foot-rule" x1="80" y1="628" x2="1200" y2="628" stroke="{RULE}" stroke-width="1"/>')
    p.kicker()
    p.text("title", "title", "80 104 1120 104", 80, 158, "PAGE_TITLE", 40, INK, bold=True)
    p.text("lead", "subtitle", "80 214 736 64", 80, 242, "SUBTITLE", 20, INK)
    p.text("context", "body", "848 214 352 64", 848, 238, "CONTEXT", 16, MUTED)
    p.proxy("exhibit", "80 306 736 306", f'<rect x="80" y="306" width="736" height="306" fill="{PALE}"/>'
            f'<text x="80" y="332" fill="{MUTED}">{{{{CONTENT_AREA}}}}</text>')
    p.text("annotation", "body", "848 306 352 306", 848, 332, "SIDEBAR", 18, INK)
    p.text("source", "body", "80 644 900 32", 80, 666, "SOURCE", 14, MUTED)
    p.folio()
    P.append(p)

    p = Proto("03d_content_comparison", "w-comparison", "Aligned qualitative comparison")
    p.layer(f'<line id="header-rule" x1="80" y1="292" x2="1200" y2="292" stroke="{INK}" stroke-width="3"/>')
    p.layer(f'<line id="row-rule-1" x1="80" y1="408" x2="1200" y2="408" stroke="{RULE}" stroke-width="1"/>')
    p.layer(f'<line id="row-rule-2" x1="80" y1="520" x2="1200" y2="520" stroke="{RULE}" stroke-width="1"/>')
    p.layer(f'<line id="row-rule-3" x1="80" y1="628" x2="1200" y2="628" stroke="{RULE}" stroke-width="1"/>')
    p.kicker()
    p.text("title", "title", "80 104 1120 104", 80, 158, "PAGE_TITLE", 40, INK, bold=True)
    p.text("label-left", "body", "80 230 544 50", 80, 266, "LABEL_LEFT", 26, INK)
    p.text("label-right", "body", "656 230 544 50", 656, 266, "LABEL_RIGHT", 26, INK)
    for i, y in enumerate((304, 420, 532)):
        p.text(f"left-{i + 1}", "body", f"80 {y} 544 90", 80, y + 26, f"LEFT_{i + 1}", 18, INK)
        p.text(f"right-{i + 1}", "body", f"656 {y} 544 90", 656, y + 26, f"RIGHT_{i + 1}", 18, INK)
    p.text("source", "body", "80 644 900 32", 80, 666, "SOURCE", 14, MUTED)
    p.folio()
    P.append(p)

    p = Proto("03e_content_table", "w-open-table", "Open table region")
    p.kicker()
    p.text("title", "title", "80 104 1120 104", 80, 158, "PAGE_TITLE", 40, INK, bold=True)
    p.text("lead", "subtitle", "80 214 1120 50", 80, 242, "SUBTITLE", 20, MUTED)
    rows = "".join(f'<line x1="80" y1="{y}" x2="1200" y2="{y}" stroke="{RULE}"/>' for y in (390, 460, 530))
    p.proxy("information", "80 280 1120 332",
            f'<line x1="80" y1="282" x2="1200" y2="282" stroke="#70777B" stroke-width="3"/>'
            f'<text x="80" y="314" font-size="18" fill="{INK}">{{{{CONTENT_AREA}}}}</text>'
            f'<line x1="80" y1="330" x2="1200" y2="330" stroke="#70777B" stroke-width="2"/>{rows}'
            f'<line x1="80" y1="610" x2="1200" y2="610" stroke="#70777B" stroke-width="2"/>')
    p.text("source", "body", "80 644 900 32", 80, 666, "SOURCE", 14, MUTED)
    p.folio()
    P.append(p)

    p = Proto("03f_content_chronology", "w-chronology", "Horizontal typographic chronology")
    p.layer(f'<line id="time-rule" x1="80" y1="300" x2="1200" y2="300" stroke="{INK}" stroke-width="3"/>')
    p.layers.append(ticks("time-tick", 292, COLS4, h=16, w=3))
    p.layer(f'<line id="foot-rule" x1="80" y1="628" x2="1200" y2="628" stroke="{RULE}" stroke-width="1"/>')
    p.kicker()
    p.text("title", "title", "80 104 1120 104", 80, 158, "PAGE_TITLE", 40, INK, bold=True)
    for i, x in enumerate(COLS4):
        p.text(f"time-{i + 1}", "body", f"{x} 320 256 60", x, 362, f"TIME_{i + 1}", 32, INK)
        p.text(f"event-{i + 1}", "body", f"{x} 392 256 220", x, 418, f"EVENT_{i + 1}", 18, INK)
    p.text("source", "body", "80 644 900 32", 80, 666, "SOURCE", 14, MUTED)
    p.folio()
    P.append(p)

    p = Proto("03g_content_marginalia", "w-marginalia", "Main text with anchored side notes")
    p.layer(f'<line id="header-rule" x1="80" y1="96" x2="1200" y2="96" stroke="{RULE}" stroke-width="1"/>')
    p.layer(f'<line id="margin-rule" x1="832" y1="230" x2="832" y2="612" stroke="{RULE}" stroke-width="1"/>')
    p.layer(f'<line id="quote-rule" x1="848" y1="470" x2="944" y2="470" stroke="{INK}" stroke-width="3"/>')
    p.kicker()
    p.text("title", "title", "80 108 1120 110", 80, 166, "PAGE_TITLE", 44, INK, bold=True)
    p.text("main-copy", "body", "80 230 736 382", 80, 256, "CONTENT_AREA", 18, INK)
    p.text("note-1", "body", "848 230 352 220", 848, 254, "NOTE_1", 16, MUTED)
    p.text("pull-quote", "body", "848 486 352 126", 848, 516, "KEY_MESSAGE", 22, INK, italic=True)
    p.text("source", "body", "80 644 900 32", 80, 666, "SOURCE", 14, MUTED)
    p.folio()
    P.append(p)

    p = Proto("03h_content_side_photo", "w-side-photo", "Reading column and edge photograph")
    p.picture("photo", 640, 0, 640, 720)
    p.kicker(MUTED, "80 48 528 36")
    p.text("title", "title", "80 104 528 160", 80, 160, "PAGE_TITLE", 40, INK, bold=True)
    p.text("lead", "subtitle", "80 280 528 70", 80, 306, "SUBTITLE", 20, MUTED)
    p.text("main-copy", "body", "80 366 528 240", 80, 392, "CONTENT_AREA", 18, INK)
    p.text("source", "body", "80 644 440 32", 80, 666, "SOURCE", 14, MUTED)
    p.folio(MUTED, "508 652 100 32", 508, 676)
    P.append(p)

    p = Proto("03i_content_gallery", "w-gallery", "Three-photo essay")
    p.picture("photo-wide", 0, 0, 624, 440)
    p.picture("photo-mid", 640, 0, 320, 440)
    p.picture("photo-edge", 976, 0, 304, 440)
    p.text("title", "title", "80 470 1120 70", 80, 520, "PAGE_TITLE", 36, INK, bold=True)
    p.text("lead", "subtitle", "80 556 1000 50", 80, 584, "SUBTITLE", 20, INK)
    p.text("source", "body", "80 644 900 32", 80, 666, "SOURCE", 14, MUTED)
    p.folio()
    P.append(p)

    p = Proto("03j_content_metrics", "w-metrics", "Hero figures on a specimen rule")
    p.layer(f'<line id="specimen-rule" x1="80" y1="300" x2="1200" y2="300" stroke="{INK}" stroke-width="2"/>')
    p.layers.append(ticks("specimen-tick", 300, COLS4 + (1200,), h=14))
    p.layer(f'<line id="foot-rule" x1="80" y1="628" x2="1200" y2="628" stroke="{RULE}" stroke-width="1"/>')
    p.kicker()
    p.text("title", "title", "80 104 1120 104", 80, 158, "PAGE_TITLE", 40, INK, bold=True)
    p.text("lead", "subtitle", "80 214 1120 60", 80, 242, "SUBTITLE", 20, MUTED)
    for i, x in enumerate(COLS4):
        p.text(f"metric-{i + 1}", "body", f"{x} 316 256 136", x, 416, f"METRIC_{i + 1}", 88, INK, bold=True)
        p.text(f"metric-label-{i + 1}", "body", f"{x} 456 256 150", x, 480, f"LABEL_{i + 1}", 16, MUTED)
    p.text("source", "body", "80 644 900 32", 80, 666, "SOURCE", 14, MUTED)
    p.folio()
    P.append(p)

    p = Proto("03k_content_overlay", "w-overlay", "Die-cut plate over a full-bleed photograph")
    p.picture("hero", 0, 0, 1280, 720)
    p.deco(f'<path id="plate" d="M 360 150 L 756 150 A 24 24 0 0 0 804 150 L 1200 150 L 1200 570 L 804 570 '
           f'A 24 24 0 0 0 756 570 L 360 570 Z" fill="{WHITE}" fill-opacity="0.92"/>')
    p.deco(f'<line id="plate-rule" x1="420" y1="330" x2="1140" y2="330" stroke="{INK}" stroke-opacity="0.22" '
           f'stroke-width="1.5"/>')
    p.kicker(WHITE)
    p.text("title", "title", "420 186 720 130", 420, 244, "PAGE_TITLE", 44, INK, bold=True)
    p.text("main-copy", "body", "420 346 720 200", 420, 374, "CONTENT_AREA", 18, INK)
    p.text("source", "body", "80 644 800 32", 80, 666, "SOURCE", 14, WHITE)
    p.folio(WHITE)
    P.append(p)

    p = Proto("03l_content_deconstruct", "w-deconstruct", "Modular check mask over a full-bleed photograph")
    p.picture("hero", 0, 0, 1280, 720)
    for i, (x, y, w, h) in enumerate([(400, 60, 400, 120), (40, 250, 300, 180), (600, 380, 360, 200)]):
        p.deco(f'<rect id="veil-{i + 1}" x="{x}" y="{y}" width="{w}" height="{h}" fill="{DARK}" fill-opacity="0.34"/>')
    for i, (x, y, w, h) in enumerate([(640, 120, 240, 140), (120, 440, 320, 140), (700, 400, 200, 160)]):
        p.deco(f'<rect id="glass-{i + 1}" x="{x}" y="{y}" width="{w}" height="{h}" fill="{DARK}" fill-opacity="0.58"/>')
    for i, (x, y, w, h) in enumerate([(0, 0, 176, 140), (176, 140, 480, 160), (880, 0, 400, 380),
                                      (560, 560, 720, 160), (0, 600, 176, 120), (0, 300, 120, 140)]):
        p.deco(f'<rect id="cell-{i + 1}" x="{x}" y="{y}" width="{w}" height="{h}" fill="{DARK}"/>')
    p.deco(f'<path id="arrow-ne" d="M 1180 344 L 1210 314 M 1186 314 L 1210 314 L 1210 338" fill="none" '
           f'stroke="{WHITE}" stroke-width="2.5"/>')
    p.text("kicker", "body", "24 40 140 80", 24, 64, "SECTION_NAME", 14, WHITE, bold=True, ls=1)
    p.text("title", "title", "200 164 440 112", 200, 204, "PAGE_TITLE", 30, WHITE, bold=True)
    p.text("main-copy", "body", "904 40 272 300", 904, 70, "CONTENT_AREA", 16, LIGHT)
    p.text("source", "body", "584 584 520 80", 584, 614, "SOURCE", 18, WHITE)
    p.folio(LIGHT)
    P.append(p)

    p = Proto("03m_content_pillars", "w-pillars", "Inverted field with staggered pillars")
    p.layer(f'<rect id="field" width="1280" height="720" fill="{DARK}"/>')
    for i, (x, y, w, h) in enumerate([(300, 380, 120, 160), (560, 150, 140, 140), (850, 420, 130, 150)]):
        p.layer(f'<rect id="pillar-echo-{i + 1}" x="{x}" y="{y}" width="{w}" height="{h}" fill="{WHITE}" '
                f'fill-opacity="0.12"/>')
    for i, (x, y, h) in enumerate([(80, 430, 290), (368, 200, 400), (656, 480, 240), (944, 110, 360)]):
        p.layer(f'<rect id="pillar-{i + 1}" x="{x}" y="{y}" width="256" height="{h}" fill="{WHITE}" '
                f'fill-opacity="0.96"/>')
    p.kicker(WHITE, "80 48 600 36")
    p.text("lead", "subtitle", "80 100 260 140", 80, 126, "SUBTITLE", 18, LIGHT)
    for i, (x, y) in enumerate([(80, 430), (368, 200), (656, 480), (944, 110)]):
        p.text(f"step-{i + 1}", "body", f"{x + 20} {y + 20} 216 110", x + 20, y + 46, f"STEP_{i + 1}", 16, DARK,
               bold=True)
    p.text("body-left", "body", "368 616 256 70", 368, 640, "CONTENT_LEFT", 16, WHITE)
    p.text("body-right", "body", "944 490 256 140", 944, 514, "CONTENT_RIGHT", 16, LIGHT)
    p.folio(LIGHT)
    P.append(p)

    p = Proto("03n_content_quote", "w-quote", "Photograph and pull quote")
    p.picture("photo", 0, 0, 560, 720)
    p.layer(f'<line id="quote-rule" x1="640" y1="132" x2="720" y2="132" stroke="{INK}" stroke-width="4"/>')
    p.kicker(MUTED, "640 48 560 36", 640, 72)
    p.text("quote", "body", "640 160 560 320", 640, 230, "KEY_MESSAGE", 40, INK, italic=True)
    p.text("attribution", "body", "640 500 560 64", 640, 530, "CONTENT_AREA", 16, MUTED, ls=1)
    p.text("source", "body", "640 644 440 32", 640, 666, "SOURCE", 14, MUTED)
    p.folio()
    P.append(p)

    p = Proto("04_ending", "w-ending", "Photographic close")
    p.picture("hero", 0, 0, 1280, 400)
    p.layer(f'<line id="closing-rule" x1="80" y1="570" x2="1200" y2="570" stroke="{RULE}" stroke-width="1"/>')
    p.text("title", "title", "80 424 1000 100", 80, 484, "THANK_YOU", 48, INK, bold=True)
    p.text("subtitle", "subtitle", "80 524 1000 40", 80, 552, "ENDING_SUBTITLE", 20, MUTED)
    p.text("contact", "body", "80 584 544 92", 80, 608, "CONTACT_INFO", 16, INK)
    p.text("closing", "body", "656 584 420 92", 656, 608, "CLOSING_MESSAGE", 16, INK)
    p.folio()
    P.append(p)
    return P


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    protos = build()
    for p in protos:
        (OUT / f"{p.stem}.svg").write_text(p.svg(), encoding="utf-8")
    print(f"wrote {len(protos)} prototypes to {OUT}")
    print("placeholders:")
    for p in protos:
        print(f'  {p.stem}: [{", ".join(chr(34) + t + chr(34) for t in p.tokens)}]')
