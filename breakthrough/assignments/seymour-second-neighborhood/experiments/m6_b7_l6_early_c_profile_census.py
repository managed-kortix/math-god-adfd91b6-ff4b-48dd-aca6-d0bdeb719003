#!/usr/bin/env python3
"""Produce the authoritative early C-profile orbit census for frozen B7-l6."""

import argparse
import hashlib
import itertools
import json
import tempfile
from functools import lru_cache
from pathlib import Path

import m6_b7_l6_state_split as states

HERE = Path(__file__).resolve().parent
PREFIX = "m6-b7-l6-early-c-profile"
FORMAT = f"{PREFIX}-cnf-v1"
MANIFEST_FORMAT = f"{PREFIX}-census-v1"
HASH_FORMAT = f"{PREFIX}-hashes-v1"
B = tuple(range(9, 16))
ORBIT_COUNT = 60
STATE_COUNT = 30
STATE_INCIDENCES = 260
PARENT_COUNT = 42
ORBIT_INCIDENCES = 544
CERTIFIED = {34: 0, 35: 1}
SCOUT_UNSAT = 31
SCOUT_TIMEOUT = 27
TOTAL_ELIMINATED = len(CERTIFIED) + SCOUT_UNSAT
SOURCE_PATHS = {
    "state-manifest": HERE / "m6-b7-l6-state-split.tsv",
    "state-hashes": HERE / "m6-b7-l6-state-leaf-hashes.tsv",
    "state-scout": HERE / "m6-b7-l6-state-scout-30s.json",
    "hard-orbit-manifest": HERE / "m6-b7-l6-hard-orbits.tsv",
    "hard-orbit-scout": HERE / "m6-b7-l6-hard-orbit-scout-20s.json",
    "profile-manifest": HERE / "m6-b7-l6-c-to-b-31-orbits.tsv",
    "profile-hashes": HERE / "m6-b7-l6-c-to-b-31-orbits-hashes.tsv",
    "profile-certificates": HERE / "m6-b7-l6-c-to-b-31-orbit-certificates.tsv",
}
SOURCE_IDENTITIES = {
    "state-manifest": (4382, "a3b8f9d17b50dbfccd5f00740b33c6e90f6f10d26a3854dd627a45681e5c890e"),
    "state-hashes": (3163, "eec464838f7d01e6cf053c7cbf8fa1442068d78738f4bd2772b15a8417543ae4"),
    "state-scout": (6948, "69c1d56145ec2544702717b252bd1e3796c882c68ca95023488b959e2af2f763"),
    "hard-orbit-manifest": (5533, "6c1080c6f97f92e68a9de6bc762145ceac9086f0b87dc4aa4ed73a746861b2d4"),
    "hard-orbit-scout": (11413, "32fa8260e2efb3cc326bafc2ce2d375ec84bf77ebb2fb5f9efd96b5b995ef31a"),
    "profile-manifest": (1020, "9ca5f13d10b740a2c6caef730d272c4c407bc5c340bf9fda11b2668ad63389ae"),
    "profile-hashes": (397, "1d4a99023eab6a06ba85ac21e91b2e1af93454d016dc6463b6191d53df4f9305"),
    "profile-certificates": (3546, "8afc7a2261e76ff878506bec5ea498fafd5baf7e212c532086cf414ff94d2cea"),
}


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def verify_sources():
    for name, path in SOURCE_PATHS.items():
        expected = SOURCE_IDENTITIES[name]
        actual = identity(path)
        if expected[0] and actual[0] != expected[0]:
            raise RuntimeError(f"bound source size changed: {name}")
        if expected[1] and actual[1] != expected[1]:
            raise RuntimeError(f"bound source hash changed: {name}")


def representative(left_size, right_size, intersection):
    left = frozenset(B[:left_size])
    right = frozenset(B[:intersection] + B[left_size:left_size + right_size - intersection])
    if len(left) != left_size or len(right) != right_size or len(left & right) != intersection:
        raise RuntimeError("invalid canonical S7 representative")
    return left, right


