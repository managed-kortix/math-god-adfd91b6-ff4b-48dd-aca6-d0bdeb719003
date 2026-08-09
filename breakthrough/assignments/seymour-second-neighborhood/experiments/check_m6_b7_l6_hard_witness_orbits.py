#!/usr/bin/env python3
"""Independent stabilizer and CNF checker for the hard robust-witness split."""

import argparse
import hashlib
import itertools
import json
from functools import lru_cache
from pathlib import Path

import check_m6_b7_l6_hard_orbits as source
from check_m6_parent_cnf import (
    BASE_CLAUSES, BASE_CLAUSE_SHA256, BASE_VARIABLES, BASE_VARIABLE_MAP_SHA256,
    PAIRS, clause_sha256, expected_projection, parse_cnf, variable_map_sha256,
)
from snc_cnf import generate

HERE = Path(__file__).resolve().parent
FORMAT = "m6-b7-l6-hard-witness-orbit-cnf-v1"
MANIFEST_FORMAT = "m6-b7-l6-hard-witness-orbits-v1"
HASH_FORMAT = "m6-b7-l6-hard-witness-orbit-hashes-v1"
HASH_PATH = HERE / "m6-b7-l6-hard-witness-orbit-hashes.tsv"
B_VERTICES = tuple(range(9, 16))
C_VERTICES = (16, 17)
TIMEOUT_ORBITS, TIMEOUT_INCIDENCES, WITNESS_LEAVES, WITNESS_INCIDENCES = 28, 252, 117, 1066
SOURCE_PATHS = {
    "orbit-manifest": HERE / "m6-b7-l6-hard-orbits.tsv",
    "orbit-hash-ledger": HERE / "m6-b7-l6-hard-orbit-hashes.tsv",
    "orbit-scout": HERE / "m6-b7-l6-hard-orbit-scout-20s.json",
    "orbit-certificate-ledger": HERE / "m6-b7-l6-hard-orbit-certificates.tsv",
}
SOURCE_IDENTITIES = {
    "orbit-manifest": (5533, "6c1080c6f97f92e68a9de6bc762145ceac9086f0b87dc4aa4ed73a746861b2d4"),
    "orbit-hash-ledger": (4025, "83fe978c89f6f0c7901924123a322d42c2f31a1a15e931cdb30e861e31497030"),
    "orbit-scout": (11413, "32fa8260e2efb3cc326bafc2ce2d375ec84bf77ebb2fb5f9efd96b5b995ef31a"),
    "orbit-certificate-ledger": (6987, "cd46a986097405c2d270f15f2525df67e586cc53137e09ef5eafeafd42f2bd02"),
}


def verify_sources():
    for name, path in SOURCE_PATHS.items():
        data = path.read_bytes()
        if (len(data), hashlib.sha256(data).hexdigest()) != SOURCE_IDENTITIES[name]:
            raise RuntimeError(f"bound frozen orbit source changed: {name}")


def explicit_stabilizer(subsets):
    result = []
    for image in itertools.permutations(B_VERTICES):
        permutation = dict(zip(B_VERTICES, image))
        if all({permutation[b] for b in subset} == set(subset) for subset in subsets):
            result.append(permutation)
    return tuple(result)


def eligible(state, subsets, deleted):
    witnesses = {b for b in B_VERTICES if b not in subsets[deleted - 16]}
    other = 33 - deleted
    if state[1] == f"{other}>{deleted}":
        witnesses.add(other)
    return witnesses


def canonical_orbits(state, subsets):
    high = tuple(c for c, bit in zip(C_VERTICES, state[2]) if bit)
    universe = set(itertools.product(*(eligible(state, subsets, c) for c in high)))
    group = explicit_stabilizer(subsets)
    cells = []
    unseen = set(universe)
    while unseen:
        representative = min(unseen)
        orbit = {tuple(permutation.get(w, w) for w in representative) for permutation in group}
        if not orbit <= universe:
            raise RuntimeError("explicit stabilizer failed to preserve witness eligibility")
        cells.append((representative, len(orbit)))
        unseen -= orbit
    if sum(size for _, size in cells) != len(universe):
        raise RuntimeError("witness orbits are not a disjoint complete labelled cover")
    if any(representative != min(tuple(permutation.get(w, w) for w in representative)
                                 for permutation in group) for representative, _ in cells):
        raise RuntimeError("noncanonical witness representative")
    return high, tuple(cells)


