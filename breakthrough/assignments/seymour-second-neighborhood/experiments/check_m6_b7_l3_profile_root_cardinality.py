#!/usr/bin/env python3
"""Independently reconstruct and audit the clean B7-l3 19-profile campaign."""

import argparse
import hashlib
import itertools
import re
import tempfile
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

import check_m6_clean_sink_group_cnf as clean
from check_m6_parent_cnf import (BASE_CLAUSES, BASE_CLAUSE_SHA256, BASE_VARIABLES,
                                 BASE_VARIABLE_MAP_SHA256, PAIRS, clause_sha256,
                                 expected_projection, parse_cnf, variable_map_sha256)
from snc_cnf import generate

HERE = Path(__file__).resolve().parent
PREFIX = "m6-b7-l3-profile-root-cardinality"
MANIFEST = HERE / f"{PREFIX}.tsv"
HASHES = HERE / f"{PREFIX}-hashes.tsv"
A = tuple(range(1, 9))
B = tuple(range(9, 16))
C = (16, 17)
SOURCE_IDENTITIES = {
    "clean-parent-manifest": (1838, "6e7eee0ddd5b4c7ef02cdf459c9a0647f720513e7ee4987a3a8b0c17af37eeda"),
    "clean-remaining-stream": (2262190, "416b7e51a73637784342a374be8e15a1a58032b61fc1140f39f0768d1ff4b642"),
    "clean-partition-manifest": (2104, "733e06c8aa9881e0006409efff23729f1bf88d8af7b1a70e8a78fd3775b53217"),
}


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def independent_states(row):
    colors = ["R"] + ["A"] * 8 + ["B"] * 7 + ["C"] * 2
    holes = frozenset(expected_projection(row)[1])
    hvec = tuple(sum(tuple(sorted((c, v))) in holes for v in range(18) if colors[v] in "RA") for c in C)
    internal_options = ("h",) if (16, 17) in holes else ("16>17", "17>16")
    result = []
    for internal in internal_options:
        internal_out = {"h": (0, 0), "16>17": (1, 0), "17>16": (0, 1)}[internal]
        for high in itertools.product((0, 1), repeat=2):
            cb = []
            for i, c in enumerate(C):
                forced = sum(colors[v] in "RA" and tuple(sorted((c, v))) not in holes for v in range(18))
                slots = sum(colors[v] == "B" and tuple(sorted((c, v))) not in holes for v in range(18))
                value = 8 + high[i] - forced - internal_out[i]
                if not 0 <= value <= slots:
                    break
                cb.append(value)
            if len(cb) == 2 and not any(high[i] and not internal_out[i] and cb[i] == 0 for i in range(2)):
                result.append((hvec, internal, high, tuple(cb)))
    return result


def state_key(state):
    hvec, internal, high, cb = state
    code = {"h": "h", "16>17": "f", "17>16": "r"}[internal]
    return f"h{hvec[0]}{hvec[1]}-c{code}-m{high[0]}{high[1]}-b{cb[0]}{cb[1]}"


def representative(left_size, right_size, intersection):
    return (frozenset(B[:left_size]),
            frozenset(B[:intersection] + B[left_size:left_size + right_size - intersection]))


@lru_cache(maxsize=None)
def independent_orbits(left_size, right_size):
    universe = {(frozenset(left), frozenset(right)) for left in itertools.combinations(B, left_size)
                for right in itertools.combinations(B, right_size)}
    unseen, result = set(universe), []
    while unseen:
        seed = min(unseen, key=lambda x: (len(x[0] & x[1]), tuple(sorted(x[0])), tuple(sorted(x[1]))))
        images = set()
        for image in itertools.permutations(B):
            mapping = dict(zip(B, image))
            images.add((frozenset(mapping[v] for v in seed[0]), frozenset(mapping[v] for v in seed[1])))
        if not images <= unseen:
            raise RuntimeError("independent S7 orbits overlap")
        unseen.difference_update(images)
        result.append((len(seed[0] & seed[1]), len(images)))
    return tuple(sorted(result))


@lru_cache(maxsize=1)
def derive():
    groups = clean.derive_groups(HERE / "m6-clean-sink-remaining.tsv",
                                 HERE / "m6-placement-cover.txt", HERE / "m6-placement-filter.txt")
    parents = tuple(groups["B7-l3"])
    cells = defaultdict(list)
    for member in parents:
        for state in independent_states(member[2]):
            cells[state].append(member)
    states = [(state_key(state), state, cells[state]) for state in sorted(cells)]
    ordered = sorted(enumerate(states), key=lambda item: (item[1][1][1], item[1][1][2],
                                                           item[1][1][3], item[1][1][0]))
    profiles = []
    for state_ordinal, (key, state, members) in ordered:
        for intersection, size in independent_orbits(*state[3]):
            ordinal = len(profiles)
            profiles.append((f"p{ordinal:02d}", state_ordinal, key, state, intersection,
                             representative(*state[3], intersection), size, members))
    if (len(parents), len(states), sum(len(x[2]) for x in states), len(profiles),
            sum(len(x[7]) for x in profiles)) != (5016, 16, 27558, 19, 32574):
        raise RuntimeError("independent B7-l3 census differs")
    return tuple(profiles)


