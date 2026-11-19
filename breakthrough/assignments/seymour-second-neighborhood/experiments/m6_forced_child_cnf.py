#!/usr/bin/env python3
"""Emit a versioned forced C-layer child of the frozen m=6 parent gate."""

import argparse
import hashlib
from collections import Counter
from pathlib import Path

import m6_parent_cnf as parent

HERE = Path(__file__).resolve().parent
FORMAT = "m6-forced-child-cnf-v1"
MANIFEST_FORMAT = "m6-forced-child-eligible-v1"
ELIGIBLE_COUNTS = {"B6": 14649, "B7": 25766}
ELIGIBLE_ROWS = sum(ELIGIBLE_COUNTS.values())
MANIFEST_BYTES = 1131918
MANIFEST_SHA256 = "751da64e518bc3c880e3cb02b8aa8cdf1a7bcc5e1aff4d16abfc8a42d2cc1950"


def hole_parameters(row):
    totals = Counter()
    for left, right in row["edges"]:
        cells = sorted((row["word"][left], row["word"][right]), key="RABC".index)
        totals["".join(cells)] += 1
    lam = totals["RC"] + totals["AC"] + totals["CC"]
    q = totals["BC"]
    return lam, q, 6 - lam - q


def is_eligible(row):
    # If t is the number of high C vertices and r=e(C,B), exact C-row sums give
    # t=6-lambda+r in B6 and t=3-lambda+r in B7.  Since t<=|C| and r>=0,
    # lambda=3 (B6) and lambda=1 (B7) force respectively (t,r)=(3,0),(2,0).
    lam, _, _ = hole_parameters(row)
    return lam == (3 if row["branch"] == "B6" else 1)


def eligible_rows(rows, statuses):
    result = []
    accepted_ordinal = 0
    for row, status in zip(rows, statuses):
        if status == 0:
            if is_eligible(row):
                result.append((accepted_ordinal, row))
            accepted_ordinal += 1
    counts = Counter(row["branch"] for _, row in result)
    if len(result) != ELIGIBLE_ROWS or counts != Counter(ELIGIBLE_COUNTS):
        raise RuntimeError(f"forced-child eligible partition changed: {counts}")
    return result


def manifest_payload(eligible):
    lines = [
        MANIFEST_FORMAT,
        f"cover-sha256\t{parent.COVER_SHA256}",
        f"filter-sha256\t{parent.FILTER_SHA256}",
        f"count\t{len(eligible)}",
        "branch-counts\tB6:14649;B7:25766",
        "columns\tchild-ordinal,accepted-ordinal,cover-index,branch,lambda,q,h",
    ]
    for child_ordinal, (accepted_ordinal, row) in enumerate(eligible):
        lam, q, h = hole_parameters(row)
        lines.append(
            f"{child_ordinal:05d}\t{accepted_ordinal:05d}\t{row['cover_index']:06d}\t"
            f"{row['branch']}\t{lam}\t{q}\t{h}"
        )
    return ("\n".join(lines) + "\n").encode("ascii")


def select_eligible(eligible, child_ordinal=None, accepted_ordinal=None, cover_index=None):
    supplied = sum(value is not None for value in (child_ordinal, accepted_ordinal, cover_index))
    if supplied != 1:
        raise ValueError("select exactly one child ordinal, accepted ordinal, or cover index")
    if child_ordinal is not None:
        if not 0 <= child_ordinal < len(eligible):
            raise ValueError("child ordinal out of range")
        accepted, row = eligible[child_ordinal]
        return child_ordinal, accepted, row
    key = accepted_ordinal if accepted_ordinal is not None else cover_index
    field = 0 if accepted_ordinal is not None else 1
    for child, (accepted, row) in enumerate(eligible):
        candidate = accepted if field == 0 else row["cover_index"]
        if candidate == key:
            return child, accepted, row
    raise ValueError("selected parent is absent or not in a forced regime")


def forced_suffix(cnf, branch):
    labels = parent.CELL_LABELS[branch]
    b_labels, c_labels = labels[2], labels[3]
    orientation = [(-cnf.names[f"a_{c}_{b}"],) for c in c_labels for b in b_labels]
    high = [(cnf.names[f"cnt_d1_{c}_17_9"],) for c in c_labels]
    return orientation + high


def build_child(row):
    cnf, embedding, holes = parent.build_parent(row)
    suffix = forced_suffix(cnf, row["branch"])
    cnf.clauses.extend(suffix)
    return cnf, embedding, holes, suffix


