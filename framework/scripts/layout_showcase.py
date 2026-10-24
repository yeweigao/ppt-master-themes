#!/usr/bin/env python3
"""Build a theme's showcase pages on top of a shared Layout's prototypes.

A showcase page *is* the Layout prototype: the root <svg> keeps the Layout's
data-pptx-master / data-pptx-layout, every placeholder group keeps its id, idx
and bounds, and layout-layer elements stay in place. The theme only restyles
them, fills placeholders with real copy and images, and adds decoration
elements (data-pptx-role="decoration"). That is what lets scripts/list_themes.py
report the page as a showcased prototype and lets an agent calibrate on it.

Used by themes/<id>/gen_layout_showcase.py. Standard library only; the optional
fit check uses Pillow and fontconfig (fc-match) when they are available.
"""
from __future__ import annotations

import copy
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)
Q = "{%s}" % SVG_NS
ROOT = Path(__file__).resolve().parents[2]
LAYOUTS = ROOT / "layouts"


def _q(tag: str) -> str:
    return Q + tag


def fragment(markup: str) -> list[ET.Element]:
    """Parse SVG markup (one or more elements) into elements in the SVG namespace."""
    wrapper = ET.fromstring(f'<svg xmlns="{SVG_NS}">{markup}</svg>')
    return list(wrapper)


def text_markup(lines, *, x, y, size, fill, family, weight=None, ls=None, lh=1.2,
                anchor=None, italic=False, opacity=None, carrier=False, extra="") -> str:
    """One <text> with explicit line breaks (a list of strings, or one string)."""
    if isinstance(lines, str):
        lines = [lines]
    lines = [line if line.strip() else "\u00a0" for line in lines]  # keep blank lines
    attrs = [f'x="{x}"', f'y="{y}"', f'fill="{fill}"', f'font-size="{size}"',
             f'font-family="{escape(family, {chr(34): "&quot;"})}"']
    if carrier:
        attrs.insert(0, 'data-pptx-carrier="true"')
    if weight:
        attrs.append(f'font-weight="{weight}"')
    if ls is not None:
        attrs.append(f'letter-spacing="{ls}"')
    if anchor:
        attrs.append(f'text-anchor="{anchor}"')
    if italic:
        attrs.append('font-style="italic"')
    if opacity is not None:
        attrs.append(f'fill-opacity="{opacity}"')
    if extra:
        attrs.append(extra)
    step = round(size * lh, 2)
    body = escape(lines[0])
    for line in lines[1:]:
        body += f'<tspan x="{x}" dy="{step}">{escape(line)}</tspan>'
    return f'<text {" ".join(attrs)}>{body}</text>'