def member_payload(members):
    lines = ["columns\tselector-ordinal,accepted-ordinal,cover-index"]
    lines.extend(f"{i:03d}\t{accepted:05d}\t{cover:06d}" for i, (accepted, cover, _) in enumerate(members))
    return ("\n".join(lines) + "\n").encode("ascii")


def add_threshold(names, clauses, inputs, tag):
    previous = []
    for index, literal in enumerate(inputs, 1):
        current = []
        for target in range(1, index + 1):
            names.append(f"cnt_{tag}_{index}_{target}")
            value = len(names)
            current.append(value)
            same = previous[target - 1] if target <= len(previous) else None
            lower = previous[target - 2] if target >= 2 else True
            if same is not None:
                clauses.append((-same, value))
            clauses.append((-literal, value) if lower is True else (-literal, -lower, value))
            if same is None:
                clauses.append((-value, literal))
                if lower is not True:
                    clauses.append((-value, lower))
            else:
                clauses.append((-value, same, literal))
                if lower is not True:
                    clauses.append((-value, same, lower))
        previous = current
    return previous


def reconstruct(profile):
    _, _, _, state, _, subsets, _, members = profile
    cnf = generate(18, 7, 6, robust_witness=True, arc_minimal=True)
    if len(cnf.names) != BASE_VARIABLES or variable_map_sha256(tuple(cnf.names)) != BASE_VARIABLE_MAP_SHA256 or \
            len(cnf.clauses) != BASE_CLAUSES["B7"] or clause_sha256(tuple(cnf.clauses)) != BASE_CLAUSE_SHA256["B7"]:
        raise RuntimeError("independent B7 base differs")
    names, clauses = list(cnf.names), list(cnf.clauses)
    number = {name: i for i, name in enumerate(names, 1)}
    _, internal, high, _ = state
    clauses.append((number[{"h": "h_16_17", "16>17": "a_16_17", "17>16": "a_17_16"}[internal]],))
    for c, bit in zip(C, high):
        value = number[f"cnt_d1_{c}_17_9"]
        clauses.append((value if bit else -value,))
    for c, subset in zip(C, subsets):
        for b in B:
            value = number[f"a_{c}_{b}"]
            clauses.append((value if b in subset else -value,))
    selectors = []
    for i in range(len(members)):
        names.append(f"b7_l3_profile_parent_{i:03d}")
        selectors.append(len(names))
    clauses.append(tuple(selectors))
    for selector, (_, _, row) in zip(selectors, members):
        holes = frozenset(expected_projection(row)[1])
        for u, v in PAIRS:
            value = number[f"h_{u}_{v}"]
            clauses.append((-selector, value if (u, v) in holes else -value))
    before = len(names), len(clauses)
    high_all = tuple(number[f"cnt_d1_{v}_17_9"] for v in range(18))
    edges = tuple(number[f"a_{a}_{b}"] for a in A for b in B)
    holes = tuple(number[f"h_{a}_{b}"] for i, a in enumerate(A) for b in A[i + 1:])
    high_a = tuple(number[f"cnt_d1_{a}_17_9"] for a in A)
    global_count = add_threshold(names, clauses, high_all, "b7_l3_root_global_high")
    edge_count = add_threshold(names, clauses, edges, "b7_l3_root_AB_edges")
    rhs_count = add_threshold(names, clauses, holes + high_a, "b7_l3_root_A_holes_high")
    clauses.extend(((global_count[2],), (-global_count[3],), (edge_count[35],)))
    for offset in range(1, len(rhs_count) + 1):
        if 36 + offset <= len(edge_count):
            clauses.extend(((-rhs_count[offset - 1], edge_count[35 + offset]),
                            (rhs_count[offset - 1], -edge_count[35 + offset])))
        else:
            clauses.append((-rhs_count[offset - 1],))
    return names, clauses, selectors, (len(names) - before[0], len(clauses) - before[1])


def load_manifest():
    data = MANIFEST.read_bytes()
    lines = data.decode("ascii").splitlines()
    columns = "columns\tposition,key,state-ordinal,state-key,h16,h17,internal,high-mask,cb16,cb17,t,S7-orbit-size,parents,variables,clauses,member-sha256"
    if data != ("\n".join(lines) + "\n").encode("ascii") or lines[0] != f"{PREFIX}-manifest-v1" or \
            lines.count(columns) != 1:
        raise RuntimeError("manifest framing differs")
    rows = lines[lines.index(columns) + 1:]
    if len(rows) != 19 or "certificate-status\tnot-started" not in lines:
        raise RuntimeError("manifest scope or certificate status differs")
    return data, rows


