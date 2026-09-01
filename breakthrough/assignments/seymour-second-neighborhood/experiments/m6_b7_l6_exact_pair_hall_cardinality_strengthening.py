#!/usr/bin/env python3
"""Add authoritative redundant cardinality identities to Hall-synchronized all33."""

import argparse
import hashlib
import tempfile
from pathlib import Path

import m6_b7_l6_exact_pair_timeout_hall_failure as hall
from snc_cnf import threshold

HERE = Path(__file__).resolve().parent
PREFIX = "m6-b7-l6-exact-pair-hall-cardinality-strengthening"
FORMAT = f"{PREFIX}-cnf-v1"
MANIFEST_FORMAT = f"{PREFIX}-manifest-v1"
HASH_FORMAT = f"{PREFIX}-hashes-v1"
MEMBERSHIPS = 33
ANCESTRY = {
    "all33-hall-verifier": HERE / "verify_m6_b7_l6_exact_pair_timeout_hall_failure_all33.py",
    "direct-hall-certificates": HERE / "m6-b7-l6-exact-pair-timeout-hall-failure-scout-unsat-certificates.tsv",
    "split-hall-certificates": HERE / "m6-b7-l6-exact-pair-timeout-hall-failure-cardinality-split-certificates.tsv",
}


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def scope():
    records = hall.scope()
    if len(records) != MEMBERSHIPS:
        raise RuntimeError("cardinality scope is not committed Hall all33")
    return records


def cardinality_inputs(cnf, row):
    universe, support = hall.hall_sets(row)
    edge_inputs = tuple(cnf.names[f"a_{s}_{u}"] for s in support for u in universe)
    hole_inputs = tuple(cnf.names[f"h_{min(x, y)}_{max(x, y)}"]
                        for i, x in enumerate(support) for y in support[i + 1:])
    high_s_inputs = tuple(cnf.names[f"cnt_d1_{s}_17_9"] for s in support)
    high_all_inputs = tuple(cnf.names[f"cnt_d1_{v}_17_9"] for v in range(18))
    return universe, support, edge_inputs, hole_inputs, high_s_inputs, high_all_inputs


def extend(cnf, row):
    before = len(cnf.names), len(cnf.clauses)
    universe, support, edge_inputs, hole_inputs, high_s_inputs, high_all_inputs = \
        cardinality_inputs(cnf, row)
    edge_count = threshold(cnf, edge_inputs, "audit_SU_edges")
    rhs_count = threshold(cnf, hole_inputs + high_s_inputs, "audit_S_holes_high")
    global_high = threshold(cnf, high_all_inputs, "audit_global_high")
    cnf.add(global_high[2])
    cnf.add(-global_high[3])
    cnf.add(edge_count[35])
    for offset in range(1, len(rhs_count) + 1):
        if 36 + offset <= len(edge_count):
            cnf.add(-rhs_count[offset - 1], edge_count[35 + offset])
            cnf.add(rhs_count[offset - 1], -edge_count[35 + offset])
        else:
            cnf.add(-rhs_count[offset - 1])
    delta = len(cnf.names) - before[0], len(cnf.clauses) - before[1]
    return universe, support, delta


def build_membership(record):
    row, member = record
    cnf, selectors = hall.singleton.build_membership(member)
    universe, support, delta = extend(cnf, row)
    return cnf, selectors, universe, support, delta


def dimensions(record):
    cnf, _, _, _, _ = build_membership(record)
    return len(cnf.names), len(cnf.clauses)


