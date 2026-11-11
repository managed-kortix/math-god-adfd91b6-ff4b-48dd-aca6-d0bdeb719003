#!/usr/bin/env python3
"""Independent checker for the 101 exact-pair singleton memberships."""

import argparse
import hashlib
import json
import math
import re
import tempfile
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

import check_m6_b7_l6_early_c_certificate_residual_exact_pairs as grouped
import m6_b7_l6_early_c_certificate_residual_exact_pair_singleton_parent as producer
from check_m6_parent_cnf import expected_projection, parse_cnf

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / f"{producer.PREFIX}.tsv"
HASHES = HERE / f"{producer.PREFIX}-hashes.tsv"
SCOUT = HERE / f"{producer.PREFIX}-scout-5s.json"
SOLVER_PATH = "/tmp/opencode/cadical-1.7.3/build/cadical"
SOLVER_IDENTITY = (1002216, "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292", "1.7.3")
SCOUT_SECONDS = 5
SCOUT_JOBS = 2
SCOUT_IDENTITY = (29545, "adc5c7af3ffdc53512e953b98019334835612040481204d0dd921ecc6287cb88")
SCOUT_STATUS_SHA256 = "2aba0fa29668f483edec154f65692783d01038a147ef79a708f1f0c49e28d1e1"
SCOUT_TOTALS = {"SAT": 0, "UNSAT": 68, "TIMEOUT": 33}


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def independent_projection(child, parent):
    return frozenset(expected_projection(child[2][7][parent][2])[1])


@lru_cache(maxsize=1)
def derive():
    producer.verify_ancestry()
    cells = grouped.derive()
    grouped_manifest = grouped.manifest_payload(cells)
    if producer.ANCESTRY_PATHS["grouped-manifest"].read_bytes() != grouped_manifest:
        raise RuntimeError("committed grouped manifest differs from independent reconstruction")
    memberships = []
    by_cell = defaultdict(list)
    for cell, record in enumerate(cells):
        _, child = record
        projections = []
        for parent in child[5]:
            projection = independent_projection(child, parent)
            if len(projection) != 6:
                raise RuntimeError("selected parent projection does not contain six holes")
            projections.append(projection)
            member = (cell, record, parent)
            memberships.append(member)
            by_cell[cell].append(member)
        if len(projections) != len(set(projections)):
            raise RuntimeError("compatible selectors do not have distinct parent projections")
        if tuple(member[2] for member in by_cell[cell]) != child[5]:
            raise RuntimeError("singleton split is not exhaustive in grouped selector order")
    if len(cells) != producer.CELLS or len(memberships) != producer.MEMBERSHIPS:
        raise RuntimeError("independent 20/101 singleton census differs")
    if set((member[0], member[2]) for member in memberships) != {
            (cell, parent) for cell, (_, child) in enumerate(cells) for parent in child[5]}:
        raise RuntimeError("singleton memberships do not biject with grouped cell-parent memberships")
    return tuple(cells), tuple(memberships)


@lru_cache(maxsize=1)
def canonical_manifest():
    cells, memberships = derive()
    data = producer.manifest_payload(cells, memberships)
    if MANIFEST.read_bytes() != data:
        raise RuntimeError("singleton manifest differs from independent refinement")
    return data


@lru_cache(maxsize=1)
def load_hashes(path=HASHES):
    manifest = canonical_manifest()
    data = path.read_bytes()
    lines = data.decode("ascii").splitlines()
    header = [producer.HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
              f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}",
              f"memberships\t{producer.MEMBERSHIPS}",
              "columns\tmembership,key,cell,parent,variables,clauses,cnf-bytes,cnf-sha256"]
    memberships = derive()[1]
    if lines[:5] != header or len(lines) != len(memberships) + 5:
        raise RuntimeError("singleton hash ledger framing differs")
    result = {}
    for ordinal, (line, member) in enumerate(zip(lines[5:], memberships)):
        fields = line.split("\t")
        variables, clauses = producer.dimensions(member)
        expected = [f"{ordinal:03d}", producer.membership_key(member), f"{member[0]:03d}",
                    f"{member[2]:02d}", str(variables), str(clauses)]
        if len(fields) != 8 or fields[:6] != expected or not fields[6].isdigit() or \
                re.fullmatch(r"[0-9a-f]{64}", fields[7]) is None:
            raise RuntimeError(f"singleton hash row differs: {ordinal:03d}")
        if fields[1] in result:
            raise RuntimeError("duplicate singleton hash key")
        result[fields[1]] = int(fields[6]), fields[7]
    if data != ("\n".join(lines) + "\n").encode("ascii"):
        raise RuntimeError("singleton hash ledger is not canonical ASCII TSV")
    return result


def reconstruct(member):
    _, record, parent = member
    names, clauses, selectors = grouped.reconstruct(record)
    clauses.append((selectors[parent],))
    return names, clauses, selectors


