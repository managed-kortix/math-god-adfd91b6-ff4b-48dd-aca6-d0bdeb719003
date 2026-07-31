#!/usr/bin/env python3
"""Independently authenticate a frozen-parent m=6 forced C-layer child CNF."""

import argparse
import hashlib
from collections import Counter
from pathlib import Path

from check_m6_parent_cnf import (
    BASE_CLAUSES, BASE_CLAUSE_SHA256, BASE_VARIABLES, BASE_VARIABLE_MAP_SHA256,
    COVER_ROWS, COVER_SHA256, FILTER_SHA256, LABELS, PAIRS, clause_sha256,
    expected_projection, parse_cnf, read_acceptance, read_cover, variable_map_sha256,
)
from snc_cnf import generate

HERE = Path(__file__).resolve().parent
FORMAT = "m6-forced-child-cnf-v1"
MANIFEST_FORMAT = "m6-forced-child-eligible-v1"
MANIFEST_BYTES = 1131918
MANIFEST_SHA256 = "751da64e518bc3c880e3cb02b8aa8cdf1a7bcc5e1aff4d16abfc8a42d2cc1950"
ELIGIBLE_COUNTS = Counter({"B6": 14649, "B7": 25766})


def parameters(row):
    branch, _, _, _, colors, _, holes = row
    totals = Counter()
    for left, right in holes:
        pair = "".join(sorted((colors[left], colors[right]), key="RABC".index))
        totals[pair] += 1
    lam = totals["RC"] + totals["AC"] + totals["CC"]
    q = totals["BC"]
    return branch, lam, q, 6 - lam - q


def eligible_indices(rows, statuses):
    result = []
    accepted = 0
    for index, (row, status) in enumerate(zip(rows, statuses)):
        if status == 0:
            branch, lam, _, _ = parameters(row)
            # Independently apply t=6-lambda+r (B6), t=3-lambda+r (B7),
            # t<=|C|, and r>=0: lambda 3/1 forces all C high and r=0.
            if lam == (3 if branch == "B6" else 1):
                result.append((accepted, index))
            accepted += 1
    if Counter(rows[index][0] for _, index in result) != ELIGIBLE_COUNTS:
        raise RuntimeError("independently derived eligible partition changed")
    return result


def manifest_payload(rows, eligible):
    lines = [
        MANIFEST_FORMAT,
        f"cover-sha256\t{COVER_SHA256}",
        f"filter-sha256\t{FILTER_SHA256}",
        f"count\t{len(eligible)}",
        "branch-counts\tB6:14649;B7:25766",
        "columns\tchild-ordinal,accepted-ordinal,cover-index,branch,lambda,q,h",
    ]
    for child, (accepted, index) in enumerate(eligible):
        branch, lam, q, h = parameters(rows[index])
        lines.append(f"{child:05d}\t{accepted:05d}\t{index:06d}\t{branch}\t{lam}\t{q}\t{h}")
    return ("\n".join(lines) + "\n").encode("ascii")