@lru_cache(maxsize=None)
def derive_s7_orbits(left_size, right_size):
    universe = {(frozenset(left), frozenset(right))
                for left in itertools.combinations(B, left_size)
                for right in itertools.combinations(B, right_size)}
    permutations = tuple(dict(zip(B, image)) for image in itertools.permutations(B))
    result, covered = [], set()
    low, high = max(0, left_size + right_size - len(B)), min(left_size, right_size)
    for intersection in range(low, high + 1):
        seed = representative(left_size, right_size, intersection)
        orbit = {(frozenset(p[v] for v in seed[0]), frozenset(p[v] for v in seed[1]))
                 for p in permutations}
        if covered & orbit or not orbit <= universe:
            raise RuntimeError("S7 orbit overlap or escape")
        covered.update(orbit)
        result.append((intersection, seed, len(orbit)))
    if len(permutations) != 5040 or covered != universe:
        raise RuntimeError("S7 orbit exhaustion failed")
    return tuple(result)


def scout_sequence(orbits):
    state = json.loads(SOURCE_PATHS["state-scout"].read_text(encoding="ascii"))
    hard = json.loads(SOURCE_PATHS["hard-orbit-scout"].read_text(encoding="ascii"))
    if state.get("manifest_sha256") != SOURCE_IDENTITIES["state-manifest"][1] or \
            hard.get("manifest_sha256") != SOURCE_IDENTITIES["hard-orbit-manifest"][1]:
        raise RuntimeError("scout provenance manifest binding changed")
    if state.get("seconds_per_leaf") != 30 or hard.get("seconds_per_leaf") != 20 or \
            not state.get("solver_sha256") or not hard.get("solver_sha256"):
        raise RuntimeError("scout solver identity or timeout changed")
    state_rows = {row["leaf"]: row for row in state["rows"]}
    hard_rows = {(row["state_leaf"], row["intersection_t"]): row for row in hard["rows"]}
    result = []
    for ordinal, orbit in enumerate(orbits):
        if ordinal in CERTIFIED:
            continue
        state_row = state_rows[orbit[1]]
        if state_row["status"] == "UNSAT":
            if state_row["seconds"] >= 20:
                raise RuntimeError("projected state UNSAT was not observed within 20 seconds")
            row, source = state_row, "state-scout-observed-within-20s"
        else:
            row, source = hard_rows[(orbit[1], orbit[4])], "hard-orbit-scout-20s"
        if row["status"] not in ("UNSAT", "TIMEOUT"):
            raise RuntimeError("unexpected scout status")
        result.append((ordinal, row["status"], source, row["cnf_sha256"]))
    counts = {status: sum(item[1] == status for item in result) for status in ("UNSAT", "TIMEOUT")}
    if len(result) != 58 or counts != {"UNSAT": SCOUT_UNSAT, "TIMEOUT": SCOUT_TIMEOUT}:
        raise RuntimeError("58-orbit scout status census changed")
    return tuple(result)


def scout_sequence_payload(sequence):
    return ("\n".join(f"{ordinal:02d}\t{status}\t{source}\t{digest}"
                      for ordinal, status, source, digest in sequence) + "\n").encode("ascii")


def load_orbits():
    verify_sources()
    source_states = states.load_leaves()
    if len(source_states) != STATE_COUNT or sum(len(x[2]) for x in source_states) != STATE_INCIDENCES:
        raise RuntimeError("frozen state census changed")
    parents = {accepted for _, _, members in source_states for accepted, _, _ in members}
    if len(parents) != PARENT_COUNT:
        raise RuntimeError("frozen parent census changed")
    ordered_states = sorted(enumerate(source_states),
                            key=lambda item: (item[1][1][1], item[1][1][2],
                                              item[1][1][3], item[1][1][0]))
    orbits = []
    for state_ordinal, (state_key, state, members) in ordered_states:
        left_size, right_size = state[3]
        for intersection, subsets, orbit_size in derive_s7_orbits(left_size, right_size):
            ordinal = len(orbits)
            orbits.append((f"o{ordinal:02d}", state_ordinal, state_key, state,
                           intersection, subsets, orbit_size, members))
    if len(orbits) != ORBIT_COUNT or sum(len(x[7]) for x in orbits) != ORBIT_INCIDENCES:
        raise RuntimeError("60-orbit census totals changed")
    if [(orbits[i][3][3], orbits[i][4]) for i in CERTIFIED] != [((3, 1), 0), ((3, 1), 1)]:
        raise RuntimeError("certified (3,1) orbit ordinals changed")
    return orbits


