#!/usr/bin/env python3
"""Independent checker for the certificate-relative binary all-different layer."""

import argparse
from collections import Counter
import hashlib
import itertools
import json
import math
import re
import tempfile
from pathlib import Path

import check_m6_b7_l6_exact_pair_timeout_hall_failure as hall_check
import verify_m6_b7_l6_exact_pair_timeout_hall_failure_all33 as all33
from check_m6_parent_cnf import parse_cnf

HERE = Path(__file__).resolve().parent
PREFIX = "m6-b7-l6-exact-pair-hall-binary-alldifferent"
FORMAT = f"{PREFIX}-cnf-v1"
MANIFEST_FORMAT = f"{PREFIX}-manifest-v1"
HASH_FORMAT = f"{PREFIX}-hashes-v1"
MEMBERSHIPS = 33
ADDED_VARIABLES = 84
ADDED_CLAUSES = 336
MANIFEST = HERE / f"{PREFIX}.tsv"
HASHES = HERE / f"{PREFIX}-hashes.tsv"
SCOUT = HERE / f"{PREFIX}-scout-30s.json"
SCOUT_SECONDS = 30
SCOUT_JOBS = 8
SOLVER = "/tmp/opencode/cadical-1.7.3/build/cadical"
SOLVER_IDENTITY = (1002216, "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292", "1.7.3")
SOLVER_OPTIONS = ("--restart=false", "--phase=false", "--seed=3")
UNSAT_MEMBERSHIPS = ()
SCOUT_TOTALS = {"TIMEOUT": 33}
SCOUT_IDENTITY = (7797, "8adad66aa1418e340de0fd817853fb5dddac67f6371acc5118feb8bca846ac7c")
ANCESTRY = {
    "all33-hall-verifier": HERE / "verify_m6_b7_l6_exact_pair_timeout_hall_failure_all33.py",
    "direct-hall-certificates": HERE / "m6-b7-l6-exact-pair-timeout-hall-failure-scout-unsat-certificates.tsv",
    "split-hall-certificates": HERE / "m6-b7-l6-exact-pair-timeout-hall-failure-cardinality-split-certificates.tsv",
}


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def independent_scope():
    records = hall_check.independent_scope()
    audited, _, _ = all33.scope_audit()
    observed = tuple((position, row[0]["membership"]) for position, row in enumerate(records))
    if len(records) != MEMBERSHIPS or observed != audited:
        raise RuntimeError("binary all-different scope differs from committed Hall all33 ancestry")
    return records


def hall_sets(row):
    pair = set(row["pair"])
    nonout = set(range(18)) - set(row["out"]) - {row["low"]}
    universe, support = tuple(sorted(nonout - pair)), tuple(row["out"])
    if len(universe) != 7 or len(support) != 8:
        raise RuntimeError("independent Hall partition is not 7-by-8")
    return universe, support


def add_extension(names, clauses, universe, support):
    def new(name):
        names.append(name)
        return len(names)

    bits = {}
    for u in universe:
        bits[u] = tuple(new(f"hall_match_bit_{u}_{bit}") for bit in range(3))
        clauses.append(tuple(names.index(f"a_{s}_{u}") + 1 for s in support))
        for value, s in enumerate(support):
            mismatch = tuple(-bits[u][bit] if (value >> bit) & 1 else bits[u][bit]
                             for bit in range(3))
            clauses.append((*mismatch, names.index(f"a_{s}_{u}") + 1))
    for left_index, left in enumerate(universe):
        for right in universe[left_index + 1:]:
            differs = []
            for bit in range(3):
                value = new(f"hall_match_diff_{left}_{right}_{bit}")
                x, y = bits[left][bit], bits[right][bit]
                differs.append(value)
                clauses.extend(((-value, x, y), (-value, -x, -y),
                                (value, -x, y), (value, x, -y)))
            clauses.append(tuple(differs))
    return bits


def reconstruct(record):
    row, member = record
    names, clauses, selectors = hall_check.base.reconstruct(member)
    names, clauses = list(names), list(clauses)
    universe, support = hall_sets(row)
    bits = add_extension(names, clauses, universe, support)
    return names, clauses, selectors, universe, support, bits


def dimensions(record):
    variables, clauses = hall_check.base.producer.dimensions(record[1])
    return variables + ADDED_VARIABLES, clauses + ADDED_CLAUSES