def check_cover(regenerate=True):
    cells, memberships = derive()
    manifest = canonical_manifest()
    hashes = load_hashes()
    if regenerate:
        with tempfile.TemporaryDirectory(prefix="exact-pair-singleton-check-", dir=HERE.parent) as directory:
            path = Path(directory) / "membership.cnf"
            for ordinal, member in enumerate(memberships):
                names, clauses, selectors = reconstruct(member)
                with path.open("w", encoding="ascii", newline="\n") as handle:
                    for name, value in producer.metadata(ordinal, member, manifest, selectors):
                        handle.write(f"c {name} {value}\n")
                    for number, name in enumerate(names, 1):
                        handle.write(f"c var {number} {name}\n")
                    handle.write(f"p cnf {len(names)} {len(clauses)}\n")
                    for clause in clauses:
                        handle.write(" ".join(map(str, clause)) + " 0\n")
                if identity(path) != hashes[producer.membership_key(member)]:
                    raise RuntimeError(f"regenerated singleton membership {ordinal:03d} differs")
    counts = Counter(sum(1 for member in memberships if member[0] == cell) for cell in range(len(cells)))
    print(f"PASS grouped_cells={len(cells)} memberships={len(memberships)} "
          f"parent_counts={dict(sorted(counts.items()))} disjoint={len(cells)} exhaustive={len(cells)} "
          f"manifest_sha256={hashlib.sha256(manifest).hexdigest()}")
    return cells, memberships, manifest


def check(path):
    _, memberships, manifest = check_cover(regenerate=False)
    metadata, variables, clauses, declared = parse_cnf(path)
    try:
        ordinal = int(dict(metadata).get("membership", "-1"))
    except ValueError as error:
        raise RuntimeError("invalid singleton membership ordinal") from error
    if not 0 <= ordinal < len(memberships):
        raise RuntimeError("singleton membership outside manifest")
    member = memberships[ordinal]
    expected_variables, expected_clauses, selectors = reconstruct(member)
    if metadata != producer.metadata(ordinal, member, manifest, selectors) or \
            variables != expected_variables or clauses != expected_clauses or \
            declared != producer.dimensions(member):
        raise RuntimeError("singleton CNF differs from exact selected parent and q pattern")
    digest = identity(path)
    if digest != load_hashes()[producer.membership_key(member)]:
        raise RuntimeError("singleton CNF hash differs")
    print(f"PASS membership={ordinal:03d} key={producer.membership_key(member)} "
          f"selector={selectors[member[2]]} sha256={digest[1]}")


def check_scout(path=SCOUT, require_frozen_identity=True):
    _, memberships, manifest = check_cover(regenerate=False)
    raw = path.read_bytes()
    if require_frozen_identity and (SCOUT_IDENTITY is None or identity(path) != SCOUT_IDENTITY):
        raise RuntimeError("singleton scout identity differs")
    payload = json.loads(raw.decode("ascii"))
    if raw != (json.dumps(payload, sort_keys=True, indent=2) + "\n").encode("ascii"):
        raise RuntimeError("singleton scout is not canonical ASCII JSON")
    ledger = HASHES.read_bytes()
    expected_header = {
        "schema": f"{producer.PREFIX}-scout-v1", "seconds_per_membership": SCOUT_SECONDS,
        "jobs": SCOUT_JOBS, "solver": SOLVER_PATH, "solver_bytes": SOLVER_IDENTITY[0],
        "solver_sha256": SOLVER_IDENTITY[1], "solver_version": SOLVER_IDENTITY[2],
        "manifest_bytes": len(manifest), "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
        "hash_ledger_bytes": len(ledger), "hash_ledger_sha256": hashlib.sha256(ledger).hexdigest(),
        "status_sequence_sha256": SCOUT_STATUS_SHA256,
    }
    if set(payload) != set(expected_header) | {"rows"} or any(
            payload.get(name) != value for name, value in expected_header.items()):
        raise RuntimeError("singleton scout provenance differs")
    rows = payload.get("rows", [])
    hashes = load_hashes()
    if len(rows) != len(memberships):
        raise RuntimeError("singleton scout is not exhaustive")
    for ordinal, (member, row) in enumerate(zip(memberships, rows)):
        expected = {"membership": ordinal, "key": producer.membership_key(member),
                    "cell": member[0], "source_child": member[1][0], "parent": member[2],
                    "job": ordinal % SCOUT_JOBS,
                    "cnf_sha256": hashes[producer.membership_key(member)][1]}
        if set(row) != set(expected) | {"status", "seconds"} or any(
                row.get(name) != value for name, value in expected.items()):
            raise RuntimeError(f"singleton scout row differs: {ordinal:03d}")
        seconds = row.get("seconds")
        if row.get("status") not in ("SAT", "UNSAT", "TIMEOUT") or isinstance(seconds, bool) or \
                not isinstance(seconds, (int, float)) or not math.isfinite(seconds) or \
                (row["status"] == "TIMEOUT" and not SCOUT_SECONDS <= seconds <= SCOUT_SECONDS + 1) or \
                (row["status"] != "TIMEOUT" and not 0 <= seconds < SCOUT_SECONDS):
            raise RuntimeError(f"singleton scout status/timing differs: {ordinal:03d}")
    statuses = "".join({"SAT": "S", "UNSAT": "U", "TIMEOUT": "T"}[row["status"]] for row in rows)
    totals = {status: sum(row["status"] == status for row in rows)
              for status in ("SAT", "UNSAT", "TIMEOUT")}
    if hashlib.sha256(statuses.encode("ascii")).hexdigest() != SCOUT_STATUS_SHA256 or totals != SCOUT_TOTALS:
        raise RuntimeError("singleton scout exact statuses differ")
    print(f"PASS singleton_scout totals={totals} status_sha256={SCOUT_STATUS_SHA256}")
    return totals


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", type=Path, nargs="?")
    parser.add_argument("--cover", action="store_true")
    parser.add_argument("--scout", action="store_true")
    args = parser.parse_args()
    if args.cover:
        check_cover()
    if args.cnf:
        check(args.cnf)
    if args.scout:
        check_scout()
    if not args.cover and not args.cnf and not args.scout:
        parser.error("provide a CNF, --cover, or --scout")


if __name__ == "__main__":
    main()
