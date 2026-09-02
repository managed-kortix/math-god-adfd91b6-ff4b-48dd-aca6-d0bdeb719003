#!/usr/bin/env python3
"""Emit the clean B7-l4 40-profile root-cardinality campaign."""

import argparse
import hashlib
import itertools
import tempfile
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

import m6_clean_sink_group_cnf as source
from snc_cnf import threshold

HERE = Path(__file__).resolve().parent
PREFIX = "m6-b7-l4-profile-root-cardinality"
FORMAT = f"{PREFIX}-cnf-v1"
MANIFEST_FORMAT = f"{PREFIX}-manifest-v1"
HASH_FORMAT = f"{PREFIX}-hashes-v1"
GROUP = "B7-l4"
A = tuple(range(1, 9))
B = tuple(range(9, 16))
C = (16, 17)
PROFILE_COUNT = 40
PARENT_COUNT = 1649
STATE_COUNT = 28
STATE_INCIDENCES = 10036
PROFILE_INCIDENCES = 14464
SOURCE_PATHS = {
    "clean-parent-manifest": HERE / "m6-clean-sink-selector-groups.tsv",
    "clean-remaining-stream": HERE / "m6-clean-sink-remaining.tsv",
    "clean-partition-manifest": HERE / "m6-clean-sink-manifest.tsv",
}
SOURCE_IDENTITIES = {
    "clean-parent-manifest": (1838, "6e7eee0ddd5b4c7ef02cdf459c9a0647f720513e7ee4987a3a8b0c17af37eeda"),
    "clean-remaining-stream": (2262190, "416b7e51a73637784342a374be8e15a1a58032b61fc1140f39f0768d1ff4b642"),
    "clean-partition-manifest": (2104, "733e06c8aa9881e0006409efff23729f1bf88d8af7b1a70e8a78fd3775b53217"),
}


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def state_key(state):
    hvec, internal, high, cb = state
    code = {"h": "h", "16>17": "f", "17>16": "r"}[internal]
    return f"h{hvec[0]}{hvec[1]}-c{code}-m{high[0]}{high[1]}-b{cb[0]}{cb[1]}"


def parent_states(row):
    labels = source.parent.CELL_LABELS["B7"]
    holes = source.parent.embedded_holes(row["branch"], row["word"], row["edges"])[1]
    colors = {vertex: cell for vertices, cell in zip(labels, "RABC") for vertex in vertices}
    hvec = tuple(sum(tuple(sorted((c, v))) in holes for v in range(18) if colors[v] in "RA") for c in C)
    internal_options = ("h",) if C in holes else ("16>17", "17>16")
    result = []
    for internal in internal_options:
        internal_out = {"h": (0, 0), "16>17": (1, 0), "17>16": (0, 1)}[internal]
        for high in itertools.product((0, 1), repeat=2):
            cb = []
            for index, c in enumerate(C):
                forced = sum(colors[v] in "RA" and tuple(sorted((c, v))) not in holes for v in range(18))
                available = sum(colors[v] == "B" and tuple(sorted((c, v))) not in holes for v in range(18))
                value = 8 + high[index] - forced - internal_out[index]
                if not 0 <= value <= available:
                    break
                cb.append(value)
            if len(cb) == 2 and not any(high[i] and not internal_out[i] and cb[i] == 0 for i in range(2)):
                result.append((hvec, internal, high, tuple(cb)))
    return result


def representative(left_size, right_size, intersection):
    left = frozenset(B[:left_size])
    right = frozenset(B[:intersection] + B[left_size:left_size + right_size - intersection])
    return left, right


@lru_cache(maxsize=None)
def orbit_sizes(left_size, right_size):
    result = []
    for intersection in range(max(0, left_size + right_size - 7), min(left_size, right_size) + 1):
        left, right = representative(left_size, right_size, intersection)
        images = set()
        for image in itertools.permutations(B):
            mapping = dict(zip(B, image))
            images.add((frozenset(mapping[v] for v in left), frozenset(mapping[v] for v in right)))
        result.append((intersection, (left, right), len(images)))
    return tuple(result)


