#!/usr/bin/env python3
"""Independent checker for compact positive-gain children and their partition."""

import argparse
import hashlib
import json
import re
from functools import lru_cache
from pathlib import Path

import check_m6_b7_l6_hard_witness_orbits as source
from check_m6_parent_cnf import parse_cnf

HERE = Path(__file__).resolve().parent
FORMAT = "m6-b7-l6-hard-witness-positive-gain-cnf-v1"
MANIFEST_FORMAT = "m6-b7-l6-hard-witness-positive-gain-v1"
HASH_FORMAT = "m6-b7-l6-hard-witness-positive-gain-hashes-v1"
HASH_PATH = HERE / "m6-b7-l6-hard-witness-positive-gain-hashes.tsv"
SCOUT_PATH = HERE / "m6-b7-l6-hard-witness-positive-gain-scout-20s.json"
NO_GAIN_MANIFEST = HERE / "m6-b7-l6-hard-witness-no-gain.tsv"
NO_GAIN_HASH_PATH = HERE / "m6-b7-l6-hard-witness-no-gain-hashes.tsv"
HASH_COLUMNS = "columns\tleaf-ordinal,key,positive-path-literals,alo-clauses,parents,variables,clauses,cnf-sha256"
SOLVER_IDENTITY = (1002216, "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292", "1.7.3")
SOLVER_PATH = "/tmp/opencode/cadical-1.7.3/build/cadical"
SCOUT_STATUSES = "T" * 42 + "U" + "T" * 52 + "U" + "T" + "U" + "T" * 19
SCOUT_COUNTS = {"SAT": 0, "UNSAT": 3, "TIMEOUT": 114}
SCOUT_INCIDENCES = {"SAT": 0, "UNSAT": 30, "TIMEOUT": 1036}
SCOUT_UNSAT_ORDINALS = (42, 95, 97)
SOURCE_PATHS = {
    "witness-manifest": HERE / "m6-b7-l6-hard-witness-orbits.tsv",
    "witness-hash-ledger": HERE / "m6-b7-l6-hard-witness-orbit-hashes.tsv",
    "witness-scout": HERE / "m6-b7-l6-hard-witness-orbit-scout-20s.json",
    "no-gain-manifest": NO_GAIN_MANIFEST,
    "no-gain-hash-ledger": HERE / "m6-b7-l6-hard-witness-no-gain-hashes.tsv",
    "no-gain-scout": HERE / "m6-b7-l6-hard-witness-no-gain-scout-20s.json",
    "no-gain-certificate-ledger": HERE / "m6-b7-l6-hard-witness-no-gain-certificates.tsv",
}
SOURCE_IDENTITIES = {
    "witness-manifest": (7151, "0329c78e2f563670c623206daf8b6b143c3813eac2f50d5e6f7c12b6b791186a"),
    "witness-hash-ledger": (11078, "d38e453e802408fb61b0c8f91641f16e231cfbec875993256b8dfe5acfa59513"),
    "witness-scout": (48447, "1452d679f8cbb12350ec37564f69303fdbc04b3cecf1c037d66f99d8e72d1a3a"),
    "no-gain-manifest": (6831, "a464607da5ca77da9beb4d5634ea5bc51036f44cad3f22354abfae0da9fe83f4"),
    "no-gain-hash-ledger": (11440, "35ceea03f8b3f9d4cc054da5c3114e8fa9b04d1955f2a9bf64b163750fccab90"),
    "no-gain-scout": (48487, "43bf624d24ca9459bf4de999385ed27367392a174aba46fe95b0773e6d1d7a64"),
    "no-gain-certificate-ledger": (26475, "f780c44424d7925b3b2a1e3d7ee1cbc757a7fc0b1daf14264d9699cc9d1532ec"),
}
LEAVES, INCIDENCES = 117, 1066


def verify_sources():
    for name, path in SOURCE_PATHS.items():
        data = path.read_bytes()
        if (len(data), hashlib.sha256(data).hexdigest()) != SOURCE_IDENTITIES[name]:
            raise RuntimeError(f"bound frozen source changed: {name}")


