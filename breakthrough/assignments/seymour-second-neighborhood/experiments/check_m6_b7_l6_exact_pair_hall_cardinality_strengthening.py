#!/usr/bin/env python3
"""Independent reconstruction and semantic audit of the all33 cardinality layer."""

import argparse
import hashlib
import itertools
import re
import tempfile
from pathlib import Path

import check_m6_b7_l6_exact_pair_timeout_hall_failure as hall_check
import m6_b7_l6_exact_pair_hall_cardinality_strengthening as producer
import verify_m6_b7_l6_exact_pair_timeout_hall_failure_all33 as all33
from check_m6_parent_cnf import parse_cnf

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / f"{producer.PREFIX}.tsv"
HASHES = HERE / f"{producer.PREFIX}-hashes.tsv"


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def independent_scope():
    records = hall_check.independent_scope()
    audited, _, _ = all33.scope_audit()
    observed = tuple((position, row[0]["membership"]) for position, row in enumerate(records))
    if len(records) != 33 or observed != audited:
        raise RuntimeError("cardinality scope differs from Hall all33 ancestry")
    return records


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


def reconstruct(record):
    row, member = record
    names, clauses, selectors = hall_check.base.reconstruct(member)
    names, clauses = list(names), list(clauses)
    pair = set(row["pair"])
    nonout = set(range(18)) - set(row["out"]) - {row["low"]}
    universe, support = tuple(sorted(nonout - pair)), tuple(row["out"])
    if len(universe) != 7 or len(support) != 8:
        raise RuntimeError("independent cardinality partition is not 7-by-8")
    number = {name: index for index, name in enumerate(names, 1)}
    edge_inputs = tuple(number[f"a_{s}_{u}"] for s in support for u in universe)
    hole_inputs = tuple(number[f"h_{min(x, y)}_{max(x, y)}"]
                        for i, x in enumerate(support) for y in support[i + 1:])
    high_s = tuple(number[f"cnt_d1_{s}_17_9"] for s in support)
    high_all = tuple(number[f"cnt_d1_{v}_17_9"] for v in range(18))
    before = len(names), len(clauses)
    edge_count = add_threshold(names, clauses, edge_inputs, "audit_SU_edges")
    rhs_count = add_threshold(names, clauses, hole_inputs + high_s, "audit_S_holes_high")
    global_high = add_threshold(names, clauses, high_all, "audit_global_high")
    clauses.extend(((global_high[2],), (-global_high[3],), (edge_count[35],)))
    for offset in range(1, len(rhs_count) + 1):
        if 36 + offset <= len(edge_count):
            clauses.extend(((-rhs_count[offset - 1], edge_count[35 + offset]),
                            (rhs_count[offset - 1], -edge_count[35 + offset])))
        else:
            clauses.append((-rhs_count[offset - 1],))
    return names, clauses, selectors, universe, support, \
        (len(names) - before[0], len(clauses) - before[1])


def check_cover(regenerate=True):
    independent = independent_scope()
    records = producer.scope()
    manifest = producer.manifest_payload(records)
    if MANIFEST.read_bytes() != manifest:
        raise RuntimeError("cardinality manifest differs")
    lines = HASHES.read_text(encoding="ascii").splitlines()
    if len(lines) != 38 or lines[:5] != producer.hash_payload(records, manifest).decode("ascii").splitlines()[:5]:
        raise RuntimeError("cardinality hash ledger framing differs")
    hashes = []
    for position, line in enumerate(lines[5:]):
        fields = line.split("\t")
        if len(fields) != 7 or fields[0] != f"{position:03d}" or not fields[5].isdigit() or \
                re.fullmatch(r"[0-9a-f]{64}", fields[6]) is None:
            raise RuntimeError("cardinality hash row differs")
        hashes.append((int(fields[5]), fields[6]))
    with tempfile.TemporaryDirectory(prefix="hall-cardinality-check-", dir=HERE.parent) as directory:
        path = Path(directory) / "membership.cnf"
        for position, (record, independent_record) in enumerate(zip(records, independent)):
            names, clauses, selectors, universe, support, delta = reconstruct(independent_record)
            expected = producer.build_membership(record)
            if delta != expected[4]:
                raise RuntimeError("independent fresh-counter dimensions differ")
            if regenerate:
                producer.write_membership(path, position, record, _CNFView(names, clauses), selectors,
                                          universe, support, delta, manifest)
                if identity(path) != hashes[position]:
                    raise RuntimeError(f"regenerated cardinality CNF differs: {position:03d}")
    print(f"PASS memberships=33 manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


class _CNFView:
    def __init__(self, names, clauses):
        self.names = {name: index for index, name in enumerate(names, 1)}
        self.clauses = clauses


def check(path):
    independent = independent_scope()
    records = producer.scope()
    metadata, variables, clauses, declared = parse_cnf(path)
    position = int(dict(metadata).get("position", "-1"))
    if not 0 <= position < 33:
        raise RuntimeError("cardinality position outside scope")
    names, expected, selectors, universe, support, delta = reconstruct(independent[position])
    manifest = producer.manifest_payload(records)
    if metadata != producer.metadata(position, records[position], manifest, selectors, universe,
                                     support, delta) or variables != names or clauses != expected or \
            declared != (len(names), len(expected)):
        raise RuntimeError("cardinality CNF differs from independent reconstruction")
    print(f"PASS position={position:03d} sha256={identity(path)[1]}")


def semantic_audit():
    checked = 0
    if 153 - 6 != 147 or 147 - 18 * 8 != 3:
        raise RuntimeError("global arc/high arithmetic failed")
    for holes, high_s in itertools.product(range(29), range(4)):
        internal = 28 - holes
        degree_sum = 64 + high_s
        cut = degree_sum - internal
        if cut != 36 + holes + high_s:
            raise RuntimeError("cut identity arithmetic failed")
        checked += 1
    for bits in itertools.product((8, 9), repeat=18):
        if sum(bits) == 147 and sum(value == 9 for value in bits) != 3:
            raise RuntimeError("degree sequence high count failed")
    print(f"PASS semantic_audit cut_cases={checked} degree_vectors={2 ** 18}")


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