def write_child(path, cnf, child_ordinal, accepted_ordinal, row, embedding, holes,
                manifest_bytes, manifest_sha256):
    branch = row["branch"]
    lam, q, h = hole_parameters(row)
    parent_clauses = parent.BASE_CLAUSES[branch] + len(parent.PAIRS)
    orientation_units = len(parent.CELL_LABELS[branch][2]) * len(parent.CELL_LABELS[branch][3])
    high_units = len(parent.CELL_LABELS[branch][3])
    metadata = [
        ("format", FORMAT), ("cover-sha256", parent.COVER_SHA256),
        ("filter-sha256", parent.FILTER_SHA256),
        ("eligible-manifest-format", MANIFEST_FORMAT),
        ("eligible-manifest-bytes", str(manifest_bytes)),
        ("eligible-manifest-sha256", manifest_sha256),
        ("eligible-count", str(ELIGIBLE_ROWS)),
        ("eligible-branch-counts", "B6:14649;B7:25766"),
        ("child-ordinal", str(child_ordinal)),
        ("accepted-ordinal", str(accepted_ordinal)),
        ("cover-index", str(row["cover_index"])), ("branch", branch),
        ("b-size", "6" if branch == "B6" else "7"),
        ("support-index", str(row["support"])), ("support-order", str(row["order"])),
        ("support-code", row["code"]), ("placement", row["word"]),
        ("orbit-weight", str(row["weight"])),
        ("embedding", ",".join(f"{key}:{embedding[key]}" for key in sorted(embedding))),
        ("holes", ",".join(f"{left}-{right}" for left, right in sorted(holes))),
        ("lambda", str(lam)), ("q", str(q)), ("h", str(h)), ("r", "0"),
        ("high-c", ",".join(map(str, parent.CELL_LABELS[branch][3]))),
        ("model", "generate(18,bsize,6,robust_witness=True,arc_minimal=True)"),
        ("base-variables", str(parent.BASE_VARIABLES)),
        ("base-variable-map-sha256", parent.BASE_VARIABLE_MAP_SHA256),
        ("base-clauses", str(parent.BASE_CLAUSES[branch])),
        ("base-clause-sha256", parent.BASE_CLAUSE_SHA256[branch]),
        ("hole-units", str(len(parent.PAIRS))), ("parent-clauses", str(parent_clauses)),
        ("orientation-units", str(orientation_units)), ("high-c-units", str(high_units)),
    ]
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for key, value in metadata:
            handle.write(f"c {key} {value}\n")
        for name, number in cnf.names.items():
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    selector = parser.add_mutually_exclusive_group()
    selector.add_argument("--child-ordinal", type=int)
    selector.add_argument("--accepted-ordinal", type=int)
    selector.add_argument("--cover-index", type=int)
    parser.add_argument("--cover", type=Path, default=parent.COVER)
    parser.add_argument("--filter", type=Path, default=parent.FILTER)
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output is None and args.manifest_output is None:
        parser.error("at least one of --output and --manifest-output is required")
    if args.output is not None and all(value is None for value in
                                       (args.child_ordinal, args.accepted_ordinal, args.cover_index)):
        parser.error("--output requires a selector")
    rows = parent.load_cover(args.cover)
    statuses = parent.load_statuses(args.filter)
    eligible = eligible_rows(rows, statuses)
    manifest = manifest_payload(eligible)
    digest = hashlib.sha256(manifest).hexdigest()
    if MANIFEST_BYTES and (len(manifest) != MANIFEST_BYTES or digest != MANIFEST_SHA256):
        raise RuntimeError("eligible manifest differs from frozen fingerprint")
    if args.manifest_output:
        args.manifest_output.write_bytes(manifest)
    if args.output:
        child, accepted, row = select_eligible(
            eligible, args.child_ordinal, args.accepted_ordinal, args.cover_index)
        cnf, embedding, holes, suffix = build_child(row)
        write_child(args.output, cnf, child, accepted, row, embedding, holes,
                    len(manifest), digest)
        print(
            f"child_ordinal={child} accepted_ordinal={accepted} cover_index={row['cover_index']} "
            f"branch={row['branch']} lambda={hole_parameters(row)[0]} r=0 "
            f"vars={len(cnf.names)} clauses={len(cnf.clauses)} child_units={len(suffix)} "
            f"output={args.output}"
        )
    print(f"eligible={len(eligible)} B6=14649 B7=25766 manifest_bytes={len(manifest)} sha256={digest}")


if __name__ == "__main__":
    main()