@lru_cache(maxsize=1)
def derive_leaves():
    verify_sources()
    leaves = source.derive_leaves()
    if len(leaves) != LEAVES or sum(len(leaf[2][6]) for leaf in leaves) != INCIDENCES:
        raise RuntimeError("independent frozen witness frontier changed")
    return leaves


def gain_names(leaf):
    return tuple(f"p_{witness}_{midpoint}_{deleted}"
                 for deleted, witness in zip(leaf[3], leaf[4])
                 for midpoint in range(18) if midpoint not in (witness, deleted))


def dimensions(leaf):
    variables, clauses = source.dimensions(leaf)
    return variables, clauses + 1


def manifest_payload(leaves):
    lines = [MANIFEST_FORMAT]
    for name, item in SOURCE_IDENTITIES.items():
        lines.extend((f"{name}-bytes\t{item[0]}", f"{name}-sha256\t{item[1]}"))
    lines.extend((f"leaves\t{LEAVES}", f"parent-incidences\t{INCIDENCES}",
                  "children-per-source\t1", "refinement\tpositive-gain",
                  "partition\tpositive ALO versus committed conjunction of negative units",
                  "partition-exhaustive\tP or not-P, where P is the listed path-variable ALO",
                  "partition-disjoint\tP and not-P is propositionally false",
                  "columns\tleaf-ordinal,key,parent-orbit,parent-key,high-C,ordered-witnesses,"
                  "positive-path-literals,alo-clauses,parents,variables,clauses"))
    for ordinal, leaf in enumerate(leaves):
        variables, clauses = dimensions(leaf)
        lines.append(f"{ordinal:03d}\t{leaf[0]}\t{leaf[1]:02d}\t{leaf[2][0]}\t"
                     f"{','.join(map(str, leaf[3]))}\t{','.join(map(str, leaf[4]))}\t"
                     f"{len(gain_names(leaf))}\t1\t{len(leaf[2][6])}\t{variables}\t{clauses}")
    return ("\n".join(lines) + "\n").encode("ascii")


def load_hashes(manifest, path=HASH_PATH):
    data = path.read_bytes()
    lines = data.decode("ascii").splitlines()
    if len(lines) != LEAVES + 5 or lines[0] != HASH_FORMAT:
        raise RuntimeError("malformed positive-gain hash ledger")
    if lines[1] != f"manifest-bytes\t{len(manifest)}" or \
            lines[2] != f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}" or \
            lines[3] != f"leaves\t{LEAVES}" or lines[4] != HASH_COLUMNS:
        raise RuntimeError("positive-gain hash ledger is not bound to manifest")
    hashes = {}
    for ordinal, line in enumerate(lines[5:]):
        fields = line.split("\t")
        leaf = derive_leaves()[ordinal]
        expected = [f"{ordinal:03d}", leaf[0], str(len(gain_names(leaf))), "1",
                    str(len(leaf[2][6])), str(dimensions(leaf)[0]), str(dimensions(leaf)[1])]
        if len(fields) != 8 or fields[:7] != expected or re.fullmatch(r"[0-9a-f]{64}", fields[7]) is None:
            raise RuntimeError("malformed or incorrect positive-gain hash row")
        hashes[leaf[0]] = fields[7]
    if data != ("\n".join(lines) + "\n").encode("ascii"):
        raise RuntimeError("positive-gain hash ledger is not canonical ASCII TSV")
    return hashes


