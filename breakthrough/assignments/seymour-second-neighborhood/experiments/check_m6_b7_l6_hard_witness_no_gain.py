#!/usr/bin/env python3
"""Independent structural checker for the frozen witness no-gain layer."""

import argparse
import hashlib
import json
import re
from functools import lru_cache
from pathlib import Path

import check_m6_b7_l6_hard_witness_orbits as source
from check_m6_parent_cnf import parse_cnf

HERE = Path(__file__).resolve().parent
FORMAT = "m6-b7-l6-hard-witness-no-gain-cnf-v1"
MANIFEST_FORMAT = "m6-b7-l6-hard-witness-no-gain-v1"
HASH_FORMAT = "m6-b7-l6-hard-witness-no-gain-hashes-v1"
HASH_PATH = HERE / "m6-b7-l6-hard-witness-no-gain-hashes.tsv"
SCOUT_PATH = HERE / "m6-b7-l6-hard-witness-no-gain-scout-20s.json"
HASH_COLUMNS = "columns\tleaf-ordinal,key,negative-path-units,parents,variables,clauses,cnf-sha256"
SOLVER_IDENTITY = (1002216, "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292", "1.7.3")
SCOUT_STATUSES = (
    "TTTTTUUTUUUUUTTTTUUUUUUUUUTTTTTTUTTTTUUTUUTTUUTUUUUUUUTTTTUUUUU"
    "TTUUUUUUUUUTTUUTUUUTUUTUUUUUUUTTUUUTTUUUUUTTUUUUUUUUUT"
)
SOURCE_PATHS = {
    "witness-manifest": HERE / "m6-b7-l6-hard-witness-orbits.tsv",
    "witness-hash-ledger": HERE / "m6-b7-l6-hard-witness-orbit-hashes.tsv",
    "witness-scout": HERE / "m6-b7-l6-hard-witness-orbit-scout-20s.json",
    "prior-certificate-ledger": HERE / "m6-b7-l6-hard-orbit-certificates.tsv",
}
SOURCE_IDENTITIES = {
    "witness-manifest": (7151, "0329c78e2f563670c623206daf8b6b143c3813eac2f50d5e6f7c12b6b791186a"),
    "witness-hash-ledger": (11078, "d38e453e802408fb61b0c8f91641f16e231cfbec875993256b8dfe5acfa59513"),
    "witness-scout": (48447, "1452d679f8cbb12350ec37564f69303fdbc04b3cecf1c037d66f99d8e72d1a3a"),
    "prior-certificate-ledger": (6987, "cd46a986097405c2d270f15f2525df67e586cc53137e09ef5eafeafd42f2bd02"),
}
LEAVES, INCIDENCES = 117, 1066


def verify_sources():
    for name, path in SOURCE_PATHS.items():
        data = path.read_bytes()
        if (len(data), hashlib.sha256(data).hexdigest()) != SOURCE_IDENTITIES[name]:
            raise RuntimeError(f"bound frozen witness source changed: {name}")


@lru_cache(maxsize=1)
def derive_leaves():
    verify_sources()
    leaves = source.derive_leaves()
    if len(leaves) != LEAVES or sum(len(leaf[2][6]) for leaf in leaves) != INCIDENCES:
        raise RuntimeError("independent frozen witness frontier changed")
    return leaves


def no_gain_names(leaf):
    return tuple(f"p_{witness}_{midpoint}_{deleted}"
                 for deleted, witness in zip(leaf[3], leaf[4])
                 for midpoint in range(18) if midpoint not in (witness, deleted))


def dimensions(leaf):
    variables, clauses = source.dimensions(leaf)
    return variables, clauses + len(no_gain_names(leaf))


