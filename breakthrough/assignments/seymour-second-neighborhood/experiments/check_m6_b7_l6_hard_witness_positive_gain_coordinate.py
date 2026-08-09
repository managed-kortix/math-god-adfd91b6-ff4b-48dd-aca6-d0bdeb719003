#!/usr/bin/env python3
"""Independent checker for the complete deletion-coordinate positive-gain cover."""

import argparse
import hashlib
import json
import re
from functools import lru_cache
from pathlib import Path

import check_m6_b7_l6_hard_witness_positive_gain as source
from check_m6_parent_cnf import parse_cnf

HERE = Path(__file__).resolve().parent
FORMAT = "m6-b7-l6-hard-witness-positive-gain-coordinate-cnf-v1"
MANIFEST_FORMAT = "m6-b7-l6-hard-witness-positive-gain-coordinate-v1"
HASH_FORMAT = "m6-b7-l6-hard-witness-positive-gain-coordinate-hashes-v1"
MANIFEST_PATH = HERE / "m6-b7-l6-hard-witness-positive-gain-coordinate.tsv"
HASH_PATH = HERE / "m6-b7-l6-hard-witness-positive-gain-coordinate-hashes.tsv"
SCOUT_PATH = HERE / "m6-b7-l6-hard-witness-positive-gain-coordinate-scout-15s.json"
SOURCE_PATHS = {
    "positive-gain-manifest": HERE / "m6-b7-l6-hard-witness-positive-gain.tsv",
    "positive-gain-hash-ledger": HERE / "m6-b7-l6-hard-witness-positive-gain-hashes.tsv",
    "positive-gain-scout": HERE / "m6-b7-l6-hard-witness-positive-gain-scout-20s.json",
    "positive-gain-certificate-ledger": HERE / "m6-b7-l6-hard-witness-positive-gain-certificates.tsv",
}
SOURCE_IDENTITIES = {
    "positive-gain-manifest": (7616, "eb0021165e41b9912c92abde3f4b26890075b0faafbabb0ced579ad6bb372ab8"),
    "positive-gain-hash-ledger": (11695, "57a146838c09dca90e83e1ca19a504967199f3fde15f330769f8867a2068552e"),
    "positive-gain-scout": (53533, "f5ed09b7134a3315a37d20db786fdd7d1675b1edc0ab6ef0969655fb7a6802f7"),
    "positive-gain-certificate-ledger": (3687, "ab44c6fccf70dc5bae6b30b82f9e3983fe9c065b82d8301db3fc76bac13e5b59"),
}
SOURCE_LEAVES, LEAVES, INCIDENCES = 114, 219, 1990
SOLVER_IDENTITY = (1002216, "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292", "1.7.3")
SOLVER_PATH = "/tmp/opencode/cadical-1.7.3/build/cadical"
SCOUT_IDENTITY = (92091, "1ad3075ef0386c8bc8afec26b5a2cd392c140d17d8a69daa025063f4e8f3efab")
SCOUT_UNSAT_ORDINALS = (20, 26, 96, 102, 172, 178, 215, 217)
SCOUT_COUNTS = {"SAT": 0, "UNSAT": 8, "TIMEOUT": 211}
SCOUT_INCIDENCES = {"SAT": 0, "UNSAT": 72, "TIMEOUT": 1918}


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def verify_sources():
    for name, path in SOURCE_PATHS.items():
        if identity(path) != SOURCE_IDENTITIES[name]:
            raise RuntimeError(f"bound frozen source changed: {name}")


