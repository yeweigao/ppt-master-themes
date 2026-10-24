#!/usr/bin/env python3
"""Generate the Boardroom Strategy Review example suite (A4, 1240x1754).

Calibrated for physical A4 print (210 x 297 mm = 595.28 x 841.89 pt on the
1240 x 1754 authoring canvas, where 1 SVG unit = 0.48 pt) and Swiss
International Style typographic hierarchy:
- Display / Cover Hero: 116-128 px Georgia Bold (55.7-61.4 pt)
- Action Title: 54-58 px Georgia Bold (25.9-27.8 pt)
- Big Evidence Number: 54-76 px Georgia Bold (25.9-36.5 pt)
- Decision Statement / Pull Quote: 32-40 px Georgia Bold / Italic (15.4-19.2 pt)
- Lead Deck: 28 px Georgia Regular (13.4 pt — distinct step above body)
- Module / Finding Heading: 28-30 px Arial Bold (13.4-14.4 pt)
- Sustained Two-Column Essay Body: 23 px Georgia Regular / 35 leading (11.0 pt)
- Module / Card / Rail Body: 19-21 px Georgia Regular / 28-30 leading (9.1-10.1 pt)
- Table Cell / Issue-Tree Node: 18-22 px Arial Bold/Regular (8.6-10.6 pt)
- Kicker / Running Head / Direct Chart & Bubble Label: 15-18 px Arial Bold (7.2-8.6 pt)
- Axis Tick / Owner / Date / Footer Floor: 14-15 px Arial (6.7-7.2 pt; never < 13-14 px)
"""
from pathlib import Path
from html import escape
import os

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "examples" / "svg"
OUT.mkdir(parents=True, exist_ok=True)

NAVY = "#071C2C"
NAVY2 = "#0D2C42"
CYAN = "#00A9F4"
RED = "#E3120B"
PAPER = "#F7F5F0"
WHITE = "#FFFFFF"
INK = "#12232F"
MUTED = "#5F6E79"
RULE = "#D5DCE1"
PALE = "#E9EEF1"
SAND = "#C9B99A"
STEEL = "#8FA3B0"

W, H = 1240, 1754


def esc(value):
    return escape(str(value), quote=False)


def est_width(value, size, family="Arial", weight="normal", ls=0):
    """Calibrated width estimate for Georgia and Arial at A4 authoring scale."""
    factor = 0.50 if family.startswith("Georgia") else 0.52
    if weight == "bold":
        factor = 0.58
    caps = sum(1 for ch in value if ch.isupper())
    if value and caps / len(value) > 0.6:
        factor += 0.06
    return len(value) * (factor * size + float(ls or 0))


def wrap(value, width, size, family="Arial", weight="normal", ls=0):
    limit = width * 0.94
    lines, current = [], ""
    for word in value.split():
        trial = word if not current else f"{current} {word}"
        if est_width(trial, size, family, weight, ls) <= limit or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text(x, y, content, size, fill, family="Arial", weight="normal",
         leading=None, ls=None, italic=False, opacity=None, anchor=None,
         carrier=False):
    attrs = [f'x="{x}"', f'y="{y}"', f'fill="{fill}"', f'font-size="{size}"']
    if family != "Arial":
        attrs.append(f'font-family="{family}"')
    if weight != "normal":
        attrs.append(f'font-weight="{weight}"')
    if ls is not None:
        attrs.append(f'letter-spacing="{ls}"')
    if italic:
        attrs.append('font-style="italic"')
    if opacity is not None:
        attrs.append(f'fill-opacity="{opacity}"')
    if anchor:
        attrs.append(f'text-anchor="{anchor}"')
    if carrier:
        attrs.append('data-pptx-carrier="true"')
    lines = content if isinstance(content, (list, tuple)) else [content]
    body = esc(lines[0])
    if len(lines) > 1:
        dy = leading if leading is not None else round(size * 1.3, 2)
        body += "".join(f'<tspan x="{x}" dy="{dy}">{esc(line)}</tspan>' for line in lines[1:])
    return f'<text {" ".join(attrs)}>{body}</text>'


class Page:
    def __init__(self, key, name, master="a4-boardroom", master_name="A4 Boardroom"):
        self.key = key
        self.i = 0
        self.d = 0
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" lang="en" viewBox="0 0 1240 1754" '
            f'font-family="Arial" font-size="24" data-pptx-master="{master}" '
            f'data-pptx-master-name="{master_name}" data-pptx-layout="{key}" '
            f'data-pptx-layout-name="{name}">',
            f'  <rect id="master-bg" data-pptx-layer="master" data-pptx-editable="false" '
            f'width="1240" height="1754" fill="{PAPER}"/>',
        ]

    def take(self):
        self.i += 1
        return self.i

    def did(self):
        self.d += 1
        return f"{self.key}-d{self.d}"

    def add(self, *items):
        self.parts.extend(items)
        return self

    def ph(self, x, top, width, height, content, size, fill, family="Arial",
           weight="normal", leading=None, ls=None, italic=False, ph_type="body",
           anchor=None, baseline=None, opacity=None, bx=None):
        idx = self.take()
        lead = leading if leading is not None else round(size * 1.3, 2)
        base = baseline if baseline is not None else round(top + size * 0.88, 2)
        body = text(x, base, content, size, fill, family, weight, lead, ls,
                    italic, opacity, anchor, carrier=True)
        pid = f"{self.key}-p{idx}"
        if bx is None:
            if anchor == "middle":
                bx = x - width / 2
            elif anchor == "end":
                bx = x - width
            else:
                bx = x
        line_count = len(content) if isinstance(content, (list, tuple)) else 1
        needed = (base - top) + (line_count - 1) * lead + size * 0.55 + 8
        height = max(height, needed)
        self.parts.append(
            f'<g id="{pid}" data-pptx-placeholder="{ph_type}" data-pptx-idx="{idx}" '
            f'data-pptx-bounds="{bx} {top} {width} {height}">{body}</g>')
        return self

    def ph_right(self, right, top, width, height, content, size, fill, **kw):
        return self.ph(right, top, width, height, content, size, fill,
                       anchor="end", bx=right - width, **kw)

    def para(self, x, top, width, height, content, size, fill, family="Arial",
             weight="normal", leading=None, ls=None, italic=False, ph_type="body"):
        lead = leading if leading is not None else round(size * 1.38, 2)
        paragraphs = [content] if isinstance(content, str) else list(content)
        lines = []
        for n, paragraph in enumerate(paragraphs):
            if n:
                lines.append("\u00A0")
            lines.extend(wrap(paragraph, width, size, family, weight, ls or 0))
        height = max(height, (len(lines) - 1) * lead + size * 1.4 + 12)
        return self.ph(x, top, width, height, lines, size, fill, family, weight,
                       lead, ls, italic, ph_type)

    def tick(self, x, baseline, content, size=14, fill=MUTED, family="Arial",
             weight="normal", ls=None, anchor=None):
        width = est_width(content, size, family, weight, ls or 0) * 1.45 + 36
        if anchor == "middle":
            left = x - width / 2
        elif anchor == "end":
            left = x - width
        else:
            left = x - 4
        top = baseline - size
        return self.ph(x, top, width, round(size * 1.7, 1), content, size, fill,
                       family, weight, baseline=baseline, ls=ls, anchor=anchor,
                       bx=left)

    def rect(self, x, y, width, height, fill, opacity=None, role="decoration"):
        op = f' fill-opacity="{opacity}"' if opacity is not None else ""
        pid = self.did()
        self.parts.append(
            f'<rect id="{pid}" data-pptx-role="{role}" x="{x}" y="{y}" '
            f'width="{width}" height="{height}" fill="{fill}"{op}/>')
        return self

    def line(self, x1, y1, x2, y2, color=RULE, width=1, opacity=None, dash=None):
        op = f' stroke-opacity="{opacity}"' if opacity is not None else ""
        da = f' stroke-dasharray="{dash}"' if dash else ""
        pid = self.did()
        self.parts.append(
            f'<line id="{pid}" data-pptx-role="decoration" x1="{x1}" y1="{y1}" '
            f'x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{op}{da}/>')
        return self

    def circle(self, cx, cy, r, fill, opacity=None, stroke=None, sw=2):
        op = f' fill-opacity="{opacity}"' if opacity is not None else ""
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        pid = self.did()
        self.parts.append(
            f'<circle id="{pid}" data-pptx-role="decoration" cx="{cx}" cy="{cy}" '
            f'r="{r}" fill="{fill}"{op}{st}/>')
        return self

    def diamond(self, cx, cy, r, fill):
        pid = self.did()
        self.parts.append(
            f'<polygon id="{pid}" data-pptx-role="decoration" '
            f'points="{cx},{cy-r} {cx+r},{cy} {cx},{cy+r} {cx-r},{cy}" fill="{fill}"/>')
        return self

    def image(self, x, y, width, height, href):
        idx = self.take()
        pid = f"{self.key}-pic{idx}"
        self.parts.append(
            f'<g id="{pid}" data-pptx-placeholder="picture" data-pptx-idx="{idx}" '
            f'data-pptx-bounds="{x} {y} {width} {height}">'
            f'<image data-pptx-carrier="true" x="{x}" y="{y}" width="{width}" '
            f'height="{height}" preserveAspectRatio="xMidYMid slice" href="{href}"/></g>')
        return self

    def header(self, section, page_no, dark=False):
        color = "#C8D5DE" if dark else MUTED
        self.rect(90, 76, 13, 13, RED)
        self.ph(118, 64, 720, 36, section.upper(), 16, color, weight="bold",
                ls="2.2", baseline=90)
        self.ph_right(1150, 64, 300, 36, f"STRATEGY REVIEW / {page_no:02d}", 14,
                      color, weight="bold", ls="1.4", baseline=90,
                      ph_type="slide-number")
        if not dark:
            self.line(90, 108, 1150, 108, NAVY, 2)
        return self

    def footer(self, source, page_no, dark=False,
               note="ILLUSTRATIVE EXHIBIT / DEMONSTRATION DATA"):
        color = "#9FB1BE" if dark else MUTED
        if not dark:
            self.line(90, 1638, 1150, 1638, RULE, 1)
        self.ph(90, 1648, 920, 34, source.upper(), 14, color, ls="1.0", baseline=1672)
        self.ph(90, 1682, 920, 32, note, 13, color, ls="0.8", baseline=1704)
        self.ph_right(1150, 1648, 110, 36, f"{page_no:02d}", 16, color,
                      weight="bold", baseline=1674, ph_type="slide-number")
        return self

    def action(self, kicker, lines, top=186, size=56, leading=None, width=1060,
               fill=INK, height=None):
        lead = leading if leading is not None else round(size * 1.16, 2)
        if kicker:
            self.ph(90, top - 44, 760, 32, kicker.upper(), 16, RED, weight="bold",
                    ls="2.2", baseline=top - 18)
        if isinstance(lines, str):
            lines = [lines]
        h = height if height is not None else len(lines) * lead + 30
        self.ph(90, top, width, h, lines, size, fill, family="Georgia",
                weight="bold", leading=lead, ph_type="title")
        return self

    def lead(self, content, top, width=1020, size=27, fill=MUTED, lines=2,
             leading=38):
        return self.para(90, top, width, lines * (leading or size * 1.40) + 16,
                         content, size, fill, family="Georgia", leading=leading)

    def svg(self):
        return "\n".join(self.parts) + "\n</svg>\n"


