#!/usr/bin/env python3
"""Boardroom Editorial on the shared a4-editorial Layout.

Writes examples/a4-editorial/<prototype>.svg. Each page is the Layout prototype
restyled with the Boardroom Theme DNA: warm paper, a navy band where a decision
is asked, cyan for the recommended path and red for risk (one accent per
exhibit), Georgia for the claim and argument, Arial tracked capitals for the
evidence apparatus, photography only at the open and close. Every figure is
illustrative demonstration data.

    python3 themes/boardroom/gen_layout_showcase.py [--check]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "framework" / "scripts"))
from layout_showcase import Page, fit_report, text_markup  # noqa: E402

IMG = "../images/"
TOTAL = 8

PAPER, NAVY, CYAN, RED = "#F7F5F0", "#071C2C", "#00A9F4", "#E3120B"
STEEL, INK, MUTED, RULE, ON_NAVY, WHITE = "#8FA3B0", "#12232F", "#5F6E79", "#D5DCE1", "#C8D5DE", "#FFFFFF"
SERIF = "Georgia, 'Times New Roman', serif"
SANS = "Arial, Helvetica, sans-serif"
NOTE = "ILLUSTRATIVE EXHIBIT  ·  ALL FIGURES ARE DEMONSTRATION DATA"


def caps(p, id_, lines, x, y, fill=INK, anchor=None, size=15, lh=1.6, weight="bold"):
    """Arial tracked capitals: the evidence apparatus (never below 15 px)."""
    p.text(id_, lines, x=x, y=y, size=size, fill=fill, family=SANS, weight=weight, ls=2.2, anchor=anchor, lh=lh)


def caps_deco(text, x, y, fill=INK, anchor=None, size=15, lh=1.6):
    return text_markup(text, x=x, y=y, size=size, fill=fill, family=SANS, weight="bold", ls=2.2, anchor=anchor, lh=lh)


def kicker(p, text, y=124, fill=INK):
    p.add(f'<rect x="100" y="{y - 12}" width="11" height="11" fill="{RED}"/>', after="master-bg")
    caps(p, "kicker", text, 122, y, fill)


def footer(p, n, dark=False, note=True):
    fill = ON_NAVY if dark else MUTED
    p.add(f'<line x1="100" y1="1628" x2="1140" y2="1628" stroke="{STEEL if dark else RULE}" stroke-width="1"/>'
          + (caps_deco(NOTE, 100, 1668, fill) if note else ""), after="master-bg")
    caps(p, "folio", f"{n:02d} / {TOTAL:02d}", 1140, 1668, fill, anchor="end")


def cover():
    p = Page("a4-editorial", "01_cover").lang("en").background(PAPER).ground(NAVY)
    p.image("hero", IMG + "ocean.jpg")
    p.add(f'<rect x="0" y="0" width="1240" height="1754" fill="{NAVY}" fill-opacity="0.55"/>', after="hero")
    p.add(f'<rect x="100" y="96" width="262" height="48" fill="{RED}"/>', after="photo-shade")
    p.add(f'<rect x="100" y="1404" width="64" height="4" fill="{CYAN}"/>', after="photo-shade")
    caps(p, "kicker", "STRATEGY / REVIEW", 120, 127, WHITE)
    p.text("title", ["The next advantage", "is operational."], size=96, fill=WHITE, family=SERIF, lh=1.1,
           y=1230)
    p.text("subtitle", ["Growth is no longer the constraint.", "The operating model is."], size=30, fill=WHITE,
           family=SERIF, lh=1.4, y=1466)
    caps(p, "edition", "BOARDROOM EDITION  ·  ISSUE 07  ·  OCTOBER 2026", 100, 1662, ON_NAVY)
    return p


def chapter():
    p = Page("a4-editorial", "02_chapter").lang("en").background(PAPER).ground(NAVY)
    p.image("hero", IMG + "horizon.jpg", opacity="0.16")
    p.style("photo-shade", fill=NAVY, fill_opacity="0.6")
    p.add(f'<rect x="100" y="96" width="140" height="44" fill="{RED}"/>' + caps_deco("PART", 120, 126, WHITE)
          + f'<line x1="100" y1="1160" x2="1140" y2="1160" stroke="{STEEL}" stroke-width="1"/>', after="photo-shade")
    p.text("chapter-number", "02", x=100, y=250, size=150, fill=WHITE, family=SERIF)
    p.text("title", ["Launches slip for one", "structural reason."], size=80, fill=WHITE, family=SERIF,
           lh=1.12, y=1290)
    p.text("description", ["Twenty-three days of delay decompose into three causes.",
                           "Only one of them is fixed by adding people."], size=28, fill=ON_NAVY, family=SERIF,
           lh=1.45, y=1508)
    return p


def evidence():
    p = Page("a4-editorial", "03r_content_evidence").lang("en").background(PAPER)
    p.style("exhibit-rule", stroke=NAVY).style("takeaway-rule", stroke=RULE)
    kicker(p, "BRIEFING  /  THE GAP")
    footer(p, 3)
    p.text("title", ["Orders are up 7.4%.", "Revenue is up 2.1%."], size=64, fill=NAVY, family=SERIF, lh=1.12,
           weight="bold", y=280)
    p.text("lead", ["The difference is not a demand problem. It is", "the cumulative cost of six planning cycles."],
           size=28, fill=INK, family=SERIF, lh=1.4, y=500)
    p.text("context", ["Index, 2022 = 100.", "The lines part in 2024", "and have not met since."],
           size=21, fill=MUTED, family=SERIF, lh=1.45, y=490)
    # Native line chart: transparent plot, hairline grid, direct labels, one accent.
    x0, x1, yb, yt, lo, hi = 170, 740, 1180, 780, 95, 130
    xs = [x0 + i * (x1 - x0) / 4 for i in range(5)]
    def ypos(v):
        return round(yb - (v - lo) / (hi - lo) * (yb - yt), 1)
    orders, revenue = [100, 104, 111, 119, 127], [100, 101.4, 103.1, 105.6, 108]
    grid = "".join(f'<line x1="{x0}" y1="{ypos(v)}" x2="{x1}" y2="{ypos(v)}" stroke="{RULE}" stroke-width="1"/>'
                   + text_markup(str(v), x=x0 - 14, y=ypos(v) + 5, size=15, fill=MUTED, family=SANS, anchor="end")
                   for v in (100, 110, 120, 130))
    years = "".join(text_markup(str(2022 + i), x=round(x), y=1214, size=15, fill=MUTED, family=SANS, anchor="middle")
                    for i, x in enumerate(xs))
    def series(vals, colour, width):
        pts = " ".join(f"{round(x)},{ypos(v)}" for x, v in zip(xs, vals))
        dots = "".join(f'<circle cx="{round(x)}" cy="{ypos(v)}" r="5" fill="{colour}"/>' for x, v in zip(xs, vals))
        return f'<polyline points="{pts}" fill="none" stroke="{colour}" stroke-width="{width}"/>' + dots
    chart = (grid + f'<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="{INK}" stroke-width="1.5"/>' + years
             + series(revenue, STEEL, 3) + series(orders, CYAN, 4)
             + caps_deco("ORDER INTAKE  127", x1, ypos(127) - 16, CYAN, anchor="end")
             + caps_deco("REVENUE  108", x1, ypos(108) + 32, MUTED, anchor="end")
             + caps_deco("INDEX, 2022 = 100", 100, 730, MUTED))
    p.proxy("exhibit", chart)
    p.text("annotation", ["What changed", "", "The order book has", "grown faster than the", "organisation's ability",
                          "to convert it. Price is", "stable; the lag is", "widening; no single", "owner holds the gate",
                          "sequence end to end."], size=22, fill=INK, family=SERIF, lh=1.45, y=728)
    caps(p, "source", "SOURCE: ILLUSTRATIVE OPERATING REVIEW  ·  INDEX AND COUNTS ARE DEMONSTRATION DATA",
         100, 1316, MUTED)
    p.text("takeaway", ["Half the gap is decision speed, not price."], size=40, fill=NAVY, family=SERIF, y=1506)
    return p


def comparison():
    p = Page("a4-editorial", "03s_content_comparison").lang("en").background(PAPER)
    p.style("header-rule", stroke=NAVY)
    for i in ("row-rule-1", "row-rule-2", "row-rule-3"):
        p.style(i, stroke=RULE)
    p.add(f'<rect x="620" y="500" width="520" height="980" fill="{CYAN}" fill-opacity="0.07"/>', after="master-bg")
    kicker(p, "THE CHOICE  /  OPERATING MODEL")
    footer(p, 4)
    rows = [(682, "DECISION SPEED"), (972, "COST TO SERVE"), (1242, "EXECUTION RISK")]
    p.add("".join(caps_deco(t, 100, y, MUTED) for y, t in rows), after="row-rule-3")
    p.text("title", ["Federate the decisions.", "Keep one owner."], size=64, fill=NAVY, family=SERIF, lh=1.12,
           weight="bold", y=280)
    p.text("label-left", "Today: central", size=38, fill=INK, family=SERIF, y=590)
    p.text("label-right", "Proposed: federated", size=38, fill=CYAN, family=SERIF, y=590)
    p.text("left-1", ["Six weeks from proposal", "to decision; every launch", "queues at the same desk."],
           size=24, fill=INK, family=SERIF, lh=1.45, y=744)
    p.text("right-1", ["Two weeks. Business lines", "decide inside guardrails", "the board sets once a year."],
           size=24, fill=INK, family=SERIF, lh=1.45, y=744)
    p.text("left-2", ["Low on paper; the delay", "cost does not appear in", "any budget line."],
           size=24, fill=INK, family=SERIF, lh=1.45, y=1030)
    p.text("right-2", ["Medium. A shared platform", "funded by two portfolio", "exits, not by headcount."],
           size=24, fill=INK, family=SERIF, lh=1.45, y=1030)
    p.text("left-3", ["Drift. No owner can say", "which gate a launch", "is waiting at."],
           size=24, fill=INK, family=SERIF, lh=1.45, y=1300)
    p.text("right-3", ["Contained. One accountable", "owner per launch, one", "cadence for all."],
           size=24, fill=INK, family=SERIF, lh=1.45, y=1300)
    caps(p, "source", "TINTED COLUMN = RECOMMENDED  ·  ASSESSMENT IS ILLUSTRATIVE", 100, 1556, MUTED)
    return p


def table():
    p = Page("a4-editorial", "03h_content_table").lang("en").background(PAPER)
    kicker(p, "SCENARIOS  /  2027")
    footer(p, 5)
    p.text("title", "Three futures; one is affordable.", size=54, fill=NAVY, family=SERIF, weight="bold", y=280)
    p.text("lead", ["Each scenario holds a different demand, price and cost path.",
                    "Only one funds the plan and clears the covenant."], size=28, fill=MUTED, family=SERIF,
           lh=1.4, y=468)
    cols = [(100, None, "MEASURE"), (700, "end", "BASE"), (920, "end", "ACCELERATE"), (1140, "end", "STRESS")]
    rows = [("Demand growth", "+2.1%", "+4.0%", "−1.5%"), ("Price", "Flat", "+1.0%", "−2.0%"),
            ("2027 operating margin", "21.0%", "22.8%", "17.9%"), ("Free cash flow", "0.9bn", "1.4bn", "0.3bn"),
            ("Headcount", "Flat", "−4%", "−9%")]
    t = (f'<rect x="760" y="612" width="190" height="638" fill="{CYAN}" fill-opacity="0.08"/>'
         f'<line x1="100" y1="612" x2="1140" y2="612" stroke="{NAVY}" stroke-width="3"/>')
    t += "".join(caps_deco(h, x, 664, CYAN if h == "ACCELERATE" else MUTED, anchor=a) for x, a, h in cols)
    t += f'<line x1="100" y1="690" x2="1140" y2="690" stroke="{NAVY}" stroke-width="1.5"/>'
    for i, r in enumerate(rows):
        y = 690 + 112 * i
        t += text_markup(r[0], x=100, y=y + 68, size=22, fill=INK, family=SANS)
        for (x, a, h), v in zip(cols[1:], r[1:]):
            colour = RED if v.startswith("−") and h == "STRESS" else NAVY if h == "ACCELERATE" else INK
            t += text_markup(v, x=x, y=y + 68, size=24, fill=colour, family=SANS,
                             weight="bold" if h == "ACCELERATE" else None, anchor="end")
        t += f'<line x1="100" y1="{y + 112}" x2="1140" y2="{y + 112}" stroke="{RULE}" stroke-width="1"/>'
    t += f'<line x1="100" y1="1250" x2="1140" y2="1250" stroke="{NAVY}" stroke-width="1.5"/>'
    p.proxy("information", t)
    caps(p, "source", "COVENANT: 22.0% OPERATING MARGIN  ·  VALUES ARE DEMONSTRATION DATA", 100, 1316, MUTED)
    p.text("takeaway", ["Accelerate is the only path that clears 22.0%", "without cutting into the core."],
           size=36, fill=NAVY, family=SERIF, lh=1.3, y=1476)
    return p


def chronology():
    p = Page("a4-editorial", "03t_content_chronology").lang("en").background(PAPER)
    p.style("time-rule-1", stroke=NAVY).style("time-rule-4", stroke=NAVY)
    p.style("time-rule-2", stroke=RULE).style("time-rule-3", stroke=RULE)
    kicker(p, "THE PLAN  /  FIRST NINETY DAYS")
    footer(p, 6, note=False)
    gates = "".join(f'<path d="M 440 {y - 9} L 449 {y} L 440 {y + 9} L 431 {y} Z" fill="{RED}"/>'
                    for y in (830, 1190, 1550))
    p.add(gates, after="time-rule-4")
    p.text("title", ["Ninety days, three gates."], size=64, fill=NAVY, family=SERIF, weight="bold", y=290)
    for i, (when, gate) in enumerate([("Weeks 1–3", "GATE 1  ·  FRI 20 NOV"),
                                      ("Weeks 4–8", "GATE 2  ·  FRI 18 DEC"),
                                      ("Weeks 9–12", "GATE 3  ·  FRI 22 JAN")]):
        y0 = 530 + 360 * i
        p.text(f"time-{i + 1}", when, size=44, fill=NAVY, family=SERIF, y=y0 + 70)
        p.add(caps_deco(gate, 100, y0 + 124, RED), after="time-rule-4")
    events = [["Simplify the portfolio", "Cut two product lines and publish kill criteria", "before the next budget cycle. Owner: CEO / CFO."],
              ["Rebuild decision rights", "One launch owner, two decision gates and three", "planning cycles instead of six. Owner: COO."],
              ["Reset the operating rhythm", "Quarterly gates, monthly review, weekly delivery", "cell with the same metrics. Owner: COO / CHRO."]]
    for i, ev in enumerate(events):
        y0 = 530 + 360 * i
        p.text(f"event-{i + 1}", ev, size=24, fill=INK, family=SERIF, lh=1.5, y=y0 + 40)
    caps(p, "source", "NO WORKSTREAM STARTS WITHOUT A NAMED OWNER  ·  ILLUSTRATIVE", 100, 1668, MUTED)
    return p


def pillars():
    p = Page("a4-editorial", "03z_content_pillars").lang("en").background(PAPER)
    p.style("field", fill=NAVY)
    for i in ("pillar-1", "pillar-2", "pillar-3", "pillar-4"):
        p.style(i, fill=PAPER, fill_opacity="0.97")
    for i in ("numeral-vec-1", "numeral-vec-2", "numeral-vec-3", "numeral-vec-4"):
        p.style(i, fill=NAVY)
    p.style("pillar-echo-2", fill=CYAN, fill_opacity="0.22")
    caps(p, "kicker", "THE TEST  /  FOUR NUMBERS", 100, 130, WHITE)
    p.text("lead", ["Four numbers the board", "will watch, each with a", "baseline, a target and", "one owner."],
           size=28, fill=ON_NAVY, family=SERIF, lh=1.4, y=226)
    steps = [("step-1", 120, 1140, ["MARGIN", "18.6% → 22.8%", "OWNER: CFO"]),
             ("step-2", 390, 700, ["LAUNCH CYCLE", "23 → 9 DAYS", "OWNER: COO"]),
             ("step-3", 660, 1240, ["DECISION GATES", "14 → 4", "OWNER: COO"]),
             ("step-4", 930, 280, ["ON-TIME DELIVERY", "78% → 94%", "OWNER: BU LEADS"])]
    for id_, x, y, lines in steps:
        p.text(id_, lines, x=x, y=y, size=16, fill=NAVY, family=SANS, weight="bold", ls=1.2, lh=1.55)
    p.text("body-left", ["Read left to right:", "margin moves first,", "delivery follows", "once gates are cut."],
           size=20, fill=WHITE, family=SERIF, lh=1.45, y=1398)
    p.text("body-right", ["A number without", "an owner is a wish.", "", "Review cadence: one", "page, one owner,",
                          "monthly. No", "re-baselining", "between gates; two", "consecutive misses", "trigger a board", "memo."],
           size=20, fill=ON_NAVY, family=SERIF, lh=1.45, y=1036)
    caps(p, "folio", f"07 / {TOTAL:02d}", 1140, 1668, ON_NAVY, anchor="end")
    return p


def ending():
    p = Page("a4-editorial", "04_ending").lang("en").background(PAPER)
    p.image("hero", IMG + "dunes.jpg")
    p.add(f'<rect x="0" y="0" width="1240" height="900" fill="{NAVY}" fill-opacity="0.45"/>'
          f'<rect x="100" y="96" width="200" height="48" fill="{RED}"/>' + caps_deco("THE DECISION", 120, 127, WHITE),
          after="hero")
    p.style("closing-rule", stroke=RULE)
    footer(p, 8)
    p.text("title", "Decide by Friday.", size=88, fill=NAVY, family=SERIF, weight="bold", y=1100)
    p.text("subtitle", "Approve the three moves. Name the owners. Hold the first gate in thirty days.",
           size=26, fill=MUTED, family=SERIF, y=1300)
    caps(p, "contact", ["FRI 30 OCT  ·  BOARD DECISION", "MON 02 NOV  ·  OWNER LETTERS", "FRI 20 NOV  ·  GATE 1 REVIEW"],
         100, 1494, NAVY, lh=1.75)
    p.text("closing", ["The ask: 0.4bn and three owners,", "decided in one meeting."], size=26, fill=NAVY,
           family=SERIF, lh=1.4, y=1500)
    return p


PAGES = [cover, chapter, evidence, comparison, table, chronology, pillars, ending]

# --- 16:9 (ppt169-editorial) ---------------------------------------------------
W169 = "ppt169-editorial"
TOTAL_169 = 8


def caps169(p, id_, lines, x, y, fill=INK, anchor=None, lh=1.6, weight="bold"):
    p.text(id_, lines, x=x, y=y, size=14, fill=fill, family=SANS, weight=weight, ls=2, anchor=anchor, lh=lh)


def caps169_deco(text, x, y, fill=INK, anchor=None):
    return text_markup(text, x=x, y=y, size=14, fill=fill, family=SANS, weight="bold", ls=2, anchor=anchor)


def kicker169(p, text, fill=INK):
    p.add(f'<rect x="80" y="61" width="10" height="10" fill="{RED}"/>', after="master-bg")
    caps169(p, "kicker", text, 100, 72, fill)


def foot169(p, n, note=NOTE, dark=False):
    fill = ON_NAVY if dark else MUTED
    caps169(p, "source", note, 80, 668, fill, weight=None)
    caps169(p, "folio", f"{n:02d} / {TOTAL_169:02d}", 1200, 676, fill, anchor="end")


def cover_169():
    p = Page(W169, "01_cover").lang("en").background(PAPER).ground(NAVY)
    p.image("hero", IMG + "ocean.jpg")
    p.add(f'<rect width="1280" height="720" fill="{NAVY}" fill-opacity="0.55"/>', after="hero")
    p.add(f'<rect x="80" y="50" width="232" height="34" fill="{RED}"/>'
          f'<rect x="80" y="572" width="56" height="4" fill="{CYAN}"/>', after="photo-shade")
    caps169(p, "kicker", "STRATEGY / REVIEW", 96, 72, WHITE)
    p.text("title", ["The next advantage", "is operational."], size=60, fill=WHITE, family=SERIF, lh=1.12, y=476)
    p.text("subtitle", "Growth is no longer the constraint. The operating model is.", size=22, fill=WHITE,
           family=SERIF, y=616)
    caps169(p, "edition", "BOARDROOM EDITION  ·  ISSUE 07  ·  OCTOBER 2026", 80, 678, ON_NAVY)
    return p


def statement_169():
    p = Page(W169, "03a_content_statement").lang("en").background(PAPER)
    for i in ("top-rule", "tick-1", "tick-2", "tick-3", "tick-4", "short-rule"):
        p.style(i, stroke=NAVY)
    kicker169(p, "THE ARGUMENT  /  IN ONE PAGE")
    p.text("title", ["Growth is no longer", "the constraint."], size=80, fill=NAVY, family=SERIF, weight="bold",
           lh=1.08, ls=-1, y=220)
    p.text("lead", ["Execution is. The gap between demand", "and revenue now sits inside the", "operating model."],
           size=22, fill=NAVY, family=SERIF, weight="bold", lh=1.35, y=528)
    p.text("main-copy", ["Order intake is healthy. What has changed is", "the cost of choosing, staffing and shipping:",
                         "six planning cycles, fourteen gates and no", "single owner of a launch."],
           size=18, fill=INK, family=SERIF, lh=1.45, y=522)
    caps169(p, "folio", f"02 / {TOTAL_169:02d}", 1200, 676, MUTED, anchor="end")
    return p


def evidence_169():
    p = Page(W169, "03c_content_evidence").lang("en").background(PAPER)
    p.style("exhibit-rule", stroke=NAVY).style("foot-rule", stroke=RULE)
    kicker169(p, "BRIEFING  /  THE GAP")
    p.text("title", "Orders are up 7.4%. Revenue is up 2.1%.", size=40, fill=NAVY, family=SERIF, weight="bold", y=158)
    p.text("lead", "The difference is the cost of six planning cycles, not demand.", size=20, fill=INK, family=SERIF,
           y=246)
    p.text("context", ["Index, 2022 = 100.", "Illustrative data."], size=16, fill=MUTED, family=SERIF, lh=1.4, y=238)
    x0, x1, yb, yt, lo, hi = 140, 760, 580, 340, 95, 130
    xs = [x0 + i * (x1 - x0) / 4 for i in range(5)]
    def ypos(v):
        return round(yb - (v - lo) / (hi - lo) * (yb - yt), 1)
    orders, revenue = [100, 104, 111, 119, 127], [100, 101.4, 103.1, 105.6, 108]
    grid = "".join(f'<line x1="{x0}" y1="{ypos(v)}" x2="{x1}" y2="{ypos(v)}" stroke="{RULE}" stroke-width="1"/>'
                   + text_markup(str(v), x=x0 - 12, y=ypos(v) + 5, size=14, fill=MUTED, family=SANS, anchor="end")
                   for v in (100, 110, 120, 130))
    years = "".join(text_markup(str(2022 + i), x=round(x), y=604, size=14, fill=MUTED, family=SANS, anchor="middle")
                    for i, x in enumerate(xs))
    def series(vals, colour, width):
        pts = " ".join(f"{round(x)},{ypos(v)}" for x, v in zip(xs, vals))
        return (f'<polyline points="{pts}" fill="none" stroke="{colour}" stroke-width="{width}"/>'
                + "".join(f'<circle cx="{round(x)}" cy="{ypos(v)}" r="4" fill="{colour}"/>' for x, v in zip(xs, vals)))
    p.proxy("exhibit", grid + f'<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="{INK}" stroke-width="1.5"/>'
            + years + series(revenue, STEEL, 3) + series(orders, CYAN, 4)
            + caps169_deco("ORDER INTAKE 127", x1, ypos(127) - 14, CYAN, anchor="end")
            + caps169_deco("REVENUE 108", x1, ypos(108) + 28, MUTED, anchor="end"))
    p.text("annotation", ["What changed", "", "The order book grew", "faster than the ability", "to convert it. Price is",
                          "stable; no single owner", "holds the gate sequence."], size=18, fill=INK, family=SERIF,
           lh=1.45, y=332)
    foot169(p, 3)
    return p


def comparison_169():
    p = Page(W169, "03d_content_comparison").lang("en").background(PAPER)
    p.style("header-rule", stroke=NAVY)
    for i in (1, 2, 3):
        p.style(f"row-rule-{i}", stroke=RULE)
    p.add(f'<rect x="640" y="220" width="560" height="408" fill="{CYAN}" fill-opacity="0.07"/>', after="row-rule-3")
    kicker169(p, "THE CHOICE  /  OPERATING MODEL")
    p.text("title", "Federate the decisions. Keep one owner.", size=40, fill=NAVY, family=SERIF, weight="bold", y=158)
    p.text("label-left", "Today: central", size=26, fill=INK, family=SERIF, y=266)
    p.text("label-right", "Proposed: federated", size=26, fill=CYAN, family=SERIF, y=266)
    cells = [("Six weeks from proposal to decision;", "every launch queues at one desk."),
             ("Two weeks. Business lines decide", "inside guardrails set once a year."),
             ("Low on paper; the delay cost", "appears in no budget line."),
             ("Medium. A shared platform funded", "by two portfolio exits."),
             ("Drift. No owner can say which", "gate a launch is waiting at."),
             ("Contained. One owner per launch,", "one cadence for all.")]
    for i, ys in enumerate((330, 446, 558)):
        p.text(f"left-{i + 1}", list(cells[2 * i]), size=18, fill=INK, family=SERIF, lh=1.45, y=ys)
        p.text(f"right-{i + 1}", list(cells[2 * i + 1]), size=18, fill=INK, family=SERIF, lh=1.45, y=ys)
    foot169(p, 4, "TINTED COLUMN = RECOMMENDED  ·  ASSESSMENT IS ILLUSTRATIVE")
    return p


def table_169():
    p = Page(W169, "03e_content_table").lang("en").background(PAPER)
    kicker169(p, "SCENARIOS  /  2027")
    p.text("title", "Three futures; one is affordable.", size=40, fill=NAVY, family=SERIF, weight="bold", y=158)
    p.text("lead", "Only Accelerate funds the plan and clears the 22.0% covenant.", size=20, fill=MUTED,
           family=SERIF, y=242)
    cols = [(80, None, "MEASURE"), (720, "end", "BASE"), (960, "end", "ACCELERATE"), (1200, "end", "STRESS")]
    rows = [("Demand growth", "+2.1%", "+4.0%", "−1.5%"), ("Price", "Flat", "+1.0%", "−2.0%"),
            ("2027 operating margin", "21.0%", "22.8%", "17.9%"), ("Free cash flow", "0.9bn", "1.4bn", "0.3bn"),
            ("Headcount", "Flat", "−4%", "−9%")]
    t = (f'<rect x="800" y="282" width="176" height="328" fill="{CYAN}" fill-opacity="0.08"/>'
         f'<line x1="80" y1="282" x2="1200" y2="282" stroke="{NAVY}" stroke-width="3"/>')
    t += "".join(caps169_deco(h, x, 316, CYAN if h == "ACCELERATE" else MUTED, anchor=a) for x, a, h in cols)
    t += f'<line x1="80" y1="332" x2="1200" y2="332" stroke="{NAVY}" stroke-width="1.5"/>'
    for i, r in enumerate(rows):
        y = 332 + 55 * i
        t += text_markup(r[0], x=80, y=y + 35, size=18, fill=INK, family=SANS)
        for (x, a, h), v in zip(cols[1:], r[1:]):
            colour = RED if v.startswith("−") and h == "STRESS" else NAVY if h == "ACCELERATE" else INK
            t += text_markup(v, x=x if h != "ACCELERATE" else 960, y=y + 35, size=18, fill=colour, family=SANS,
                             weight="bold" if h == "ACCELERATE" else None, anchor="end")
        t += f'<line x1="80" y1="{y + 55}" x2="1200" y2="{y + 55}" stroke="{RULE}" stroke-width="1"/>'
    p.proxy("information", t)
    foot169(p, 5, "COVENANT: 22.0% OPERATING MARGIN  ·  VALUES ARE DEMONSTRATION DATA")
    return p


def metrics_169():
    p = Page(W169, "03j_content_metrics").lang("en").background(PAPER)
    p.style("specimen-rule", stroke=NAVY).style("foot-rule", stroke=RULE)
    for i in range(1, 6):
        p.style(f"specimen-tick-{i}", stroke=NAVY)
    kicker169(p, "THE TEST  /  FOUR NUMBERS")
    p.text("title", "Four numbers the board will watch.", size=40, fill=NAVY, family=SERIF, weight="bold", y=158)
    p.text("lead", "Each has a baseline, a ninety-day checkpoint and one owner.", size=20, fill=MUTED, family=SERIF,
           y=244)
    for i, (val, lab, col) in enumerate([("18.6%", ["MARGIN, FY24", "TARGET 22.8%  ·  CFO"], NAVY),
                                         ("23", ["DAYS ADDED PER LAUNCH", "TARGET 9  ·  COO"], RED),
                                         ("14", ["APPROVAL GATES", "TARGET 4  ·  COO"], NAVY),
                                         ("78%", ["ON-TIME DELIVERY", "TARGET 94%  ·  BU LEADS"], NAVY)]):
        p.text(f"metric-{i + 1}", val, size=80, fill=col, family=SERIF, y=414)
        caps169(p, f"metric-label-{i + 1}", lab, [80, 368, 656, 944][i], 480, MUTED, lh=1.7)
    foot169(p, 6)
    return p


def pillars_169():
    p = Page(W169, "03m_content_pillars").lang("en").background(PAPER)
    p.style("field", fill=NAVY)
    for i in range(1, 5):
        p.style(f"pillar-{i}", fill=PAPER, fill_opacity="0.97")
    p.style("pillar-echo-2", fill=CYAN, fill_opacity="0.22")
    caps169(p, "kicker", "THE PLAN  /  THREE MOVES AND A GATE", 80, 72, WHITE)
    p.text("lead", ["Three moves, in this", "order, then one gate", "the board can check."], size=18, fill=ON_NAVY,
           family=SERIF, lh=1.45, y=126)
    for i, (x, y, lines) in enumerate([(80, 430, ["01  SIMPLIFY", "CUT TWO LINES", "OWNER: CEO / CFO"]),
                                       (368, 200, ["02  DECISION RIGHTS", "ONE LAUNCH OWNER", "OWNER: COO"]),
                                       (656, 480, ["03  RHYTHM", "ONE CADENCE", "OWNER: COO / CHRO"]),
                                       (944, 110, ["GATE 1", "FRI 20 NOV", "BOARD REVIEW"])]):
        p.text(f"step-{i + 1}", lines, x=x + 20, y=y + 46, size=15, fill=NAVY, family=SANS, weight="bold", ls=1,
               lh=1.55)
    p.text("body-left", ["Read left to right:", "the order of the moves."], size=16, fill=WHITE, family=SERIF, lh=1.4, y=640)
    p.text("body-right", ["No workstream starts", "without a named owner;", "two missed checkpoints", "trigger a board memo."],
           size=16, fill=ON_NAVY, family=SERIF, lh=1.45, y=514)
    caps169(p, "folio", f"07 / {TOTAL_169:02d}", 1200, 676, ON_NAVY, anchor="end")
    return p


def ending_169():
    p = Page(W169, "04_ending").lang("en").background(PAPER)
    p.image("hero", IMG + "dunes.jpg")
    p.add(f'<rect width="1280" height="400" fill="{NAVY}" fill-opacity="0.45"/>'
          f'<rect x="80" y="50" width="190" height="34" fill="{RED}"/>' + caps169_deco("THE DECISION", 96, 72, WHITE),
          after="hero")
    p.style("closing-rule", stroke=RULE)
    p.text("title", "Decide by Friday.", size=56, fill=NAVY, family=SERIF, weight="bold", y=490)
    p.text("subtitle", "Approve the three moves. Name the owners. Hold the first gate in thirty days.", size=20,
           fill=MUTED, family=SERIF, y=552)
    caps169(p, "contact", ["FRI 30 OCT  ·  BOARD DECISION", "FRI 20 NOV  ·  GATE 1 REVIEW"], 80, 610, NAVY)
    p.text("closing", ["The ask: 0.4bn and three owners,", "decided in one meeting."], size=18, fill=NAVY,
           family=SERIF, lh=1.4, y=610)
    caps169(p, "folio", f"08 / {TOTAL_169:02d}", 1200, 676, MUTED, anchor="end")
    return p


PAGES_169 = [cover_169, statement_169, evidence_169, comparison_169, table_169, metrics_169, pillars_169, ending_169]


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
