#!/usr/bin/env python3
"""Independent checker for the frozen exact-pair Hall-failure extension."""

import argparse
from collections import Counter
import hashlib
import itertools
import json
import math
import re
import tempfile
from pathlib import Path

import check_m6_b7_l6_early_c_certificate_residual_exact_pair_singleton_parent as base
import check_m6_b7_l6_exact_pair_timeout_complete_cut as cut_checker
from check_m6_parent_cnf import parse_cnf

HERE = Path(__file__).resolve().parent
PREFIX = "m6-b7-l6-exact-pair-timeout-hall-failure"
FORMAT = f"{PREFIX}-cnf-v1"
MANIFEST_FORMAT = f"{PREFIX}-manifest-v1"
HASH_FORMAT = f"{PREFIX}-hashes-v1"
MEMBERSHIPS = 33
ADDED_VARIABLES = 142
ADDED_CLAUSES = 480
MANIFEST = HERE / f"{PREFIX}.tsv"
HASHES = HERE / f"{PREFIX}-hashes.tsv"
SCOUT = HERE / f"{PREFIX}-scout-180s.json"
SCOUT_SECONDS = 180
SCOUT_JOBS = 2
SOLVER = "/tmp/opencode/cadical-1.7.3/build/cadical"
SOLVER_IDENTITY = (1002216, "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292", "1.7.3")
DEFAULT_OPTIONS = ("--restart=false", "--phase=false", "--seed=3")
POSITION_OPTIONS = {10: ("--restart=false",)}
SCOUT_TOTALS = {"UNSAT": 29, "TIMEOUT": 4}
SCOUT_IDENTITY = (11240, "f2b1c935a985b3e73428e8c9b3b4e0c87264a519fe0bb6a421ffcd5a14dc7d93")
SCOUT_STATUS_SHA256 = "bce3c926a1d6db19ec646f6aa373743423fd6b6fb71b6cfd4a46f8865577b29b"


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def independent_scope():
    semantic = cut_checker.derive()
    memberships = base.derive()[1]
    result = tuple((row, memberships[row["membership"]]) for row in semantic)
    if len(result) != MEMBERSHIPS:
        raise RuntimeError("independent Hall-failure scope differs")
    return result


def add_threshold(names, clauses, inputs, tag):
    previous = []
    for index, literal in enumerate(inputs, 1):
        current = []
        for target in range(1, index + 1):
            name = f"cnt_{tag}_{index}_{target}"
            names.append(name)
            value = len(names)
            current.append(value)
            old_same = previous[target - 1] if target <= len(previous) else None
            old_lower = previous[target - 2] if target >= 2 else True
            if old_same is not None:
                clauses.append((-old_same, value))
            clauses.append((-literal, value) if old_lower is True else (-literal, -old_lower, value))
            if old_same is None:
                clauses.append((-value, literal))
                if old_lower is not True:
                    clauses.append((-value, old_lower))
            elif old_lower is True:
                clauses.append((-value, old_same, literal))
            else:
                clauses.append((-value, old_same, literal))
                clauses.append((-value, old_same, old_lower))
        previous = current
    return previous


