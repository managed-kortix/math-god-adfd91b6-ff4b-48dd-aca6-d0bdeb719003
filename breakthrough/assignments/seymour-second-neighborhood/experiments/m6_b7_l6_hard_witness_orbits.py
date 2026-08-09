#!/usr/bin/env python3
"""Split exactly the 28 frozen hard-orbit TIMEOUTs by robust-witness orbits."""

import argparse
import hashlib
import itertools
import json
import tempfile
from pathlib import Path

import m6_b7_l6_hard_orbits as source

HERE = Path(__file__).resolve().parent
FORMAT = "m6-b7-l6-hard-witness-orbit-cnf-v1"
MANIFEST_FORMAT = "m6-b7-l6-hard-witness-orbits-v1"
HASH_FORMAT = "m6-b7-l6-hard-witness-orbit-hashes-v1"
B_VERTICES = tuple(range(9, 16))
C_VERTICES = (16, 17)
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
TIMEOUT_ORBITS = 28
TIMEOUT_INCIDENCES = 252
WITNESS_LEAVES = 117
WITNESS_INCIDENCES = 1066


def identity(data):
    return len(data), hashlib.sha256(data).hexdigest()


def verify_sources():
    for name, path in SOURCE_PATHS.items():
        if identity(path.read_bytes()) != SOURCE_IDENTITIES[name]:
            raise RuntimeError(f"bound frozen orbit source changed: {name}")


def timeout_ordinals():
    verify_sources()
    payload = json.loads(SOURCE_PATHS["orbit-scout"].read_text(encoding="ascii"))
    if payload.get("schema") != "m6-b7-l6-hard-orbit-scout-v1":
        raise RuntimeError("wrong frozen orbit scout schema")
    rows = payload.get("rows", [])
    result = tuple(row["leaf"] for row in rows if row.get("status") == "TIMEOUT")
    if len(result) != TIMEOUT_ORBITS or sum(rows[i]["parents"] for i in result) != TIMEOUT_INCIDENCES:
        raise RuntimeError("frozen TIMEOUT frontier changed")
    return result


def eligible_witnesses(state, subsets, deleted):
    result = [b for b in B_VERTICES if b not in subsets[deleted - 16]]
    other = 33 - deleted
    if state[1] == f"{other}>{deleted}":
        result.append(other)
    return tuple(result)


def stabilizer(subsets):
    cells = {}
    for b in B_VERTICES:
        cells.setdefault(tuple(b in subset for subset in subsets), []).append(b)
    permutations = []
    for images in itertools.product(*(itertools.permutations(cell) for cell in cells.values())):
        permutation = {vertex: vertex for vertex in C_VERTICES}
        for cell, image in zip(cells.values(), images):
            permutation.update(zip(cell, image))
        permutations.append(permutation)
    return tuple(permutations)


def witness_orbits(state, subsets):
    high = tuple(c for c, bit in zip(C_VERTICES, state[2]) if bit)
    choices = set(itertools.product(*(eligible_witnesses(state, subsets, c) for c in high)))
    permutations = stabilizer(subsets)
    records = []
    while choices:
        representative = min(choices)
        orbit = {tuple(permutation.get(w, w) for w in representative) for permutation in permutations}
        if not orbit <= choices:
            raise RuntimeError("stabilizer does not preserve eligible witness tuples")
        choices -= orbit
        records.append((representative, len(orbit)))
    return high, tuple(records)


def load_leaves():
    parent_leaves = source.load_leaves()
    leaves = []
    for parent_ordinal in timeout_ordinals():
        parent = parent_leaves[parent_ordinal]
        high, orbits = witness_orbits(parent[3], parent[5])
        for witness_ordinal, (witnesses, orbit_size) in enumerate(orbits):
            key = f"o{parent_ordinal:02d}-w{witness_ordinal:02d}"
            leaves.append((key, parent_ordinal, parent, high, witnesses, orbit_size))
    if len(leaves) != WITNESS_LEAVES or sum(len(leaf[2][6]) for leaf in leaves) != WITNESS_INCIDENCES:
        raise RuntimeError("robust-witness orbit totals changed")
    return leaves


