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
    "source_sha256": "37d544d1dcbcdac0b154d2f6008f3aa3a81bf805ee87e807a4f1b98ffbbc2b30",
    "output_sha256": "60fbcbae34101b17d429dc202a463e7d9c08c6486055ac88e4c15b41898c3c0a",
    "arguments": ("--print-manifest",),
    "schema": "hexacyclic-multiblock-scope-conclusion-v1",
    "block_scope": "at-least-two-positive-rank-cyclic-blocks",
}

SINGLE_BLOCK = {
    "name": "rank-six-orders2-10-owner",
    "path": HERE / "rank-six-order2-10-master-verifier.py",
    "source_sha256": "21aabed4eee24f36dc9ddf0460423d0fdd6d20a56e80a60ffed69c796c163bf1",
    "output_sha256": "e32149c665638e1d9cd08f8050cd4a7c7cae9f76c51b49f9cda3e0cfb2645834",
    "execution_evidence_path": HERE / "rank-six-order2-10-child-execution-evidence.json",
    "execution_evidence_sha256": "bbbb8eff45f8009dfb49e926c4952ae0b231ed6e02e708bddfb13b4aac17bb5d",
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
    sector = manifest.get("pentagon_sector_execution_m3")
    require(type(sector) is dict, "multiblock m=3 sector receipt omitted")
    require(sector.get("file_sha256") ==
            "9c143530e6ffa2b9c1255236927fa3c75e9bc54a7fa77b6fcdd6c83b665340da",
            "multiblock m=3 sector verifier receipt changed")
    require(sector.get("output_sha256") ==
            "0f765321830d96f0d84845ee6961a158177d003df0f84d10a5b13ce3236b7030",
            "multiblock m=3 sector output receipt changed")
    require(sector.get("scope") ==
            "bridge-free D+C5+3C3 pentagon sectors (m=3)",
            "multiblock m=3 sector scope receipt changed")
    require(sector.get("block_node_trees") == 125 and
            sector.get("weighted_encodings") == 3149280 and
            sector.get("relevant_encodings") == 1667520 and
            sector.get("leaf_encodings") == 1481760,
            "multiblock m=3 sector census receipt changed")
    sector_required = sector.get("required_lines")
    require(type(sector_required) is list and
            "credit lower endpoint min(4-h) 1" in sector_required and
            "EXACT SECTOR CHECK: PASS" in sector_required,
            "multiblock m=3 sector acceptance ledger changed")
    receipt = manifest.get("diamond_two_triangle_execution")
    require(type(receipt) is dict, "multiblock DTT execution receipt omitted")
    require(receipt.get("note_sha256") ==
            "9107ef2821d441da401079982ae8d0b6c98cee17ae7e52268a9b6ad895b8e11b",
            "multiblock DTT note receipt changed")
    require(receipt.get("file_sha256") ==
            "24da5324c6695de4795fbd7885fbeadf986fabe1b52e2aec2082c92223addc9a",
            "multiblock DTT verifier receipt changed")
    require(receipt.get("output_sha256") ==
            "a6f61bdafa04dcc1705634ab7b026b7ce5c0cf1b9d7809cf0f5e7b94b7034ff2",
            "multiblock DTT output receipt changed")
    require(receipt.get("scope") ==
            "scope exclusions: one-root tree attachments only; no multi-interface acyclic connectors; no positive-rank connector blocks; no D+T^3",
            "multiblock DTT scope receipt changed")
    required = receipt.get("required_lines")
    require(type(required) is list and
            "uniform packet bound: sigma(D+TT)=3+Delta/2>3" in required and
            "rejected hostile mutations: 11" in required,
            "multiblock DTT required-line receipt changed")


def validate_single_block(manifest):
    require(manifest.get("schema") == SINGLE_BLOCK["schema"],
            "single-block schema changed")
    require(manifest.get("evidence_kind") == "exact-theorem-owner",
            "single-block evidence is not an exact theorem owner")
    require(manifest.get("scope") == {
        "graph": "finite simple connected",
        "cyclomatic_rank": 6,
        "edge_vertex_relation": "|E(G)|=|V(G)|+5",
        "block_scope": "exactly-one-positive-rank-cyclic-block",
    }, "single-block scope changed")
    require(SINGLE_BLOCK["block_scope"] == "exactly-one-positive-rank-cyclic-block",
            "parent single-block branch contract widened")
    require(manifest.get("excluded_scope") ==
            "multiblock and all-connected hexacyclic graphs",
            "single-block exclusion ledger changed")
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
    expected_replays = [
        "authenticated-committed-independent-exact-census",
        "authenticated-committed-exact-conditional-interface",
        *("authenticated-committed-full-exact-execution" for _ in range(4)),
    ]
    require([row.get("replay") for row in dependencies] == expected_replays,
            "single-block layered replay semantics changed")
    require(all(row.get("execution_evidence_sha256") ==
                SINGLE_BLOCK["execution_evidence_sha256"]
                and row.get("execution_evidence_record") == row.get("name")
                and isinstance(row.get("source_sha256"), str)
                and isinstance(row.get("output_sha256"), str)
                for row in dependencies),
            "single-block owner lacks authenticated committed execution evidence")
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
    if owner is SINGLE_BLOCK:
        evidence_path = owner["execution_evidence_path"]
        require(evidence_path.is_file(), "missing single-block child execution evidence")
        require(hashlib.sha256(evidence_path.read_bytes()).hexdigest() ==
                owner["execution_evidence_sha256"],
                "single-block child execution evidence changed")
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
        **({
            "child_execution_evidence_sha256": owner["execution_evidence_sha256"],
            "promotion": "authenticated-committed-exact-child-executions",
        } if owner is SINGLE_BLOCK else {}),
    }


