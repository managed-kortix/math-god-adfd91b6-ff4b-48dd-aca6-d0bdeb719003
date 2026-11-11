#!/usr/bin/env python3
"""Compose all certified chunks and close the four frozen B7-l2 profiles."""

import argparse
from pathlib import Path
import subprocess
import sys

import check_m6_b7_l2_parent_chunk_cover as cover

HERE = Path(__file__).resolve().parent


def audit():
    import verify_m6_b7_l2_parent_chunk_certificates as certificates

    metadata, rows = certificates.load_ledger()
    certificates.verify_bindings(metadata)
    certificates.artifact_paths(rows)
    profiles, leaves = cover.derive_cover()
    if len(rows) != 652 or len(leaves) != 652:
        raise RuntimeError("certificate/leaf composition scope changed")
    for ordinal, (row, leaf) in enumerate(zip(rows, leaves)):
        position, key, chunk, start, stop, members = leaf
        expected = (f"{ordinal:03d}", f"{position:02d}", f"{chunk:03d}", f"{start:04d}",
                    f"{stop:04d}", str(len(members)))
        observed = tuple(row[name] for name in ("leaf", "profile", "chunk", "start", "stop", "parents"))
        if observed != expected or row["key"] != f"p{position:02d}-c{chunk:03d}":
            raise RuntimeError("certificate row does not compose with independent cover")
    parent_sets = []
    for position in range(4):
        members = [(accepted, index) for leaf in leaves if leaf[0] == position for accepted, index, _ in leaf[-1]]
        parent_sets.append(members)
    if any(len(items) != 8119 or len(set(items)) != 8119 for items in parent_sets) or \
            sum(len(leaf[-1]) for leaf in leaves) != 32476:
        raise RuntimeError("four-profile parent closure changed")
    print("PASS closure=652/652 leaves profiles=4 disjoint=yes exhaustive=yes")
    print("PASS parents=8119 profile_parent_incidences=32476")
    print("PASS implication=entire-clean-B7-l2-parent-campaign-closed other-residual-groups=not-claimed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checker", type=Path)
    parser.add_argument("--representative-replay", action="store_true")
    args = parser.parse_args()
    audit()
    if args.representative_replay:
        if args.checker is None:
            parser.error("--representative-replay requires --checker")
        verifier = HERE / "verify_m6_b7_l2_parent_chunk_certificates.py"
        subprocess.run([sys.executable, str(verifier), "--checker", str(args.checker.resolve(strict=True)),
                        "--representative"], check=True)
        audit()


if __name__ == "__main__":
    main()