def timeout_ordinals():
    verify_sources()
    payload = json.loads(SOURCE_PATHS["positive-gain-scout"].read_text(encoding="ascii"))
    rows = payload.get("rows", [])
    if len(rows) != 117 or any(row.get("leaf") != ordinal for ordinal, row in enumerate(rows)):
        raise RuntimeError("source scout does not exactly cover 117 ordered leaves")
    unsat = tuple(row["leaf"] for row in rows if row.get("status") == "UNSAT")
    if any(row.get("status") not in ("UNSAT", "TIMEOUT") for row in rows):
        raise RuntimeError("source scout status outside frozen UNSAT/TIMEOUT scope")
    ledger = SOURCE_PATHS["positive-gain-certificate-ledger"].read_text(encoding="ascii").splitlines()
    markers = [i for i, line in enumerate(ledger) if line.startswith("columns\t")]
    if len(markers) != 1:
        raise RuntimeError("source certificate ledger columns changed")
    certified = tuple(int(line.split("\t", 1)[0]) for line in ledger[markers[0] + 1:])
    if unsat != (42, 95, 97) or certified != unsat:
        raise RuntimeError("source scout and certificate scope are not exactly bound")
    result = tuple(row["leaf"] for row in rows if row["status"] == "TIMEOUT")
    if len(result) != SOURCE_LEAVES:
        raise RuntimeError("source TIMEOUT count changed")
    return result


@lru_cache(maxsize=1)
def derive_children():
    leaves = source.derive_leaves()
    result = []
    for source_ordinal in timeout_ordinals():
        leaf = leaves[source_ordinal]
        for coordinate, (deleted, witness) in enumerate(zip(leaf[3], leaf[4])):
            result.append((source_ordinal, coordinate, deleted, witness, leaf))
    if len(result) != LEAVES or sum(len(child[4][2][6]) for child in result) != INCIDENCES:
        raise RuntimeError("independent deletion-coordinate census changed")
    return tuple(result)


def child_key(child):
    return f"{child[4][0]}-c{child[2]}"


def gain_names(child):
    _, _, deleted, witness, _ = child
    return tuple(f"p_{witness}_{midpoint}_{deleted}" for midpoint in range(18)
                 if midpoint not in (witness, deleted))


def dimensions(child):
    variables, clauses = source.source.dimensions(child[4])
    return variables, clauses + 1


def manifest_payload(children):
    lines = [MANIFEST_FORMAT]
    for name, item in SOURCE_IDENTITIES.items():
        lines.extend((f"{name}-bytes\t{item[0]}", f"{name}-sha256\t{item[1]}"))
    lines.extend((f"source-timeout-leaves\t{SOURCE_LEAVES}", f"leaves\t{LEAVES}",
                  f"parent-incidence-memberships\t{INCIDENCES}",
                  "children-per-source\tone per selected deletion coordinate (one or two)",
                  "coordinate-alo-width\t16",
                  "existential-coverage\tfor source OR_i P_i, child i is P_i; OR_i child_i equals source",
                  "overlap\tallowed exactly when two-coordinate source has both P_0 and P_1 true",
                  "not-a-partition\ttwo-coordinate children may share models; coverage is existential",
                  "columns\tleaf-ordinal,key,source-leaf-ordinal,source-key,coordinate,deleted,witness,"
                  "coordinate-path-literals,alo-clauses,parents,variables,clauses"))
    for ordinal, child in enumerate(children):
        source_ordinal, coordinate, deleted, witness, leaf = child
        variables, clauses = dimensions(child)
        lines.append(f"{ordinal:03d}\t{child_key(child)}\t{source_ordinal:03d}\t{leaf[0]}\t"
                     f"{coordinate}\t{deleted}\t{witness}\t16\t1\t{len(leaf[2][6])}\t"
                     f"{variables}\t{clauses}")
    return ("\n".join(lines) + "\n").encode("ascii")


def load_hashes(manifest, path=HASH_PATH):
    data = path.read_bytes()
    lines = data.decode("ascii").splitlines()
    columns = "columns\tleaf-ordinal,key,source-leaf-ordinal,coordinate,deleted,witness,coordinate-path-literals,alo-clauses,parents,variables,clauses,cnf-sha256"
    if len(lines) != LEAVES + 5 or lines[:5] != [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
            f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}", f"leaves\t{LEAVES}", columns]:
        raise RuntimeError("coordinate hash ledger header or manifest binding differs")
    result = {}
    for ordinal, (child, line) in enumerate(zip(derive_children(), lines[5:])):
        fields = line.split("\t")
        variables, clauses = dimensions(child)
        expected = [f"{ordinal:03d}", child_key(child), f"{child[0]:03d}", str(child[1]),
                    str(child[2]), str(child[3]), "16", "1", str(len(child[4][2][6])),
                    str(variables), str(clauses)]
        if len(fields) != 12 or fields[:11] != expected or re.fullmatch(r"[0-9a-f]{64}", fields[11]) is None:
            raise RuntimeError("coordinate hash row differs")
        if fields[1] in result:
            raise RuntimeError("duplicate coordinate child key")
        result[fields[1]] = fields[11]
    if data != ("\n".join(lines) + "\n").encode("ascii"):
        raise RuntimeError("coordinate hash ledger is not canonical ASCII TSV")
    return result


