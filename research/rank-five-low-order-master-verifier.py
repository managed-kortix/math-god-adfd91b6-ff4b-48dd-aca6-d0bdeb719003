#!/usr/bin/env python3
"""Fail-closed master audit for all rank-five kernels of order at most four."""

import argparse
import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
KERNEL_FIXTURE = HERE / "fixtures" / "rank-five-kernels.json"
SIX_PATH_PROOF = (ROOT / "positive-square-energy" / "pentacyclic-general"
                  / "six-path-dnn-theorem.md")
KERNEL_FIXTURE_SHA256 = "027c84d6dd777a29b3dc93389ab30b5d43f6507eddceb4ea286f1240da95b884"
SIX_PATH_PROOF_SHA256 = "3eef886673c68c267dea7911c373309c56a6ce02ef1bc254b92b394faeb8aa7e"
EXPECTED_COUNTS = (1, 3, 13)
EXPECTED_CODES = (
    ((6,),),
    ((1, 2, 4), (1, 3, 3), (2, 2, 3)),
    ((0, 1, 2, 1, 2, 2), (0, 1, 2, 2, 1, 2),
     (0, 1, 2, 2, 2, 1), (0, 1, 3, 3, 1, 0),
     (0, 2, 1, 1, 3, 1), (0, 2, 2, 2, 2, 0),
     (1, 0, 2, 1, 1, 3), (1, 0, 2, 2, 0, 3),
     (1, 1, 1, 1, 1, 3), (1, 1, 1, 1, 2, 2),
     (1, 1, 2, 2, 1, 1), (1, 2, 0, 0, 3, 2),
     (2, 0, 1, 1, 0, 4)),
)
DEPENDENCIES = (
    ("three-vertex", "rank-five-three-vertex-orbit-verifier.py", ("--emit",),
     "automorphism_orbits_by_kernel: 30,20,24 (total 74)", (3,),
     "4bdb730702ad34936c988c26a4f8f32036fda5657c22301ddd70d70a416d1659"),
    ("four-vertex-sieve", "rank-five-four-vertex-tetrahedral-sieve-verifier.py",
     ("--emit",), "sieve_partition: 808 certified + 13 residual", (4,),
     "d047fe18201a136380bd8d67f833c4bc862f5d088ea7cdb101758ac1319d4ae2"),
    ("four-vertex-frontier", "rank-five-four-vertex-residual-frontier-verifier.py",
     ("--emit",),
     "certificates: 116 strict rational path-vector + 1 kernel-9 symbolic equality",
     (4,), "eb011b634098bb50f1c4d95e1dce37f80b581b13b48d4d885be875e6a93247c6"),
)
EXPECTED_MANIFEST_SHA256 = "691d3d2e22740e502001c3150910095ac554c13f70fb88f77b8b432fa8bfdedf"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def load_kernel_selection(path=KERNEL_FIXTURE, expected_digest=KERNEL_FIXTURE_SHA256):
    try:
        raw = path.read_bytes()
        payload = json.loads(raw)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"cannot load kernel fixture: {error}") from error
    require(expected_digest == KERNEL_FIXTURE_SHA256, "kernel digest policy changed")
    require(hashlib.sha256(raw).hexdigest() == expected_digest,
            "rank-five kernel fixture digest changed")
    require(raw == canonical_bytes(payload), "rank-five kernel fixture is not canonical JSON")
    require(payload.get("beta") == 5, "kernel fixture rank changed")
    selected = tuple(tuple(tuple(record["code"]) for record in payload.get("kernels", ())
                           if record.get("n") == order) for order in (2, 3, 4))
    require(tuple(map(len, selected)) == EXPECTED_COUNTS, "low-order count is not 1+3+13")
    require(selected == EXPECTED_CODES, "low-order kernel selection changed")
    require(sum(map(len, selected)) == 17, "low-order kernel total changed")
    return selected


