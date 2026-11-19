#!/usr/bin/env python3
"""Independent checker for the exact grouped B7-l6 C-to-B (3,1) campaign."""

import argparse
import hashlib
import itertools
import re
from functools import lru_cache
from pathlib import Path

import check_m6_clean_sink_group_cnf as committed
from check_m6_parent_cnf import (BASE_CLAUSES, BASE_CLAUSE_SHA256, BASE_VARIABLES,
                                 BASE_VARIABLE_MAP_SHA256, PAIRS, clause_sha256,
                                 expected_projection, parse_cnf, variable_map_sha256)
from snc_cnf import generate

HERE = Path(__file__).resolve().parent
PREFIX = "m6-b7-l6-c-to-b-31-orbits"
MANIFEST = HERE / f"{PREFIX}.tsv"
HASHES = HERE / f"{PREFIX}-hashes.tsv"
FORMAT = f"{PREFIX}-cnf-v1"
MANIFEST_FORMAT = f"{PREFIX}-v1"
HASH_FORMAT = f"{PREFIX}-hashes-v1"
B = tuple(range(9, 16))
C = (16, 17)
PROFILES = ((frozenset(B[:3]), frozenset((B[3],))),
            (frozenset(B[:3]), frozenset((B[0],))))
SOURCE_PATHS = {
    "placement-cover": HERE / "m6-placement-cover.txt",
    "placement-filter": HERE / "m6-placement-filter.txt",
    "clean-parent-manifest": HERE / "m6-clean-sink-selector-groups.tsv",
    "clean-remaining-stream": HERE / "m6-clean-sink-remaining.tsv",
}
SOURCE_IDENTITIES = {
    "placement-cover": (6659672, "22d7744f1eecee3ea22527e4beec645ae999c912184f1f23c1a7f701e966ed5e"),
    "placement-filter": (95083, "9bfd2fadda610dde6cef7c13956edba6b0fa763e2ffc31226c0ddf1323fd1d0c"),
    "clean-parent-manifest": (1838, "6e7eee0ddd5b4c7ef02cdf459c9a0647f720513e7ee4987a3a8b0c17af37eeda"),
    "clean-remaining-stream": (2262190, "416b7e51a73637784342a374be8e15a1a58032b61fc1140f39f0768d1ff4b642"),
}


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def colors_and_holes(row):
    labels = ((0,), tuple(range(1, 9)), tuple(range(9, 16)), (16, 17))
    holes = frozenset(expected_projection(row)[1])
    colors = {v: cell for vertices, cell in zip(labels, "RABC") for v in vertices}
    return colors, holes


def independently_compatible(row):
    colors, holes = colors_and_holes(row)
    if (16, 17) in holes:
        return False
    required = []
    for i, c in enumerate(C):
        fixed = sum(colors[v] in "RA" and tuple(sorted((c, v))) not in holes for v in range(18))
        fixed += (0, 1)[i]
        available = sum(colors[v] == "B" and tuple(sorted((c, v))) not in holes for v in range(18))
        value = 8 + (1, 0)[i] - fixed
        if not 0 <= value <= available:
            return False
        required.append(value)
    return tuple(required) == (3, 1)


@lru_cache(maxsize=1)
def derive():
    for name, path in SOURCE_PATHS.items():
        if identity(path) != SOURCE_IDENTITIES[name]:
            raise RuntimeError(f"strict source binding changed: {name}")
    groups = committed.derive_groups(
        SOURCE_PATHS["clean-remaining-stream"], SOURCE_PATHS["placement-cover"],
        SOURCE_PATHS["placement-filter"])
    all_parents = tuple(groups["B7-l6"])
    parents = tuple(item for item in all_parents if independently_compatible(item[2]))
    expected = ((23728, 112443), (23737, 112460), (24899, 114188), (24952, 114264),
                (24958, 114275), (29966, 121458), (30098, 121657), (30101, 121663),
                (41947, 138180), (42075, 138397))
    if len(all_parents) != 42 or tuple((x[0], x[1]) for x in parents) != expected:
        raise RuntimeError("direct committed-cover exhaustion is not exactly the ten parents")
    return all_parents, parents