# ---------------------------------------------------------------- page 1
def page_cover():
    p = Page("br-cover", "Bold boardroom cover")
    p.image(0, 0, 1240, 1754, "../images/ocean.jpg")
    p.add('<defs><linearGradient id="cover-shade" x1="0" y1="0" x2="0" y2="1">'
          '<stop offset="0" stop-color="#071C2C" stop-opacity="0.70"/>'
          '<stop offset="0.55" stop-color="#071C2C" stop-opacity="0.84"/>'
          '<stop offset="1" stop-color="#071C2C" stop-opacity="0.97"/>'
          '</linearGradient></defs>')
    p.rect(0, 0, 1240, 1754, "url(#cover-shade)")
    p.rect(90, 92, 420, 60, RED)
    p.ph(112, 100, 380, 44, "STRATEGY / REVIEW", 24, WHITE, weight="bold",
         ls="2.4", baseline=134)
    p.ph_right(1150, 100, 340, 44, "ISSUE 07 / OCTOBER 2026", 15, "#C8D5DE",
               weight="bold", ls="1.8", baseline=132)
    p.line(90, 188, 1150, 188, WHITE, 1, 0.45)
    p.ph(90, 236, 820, 36, "THE OPERATING MODEL QUESTION", 18, CYAN,
         weight="bold", ls="2.8", baseline=264)
    p.ph(90, 318, 1040, 470, ["The next", "advantage is", "operational."], 128,
         WHITE, family="Georgia", weight="bold", leading=132, ph_type="title")
    p.rect(90, 836, 130, 5, CYAN)
    p.ph(90, 874, 860, 130, ["Growth is no longer the constraint.",
                             "The operating model is."], 34, "#D8E2E9",
         family="Georgia", leading=46, ph_type="subtitle")
    p.ph(90, 1118, 900, 34,
         "INSIDE / THE BRIDGE · WHERE TO PLAY · THE PLAN · THE TESTS",
         15, "#9FB1BE", weight="bold", ls="1.6", baseline=1144)
    facts = [("4.2 pts", "MARGIN GAP"), ("23 days", "DELIVERY DELAY"),
             ("90 days", "TO FIRST GATE")]
    for i, (big, small) in enumerate(facts):
        x = 90 + i * 330
        p.ph(x, 1296, 300, 78, big, 54, WHITE, family="Georgia", weight="bold",
             baseline=1356)
        p.ph(x, 1378, 300, 32, small, 15, "#9FB1BE", weight="bold", ls="1.8",
             baseline=1402)
    p.line(90, 1560, 1150, 1560, WHITE, 1, 0.35)
    p.ph(90, 1582, 860, 36, "A4 / BOARDROOM EDITION · RESEARCH-LED, EDITORIALLY EDITED",
         15, "#C8D5DE", weight="bold", ls="1.4", baseline=1610)
    p.ph_right(1150, 1582, 110, 36, "01", 16, WHITE, weight="bold",
               baseline=1610, ph_type="slide-number")
    return p


# ---------------------------------------------------------------- page 2
def page_argument():
    p = Page("br-argument", "The argument in one page")
    p.rect(0, 0, 1240, 1754, PAPER)
    p.header("The argument / in one page", 2)
    p.action("THE ARGUMENT", ["Growth is no longer the constraint.",
                              "Execution is."], top=168, size=56)
    p.lead("Order intake is healthy. The gap between demand and revenue now sits "
           "inside the operating model — in the way we choose, staff and ship work.",
           top=364, width=1020, size=27, lines=2, leading=38)
    findings = [
        ("01", "Demand is not the problem.",
         "Order intake grew 7.4% while revenue grew 2.1%. The gap is delivery, not appetite."),
        ("02", "Complexity is the tax.",
         "Six planning cycles and fourteen approval gates add twenty-three days to every launch."),
        ("03", "The fix is structural.",
         "Simplify the portfolio, rebuild the operating rhythm, and fund the boring core."),
    ]
    for i, (num, title, body) in enumerate(findings):
        x = 90 + i * 370
        p.rect(x, 548, 64, 4, RED)
        p.ph(x, 566, 80, 52, num, 28, RED, family="Georgia", weight="bold",
             baseline=602)
        p.ph(x, 630, 330, 100, wrap(title, 330, 28, weight="bold"), 28, INK,
             weight="bold", leading=34)
        p.para(x, 744, 330, 220, body, 20, MUTED, family="Georgia", leading=29)
    p.line(90, 1006, 1150, 1006, RULE, 1)
    metrics = [("4.2", "PTS", "margin gap"), ("23", "DAYS", "delivery delay"),
               ("3", "MOVES", "to reset the model")]
    for i, (big, unit, cap) in enumerate(metrics):
        x = 90 + i * 370
        p.ph(x, 1034, 330, 96, big, 76, NAVY, family="Georgia", weight="bold",
             baseline=1112)
        p.ph(x, 1122, 330, 32, f"{unit} / {cap.upper()}", 15, MUTED,
             weight="bold", ls="1.6", baseline=1148)
    p.rect(0, 1236, 1240, 288, NAVY)
    p.ph(90, 1268, 420, 32, "THE DECISION", 16, CYAN, weight="bold", ls="2.2",
         baseline=1294)
    p.ph(90, 1312, 410, 110, ["Three questions", "for the board."], 36, WHITE,
         family="Georgia", weight="bold", leading=44)
    decisions = [("01", ["Where will we", "stop competing?"]),
                 ("02", ["Which two bottlenecks", "do we fund?"]),
                 ("03", ["Who owns the", "operating rhythm?"])]
    for i, (num, lines) in enumerate(decisions):
        x = 510 + i * 218
        p.ph(x, 1296, 204, 34, num, 16, CYAN, weight="bold", ls="1.6", baseline=1322)
        p.ph(x, 1334, 204, 120, lines, 20, WHITE, weight="bold", leading=28)
    p.footer("Illustrative board memo · figures are demonstration data", 2)
    return p


