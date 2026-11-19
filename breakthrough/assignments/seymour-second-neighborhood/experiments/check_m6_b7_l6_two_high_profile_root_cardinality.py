#!/usr/bin/env python3
"""Producer-independent reconstruction and semantic audit of root cardinality."""

import argparse
import hashlib
import itertools
import re
import tempfile
from pathlib import Path

import check_m6_b7_l6_early_c_profile_census as census_check
from check_m6_parent_cnf import parse_cnf

HERE = Path(__file__).resolve().parent
PREFIX = "m6-b7-l6-two-high-profile-root-cardinality"
SCOPE = (12, 13, 14, 15, 16, 17, 36, 37, 38, 39, 40, 41, 42, 43, 55, 56, 57, 58, 59)
A = tuple(range(1, 9))
B = tuple(range(9, 16))


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


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


def independent_scope():
    orbits = census_check.derive()
    if len(orbits) != 60 or any(orbits[i][3][2] != (1, 1) for i in SCOPE):
        raise RuntimeError("independent two-high scope changed")
    return orbits


def reconstruct(ordinal, orbits):
    names, clauses, selectors = census_check.reconstruct(orbits[ordinal])
    names, clauses = list(names), list(clauses)
    number = {name: index for index, name in enumerate(names, 1)}
    high_all = tuple(number[f"cnt_d1_{v}_17_9"] for v in range(18))
    edges = tuple(number[f"a_{a}_{b}"] for a in A for b in B)
    holes = tuple(number[f"h_{a}_{b}"] for i, a in enumerate(A) for b in A[i + 1:])
    high_a = tuple(number[f"cnt_d1_{a}_17_9"] for a in A)
    before = len(names), len(clauses)
    global_count = add_threshold(names, clauses, high_all, "root_audit_global_high")
    edge_count = add_threshold(names, clauses, edges, "root_audit_AB_edges")
    rhs_count = add_threshold(names, clauses, holes + high_a, "root_audit_A_holes_high")
    clauses.extend(((global_count[2],), (-global_count[3],), (edge_count[35],)))
    for offset in range(1, len(rhs_count) + 1):
        if 36 + offset <= len(edge_count):
            clauses.extend(((-rhs_count[offset - 1], edge_count[35 + offset]),
                            (rhs_count[offset - 1], -edge_count[35 + offset])))
        else:
            clauses.append((-rhs_count[offset - 1],))
    return names, clauses, selectors, (len(names) - before[0], len(clauses) - before[1])


def load_manifest():
    path = HERE / f"{PREFIX}.tsv"
    data = path.read_bytes()
    lines = data.decode("ascii").splitlines()
    if data != ("\n".join(lines) + "\n").encode("ascii") or lines[0] != f"{PREFIX}-manifest-v1":
        raise RuntimeError("manifest framing changed")
    columns = "columns\tposition,orbit,key,state-key,t,parents,variables,clauses"
    if lines.count(columns) != 1:
        raise RuntimeError("manifest rows changed")
    rows = lines[lines.index(columns) + 1:]
    if len(rows) != 19:
        raise RuntimeError("manifest row count changed")
    return data, rows


def expected_metadata(position, ordinal, orbit, manifest, selectors, delta):
    return [("format", f"{PREFIX}-cnf-v1"), ("manifest-format", f"{PREFIX}-manifest-v1"),
            ("manifest-bytes", str(len(manifest))), ("manifest-sha256", hashlib.sha256(manifest).hexdigest()),
            ("position", str(position)), ("orbit", str(ordinal)), ("key", orbit[0]),
            ("state-key", orbit[2]), ("intersection-t", str(orbit[4])), ("parents", str(len(orbit[7]))),
            ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1])),
            ("global-high", "3"), ("root-identity", "e(A,B)=36+H(A)+high(A)"),
            ("cardinality-added-variables", str(delta[0])),
            ("cardinality-added-clauses", str(delta[1])), ("lrat-status", "checked")]