@lru_cache(maxsize=1)
def derive_ordered_subset_orbits():
    """Derive the ordered (3,1) subset orbits from all 7! labelled actions."""
    universe = tuple((frozenset(left), frozenset((right,)))
                     for left in itertools.combinations(B, 3) for right in B)
    permutations = tuple(dict(zip(B, image)) for image in itertools.permutations(B))
    unseen, orbits = set(universe), []
    while unseen:
        seed = min(unseen, key=lambda pair: (tuple(sorted(pair[0])), tuple(pair[1])))
        orbit = frozenset((frozenset(mapping[x] for x in seed[0]),
                           frozenset(mapping[x] for x in seed[1])) for mapping in permutations)
        if not orbit <= unseen:
            raise RuntimeError("ordered subset orbits overlap")
        unseen.difference_update(orbit)
        orbits.append((seed, orbit))
    orbits.sort(key=lambda item: len(item[0][0] & item[0][1]))
    if len(permutations) != 5040 or unseen or len(universe) != 245 or \
            tuple(len(orbit) for _, orbit in orbits) != (140, 105) or \
            tuple(len(left & right) for (left, right), _ in orbits) != (0, 1):
        raise RuntimeError("full S7 ordered subset orbit derivation differs")
    representatives = tuple(PROFILES[len(left & right)] for (left, right), _ in orbits)
    for representative, (_, orbit) in zip(representatives, orbits):
        if representative not in orbit:
            raise RuntimeError("canonical ordered subset representative is outside its orbit")
    return tuple((representative, orbit) for representative, (_, orbit) in zip(representatives, orbits))


def member_payload(parents):
    lines = ["columns\tselector-ordinal,accepted-ordinal,cover-index,support,graph6,word"]
    lines.extend(f"{i:02d}\t{a:05d}\t{cover:06d}\t{row[1]:03d}\t{row[3]}\t{row[4]}"
                 for i, (a, cover, row) in enumerate(parents))
    return ("\n".join(lines) + "\n").encode("ascii")


def dimensions():
    return BASE_VARIABLES + 10, BASE_CLAUSES["B7"] + 1548


def manifest_payload(all_parents, parents):
    member = member_payload(parents)
    lines = [MANIFEST_FORMAT]
    for name, value in SOURCE_IDENTITIES.items():
        lines.extend((f"{name}-bytes\t{value[0]}", f"{name}-sha256\t{value[1]}"))
    lines.extend(("branch\tB7", "lambda\t6", f"committed-B7-l6-parents\t{len(all_parents)}",
                  "ordered-C-row-sizes\t3,1", "internal-C\t17>16", "high-mask\t10",
                  "compatible-parents\t10", f"compatible-parent-sha256\t{hashlib.sha256(member).hexdigest()}",
                  "exhaustion\tfilter all 42 committed B7-l6 parents by direct rooted-cell degree accounting; exactly these 10 admit required ordered C-to-B counts (3,1)",
                  "orbits\t2", "columns\torbit,t,C16-subset,C17-subset,parents,variables,clauses"))
    variables, clauses = dimensions()
    for t, subsets in enumerate(PROFILES):
        lines.append(f"{t}\t{t}\t{','.join(map(str, sorted(subsets[0])))}\t"
                     f"{','.join(map(str, sorted(subsets[1])))}\t10\t{variables}\t{clauses}")
    return ("\n".join(lines) + "\n").encode("ascii")


def expected_metadata(t, manifest, parents, selectors):
    result = [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
              ("manifest-bytes", str(len(manifest))), ("manifest-sha256", hashlib.sha256(manifest).hexdigest())]
    for name, value in SOURCE_IDENTITIES.items():
        result.extend(((f"{name}-bytes", str(value[0])), (f"{name}-sha256", value[1])))
    result.extend((("branch", "B7"), ("lambda", "6"), ("ordered-C-row-sizes", "3,1"),
                   ("intersection-t", str(t)), ("internal-C", "17>16"), ("high-mask", "10"),
                   ("C16-subset", ",".join(map(str, sorted(PROFILES[t][0])))),
                   ("C17-subset", ",".join(map(str, sorted(PROFILES[t][1])))),
                   ("committed-parent-census", "42"), ("compatible-parents", "10"),
                   ("compatible-parent-sha256", hashlib.sha256(member_payload(parents)).hexdigest()),
                   ("profile-unit-clauses", "17"), ("alo-clauses", "1"),
                   ("guarded-hole-clauses-per-parent", "153"),
                   ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1]))))
    return result


@lru_cache(maxsize=1)
def check_manifest():
    all_parents, parents = derive()
    derive_ordered_subset_orbits()
    payload = manifest_payload(all_parents, parents)
    if MANIFEST.read_bytes() != payload:
        raise RuntimeError("manifest differs from independent committed-cover exhaustion")
    return parents, payload


@lru_cache(maxsize=1)
def load_hashes():
    _, manifest = check_manifest()
    lines = HASHES.read_text(encoding="ascii").splitlines()
    expected = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
                f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}", "groups\t2",
                "columns\torbit,t,parents,variables,clauses,cnf-bytes,cnf-sha256"]
    if lines[:5] != expected or len(lines) != 7 or HASHES.read_bytes() != ("\n".join(lines) + "\n").encode("ascii"):
        raise RuntimeError("hash ledger framing differs")
    result = []
    variables, clauses = dimensions()
    for t, line in enumerate(lines[5:]):
        fields = line.split("\t")
        if fields[:5] != [str(t), str(t), "10", str(variables), str(clauses)] or len(fields) != 7 or \
                not fields[5].isdigit() or re.fullmatch(r"[0-9a-f]{64}", fields[6]) is None:
            raise RuntimeError(f"hash row differs: t={t}")
        result.append((int(fields[5]), fields[6]))
    return tuple(result)


