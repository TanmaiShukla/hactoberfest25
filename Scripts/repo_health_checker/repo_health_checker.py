#!/usr/bin/env python3
"""
Repo Health Checker
A small CLI utility that checks for presence (and minimal content) of common repo files.

Usage:
    python repo_health_checker.py                # checks current directory
    python repo_health_checker.py /path/to/repo  # checks given path
    python repo_health_checker.py --json /path   # prints machine-readable JSON
"""

from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
from typing import Dict, List


DEFAULT_FILES = {
    "README": ["README.md", "readme.md"],
    "LICENSE": ["LICENSE", "LICENSE.md"],
    "CONTRIBUTING": ["CONTRIBUTING.md", "CONTRIBUTING"],
    "CONTRIBUTORS": ["CONTRIBUTORS.md", "CONTRIBUTORS"],
    "CODE_OF_CONDUCT": ["CODE_OF_CONDUCT.md", "code_of_conduct.md"],
    "GITHUB_WORKFLOWS": [".github/workflows"],
    "PYPROJECT_OR_SETUP": ["pyproject.toml", "setup.py", "requirements.txt"],
    ".gitignore": [".gitignore"],
    "SCRIPTS_FOLDER": ["Scripts", "scripts"]
}


def find_any(path: Path, candidates: List[str]) -> Path | None:
    """
    Return the first candidate that exists inside path (file or dir), or None.
    """
    for candidate in candidates:
        candidate_path = path / candidate
        if candidate_path.exists():
            return candidate_path
    return None


def file_has_min_content(p: Path, min_chars: int = 20) -> bool:
    """Return True if file exists and has at least min_chars non-whitespace chars."""
    if not p.is_file():
        return False
    try:
        text = p.read_text(encoding="utf-8", errors="ignore").strip()
    except Exception:
        return False
    # count non-whitespace characters
    return len("".join(text.split())) >= min_chars


def check_repo(path: Path) -> Dict[str, Dict[str, object]]:
    """
    Check for expected files/dirs and return a dict with findings and suggestions.
    """
    findings: Dict[str, Dict[str, object]] = {}
    for key, candidates in DEFAULT_FILES.items():
        found = find_any(path, candidates)
        entry: Dict[str, object] = {"found": False, "path": None, "ok": False, "notes": []}
        if found:
            entry["found"] = True
            entry["path"] = str(found.relative_to(path))
            if found.is_file():
                ok = file_has_min_content(found, min_chars=30)
                entry["ok"] = ok
                if not ok:
                    entry["notes"].append("File seems too short or empty; consider adding basic content.")
            else:  # directory
                # if directory, check if non-empty
                try:
                    entries = list(found.iterdir())
                except Exception:
                    entries = []
                if entries:
                    entry["ok"] = True
                else:
                    entry["ok"] = False
                    entry["notes"].append("Directory exists but appears empty.")
        else:
            entry["notes"].append(f"Missing — consider adding {', '.join(candidates)}")
        findings[key] = entry
    # Additional lightweight checks
    # check for at least one .py file (only if project is Python-heavy)
    py_files = list(path.rglob("*.py"))
    findings["PYTHON_FILES"] = {
        "found": bool(py_files),
        "count": len(py_files),
        "notes": [] if py_files else ["No .py files found — repository might not be Python-based."]
    }
    return findings


def pretty_print(findings: Dict[str, Dict[str, object]], base_path: Path) -> None:
    print(f"\nRepo Health Check for: {base_path.resolve()}\n" + "-" * 60)
    good = []
    warn = []
    for key, info in findings.items():
        if key == "PYTHON_FILES":
            print(f"{key:20}: found={info['found']}, count={info['count']}")
            if info["notes"]:
                print(" " * 24 + "Note: " + "; ".join(info["notes"]))
            continue
        status = "OK" if info["found"] and info["ok"] else ("MISSING" if not info["found"] else "INCOMPLETE")
        line = f"{key:20}: {status}"
        if info.get("path"):
            line += f"  ({info['path']})"
        print(line)
        if info.get("notes"):
            for n in info["notes"]:
                print(" " * 24 + "- " + n)
        if status == "OK":
            good.append(key)
        else:
            warn.append((key, status))
    print("\nSummary:")
    print(f"  ✅ Good: {len(good)}")
    print(f"  ⚠️ Issues / Missing: {len(warn)}")
    if warn:
        print("  Suggestions:")
        for k, s in warn:
            print(f"   - {k}: {s}")
    print("-" * 60 + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Repo Health Checker - simple checks for common repo files")
    parser.add_argument("path", nargs="?", default=".", help="path to repository (default: current directory)")
    parser.add_argument("--json", action="store_true", help="output machine-readable JSON")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    base = Path(args.path).resolve()
    if not base.exists():
        print(f"Error: path '{base}' does not exist.")
        raise SystemExit(2)
    findings = check_repo(base)
    if args.json:
        print(json.dumps(findings, indent=2))
    else:
        pretty_print(findings, base)


if __name__ == "__main__":
    main()
