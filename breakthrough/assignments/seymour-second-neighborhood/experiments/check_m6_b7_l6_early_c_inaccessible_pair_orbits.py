#!/usr/bin/env python3
"""Independent universe, stabilizer, parent-support, and CNF checker."""

import argparse
import hashlib
import itertools
import json
import math
import re
import tempfile
from functools import lru_cache
from pathlib import Path

import check_m6_b7_l6_early_c_profile_census as source
from check_m6_parent_cnf import (BASE_CLAUSES, BASE_CLAUSE_SHA256, BASE_VARIABLES,
                                 BASE_VARIABLE_MAP_SHA256, PAIRS, clause_sha256,
                                 expected_projection, parse_cnf, variable_map_sha256)
from snc_cnf import generate

HERE = Path(__file__).resolve().parent
PREFIX = "m6-b7-l6-early-c-inaccessible-pair"
FORMAT = f"{PREFIX}-cnf-v1"
MANIFEST_FORMAT = f"{PREFIX}-orbits-v1"
HASH_FORMAT = f"{PREFIX}-hashes-v1"
MANIFEST = HERE / f"{PREFIX}-orbits.tsv"
HASHES = HERE / f"{PREFIX}-hashes.tsv"
SCOUT = HERE / f"{PREFIX}-scout-1s.json"
PROFILES = (3, 11, 23, 25, 28, 47, 49, 54)
B = tuple(range(9, 16))
C = (16, 17)
CHILDREN, MEMBERSHIPS = 192, 746
SOURCE_IDENTITY = (10271, "985a558c3b831994ed2febbb3e4569cf7df4869919f897c3ab6e0e96dbdce5f9")
SOLVER_IDENTITY = ("/tmp/opencode/cadical-1.7.3/build/cadical", 1002216,
                   "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292", "1.7.3")
STATUS_SEQUENCE = ("UTUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUTUUUTUUUTUUUTUUUUUUUUUTUUUUUUUUUUUUUUUUUUUUUUU"
                   "TUUUUUUUTUUUTUUUUUUUUUUUUUUUUUTUUUTUUUTUUTUUUUUUTUUUUUUUUUUUUUUUUUUUUUUUUUUUTUUU"
                   "TUUUTUUUUUUUUUUUUUUUUUTUUUTUTUUUU")
STATUS_SEQUENCE_SHA256 = "07e6e6e189544bede5004996a7bcb70db3ad4ed99bd20de5b1632e86388d2434"
SCOUT_IDENTITY = (47594, "1c324d6ce3b73ebdb9abdc8bafcaed1a3373541b208c7ef22002d1556bd3a480")


def explicit_stabilizer(subsets):
    result = []
    for image in itertools.permutations(B):
        permutation = dict(zip(B, image))
        if all({permutation[v] for v in subset} == set(subset) for subset in subsets):
            result.append(permutation)
    return tuple(result)


def low_vertex(state):
    low = tuple(c for c, high in zip(C, state[2]) if not high)
    if len(low) != 1:
        raise RuntimeError("selected profile is not one-high")
    return low[0]


def parent_nonoutneighbors(profile, row):
    state, subsets = profile[3], profile[5]
    low = low_vertex(state)
    holes = frozenset(expected_projection(row)[1])
    result = set()
    for vertex in range(18):
        if vertex == low:
            continue
        pair = tuple(sorted((low, vertex)))
        if vertex < 9 and pair in holes:
            result.add(vertex)
        elif vertex in B and vertex not in subsets[low - 16]:
            result.add(vertex)
        elif vertex in C and (state[1] == "h" or state[1] == f"{vertex}>{low}"):
            result.add(vertex)
    # The profile fixes low outdegree eight. Every one of the other 17
    # vertices is either an outneighbor or a nonoutneighbor, hence exactly nine
    # are in this set. If fewer than two were q-inaccessible, at least eight of
    # these nine nonoutneighbors would be exact second neighbors. Together with
    # eight first neighbors this gives d++ >= d+ = 8, contradicting badness.
    if len(result) != 9:
        raise RuntimeError("independent degree-eight nonoutneighbor census differs")
    return holes, frozenset(result)


