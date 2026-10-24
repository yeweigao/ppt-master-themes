#!/usr/bin/env python3
"""List the themes and layouts in this package, with absolute workspace roots.

    python3 scripts/list_themes.py                 # readable summary
    python3 scripts/list_themes.py --json          # machine-readable
    python3 scripts/list_themes.py --roots natgeo a4-editorial
        # print the Stage-1 template_options block for exactly these ids

Themes are discovered from themes/*/theme.json (the _template scaffold is skipped),
layouts from layouts/*/workspace/templates/design_spec.layout.*.md. Adding a theme
or a layout directory is enough; nothing else needs editing. Standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def svg_ids(svg: Path) -> tuple[str | None, str | None]:
    """(data-pptx-master, data-pptx-layout) from the root <svg> element."""
    head = svg.read_text(encoding="utf-8", errors="replace")[:2000]
    m = re.search(r'data-pptx-master="([^"]+)"', head)
    l = re.search(r'data-pptx-layout="([^"]+)"', head)
    return (m.group(1) if m else None, l.group(1) if l else None)


def frontmatter(md: Path) -> dict:
    text = md.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    out = {}
    if m:
        for line in m.group(1).splitlines():
            k, sep, v = line.partition(":")
            if sep and not line.startswith((" ", "\t")):
                out[k.strip()] = v.strip().strip('"')
    return out


def layouts() -> list[dict]:
    found = []
    for spec in sorted(ROOT.glob("layouts/*/workspace/templates/design_spec.layout.*.md")):
        fm = frontmatter(spec)
        tpl = spec.parent
        found.append({
            "id": fm.get("layout_id", spec.parent.parent.parent.name),
            "kind": "layout",
            "summary": fm.get("summary", ""),
            "canvas": fm.get("canvas_format"),
            "prototypes": sorted(p.stem for p in tpl.glob("*.svg")),
            "_layout_attrs": {svg_ids(p)[1]: p.stem for p in tpl.glob("*.svg") if svg_ids(p)[1]},
            "workspace": str(tpl.parent),
            "readme": str(spec.parent.parent.parent / "README.md"),
            "filled_references": str(ROOT / "website" / "artwork" / "templates"),
        })
    return found


def themes(lay: list[dict]) -> list[dict]:
    by_master = {l["id"]: l["_layout_attrs"] for l in lay}
    found = []
    for tj in sorted(ROOT.glob("themes/*/theme.json")):
        tdir = tj.parent
        if tdir.name.startswith("_"):
            continue
        try:
            d = json.loads(tj.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"warning: {tj} is not valid JSON: {e}", file=sys.stderr)
            continue
        showcased, own = [], []
        example_dirs = [tdir / "examples" / "svg"] + [tdir / "examples" / m for m in by_master]
        for ex in sorted(p for d in example_dirs for p in d.glob("*.svg")):
            master, layout = svg_ids(ex)
            proto = by_master.get(master, {}).get(layout)
            (showcased if proto else own).append(f"{ex.stem} -> {master}/{proto}" if proto else ex.stem)
        found.append({
            "id": d.get("id", tdir.name),
            "kind": "style",
            "name": d.get("name"),
            "name_zh": d.get("name_zh"),
            "summary": d.get("summary", ""),
            "use_when": d.get("use_when", []),
            "avoid_when": d.get("avoid_when", []),
            "maturity": d.get("maturity", "stable"),
            "tested_with_ppt_master": d.get("tested_with_ppt_master", []),
            "workspace": str(tdir / d.get("style_workspace", "workspace")),
            "style_spec": str(tdir / d.get("style_spec", "")),
            "recipes": str(tdir / d.get("recipes", "recipes.md")),
            "examples": [str(d) for d in example_dirs if d.is_dir()],
            "showcased_prototypes": showcased,
            "theme_pages": own,
        })
    return found


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--roots", nargs="+", metavar="ID", help="theme and/or layout ids to hand off")
    ap.add_argument("--lang", default="zh", help="UI language for the Stage-1 block")
    args = ap.parse_args()

    lay = layouts()
    th = themes(lay)
    for l in lay:
        l.pop("_layout_attrs", None)
    index = {x["id"]: x for x in th + lay}

    if args.roots:
        unknown = [i for i in args.roots if i not in index]
        if unknown:
            sys.exit(f"unknown id(s): {', '.join(unknown)}; known: {', '.join(index)}")
        kinds = [index[i]["kind"] for i in args.roots]
        dup = {k for k in kinds if kinds.count(k) > 1}
        if dup:
            sys.exit(f"more than one {'/'.join(sorted(dup))} root; ask the user to pick one per kind")
        roots = [index[i]["workspace"] for i in args.roots]
        print(json.dumps({"stage": "stage1", "template_options": {
            "schema_version": 1, "phase": "template", "lang": args.lang,
            "default_mode": "templates", "explicit_workspace_roots": roots}}, ensure_ascii=False, indent=2))
        print("\napply after Stage-1 confirmation:\n  python3 \"$PM/scripts/apply_template.py\" \"$P\" "
              + " ".join(f'--root "{r}"' for r in roots))
        return

    if args.json:
        print(json.dumps({"package_root": str(ROOT), "themes": th, "layouts": lay}, ensure_ascii=False, indent=2))
        return

    print(f"package root: {ROOT}\n")
    print("THEMES (kind: style)")
    for t in th:
        tag = "" if t["maturity"] == "stable" else f"  [{t['maturity']}]"
        print(f"\n  {t['id']}  {t['name']} / {t['name_zh']}{tag}")
        print(f"    use when : {'；'.join(t['use_when']) or '-'}")
        print(f"    avoid    : {'；'.join(t['avoid_when']) or '-'}")
        print(f"    tested   : {', '.join(t['tested_with_ppt_master']) or 'not end-to-end tested'}")
        print(f"    showcase : {len(t['showcased_prototypes'])} layout prototypes + {len(t['theme_pages'])} theme pages")
        print(f"    root     : {t['workspace']}")
    print("\nLAYOUTS (kind: layout)")
    for l in lay:
        print(f"\n  {l['id']}  canvas {l['canvas']}, {len(l['prototypes'])} prototypes")
        print(f"    root     : {l['workspace']}")
        print(f"    catalog  : {l['readme']}")


if __name__ == "__main__":
    main()
