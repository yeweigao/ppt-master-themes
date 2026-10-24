#!/usr/bin/env python3
"""Objective design-discipline metrics for one or more decks of SVG pages.

    python3 evals/svg_metrics.py A=/path/to/plain/svg_output B=/path/to/themed/svg_output
    python3 evals/svg_metrics.py themes/natgeo/examples/svg --json

Each argument is a directory of page SVGs, optionally prefixed with a label. The
numbers are evidence for the rubric, not a verdict: a lower count is not always
better (a theme may declare gradients or italics on purpose). Standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

NUM = re.compile(r"-?\d+(?:\.\d+)?")
MONO = ("mono", "courier", "consolas", "menlo")


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def style_map(el) -> dict:
    out = {}
    for part in (el.get("style") or "").split(";"):
        k, sep, v = part.partition(":")
        if sep:
            out[k.strip()] = v.strip()
    return out


def attr(el, name, inherited):
    v = style_map(el).get(name) or el.get(name)
    return v if v is not None else inherited.get(name)


def weight(v) -> int:
    if v is None:
        return 400
    v = str(v).strip().lower()
    return {"normal": 400, "bold": 700, "bolder": 800, "lighter": 300}.get(v, int(float(v)) if NUM.fullmatch(v) else 400)


def first_family(v) -> str | None:
    if not v:
        return None
    return v.split(",")[0].strip().strip("'\"").lower()


def page_metrics(svg: Path) -> dict:
    root = ET.parse(svg).getroot()
    vb = [float(x) for x in NUM.findall(root.get("viewBox") or "0 0 1280 720")][:4]
    w, h = (vb[2], vb[3]) if len(vb) == 4 else (1280, 720)
    floor = 14 if h > w * 1.2 else 12
    m = {"sizes": [], "pairs": [], "families": set(), "below_floor": 0, "italic": 0, "mono": 0,
         "rounded": 0, "pills": 0, "filters": 0, "gradients": 0, "fills": set(), "text_runs": 0}

    def walk(el, inh):
        tag = local(el.tag)
        cur = dict(inh)
        for k in ("font-size", "font-weight", "font-family", "font-style"):
            v = attr(el, k, {})
            if v is not None:
                cur[k] = v
        if tag in ("filter",):
            m["filters"] += 1
        if tag in ("linearGradient", "radialGradient"):
            m["gradients"] += 1
        if tag == "rect":
            rx = float(NUM.findall(el.get("rx") or el.get("ry") or "0")[0] or 0) if (el.get("rx") or el.get("ry")) else 0
            rh = float((NUM.findall(el.get("height") or "0") or ["0"])[0])
            if rx > 0:
                m["rounded"] += 1
                if rh and rx >= rh / 2 - 0.5:
                    m["pills"] += 1
        fill = attr(el, "fill", {})
        if fill and fill.startswith("#"):
            m["fills"].add(fill.upper()[:7])
        if tag in ("text", "tspan") and (el.text or "").strip():
            m["text_runs"] += 1
            fs = cur.get("font-size")
            if fs and NUM.search(str(fs)):
                size = float(NUM.search(str(fs)).group())
                m["sizes"].append(size)
                m["pairs"].append((round(size), weight(cur.get("font-weight"))))
                if size < floor:
                    m["below_floor"] += 1
            fam = first_family(cur.get("font-family"))
            if fam:
                m["families"].add(fam)
                if any(k in fam for k in MONO):
                    m["mono"] += 1
            if str(cur.get("font-style", "")).lower() == "italic":
                m["italic"] += 1
        for child in el:
            walk(child, cur)

    walk(root, {})
    m["floor"] = floor
    return m


def deck_metrics(folder: Path) -> dict:
    pages = sorted(folder.glob("*.svg"))
    if not pages:
        sys.exit(f"no .svg files in {folder}")
    agg = defaultdict(int)
    sizes, families, fills = [], set(), set()
    weights_by_size = defaultdict(set)
    per_page_fills = []
    for p in pages:
        m = page_metrics(p)
        for k in ("below_floor", "italic", "mono", "rounded", "pills", "filters", "gradients", "text_runs"):
            agg[k] += m[k]
        sizes += m["sizes"]
        families |= m["families"]
        fills |= m["fills"]
        per_page_fills.append(len(m["fills"]))
        for s, wgt in m["pairs"]:
            weights_by_size[s].add(wgt)
    distinct = sorted(set(round(s) for s in sizes))
    mixed = sorted(s for s, ws in weights_by_size.items() if len(ws) > 1)
    return {
        "pages": len(pages),
        "min_font": min(sizes) if sizes else None,
        "text_below_floor": agg["below_floor"],
        "distinct_font_sizes": len(distinct),
        "size_ratio_max_min": round(max(sizes) / min(sizes), 1) if sizes else None,
        "font_families": len(families),
        "families": sorted(families),
        "sizes_with_mixed_weights": len(mixed),
        "mixed_weight_sizes": mixed[:12],
        "italic_runs": agg["italic"],
        "monospace_runs": agg["mono"],
        "rounded_rects": agg["rounded"],
        "pill_shapes": agg["pills"],
        "filters_(shadow/blur)": agg["filters"],
        "gradients": agg["gradients"],
        "distinct_fill_colors": len(fills),
        "max_fill_colors_on_a_page": max(per_page_fills),
    }


ROWS = [
    ("pages", "pages"),
    ("min_font", "smallest text (px)"),
    ("text_below_floor", "text runs below floor (A4 14 / 16:9 12)"),
    ("distinct_font_sizes", "distinct font sizes (ladder discipline)"),
    ("size_ratio_max_min", "largest / smallest size (scale contrast)"),
    ("font_families", "font families"),
    ("sizes_with_mixed_weights", "sizes set in >1 weight (W(S) conflicts)"),
    ("italic_runs", "italic text runs"),
    ("monospace_runs", "monospace text runs"),
    ("rounded_rects", "rounded rectangles"),
    ("pill_shapes", "pill shapes"),
    ("filters_(shadow/blur)", "filters (shadow / blur)"),
    ("gradients", "gradients"),
    ("distinct_fill_colors", "distinct fill colours (deck)"),
    ("max_fill_colors_on_a_page", "max fill colours on one page"),
]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("decks", nargs="+", help="[LABEL=]directory of page SVGs")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    results = {}
    for spec in args.decks:
        label, sep, path = spec.partition("=")
        if not sep:
            label, path = Path(spec).name or spec, spec
        results[label] = deck_metrics(Path(path))
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return
    labels = list(results)
    print("| metric | " + " | ".join(labels) + " |")
    print("|---|" + "---|" * len(labels))
    for key, name in ROWS:
        print(f"| {name} | " + " | ".join(str(results[l][key]) for l in labels) + " |")
    for l in labels:
        print(f"\n{l} families: {', '.join(results[l]['families'])}")


if __name__ == "__main__":
    main()
