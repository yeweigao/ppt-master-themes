#!/usr/bin/env python3
"""ppt-master-themes compatibility check.

Usage: python3 compat_check.py --pm <ppt-master root> [--theme natgeo] [--themes-root <skill root>]
Maintenance-only check: attribution guard, entry interfaces, Style template validation,
the theme's discovery fields and Theme DNA, every package Layout's template validation, a
combined Style + Layout apply_template dry-run, and declared assets. Not a runtime stage or
end-to-end certification.
Exit 0 = OK (warnings allowed), 1 = blocking problem.
"""
import argparse, json, re, subprocess, sys, tempfile, os
from pathlib import Path

REQ_SCRIPTS = ["svg_quality_checker.py", "svg_to_pptx.py", "finalize_svg.py",
               "text_measure.py", "apply_template.py",
               "project_manager.py"]
REQ_REFS = ["executor-base.md", "strategist-template.md", "artifact-ownership.md"]
REQ_FILES = ["workflows/routing.md", "templates/styles/README.md"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pm", required=True, help="ppt-master root (contains SKILL.md)")
    ap.add_argument("--theme", default="natgeo")
    ap.add_argument("--themes-root", default=str(Path(__file__).resolve().parents[2]))
    a = ap.parse_args()
    pm, root = Path(a.pm).expanduser(), Path(a.themes_root).expanduser().resolve()
    if not pm.is_absolute():
        report(None, ['--pm requires the host/user-provided absolute skill directory'], [])
    guard = pm / 'scripts' / 'attribution_guard.py'
    if not guard.is_file():
        report(None, ['attribution_guard.py missing; stop and consult the supplied skill entry'], [])
    # The entry is read before the guard. No other ppt-master tool runs on guard failure.
    entry = pm / 'SKILL.md'
    if not entry.is_file():
        report(None, [f'SKILL.md not found under {pm}'], [])
    entry_text = entry.read_text(encoding='utf-8')
    guarded = subprocess.run([sys.executable, str(guard)], capture_output=True, text=True, encoding='utf-8')
    if guarded.returncode != 0:
        print(guarded.stdout + guarded.stderr, end='')
        report(None, ['attribution guard failed; no further inspection or tools run'], [])
    errs, warns = [], []
    skill = pm / "SKILL.md"
    ver = None
    if skill.exists():
        m = re.search(r'version:\s*"?([\d.]+)', entry_text)
        ver = m.group(1) if m else None
    else:
        errs.append(f"SKILL.md not found under {pm}")
    tdir = root / "themes" / a.theme
    tj = tdir / "theme.json"
    if not tj.exists():
        errs.append(f"theme.json missing: {tj}"); report(ver, errs, warns); return
    theme = json.loads(tj.read_text(encoding="utf-8"))
    tested = theme.get("tested_with_ppt_master", [])
    if not tested:
        warns.append('no end-to-end tested version declared; this checks maintenance interfaces only')
    elif ver and ver not in tested:
        major = ver.split(".")[0]
        if any(t.split(".")[0] == major for t in tested):
            warns.append(f"ppt-master {ver} not in tested list {tested} (same major) - maintenance smoke check only; follow the selected runtime gate cadence")
        else:
            errs.append(f"ppt-master {ver} major differs from tested {tested} - re-verify graft points before use")
    for s in REQ_SCRIPTS:
        if not (pm / "scripts" / s).exists(): errs.append(f"missing script scripts/{s}")
    for r in REQ_REFS:
        if not (pm / "references" / r).exists(): warns.append(f"missing reference references/{r}")
    for path in REQ_FILES:
        if not (pm / path).is_file(): errs.append(f'missing integration authority {path}')
    ws = tdir / theme.get("style_workspace", "workspace")
    specs = list((ws / "templates").glob("design_spec.style.*.md"))
    if (ws / 'templates' / 'design_spec.md').is_file():
        specs.append(ws / 'templates' / 'design_spec.md')
    if not specs: errs.append("theme workspace has no Style design spec")
    env = dict(os.environ)
    chk = pm / "scripts" / "svg_quality_checker.py"
    if chk.exists() and specs:
        p = subprocess.run([sys.executable, str(chk), str(ws / "templates"), "--template-mode",
                            "--canonical-authoring"], capture_output=True, text=True, env=env)
        if p.returncode != 0:
            errs.append("template-mode validation failed:\n" + (p.stdout + p.stderr)[-1500:])
    at = pm / "scripts" / "apply_template.py"
    if at.exists() and specs:
        with tempfile.TemporaryDirectory() as td:
            proj = Path(td) / "probe"; (proj / "svg_output").mkdir(parents=True)
            p = subprocess.run([sys.executable, str(at), str(proj), "--root", str(ws), "--dry-run"],
                               capture_output=True, text=True, env=env)
            if p.returncode != 0:
                errs.append("apply_template --root dry-run returned non-zero:\n" + (p.stdout + p.stderr)[-800:])
    # Discovery fields and Theme DNA: what SKILL.md and ppt-master's Stage 2 rely on.
    for key in ("use_when", "avoid_when"):
        if not theme.get(key):
            errs.append(f"theme.json lacks {key}; list_themes.py cannot recommend the theme")
    for spec in specs:
        body = spec.read_text(encoding="utf-8")
        for field in ("**Theme DNA**", "**Extension Rule**"):
            if field not in body:
                errs.append(f"{spec.name} lacks {field} in section V")
    # Every package Layout validates on its own canvas and installs together with this Style.
    for lspec in sorted(root.glob("layouts/*/workspace/templates/design_spec.layout.*.md")):
        lws = lspec.parent.parent
        fmt = re.search(r"^canvas_format:\s*(\S+)", lspec.read_text(encoding="utf-8"), re.M)
        if chk.exists():
            cmd = [sys.executable, str(chk), str(lws / "templates"), "--template-mode", "--canonical-authoring"]
            if fmt:
                cmd += ["--format", fmt.group(1)]
            p = subprocess.run(cmd, capture_output=True, text=True, env=env)
            if p.returncode != 0:
                errs.append(f"layout {lws.parent.name} template-mode validation failed:\n" + (p.stdout + p.stderr)[-1200:])
        if at.exists() and specs:
            with tempfile.TemporaryDirectory() as td:
                proj = Path(td) / "probe"; (proj / "svg_output").mkdir(parents=True)
                p = subprocess.run([sys.executable, str(at), str(proj), "--root", str(ws), "--root", str(lws),
                                    "--dry-run"], capture_output=True, text=True, env=env)
                if p.returncode != 0:
                    errs.append(f"apply_template dry-run of {a.theme} + {lws.parent.name} failed:\n"
                                + (p.stdout + p.stderr)[-800:])
    fonts = tdir / "fonts"
    for fam in theme.get("fonts", []):
        for face, spec in fam.get("embed", {}).items():
            if not (tdir / spec["source"]).exists(): errs.append(f"font source missing for {fam['family']} {face}: {spec['source']}")
        if fam.get("license_file") and not (tdir / fam["license_file"]).exists(): warns.append(f"licence file missing: {fam['license_file']}")
    print("Scope: maintenance interfaces only; not generation, visual review, or export verification")
    report(ver, errs, warns)

def report(ver, errs, warns):
    print(f"ppt-master version: {ver}")
    for w in warns: print("WARN:", w)
    for e in errs: print("ERROR:", e)
    print("RESULT:", "OK" if not errs else "BLOCKED")
    sys.exit(1 if errs else 0)

if __name__ == "__main__":
    main()
