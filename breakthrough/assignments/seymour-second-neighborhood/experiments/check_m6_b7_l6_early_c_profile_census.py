#!/usr/bin/env python3
"""Independently check the authoritative frozen 60-orbit C-profile census."""

import argparse
import ast
import hashlib
import itertools
import json
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
PREFIX = "m6-b7-l6-early-c-profile"
FORMAT = f"{PREFIX}-cnf-v1"
MANIFEST_FORMAT = f"{PREFIX}-census-v1"
HASH_FORMAT = f"{PREFIX}-hashes-v1"
MANIFEST = HERE / f"{PREFIX}-census.tsv"
HASHES = HERE / f"{PREFIX}-hashes.tsv"
SCOUT = HERE / f"{PREFIX}-scout.json"
PROVENANCE = HERE / f"{PREFIX}-provenance.tsv"
PROVENANCE_FORMAT = f"{PREFIX}-provenance-v1"
PROVENANCE_CANONICAL_SHA256 = "b7a42034ec5bfeb5c0a0bf7769c867bcbccb7dcf13d77cc27b78431eb1706f46"
B = tuple(range(9, 16))
C = (16, 17)
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
def independent_s7_orbits(left_size, right_size):
    universe = {(frozenset(left), frozenset(right))
                for left in itertools.combinations(B, left_size)
                for right in itertools.combinations(B, right_size)}
    unseen, result = set(universe), []
    while unseen:
        seed = min(unseen, key=lambda x: (len(x[0] & x[1]), tuple(sorted(x[0])), tuple(sorted(x[1]))))
        orbit = set()
        for image in itertools.permutations(B):
            mapping = dict(zip(B, image))
            orbit.add((frozenset(mapping[x] for x in seed[0]), frozenset(mapping[x] for x in seed[1])))
        if not orbit <= unseen:
            raise RuntimeError("independent S7 orbits overlap")
        unseen.difference_update(orbit)
        result.append((len(seed[0] & seed[1]), len(orbit)))
    result.sort()
    expected_t = list(range(max(0, left_size + right_size - 7), min(left_size, right_size) + 1))
    if [x[0] for x in result] != expected_t:
        raise RuntimeError("independent S7 intersection census differs")
    return tuple(result)


def permute_holes(holes, mapping):
    return frozenset(tuple(sorted((mapping.get(u, u), mapping.get(v, v)))) for u, v in holes)


def check_parent_support_closure(members, permutations=None, supports_override=None):
    supports = ({frozenset(expected_projection(row)[1]) for _, _, row in members}
                if supports_override is None else set(supports_override))
    if supports_override is None and len(supports) != len(members):
        raise RuntimeError("parent-support disjunction contains duplicate supports")
    permutations = itertools.permutations(B) if permutations is None else permutations
    count = 0
    for image in permutations:
        count += 1
        mapping = dict(zip(B, image))
        if {permute_holes(support, mapping) for support in supports} != supports:
            raise RuntimeError("parent-support disjunction is not closed under an S7 permutation")
    if count != 5040:
        raise RuntimeError("parent-support closure did not exhaust S7")


@lru_cache(maxsize=1)
def derive():
    for name, path in SOURCE_PATHS.items():
        if identity(path) != SOURCE_IDENTITIES[name]:
            raise RuntimeError(f"strict source binding changed: {name}")
    groups = clean.derive_groups(HERE / "m6-clean-sink-remaining.tsv",
                                 HERE / "m6-placement-cover.txt", HERE / "m6-placement-filter.txt")
    parents = tuple(groups["B7-l6"])
    cells = defaultdict(list)
    for member in parents:
        for state in independent_states(member[2]):
            cells[state].append(member)
    source_states = [(state_key(state), state, cells[state]) for state in sorted(cells)]
    if len(parents) != 42 or len(source_states) != 30 or sum(len(x[2]) for x in source_states) != 260:
        raise RuntimeError("independent 42/30/260 census differs")
    ordered = sorted(enumerate(source_states), key=lambda x: (x[1][1][1], x[1][1][2], x[1][1][3], x[1][1][0]))
    orbits = []
    for state_ordinal, (key, state, members) in ordered:
        check_parent_support_closure(members)
        p, q = state[3]
        for intersection, orbit_size in independent_s7_orbits(p, q):
            ordinal = len(orbits)
            orbits.append((f"o{ordinal:02d}", state_ordinal, key, state, intersection,
                           representative(p, q, intersection), orbit_size, members))
    if len(orbits) != 60 or sum(len(x[7]) for x in orbits) != 544:
        raise RuntimeError("independent 60/544 orbit census differs")
    if [(orbits[i][3][3], orbits[i][4]) for i in (34, 35)] != [((3, 1), 0), ((3, 1), 1)]:
        raise RuntimeError("certified orbit mapping differs")
    return orbits


