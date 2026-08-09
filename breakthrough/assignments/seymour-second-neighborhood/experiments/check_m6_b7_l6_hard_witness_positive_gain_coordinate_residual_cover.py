#!/usr/bin/env python3
"""Independent complete source-coverage checker for the residual cover."""

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

import check_m6_b7_l6_hard_witness_positive_gain_coordinate as frozen
import m6_b7_l6_hard_witness_positive_gain_coordinate_residual_cover as producer
from check_m6_parent_cnf import parse_cnf

HERE = Path(__file__).resolve().parent
MANIFEST_PATH = HERE / "m6-b7-l6-hard-witness-positive-gain-coordinate-residual-cover.tsv"
HASH_PATH = HERE / "m6-b7-l6-hard-witness-positive-gain-coordinate-residual-cover-hashes.tsv"
SCOUT_PATH = HERE / "m6-b7-l6-hard-witness-positive-gain-coordinate-residual-cover-scout-15s.json"


def independently_reduce(child):
    deleted, witness, leaf = child[2], child[3], child[4]
    other = 33 - deleted
    state, subsets = leaf[2][3][1], leaf[2][5]
    full = tuple((witness, midpoint, deleted) for midpoint in range(18) if midpoint not in (witness, deleted))
    if witness == other and state == f"{other}>{deleted}":
        return "tautological", full
    if witness in producer.C:
        raise RuntimeError("unproved C-witness reduction")
    if state == f"{other}>{deleted}" and witness not in subsets[other - 16]:
        return "structural", ((witness, other, deleted),)
    paths = tuple((witness, midpoint, deleted) for midpoint in producer.B
                  if midpoint != witness and midpoint not in subsets[deleted - 16])
    if not 2 <= len(paths) <= 6:
        raise RuntimeError("independent B reduction width differs")
    return "b-reduced", paths


def path_name(path):
    return f"p_{path[0]}_{path[1]}_{path[2]}"


def prove_source_disjunction(items, retained, certified):
    """Reconstruct the source ALO and prove its residual child disjunction."""
    leaf = items[0][1][4]
    source_literals = set(frozen.source.gain_names(leaf))
    coordinate_literals = []
    for _, child, _, _ in items:
        literals = {path_name(path) for path in producer.coordinate.coordinate_paths(child)}
        if len(literals) != 16:
            raise RuntimeError("coordinate child does not reconstruct a 16-literal ALO")
        coordinate_literals.append(literals)
    if set().union(*coordinate_literals) != source_literals or any(
            coordinate_literals[i] & coordinate_literals[j]
            for i in range(len(coordinate_literals)) for j in range(i)):
        raise RuntimeError("coordinate children do not reconstruct the source disjunction")

    uncertified = [item for item in items if item[0] not in certified]
    equivalent = [item for item in uncertified if item[2] in ("tautological", "structural")]
    if equivalent:
        if retained != equivalent[:1]:
            raise RuntimeError("source-equivalent representative selection differs")
        return

    expected = uncertified
    if retained != expected:
        raise RuntimeError("residual source is not exactly its uncertified child disjunction")
    if not expected:
        raise RuntimeError("coordinate certificates unexpectedly close a whole source")
    for item in retained:
        reduced = {path_name(path) for path in item[3]}
        full = coordinate_literals[items.index(item)]
        if not reduced or not reduced <= full or item[2] != "b-reduced":
            raise RuntimeError("proper child reduction is not contained in its coordinate ALO")


