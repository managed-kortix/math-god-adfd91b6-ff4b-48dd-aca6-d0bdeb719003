#!/usr/bin/env python3
"""Emit the exact C-to-B subset-intersection refinement of hard B7-l6 states."""

import argparse
import hashlib
import itertools
from pathlib import Path

import m6_b7_l6_state_split as states

HERE = Path(__file__).resolve().parent
FORMAT = "m6-b7-l6-hard-orbit-cnf-v1"
MANIFEST_FORMAT = "m6-b7-l6-hard-orbits-v1"
HASH_FORMAT = "m6-b7-l6-hard-orbit-hashes-v1"
B_VERTICES = tuple(range(9, 16))
SOURCE_PATHS = {
    "state-manifest": HERE / "m6-b7-l6-state-split.tsv",
    "state-hash-ledger": HERE / "m6-b7-l6-state-leaf-hashes.tsv",
    "state-scout": HERE / "m6-b7-l6-state-scout-30s.json",
    "state-certificate-ledger": HERE / "m6-b7-l6-state-certificates.tsv",
}
SOURCE_IDENTITIES = {
    "state-manifest": (4382, "a3b8f9d17b50dbfccd5f00740b33c6e90f6f10d26a3854dd627a45681e5c890e"),
    "state-hash-ledger": (3163, "eec464838f7d01e6cf053c7cbf8fa1442068d78738f4bd2772b15a8417543ae4"),
    "state-scout": (6948, "69c1d56145ec2544702717b252bd1e3796c882c68ca95023488b959e2af2f763"),
    "state-certificate-ledger": (5030, "037a4a6e51ef5cd76dc070bd461481ef90ac5520a875c0a96973c60f991172c7"),
}
HARD_STATE_ORDINALS = (1, 3, 5, 7, 9, 11, 12, 13, 15, 17, 19, 20, 21, 23, 24, 25, 27, 28, 29)
HARD_STATES = 19
HARD_INCIDENCES = 170
ORBIT_LEAVES = 42
ORBIT_INCIDENCES = 392


def identity(data):
    return len(data), hashlib.sha256(data).hexdigest()


def verify_sources():
    for name, path in SOURCE_PATHS.items():
        if identity(path.read_bytes()) != SOURCE_IDENTITIES[name]:
            raise RuntimeError(f"bound hard-state source changed: {name}")


def representative(left_size, right_size, intersection):
    left = frozenset(B_VERTICES[:left_size])
    right = frozenset(B_VERTICES[:intersection] +
                      B_VERTICES[left_size:left_size + right_size - intersection])
    if len(right) != right_size or len(left & right) != intersection:
        raise RuntimeError("invalid canonical subset-intersection representative")
    return left, right


def load_leaves():
    verify_sources()
    source_leaves = states.load_leaves()
    hard = [source_leaves[i] for i in HARD_STATE_ORDINALS]
    if len(hard) != HARD_STATES or sum(len(leaf[2]) for leaf in hard) != HARD_INCIDENCES:
        raise RuntimeError("committed hard-state frontier changed")
    leaves = []
    for source_ordinal, (source_key, state, members) in zip(HARD_STATE_ORDINALS, hard):
        left_size, right_size = state[3]
        low, high = max(0, left_size + right_size - 7), min(left_size, right_size)
        for intersection in range(low, high + 1):
            key = f"s{source_ordinal:02d}-t{intersection}"
            leaves.append((key, source_ordinal, source_key, state, intersection,
                           representative(left_size, right_size, intersection), members))
    if len(leaves) != ORBIT_LEAVES or sum(len(leaf[6]) for leaf in leaves) != ORBIT_INCIDENCES:
        raise RuntimeError("hard subset-intersection orbit totals changed")
    return leaves


def member_payload(members):
    lines = ["columns\tselector-ordinal,accepted-ordinal,cover-index"]
    lines.extend(f"{i:02d}\t{accepted:05d}\t{cover:06d}"
                 for i, (accepted, cover, _) in enumerate(members))
    return ("\n".join(lines) + "\n").encode("ascii")


def dimensions(count):
    return states.source.parent.BASE_VARIABLES + count, states.source.parent.BASE_CLAUSES["B7"] + 18 + 153 * count


def build_leaf(leaf):
    _, _, _, state, _, subsets, members = leaf
    cnf = states.source.parent.generate(18, 7, 6, robust_witness=True, arc_minimal=True)
    _, internal, high, _ = state
    internal_var = cnf.names[{"h": "h_16_17", "16>17": "a_16_17", "17>16": "a_17_16"}[internal]]
    cnf.add(internal_var)
    for c, bit in zip(states.C_VERTICES, high):
        variable = cnf.names[f"cnt_d1_{c}_17_9"]
        cnf.add(variable if bit else -variable)
    for c, subset in zip(states.C_VERTICES, subsets):
        for b in B_VERTICES:
            variable = cnf.names[f"a_{c}_{b}"]
            cnf.add(variable if b in subset else -variable)
    selectors = [cnf.var(f"b7_l6_hard_orbit_selector_{i:02d}") for i in range(len(members))]
    cnf.add(*selectors)
    for selector, (_, _, row) in zip(selectors, members):
        holes = states.source.parent.embedded_holes(row["branch"], row["word"], row["edges"])[1]
        for pair in states.source.parent.PAIRS:
            hole = cnf.names[f"h_{pair[0]}_{pair[1]}"]
            cnf.add(-selector, hole if pair in holes else -hole)
    return cnf, selectors


