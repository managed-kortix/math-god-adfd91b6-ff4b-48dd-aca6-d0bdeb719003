#!/usr/bin/env python3
"""Typed fail-closed adapter for the rank-six single-block owner theorem.

This adapter does not turn structural owners into DNN owners.  It authenticates
and replays the established rank-six theorem owner, then records the exact
all-length split needed by the physical R61 theorem:

    DNN  disjoint-union  K110-0  disjoint-union  K110-1  disjoint-union  K223.
"""

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
MASTER = HERE / "rank-six-order2-10-master-verifier.py"
MASTER_SHA256 = "21aabed4eee24f36dc9ddf0460423d0fdd6d20a56e80a60ffed69c796c163bf1"
MASTER_OUTPUT_SHA256 = "e32149c665638e1d9cd08f8050cd4a7c7cae9f76c51b49f9cda3e0cfb2645834"
CHILD_EVIDENCE = HERE / "rank-six-order2-10-child-execution-evidence.json"
CHILD_EVIDENCE_SHA256 = "bbbb8eff45f8009dfb49e926c4952ae0b231ed6e02e708bddfb13b4aac17bb5d"
ORDER5 = HERE / "rank-six-order-five-kernel-theorem-verifier.py"
ORDER5_SHA256 = "7c6f4048f9c4bf955aaab71a2e92aaec36cf6ba6aa7d6feaa2fff50fe2881046"
ORDER6 = HERE / "rank-six-order-six-kernel-theorem-verifier.py"
ORDER6_SHA256 = "e4b5b21900eafd41910ab7fda7f0b178effaef37411cfb36da983d9f8686a46c"
KERNELS = HERE / "fixtures" / "rank-six-kernels.json"
KERNELS_SHA256 = "5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476"
COUNTS = (1, 4, 26, 84, 216, 314, 325, 162, 66)
OWNERS = ("DNN", "K110-0", "K110-1", "K223")


class VerificationError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def strict_json_bytes(raw, label):
    def duplicate_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise VerificationError(f"duplicate key in {label}: {key}")
            result[key] = value
        return result

    def reject_constant(value):
        raise VerificationError(f"nonstandard JSON constant in {label}: {value}")

    try:
        payload = json.loads(raw.decode("ascii"), object_pairs_hook=duplicate_pairs,
                             parse_constant=reject_constant)
    except (UnicodeError, json.JSONDecodeError, ValueError) as error:
        raise VerificationError(f"cannot parse {label}: {error}") from error
    require(raw == canonical_bytes(payload), f"{label} is not canonical ASCII JSON")
    return payload


def authenticate(path, digest, label):
    require(path.is_file() and not path.is_symlink(), f"missing or symlinked {label}")
    require(path.resolve().is_relative_to(ROOT.resolve()), f"{label} escapes repository")
    require(hashlib.sha256(path.read_bytes()).hexdigest() == digest,
            f"{label} digest changed")


def run_exact(path, arguments):
    completed = subprocess.run((sys.executable, "-I", "-B", str(path), *arguments),
                               cwd=ROOT, check=False, capture_output=True)
    require(completed.returncode == 0, f"child failed: {path.name}")
    require(completed.stderr == b"", f"child wrote stderr: {path.name}")
    try:
        completed.stdout.decode("ascii")
    except UnicodeError as error:
        raise VerificationError(f"child output is not ASCII: {path.name}") from error
    return completed.stdout


def parse_master_output(raw):
    first, separator, report = raw.partition(b"\n")
    require(separator == b"\n" and report ==
            b"rank-six orders2-10 master implication audit passed\n",
            "rank-six master report changed")
    manifest = strict_json_bytes(first + b"\n", "rank-six master manifest")
    require(set(manifest) == {
        "attachments", "conclusion", "counts_by_order_2_to_10", "dependencies",
        "evidence_kind", "excluded_scope", "finite_premise", "implication",
        "kernel_count", "kernel_fixture_sha256", "kernel_interval", "length_scope",
        "orders", "schema", "scope",
    }, "rank-six master manifest fields changed")
    require(manifest["schema"] == "rank-six-order2-10-master-implication-v1" and
            manifest["evidence_kind"] == "exact-theorem-owner",
            "rank-six master schema changed")
    require(manifest["scope"] == {
        "block_scope": "exactly-one-positive-rank-cyclic-block",
        "cyclomatic_rank": 6,
        "edge_vertex_relation": "|E(G)|=|V(G)|+5",
        "graph": "finite simple connected",
    }, "rank-six master scope changed")
    require(manifest["conclusion"] == {
        "bound": "|V(G)|", "quantity": "s+(G)", "relation": ">=",
        "statement": "s+(G)>=|V(G)|", "strict": False,
    }, "rank-six master conclusion changed")
    require(manifest["counts_by_order_2_to_10"] == list(COUNTS) and
            manifest["kernel_count"] == 1198 and manifest["kernel_interval"] == [1, 1198],
            "rank-six master census changed")
    require(manifest["kernel_fixture_sha256"] == KERNELS_SHA256 and
            manifest["excluded_scope"] == "multiblock and all-connected hexacyclic graphs",
            "rank-six master boundary changed")
    return manifest


