#!/usr/bin/env python3
"""Layered fail-closed verifier for the order-eight rank-six kernel theorem."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPERIMENTS = ROOT / "positive-square-energy" / "experiments"
KERNEL_FIXTURE = HERE / "fixtures" / "rank-six-kernels.json"
CENSUS_PROGRAM = EXPERIMENTS / "rank6_order8_orbit_frontier_census.py"
CENSUS_FIXTURE = EXPERIMENTS / "rank6_order8_orbit_frontier_census.json"
PACK_AUDITOR = EXPERIMENTS / "rank6_order8_pack_auditor.py"
PACK_MANIFEST = EXPERIMENTS / "rank6_order8_search_manifest.json"
SEGMENTED_EVIDENCE = (EXPERIMENTS / "rank6_order8_chunk_replays" /
                      "aggregate.json")
SYMBOLIC_PROGRAM = EXPERIMENTS / "rank6_order8_symbolic_recognizers.py"
SYMBOLIC_FIXTURE = EXPERIMENTS / "rank6_order8_symbolic_templates.json"

DEPENDENCIES = {
    "kernel_fixture": (KERNEL_FIXTURE,
        "5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476"),
    "census_program": (CENSUS_PROGRAM,
        "83527bb0b5dba2cd19040fc23c3c9f02fe4c6bed21620eb1ca7c571b70cb3407"),
    "census_fixture": (CENSUS_FIXTURE,
        "724fdb337b7bb9225b1a8691c28e131ae1c8de7dc38bb13a5adbb98c1f92218e"),
    "pack_auditor": (PACK_AUDITOR,
        "f6a7a673f86999bcd7e2056408450014296ff603eb56f082ac1e87fa256ac857"),
    "pack_manifest": (PACK_MANIFEST,
        "9512d8a04c05209d42c0be34d4e1c636d6d8c3b7773cf04768490d1100d46e2d"),
    "segmented_evidence": (SEGMENTED_EVIDENCE,
        "7500b864bb11fcbfd68ae6a05701ed59a3f0bcaf243e93353a9d5605ee64f763"),
    "symbolic_program": (SYMBOLIC_PROGRAM,
        "755dd24b9e3f129dc6cd4fe590c4c13031bd22c41054ca29082981e3f5d909fe"),
    "symbolic_fixture": (SYMBOLIC_FIXTURE,
        "2f457374d9627bd27339a0988aa47149db825dd0cba050c71ac9accfa3f72b95"),
}
EXPECTED_SCOPE = "order=8;rank=6;kernels=K646-K970;single-positive-rank-cyclic-block"
EXPECTED_CONCLUSION = "kappa(B)<=|E(B)|+5;therefore s+(G)>=|V(G)| after rooted-tree lift"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def strict_json(path, label):
    def pairs(rows):
        result = {}
        for key, value in rows:
            require(key not in result, f"duplicate key in {label}: {key}")
            result[key] = value
        return result

    def reject_constant(value):
        raise ValueError(f"nonstandard JSON constant in {label}: {value}")

    raw = path.read_bytes()
    try:
        payload = json.loads(raw.decode("ascii"), object_pairs_hook=pairs,
                             parse_constant=reject_constant)
    except (UnicodeError, json.JSONDecodeError, ValueError) as error:
        raise RuntimeError(f"cannot parse {label}: {error}") from error
    require(raw == canonical_bytes(payload), f"{label} is not canonical ASCII JSON")
    return raw, payload


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_registry(dependencies=DEPENDENCIES, scope=EXPECTED_SCOPE,
                      conclusion=EXPECTED_CONCLUSION):
    require(dependencies == DEPENDENCIES, "dependency registry changed")
    require(scope == EXPECTED_SCOPE, "theorem scope changed")
    require(conclusion == EXPECTED_CONCLUSION, "theorem conclusion changed")
    require("hexacyclic" not in scope and "all connected" not in scope,
            "scope was widened beyond the order-eight single-block class")


def audit_dependencies():
    result = {}
    for name, (path, expected) in DEPENDENCIES.items():
        require(path.is_file(), f"missing dependency: {name}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        require(expected is not None and actual == expected,
                f"dependency digest changed or is not frozen: {name}")
        result[name] = actual
    return result


def audit_census():
    raw, payload = strict_json(CENSUS_FIXTURE, "order-eight census fixture")
    census = load_module("rank6_order8_census_for_master", CENSUS_PROGRAM)
    census.verify(payload)
    require(payload["kernel_interval"] == [646, 970] and payload["kernel_total"] == 325,
            "order-eight kernel interval changed")
    require((payload["physical_total"], payload["orbit_total"],
             payload["tetrahedral_certified_total"],
             payload["tetrahedral_residual_total"], payload["frontier_target_total"]) ==
            (1598512, 1045292, 942304, 102988, 1441832),
            "exact census totals changed")
    require(payload["full_theorem"] is False,
            "census fixture must remain a fail-closed non-theorem artifact")
    return hashlib.sha256(raw).hexdigest(), payload


def validate_frontier_report(report):
    require(type(report) is dict and set(report) == {
        "status", "covered_residual_range", "residual_total", "covered_target_total",
        "unresolved_target_total", "symbolic_certified_target_total", "unresolved_keys",
        "exact_cost_five_target_total", "symbolic_expected_in_coverage",
        "symbolic_rationally_certified_target_total", "symbolic_unexpected_target_total",
        "symbolic_coverage_match", "exact_audit"}, "exact audit report fields changed")
    require(report["status"] == "complete" and report["exact_audit"] is True,
            "exact frontier transcript is incomplete")
    require((report["covered_residual_range"], report["residual_total"],
             report["covered_target_total"]) == ([0, 102988], 102988, 1441832),
            "frontier coverage changed")
    require(report["unresolved_target_total"] == 24 and
            report["symbolic_certified_target_total"] == 24,
            "24-target symbolic ownership changed")
    require(report["symbolic_unexpected_target_total"] == 0 and
            report["symbolic_coverage_match"] is True,
            "symbolic target partition changed")
    require(len(report["unresolved_keys"]) == 24 and
            len({tuple(key) for key in report["unresolved_keys"]}) == 24,
            "symbolic key ledger width or uniqueness changed")
    return report


def audit_exact_frontier(chunk_index=None):
    auditor = load_module("rank6_order8_pack_for_master", PACK_AUDITOR)
    report, complete = auditor.audit(PACK_MANIFEST, exact=True, chunk_index=chunk_index)
    require(complete, "exhaustive exact frontier is incomplete")
    if chunk_index is None:
        validate_frontier_report(report)
    return report


def validate_segmented_evidence(aggregate, records, reports, pack):
    require(aggregate.get("schema") ==
            "rank-six-order-eight-chunk-audit-aggregate-v2" and
            aggregate.get("proof_semantics") ==
            "receipt_index_only_no_proof_by_itself" and
            aggregate.get("exact_proof") is False,
            "aggregate must remain an index with no proof by itself")
    require(len(records) == len(reports) == len(pack["chunks"]) == 17,
            "segmented evidence must contain exactly 17 receipts")
    require([record.get("chunk_index") for record in records] == list(range(17)) and
            [record.get("residual_range") for record in records] ==
            [chunk["residual_range"] for chunk in pack["chunks"]],
            "receipt partition is not the exact manifest partition")
    rational = sum(report["covered_target_total"] -
                   report["symbolic_certified_target_total"] for report in reports)
    symbolic = sum(report["symbolic_certified_target_total"] for report in reports)
    certified = sum(report["covered_target_total"] for report in reports)
    require((rational, symbolic, certified) == (1441808, 24, 1441832) and
            aggregate.get("ownership") == {
                "rational_owner_target_total": rational,
                "symbolic_owner_target_total": symbolic,
                "certified_target_total": certified,
                "complete_disjoint_ownership": True,
            }, "exact aggregate ownership totals changed")
    require(all(report["status"] == "complete" and
                report["exact_audit"] is True and
                report["unresolved_target_total"] ==
                report["symbolic_certified_target_total"]
                for report in reports),
            "a receipt does not own every target in its exact range")
    require(aggregate.get("report", {}).get("covered_residual_range") == [0, 102988] and
            aggregate.get("report", {}).get("covered_target_total") == certified,
            "aggregate universe changed")
    return {
        "rational_targets": rational,
        "symbolic_targets": symbolic,
        "certified_targets": certified,
        "complete_disjoint_ownership": True,
    }


def segmented_exact_replays(pack):
    auditor = load_module("rank6_order8_segmented_for_promotion", PACK_AUDITOR)
    raw, aggregate = strict_json(SEGMENTED_EVIDENCE, "order-eight receipt aggregate")
    require(hashlib.sha256(raw).hexdigest() == DEPENDENCIES["segmented_evidence"][1],
            "receipt aggregate identity changed")
    require(aggregate.get("auditor_sha256") == DEPENDENCIES["pack_auditor"][1] and
            aggregate.get("manifest_sha256") == DEPENDENCIES["pack_manifest"][1] and
            aggregate.get("dependency_sha256") == pack["dependency_sha256"] and
            aggregate.get("covered_key_stream_sha256") ==
            pack["covered_key_stream_sha256"],
            "receipt aggregate input identities changed")
    records = aggregate.get("chunks")
    require(type(records) is list, "receipt aggregate index is malformed")
    root = SEGMENTED_EVIDENCE.parent.resolve()
    reports = []
    for expected_index, record in enumerate(records):
        require(type(record) is dict and set(record) == {
            "chunk_index", "path", "residual_range", "transcript_sha256",
            "rational_owner_target_total", "symbolic_owner_target_total",
        }, "receipt index fields changed")
        path = (root / record["path"]).resolve()
        try:
            path.relative_to(root)
        except ValueError as error:
            raise RuntimeError("receipt path escapes aggregate directory") from error
        receipt_raw, receipt = auditor.authenticate_chunk_transcript(
            PACK_MANIFEST, path, (pack, DEPENDENCIES["pack_manifest"][1]))
        report = receipt["report"]
        require(expected_index == record["chunk_index"] == receipt["chunk_index"] and
                hashlib.sha256(receipt_raw).hexdigest() ==
                record["transcript_sha256"] and
                record["residual_range"] == receipt["chunk"]["residual_range"] and
                record["rational_owner_target_total"] ==
                report["covered_target_total"] -
                report["symbolic_certified_target_total"] and
                record["symbolic_owner_target_total"] ==
                report["symbolic_certified_target_total"],
                "receipt identity or ownership index changed")
        reports.append(report)
    return validate_segmented_evidence(aggregate, records, reports, pack)


def audit():
    validate_registry()
    dependencies = audit_dependencies()
    census_digest, census = audit_census()
    auditor = load_module("rank6_order8_pack_for_promotion", PACK_AUDITOR)
    pack, manifest_digest = auditor.authenticate_artifacts(PACK_MANIFEST)
    require(manifest_digest == dependencies["pack_manifest"],
            "promotion owner audited another manifest")
    ownership = segmented_exact_replays(pack)
    manifest = {
        "schema": "rank-six-order-eight-kernel-theorem-master-v1",
        "scope": EXPECTED_SCOPE,
        "kernel_fixture_sha256": dependencies["kernel_fixture"],
        "dependencies": dependencies,
        "final_pack": {
            "manifest_sha256": dependencies["pack_manifest"],
            "covered_key_stream_sha256": pack["covered_key_stream_sha256"],
            "residual_range": [0, 102988],
            "segments": 17,
            "replay": "authenticated receipts from 17 independent exact chunk replays",
            "execution_evidence": str(SEGMENTED_EVIDENCE.relative_to(ROOT)),
            "aggregate_semantics": "authenticated index only; no proof by itself",
        },
        "census": {
            "fixture_sha256": census_digest,
            "kernels": census["kernel_total"],
            "physical_rows": census["physical_total"],
            "automorphism_orbits": census["orbit_total"],
            "coarse_orbits": census["tetrahedral_certified_total"],
            "residual_orbits": census["tetrahedral_residual_total"],
        },
        "frontier": {
            "targets": ownership["certified_targets"],
            "rational_targets": ownership["rational_targets"],
            "symbolic_targets": ownership["symbolic_targets"],
            "complete_disjoint_ownership": True,
            "verification": "authenticated execution receipt for independent exact replay of every manifest chunk",
        },
        "length_scope": "arbitrary positive simple-subdivision lengths via same-parity monotonicity",
        "attachments": "arbitrary finite rooted trees at branch or subdivision vertices",
        "conclusion": EXPECTED_CONCLUSION,
        "excluded_claims": [
            "order-nine or order-ten rank-six kernels",
            "multiblock or all connected hexacyclic graphs",
            "STATE or project-global promotion",
        ],
    }
    return manifest, hashlib.sha256(canonical_bytes(manifest)).hexdigest()


def practical_audit(chunk_index):
    validate_registry()
    dependencies = audit_dependencies()
    census_digest, _ = audit_census()
    auditor = load_module("rank6_order8_pack_for_practical", PACK_AUDITOR)
    pack = auditor.load_manifest(PACK_MANIFEST)
    require(type(chunk_index) is int and 0 <= chunk_index < len(pack["chunks"]),
            "practical chunk index is out of range")
    report = audit_exact_frontier(chunk_index)
    require(report["covered_residual_range"] ==
            pack["chunks"][chunk_index]["residual_range"],
            "practical chunk coverage changed")
    payload = {
        "dependencies": dependencies,
        "census_fixture_sha256": census_digest,
        "pack_manifest_sha256": dependencies["pack_manifest"],
        "chunk_index": chunk_index,
        "covered_residual_range": report["covered_residual_range"],
        "covered_target_total": report["covered_target_total"],
        "theorem_evidence": False,
    }
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def expect_rejected(action, label):
    try:
        action()
    except (RuntimeError, TypeError, ValueError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_self_checks():
    mutations = 0
    for name in DEPENDENCIES:
        changed = deepcopy(DEPENDENCIES)
        del changed[name]
        expect_rejected(lambda changed=changed: validate_registry(changed),
                        f"dependency omitted: {name}")
        mutations += 1
    changed = deepcopy(DEPENDENCIES)
    path, _ = changed["pack_manifest"]
    changed["pack_manifest"] = path, "0" * 64
    expect_rejected(lambda: validate_registry(changed), "manifest digest changed")
    mutations += 1
    expect_rejected(lambda: validate_registry(
        DEPENDENCIES, EXPECTED_SCOPE + ";all-connected-hexacyclic"), "scope widened")
    mutations += 1
    expect_rejected(lambda: validate_registry(
        DEPENDENCIES, EXPECTED_SCOPE, "unchecked status flag"), "conclusion weakened")
    mutations += 1
    valid_report = {
        "status": "complete", "covered_residual_range": [0, 102988],
        "residual_total": 102988, "covered_target_total": 1441832,
        "unresolved_target_total": 24, "symbolic_certified_target_total": 24,
        "unresolved_keys": [[index, None] for index in range(24)],
        "exact_cost_five_target_total": 0, "symbolic_expected_in_coverage": 256,
        "symbolic_rationally_certified_target_total": 232,
        "symbolic_unexpected_target_total": 0, "symbolic_coverage_match": True,
        "exact_audit": True,
    }
    for label, mutate in (
            ("transcript completeness forged", lambda row: row.__setitem__("status", "incomplete")),
            ("transcript target omitted", lambda row: row.__setitem__("covered_target_total", 1441831)),
            ("transcript symbolic ownership forged",
             lambda row: row.__setitem__("symbolic_certified_target_total", 23)),
            ("transcript key duplicated", lambda row: row["unresolved_keys"].__setitem__(1, [0, None]))):
        changed = deepcopy(valid_report)
        mutate(changed)
        expect_rejected(lambda changed=changed: validate_frontier_report(changed), label)
        mutations += 1
    return mutations


def report(digest, mutations):
    return "\n".join((
        "rank-six order-eight kernel theorem: 17 independent exact replay receipts passed",
        "census: kernels=325 physical=1598512 orbits=1045292 coarse=942304 residual=102988",
        "frontier: total=1441832 rational=1441808 symbolic=24 complete=true",
        "lengths: arbitrary same-parity lengthening from canonical-plus-coordinate targets",
        "attachments: arbitrary rooted trees at branch and subdivision vertices",
        "conclusion: s+(G)>=|V(G)| for the order-eight single-block class",
        "nonclaim: no order-nine, order-ten, multiblock, all-connected, STATE, or global conclusion",
        f"exact_dependency_manifest_sha256: {digest}",
        f"rejected_hostile_mutations: {mutations}",
        "verification_layer: committed-independent-exact-chunk-replays",
        "hash_boundary: owner authenticates every receipt; aggregate is no proof by itself",
    )) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-manifest", action="store_true")
    parser.add_argument("--full", action="store_true",
                        help="replay all 1,441,832 exact target audits")
    parser.add_argument("--practical", action="store_true",
                        help="pin the full universe and exactly replay one of 17 chunks")
    parser.add_argument("--chunk-index", type=int, default=0)
    args = parser.parse_args()
    require(args.full != args.practical,
            "select exactly one of --full or --practical")
    if args.practical:
        require(not args.print_manifest,
                "--practical cannot emit a theorem child manifest")
        digest = practical_audit(args.chunk_index)
        sys.stdout.write(
            "rank-six order-eight practical audit: pins and exact chunk replay passed\n"
            f"chunk_index: {args.chunk_index}\n"
            f"practical_audit_sha256: {digest}\n"
            "nonclaim: practical mode is not theorem evidence and emits no child manifest\n")
        return 0
    require(args.chunk_index == 0, "--chunk-index is valid only with --practical")
    manifest, digest = audit()
    mutations = hostile_self_checks()
    require(mutations == len(DEPENDENCIES) + 7, "hostile mutation count changed")
    output = report(digest, mutations)
    if args.print_manifest:
        sys.stdout.write(canonical_bytes(manifest).decode("ascii"))
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
