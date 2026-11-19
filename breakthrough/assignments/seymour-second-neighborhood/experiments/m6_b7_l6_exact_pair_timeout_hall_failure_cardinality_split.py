#!/usr/bin/env python3
"""Split the four frozen Hall-failure TIMEOUTs by exact nonzero |K|."""

import argparse
import hashlib
import tempfile
from pathlib import Path

import m6_b7_l6_exact_pair_timeout_hall_failure as hall

HERE = Path(__file__).resolve().parent
PREFIX = "m6-b7-l6-exact-pair-timeout-hall-failure-cardinality-split"
FORMAT = f"{PREFIX}-cnf-v1"
MANIFEST_FORMAT = f"{PREFIX}-manifest-v1"
HASH_FORMAT = f"{PREFIX}-hashes-v1"
TIMEOUT_MEMBERSHIPS = (28, 54, 69, 70)
CARDINALITIES = tuple(range(1, 8))
CHILDREN = 28
PARENT_SCOUT = HERE / f"{hall.PREFIX}-scout-180s.json"


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def parents():
    records = hall.scope()
    selected = tuple((position, record) for position, record in enumerate(records)
                     if record[0]["membership"] in TIMEOUT_MEMBERSHIPS)
    if tuple(record[0]["membership"] for _, record in selected) != TIMEOUT_MEMBERSHIPS:
        raise RuntimeError("frozen Hall TIMEOUT parent scope changed")
    return selected


def children():
    result = tuple((parent_position, record, cardinality)
                   for parent_position, record in parents()
                   for cardinality in CARDINALITIES)
    if len(result) != CHILDREN:
        raise RuntimeError("cardinality child scope changed")
    return result


def exact_cardinality_units(cnf, cardinality):
    thresholds = [cnf.names[f"cnt_hall_K_7_{size}"] for size in CARDINALITIES]
    units = [thresholds[cardinality - 1]]
    if cardinality < 7:
        units.append(-thresholds[cardinality])
    for literal in units:
        cnf.add(literal)
    return tuple(units)


def build_child(child):
    parent_position, record, cardinality = child
    cnf, selectors, universe, support = hall.build_membership(record)
    units = exact_cardinality_units(cnf, cardinality)
    return cnf, selectors, universe, support, units


def dimensions(child):
    variables, clauses = hall.dimensions(child[1])
    return variables, clauses + (1 if child[2] == 7 else 2)


def manifest_payload(scope):
    parent_manifest = hall.manifest_payload(hall.scope())
    parent_scout = PARENT_SCOUT.read_bytes()
    lines = [MANIFEST_FORMAT,
             f"parent-manifest-bytes\t{len(parent_manifest)}",
             f"parent-manifest-sha256\t{hashlib.sha256(parent_manifest).hexdigest()}",
             f"parent-scout-bytes\t{len(parent_scout)}",
             f"parent-scout-sha256\t{hashlib.sha256(parent_scout).hexdigest()}",
             "parent-memberships\t028,054,069,070", "cardinalities\t1,2,3,4,5,6,7",
             f"children\t{CHILDREN}",
             "partition\texactly one child for every nonempty assignment to the seven hall_K variables",
             "constraint\tchild k adds |K|>=k and, for k<7, |K|<k+1 using committed exact threshold outputs",
             "columns\tchild,parent-position,membership,key,cardinality,U,S,variables,clauses"]
    for child_position, (parent_position, record, cardinality) in enumerate(scope):
        row, member = record
        universe, support = hall.hall_sets(row)
        variables, clauses = dimensions((parent_position, record, cardinality))
        lines.append(f"{child_position:03d}\t{parent_position:03d}\t{row['membership']:03d}\t"
                     f"{hall.singleton.membership_key(member)}\t{cardinality}\t"
                     f"{','.join(map(str, universe))}\t{','.join(map(str, support))}\t"
                     f"{variables}\t{clauses}")
    return ("\n".join(lines) + "\n").encode("ascii")


def metadata(child_position, child, manifest, selectors, universe, support, units):
    parent_position, record, cardinality = child
    row, member = record
    return [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
            ("manifest-bytes", str(len(manifest))),
            ("manifest-sha256", hashlib.sha256(manifest).hexdigest()),
            ("child", str(child_position)), ("parent-position", str(parent_position)),
            ("membership", str(row["membership"])),
            ("key", hall.singleton.membership_key(member)), ("cell", str(member[0])),
            ("parent-ordinal", str(member[2])),
            ("selected-selector", str(selectors[member[2]])),
            ("hall-U", ",".join(map(str, universe))),
            ("hall-S", ",".join(map(str, support))),
            ("hall-K-cardinality", str(cardinality)),
            ("cardinality-units", ",".join(map(str, units))), ("lrat-status", "not-generated")]


def write_child(path, child_position, child, cnf, selectors, universe, support, units, manifest):
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in metadata(child_position, child, manifest, selectors, universe, support, units):
            handle.write(f"c {name} {value}\n")
        for name, number in cnf.names.items():
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def populate_hashes(scope, manifest):
    result = []
    with tempfile.TemporaryDirectory(prefix="hall-cardinality-hashes-", dir=HERE.parent) as directory:
        path = Path(directory) / "child.cnf"
        for child_position, child in enumerate(scope):
            built = build_child(child)
            write_child(path, child_position, child, *built, manifest)
            result.append(identity(path))
    return tuple(result)


def hash_payload(scope, manifest, hashes):
    lines = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
             f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}",
             f"children\t{CHILDREN}",
             "columns\tchild,membership,cardinality,variables,clauses,cnf-bytes,cnf-sha256"]
    for child_position, (child, (size, digest)) in enumerate(zip(scope, hashes)):
        variables, clauses = dimensions(child)
        lines.append(f"{child_position:03d}\t{child[1][0]['membership']:03d}\t{child[2]}\t"
                     f"{variables}\t{clauses}\t{size}\t{digest}")
    return ("\n".join(lines) + "\n").encode("ascii")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--child", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--hash-output", type=Path)
    args = parser.parse_args()
    scope = children()
    manifest = manifest_payload(scope)
    if args.manifest_output:
        args.manifest_output.write_bytes(manifest)
    if args.hash_output:
        args.hash_output.write_bytes(hash_payload(scope, manifest, populate_hashes(scope, manifest)))
    if args.output:
        if args.child is None or not 0 <= args.child < CHILDREN:
            parser.error("--output requires a valid --child")
        built = build_child(scope[args.child])
        write_child(args.output, args.child, scope[args.child], *built, manifest)
    print(f"PASS parents=4 children={CHILDREN} manifest_sha256="
          f"{hashlib.sha256(manifest).hexdigest()}")


if __name__ == "__main__":
    main()