def member_payload(members):
    lines = ["columns\tselector-ordinal,accepted-ordinal,cover-index"]
    lines.extend(f"{i:02d}\t{accepted:05d}\t{cover:06d}"
                 for i, (accepted, cover, _) in enumerate(members))
    return ("\n".join(lines) + "\n").encode("ascii")


def dimensions(count):
    return states.source.parent.BASE_VARIABLES + count, states.source.parent.BASE_CLAUSES["B7"] + 18 + 153 * count


def build_orbit(orbit):
    _, _, _, state, _, subsets, _, members = orbit
    cnf = states.source.parent.generate(18, 7, 6, robust_witness=True, arc_minimal=True)
    _, internal, high, _ = state
    cnf.add(cnf.names[{"h": "h_16_17", "16>17": "a_16_17", "17>16": "a_17_16"}[internal]])
    for c, bit in zip(states.C_VERTICES, high):
        number = cnf.names[f"cnt_d1_{c}_17_9"]
        cnf.add(number if bit else -number)
    for c, subset in zip(states.C_VERTICES, subsets):
        for b in B:
            number = cnf.names[f"a_{c}_{b}"]
            cnf.add(number if b in subset else -number)
    selectors = [cnf.var(f"early_c_profile_parent_{i:02d}") for i in range(len(members))]
    cnf.add(*selectors)
    for selector, (_, _, row) in zip(selectors, members):
        holes = states.source.parent.embedded_holes(row["branch"], row["word"], row["edges"])[1]
        for pair in states.source.parent.PAIRS:
            number = cnf.names[f"h_{pair[0]}_{pair[1]}"]
            cnf.add(-selector, number if pair in holes else -number)
    return cnf, selectors


def manifest_payload(orbits):
    sequence = scout_sequence(orbits)
    scout_status = {ordinal: f"SCOUT-{status}" for ordinal, status, _, _ in sequence}
    sequence_payload = scout_sequence_payload(sequence)
    lines = [MANIFEST_FORMAT]
    for name in SOURCE_PATHS:
        size, digest = identity(SOURCE_PATHS[name])
        lines.extend((f"{name}-bytes\t{size}", f"{name}-sha256\t{digest}"))
    lines.extend((f"states\t{STATE_COUNT}", f"state-parent-incidences\t{STATE_INCIDENCES}",
                   f"distinct-parents\t{PARENT_COUNT}", f"orbits\t{ORBIT_COUNT}",
                   f"orbit-parent-incidences\t{ORBIT_INCIDENCES}", "S7-permutations\t5040",
                    "certified-orbits\t34,35", f"SCOUT-UNSAT-orbits\t{SCOUT_UNSAT}",
                    f"SCOUT-TIMEOUT-orbits\t{SCOUT_TIMEOUT}", "SCOUT-SAT-orbits\t0",
                   f"total-eliminated-including-certified\t{TOTAL_ELIMINATED}",
                   f"scout-status-sequence-sha256\t{hashlib.sha256(sequence_payload).hexdigest()}",
                    "certified-profile-map\t34:t0,35:t1",
                    "certified-serialization-equivalence\tidentical numbered variable map and DIMACS clause stream; census comments intentionally differ",
                   "certified-source-cnf-sha256\t0c06a73c9308bae4eee1b309362485d24ed6508c7de8e64bf87c647805048b5f,d6bc88cf265db8aaaf5ff6f93160c0ca24bb7c1ba9341ad5704c9f29795eae2a",
                   "uncertified-orbit-31\tyes",
                  "ordering\tinternal-C,high-mask,(cb16,cb17),(h16,h17),intersection-t",
                  "columns\torbit,key,state-ordinal,state-key,h16,h17,internal,high-mask,cb16,cb17,t,S7-orbit-size,parents,variables,clauses,status,member-sha256"))
    for ordinal, orbit in enumerate(orbits):
        key, state_ordinal, state_key, state, intersection, _, orbit_size, members = orbit
        hvec, internal, high, cb = state
        variables, clauses = dimensions(len(members))
        status = "CERTIFIED" if ordinal in CERTIFIED else scout_status[ordinal]
        lines.append(f"{ordinal:02d}\t{key}\t{state_ordinal:02d}\t{state_key}\t{hvec[0]}\t{hvec[1]}\t"
                     f"{internal}\t{high[0]}{high[1]}\t{cb[0]}\t{cb[1]}\t{intersection}\t{orbit_size}\t"
                     f"{len(members)}\t{variables}\t{clauses}\t{status}\t"
                     f"{hashlib.sha256(member_payload(members)).hexdigest()}")
    return ("\n".join(lines) + "\n").encode("ascii")