def validate_registry(registry):
    require(set(registry) == {
        "schema", "scope", "complete_disjoint_ownership", "owners",
        "owner_rules", "finite_frontier_ledger", "kernel_fixture_sha256",
        "counts_by_order_2_to_10", "kernel_count", "master_owner",
        "excluded_claims",
    }, "typed registry fields changed")
    require(registry["schema"] == "r61-rank-six-single-block-owner-registry-v1",
            "typed registry schema changed")
    require(registry["scope"] ==
            "all finite simple connected cyclomatic-rank-six graphs with exactly one positive-rank cyclic block",
            "typed registry scope changed")
    require(registry["complete_disjoint_ownership"] is True and
            registry["owners"] == list(OWNERS), "typed owner partition changed")
    require(registry["kernel_fixture_sha256"] == KERNELS_SHA256 and
            registry["counts_by_order_2_to_10"] == list(COUNTS) and
            registry["kernel_count"] == 1198, "typed registry census changed")

    rules = registry["owner_rules"]
    require(set(rules) == set(OWNERS), "typed owner rules changed")
    require(rules["DNN"] == {
        "certificate": "kappa(R)<=|E(R)|+5",
        "families": [
            "every orders-2-10 finite-owner state except the three structural all-length schemas below",
            "K110 all-odd with at least two long paths, by one of the two strict two-long edge-orbit certificates and fixed-parity lengthening",
            "K223 with at least one long path, by a chosen one-coordinate exact frontier and fixed-parity lengthening",
        ],
    }, "DNN rule changed")
    require(rules["K110-0"] == {
        "core": "actual all-unit K5", "long_paths": 0,
        "certificate": "structural induced territory",
    }, "K110-0 rule changed")
    require(rules["K110-1"] == {
        "core": "K5 with exactly one odd path of length at least three",
        "long_paths": 1, "certificate": "structural induced territory",
    }, "K110-1 rule changed")
    require(rules["K223"] == {
        "core": "canonical all-unit K223 row 001111011011111",
        "long_paths": 0, "certificate": "structural induced territory",
    }, "K223 rule changed")
    require(registry["finite_frontier_ledger"] == {
        "orders_2_to_4": "all-DNN",
        "order_5": {"rational_DNN": 1120, "symbolic_DNN": 2,
                    "structural_K110_frontiers": 11},
        "order_6": {"rational_DNN": 31235, "symbolic_DNN": 12,
                    "structural_K223": 1},
        "orders_7_to_10": "all-DNN",
    }, "finite frontier ledger changed")
    require(registry["master_owner"] == {
        "path": "research/rank-six-order2-10-master-verifier.py",
        "source_sha256": MASTER_SHA256,
        "canonical_output_sha256": MASTER_OUTPUT_SHA256,
    }, "master owner identity changed")
    require(registry["excluded_claims"] == [
        "a DNN excess-five certificate for K110-0",
        "a DNN excess-five certificate for K110-1",
        "a DNN excess-five certificate for canonical K223",
        "multiple positive-rank cyclic blocks",
        "all connected hexacyclic graphs",
        "physical rank-(6,1) bridge theorem without the separate bridge proof",
    ], "typed registry nonclaims changed")


def registry_payload():
    registry = {
        "schema": "r61-rank-six-single-block-owner-registry-v1",
        "scope": "all finite simple connected cyclomatic-rank-six graphs with exactly one positive-rank cyclic block",
        "complete_disjoint_ownership": True,
        "owners": list(OWNERS),
        "owner_rules": {
            "DNN": {
                "certificate": "kappa(R)<=|E(R)|+5",
                "families": [
                    "every orders-2-10 finite-owner state except the three structural all-length schemas below",
                    "K110 all-odd with at least two long paths, by one of the two strict two-long edge-orbit certificates and fixed-parity lengthening",
                    "K223 with at least one long path, by a chosen one-coordinate exact frontier and fixed-parity lengthening",
                ],
            },
            "K110-0": {"core": "actual all-unit K5", "long_paths": 0,
                        "certificate": "structural induced territory"},
            "K110-1": {"core": "K5 with exactly one odd path of length at least three",
                        "long_paths": 1, "certificate": "structural induced territory"},
            "K223": {"core": "canonical all-unit K223 row 001111011011111",
                      "long_paths": 0, "certificate": "structural induced territory"},
        },
        "finite_frontier_ledger": {
            "orders_2_to_4": "all-DNN",
            "order_5": {"rational_DNN": 1120, "symbolic_DNN": 2,
                        "structural_K110_frontiers": 11},
            "order_6": {"rational_DNN": 31235, "symbolic_DNN": 12,
                        "structural_K223": 1},
            "orders_7_to_10": "all-DNN",
        },
        "kernel_fixture_sha256": KERNELS_SHA256,
        "counts_by_order_2_to_10": list(COUNTS),
        "kernel_count": 1198,
        "master_owner": {
            "path": "research/rank-six-order2-10-master-verifier.py",
            "source_sha256": MASTER_SHA256,
            "canonical_output_sha256": MASTER_OUTPUT_SHA256,
        },
        "excluded_claims": [
            "a DNN excess-five certificate for K110-0",
            "a DNN excess-five certificate for K110-1",
            "a DNN excess-five certificate for canonical K223",
            "multiple positive-rank cyclic blocks",
            "all connected hexacyclic graphs",
            "physical rank-(6,1) bridge theorem without the separate bridge proof",
        ],
    }
    validate_registry(registry)
    return registry


