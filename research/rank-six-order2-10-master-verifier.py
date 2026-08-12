#!/usr/bin/env python3
"""Completion-gated master skeleton for rank-six kernel orders two through ten."""

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
ORDER_COUNTS = (1, 4, 26, 84, 216, 314, 325, 162, 66)
FINAL_CONCLUSION = "kappa(B)<=|E(B)|+5;therefore s+(G)>=|V(G)| after rooted-tree lift"
CENSUS = {
    "name": "kernel-census",
    "path": HERE / "rank-six-kernel-census-verifier.py",
    "source_sha256": "325b78066b626a00deaceb6a026377dd7f898a906c63c597f77831548585e1ee",
    "output_sha256": "784510e470ae004712dc0b1bb8d8419f2daecea4a4b5caed05f7eadaff62a814",
}
ANALYTIC_LIFT = {
    "name": "conditional-analytic-lift",
    "path": HERE / "rank-six-conditional-analytic-lift-verifier.py",
    "manifest_path": HERE / "rank-six-conditional-analytic-lift-manifest.json",
    "source_sha256": "97c49fa7d1c9c162f4592e0954d63271eb98416fbab59605a9e58a0ada1043df",
    "manifest_sha256": "b6ab90a895fcd7d6ebcf3b32b69676847c35dd7d070e9b8c6c4c13150bda94f6",
    "output_sha256": "a86a7dc77ba8d0a6131acb6d457d4a10129615d156cae3de01e5997b61e40d8a",
    "schema": "rank-six-conditional-analytic-lift-v1",
}

# A promotion owner is registered only after its source and canonical full-replay
# output have been frozen. None is a deliberate closed gate, never a wildcard.
OWNERS = (
    {
        "name": "orders-2-7",
        "orders": (2, 3, 4, 5, 6, 7),
        "kernel_interval": (1, 645),
        "kernel_count": 645,
        "path": HERE / "rank-six-order2-7-master-verifier.py",
        "source_sha256": "a84d100a61433eae1944db1036693a0eec136c53343192d6c238392335cf742f",
        "output_sha256": "82b6a386356a287267e1a3f2b8ad149b73a8827145e2a4f1a8da72bbc8bbb428",
        "arguments": ("--emit", "--print-manifest"),
        "schema": "rank-six-order2-7-master-verifier-v1",
        "adapter": "existing-orders2-7-implication-owner",
    },
    {
        "name": "order-8",
        "orders": (8,),
        "kernel_interval": (646, 970),
        "kernel_count": 325,
        "path": HERE / "rank-six-order-eight-kernel-theorem-verifier.py",
        "source_sha256": "247fc797251f19ce1fde2824f24543e2eaa7d3d3dfe4411bcc6eb829aa3e9703",
        "output_sha256": "01127da2253626e85f66034ab226b78872045ad9392214b767d86aa204e8c61d",
        "arguments": ("--full", "--print-manifest"),
        "schema": "rank-six-order-eight-kernel-theorem-master-v1",
        "adapter": "promotion-owner-segmented-exact-executions",
    },
    {
        "name": "order-9-promotion",
        "orders": (9,),
        "kernel_interval": (971, 1132),
        "kernel_count": 162,
        "path": HERE / "rank-six-order-nine-kernel-theorem-verifier.py",
        "source_sha256": "d11b6da30ccff5905cf851d33fc6a5d0cfc6650f3e8317224ddc0d8a2e4cd3d9",
        "output_sha256": "dd6a5a1e9b905955affde5fa64e0b8187dc39ad35c02ab007172da3358dff4f4",
        "arguments": ("--full", "--print-manifest"),
        "schema": "rank-six-order-nine-kernel-theorem-master-v1",
        "adapter": "promotion-owner-full-exact-replay",
    },
    {
        "name": "order-10-promotion",
        "orders": (10,),
        "kernel_interval": (1133, 1198),
        "kernel_count": 66,
        "path": HERE / "rank-six-order-ten-kernel-theorem-verifier.py",
        "source_sha256": "4cb22611448755d1eea984271251b542ab96f519cc052f3aeda8d56c04c61819",
        "output_sha256": "767bbf4dd142afd7eb5a45dffeb738734948412ca53358c40d3655b28403725e",
        "arguments": ("--full", "--print-manifest"),
        "schema": "rank-six-order-ten-kernel-theorem-master-v1",
        "adapter": "promotion-owner-segmented-exact-executions",
    },
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def strict_json_bytes(raw, label):
    def reject_constant(value):
        raise ValueError(f"nonstandard JSON constant in {label}: {value}")

    try:
        payload = json.loads(raw.decode("ascii"), parse_constant=reject_constant)
    except (UnicodeError, json.JSONDecodeError, ValueError) as error:
        raise RuntimeError(f"cannot parse {label}: {error}") from error
    require(raw == canonical_bytes(payload), f"{label} is not canonical ASCII JSON")
    return payload


def audit_fixture():
    raw = KERNEL_FIXTURE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == KERNEL_SHA256,
            "rank-six kernel fixture digest changed")
    payload = strict_json_bytes(raw, "rank-six kernel fixture")
    require(payload.get("beta") == 6 and payload.get("orders") == [2, 10],
            "rank-six kernel fixture scope changed")
    rows = payload.get("kernels")
    require(type(rows) is list, "rank-six kernel rows are malformed")
    counts = tuple(sum(row.get("n") == order for row in rows) for order in range(2, 11))
    require(counts == ORDER_COUNTS and len(rows) == 1198,
            "orders 2-10 kernel partition changed")
    return counts


