#!/usr/bin/env python3
"""Independent checker for the exact 28-child Hall |K| partition."""

import argparse
import hashlib
import itertools
import re
import tempfile
from pathlib import Path

import check_m6_b7_l6_exact_pair_timeout_hall_failure as hall_check
import m6_b7_l6_exact_pair_timeout_hall_failure_cardinality_split as producer
from check_m6_parent_cnf import parse_cnf

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / f"{producer.PREFIX}.tsv"
HASHES = HERE / f"{producer.PREFIX}-hashes.tsv"


def independent_children():
    records = hall_check.independent_scope()
    parents = tuple((position, record) for position, record in enumerate(records)
                    if record[0]["membership"] in (28, 54, 69, 70))
    if tuple(record[0]["membership"] for _, record in parents) != (28, 54, 69, 70):
        raise RuntimeError("independent timeout parent scope changed")
    return tuple((position, record, cardinality) for position, record in parents
                 for cardinality in range(1, 8))


def reconstruct(child):
    parent_position, record, cardinality = child
    names, clauses, selectors, universe, support = hall_check.reconstruct(record)
    names, clauses = list(names), list(clauses)
    thresholds = [names.index(f"cnt_hall_K_7_{size}") + 1 for size in range(1, 8)]
    units = [thresholds[cardinality - 1]]
    if cardinality < 7:
        units.append(-thresholds[cardinality])
    clauses.extend((literal,) for literal in units)
    return names, clauses, selectors, universe, support, tuple(units)


def manifest_payload(scope):
    parent_manifest = hall_check.manifest_payload(hall_check.independent_scope())
    parent_scout = producer.PARENT_SCOUT.read_bytes()
    lines = [producer.MANIFEST_FORMAT,
             f"parent-manifest-bytes\t{len(parent_manifest)}",
             f"parent-manifest-sha256\t{hashlib.sha256(parent_manifest).hexdigest()}",
             f"parent-scout-bytes\t{len(parent_scout)}",
             f"parent-scout-sha256\t{hashlib.sha256(parent_scout).hexdigest()}",
             "parent-memberships\t028,054,069,070", "cardinalities\t1,2,3,4,5,6,7",
             "children\t28",
             "partition\texactly one child for every nonempty assignment to the seven hall_K variables",
             "constraint\tchild k adds |K|>=k and, for k<7, |K|<k+1 using committed exact threshold outputs",
             "columns\tchild,parent-position,membership,key,cardinality,U,S,variables,clauses"]
    for child_position, child in enumerate(scope):
        parent_position, record, cardinality = child
        row, member = record
        universe, support = hall_check.hall_sets(row)
        variables, base_clauses = hall_check.dimensions(record)
        clauses = base_clauses + (1 if cardinality == 7 else 2)
        lines.append(f"{child_position:03d}\t{parent_position:03d}\t{row['membership']:03d}\t"
                     f"{hall_check.base.producer.membership_key(member)}\t{cardinality}\t"
                     f"{','.join(map(str, universe))}\t{','.join(map(str, support))}\t"
                     f"{variables}\t{clauses}")
    return ("\n".join(lines) + "\n").encode("ascii")


def metadata(child_position, child, manifest, selectors, universe, support, units):
    parent_position, record, cardinality = child
    row, member = record
    return [("format", producer.FORMAT), ("manifest-format", producer.MANIFEST_FORMAT),
            ("manifest-bytes", str(len(manifest))),
            ("manifest-sha256", hashlib.sha256(manifest).hexdigest()),
            ("child", str(child_position)), ("parent-position", str(parent_position)),
            ("membership", str(row["membership"])),
            ("key", hall_check.base.producer.membership_key(member)), ("cell", str(member[0])),
            ("parent-ordinal", str(member[2])), ("selected-selector", str(selectors[member[2]])),
            ("hall-U", ",".join(map(str, universe))), ("hall-S", ",".join(map(str, support))),
            ("hall-K-cardinality", str(cardinality)),
            ("cardinality-units", ",".join(map(str, units))), ("lrat-status", "not-generated")]


