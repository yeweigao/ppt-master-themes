#!/usr/bin/env python3
"""Install ppt-master-themes (and, if absent, the latest ppt-master release) into agent hosts.

    python3 scripts/install.py --target all                 # Claude Code + Codex + WorkBuddy, user scope
    python3 scripts/install.py --target codex --scope project
    python3 scripts/install.py --target claude --dry-run

Both skills end up side by side in each host's skills folder, which is the first
place scripts/ensure_ppt_master.py looks. On macOS/Linux the entries are symlinks
to this checkout (edits apply everywhere at once); on Windows, or with --copy,
they are copies. Existing entries are never overwritten or deleted.
Standard library only; Python 3.8+.
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKAGE_ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import ensure_ppt_master as epm  # noqa: E402

SKILL_NAME = "ppt-master-themes"
COPY_IGNORE = shutil.ignore_patterns(".git", "node_modules", "projects", "vibe_images",
                                     "dist", "qa", "__pycache__", "*.pyc", ".DS_Store")


def host_dirs(target: str, scope: str, project: Path) -> list[Path]:
    home = Path.home()
    if scope == "project":
        rel = {"claude": [".claude/skills"], "codex": [".agents/skills"], "workbuddy": [".workbuddy/skills"]}
        return [project / r for r in rel[target]]
    if target == "claude":
        return [home / ".claude" / "skills"]
    if target == "codex":
        return [home / ".agents" / "skills"]
    appdata = os.environ.get("APPDATA")
    if os.name == "nt" and appdata:
        return [Path(appdata) / "WorkBuddy" / "skills"]
    return [home / ".workbuddy" / "skills"]


def place(src: Path, dst: Path, use_copy: bool, dry: bool) -> str:
    if dst.is_symlink() or dst.exists():
        try:
            if dst.resolve() == src.resolve():
                return f"ok      {dst} (already points here)"
        except OSError:
            pass
        return f"skip    {dst} exists; left untouched"
    if dry:
        return f"would   {'copy' if use_copy else 'link'} {dst} -> {src}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    if use_copy:
        shutil.copytree(src, dst, ignore=COPY_IGNORE)
        return f"copied  {dst}"
    os.symlink(src, dst, target_is_directory=True)
    return f"linked  {dst} -> {src}"


def locate_pm() -> Path | None:
    for _source, path in epm.candidates():
        d = epm.resolve_skill_dir(path)
        if d and epm.version_ok(epm.read_version(d)):
            return d
    return None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target", nargs="+", required=True, choices=["claude", "codex", "workbuddy", "all"])
    ap.add_argument("--scope", choices=["user", "project"], default="user")
    ap.add_argument("--project-dir", default=os.getcwd(), help="project root for --scope project")
    ap.add_argument("--copy", action="store_true", help="copy instead of symlink (default on Windows)")
    ap.add_argument("--no-ppt-master", action="store_true", help="do not fetch or link ppt-master")
    ap.add_argument("--ref", help="ppt-master tag or branch to fetch instead of the latest release")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    targets = ["claude", "codex", "workbuddy"] if "all" in args.target else args.target
    use_copy = args.copy or os.name == "nt"
    project = Path(args.project_dir).resolve()

    pm = None
    if not args.no_ppt_master:
        pm = locate_pm()
        if pm:
            print(f"found   ppt-master {epm.read_version(pm)} at {pm}")
        else:
            ref = args.ref
            if not ref:
                ref, msg = epm.latest_release_tag()
                if not ref:
                    sys.exit(f"error   could not read ppt-master releases: {msg}")
            dest = epm.cache_root() / f"ppt-master-{ref.lstrip('v').replace('/', '-')}"
            if args.dry_run:
                print(f"would   fetch ppt-master {ref} into {dest}")
            else:
                ok, msg = epm.fetch(dest, ref)
                pm = epm.resolve_skill_dir(dest)
                if not pm:
                    sys.exit(f"error   could not fetch ppt-master: {msg}")
                print(f"fetched ppt-master {ref} into {dest}")
            req = pm / "requirements.txt"
            if req.is_file():
                print(f"note    install its Python dependencies: python3 -m pip install -r \"{req}\"")

    for t in targets:
        for skills in host_dirs(t, args.scope, project):
            print(f"[{t}] {skills}")
            print("  " + place(PACKAGE_ROOT, skills / SKILL_NAME, use_copy, args.dry_run))
            if pm and pm.parent != skills:
                print("  " + place(pm, skills / "ppt-master", use_copy, args.dry_run))
    print("done. Restart the agent so it reloads skills, then ask it to use ppt-master-themes.")


if __name__ == "__main__":
    main()