def load_no_gain_hashes(path=NO_GAIN_HASH_PATH):
    lines = path.read_text(encoding="ascii").splitlines()
    marker = "columns\tleaf-ordinal,key,negative-path-units,parents,variables,clauses,cnf-sha256"
    try:
        rows = lines[lines.index(marker) + 1:]
    except ValueError as error:
        raise RuntimeError("no-gain hash ledger column binding differs") from error
    if len(rows) != LEAVES:
        raise RuntimeError("no-gain hash ledger omits or duplicates leaves")
    result = {}
    for ordinal, (leaf, line) in enumerate(zip(derive_leaves(), rows)):
        fields = line.split("\t")
        expected = [f"{ordinal:03d}", leaf[0], str(len(gain_names(leaf))),
                    str(len(leaf[2][6])), str(source.dimensions(leaf)[0]),
                    str(source.dimensions(leaf)[1] + len(gain_names(leaf)))]
        if len(fields) != 7 or fields[:6] != expected or re.fullmatch(r"[0-9a-f]{64}", fields[6]) is None:
            raise RuntimeError("malformed or incorrect no-gain hash row")
        result[leaf[0]] = fields[6]
    return result


def no_gain_manifest_payload(leaves):
    identities = {
        "witness-manifest": SOURCE_IDENTITIES["witness-manifest"],
        "witness-hash-ledger": SOURCE_IDENTITIES["witness-hash-ledger"],
        "witness-scout": SOURCE_IDENTITIES["witness-scout"],
        "prior-certificate-ledger": (6987, "cd46a986097405c2d270f15f2525df67e586cc53137e09ef5eafeafd42f2bd02"),
    }
    lines = ["m6-b7-l6-hard-witness-no-gain-v1"]
    for name, item in identities.items():
        lines.extend((f"{name}-bytes\t{item[0]}", f"{name}-sha256\t{item[1]}"))
    lines.extend((f"leaves\t{LEAVES}", f"parent-incidences\t{INCIDENCES}",
                  "children-per-source\t1", "scope\texact-no-gain-only; gain refinements excluded",
                  "columns\tleaf-ordinal,key,parent-orbit,parent-key,high-C,ordered-witnesses,"
                  "negative-path-units,parents,variables,clauses"))
    for ordinal, leaf in enumerate(leaves):
        variables, clauses = source.dimensions(leaf)
        lines.append(f"{ordinal:03d}\t{leaf[0]}\t{leaf[1]:02d}\t{leaf[2][0]}\t"
                     f"{','.join(map(str, leaf[3]))}\t{','.join(map(str, leaf[4]))}\t"
                     f"{len(gain_names(leaf))}\t{len(leaf[2][6])}\t{variables}\t"
                     f"{clauses + len(gain_names(leaf))}")
    return ("\n".join(lines) + "\n").encode("ascii")


def reconstruct_common(leaf):
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
    return names, expected_names, expected, selectors


def no_gain_cnf_payload(ordinal, leaf, names, variables, clauses, selectors, manifest):
    identities = {
        "witness-manifest": SOURCE_IDENTITIES["witness-manifest"],
        "witness-hash-ledger": SOURCE_IDENTITIES["witness-hash-ledger"],
        "witness-scout": SOURCE_IDENTITIES["witness-scout"],
        "prior-certificate-ledger": (6987, "cd46a986097405c2d270f15f2525df67e586cc53137e09ef5eafeafd42f2bd02"),
    }
    metadata = [("format", "m6-b7-l6-hard-witness-no-gain-cnf-v1"),
                ("manifest-format", "m6-b7-l6-hard-witness-no-gain-v1"),
                ("manifest-bytes", str(len(manifest))),
                ("manifest-sha256", hashlib.sha256(manifest).hexdigest())]
    for name, item in identities.items():
        metadata.extend(((f"{name}-bytes", str(item[0])), (f"{name}-sha256", item[1])))
    metadata.extend((("leaf-ordinal", str(ordinal)), ("source-witness-key", leaf[0]),
                     ("parent-orbit-ordinal", str(leaf[1])), ("parent-orbit-key", leaf[2][0]),
                     ("high-C-order", ",".join(map(str, leaf[3]))),
                     ("ordered-witnesses", ",".join(map(str, leaf[4]))),
                     ("children-per-source", "1"), ("refinement", "exact-no-gain"),
                     ("negative-path-unit-clauses", str(len(gain_names(leaf)))),
                     ("gain-refinement-leaves", "excluded"), ("parents", str(len(leaf[2][6]))),
                     ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1]))))
    lines = [f"c {name} {value}" for name, value in metadata]
    lines.extend(f"c var {number} {name}" for number, name in enumerate(variables, 1))
    lines.append(f"p cnf {len(variables)} {len(clauses)}")
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in clauses)
    return ("\n".join(lines) + "\n").encode("ascii")


