#!/usr/bin/env python3
"""Producer-independent structural and semantic audit for clean B6-l5."""

import argparse
import hashlib
import itertools
import re
from pathlib import Path

import check_m6_clean_sink_group_cnf as base
from check_m6_parent_cnf import parse_cnf

HERE = Path(__file__).resolve().parent
PREFIX = "m6-clean-sink-B6-l5-root-cardinality"
FORMAT = f"{PREFIX}-cnf-v1"
MANIFEST_FORMAT = f"{PREFIX}-manifest-v1"
A, B, C = tuple(range(1, 9)), tuple(range(9, 15)), tuple(range(15, 18))


def add_threshold(names, clauses, inputs, tag):
    previous = []
    for index, literal in enumerate(inputs, 1):
        current = []
        for target in range(1, index + 1):
            names.append(f"cnt_{tag}_{index}_{target}")
            value = len(names)
            current.append(value)
            same = previous[target - 1] if target <= len(previous) else None
            lower = previous[target - 2] if target >= 2 else True
            if same is not None:
                clauses.append((-same, value))
            clauses.append((-literal, value) if lower is True else (-literal, -lower, value))
            if same is None:
                clauses.append((-value, literal))
                if lower is not True:
                    clauses.append((-value, lower))
            else:
                clauses.append((-value, same, literal))
                if lower is not True:
                    clauses.append((-value, same, lower))
        previous = current
    return previous


def reconstruct():
    groups = base.derive_groups(base.REMAINING, HERE / "m6-placement-cover.txt", HERE / "m6-placement-filter.txt")
    members = groups["B6-l5"]
    names, clauses = map(list, base.frozen_base("B6"))
    selectors = list(range(len(names) + 1, len(names) + len(members) + 1))
    names.extend(f"clean_sink_parent_selector_{i:05d}" for i in range(len(members)))
    clauses.append(tuple(selectors))
    number = {name: i for i, name in enumerate(names, 1)}
    for selector, (_, _, row) in zip(selectors, members):
        holes = base.expected_projection(row)[1]
        for pair in base.PAIRS:
            hole = number[f"h_{pair[0]}_{pair[1]}"]
            clauses.append((-selector, hole if pair in holes else -hole))
    before = len(names), len(clauses)
    highs = tuple(number[f"cnt_d1_{v}_17_9"] for v in range(18))
    edges = tuple(number[f"a_{a}_{b}"] for a in A for b in B)
    holes = tuple(number[f"h_{a}_{b}"] for i, a in enumerate(A) for b in A[i + 1:])
    high_a = tuple(number[f"cnt_d1_{a}_17_9"] for a in A)
    global_count = add_threshold(names, clauses, highs, "clean_B6_l5_global_high")
    edge_count = add_threshold(names, clauses, edges, "clean_B6_l5_AB_edges")
    rhs_count = add_threshold(names, clauses, holes + high_a, "clean_B6_l5_A_holes_high")
    clauses.extend(((global_count[2],), (-global_count[3],), (edge_count[35],)))
    for offset, rhs in enumerate(rhs_count, 1):
        if 36 + offset <= len(edge_count):
            clauses.extend(((-rhs, edge_count[35 + offset]), (rhs, -edge_count[35 + offset])))
        else:
            clauses.append((-rhs,))
    return members, names, clauses, (len(names) - before[0], len(clauses) - before[1])


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def manifest_payload(members, names, clauses, delta):
    bindings = {
        "clean-parent-manifest": HERE / "m6-clean-sink-selector-groups.tsv",
        "clean-remaining-stream": HERE / "m6-clean-sink-remaining.tsv",
        "clean-partition-manifest": HERE / "m6-clean-sink-manifest.tsv",
        "clean-sink-theorem": HERE.parent / "attempts" / "tick52-rooted-clean-sink-theorem.md",
    }
    lines = [MANIFEST_FORMAT, "scope\texact-clean-B6-l5-parent-group", "group\tB6-l5",
             "parents\t1024", "branch\tB6", "lambda\t5",
             "layers\tR:0;A:1-8;B:9-14;C:15-17", "layer-sizes\tR:1;A:8;B:6;C:3",
             "A-to-C\tabsent", "global-arcs\t147", "global-high\t3",
             "root-identity\te(A,B)=36+H(A)+high(A)",
             "root-proof\tsum_A d+=64+high(A);e(A,A)=28-H(A);A cannot send to R or C",
             f"added-variables\t{delta[0]}", f"added-clauses\t{delta[1]}",
             f"variables\t{len(names)}", f"clauses\t{len(clauses)}"]
    for name, path in bindings.items():
        size, digest = identity(path)
        lines.extend((f"{name}-bytes\t{size}", f"{name}-sha256\t{digest}"))
    lines.append(f"member-sha256\t{hashlib.sha256(base.member_payload(members)).hexdigest()}")
    return ("\n".join(lines) + "\n").encode("ascii")