def hostile_self_checks(registry):
    mutations = []

    def add(label, mutate):
        candidate = deepcopy(registry)
        mutate(candidate)
        mutations.append((label, candidate))

    add("owner omitted", lambda value: value["owners"].remove("K110-1"))
    add("one-long relabeled DNN", lambda value: value["owner_rules"]["K110-1"].update(
        certificate="kappa(R)<=|E(R)|+5"))
    add("two-long uncovered", lambda value: value["owner_rules"]["DNN"]["families"].pop(1))
    add("K223 descendants structural", lambda value: value["owner_rules"]["K223"].update(
        core="all K223 descendants"))
    add("coverage status false", lambda value: value.update(complete_disjoint_ownership=False))
    add("count-only widening", lambda value: value.update(
        scope="all connected hexacyclic graphs"))
    add("master output changed", lambda value: value["master_owner"].update(
        canonical_output_sha256="0" * 64))
    for label, candidate in mutations:
        try:
            validate_registry(candidate)
        except (KeyError, TypeError, VerificationError, ValueError):
            continue
        raise VerificationError(f"hostile mutation accepted: {label}")
    return tuple(label for label, _ in mutations)


def audit():
    for path, digest, label in (
        (MASTER, MASTER_SHA256, "rank-six master"),
        (CHILD_EVIDENCE, CHILD_EVIDENCE_SHA256, "rank-six child evidence"),
        (ORDER5, ORDER5_SHA256, "order-five owner"),
        (ORDER6, ORDER6_SHA256, "order-six owner"),
        (KERNELS, KERNELS_SHA256, "rank-six kernel fixture"),
    ):
        authenticate(path, digest, label)
    master_output = run_exact(MASTER, ("--emit", "--print-manifest"))
    require(hashlib.sha256(master_output).hexdigest() == MASTER_OUTPUT_SHA256,
            "rank-six master canonical output changed")
    parse_master_output(master_output)
    registry = registry_payload()
    rejected = hostile_self_checks(registry)
    require(rejected == ("owner omitted", "one-long relabeled DNN", "two-long uncovered",
                         "K223 descendants structural", "coverage status false",
                         "count-only widening", "master output changed"),
            "hostile mutation ledger changed")
    return {
        "schema": "r61-rank-six-single-block-owner-registry-receipt-v1",
        "registry": registry,
        "authentication": {
            "mode": "fresh-rank-six-master-execution-over-authenticated-committed-child-evidence",
            "rank_six_master_output_sha256": MASTER_OUTPUT_SHA256,
            "rank_six_child_execution_evidence_sha256": CHILD_EVIDENCE_SHA256,
            "caveat": "authenticated committed child execution records are attestations, not fresh replays of every underlying exact segment",
        },
        "hostile_mutations_rejected": list(rejected),
    }


def optimized_output(arguments):
    completed = subprocess.run((sys.executable, "-I", "-B", "-O", str(Path(__file__).resolve()),
                                "--optimized-child", *arguments),
                               cwd=ROOT, check=False, capture_output=True)
    require(completed.returncode == 0 and completed.stderr == b"",
            "optimized typed registry audit failed")
    return completed.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--print-manifest", action="store_true")
    parser.add_argument("--optimized-child", action="store_true")
    args = parser.parse_args()
    try:
        receipt = audit()
        output = canonical_bytes(receipt) if args.print_manifest else (
            b"R61 rank-six typed owner registry: exact audit passed\n")
        if not args.optimized_child and not args.emit and sys.flags.optimize == 0:
            child_args = ("--print-manifest",) if args.print_manifest else ()
            require(optimized_output(child_args) == output,
                    "normal and optimized typed registry outputs differ")
        sys.stdout.buffer.write(output)
        return 0
    except (OSError, VerificationError, TypeError, ValueError) as error:
        sys.stderr.write(f"R61 typed rank-six owner registry: FAIL CLOSED: {error}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
