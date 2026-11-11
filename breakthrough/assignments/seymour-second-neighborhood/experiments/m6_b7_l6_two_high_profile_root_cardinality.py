#!/usr/bin/env python3
"""Strengthen the exact 19 remaining two-high early C-profile cells."""

import argparse
import hashlib
import tempfile
from pathlib import Path

import m6_b7_l6_early_c_profile_census as census
from snc_cnf import threshold

HERE = Path(__file__).resolve().parent
PREFIX = "m6-b7-l6-two-high-profile-root-cardinality"
FORMAT = f"{PREFIX}-cnf-v1"
MANIFEST_FORMAT = f"{PREFIX}-manifest-v1"
HASH_FORMAT = f"{PREFIX}-hashes-v1"
SCOPE = (12, 13, 14, 15, 16, 17, 36, 37, 38, 39, 40, 41, 42, 43, 55, 56, 57, 58, 59)
A = tuple(range(1, 9))
B = tuple(range(9, 16))


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def scope():
    orbits = census.load_orbits()
    timeout = {i for i, status, _, _ in census.scout_sequence(orbits) if status == "TIMEOUT"}
    one_high = {3, 11, 23, 25, 28, 47, 49, 54}
    if tuple(sorted(timeout - one_high)) != SCOPE or any(orbits[i][3][2] != (1, 1) for i in SCOPE):
        raise RuntimeError("exact remaining two-high profile scope changed")
    return orbits


def extend(cnf):
    before = len(cnf.names), len(cnf.clauses)
    high_all = tuple(cnf.names[f"cnt_d1_{v}_17_9"] for v in range(18))
    edges = tuple(cnf.names[f"a_{a}_{b}"] for a in A for b in B)
    holes = tuple(cnf.names[f"h_{a}_{b}"] for i, a in enumerate(A) for b in A[i + 1:])
    high_a = tuple(cnf.names[f"cnt_d1_{a}_17_9"] for a in A)
    global_count = threshold(cnf, high_all, "root_audit_global_high")
    edge_count = threshold(cnf, edges, "root_audit_AB_edges")
    rhs_count = threshold(cnf, holes + high_a, "root_audit_A_holes_high")
    cnf.add(global_count[2])
    cnf.add(-global_count[3])
    cnf.add(edge_count[35])
    for offset in range(1, len(rhs_count) + 1):
        if 36 + offset <= len(edge_count):
            cnf.add(-rhs_count[offset - 1], edge_count[35 + offset])
            cnf.add(rhs_count[offset - 1], -edge_count[35 + offset])
        else:
            cnf.add(-rhs_count[offset - 1])
    return len(cnf.names) - before[0], len(cnf.clauses) - before[1]


def build(ordinal, orbits):
    cnf, selectors = census.build_orbit(orbits[ordinal])
    return cnf, selectors, extend(cnf)


def manifest_payload(orbits):
    census_paths = {
        "census-manifest": HERE / "m6-b7-l6-early-c-profile-census.tsv",
        "census-hashes": HERE / "m6-b7-l6-early-c-profile-hashes.tsv",
        "census-provenance": HERE / "m6-b7-l6-early-c-profile-provenance.tsv",
    }
    lines = [MANIFEST_FORMAT, "scope-orbits\t" + ",".join(f"{i:02d}" for i in SCOPE),
             "profiles\t19", "profile-high-mask\t11", "global-arcs\t147",
             "global-high\t3", "root-A\t1,2,3,4,5,6,7,8", "root-B\t9,10,11,12,13,14,15",
             "root-identity\te(A,B)=36+H(A)+high(A)",
             "root-proof\tsum_A d+=64+high(A); e(A,A)=28-H(A); A cannot send to root or C",
             "fresh-counters\t18 global-high, 56 A-to-B arcs, 28 A-holes plus eight A-high indicators",
             "added-variables\t2433", "added-clauses\t9571", "proof-status\tchecked-LRAT"]
    for name, path in census_paths.items():
        size, digest = identity(path)
        lines.extend((f"{name}-bytes\t{size}", f"{name}-sha256\t{digest}"))
    lines.append("columns\tposition,orbit,key,state-key,t,parents,variables,clauses")
    for position, ordinal in enumerate(SCOPE):
        orbit = orbits[ordinal]
        cnf, _, delta = build(ordinal, orbits)
        if delta != (2433, 9571):
            raise RuntimeError("fresh counter dimensions changed")
        lines.append(f"{position:02d}\t{ordinal:02d}\t{orbit[0]}\t{orbit[2]}\t{orbit[4]}\t"
                     f"{len(orbit[7])}\t{len(cnf.names)}\t{len(cnf.clauses)}")
    return ("\n".join(lines) + "\n").encode("ascii")


def metadata(position, ordinal, orbit, manifest, selectors, delta):
    return [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
            ("manifest-bytes", str(len(manifest))),
            ("manifest-sha256", hashlib.sha256(manifest).hexdigest()),
            ("position", str(position)), ("orbit", str(ordinal)), ("key", orbit[0]),
            ("state-key", orbit[2]), ("intersection-t", str(orbit[4])),
            ("parents", str(len(orbit[7]))), ("first-selector", str(selectors[0])),
            ("last-selector", str(selectors[-1])), ("global-high", "3"),
            ("root-identity", "e(A,B)=36+H(A)+high(A)"),
            ("cardinality-added-variables", str(delta[0])),
            ("cardinality-added-clauses", str(delta[1])), ("lrat-status", "checked")]


def write_cnf(path, position, ordinal, orbit, cnf, selectors, delta, manifest):
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in metadata(position, ordinal, orbit, manifest, selectors, delta):
            handle.write(f"c {name} {value}\n")
        for name, number in cnf.names.items():
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def hash_payload(orbits, manifest, hashes=None):
    hashes = hashes or (("", ""),) * len(SCOPE)
    lines = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
             f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}", "profiles\t19",
             "columns\tposition,orbit,key,parents,variables,clauses,cnf-bytes,cnf-sha256"]
    for position, (ordinal, (size, digest)) in enumerate(zip(SCOPE, hashes)):
        orbit = orbits[ordinal]
        cnf, _, _ = build(ordinal, orbits)
        lines.append(f"{position:02d}\t{ordinal:02d}\t{orbit[0]}\t{len(orbit[7])}\t"
                     f"{len(cnf.names)}\t{len(cnf.clauses)}\t{size}\t{digest}")
    return ("\n".join(lines) + "\n").encode("ascii")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--position", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--hash-output", type=Path)
    parser.add_argument("--populate-hashes", action="store_true")
    args = parser.parse_args()
    orbits, hashes = scope(), None
    manifest = manifest_payload(orbits)
    if args.manifest_output:
        args.manifest_output.write_bytes(manifest)
    if args.populate_hashes:
        values = []
        with tempfile.TemporaryDirectory(prefix="two-high-root-hashes-", dir=HERE.parent) as directory:
            path = Path(directory) / "profile.cnf"
            for position, ordinal in enumerate(SCOPE):
                write_cnf(path, position, ordinal, orbits[ordinal], *build(ordinal, orbits), manifest)
                values.append(identity(path))
        hashes = tuple(values)
    if args.hash_output:
        args.hash_output.write_bytes(hash_payload(orbits, manifest, hashes))
    if args.output:
        if args.position is None or not 0 <= args.position < len(SCOPE):
            parser.error("--output requires --position in 0..18")
        ordinal = SCOPE[args.position]
        write_cnf(args.output, args.position, ordinal, orbits[ordinal], *build(ordinal, orbits), manifest)
    print(f"PASS profiles=19 manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


if __name__ == "__main__":
    main()