def write_orbit(path, ordinal, orbit, cnf, selectors, manifest):
    key, state_ordinal, state_key, state, intersection, subsets, orbit_size, members = orbit
    hvec, internal, high, cb = state
    metadata = [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
                ("manifest-bytes", str(len(manifest))),
                ("manifest-sha256", hashlib.sha256(manifest).hexdigest()),
                ("orbit", str(ordinal)), ("orbit-key", key), ("state-ordinal", str(state_ordinal)),
                ("state-key", state_key), ("h-vector", f"{hvec[0]},{hvec[1]}"),
                ("internal-C", internal), ("high-mask", f"{high[0]}{high[1]}"),
                ("C-row-sizes", f"{cb[0]},{cb[1]}"), ("intersection-t", str(intersection)),
                ("S7-orbit-size", str(orbit_size)), ("parents", str(len(members))),
                ("member-sha256", hashlib.sha256(member_payload(members)).hexdigest()),
                ("C16-subset", ",".join(map(str, sorted(subsets[0])))),
                ("C17-subset", ",".join(map(str, sorted(subsets[1])))),
                ("state-unit-clauses", "3"), ("C-B-unit-clauses", "14"),
                ("alo-clauses", "1"), ("guarded-hole-clauses-per-parent", "153"),
                ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1]))]
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in metadata:
            handle.write(f"c {name} {value}\n")
        for name, number in cnf.names.items():
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(cnf.names)} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def hash_payload(orbits, manifest, identities):
    lines = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
             f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}", f"orbits\t{ORBIT_COUNT}",
             "columns\torbit,key,parents,variables,clauses,cnf-bytes,cnf-sha256"]
    for ordinal, orbit in enumerate(orbits):
        size, digest = identities.get(ordinal, ("", ""))
        variables, clauses = dimensions(len(orbit[7]))
        lines.append(f"{ordinal:02d}\t{orbit[0]}\t{len(orbit[7])}\t{variables}\t{clauses}\t{size}\t{digest}")
    return ("\n".join(lines) + "\n").encode("ascii")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--orbit", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--hash-output", type=Path)
    parser.add_argument("--populate-hashes", action="store_true")
    args = parser.parse_args()
    orbits = load_orbits()
    manifest = manifest_payload(orbits)
    if args.manifest_output:
        args.manifest_output.write_bytes(manifest)
    identities = {}
    if args.populate_hashes:
        with tempfile.TemporaryDirectory(prefix="early-c-profile-", dir=HERE.parent) as directory:
            for ordinal, orbit in enumerate(orbits):
                path = Path(directory) / "orbit.cnf"
                cnf, selectors = build_orbit(orbit)
                write_orbit(path, ordinal, orbit, cnf, selectors, manifest)
                identities[ordinal] = identity(path)
    if args.hash_output:
        args.hash_output.write_bytes(hash_payload(orbits, manifest, identities))
    if args.output:
        if args.orbit is None or not 0 <= args.orbit < ORBIT_COUNT:
            parser.error("--output requires --orbit in 0..59")
        cnf, selectors = build_orbit(orbits[args.orbit])
        write_orbit(args.output, args.orbit, orbits[args.orbit], cnf, selectors, manifest)
    print(f"PASS states=30 incidences=260 parents=42 orbits=60 orbit_incidences=544 "
          f"manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


if __name__ == "__main__":
    main()
