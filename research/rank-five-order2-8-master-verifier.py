#!/usr/bin/env python3
"""Fail-closed implication audit for all 118 rank-five suppressed kernels."""

import argparse
import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
KERNEL_FIXTURE = HERE / "fixtures" / "rank-five-kernels.json"
KERNEL_SHA256 = "027c84d6dd777a29b3dc93389ab30b5d43f6507eddceb4ea286f1240da95b884"
ORDER_COUNTS = (1, 3, 13, 24, 38, 23, 16)
CENSUS = (
    "exact-census",
    HERE / "rank-five-kernel-census-verifier.py",
    "865cef39509530679374aca0df3ea7d98436452487e767098784358cf28c09e8",
    (),
    "canonical_counts_n2_to_n8: 1,3,13,24,38,23,16 (total 118)",
    "classification",
)
THEOREMS = (
    ("orders-2-4", HERE / "rank-five-low-order-master-verifier.py",
     "0440ac32c22963589910aa26d3df049e5efa619436fd0feef21efb1b78f6878c",
     ("--emit",), "conclusion: s+(G)>=|V(G)| for every selected kernel subdivision",
     "orders=2,3,4;rows=1,3,13"),
    ("order-5-main", ROOT / "pentacyclic" / "research" / "order5-kernel-family-theorem-verifier.py",
     "fc7c294f1c272cc1da01f8928032f0e0d9c29636b7f1fbde8455ae65533bcccf",
     (), "excluded_without_claim=K32_all_odd_K5-e", "order=5;rows=24;except=K32-all-odd"),
    ("order-5-K5e", ROOT / "pentacyclic" / "research" / "all-odd-k5e-theorem-verifier.py",
     "43a64e32f91382980d908038530d52ffca8e06ceaca43dbee683b6ae0b241334",
     (), "all-odd K5-e theorem verifier: PASS", "order=5;only=K32-all-odd"),
    ("order-6", ROOT / "pentacyclic" / "research" / "order6-kernel-family-theorem-verifier.py",
     "67b356163b8659b9bf0c5327877a7767408dd7f0b7f956c8bf45388f6c941642",
     (), "order-six rank-five kernel-family theorem: exact audit passed", "order=6;rows=38"),
    ("order-7", ROOT / "pentacyclic" / "research" / "order7-kernel-family-theorem-verifier.py",
     "e1dcd7a8d42fbc623d372529bcd0b2b887ff82420a19b3f7986c4acdc0fcebe0",
     (), "order-seven rank-five kernel-family theorem: exact audit passed", "order=7;rows=23"),
    ("order-8", ROOT / "pentacyclic" / "research" / "order8-kernel-family-theorem-verifier.py",
     "bd95d469ca99195caf6fabba1936156c868565be3bad1a3ce60770d45d93d2ab",
     ("--emit",), "order-eight rank-five kernel-family theorem: exact audit passed", "order=8;rows=16"),
)
EXPECTED_COVERAGE = tuple(entry[5] for entry in THEOREMS)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def audit_fixture():
    try:
        raw = KERNEL_FIXTURE.read_bytes()
        payload = json.loads(raw)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"cannot load kernel fixture: {error}") from error
    require(hashlib.sha256(raw).hexdigest() == KERNEL_SHA256, "kernel fixture digest changed")
    require(raw == canonical_bytes(payload), "kernel fixture is not canonical JSON")
    require(payload.get("beta") == 5 and payload.get("orders") == [2, 8],
            "kernel fixture scope changed")
    rows = payload.get("kernels", ())
    counts = tuple(sum(record.get("n") == order for record in rows) for order in range(2, 9))
    require(counts == ORDER_COUNTS and len(rows) == 118, "order 2-8 kernel partition changed")
    return counts


def validate_registry(census=CENSUS, theorems=THEOREMS):
    require(census == CENSUS, "exact census dependency changed")
    require(theorems == THEOREMS, "theorem dependency registry changed")
    require(tuple(entry[5] for entry in theorems) == EXPECTED_COVERAGE,
            "theorem scope partition changed")
    require(len({entry[0] for entry in (census,) + theorems}) == 7,
            "dependency names are not unique")


def invoke(entry):
    name, path, digest, arguments, required_line, unused_scope = entry
    require(path.is_file(), f"missing exact dependency: {name}")
    require(hashlib.sha256(path.read_bytes()).hexdigest() == digest,
            f"dependency file digest changed: {name}")
    optimize = ("-O",) if sys.flags.optimize else ()
    completed = subprocess.run((sys.executable, *optimize, str(path), *arguments),
                               check=False, capture_output=True, text=True)
    require(completed.returncode == 0, f"exact dependency failed: {name}")
    require(completed.stderr == "", f"exact dependency wrote stderr: {name}")
    require(required_line in completed.stdout, f"dependency acceptance ledger changed: {name}")
    return {
        "name": name,
        "file_sha256": digest,
        "output_sha256": hashlib.sha256(completed.stdout.encode("utf-8")).hexdigest(),
        "scope": entry[5],
    }


def audit(census=CENSUS, theorems=THEOREMS):
    validate_registry(census, theorems)
    counts = audit_fixture()
    records = tuple(invoke(entry) for entry in (census,) + theorems)
    manifest = {
        "schema": "rank-five-order2-8-master-verifier-v1",
        "kernel_fixture_sha256": KERNEL_SHA256,
        "counts_by_order_2_to_8": list(counts),
        "dependencies": records,
        "scope": "all simple subdivisions of the 118 rank-five suppressed kernels",
        "attachments": "arbitrary rooted trees at arbitrary subdivision vertices",
        "conclusion": "s+(G)>=|V(G)|",
        "excluded_claim": "connected pentacyclic graphs with multiple cyclic blocks",
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
    entry = list(changed[2])
    entry[5] = "order=5;rows=24"
    changed[2] = tuple(entry)
    expect_rejected(lambda: validate_registry(CENSUS, tuple(changed)), "K5-e scope widened")
    mutations += 1
    changed_census = list(CENSUS)
    changed_census[2] = "0" * 64
    expect_rejected(lambda: validate_registry(tuple(changed_census), THEOREMS),
                    "census digest changed")
    mutations += 1
    return mutations


def report(digest, mutations):
    return "\n".join((
        "rank-five order-2-8 master verifier: all exact audits passed",
        "kernel_census: counts=1+3+13+24+38+23+16=118",
        "theorem_owners: orders2-4 + order5-main/K5-e + order6 + order7 + order8",
        "scope: every simple subdivision; arbitrary rooted-tree attachments",
        "conclusion: s+(G)>=|V(G)| for every selected single-block family",
        "nonclaim: connected pentacyclic multiblock graphs are not concluded here",
        f"exact_dependency_manifest_sha256: {digest}",
        f"rejected_hostile_mutations: {mutations}",
    )) + "\n"


def optimized_output():
    completed = subprocess.run((sys.executable, "-O", str(Path(__file__).resolve()), "--emit"),
                               check=False, capture_output=True, text=True)
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
    require(mutations == 9, "hostile mutation count changed")
    output = report(digest, mutations)
    if not args.emit and sys.flags.optimize == 0:
        require(optimized_output() == output, "normal and python -O output differ")
    if args.print_manifest:
        sys.stdout.write(canonical_bytes(manifest).decode("ascii"))
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
