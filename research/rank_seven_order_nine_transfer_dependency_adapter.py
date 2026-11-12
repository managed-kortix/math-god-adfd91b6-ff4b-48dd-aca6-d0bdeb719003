#!/usr/bin/env python3
"""Fail-closed dependency adapter for the order-nine induced transfer.

This adapter has a deliberately non-promotional claim boundary.  It authenticates
and executes the finite induced-partition classifier, checks the elementary
rank-type exhaustion independently, and records the exact analytic statements
which still require mathematical review.  It never turns a source hash, a text
marker, or a caller-supplied Boolean into semantic authentication.

The emitted contract is suitable for binding into a larger exact-key ledger,
but it does not discharge an analytic premise and it does not establish theorem
eligibility, a global claim, or publication readiness.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any, NoReturn

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "research"
EXPERIMENTS = ROOT / "positive-square-energy" / "experiments"
HEPTACYCLIC = ROOT / "positive-square-energy" / "heptacyclic-general"

TRANSFER_VERIFIER = HERE / "rank-seven-order-nine-induced-partition-transfer-verifier.py"
KERNEL_FIXTURE = HERE / "fixtures" / "rank-seven-kernel-frontier-census.json"
AFTER_SOS = EXPERIMENTS / "rank7_order9_after_sos_remainder.jsonl.xz"
GRAM_OWNERS = (
    EXPERIMENTS / "rank7_order9_dominant_family_gram_owners.jsonl.xz",
    EXPERIMENTS / "rank7_order9_third_family_cycle_gram_owners.jsonl.xz",
    EXPERIMENTS / "rank7_order9_fourth_family_cycle_gram_owners.jsonl.xz",
)
TRANSFER_NOTE = HEPTACYCLIC / "rank-seven-order-nine-induced-partition-transfer.md"
BICYCLIC_PAPER = ROOT / "all-bicyclic-graphs" / "paper.tex"
TRICYCLIC_PAPER = ROOT / "all-tricyclic-graphs" / "paper.tex"
TETRACYCLIC_PAPER = ROOT / "all-tetracyclic-graphs" / "paper.tex"

SCHEMA = "rank-seven-order-nine-transfer-dependency-adapter-v1"
Json = Any

SOURCE_PINS = {
    TRANSFER_VERIFIER: "4b9cb58aeb68b869b9c254a21ae7bd3cf18fc7360e7afb0a47fd8e570c40b2fe",
    KERNEL_FIXTURE: "a241139ab54ce4cce1ab3812887359edb241c0abfb1018e804b4a5f86762cfd5",
    AFTER_SOS: "2a45b69d495e65c47d4b3c668572b0b7922e808c905c501c97e513df47d05089",
    GRAM_OWNERS[0]: "5d41ae256f123a6fa6a31bed226b069ea070e52aaf50199c06d0dbfd0b914de9",
    GRAM_OWNERS[1]: "9955f46b32f0b714f6c3b6b19778cd93f72bdb05ccd3c6e881a79bab288a77bf",
    GRAM_OWNERS[2]: "6423fd051a754ba0c810f79a51e83391926c2049ccf20c8cef0ad4c2a4e3867d",
    TRANSFER_NOTE: "3069961fe0937eabf3281685bcc04dd4e77de20150ddd49b57f1fa0eeb6c58ad",
    BICYCLIC_PAPER: "56a2b521ed0fee18d7e34ebb330e5b181e00979805fca951398f7a33d35b19da",
    TRICYCLIC_PAPER: "13f8f8c7996c0f58f764c52b4a5b915132038e2ce38d3e56285f1bf952990fc1",
    TETRACYCLIC_PAPER: "7d8174e64095e5cccf90776ccac92d2dd2ca3f73d500e2518461f5dfb907b93b",
}

TRANSFER_OUTPUT_SHA256 = "70154fd4dbded871ae77ffdc6a8ffdf7dc23ac86b8411aba983a90029fb642cd"
TRANSFER_PASS_LINE = "rank-seven order-nine induced-partition transfer verifier: PASS"
TRANSFER_FIELDS = frozenset({
    "analytic_dependencies_authenticated", "applicable_kernels",
    "canonical_kernel_types", "canonical_short_obstruction_rows",
    "coordinate_long_frontiers", "deletion_choice_counts",
    "kernel_transfer_types", "obstruction_kernels", "obstruction_orbits",
    "obstruction_physical", "partition_owned_orbits",
    "partition_owned_physical", "post_lane_orbits", "post_lane_physical",
    "represented_obstruction_kernels", "short_targets_per_row",
    "source_orbits_recomputed", "target_orbits", "target_physical",
})
EXPECTED_TRANSFER = {
    "analytic_dependencies_authenticated": False,
    "applicable_kernels": 4022,
    "canonical_kernel_types": {
        "2-cross-4": 1122, "3-cross-2": 400,
        "3-cross-3": 1689, "4-cross-2": 811,
    },
    "canonical_short_obstruction_rows": 1615,
    "coordinate_long_frontiers": 24225,
    "deletion_choice_counts": {"6": 216, "7": 208, "8": 49},
    "kernel_transfer_types": {
        "2-cross-4": 23913, "3-cross-2": 51251,
        "3-cross-3": 104224, "4-cross-2": 88722,
    },
    "obstruction_kernels": 473,
    "obstruction_orbits": 1615,
    "obstruction_physical": 1945,
    "partition_owned_orbits": 268110,
    "partition_owned_physical": 302177,
    "post_lane_orbits": 269725,
    "post_lane_physical": 304122,
    "represented_obstruction_kernels": 115,
    "short_targets_per_row": {"1": 697, "2": 513, "3": 245, "4": 160},
    "source_orbits_recomputed": 272520,
    "target_orbits": {
        "cubic-vertex-long-incidence": 22742,
        "cubic-vertex-short-incidence": 3098,
        "partition": 4289760,
    },
    "target_physical": {
        "cubic-vertex-long-incidence": 27402,
        "cubic-vertex-short-incidence": 3718,
        "partition": 4834832,
    },
}

REVIEWED_AXIOMS = (
    {
        "id": "positive-part-variational-induced-superadditivity",
        "status": "review-required",
        "statement": (
            "For every finite simple graph G and every disjoint vertex partition "
            "V(G)=U disjoint_union W, s+(G)>=s+(G[U])+s+(G[W]); equivalently "
            "sigma(G)>=sigma(G[U])+sigma(G[W])."
        ),
        "hypotheses": [
            "G is a finite simple undirected graph",
            "U and W form an exact disjoint vertex partition of G",
        ],
        "source_path": "positive-square-energy/heptacyclic-general/"
                       "rank-seven-order-nine-induced-partition-transfer.md",
        "source_sha256": SOURCE_PINS[TRANSFER_NOTE],
        "source_locator": "Sharp transfer inequality, equation (2) and variational proof",
        "semantic_proof_executed": False,
    },
    {
        "id": "connected-simple-cyclomatic-rank-two-theorem",
        "status": "review-required",
        "statement": (
            "Every finite simple connected graph H of cyclomatic rank two, "
            "including arbitrary finite rooted one-root tree attachments, satisfies "
            "s+(H)>=|V(H)|."
        ),
        "hypotheses": [
            "H is finite, simple, and connected",
            "|E(H)|=|V(H)|+1",
            "each attached tree meets the realization at exactly one root",
        ],
        "source_path": "all-bicyclic-graphs/paper.tex",
        "source_sha256": SOURCE_PINS[BICYCLIC_PAPER],
        "source_locator": "Theorem 1.1 (lines 56-62); proof concludes strict inequality",
        "semantic_proof_executed": False,
    },
    {
        "id": "connected-simple-cyclomatic-rank-three-theorem",
        "status": "review-required",
        "statement": (
            "Every finite simple connected graph H of cyclomatic rank three, "
            "including arbitrary finite rooted one-root tree attachments, satisfies "
            "s+(H)>=|V(H)|."
        ),
        "hypotheses": [
            "H is finite, simple, and connected",
            "|E(H)|=|V(H)|+2",
            "each attached tree meets the realization at exactly one root",
        ],
        "source_path": "all-tricyclic-graphs/paper.tex",
        "source_sha256": SOURCE_PINS[TRICYCLIC_PAPER],
        "source_locator": "Theorem 1.1 (lines 61-67)",
        "semantic_proof_executed": False,
    },
    {
        "id": "connected-simple-cyclomatic-rank-four-theorem",
        "status": "review-required",
        "statement": (
            "Every finite simple connected graph H of cyclomatic rank four, "
            "including arbitrary finite rooted one-root tree attachments, satisfies "
            "s+(H)>=|V(H)|."
        ),
        "hypotheses": [
            "H is finite, simple, and connected",
            "|E(H)|=|V(H)|+3",
            "each attached tree meets the realization at exactly one root",
        ],
        "source_path": "all-tetracyclic-graphs/paper.tex",
        "source_sha256": SOURCE_PINS[TETRACYCLIC_PAPER],
        "source_locator": "Theorem 1.1 (lines 65-71)",
        "semantic_proof_executed": False,
    },
    {
        "id": "uniform-induced-territory-construction",
        "status": "review-required",
        "statement": (
            "For every simple subdivision of a qualifying rank-seven kernel and every "
            "permitted rooted one-root attachment, the oriented crossing-path rule gives "
            "an exact induced vertex partition U,W; both territories are finite, simple, "
            "and connected, and their cyclomatic ranks equal those of K[S],K[T]."
        ),
        "hypotheses": [
            "replacement-path interiors are mutually disjoint and avoid branch vertices",
            "at most one unit replacement path occurs in each parallel class",
            "attached nonroot tree vertices are new and pairwise disjoint",
            "each tree is identified with exactly one realization root and has no other edges",
            "K[S] and K[T] are connected and each has cyclomatic rank at least two",
        ],
        "source_path": "positive-square-energy/heptacyclic-general/"
                       "rank-seven-order-nine-induced-partition-transfer.md",
        "source_sha256": SOURCE_PINS[TRANSFER_NOTE],
        "source_locator": "Scope and conclusion; Construction and exact rank accounting",
        "semantic_proof_executed": False,
    },
)

AXIOM_FIELDS = frozenset({
    "id", "status", "statement", "hypotheses", "source_path", "source_sha256",
    "source_locator", "semantic_proof_executed",
})
CONTRACT_FIELDS = frozenset({
    "schema", "scope", "source_bytes_authenticated", "source_sha256",
    "executed_finite_gates", "reviewed_analytic_axioms", "reviewed_axiom_registry_sha256",
    "rank_type_exhaustion", "transfer_scope", "all_analytic_dependencies_executed",
    "analytic_dependencies_authenticated", "reviewed_axioms_accepted",
    "bounded_transfer_implication_discharged", "theorem_eligible", "global_claim",
    "claim_boundary",
})


def fail(message: str) -> NoReturn:
    raise RuntimeError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def exact_bool(value: object, label: str) -> bool:
    require(type(value) is bool, f"{label}: expected exact boolean")
    return value


def exact_int(value: object, label: str, minimum: int = 0) -> int:
    require(type(value) is int and value >= minimum,
            f"{label}: expected exact integer at least {minimum}")
    return value


def validate_json(value: object, label: str = "value") -> None:
    value_type = type(value)
    if value is None or value_type in (str, bool, int):
        return
    if value_type is list:
        for index, item in enumerate(value):
            validate_json(item, f"{label}[{index}]")
        return
    if value_type is dict:
        require(all(type(key) is str for key in value),
                f"{label}: non-string JSON key")
        for key, item in value.items():
            validate_json(item, f"{label}.{key}")
        return
    fail(f"{label}: forbidden non-JSON or non-integral value")


def canonical_bytes(value: Json) -> bytes:
    validate_json(value)
    try:
        encoded = json.dumps(value, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=True, allow_nan=False)
        return (encoded + "\n").encode("ascii")
    except (TypeError, ValueError, UnicodeError) as error:
        raise RuntimeError("canonical JSON encoding failed") from error


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def relative(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError as error:
        raise RuntimeError("dependency path escaped repository root") from error


def audit_sources(pins: dict[Path, str] = SOURCE_PINS) -> dict[str, str]:
    require(type(pins) is dict and set(pins) == set(SOURCE_PINS),
            "source dependency registry changed")
    records: dict[str, str] = {}
    for path, expected in SOURCE_PINS.items():
        require(isinstance(path, Path) and type(expected) is str and len(expected) == 64,
                "malformed pinned source record")
        require(path.is_file(), f"missing dependency: {relative(path)}")
        observed = sha256_bytes(path.read_bytes())
        require(observed == expected, f"dependency bytes changed: {relative(path)}")
        records[relative(path)] = observed
    require(len(records) == len(SOURCE_PINS), "source registry cardinality changed")
    return records


def strict_json(raw: bytes, label: str) -> Json:
    try:
        text = raw.decode("ascii")
        value = json.loads(
            text,
            parse_float=lambda token: fail(f"{label}: float forbidden"),
            parse_constant=lambda token: fail(f"{label}: nonstandard number {token}"),
        )
    except (UnicodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"{label}: invalid canonical JSON") from error
    require(canonical_bytes(value) == raw, f"{label}: noncanonical JSON")
    return value


def validate_transfer_result(result: object) -> dict[str, Json]:
    require(type(result) is dict and set(result) == TRANSFER_FIELDS,
            "finite transfer result schema changed")
    require(canonical_bytes(result) == canonical_bytes(EXPECTED_TRANSFER),
            "finite transfer result changed")
    require(result["analytic_dependencies_authenticated"] is False,
            "finite transfer child crossed its analytic claim boundary")
    for key, value in result.items():
        if key in {
            "applicable_kernels", "canonical_short_obstruction_rows",
            "coordinate_long_frontiers", "obstruction_kernels", "obstruction_orbits",
            "obstruction_physical", "partition_owned_orbits", "partition_owned_physical",
            "post_lane_orbits", "post_lane_physical", "represented_obstruction_kernels",
            "source_orbits_recomputed",
        }:
            exact_int(value, f"transfer.{key}")
    return result


def parse_transfer_output(raw: bytes) -> dict[str, Json]:
    require(sha256_bytes(raw) == TRANSFER_OUTPUT_SHA256,
            "finite transfer stdout digest changed")
    lines = raw.splitlines(keepends=True)
    require(len(lines) == 2 and lines[1] == (TRANSFER_PASS_LINE + "\n").encode("ascii"),
            "finite transfer stdout framing changed")
    result = strict_json(lines[0], "finite transfer result")
    return validate_transfer_result(result)


def run_transfer_once(*, optimized: bool) -> tuple[bytes, dict[str, Json]]:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(("-B", str(TRANSFER_VERIFIER)))
    completed = subprocess.run(command, cwd=ROOT, check=False, capture_output=True)
    require(completed.returncode == 0,
            f"finite transfer {'optimized' if optimized else 'normal'} execution failed")
    require(completed.stderr == b"",
            f"finite transfer {'optimized' if optimized else 'normal'} wrote stderr")
    return completed.stdout, parse_transfer_output(completed.stdout)


def execute_transfer_pair() -> dict[str, Json]:
    normal_raw, normal = run_transfer_once(optimized=False)
    optimized_raw, optimized = run_transfer_once(optimized=True)
    require(normal_raw == optimized_raw and
            canonical_bytes(normal) == canonical_bytes(optimized),
            "finite transfer normal and -O outputs differ")
    return {
        "id": "order-nine-induced-partition-finite-classifier",
        "evidence_kind": "executed-finite-gate",
        "source_path": relative(TRANSFER_VERIFIER),
        "source_sha256": SOURCE_PINS[TRANSFER_VERIFIER],
        "normal_output_sha256": sha256_bytes(normal_raw),
        "optimized_output_sha256": sha256_bytes(optimized_raw),
        "normal_optimized_byte_identical": True,
        "child_analytic_dependencies_authenticated": False,
        "applicable_kernels": normal["applicable_kernels"],
        "obstruction_kernels": normal["obstruction_kernels"],
        "owned_rows": normal["partition_owned_orbits"],
        "owned_physical_rows": normal["partition_owned_physical"],
        "owned_targets": normal["target_orbits"]["partition"],
        "finite_gate_passed": True,
        "analytic_implication_established": False,
    }


def rank_type_exhaustion() -> dict[str, Json]:
    """Execute the elementary beta/crossing arithmetic with exact integers."""
    candidates: list[list[int]] = []
    for beta_left, beta_right, crossing in itertools.product(range(2, 8), repeat=3):
        if beta_left < beta_right:
            continue
        if beta_left + beta_right + crossing - 1 == 7:
            candidates.append([beta_left, beta_right, crossing])
    expected = [[4, 2, 2], [3, 3, 2], [3, 2, 3], [2, 2, 4]]
    candidates.sort(reverse=True)
    expected.sort(reverse=True)
    require(candidates == expected, "rank/crossing type exhaustion changed")
    require(all(left in (2, 3, 4) and right in (2, 3, 4) and
                crossing in (2, 3, 4)
                for left, right, crossing in candidates),
            "rank/crossing type escaped lower-rank theorem scopes")
    distribution = Counter((left, right, crossing) for left, right, crossing in candidates)
    require(all(count == 1 for count in distribution.values()),
            "rank/crossing exhaustion has duplicates")
    return {
        "evidence_kind": "executed-finite-integer-gate",
        "identity": "beta_left+beta_right+crossing-1=7",
        "hypotheses": [
            "beta_left>=beta_right>=2",
            "crossing>=2 (a one-edge cut would be a bridge in the 2-connected kernel)",
        ],
        "types": [
            {"ranks": [left, right], "crossing_physical_edges": crossing}
            for left, right, crossing in candidates
        ],
        "exhaustive": True,
        "all_territory_ranks_in_2_through_4": True,
        "analytic_theorem_application_established": False,
    }


def reviewed_axiom_registry() -> tuple[list[dict[str, Json]], str]:
    records = json.loads(canonical_bytes(list(REVIEWED_AXIOMS)))
    require(type(records) is list and len(records) == 5,
            "reviewed axiom registry cardinality changed")
    identifiers = []
    for index, record in enumerate(records):
        require(type(record) is dict and set(record) == AXIOM_FIELDS,
                f"reviewed axiom {index}: schema changed")
        require(type(record["id"]) is str and bool(record["id"]) and
                record["id"].isascii() and "\n" not in record["id"],
                f"reviewed axiom {index}: invalid id")
        identifiers.append(record["id"])
        require(record["status"] == "review-required" and
                type(record["statement"]) is str and bool(record["statement"]) and
                type(record["hypotheses"]) is list and bool(record["hypotheses"]) and
                all(type(item) is str and bool(item) for item in record["hypotheses"]) and
                type(record["source_path"]) is str and bool(record["source_path"]) and
                type(record["source_sha256"]) is str and
                len(record["source_sha256"]) == 64 and
                type(record["source_locator"]) is str and bool(record["source_locator"]) and
                record["semantic_proof_executed"] is False,
                f"reviewed axiom {index}: semantic boundary changed")
        source_path = ROOT / record["source_path"]
        require(source_path in SOURCE_PINS and
                record["source_sha256"] == SOURCE_PINS[source_path],
                f"reviewed axiom {record['id']}: source binding changed")
    require(len(set(identifiers)) == len(identifiers),
            "reviewed axiom ids are not unique")
    return records, sha256_bytes(canonical_bytes(records))


def build_contract(*, execute_finite_gate: bool) -> dict[str, Json]:
    exact_bool(execute_finite_gate, "execute finite gate")
    sources = audit_sources()
    axioms, axiom_digest = reviewed_axiom_registry()
    rank_types = rank_type_exhaustion()
    if execute_finite_gate:
        gates = [execute_transfer_pair()]
    else:
        gates = [{
            "id": "order-nine-induced-partition-finite-classifier",
            "evidence_kind": "registered-unexecuted-finite-gate",
            "source_path": relative(TRANSFER_VERIFIER),
            "source_sha256": SOURCE_PINS[TRANSFER_VERIFIER],
            "expected_output_sha256": TRANSFER_OUTPUT_SHA256,
            "finite_gate_passed": False,
            "analytic_implication_established": False,
        }]
    contract = {
        "schema": SCHEMA,
        "scope": "rank-seven order-nine induced-partition transfer dependency boundary",
        "source_bytes_authenticated": True,
        "source_sha256": sources,
        "executed_finite_gates": gates,
        "reviewed_analytic_axioms": axioms,
        "reviewed_axiom_registry_sha256": axiom_digest,
        "rank_type_exhaustion": rank_types,
        "transfer_scope": {
            "kernel_hypothesis": (
                "loopless 2-connected rank-seven multigraph kernel on nine branch vertices"
            ),
            "witness_hypothesis": (
                "nontrivial branch partition with both induced sides connected and rank>=2"
            ),
            "rank_crossing_types": [[4, 2, 2], [3, 3, 2], [3, 2, 3], [2, 2, 4]],
            "simple_realization_rule": (
                "positive-length edge replacements with disjoint interiors and at most one "
                "unit replacement in each parallel class"
            ),
            "rooted_attachment_rule": (
                "each finite attached tree is identified at exactly one realization root; "
                "nonroot vertices are new/disjoint and there are no further attachment edges"
            ),
            "target_indices": list(range(16)),
            "target_contract_kind": "generated row-times-0..15 contract; not observed child evidence",
        },
        "all_analytic_dependencies_executed": False,
        "analytic_dependencies_authenticated": False,
        "reviewed_axioms_accepted": False,
        "bounded_transfer_implication_discharged": False,
        "theorem_eligible": False,
        "global_claim": False,
        "claim_boundary": (
            "source-byte authentication plus executed finite gates only; five exact analytic "
            "axioms remain review-required and are not made true by this adapter"
        ),
    }
    validate_contract(contract)
    return contract


def validate_contract(contract: object) -> None:
    require(type(contract) is dict and set(contract) == CONTRACT_FIELDS,
            "adapter contract schema changed")
    require(contract["schema"] == SCHEMA and
            contract["source_bytes_authenticated"] is True,
            "adapter identity or source authentication changed")
    require(type(contract["source_sha256"]) is dict and
            set(contract["source_sha256"]) == {relative(path) for path in SOURCE_PINS},
            "adapter source registry changed")
    for path, expected in SOURCE_PINS.items():
        require(contract["source_sha256"][relative(path)] == expected,
                f"adapter source pin changed: {relative(path)}")
    axioms = contract["reviewed_analytic_axioms"]
    expected_axioms, expected_digest = reviewed_axiom_registry()
    require(canonical_bytes(axioms) == canonical_bytes(expected_axioms) and
            contract["reviewed_axiom_registry_sha256"] == expected_digest,
            "reviewed axiom registry changed")
    require(contract["rank_type_exhaustion"] == rank_type_exhaustion(),
            "rank-type exhaustion record changed")
    require(contract["scope"] ==
            "rank-seven order-nine induced-partition transfer dependency boundary" and
            contract["claim_boundary"] == (
                "source-byte authentication plus executed finite gates only; five exact "
                "analytic axioms remain review-required and are not made true by this adapter"
            ), "adapter claim boundary changed")
    require(contract["transfer_scope"] == {
            "kernel_hypothesis": (
                "loopless 2-connected rank-seven multigraph kernel on nine branch vertices"
            ),
            "witness_hypothesis": (
                "nontrivial branch partition with both induced sides connected and rank>=2"
            ),
            "rank_crossing_types": [[4, 2, 2], [3, 3, 2], [3, 2, 3], [2, 2, 4]],
            "simple_realization_rule": (
                "positive-length edge replacements with disjoint interiors and at most one "
                "unit replacement in each parallel class"
            ),
            "rooted_attachment_rule": (
                "each finite attached tree is identified at exactly one realization root; "
                "nonroot vertices are new/disjoint and there are no further attachment edges"
            ),
            "target_indices": list(range(16)),
            "target_contract_kind":
                "generated row-times-0..15 contract; not observed child evidence",
        }, "transfer scope changed")
    require(type(contract["executed_finite_gates"]) is list and
            len(contract["executed_finite_gates"]) == 1 and
            contract["executed_finite_gates"][0]["analytic_implication_established"] is False,
            "finite gate crossed the analytic boundary")
    require(contract["all_analytic_dependencies_executed"] is False and
            contract["analytic_dependencies_authenticated"] is False and
            contract["reviewed_axioms_accepted"] is False and
            contract["bounded_transfer_implication_discharged"] is False and
            contract["theorem_eligible"] is False and
            contract["global_claim"] is False,
            "adapter promoted a reviewed axiom or theorem claim")


def expect_rejected(action: object, label: str) -> None:
    require(callable(action), "hostile action is not callable")
    try:
        action()
    except (RuntimeError, TypeError, ValueError, KeyError):
        return
    fail(f"hostile adapter mutation accepted: {label}")


def hostile_contract_checks(contract: dict[str, Json]) -> int:
    mutations: list[tuple[str, dict[str, Json]]] = []
    for field in (
        "all_analytic_dependencies_executed", "analytic_dependencies_authenticated",
        "reviewed_axioms_accepted", "bounded_transfer_implication_discharged",
        "theorem_eligible", "global_claim",
    ):
        candidate = json.loads(canonical_bytes(contract))
        candidate[field] = True
        mutations.append((f"promoted {field}", candidate))

    candidate = json.loads(canonical_bytes(contract))
    candidate["reviewed_analytic_axioms"] = candidate["reviewed_analytic_axioms"][:-1]
    mutations.append(("omitted reviewed axiom", candidate))

    candidate = json.loads(canonical_bytes(contract))
    candidate["reviewed_analytic_axioms"].append(
        json.loads(canonical_bytes(candidate["reviewed_analytic_axioms"][0])))
    mutations.append(("duplicated reviewed axiom", candidate))

    candidate = json.loads(canonical_bytes(contract))
    candidate["reviewed_analytic_axioms"][0]["status"] = "executed"
    mutations.append(("relabeled reviewed axiom as executed", candidate))

    candidate = json.loads(canonical_bytes(contract))
    candidate["reviewed_analytic_axioms"][1]["semantic_proof_executed"] = True
    mutations.append(("forged semantic execution bit", candidate))

    candidate = json.loads(canonical_bytes(contract))
    candidate["reviewed_analytic_axioms"][2]["source_sha256"] = "0" * 64
    mutations.append(("forged reviewed source digest", candidate))

    candidate = json.loads(canonical_bytes(contract))
    candidate["reviewed_analytic_axioms"][3]["hypotheses"] = []
    mutations.append(("weakened reviewed hypotheses", candidate))

    candidate = json.loads(canonical_bytes(contract))
    candidate["rank_type_exhaustion"]["types"] = \
        candidate["rank_type_exhaustion"]["types"][:-1]
    mutations.append(("omitted rank type", candidate))

    candidate = json.loads(canonical_bytes(contract))
    candidate["source_sha256"].pop(relative(BICYCLIC_PAPER))
    mutations.append(("omitted pinned source", candidate))

    candidate = json.loads(canonical_bytes(contract))
    candidate["executed_finite_gates"][0]["analytic_implication_established"] = True
    mutations.append(("promoted finite child to analytic proof", candidate))

    for label, candidate in mutations:
        expect_rejected(lambda candidate=candidate: validate_contract(candidate), label)
    require(len(mutations) == 15, "hostile adapter mutation ledger changed")
    return len(mutations)


def main() -> int:
    execute = "--execute" in sys.argv[1:]
    require(set(sys.argv[1:]).issubset({"--execute"}), "unknown adapter argument")
    contract = build_contract(execute_finite_gate=execute)
    mutations = hostile_contract_checks(contract)
    output = {
        "contract": contract,
        "hostile_mutations_rejected": mutations,
        "status": "PASS-NONPROMOTIONAL",
    }
    sys.stdout.buffer.write(canonical_bytes(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