def root_manifest(dependencies, split):
    require(type(dependencies) is list and len(dependencies) == 2,
            "both proof branches are mandatory")
    expected = [
        {
            "name": MULTIBLOCK["name"],
            "schema": MULTIBLOCK["schema"],
            "block_scope": "at-least-two-positive-rank-cyclic-blocks",
            "source_sha256": MULTIBLOCK["source_sha256"],
            "output_sha256": MULTIBLOCK["output_sha256"],
            "evidence": "canonical-exact-owner-manifest",
        },
        {
            "name": SINGLE_BLOCK["name"],
            "schema": SINGLE_BLOCK["schema"],
            "block_scope": "exactly-one-positive-rank-cyclic-block",
            "source_sha256": SINGLE_BLOCK["source_sha256"],
            "output_sha256": SINGLE_BLOCK["output_sha256"],
            "evidence": "canonical-exact-owner-manifest",
            "child_execution_evidence_sha256":
                SINGLE_BLOCK["execution_evidence_sha256"],
            "promotion": "authenticated-committed-exact-child-executions",
        },
    ]
    require(dependencies == expected,
            "proof receipts are not the ordered, unique multiblock/single-block pair")
    require(split["branch_predicates"] == [
        dependencies[0]["block_scope"], dependencies[1]["block_scope"]
    ], "proof receipts do not match the analytic branch predicates")
    require(split["multiblock_partitions"] == [
        list(row) for row in sorted(PARTITIONS - {(6,)}, reverse=True)
    ] and split["single_block_partitions"] == [[6]],
            "proof receipts do not match the analytic partition split")
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
    valid_multiblock = {
        "schema": MULTIBLOCK["schema"],
        "scope": {
            "graph": "finite simple connected", "cyclomatic_rank": 6,
            "edge_vertex_relation": "|E(G)|=|V(G)|+5",
            "block_scope": MULTIBLOCK["block_scope"],
            "block_rank_partitions": [
                list(row) for row in sorted(PARTITIONS - {(6,)}, reverse=True)
            ],
        },
        "conclusion": EXPECTED_CONCLUSION,
        "ledger": {"integer_partitions": 11, "multiblock_partitions": 10,
                   "packets": 9, "presieve_rows": 5,
                   "rank5_structural_families": 3, "owner_cases": 12},
        "pentagon_sector_execution_m3": {
            "file_sha256": "9c143530e6ffa2b9c1255236927fa3c75e9bc54a7fa77b6fcdd6c83b665340da",
            "output_sha256": "0f765321830d96f0d84845ee6961a158177d003df0f84d10a5b13ce3236b7030",
            "scope": "bridge-free D+C5+3C3 pentagon sectors (m=3)",
            "block_node_trees": 125,
            "weighted_encodings": 3149280,
            "relevant_encodings": 1667520,
            "leaf_encodings": 1481760,
            "required_lines": ["credit lower endpoint min(4-h) 1",
                               "EXACT SECTOR CHECK: PASS"],
        },
        "diamond_two_triangle_execution": {
            "note_sha256": "9107ef2821d441da401079982ae8d0b6c98cee17ae7e52268a9b6ad895b8e11b",
            "file_sha256": "24da5324c6695de4795fbd7885fbeadf986fabe1b52e2aec2082c92223addc9a",
            "output_sha256": "a6f61bdafa04dcc1705634ab7b026b7ce5c0cf1b9d7809cf0f5e7b94b7034ff2",
            "scope": "scope exclusions: one-root tree attachments only; no multi-interface acyclic connectors; no positive-rank connector blocks; no D+T^3",
            "required_lines": ["uniform packet bound: sigma(D+TT)=3+Delta/2>3",
                               "rejected hostile mutations: 11"],
        },
    }
    missing_sector = deepcopy(valid_multiblock)
    del missing_sector["pentagon_sector_execution_m3"]
    expect_rejected(lambda: validate_multiblock(missing_sector),
                    "m=3 sector receipt omitted")
    checks += 1
    wrong_sector = deepcopy(valid_multiblock)
    wrong_sector["pentagon_sector_execution_m3"]["scope"] = (
        "bridge-free D+C5+2C3 pentagon sectors (m=2)")
    expect_rejected(lambda: validate_multiblock(wrong_sector),
                    "m=3 sector receipt mis-scoped")
    checks += 1
    missing_receipt = deepcopy(valid_multiblock)
    del missing_receipt["diamond_two_triangle_execution"]
    expect_rejected(lambda: validate_multiblock(missing_receipt), "DTT receipt omitted")
    checks += 1
    changed_receipt = deepcopy(valid_multiblock)
    changed_receipt["diamond_two_triangle_execution"]["scope"] = "D+T^3 allowed"
    expect_rejected(lambda: validate_multiblock(changed_receipt), "DTT receipt widened")
    checks += 1
    multiblock_receipt = invoke(MULTIBLOCK)
    single_block_receipt = invoke(SINGLE_BLOCK)
    canonical_split = analytic_block_split()
    expect_rejected(
        lambda: root_manifest([single_block_receipt, single_block_receipt],
                              canonical_split),
        "multiblock branch replaced by duplicate single-block receipt")
    checks += 1
    expect_rejected(
        lambda: root_manifest([multiblock_receipt, multiblock_receipt],
                              canonical_split),
        "single-block branch replaced by duplicate multiblock receipt")
    checks += 1
    expect_rejected(
        lambda: root_manifest([single_block_receipt, multiblock_receipt],
                              canonical_split),
        "proof receipts reordered")
    checks += 1
    expect_rejected(
        lambda: root_manifest([multiblock_receipt], canonical_split),
        "single-block receipt omitted")
    checks += 1
    widened_single = deepcopy(single_block_receipt)
    widened_single["block_scope"] = "all-positive-rank-block-configurations"
    expect_rejected(
        lambda: root_manifest([multiblock_receipt, widened_single], canonical_split),
        "single-block receipt widened independently of partition contract")
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
    require(hostile_self_checks() == 25, "hostile mutation count changed")
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