def manifest_payload(leaves):
    lines = [MANIFEST_FORMAT]
    for name, item in SOURCE_IDENTITIES.items():
        lines.extend((f"{name}-bytes\t{item[0]}", f"{name}-sha256\t{item[1]}"))
    lines.extend((f"leaves\t{LEAVES}", f"parent-incidences\t{INCIDENCES}",
                  "children-per-source\t1", "scope\texact-no-gain-only; gain refinements excluded",
                  "columns\tleaf-ordinal,key,parent-orbit,parent-key,high-C,ordered-witnesses,"
                  "negative-path-units,parents,variables,clauses"))
    for ordinal, leaf in enumerate(leaves):
        variables, clauses = dimensions(leaf)
        lines.append(f"{ordinal:03d}\t{leaf[0]}\t{leaf[1]:02d}\t{leaf[2][0]}\t"
                     f"{','.join(map(str, leaf[3]))}\t{','.join(map(str, leaf[4]))}\t"
                     f"{len(no_gain_names(leaf))}\t{len(leaf[2][6])}\t{variables}\t{clauses}")
    return ("\n".join(lines) + "\n").encode("ascii")


def load_hashes(manifest, path=HASH_PATH):
    data = path.read_bytes()
    lines = data.decode("ascii").splitlines()
    if len(lines) != LEAVES + 5 or lines[0] != HASH_FORMAT:
        raise RuntimeError("malformed no-gain hash ledger")
    if lines[1] != f"manifest-bytes\t{len(manifest)}" or \
            lines[2] != f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}" or \
            lines[3] != f"leaves\t{LEAVES}" or lines[4] != HASH_COLUMNS:
        raise RuntimeError("no-gain hash ledger is not bound to manifest")
    hashes = {}
    for ordinal, line in enumerate(lines[5:]):
        fields = line.split("\t")
        if len(fields) != 7 or fields[0] != f"{ordinal:03d}" or \
                re.fullmatch(r"[0-9a-f]{64}", fields[6]) is None:
            raise RuntimeError("malformed no-gain hash row")
        leaf = derive_leaves()[ordinal]
        if fields[1:6] != [leaf[0], str(len(no_gain_names(leaf))), str(len(leaf[2][6])),
                            str(dimensions(leaf)[0]), str(dimensions(leaf)[1])]:
            raise RuntimeError("no-gain hash row metadata differs")
        hashes[fields[1]] = fields[6]
    if data != ("\n".join(lines) + "\n").encode("ascii"):
        raise RuntimeError("no-gain hash ledger is not canonical ASCII TSV")
    return hashes


def check_scout(path=SCOUT_PATH, hash_path=HASH_PATH):
    leaves = derive_leaves()
    manifest = manifest_payload(leaves)
    hashes = load_hashes(manifest, hash_path)
    payload = json.loads(path.read_text(encoding="ascii"))
    ledger = hash_path.read_bytes()
    if payload.get("schema") != "m6-b7-l6-hard-witness-no-gain-scout-v1" or \
            payload.get("seconds_per_leaf") != 20 or \
            (payload.get("solver_bytes"), payload.get("solver_sha256"),
             payload.get("solver_version")) != SOLVER_IDENTITY or \
            (payload.get("manifest_bytes"), payload.get("manifest_sha256")) != \
            (len(manifest), hashlib.sha256(manifest).hexdigest()) or \
            (payload.get("hash_ledger_bytes"), payload.get("hash_ledger_sha256")) != \
            (len(ledger), hashlib.sha256(ledger).hexdigest()):
        raise RuntimeError("committed no-gain scout provenance differs")
    rows = payload.get("rows", [])
    if len(rows) != LEAVES:
        raise RuntimeError("committed no-gain scout is incomplete")
    for ordinal, (leaf, row) in enumerate(zip(leaves, rows)):
        status = "UNSAT" if SCOUT_STATUSES[ordinal] == "U" else "TIMEOUT"
        expected = {"leaf": ordinal, "key": leaf[0], "parent_orbit": leaf[1],
                    "parent_key": leaf[2][0], "parents": len(leaf[2][6]),
                    "high_c": list(leaf[3]), "ordered_witnesses": list(leaf[4]),
                    "negative_path_units": len(no_gain_names(leaf)),
                    "cnf_sha256": hashes[leaf[0]], "status": status}
        if any(row.get(name) != value for name, value in expected.items()):
            raise RuntimeError(f"committed no-gain scout row differs: {ordinal:03d}")
    counts = {status: sum(row["status"] == status for row in rows)
              for status in ("UNSAT", "TIMEOUT")}
    incidences = {status: sum(row["parents"] for row in rows if row["status"] == status)
                  for status in counts}
    if counts != {"UNSAT": 75, "TIMEOUT": 42} or incidences != {"UNSAT": 686, "TIMEOUT": 380}:
        raise RuntimeError("committed no-gain scout frontier differs")
    print("PASS scout=75-UNSAT/42-TIMEOUT incidences=686/380")
    return payload