# ---------------------------------------------------------------- page 3
def page_contents():
    p = Page("br-contents", "Contents / five decisions")
    p.rect(0, 0, 1240, 1754, PAPER)
    p.header("Contents / October 2026", 3)
    p.action("CONTENTS", "Five decisions, in order.", top=176, size=56)
    p.lead("This is a working review, not a deck of themes. Each section ends with "
           "a choice the board can take, defer or reject.", top=276, width=750,
           size=23, lines=2, leading=33)
    rows = [
        ("01", "The argument", "Demand is healthy; delivery is not.", "02"),
        ("02", "The evidence", "Where the twenty-three days actually go.", "04"),
        ("03", "The choices", "Three operating models, one answer.", "09"),
        ("04", "The plan", "Ninety days, three gates, named owners.", "10"),
        ("05", "The test", "Six numbers the board will watch.", "14"),
    ]
    for i, (num, title, desc, page) in enumerate(rows):
        top = 432 + i * 186
        p.ph(90, top, 66, 60, num, 34, RED, family="Georgia", weight="bold",
             baseline=top + 42)
        p.ph(168, top - 4, 560, 44, title, 30, INK, weight="bold", baseline=top + 34)
        p.para(168, top + 52, 580, 80, desc, 21, MUTED, family="Georgia", leading=30)
        p.ph_right(830, top - 4, 70, 44, page, 20, MUTED, weight="bold",
                   baseline=top + 34)
        p.line(90, top + 140, 830, top + 140, RULE, 1)
    p.rect(870, 150, 280, 1390, NAVY)
    p.ph(900, 188, 220, 32, "AT A GLANCE", 15, CYAN, weight="bold", ls="2.0",
         baseline=214)
    p.line(900, 236, 1120, 236, "#5C7180", 1)
    stats = [("4.2", "PTS", "margin gap to close"), ("23", "DAYS", "in every launch"),
             ("90", "DAYS", "to the first gate")]
    for i, (big, unit, cap) in enumerate(stats):
        top = 286 + i * 220
        p.ph(900, top, 220, 92, big, 64, WHITE, family="Georgia", weight="bold",
             baseline=top + 64)
        p.ph(900, top + 78, 230, 30, f"{unit} / {cap.upper()}", 13, "#C8D5DE",
             weight="bold", ls="1.0", baseline=top + 100)
        p.line(900, top + 124, 1120, top + 124, "#5C7180", 1)
    p.ph(900, 998, 220, 30, "READING TIME", 14, CYAN, weight="bold", ls="1.6",
         baseline=1022)
    p.ph(900, 1034, 220, 48, "12 min", 32, WHITE, family="Georgia", weight="bold",
         baseline=1072)
    p.ph(900, 1132, 220, 30, "BOARD PAPER", 14, CYAN, weight="bold", ls="1.6",
         baseline=1156)
    p.ph(900, 1168, 220, 72, ["Decision", "required"], 24, WHITE, weight="bold",
         leading=30)
    p.line(900, 1296, 1120, 1296, "#5C7180", 1)
    p.para(900, 1324, 220, 170,
           "All figures are illustrative and constructed for this template.", 16,
           "#C8D5DE", family="Georgia", leading=24)
    p.footer("Boardroom strategy review · contents", 3)
    return p


# ---------------------------------------------------------------- page 4
def page_briefing():
    p = Page("br-briefing", "Briefing / the demand gap")
    p.rect(0, 0, 1240, 1754, PAPER)
    p.header("Briefing / the gap", 4)
    p.action("BRIEFING", ["Orders are up 7.4%.", "Revenue is up 2.1%."],
             top=168, size=56)
    p.lead("The difference is not a demand problem. It is the cumulative cost of "
           "six planning cycles, fourteen gates and no single owner.", top=354,
           width=1020, size=27, lines=2, leading=38)
    # chart
    p.ph(90, 482, 720, 34, "ORDER INTAKE VS REVENUE / INDEX, 2022 = 100", 15, MUTED,
         weight="bold", ls="1.5", baseline=508)
    x0, x1, ytop, ybase = 148, 790, 560, 1000
    for label in (130, 120, 110, 100):
        y = ytop + (130 - label) / 30 * (ybase - ytop)
        p.line(x0, y, x1, y, RULE, 1, 0.8)
        p.tick(134, y + 5, str(label), 14, MUTED, anchor="end")
    years = ["2022", "2023", "2024", "2025", "2026"]
    for i, year in enumerate(years):
        x = x0 + i * (x1 - x0) / 4
        p.tick(x, 1036, year, 14, MUTED, anchor="middle")
    intake = [100, 106, 112, 120, 127]
    revenue = [100, 102, 104, 106, 108]
    def cy(value):
        return ybase - (value - 100) * (ybase - ytop) / 30
    def cx(i):
        return x0 + i * (x1 - x0) / 4
    for series, color, width in ((intake, NAVY, 4), (revenue, CYAN, 4)):
        pts = " ".join(f"{cx(i)},{cy(v)}" for i, v in enumerate(series))
        p.add(f'<polyline id="{p.did()}" data-pptx-role="decoration" points="{pts}" '
              f'fill="none" stroke="{color}" stroke-width="{width}" '
              f'stroke-linejoin="round" stroke-linecap="round"/>')
        for i, v in enumerate(series):
            p.circle(cx(i), cy(v), 5 if color == NAVY else 5.5, WHITE, 1, color, 2.5)
    p.ph(x1, cy(127) - 34, 280, 28, "ORDER INTAKE / 127", 15, NAVY,
         weight="bold", ls="1.2", baseline=cy(127) - 12, anchor="end")
    p.ph(x1, cy(108) + 18, 280, 28, "REVENUE / 108", 15, CYAN,
         weight="bold", ls="1.2", baseline=cy(108) + 40, anchor="end")
    # right rail
    p.rect(840, 486, 310, 594, PAPER)
    p.line(840, 486, 1150, 486, NAVY, 2)
    p.ph(840, 506, 310, 32, "THE GAP, DECOMPOSED", 15, RED, weight="bold",
         ls="1.8", baseline=530)
    rail = [("23", "DAYS", "added to every launch by the current gate sequence"),
            ("14", "GATES", "of approval between concept and first shipment"),
            ("6", "CYCLES", "of planning that re-open decisions already taken")]
    for i, (big, unit, cap) in enumerate(rail):
        top = 556 + i * 168
        p.ph(840, top, 110, 68, big, 52, NAVY, family="Georgia", weight="bold",
             baseline=top + 50)
        p.ph(950, top + 14, 190, 28, unit, 15, RED, weight="bold", ls="1.6",
             baseline=top + 34)
        p.para(840, top + 62, 300, 84, cap, 18, MUTED, family="Georgia", leading=25)
        p.line(840, top + 150, 1150, top + 150, RULE, 1)
    # body
    p.ph(90, 1094, 340, 32, "WHAT CHANGED", 16, RED, weight="bold", ls="2.0",
         baseline=1120)
    p.para(90, 1132, 335, 380,
           "The order book has grown faster than the organisation's ability to "
           "convert it. Revenue follows intake with a two-year lag, and the lag is "
           "widening, not closing.", 20, INK, family="Georgia", leading=30)
    p.para(445, 1132, 335, 380,
           "Price is not the constraint. Win rates and average selling prices are "
           "stable. What has changed is the volume of exceptions each launch now "
           "carries through the same fixed gate sequence.", 20, INK,
           family="Georgia", leading=30)
    p.rect(810, 1094, 340, 412, NAVY)
    p.ph(840, 1126, 280, 30, "PULL QUOTE", 15, CYAN, weight="bold", ls="2.0",
         baseline=1150)
    p.para(840, 1170, 280, 240,
           "We are not short of demand. We are short of throughput.", 30, WHITE,
           family="Georgia", italic=True, leading=42)
    p.ph(840, 1432, 280, 30, "COO / OPERATING REVIEW", 14, "#9FB1BE",
         weight="bold", ls="1.4", baseline=1456)
    p.footer("Illustrative operating review · index and counts are demonstration data", 4)
    return p