def verify_parent_invariance(profile, supports, group):
    support_set = {holes for holes, _ in supports}
    for holes, nonout in supports:
        for permutation in group:
            image_holes = frozenset(tuple(sorted((permutation.get(a, a), permutation.get(b, b))))
                                    for a, b in holes)
            if image_holes not in support_set:
                raise RuntimeError("profile stabilizer does not preserve parent supports")
            image_nonout = frozenset(permutation.get(v, v) for v in nonout)
            expected = dict(supports)[image_holes]
            if image_nonout != expected:
                raise RuntimeError("parent support and pair compatibility do not transform together")


@lru_cache(maxsize=1)
def derive_children():
    data = (HERE / "m6-b7-l6-early-c-profile-census.tsv").read_bytes()
    if (len(data), hashlib.sha256(data).hexdigest()) != SOURCE_IDENTITY:
        raise RuntimeError("frozen profile source changed")
    profiles = source.derive()
    children = []
    for profile_ordinal in PROFILES:
        profile = profiles[profile_ordinal]
        supports = tuple(parent_nonoutneighbors(profile, row) for _, _, row in profile[7])
        if len({holes for holes, _ in supports}) != len(supports):
            raise RuntimeError("duplicate parent supports")
        group = explicit_stabilizer(profile[5])
        verify_parent_invariance(profile, supports, group)
        universe = {frozenset(pair) for _, nonout in supports for pair in itertools.combinations(nonout, 2)}
        unseen = set(universe)
        pair_ordinal = 0
        while unseen:
            seed = min(unseen, key=lambda pair: tuple(sorted(pair)))
            orbit = {frozenset(permutation.get(v, v) for v in seed) for permutation in group}
            if not orbit <= universe:
                raise RuntimeError("pair orbit escapes exact parent-derived universe")
            representative = min(orbit, key=lambda pair: tuple(sorted(pair)))
            compatible = tuple(i for i, (_, nonout) in enumerate(supports) if representative <= nonout)
            if not compatible:
                raise RuntimeError("canonical pair lost all compatible parent support")
            key = f"o{profile_ordinal:02d}-i{pair_ordinal:02d}"
            children.append((key, profile_ordinal, profile, representative, len(orbit), compatible))
            unseen -= orbit
            pair_ordinal += 1
    if len(children) != CHILDREN or sum(len(child[5]) for child in children) != MEMBERSHIPS:
        raise RuntimeError("independent 192/746 cover differs")
    return tuple(children)


def dimensions(child):
    count = len(child[2][7])
    return BASE_VARIABLES + count, BASE_CLAUSES["B7"] + 18 + 153 * count + 2 + count - len(child[5])


def manifest_payload(children):
    lines = [MANIFEST_FORMAT, f"source-bytes\t{SOURCE_IDENTITY[0]}",
             f"source-sha256\t{SOURCE_IDENTITY[1]}",
             "profiles\t" + ",".join(f"{profile:02d}" for profile in PROFILES),
             f"children\t{CHILDREN}", f"parent-pair-memberships\t{MEMBERSHIPS}",
             "semantics\tq is exact distance two; each child adds two -q units",
             "cover\texistential ALO overlap cover modulo profile stabilizer with compatible parent support",
             "columns\tchild,key,profile,pair-orbit,low-C,pair,labelled-orbit-size,compatible-parents,variables,clauses"]
    for ordinal, child in enumerate(children):
        variables, clauses = dimensions(child)
        lines.append(f"{ordinal:03d}\t{child[0]}\t{child[1]:02d}\t{child[0].rsplit('i', 1)[1]}\t"
                     f"{low_vertex(child[2][3])}\t{','.join(map(str, sorted(child[3])))}\t{child[4]}\t"
                     f"{len(child[5])}\t{variables}\t{clauses}")
    return ("\n".join(lines) + "\n").encode("ascii")


def load_hashes(manifest, path=HASHES):
    data = path.read_bytes()
    lines = data.decode("ascii").splitlines()
    expected = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
                f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}",
                f"children\t{CHILDREN}",
                "columns\tchild,key,compatible-parents,variables,clauses,cnf-bytes,cnf-sha256"]
    if lines[:5] != expected or len(lines) != CHILDREN + 5:
        raise RuntimeError("pair hash ledger framing differs")
    result = {}
    children = derive_children()
    for ordinal, (line, child) in enumerate(zip(lines[5:], children)):
        fields = line.split("\t")
        if len(fields) != 7 or fields[0] != f"{ordinal:03d}" or not fields[5].isdigit() or \
                re.fullmatch(r"[0-9a-f]{64}", fields[6]) is None:
            raise RuntimeError("malformed pair hash row")
        variables, clauses = dimensions(child)
        if fields[1] != child[0] or fields[2:5] != [str(len(child[5])), str(variables), str(clauses)]:
            raise RuntimeError("pair hash row support or dimensions differ")
        result[fields[1]] = int(fields[5]), fields[6]
    canonical = ("\n".join(lines) + "\n").encode("ascii")
    if data != canonical or len(result) != CHILDREN:
        raise RuntimeError("pair hash ledger is not canonical and complete")
    return result