def manifest_payload(records):
    first = build_membership(records[0])[4]
    if any(build_membership(record)[4] != first for record in records):
        raise RuntimeError("cardinality extension dimensions differ by membership")
    lines = [MANIFEST_FORMAT, f"memberships\t{MEMBERSHIPS}",
             "scope\texactly the ordered 33 memberships certified Hall-synchronized by the committed all33 verifier",
             "global-arcs\t153 unordered pairs minus six holes equals 147 arcs",
             "global-high\tdegrees are 8 or 9, so 147=18*8+high(V) and high(V)=3",
             "cut-identity\te(S,U)=36+H(S)+high(S)",
             "cut-proof\tsum_S d+=64+high(S); internal S arcs=28-H(S); no S arc enters low-C or either exact-inaccessible endpoint",
             "fresh-counters\texact unary counters for 56 S-to-U arcs, 28 S-holes plus eight S-high indicators, and all 18 high indicators",
             "strengthening\thigh(V)=3 and every threshold consequence of e(S,U)=36+H(S)+high(S)",
             f"added-variables\t{first[0]}", f"added-clauses\t{first[1]}",
             "proof-status\tscout-only"]
    for name, path in ANCESTRY.items():
        size, digest = identity(path)
        lines.extend((f"ancestry-{name}-bytes\t{size}", f"ancestry-{name}-sha256\t{digest}"))
    lines.append("columns\tposition,membership,key,cell,parent,U,S,variables,clauses")
    for position, (row, member) in enumerate(records):
        universe, support = hall.hall_sets(row)
        variables, clauses = dimensions((row, member))
        lines.append(f"{position:03d}\t{row['membership']:03d}\t{hall.singleton.membership_key(member)}\t"
                     f"{member[0]:03d}\t{member[2]:02d}\t{','.join(map(str, universe))}\t"
                     f"{','.join(map(str, support))}\t{variables}\t{clauses}")
    return ("\n".join(lines) + "\n").encode("ascii")


def metadata(position, record, manifest, selectors, universe, support, delta):
    row, member = record
    return [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
            ("manifest-bytes", str(len(manifest))),
            ("manifest-sha256", hashlib.sha256(manifest).hexdigest()),
            ("position", str(position)), ("membership", str(row["membership"])),
            ("key", hall.singleton.membership_key(member)), ("cell", str(member[0])),
            ("parent-ordinal", str(member[2])), ("selected-selector", str(selectors[member[2]])),
            ("hall-U", ",".join(map(str, universe))), ("hall-S", ",".join(map(str, support))),
            ("global-arcs", "147"), ("global-high", "3"),
            ("cut-identity", "e(S,U)=36+H(S)+high(S)"),
            ("cardinality-added-variables", str(delta[0])),
            ("cardinality-added-clauses", str(delta[1])), ("lrat-status", "scout-only")]


def write_membership(path, position, record, cnf, selectors, universe, support, delta, manifest):
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in metadata(position, record, manifest, selectors, universe, support, delta):
            handle.write(f"c {name} {value}\n")
        for name, number in cnf.names.items():
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def populate_hashes(records, manifest):
    result = []
    with tempfile.TemporaryDirectory(prefix="hall-cardinality-hashes-", dir=HERE.parent) as directory:
        path = Path(directory) / "membership.cnf"
        for position, record in enumerate(records):
            built = build_membership(record)
            write_membership(path, position, record, *built, manifest)
            result.append(identity(path))
    return tuple(result)


def hash_payload(records, manifest, hashes=None):
    hashes = hashes or (("", ""),) * len(records)
    lines = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
             f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}",
             f"memberships\t{MEMBERSHIPS}",
             "columns\tposition,membership,key,variables,clauses,cnf-bytes,cnf-sha256"]
    for position, ((row, member), (size, digest)) in enumerate(zip(records, hashes)):
        variables, clauses = dimensions((row, member))
        lines.append(f"{position:03d}\t{row['membership']:03d}\t{hall.singleton.membership_key(member)}\t"
                     f"{variables}\t{clauses}\t{size}\t{digest}")
    return ("\n".join(lines) + "\n").encode("ascii")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--position", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--hash-output", type=Path)
    parser.add_argument("--populate-hashes", action="store_true")
    args = parser.parse_args()
    records = scope()
    manifest = manifest_payload(records)
    if args.manifest_output:
        args.manifest_output.write_bytes(manifest)
    if args.hash_output:
        hashes = populate_hashes(records, manifest) if args.populate_hashes else None
        args.hash_output.write_bytes(hash_payload(records, manifest, hashes))
    if args.output:
        if args.position is None or not 0 <= args.position < MEMBERSHIPS:
            parser.error("--output requires a valid --position")
        write_membership(args.output, args.position, records[args.position],
                         *build_membership(records[args.position]), manifest)
    print(f"PASS memberships={MEMBERSHIPS} manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


if __name__ == "__main__":
    main()
