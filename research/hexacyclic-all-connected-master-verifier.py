#!/usr/bin/env python3
"""Fail-closed all-connected rank-six master skeleton."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent

MULTIBLOCK = {
    "name": "canonical-multiblock-owner",
    "path": HERE / "hexacyclic-multiblock-ledger-verifier.py",
    "source_sha256": "3052fe48c2f80115259a344523d8ef7a556bea07039e405493108ffd67a37c24",
    "output_sha256": "c391247907833695586eac184379a8bd34800bc76d26a851d20dcf9903f85611",
    "arguments": ("--print-manifest",),
    "schema": "hexacyclic-multiblock-scope-conclusion-v1",
    "block_scope": "at-least-two-positive-rank-cyclic-blocks",
}

# This owner is deliberately unregistered until the orders 2--10 master has
# four exact replay owners and its canonical output has been frozen.
SINGLE_BLOCK = {
    "name": "rank-six-orders2-10-owner",
    "path": HERE / "rank-six-order2-10-master-verifier.py",
    "source_sha256": None,
    "output_sha256": None,
    "arguments": ("--emit", "--print-manifest"),
    "schema": "rank-six-order2-10-master-implication-v1",
    "block_scope": "exactly-one-positive-rank-cyclic-block",
}

OWNERS = (MULTIBLOCK, SINGLE_BLOCK)
PARTITIONS = {
    (1, 1, 1, 1, 1, 1),
    (2, 1, 1, 1, 1),
    (2, 2, 1, 1),
    (2, 2, 2),
    (3, 1, 1, 1),
    (3, 2, 1),
    (3, 3),
    (4, 1, 1),
    (4, 2),
    (5, 1),
    (6,),
}
EXPECTED_CONCLUSION = {
    "quantity": "s+(G)",
    "relation": ">=",
    "bound": "|V(G)|",
    "statement": "s+(G)>=|V(G)|",
    "strict": False,
}
FORBIDDEN_PROMOTION_KEYS = {
    "ready_for_theorem_promotion", "theorem_claimed", "status",
    "conditional", "draft", "completion_status",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def strict_json_bytes(raw, label):
    def pairs(rows):
        result = {}
        for key, value in rows:
            require(key not in result, f"duplicate key in {label}: {key}")
            result[key] = value
        return result

    def reject_constant(value):
        raise RuntimeError(f"nonstandard JSON constant in {label}: {value}")

    try:
        payload = json.loads(raw.decode("ascii"), object_pairs_hook=pairs,
                             parse_constant=reject_constant)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"cannot parse {label}: {error}") from error
    require(raw == canonical_bytes(payload), f"{label} is not canonical ASCII JSON")
    return payload


def integer_partitions(total, maximum=None):
    if total == 0:
        return {()}
    if maximum is None or maximum > total:
        maximum = total
    result = set()
    for first in range(maximum, 0, -1):
        for suffix in integer_partitions(total - first, first):
            result.add((first,) + suffix)
    return result


def analytic_block_split(partitions=PARTITIONS):
    generated = integer_partitions(6)
    require(partitions == generated == PARTITIONS,
            "positive cyclic-block ranks are not the exact partitions of six")
    multiblock = partitions - {(6,)}
    single_block = partitions & {(6,)}
    require(len(multiblock) == 10 and single_block == {(6,)},
            "analytic branch widths changed")
    require(multiblock.isdisjoint(single_block), "analytic branches overlap")
    require(multiblock | single_block == partitions, "analytic branches are not exhaustive")
    return {
        "lemma": "cyclomatic rank is the sum of positive-rank cyclic-block ranks",
        "justification": "adjoining a block at one cut vertex adds |E(B)|-|V(B)|+1",
        "all_partitions": [list(row) for row in sorted(partitions, reverse=True)],
        "multiblock_partitions": [list(row) for row in sorted(multiblock, reverse=True)],
        "single_block_partitions": [[6]],
        "branch_predicates": [
            "at-least-two-positive-rank-cyclic-blocks",
            "exactly-one-positive-rank-cyclic-block",
        ],
        "disjoint": True,
        "exhaustive": True,
    }


def walk_keys(payload):
    if isinstance(payload, dict):
        for key, value in payload.items():
            yield key
            yield from walk_keys(value)
    elif isinstance(payload, list):
        for value in payload:
            yield from walk_keys(value)


def validate_conclusion(conclusion, owner_name):
    require(conclusion == EXPECTED_CONCLUSION,
            f"nonstrict conclusion changed: {owner_name}")


def validate_multiblock(manifest):
    require(manifest.get("schema") == MULTIBLOCK["schema"],
            "multiblock schema changed")
    require(manifest.get("scope") == {
        "graph": "finite simple connected",
        "cyclomatic_rank": 6,
        "edge_vertex_relation": "|E(G)|=|V(G)|+5",
        "block_scope": MULTIBLOCK["block_scope"],
        "block_rank_partitions": [
            list(row) for row in sorted(PARTITIONS - {(6,)}, reverse=True)
        ],
    }, "multiblock scope or exact partition list changed")
    validate_conclusion(manifest.get("conclusion"), MULTIBLOCK["name"])
    ledger = manifest.get("ledger", {})
    require(ledger == {
        "integer_partitions": 11,
        "multiblock_partitions": 10,
        "packets": 9,
        "presieve_rows": 5,
        "rank5_structural_families": 3,
        "owner_cases": 12,
    }, "multiblock owner-exact ledger changed")


def validate_single_block(manifest):
    require(manifest.get("schema") == SINGLE_BLOCK["schema"],
            "single-block schema changed")
    require(manifest.get("evidence_kind") == "exact-theorem-owner",
            "single-block evidence is not an exact theorem owner")
    require(manifest.get("scope") == {
        "graph": "finite simple connected",
        "cyclomatic_rank": 6,
        "edge_vertex_relation": "|E(G)|=|V(G)|+5",
        "block_scope": SINGLE_BLOCK["block_scope"],
    }, "single-block scope changed")
    validate_conclusion(manifest.get("conclusion"), SINGLE_BLOCK["name"])
    require(manifest.get("orders") == list(range(2, 11)),
            "single-block orders are not exactly 2 through 10")
    require(manifest.get("counts_by_order_2_to_10") ==
            [1, 4, 26, 84, 216, 314, 325, 162, 66],
            "single-block order counts changed")
    require(manifest.get("kernel_interval") == [1, 1198] and
            manifest.get("kernel_count") == 1198,
            "single-block kernel universe changed")
    dependencies = manifest.get("dependencies")
    require(type(dependencies) is list and len(dependencies) == 6,
            "single-block exact dependency registry changed")
    require([row.get("name") for row in dependencies] ==
            ["kernel-census", "conditional-analytic-lift", "orders-2-7", "order-8",
             "order-9-promotion", "order-10-promotion"],
            "single-block owner registry changed")
    require(all(row.get("replay") in {"full-exact", "independent-exact-census",
                                      "exact-conditional-interface"}
                and isinstance(row.get("source_sha256"), str)
                and isinstance(row.get("output_sha256"), str)
                for row in dependencies),
            "single-block owner lacks frozen exact replay evidence")
    require(not (set(walk_keys(manifest)) & FORBIDDEN_PROMOTION_KEYS),
            "draft, conditional, or status-only promotion field rejected")


def parse_owner_output(stdout, owner):
    if owner is MULTIBLOCK:
        raw = stdout.encode("ascii")
    else:
        first, separator, remainder = stdout.partition("\n")
        require(separator == "\n" and remainder,
                "single-block owner omitted its exact audit report")
        raw = (first + "\n").encode("ascii")
    return strict_json_bytes(raw, f"{owner['name']} manifest")


def invoke(owner):
    name = owner["name"]
    require(owner["source_sha256"] is not None,
            f"unregistered theorem-owner source: {name}")
    require(owner["output_sha256"] is not None,
            f"unregistered canonical theorem-owner output: {name}")
    require(owner["path"].is_file(), f"missing theorem owner: {name}")
    require(hashlib.sha256(owner["path"].read_bytes()).hexdigest() ==
            owner["source_sha256"], f"theorem-owner source changed: {name}")
    optimize = ("-O",) if sys.flags.optimize else ()
    completed = subprocess.run(
        (sys.executable, *optimize, str(owner["path"]), *owner["arguments"]),
        check=False, capture_output=True, text=True,
    )
    require(completed.returncode == 0, f"theorem owner failed: {name}")
    require(completed.stderr == "", f"theorem owner wrote stderr: {name}")
    require(hashlib.sha256(completed.stdout.encode("ascii")).hexdigest() ==
            owner["output_sha256"], f"canonical theorem-owner output changed: {name}")
    manifest = parse_owner_output(completed.stdout, owner)
    (validate_multiblock if owner is MULTIBLOCK else validate_single_block)(manifest)
    return {
        "name": name,
        "schema": owner["schema"],
        "block_scope": owner["block_scope"],
        "source_sha256": owner["source_sha256"],
        "output_sha256": owner["output_sha256"],
        "evidence": "canonical-exact-owner-manifest",
    }


def root_manifest(dependencies, split):
    require(len(dependencies) == 2, "both proof branches are mandatory")
    return {
        "schema": "hexacyclic-all-connected-master-v1",
        "evidence_kind": "exact-two-branch-theorem",
        "scope": {
            "graph": "finite simple connected",
            "cyclomatic_rank": 6,
            "edge_vertex_relation": "|E(G)|=|V(G)|+5",
            "block_scope": "all-positive-rank-block-configurations",
        },
        "analytic_block_split": split,
        "dependencies": dependencies,
        "conclusion": EXPECTED_CONCLUSION,
        "excluded_claims": [
            "strict inequality",
            "equality classification",
            "edge or subdivision monotonicity",
            "status-only, draft, or conditional promotion",
        ],
    }


def expect_rejected(action, label):
    try:
        action()
    except (RuntimeError, TypeError, ValueError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_self_checks():
    checks = 0
    for missing in PARTITIONS:
        expect_rejected(lambda missing=missing: analytic_block_split(PARTITIONS - {missing}),
                        f"partition omitted: {missing}")
        checks += 1
    overlap = deepcopy(PARTITIONS)
    overlap.remove((6,))
    expect_rejected(lambda: analytic_block_split(overlap), "single branch omitted")
    checks += 1
    bad_conclusion = dict(EXPECTED_CONCLUSION)
    bad_conclusion["relation"] = ">"
    bad_conclusion["statement"] = "s+(G)>|V(G)|"
    bad_conclusion["strict"] = True
    expect_rejected(lambda: validate_conclusion(bad_conclusion, "mutation"),
                    "strict promotion")
    checks += 1
    status_only = {
        "schema": SINGLE_BLOCK["schema"],
        "evidence_kind": "exact-theorem-owner",
        "ready_for_theorem_promotion": True,
    }
    expect_rejected(lambda: validate_single_block(status_only), "status-only owner")
    checks += 1
    conditional = {
        "schema": SINGLE_BLOCK["schema"],
        "evidence_kind": "conditional-implication",
    }
    expect_rejected(lambda: validate_single_block(conditional), "conditional owner")
    checks += 1
    missing_lift = {
        "schema": SINGLE_BLOCK["schema"],
        "evidence_kind": "exact-theorem-owner",
        "scope": {
            "graph": "finite simple connected",
            "cyclomatic_rank": 6,
            "edge_vertex_relation": "|E(G)|=|V(G)|+5",
            "block_scope": SINGLE_BLOCK["block_scope"],
        },
        "conclusion": EXPECTED_CONCLUSION,
        "orders": list(range(2, 11)),
        "counts_by_order_2_to_10": [1, 4, 26, 84, 216, 314, 325, 162, 66],
        "kernel_interval": [1, 1198],
        "kernel_count": 1198,
        "dependencies": [
            {"name": name, "replay": "full-exact", "source_sha256": "0" * 64,
             "output_sha256": "0" * 64}
            for name in ("kernel-census", "orders-2-7", "order-8",
                         "order-9-promotion", "order-10-promotion")
        ],
    }
    expect_rejected(lambda: validate_single_block(missing_lift),
                    "conditional analytic lift omitted")
    checks += 1
    return checks


def audit():
    split = analytic_block_split()
    require(hostile_self_checks() == 16, "hostile mutation count changed")
    blockers = [owner["name"] for owner in OWNERS
                if owner["source_sha256"] is None or owner["output_sha256"] is None
                or not owner["path"].is_file()]
    require(not blockers, "all-connected promotion gate closed: " + ", ".join(blockers))
    dependencies = [invoke(owner) for owner in OWNERS]
    return root_manifest(dependencies, split)


def optimized_output():
    completed = subprocess.run(
        (sys.executable, "-O", str(Path(__file__).resolve()), "--emit"),
        check=False, capture_output=True, text=True,
    )
    require(completed.returncode == 0, "python -O all-connected master failed")
    require(completed.stderr == "", "python -O all-connected master wrote stderr")
    return completed.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--print-manifest", action="store_true")
    args = parser.parse_args()
    try:
        manifest = audit()
    except (OSError, RuntimeError, TypeError, ValueError) as error:
        sys.stderr.write(f"hexacyclic all-connected master: FAIL CLOSED: {error}\n")
        return 1
    if args.print_manifest:
        sys.stdout.write(canonical_bytes(manifest).decode("ascii"))
    output = "hexacyclic all-connected master audit passed\n"
    if not args.emit and not args.print_manifest and sys.flags.optimize == 0:
        require(optimized_output() == output, "normal and python -O output differ")
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