def write_reconstruction(path, position, ordinal, orbit, manifest):
    names, clauses, selectors, delta = reconstruct(ordinal, independent_scope())
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in expected_metadata(position, ordinal, orbit, manifest, selectors, delta):
            handle.write(f"c {name} {value}\n")
        for number, name in enumerate(names, 1):
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(names)} {len(clauses)}\n")
        for clause in clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def check_cover(regenerate=True):
    orbits = independent_scope()
    manifest, rows = load_manifest()
    if tuple(int(row.split("\t")[1]) for row in rows) != SCOPE:
        raise RuntimeError("manifest scope differs")
    hash_lines = (HERE / f"{PREFIX}-hashes.tsv").read_text(encoding="ascii").splitlines()
    if len(hash_lines) != 24 or hash_lines[0] != f"{PREFIX}-hashes-v1":
        raise RuntimeError("hash ledger framing differs")
    hashes = []
    for position, line in enumerate(hash_lines[5:]):
        fields = line.split("\t")
        if len(fields) != 8 or fields[:2] != [f"{position:02d}", f"{SCOPE[position]:02d}"] or \
                not fields[6].isdigit() or re.fullmatch(r"[0-9a-f]{64}", fields[7]) is None:
            raise RuntimeError("hash row changed")
        hashes.append((int(fields[6]), fields[7]))
    for ordinal in SCOPE:
        if reconstruct(ordinal, orbits)[3] != (2433, 9571):
            raise RuntimeError("fresh counter dimensions differ")
    if regenerate:
        with tempfile.TemporaryDirectory(prefix="two-high-root-check-", dir=HERE.parent) as directory:
            path = Path(directory) / "profile.cnf"
            for position, ordinal in enumerate(SCOPE):
                write_reconstruction(path, position, ordinal, orbits[ordinal], manifest)
                if identity(path) != hashes[position]:
                    raise RuntimeError(f"regenerated CNF differs: {ordinal:02d}")
    print(f"PASS profiles=19 manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


def check(path):
    orbits = independent_scope()
    manifest, _ = load_manifest()
    metadata, variables, clauses, declared = parse_cnf(path)
    position = int(dict(metadata).get("position", "-1"))
    if not 0 <= position < 19:
        raise RuntimeError("position outside exact scope")
    ordinal = SCOPE[position]
    names, expected, selectors, delta = reconstruct(ordinal, orbits)
    if metadata != expected_metadata(position, ordinal, orbits[ordinal], manifest, selectors, delta) or \
            variables != names or clauses != expected or declared != (len(names), len(expected)):
        raise RuntimeError("CNF differs from independent reconstruction")
    print(f"PASS position={position:02d} orbit={ordinal:02d} sha256={identity(path)[1]}")


def semantic_audit():
    if 153 - 6 != 147 or 147 != 18 * 8 + 3:
        raise RuntimeError("global high derivation failed")
    cut_cases = 0
    for holes, high_a in itertools.product(range(29), range(4)):
        degree_sum = 64 + high_a
        internal = 28 - holes
        if degree_sum - internal != 36 + holes + high_a:
            raise RuntimeError("root cut identity failed")
        cut_cases += 1
    for degrees in itertools.product((8, 9), repeat=18):
        if sum(degrees) == 147 and sum(value == 9 for value in degrees) != 3:
            raise RuntimeError("global degree semantic audit failed")
    print(f"PASS semantic_audit cut_cases={cut_cases} degree_vectors={2 ** 18}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", nargs="?", type=Path)
    parser.add_argument("--cover", action="store_true")
    parser.add_argument("--semantic", action="store_true")
    args = parser.parse_args()
    if args.cover:
        check_cover()
    if args.semantic:
        semantic_audit()
    if args.cnf:
        check(args.cnf)
    if not (args.cover or args.semantic or args.cnf):
        parser.error("select --cover, --semantic, or a CNF")


if __name__ == "__main__":
    main()