def member_payload(members):
    lines = ["columns\tselector-ordinal,accepted-ordinal,cover-index"]
    lines.extend(f"{i:02d}\t{accepted:05d}\t{cover:06d}" for i, (accepted, cover, _) in enumerate(members))
    return ("\n".join(lines) + "\n").encode("ascii")


def dimensions(count):
    return BASE_VARIABLES + count, BASE_CLAUSES["B7"] + 18 + 153 * count


def manifest_payload(orbits):
    sequence = independent_scout_sequence(orbits)
    scout_status = {ordinal: f"SCOUT-{status}" for ordinal, status, _, _ in sequence}
    sequence_payload = scout_sequence_payload(sequence)
    lines = [MANIFEST_FORMAT]
    for name, item in SOURCE_IDENTITIES.items():
        lines.extend((f"{name}-bytes\t{item[0]}", f"{name}-sha256\t{item[1]}"))
    lines.extend(("states\t30", "state-parent-incidences\t260", "distinct-parents\t42", "orbits\t60",
                  "orbit-parent-incidences\t544", "S7-permutations\t5040", "certified-orbits\t34,35",
                   "SCOUT-UNSAT-orbits\t31", "SCOUT-TIMEOUT-orbits\t27", "SCOUT-SAT-orbits\t0",
                  "total-eliminated-including-certified\t33",
                  f"scout-status-sequence-sha256\t{hashlib.sha256(sequence_payload).hexdigest()}",
                   "certified-profile-map\t34:t0,35:t1",
                   "certified-serialization-equivalence\tidentical numbered variable map and DIMACS clause stream; census comments intentionally differ",
                  "certified-source-cnf-sha256\t0c06a73c9308bae4eee1b309362485d24ed6508c7de8e64bf87c647805048b5f,d6bc88cf265db8aaaf5ff6f93160c0ca24bb7c1ba9341ad5704c9f29795eae2a",
                  "uncertified-orbit-31\tyes",
                  "ordering\tinternal-C,high-mask,(cb16,cb17),(h16,h17),intersection-t",
                  "columns\torbit,key,state-ordinal,state-key,h16,h17,internal,high-mask,cb16,cb17,t,S7-orbit-size,parents,variables,clauses,status,member-sha256"))
    for ordinal, orbit in enumerate(orbits):
        key, state_ordinal, state_key_value, state, intersection, _, orbit_size, members = orbit
        hvec, internal, high, cb = state
        variables, clauses = dimensions(len(members))
        status = "CERTIFIED" if ordinal in (34, 35) else scout_status[ordinal]
        lines.append(f"{ordinal:02d}\t{key}\t{state_ordinal:02d}\t{state_key_value}\t{hvec[0]}\t{hvec[1]}\t"
                     f"{internal}\t{high[0]}{high[1]}\t{cb[0]}\t{cb[1]}\t{intersection}\t{orbit_size}\t"
                     f"{len(members)}\t{variables}\t{clauses}\t{status}\t"
                     f"{hashlib.sha256(member_payload(members)).hexdigest()}")
    return ("\n".join(lines) + "\n").encode("ascii")


def scout_sequence_payload(sequence):
    return ("\n".join(f"{ordinal:02d}\t{status}\t{source}\t{digest}"
                      for ordinal, status, source, digest in sequence) + "\n").encode("ascii")


