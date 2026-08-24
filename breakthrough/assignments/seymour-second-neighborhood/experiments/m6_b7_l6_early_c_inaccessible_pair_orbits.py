#!/usr/bin/env python3
"""Cover eight one-high early C profiles by low-C inaccessible-pair orbits."""

import argparse
import hashlib
import itertools
import tempfile
from pathlib import Path

import m6_b7_l6_early_c_profile_census as source

HERE = Path(__file__).resolve().parent
PREFIX = "m6-b7-l6-early-c-inaccessible-pair"
FORMAT = f"{PREFIX}-cnf-v1"
MANIFEST_FORMAT = f"{PREFIX}-orbits-v1"
HASH_FORMAT = f"{PREFIX}-hashes-v1"
PROFILES = (3, 11, 23, 25, 28, 47, 49, 54)
B = tuple(range(9, 16))
C = (16, 17)
CHILDREN = 192
MEMBERSHIPS = 746
SOURCE_PATH = HERE / "m6-b7-l6-early-c-profile-census.tsv"
SOURCE_IDENTITY = (10271, "985a558c3b831994ed2febbb3e4569cf7df4869919f897c3ab6e0e96dbdce5f9")


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def stabilizer(subsets):
    cells = {}
    for b in B:
        cells.setdefault(tuple(b in subset for subset in subsets), []).append(b)
    result = []
    for images in itertools.product(*(itertools.permutations(cell) for cell in cells.values())):
        permutation = {}
        for cell, image in zip(cells.values(), images):
            permutation.update(zip(cell, image))
        result.append(permutation)
    return tuple(result)


def parent_holes(row):
    return frozenset(source.states.source.parent.embedded_holes(
        row["branch"], row["word"], row["edges"])[1])


def low_vertex(state):
    low = tuple(c for c, high in zip(C, state[2]) if not high)
    if len(low) != 1:
        raise RuntimeError("profile is not one-high")
    return low[0]


def nonoutneighbors(low, state, subsets, holes):
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
    if len(result) != 9:
        raise RuntimeError("degree-eight low C does not have nine nonoutneighbors")
    return frozenset(result)


def pair_orbits(profile):
    state, subsets, members = profile[3], profile[5], profile[7]
    low = low_vertex(state)
    supports = tuple((parent_holes(row), nonoutneighbors(low, state, subsets, parent_holes(row)))
                     for _, _, row in members)
    universe = {frozenset(pair) for _, nonout in supports for pair in itertools.combinations(nonout, 2)}
    group = stabilizer(subsets)
    unseen, records = set(universe), []
    while unseen:
        seed = min(unseen, key=lambda pair: tuple(sorted(pair)))
        orbit = {frozenset(permutation.get(v, v) for v in seed) for permutation in group}
        if not orbit <= universe:
            raise RuntimeError("profile stabilizer does not preserve the pair universe")
        representative = min(orbit, key=lambda pair: tuple(sorted(pair)))
        compatible = tuple(i for i, (_, nonout) in enumerate(supports) if representative <= nonout)
        if not compatible:
            raise RuntimeError("pair orbit has no compatible parent support")
        records.append((representative, len(orbit), compatible))
        unseen -= orbit
    return low, tuple(records)


def load_children():
    if identity(SOURCE_PATH) != SOURCE_IDENTITY:
        raise RuntimeError("frozen early C profile census changed")
    profiles = source.load_orbits()
    children = []
    for profile_ordinal in PROFILES:
        profile = profiles[profile_ordinal]
        low, records = pair_orbits(profile)
        for pair_ordinal, (pair, orbit_size, compatible) in enumerate(records):
            key = f"o{profile_ordinal:02d}-i{pair_ordinal:02d}"
            children.append((key, profile_ordinal, profile, pair, orbit_size, compatible))
    if len(children) != CHILDREN or sum(len(child[5]) for child in children) != MEMBERSHIPS:
        raise RuntimeError("inaccessible-pair cover totals changed")
    return tuple(children)


def dimensions(child):
    parents = len(child[2][7])
    variables, clauses = source.dimensions(parents)
    return variables, clauses + 2 + parents - len(child[5])


def build_child(child):
    cnf, selectors = source.build_orbit(child[2])
    low = low_vertex(child[2][3])
    for vertex in sorted(child[3]):
        cnf.add(-cnf.names[f"q_{low}_{vertex}"])
    compatible = set(child[5])
    for index, selector in enumerate(selectors):
        if index not in compatible:
            cnf.add(-selector)
    return cnf, selectors


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


def write_child(path, ordinal, child, cnf, selectors, manifest):
    compatible = set(child[5])
    metadata = [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
                ("manifest-bytes", str(len(manifest))),
                ("manifest-sha256", hashlib.sha256(manifest).hexdigest()),
                ("source-bytes", str(SOURCE_IDENTITY[0])), ("source-sha256", SOURCE_IDENTITY[1]),
                ("child", str(ordinal)), ("child-key", child[0]),
                ("profile", str(child[1])), ("profile-key", child[2][0]),
                ("low-C", str(low_vertex(child[2][3]))),
                ("inaccessible-pair", ",".join(map(str, sorted(child[3])))),
                ("labelled-pair-orbit-size", str(child[4])),
                ("compatible-parent-ordinals", ",".join(map(str, child[5]))),
                ("compatible-parents", str(len(child[5]))),
                ("inaccessible-q-unit-clauses", "2"),
                ("excluded-selector-unit-clauses", str(len(selectors) - len(compatible))),
                ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1]))]
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in metadata:
            handle.write(f"c {name} {value}\n")
        for name, number in cnf.names.items():
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def hash_payload(children, manifest, hashes):
    lines = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
             f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}", f"children\t{CHILDREN}",
             "columns\tchild,key,compatible-parents,variables,clauses,cnf-bytes,cnf-sha256"]
    for ordinal, child in enumerate(children):
        variables, clauses = dimensions(child)
        size, digest = hashes.get(child[0], ("", ""))
        lines.append(f"{ordinal:03d}\t{child[0]}\t{len(child[5])}\t{variables}\t{clauses}\t{size}\t{digest}")
    return ("\n".join(lines) + "\n").encode("ascii")


def populate_hashes(children, manifest):
    result = {}
    with tempfile.TemporaryDirectory(prefix="inaccessible-pair-hashes-", dir=HERE.parent) as directory:
        path = Path(directory) / "child.cnf"
        for ordinal, child in enumerate(children):
            cnf, selectors = build_child(child)
            write_child(path, ordinal, child, cnf, selectors, manifest)
            result[child[0]] = identity(path)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--child", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--hash-output", type=Path)
    parser.add_argument("--populate-hashes", action="store_true")
    args = parser.parse_args()
    children = load_children()
    manifest = manifest_payload(children)
    if args.manifest_output:
        args.manifest_output.write_bytes(manifest)
    if args.hash_output:
        hashes = populate_hashes(children, manifest) if args.populate_hashes else {}
        args.hash_output.write_bytes(hash_payload(children, manifest, hashes))
    if args.output:
        if args.child is None or not 0 <= args.child < len(children):
            parser.error("--output requires a valid --child")
        cnf, selectors = build_child(children[args.child])
        write_child(args.output, args.child, children[args.child], cnf, selectors, manifest)
    print(f"PASS profiles=8 children={CHILDREN} memberships={MEMBERSHIPS} "
          f"manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


if __name__ == "__main__":
    main()