def reconstruct_common(leaf):
    names, clauses = source.source.frozen_base()
    names = list(names)
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
    variables = names + [f"b7_l6_hard_orbit_selector_{i:02d}" for i in range(len(selectors))]
    expected = list(clauses) + units + [tuple(selectors)]
    for selector, (_, _, row) in zip(selectors, parent[6]):
        holes = source.source.expected_projection(row)[1]
        for pair in source.source.PAIRS:
            hole = names.index(f"h_{pair[0]}_{pair[1]}") + 1
            expected.append((-selector, hole if pair in holes else -hole))
    for deleted, witness in zip(leaf[3], leaf[4]):
        expected.append((names.index(f"wit_{witness}_{deleted}") + 1,))
    return names, variables, expected, selectors


def reconstruct(child):
    names, variables, clauses, selectors = reconstruct_common(child[4])
    clauses.append(tuple(names.index(name) + 1 for name in gain_names(child)))
    return variables, clauses, selectors


def expected_metadata(ordinal, child, manifest, selectors):
    result = [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
              ("manifest-bytes", str(len(manifest))),
              ("manifest-sha256", hashlib.sha256(manifest).hexdigest())]
    for name, item in SOURCE_IDENTITIES.items():
        result.extend(((f"{name}-bytes", str(item[0])), (f"{name}-sha256", item[1])))
    result.extend((("leaf-ordinal", str(ordinal)), ("key", child_key(child)),
                   ("source-leaf-ordinal", str(child[0])), ("source-witness-key", child[4][0]),
                   ("coordinate", str(child[1])), ("deleted", str(child[2])),
                   ("witness", str(child[3])), ("coordinate-path-literals", "16"),
                   ("coordinate-path-alo-clauses", "1"),
                   ("existential-coverage", "coordinate-ALO-overlap-allowed"),
                   ("parents", str(len(child[4][2][6]))), ("first-selector", str(selectors[0])),
                   ("last-selector", str(selectors[-1]))))
    return result


def check(path):
    children = derive_children()
    manifest = manifest_payload(children)
    metadata, variables, clauses, declared = parse_cnf(path)
    try:
        ordinal = int(dict(metadata).get("leaf-ordinal", "-1"))
    except ValueError as error:
        raise RuntimeError("invalid coordinate child ordinal") from error
    if not 0 <= ordinal < LEAVES:
        raise RuntimeError("coordinate child ordinal outside frozen cover")
    child = children[ordinal]
    expected_variables, expected_clauses, selectors = reconstruct(child)
    if metadata != expected_metadata(ordinal, child, manifest, selectors) or variables != expected_variables:
        raise RuntimeError("coordinate child metadata or variable map differs")
    if clauses != expected_clauses or declared != dimensions(child):
        raise RuntimeError("coordinate child clauses or dimensions differ")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != load_hashes(manifest)[child_key(child)]:
        raise RuntimeError("coordinate child hash differs")
    print(f"PASS coordinate={ordinal:03d} key={child_key(child)} source={child[0]:03d} "
          f"deleted={child[2]} witness={child[3]} parents={len(child[4][2][6])} sha256={digest}")
    return variables, clauses