# ---------------------------------------------------------------- page 5
def page_waterfall():
    p = Page("br-waterfall", "Margin bridge")
    p.rect(0, 0, 1240, 1754, PAPER)
    p.header("The bridge / margin", 5)
    p.action("THE BRIDGE", "Four moves close the 4.2-point gap.", top=168, size=56)
    p.lead("Margin bridge, FY2024 to FY2027, percentage points. Cost is shown as "
           "a negative move; all other bars are accretive.", top=282, width=1020,
           size=27, lines=2, leading=38)
    x0, ybase, scale = 210, 1170, 88
    def my(v):
        return ybase - (v - 16) * scale
    for v in (16, 18, 20, 22, 24):
        y = my(v)
        p.line(190, y, 1140, y, RULE, 1, 0.9)
        p.tick(176, y + 5, f"{v}%", 14, MUTED, anchor="end")
    bars = [
        ("FY24\nmargin", 18.6, 18.6, NAVY, "18.6%"),
        ("Pricing\ndiscipline", 18.6, 20.5, CYAN, "+1.9"),
        ("Portfolio\nfocus", 20.5, 22.0, CYAN, "+1.5"),
        ("Delivery\nyield", 22.0, 23.2, CYAN, "+1.2"),
        ("Transition\ncost", 23.2, 22.8, RED, "-0.4"),
        ("FY27\ntarget", 14.0, 22.8, NAVY, "22.8%"),
    ]
    xs = [210 + i * 160 for i in range(6)]
    for i, (label, start, end, color, tag) in enumerate(bars):
        x = xs[i]
        top, bottom = sorted((my(end), my(start)))
        if i == 5:
            top, bottom = my(22.8), ybase
        p.rect(x, top, 124, bottom - top, color, 0.92 if color == RED else None)
        if i == 4:
            p.tick(x + 62, top + 25, tag, 17, WHITE, weight="bold", anchor="middle")
        else:
            p.tick(x + 62, top - 14, tag, 20, color if color != NAVY else NAVY,
                   weight="bold", anchor="middle")
        p.ph(x - 12, 1196, 148, 72, label.split("\n"), 17, INK, weight="bold",
             leading=23, anchor="middle")
        if i < 5:
            p.line(x + 124, my(end), xs[i + 1], my(end), MUTED, 1, 0.7, "4 5")
    p.rect(90, 1326, 1060, 210, NAVY)
    p.ph(120, 1360, 320, 30, "SO WHAT", 15, CYAN, weight="bold", ls="2.2",
         baseline=1384)
    p.ph(120, 1398, 680, 110, ["Half the gap is decision speed,", "not price."],
         36, WHITE, family="Georgia", weight="bold", leading=45)
    p.ph_right(1120, 1354, 280, 96, "4.2", 74, CYAN, family="Georgia",
               weight="bold", baseline=1426)
    p.ph_right(1120, 1436, 280, 30, "PTS / TOTAL GAP", 15, "#9FB1BE",
               weight="bold", ls="1.6", baseline=1460)
    p.footer("Illustrative margin bridge · values are demonstration data", 5)
    return p


# ---------------------------------------------------------------- page 6
def page_matrix():
    p = Page("br-matrix", "Where to play")
    p.rect(0, 0, 1240, 1754, PAPER)
    p.header("Where to play", 6)
    p.action("WHERE TO PLAY", "We win in two quadrants, not four.",
             top=168, size=56)
    p.lead("Each bubble is a business line. Position reflects relative "
           "differentiation and willingness to pay; size reflects revenue.",
           top=282, width=1020, size=27, lines=2, leading=38)
    mx0, mx1, my0, my1 = 230, 1010, 440, 1200
    p.line(mx0, my1, mx1, my1, MUTED, 1, 0.55)
    p.line((mx0 + mx1) / 2, my0, (mx0 + mx1) / 2, my1, MUTED, 1, 0.45, "7 8")
    p.line(mx0, (my0 + my1) / 2, mx1, (my0 + my1) / 2, MUTED, 1, 0.45, "7 8")
    p.ph(mx1 - 16, my0 + 16, 220, 34, "BUILD", 18, NAVY, weight="bold", ls="2.2",
         baseline=my0 + 42, anchor="end")
    p.ph(mx0 + 16, my0 + 16, 200, 34, "HOLD", 18, MUTED, weight="bold", ls="2.2",
         baseline=my0 + 42)
    p.ph(mx1 - 16, my1 - 46, 220, 34, "FIX", 18, MUTED, weight="bold",
         ls="2.2", baseline=my1 - 20, anchor="end")
    p.ph(mx0 + 16, my1 - 46, 200, 34, "EXIT", 18, RED, weight="bold", ls="2.2",
         baseline=my1 - 20)
    p.ph(mx0, my0 - 38, 560, 32, "WILLINGNESS TO PAY →", 15, MUTED, weight="bold",
         ls="1.6", baseline=my0 - 12)
    p.ph(mx0, my1 + 18, 780, 32, "DEGREE OF DIFFERENTIATION →", 15, MUTED,
         weight="bold", ls="1.6", baseline=my1 + 42)
    p.tick(mx0, my1 + 70, "LOW", 14, MUTED, weight="bold")
    p.tick(mx1, my1 + 70, "HIGH", 14, MUTED, weight="bold", anchor="end")
    p.tick(mx0 - 14, my1 - 2, "LOW", 14, MUTED, weight="bold", anchor="end")
    p.tick(mx0 - 14, my0 + 10, "HIGH", 14, MUTED, weight="bold", anchor="end")
    def bx(g):
        return mx0 + g / 8 * (mx1 - mx0)
    def by(m):
        return my1 - (m - 8) / 22 * (my1 - my0)
    bubbles = [
        ("Core platform", 6.2, 24.0, 52, NAVY, WHITE),
        ("Data services", 7.1, 21.0, 30, CYAN, INK),
        ("Field service", 3.8, 22.0, 20, NAVY, WHITE),
        ("Managed ops", 2.4, 20.0, 58, STEEL, WHITE),
        ("Maintenance", 0.9, 17.2, 28, "#B9C7CF", INK),
        ("Adjacent tools", 5.2, 11.0, 26, "#B9C7CF", INK),
        ("Custom projects", 1.5, 12.2, 52, RED, WHITE),
        ("Hardware", 2.8, 8.8, 34, RED, WHITE),
        ("Legacy licences", 0.6, 25.0, 22, SAND, INK),
    ]
    for name, g, m, r, fill, ink in bubbles:
        cx, cy = bx(g), by(m)
        p.circle(cx, cy, r, fill, 0.88 if fill in (RED, CYAN) else None)
        p.tick(cx, cy - r - 12, name, 16, INK, weight="bold", anchor="middle")
    for i, (head, body) in enumerate([
        ("BUILD", "Fund the platform and data services; protect the price premium."),
        ("FIX", "Managed operations and maintenance carry the volume; simplify both."),
        ("EXIT", "Custom projects and hardware consume capital without a moat.")]):
        x = 90 + i * 370
        p.line(x, 1304, x + 320, 1304, RED if i == 2 else NAVY, 3)
        p.ph(x, 1318, 320, 32, head, 17, RED if i == 2 else NAVY, weight="bold",
             ls="2.0", baseline=1344)
        p.para(x, 1356, 320, 110, body, 20, MUTED, family="Georgia", leading=29)
    p.footer("Illustrative portfolio map · positions and sizes are demonstration data", 6)
    return p


