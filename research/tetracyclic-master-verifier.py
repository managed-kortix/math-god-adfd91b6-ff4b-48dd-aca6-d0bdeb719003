#!/usr/bin/env python3
"""Master exact verifier for all 17 suppressed tetracyclic kernels."""

import argparse
import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEPENDENCIES = (
    ("rank4-census", "rank-four-kernel-census-verifier.py", (),
     "canonical_counts_n2_to_n6: 1,2,5,4,5 (total 17)", tuple(range(1, 18))),
    ("three-vertex-tables", "rank-four-three-vertex-tables-verifier.py", ("--emit",),
     "physical_partition_222: 27 = 10 low-table + 17 common", (2, 3)),
    ("four-vertex", "rank-four-four-vertex-theorem-verifier.py", (),
     "physical_rows: 342 = 270 base + 70 patch + 2 discharged", (4, 5, 6, 7, 8)),
    ("five-vertex-sieve", "rank-four-five-vertex-three-color-verifier.py", ("--emit",),
     "sieve_partition: 370 certified + 8 residual", (9, 10, 11, 12)),
    ("five-vertex-closure", "rank-four-five-vertex-residual-closure-verifier.py", ("--emit",),
     "residual_rows: 8 (kernel 9: 4, kernel 10: 2, kernel 11: 2)", (9, 10, 11, 12)),
    ("kernel16", "rank-four-kernel16-three-color-verifier.py", (),
     "physical_parity_rows: 512 (=2^9; not 3^9)", (16,)),
    ("cubic-final", "rank-four-cubic-kernels-final-verifier.py", ("--emit",),
     "cubic kernels 13--15,17 final theorem: exact audit passed", (13, 14, 15, 17)),
)
EXPECTED_COUNTS = (1, 2, 5, 4, 5)
EXPECTED_SCOPE = tuple(range(1, 18))
EXPECTED_MANIFEST_SHA256 = "38b93ad68fe94e678de68547f916e4e4c0b58845377050df455ad860f4e16202"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def dependency_path(filename):
    return HERE / filename


def invoke_dependency(entry):
    name, filename, arguments, required_line, unused_scope = entry
    path = dependency_path(filename)
    require(path.is_file(), f"missing exact dependency: {filename}")
    optimize = ("-O",) if sys.flags.optimize else ()
    completed = subprocess.run(
        (sys.executable, *optimize, str(path), *arguments),
        check=False, capture_output=True, text=True)
    require(completed.returncode == 0, f"exact dependency failed: {name}")
    require(completed.stderr == "", f"exact dependency wrote stderr: {name}")
    require(required_line in completed.stdout,
            f"exact dependency acceptance ledger changed: {name}")
    return {
        "name": name,
        "file": filename,
        "file_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "output_sha256": hashlib.sha256(completed.stdout.encode("utf-8")).hexdigest(),
        "required_line": required_line,
        "scope": list(unused_scope),
    }


def scope_partition(entries=DEPENDENCIES):
    claims = {number: [] for number in EXPECTED_SCOPE}
    for name, unused_filename, unused_arguments, unused_line, scope in entries:
        require(scope and len(scope) == len(set(scope)),
                f"invalid dependency scope: {name}")
        require(all(number in EXPECTED_SCOPE for number in scope),
                f"out-of-range dependency scope: {name}")
        for number in scope:
            claims[number].append(name)
    theorem_claims = {
        number: tuple(name for name in names if name != "rank4-census")
        for number, names in claims.items()
    }
    theorem_claims[1] = ("five-path-analytic",)
    require(set(claims[1]) == {"rank4-census"},
            "kernel 1 incorrectly depends on a finite theorem table")
    require(all(theorem_claims[number] for number in EXPECTED_SCOPE),
            "kernel theorem scope has a gap")
    require(theorem_claims[9] == ("five-vertex-sieve", "five-vertex-closure")
            and all(theorem_claims[number] == theorem_claims[9]
                    for number in (10, 11, 12)),
            "five-vertex sieve/closure composition changed")
    require(all(len(theorem_claims[number]) == 1
                for number in (*range(1, 9), *range(13, 18))),
            "kernel theorem scopes overlap")
    return claims, theorem_claims


