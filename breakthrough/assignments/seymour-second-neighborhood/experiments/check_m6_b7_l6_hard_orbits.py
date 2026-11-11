#!/usr/bin/env python3
"""Independent labelled-S7 checker for the hard B7-l6 orbit refinement."""

import argparse
import hashlib
import itertools
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

import check_m6_b7_l6_state_split as source
from check_m6_parent_cnf import (
    BASE_CLAUSES, BASE_CLAUSE_SHA256, BASE_VARIABLES, BASE_VARIABLE_MAP_SHA256,
    PAIRS, clause_sha256, expected_projection, parse_cnf, variable_map_sha256,
)
from snc_cnf import generate

HERE = Path(__file__).resolve().parent
FORMAT = "m6-b7-l6-hard-orbit-cnf-v1"
MANIFEST_FORMAT = "m6-b7-l6-hard-orbits-v1"
HASH_FORMAT = "m6-b7-l6-hard-orbit-hashes-v1"
HASH_PATH = HERE / "m6-b7-l6-hard-orbit-hashes.tsv"
B_VERTICES = tuple(range(9, 16))
HARD_STATE_ORDINALS = (1, 3, 5, 7, 9, 11, 12, 13, 15, 17, 19, 20, 21, 23, 24, 25, 27, 28, 29)
HARD_STATES, HARD_INCIDENCES, ORBIT_LEAVES, ORBIT_INCIDENCES = 19, 170, 42, 392
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


def verify_sources():
    for name, path in SOURCE_PATHS.items():
        data = path.read_bytes()
        if (len(data), hashlib.sha256(data).hexdigest()) != SOURCE_IDENTITIES[name]:
            raise RuntimeError(f"bound hard-state source changed: {name}")


@lru_cache(maxsize=None)
def labelled_orbits(left_size, right_size):
    universe = {(left, right) for left in itertools.combinations(B_VERTICES, left_size)
                for right in itertools.combinations(B_VERTICES, right_size)}
    cells = []
    low, high = max(0, left_size + right_size - 7), min(left_size, right_size)
    for intersection in range(low, high + 1):
        left = tuple(B_VERTICES[:left_size])
        right = tuple(B_VERTICES[:intersection] +
                      B_VERTICES[left_size:left_size + right_size - intersection])
        orbit = set()
        for permutation in itertools.permutations(B_VERTICES):
            orbit.add((tuple(sorted(permutation[b - 9] for b in left)),
                       tuple(sorted(permutation[b - 9] for b in right))))
        cells.append((intersection, (frozenset(left), frozenset(right)), orbit))
    if set().union(*(cell[2] for cell in cells)) != universe or sum(len(cell[2]) for cell in cells) != len(universe):
        raise RuntimeError("explicit labelled S7 orbits do not partition all subset pairs")
    records = []
    for intersection, representative, members in cells:
        if any(len(set(left) & set(right)) != intersection for left, right in members):
            raise RuntimeError("intersection is not invariant on a labelled S7 orbit")
        records.append((intersection, representative, len(members)))
    if len({record[0] for record in records}) != len(records):
        raise RuntimeError("subset intersection does not separate the labelled S7 orbits")
    return tuple(records)


@lru_cache(maxsize=1)
def derive_leaves():
    verify_sources()
    state_leaves = source.derive_leaves()
    hard = [state_leaves[i] for i in HARD_STATE_ORDINALS]
    if len(hard) != HARD_STATES or sum(len(leaf[2]) for leaf in hard) != HARD_INCIDENCES:
        raise RuntimeError("independent hard-state frontier changed")
    leaves = []
    for source_ordinal, (source_key, state, members) in zip(HARD_STATE_ORDINALS, hard):
        for intersection, representative, orbit_size in labelled_orbits(*state[3]):
            leaves.append((f"s{source_ordinal:02d}-t{intersection}", source_ordinal, source_key,
                           state, intersection, representative, members, orbit_size))
    if len(leaves) != ORBIT_LEAVES or sum(len(leaf[6]) for leaf in leaves) != ORBIT_INCIDENCES:
        raise RuntimeError("independent hard-orbit counts changed")
    return leaves