def load_profiles():
    for name, path in SOURCE_PATHS.items():
        if identity(path) != SOURCE_IDENTITIES[name]:
            raise RuntimeError(f"frozen source identity changed: {name}")
    parents = source.load_groups()[GROUP]
    cells = defaultdict(list)
    for member in parents:
        for state in parent_states(member[2]):
            cells[state].append(member)
    states = [(state_key(state), state, cells[state]) for state in sorted(cells)]
    ordered = sorted(enumerate(states), key=lambda item: (item[1][1][1], item[1][1][2],
                                                           item[1][1][3], item[1][1][0]))
    profiles = []
    for state_ordinal, (key, state, members) in ordered:
        for intersection, subsets, size in orbit_sizes(*state[3]):
            ordinal = len(profiles)
            profiles.append((f"p{ordinal:02d}", state_ordinal, key, state, intersection,
                             subsets, size, members))
    if len(parents) != PARENT_COUNT or len(states) != STATE_COUNT or \
            sum(len(item[2]) for item in states) != STATE_INCIDENCES or \
            len(profiles) != PROFILE_COUNT or sum(len(item[7]) for item in profiles) != PROFILE_INCIDENCES:
        raise RuntimeError("frozen B7-l4 1649/28/10036/40/14464 census changed")
    return profiles


def member_payload(members):
    lines = ["columns\tselector-ordinal,accepted-ordinal,cover-index"]
    lines.extend(f"{i:03d}\t{accepted:05d}\t{cover:06d}" for i, (accepted, cover, _) in enumerate(members))
    return ("\n".join(lines) + "\n").encode("ascii")


def extend(cnf):
    before = len(cnf.names), len(cnf.clauses)
    high_all = tuple(cnf.names[f"cnt_d1_{v}_17_9"] for v in range(18))
    edges = tuple(cnf.names[f"a_{a}_{b}"] for a in A for b in B)
    holes = tuple(cnf.names[f"h_{a}_{b}"] for i, a in enumerate(A) for b in A[i + 1:])
    high_a = tuple(cnf.names[f"cnt_d1_{a}_17_9"] for a in A)
    global_count = threshold(cnf, high_all, "b7_l4_root_global_high")
    edge_count = threshold(cnf, edges, "b7_l4_root_AB_edges")
    rhs_count = threshold(cnf, holes + high_a, "b7_l4_root_A_holes_high")
    cnf.add(global_count[2])
    cnf.add(-global_count[3])
    cnf.add(edge_count[35])
    for offset in range(1, len(rhs_count) + 1):
        if 36 + offset <= len(edge_count):
            cnf.add(-rhs_count[offset - 1], edge_count[35 + offset])
            cnf.add(rhs_count[offset - 1], -edge_count[35 + offset])
        else:
            cnf.add(-rhs_count[offset - 1])
    return len(cnf.names) - before[0], len(cnf.clauses) - before[1]


def build(profile):
    _, _, _, state, _, subsets, _, members = profile
    cnf = source.parent.generate(18, 7, 6, robust_witness=True, arc_minimal=True)
    _, internal, high, _ = state
    cnf.add(cnf.names[{"h": "h_16_17", "16>17": "a_16_17", "17>16": "a_17_16"}[internal]])
    for c, bit in zip(C, high):
        number = cnf.names[f"cnt_d1_{c}_17_9"]
        cnf.add(number if bit else -number)
    for c, subset in zip(C, subsets):
        for b in B:
            number = cnf.names[f"a_{c}_{b}"]
            cnf.add(number if b in subset else -number)
    selectors = [cnf.var(f"b7_l4_profile_parent_{i:03d}") for i in range(len(members))]
    cnf.add(*selectors)
    for selector, (_, _, row) in zip(selectors, members):
        holes = source.parent.embedded_holes(row["branch"], row["word"], row["edges"])[1]
        for u, v in source.parent.PAIRS:
            number = cnf.names[f"h_{u}_{v}"]
            cnf.add(-selector, number if (u, v) in holes else -number)
    delta = extend(cnf)
    if delta != (2433, 9571):
        raise RuntimeError("root-cardinality counter dimensions changed")
    return cnf, selectors, delta