def reconstruct(record):
    row, member = record
    names, clauses, selectors = base.reconstruct(member)
    names, clauses = list(names), list(clauses)
    pair = set(row["pair"])
    nonout = set(range(18)) - set(row["out"]) - {row["low"]}
    universe, support = tuple(sorted(nonout - pair)), tuple(row["out"])
    if len(universe) != 7 or len(support) != 8:
        raise RuntimeError("independent 7-by-8 Hall partition failed")

    def new(name):
        names.append(name)
        return len(names)

    chosen = [new(f"hall_K_{u}") for u in universe]
    links = {}
    for u, selected in zip(universe, chosen):
        for s in support:
            link = new(f"hall_link_{u}_{s}")
            arc = names.index(f"a_{s}_{u}") + 1
            links[u, s] = link
            clauses.extend(((-link, selected), (-link, arc), (link, -selected, -arc)))
    gamma = []
    for s in support:
        value = new(f"hall_Gamma_{s}")
        gamma.append(value)
        incident = tuple(links[u, s] for u in universe)
        clauses.extend((-link, value) for link in incident)
        clauses.append((-value, *incident))
    k_threshold = add_threshold(names, clauses, chosen, "hall_K")
    gamma_threshold = add_threshold(names, clauses, gamma, "hall_Gamma")
    blockers = []
    for size in range(1, 8):
        blocker = new(f"hall_defect_{size}")
        blockers.append(blocker)
        clauses.extend(((-blocker, k_threshold[size - 1]),
                        (-blocker, -gamma_threshold[size - 1]),
                        (blocker, -k_threshold[size - 1], gamma_threshold[size - 1])))
    clauses.append(tuple(blockers))
    return names, clauses, selectors, universe, support


def dimensions(record):
    variables, clauses = base.producer.dimensions(record[1])
    return variables + ADDED_VARIABLES, clauses + ADDED_CLAUSES


def hall_sets(row):
    pair = set(row["pair"])
    nonout = set(range(18)) - set(row["out"]) - {row["low"]}
    universe, support = tuple(sorted(nonout - pair)), tuple(row["out"])
    if len(universe) != 7 or len(support) != 8:
        raise RuntimeError("independent 7-by-8 Hall partition failed")
    return universe, support


def manifest_payload(records):
    census = HERE / f"{cut_checker.producer.PREFIX}.tsv"
    census_data = census.read_bytes()
    lines = [MANIFEST_FORMAT, f"cut-census-bytes\t{len(census_data)}",
             f"cut-census-sha256\t{hashlib.sha256(census_data).hexdigest()}",
             f"memberships\t{MEMBERSHIPS}",
             "scope\texactly the ordered 33 committed five-second singleton TIMEOUT memberships",
             "U\tthe seven q-positive vertices outside S, low-C, and the exact inaccessible pair",
             "S\tthe eight vertices of N+(low-C)",
             "incidence\tu is adjacent to s exactly when the original arc s->u is present",
             "selection\tan arbitrary nonempty K subset of U",
             "neighborhood\tGamma(K) is encoded exactly as {s in S: exists u in K with s->u}",
             "violation\t|Gamma(K)|<|K|", f"added-variables\t{ADDED_VARIABLES}",
             f"added-clauses\t{ADDED_CLAUSES}",
             "proof-status\tscout-only; no UNSAT certificate generated",
             "theorem-status\tHall synchronization is not yet a theorem until complements/residual cases are handled and UNSAT certificates are checked",
             "columns\tposition,membership,key,cell,parent,U,S,variables,clauses"]
    for position, (row, member) in enumerate(records):
        universe, support = hall_sets(row)
        variables, clauses = dimensions((row, member))
        lines.append(f"{position:03d}\t{row['membership']:03d}\t{base.producer.membership_key(member)}\t"
                     f"{member[0]:03d}\t{member[2]:02d}\t{','.join(map(str, universe))}\t"
                     f"{','.join(map(str, support))}\t{variables}\t{clauses}")
    return ("\n".join(lines) + "\n").encode("ascii")


def metadata(position, record, manifest, selectors, universe, support):
    row, member = record
    return [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
            ("manifest-bytes", str(len(manifest))),
            ("manifest-sha256", hashlib.sha256(manifest).hexdigest()),
            ("position", str(position)), ("membership", str(row["membership"])),
            ("key", base.producer.membership_key(member)), ("cell", str(member[0])),
            ("parent-ordinal", str(member[2])), ("selected-selector", str(selectors[member[2]])),
            ("hall-U", ",".join(map(str, universe))), ("hall-S", ",".join(map(str, support))),
            ("hall-incidence", "s->u"), ("hall-added-variables", str(ADDED_VARIABLES)),
            ("hall-added-clauses", str(ADDED_CLAUSES)), ("lrat-status", "not-generated")]