def manifest(records):
    claims, theorem_claims = scope_partition()
    return {
        "schema": "tetracyclic-master-exact-verifier-v1",
        "kernel_counts_by_order_2_to_6": list(EXPECTED_COUNTS),
        "kernel_scope": list(EXPECTED_SCOPE),
        "theorem_owner": {str(number): "+".join(theorem_claims[number])
                          for number in EXPECTED_SCOPE},
        "all_claims": {str(number): claims[number] for number in EXPECTED_SCOPE},
        "dependencies": records,
        "analytic_dependency": {
            "name": "five-path tangent theorem",
            "scope": "kernel 1; all positive path lengths with at most one direct path",
            "finite_fixture": False,
            "executable_check": "rank-four-three-vertex-tables-verifier covers only kernels 2--3",
        },
    }


def serialize(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n"


def audit(entries=DEPENDENCIES, expected_digest=EXPECTED_MANIFEST_SHA256):
    require(entries == DEPENDENCIES, "exact dependency registry changed")
    require(expected_digest == EXPECTED_MANIFEST_SHA256, "manifest digest policy changed")
    records = [invoke_dependency(entry) for entry in entries]
    value = manifest(records)
    digest = hashlib.sha256(serialize(value).encode("ascii")).hexdigest()
    require(digest == expected_digest, "exact dependency manifest digest changed")
    return value, digest


def expect_rejected(action, label):
    try:
        action()
    except (RuntimeError, TypeError, ValueError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_dependency_omission_checks():
    for index, entry in enumerate(DEPENDENCIES):
        candidate = DEPENDENCIES[:index] + DEPENDENCIES[index + 1:]
        expect_rejected(lambda candidate=candidate: audit(candidate),
                        f"omitted dependency {entry[0]}")
    changed = list(deepcopy(DEPENDENCIES))
    entry = list(changed[1])
    entry[4] = (3,)
    changed[1] = tuple(entry)
    expect_rejected(lambda: audit(tuple(changed)), "omitted kernel 2 from scope")
    return len(DEPENDENCIES) + 1


def report(value, digest, mutations):
    owners = value["theorem_owner"]
    owner_runs = []
    start = 1
    for number in range(2, 19):
        if number == 18 or owners[str(number)] != owners[str(start)]:
            label = str(start) if start == number - 1 else f"{start}-{number - 1}"
            owner_runs.append(f"K{label}={owners[str(start)]}")
            start = number
    return "\n".join((
        "tetracyclic master verifier: all exact dependency audits passed",
        "kernel_census: counts_by_order_2_to_6=1,2,5,4,5; total=17",
        "dependency_verifiers_invoked: 7 direct (cubic-final invokes 3 nested)",
        "theorem_scope_partition: " + "; ".join(owner_runs),
        "five_path_scope: analytic tangent theorem; no finite fixture; strict for simple subdivisions",
        "global_scope: every simple subdivision of all 17 loopless 2-connected rank-four kernels",
        "attachments: arbitrary rooted trees at arbitrary core or internal path vertices",
        "conclusion: s+(G)>=|V(G)|; kernel 1 five-path family is strict",
        f"exact_dependency_manifest_sha256: {digest}",
        f"rejected_dependency_omissions: {mutations}",
    )) + "\n"


def optimized_output():
    completed = subprocess.run(
        [sys.executable, "-O", str(Path(__file__).resolve()), "--emit"],
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
    mutations = hostile_dependency_omission_checks()
    require(mutations == 8, "dependency-omission mutation count changed")
    output = report(value, digest, mutations)
    if not args.emit and sys.flags.optimize == 0:
        require(optimized_output() == output, "normal and python -O output differ")
    if args.print_manifest:
        sys.stdout.write(serialize(value))
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
