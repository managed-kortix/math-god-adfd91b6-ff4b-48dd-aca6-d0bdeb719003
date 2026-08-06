#!/usr/bin/env python3
"""Fail-closed implication audit for rank-six kernels of orders two through seven."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent
KERNEL_FIXTURE = HERE / "fixtures" / "rank-six-kernels.json"
KERNEL_SHA256 = "5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476"
ORDER_COUNTS = (1, 4, 26, 84, 216, 314)
CENSUS = (
    "exact-census",
    HERE / "rank-six-kernel-census-verifier.py",
    "325b78066b626a00deaceb6a026377dd7f898a906c63c597f77831548585e1ee",
    "canonical_counts_n2_to_n10: 1,4,26,84,216,314,325,162,66 (total 1198)",
    "classification=orders2-10;selected=orders2-7",
)
THEOREMS = (
    (
        "orders-2-4",
        HERE / "rank-six-low-order-master-verifier.py",
        "aa440adb33e7315cf8abe1d83d7d201e3faacb50d6b67900cce133397c8de458",
        "rank-six low-order master theorem: all exact audits passed",
        "orders=2,3,4;rows=1,4,26",
    ),
    (
        "order-5",
        HERE / "rank-six-order-five-kernel-theorem-verifier.py",
        "7c6f4048f9c4bf955aaab71a2e92aaec36cf6ba6aa7d6feaa2fff50fe2881046",
        "rank-six order-five kernel theorem: exact audit passed",
        "order=5;rows=84",
    ),
    (
        "order-6",
        HERE / "rank-six-order-six-kernel-theorem-verifier.py",
        "e4b5b21900eafd41910ab7fda7f0b178effaef37411cfb36da983d9f8686a46c",
        "rank-six order-six kernel theorem: exact audit passed",
        "order=6;rows=216",
    ),
    (
        "order-7",
        HERE / "rank-six-order-seven-equality-frontier-verifier.py",
        "a9806d2a6a8fc1e7c93b3c0b6ec18cef84a7184e15b25cae4455e2cb5b4f4457",
        "batched_exact=319163 equality_exact=39 frontier_targets=319202",
        "order=7;rows=314",
    ),
)
EXPECTED_COVERAGE = tuple(entry[4] for entry in THEOREMS)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def load_json(raw):
    def reject_constant(value):
        raise ValueError(f"nonstandard JSON constant: {value}")

    return json.loads(raw.decode("ascii"), parse_constant=reject_constant)


def audit_fixture():
    try:
        raw = KERNEL_FIXTURE.read_bytes()
        payload = load_json(raw)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        raise RuntimeError(f"cannot load kernel fixture: {error}") from error
    require(hashlib.sha256(raw).hexdigest() == KERNEL_SHA256,
            "rank-six kernel fixture digest changed")
    require(raw == canonical_bytes(payload), "rank-six kernel fixture is not canonical JSON")
    require(payload.get("beta") == 6 and payload.get("orders") == [2, 10],
            "rank-six kernel fixture scope changed")
    rows = payload.get("kernels")
    require(type(rows) is list, "rank-six kernel rows are malformed")
    counts = tuple(sum(record.get("n") == order for record in rows)
                   for order in range(2, 8))
    require(counts == ORDER_COUNTS and sum(counts) == 645,
            "order 2-7 kernel partition changed")
    require(sum(record.get("n") >= 8 for record in rows) == 553,
            "unproved order 8-10 boundary changed")
    return counts


def validate_registry(census=CENSUS, theorems=THEOREMS):
    require(census == CENSUS, "exact census dependency changed")
    require(theorems == THEOREMS, "theorem dependency registry changed")
    require(tuple(entry[4] for entry in theorems) == EXPECTED_COVERAGE,
            "theorem scope partition changed")
    require(len({entry[0] for entry in (census,) + theorems}) == 5,
            "dependency names are not unique")


def invoke(entry):
    name, path, digest, required_line, scope = entry
    require(path.is_file(), f"missing exact dependency: {name}")
    require(hashlib.sha256(path.read_bytes()).hexdigest() == digest,
            f"dependency file digest changed: {name}")
    optimize = ("-O",) if sys.flags.optimize else ()
    completed = subprocess.run(
        (sys.executable, *optimize, str(path), "--emit"),
        check=False,
        capture_output=True,
        text=True,
    )
    require(completed.returncode == 0, f"exact dependency failed: {name}")
    require(completed.stderr == "", f"exact dependency wrote stderr: {name}")
    require(required_line in completed.stdout,
            f"dependency acceptance ledger changed: {name}")
    return {
        "name": name,
        "file_sha256": digest,
        "output_sha256": hashlib.sha256(completed.stdout.encode("utf-8")).hexdigest(),
        "scope": scope,
    }


def audit(census=CENSUS, theorems=THEOREMS):
    validate_registry(census, theorems)
    counts = audit_fixture()
    dependencies = tuple(invoke(entry) for entry in (census,) + theorems)
    manifest = {
        "schema": "rank-six-order2-7-master-verifier-v1",
        "kernel_fixture_sha256": KERNEL_SHA256,
        "counts_by_order_2_to_7": list(counts),
        "dependencies": dependencies,
        "scope": "all simple subdivisions of the 645 rank-six kernels of orders 2 through 7",
        "attachments": "arbitrary rooted trees at arbitrary subdivision vertices",
        "conclusion": "s+(G)>=|V(G)|",
        "excluded_claims": [
            "rank-six kernels of orders 8 through 10",
            "all connected hexacyclic graphs",
        ],
    }
    return manifest, hashlib.sha256(canonical_bytes(manifest)).hexdigest()


def expect_rejected(action, label):
    try:
        action()
    except (RuntimeError, TypeError, ValueError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_self_checks():
    mutations = 0
    expect_rejected(lambda: validate_registry(None, THEOREMS), "census omitted")
    mutations += 1
    for index, entry in enumerate(THEOREMS):
        candidate = THEOREMS[:index] + THEOREMS[index + 1:]
        expect_rejected(lambda candidate=candidate: validate_registry(CENSUS, candidate),
                        f"theorem omitted: {entry[0]}")
        mutations += 1
    changed = list(deepcopy(THEOREMS))
    entry = list(changed[-1])
    entry[4] = "order=7;rows=314;implies=all-hexacyclic"
    changed[-1] = tuple(entry)
    expect_rejected(lambda: validate_registry(CENSUS, tuple(changed)),
                    "order-seven scope widened")
    mutations += 1
    changed_census = list(CENSUS)
    changed_census[2] = "0" * 64
    expect_rejected(lambda: validate_registry(tuple(changed_census), THEOREMS),
                    "census digest changed")
    mutations += 1
    return mutations


def report(digest, mutations):
    return "\n".join((
        "rank-six order-2-7 master verifier: all exact audits passed",
        "kernel_census: counts=1+4+26+84+216+314=645",
        "theorem_owners: orders2-4 + order5 + order6 + order7",
        "order7_frontier: rational=319163 equality=39 total=319202",
        "scope: every simple subdivision; arbitrary rooted-tree attachments",
        "conclusion: s+(G)>=|V(G)| for every selected single-block family",
        "nonclaim: orders8-10 and all connected hexacyclic graphs are not concluded here",
        f"exact_dependency_manifest_sha256: {digest}",
        f"rejected_hostile_mutations: {mutations}",
    )) + "\n"


def optimized_output():
    completed = subprocess.run(
        (sys.executable, "-O", str(Path(__file__).resolve()), "--emit"),
        check=False,
        capture_output=True,
        text=True,
    )
    require(completed.returncode == 0, "python -O master verifier failed")
    require(completed.stderr == "", "python -O master verifier wrote stderr")
    return completed.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--print-manifest", action="store_true")
    args = parser.parse_args()
    manifest, digest = audit()
    mutations = hostile_self_checks()
    require(mutations == 7, "hostile mutation count changed")
    output = report(digest, mutations)
    if not args.emit and sys.flags.optimize == 0:
        require(optimized_output() == output, "normal and python -O output differ")
    if args.print_manifest:
        sys.stdout.write(canonical_bytes(manifest).decode("ascii"))
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
