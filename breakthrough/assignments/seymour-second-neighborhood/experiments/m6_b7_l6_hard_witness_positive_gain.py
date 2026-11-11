#!/usr/bin/env python3
"""Add one compact positive-gain child to every frozen hard witness leaf."""

import argparse
import hashlib
import tempfile
from pathlib import Path

import m6_b7_l6_hard_witness_orbits as source

HERE = Path(__file__).resolve().parent
FORMAT = "m6-b7-l6-hard-witness-positive-gain-cnf-v1"
MANIFEST_FORMAT = "m6-b7-l6-hard-witness-positive-gain-v1"
HASH_FORMAT = "m6-b7-l6-hard-witness-positive-gain-hashes-v1"
SOURCE_PATHS = {
    "witness-manifest": HERE / "m6-b7-l6-hard-witness-orbits.tsv",
    "witness-hash-ledger": HERE / "m6-b7-l6-hard-witness-orbit-hashes.tsv",
    "witness-scout": HERE / "m6-b7-l6-hard-witness-orbit-scout-20s.json",
    "no-gain-manifest": HERE / "m6-b7-l6-hard-witness-no-gain.tsv",
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
LEAVES = 117
INCIDENCES = 1066


def identity(data):
    return len(data), hashlib.sha256(data).hexdigest()


def verify_sources():
    for name, path in SOURCE_PATHS.items():
        if identity(path.read_bytes()) != SOURCE_IDENTITIES[name]:
            raise RuntimeError(f"bound frozen source changed: {name}")


def load_leaves():
    verify_sources()
    leaves = source.load_leaves()
    if len(leaves) != LEAVES or sum(len(leaf[2][6]) for leaf in leaves) != INCIDENCES:
        raise RuntimeError("frozen witness frontier changed")
    return leaves


def gain_paths(leaf):
    return tuple((witness, midpoint, deleted)
                 for deleted, witness in zip(leaf[3], leaf[4])
                 for midpoint in range(18) if midpoint not in (witness, deleted))


def dimensions(leaf):
    variables, clauses = source.dimensions(leaf)
    return variables, clauses + 1


def build_leaf(leaf):
    cnf, selectors = source.build_leaf(leaf)
    cnf.add(*(cnf.names[f"p_{witness}_{midpoint}_{deleted}"]
              for witness, midpoint, deleted in gain_paths(leaf)))
    return cnf, selectors


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
                     f"{len(gain_paths(leaf))}\t1\t{len(leaf[2][6])}\t{variables}\t{clauses}")
    return ("\n".join(lines) + "\n").encode("ascii")


def hash_payload(leaves, manifest, hashes=None):
    hashes = hashes or {}
    lines = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
             f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}", f"leaves\t{LEAVES}",
             "columns\tleaf-ordinal,key,positive-path-literals,alo-clauses,parents,variables,clauses,cnf-sha256"]
    for ordinal, leaf in enumerate(leaves):
        variables, clauses = dimensions(leaf)
        lines.append(f"{ordinal:03d}\t{leaf[0]}\t{len(gain_paths(leaf))}\t1\t"
                     f"{len(leaf[2][6])}\t{variables}\t{clauses}\t{hashes.get(leaf[0], '')}")
    return ("\n".join(lines) + "\n").encode("ascii")


def metadata(ordinal, leaf, manifest, selectors):
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
                   ("positive-path-literals", str(len(gain_paths(leaf)))),
                   ("positive-path-alo-clauses", "1"),
                   ("complement", "committed-exact-no-gain"),
                   ("parents", str(len(leaf[2][6]))),
                   ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1]))))
    return result


def write_leaf(path, ordinal, leaf, cnf, selectors, manifest):
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in metadata(ordinal, leaf, manifest, selectors):
            handle.write(f"c {name} {value}\n")
        for name, number in cnf.names.items():
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def populate_hashes(leaves, manifest):
    hashes = {}
    with tempfile.TemporaryDirectory(prefix="m6-witness-positive-gain-hashes-", dir=HERE.parent) as directory:
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
        print(f"leaf={args.leaf:03d} key={leaf[0]} alo_width={len(gain_paths(leaf))} "
              f"parents={len(leaf[2][6])} vars={len(cnf.names)} clauses={len(cnf.clauses)} "
              f"sha256={hashlib.sha256(args.output.read_bytes()).hexdigest()}")
    print(f"leaves={LEAVES} incidences={INCIDENCES} "
          f"manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


if __name__ == "__main__":
    main()