def independent_scout_sequence(orbits):
    state = json.loads(SOURCE_PATHS["state-scout"].read_text(encoding="ascii"))
    hard = json.loads(SOURCE_PATHS["hard-orbit-scout"].read_text(encoding="ascii"))
    if state.get("schema") != "m6-b7-l6-state-scout-v1" or \
            state.get("manifest_sha256") != SOURCE_IDENTITIES["state-manifest"][1] or \
            hard.get("schema") != "m6-b7-l6-hard-orbit-scout-v1" or \
            hard.get("manifest_sha256") != SOURCE_IDENTITIES["hard-orbit-manifest"][1] or \
            state.get("seconds_per_leaf") != 30 or hard.get("seconds_per_leaf") != 20 or \
            not state.get("solver_sha256") or not hard.get("solver_sha256"):
        raise RuntimeError("independent scout provenance validation failed")
    state_rows = {row["leaf"]: row for row in state["rows"]}
    hard_rows = {(row["state_leaf"], row["intersection_t"]): row for row in hard["rows"]}
    if set(state_rows) != set(range(30)) or len(hard_rows) != 42:
        raise RuntimeError("source scout row exhaustion differs")
    result = []
    for ordinal, orbit in enumerate(orbits):
        if ordinal in (34, 35):
            continue
        state_row = state_rows[orbit[1]]
        if state_row["status"] == "UNSAT":
            if state_row["seconds"] >= 20:
                raise RuntimeError("state result was not observed inside the 20-second envelope")
            row, source = state_row, "state-scout-observed-within-20s"
        else:
            row, source = hard_rows[(orbit[1], orbit[4])], "hard-orbit-scout-20s"
        result.append((ordinal, row["status"], source, row["cnf_sha256"]))
    statuses = [item[1] for item in result]
    if len(result) != 58 or statuses.count("UNSAT") != 31 or statuses.count("TIMEOUT") != 27 or \
            set(statuses) != {"UNSAT", "TIMEOUT"}:
        raise RuntimeError("independent scout sequence totals differ")
    return tuple(result)


def check_scout(orbits, manifest):
    sequence = independent_scout_sequence(orbits)
    data = json.loads(SCOUT.read_text(encoding="ascii"))
    rows = data.get("rows", [])
    observed = tuple((row.get("orbit"), row.get("status"), row.get("source"),
                      row.get("source_cnf_sha256")) for row in rows)
    expected_header = {
        "schema": "m6-b7-l6-early-c-profile-scout-v1",
        "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
        "excluded_certified_orbits": [34, 35], "orbit_31_certified": False,
        "seconds_per_orbit": 20, "scout_unsat": 31, "scout_timeout": 27, "scout_sat": 0,
        "total_eliminated_including_certified": 33,
        "status_sequence_sha256": hashlib.sha256(scout_sequence_payload(sequence)).hexdigest(),
        "state_scout_bytes": SOURCE_IDENTITIES["state-scout"][0],
        "state_scout_sha256": SOURCE_IDENTITIES["state-scout"][1],
        "hard_scout_bytes": SOURCE_IDENTITIES["hard-orbit-scout"][0],
        "hard_scout_sha256": SOURCE_IDENTITIES["hard-orbit-scout"][1],
    }
    expected_row_keys = {"orbit", "key", "state", "state_key", "intersection_t", "parents",
                         "status", "source", "source_cnf_sha256"}
    for row, orbit in zip(rows, (orbit for i, orbit in enumerate(orbits) if i not in (34, 35))):
        if set(row) != expected_row_keys or row["key"] != orbit[0] or row["state"] != orbit[1] or \
                row["state_key"] != orbit[2] or row["intersection_t"] != orbit[4] or \
                row["parents"] != len(orbit[7]):
            raise RuntimeError("scout row structure differs from independent orbit census")
    canonical = (json.dumps(data, sort_keys=True, indent=2) + "\n").encode("ascii")
    if SCOUT.read_bytes() != canonical or observed != sequence or \
            any(data.get(key) != value for key, value in expected_header.items()):
        raise RuntimeError("scout artifact differs from independent provenance/status sequence")


def load_hashes(manifest, path=HASHES):
    lines = path.read_text(encoding="ascii").splitlines()
    expected = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
                f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}", "orbits\t60",
                "columns\torbit,key,parents,variables,clauses,cnf-bytes,cnf-sha256"]
    if lines[:5] != expected or len(lines) != 65 or path.read_bytes() != ("\n".join(lines) + "\n").encode("ascii"):
        raise RuntimeError("hash ledger framing differs")
    result = []
    for ordinal, line in enumerate(lines[5:]):
        fields = line.split("\t")
        if len(fields) != 7 or fields[0] != f"{ordinal:02d}" or not fields[5].isdigit() or \
                re.fullmatch(r"[0-9a-f]{64}", fields[6]) is None:
            raise RuntimeError("malformed orbit hash row")
        result.append((int(fields[5]), fields[6]))
    return tuple(result)