def validate_partition(owners=OWNERS):
    require(type(owners) is tuple and len(owners) == 4, "owner registry width changed")
    orders = []
    kernel_ids = []
    for owner in owners:
        require(set(owner) == set(OWNERS[0]), f"owner fields changed: {owner.get('name')}")
        orders.extend(owner["orders"])
        first, last = owner["kernel_interval"]
        require(last - first + 1 == owner["kernel_count"],
                f"kernel count/interval mismatch: {owner['name']}")
        kernel_ids.extend(range(first, last + 1))
    require(tuple(orders) == tuple(range(2, 11)), "owner orders are not exactly 2 through 10")
    require(tuple(kernel_ids) == tuple(range(1, 1199)),
            "owner kernel intervals are not the exact contiguous K1-K1198 partition")
    require(sum(owner["kernel_count"] for owner in owners) == 1198,
            "owner kernel total changed")


def parse_child_output(stdout, owner):
    first_line, separator, remainder = stdout.partition("\n")
    require(separator == "\n" and remainder, f"missing child report: {owner['name']}")
    manifest = strict_json_bytes((first_line + "\n").encode("ascii"),
                                 f"{owner['name']} child manifest")
    require(manifest.get("schema") == owner["schema"],
            f"child schema changed: {owner['name']}")
    require(manifest.get("kernel_fixture_sha256") == KERNEL_SHA256,
            f"child fixture identity changed: {owner['name']}")
    return manifest


def validate_child_manifest(owner, manifest):
    name = owner["name"]
    if name == "orders-2-7":
        require(manifest.get("counts_by_order_2_to_7") == list(ORDER_COUNTS[:6]),
                "orders-2-7 counts changed")
        require(manifest.get("scope") ==
                "all simple subdivisions of the 645 rank-six kernels of orders 2 through 7",
                "orders-2-7 scope changed")
        require(manifest.get("conclusion") == "s+(G)>=|V(G)|",
                "orders-2-7 implication changed")
    else:
        expected_scope = (f"order={owner['orders'][0]};rank=6;kernels="
                          f"K{owner['kernel_interval'][0]}-K{owner['kernel_interval'][1]};"
                          "single-positive-rank-cyclic-block")
        require(manifest.get("scope") == expected_scope, f"child scope changed: {name}")
        require(manifest.get("conclusion") == FINAL_CONCLUSION,
                f"child conclusion changed: {name}")
        require(manifest.get("frontier", {}).get("complete_disjoint_ownership") is True,
                f"status-only or incomplete owner rejected: {name}")
    require("all connected hexacyclic" not in manifest.get("scope", "").lower(),
            f"multiblock scope widening rejected: {name}")
    require("ready_for_theorem_promotion" not in manifest,
            f"status-only promotion record rejected: {name}")


def invoke(owner):
    name = owner["name"]
    require(owner["source_sha256"] is not None, f"unregistered promotion source: {name}")
    require(owner["output_sha256"] is not None, f"unregistered canonical output: {name}")
    require(owner["path"].is_file(), f"missing promotion owner: {name}")
    require(hashlib.sha256(owner["path"].read_bytes()).hexdigest() == owner["source_sha256"],
            f"owner source digest changed: {name}")
    optimize = ("-O",) if sys.flags.optimize else ()
    completed = subprocess.run(
        (sys.executable, *optimize, str(owner["path"]), *owner["arguments"]),
        check=False, capture_output=True, text=True,
    )
    require(completed.returncode == 0, f"full exact owner failed: {name}")
    require(completed.stderr == "", f"full exact owner wrote stderr: {name}")
    actual_output = hashlib.sha256(completed.stdout.encode("utf-8")).hexdigest()
    require(actual_output == owner["output_sha256"], f"owner output digest changed: {name}")
    manifest = parse_child_output(completed.stdout, owner)
    validate_child_manifest(owner, manifest)
    return {
        "name": name,
        "orders": list(owner["orders"]),
        "kernel_interval": list(owner["kernel_interval"]),
        "kernel_count": owner["kernel_count"],
        "source_sha256": owner["source_sha256"],
        "output_sha256": owner["output_sha256"],
        "schema": owner["schema"],
        "replay": "full-exact",
    }