class Page:
    def __init__(self, layout: str, prototype: str):
        self.layout = layout
        self.prototype = prototype
        src = LAYOUTS / layout / "workspace" / "templates" / f"{prototype}.svg"
        self.tree = ET.parse(src)
        self.root = self.tree.getroot()
        vb = [float(v) for v in self.root.get("viewBox", "0 0 1240 1754").split()]
        self.w, self.h = vb[2], vb[3]
        self.floor = 14 if self.h > self.w else 12  # A4 print floor / 16:9 projection floor
        self.texts: list[dict] = []  # for the fit check
        self._cursor: dict = {}  # anchor id -> last element inserted after it (keeps call order)
        self._deco = 0
        self.decor_texts: list[dict] = []

    # -- lookup -------------------------------------------------------------
    def el(self, id_: str) -> ET.Element:
        for e in self.root.iter():
            if e.get("id") == id_:
                return e
        raise KeyError(f"{self.prototype}: no element with id={id_!r}")

    def _parent(self, child: ET.Element) -> ET.Element:
        for p in self.root.iter():
            if child in list(p):
                return p
        raise KeyError("parent not found")

    # -- styling ------------------------------------------------------------
    def lang(self, code: str) -> "Page":
        self.root.set("lang", code)
        return self

    def background(self, fill: str) -> "Page":
        """The Master background. It must be identical on every page of a deck (ppt-master
        rejects a Master element that differs across slides), so call it with the theme's
        one base ground and use ground() for a page-specific field."""
        self.el("master-bg").set("fill", fill)
        return self

    def ground(self, fill: str) -> "Page":
        """A slide-local full-canvas background (ink, navy, deep...) painted right after the
        Master background and before Master/Layout shapes, as PPTX paint order requires."""
        bg = self.el("master-bg")
        parent = self._parent(bg)
        e = fragment(f'<rect id="slide-ground" data-pptx-role="background" width="{self.w:g}" height="{self.h:g}" fill="{fill}"/>')[0]
        parent.insert(list(parent).index(bg) + 1, e)
        return self

    def style(self, id_: str, **attrs) -> "Page":
        """Restyle a layout or decoration element (attribute names use _ for -)."""
        e = self.el(id_)
        for k, v in attrs.items():
            k = k.replace("_", "-")
            if v is None:
                e.attrib.pop(k, None)
            else:
                e.set(k, str(v))
        return self

    def hide(self, id_: str) -> "Page":
        """Hide a decoration (never a placeholder or layout element) without deleting it."""
        e = self.el(id_)
        if e.get("data-pptx-role") != "decoration":
            raise ValueError(f"{id_} is not a decoration; restyle layout elements instead")
        e.set("opacity", "0")
        return self

    def defs(self, markup: str) -> "Page":
        d = self.root.find(_q("defs"))
        if d is None:
            d = ET.Element(_q("defs"))
            self.root.insert(0, d)
        for e in fragment(markup):
            d.append(e)
        return self

    def add(self, markup: str, *, before: str | None = None, after: str | None = None) -> "Page":
        """Insert decoration elements. Each top-level element gets data-pptx-role="decoration"."""
        els = fragment(markup)
        for e in els:
            if e.get("data-pptx-role") is None and e.get("data-pptx-layer") is None:
                e.set("data-pptx-role", "decoration")
            if e.get("id") is None:  # ppt-master requires a stable id on every role-bearing element
                self._deco += 1
                e.set("id", f"theme-deco-{self._deco:02d}")
            if e.tag == _q("text"):
                self.decor_texts.append(e)
        if before or after:
            anchor = self.el(before or after)
            if after and after in self._cursor:
                anchor = self._cursor[after]
            parent = self._parent(anchor)
            idx = list(parent).index(anchor) + (1 if after else 0)
            if parent is self.root:
                # Paint order: master/layout layers first, then slide content. A decoration
                # can never sit beneath a layout-layer element.
                layer_idx = [i for i, c in enumerate(parent)
                             if c.get("data-pptx-layer") or c.get("data-pptx-role") == "background"]
                if layer_idx and idx <= layer_idx[-1]:
                    idx = layer_idx[-1] + 1
            for i, e in enumerate(els):
                parent.insert(idx + i, e)
            if after:
                self._cursor[after] = els[-1]
        else:
            for e in els:
                self.root.append(e)
        return self

    # -- placeholders ---------------------------------------------------------
    def text(self, id_: str, lines, *, size, fill, family, x=None, y=None, weight=None, ls=None,
             lh=1.2, anchor=None, italic=False, bounds: str | None = None) -> "Page":
        g = self.el(id_)
        old = g.find(_q("text"))
        bx, by, bw, bh = [float(v) for v in g.get("data-pptx-bounds").split()]
        x = x if x is not None else (old.get("x") if old is not None else bx)
        y = y if y is not None else (old.get("y") if old is not None else by + size)
        if bounds:
            g.set("data-pptx-bounds", bounds)
            bx, by, bw, bh = [float(v) for v in bounds.split()]
        new = fragment(text_markup(lines, x=x, y=y, size=size, fill=fill, family=family, weight=weight,
                                   ls=ls, lh=lh, anchor=anchor, italic=italic, carrier=True))[0]
        if g.get("data-pptx-binding") == "proxy":
            for c in list(g):
                g.remove(c)
            g.append(new)
        elif old is not None:
            g.insert(list(g).index(old), new)
            g.remove(old)
        else:
            g.append(new)
        self.texts.append({"id": id_, "lines": [lines] if isinstance(lines, str) else list(lines),
                           "x": float(x), "y": float(y), "size": size, "family": family,
                           "weight": weight, "italic": italic, "ls": ls or 0, "lh": lh,
                           "anchor": anchor, "bounds": (bx, by, bw, bh)})
        return self

    def proxy(self, id_: str, markup: str) -> "Page":
        """Replace an object placeholder's proxy content with native drawn content."""
        g = self.el(id_)
        for c in list(g):
            g.remove(c)
        for e in fragment(markup):
            g.append(e)
        return self

    def image(self, id_: str, href: str, *, par: str = "xMidYMid slice", opacity=None) -> "Page":
        img = self.el(id_).find(_q("image"))
        img.set("href", href)
        img.set("preserveAspectRatio", par)
        if opacity is not None:
            img.set("opacity", str(opacity))
        return self

    # -- output -------------------------------------------------------------
    def save(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        ET.indent(self.tree, space="  ")
        self.tree.write(path, encoding="utf-8", xml_declaration=False)
        return path


# -- fit check -----------------------------------------------------------------
# The authority is ppt-master's own estimator (scripts/text_measure.py), because
# its svg_quality_checker rejects any carrier text whose estimated extent leaves
# the placeholder bounds, and decoration text that leaves the canvas. Real glyph
# widths do not matter here; the checker's estimate does.

def _pm_measure():
    import importlib
    import sys as _sys
    sys_path = ROOT / "scripts"
    if str(sys_path) not in _sys.path:
        _sys.path.insert(0, str(sys_path))
    try:
        epm = importlib.import_module("ensure_ppt_master")
    except ImportError:
        return None
    for _source, path in epm.candidates():
        d = epm.resolve_skill_dir(path)
        if d:
            _sys.path.insert(0, str(d / "scripts"))
            try:
                return importlib.import_module("text_measure")
            except ImportError:
                return None
    return None


_TM = None


def _width(tm, line, family, size, weight, ls):
    w = "bold" if str(weight) in ("bold", "700", "800") else "normal"
    return tm.measure_text(line, size=size, family=family, weight=w, letter_spacing=float(ls or 0),
                           include_headroom=True)


def fit_report(page: Page, tolerance: float = 1.0) -> list[str]:
    """Problems ppt-master's checker would raise: text outside its placeholder bounds,
    decoration text outside the canvas, or text below the floor (14 px A4, 12 px 16:9)."""
    global _TM
    if _TM is None:
        _TM = _pm_measure() or False
    tm = _TM
    issues = []
    for t in page.texts:
        if t["size"] < page.floor:
            issues.append(f'{page.prototype}#{t["id"]} size {t["size"]} below the {page.floor}px floor')
        if not tm:
            continue
        bx, by, bw, bh = t["bounds"]
        width = max(_width(tm, ln, t["family"], t["size"], t["weight"], t["ls"]) for ln in t["lines"])
        left = t["x"] - (width if t["anchor"] == "end" else width / 2 if t["anchor"] == "middle" else 0)
        top = t["y"] - 0.85 * t["size"]
        bottom = t["y"] + t["size"] * t["lh"] * (len(t["lines"]) - 1) + 0.35 * t["size"]
        if left < bx - tolerance or left + width > bx + bw + tolerance:
            issues.append(f'{page.prototype}#{t["id"]} width {left:.0f}-{left + width:.0f} outside box {bx:.0f}-{bx + bw:.0f}')
        if top < by - tolerance or bottom > by + bh + tolerance:
            issues.append(f'{page.prototype}#{t["id"]} height {top:.0f}-{bottom:.0f} outside box {by:.0f}-{by + bh:.0f}')
    if tm:
        for e in page.decor_texts:
            size = float(e.get("font-size", 24))
            lines = [e.text or ""] + [c.text or "" for c in e]
            width = max(_width(tm, ln, e.get("font-family", "Arial"), size, e.get("font-weight"),
                               e.get("letter-spacing")) for ln in lines)
            x = float(e.get("x"))
            a = e.get("text-anchor")
            left = x - (width if a == "end" else width / 2 if a == "middle" else 0)
            if size < page.floor:
                issues.append(f'{page.prototype}#{e.get("id")} decoration size {size} below the {page.floor}px floor')
            if left < -tolerance or left + width > page.w + tolerance:
                issues.append(f'{page.prototype}#{e.get("id")} decoration "{lines[0][:20]}" {left:.0f}-{left + width:.0f} leaves the canvas')
    else:
        issues.append("(width check skipped: ppt-master's text_measure.py not found; run scripts/ensure_ppt_master.py)")
    return issues