def reconstruct(orbit):
    _, _, _, state, _, subsets, _, members = orbit
    cnf = generate(18, 7, 6, robust_witness=True, arc_minimal=True)
    if len(cnf.names) != BASE_VARIABLES or variable_map_sha256(tuple(cnf.names)) != BASE_VARIABLE_MAP_SHA256 or \
            len(cnf.clauses) != BASE_CLAUSES["B7"] or clause_sha256(tuple(cnf.clauses)) != BASE_CLAUSE_SHA256["B7"]:
        raise RuntimeError("independent B7 base differs")
    _, internal, high, _ = state
    cnf.add(cnf.names[{"h": "h_16_17", "16>17": "a_16_17", "17>16": "a_17_16"}[internal]])
    for c, bit in zip(C, high):
        number = cnf.names[f"cnt_d1_{c}_17_9"]
        cnf.add(number if bit else -number)
    for c, subset in zip(C, subsets):
        for b in B:
            number = cnf.names[f"a_{c}_{b}"]
            cnf.add(number if b in subset else -number)
    selectors = [cnf.var(f"early_c_profile_parent_{i:02d}") for i in range(len(members))]
    cnf.add(*selectors)
    for selector, (_, _, row) in zip(selectors, members):
        holes = frozenset(expected_projection(row)[1])
        for u, v in PAIRS:
            number = cnf.names[f"h_{u}_{v}"]
            cnf.add(-selector, number if (u, v) in holes else -number)
    return list(cnf.names), list(cnf.clauses), selectors


def expected_metadata(ordinal, orbit, manifest, selectors):
    key, state_ordinal, state_key_value, state, intersection, subsets, orbit_size, members = orbit
    hvec, internal, high, cb = state
    return [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT), ("manifest-bytes", str(len(manifest))),
            ("manifest-sha256", hashlib.sha256(manifest).hexdigest()), ("orbit", str(ordinal)),
            ("orbit-key", key), ("state-ordinal", str(state_ordinal)), ("state-key", state_key_value),
            ("h-vector", f"{hvec[0]},{hvec[1]}"), ("internal-C", internal),
            ("high-mask", f"{high[0]}{high[1]}"), ("C-row-sizes", f"{cb[0]},{cb[1]}"),
            ("intersection-t", str(intersection)), ("S7-orbit-size", str(orbit_size)),
            ("parents", str(len(members))), ("member-sha256", hashlib.sha256(member_payload(members)).hexdigest()),
            ("C16-subset", ",".join(map(str, sorted(subsets[0])))),
            ("C17-subset", ",".join(map(str, sorted(subsets[1])))), ("state-unit-clauses", "3"),
            ("C-B-unit-clauses", "14"), ("alo-clauses", "1"),
            ("guarded-hole-clauses-per-parent", "153"), ("first-selector", str(selectors[0])),
             ("last-selector", str(selectors[-1]))]


def write_reconstruction(path, ordinal, orbit, manifest):
    names, clauses, selectors = reconstruct(orbit)
    metadata = expected_metadata(ordinal, orbit, manifest, selectors)
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in metadata:
            handle.write(f"c {name} {value}\n")
        for number, name in enumerate(names, 1):
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(names)} {len(clauses)}\n")
        for clause in clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def runtime_source_closure():
    roots = (HERE / "m6_b7_l6_early_c_profile_census.py", Path(__file__).resolve(),
             HERE / "test_m6_b7_l6_early_c_profile_census.py",
             HERE / "m6_b7_l6_early_c_profile_scout.py")
    local_modules = {path.stem: path.resolve() for path in HERE.glob("*.py")}
    pending, visited = list(roots), set()
    while pending:
        path = pending.pop()
        if path in visited:
            continue
        visited.add(path)
        tree = ast.parse(path.read_text(encoding="ascii"), filename=str(path))
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                imports.append(node.module.split(".", 1)[0])
        pending.extend(local_modules[name] for name in imports if name in local_modules)
    return tuple(sorted(visited))


def canonical_checker_hash():
    data = Path(__file__).read_bytes()
    marker = f'PROVENANCE_CANONICAL_SHA256 = "{PROVENANCE_CANONICAL_SHA256}"'.encode("ascii")
    token = b'PROVENANCE_CANONICAL_SHA256 = "' + b"0" * 64 + b'"'
    if data.count(marker) != 1:
        raise RuntimeError("checker provenance self-pin marker changed")
    return hashlib.sha256(data.replace(marker, token)).hexdigest()


