#!/usr/bin/env python3
"""Independently audit the cap-50 cover of all four B7-l2 profiles."""

import argparse
import hashlib
import itertools
import re
import tempfile
from collections import defaultdict
from pathlib import Path

import check_m6_clean_sink_group_cnf as clean
from check_m6_parent_cnf import expected_projection, parse_cnf
import m6_b7_l2_parent_chunk_cover as producer

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / f"{producer.PREFIX}.tsv"
HASHES = HERE / f"{producer.PREFIX}-hashes.tsv"
C = (16, 17)


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def independent_states(row):
    colors = ["R"] + ["A"] * 8 + ["B"] * 7 + ["C"] * 2
    holes = frozenset(expected_projection(row)[1])
    hvec = tuple(sum(tuple(sorted((c, v))) in holes for v in range(18) if colors[v] in "RA")
                 for c in C)
    internal_options = ("h",) if (16, 17) in holes else ("16>17", "17>16")
    result = []
    for internal in internal_options:
        internal_out = {"h": (0, 0), "16>17": (1, 0), "17>16": (0, 1)}[internal]
        for high in itertools.product((0, 1), repeat=2):
            cb = []
            for index, c in enumerate(C):
                forced = sum(colors[v] in "RA" and tuple(sorted((c, v))) not in holes
                             for v in range(18))
                available = sum(colors[v] == "B" and tuple(sorted((c, v))) not in holes
                                for v in range(18))
                value = 8 + high[index] - forced - internal_out[index]
                if not 0 <= value <= available:
                    break
                cb.append(value)
            if len(cb) == 2 and not any(high[i] and not internal_out[i] and cb[i] == 0
                                        for i in range(2)):
                result.append((hvec, internal, high, tuple(cb)))
    return result


def state_key(state):
    hvec, internal, high, cb = state
    code = {"h": "h", "16>17": "f", "17>16": "r"}[internal]
    return f"h{hvec[0]}{hvec[1]}-c{code}-m{high[0]}{high[1]}-b{cb[0]}{cb[1]}"


def derive_cover():
    groups = clean.derive_groups(HERE / "m6-clean-sink-remaining.tsv",
                                 HERE / "m6-placement-cover.txt", HERE / "m6-placement-filter.txt")
    parents = tuple(groups["B7-l2"])
    cells = defaultdict(list)
    for member in parents:
        for state in independent_states(member[2]):
            cells[state].append(member)
    states = [(state_key(state), state, cells[state]) for state in sorted(cells)]
    ordered = sorted(enumerate(states), key=lambda item: (item[1][1][1], item[1][1][2],
                                                           item[1][1][3], item[1][1][0]))
    profiles = [(f"p{position:02d}", state_ordinal, key, state, members)
                for position, (state_ordinal, (key, state, members)) in enumerate(ordered)]
    if len(parents) != 8119 or len(profiles) != 4 or any(len(profile[-1]) != 8119
                                                        for profile in profiles):
        raise RuntimeError("independent four-profile 8119-parent census differs")
    leaves = []
    for position, profile in enumerate(profiles):
        members = profile[-1]
        for chunk, start in enumerate(range(0, len(members), 50)):
            leaves.append((position, profile[0], chunk, start, min(start + 50, len(members)),
                           members[start:start + 50]))
    flattened = [[(a, c) for leaf in leaves if leaf[0] == position for a, c, _ in leaf[-1]]
                 for position in range(4)]
    expected = [[(a, c) for a, c, _ in profile[-1]] for profile in profiles]
    if len(leaves) != 652 or any(sum(leaf[0] == p for leaf in leaves) != 163 for p in range(4)) or \
            flattened != expected or any(len(set(items)) != 8119 for items in flattened):
        raise RuntimeError("independent chunks are not exact, ordered, disjoint covers")
    return tuple(profiles), tuple(leaves)