def invoke_census():
    require(CENSUS["path"].is_file(), "missing exact kernel census")
    require(hashlib.sha256(CENSUS["path"].read_bytes()).hexdigest() ==
            CENSUS["source_sha256"], "kernel census source digest changed")
    optimize = ("-O",) if sys.flags.optimize else ()
    completed = subprocess.run(
        (sys.executable, *optimize, str(CENSUS["path"])),
        check=False, capture_output=True, text=True,
    )
    require(completed.returncode == 0, "exact kernel census failed")
    require(completed.stderr == "", "exact kernel census wrote stderr")
    require(hashlib.sha256(completed.stdout.encode("utf-8")).hexdigest() ==
            CENSUS["output_sha256"], "kernel census output digest changed")
    require("canonical_counts_n2_to_n10: 1,4,26,84,216,314,325,162,66 (total 1198)"
            in completed.stdout, "kernel census partition report changed")
    return {
        "name": CENSUS["name"],
        "orders": list(range(2, 11)),
        "kernel_interval": [1, 1198],
        "kernel_count": 1198,
        "source_sha256": CENSUS["source_sha256"],
        "output_sha256": CENSUS["output_sha256"],
        "replay": "independent-exact-census",
    }


def invoke_analytic_lift():
    for key in ("path", "manifest_path"):
        require(ANALYTIC_LIFT[key].is_file(), f"missing analytic lift {key}")
    require(hashlib.sha256(ANALYTIC_LIFT["path"].read_bytes()).hexdigest() ==
            ANALYTIC_LIFT["source_sha256"], "analytic lift source digest changed")
    require(hashlib.sha256(ANALYTIC_LIFT["manifest_path"].read_bytes()).hexdigest() ==
            ANALYTIC_LIFT["manifest_sha256"], "analytic lift manifest digest changed")
    optimize = ("-O",) if sys.flags.optimize else ()
    completed = subprocess.run(
        (sys.executable, *optimize, str(ANALYTIC_LIFT["path"]),
         "--emit", "--print-manifest"),
        check=False, capture_output=True, text=True,
    )
    require(completed.returncode == 0, "conditional analytic lift failed")
    require(completed.stderr == "", "conditional analytic lift wrote stderr")
    require(hashlib.sha256(completed.stdout.encode("ascii")).hexdigest() ==
            ANALYTIC_LIFT["output_sha256"], "analytic lift output digest changed")
    first_line, separator, report = completed.stdout.partition("\n")
    require(separator == "\n" and report, "analytic lift report is missing")
    manifest = strict_json_bytes((first_line + "\n").encode("ascii"),
                                 "conditional analytic lift manifest")
    require(manifest.get("schema") == ANALYTIC_LIFT["schema"],
            "analytic lift schema changed")
    require(manifest.get("finite_premise", {}).get("result") ==
            "kappa(B)<=|E(B)|+5", "analytic lift premise changed")
    require(manifest.get("conclusion") == "s+(G)>=|V(G)|",
            "analytic lift conclusion changed")
    require("global_claim=false finite_premise_discharged=false" in report,
            "analytic lift nonclaim boundary changed")
    return {
        "name": ANALYTIC_LIFT["name"],
        "source_sha256": ANALYTIC_LIFT["source_sha256"],
        "manifest_sha256": ANALYTIC_LIFT["manifest_sha256"],
        "output_sha256": ANALYTIC_LIFT["output_sha256"],
        "schema": ANALYTIC_LIFT["schema"],
        "replay": "exact-conditional-interface",
    }


def implication_manifest(counts, dependencies):
    require(len(dependencies) == 6,
            "implication requires the census, analytic lift, and all four owners")
    return {
        "schema": "rank-six-order2-10-master-implication-v1",
        "evidence_kind": "exact-theorem-owner",
        "scope": {
            "graph": "finite simple connected",
            "cyclomatic_rank": 6,
            "edge_vertex_relation": "|E(G)|=|V(G)|+5",
            "block_scope": "exactly-one-positive-rank-cyclic-block",
        },
        "conclusion": {
            "quantity": "s+(G)",
            "relation": ">=",
            "bound": "|V(G)|",
            "statement": "s+(G)>=|V(G)|",
            "strict": False,
        },
        "kernel_fixture_sha256": KERNEL_SHA256,
        "counts_by_order_2_to_10": list(counts),
        "orders": list(range(2, 11)),
        "kernel_interval": [1, 1198],
        "kernel_count": 1198,
        "dependencies": dependencies,
        "finite_premise": "kappa(B)<=|E(B)|+5 for every finite-owner subdivision family",
        "length_scope": "arbitrary positive simple-subdivision lengths",
        "attachments": "arbitrary finite rooted trees at branch or subdivision vertices",
        "implication": (
            "if every registered finite owner discharges the analytic-lift premise, while "
            "the typed orders-2-7 owner proves its stated spectral implication, then the "
            "combined owner partition gives s+(G)>=|V(G)| for its single-block families"
        ),
        "excluded_scope": "multiblock and all-connected hexacyclic graphs",
    }