def manifest_payload(profiles):
    lines = [MANIFEST_FORMAT]
    for name, item in SOURCE_IDENTITIES.items():
        lines.extend((f"{name}-bytes\t{item[0]}", f"{name}-sha256\t{item[1]}"))
    lines.extend((f"parent-group\t{GROUP}", f"parents\t{PARENT_COUNT}", f"states\t{STATE_COUNT}",
                  f"state-parent-incidences\t{STATE_INCIDENCES}", f"profiles\t{PROFILE_COUNT}",
                  f"profile-parent-incidences\t{PROFILE_INCIDENCES}", "S7-permutations\t5040",
                  "global-arcs\t147", "global-high\t3", "root-A\t1,2,3,4,5,6,7,8",
                  "root-B\t9,10,11,12,13,14,15", "root-identity\te(A,B)=36+H(A)+high(A)",
                  "added-variables\t2433", "added-clauses\t9571", "certificate-status\tnot-started",
                  "ordering\tinternal-C,high-mask,(cb16,cb17),(h16,h17),intersection-t",
                  "columns\tposition,key,state-ordinal,state-key,h16,h17,internal,high-mask,cb16,cb17,t,S7-orbit-size,parents,variables,clauses,member-sha256"))
    for position, profile in enumerate(profiles):
        key, state_ordinal, state_key_value, state, intersection, _, size, members = profile
        hvec, internal, high, cb = state
        cnf, _, _ = build(profile)
        lines.append(f"{position:02d}\t{key}\t{state_ordinal:02d}\t{state_key_value}\t{hvec[0]}\t{hvec[1]}\t"
                     f"{internal}\t{high[0]}{high[1]}\t{cb[0]}\t{cb[1]}\t{intersection}\t{size}\t"
                     f"{len(members)}\t{len(cnf.names)}\t{len(cnf.clauses)}\t"
                     f"{hashlib.sha256(member_payload(members)).hexdigest()}")
    return ("\n".join(lines) + "\n").encode("ascii")


def metadata(position, profile, manifest, selectors, delta):
    key, state_ordinal, state_key_value, state, intersection, subsets, size, members = profile
    hvec, internal, high, cb = state
    return [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT), ("manifest-bytes", str(len(manifest))),
            ("manifest-sha256", hashlib.sha256(manifest).hexdigest()), ("position", str(position)),
            ("key", key), ("state-ordinal", str(state_ordinal)), ("state-key", state_key_value),
            ("h-vector", f"{hvec[0]},{hvec[1]}"), ("internal-C", internal),
            ("high-mask", f"{high[0]}{high[1]}"), ("C-row-sizes", f"{cb[0]},{cb[1]}"),
            ("intersection-t", str(intersection)), ("S7-orbit-size", str(size)),
            ("C16-subset", ",".join(map(str, sorted(subsets[0])))),
            ("C17-subset", ",".join(map(str, sorted(subsets[1])))), ("parents", str(len(members))),
            ("member-sha256", hashlib.sha256(member_payload(members)).hexdigest()),
            ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1])),
            ("global-high", "3"), ("root-identity", "e(A,B)=36+H(A)+high(A)"),
            ("cardinality-added-variables", str(delta[0])), ("cardinality-added-clauses", str(delta[1])),
            ("certificate-status", "not-started")]


def write_cnf(path, position, profile, cnf, selectors, delta, manifest):
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in metadata(position, profile, manifest, selectors, delta):
            handle.write(f"c {name} {value}\n")
        for name, number in cnf.names.items():
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def hash_payload(profiles, manifest, identities=None):
    identities = identities or (("", ""),) * PROFILE_COUNT
    lines = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
             f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}", f"profiles\t{PROFILE_COUNT}",
             "columns\tposition,key,parents,variables,clauses,cnf-bytes,cnf-sha256"]
    for position, (profile, item) in enumerate(zip(profiles, identities)):
        cnf, _, _ = build(profile)
        lines.append(f"{position:02d}\t{profile[0]}\t{len(profile[7])}\t{len(cnf.names)}\t"
                     f"{len(cnf.clauses)}\t{item[0]}\t{item[1]}")
    return ("\n".join(lines) + "\n").encode("ascii")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--position", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--hash-output", type=Path)
    parser.add_argument("--populate-hashes", action="store_true")
    args = parser.parse_args()
    profiles = load_profiles()
    manifest = manifest_payload(profiles)
    if args.manifest_output:
        args.manifest_output.write_bytes(manifest)
    identities = None
    if args.populate_hashes:
        values = []
        with tempfile.TemporaryDirectory(prefix="b7-l4-root-hashes-", dir=HERE.parent) as directory:
            path = Path(directory) / "profile.cnf"
            for position, profile in enumerate(profiles):
                write_cnf(path, position, profile, *build(profile), manifest)
                values.append(identity(path))
        identities = tuple(values)
    if args.hash_output:
        args.hash_output.write_bytes(hash_payload(profiles, manifest, identities))
    if args.output:
        if args.position is None or not 0 <= args.position < PROFILE_COUNT:
            parser.error("--output requires --position in 0..52")
        write_cnf(args.output, args.position, profiles[args.position], *build(profiles[args.position]), manifest)
    print(f"PASS parents=1649 states=28 profiles=40 incidences=14464 manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


if __name__ == "__main__":
    main()