def dimensions(leaf):
    parents = len(leaf[2][6])
    variables, clauses = source.dimensions(parents)
    return variables, clauses + len(leaf[3])


def build_leaf(leaf):
    cnf, selectors = source.build_leaf(leaf[2])
    for deleted, witness in zip(leaf[3], leaf[4]):
        cnf.add(cnf.names[f"wit_{witness}_{deleted}"])
    return cnf, selectors


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


def hash_payload(leaves, manifest, hashes=None):
    hashes = hashes or {}
    lines = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
             f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}",
             f"witness-leaves\t{WITNESS_LEAVES}",
             "columns\twitness-ordinal,key,parents,variables,clauses,cnf-sha256"]
    for ordinal, leaf in enumerate(leaves):
        variables, clauses = dimensions(leaf)
        lines.append(f"{ordinal:03d}\t{leaf[0]}\t{len(leaf[2][6])}\t{variables}\t{clauses}\t{hashes.get(leaf[0], '')}")
    return ("\n".join(lines) + "\n").encode("ascii")


def write_leaf(path, ordinal, leaf, cnf, selectors, manifest):
    key, parent_ordinal, parent, high, witnesses, orbit_size = leaf
    metadata = [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
                ("manifest-bytes", str(len(manifest))),
                ("manifest-sha256", hashlib.sha256(manifest).hexdigest())]
    for name, item in SOURCE_IDENTITIES.items():
        metadata.extend(((f"{name}-bytes", str(item[0])), (f"{name}-sha256", item[1])))
    metadata.extend((("witness-ordinal", str(ordinal)), ("witness-key", key),
                     ("parent-orbit-ordinal", str(parent_ordinal)), ("parent-orbit-key", parent[0]),
                     ("high-C-order", ",".join(map(str, high))),
                     ("ordered-witnesses", ",".join(map(str, witnesses))),
                     ("labelled-witness-orbit-size", str(orbit_size)),
                     ("existential-cover", "ALO-overlap-equisatisfiable"),
                     ("robust-witness-unit-clauses", str(len(high))),
                     ("parents", str(len(parent[6]))), ("first-selector", str(selectors[0])),
                     ("last-selector", str(selectors[-1]))))
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in metadata:
            handle.write(f"c {name} {value}\n")
        for name, number in cnf.names.items():
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def populate_hashes(leaves, manifest):
    hashes = {}
    with tempfile.TemporaryDirectory(prefix="m6-hard-witness-hashes-", dir=HERE.parent) as directory:
        path = Path(directory) / "leaf.cnf"
        for ordinal, leaf in enumerate(leaves):
            cnf, selectors = build_leaf(leaf)
            write_leaf(path, ordinal, leaf, cnf, selectors, manifest)
            hashes[leaf[0]] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--leaf", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--hash-output", type=Path)
    parser.add_argument("--populate-hashes", action="store_true")
    args = parser.parse_args()
    leaves = load_leaves()
    manifest = manifest_payload(leaves)
    if args.manifest_output:
        args.manifest_output.write_bytes(manifest)
    if args.hash_output:
        hashes = populate_hashes(leaves, manifest) if args.populate_hashes else None
        args.hash_output.write_bytes(hash_payload(leaves, manifest, hashes))
    if args.output:
        if args.leaf is None or not 0 <= args.leaf < len(leaves):
            parser.error("--output requires a valid --leaf")
        leaf = leaves[args.leaf]
        cnf, selectors = build_leaf(leaf)
        write_leaf(args.output, args.leaf, leaf, cnf, selectors, manifest)
        print(f"leaf={args.leaf:03d} key={leaf[0]} parents={len(leaf[2][6])} "
              f"vars={len(cnf.names)} clauses={len(cnf.clauses)} "
              f"sha256={hashlib.sha256(args.output.read_bytes()).hexdigest()}")
    print(f"timeout_orbits={TIMEOUT_ORBITS} timeout_incidences={TIMEOUT_INCIDENCES} "
          f"witness_leaves={WITNESS_LEAVES} witness_incidences={WITNESS_INCIDENCES} "
          f"manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


if __name__ == "__main__":
    main()