# ---------------------------------------------------------------- page 7
def page_issue_tree():
    p = Page("br-tree", "Issue tree / launch delay")
    p.rect(0, 0, 1240, 1754, PAPER)
    p.header("Diagnosis / issue tree", 7)
    p.action("DIAGNOSIS", "Launches slip for one structural reason.",
             top=168, size=56, width=1060)
    p.lead("The twenty-three day delay decomposes into three causes. Only one "
           "of them is fixed by adding people.", top=282, width=920, size=28,
           lines=2, leading=40)
    p.rect(390, 372, 460, 88, NAVY)
    p.ph(414, 388, 412, 60, ["23-day launch delay"], 28, WHITE, weight="bold",
         baseline=428, anchor=None)
    p.line(620, 460, 620, 494, NAVY, 2)
    p.line(250, 494, 990, 494, NAVY, 2)
    for cx in (250, 620, 990):
        p.line(cx, 494, cx, 524, NAVY, 2)
    children = [
        (90, "Portfolio load", "Too many launches, each with a business case."),
        (460, "Decision rights", "No single owner; fourteen gates share a veto."),
        (830, "Handoffs", "Six teams, six systems, no shared definition of done."),
    ]
    for x, title, body in children:
        critical = title == "Decision rights"
        p.rect(x, 524, 320, 114, RED if critical else WHITE)
        p.ph(x + 20, 536, 280, 34, title, 22, WHITE if critical else INK,
             weight="bold", baseline=564)
        p.para(x + 20, 574, 280, 58, body, 17, "#FFE1DF" if critical else MUTED,
               leading=23)
        p.line(x + 22, 638, x + 22, 826, NAVY, 1.5, 0.55)
        for j in range(2):
            y = 706 + j * 120
            p.line(x + 22, y, x + 44, y, NAVY, 1.5, 0.55)
            p.rect(x + 44, y - 42, 276, 84, WHITE)
    leaves = [
        [(90 + 44, "11 active lines", "Four carry 80% of revenue."),
         (90 + 44, "No kill criteria", "Every case clears the same hurdle.")],
        [(460 + 44, "No named owner", "Accountability split three ways."),
         (460 + 44, "Veto at every gate", "Fourteen signatures, no deadline.")],
        [(830 + 44, "Six definitions", "Of 'ready' across six teams."),
         (830 + 44, "Manual re-entry", "Three systems, no reconciliation.")],
    ]
    for group in leaves:
        for j, (x, title, body) in enumerate(group):
            y = 706 + j * 120
            p.ph(x + 16, y - 32, 244, 28, title, 18, INK, weight="bold",
                 baseline=y - 8)
            p.para(x + 16, y - 2, 244, 42, body, 16, MUTED, family="Georgia",
                   leading=21)
    p.line(90, 996, 1150, 996, RULE, 1)
    evidence = [("6", "PLANNING CYCLES", "that re-open settled decisions"),
                ("14", "APPROVAL GATES", "between concept and shipment"),
                ("23", "DAYS OF DELAY", "added to every single launch")]
    for i, (big, unit, cap) in enumerate(evidence):
        x = 90 + i * 370
        p.ph(x, 1022, 100, 76, big, 56, RED, family="Georgia", weight="bold",
             baseline=1084)
        p.ph(x + 100, 1038, 250, 28, unit, 15, MUTED, weight="bold", ls="1.4",
             baseline=1060)
        p.para(x, 1106, 320, 70, cap, 19, MUTED, family="Georgia", leading=27)
    p.rect(0, 1244, 1240, 260, NAVY)
    p.ph(90, 1280, 420, 30, "THE IMPLICATION", 15, CYAN, weight="bold", ls="2.2",
         baseline=1304)
    p.ph(90, 1318, 760, 80, "One owner. Two gates. One cadence.", 36, WHITE,
         family="Georgia", weight="bold", baseline=1368)
    p.para(90, 1388, 780, 90,
           "Move authority to a single launch owner, cut the gate sequence to two "
           "decision points, and publish the date the owner has committed to.",
           20, "#C8D5DE", family="Georgia", leading=29)
    p.ph_right(1120, 1314, 220, 80, "1", 72, CYAN, family="Georgia",
               weight="bold", baseline=1384)
    p.ph_right(1120, 1396, 220, 28, "OWNER", 15, "#9FB1BE", weight="bold",
               ls="1.6", baseline=1420)
    p.footer("Illustrative issue tree · counts are demonstration data", 7)
    return p


# ---------------------------------------------------------------- page 8
def page_scenarios():
    p = Page("br-scenarios", "Three scenarios")
    p.rect(0, 0, 1240, 1754, PAPER)
    p.header("Scenarios / 2027", 8)
    p.action("SCENARIOS", "Three futures; one is affordable.", top=168, size=56)
    p.lead("Each scenario holds a different demand, price and cost path. The "
           "middle case is the only one that funds the plan and clears the covenant.",
           top=282, width=1020, size=27, lines=2, leading=38)
    cols = [
        (90, "BASE", "Markets hold", NAVY, "Continue the current rhythm."),
        (470, "ACCELERATE", "Recommended", CYAN, "Execute the three moves."),
        (850, "STRESS", "Demand contracts", RED, "Delay and protect cash."),
    ]
    p.rect(470, 422, 300, 5, CYAN)
    for x, name, note, color, _ in cols:
        p.ph(x, 434, 300, 34, name, 20, color, weight="bold", ls="2.0", baseline=460)
        p.ph(x, 468, 300, 28, note.upper(), 14, MUTED, weight="bold", ls="1.4",
             baseline=490)
    rows = [
        ("DEMAND GROWTH", ["+2.1%", "+4.0%", "-1.5%"]),
        ("PRICE", ["Flat", "+1.0%", "-2.0%"]),
        ("2027 MARGIN", ["21.0%", "22.8%", "17.9%"]),
        ("FREE CASH", ["0.9bn", "1.4bn", "0.3bn"]),
        ("HEADCOUNT", ["Flat", "-4%", "-9%"]),
    ]
    for i, (label, values) in enumerate(rows):
        top = 532 + i * 118
        p.ph(90, top, 360, 26, label, 14, MUTED, weight="bold", ls="1.4",
             baseline=top + 20)
        for j, value in enumerate(values):
            x = 90 + j * 380
            p.ph(x, top + 16, 300, 56, value, 30, INK, weight="bold",
                 baseline=top + 58)
        p.line(90, top + 88, 1150, top + 88, RULE, 1)
    p.ph(90, 1132, 620, 28, "2027 OPERATING MARGIN / COVENANT AT 22.0%", 15, MUTED,
         weight="bold", ls="1.4", baseline=1156)
    cx0, cx1 = 450, 1150
    def mx(v):
        return cx0 + (v - 16) / 8 * (cx1 - cx0)
    for v in (16, 18, 20, 22, 24):
        x = mx(v)
        p.line(x, 1196, x, 1356, RULE, 1)
        p.tick(x, 1384, f"{v}%", 14, MUTED, anchor="middle")
    cov = mx(22)
    p.line(cov, 1180, cov, 1356, RED, 1.5, 0.9, "5 4")
    p.ph(cov + 12, 1172, 160, 26, "COVENANT", 14, RED, weight="bold",
         ls="1.2", baseline=1194)
    for i, ((x, name, note, color, _), v) in enumerate(
            zip(cols, [float(value.rstrip("%")) for value in rows[2][1]])):
        y = 1236 + i * 50
        p.circle(90, y - 4, 6, color)
        p.ph(110, y - 20, 300, 30, name, 16, INK, weight="bold", ls="1.4",
             baseline=y + 4)
        dx = mx(v)
        p.circle(dx, y, 11, color)
        p.ph(dx + 18, y - 18, 100, 30, f"{v:.1f}%", 16, color, weight="bold",
             baseline=y + 6)
    p.rect(90, 1476, 5, 54, RED)
    p.ph(112, 1480, 1020, 48,
         "SWITCH TRIGGER: two consecutive quarters of order intake below 2%.",
         18, INK, weight="bold", ls="0.8", baseline=1512)
    p.footer("Illustrative scenario set · all values are demonstration data", 8)
    return p