def expected_metadata(ordinal, leaf, manifest, selectors):
    result = [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
              ("manifest-bytes", str(len(manifest))),
              ("manifest-sha256", hashlib.sha256(manifest).hexdigest())]
    for name, item in SOURCE_IDENTITIES.items():
        result.extend(((f"{name}-bytes", str(item[0])), (f"{name}-sha256", item[1])))
    result.extend((("leaf-ordinal", str(ordinal)), ("source-witness-key", leaf[0]),
                   ("parent-orbit-ordinal", str(leaf[1])), ("parent-orbit-key", leaf[2][0]),
                   ("high-C-order", ",".join(map(str, leaf[3]))),
                   ("ordered-witnesses", ",".join(map(str, leaf[4]))),
                   ("children-per-source", "1"), ("refinement", "exact-no-gain"),
                   ("negative-path-unit-clauses", str(len(no_gain_names(leaf)))),
                   ("gain-refinement-leaves", "excluded"), ("parents", str(len(leaf[2][6]))),
                   ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1]))))
    return result


def check(path):
    leaves = derive_leaves()
    manifest = manifest_payload(leaves)
    metadata, variables, clauses, declared = parse_cnf(path)
    ordinal = int(dict(metadata).get("leaf-ordinal", "-1"))
    if not 0 <= ordinal < LEAVES:
        raise RuntimeError("no-gain leaf ordinal outside frozen frontier")
    leaf = leaves[ordinal]
    source_names, source_clauses = source.frozen_base()
    names = list(source_names)
    parent, state, subsets = leaf[2], leaf[2][3], leaf[2][5]
    units = [(names.index({"h": "h_16_17", "16>17": "a_16_17", "17>16": "a_17_16"}[state[1]]) + 1,)]
    for c, bit in zip((16, 17), state[2]):
        variable = names.index(f"cnt_d1_{c}_17_9") + 1
        units.append((variable if bit else -variable,))
    for c, subset in zip((16, 17), subsets):
        for b in range(9, 16):
            variable = names.index(f"a_{c}_{b}") + 1
            units.append((variable if b in subset else -variable,))
    selectors = list(range(len(names) + 1, len(names) + len(parent[6]) + 1))
    expected_names = names + [f"b7_l6_hard_orbit_selector_{i:02d}" for i in range(len(selectors))]
    expected = list(source_clauses) + units + [tuple(selectors)]
    for selector, (_, _, row) in zip(selectors, parent[6]):
        holes = source.expected_projection(row)[1]
        for pair in source.PAIRS:
            hole = names.index(f"h_{pair[0]}_{pair[1]}") + 1
            expected.append((-selector, hole if pair in holes else -hole))
    for deleted, witness in zip(leaf[3], leaf[4]):
        expected.append((names.index(f"wit_{witness}_{deleted}") + 1,))
    for path_name in no_gain_names(leaf):
        expected.append((-(names.index(path_name) + 1),))
    if metadata != expected_metadata(ordinal, leaf, manifest, selectors) or variables != expected_names:
        raise RuntimeError("no-gain metadata or variable map differs")
    if clauses != expected or declared != dimensions(leaf):
        raise RuntimeError("no-gain CNF clauses or dimensions differ")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != load_hashes(manifest)[leaf[0]]:
        raise RuntimeError("no-gain CNF hash differs from ledger")
    print(f"PASS no-gain={ordinal:03d} key={leaf[0]} units={len(no_gain_names(leaf))} "
          f"parents={len(parent[6])} vars={declared[0]} clauses={declared[1]} sha256={digest}")
    return variables, clauses


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", type=Path, nargs="?")
    parser.add_argument("--scout", action="store_true")
    args = parser.parse_args()
    if args.scout:
        check_scout()
    if args.cnf:
        check(args.cnf)
    if not args.scout and not args.cnf:
        parser.error("provide a CNF or --scout")


if __name__ == "__main__":
    main()