def reconstruct(t, parents):
    cnf = generate(18, 7, 6, robust_witness=True, arc_minimal=True)
    base_names, base_clauses = tuple(cnf.names), tuple(cnf.clauses)
    if (len(base_names) != BASE_VARIABLES or variable_map_sha256(base_names) != BASE_VARIABLE_MAP_SHA256 or
            len(base_clauses) != BASE_CLAUSES["B7"] or clause_sha256(base_clauses) != BASE_CLAUSE_SHA256["B7"]):
        raise RuntimeError("independent B7 base identity differs")
    cnf.add(cnf.names["a_17_16"])
    cnf.add(cnf.names["cnt_d1_16_17_9"])
    cnf.add(-cnf.names["cnt_d1_17_17_9"])
    for c, subset in zip(C, PROFILES[t]):
        for b in B:
            number = cnf.names[f"a_{c}_{b}"]
            cnf.add(number if b in subset else -number)
    selectors = [cnf.var(f"b7_l6_c_to_b_31_t{t}_parent_{i:02d}") for i in range(10)]
    cnf.add(*selectors)
    for selector, (_, _, row) in zip(selectors, parents):
        holes = frozenset(expected_projection(row)[1])
        for pair in PAIRS:
            number = cnf.names[f"h_{pair[0]}_{pair[1]}"]
            cnf.add(-selector, number if pair in holes else -number)
    return list(cnf.names), list(cnf.clauses), selectors


def validate_clause_families(t, names, clauses, selectors, parents):
    name_to_number = {name: number for number, name in enumerate(names, start=1)}
    base_count = BASE_CLAUSES["B7"]
    profile = clauses[base_count:base_count + 17]
    expected_profile = [(name_to_number["a_17_16"],),
                        (name_to_number["cnt_d1_16_17_9"],),
                        (-name_to_number["cnt_d1_17_17_9"],)]
    for c, subset in zip(C, PROFILES[t]):
        expected_profile.extend(((name_to_number[f"a_{c}_{b}"] if b in subset else
                                  -name_to_number[f"a_{c}_{b}"],) for b in B))
    if profile != expected_profile or clauses[base_count + 17] != tuple(selectors):
        raise RuntimeError("profile units or exact selector ALO differ")
    if len(set(selectors)) != 10 or selectors != list(range(BASE_VARIABLES + 1, BASE_VARIABLES + 11)):
        raise RuntimeError("selector variables are not the exact canonical fresh block")
    projections = clauses[base_count + 18:]
    if len(projections) != len(parents) * len(PAIRS):
        raise RuntimeError("guarded projection clause count differs")
    for parent_index, (selector, (_, _, row)) in enumerate(zip(selectors, parents)):
        holes = frozenset(expected_projection(row)[1])
        expected = [(-selector, name_to_number[f"h_{u}_{v}"] if (u, v) in holes else
                     -name_to_number[f"h_{u}_{v}"]) for u, v in PAIRS]
        block = projections[parent_index * len(PAIRS):(parent_index + 1) * len(PAIRS)]
        if block != expected:
            raise RuntimeError(f"guarded parent projection differs: parent={parent_index}")


def check(path):
    parents, manifest = check_manifest()
    hashes = load_hashes()
    metadata, variables, clauses, declared = parse_cnf(path)
    try:
        t = int(dict(metadata).get("intersection-t", "-1"))
    except ValueError as error:
        raise RuntimeError("invalid intersection orbit") from error
    if t not in (0, 1):
        raise RuntimeError("intersection orbit outside t=0,1")
    names, expected_clauses, selectors = reconstruct(t, parents)
    validate_clause_families(t, names, expected_clauses, selectors, parents)
    if metadata != expected_metadata(t, manifest, parents, selectors) or variables != names or \
            clauses != expected_clauses or declared != dimensions():
        raise RuntimeError("CNF differs from independent exact reconstruction")
    if identity(path) != hashes[t]:
        raise RuntimeError("CNF identity differs from strict hash ledger")
    print(f"PASS t={t} parents=10 vars={declared[0]} clauses={declared[1]} sha256={hashes[t][1]}")


def check_exhaustion():
    all_parents, parents = derive()
    manifest = manifest_payload(all_parents, parents)
    if MANIFEST.read_bytes() != manifest:
        raise RuntimeError("frozen manifest mismatch")
    load_hashes()
    orbits = derive_ordered_subset_orbits()
    print(f"PASS exhaustion committed={len(all_parents)} compatible={len(parents)} excluded={len(all_parents)-len(parents)} "
          f"permutations=5040 ordered_pairs=245 orbit_sizes={','.join(str(len(orbit)) for _, orbit in orbits)} "
          f"member_sha256={hashlib.sha256(member_payload(parents)).hexdigest()}")


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