def load_hashes(path=HASHES):
    records = independent_scope()
    manifest = manifest_payload(records)
    lines = path.read_text(encoding="ascii").splitlines()
    expected = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
                f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}",
                f"memberships\t{MEMBERSHIPS}",
                "columns\tposition,membership,key,variables,clauses,cnf-bytes,cnf-sha256"]
    if lines[:5] != expected or len(lines) != 5 + len(records):
        raise RuntimeError("Hall hash ledger framing differs")
    result = []
    for position, (line, (row, member)) in enumerate(zip(lines[5:], records)):
        fields = line.split("\t")
        variables, clauses = dimensions((row, member))
        prefix = [f"{position:03d}", f"{row['membership']:03d}",
                  base.producer.membership_key(member), str(variables), str(clauses)]
        if len(fields) != 7 or fields[:5] != prefix or not fields[5].isdigit() or \
                re.fullmatch(r"[0-9a-f]{64}", fields[6]) is None:
            raise RuntimeError(f"Hall hash row differs: {position:03d}")
        result.append((int(fields[5]), fields[6]))
    if path.read_bytes() != ("\n".join(lines) + "\n").encode("ascii"):
        raise RuntimeError("Hall hash ledger is not canonical ASCII TSV")
    return tuple(result)


def check_cover(regenerate=True):
    records = independent_scope()
    manifest = manifest_payload(records)
    if MANIFEST.read_bytes() != manifest:
        raise RuntimeError("Hall manifest differs from independent scope")
    hashes = load_hashes()
    for record in records:
        names, clauses, _, _, _ = reconstruct(record)
        base_variables, base_clauses = base.producer.dimensions(record[1])
        if (len(names) - base_variables, len(clauses) - base_clauses) != \
                (ADDED_VARIABLES, ADDED_CLAUSES):
            raise RuntimeError("independent Hall dimensions differ")
    if regenerate:
        with tempfile.TemporaryDirectory(prefix="hall-failure-check-", dir=HERE.parent) as directory:
            path = Path(directory) / "membership.cnf"
            for position, record in enumerate(records):
                names, clauses, selectors, universe, support = reconstruct(record)
                with path.open("w", encoding="ascii", newline="\n") as handle:
                    for name, value in metadata(position, record, manifest, selectors,
                                                universe, support):
                        handle.write(f"c {name} {value}\n")
                    for number, name in enumerate(names, 1):
                        handle.write(f"c var {number} {name}\n")
                    handle.write(f"p cnf {len(names)} {len(clauses)}\n")
                    for clause in clauses:
                        handle.write(" ".join(map(str, clause)) + " 0\n")
                if identity(path) != hashes[position]:
                    raise RuntimeError(f"regenerated Hall membership differs: {position:03d}")
    print(f"PASS memberships={len(records)} added_vars={ADDED_VARIABLES} "
          f"added_clauses={ADDED_CLAUSES} manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


def check(path):
    records = independent_scope()
    manifest = manifest_payload(records)
    parsed_metadata, variables, clauses, declared = parse_cnf(path)
    try:
        position = int(dict(parsed_metadata).get("position", "-1"))
    except ValueError as error:
        raise RuntimeError("invalid Hall position") from error
    if not 0 <= position < len(records):
        raise RuntimeError("Hall position outside manifest")
    names, expected_clauses, selectors, universe, support = reconstruct(records[position])
    if parsed_metadata != metadata(position, records[position], manifest, selectors, universe, support) or \
            variables != names or clauses != expected_clauses or declared != dimensions(records[position]):
        raise RuntimeError("Hall CNF differs from independent exact reconstruction")
    if identity(path) != load_hashes()[position]:
        raise RuntimeError("Hall CNF hash differs")
    print(f"PASS position={position:03d} membership={records[position][0]['membership']:03d} "
          f"sha256={identity(path)[1]}")


def maximum_matching(graph, left_size, right_size):
    match = [-1] * right_size

    def augment(left, seen):
        for right in range(right_size):
            if not graph[left][right] or seen[right]:
                continue
            seen[right] = True
            if match[right] < 0 or augment(match[right], seen):
                match[right] = left
                return True
        return False

    return sum(augment(left, [False] * right_size) for left in range(left_size))


def locally_satisfiable(clauses, assumptions):
    clauses = tuple(tuple(clause) for clause in clauses) + tuple((literal,) for literal in assumptions)

    def solve(current):
        while True:
            if any(not clause for clause in current):
                return False
            unit = next((clause[0] for clause in current if len(clause) == 1), None)
            if unit is None:
                break
            reduced = []
            for clause in current:
                if unit in clause:
                    continue
                reduced.append(tuple(literal for literal in clause if literal != -unit))
            current = tuple(reduced)
        if not current:
            return True
        literal = min(current, key=len)[0]
        return solve(current + ((literal,),)) or solve(current + ((-literal,),))

    return solve(clauses)


def tiny_hall_cnf(left_size, right_size):
    names, clauses = [], []

    def new(name):
        names.append(name)
        return len(names)

    edges = [[new(f"edge_{left}_{right}") for right in range(right_size)]
             for left in range(left_size)]
    chosen = [new(f"chosen_{left}") for left in range(left_size)]
    links = {}
    for left in range(left_size):
        for right in range(right_size):
            link = new(f"link_{left}_{right}")
            links[left, right] = link
            clauses.extend(((-link, chosen[left]), (-link, edges[left][right]),
                            (link, -chosen[left], -edges[left][right])))
    gamma = []
    for right in range(right_size):
        value = new(f"gamma_{right}")
        gamma.append(value)
        incident = tuple(links[left, right] for left in range(left_size))
        clauses.extend((-link, value) for link in incident)
        clauses.append((-value, *incident))
    k_threshold = add_threshold(names, clauses, chosen, "tiny_K")
    gamma_threshold = add_threshold(names, clauses, gamma, "tiny_Gamma")
    blockers = []
    for size in range(1, left_size + 1):
        blocker = new(f"defect_{size}")
        blockers.append(blocker)
        clauses.extend(((-blocker, k_threshold[size - 1]),
                        (-blocker, -gamma_threshold[size - 1]),
                        (blocker, -k_threshold[size - 1], gamma_threshold[size - 1])))
    clauses.append(tuple(blockers))
    return edges, chosen, tuple(clauses)


def truth_table_audit():
    left_size = right_size = 3
    edges, chosen, clauses = tiny_hall_cnf(left_size, right_size)
    checked = 0
    for mask in range(1 << (left_size * right_size)):
        graph = [[bool(mask & (1 << (left * right_size + right)))
                  for right in range(right_size)] for left in range(left_size)]
        deficient = False
        for subset_mask in range(1, 1 << left_size):
            neighborhood = {right for left in range(left_size) if subset_mask & (1 << left)
                            for right in range(right_size) if graph[left][right]}
            expected = len(neighborhood) < subset_mask.bit_count()
            assumptions = [edges[left][right] if graph[left][right] else -edges[left][right]
                           for left in range(left_size) for right in range(right_size)]
            assumptions.extend(chosen[left] if subset_mask & (1 << left) else -chosen[left]
                               for left in range(left_size))
            if locally_satisfiable(clauses, assumptions) != expected:
                raise RuntimeError("tiny compact Hall CNF disagrees with direct subset semantics")
            deficient |= expected
            checked += 1
        blocker = maximum_matching(graph, left_size, right_size) < left_size
        if deficient != blocker:
            raise RuntimeError("tiny Hall truth table disagrees with matching blocker")
    print(f"PASS truth_table graphs={1 << 9} compact_cnf_instances={checked} "
          "local_dpll=yes matching_blocker_equivalent=yes")


def check_scout(path=SCOUT):
    records = independent_scope()
    manifest = manifest_payload(records)
    ledger = HASHES.read_bytes()
    hashes = load_hashes()
    raw = path.read_bytes()
    if identity(path) != SCOUT_IDENTITY:
        raise RuntimeError("Hall scout full identity differs")
    data = json.loads(raw.decode("ascii"))
    if raw != (json.dumps(data, sort_keys=True, indent=2) + "\n").encode("ascii"):
        raise RuntimeError("Hall scout is not canonical ASCII JSON")
    expected_header = {
        "schema": f"{PREFIX}-scout-v1", "seconds_per_membership": SCOUT_SECONDS,
        "jobs": SCOUT_JOBS, "solver": SOLVER, "solver_bytes": SOLVER_IDENTITY[0],
        "solver_sha256": SOLVER_IDENTITY[1], "solver_version": SOLVER_IDENTITY[2],
        "default_solver_options": list(DEFAULT_OPTIONS),
        "position_options": {str(key): list(value) for key, value in POSITION_OPTIONS.items()},
        "manifest_bytes": len(manifest), "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
        "hash_ledger_bytes": len(ledger), "hash_ledger_sha256": hashlib.sha256(ledger).hexdigest(),
    }
    if set(data) != set(expected_header) | {"status_sequence_sha256", "rows"} or any(
            data.get(key) != value for key, value in expected_header.items()):
        raise RuntimeError("Hall scout provenance differs")
    rows = data["rows"]
    if len(rows) != len(records):
        raise RuntimeError("Hall scout scope is not exhaustive")
    for position, (record, row) in enumerate(zip(records, rows)):
        options = POSITION_OPTIONS.get(position, DEFAULT_OPTIONS)
        expected = {"position": position, "membership": record[0]["membership"],
                    "job": position % SCOUT_JOBS, "solver_options": list(options),
                    "cnf_sha256": hashes[position][1]}
        if set(row) != set(expected) | {"status", "seconds"} or any(
                row.get(key) != value for key, value in expected.items()):
            raise RuntimeError(f"Hall scout row differs: {position:03d}")
        seconds = row.get("seconds")
        if row.get("status") not in ("UNSAT", "TIMEOUT") or isinstance(seconds, bool) or \
                not isinstance(seconds, (int, float)) or not math.isfinite(seconds) or \
                (row["status"] == "TIMEOUT" and not SCOUT_SECONDS <= seconds <= SCOUT_SECONDS + 1) or \
                (row["status"] == "UNSAT" and not 0 <= seconds < SCOUT_SECONDS):
            raise RuntimeError(f"Hall scout timing differs: {position:03d}")
    sequence = "".join("U" if row["status"] == "UNSAT" else "T" for row in rows)
    totals = Counter(row["status"] for row in rows)
    if data["status_sequence_sha256"] != SCOUT_STATUS_SHA256 or \
            hashlib.sha256(sequence.encode("ascii")).hexdigest() != SCOUT_STATUS_SHA256 or \
            totals != Counter(SCOUT_TOTALS):
        raise RuntimeError("Hall scout status sequence differs")
    print(f"PASS scout totals={dict(totals)} status_sha256={data['status_sequence_sha256']} "
          f"scout_sha256={hashlib.sha256(raw).hexdigest()}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", type=Path, nargs="?")
    parser.add_argument("--cover", action="store_true")
    parser.add_argument("--truth-table", action="store_true")
    parser.add_argument("--scout", action="store_true")
    args = parser.parse_args()
    if args.cover:
        check_cover()
    if args.truth_table:
        truth_table_audit()
    if args.scout:
        check_scout()
    if args.cnf:
        check(args.cnf)
    if not args.cover and not args.truth_table and not args.scout and not args.cnf:
        parser.error("provide a CNF, --cover, --truth-table, or --scout")


if __name__ == "__main__":
    main()