def member_payload(members):
    lines = ["columns\tselector-ordinal,accepted-ordinal,cover-index"]
    lines.extend(f"{i:02d}\t{accepted:05d}\t{cover:06d}"
                 for i, (accepted, cover, _) in enumerate(members))
    return ("\n".join(lines) + "\n").encode("ascii")


def dimensions(count):
    return BASE_VARIABLES + count, BASE_CLAUSES["B7"] + 18 + 153 * count


def manifest_payload(leaves):
    lines = [MANIFEST_FORMAT]
    for name, item in SOURCE_IDENTITIES.items():
        lines.extend((f"{name}-bytes\t{item[0]}", f"{name}-sha256\t{item[1]}"))
    lines.extend((f"hard-states\t{HARD_STATES}", f"hard-state-incidences\t{HARD_INCIDENCES}",
                  f"orbit-leaves\t{ORBIT_LEAVES}", f"parent-orbit-incidences\t{ORBIT_INCIDENCES}",
                  "forced-C-B-arc-literals\t14",
                  "columns\torbit-ordinal,key,state-ordinal,state-key,t,cb16,cb17,parents,variables,clauses,member-sha256"))
    for ordinal, (key, state_ordinal, state_key, state, intersection, _, members, _) in enumerate(leaves):
        variables, clauses = dimensions(len(members))
        lines.append(f"{ordinal:02d}\t{key}\t{state_ordinal:02d}\t{state_key}\t{intersection}\t"
                     f"{state[3][0]}\t{state[3][1]}\t{len(members)}\t{variables}\t{clauses}\t"
                     f"{hashlib.sha256(member_payload(members)).hexdigest()}")
    return ("\n".join(lines) + "\n").encode("ascii")


def load_hashes():
    lines = HASH_PATH.read_text(encoding="ascii").splitlines()
    if len(lines) != ORBIT_LEAVES + 5 or lines[0] != HASH_FORMAT:
        raise RuntimeError("malformed hard-orbit hash ledger")
    result = {}
    for ordinal, line in enumerate(lines[5:]):
        fields = line.split("\t")
        if len(fields) != 6 or fields[0] != f"{ordinal:02d}" or len(fields[5]) != 64:
            raise RuntimeError("malformed hard-orbit hash row")
        result[fields[1]] = fields[5]
    return result


@lru_cache(maxsize=1)
def frozen_base():
    cnf = generate(18, 7, 6, robust_witness=True, arc_minimal=True)
    return tuple(cnf.names), tuple(cnf.clauses)


def expected_metadata(ordinal, leaf, manifest, selectors):
    key, state_ordinal, state_key, state, intersection, subsets, members, _ = leaf
    result = [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
              ("manifest-bytes", str(len(manifest))),
              ("manifest-sha256", hashlib.sha256(manifest).hexdigest())]
    for name, item in SOURCE_IDENTITIES.items():
        result.extend(((f"{name}-bytes", str(item[0])), (f"{name}-sha256", item[1])))
    result.extend((("orbit-ordinal", str(ordinal)), ("orbit-key", key),
                   ("state-ordinal", str(state_ordinal)), ("state-key", state_key),
                   ("intersection-t", str(intersection)), ("parents", str(len(members))),
                   ("member-sha256", hashlib.sha256(member_payload(members)).hexdigest()),
                   ("C16-subset", ",".join(map(str, sorted(subsets[0])))),
                   ("C17-subset", ",".join(map(str, sorted(subsets[1])))),
                   ("state-unit-clauses", "3"), ("forced-C-B-arc-unit-clauses", "14"),
                   ("alo-clauses", "1"), ("guarded-hole-clauses-per-parent", "153"),
                   ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1]))))
    return result