def six_path_analytic_checks(proof_digest=SIX_PATH_PROOF_SHA256, ledger=None):
    require(proof_digest == SIX_PATH_PROOF_SHA256, "six-path proof digest policy changed")
    require(hashlib.sha256(SIX_PATH_PROOF.read_bytes()).hexdigest() == proof_digest,
            "six-path analytic proof changed")
    expected = {
        "no_unit_even_counts": tuple(range(7)),
        "unit_even_counts": tuple(range(6)),
        "no_unit_endpoint_values": (0, 2, 4, 3, 2, 1, 0),
        "exceptional_derivative": 8,
        "unit_middle_numerators": (8, 9, 10),
        "unit_endpoint_values": (0, 2),
        "unit_e5_numerator": 11,
        "common_denominator": 3,
        "budget": 4,
        "rank": 5,
        "path_count": 6,
    }
    value = expected if ledger is None else ledger
    require(value == expected, "six-path analytic ledger changed")
    require(value["no_unit_even_counts"] == tuple(range(value["path_count"] + 1)),
            "no-unit parity split is incomplete")
    require(value["unit_even_counts"] == tuple(range(value["path_count"])),
            "unit parity split is incomplete")
    values = value["no_unit_endpoint_values"]
    require(all(entry < 4 for index, entry in enumerate(values) if index != 2),
            "no-unit endpoint witness exceeds budget")
    require(values[2] == 4 and value["exceptional_derivative"] > 0,
            "exceptional e=2 left-neighborhood check changed")
    denominator = value["common_denominator"]
    require(all(Fraction(numerator, denominator) < 4
                for numerator in value["unit_middle_numerators"]),
            "unit middle witness exceeds budget")
    require(all(entry < 4 for entry in value["unit_endpoint_values"]),
            "unit endpoint witness exceeds budget")
    require(Fraction(value["unit_e5_numerator"], denominator) < 4,
            "unit e=5 witness exceeds budget")
    require(value["budget"] == value["rank"] - 1 == 4,
            "rank-five excess threshold changed")
    return value


def invoke_dependency(entry):
    name, filename, arguments, required_line, scope, expected_file_digest = entry
    path = HERE / filename
    require(path.is_file(), f"missing exact dependency: {filename}")
    require(hashlib.sha256(path.read_bytes()).hexdigest() == expected_file_digest,
            f"dependency file digest changed: {name}")
    optimize = ("-O",) if sys.flags.optimize else ()
    completed = subprocess.run((sys.executable, *optimize, str(path), *arguments),
                               check=False, capture_output=True, text=True)
    require(completed.returncode == 0, f"exact dependency failed: {name}")
    require(completed.stderr == "", f"exact dependency wrote stderr: {name}")
    require(required_line in completed.stdout, f"dependency acceptance ledger changed: {name}")
    return {
        "name": name,
        "file": filename,
        "file_sha256": expected_file_digest,
        "output_sha256": hashlib.sha256(completed.stdout.encode("utf-8")).hexdigest(),
        "required_line": required_line,
        "orders": list(scope),
    }


def scope_partition(entries=DEPENDENCIES):
    require(entries == DEPENDENCIES, "exact dependency registry changed")
    claims = {2: ["six-path-analytic"], 3: [], 4: []}
    for name, unused_file, unused_arguments, unused_line, scope, unused_digest in entries:
        require(scope and len(scope) == len(set(scope)), f"invalid dependency scope: {name}")
        require(all(order in claims for order in scope), f"out-of-range dependency scope: {name}")
        for order in scope:
            claims[order].append(name)
    require(claims[2] == ["six-path-analytic"], "two-vertex theorem owner changed")
    require(claims[3] == ["three-vertex"], "three-vertex theorem owner changed")
    require(claims[4] == ["four-vertex-sieve", "four-vertex-frontier"],
            "four-vertex sieve/frontier composition changed")
    return claims


