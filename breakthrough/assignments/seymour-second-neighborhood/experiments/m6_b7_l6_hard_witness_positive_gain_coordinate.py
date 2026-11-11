#!/usr/bin/env python3
"""Split every frozen positive-gain TIMEOUT by deletion coordinate."""

import argparse
import hashlib
import json
import tempfile
from pathlib import Path

import m6_b7_l6_hard_witness_positive_gain as source

HERE = Path(__file__).resolve().parent
FORMAT = "m6-b7-l6-hard-witness-positive-gain-coordinate-cnf-v1"
MANIFEST_FORMAT = "m6-b7-l6-hard-witness-positive-gain-coordinate-v1"
HASH_FORMAT = "m6-b7-l6-hard-witness-positive-gain-coordinate-hashes-v1"
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
SOURCE_LEAVES = 114
LEAVES = 219
INCIDENCES = 1990


def identity(data):
    return len(data), hashlib.sha256(data).hexdigest()


def verify_sources():
    for name, path in SOURCE_PATHS.items():
        if identity(path.read_bytes()) != SOURCE_IDENTITIES[name]:
            raise RuntimeError(f"bound frozen source changed: {name}")


def timeout_ordinals():
    verify_sources()
    scout = json.loads(SOURCE_PATHS["positive-gain-scout"].read_text(encoding="ascii"))
    rows = scout.get("rows", [])
    if len(rows) != 117 or any(row.get("leaf") != i for i, row in enumerate(rows)):
        raise RuntimeError("positive-gain scout does not exactly cover its source leaves")
    if any(row.get("status") not in ("UNSAT", "TIMEOUT") for row in rows):
        raise RuntimeError("positive-gain scout contains an unexpected status")
    unsat = tuple(row["leaf"] for row in rows if row["status"] == "UNSAT")
    ledger = SOURCE_PATHS["positive-gain-certificate-ledger"].read_text(encoding="ascii").splitlines()
    marker = next((i for i, line in enumerate(ledger) if line.startswith("columns\t")), -1)
    certified = tuple(int(line.split("\t", 1)[0]) for line in ledger[marker + 1:])
    if unsat != (42, 95, 97) or certified != unsat:
        raise RuntimeError("scout UNSAT set and committed certificate scope differ")
    result = tuple(row["leaf"] for row in rows if row["status"] == "TIMEOUT")
    if len(result) != SOURCE_LEAVES:
        raise RuntimeError("positive-gain TIMEOUT source count changed")
    return result


def load_leaves():
    sources = source.load_leaves()
    children = []
    for source_ordinal in timeout_ordinals():
        leaf = sources[source_ordinal]
        for coordinate, (deleted, witness) in enumerate(zip(leaf[3], leaf[4])):
            children.append((source_ordinal, coordinate, deleted, witness, leaf))
    if len(children) != LEAVES or sum(len(child[4][2][6]) for child in children) != INCIDENCES:
        raise RuntimeError("deletion-coordinate child census changed")
    return tuple(children)


def child_key(child):
    return f"{child[4][0]}-c{child[2]}"


def coordinate_paths(child):
    _, _, deleted, witness, _ = child
    return tuple((witness, midpoint, deleted) for midpoint in range(18)
                 if midpoint not in (witness, deleted))


def dimensions(child):
    variables, clauses = source.source.dimensions(child[4])
    return variables, clauses + 1


def build_leaf(child):
    cnf, selectors = source.source.build_leaf(child[4])
    cnf.add(*(cnf.names[f"p_{witness}_{midpoint}_{deleted}"]
              for witness, midpoint, deleted in coordinate_paths(child)))
    return cnf, selectors


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


def hash_payload(children, manifest, hashes=None):
    hashes = hashes or {}
    lines = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
             f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}", f"leaves\t{LEAVES}",
             "columns\tleaf-ordinal,key,source-leaf-ordinal,coordinate,deleted,witness,"
             "coordinate-path-literals,alo-clauses,parents,variables,clauses,cnf-sha256"]
    for ordinal, child in enumerate(children):
        source_ordinal, coordinate, deleted, witness, leaf = child
        variables, clauses = dimensions(child)
        lines.append(f"{ordinal:03d}\t{child_key(child)}\t{source_ordinal:03d}\t{coordinate}\t"
                     f"{deleted}\t{witness}\t16\t1\t{len(leaf[2][6])}\t{variables}\t{clauses}\t"
                     f"{hashes.get(child_key(child), '')}")
    return ("\n".join(lines) + "\n").encode("ascii")


def metadata(ordinal, child, manifest, selectors):
    source_ordinal, coordinate, deleted, witness, leaf = child
    result = [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
              ("manifest-bytes", str(len(manifest))),
              ("manifest-sha256", hashlib.sha256(manifest).hexdigest())]
    for name, item in SOURCE_IDENTITIES.items():
        result.extend(((f"{name}-bytes", str(item[0])), (f"{name}-sha256", item[1])))
    result.extend((("leaf-ordinal", str(ordinal)), ("key", child_key(child)),
                   ("source-leaf-ordinal", str(source_ordinal)), ("source-witness-key", leaf[0]),
                   ("coordinate", str(coordinate)), ("deleted", str(deleted)),
                   ("witness", str(witness)), ("coordinate-path-literals", "16"),
                   ("coordinate-path-alo-clauses", "1"),
                   ("existential-coverage", "coordinate-ALO-overlap-allowed"),
                   ("parents", str(len(leaf[2][6]))), ("first-selector", str(selectors[0])),
                   ("last-selector", str(selectors[-1]))))
    return result


def write_leaf(path, ordinal, child, cnf, selectors, manifest):
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in metadata(ordinal, child, manifest, selectors):
            handle.write(f"c {name} {value}\n")
        for name, number in cnf.names.items():
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def populate_hashes(children, manifest):
    hashes = {}
    with tempfile.TemporaryDirectory(prefix="m6-positive-coordinate-hashes-", dir=HERE.parent) as directory:
        path = Path(directory) / "leaf.cnf"
        for ordinal, child in enumerate(children):
            cnf, selectors = build_leaf(child)
            write_leaf(path, ordinal, child, cnf, selectors, manifest)
            hashes[child_key(child)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--leaf", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--hash-output", type=Path)
    parser.add_argument("--populate-hashes", action="store_true")
    args = parser.parse_args()
    children = load_leaves()
    manifest = manifest_payload(children)
    if args.manifest_output:
        args.manifest_output.write_bytes(manifest)
    if args.hash_output:
        hashes = populate_hashes(children, manifest) if args.populate_hashes else None
        args.hash_output.write_bytes(hash_payload(children, manifest, hashes))
    if args.output:
        if args.leaf is None or not 0 <= args.leaf < len(children):
            parser.error("--output requires a valid --leaf")
        child = children[args.leaf]
        cnf, selectors = build_leaf(child)
        write_leaf(args.output, args.leaf, child, cnf, selectors, manifest)
        print(f"leaf={args.leaf:03d} key={child_key(child)} parents={len(child[4][2][6])} "
              f"vars={len(cnf.names)} clauses={len(cnf.clauses)} "
              f"sha256={hashlib.sha256(args.output.read_bytes()).hexdigest()}")
    print(f"source_timeout_leaves={SOURCE_LEAVES} leaves={LEAVES} incidences={INCIDENCES} "
          f"manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


if __name__ == "__main__":
    main()
