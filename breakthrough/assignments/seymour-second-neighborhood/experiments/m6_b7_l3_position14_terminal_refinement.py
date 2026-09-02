#!/usr/bin/env python3
"""Emit the exact 20-leaf terminal refinement of B7-l3 profile position 14."""

import argparse
import hashlib
import tempfile
from functools import lru_cache
from pathlib import Path

import m6_b7_l3_profile_root_cardinality as profiles
import m6_clean_sink_balanced_shards as balanced
from snc_cnf import threshold

HERE = Path(__file__).resolve().parent
PREFIX = "m6-b7-l3-position14-terminal-refinement"
FORMAT = f"{PREFIX}-cnf-v1"
MANIFEST_FORMAT = f"{PREFIX}-manifest-v1"
HASH_FORMAT = f"{PREFIX}-hashes-v1"
POSITION = 14
LEAVES = 60
PARENTS = 1269
HIGH_VALUES = tuple(range(4))
SOURCE_PATHS = {
    "profile-manifest": HERE / "m6-b7-l3-profile-root-cardinality.tsv",
    "profile-hashes": HERE / "m6-b7-l3-profile-root-cardinality-hashes.tsv",
    "balanced-manifest": HERE / "m6-clean-sink-balanced-shards.tsv",
    "balanced-hashes": HERE / "m6-clean-sink-balanced-shard-hashes.tsv",
    "eighteen-profile-ledger": HERE / "m6-b7-l3-profile-root-cardinality-except-position14-certificates.tsv",
    "eighteen-profile-packages": HERE / "m6-b7-l3-profile-root-cardinality-except-position14-packages.tsv",
}


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


SOURCE_IDENTITIES = {name: identity(path) for name, path in SOURCE_PATHS.items()}


@lru_cache(maxsize=1)
def position14_profile():
    return profiles.load_profiles()[POSITION]


def member_payload(members):
    lines = ["columns\tselector-ordinal,accepted-ordinal,cover-index"]
    lines.extend(f"{i:03d}\t{accepted:05d}\t{cover:06d}"
                 for i, (accepted, cover, _) in enumerate(members))
    return ("\n".join(lines) + "\n").encode("ascii")


@lru_cache(maxsize=1)
def load_leaves():
    for name, path in SOURCE_PATHS.items():
        if identity(path) != SOURCE_IDENTITIES[name]:
            raise RuntimeError(f"frozen source identity changed: {name}")
    parent_profile = position14_profile()
    parent_ids = {(accepted, cover) for accepted, cover, _ in parent_profile[7]}
    intersections = []
    for shard_ordinal, shard in enumerate(balanced.load_shards()):
        members = [member for member in shard[-1] if (member[0], member[1]) in parent_ids]
        if members:
            if shard[1] != "B7-l3" or shard[3] != 1 or len(members) != len(shard[-1]):
                raise RuntimeError("position-14/balanced-shard intersection changed")
            intersections.append((shard_ordinal, shard, members))
    flattened = [(member[0], member[1]) for _, _, members in intersections for member in members]
    if len(intersections) != 5 or len(flattened) != PARENTS or set(flattened) != parent_ids:
        raise RuntimeError("five q,H_CC shard intersections are not an exact position-14 cover")
    leaves = []
    for shard_ordinal, shard, members in intersections:
        chunks = tuple(members[i:i + 100] for i in range(0, len(members), 100))
        for chunk, selected in enumerate(chunks):
            for high_a in HIGH_VALUES:
                key = f"p14-{shard[0]}-c{chunk:02d}-ha{high_a}"
                leaves.append((key, shard_ordinal, shard[0], shard[2], shard[3], chunk, high_a, selected))
    if len(leaves) != LEAVES:
        raise RuntimeError("terminal leaf count changed")
    return tuple(leaves)


def build(leaf):
    members, high_a = leaf[-1], leaf[6]
    profile = position14_profile()
    _, _, _, state, _, subsets, _, _ = profile
    cnf = balanced.source.parent.generate(18, 7, 6, robust_witness=True, arc_minimal=True)
    _, internal, high, _ = state
    cnf.add(cnf.names[{"h": "h_16_17", "16>17": "a_16_17", "17>16": "a_17_16"}[internal]])
    for c, bit in zip(profiles.C, high):
        number = cnf.names[f"cnt_d1_{c}_17_9"]
        cnf.add(number if bit else -number)
    for c, subset in zip(profiles.C, subsets):
        for b in profiles.B:
            number = cnf.names[f"a_{c}_{b}"]
            cnf.add(number if b in subset else -number)
    selectors = [cnf.var(f"b7_l3_p14_leaf_parent_{i:03d}") for i in range(len(members))]
    cnf.add(*selectors)
    for selector, (_, _, row) in zip(selectors, members):
        holes = balanced.source.parent.embedded_holes(row["branch"], row["word"], row["edges"])[1]
        for u, v in balanced.source.parent.PAIRS:
            number = cnf.names[f"h_{u}_{v}"]
            cnf.add(-selector, number if (u, v) in holes else -number)
    root_delta = profiles.extend(cnf)
    before = len(cnf.names), len(cnf.clauses)
    high_inputs = tuple(cnf.names[f"cnt_d1_{a}_17_9"] for a in profiles.A)
    count = threshold(cnf, high_inputs, "b7_l3_p14_leaf_high_A")
    if high_a:
        cnf.add(count[high_a - 1])
    cnf.add(-count[high_a])
    split_delta = len(cnf.names) - before[0], len(cnf.clauses) - before[1]
    if root_delta != (2433, 9571) or split_delta != (36, 129 + (high_a != 0)):
        raise RuntimeError("terminal counter dimensions changed")
    return cnf, selectors, root_delta, split_delta