def manifest_payload(leaves):
    lines = [MANIFEST_FORMAT]
    for name, item in SOURCE_IDENTITIES.items():
        lines.extend((f"{name}-bytes\t{item[0]}", f"{name}-sha256\t{item[1]}"))
    lines.extend((f"hard-states\t{HARD_STATES}", f"hard-state-incidences\t{HARD_INCIDENCES}",
                  f"orbit-leaves\t{ORBIT_LEAVES}", f"parent-orbit-incidences\t{ORBIT_INCIDENCES}",
                  "forced-C-B-arc-literals\t14",
                  "columns\torbit-ordinal,key,state-ordinal,state-key,t,cb16,cb17,parents,variables,clauses,member-sha256"))
    for ordinal, (key, source_ordinal, source_key, state, intersection, _, members) in enumerate(leaves):
        variables, clauses = dimensions(len(members))
        lines.append(f"{ordinal:02d}\t{key}\t{source_ordinal:02d}\t{source_key}\t{intersection}\t"
                     f"{state[3][0]}\t{state[3][1]}\t{len(members)}\t{variables}\t{clauses}\t"
                     f"{hashlib.sha256(member_payload(members)).hexdigest()}")
    return ("\n".join(lines) + "\n").encode("ascii")


def hash_payload(leaves, manifest, hashes=None):
    hashes = hashes or {}
    lines = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
             f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}", f"orbit-leaves\t{ORBIT_LEAVES}",
             "columns\torbit-ordinal,key,parents,variables,clauses,cnf-sha256"]
    for ordinal, leaf in enumerate(leaves):
        variables, clauses = dimensions(len(leaf[6]))
        lines.append(f"{ordinal:02d}\t{leaf[0]}\t{len(leaf[6])}\t{variables}\t{clauses}\t{hashes.get(leaf[0], '')}")
    return ("\n".join(lines) + "\n").encode("ascii")


def write_leaf(path, ordinal, leaf, cnf, selectors, manifest):
    key, source_ordinal, source_key, state, intersection, subsets, members = leaf
    metadata = [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
                ("manifest-bytes", str(len(manifest))),
                ("manifest-sha256", hashlib.sha256(manifest).hexdigest())]
    for name, item in SOURCE_IDENTITIES.items():
        metadata.extend(((f"{name}-bytes", str(item[0])), (f"{name}-sha256", item[1])))
    metadata.extend((("orbit-ordinal", str(ordinal)), ("orbit-key", key),
                     ("state-ordinal", str(source_ordinal)), ("state-key", source_key),
                     ("intersection-t", str(intersection)), ("parents", str(len(members))),
                     ("member-sha256", hashlib.sha256(member_payload(members)).hexdigest()),
                     ("C16-subset", ",".join(map(str, sorted(subsets[0])))),
                     ("C17-subset", ",".join(map(str, sorted(subsets[1])))),
                     ("state-unit-clauses", "3"), ("forced-C-B-arc-unit-clauses", "14"),
                     ("alo-clauses", "1"), ("guarded-hole-clauses-per-parent", "153"),
                     ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1]))))
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in metadata:
            handle.write(f"c {name} {value}\n")
        for name, number in cnf.names.items():
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--leaf", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--hash-output", type=Path)
    args = parser.parse_args()
    leaves = load_leaves()
    manifest = manifest_payload(leaves)
    if args.manifest_output:
        args.manifest_output.write_bytes(manifest)
    if args.hash_output:
        args.hash_output.write_bytes(hash_payload(leaves, manifest))
    if args.output:
        if args.leaf is None or not 0 <= args.leaf < len(leaves):
            parser.error("--output requires a valid --leaf")
        leaf = leaves[args.leaf]
        cnf, selectors = build_leaf(leaf)
        write_leaf(args.output, args.leaf, leaf, cnf, selectors, manifest)
        print(f"leaf={args.leaf:02d} key={leaf[0]} parents={len(leaf[6])} vars={len(cnf.names)} "
              f"clauses={len(cnf.clauses)} sha256={hashlib.sha256(args.output.read_bytes()).hexdigest()}")
    print(f"hard_states={HARD_STATES} hard_incidences={HARD_INCIDENCES} orbit_leaves={ORBIT_LEAVES} "
          f"orbit_incidences={ORBIT_INCIDENCES} manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


if __name__ == "__main__":
    main()