@lru_cache(maxsize=1)
def frozen_base():
    cnf = generate(18, 7, 6, robust_witness=True, arc_minimal=True)
    names, clauses = tuple(cnf.names), tuple(cnf.clauses)
    if len(names) != BASE_VARIABLES or variable_map_sha256(names) != BASE_VARIABLE_MAP_SHA256 or \
            len(clauses) != BASE_CLAUSES["B7"] or clause_sha256(clauses) != BASE_CLAUSE_SHA256["B7"]:
        raise RuntimeError("independent B7 base changed")
    return names, clauses


def reconstruct(child):
    names, clauses = map(list, frozen_base())
    profile, state, subsets = child[2], child[2][3], child[2][5]
    units = [(names.index({"h": "h_16_17", "16>17": "a_16_17", "17>16": "a_17_16"}[state[1]]) + 1,)]
    for c, high in zip(C, state[2]):
        variable = names.index(f"cnt_d1_{c}_17_9") + 1
        units.append((variable if high else -variable,))
    for c, subset in zip(C, subsets):
        for b in B:
            variable = names.index(f"a_{c}_{b}") + 1
            units.append((variable if b in subset else -variable,))
    selectors = list(range(BASE_VARIABLES + 1, BASE_VARIABLES + len(profile[7]) + 1))
    names += [f"early_c_profile_parent_{i:02d}" for i in range(len(selectors))]
    clauses += units + [tuple(selectors)]
    for selector, (_, _, row) in zip(selectors, profile[7]):
        holes = frozenset(expected_projection(row)[1])
        for pair in PAIRS:
            variable = names.index(f"h_{pair[0]}_{pair[1]}") + 1
            clauses.append((-selector, variable if pair in holes else -variable))
    low = low_vertex(state)
    for vertex in sorted(child[3]):
        clauses.append((-(names.index(f"q_{low}_{vertex}") + 1),))
    compatible = set(child[5])
    clauses.extend((-selector,) for i, selector in enumerate(selectors) if i not in compatible)
    return names, clauses, selectors


def metadata(ordinal, child, manifest, selectors):
    return [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
            ("manifest-bytes", str(len(manifest))),
            ("manifest-sha256", hashlib.sha256(manifest).hexdigest()),
            ("source-bytes", str(SOURCE_IDENTITY[0])), ("source-sha256", SOURCE_IDENTITY[1]),
            ("child", str(ordinal)), ("child-key", child[0]), ("profile", str(child[1])),
            ("profile-key", child[2][0]), ("low-C", str(low_vertex(child[2][3]))),
            ("inaccessible-pair", ",".join(map(str, sorted(child[3])))),
            ("labelled-pair-orbit-size", str(child[4])),
            ("compatible-parent-ordinals", ",".join(map(str, child[5]))),
            ("compatible-parents", str(len(child[5]))), ("inaccessible-q-unit-clauses", "2"),
            ("excluded-selector-unit-clauses", str(len(selectors) - len(child[5]))),
            ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1]))]


def write_reconstruction(path, ordinal, child, manifest):
    names, clauses, selectors = reconstruct(child)
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in metadata(ordinal, child, manifest, selectors):
            handle.write(f"c {name} {value}\n")
        for number, name in enumerate(names, 1):
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(names)} {len(clauses)}\n")
        for clause in clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def check(path):
    children = derive_children()
    manifest = manifest_payload(children)
    if MANIFEST.read_bytes() != manifest:
        raise RuntimeError("frozen pair manifest differs")
    parsed_metadata, variables, clauses, declared = parse_cnf(path)
    ordinal = int(dict(parsed_metadata).get("child", "-1"))
    if not 0 <= ordinal < CHILDREN:
        raise RuntimeError("child ordinal outside exact cover")
    child = children[ordinal]
    names, expected, selectors = reconstruct(child)
    if parsed_metadata != metadata(ordinal, child, manifest, selectors) or variables != names or \
            clauses != expected or declared != dimensions(child):
        raise RuntimeError("pair child CNF differs from independent reconstruction")
    digest = (path.stat().st_size, hashlib.sha256(path.read_bytes()).hexdigest())
    if digest != load_hashes(manifest)[child[0]]:
        raise RuntimeError("pair child CNF identity differs")
    print(f"PASS child={ordinal:03d} key={child[0]} parents={len(child[5])} sha256={digest[1]}")