def manifest_payload(leaves):
    lines = [MANIFEST_FORMAT]
    for name, item in SOURCE_IDENTITIES.items():
        lines.extend((f"{name}-bytes\t{item[0]}", f"{name}-sha256\t{item[1]}"))
    lines.extend(("parent-profile-position\t14", "parent-profile-key\tp14", f"parents\t{PARENTS}",
                  "q-hcc-intersections\t5", "parent-chunk-cap\t100", "high-A-values\t0,1,2,3", f"leaves\t{LEAVES}",
                  "cover\tdisjoint-and-exhaustive", "ordering\tbalanced-shard-ordinal,parent-chunk,high(A)",
                  "columns\tleaf-ordinal,key,shard-ordinal,shard-key,q,H_CC,chunk,high-A,parents,variables,clauses,member-sha256"))
    for ordinal, leaf in enumerate(leaves):
        cnf, _, _, _ = build(leaf)
        lines.append(f"{ordinal:02d}\t{leaf[0]}\t{leaf[1]:02d}\t{leaf[2]}\t{leaf[3]}\t{leaf[4]}\t"
                     f"{leaf[5]}\t{leaf[6]}\t{len(leaf[-1])}\t{len(cnf.names)}\t{len(cnf.clauses)}\t"
                     f"{hashlib.sha256(member_payload(leaf[-1])).hexdigest()}")
    return ("\n".join(lines) + "\n").encode("ascii")


def metadata(ordinal, leaf, manifest, selectors, root_delta, split_delta):
    return [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
            ("manifest-bytes", str(len(manifest))),
            ("manifest-sha256", hashlib.sha256(manifest).hexdigest()),
            ("parent-profile-position", "14"), ("parent-profile-key", "p14"),
            ("leaf-ordinal", str(ordinal)), ("leaf-key", leaf[0]),
            ("shard-ordinal", str(leaf[1])), ("shard-key", leaf[2]), ("q", str(leaf[3])),
            ("H_CC", str(leaf[4])), ("chunk", str(leaf[5])), ("high-A", str(leaf[6])),
            ("parents", str(len(leaf[-1]))),
            ("member-sha256", hashlib.sha256(member_payload(leaf[-1])).hexdigest()),
            ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1])),
            ("root-cardinality-added-variables", str(root_delta[0])),
            ("root-cardinality-added-clauses", str(root_delta[1])),
            ("high-A-added-variables", str(split_delta[0])),
            ("high-A-added-clauses", str(split_delta[1]))]


def write_cnf(path, ordinal, leaf, cnf, selectors, root_delta, split_delta, manifest):
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in metadata(ordinal, leaf, manifest, selectors, root_delta, split_delta):
            handle.write(f"c {name} {value}\n")
        for name, number in cnf.names.items():
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def hash_payload(leaves, manifest, identities):
    lines = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
             f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}", f"leaves\t{LEAVES}",
             "columns\tleaf-ordinal,key,parents,variables,clauses,cnf-bytes,cnf-sha256"]
    for ordinal, (leaf, item) in enumerate(zip(leaves, identities)):
        cnf, _, _, _ = build(leaf)
        lines.append(f"{ordinal:02d}\t{leaf[0]}\t{len(leaf[-1])}\t{len(cnf.names)}\t{len(cnf.clauses)}\t{item[0]}\t{item[1]}")
    return ("\n".join(lines) + "\n").encode("ascii")


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
    identities = (("", ""),) * LEAVES
    if args.populate_hashes:
        values = []
        with tempfile.TemporaryDirectory(prefix="b7-l3-p14-hashes-", dir=HERE.parent) as directory:
            path = Path(directory) / "leaf.cnf"
            for ordinal, leaf in enumerate(leaves):
                write_cnf(path, ordinal, leaf, *build(leaf), manifest)
                values.append(identity(path))
        identities = tuple(values)
    if args.hash_output:
        args.hash_output.write_bytes(hash_payload(leaves, manifest, identities))
    if args.output:
        if args.leaf is None or not 0 <= args.leaf < LEAVES:
            parser.error("--output requires --leaf in 0..19")
        write_cnf(args.output, args.leaf, leaves[args.leaf], *build(leaves[args.leaf]), manifest)
    print(f"PASS position=14 parents={PARENTS} intersections=5 leaves={LEAVES} manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


if __name__ == "__main__":
    main()