def load_hashes(scope, manifest):
    lines = HASHES.read_text(encoding="ascii").splitlines()
    expected = [producer.HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
                f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}", "children\t28",
                "columns\tchild,membership,cardinality,variables,clauses,cnf-bytes,cnf-sha256"]
    if lines[:5] != expected or len(lines) != 33:
        raise RuntimeError("split hash ledger framing changed")
    result = []
    for child_position, (line, child) in enumerate(zip(lines[5:], scope)):
        fields = line.split("\t")
        variables, base_clauses = hall_check.dimensions(child[1])
        clauses = base_clauses + (1 if child[2] == 7 else 2)
        prefix = [f"{child_position:03d}", f"{child[1][0]['membership']:03d}", str(child[2]),
                  str(variables), str(clauses)]
        if len(fields) != 7 or fields[:5] != prefix or not fields[5].isdigit() or \
                re.fullmatch(r"[0-9a-f]{64}", fields[6]) is None:
            raise RuntimeError(f"split hash row changed: {child_position:03d}")
        result.append((int(fields[5]), fields[6]))
    return tuple(result)


def partition_audit():
    children = independent_children()
    if len(children) != 28:
        raise RuntimeError("partition does not have 28 children")
    for parent_position, group in itertools.groupby(children, key=lambda child: child[0]):
        group = tuple(group)
        if tuple(child[2] for child in group) != tuple(range(1, 8)):
            raise RuntimeError("parent cardinalities are not exact 1..7")
        covered = {}
        for mask in range(1, 1 << 7):
            matches = [child[2] for child in group if mask.bit_count() == child[2]]
            if len(matches) != 1:
                raise RuntimeError("nonempty K assignment is not covered exactly once")
            covered[mask] = matches[0]
        if len(covered) != 127:
            raise RuntimeError("nonempty K partition is not exhaustive")
    print("PASS parents=4 children=28 nonempty_K_per_parent=127 disjoint=yes exhaustive=yes")


def check_cover(regenerate=True):
    scope = independent_children()
    manifest = manifest_payload(scope)
    if MANIFEST.read_bytes() != manifest:
        raise RuntimeError("split manifest differs from independent reconstruction")
    hashes = load_hashes(scope, manifest)
    partition_audit()
    if regenerate:
        with tempfile.TemporaryDirectory(prefix="hall-cardinality-check-", dir=HERE.parent) as directory:
            path = Path(directory) / "child.cnf"
            for child_position, child in enumerate(scope):
                names, clauses, selectors, universe, support, units = reconstruct(child)
                with path.open("w", encoding="ascii", newline="\n") as handle:
                    for name, value in metadata(child_position, child, manifest, selectors, universe,
                                                support, units):
                        handle.write(f"c {name} {value}\n")
                    for number, name in enumerate(names, 1):
                        handle.write(f"c var {number} {name}\n")
                    handle.write(f"p cnf {len(names)} {len(clauses)}\n")
                    for clause in clauses:
                        handle.write(" ".join(map(str, clause)) + " 0\n")
                if producer.identity(path) != hashes[child_position]:
                    raise RuntimeError(f"regenerated split child differs: {child_position:03d}")
    print(f"PASS children=28 manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


def check(path):
    scope = independent_children()
    manifest = manifest_payload(scope)
    parsed_metadata, variables, clauses, declared = parse_cnf(path)
    child_position = int(dict(parsed_metadata).get("child", "-1"))
    if not 0 <= child_position < 28:
        raise RuntimeError("child outside exact split")
    expected = reconstruct(scope[child_position])
    names, expected_clauses, selectors, universe, support, units = expected
    if parsed_metadata != metadata(child_position, scope[child_position], manifest, selectors,
                                   universe, support, units) or variables != names or \
            clauses != expected_clauses or declared != (len(names), len(expected_clauses)):
        raise RuntimeError("child CNF differs from independent reconstruction")
    if producer.identity(path) != load_hashes(scope, manifest)[child_position]:
        raise RuntimeError("child CNF hash differs")
    print(f"PASS child={child_position:03d} membership={scope[child_position][1][0]['membership']:03d} "
          f"cardinality={scope[child_position][2]}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", type=Path, nargs="?")
    parser.add_argument("--cover", action="store_true")
    parser.add_argument("--partition", action="store_true")
    args = parser.parse_args()
    if args.cover:
        check_cover()
    if args.partition:
        partition_audit()
    if args.cnf:
        check(args.cnf)
    if not args.cover and not args.partition and not args.cnf:
        parser.error("provide a CNF, --cover, or --partition")


if __name__ == "__main__":
    main()