def load_manifest():
    data = MANIFEST.read_bytes()
    lines = data.decode("ascii").splitlines()
    columns = ("columns\tleaf-ordinal,key,profile-position,profile-key,chunk,start,stop,parents,"
               "variables,clauses,member-sha256")
    rows = lines[lines.index(columns) + 1:] if lines.count(columns) == 1 else []
    if data != ("\n".join(lines) + "\n").encode("ascii") or lines[0] != producer.MANIFEST_FORMAT or \
            len(rows) != 652 or "certificate-status\tnot-started" not in lines:
        raise RuntimeError("chunk manifest framing differs")
    return data, rows


def load_hashes(manifest):
    lines = HASHES.read_text(encoding="ascii").splitlines()
    expected = [producer.HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
                f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}", "leaves\t652",
                "columns\tleaf-ordinal,key,parents,variables,clauses,cnf-bytes,cnf-sha256"]
    if lines[:5] != expected or len(lines) != 657:
        raise RuntimeError("chunk hash ledger framing differs")
    result = []
    for ordinal, line in enumerate(lines[5:]):
        fields = line.split("\t")
        if len(fields) != 7 or fields[0] != f"{ordinal:03d}" or not fields[5].isdigit() or \
                re.fullmatch(r"[0-9a-f]{64}", fields[6]) is None:
            raise RuntimeError("chunk hash row differs")
        result.append((int(fields[5]), fields[6]))
    return tuple(result)


def audit(regenerate=False):
    _, independent = derive_cover()
    leaves = producer.load_leaves()
    manifest, rows = load_manifest()
    hashes = load_hashes(manifest)
    observed = [(leaf[1], leaf[2], leaf[3], leaf[4], leaf[5],
                 [(a, c) for a, c, _ in leaf[-1]]) for leaf in leaves]
    expected = [(position, key, chunk, start, stop, [(a, c) for a, c, _ in members])
                for position, key, chunk, start, stop, members in independent]
    if observed != expected or tuple(row.split("\t")[1] for row in rows) != tuple(x[0] for x in leaves):
        raise RuntimeError("producer and independent chunk covers differ")
    if regenerate:
        with tempfile.TemporaryDirectory(prefix="b7-l2-chunk-check-", dir=HERE.parent) as directory:
            path = Path(directory) / "leaf.cnf"
            for ordinal, leaf in enumerate(leaves):
                producer.write_cnf(path, ordinal, leaf, *producer.build(leaf), manifest)
                if identity(path) != hashes[ordinal]:
                    raise RuntimeError(f"regenerated leaf differs: {ordinal:03d}")
    print("PASS profiles=4 parents_per_profile=8119 chunks_per_profile=163 leaves=652 "
          "disjoint=yes exhaustive=yes")


def check(path):
    derive_cover()
    leaves = producer.load_leaves()
    manifest, _ = load_manifest()
    hashes = load_hashes(manifest)
    metadata, variables, clauses, declared = parse_cnf(path)
    ordinal = int(dict(metadata).get("leaf-ordinal", "-1"))
    if not 0 <= ordinal < 652:
        raise RuntimeError("leaf ordinal outside 0..651")
    cnf, selectors, delta = producer.build(leaves[ordinal])
    if metadata != producer.metadata(ordinal, leaves[ordinal], manifest, selectors, delta) or \
            variables != list(cnf.names) or clauses != list(cnf.clauses) or \
            declared != (len(cnf.names), len(cnf.clauses)) or identity(path) != hashes[ordinal]:
        raise RuntimeError("leaf CNF differs from reconstruction")
    print(f"PASS leaf={ordinal:03d} sha256={identity(path)[1]}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", nargs="?", type=Path)
    parser.add_argument("--cover", action="store_true")
    parser.add_argument("--regenerate", action="store_true")
    args = parser.parse_args()
    if args.cover:
        audit(args.regenerate)
    if args.cnf:
        check(args.cnf)
    if not (args.cover or args.cnf):
        parser.error("select --cover or a CNF")


if __name__ == "__main__":
    main()