def manifest(records, selected, analytic):
    claims = scope_partition()
    return {
        "schema": "rank-five-low-order-master-exact-verifier-v1",
        "kernel_fixture_sha256": KERNEL_FIXTURE_SHA256,
        "kernel_counts_by_order_2_to_4": list(EXPECTED_COUNTS),
        "kernel_total": sum(EXPECTED_COUNTS),
        "selected_codes": [[list(code) for code in rows] for rows in selected],
        "theorem_owner": {str(order): "+".join(claims[order]) for order in claims},
        "six_path_analytic": {
            "proof_sha256": SIX_PATH_PROOF_SHA256,
            "finite_ledger": {key: list(value) if isinstance(value, tuple) else value
                              for key, value in analytic.items()},
            "scope": "all positive six-path lengths with at most one unit length",
        },
        "dependencies": records,
        "conclusion": "DNN excess <= 4 for every simple subdivision; strict at order 2",
    }


def serialize(value):
    return canonical_bytes(value).decode("ascii")


def audit(entries=DEPENDENCIES, expected_digest=EXPECTED_MANIFEST_SHA256):
    require(expected_digest == EXPECTED_MANIFEST_SHA256, "manifest digest policy changed")
    selected = load_kernel_selection()
    analytic = six_path_analytic_checks()
    scope_partition(entries)
    records = [invoke_dependency(entry) for entry in entries]
    value = manifest(records, selected, analytic)
    digest = hashlib.sha256(canonical_bytes(value)).hexdigest()
    require(digest == expected_digest, "exact dependency manifest digest changed")
    return value, digest


def expect_rejected(action, label):
    try:
        action()
    except (IndexError, KeyError, RuntimeError, TypeError, ValueError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_self_checks():
    mutations = 0
    for index, entry in enumerate(DEPENDENCIES):
        candidate = DEPENDENCIES[:index] + DEPENDENCIES[index + 1:]
        expect_rejected(lambda candidate=candidate: scope_partition(candidate),
                        f"omitted dependency {entry[0]}")
        mutations += 1
    changed = list(deepcopy(DEPENDENCIES))
    entry = list(changed[2])
    entry[4] = (3,)
    changed[2] = tuple(entry)
    expect_rejected(lambda: scope_partition(tuple(changed)), "frontier scope moved")
    mutations += 1
    bad_ledger = dict(six_path_analytic_checks())
    bad_ledger["unit_even_counts"] = tuple(range(5))
    expect_rejected(lambda: six_path_analytic_checks(ledger=bad_ledger),
                    "six-path parity case omitted")
    mutations += 1
    expect_rejected(lambda: six_path_analytic_checks("0" * 64), "six-path digest mutation")
    mutations += 1
    expect_rejected(lambda: load_kernel_selection(expected_digest="0" * 64),
                    "kernel fixture digest mutation")
    mutations += 1
    expect_rejected(lambda: audit(expected_digest="0" * 64), "manifest digest mutation")
    mutations += 1
    return mutations


def report(value, digest, mutations):
    return "\n".join((
        "rank-five low-order master theorem: all exact audits passed",
        "kernel_selection_by_order_2_to_4: 1+3+13=17 exact fixture rows",
        "order_2: six-path analytic ledger; all lengths; strict excess < 4",
        "order_3: 98 physical rows / 74 orbits; exact excess <= 4",
        "order_4: 821 orbits = 808 sieve + 13 frontier-closed residual",
        "frontier_covering_set: selected 117 targets = 116 strict rational + 1 symbolic equality",
        "attachments: arbitrary rooted trees at arbitrary subdivision vertices",
        "conclusion: s+(G)>=|V(G)| for every selected kernel subdivision",
        f"exact_dependency_manifest_sha256: {digest}",
        f"rejected_hostile_mutations: {mutations}",
    )) + "\n"


def optimized_output():
    completed = subprocess.run([sys.executable, "-O", str(Path(__file__).resolve()), "--emit"],
                               check=False, capture_output=True, text=True)
    require(completed.returncode == 0, "python -O master verifier failed")
    require(completed.stderr == "", "python -O master verifier wrote stderr")
    return completed.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--print-manifest", action="store_true")
    args = parser.parse_args()
    value, digest = audit()
    mutations = hostile_self_checks()
    require(mutations == 8, "hostile mutation count changed")
    output = report(value, digest, mutations)
    if not args.emit and sys.flags.optimize == 0:
        require(optimized_output() == output, "normal and python -O output differ")
    if args.print_manifest:
        sys.stdout.write(serialize(value))
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