def metadata(position, profile, manifest, selectors, delta):
    key, state_ordinal, state_key_value, state, intersection, subsets, size, members = profile
    hvec, internal, high, cb = state
    return [("format", f"{PREFIX}-cnf-v1"), ("manifest-format", f"{PREFIX}-manifest-v1"),
            ("manifest-bytes", str(len(manifest))), ("manifest-sha256", hashlib.sha256(manifest).hexdigest()),
            ("position", str(position)), ("key", key), ("state-ordinal", str(state_ordinal)),
            ("state-key", state_key_value), ("h-vector", f"{hvec[0]},{hvec[1]}"), ("internal-C", internal),
            ("high-mask", f"{high[0]}{high[1]}"), ("C-row-sizes", f"{cb[0]},{cb[1]}"),
            ("intersection-t", str(intersection)), ("S7-orbit-size", str(size)),
            ("C16-subset", ",".join(map(str, sorted(subsets[0])))),
            ("C17-subset", ",".join(map(str, sorted(subsets[1])))), ("parents", str(len(members))),
            ("member-sha256", hashlib.sha256(member_payload(members)).hexdigest()),
            ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1])),
            ("global-high", "3"), ("root-identity", "e(A,B)=36+H(A)+high(A)"),
            ("cardinality-added-variables", str(delta[0])), ("cardinality-added-clauses", str(delta[1])),
            ("certificate-status", "not-started")]


def write_reconstruction(path, position, profile, manifest):
    names, clauses, selectors, delta = reconstruct(profile)
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in metadata(position, profile, manifest, selectors, delta):
            handle.write(f"c {name} {value}\n")
        for number, name in enumerate(names, 1):
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(names)} {len(clauses)}\n")
        for clause in clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def load_hashes(manifest):
    lines = HASHES.read_text(encoding="ascii").splitlines()
    expected = [f"{PREFIX}-hashes-v1", f"manifest-bytes\t{len(manifest)}",
                f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}", "profiles\t19",
                "columns\tposition,key,parents,variables,clauses,cnf-bytes,cnf-sha256"]
    if lines[:5] != expected or len(lines) != 24:
        raise RuntimeError("hash ledger framing differs")
    result = []
    for position, line in enumerate(lines[5:]):
        fields = line.split("\t")
        if len(fields) != 7 or fields[:2] != [f"{position:02d}", f"p{position:02d}"] or \
                not fields[5].isdigit() or re.fullmatch(r"[0-9a-f]{64}", fields[6]) is None:
            raise RuntimeError("hash ledger row differs")
        result.append((int(fields[5]), fields[6]))
    return tuple(result)


def semantic_audit():
    if 153 - 6 != 147 or 147 != 18 * 8 + 3:
        raise RuntimeError("global high derivation failed")
    for holes, high_a in itertools.product(range(29), range(9)):
        if 64 + high_a - (28 - holes) != 36 + holes + high_a:
            raise RuntimeError("root cut identity failed")
    for degrees in itertools.product((8, 9), repeat=18):
        if sum(degrees) == 147 and sum(value == 9 for value in degrees) != 3:
            raise RuntimeError("global degree audit failed")
    print("PASS semantic_audit cut_cases=261 degree_vectors=262144")


def check_cover(regenerate=True):
    profiles = derive()
    manifest, rows = load_manifest()
    hashes = load_hashes(manifest)
    if tuple(row.split("\t")[1] for row in rows) != tuple(f"p{i:02d}" for i in range(19)):
        raise RuntimeError("manifest profile order differs")
    if {reconstruct(profile)[3] for profile in profiles} != {(2433, 9571)}:
        raise RuntimeError("fresh counter dimensions differ")
    if regenerate:
        with tempfile.TemporaryDirectory(prefix="b7-l3-root-check-", dir=HERE.parent) as directory:
            path = Path(directory) / "profile.cnf"
            for position, profile in enumerate(profiles):
                write_reconstruction(path, position, profile, manifest)
                if identity(path) != hashes[position]:
                    raise RuntimeError(f"regenerated profile differs: {position:02d}")
    print(f"PASS parents=5016 states=16 profiles=19 incidences=32574 manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


def check(path):
    profiles = derive()
    manifest, _ = load_manifest()
    metadata_rows, variables, clauses, declared = parse_cnf(path)
    position = int(dict(metadata_rows).get("position", "-1"))
    if not 0 <= position < 19:
        raise RuntimeError("position outside 0..52")
    names, expected, selectors, delta = reconstruct(profiles[position])
    if metadata_rows != metadata(position, profiles[position], manifest, selectors, delta) or \
            variables != names or clauses != expected or declared != (len(names), len(expected)) or \
            identity(path) != load_hashes(manifest)[position]:
        raise RuntimeError("CNF differs from independent reconstruction")
    print(f"PASS position={position:02d} sha256={identity(path)[1]}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", nargs="?", type=Path)
    parser.add_argument("--cover", action="store_true")
    parser.add_argument("--semantic", action="store_true")
    args = parser.parse_args()
    if args.cover:
        check_cover()
    if args.semantic:
        semantic_audit()
    if args.cnf:
        check(args.cnf)
    if not (args.cover or args.semantic or args.cnf):
        parser.error("select --cover, --semantic, or a CNF")


if __name__ == "__main__":
    main()