# ---------------------------------------------------------------- page 9
def page_choice():
    p = Page("br-choice", "Three operating models")
    p.rect(0, 0, 1240, 1754, PAPER)
    p.header("The choice / operating model", 9)
    p.action("THE CHOICE", "Three operating models, one answer.", top=168, size=56)
    p.lead("The question is not centralise or decentralise. It is where the "
           "decision right sits for launches, pricing and service.", top=282,
           width=1020, size=27, lines=2, leading=38)
    p.rect(90, 386, 1060, 66, NAVY)
    p.rect(640, 452, 250, 588, PALE, 0.85)
    p.ph(110, 400, 270, 32, "CRITERION", 15, WHITE, weight="bold", ls="1.6",
         baseline=426)
    for i, name in enumerate(["STATUS QUO", "FEDERATED", "LOCAL"]):
        p.ph(400 + i * 250, 400, 240, 32, name, 15, WHITE, weight="bold",
             ls="1.6", baseline=426)
    rows = [
        ("Decision speed", "Six weeks", "Two weeks", "Four weeks"),
        ("Cost to serve", "Low", "Medium", "High"),
        ("Control", "Central", "Federated", "Local"),
        ("Required capex", "0.2bn", "0.6bn", "0.9bn"),
        ("Execution risk", "Low", "Medium", "High"),
        ("Verdict", "Drift", "RECOMMENDED", "Too slow"),
    ]
    for i, (label, a, b, c) in enumerate(rows):
        top = 452 + i * 98
        p.ph(110, top + 4, 270, 38, label, 21, INK, weight="bold", baseline=top + 42)
        for j, value in enumerate((a, b, c)):
            x = 400 + j * 250
            color = CYAN if (j == 1 and i == 5) else INK
            p.ph(x, top + 4, 230, 38, value, 21, color,
                 weight="bold" if (j == 1 and i == 5) else "normal",
                 baseline=top + 42)
        p.line(90, top + 78, 1150, top + 78, RULE, 1)
    p.ph(90, 1076, 320, 30, "WHY FEDERATED", 16, RED, weight="bold", ls="2.0",
         baseline=1100)
    p.para(90, 1114, 345, 310,
           "It keeps customer proximity while putting launch, pricing and service "
           "decisions under one accountable owner. It is the only model that "
           "removes a gate without adding a layer.", 20, INK, family="Georgia",
           leading=30)
    p.para(465, 1114, 345, 310,
           "Cost is contained by a shared platform, not by a central committee. "
           "Capex is funded from the portfolio exits, so the model pays for itself "
           "inside four quarters.", 20, INK, family="Georgia", leading=30)
    p.rect(840, 1076, 310, 344, NAVY)
    p.ph(870, 1106, 250, 28, "FUNDING", 15, CYAN, weight="bold", ls="1.8",
         baseline=1130)
    p.ph(870, 1146, 250, 84, "0.6bn", 60, WHITE, family="Georgia", weight="bold",
         baseline=1218)
    p.para(870, 1234, 254, 96, "over four quarters, funded by two portfolio exits.",
           19, "#C8D5DE", family="Georgia", leading=27)
    p.line(870, 1344, 1120, 1344, "#5C7180", 1)
    p.ph(870, 1356, 250, 28, "PAYBACK / 11 MONTHS", 14, "#9FB1BE", weight="bold",
         ls="1.4", baseline=1380)
    p.footer("Illustrative operating-model comparison · values are demonstration data", 9)
    return p


# ---------------------------------------------------------------- page 10
def page_roadmap():
    p = Page("br-roadmap", "The first ninety days")
    p.rect(0, 0, 1240, 1754, PAPER)
    p.header("The plan / first ninety days", 10)
    p.action("THE PLAN", "Ninety days, three gates.", top=168, size=56)
    p.lead("One plan, three workstreams, and a decision at every gate. No "
           "workstream starts without a named owner.", top=282, width=1020,
           size=27, lines=2, leading=38)
    tx0, tx1 = 310, 1140
    week = (tx1 - tx0) / 12
    p.ph(90, 392, 200, 30, "WEEK", 15, MUTED, weight="bold", ls="1.4",
         baseline=414)
    for w in (0, 3, 7, 11):
        p.tick(tx0 + (w + 0.5) * week, 414, f"W{w + 1}", 15, MUTED,
               weight="bold", anchor="middle")
    for i, (label, y) in enumerate([("COMMERCIAL", 470), ("OPERATIONS", 624),
                                    ("ORGANIZATION", 778)]):
        p.ph(90, y + 38, 210, 32, label, 16, NAVY, weight="bold", ls="1.4",
             baseline=y + 64)
        p.line(90, y + 116, 1150, y + 116, RULE, 1)
    def bar(x, w, y, color, label, ink=WHITE):
        p.rect(x, y, w, 54, color)
        p.ph(x + 12, y + 10, w - 24, 34, label, 15, ink, weight="bold", ls="1.0",
             baseline=y + 34)
    bar(tx0, week * 4, 496, NAVY, "PRICE ARCHITECTURE")
    bar(tx0 + week * 4, week * 4, 496, NAVY, "PORTFOLIO CUT")
    bar(tx0 + week * 8, week * 4, 496, NAVY, "ACCOUNT PLANS")
    bar(tx0, week * 4, 650, STEEL, "BOTTLENECK MAP")
    bar(tx0 + week * 4, week * 4, 650, CYAN, "DECISION RIGHTS", INK)
    bar(tx0 + week * 8, week * 4, 650, STEEL, "PILOT CELL")
    bar(tx0 + week, week * 4, 804, NAVY2, "OWNER MODEL")
    bar(tx0 + week * 4, week * 8, 804, SAND, "INCENTIVE RESET", INK)
    for i, gx in enumerate((tx0 + week * 4, tx0 + week * 8, tx1)):
        p.line(gx, 440, gx, 940, RED, 1.5, 0.5, "5 6")
        p.diamond(gx, 952, 12, RED)
        p.tick(gx, 992, f"G{i + 1}", 16, RED, weight="bold", anchor="middle")
    p.rect(0, 1164, 1240, 250, NAVY)
    p.ph(90, 1196, 360, 30, "DAY 90 / THE DECISION", 15, CYAN, weight="bold",
         ls="2.0", baseline=1220)
    p.ph(90, 1236, 520, 76, "Approve scale-up, or stop.", 36, WHITE,
         family="Georgia", weight="bold", baseline=1286)
    for i, condition in enumerate(["Two gates cleared", "One owner per move",
                                   "Capex inside 0.2bn"]):
        x = 620 + i * 180
        p.ph(x, 1226, 90, 30, f"0{i + 1}", 16, CYAN, weight="bold", baseline=1250)
        p.para(x, 1260, 166, 68, condition, 18, WHITE, weight="bold", leading=25)
    p.ph(90, 1456, 1060, 34,
         "NO NEW HEADCOUNT BEFORE GATE 2 · GATE REVIEWS REPLACE STAGE-GATE COMMITTEES",
         15, MUTED, weight="bold", ls="1.1", baseline=1482)
    p.footer("Illustrative ninety-day plan · dates and gates are demonstration data", 10)
    return p


# ---------------------------------------------------------------- page 11
def page_portfolio():
    p = Page("br-portfolio", "Portfolio bubble chart")
    p.rect(0, 0, 1240, 1754, PAPER)
    p.header("Portfolio / capital allocation", 11)
    p.action("PORTFOLIO", "Fund four, fix three, exit two.", top=168, size=56)
    p.lead("Market growth against operating margin. Bubble size is revenue; the "
           "dashed lines mark the portfolio's median position.", top=282,
           width=1020, size=27, lines=2, leading=38)
    gx0, gx1, gy0, gy1 = 230, 1050, 434, 1190
    p.line(gx0, gy1, gx1, gy1, MUTED, 1, 0.6)
    p.line(gx0, gy0, gx0, gy1, MUTED, 1, 0.6)
    p.line(640, gy0, 640, gy1, MUTED, 1, 0.5, "7 8")
    p.line(gx0, 800, gx1, 800, MUTED, 1, 0.5, "7 8")
    for v in (5, 10, 15, 20, 25):
        y = gy1 - (v - 5) / 22 * (gy1 - gy0)
        p.line(gx0, y, gx1, y, RULE, 1, 0.6)
        p.tick(gx0 - 14, y + 5, f"{v}%", 14, MUTED, anchor="end")
    for v in (0, 2, 4, 6, 8):
        x = gx0 + v / 8 * (gx1 - gx0)
        p.tick(x, gy1 + 26, f"{v}%", 14, MUTED, anchor="middle")
    p.ph(gx0, gy1 + 48, 780, 30, "MARKET GROWTH →", 15, MUTED, weight="bold",
         ls="1.6", baseline=gy1 + 72)
    p.ph(gx0, gy0 - 36, 560, 30, "OPERATING MARGIN ↑", 15, MUTED, weight="bold",
         ls="1.6", baseline=gy0 - 10)
    def bx(g):
        return gx0 + g / 8 * (gx1 - gx0)
    def by(m):
        return gy1 - (m - 5) / 22 * (gy1 - gy0)
    bubbles = [
        ("Core platform", 6.2, 24.0, 52, NAVY),
        ("Data services", 7.1, 21.0, 30, CYAN),
        ("Field service", 3.8, 22.0, 20, NAVY),
        ("Managed ops", 2.4, 20.0, 58, STEEL),
        ("Maintenance", 0.9, 17.2, 28, "#B9C7CF"),
        ("Adjacent tools", 5.2, 11.0, 26, "#B9C7CF"),
        ("Custom projects", 1.5, 12.2, 52, RED),
        ("Hardware", 2.8, 8.8, 34, RED),
        ("Legacy licences", 0.6, 25.0, 22, SAND),
    ]
    for name, g, m, r, fill in bubbles:
        cx, cy = bx(g), by(m)
        p.circle(cx, cy, r, fill, 0.88 if fill in (RED, CYAN) else None)
        p.tick(cx, cy - r - 12, name, 16, INK, weight="bold", anchor="middle")
    p.rect(0, 1324, 1240, 264, NAVY)
    p.rect(90, 1358, 10, 10, CYAN)
    p.ph(112, 1348, 680, 30, "62% OF CAPITAL SITS BELOW THE LINE", 15, CYAN,
         weight="bold", ls="1.4", baseline=1372)
    for i, (head, color, body) in enumerate([
        ("FUND", CYAN, "Platform, data, field service: protect price and compound."),
        ("FIX", STEEL, "Managed operations: simplify the offer and the cost base."),
        ("EXIT", RED, "Custom projects, hardware, legacy: sell or wind down.")]):
        x = 90 + i * 370
        p.circle(x + 10, 1424, 7, color)
        p.ph(x + 28, 1408, 300, 30, head, 18, WHITE, weight="bold", ls="2.0",
             baseline=1432)
        p.para(x, 1448, 330, 100, body, 20, "#C8D5DE", family="Georgia", leading=29)
    p.footer("Illustrative portfolio map · positions and sizes are demonstration data", 11)
    return p