def manifest_payload(records):
    lines = [MANIFEST_FORMAT, f"memberships\t{MEMBERSHIPS}",
             "scope\texactly the ordered 33 memberships certified Hall-synchronized by the committed all33 verifier",
             "U\tthe seven q-positive vertices from the committed Hall bipartition",
             "S\tthe ordered eight vertices of N+(low-C)",
             "domain\tthree bits per u encode exactly values 0..7; value i denotes S[i]",
             "channel\tvalue i selected for u implies the original arc S[i]->u",
             "all-different\tevery unordered pair of U has a three-bit XOR disequality",
             "row-support\teach u has at least one incident S->u arc; implied by Hall synchronization",
             f"added-variables\t{ADDED_VARIABLES}", f"added-clauses\t{ADDED_CLAUSES}",
             "extension-theorem\tevery Hall-synchronized graph extends by encoding a saturating matching",
             "projection-theorem\tevery satisfying extension decodes to an injective U-to-S arc matching"]
    for name, path in ANCESTRY.items():
        size, digest = identity(path)
        lines.extend((f"ancestry-{name}-bytes\t{size}", f"ancestry-{name}-sha256\t{digest}"))
    lines.append("columns\tposition,membership,key,cell,parent,U,S,variables,clauses")
    for position, (row, member) in enumerate(records):
        universe, support = hall_sets(row)
        variables, clauses = dimensions((row, member))
        lines.append(f"{position:03d}\t{row['membership']:03d}\t{hall_check.base.producer.membership_key(member)}\t"
                     f"{member[0]:03d}\t{member[2]:02d}\t{','.join(map(str, universe))}\t"
                     f"{','.join(map(str, support))}\t{variables}\t{clauses}")
    return ("\n".join(lines) + "\n").encode("ascii")


def metadata(position, record, manifest, selectors, universe, support):
    row, member = record
    return [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
            ("manifest-bytes", str(len(manifest))),
            ("manifest-sha256", hashlib.sha256(manifest).hexdigest()),
            ("position", str(position)), ("membership", str(row["membership"])),
            ("key", hall_check.base.producer.membership_key(member)), ("cell", str(member[0])),
            ("parent-ordinal", str(member[2])), ("selected-selector", str(selectors[member[2]])),
            ("hall-U", ",".join(map(str, universe))), ("hall-S", ",".join(map(str, support))),
            ("matching-domain", "binary-0..7"), ("matching-channel", "S[value]->u"),
            ("matching-added-variables", str(ADDED_VARIABLES)),
            ("matching-added-clauses", str(ADDED_CLAUSES)), ("lrat-status", "scout-only")]


def load_hashes(path=HASHES):
    records = independent_scope()
    manifest = manifest_payload(records)
    lines = path.read_text(encoding="ascii").splitlines()
    expected = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
                f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}",
                f"memberships\t{MEMBERSHIPS}",
                "columns\tposition,membership,key,variables,clauses,cnf-bytes,cnf-sha256"]
    if lines[:5] != expected or len(lines) != 5 + len(records):
        raise RuntimeError("binary all-different hash ledger framing differs")
    result = []
    for position, (line, (row, member)) in enumerate(zip(lines[5:], records)):
        fields = line.split("\t")
        variables, clauses = dimensions((row, member))
        prefix = [f"{position:03d}", f"{row['membership']:03d}",
                  hall_check.base.producer.membership_key(member), str(variables), str(clauses)]
        if len(fields) != 7 or fields[:5] != prefix or not fields[5].isdigit() or \
                re.fullmatch(r"[0-9a-f]{64}", fields[6]) is None:
            raise RuntimeError(f"binary all-different hash row differs: {position:03d}")
        result.append((int(fields[5]), fields[6]))
    if path.read_bytes() != ("\n".join(lines) + "\n").encode("ascii"):
        raise RuntimeError("binary all-different hash ledger is not canonical ASCII TSV")
    return tuple(result)