def validate_model(variables, clauses, literals, selectors):
    values = {}
    for literal in literals:
        if not 1 <= abs(literal) <= len(variables) or abs(literal) in values:
            raise RuntimeError("model contains invalid or duplicate assignment")
        values[abs(literal)] = literal > 0
    if len(values) != len(variables):
        raise RuntimeError("model is incomplete")
    if any(not any(values[abs(lit)] == (lit > 0) for lit in clause) for clause in clauses):
        raise RuntimeError("model falsifies a clause")
    selected = [i for i, selector in enumerate(selectors) if values[selector]]
    if len(selected) != 1:
        raise RuntimeError("model does not select exactly one parent")
    return values, selected[0]


def check(path, model_literals=None):
    leaves = derive_leaves()
    manifest = manifest_payload(leaves)
    metadata, variables, clauses, declared = parse_cnf(path)
    ordinal = int(dict(metadata).get("orbit-ordinal", "-1"))
    if not 0 <= ordinal < ORBIT_LEAVES:
        raise RuntimeError("orbit ordinal outside exact cover")
    leaf = leaves[ordinal]
    names, base_clauses = map(list, frozen_base())
    if (len(names) != BASE_VARIABLES or variable_map_sha256(names) != BASE_VARIABLE_MAP_SHA256 or
            len(base_clauses) != BASE_CLAUSES["B7"] or clause_sha256(base_clauses) != BASE_CLAUSE_SHA256["B7"]):
        raise RuntimeError("independent B7 base identity changed")
    state = leaf[3]
    unit_clauses = [(names.index({"h": "h_16_17", "16>17": "a_16_17", "17>16": "a_17_16"}[state[1]]) + 1,)]
    for c, bit in zip((16, 17), state[2]):
        var = names.index(f"cnt_d1_{c}_17_9") + 1
        unit_clauses.append((var if bit else -var,))
    for c, subset in zip((16, 17), leaf[5]):
        for b in B_VERTICES:
            var = names.index(f"a_{c}_{b}") + 1
            unit_clauses.append((var if b in subset else -var,))
    selectors = list(range(BASE_VARIABLES + 1, BASE_VARIABLES + len(leaf[6]) + 1))
    expected_names = names + [f"b7_l6_hard_orbit_selector_{i:02d}" for i in range(len(selectors))]
    if metadata != expected_metadata(ordinal, leaf, manifest, selectors) or variables != expected_names:
        raise RuntimeError("hard-orbit metadata or variable map differs")
    prefix = base_clauses + unit_clauses + [tuple(selectors)]
    if clauses[:len(prefix)] != prefix:
        raise RuntimeError("base/state/14-arc/ALO prefix differs")
    suffix = iter(clauses[len(prefix):])
    for selector, (_, _, row) in zip(selectors, leaf[6]):
        holes = expected_projection(row)[1]
        for pair in PAIRS:
            hole = names.index(f"h_{pair[0]}_{pair[1]}") + 1
            if next(suffix, None) != (-selector, hole if pair in holes else -hole):
                raise RuntimeError("selector guard differs from exact parent")
    if next(suffix, None) is not None or declared != dimensions(len(leaf[6])):
        raise RuntimeError("hard-orbit suffix or dimensions differ")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != load_hashes()[leaf[0]]:
        raise RuntimeError("hard-orbit CNF hash differs from ledger")
    if model_literals is not None:
        values, selected = validate_model(variables, clauses, model_literals, selectors)
        holes = expected_projection(leaf[6][selected][2])[1]
        if any(values[names.index(f"h_{a}_{b}") + 1] != ((a, b) in holes) for a, b in PAIRS):
            raise RuntimeError("model attribution holes disagree with parent")
    print(f"PASS orbit={ordinal:02d} key={leaf[0]} parents={len(leaf[6])} vars={declared[0]} "
          f"clauses={declared[1]} sha256={digest}")
    return variables, clauses, leaf[6], selectors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", type=Path)
    args = parser.parse_args()
    check(args.cnf)


if __name__ == "__main__":
    main()