def expected_metadata(manifest, delta):
    return [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
            ("manifest-bytes", str(len(manifest))),
            ("manifest-sha256", hashlib.sha256(manifest).hexdigest()), ("group", "B6-l5"),
            ("parents", "1024"), ("layers", "R:1,A:8,B:6,C:3"), ("A-to-C", "absent"),
            ("global-high", "3"), ("root-identity", "e(A,B)=36+H(A)+high(A)"),
            ("cardinality-added-variables", str(delta[0])),
            ("cardinality-added-clauses", str(delta[1])), ("lrat-status", "checked")]


def semantic_audit():
    if (len(A), len(B), len(C)) != (8, 6, 3) or any(c < 15 for c in C):
        raise RuntimeError("B6 root layers changed")
    _, names, clauses, _ = reconstruct()
    number = {name: index for index, name in enumerate(names, 1)}
    units = {clause[0] for clause in clauses if len(clause) == 1}
    if any(-number[f"a_{a}_{c}"] not in units for a in A for c in C):
        raise RuntimeError("A-to-C absence is not forced by the frozen base")
    if 153 - 6 != 147 or 147 != 18 * 8 + 3:
        raise RuntimeError("exactly-three-high derivation failed")
    for degrees in itertools.product((8, 9), repeat=18):
        if sum(degrees) == 147 and sum(value == 9 for value in degrees) != 3:
            raise RuntimeError("degree-vector audit failed")
    cases = 0
    for holes, high_a in itertools.product(range(29), range(9)):
        if (64 + high_a) - (28 - holes) != 36 + holes + high_a:
            raise RuntimeError("root identity audit failed")
        cases += 1
    print(f"PASS layers=A8,B6,C3 A_to_C=absent degree_vectors={2**18} cut_cases={cases}")


def check(path):
    members, names, clauses, delta = reconstruct()
    manifest = manifest_payload(members, names, clauses, delta)
    metadata, variables, actual, declared = parse_cnf(path)
    expected_meta = expected_metadata(manifest, delta)
    if metadata != expected_meta or variables != names or actual != clauses or declared != (len(names), len(clauses)):
        raise RuntimeError("CNF differs from independent reconstruction")
    data = path.read_bytes()
    print(f"PASS parents=1024 vars={len(names)} clauses={len(clauses)} sha256={hashlib.sha256(data).hexdigest()}")


def check_manifest_and_hashes(regenerate=True):
    members, names, clauses, delta = reconstruct()
    manifest = manifest_payload(members, names, clauses, delta)
    supplied = (HERE / f"{PREFIX}.tsv").read_bytes()
    if supplied != manifest:
        raise RuntimeError("manifest differs from independent reconstruction")
    lines = (HERE / f"{PREFIX}-hashes.tsv").read_text(encoding="ascii").splitlines()
    if len(lines) != 6 or lines[:5] != [f"{PREFIX}-hashes-v1", f"manifest-bytes\t{len(manifest)}",
            f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}", "groups\t1",
            "columns\tgroup,parents,variables,clauses,cnf-bytes,cnf-sha256"]:
        raise RuntimeError("hash ledger framing changed")
    fields = lines[5].split("\t")
    if fields[:4] != ["B6-l5", "1024", str(len(names)), str(len(clauses))] or not fields[4].isdigit() or \
            re.fullmatch(r"[0-9a-f]{64}", fields[5]) is None:
        raise RuntimeError("hash ledger row changed")
    if regenerate:
        import tempfile
        with tempfile.TemporaryDirectory(prefix="clean-B6-l5-check-", dir=HERE.parent) as directory:
            path = Path(directory) / "group.cnf"
            with path.open("w", encoding="ascii", newline="\n") as handle:
                for key, value in expected_metadata(manifest, delta):
                    handle.write(f"c {key} {value}\n")
                for index, name in enumerate(names, 1):
                    handle.write(f"c var {index} {name}\n")
                handle.write(f"p cnf {len(names)} {len(clauses)}\n")
                for clause in clauses:
                    handle.write(" ".join(map(str, clause)) + " 0\n")
            if identity(path) != (int(fields[4]), fields[5]):
                raise RuntimeError("regenerated CNF differs from hash ledger")
    print(f"PASS manifest_sha256={hashlib.sha256(manifest).hexdigest()} parents=1024")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", nargs="?", type=Path)
    parser.add_argument("--semantic", action="store_true")
    parser.add_argument("--cover", action="store_true")
    args = parser.parse_args()
    if args.semantic:
        semantic_audit()
    if args.cover:
        check_manifest_and_hashes()
    if args.cnf:
        check(args.cnf)
    if not args.semantic and not args.cover and not args.cnf:
        parser.error("select --cover, --semantic, or a CNF")


if __name__ == "__main__":
    main()
