#!/usr/bin/env python3
"""Fail-closed rank-seven single-block master skeleton for orders 2 through 12."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CENSUS = ROOT / "research/fixtures/rank-seven-kernel-frontier-census.json"
CENSUS_SHA256 = "a241139ab54ce4cce1ab3812887359edb241c0abfb1018e804b4a5f86762cfd5"
ORDER_COUNTS = (1, 6, 47, 233, 914, 2270, 4015, 4495, 3396, 1391, 365)
COMPLETED = (
    {"name": "orders-2-4", "orders": (2, 3, 4), "kernel_count": 54,
     "path": HERE / "rank-seven-orders2-4-kernel-theorem-verifier.py",
     "source_sha256": "7332b98f7f0780faff038e758451bb53cdebbb6f4c90c3f0785649be5064ec7d",
     "arguments": ("--emit",),
     "output_lines": ("rank-seven orders2-4 kernel theorem: exact hostile audit passed",
                      "conclusion: s+(G)>=|V(G)| for rank-seven kernel orders 2 through 4")},
    {"name": "order-5", "orders": (5,), "kernel_count": 233,
     "path": HERE / "rank-seven-order-five-kernel-theorem-verifier.py",
     "source_sha256": "c2a072cfd38b461151495b4cc3bbebcbc9af4f3fae23fc9fc9263ddea5759f64",
     "arguments": ("--emit",),
     "output_lines": ("rank-seven order-five kernel theorem: exact fail-closed audit passed",
                      "conclusion=s+(G)>=|V(G)| for rank-seven kernel order five only")},
    {"name": "order-6", "orders": (6,), "kernel_count": 914,
     "path": HERE / "rank-seven-order-six-kernel-theorem-verifier.py",
     "source_sha256": "730328936de82a57697945a1accf80fd1c3d8b85bb8c0731575060dda39b551d", "arguments": (),
     "output_lines": ("rank-seven order-six kernel theorem: exact audit passed",
                      "conclusion=s+(G)>=|V(G)| for rank-seven kernel order six only")},
)
PLACEHOLDERS = tuple({
    "name": f"order-{order}", "orders": (order,),
    "kernel_count": ORDER_COUNTS[order - 2], "path": None,
    "source_sha256": None, "output_sha256": None,
    "status": "blocked-unregistered-exact-owner",
} for order in range(7, 13))
ANALYTIC_LIFT = {
    "name": "conditional-analytic-lift-budget-6",
    "path": HERE / "rank-seven-conditional-analytic-lift-verifier.py",
    "source_sha256": "55e7d67a670f22a7b872b122f3aadcd2036ba922993f5faac1c5b72e2232e611",
    "arguments": ("--print-manifest",),
    "schema": "rank-seven-conditional-analytic-lift-v1",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def audit_census():
    raw = CENSUS.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == CENSUS_SHA256, "kernel census digest changed")
    payload = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(payload), "kernel census is not canonical ASCII JSON")
    require(payload.get("beta") == 7 and payload.get("orders") == [2, 12] and
            payload.get("counts_by_order_n2_to_n12") == list(ORDER_COUNTS),
            "kernel census scope or exact order partition changed")
    return payload


def validate_registry(completed=COMPLETED, placeholders=PLACEHOLDERS):
    completed_orders = tuple(order for owner in completed for order in owner["orders"])
    placeholder_orders = tuple(order for owner in placeholders for order in owner["orders"])
    require(completed_orders == tuple(range(2, 7)), "completed orders are not exactly 2 through 6")
    require(placeholder_orders == tuple(range(7, 13)),
            "placeholder orders are not exactly 7 through 12")
    require(set(completed_orders).isdisjoint(placeholder_orders), "order owners overlap")
    require(set(completed_orders) | set(placeholder_orders) == set(range(2, 13)),
            "order owners are not exhaustive")
    require(sum(owner["kernel_count"] for owner in completed + placeholders) ==
            sum(ORDER_COUNTS), "kernel owner counts do not partition the census")
    require(all(owner["path"] is None and owner["source_sha256"] is None and
                owner["output_sha256"] is None and
                owner["status"] == "blocked-unregistered-exact-owner"
                for owner in placeholders), "placeholder silently registered an owner")


def invoke_completed(owner):
    require(owner["path"].is_file(), f"missing completed owner: {owner['name']}")
    digest = hashlib.sha256(owner["path"].read_bytes()).hexdigest()
    require(owner["source_sha256"] == digest, f"completed owner digest changed: {owner['name']}")
    command = [sys.executable]
    if sys.flags.optimize:
        command.append("-O")
    command.extend((str(owner["path"]), *owner["arguments"]))
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    require(completed.returncode == 0 and completed.stderr == "",
            f"completed owner failed: {owner['name']}")
    require(all(line in completed.stdout for line in owner["output_lines"]),
            f"completed owner output changed: {owner['name']}")
    return {"name": owner["name"], "orders": list(owner["orders"]),
            "kernel_count": owner["kernel_count"], "status": "completed-exact-owner",
            "source_sha256": digest,
            "output_sha256": hashlib.sha256(completed.stdout.encode("ascii")).hexdigest()}


def invoke_lift():
    require(ANALYTIC_LIFT["path"].is_file(), "conditional analytic lift is missing")
    digest = hashlib.sha256(ANALYTIC_LIFT["path"].read_bytes()).hexdigest()
    require(ANALYTIC_LIFT["source_sha256"] == digest, "analytic lift digest changed")
    completed = subprocess.run((sys.executable, str(ANALYTIC_LIFT["path"]),
                                *ANALYTIC_LIFT["arguments"]),
                               check=False, capture_output=True, text=True)
    require(completed.returncode == 0 and completed.stderr == "", "analytic lift failed")
    first, separator, report = completed.stdout.partition("\n")
    require(separator and report, "analytic lift omitted report")
    manifest = json.loads(first)
    require(manifest.get("schema") == ANALYTIC_LIFT["schema"] and
            manifest.get("budget") == 6 and manifest.get("global_claim") is False and
            manifest.get("finite_premise_discharged") is False,
            "analytic lift lost its conditional nonclaim boundary")
    return {"name": ANALYTIC_LIFT["name"], "budget": 6,
            "status": "registered-conditional-interface", "source_sha256": digest}


def blockers():
    return [{"name": owner["name"], "orders": list(owner["orders"]),
             "kernel_count": owner["kernel_count"], "reason": owner["status"]}
            for owner in PLACEHOLDERS]


def hostile_checks():
    count = 0
    for index in range(len(PLACEHOLDERS)):
        changed = PLACEHOLDERS[:index] + PLACEHOLDERS[index + 1:]
        try:
            validate_registry(COMPLETED, changed)
        except (RuntimeError, TypeError):
            count += 1
        else:
            raise RuntimeError("omitted placeholder accepted")
    changed = deepcopy(PLACEHOLDERS)
    changed[0]["path"] = HERE / "forged.py"
    try:
        validate_registry(COMPLETED, changed)
    except (RuntimeError, TypeError):
        count += 1
    else:
        raise RuntimeError("silent placeholder promotion accepted")
    return count


def audit():
    audit_census()
    validate_registry()
    require(hostile_checks() == 7, "hostile blocker count changed")
    completed = [invoke_completed(owner) for owner in COMPLETED]
    lift = invoke_lift()
    open_blockers = blockers()
    require(open_blockers, "skeleton unexpectedly has no blockers")
    return {
        "schema": "rank-seven-order2-12-master-skeleton-v1",
        "evidence_kind": "fail-closed-incomplete-master-skeleton",
        "scope": {"rank": 7, "block_scope": "exactly-one-positive-rank-cyclic-block",
                  "kernel_orders": [2, 12], "kernel_count": sum(ORDER_COUNTS)},
        "exact_order_partition": {"completed": list(range(2, 7)),
                                  "blocked": list(range(7, 13))},
        "counts_by_order_2_to_12": list(ORDER_COUNTS),
        "completed_owners": completed,
        "placeholders": open_blockers,
        "conditional_analytic_lift": lift,
        "promotion_gate": {"open": False, "blockers": [row["name"] for row in open_blockers]},
        "global_claim": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-manifest", action="store_true")
    args = parser.parse_args()
    try:
        manifest = audit()
    except (OSError, RuntimeError, TypeError, ValueError, json.JSONDecodeError) as error:
        sys.stderr.write(f"rank-seven orders2-12 master skeleton: FAIL CLOSED: {error}\n")
        return 1
    if args.print_manifest:
        sys.stdout.write(canonical_bytes(manifest).decode("ascii"))
    sys.stdout.write("rank-seven orders2-12 master skeleton audit passed\n"
                     "completed_orders=2-6 blocked_orders=7-12 budget=6\n"
                     "promotion_gate=closed global_claim=false\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