# ---------------------------------------------------------------- page 12
def page_essay():
    p = Page("br-essay", "The leader essay")
    p.rect(0, 0, 1240, 1754, PAPER)
    p.rect(90, 86, 228, 44, RED)
    p.ph(110, 92, 196, 32, "THE LEADER", 16, WHITE, weight="bold", ls="2.4",
         baseline=118)
    p.ph_right(1150, 88, 240, 32, "12 / THE LEADER", 14, MUTED, weight="bold",
               ls="1.6", baseline=116, ph_type="slide-number")
    p.line(90, 148, 1150, 148, NAVY, 2)
    p.ph(90, 204, 1040, 130, "The case for boring.", 84, INK, family="Georgia",
         weight="bold", baseline=298, ph_type="title")
    p.ph(90, 342, 920, 120,
         ["The case for a strategy that survives", "contact with the calendar."],
         32, MUTED, family="Georgia", italic=True, leading=44, ph_type="subtitle")
    p.ph(90, 480, 760, 28, "BY THE STRATEGY OFFICE · 6 MIN READ · OCTOBER 2026",
         14, MUTED, weight="bold", ls="1.6", baseline=502)
    p.line(90, 528, 1150, 528, RULE, 1)
    left = [
        ("The strategy industry has a weakness for drama. Transformation "
         "programmes are announced with the gravity of moon landings, then "
         "quietly re-baselined when the quarter turns. The result is a familiar "
         "pattern: a bold diagnosis, a crowded slide, and a second year that "
         "looks much like the first."),
        ("The alternative is less photogenic. Pick a small number of moves "
         "that change how work actually flows, assign one owner to each, and "
         "measure them every month until the behaviour sticks. Call it boring "
         "if you like. Boring compounds."),
    ]
    right = [
        ("That is the bet in this review. Three moves — simplify the portfolio, "
         "rebuild decision rights, reset the operating rhythm — are unglamorous "
         "individually. Together they close a 4.2-point margin gap and take "
         "twenty-three days out of every launch."),
        ("The test is not whether the plan sounds ambitious. It is whether the "
         "organisation can repeat it without a programme office standing over "
         "it. Discipline, not drama, is the strategy. The board will know within "
         "one quarter whether the habit has taken."),
    ]
    p.para(90, 560, 500, 620, left, 23, INK, family="Georgia", leading=35)
    p.para(624, 560, 500, 620, right, 23, INK, family="Georgia", leading=35)
    p.line(607, 560, 607, 1200, RULE, 1)
    p.rect(90, 1244, 6, 140, RED)
    p.ph(120, 1248, 980, 150,
         ["“Boring is not a lack of ambition.", "It is ambition with a schedule.”"],
         38, NAVY, family="Georgia", italic=True, leading=50)
    p.ph(120, 1412, 900, 28, "THE STRATEGY OFFICE / FOR THE BOARD, OCTOBER 2026",
         14, MUTED, weight="bold", ls="1.6", baseline=1434)
    p.line(90, 1476, 1150, 1476, RULE, 1)
    p.ph(90, 1496, 940, 30, "NEXT: THE PLAN ON PAGE 10 · THE TEST ON PAGE 14",
         14, MUTED, weight="bold", ls="1.4", baseline=1520)
    p.footer("The leader · boardroom strategy review", 12)
    return p


# ---------------------------------------------------------------- page 13
def page_recommendation():
    p = Page("br-recommendation", "Three moves in sequence")
    p.rect(0, 0, 1240, 1754, PAPER)
    p.header("Recommendation / three moves", 13)
    p.action("RECOMMENDATION", "Three moves, in this sequence.", top=168, size=56)
    p.lead("Each move has one owner, a funded cost and a measurable contribution. "
           "Together they close the gap; separately they leak.", top=282,
           width=1020, size=27, lines=2, leading=38)
    headers = [(690, "OWNER"), (855, "INVEST"), (1000, "IMPACT")]
    for x, name in headers:
        p.ph(x, 380, 140, 28, name, 15, MUTED, weight="bold", ls="1.4",
             baseline=402)
    p.line(90, 414, 1150, 414, NAVY, 1.5)
    moves = [
        ("01", "Simplify the portfolio",
         "Cut two lines, fund four. Publish kill criteria before the next budget cycle.",
         "CEO / CFO", "0.1bn", "+1.1 pts"),
        ("02", "Rebuild decision rights",
         "One launch owner, two decision gates, three planning cycles instead of six.",
         "COO", "0.2bn", "+1.6 pts"),
        ("03", "Reset the operating rhythm",
         "Quarterly gate, monthly review, weekly delivery cell with the same metrics.",
         "COO / CHRO", "0.1bn", "+1.5 pts"),
    ]
    for i, (num, title, body, owner, invest, impact) in enumerate(moves):
        top = 446 + i * 252
        p.ph(90, top, 84, 74, num, 44, RED, family="Georgia", weight="bold",
             baseline=top + 54)
        p.ph(180, top, 490, 48, title, 30, INK, weight="bold", baseline=top + 36)
        p.para(180, top + 54, 480, 110, body, 20, MUTED, family="Georgia",
               leading=29)
        p.ph(690, top + 2, 150, 36, owner, 19, INK, weight="bold", baseline=top + 34)
        p.ph(855, top + 2, 130, 36, invest, 20, INK, weight="bold", baseline=top + 34)
        p.ph(1000, top + 2, 150, 36, impact, 22, NAVY, weight="bold",
             baseline=top + 34)
        p.line(90, top + 174, 1150, top + 174, RULE, 1)
    p.line(90, 1184, 1150, 1184, NAVY, 2)
    p.ph(690, 1196, 300, 30, "TOTAL / FOUR QUARTERS", 15, MUTED, weight="bold",
         ls="1.4", baseline=1220)
    p.ph(1000, 1190, 150, 40, "+4.2 pts", 30, NAVY, family="Georgia",
         weight="bold", baseline=1224)
    p.rect(0, 1256, 1240, 268, NAVY)
    p.rect(90, 1288, 136, 48, RED)
    p.ph(106, 1296, 110, 32, "THE ASK", 15, WHITE, weight="bold", ls="1.6",
         baseline=1322)
    p.ph(90, 1354, 720, 64, "Approve 0.4bn and three owners.", 36, WHITE,
         family="Georgia", weight="bold", baseline=1402)
    p.para(90, 1418, 720, 76,
           "Decision by Friday; owner letters within five working days; first gate "
           "thirty days from approval.", 20, "#C8D5DE", family="Georgia", leading=29)
    for i, (date, item) in enumerate([("FRI 30 OCT", "BOARD DECISION"),
                                      ("MON 02 NOV", "OWNER LETTERS"),
                                      ("FRI 27 NOV", "GATE 1 REVIEW")]):
        p.ph(845, 1310 + i * 54, 305, 34, f"{date}  /  {item}", 15,
             WHITE, weight="bold", ls="1.0", baseline=1336 + i * 54)
    p.footer("Illustrative recommendation · figures are demonstration data", 13)
    return p


