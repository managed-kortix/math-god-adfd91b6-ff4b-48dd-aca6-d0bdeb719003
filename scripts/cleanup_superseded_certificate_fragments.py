#!/usr/bin/env python3
"""Remove only explicitly audited, untracked certificate build leftovers."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = ROOT / "positive-square-energy" / "experiments"

SUPERSEDED_FRAGMENT_DIRECTORIES = (
    "rank6_order10_search_ckpt/chunk-50000-55000.r10g.xz.fragments",
    "rank6_order10_search_ckpt/chunk-55000-60000.r10g.xz.fragments",
    "rank6_order10_search_ckpt/chunk-60000-65000.r10g.xz.fragments",
    "rank6_order10_search_ckpt/chunk-65000-70000.r10g.xz.fragments",
    "rank6_order10_search_ckpt/chunk-70000-75000.r10g.xz.fragments",
    "rank6_order10_search_ckpt/chunk-75000-80000.r10g.xz.fragments",
    "rank6_order10_search_ckpt/chunk-80000-85000.r10g.xz.fragments",
    "rank6_order10_search_ckpt/chunk-85000-90000.r10g.xz.fragments",
    "rank6_order10_search_ckpt/chunk-90000-95000.r10g.xz.fragments",
    "rank6_order10_search_ckpt/chunk-95000-100000.r10g.xz.fragments",
    "rank6_order10_search_ckpt/chunk-100000-105000.r10g.xz.fragments",
    "rank6_order10_search_ckpt/chunk-105000-110000.r10g.xz.fragments",
    "rank6_order10_search_ckpt/chunk-110000-113865.r10g.xz.fragments",
    "rank6_order10_search_ckpt/chunk-113865-117726.r10g.xz.fragments",
    "rank6_order10_search_ckpt/chunk-117726-121582.r10g.xz.fragments",
    "rank6_order10_search_ckpt/chunk-121582-125457.r10g.xz.fragments",
    "rank7_order7_chunk_00000_05000.r7g.xz.fragments",
    "rank7_order7_chunk_05000_15000.r7g.xz.fragments",
    "rank7_order7_chunk_15000_25000.r7g.xz.fragments",
    "rank7_order7_chunk_25000_33000.r7g.xz.fragments",
    "rank7_order7_chunk_29000_32000.r7g.xz.fragments",
    "rank7_order7_chunk_32000_35000.r7g.xz.fragments",
    "rank7_order7_chunk_33000_40964.r7g.xz.fragments",
    "rank7_order7_chunk_35000_38000.r7g.xz.fragments",
    "rank7_order7_chunk_38000_40964.r7g.xz.fragments",
    "rank7_order8_chunk_000000_005000.r7o8g.xz.fragments",
)

PRESERVED_RESTART_DIRECTORIES = (
    "rank7_order8_chunk_005000_010000.r7o8g.xz.fragments",
    "rank7_order8_chunk_010000_015000.r7o8g.xz.fragments",
    "rank7_order8_chunk_015000_020000.r7o8g.xz.fragments",
    "rank7_order8_chunk_020000_025000.r7o8g.xz.fragments",
)

MERGED_OUTPUT_OVERRIDES = {
    "rank7_order7_chunk_25000_33000.r7g.xz.fragments": (
        "rank7_order7_chunk_25000_29000.r7g.xz",
        "rank7_order7_chunk_29000_32000.r7g.xz",
        "rank7_order7_chunk_32000_35000.r7g.xz",
    ),
    "rank7_order7_chunk_33000_40964.r7g.xz.fragments": (
        "rank7_order7_chunk_32000_35000.r7g.xz",
        "rank7_order7_chunk_35000_38000.r7g.xz",
        "rank7_order7_chunk_38000_40964.r7g.xz",
    ),
}

LATEX_JUNK = (
    "all-tetracyclic-cacti/paper.aux",
    "all-tetracyclic-cacti/paper.log",
    "all-tetracyclic-cacti/paper.out",
    "sharp-cactus-dnn/paper.aux",
    "sharp-cactus-dnn/paper.fdb_latexmk",
    "sharp-cactus-dnn/paper.fls",
    "sharp-cactus-dnn/paper.log",
    "sharp-cactus-dnn/paper.out",
)


def merged_outputs(relative: str, fragment_directory: Path) -> tuple[Path, ...]:
    overrides = MERGED_OUTPUT_OVERRIDES.get(relative)
    if overrides is not None:
        return tuple(EXPERIMENTS / output for output in overrides)
    return (fragment_directory.with_suffix(""),)


def is_tracked(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", "--", str(relative)],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def open_paths() -> set[Path]:
    paths: set[Path] = set()
    proc = Path("/proc")
    for process in proc.iterdir():
        if not process.name.isdigit() or int(process.name) == os.getpid():
            continue
        fd_directory = process / "fd"
        try:
            descriptors = tuple(fd_directory.iterdir())
        except (FileNotFoundError, PermissionError):
            continue
        for descriptor in descriptors:
            try:
                target = descriptor.resolve(strict=True)
            except (FileNotFoundError, PermissionError, OSError):
                continue
            try:
                target.relative_to(ROOT)
            except ValueError:
                continue
            paths.add(target)
    return paths


def in_directory(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
        return True
    except ValueError:
        return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="perform the audited removals")
    args = parser.parse_args()

    active_paths = open_paths()
    removed = skipped = 0
    for relative in SUPERSEDED_FRAGMENT_DIRECTORIES:
        directory = EXPERIMENTS / relative
        outputs = merged_outputs(relative, directory)
        if not directory.exists():
            continue
        if not all(output.is_file() and is_tracked(output) for output in outputs):
            print(f"KEEP no committed merged pack: {directory.relative_to(ROOT)}")
            skipped += 1
            continue
        if any(in_directory(path, directory) or path in outputs for path in active_paths):
            print(f"KEEP active path: {directory.relative_to(ROOT)}")
            skipped += 1
            continue
        print(f"{'REMOVE' if args.apply else 'WOULD REMOVE'} {directory.relative_to(ROOT)}")
        if args.apply:
            shutil.rmtree(directory)
        removed += 1

    for relative in PRESERVED_RESTART_DIRECTORIES:
        directory = EXPERIMENTS / relative
        if directory.exists():
            print(f"KEEP incomplete restart: {directory.relative_to(ROOT)}")

    for relative in LATEX_JUNK:
        path = ROOT / relative
        if not path.exists():
            continue
        if path in active_paths:
            print(f"KEEP active path: {path.relative_to(ROOT)}")
            skipped += 1
            continue
        print(f"{'REMOVE' if args.apply else 'WOULD REMOVE'} {path.relative_to(ROOT)}")
        if args.apply:
            path.unlink()
        removed += 1

    mode = "removed" if args.apply else "selected"
    print(f"{mode}={removed} skipped={skipped}")


if __name__ == "__main__":
    main()
