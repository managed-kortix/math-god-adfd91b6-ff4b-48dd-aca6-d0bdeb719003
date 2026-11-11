#!/usr/bin/env python3
"""Independent checker for the exact residual singleton-parent split."""

import argparse
import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

import check_m6_b7_l6_hard_witness_positive_gain_coordinate_residual_cover as residual
import m6_b7_l6_hard_witness_positive_gain_coordinate_residual_singleton_parent as producer
from check_m6_parent_cnf import LABELS, PAIRS, parse_cnf

HERE = Path(__file__).resolve().parent
MANIFEST_PATH = HERE / "m6-b7-l6-hard-witness-positive-gain-coordinate-residual-singleton-parent.tsv"
HASH_PATH = HERE / "m6-b7-l6-hard-witness-positive-gain-coordinate-residual-singleton-parent-hashes.tsv"
SCOUT_PATH = HERE / "m6-b7-l6-hard-witness-positive-gain-coordinate-residual-singleton-parent-scout-5s.json"
SOLVER_IDENTITY = (1002216, "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292", "1.7.3")
SOLVER_PATH = "/tmp/opencode/cadical-1.7.3/build/cadical"
SCOUT_IDENTITY = (487540, "c6b506308b52f93214b708fb03053a8f1502d085d13ab751b90fca2ee246efc2")
SCOUT_SCHEMA = "m6-b7-l6-hard-witness-positive-gain-coordinate-residual-singleton-parent-scout-v1"
SCOUT_SECONDS = 5
SCOUT_JOBS = 2
SCOUT_STATUS_SHA256 = "1c820b0de4e79a0ac355e9603566eca4a77eedf84f15989a124bdccbb30fbf82"
SCOUT_TOTALS = {"SAT": 0, "UNSAT": 127, "TIMEOUT": 1255}


def independent_projection(row):
    positions = Counter()
    image = {}
    for vertex, cell in enumerate(row["word"]):
        choices = LABELS[row["branch"]][cell]
        image[vertex] = choices[positions[cell]]
        positions[cell] += 1
    return frozenset(tuple(sorted((image[a], image[b]))) for a, b in row["edges"])


@lru_cache(maxsize=1)
def derive():
    producer.verify_identities()
    cover, residual_manifest = residual.check_coverage()
    if producer.IDENTITY_PATHS["residual-manifest"].read_bytes() != residual_manifest:
        raise RuntimeError("bound residual manifest differs from independent reconstruction")
    memberships = []
    grouped = defaultdict(list)
    for leaf_ordinal, item in enumerate(cover):
        parent_rows = item[1][4][2][6]
        projections = []
        for parent_ordinal, parent in enumerate(parent_rows):
            projection = independent_projection(parent[2])
            if len(projection) != 6:
                raise RuntimeError("parent does not have exactly six holes")
            projections.append(projection)
            member = (leaf_ordinal, item, parent_ordinal, parent)
            memberships.append(member)
            grouped[leaf_ordinal].append(member)
        if len(projections) != len(set(projections)):
            raise RuntimeError("two selectors in one residual leaf have the same parent projection")
        if not parent_rows:
            raise RuntimeError("residual leaf has no parent selector")
    if len(cover) != producer.LEAVES or len(memberships) != producer.MEMBERSHIPS:
        raise RuntimeError("independent singleton-parent census differs")
    if tuple(len(grouped[i]) for i in range(len(cover))) != tuple(
            len(item[1][4][2][6]) for item in cover):
        raise RuntimeError("per-leaf selector cover omits or duplicates a parent")
    return tuple(cover), tuple(memberships)


@lru_cache(maxsize=1)
def canonical_manifest():
    cover, memberships = derive()
    data = producer.manifest_payload(cover, memberships)
    if MANIFEST_PATH.read_bytes() != data:
        raise RuntimeError("singleton-parent manifest differs from independent cover")
    return data


@lru_cache(maxsize=1)
def load_hashes(path=HASH_PATH):
    manifest = canonical_manifest()
    data = path.read_bytes()
    lines = data.decode("ascii").splitlines()
    header = [producer.HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
              f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}",
              f"memberships\t{producer.MEMBERSHIPS}",
              "columns\tmembership-ordinal,key,residual-leaf-ordinal,parent-ordinal,accepted-ordinal,cover-index,variables,clauses,cnf-sha256"]
    memberships = derive()[1]
    if lines[:5] != header or len(lines) != len(memberships) + 5:
        raise RuntimeError("singleton-parent hash ledger framing differs")
    result = {}
    for ordinal, (member, line) in enumerate(zip(memberships, lines[5:])):
        fields = line.split("\t")
        variables, clauses = producer.dimensions(member)
        expected = [f"{ordinal:04d}", producer.membership_key(member), f"{member[0]:03d}",
                    f"{member[2]:02d}", f"{member[3][0]:05d}", f"{member[3][1]:06d}",
                    str(variables), str(clauses)]
        if len(fields) != 9 or fields[:8] != expected or re.fullmatch(r"[0-9a-f]{64}", fields[8]) is None:
            raise RuntimeError(f"singleton-parent hash row differs: {ordinal:04d}")
        if fields[1] in result:
            raise RuntimeError("duplicate singleton-parent key")
        result[fields[1]] = fields[8]
    if data != ("\n".join(lines) + "\n").encode("ascii"):
        raise RuntimeError("singleton-parent hash ledger is not canonical ASCII TSV")
    return result


def check_cover():
    cover, memberships = derive()
    manifest = canonical_manifest()
    load_hashes()
    counts = Counter(len(item[1][4][2][6]) for item in cover)
    print(f"PASS singleton-selector-cover residual-leaves={len(cover)} memberships={len(memberships)} "
          f"parent-counts={dict(sorted(counts.items()))} disjoint=153 exhaustive=153 "
          f"manifest_sha256={hashlib.sha256(manifest).hexdigest()}")
    return cover, memberships, manifest