def validate_complement(leaf, names, positive_alo, negative_units):
    expected_positive = tuple(names.index(name) + 1 for name in gain_names(leaf))
    if positive_alo != expected_positive or negative_units != [(-literal,) for literal in positive_alo]:
        raise RuntimeError("no-gain negative units are not literalwise complements of positive ALO")


def check_partition(no_gain_path=NO_GAIN_MANIFEST, no_gain_hash_path=NO_GAIN_HASH_PATH):
    leaves = derive_leaves()
    lines = no_gain_path.read_text(encoding="ascii").splitlines()
    marker = "columns\tleaf-ordinal,key,parent-orbit,parent-key,high-C,ordered-witnesses,negative-path-units,parents,variables,clauses"
    try:
        start = lines.index(marker) + 1
    except ValueError as error:
        raise RuntimeError("no-gain manifest column binding differs") from error
    rows = lines[start:]
    if len(rows) != LEAVES:
        raise RuntimeError("no-gain complement omits or duplicates source leaves")
    seen = set()
    for ordinal, (leaf, line) in enumerate(zip(leaves, rows)):
        fields = line.split("\t")
        key = fields[1] if len(fields) > 1 else ""
        if key in seen:
            raise RuntimeError("no-gain complement duplicates a source leaf")
        seen.add(key)
        expected = [f"{ordinal:03d}", leaf[0], f"{leaf[1]:02d}", leaf[2][0],
                    ",".join(map(str, leaf[3])), ",".join(map(str, leaf[4])),
                    str(len(gain_names(leaf))), str(len(leaf[2][6]))]
        if len(fields) != 10 or fields[:8] != expected:
            raise RuntimeError("no-gain complement path set or source binding differs")
    if seen != {leaf[0] for leaf in leaves}:
        raise RuntimeError("no-gain complement source cover differs")
    manifest = no_gain_manifest_payload(leaves)
    if no_gain_path.read_bytes() != manifest:
        raise RuntimeError("no-gain manifest differs from independent reconstruction")
    hashes = load_no_gain_hashes(no_gain_hash_path)
    for ordinal, leaf in enumerate(leaves):
        names, variables, common, selectors = reconstruct_common(leaf)
        positive_alo = tuple(names.index(name) + 1 for name in gain_names(leaf))
        negative_units = [(-literal,) for literal in positive_alo]
        validate_complement(leaf, names, positive_alo, negative_units)
        clauses = common + negative_units
        payload = no_gain_cnf_payload(ordinal, leaf, names, variables, clauses, selectors, manifest)
        if hashlib.sha256(payload).hexdigest() != hashes[leaf[0]]:
            raise RuntimeError(f"independently reconstructed no-gain CNF hash differs: {ordinal:03d}")
    print("PASS partition=117 reconstructed-no-gain-CNFs=117 literalwise-complements=117 proof=P-or-not-P path_literals=16/32")


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
                   ("children-per-source", "1"), ("refinement", "positive-gain"),
                   ("positive-path-literals", str(len(gain_names(leaf)))),
                   ("positive-path-alo-clauses", "1"),
                   ("complement", "committed-exact-no-gain"),
                   ("parents", str(len(leaf[2][6]))),
                   ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1]))))
    return result


def reconstruct(leaf):
    names, expected_names, expected, selectors = reconstruct_common(leaf)
    expected.append(tuple(names.index(path_name) + 1 for path_name in gain_names(leaf)))
    return expected_names, expected, selectors


