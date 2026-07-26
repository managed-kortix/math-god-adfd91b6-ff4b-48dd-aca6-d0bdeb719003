#!/usr/bin/env python3
"""Fail-closed local checks for destination-aware result publication."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "research" / "publication-manifest.json"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def check(item_id: str) -> None:
    data = json.loads(MANIFEST.read_text())
    matches = [x for x in data["results"] if x["id"] == item_id]
    if len(matches) != 1:
        raise SystemExit(f"expected exactly one manifest item {item_id!r}")
    item = matches[0]
    folder = item.get("paper_folder")
    if folder:
        base = ROOT / folder
        for name in ("paper.tex", "paper.pdf"):
            path = base / name
            if not path.is_file() or path.stat().st_size == 0:
                raise SystemExit(f"missing artifact: {path.relative_to(ROOT)}")
    print(json.dumps({
        "id": item_id,
        "kind": item["kind"],
        "scope_status": item["scope_status"],
        "ocb": item["ocb"],
        "git_commit": git("rev-parse", "HEAD"),
        "working_tree_clean": not bool(git("status", "--porcelain")),
    }, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    command = sub.add_parser("check")
    command.add_argument("manifest_id")
    args = parser.parse_args()
    if args.command == "check":
        check(args.manifest_id)


if __name__ == "__main__":
    main()