def check_scout(manifest, hashes, path=SCOUT, require_frozen_identity=True):
    raw = path.read_bytes()
    if require_frozen_identity and (len(raw), hashlib.sha256(raw).hexdigest()) != SCOUT_IDENTITY:
        raise RuntimeError("pair scout bytes or hash differ")
    data = json.loads(raw.decode("ascii"))
    rows = data.get("rows", [])
    ledger_identity = (HASHES.stat().st_size, hashlib.sha256(HASHES.read_bytes()).hexdigest())
    expected_header = {
        "schema": f"{PREFIX}-scout-v1", "seconds_per_child": 1,
        "solver": SOLVER_IDENTITY[0], "solver_bytes": SOLVER_IDENTITY[1],
        "solver_sha256": SOLVER_IDENTITY[2], "solver_version": SOLVER_IDENTITY[3],
        "manifest_bytes": len(manifest), "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
        "hash_ledger_bytes": ledger_identity[0], "hash_ledger_sha256": ledger_identity[1],
        "status_sequence_sha256": STATUS_SEQUENCE_SHA256,
    }
    if set(data) != set(expected_header) | {"rows"} or \
            any(data.get(key) != value for key, value in expected_header.items()) or len(rows) != CHILDREN:
        raise RuntimeError("pair scout provenance or framing differs")
    statuses = "".join({"UNSAT": "U", "TIMEOUT": "T"}.get(row.get("status"), "?") for row in rows)
    if statuses != STATUS_SEQUENCE or hashlib.sha256(statuses.encode("ascii")).hexdigest() != STATUS_SEQUENCE_SHA256:
        raise RuntimeError("pair scout exact 192-status sequence differs")
    expected_keys = {"child", "key", "profile", "compatible_parents", "status", "seconds", "cnf_sha256"}
    for ordinal, (row, child) in enumerate(zip(rows, derive_children())):
        if set(row) != expected_keys or row.get("child") != ordinal or row.get("key") != child[0] or \
                row.get("profile") != child[1] or \
                row.get("compatible_parents") != len(child[5]) or row.get("cnf_sha256") != hashes[child[0]][1]:
            raise RuntimeError("pair scout row differs")
        seconds = row.get("seconds")
        if isinstance(seconds, bool) or not isinstance(seconds, (int, float)) or not math.isfinite(seconds) or \
                (row["status"] == "UNSAT" and not 0 <= seconds < 1) or \
                (row["status"] == "TIMEOUT" and not 1 <= seconds <= 2):
            raise RuntimeError("pair scout timing differs")
    if raw != (json.dumps(data, sort_keys=True, indent=2) + "\n").encode("ascii"):
        raise RuntimeError("pair scout JSON is not canonical")


def check_exhaustion():
    children = derive_children()
    manifest = manifest_payload(children)
    if MANIFEST.read_bytes() != manifest:
        raise RuntimeError("frozen pair manifest differs")
    hashes = load_hashes(manifest)
    with tempfile.TemporaryDirectory(prefix="inaccessible-pair-check-", dir=HERE.parent) as directory:
        path = Path(directory) / "child.cnf"
        for ordinal, child in enumerate(children):
            write_reconstruction(path, ordinal, child, manifest)
            if (path.stat().st_size, hashlib.sha256(path.read_bytes()).hexdigest()) != hashes[child[0]]:
                raise RuntimeError(f"regenerated child {ordinal:03d} differs")
    check_scout(manifest, hashes)
    print(f"PASS profiles=8 children={CHILDREN} memberships={MEMBERSHIPS} SCOUT-UNSAT=172 "
          f"SCOUT-TIMEOUT=20 manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", type=Path, nargs="?")
    parser.add_argument("--exhaustion", action="store_true")
    args = parser.parse_args()
    if args.exhaustion:
        check_exhaustion()
    if args.cnf:
        check(args.cnf)
    if not args.exhaustion and not args.cnf:
        parser.error("provide --exhaustion or a CNF")


if __name__ == "__main__":
    main()