# ---------------------------------------------------------------- page 14
def page_scoreboard():
    p = Page("br-scoreboard", "The scoreboard")
    p.rect(0, 0, 1240, 1754, PAPER)
    p.header("The scoreboard / six numbers", 14)
    p.action("THE TEST", "Six numbers the board will watch.", top=168, size=56)
    p.lead("Baseline, ninety-day checkpoint and twelve-month target. One owner "
           "per number; no number without a review date.", top=282, width=1020,
           size=27, lines=2, leading=38)
    cards = [
        ("MARGIN", "18.6%", 0.19, "19.4%", "22.8%", "CFO / MONTHLY"),
        ("LAUNCH CYCLE", "23 days", 0.50, "16 days", "9 days", "COO / MONTHLY"),
        ("DECISION GATES", "14", 0.60, "8", "4", "COO / MONTHLY"),
        ("ON-TIME DELIVERY", "78%", 0.50, "86%", "94%", "BU LEADS / MONTHLY"),
        ("PORTFOLIO LINES", "11", 0.50, "9", "7", "CEO / QUARTERLY"),
        ("ENGAGEMENT", "61%", 0.38, "66%", "74%", "CHRO / QUARTERLY"),
    ]
    for i, (label, base, prog, mid, target, owner) in enumerate(cards):
        col, row = i % 2, i // 2
        x = 90 + col * 560
        top = 390 + row * 270
        p.line(x, top, x + 500, top, RULE, 1)
        p.ph(x, top + 6, 340, 28, label, 16, MUTED, weight="bold", ls="1.6",
             baseline=top + 30)
        p.ph(x + 500, top + 6, 110, 28, f"{i + 1:02d} / 06", 14, MUTED,
             weight="bold", ls="1.2", baseline=top + 30, anchor="end")
        p.ph(x, top + 54, 250, 70, base, 54, INK, family="Georgia",
             weight="bold", baseline=top + 106)
        p.ph(x, top + 116, 250, 26, "BASELINE / FY24", 14, MUTED, weight="bold",
             ls="1.2", baseline=top + 138)
        tx0, tx1, ty = x + 260, x + 480, top + 84
        p.line(tx0, ty - 7, tx0, ty + 7, MUTED, 1.5)
        p.line(tx1, ty - 8, tx1, ty + 8, NAVY, 2.5)
        dxt = tx0 + (tx1 - tx0) * prog
        p.line(tx0, ty, dxt, ty, NAVY, 2.5)
        p.line(dxt, ty, tx1, ty, STEEL, 1.5)
        p.circle(tx0, ty, 5, PAPER, None, MUTED, 1.5)
        p.circle(dxt, ty, 6, NAVY)
        p.ph(dxt, top + 44, 170, 28, f"90-DAY {mid}", 15, INK, weight="bold",
             ls="0.8", baseline=top + 66, anchor="middle")
        p.ph(tx1, top + 104, 220, 28, f"TARGET {target} / 12M", 14, NAVY,
             weight="bold", ls="0.8", baseline=top + 128, anchor="end")
        p.line(x, top + 174, x + 500, top + 174, RULE, 1)
        p.ph(x, top + 182, 400, 28, f"OWNER / {owner}", 14, MUTED,
             weight="bold", ls="1.2", baseline=top + 206)
    p.line(90, 1218, 1150, 1218, NAVY, 2)
    p.ph(90, 1244, 520, 30, "READING THE SCOREBOARD", 15, RED, weight="bold",
         ls="2.0", baseline=1268)
    p.ph(90, 1288, 520, 110, ["A number without", "an owner is a wish."], 40,
         INK, family="Georgia", weight="bold", leading=48, baseline=1332)
    p.ph(90, 1406, 520, 28, "OPERATING PRINCIPLE / REVIEW NOTES", 14, MUTED,
         weight="bold", ls="1.4", baseline=1428)
    governance = [
        ("REVIEW CADENCE", "One page, one owner, monthly. No re-baselining between gates."),
        ("GATE RULE", "Targets reset only at a gate, with a written case and a date."),
        ("ESCALATION", "Two consecutive misses trigger a board memo, not a new plan."),
    ]
    for i, (head, body) in enumerate(governance):
        top = 1244 + i * 96
        p.line(640, top, 1150, top, RULE, 1)
        p.ph(640, top + 10, 510, 28, head, 15, RED if i == 2 else NAVY,
             weight="bold", ls="1.6", baseline=top + 32)
        p.para(640, top + 40, 510, 56, body, 19, INK, family="Georgia",
               leading=26)
    p.line(90, 1548, 1150, 1548, RULE, 1)
    p.ph(90, 1558, 1060, 30,
         "NO NUMBER MOVES WITHOUT A GATE DECISION / REVIEWED MONTHLY",
         14, MUTED, weight="bold", ls="1.2", baseline=1582)
    p.footer("Illustrative scorecard · baselines and targets are demonstration data", 14)
    return p


# ---------------------------------------------------------------- page 15
def page_ending():
    p = Page("br-ending", "The decision")
    p.image(0, 0, 1240, 1754, "../images/dunes.jpg")
    p.add('<defs><linearGradient id="end-shade" x1="0" y1="0" x2="0" y2="1">'
          '<stop offset="0" stop-color="#071C2C" stop-opacity="0.78"/>'
          '<stop offset="0.6" stop-color="#071C2C" stop-opacity="0.87"/>'
          '<stop offset="1" stop-color="#071C2C" stop-opacity="0.97"/>'
          '</linearGradient></defs>')
    p.rect(0, 0, 1240, 1754, "url(#end-shade)")
    p.rect(90, 92, 316, 58, RED)
    p.ph(110, 98, 280, 44, "THE DECISION", 22, WHITE, weight="bold", ls="2.4",
         baseline=134)
    p.ph_right(1150, 100, 240, 40, "15 / END", 15, "#C8D5DE", weight="bold",
               ls="1.6", baseline=130, ph_type="slide-number")
    p.line(90, 180, 1150, 180, WHITE, 1, 0.4)
    p.ph(90, 236, 760, 36, "THE BOARD ASK", 18, CYAN, weight="bold", ls="2.8",
         baseline=264)
    p.ph(90, 316, 1040, 350, ["Decide", "by Friday."], 116, WHITE,
         family="Georgia", weight="bold", leading=128, ph_type="title")
    p.ph(90, 700, 880, 130,
         ["Approve the three moves. Name the owners.", "Hold the first gate in thirty days."],
         34, "#D8E2E9", family="Georgia", leading=46, ph_type="subtitle")
    steps = [("FRI 30 OCT", "Board decision"), ("MON 02 NOV", "Owner letters"),
             ("FRI 27 NOV", "Gate 1 review")]
    for i, (date, label) in enumerate(steps):
        x = 90 + i * 360
        p.line(x, 1020, x + 310, 1020, WHITE, 1, 0.5)
        p.ph(x, 1036, 310, 30, date, 16, CYAN, weight="bold", ls="1.8",
             baseline=1060)
        p.ph(x, 1074, 310, 42, label, 26, WHITE, weight="bold", baseline=1108)
    p.line(90, 1520, 1150, 1520, WHITE, 1, 0.35)
    p.ph(90, 1540, 920, 34,
         "BOARDROOM / A4 STRATEGY REVIEW · PREPARED FOR THE BOARD, OCTOBER 2026",
         14, "#C8D5DE", weight="bold", ls="1.2", baseline=1564)
    p.ph(90, 1574, 920, 32,
         "ILLUSTRATIVE EXHIBIT · ALL FIGURES ARE DEMONSTRATION DATA", 13,
         "#9FB1BE", weight="bold", ls="1.0", baseline=1598)
    p.ph_right(1150, 1540, 110, 34, "15", 16, WHITE, weight="bold",
               baseline=1566, ph_type="slide-number")
    return p


PAGES = {
    "01_cover": page_cover,
    "02_argument": page_argument,
    "03_contents": page_contents,
    "04_briefing": page_briefing,
    "05_waterfall": page_waterfall,
    "06_matrix": page_matrix,
    "07_issue_tree": page_issue_tree,
    "08_scenarios": page_scenarios,
    "09_choice": page_choice,
    "10_roadmap": page_roadmap,
    "11_portfolio": page_portfolio,
    "12_essay": page_essay,
    "13_recommendation": page_recommendation,
    "14_scoreboard": page_scoreboard,
    "15_ending": page_ending,
}


if __name__ == "__main__":
    wanted = os.environ.get("PAGES", "").split(",") if os.environ.get("PAGES") else list(PAGES)
    for name in wanted:
        name = name.strip()
        if not name:
            continue
        (OUT / f"{name}.svg").write_text(PAGES[name]().svg(), encoding="utf-8")
        print("wrote", name)