def check(path):
    leaves = derive_leaves()
    manifest = manifest_payload(leaves)
    metadata, variables, clauses, declared = parse_cnf(path)
    ordinal = int(dict(metadata).get("leaf-ordinal", "-1"))
    if not 0 <= ordinal < LEAVES:
        raise RuntimeError("positive-gain leaf ordinal outside frozen frontier")
    leaf = leaves[ordinal]
    expected_names, expected, selectors = reconstruct(leaf)
    if metadata != expected_metadata(ordinal, leaf, manifest, selectors) or variables != expected_names:
        raise RuntimeError("positive-gain metadata or variable map differs")
    if clauses != expected or declared != dimensions(leaf):
        raise RuntimeError("positive-gain CNF clauses or dimensions differ")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != load_hashes(manifest)[leaf[0]]:
        raise RuntimeError("positive-gain CNF hash differs from ledger")
    print(f"PASS positive-gain={ordinal:03d} key={leaf[0]} alo_width={len(gain_names(leaf))} "
          f"parents={len(leaf[2][6])} vars={declared[0]} clauses={declared[1]} sha256={digest}")
    return variables, clauses


def check_scout(path=SCOUT_PATH, hash_path=HASH_PATH):
    leaves = derive_leaves()
    manifest = manifest_payload(leaves)
    hashes = load_hashes(manifest, hash_path)
    payload = json.loads(path.read_text(encoding="ascii"))
    ledger = hash_path.read_bytes()
    if payload.get("schema") != "m6-b7-l6-hard-witness-positive-gain-scout-v1" or \
            payload.get("seconds_per_leaf") != 20 or \
            payload.get("solver") != SOLVER_PATH or \
            (payload.get("solver_bytes"), payload.get("solver_sha256"), payload.get("solver_version")) != SOLVER_IDENTITY or \
            (payload.get("manifest_bytes"), payload.get("manifest_sha256")) != (len(manifest), hashlib.sha256(manifest).hexdigest()) or \
            (payload.get("hash_ledger_bytes"), payload.get("hash_ledger_sha256")) != (len(ledger), hashlib.sha256(ledger).hexdigest()):
        raise RuntimeError("positive-gain scout provenance differs")
    rows = payload.get("rows", [])
    if len(rows) != LEAVES:
        raise RuntimeError("positive-gain scout omits or duplicates leaves")
    for ordinal, (leaf, row) in enumerate(zip(leaves, rows)):
        status = {"T": "TIMEOUT", "U": "UNSAT"}[SCOUT_STATUSES[ordinal]]
        expected = {"leaf": ordinal, "key": leaf[0], "parent_orbit": leaf[1],
                    "parent_key": leaf[2][0], "parents": len(leaf[2][6]),
                    "high_c": list(leaf[3]), "ordered_witnesses": list(leaf[4]),
                    "positive_path_literals": len(gain_names(leaf)),
                    "positive_path_alo_clauses": 1, "cnf_sha256": hashes[leaf[0]],
                    "status": status}
        if any(row.get(name) != value for name, value in expected.items()):
            raise RuntimeError(f"positive-gain scout row differs: {ordinal:03d}")
    counts = {status: sum(row["status"] == status for row in rows) for status in ("SAT", "UNSAT", "TIMEOUT")}
    incidences = {status: sum(row["parents"] for row in rows if row["status"] == status) for status in counts}
    unsat_ordinals = tuple(row["leaf"] for row in rows if row["status"] == "UNSAT")
    if counts != SCOUT_COUNTS or incidences != SCOUT_INCIDENCES or unsat_ordinals != SCOUT_UNSAT_ORDINALS:
        raise RuntimeError("positive-gain scout frozen totals or UNSAT ordinals differ")
    print(f"PASS scout counts={counts} incidences={incidences} unsat_ordinals={unsat_ordinals}")
    return payload


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", type=Path, nargs="?")
    parser.add_argument("--partition", action="store_true")
    parser.add_argument("--scout", action="store_true")
    args = parser.parse_args()
    if args.partition:
        check_partition()
    if args.scout:
        check_scout()
    if args.cnf:
        check(args.cnf)
    if not args.partition and not args.scout and not args.cnf:
        parser.error("provide a CNF, --partition, or --scout")


if __name__ == "__main__":
    main()