def verify_parent_invariance(parent):
    group = explicit_stabilizer(parent[5])
    projections = {frozenset(expected_projection(row)[1]) for _, _, row in parent[6]}
    for holes in projections:
        for permutation in group:
            image = frozenset(tuple(sorted((permutation.get(a, a), permutation.get(b, b))))
                              for a, b in holes)
            if image not in projections:
                raise RuntimeError("fixed-subset stabilizer does not preserve parent selector family")


@lru_cache(maxsize=1)
def derive_leaves():
    verify_sources()
    parents = source.derive_leaves()
    scout = json.loads(SOURCE_PATHS["orbit-scout"].read_text(encoding="ascii"))
    rows = scout.get("rows", [])
    ordinals = tuple(row["leaf"] for row in rows if row.get("status") == "TIMEOUT")
    if len(ordinals) != TIMEOUT_ORBITS or sum(rows[i]["parents"] for i in ordinals) != TIMEOUT_INCIDENCES:
        raise RuntimeError("independent frozen TIMEOUT frontier changed")
    leaves = []
    for parent_ordinal in ordinals:
        parent = parents[parent_ordinal]
        verify_parent_invariance(parent)
        high, cells = canonical_orbits(parent[3], parent[5])
        for witness_ordinal, (witnesses, orbit_size) in enumerate(cells):
            leaves.append((f"o{parent_ordinal:02d}-w{witness_ordinal:02d}", parent_ordinal,
                           parent, high, witnesses, orbit_size))
    if len(leaves) != WITNESS_LEAVES or sum(len(leaf[2][6]) for leaf in leaves) != WITNESS_INCIDENCES:
        raise RuntimeError("independent witness-orbit totals changed")
    return tuple(leaves)


def dimensions(leaf):
    count = len(leaf[2][6])
    return BASE_VARIABLES + count, BASE_CLAUSES["B7"] + 18 + 153 * count + len(leaf[3])


def manifest_payload(leaves):
    lines = [MANIFEST_FORMAT]
    for name, item in SOURCE_IDENTITIES.items():
        lines.extend((f"{name}-bytes\t{item[0]}", f"{name}-sha256\t{item[1]}"))
    lines.extend((f"timeout-orbits\t{TIMEOUT_ORBITS}", f"timeout-parent-incidences\t{TIMEOUT_INCIDENCES}",
                  f"witness-leaves\t{WITNESS_LEAVES}", f"witness-parent-incidences\t{WITNESS_INCIDENCES}",
                  "cover\texistential-ALO; overlaps allowed; equisatisfiable modulo fixed-subset stabilizer",
                  "columns\twitness-ordinal,key,parent-orbit,parent-key,witness-orbit,high-C,ordered-witnesses,"
                  "labelled-orbit-size,parents,variables,clauses"))
    for ordinal, leaf in enumerate(leaves):
        key, parent_ordinal, parent, high, witnesses, orbit_size = leaf
        variables, clauses = dimensions(leaf)
        lines.append(f"{ordinal:03d}\t{key}\t{parent_ordinal:02d}\t{parent[0]}\t{key.rsplit('w', 1)[1]}\t"
                     f"{','.join(map(str, high))}\t{','.join(map(str, witnesses))}\t{orbit_size}\t"
                     f"{len(parent[6])}\t{variables}\t{clauses}")
    return ("\n".join(lines) + "\n").encode("ascii")


def load_hashes():
    lines = HASH_PATH.read_text(encoding="ascii").splitlines()
    if len(lines) != WITNESS_LEAVES + 5 or lines[0] != HASH_FORMAT:
        raise RuntimeError("malformed witness hash ledger")
    hashes = {}
    for ordinal, line in enumerate(lines[5:]):
        fields = line.split("\t")
        if len(fields) != 6 or fields[0] != f"{ordinal:03d}" or len(fields[5]) != 64:
            raise RuntimeError("malformed witness hash row")
        hashes[fields[1]] = fields[5]
    return hashes


