#!/usr/bin/env python3
"""Exact-execution promotion owner for order-ten rank-six kernels."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPERIMENTS = ROOT / "positive-square-energy" / "experiments"
COVERAGE_GATE = HERE / "rank-six-order-ten-coverage-verifier.py"
PACK_AUDITOR = EXPERIMENTS / "rank6_order10_pack_auditor.py"
DEFAULT_MANIFEST = EXPERIMENTS / "rank6_order10_search_manifest.json"
SEGMENTED_EVIDENCE = (EXPERIMENTS / "rank6_order10_chunk_replays" / "final" /
                      "aggregate.json")
KERNEL_FIXTURE = HERE / "fixtures" / "rank-six-kernels.json"
ANALYTIC_LIFT = HERE / "rank-six-conditional-analytic-lift-verifier.py"
ANALYTIC_LIFT_MANIFEST = HERE / "rank-six-conditional-analytic-lift-manifest.json"
ANALYTIC_LIFT_PROOF_NOTE = (ROOT / "positive-square-energy" / "hexacyclic-general" /
                            "conditional-analytic-lift-proof-note.md")

DEPENDENCIES = {
    "coverage_gate": (COVERAGE_GATE,
        "30a6341dc7a1763b1b87e465b68f44dc140a8dae4d4bd739f7d9b4285ecb0390"),
    "pack_auditor": (PACK_AUDITOR,
        "c6047843a29b9d6755855d165f9b4dac1ede39c8f1002a5fffa97ca663303d8e"),
    "pack_manifest": (DEFAULT_MANIFEST,
        "5162243e0535ca41f72fa0c7bd27e6ee240d485567e56b8c8dfbcf3a4ecbf3b6"),
    "segmented_evidence": (SEGMENTED_EVIDENCE,
        "8c48944fc4a657241ed6519b05acb2af0efefee56064f680f92bad9ddc7bcabf"),
    "kernel_fixture": (KERNEL_FIXTURE,
        "5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476"),
    "census": (EXPERIMENTS / "rank6_order10_cubic_frontier_census.py",
        "536981d000d417b7edaa94461ad3bfa6540c1f400e560c244eec585cae0000de"),
    "witness_stream": (EXPERIMENTS / "rank6_order10_cubic_exact_rational.py",
        "fb419856225aeb513285ae5467233b1cccc096b9632170c6bbfac905abf08827"),
    "equality_recognizer": (EXPERIMENTS / "rank6_order10_equality_recognizer.py",
        "05f85ab4d5bb7d1729c2ab6b6817a89dad7e6d7e740d301d23793aab9fdb1433"),
    "equality_recognizer_fixture": (
        EXPERIMENTS / "rank6_order10_equality_recognizer.json",
        "4344461fd13b0056f719fa6f56963095c9596ff81bdd0e4e0e962dbc0bc7ac74"),
    "symbolic_ledger": (EXPERIMENTS / "rank6_orders8_10_atom_ledger_search.py",
        "6b39d2d1b33d251e505b4b79bd3a4703a440407119c803a26afa1266a2c9461f"),
    "symbolic_ledger_fixture": (
        EXPERIMENTS / "rank6_orders8_10_atom_ledger_classification.json",
        "cc20f4c684ef269297cd7c1d2bc888508fdc31f16cc26e8cb1c2e86792052059"),
    "analytic_lift_owner": (ANALYTIC_LIFT,
        "97c49fa7d1c9c162f4592e0954d63271eb98416fbab59605a9e58a0ada1043df"),
    "analytic_lift_manifest": (ANALYTIC_LIFT_MANIFEST,
        "b6ab90a895fcd7d6ebcf3b32b69676847c35dd7d070e9b8c6c4c13150bda94f6"),
    "analytic_lift_proof_note": (ANALYTIC_LIFT_PROOF_NOTE,
        "2ecc321b60ec42ddf1b8980dffc019eaeaa55738dea5ee014596cf3e814692b4"),
}
ANALYTIC_LIFT_OUTPUT_SHA256 = \
    "a86a7dc77ba8d0a6131acb6d457d4a10129615d156cae3de01e5997b61e40d8a"
MANIFEST_TRANSITIVE_NAMES = {
    "census", "equality_recognizer", "equality_recognizer_fixture",
    "symbolic_ledger", "symbolic_ledger_fixture", "witness_stream",
}
EXPECTED_SCOPE = "order=10;rank=6;kernels=K1133-K1198;single-positive-rank-cyclic-block"
EXPECTED_CONCLUSION = "kappa(B)<=|E(B)|+5;therefore s+(G)>=|V(G)| after rooted-tree lift"
EXPECTED_CENSUS = {
    "kernel_interval": [1133, 1198],
    "kernel_total": 66,
    "physical_total": 1508832,
    "parity_orbit_total": 497572,
    "coarse_certified_total": 372115,
    "coarse_residual_total": 125457,
    "frontier_target_total": 2007312,
}
EXPECTED_SYMBOLIC_PROFILES = {
    "mixed-1_simplex-3-4": 18,
    "mixed-2_simplex-4": 152,
    "mixed-5_simplex-none": 8,
}


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
        raise RuntimeError(f"nonstandard JSON constant in {label}: {value}")

    raw = path.read_bytes()
    try:
        payload = json.loads(raw.decode("ascii"), object_pairs_hook=pairs,
                             parse_constant=reject_constant)
    except (UnicodeError, json.JSONDecodeError) as error:
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
    require(scope == EXPECTED_SCOPE, "promotion scope changed")
    require(conclusion == EXPECTED_CONCLUSION, "promotion conclusion changed")
    lowered = scope.lower()
    require("order=10" in lowered and "rank=6" in lowered and
            "all connected" not in lowered and "multiblock" not in lowered,
            "scope was widened beyond the order-ten single-block class")


def audit_dependencies():
    digests = {}
    for name, (path, expected) in DEPENDENCIES.items():
        require(path.is_file(), f"missing dependency: {name}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        require(actual == expected, f"dependency digest changed: {name}")
        digests[name] = actual
    return digests


def audit_analytic_lift():
    optimize = ("-O",) if sys.flags.optimize else ()
    completed = subprocess.run(
        (sys.executable, *optimize, str(ANALYTIC_LIFT), "--emit", "--print-manifest"),
        check=False, capture_output=True, text=True,
    )
    require(completed.returncode == 0, "pinned conditional analytic lift failed")
    require(completed.stderr == "", "pinned conditional analytic lift wrote stderr")
    require(hashlib.sha256(completed.stdout.encode("ascii")).hexdigest() ==
            ANALYTIC_LIFT_OUTPUT_SHA256, "conditional analytic lift output changed")
    first_line, separator, report = completed.stdout.partition("\n")
    require(separator == "\n" and report, "conditional analytic lift report is missing")
    manifest = json.loads(first_line)
    require(canonical_bytes(manifest) == (first_line + "\n").encode("ascii"),
            "conditional analytic lift manifest is not canonical")
    require(manifest.get("schema") == "rank-six-conditional-analytic-lift-v1" and
            manifest.get("finite_premise", {}).get("result") == "kappa(B)<=|E(B)|+5" and
            manifest.get("conclusion") == "s+(G)>=|V(G)|",
            "conditional analytic lift contract changed")
    require(manifest.get("proof_note") == {
        "path": "positive-square-energy/hexacyclic-general/conditional-analytic-lift-proof-note.md",
        "sha256": DEPENDENCIES["analytic_lift_proof_note"][1],
    }, "conditional analytic lift proof-note ownership changed")
    require("global_claim=false finite_premise_discharged=false" in report,
            "conditional analytic lift lost its nonclaim boundary")


def audit_manifest(manifest_path, dependencies, require_full):
    raw, manifest = strict_json(manifest_path, "order-ten pack manifest")
    require(manifest.get("schema") ==
            "rank-six-order-ten-r10g-search-pack-manifest-v1",
            "pack manifest schema changed")
    require(manifest.get("residual_total") == 125457 and
            manifest.get("frontiers_per_residual") == 16,
            "pack manifest universe changed")
    covered = manifest.get("covered_residual_range")
    require(type(covered) is list and len(covered) == 2 and covered[0] == 0 and
            type(covered[1]) is int and 0 < covered[1] <= 125457 and
            manifest.get("covered_target_total") == covered[1] * 16,
            "pack manifest coverage arithmetic changed")
    chunks = manifest.get("chunks")
    require(type(chunks) is list and chunks, "pack manifest has no segments")
    expected_start = 0
    for index, chunk in enumerate(chunks):
        start, stop = chunk.get("residual_range", [None, None])
        require(start == expected_start and type(stop) is int and start < stop <= 125457,
                f"pack segment {index} is not the next exact range")
        expected_start = stop
    require(expected_start == covered[1], "pack segments disagree with covered range")
    if require_full:
        require(covered == [0, 125457] and
                manifest.get("covered_target_total") == 2007312,
                "promotion gate closed until the full manifest covers all exact targets")
    expected_transitive = {
        "kernel_source": dependencies["kernel_fixture"],
        **{name: dependencies[name] for name in MANIFEST_TRANSITIVE_NAMES},
    }
    require(manifest.get("dependency_sha256") == expected_transitive,
            "manifest transitive dependency registry changed")
    return hashlib.sha256(raw).hexdigest(), manifest


def validate_coverage(payload, ready, manifest_sha256):
    require(ready is True, "coverage gate did not inherit a complete exact replay")
    require(payload.get("schema") == "rank-six-order-ten-master-coverage-v1" and
            payload.get("status") == "ready" and
            payload.get("ready_for_theorem_promotion") is True and
            payload.get("theorem_claimed") is False,
            "coverage gate contract changed")
    require(payload.get("manifest_sha256") == manifest_sha256,
            "coverage gate audited another manifest")
    require(payload.get("census") == EXPECTED_CENSUS, "exact census changed")
    require(payload.get("coverage") == {
        "covered_residual_range": [0, 125457],
        "residual_total": 125457,
        "missing_residual_total": 0,
        "covered_target_total": 2007312,
        "target_total": 2007312,
        "missing_target_total": 0,
    }, "exact full coverage changed")
    ownership = payload.get("ownership", {})
    require(ownership.get("certified_targets") == 2007312 and
            ownership.get("uncertified_covered_targets") == 0 and
            ownership.get("symbolic_dictionary_targets") == 692 and
            ownership.get("unexpected_unresolved_targets") == 0 and
            ownership.get("complete_disjoint_ownership") is True and
            ownership.get("rational_targets") + ownership.get("symbolic_only_targets") ==
            2007312, "exact disjoint ownership changed")
    require(payload.get("lift_contract") == {
        "lengths": "canonical-plus-one-coordinate frontier and fixed-parity monotonicity",
        "attachments": "one-vertex-sum lift for arbitrary finite rooted trees",
    }, "coverage lift contract changed")
    return ownership


def exact_segment_replay(manifest_path, chunk_index):
    auditor = load_module("rank6_order10_segment_for_promotion", PACK_AUDITOR)
    report, complete = auditor.audit(manifest_path, exact=True, chunk_index=chunk_index)
    require(complete and report.get("status") == "complete" and
            report.get("exact_audit") is True and
            report.get("uncertified_target_total") == 0 and
            report.get("exact_certified_target_total") ==
            report.get("covered_target_total"),
            "practical segment exact replay failed")
    require(report.get("census") == EXPECTED_CENSUS, "segment census changed")
    profiles = report.get("symbolic_profiles", {})
    require({name: row.get("decompositions") for name, row in profiles.items()} ==
            EXPECTED_SYMBOLIC_PROFILES, "symbolic profile decomposition counts changed")
    return report


def exact_full_replay(manifest_path, manifest_sha256):
    gate = load_module("rank6_order10_coverage_for_promotion", COVERAGE_GATE)
    payload, ready = gate.completion_payload(manifest_path, exact=True)
    return validate_coverage(payload, ready, manifest_sha256)


def validate_segmented_bookkeeping(aggregate, records, reports, pack):
    require(aggregate.get("schema") ==
            "rank-six-order-ten-chunk-audit-aggregate-v1" and
            aggregate.get("proof_semantics") ==
            "checkpoint_index_only_no_proof_without_exact_replay" and
            aggregate.get("exact_proof") is False,
            "aggregate must remain an index, not an execution claim")
    require(len(records) == len(reports) == len(pack["chunks"]) == 23,
            "segmented evidence must contain exactly 23 execution receipts")
    require([record.get("chunk_index") for record in records] == list(range(23)) and
            [record.get("residual_range") for record in records] ==
            [chunk["residual_range"] for chunk in pack["chunks"]],
            "segmented execution receipt partition changed")
    require(aggregate.get("covered_residual_range") == [0, 125457] and
            aggregate.get("covered_target_total") == 2007312 and
            aggregate.get("manifest_sha256") == DEPENDENCIES["pack_manifest"][1] and
            aggregate.get("manifest_covered_key_stream_sha256") ==
            pack["covered_key_stream_sha256"],
            "segmented aggregate universe changed")
    rational = sum(report.get("disjoint_rational_owner_target_total", -1)
                   for report in reports)
    symbolic = sum(report.get("disjoint_symbolic_owner_target_total", -1)
                   for report in reports)
    certified = sum(report.get("exact_certified_target_total", -1)
                    for report in reports)
    require(certified == rational + symbolic == 2007312 and
            rational == aggregate.get("disjoint_rational_owner_target_total") and
            symbolic == aggregate.get("disjoint_symbolic_owner_target_total") and
            all(report.get("status") == "complete" and
                report.get("exact_audit") is True and
                report.get("uncertified_target_total") == 0
                for report in reports),
            "segmented exact-execution ownership is incomplete")
    return {
        "rational_targets": rational,
        "symbolic_only_targets": symbolic,
        "certified_targets": certified,
        "complete_disjoint_ownership": True,
    }


def hostile_segmented_self_checks(aggregate, records, reports, pack):
    mutations = 0
    for label, mutate in (
            ("aggregate execution claim forged",
             lambda row: row.__setitem__("exact_proof", True)),
            ("aggregate coverage truncated",
             lambda row: row.__setitem__("covered_residual_range", [0, 125456]))):
        changed = deepcopy(aggregate)
        mutate(changed)
        expect_rejected(
            lambda changed=changed: validate_segmented_bookkeeping(
                changed, records, reports, pack), label)
        mutations += 1
    changed_records = deepcopy(records)
    del changed_records[-1]
    expect_rejected(lambda: validate_segmented_bookkeeping(
        aggregate, changed_records, reports, pack), "execution receipt omitted")
    mutations += 1
    changed_reports = deepcopy(reports)
    changed_reports[0]["uncertified_target_total"] = 1
    expect_rejected(lambda: validate_segmented_bookkeeping(
        aggregate, records, changed_reports, pack), "uncertified target forged")
    mutations += 1
    return mutations


def segmented_exact_executions(manifest_path, pack):
    auditor = load_module("rank6_order10_segmented_for_promotion", PACK_AUDITOR)
    raw, aggregate = strict_json(SEGMENTED_EVIDENCE, "segmented execution aggregate")
    require(hashlib.sha256(raw).hexdigest() == DEPENDENCIES["segmented_evidence"][1],
            "segmented aggregate identity changed")
    require(aggregate.get("auditor_sha256") == DEPENDENCIES["pack_auditor"][1] and
            aggregate.get("dependency_sha256") == pack["dependency_sha256"],
            "segmented aggregate transitive identities changed")
    records = aggregate.get("chunks")
    require(type(records) is list, "segmented aggregate chunk index is malformed")
    reports = []
    root = SEGMENTED_EVIDENCE.parent.resolve()
    for expected_index, record in enumerate(records):
        require(type(record) is dict and set(record) == {
            "chunk_index", "path", "residual_range", "key_stream_sha256",
            "ownership_stream_sha256", "transcript_sha256",
        }, "segmented aggregate receipt index fields changed")
        start, stop = record["residual_range"]
        receipt_path = root / f"chunk-{start:05d}-{stop:05d}.json"
        receipt_raw, receipt = auditor.authenticate_chunk_transcript(
            manifest_path, receipt_path, pack)
        require(expected_index == record["chunk_index"] and
                hashlib.sha256(receipt_raw).hexdigest() == record["transcript_sha256"] and
                receipt["chunk_key_stream_sha256"] == record["key_stream_sha256"] and
                receipt["ownership_stream_sha256"] == record["ownership_stream_sha256"],
                "segmented execution receipt identity changed")
        reports.append(receipt["report"])
    ownership = validate_segmented_bookkeeping(aggregate, records, reports, pack)
    mutations = hostile_segmented_self_checks(aggregate, records, reports, pack)
    return ownership, mutations


def build_manifest(dependencies, pack, manifest_sha256, ownership, execution_mode):
    return {
        "schema": "rank-six-order-ten-kernel-theorem-master-v1",
        "scope": EXPECTED_SCOPE,
        "scope_contract": {
            "kernel": "loopless 2-connected cubic rank-six multigraph of order ten",
            "kernel_interval": [1133, 1198],
            "kernel_count": 66,
            "realization": "finite simple positive-length subdivision with exactly one positive-rank cyclic block",
        },
        "kernel_fixture_sha256": dependencies["kernel_fixture"],
        "dependencies": dependencies,
        "analytic_lift_owner": {
            "source_sha256": dependencies["analytic_lift_owner"],
            "manifest_sha256": dependencies["analytic_lift_manifest"],
            "proof_note_sha256": dependencies["analytic_lift_proof_note"],
            "canonical_output_sha256": ANALYTIC_LIFT_OUTPUT_SHA256,
            "premise": "kappa(B)<=|E(B)|+5",
        },
        "final_pack": {
            "manifest_sha256": manifest_sha256,
            "covered_key_stream_sha256": pack["covered_key_stream_sha256"],
            "residual_range": [0, 125457],
            "segments": len(pack["chunks"]),
            "replay": ("fresh streaming exact replay of the complete manifest"
                       if execution_mode == "fresh" else
                       "authenticated receipts from 23 independent exact segment executions"),
            "execution_evidence": (None if execution_mode == "fresh" else
                                   str(SEGMENTED_EVIDENCE.relative_to(ROOT))),
        },
        "census": EXPECTED_CENSUS,
        "frontier": {
            "targets": 2007312,
            "rational_targets": ownership["rational_targets"],
            "symbolic_targets": ownership["symbolic_only_targets"],
            "symbolic_dictionary_targets": 692,
            "symbolic_decompositions_by_profile": EXPECTED_SYMBOLIC_PROFILES,
            "complete_disjoint_ownership": True,
            "verification": "exact execution of every final-manifest segment and target",
        },
        "length_scope": "arbitrary positive simple-subdivision lengths via canonical-plus-coordinate domination and fixed-parity monotonicity",
        "attachments": "arbitrary finite rooted trees at branch or subdivision vertices",
        "conclusion": EXPECTED_CONCLUSION,
        "excluded_claims": [
            "multiblock graphs",
            "all-connected or global hexacyclic theorem",
            "STATE or project-global promotion",
        ],
    }


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
    expect_rejected(lambda: validate_registry(
        DEPENDENCIES, EXPECTED_SCOPE + ";all-connected"), "scope widened")
    mutations += 1
    expect_rejected(lambda: validate_registry(
        DEPENDENCIES, EXPECTED_SCOPE, "ready status only"), "conclusion weakened")
    mutations += 1
    return mutations


def full_audit(manifest_path, execution_mode):
    validate_registry()
    dependencies = audit_dependencies()
    audit_analytic_lift()
    manifest_sha256, pack = audit_manifest(manifest_path, dependencies, require_full=True)
    require(manifest_sha256 == dependencies["pack_manifest"],
            "theorem owner requires the pinned final manifest")
    if execution_mode == "fresh":
        ownership = exact_full_replay(manifest_path, manifest_sha256)
        execution_mutations = 0
    else:
        require(execution_mode == "segmented", "unknown exact-execution mode")
        ownership, execution_mutations = segmented_exact_executions(manifest_path, pack)
    mutations = hostile_self_checks() + execution_mutations
    require(mutations == len(DEPENDENCIES) + 2 + execution_mutations and
            execution_mutations == (4 if execution_mode == "segmented" else 0),
            "hostile mutation count changed")
    manifest = build_manifest(dependencies, pack, manifest_sha256, ownership, execution_mode)
    return manifest, hashlib.sha256(canonical_bytes(manifest)).hexdigest(), mutations


def practical_audit(manifest_path, chunk_index):
    validate_registry()
    dependencies = audit_dependencies()
    audit_analytic_lift()
    manifest_sha256, pack = audit_manifest(manifest_path, dependencies, require_full=False)
    require(0 <= chunk_index < len(pack["chunks"]), "practical segment index is out of range")
    report = exact_segment_replay(manifest_path, chunk_index)
    require(report["covered_residual_range"] == pack["chunks"][chunk_index]["residual_range"],
            "practical segment coverage changed")
    mutations = hostile_self_checks()
    require(mutations == len(DEPENDENCIES) + 2, "hostile mutation count changed")
    payload = {
        "analytic_lift_output_sha256": ANALYTIC_LIFT_OUTPUT_SHA256,
        "dependencies": dependencies,
        "manifest_sha256": manifest_sha256,
        "segment_index": chunk_index,
        "segment": report["covered_residual_range"],
        "certified_targets": report["exact_certified_target_total"],
        "theorem_evidence": False,
    }
    return hashlib.sha256(canonical_bytes(payload)).hexdigest(), report, mutations


def report(digest, mutations, execution_mode):
    return "\n".join((
        "rank-six order-ten kernel theorem: full exact execution evidence passed",
        "census: kernels=66 physical=1508832 orbits=497572 coarse=372115 residual=125457",
        "frontier: total=2007312 symbolic-dictionary=692 complete-disjoint-ownership=true",
        "analytic-lift: pinned conditional owner, manifest, proof note, and canonical output passed",
        "conclusion: s+(G)>=|V(G)| for the order-ten single-positive-rank-block class",
        "nonclaim: no multiblock, all-connected, STATE, or project-global conclusion",
        f"canonical_child_manifest_sha256: {digest}",
        f"rejected_hostile_mutations: {mutations}",
        f"verification_layer: {execution_mode}-exact-executions",
        "hash_boundary: digests authenticate identities; receipt reports record exact executions",
    )) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--full", action="store_true",
                        help="require exact evidence for all 2,007,312 targets")
    parser.add_argument("--execution-mode", choices=("segmented", "fresh"),
                        default="segmented",
                        help="authenticate exact segment receipts or run a fresh full replay")
    parser.add_argument("--print-manifest", action="store_true")
    parser.add_argument("--practical", action="store_true",
                        help="pin the universe and exactly replay one available segment")
    parser.add_argument("--chunk-index", type=int, default=0)
    args = parser.parse_args()
    require(args.full != args.practical,
            "select exactly one of --full or --practical")
    if args.practical:
        require(args.execution_mode == "segmented",
                "--execution-mode is valid only with --full")
        require(not args.print_manifest,
                "--practical cannot emit a theorem child manifest")
        digest, segment, mutations = practical_audit(args.manifest, args.chunk_index)
        sys.stdout.write(
            "rank-six order-ten practical audit: pins and exact segment replay passed\n"
            f"segment_index: {args.chunk_index}\n"
            f"segment_range: {segment['covered_residual_range']}\n"
            f"certified_targets: {segment['exact_certified_target_total']}\n"
            f"practical_audit_sha256: {digest}\n"
            f"rejected_hostile_mutations: {mutations}\n"
            "nonclaim: practical mode is not theorem evidence and emits no child manifest\n")
        return 0
    require(args.chunk_index == 0, "--chunk-index is valid only with --practical")
    manifest, digest, mutations = full_audit(args.manifest, args.execution_mode)
    if args.print_manifest:
        sys.stdout.write(canonical_bytes(manifest).decode("ascii"))
    sys.stdout.write(report(digest, mutations, args.execution_mode))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (IndexError, KeyError, OSError, OverflowError, TypeError, ValueError,
            ZeroDivisionError) as error:
        raise RuntimeError(f"fail-closed malformed input: {error}") from error
