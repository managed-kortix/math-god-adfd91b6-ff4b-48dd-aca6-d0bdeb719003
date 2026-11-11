#!/usr/bin/env python3
"""Emit the exact clean B6-l6 parent group with fresh root cardinalities."""

import argparse
import hashlib
from pathlib import Path

import m6_clean_sink_group_cnf as source
from snc_cnf import threshold

HERE = Path(__file__).resolve().parent
PREFIX = "m6-clean-sink-B6-l6-root-cardinality"
FORMAT = f"{PREFIX}-cnf-v1"
MANIFEST_FORMAT = f"{PREFIX}-manifest-v1"
HASH_FORMAT = f"{PREFIX}-hashes-v1"
GROUP = "B6-l6"
A = tuple(range(1, 9))
B = tuple(range(9, 15))
C = tuple(range(15, 18))


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def extend(cnf):
    before = len(cnf.names), len(cnf.clauses)
    highs = tuple(cnf.names[f"cnt_d1_{v}_17_9"] for v in range(18))
    edges = tuple(cnf.names[f"a_{a}_{b}"] for a in A for b in B)
    holes = tuple(cnf.names[f"h_{a}_{b}"] for i, a in enumerate(A) for b in A[i + 1:])
    high_a = tuple(cnf.names[f"cnt_d1_{a}_17_9"] for a in A)
    global_count = threshold(cnf, highs, "clean_B6_l6_global_high")
    edge_count = threshold(cnf, edges, "clean_B6_l6_AB_edges")
    rhs_count = threshold(cnf, holes + high_a, "clean_B6_l6_A_holes_high")
    cnf.add(global_count[2])
    cnf.add(-global_count[3])
    cnf.add(edge_count[35])
    for offset, rhs in enumerate(rhs_count, 1):
        if 36 + offset <= len(edge_count):
            cnf.add(-rhs, edge_count[35 + offset])
            cnf.add(rhs, -edge_count[35 + offset])
        else:
            cnf.add(-rhs)
    return len(cnf.names) - before[0], len(cnf.clauses) - before[1]


def build():
    groups = source.load_groups()
    members = groups[GROUP]
    cnf, selectors = source.build_group(GROUP, members)
    delta = extend(cnf)
    if len(members) != 220 or delta != (2013, 7899):
        raise RuntimeError("exact B6-l6 scope or fresh-counter dimensions changed")
    return members, cnf, selectors, delta


def manifest_payload(members, cnf, delta):
    bindings = {
        "clean-parent-manifest": HERE / "m6-clean-sink-selector-groups.tsv",
        "clean-remaining-stream": HERE / "m6-clean-sink-remaining.tsv",
        "clean-partition-manifest": HERE / "m6-clean-sink-manifest.tsv",
        "clean-sink-theorem": HERE.parent / "attempts" / "tick52-rooted-clean-sink-theorem.md",
    }
    lines = [MANIFEST_FORMAT, "scope\texact-clean-B6-l6-parent-group",
             "group\tB6-l6", "parents\t220", "branch\tB6", "lambda\t6",
             "layers\tR:0;A:1-8;B:9-14;C:15-17", "layer-sizes\tR:1;A:8;B:6;C:3",
             "A-to-C\tabsent", "global-arcs\t147", "global-high\t3",
             "root-identity\te(A,B)=36+H(A)+high(A)",
             "root-proof\tsum_A d+=64+high(A);e(A,A)=28-H(A);A cannot send to R or C",
             f"added-variables\t{delta[0]}", f"added-clauses\t{delta[1]}",
             f"variables\t{len(cnf.names)}", f"clauses\t{len(cnf.clauses)}"]
    for name, path in bindings.items():
        size, digest = identity(path)
        lines.extend((f"{name}-bytes\t{size}", f"{name}-sha256\t{digest}"))
    lines.append(f"member-sha256\t{hashlib.sha256(source.member_payload(members)).hexdigest()}")
    return ("\n".join(lines) + "\n").encode("ascii")


def metadata(manifest, delta):
    return [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
            ("manifest-bytes", str(len(manifest))),
            ("manifest-sha256", hashlib.sha256(manifest).hexdigest()), ("group", GROUP),
            ("parents", "220"), ("layers", "R:1,A:8,B:6,C:3"), ("A-to-C", "absent"),
            ("global-high", "3"), ("root-identity", "e(A,B)=36+H(A)+high(A)"),
            ("cardinality-added-variables", str(delta[0])),
             ("cardinality-added-clauses", str(delta[1])), ("lrat-status", "checked")]


def hash_payload(members, cnf, manifest, cnf_identity=("", "")):
    size, digest = cnf_identity
    lines = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
             f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}", "groups\t1",
             "columns\tgroup,parents,variables,clauses,cnf-bytes,cnf-sha256",
             f"{GROUP}\t{len(members)}\t{len(cnf.names)}\t{len(cnf.clauses)}\t{size}\t{digest}"]
    return ("\n".join(lines) + "\n").encode("ascii")


def write_cnf(path, cnf, manifest, delta):
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for key, value in metadata(manifest, delta):
            handle.write(f"c {key} {value}\n")
        for name, number in cnf.names.items():
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--hash-output", type=Path)
    args = parser.parse_args()
    members, cnf, _, delta = build()
    manifest = manifest_payload(members, cnf, delta)
    if args.manifest_output:
        args.manifest_output.write_bytes(manifest)
    if args.output:
        write_cnf(args.output, cnf, manifest, delta)
        print(f"PASS cnf_bytes={identity(args.output)[0]} cnf_sha256={identity(args.output)[1]}")
    if args.hash_output:
        cnf_identity = identity(args.output) if args.output else ("", "")
        args.hash_output.write_bytes(hash_payload(members, cnf, manifest, cnf_identity))
    print(f"PASS parents=220 manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


if __name__ == "__main__":
    main()