def expect_rejected(action, label):
    try:
        action()
    except (RuntimeError, TypeError, ValueError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_self_checks():
    mutations = 0
    for index, owner in enumerate(OWNERS):
        changed = OWNERS[:index] + OWNERS[index + 1:]
        expect_rejected(lambda changed=changed: validate_partition(changed),
                        f"owner omitted: {owner['name']}")
        mutations += 1
    changed = deepcopy(OWNERS)
    changed[2]["orders"] = (8,)
    expect_rejected(lambda: validate_partition(changed), "order duplicated and order nine omitted")
    mutations += 1
    changed = deepcopy(OWNERS)
    changed[3]["kernel_interval"] = (1132, 1198)
    changed[3]["kernel_count"] = 67
    expect_rejected(lambda: validate_partition(changed), "kernel interval overlap")
    mutations += 1
    status_only = {"schema": OWNERS[2]["schema"],
                   "kernel_fixture_sha256": KERNEL_SHA256,
                   "ready_for_theorem_promotion": True}
    expect_rejected(lambda: validate_child_manifest(OWNERS[2], status_only),
                    "status-only promotion owner")
    mutations += 1
    widened = {
        "schema": OWNERS[2]["schema"],
        "kernel_fixture_sha256": KERNEL_SHA256,
        "scope": "all connected hexacyclic graphs",
        "conclusion": FINAL_CONCLUSION,
        "frontier": {"complete_disjoint_ownership": True},
    }
    expect_rejected(lambda: validate_child_manifest(OWNERS[2], widened),
                    "multiblock scope widening")
    mutations += 1
    altered = {
        "schema": OWNERS[2]["schema"],
        "kernel_fixture_sha256": KERNEL_SHA256,
        "scope": "order=9;rank=6;kernels=K971-K1132;single-nontrivial-block",
        "conclusion": "unchecked positivity status",
        "frontier": {"complete_disjoint_ownership": True},
    }
    expect_rejected(lambda: validate_child_manifest(OWNERS[2], altered),
                    "owner conclusion altered")
    mutations += 1
    mismatched_scope = {
        "schema": OWNERS[1]["schema"],
        "kernel_fixture_sha256": KERNEL_SHA256,
        "scope": "order=8;rank=6;kernels=K646-K970;single-nontrivial-block",
        "conclusion": FINAL_CONCLUSION,
        "frontier": {"complete_disjoint_ownership": True},
    }
    expect_rejected(lambda: validate_child_manifest(OWNERS[1], mismatched_scope),
                    "ambiguous nontrivial-block scope")
    mutations += 1
    return mutations


def audit():
    counts = audit_fixture()
    validate_partition()
    require(hostile_self_checks() == 10, "hostile mutation count changed")
    blockers = [owner["name"] for owner in OWNERS
                 if owner["source_sha256"] is None or owner["output_sha256"] is None
                 or not owner["path"].is_file()]
    require(not blockers, "promotion gate closed: " + ", ".join(blockers))
    dependencies = [invoke_census(), invoke_analytic_lift(),
                    *(invoke(owner) for owner in OWNERS)]
    return implication_manifest(counts, dependencies)


def optimized_output():
    completed = subprocess.run(
        (sys.executable, "-O", str(Path(__file__).resolve()), "--emit"),
        check=False, capture_output=True, text=True,
    )
    require(completed.returncode == 0, "python -O master verifier failed")
    require(completed.stderr == "", "python -O master verifier wrote stderr")
    return completed.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--print-manifest", action="store_true")
    args = parser.parse_args()
    try:
        manifest = audit()
    except (OSError, RuntimeError, TypeError, ValueError) as error:
        sys.stderr.write(f"rank-six orders2-10 master: FAIL CLOSED: {error}\n")
        return 1
    if args.print_manifest:
        sys.stdout.write(canonical_bytes(manifest).decode("ascii"))
    output = "rank-six orders2-10 master implication audit passed\n"
    if not args.emit and not args.print_manifest and sys.flags.optimize == 0:
        require(optimized_output() == output, "normal and python -O output differ")
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