def check_cover(regenerate=True):
    records = independent_scope()
    manifest = manifest_payload(records)
    if MANIFEST.read_bytes() != manifest:
        raise RuntimeError("binary all-different manifest differs")
    hashes = load_hashes()
    with tempfile.TemporaryDirectory(prefix="hall-binary-check-", dir=HERE.parent) as directory:
        path = Path(directory) / "membership.cnf"
        for position, record in enumerate(records):
            names, clauses, selectors, universe, support, _ = reconstruct(record)
            base_variables, base_clauses = hall_check.base.producer.dimensions(record[1])
            if (len(names) - base_variables, len(clauses) - base_clauses) != \
                    (ADDED_VARIABLES, ADDED_CLAUSES):
                raise RuntimeError("independent binary all-different dimensions differ")
            if not regenerate:
                continue
            with path.open("w", encoding="ascii", newline="\n") as handle:
                for name, value in metadata(position, record, manifest, selectors, universe, support):
                    handle.write(f"c {name} {value}\n")
                for number, name in enumerate(names, 1):
                    handle.write(f"c var {number} {name}\n")
                handle.write(f"p cnf {len(names)} {len(clauses)}\n")
                for clause in clauses:
                    handle.write(" ".join(map(str, clause)) + " 0\n")
            if identity(path) != hashes[position]:
                raise RuntimeError(f"regenerated binary all-different membership differs: {position:03d}")
    print(f"PASS memberships={len(records)} added_vars={ADDED_VARIABLES} "
          f"added_clauses={ADDED_CLAUSES} manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


def check(path):
    records = independent_scope()
    manifest = manifest_payload(records)
    parsed_metadata, variables, clauses, declared = parse_cnf(path)
    try:
        position = int(dict(parsed_metadata).get("position", "-1"))
    except ValueError as error:
        raise RuntimeError("invalid binary all-different position") from error
    if not 0 <= position < len(records):
        raise RuntimeError("binary all-different position outside manifest")
    names, expected_clauses, selectors, universe, support, _ = reconstruct(records[position])
    if parsed_metadata != metadata(position, records[position], manifest, selectors, universe, support) or \
            variables != names or clauses != expected_clauses or declared != dimensions(records[position]):
        raise RuntimeError("binary all-different CNF differs from independent reconstruction")
    if identity(path) != load_hashes()[position]:
        raise RuntimeError("binary all-different CNF hash differs")
    print(f"PASS position={position:03d} membership={records[position][0]['membership']:03d} "
          f"sha256={identity(path)[1]}")


def maximum_matching(graph):
    match = [-1] * len(graph[0])
    def augment(left, seen):
        for right, edge in enumerate(graph[left]):
            if not edge or seen[right]:
                continue
            seen[right] = True
            if match[right] < 0 or augment(match[right], seen):
                match[right] = left
                return True
        return False
    return sum(augment(left, [False] * len(match)) for left in range(len(graph)))


def semantic_audit():
    checked_graphs = checked_extensions = 0
    for right_size in (1, 2, 4):
        bit_count = (right_size - 1).bit_length()
        for left_size in range(1, min(2, right_size) + 1):
            for mask in range(1 << (left_size * right_size)):
                graph = [[bool(mask & (1 << (left * right_size + right)))
                          for right in range(right_size)] for left in range(left_size)]
                hall = all(sum(any(graph[left][right] for left in subset) for right in range(right_size))
                           >= len(subset)
                           for size in range(1, left_size + 1)
                           for subset in itertools.combinations(range(left_size), size))
                matching = maximum_matching(graph) == left_size
                extension = False
                for values in itertools.product(range(right_size), repeat=left_size):
                    valid = len(set(values)) == left_size and all(graph[left][value]
                                                                  for left, value in enumerate(values))
                    extension |= valid
                    checked_extensions += 1
                    bits = [[(value >> bit) & 1 for bit in range(bit_count)] for value in values]
                    decoded = [sum(bit << index for index, bit in enumerate(row)) for row in bits]
                    if valid != (decoded == list(values) and len(set(decoded)) == left_size and
                                 all(graph[left][decoded[left]] for left in range(left_size))):
                        raise RuntimeError("binary extension decoding disagrees with injection semantics")
                if hall != matching or matching != extension:
                    raise RuntimeError("Hall, matching, and binary extension semantics disagree")
                checked_graphs += 1
    print(f"PASS semantic graphs={checked_graphs} extensions={checked_extensions} "
          "Hall_iff_matching_iff_extension=yes projection_is_injection=yes")


def excluded_value_counterexample():
    graph = [[left == right for right in range(8)] for left in range(7)]
    graph[6] = [False] * 7 + [True]
    if maximum_matching(graph) != 7:
        raise RuntimeError("internal excluded-value counterexample is not Hall-synchronized")
    if any(len(set(values)) == 7 and all(graph[left][value] for left, value in enumerate(values))
           for values in itertools.product(range(7), repeat=7)):
        raise RuntimeError("values 0..6 unexpectedly match a graph requiring value 7")
    print("PASS excluded_value_counterexample Hall=yes value7_required=yes forbid7_unsound=yes")


def check_scout(path=SCOUT, require_identity=True):
    records = independent_scope()
    manifest = manifest_payload(records)
    ledger = HASHES.read_bytes()
    hashes = load_hashes()
    raw = path.read_bytes()
    if require_identity and identity(path) != SCOUT_IDENTITY:
        raise RuntimeError("binary all-different scout full identity differs")
    data = json.loads(raw.decode("ascii"))
    if raw != (json.dumps(data, sort_keys=True, indent=2) + "\n").encode("ascii"):
        raise RuntimeError("binary all-different scout is not canonical ASCII JSON")
    expected_header = {
        "schema": f"{PREFIX}-scout-v1", "seconds_per_membership": SCOUT_SECONDS,
        "jobs": SCOUT_JOBS, "solver": SOLVER, "solver_bytes": SOLVER_IDENTITY[0],
        "solver_sha256": SOLVER_IDENTITY[1], "solver_version": SOLVER_IDENTITY[2],
        "solver_options": list(SOLVER_OPTIONS), "manifest_bytes": len(manifest),
        "manifest_sha256": hashlib.sha256(manifest).hexdigest(), "hash_ledger_bytes": len(ledger),
        "hash_ledger_sha256": hashlib.sha256(ledger).hexdigest(),
    }
    if set(data) != set(expected_header) | {"status_sequence_sha256", "rows"} or any(
            data.get(key) != value for key, value in expected_header.items()):
        raise RuntimeError("binary all-different scout provenance differs")
    rows = data["rows"]
    if len(rows) != len(records):
        raise RuntimeError("binary all-different scout scope is not exhaustive")
    for position, (record, row) in enumerate(zip(records, rows)):
        expected = {"position": position, "membership": record[0]["membership"],
                    "job": position % SCOUT_JOBS, "cnf_sha256": hashes[position][1]}
        if set(row) != set(expected) | {"status", "seconds"} or any(
                row.get(key) != value for key, value in expected.items()):
            raise RuntimeError(f"binary all-different scout row differs: {position:03d}")
        seconds = row.get("seconds")
        if row.get("status") not in ("UNSAT", "TIMEOUT") or isinstance(seconds, bool) or \
                not isinstance(seconds, (int, float)) or not math.isfinite(seconds) or \
                (row["status"] == "TIMEOUT" and not SCOUT_SECONDS <= seconds <= SCOUT_SECONDS + 1) or \
                (row["status"] == "UNSAT" and not 0 <= seconds < SCOUT_SECONDS):
            raise RuntimeError(f"binary all-different scout timing differs: {position:03d}")
    sequence = "".join("U" if row["status"] == "UNSAT" else "T" for row in rows)
    totals = Counter(row["status"] for row in rows)
    unsat = tuple(row["membership"] for row in rows if row["status"] == "UNSAT")
    if data["status_sequence_sha256"] != hashlib.sha256(sequence.encode("ascii")).hexdigest() or \
            totals != Counter(SCOUT_TOTALS) or unsat != UNSAT_MEMBERSHIPS:
        raise RuntimeError("binary all-different scout exact status sequence differs")
    print(f"PASS scout totals={dict(totals)} unsat={','.join(f'{x:03d}' for x in unsat)} "
          f"status_sha256={data['status_sequence_sha256']} scout_sha256={hashlib.sha256(raw).hexdigest()}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", type=Path, nargs="?")
    parser.add_argument("--cover", action="store_true")
    parser.add_argument("--semantic", action="store_true")
    parser.add_argument("--excluded-value-counterexample", action="store_true")
    parser.add_argument("--scout", action="store_true")
    args = parser.parse_args()
    if args.cover:
        check_cover()
    if args.semantic:
        semantic_audit()
    if args.excluded_value_counterexample:
        excluded_value_counterexample()
    if args.scout:
        check_scout()
    if args.cnf:
        check(args.cnf)
    if not args.cover and not args.semantic and not args.excluded_value_counterexample and \
            not args.scout and not args.cnf:
        parser.error("provide a CNF, --cover, --semantic, --excluded-value-counterexample, or --scout")


if __name__ == "__main__":
    main()