def canonical_provenance_hash(data):
    lines = data.splitlines(keepends=True)
    matches = [i for i, line in enumerate(lines) if line.startswith(b"checker\t")]
    if len(matches) != 1:
        raise RuntimeError("provenance checker row changed")
    fields = lines[matches[0]].rstrip(b"\n").split(b"\t")
    if len(fields) != 4:
        raise RuntimeError("provenance checker row malformed")
    fields[3] = b"0" * 64
    lines[matches[0]] = b"\t".join(fields) + b"\n"
    return hashlib.sha256(b"".join(lines)).hexdigest()


def check_provenance():
    data = PROVENANCE.read_bytes()
    lines = data.decode("ascii").splitlines()
    if not lines or lines[0] != PROVENANCE_FORMAT or lines[1] != "columns\trole,path,bytes,sha256" or \
            data != ("\n".join(lines) + "\n").encode("ascii"):
        raise RuntimeError("provenance ledger framing differs")
    rows = {}
    for line in lines[2:]:
        fields = line.split("\t")
        if len(fields) != 4 or fields[1] in rows or not fields[2].isdigit() or \
                re.fullmatch(r"[0-9a-f]{64}", fields[3]) is None:
            raise RuntimeError("provenance ledger row malformed")
        rows[fields[1]] = fields
    expected_paths = {str(path.relative_to(HERE.parent)) for path in runtime_source_closure()}
    expected_paths.update({
        "experiments/m6-b7-l6-early-c-profile-census.tsv",
        "experiments/m6-b7-l6-early-c-profile-hashes.tsv",
        "experiments/m6-b7-l6-early-c-profile-scout.json",
        "attempts/frozen-b7-l6-early-c-profile-census.md", "experiments/README.md", "notebook.md",
    })
    if set(rows) != expected_paths:
        raise RuntimeError("provenance ledger does not equal the transitive runtime/artifact closure")
    checker_key = str(Path(__file__).resolve().relative_to(HERE.parent))
    for relative, fields in rows.items():
        path = HERE.parent / relative
        size, digest = identity(path)
        expected_digest = canonical_checker_hash() if relative == checker_key else digest
        if int(fields[2]) != size or fields[3] != expected_digest:
            raise RuntimeError(f"bound provenance source changed: {relative}")
    if canonical_provenance_hash(data) != PROVENANCE_CANONICAL_SHA256:
        raise RuntimeError("checker does not pin the canonical provenance ledger")


def check(path):
    orbits = derive()
    manifest = manifest_payload(orbits)
    if MANIFEST.read_bytes() != manifest:
        raise RuntimeError("manifest differs from independent census")
    hashes = load_hashes(manifest)
    metadata, variables, clauses, declared = parse_cnf(path)
    ordinal = int(dict(metadata).get("orbit", "-1"))
    if not 0 <= ordinal < 60:
        raise RuntimeError("orbit outside 0..59")
    names, expected_clauses, selectors = reconstruct(orbits[ordinal])
    if metadata != expected_metadata(ordinal, orbits[ordinal], manifest, selectors) or variables != names or \
            clauses != expected_clauses or declared != dimensions(len(orbits[ordinal][7])):
        raise RuntimeError("CNF differs from independent reconstruction")
    if identity(path) != hashes[ordinal]:
        raise RuntimeError("CNF identity differs from hash ledger")
    print(f"PASS orbit={ordinal:02d} parents={len(orbits[ordinal][7])} sha256={hashes[ordinal][1]}")


def check_exhaustion():
    orbits = derive()
    manifest = manifest_payload(orbits)
    if MANIFEST.read_bytes() != manifest:
        raise RuntimeError("frozen manifest mismatch")
    hashes = load_hashes(manifest)
    check_scout(orbits, manifest)
    check_provenance()
    with tempfile.TemporaryDirectory(prefix="early-c-profile-check-", dir=HERE.parent) as directory:
        path = Path(directory) / "orbit.cnf"
        for ordinal, orbit in enumerate(orbits):
            write_reconstruction(path, ordinal, orbit, manifest)
            if identity(path) != hashes[ordinal]:
                raise RuntimeError(f"regenerated orbit {ordinal:02d} differs from hash ledger")
    print(f"PASS states=30 incidences=260 parents=42 orbits=60 orbit_incidences=544 "
          f"SCOUT-UNSAT=31 SCOUT-TIMEOUT=27 SCOUT-SAT=0 eliminated=33 CERTIFIED=34,35 "
          f"uncertified=31 manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


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