def check(cnf_path, cover_path, filter_path):
    rows = read_cover(cover_path)
    statuses = read_acceptance(filter_path)
    eligible = eligible_indices(rows, statuses)
    manifest = manifest_payload(rows, eligible)
    manifest_hash = hashlib.sha256(manifest).hexdigest()
    if len(manifest) != MANIFEST_BYTES or manifest_hash != MANIFEST_SHA256:
        raise RuntimeError("eligible index manifest fingerprint changed")

    metadata_items, variables, clauses, declared = parse_cnf(cnf_path)
    metadata = dict(metadata_items)
    child = int(metadata.get("child-ordinal", "-1"))
    if not 0 <= child < len(eligible):
        raise RuntimeError("child ordinal is outside the eligible manifest")
    accepted, index = eligible[child]
    row = rows[index]
    branch, support, order, code, word, weight, _ = row
    _, lam, q, h = parameters(row)
    image, holes = expected_projection(row)
    c_labels = tuple(LABELS[branch]["C"])
    b_labels = tuple(LABELS[branch]["B"])
    expected_embedding = ",".join(f"{key}:{image[key]}" for key in sorted(image))
    expected_holes = ",".join(f"{left}-{right}" for left, right in sorted(holes))
    parent_clauses = BASE_CLAUSES[branch] + len(PAIRS)
    expected_metadata = [
        ("format", FORMAT), ("cover-sha256", COVER_SHA256),
        ("filter-sha256", FILTER_SHA256), ("eligible-manifest-format", MANIFEST_FORMAT),
        ("eligible-manifest-bytes", str(MANIFEST_BYTES)),
        ("eligible-manifest-sha256", MANIFEST_SHA256),
        ("eligible-count", str(len(eligible))),
        ("eligible-branch-counts", "B6:14649;B7:25766"),
        ("child-ordinal", str(child)), ("accepted-ordinal", str(accepted)),
        ("cover-index", str(index)), ("branch", branch),
        ("b-size", "6" if branch == "B6" else "7"),
        ("support-index", str(support)), ("support-order", str(order)),
        ("support-code", code), ("placement", word), ("orbit-weight", str(weight)),
        ("embedding", expected_embedding), ("holes", expected_holes),
        ("lambda", str(lam)), ("q", str(q)), ("h", str(h)), ("r", "0"),
        ("high-c", ",".join(map(str, c_labels))),
        ("model", "generate(18,bsize,6,robust_witness=True,arc_minimal=True)"),
        ("base-variables", str(BASE_VARIABLES)),
        ("base-variable-map-sha256", BASE_VARIABLE_MAP_SHA256),
        ("base-clauses", str(BASE_CLAUSES[branch])),
        ("base-clause-sha256", BASE_CLAUSE_SHA256[branch]),
        ("hole-units", str(len(PAIRS))), ("parent-clauses", str(parent_clauses)),
        ("orientation-units", str(len(c_labels) * len(b_labels))),
        ("high-c-units", str(len(c_labels))),
    ]
    if metadata_items != expected_metadata:
        raise RuntimeError("metadata is not the exact canonical eligible-row record")

    base = generate(18, 6 if branch == "B6" else 7, 6,
                    robust_witness=True, arc_minimal=True)
    expected_names = list(base.names)
    expected_base = list(base.clauses)
    if (len(expected_names) != BASE_VARIABLES or
            variable_map_sha256(expected_names) != BASE_VARIABLE_MAP_SHA256 or
            len(expected_base) != BASE_CLAUSES[branch] or
            clause_sha256(expected_base) != BASE_CLAUSE_SHA256[branch]):
        raise RuntimeError("reconstructed exact parent base misses its committed fingerprint")
    expected_hole_units = [
        (base.names[f"h_{left}_{right}"] if (left, right) in holes else
         -base.names[f"h_{left}_{right}"],)
        for left, right in PAIRS
    ]
    expected_orientation = [(-base.names[f"a_{c}_{b}"],) for c in c_labels for b in b_labels]
    expected_high = [(base.names[f"cnt_d1_{c}_17_9"],) for c in c_labels]
    expected_clauses = expected_base + expected_hole_units + expected_orientation + expected_high
    if variables != expected_names:
        raise RuntimeError("variable map is not the exact committed parent map")
    if clauses[:BASE_CLAUSES[branch]] != expected_base:
        raise RuntimeError("exact parent base prefix authentication failed")
    if clauses[BASE_CLAUSES[branch]:parent_clauses] != expected_hole_units:
        raise RuntimeError("exact parent hole-unit prefix authentication failed")
    if clauses[parent_clauses:] != expected_orientation + expected_high:
        raise RuntimeError("exact forced-child suffix authentication failed")
    if clauses != expected_clauses or declared != (BASE_VARIABLES, len(expected_clauses)):
        raise RuntimeError("child CNF framing differs from exact prefix plus suffix")
    print(
        f"PASS child_ordinal={child} accepted_ordinal={accepted} cover_index={index} "
        f"branch={branch} lambda={lam} q={q} h={h} r=0 high_c={len(c_labels)} "
        f"orientation_units={len(expected_orientation)} clauses={len(clauses)}"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--cover", type=Path, default=HERE / "m6-placement-cover.txt")
    parser.add_argument("--filter", type=Path, default=HERE / "m6-placement-filter.txt")
    args = parser.parse_args()
    check(args.cnf, args.cover, args.filter)


if __name__ == "__main__":
    main()