@lru_cache(maxsize=1)
def frozen_base():
    cnf = generate(18, 7, 6, robust_witness=True, arc_minimal=True)
    return tuple(cnf.names), tuple(cnf.clauses)


def expected_metadata(ordinal, leaf, manifest, selectors):
    key, parent_ordinal, parent, high, witnesses, orbit_size = leaf
    result = [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
              ("manifest-bytes", str(len(manifest))),
              ("manifest-sha256", hashlib.sha256(manifest).hexdigest())]
    for name, item in SOURCE_IDENTITIES.items():
        result.extend(((f"{name}-bytes", str(item[0])), (f"{name}-sha256", item[1])))
    result.extend((("witness-ordinal", str(ordinal)), ("witness-key", key),
                   ("parent-orbit-ordinal", str(parent_ordinal)), ("parent-orbit-key", parent[0]),
                   ("high-C-order", ",".join(map(str, high))),
                   ("ordered-witnesses", ",".join(map(str, witnesses))),
                   ("labelled-witness-orbit-size", str(orbit_size)),
                   ("existential-cover", "ALO-overlap-equisatisfiable"),
                   ("robust-witness-unit-clauses", str(len(high))),
                   ("parents", str(len(parent[6]))), ("first-selector", str(selectors[0])),
                   ("last-selector", str(selectors[-1]))))
    return result


def check(path):
    leaves = derive_leaves()
    manifest = manifest_payload(leaves)
    metadata, variables, clauses, declared = parse_cnf(path)
    ordinal = int(dict(metadata).get("witness-ordinal", "-1"))
    if not 0 <= ordinal < WITNESS_LEAVES:
        raise RuntimeError("witness ordinal outside exact cover")
    leaf = leaves[ordinal]
    names, base = map(list, frozen_base())
    if (len(names) != BASE_VARIABLES or variable_map_sha256(names) != BASE_VARIABLE_MAP_SHA256 or
            len(base) != BASE_CLAUSES["B7"] or clause_sha256(base) != BASE_CLAUSE_SHA256["B7"]):
        raise RuntimeError("independent B7 base identity changed")
    parent, state, subsets = leaf[2], leaf[2][3], leaf[2][5]
    units = [(names.index({"h": "h_16_17", "16>17": "a_16_17", "17>16": "a_17_16"}[state[1]]) + 1,)]
    for c, bit in zip(C_VERTICES, state[2]):
        variable = names.index(f"cnt_d1_{c}_17_9") + 1
        units.append((variable if bit else -variable,))
    for c, subset in zip(C_VERTICES, subsets):
        for b in B_VERTICES:
            variable = names.index(f"a_{c}_{b}") + 1
            units.append((variable if b in subset else -variable,))
    selectors = list(range(BASE_VARIABLES + 1, BASE_VARIABLES + len(parent[6]) + 1))
    expected_names = names + [f"b7_l6_hard_orbit_selector_{i:02d}" for i in range(len(selectors))]
    if metadata != expected_metadata(ordinal, leaf, manifest, selectors) or variables != expected_names:
        raise RuntimeError("witness metadata or variable map differs")
    expected = base + units + [tuple(selectors)]
    for selector, (_, _, row) in zip(selectors, parent[6]):
        holes = expected_projection(row)[1]
        for pair in PAIRS:
            hole = names.index(f"h_{pair[0]}_{pair[1]}") + 1
            expected.append((-selector, hole if pair in holes else -hole))
    for deleted, witness in zip(leaf[3], leaf[4]):
        expected.append((names.index(f"wit_{witness}_{deleted}") + 1,))
    if clauses != expected or declared != dimensions(leaf):
        raise RuntimeError("witness CNF clauses or dimensions differ")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != load_hashes()[leaf[0]]:
        raise RuntimeError("witness CNF hash differs from ledger")
    print(f"PASS witness={ordinal:03d} key={leaf[0]} parents={len(parent[6])} "
          f"vars={declared[0]} clauses={declared[1]} sha256={digest}")
    return variables, clauses


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", type=Path)
    args = parser.parse_args()
    check(args.cnf)


if __name__ == "__main__":
    main()
