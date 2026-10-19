#!/usr/bin/env python3
"""Register project images in design_spec.md §VIII and spec_lock.md `## images`
(format accepted by ppt-master 6.7.x svg_quality_checker).

Usage:
  python3 register_images.py <project> [--source-note "user supplied"] \
      [--derived bg_P01.jpg=ai_cover.jpg ...] [--purpose "..."]
Every file in <project>/images is registered once (existing rows kept).
Files placed directly on pages are registered as Type=Photo. Files listed in --derived get a
"derived from X" Reference; their originals go in --source-only (Type=Source must have a
derivative and must not be referenced by SVGs, or the checker errors).
"""
import argparse, re
from pathlib import Path
from PIL import Image

HDR = ("| Filename | Dimensions | Ratio | Purpose | Type | Image pattern | Crop Policy | "
       "Acquire Via | Status | Reference | text_policy | page_role |\n"
       "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--source-note", default="supplied by the user")
    ap.add_argument("--purpose", default="Full-bleed or inline editorial photo")
    ap.add_argument("--derived", nargs="*", default=[])
    ap.add_argument("--crop", default="adaptive", choices=["adaptive", "no-crop"])
    ap.add_argument("--source-only", nargs="*", default=[], help="originals that are NOT placed on pages (only their derivatives are); registered as Type=Source")
    a = ap.parse_args()
    proj = Path(a.project); imgs = proj / "images"
    der = dict(d.split("=", 1) for d in a.derived)
    spec = proj / "design_spec.md"; lock = proj / "spec_lock.md"
    st = spec.read_text(encoding="utf-8") if spec.exists() else "# Design Spec\n"
    lt = lock.read_text(encoding="utf-8") if lock.exists() else ""
    rows, lrows = [], []
    for f in sorted(imgs.iterdir()) if imgs.exists() else []:
        if f.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"): continue
        if f"| {f.name} |" not in st:
            w, h = Image.open(f).size
            if f.name in der:
                typ, ref = "Photo", f"derived from {der[f.name]}; cropped/scaled to the page frame"
                purpose = "Prepared derivative crop"
            elif f.name in a.source_only:
                typ, ref, purpose = "Source", a.source_note, "Original kept for derivatives (not placed directly)"
            else:
                typ, ref, purpose = "Photo", a.source_note, a.purpose
            rows.append(f"| {f.name} | {w}×{h} | {w/h:.2f} | {purpose} | {typ} | editorial photo | "
                        f"{a.crop} | user | Existing | {ref} | none | content |\n")
        key = f.stem
        if not re.search(rf"^- {re.escape(key)}:", lt, re.M):
            lrows.append(f"- {key}: images/{f.name} | source=user | crop={a.crop}\n")
    if rows:
        m = re.search(r"^## VIII\..*$", st, re.M)
        if not m:
            st = st.rstrip() + "\n\n## VIII. Image Resource List\n\n" + HDR + "".join(rows)
        else:
            # append after the last table row of section VIII
            sec_end = re.search(r"^## (?!VIII\.)", st[m.end():], re.M)
            end = m.end() + (sec_end.start() if sec_end else len(st) - m.end())
            body = st[m.end():end]
            if "| Filename |" not in body:
                body = "\n\n" + HDR + "".join(rows) + "\n"
            else:
                body = body.rstrip() + "\n" + "".join(rows) + "\n"
            st = st[:m.end()] + body + st[end:]
        spec.write_text(st, encoding="utf-8")
    if lrows:
        if re.search(r"^## images\s*$", lt, re.M):
            lt = re.sub(r"(^## images\s*\n(?:- .*\n)*)", lambda mm: mm.group(1) + "".join(lrows), lt, count=1, flags=re.M)
        else:
            lt = lt.rstrip() + "\n\n## images\n" + "".join(lrows)
        lock.write_text(lt, encoding="utf-8")
    print(f"design_spec rows added: {len(rows)}; spec_lock rows added: {len(lrows)}")

if __name__ == "__main__":
    main()
