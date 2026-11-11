#!/usr/bin/env python3
"""Emit the canonical cap-50 parent-chunk cover of the four B7-l2 profiles."""

import argparse
import hashlib
import tempfile
from functools import lru_cache
from pathlib import Path

import m6_b7_l2_profile_root_cardinality as profiles

HERE = Path(__file__).resolve().parent
PREFIX = "m6-b7-l2-parent-chunk-cover"
FORMAT = f"{PREFIX}-cnf-v1"
MANIFEST_FORMAT = f"{PREFIX}-manifest-v1"
HASH_FORMAT = f"{PREFIX}-hashes-v1"
PROFILE_SOURCE = HERE / "m6_b7_l2_profile_root_cardinality.py"
PROFILE_SOURCE_IDENTITY = (
    13024,
    "8d6ddc5ffe3b2d0b95d4723c3ea9d8c2c3e5d582d6c25f43d1df477b53beb548",
)
PROFILE_COUNT = 4
PARENTS_PER_PROFILE = 8119
CHUNK_CAP = 50
CHUNKS_PER_PROFILE = 163
LEAF_COUNT = 652


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def member_payload(members):
    lines = ["columns\tselector-ordinal,accepted-ordinal,cover-index"]
    lines.extend(f"{i:03d}\t{accepted:05d}\t{cover:06d}"
                 for i, (accepted, cover, _) in enumerate(members))
    return ("\n".join(lines) + "\n").encode("ascii")


@lru_cache(maxsize=1)
def load_parent_profiles():
    if identity(PROFILE_SOURCE) != PROFILE_SOURCE_IDENTITY:
        raise RuntimeError("frozen profile producer identity changed")
    parent_profiles = profiles.load_profiles()
    if len(parent_profiles) != PROFILE_COUNT or any(len(profile[7]) != PARENTS_PER_PROFILE
                                                    for profile in parent_profiles):
        raise RuntimeError("frozen four-profile 8119-parent census changed")
    return tuple(parent_profiles)


@lru_cache(maxsize=1)
def load_leaves():
    parent_profiles = load_parent_profiles()
    leaves = []
    for position, profile in enumerate(parent_profiles):
        members = profile[7]
        chunks = tuple(members[start:start + CHUNK_CAP]
                       for start in range(0, len(members), CHUNK_CAP))
        if len(chunks) != CHUNKS_PER_PROFILE:
            raise RuntimeError("chunk count changed")
        for chunk, selected in enumerate(chunks):
            ordinal = len(leaves)
            leaves.append((f"p{position:02d}-c{chunk:03d}", position, profile[0], chunk,
                           chunk * CHUNK_CAP, chunk * CHUNK_CAP + len(selected), selected))
    if len(leaves) != LEAF_COUNT:
        raise RuntimeError("leaf count changed")
    return tuple(leaves)


def leaf_profile(leaf):
    profile = list(load_parent_profiles()[leaf[1]])
    profile[7] = leaf[-1]
    return tuple(profile)


def build(leaf):
    return profiles.build(leaf_profile(leaf))


def manifest_payload(leaves):
    lines = [MANIFEST_FORMAT,
             f"profile-producer-bytes\t{PROFILE_SOURCE_IDENTITY[0]}",
             f"profile-producer-sha256\t{PROFILE_SOURCE_IDENTITY[1]}",
             f"profiles\t{PROFILE_COUNT}",
             f"parents-per-profile\t{PARENTS_PER_PROFILE}",
             f"parent-incidences\t{PROFILE_COUNT * PARENTS_PER_PROFILE}",
             f"parent-chunk-cap\t{CHUNK_CAP}",
             f"chunks-per-profile\t{CHUNKS_PER_PROFILE}",
             f"leaves\t{LEAF_COUNT}",
             "cover\tdisjoint-and-exhaustive-within-each-profile",
             "ordering\tprofile-position,parent-offset",
             "certificate-status\tnot-started",
             "columns\tleaf-ordinal,key,profile-position,profile-key,chunk,start,stop,parents,variables,clauses,member-sha256"]
    for ordinal, leaf in enumerate(leaves):
        cnf, _, _ = build(leaf)
        lines.append(f"{ordinal:03d}\t{leaf[0]}\t{leaf[1]:02d}\t{leaf[2]}\t{leaf[3]:03d}\t"
                     f"{leaf[4]:04d}\t{leaf[5]:04d}\t{len(leaf[-1])}\t{len(cnf.names)}\t"
                     f"{len(cnf.clauses)}\t{hashlib.sha256(member_payload(leaf[-1])).hexdigest()}")
    return ("\n".join(lines) + "\n").encode("ascii")


def metadata(ordinal, leaf, manifest, selectors, delta):
    return [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
            ("manifest-bytes", str(len(manifest))),
            ("manifest-sha256", hashlib.sha256(manifest).hexdigest()),
            ("leaf-ordinal", str(ordinal)), ("leaf-key", leaf[0]),
            ("profile-position", str(leaf[1])), ("profile-key", leaf[2]),
            ("chunk", str(leaf[3])), ("parent-start", str(leaf[4])),
            ("parent-stop", str(leaf[5])), ("parents", str(len(leaf[-1]))),
            ("member-sha256", hashlib.sha256(member_payload(leaf[-1])).hexdigest()),
            ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1])),
            ("cardinality-added-variables", str(delta[0])),
            ("cardinality-added-clauses", str(delta[1])),
            ("certificate-status", "not-started")]


def write_cnf(path, ordinal, leaf, cnf, selectors, delta, manifest):
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in metadata(ordinal, leaf, manifest, selectors, delta):
            handle.write(f"c {name} {value}\n")
        for name, number in cnf.names.items():
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def populate_hashes(leaves, manifest):
    values = []
    with tempfile.TemporaryDirectory(prefix="b7-l2-chunk-hashes-", dir=HERE.parent) as directory:
        path = Path(directory) / "leaf.cnf"
        for ordinal, leaf in enumerate(leaves):
            write_cnf(path, ordinal, leaf, *build(leaf), manifest)
            values.append(identity(path))
    return tuple(values)


def hash_payload(leaves, manifest, identities):
    lines = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
             f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}",
             f"leaves\t{LEAF_COUNT}",
             "columns\tleaf-ordinal,key,parents,variables,clauses,cnf-bytes,cnf-sha256"]
    for ordinal, (leaf, item) in enumerate(zip(leaves, identities)):
        cnf, _, _ = build(leaf)
        lines.append(f"{ordinal:03d}\t{leaf[0]}\t{len(leaf[-1])}\t{len(cnf.names)}\t"
                     f"{len(cnf.clauses)}\t{item[0]}\t{item[1]}")
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
    identities = (("", ""),) * LEAF_COUNT
    if args.populate_hashes:
        identities = populate_hashes(leaves, manifest)
    if args.hash_output:
        args.hash_output.write_bytes(hash_payload(leaves, manifest, identities))
    if args.output:
        if args.leaf is None or not 0 <= args.leaf < LEAF_COUNT:
            parser.error("--output requires --leaf in 0..651")
        write_cnf(args.output, args.leaf, leaves[args.leaf], *build(leaves[args.leaf]), manifest)
    print(f"PASS profiles=4 parents_per_profile=8119 chunks_per_profile=163 leaves=652 "
          f"manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


if __name__ == "__main__":
    main()
