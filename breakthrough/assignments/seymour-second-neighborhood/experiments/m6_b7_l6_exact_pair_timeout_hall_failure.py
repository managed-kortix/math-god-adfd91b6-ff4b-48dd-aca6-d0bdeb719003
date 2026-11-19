#!/usr/bin/env python3
"""Add an exact Hall-failure witness to the 33 frozen exact-pair TIMEOUTs."""

import argparse
import hashlib
import tempfile
from pathlib import Path

import m6_b7_l6_early_c_certificate_residual_exact_pair_singleton_parent as singleton
import m6_b7_l6_exact_pair_timeout_complete_cut as cuts
from snc_cnf import threshold

HERE = Path(__file__).resolve().parent
PREFIX = "m6-b7-l6-exact-pair-timeout-hall-failure"
FORMAT = f"{PREFIX}-cnf-v1"
MANIFEST_FORMAT = f"{PREFIX}-manifest-v1"
HASH_FORMAT = f"{PREFIX}-hashes-v1"
MEMBERSHIPS = 33
ADDED_VARIABLES = 142
ADDED_CLAUSES = 480
CUT_CENSUS = HERE / f"{cuts.PREFIX}.tsv"


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def scope():
    semantic = cuts.records()
    _, memberships = singleton.load_memberships()
    selected = tuple((row, memberships[row["membership"]]) for row in semantic)
    if len(selected) != MEMBERSHIPS or any(len(row["out"]) != 8 for row, _ in selected):
        raise RuntimeError("frozen Hall-failure scope changed")
    return selected


def hall_sets(row):
    pair = frozenset(row["pair"])
    low = row["low"]
    nonout = frozenset(range(18)) - frozenset(row["out"]) - {low}
    universe = tuple(sorted(nonout - pair))
    support = tuple(row["out"])
    if len(universe) != 7 or len(support) != 8 or set(universe) & set(support):
        raise RuntimeError("Hall bipartition is not 7-by-8")
    return universe, support


def extend(cnf, row):
    universe, support = hall_sets(row)
    before = len(cnf.names), len(cnf.clauses)
    chosen = [cnf.var(f"hall_K_{u}") for u in universe]
    links = {}
    for u, k_var in zip(universe, chosen):
        for s in support:
            z = cnf.var(f"hall_link_{u}_{s}")
            arc = cnf.names[f"a_{s}_{u}"]
            links[u, s] = z
            cnf.add(-z, k_var)
            cnf.add(-z, arc)
            cnf.add(z, -k_var, -arc)
    gamma = []
    for s in support:
        value = cnf.var(f"hall_Gamma_{s}")
        gamma.append(value)
        incoming = [links[u, s] for u in universe]
        for z in incoming:
            cnf.add(-z, value)
        cnf.add(-value, *incoming)
    k_threshold = threshold(cnf, chosen, "hall_K")
    gamma_threshold = threshold(cnf, gamma, "hall_Gamma")
    blockers = []
    for size in range(1, 8):
        blocker = cnf.var(f"hall_defect_{size}")
        blockers.append(blocker)
        k_at_least = k_threshold[size - 1]
        gamma_at_least = gamma_threshold[size - 1]
        cnf.add(-blocker, k_at_least)
        cnf.add(-blocker, -gamma_at_least)
        cnf.add(blocker, -k_at_least, gamma_at_least)
    cnf.add(*blockers)
    delta = len(cnf.names) - before[0], len(cnf.clauses) - before[1]
    if delta != (ADDED_VARIABLES, ADDED_CLAUSES):
        raise RuntimeError(f"Hall extension dimensions changed: {delta}")
    return universe, support


def build_membership(record):
    row, member = record
    cnf, selectors = singleton.build_membership(member)
    universe, support = extend(cnf, row)
    return cnf, selectors, universe, support


def dimensions(record):
    variables, clauses = singleton.dimensions(record[1])
    return variables + ADDED_VARIABLES, clauses + ADDED_CLAUSES


def manifest_payload(records):
    census_identity = identity(CUT_CENSUS)
    lines = [MANIFEST_FORMAT, f"cut-census-bytes\t{census_identity[0]}",
             f"cut-census-sha256\t{census_identity[1]}", f"memberships\t{MEMBERSHIPS}",
             "scope\texactly the ordered 33 committed five-second singleton TIMEOUT memberships",
             "U\tthe seven q-positive vertices outside S, low-C, and the exact inaccessible pair",
             "S\tthe eight vertices of N+(low-C)",
             "incidence\tu is adjacent to s exactly when the original arc s->u is present",
             "selection\tan arbitrary nonempty K subset of U",
             "neighborhood\tGamma(K) is encoded exactly as {s in S: exists u in K with s->u}",
             "violation\t|Gamma(K)|<|K|",
             f"added-variables\t{ADDED_VARIABLES}", f"added-clauses\t{ADDED_CLAUSES}",
             "proof-status\tscout-only; no UNSAT certificate generated",
             "theorem-status\tHall synchronization is not yet a theorem until complements/residual cases are handled and UNSAT certificates are checked",
             "columns\tposition,membership,key,cell,parent,U,S,variables,clauses"]
    for position, (row, member) in enumerate(records):
        universe, support = hall_sets(row)
        variables, clauses = dimensions((row, member))
        lines.append(f"{position:03d}\t{row['membership']:03d}\t{singleton.membership_key(member)}\t"
                     f"{member[0]:03d}\t{member[2]:02d}\t{','.join(map(str, universe))}\t"
                     f"{','.join(map(str, support))}\t{variables}\t{clauses}")
    return ("\n".join(lines) + "\n").encode("ascii")


def metadata(position, record, manifest, selectors, universe, support):
    row, member = record
    return [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
            ("manifest-bytes", str(len(manifest))),
            ("manifest-sha256", hashlib.sha256(manifest).hexdigest()),
            ("position", str(position)), ("membership", str(row["membership"])),
            ("key", singleton.membership_key(member)), ("cell", str(member[0])),
            ("parent-ordinal", str(member[2])), ("selected-selector", str(selectors[member[2]])),
            ("hall-U", ",".join(map(str, universe))), ("hall-S", ",".join(map(str, support))),
            ("hall-incidence", "s->u"), ("hall-added-variables", str(ADDED_VARIABLES)),
             ("hall-added-clauses", str(ADDED_CLAUSES)), ("lrat-status", "not-generated")]


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
    with tempfile.TemporaryDirectory(prefix="hall-failure-hashes-", dir=HERE.parent) as directory:
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
        lines.append(f"{position:03d}\t{row['membership']:03d}\t{singleton.membership_key(member)}\t"
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