@lru_cache(maxsize=1)
def derive():
    producer.verify_sources()
    witness_sources = frozen.source.derive_leaves()
    if len(witness_sources) != producer.WITNESS_SOURCES:
        raise RuntimeError("failed to reconstruct all 117 witness sources")
    derived_children = frozen.derive_children()
    children = producer.coordinate.load_leaves()
    if len(children) != len(derived_children):
        raise RuntimeError("producer and independently reconstructed coordinate censuses differ")
    scout = frozen.check_scout()
    certified = {row["leaf"] for row in scout["rows"] if row["status"] == "UNSAT"}
    grouped = defaultdict(list)
    for ordinal, (child, derived_child) in enumerate(zip(children, derived_children)):
        if (child[:4], child[4][0]) != (derived_child[:4], derived_child[4][0]):
            raise RuntimeError("producer and independent coordinate identities differ")
        grouped[child[0]].append((ordinal, child, *independently_reduce(derived_child)))

    unresolved, cover = [], []
    covered_sources = set()
    for source_ordinal in frozen.timeout_ordinals():
        items = grouped[source_ordinal]
        unresolved.append((source_ordinal, items[0][1][4]))
        uncertified = [item for item in items if item[0] not in certified]
        equivalent = [item for item in uncertified if item[2] in ("tautological", "structural")]
        chosen = equivalent[:1] if equivalent else uncertified
        if equivalent and len(chosen) != 1:
            raise RuntimeError("source-equivalent coordinate representative is not minimal")
        prove_source_disjunction(items, chosen, certified)
        cover.extend(chosen)
        covered_sources.add(source_ordinal)

    ancestor_certified = set(range(producer.WITNESS_SOURCES)) - set(frozen.timeout_ordinals())
    if len(ancestor_certified) != producer.ANCESTOR_CERTIFICATES:
        raise RuntimeError("ancestor certificate scope changed")
    if ancestor_certified | covered_sources != set(range(producer.WITNESS_SOURCES)):
        raise RuntimeError("117-source coverage is incomplete")
    return tuple(unresolved), tuple(cover), ancestor_certified, certified


@lru_cache(maxsize=1)
def load_hashes(manifest):
    lines = HASH_PATH.read_text(encoding="ascii").splitlines()
    header = [producer.HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
              f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}",
              f"leaves\t{producer.LEAVES}",
              "columns\tcover-ordinal,key,coordinate-ordinal,disposition,alo-width,parents,variables,clauses,cnf-sha256"]
    if lines[:5] != header or len(lines) != producer.LEAVES + 5:
        raise RuntimeError("residual-cover hash ledger header differs")
    result = {}
    for ordinal, (item, line) in enumerate(zip(derive()[1], lines[5:])):
        fields = line.split("\t")
        variables, clauses = producer.dimensions(item)
        expected = [f"{ordinal:03d}", producer.key(item), f"{item[0]:03d}", item[2],
                    str(len(item[3])), str(len(item[1][4][2][6])), str(variables), str(clauses)]
        if len(fields) != 9 or fields[:8] != expected or re.fullmatch(r"[0-9a-f]{64}", fields[8]) is None:
            raise RuntimeError("residual-cover hash row differs")
        if fields[1] in result:
            raise RuntimeError("duplicate residual-cover key")
        result[fields[1]] = fields[8]
    return result


def reconstruct(item):
    coordinate_ordinal, _, _, paths = item
    derived_child = frozen.derive_children()[coordinate_ordinal]
    names, variables, clauses, selectors = frozen.reconstruct_common(derived_child[4])
    clauses.append(tuple(names.index(f"p_{w}_{midpoint}_{deleted}") + 1
                         for w, midpoint, deleted in paths))
    return variables, clauses, selectors


@lru_cache(maxsize=1)
def check_coverage():
    unresolved, cover, ancestor_certified, coordinate_certified = derive()
    dispositions = Counter(item[2] for item in cover)
    memberships = Counter()
    for item in cover:
        memberships[item[2]] += len(item[1][4][2][6])
    if (len(unresolved), sum(len(leaf[2][6]) for _, leaf in unresolved)) != (114, 1036):
        raise RuntimeError("unresolved source totals differ")
    if (len(cover), sum(len(item[1][4][2][6]) for item in cover)) != (153, 1382):
        raise RuntimeError("cover totals differ")
    if dispositions != {"tautological": 18, "structural": 42, "b-reduced": 93}:
        raise RuntimeError("cover disposition census differs")
    manifest = producer.manifest_payload(unresolved, cover)
    if MANIFEST_PATH.read_bytes() != manifest:
        raise RuntimeError("residual-cover manifest differs from independent reconstruction")
    load_hashes(manifest)
    print(f"PASS source-coverage witness=117 ancestor-certified={len(ancestor_certified)} "
          f"coordinate-certified={len(coordinate_certified)} unresolved=114/1036 cover=153/1382 "
          f"dispositions={dict(dispositions)} memberships={dict(memberships)}")
    return cover, manifest


