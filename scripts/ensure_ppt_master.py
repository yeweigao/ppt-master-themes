#!/usr/bin/env python3
"""Locate (or, with consent, fetch) the ppt-master skill this package extends.

Works the same under any agent host (Claude Code, Codex, WorkBuddy, or a plain
shell): it checks a fixed, ordered list of locations and never scans the disk.

    python3 scripts/ensure_ppt_master.py            # locate only, print JSON
    python3 scripts/ensure_ppt_master.py --fetch    # clone the latest GitHub release if missing
    python3 scripts/ensure_ppt_master.py --fetch --ref v6.7.3   # or a specific tag / branch
    python3 scripts/ensure_ppt_master.py --pm /abs/path/to/ppt-master

Exit codes: 0 found (same major version; a newer minor is reported as untested),
1 missing, 2 found but a different major version, 3 fetch failed.
Standard library only; Python 3.8+.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# Fetching takes the latest GitHub release by default. TESTED_LINE records the
# release line this package was last tested end to end against (keep it in step
# with theme.json "tested_with_ppt_master"); a newer minor still runs, with a note.
TESTED_LINE = (6, 7)
SUPPORTED_MAJOR = 6
REPO_URL = "https://github.com/hugohe3/ppt-master.git"
TAG_RE = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")

HERE = Path(__file__).resolve().parent
PACKAGE_ROOT = HERE.parent  # the ppt-master-themes skill directory


def cache_root() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    else:
        base = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    return base / "ppt-master-themes"


def candidates() -> list[tuple[str, Path]]:
    """Ordered (source, path) pairs. Each path may be a skill dir or a repo root."""
    home = Path.home()
    cwd = Path.cwd()
    out: list[tuple[str, Path]] = []
    env = os.environ.get("PPT_MASTER_HOME")
    if env:
        out.append(("env:PPT_MASTER_HOME", Path(env)))
    # Installed side by side with this package (any host's skills folder). Check the
    # path the host used (may be a symlink) before the resolved checkout location.
    invoked = __file__ if os.path.isabs(__file__) else os.path.join(os.environ.get("PWD", os.getcwd()), __file__)
    as_invoked = Path(os.path.normpath(invoked)).parent.parent
    for root in dict.fromkeys([as_invoked, PACKAGE_ROOT]):
        out.append(("sibling", root.parent / "ppt-master"))
    # Per-host skill folders, project scope first, then user scope.
    for rel in (".claude/skills", ".agents/skills", ".workbuddy/skills"):
        out.append((f"project:{rel}", cwd / rel / "ppt-master"))
    for rel in (".claude/skills", ".agents/skills", ".codex/skills", ".workbuddy/skills"):
        out.append((f"user:~/{rel}", home / rel / "ppt-master"))
    appdata = os.environ.get("APPDATA")
    if appdata:
        out.append(("user:%APPDATA%/WorkBuddy/skills", Path(appdata) / "WorkBuddy" / "skills" / "ppt-master"))
    out.append(("admin:/etc/codex/skills", Path("/etc/codex/skills/ppt-master")))
    # Claude Code plugin cache: <marketplace>/ppt-master/<version>/[skills/]ppt-master
    for pat in ("plugins/cache/*/ppt-master/*/ppt-master", "plugins/cache/*/ppt-master/*/skills/ppt-master"):
        for p in sorted(glob.glob(str(home / ".claude" / pat)), reverse=True):
            out.append(("claude-plugin-cache", Path(p)))
    # Copies fetched earlier by this script, newest first.
    fetched = sorted(cache_root().glob("ppt-master-*"), key=lambda p: version_key(p.name.split("ppt-master-", 1)[1]), reverse=True)
    out += [("fetched-cache", p) for p in fetched]
    return out


def resolve_skill_dir(path: Path) -> Path | None:
    """Return the ppt-master skill dir for a skill dir or a repository checkout."""
    for d in (path, path / "skills" / "ppt-master"):
        skill = d / "SKILL.md"
        guard = d / "scripts" / "attribution_guard.py"
        if skill.is_file() and guard.is_file():
            head = skill.read_text(encoding="utf-8", errors="replace")[:4000]
            if re.search(r"^name:\s*ppt-master\s*$", head, re.M):
                return d.resolve()
    return None


def read_version(skill_dir: Path) -> str | None:
    head = (skill_dir / "SKILL.md").read_text(encoding="utf-8", errors="replace")[:4000]
    m = re.search(r'^\s*version:\s*"?([0-9][0-9.]*)"?', head, re.M)
    return m.group(1) if m else None


def version_key(ver: str) -> tuple:
    parts = re.findall(r"\d+", ver or "")
    return tuple(int(x) for x in parts[:3]) or (0,)


def version_ok(ver: str | None) -> bool:
    """Same major version as the one this package targets."""
    return bool(ver) and version_key(ver)[0] == SUPPORTED_MAJOR


def tested(ver: str | None) -> bool:
    return bool(ver) and version_key(ver)[:2] == TESTED_LINE


def latest_release_tag() -> tuple[str | None, str]:
    """Highest vX.Y.Z tag on GitHub (releases are tagged this way)."""
    try:
        r = subprocess.run(["git", "ls-remote", "--tags", "--refs", REPO_URL], capture_output=True, text=True, timeout=60)
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        return None, f"git ls-remote failed: {e}"
    if r.returncode != 0:
        return None, (r.stderr or r.stdout).strip()[-400:]
    tags = [line.rsplit("/", 1)[-1] for line in r.stdout.splitlines()]
    tags = [t for t in tags if TAG_RE.match(t)]
    if not tags:
        return None, "no release tags found"
    return max(tags, key=version_key), "ok"


def fetch(dest: Path, ref: str) -> tuple[bool, str]:
    if dest.exists() and any(dest.iterdir()):
        return False, f"{dest} exists but is not a valid ppt-master checkout; move it aside first"
    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["git", "clone", "--depth", "1", "--branch", ref, REPO_URL, str(dest)]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
    except FileNotFoundError:
        return False, "git is not installed"
    if r.returncode != 0:
        return False, (r.stderr or r.stdout).strip()[-800:]
    return True, "cloned " + ref


def found_payload(skill_dir: Path, source: str) -> dict:
    ver = read_version(skill_dir)
    req = skill_dir / "requirements.txt"
    out = {
        "status": "found",
        "pm": str(skill_dir),
        "version": ver,
        "tested": tested(ver),
        "source": source,
        "requirements": str(req) if req.is_file() else None,
        "next": f'python3 "{skill_dir}/scripts/attribution_guard.py"',
    }
    if not tested(ver):
        out["note"] = (f"this package was last tested end to end with {TESTED_LINE[0]}.{TESTED_LINE[1]}.x; "
                       f"{ver} should work, but mention it is untested in the delivery note")
    return out


def report(payload: dict, code: int) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    sys.exit(code)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pm", help="explicit ppt-master skill dir or repository root")
    ap.add_argument("--fetch", action="store_true",
                    help="clone the latest GitHub release into the user cache if nothing is found (ask the user first)")
    ap.add_argument("--ref", help="tag or branch to fetch instead of the latest release, e.g. v6.7.3 or main")
    args = ap.parse_args()

    checked = []
    order = [("explicit:--pm", Path(args.pm))] if args.pm else candidates()
    for source, path in order:
        checked.append(str(path))
        skill_dir = resolve_skill_dir(path)
        if skill_dir:
            ver = read_version(skill_dir)
            ok = version_ok(ver)
            report(found_payload(skill_dir, source) if ok else {
                "status": "version-mismatch",
                "pm": str(skill_dir),
                "version": ver,
                "supported": f"{SUPPORTED_MAJOR}.x",
                "source": source,
                "next": (f"ppt-master {ver} is a different major version from {SUPPORTED_MAJOR}.x; its contract may "
                         "have changed. Tell the user and ask whether to continue or fetch the latest 6.x release"),
            }, 0 if ok else 2)
        if args.pm:
            report({"status": "missing", "checked": checked,
                    "next": "the --pm path does not contain ppt-master's SKILL.md and scripts/attribution_guard.py"}, 1)

    if not args.fetch:
        report({
            "status": "missing",
            "checked": checked,
            "next": ("ask the user for an existing ppt-master path, or for permission to download the "
                     "latest release from GitHub; then rerun with --pm <path> or --fetch"),
            "fetch_target": str(cache_root()),
            "manual_install": f"git clone --depth 1 {REPO_URL}   (or download from https://github.com/hugohe3/ppt-master/releases)",
        }, 1)

    ref = args.ref
    if not ref:
        ref, msg = latest_release_tag()
        if not ref:
            report({"status": "fetch-failed", "detail": msg,
                    "next": "report the failure; offer design-only output (spec draft + page plan), no PPTX export"}, 3)
    dest = cache_root() / f"ppt-master-{ref.lstrip('v').replace('/', '-')}"
    if resolve_skill_dir(dest):
        report(found_payload(resolve_skill_dir(dest), "fetched-cache:" + ref), 0)
    ok, msg = fetch(dest, ref)
    skill_dir = resolve_skill_dir(dest) if ok else None
    if not skill_dir:
        report({"status": "fetch-failed", "detail": msg, "fetch_target": str(dest),
                "next": "report the failure; offer design-only output (spec draft + page plan), no PPTX export"}, 3)
    payload = found_payload(skill_dir, "fetched:" + ref)
    req = skill_dir / "requirements.txt"
    if req.is_file():
        payload["next"] = f'install dependencies if missing: python3 -m pip install -r "{req}"; then ' + payload["next"]
    report(payload, 0)


if __name__ == "__main__":
    main()
