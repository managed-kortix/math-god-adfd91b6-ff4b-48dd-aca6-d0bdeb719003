#!/usr/bin/env python3
"""Add a binary all-different Hall matching to the frozen all33 memberships."""

import argparse
import hashlib
import tempfile
from pathlib import Path

import m6_b7_l6_exact_pair_timeout_hall_failure as hall

HERE = Path(__file__).resolve().parent
PREFIX = "m6-b7-l6-exact-pair-hall-binary-alldifferent"
FORMAT = f"{PREFIX}-cnf-v1"
MANIFEST_FORMAT = f"{PREFIX}-manifest-v1"
HASH_FORMAT = f"{PREFIX}-hashes-v1"
MEMBERSHIPS = 33
ADDED_VARIABLES = 84
ADDED_CLAUSES = 336
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
        raise RuntimeError("binary all-different scope is not committed Hall all33")
    return records


def extend(cnf, row):
    universe, support = hall.hall_sets(row)
    before = len(cnf.names), len(cnf.clauses)
    bits = {}
    for u in universe:
        bits[u] = tuple(cnf.var(f"hall_match_bit_{u}_{bit}") for bit in range(3))
        cnf.add(*(cnf.names[f"a_{s}_{u}"] for s in support))
        for value, s in enumerate(support):
            mismatch = tuple(-bits[u][bit] if (value >> bit) & 1 else bits[u][bit]
                             for bit in range(3))
            cnf.add(*mismatch, cnf.names[f"a_{s}_{u}"])
    for left_index, left in enumerate(universe):
        for right in universe[left_index + 1:]:
            differs = []
            for bit in range(3):
                value = cnf.var(f"hall_match_diff_{left}_{right}_{bit}")
                x, y = bits[left][bit], bits[right][bit]
                differs.append(value)
                cnf.add(-value, x, y)
                cnf.add(-value, -x, -y)
                cnf.add(value, -x, y)
                cnf.add(value, x, -y)
            cnf.add(*differs)
    delta = len(cnf.names) - before[0], len(cnf.clauses) - before[1]
    if delta != (ADDED_VARIABLES, ADDED_CLAUSES):
        raise RuntimeError(f"binary all-different dimensions changed: {delta}")
    return universe, support


def build_membership(record):
    row, member = record
    cnf, selectors = hall.singleton.build_membership(member)
    universe, support = extend(cnf, row)
    return cnf, selectors, universe, support


def dimensions(record):
    variables, clauses = hall.singleton.dimensions(record[1])
    return variables + ADDED_VARIABLES, clauses + ADDED_CLAUSES


def manifest_payload(records):
    lines = [MANIFEST_FORMAT, f"memberships\t{MEMBERSHIPS}",
             "scope\texactly the ordered 33 memberships certified Hall-synchronized by the committed all33 verifier",
             "U\tthe seven q-positive vertices from the committed Hall bipartition",
             "S\tthe ordered eight vertices of N+(low-C)",
             "domain\tthree bits per u encode exactly values 0..7; value i denotes S[i]",
             "channel\tvalue i selected for u implies the original arc S[i]->u",
             "all-different\tevery unordered pair of U has a three-bit XOR disequality",
             "row-support\teach u has at least one incident S->u arc; implied by Hall synchronization",
             f"added-variables\t{ADDED_VARIABLES}", f"added-clauses\t{ADDED_CLAUSES}",
             "extension-theorem\tevery Hall-synchronized graph extends by encoding a saturating matching",
             "projection-theorem\tevery satisfying extension decodes to an injective U-to-S arc matching"]
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


def metadata(position, record, manifest, selectors, universe, support):
    row, member = record
    return [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
            ("manifest-bytes", str(len(manifest))),
            ("manifest-sha256", hashlib.sha256(manifest).hexdigest()),
            ("position", str(position)), ("membership", str(row["membership"])),
            ("key", hall.singleton.membership_key(member)), ("cell", str(member[0])),
            ("parent-ordinal", str(member[2])), ("selected-selector", str(selectors[member[2]])),
            ("hall-U", ",".join(map(str, universe))), ("hall-S", ",".join(map(str, support))),
            ("matching-domain", "binary-0..7"), ("matching-channel", "S[value]->u"),
            ("matching-added-variables", str(ADDED_VARIABLES)),
            ("matching-added-clauses", str(ADDED_CLAUSES)), ("lrat-status", "scout-only")]


def write_membership(path, position, record, cnf, selectors, universe, support, manifest):
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in metadata(position, record, manifest, selectors, universe, support):
            handle.write(f"c {name} {value}\n")
        for name, number in cnf.names.items():
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def populate_hashes(records, manifest):
    result = []
    with tempfile.TemporaryDirectory(prefix="hall-binary-hashes-", dir=HERE.parent) as directory:
        path = Path(directory) / "membership.cnf"
        for position, record in enumerate(records):
            cnf, selectors, universe, support = build_membership(record)
            write_membership(path, position, record, cnf, selectors, universe, support, manifest)
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
        cnf, selectors, universe, support = build_membership(records[args.position])
        write_membership(args.output, args.position, records[args.position], cnf, selectors,
                         universe, support, manifest)
    print(f"PASS memberships={MEMBERSHIPS} added_vars={ADDED_VARIABLES} "
          f"added_clauses={ADDED_CLAUSES} manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


if __name__ == "__main__":
    main()
