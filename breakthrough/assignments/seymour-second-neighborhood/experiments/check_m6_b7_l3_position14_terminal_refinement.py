#!/usr/bin/env python3
"""Audit the exact 20-leaf B7-l3 position-14 terminal refinement."""

import argparse
import hashlib
import itertools
import re
import tempfile
from pathlib import Path

import check_m6_b7_l3_profile_root_cardinality as profile_check
import check_m6_clean_sink_balanced_shards as shard_check
import m6_b7_l3_position14_terminal_refinement as producer
from check_m6_parent_cnf import parse_cnf

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / f"{producer.PREFIX}.tsv"
HASHES = HERE / f"{producer.PREFIX}-hashes.tsv"


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def derive_cover():
    profile = profile_check.derive()[14]
    parent = {(accepted, cover): member for accepted, cover, member in profile[7]}
    intersections = []
    for ordinal, shard in enumerate(shard_check.derive_shards()):
        members = [member for member in shard[-1] if (member[0], member[1]) in parent]
        if members:
            if shard[1] != "B7-l3" or shard[3] != 1 or len(members) != len(shard[-1]):
                raise RuntimeError("independent q,H_CC intersection changed")
            intersections.append((ordinal, shard, members))
    base = [(member[0], member[1]) for _, _, members in intersections for member in members]
    leaves = [(ordinal, shard, high_a, members) for ordinal, shard, members in intersections
              for high_a in range(4)]
    assignments = [(accepted, cover, high_a) for _, _, high_a, members in leaves
                   for accepted, cover, _ in members]
    expected = {(accepted, cover, high_a) for accepted, cover in parent for high_a in range(4)}
    if len(intersections) != 5 or len(base) != 1269 or set(base) != set(parent) or \
            len(leaves) != 20 or len(assignments) != 5076 or set(assignments) != expected:
        raise RuntimeError("independent 20-leaf cover is not disjoint and exhaustive")
    return tuple(leaves)


def load_manifest():
    data = MANIFEST.read_bytes()
    lines = data.decode("ascii").splitlines()
    columns = "columns\tleaf-ordinal,key,shard-ordinal,shard-key,q,H_CC,chunk,high-A,parents,variables,clauses,member-sha256"
    if data != ("\n".join(lines) + "\n").encode("ascii") or lines[0] != producer.MANIFEST_FORMAT or \
            lines.count(columns) != 1 or len(lines[lines.index(columns) + 1:]) != 20:
        raise RuntimeError("terminal manifest framing differs")
    return data, lines[lines.index(columns) + 1:]


def load_hashes(manifest):
    lines = HASHES.read_text(encoding="ascii").splitlines()
    expected = [producer.HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
                f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}", "leaves\t20",
                "columns\tleaf-ordinal,key,parents,variables,clauses,cnf-bytes,cnf-sha256"]
    if lines[:5] != expected or len(lines) != 25:
        raise RuntimeError("terminal hash ledger framing differs")
    result = []
    for ordinal, line in enumerate(lines[5:]):
        fields = line.split("\t")
        if len(fields) != 7 or fields[0] != f"{ordinal:02d}" or not fields[5].isdigit() or \
                re.fullmatch(r"[0-9a-f]{64}", fields[6]) is None:
            raise RuntimeError("terminal hash row differs")
        result.append((int(fields[5]), fields[6]))
    return tuple(result)


def audit(regenerate=True):
    independent = derive_cover()
    leaves = producer.load_leaves()
    manifest, rows = load_manifest()
    hashes = load_hashes(manifest)
    observed = [(shard_ordinal, shard[0], high_a, len(members))
                for leaf, (shard_ordinal, shard, high_a, members) in zip(leaves, independent)]
    expected = [(leaf[1], leaf[2], leaf[6], len(leaf[-1])) for leaf in leaves]
    if observed != expected or tuple(row.split("\t")[1] for row in rows) != tuple(leaf[0] for leaf in leaves):
        raise RuntimeError("producer and independent terminal covers differ")
    if regenerate:
        with tempfile.TemporaryDirectory(prefix="b7-l3-p14-check-", dir=HERE.parent) as directory:
            path = Path(directory) / "leaf.cnf"
            for ordinal, leaf in enumerate(leaves):
                producer.write_cnf(path, ordinal, leaf, *producer.build(leaf), manifest)
                if identity(path) != hashes[ordinal]:
                    raise RuntimeError(f"regenerated terminal leaf differs: {ordinal:02d}")
    print("PASS position=14 parents=1269 intersections=5 leaves=20 disjoint=yes exhaustive=yes")


def check(path):
    derive_cover()
    leaves = producer.load_leaves()
    manifest, _ = load_manifest()
    hashes = load_hashes(manifest)
    metadata, variables, clauses, declared = parse_cnf(path)
    ordinal = int(dict(metadata).get("leaf-ordinal", "-1"))
    if not 0 <= ordinal < 20:
        raise RuntimeError("leaf ordinal outside 0..19")
    cnf, selectors, root_delta, split_delta = producer.build(leaves[ordinal])
    expected_metadata = producer.metadata(ordinal, leaves[ordinal], manifest, selectors, root_delta, split_delta)
    if metadata != expected_metadata or variables != list(cnf.names) or clauses != list(cnf.clauses) or \
            declared != (len(cnf.names), len(cnf.clauses)) or identity(path) != hashes[ordinal]:
        raise RuntimeError("terminal CNF differs from exact reconstruction")
    print(f"PASS leaf={ordinal:02d} sha256={identity(path)[1]}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", nargs="?", type=Path)
    parser.add_argument("--cover", action="store_true")
    args = parser.parse_args()
    if args.cover:
        audit()
    if args.cnf:
        check(args.cnf)
    if not (args.cover or args.cnf):
        parser.error("select --cover or a CNF")


if __name__ == "__main__":
    main()