def check_cover():
    children = derive_children()
    manifest = manifest_payload(children)
    if MANIFEST_PATH.read_bytes() != manifest:
        raise RuntimeError("coordinate manifest differs from independent reconstruction")
    load_hashes(manifest)
    grouped = {}
    for child in children:
        grouped.setdefault(child[0], []).append(child)
    if tuple(grouped) != timeout_ordinals() or any(len(items) != len(items[0][4][3]) for items in grouped.values()):
        raise RuntimeError("coordinate children omit or duplicate a selected source coordinate")
    if any(tuple(item[1] for item in items) != tuple(range(len(items))) for items in grouped.values()):
        raise RuntimeError("coordinate indices are not complete and ordered")
    one = sum(len(items) == 1 for items in grouped.values())
    two = sum(len(items) == 2 for items in grouped.values())
    if (one, two) != (9, 105):
        raise RuntimeError("one/two-coordinate source census changed")
    for items in grouped.values():
        source_names = set(source.gain_names(items[0][4]))
        child_names = [set(gain_names(item)) for item in items]
        if set().union(*child_names) != source_names or any(len(names) != 16 for names in child_names) or \
                any(child_names[i] & child_names[j] for i in range(len(items)) for j in range(i)):
            raise RuntimeError("coordinate ALOs do not exactly split the source ALO literal set")
    print(f"PASS existential-cover sources={SOURCE_LEAVES} one-coordinate={one} two-coordinate={two} "
          f"children={LEAVES} incidences={INCIDENCES} overlap=allowed-for-two-coordinate")


def check_scout(path=SCOUT_PATH):
    children = derive_children()
    manifest = manifest_payload(children)
    hashes = load_hashes(manifest)
    ledger = HASH_PATH.read_bytes()
    payload = json.loads(path.read_text(encoding="ascii"))
    if path == SCOUT_PATH and identity(path) != SCOUT_IDENTITY:
        raise RuntimeError("frozen coordinate scout identity differs")
    expected_header = {
        "schema": "m6-b7-l6-hard-witness-positive-gain-coordinate-scout-v1",
        "seconds_per_leaf": 15, "solver": SOLVER_PATH, "solver_bytes": SOLVER_IDENTITY[0],
        "solver_sha256": SOLVER_IDENTITY[1], "solver_version": SOLVER_IDENTITY[2],
        "manifest_bytes": len(manifest), "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
        "hash_ledger_bytes": len(ledger), "hash_ledger_sha256": hashlib.sha256(ledger).hexdigest(),
    }
    if any(payload.get(name) != value for name, value in expected_header.items()):
        raise RuntimeError("coordinate scout provenance differs")
    rows = payload.get("rows", [])
    if len(rows) != LEAVES:
        raise RuntimeError("coordinate scout omits or duplicates leaves")
    for ordinal, (child, row) in enumerate(zip(children, rows)):
        expected = {"leaf": ordinal, "key": child_key(child), "source_leaf": child[0],
                    "source_key": child[4][0], "coordinate": child[1], "deleted": child[2],
                    "witness": child[3], "parents": len(child[4][2][6]),
                    "coordinate_path_literals": 16, "coordinate_path_alo_clauses": 1,
                    "cnf_sha256": hashes[child_key(child)]}
        status = "UNSAT" if ordinal in SCOUT_UNSAT_ORDINALS else "TIMEOUT"
        if any(row.get(name) != value for name, value in expected.items()) or row.get("status") != status:
            raise RuntimeError(f"coordinate scout row differs: {ordinal:03d}")
    counts = {status: sum(row["status"] == status for row in rows)
              for status in ("SAT", "UNSAT", "TIMEOUT")}
    incidences = {status: sum(row["parents"] for row in rows if row["status"] == status)
                  for status in counts}
    if counts != SCOUT_COUNTS or incidences != SCOUT_INCIDENCES:
        raise RuntimeError("coordinate scout frozen totals differ")
    print(f"PASS scout counts={counts} incidences={incidences}")
    return payload


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", type=Path, nargs="?")
    parser.add_argument("--cover", action="store_true")
    parser.add_argument("--scout", action="store_true")
    args = parser.parse_args()
    if args.cover:
        check_cover()
    if args.scout:
        check_scout()
    if args.cnf:
        check(args.cnf)
    if not args.cover and not args.scout and not args.cnf:
        parser.error("provide a CNF, --cover, or --scout")


if __name__ == "__main__":
    main()