def check(path):
    cover, manifest = check_coverage()
    metadata, variables, clauses, declared = parse_cnf(path)
    try:
        ordinal = int(dict(metadata).get("cover-ordinal", "-1"))
    except ValueError as error:
        raise RuntimeError("invalid residual-cover ordinal") from error
    if not 0 <= ordinal < len(cover):
        raise RuntimeError("residual-cover ordinal outside frontier")
    item = cover[ordinal]
    expected_variables, expected_clauses, selectors = reconstruct(item)
    if metadata != producer.metadata(ordinal, item, manifest, selectors):
        raise RuntimeError("residual-cover metadata differs")
    if variables != expected_variables or clauses != expected_clauses or declared != producer.dimensions(item):
        raise RuntimeError("residual-cover CNF differs")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != load_hashes(manifest)[producer.key(item)]:
        raise RuntimeError("residual-cover CNF hash differs")
    print(f"PASS cover-leaf={ordinal:03d} key={producer.key(item)} disposition={item[2]} sha256={digest}")


def check_scout(path=SCOUT_PATH):
    cover, manifest = check_coverage()
    ledger = HASH_PATH.read_bytes()
    hashes = load_hashes(manifest)
    payload = json.loads(path.read_text(encoding="ascii"))
    expected_header = {
        "schema": "m6-b7-l6-hard-witness-positive-gain-coordinate-residual-cover-scout-v1",
        "seconds_per_leaf": 15,
        "solver": frozen.SOLVER_PATH,
        "solver_bytes": frozen.SOLVER_IDENTITY[0],
        "solver_sha256": frozen.SOLVER_IDENTITY[1],
        "solver_version": frozen.SOLVER_IDENTITY[2],
        "manifest_bytes": len(manifest),
        "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
        "hash_ledger_bytes": len(ledger),
        "hash_ledger_sha256": hashlib.sha256(ledger).hexdigest(),
    }
    if any(payload.get(name) != value for name, value in expected_header.items()):
        raise RuntimeError("residual-cover scout provenance differs")
    rows = payload.get("rows", [])
    if len(rows) != producer.LEAVES:
        raise RuntimeError("residual-cover scout omits or duplicates leaves")
    for ordinal, (item, row) in enumerate(zip(cover, rows)):
        child = item[1]
        expected = {"leaf": ordinal, "key": producer.key(item), "coordinate_leaf": item[0],
                    "source_leaf": child[0], "source_key": child[4][0],
                    "disposition": item[2], "deleted": child[2], "witness": child[3],
                    "alo_width": len(item[3]), "parents": len(child[4][2][6]),
                    "status": "TIMEOUT", "cnf_sha256": hashes[producer.key(item)]}
        if any(row.get(name) != value for name, value in expected.items()):
            raise RuntimeError(f"residual-cover scout row differs: {ordinal:03d}")
        if not isinstance(row.get("seconds"), (int, float)) or row["seconds"] < 15:
            raise RuntimeError(f"residual-cover scout timing differs: {ordinal:03d}")
    if sum(row["parents"] for row in rows) != producer.MEMBERSHIPS:
        raise RuntimeError("residual-cover scout membership total differs")
    print(f"PASS residual-scout counts={{'SAT': 0, 'UNSAT': 0, 'TIMEOUT': 153}} memberships=1382")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", type=Path, nargs="?")
    parser.add_argument("--coverage", action="store_true")
    parser.add_argument("--scout", action="store_true")
    args = parser.parse_args()
    if args.coverage:
        check_coverage()
    if args.cnf:
        check(args.cnf)
    if args.scout:
        check_scout()
    if not args.coverage and not args.scout and not args.cnf:
        parser.error("provide --coverage, --scout, or a CNF")


if __name__ == "__main__":
    main()