def reconstruct(member):
    variables, clauses, selectors = residual.reconstruct(member[1])
    clauses.append((selectors[member[2]],))
    return variables, clauses, selectors


def check(path):
    _, memberships, manifest = check_cover()
    metadata, variables, clauses, declared = parse_cnf(path)
    try:
        ordinal = int(dict(metadata).get("membership-ordinal", "-1"))
    except ValueError as error:
        raise RuntimeError("invalid singleton membership ordinal") from error
    if not 0 <= ordinal < len(memberships):
        raise RuntimeError("singleton membership ordinal outside manifest")
    member = memberships[ordinal]
    expected_variables, expected_clauses, selectors = reconstruct(member)
    if metadata != producer.metadata(ordinal, member, manifest, selectors):
        raise RuntimeError("singleton-parent metadata differs")
    if variables != expected_variables or clauses != expected_clauses or declared != producer.dimensions(member):
        raise RuntimeError("singleton-parent CNF differs from exact selected parent")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != load_hashes()[producer.membership_key(member)]:
        raise RuntimeError("singleton-parent CNF hash differs")
    print(f"PASS membership={ordinal:04d} key={producer.membership_key(member)} "
          f"selector={selectors[member[2]]} sha256={digest}")


def check_scout(path=SCOUT_PATH, hash_path=HASH_PATH, require_frozen_identity=True):
    _, memberships, manifest = check_cover()
    scout = path.read_bytes()
    if require_frozen_identity and (len(scout), hashlib.sha256(scout).hexdigest()) != SCOUT_IDENTITY:
        raise RuntimeError("singleton scout bytes or hash differ from frozen campaign")
    text = scout.decode("ascii")
    payload = json.loads(text)
    if scout != (json.dumps(payload, sort_keys=True, indent=2) + "\n").encode("ascii"):
        raise RuntimeError("singleton scout is not canonical ASCII JSON")
    ledger = hash_path.read_bytes()
    hashes = load_hashes(hash_path)
    expected_header = {
        "schema": SCOUT_SCHEMA,
        "seconds_per_membership": SCOUT_SECONDS, "jobs": SCOUT_JOBS, "solver": SOLVER_PATH,
        "solver_bytes": SOLVER_IDENTITY[0], "solver_sha256": SOLVER_IDENTITY[1],
        "solver_version": SOLVER_IDENTITY[2], "manifest_bytes": len(manifest),
        "manifest_sha256": hashlib.sha256(manifest).hexdigest(), "hash_ledger_bytes": len(ledger),
        "hash_ledger_sha256": hashlib.sha256(ledger).hexdigest(),
    }
    if set(payload) != set(expected_header) | {"rows"} or any(
            payload.get(name) != value for name, value in expected_header.items()):
        raise RuntimeError("singleton scout provenance or recorded job count differs")
    rows = payload.get("rows", [])
    if len(rows) != len(memberships):
        raise RuntimeError("singleton scout omits or duplicates memberships")
    for ordinal, (member, row) in enumerate(zip(memberships, rows)):
        expected = {"membership": ordinal, "key": producer.membership_key(member),
                    "residual_leaf": member[0], "parent_ordinal": member[2],
                    "accepted_ordinal": member[3][0], "cover_index": member[3][1],
                    "job": ordinal % SCOUT_JOBS,
                    "cnf_sha256": hashes[producer.membership_key(member)]}
        if any(row.get(name) != value for name, value in expected.items()):
            raise RuntimeError(f"singleton scout row differs: {ordinal:04d}")
        if set(row) != set(expected) | {"status", "seconds"}:
            raise RuntimeError(f"singleton scout row framing differs: {ordinal:04d}")
        if row.get("status") not in ("SAT", "UNSAT", "TIMEOUT"):
            raise RuntimeError(f"singleton scout status invalid: {ordinal:04d}")
        seconds = row.get("seconds")
        if isinstance(seconds, bool) or not isinstance(seconds, (int, float)) or not math.isfinite(seconds):
            raise RuntimeError(f"singleton scout timing invalid: {ordinal:04d}")
        if row["status"] == "TIMEOUT":
            sensible = SCOUT_SECONDS <= seconds <= SCOUT_SECONDS + 1
        else:
            sensible = 0 <= seconds < SCOUT_SECONDS
        if not sensible:
            raise RuntimeError(f"singleton scout timing/status framing differs: {ordinal:04d}")
    counts = Counter(row["status"] for row in rows)
    totals = {status: counts[status] for status in ("SAT", "UNSAT", "TIMEOUT")}
    incidences = {status: sum(1 for row in rows if row["status"] == status)
                  for status in ("SAT", "UNSAT", "TIMEOUT")}
    status_sequence = "".join({"SAT": "S", "UNSAT": "U", "TIMEOUT": "T"}[row["status"]]
                              for row in rows)
    if hashlib.sha256(status_sequence.encode("ascii")).hexdigest() != SCOUT_STATUS_SHA256:
        raise RuntimeError("singleton scout exact 1382-status sequence differs")
    if totals != SCOUT_TOTALS or incidences != SCOUT_TOTALS:
        raise RuntimeError("singleton scout totals or membership incidences differ")
    job_counts = Counter(row["job"] for row in rows)
    if job_counts != {0: 691, 1: 691}:
        raise RuntimeError("singleton scout exact job assignment differs")
    print(f"PASS singleton-scout jobs={SCOUT_JOBS} assignments=691/691 "
          f"totals={totals} incidences={incidences} status_sha256={SCOUT_STATUS_SHA256}")
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
