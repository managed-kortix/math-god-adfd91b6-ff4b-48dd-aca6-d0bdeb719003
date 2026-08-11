#!/usr/bin/env python3
"""Full exact promotion owner for order-nine rank-six kernels."""

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
COVERAGE_GATE = HERE / "rank-six-order-nine-coverage-verifier.py"
PACK_AUDITOR = EXPERIMENTS / "rank6_order9_pack_auditor.py"
PACK_MANIFEST = EXPERIMENTS / "rank6_order9_search_manifest.json"
KERNEL_FIXTURE = HERE / "fixtures" / "rank-six-kernels.json"
ANALYTIC_LIFT = HERE / "rank-six-conditional-analytic-lift-verifier.py"
ANALYTIC_LIFT_MANIFEST = HERE / "rank-six-conditional-analytic-lift-manifest.json"
ANALYTIC_LIFT_PROOF_NOTE = (ROOT / "positive-square-energy" / "hexacyclic-general" /
                            "conditional-analytic-lift-proof-note.md")

DEPENDENCIES = {
    "coverage_gate": (COVERAGE_GATE,
        "b66526e79d9b716f8c98b19dce8fc8557a0f34534f1890db595c514fa3438ff1"),
    "pack_auditor": (PACK_AUDITOR,
        "24d57b3b72b9f45b172981ad7a7e02e46749800dfb3478dc7d92751c9d8b8ce3"),
    "pack_manifest": (PACK_MANIFEST,
        "8aa9d797d9ed786ad438d6fd685e0ec576247b45c17a14749b76c45eebbe9168"),
    "kernel_fixture": (KERNEL_FIXTURE,
        "5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476"),
    "witness_pipeline": (EXPERIMENTS / "rank6_order9_sparse_witness.py",
        "0b916f2844acb878ca33f9203db8ac6cb2b165fe417f3a0b6625cf1776b0d4a6"),
    "sparse_base": (EXPERIMENTS / "rank6_order8_sparse_pipeline.py",
        "3b262613edfee4961fe990675c9a7003d595ed58c2b034d928c99daee1345f42"),
    "rational_engine": (ROOT / "pentacyclic" / "research" /
                        "order7-dim7-rational-gram-experiment.py",
        "0d7acde3eec194772dd00f7e4897e0355e2347482c8e0fdfce26f9e8473394cc"),
    "symbolic_recognizer": (EXPERIMENTS / "rank6_order9_symbolic_recognizers.py",
        "05429f9bd4c5fad16e91e4a0f65c35f1510bbcfff41bd471e6367ae22aa9f1ea"),
    "atom_classifier": (EXPERIMENTS / "rank6_orders8_10_atom_ledger_search.py",
        "6b39d2d1b33d251e505b4b79bd3a4703a440407119c803a26afa1266a2c9461f"),
    "atom_classification": (
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
    "atom_classification", "atom_classifier", "kernel_source", "rational_engine",
    "sparse_base", "symbolic_recognizer", "witness_pipeline",
}
EXPECTED_SCOPE = "order=9;rank=6;kernels=K971-K1132;single-nontrivial-block"
EXPECTED_CONCLUSION = "kappa(B)<=|E(B)|+5;therefore s+(G)>=|V(G)| after rooted-tree lift"
EXPECTED_CENSUS = {
    "kernel_interval": [971, 1132],
    "kernel_total": 162,
    "physical_total": 1726000,
    "parity_orbit_total": 1108126,
    "coarse_certified_total": 921831,
    "coarse_residual_total": 186295,
    "frontier_target_total": 2794425,
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
    require(scope == EXPECTED_SCOPE, "theorem scope changed")
    require(conclusion == EXPECTED_CONCLUSION, "theorem conclusion changed")
    lowered = scope.lower()
    require("order=9" in lowered and "rank=6" in lowered and
            "all connected" not in lowered and "multiblock" not in lowered,
            "scope was widened beyond the order-nine single-block class")


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
    raw = completed.stdout.encode("ascii")
    require(hashlib.sha256(raw).hexdigest() == ANALYTIC_LIFT_OUTPUT_SHA256,
            "conditional analytic lift canonical output changed")
    first_line, separator, report = completed.stdout.partition("\n")
    require(separator == "\n" and report, "conditional analytic lift report is missing")
    try:
        manifest = json.loads(first_line)
    except json.JSONDecodeError as error:
        raise RuntimeError("conditional analytic lift manifest is malformed") from error
    require(canonical_bytes(manifest) == (first_line + "\n").encode("ascii"),
            "conditional analytic lift manifest output is not canonical")
    require(manifest.get("schema") == "rank-six-conditional-analytic-lift-v1" and
            manifest.get("finite_premise", {}).get("result") ==
            "kappa(B)<=|E(B)|+5" and
            manifest.get("conclusion") == "s+(G)>=|V(G)|",
            "conditional analytic lift contract changed")
    require(manifest.get("proof_note") == {
        "path": "positive-square-energy/hexacyclic-general/conditional-analytic-lift-proof-note.md",
        "sha256": DEPENDENCIES["analytic_lift_proof_note"][1],
    }, "conditional analytic lift proof-note ownership changed")
    require("global_claim=false finite_premise_discharged=false" in report,
            "conditional analytic lift lost its nonclaim boundary")


def audit_manifest(dependencies):
    raw, manifest = strict_json(PACK_MANIFEST, "final order-nine pack manifest")
    require(hashlib.sha256(raw).hexdigest() == dependencies["pack_manifest"],
            "final manifest identity changed")
    require(manifest.get("schema") ==
            "rank-six-order-nine-r9g-search-pack-manifest-v1",
            "final manifest schema changed")
    require(manifest.get("covered_residual_range") == [0, 186295] and
            manifest.get("residual_total") == 186295 and
            manifest.get("frontiers_per_residual") == 15 and
            manifest.get("covered_target_total") == 2794425,
            "final manifest is not the exact full order-nine universe")
    chunks = manifest.get("chunks")
    require(type(chunks) is list and len(chunks) == 9, "final chunk partition changed")
    expected_start = 0
    for index, chunk in enumerate(chunks):
        start, stop = chunk.get("residual_range", [None, None])
        require(start == expected_start and type(stop) is int and start < stop <= 186295,
                f"final chunk {index} is not the next exact segment")
        expected_start = stop
    require(expected_start == 186295, "final chunks do not cover [0,186295)")
    expected_transitive = {
        "kernel_source": dependencies["kernel_fixture"],
        **{name: dependencies[name] for name in MANIFEST_TRANSITIVE_NAMES
           if name != "kernel_source"},
    }
    require(manifest.get("dependency_sha256") == expected_transitive,
            "manifest transitive dependency registry changed")
    return manifest


def validate_coverage(payload, ready):
    require(ready is True, "coverage gate did not inherit a complete exact replay")
    require(payload.get("schema") == "rank-six-order-nine-master-coverage-v1" and
            payload.get("status") == "ready" and
            payload.get("ready_for_theorem_promotion") is True and
            payload.get("theorem_claimed") is False,
            "coverage gate contract changed")
    require(payload.get("manifest_sha256") == DEPENDENCIES["pack_manifest"][1],
            "coverage gate audited a different final manifest")
    require(payload.get("census") == EXPECTED_CENSUS, "exact census changed")
    require(payload.get("coverage") == {
        "covered_residual_range": [0, 186295],
        "residual_total": 186295,
        "missing_residual_total": 0,
        "covered_target_total": 2794425,
        "target_total": 2794425,
        "missing_target_total": 0,
    }, "exact full coverage changed")
    ownership = payload.get("ownership", {})
    require(ownership.get("certified_targets") == 2794425 and
            ownership.get("uncertified_covered_targets") == 0 and
            ownership.get("symbolic_dictionary_targets") == 388 and
            ownership.get("unexpected_unresolved_targets") == 0 and
            ownership.get("complete_disjoint_ownership") is True and
            ownership.get("rational_targets") + ownership.get("symbolic_only_targets") ==
            2794425, "exact disjoint ownership changed")
    require(payload.get("lift_contract") == {
        "lengths": "canonical-plus-one-coordinate frontier and fixed-parity monotonicity",
        "attachments": "one-vertex-sum lift for arbitrary finite rooted trees",
    }, "coverage lift contract changed")
    return ownership


def exact_replay(chunk_index=None):
    if chunk_index is not None:
        auditor = load_module("rank6_order9_segment_for_promotion", PACK_AUDITOR)
        report, complete = auditor.audit(PACK_MANIFEST, exact=True, chunk_index=chunk_index)
        require(complete and report.get("status") == "complete" and
                report.get("replay_scope") == "single-chunk" and
                report.get("theorem_gate_eligible") is False and
                report.get("uncertified_target_total") == 0,
                "practical segment exact replay failed")
        return report
    gate = load_module("rank6_order9_coverage_for_promotion", COVERAGE_GATE)
    payload, ready = gate.completion_payload(PACK_MANIFEST, exact=True)
    return payload, validate_coverage(payload, ready)


def build_manifest(dependencies, pack, ownership):
    return {
        "schema": "rank-six-order-nine-kernel-theorem-master-v1",
        "scope": EXPECTED_SCOPE,
        "scope_contract": {
            "kernel": "loopless 2-connected rank-six multigraph of order nine and minimum degree at least three",
            "kernel_interval": [971, 1132],
            "kernel_count": 162,
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
            "manifest_sha256": dependencies["pack_manifest"],
            "covered_key_stream_sha256": pack["covered_key_stream_sha256"],
            "residual_range": [0, 186295],
            "segments": len(pack["chunks"]),
            "replay": "fresh streaming exact replay, one XZ segment at a time",
        },
        "census": EXPECTED_CENSUS,
        "frontier": {
            "targets": 2794425,
            "rational_targets": ownership["rational_targets"],
            "symbolic_targets": ownership["symbolic_only_targets"],
            "symbolic_dictionary_targets": 388,
            "complete_disjoint_ownership": True,
            "verification": "exact replay of every final-manifest segment and target",
        },
        "length_scope": "arbitrary positive simple-subdivision lengths via canonical-plus-coordinate domination and fixed-parity monotonicity",
        "length_implication": "for canonical c and any same-parity l>=c, use c if l=c, otherwise choose i with c+2e_i<=l and lengthen by two coordinatewise",
        "attachments": "arbitrary finite rooted trees at branch or subdivision vertices",
        "tree_implication": "if the block has L edges and attached trees have t edges, then |V(B)|=L-5 and kappa(G)<=L+5+t; the DNN trace identity gives s+(G)>=|V(G)|",
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
    changed = deepcopy(DEPENDENCIES)
    path, _ = changed["pack_manifest"]
    changed["pack_manifest"] = path, "0" * 64
    expect_rejected(lambda: validate_registry(changed), "final manifest digest changed")
    mutations += 1
    expect_rejected(lambda: validate_registry(
        DEPENDENCIES, EXPECTED_SCOPE + ";all-connected"), "scope widened")
    mutations += 1
    expect_rejected(lambda: validate_registry(
        DEPENDENCIES, EXPECTED_SCOPE, "ready status only"), "conclusion weakened")
    mutations += 1
    return mutations


def audit():
    validate_registry()
    dependencies = audit_dependencies()
    audit_analytic_lift()
    pack = audit_manifest(dependencies)
    _, ownership = exact_replay()
    mutations = hostile_self_checks()
    require(mutations == len(DEPENDENCIES) + 3, "hostile mutation count changed")
    manifest = build_manifest(dependencies, pack, ownership)
    return manifest, hashlib.sha256(canonical_bytes(manifest)).hexdigest(), mutations


def practical_audit():
    validate_registry()
    dependencies = audit_dependencies()
    audit_analytic_lift()
    pack = audit_manifest(dependencies)
    report = exact_replay(chunk_index=0)
    require(report["covered_residual_range"] == pack["chunks"][0]["residual_range"] and
            report["exact_certified_target_total"] == 150000,
            "practical segment coverage changed")
    mutations = hostile_self_checks()
    require(mutations == len(DEPENDENCIES) + 3, "hostile mutation count changed")
    return hashlib.sha256(canonical_bytes({
        "dependencies": dependencies,
        "analytic_lift_output_sha256": ANALYTIC_LIFT_OUTPUT_SHA256,
        "manifest_sha256": dependencies["pack_manifest"],
        "segment": report["covered_residual_range"],
        "certified_targets": report["exact_certified_target_total"],
    })).hexdigest(), mutations


def report(digest, mutations):
    return "\n".join((
        "rank-six order-nine kernel theorem: streaming full exact audit passed",
        "census: kernels=162 physical=1726000 orbits=1108126 coarse=921831 residual=186295",
        "frontier: total=2794425 complete-disjoint-ownership=true",
        "analytic-lift: pinned conditional owner, manifest, proof note, and canonical output passed",
        "lengths: arbitrary positive simple subdivisions by canonical-plus-coordinate domination",
        "attachments: arbitrary rooted trees at branch and subdivision vertices",
        "conclusion: s+(G)>=|V(G)| for the order-nine single-positive-rank-block class",
        "nonclaim: no multiblock, all-connected, STATE, or global conclusion",
        f"canonical_child_manifest_sha256: {digest}",
        f"rejected_hostile_mutations: {mutations}",
        "verification_layer: full-exact-segmented-replay",
    )) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true",
                        help="required: replay all 2,794,425 targets segment by segment")
    parser.add_argument("--print-manifest", action="store_true")
    parser.add_argument("--practical", action="store_true",
                        help="pin the full universe and exactly replay the first segment")
    args = parser.parse_args()
    require(args.full != args.practical,
            "select exactly one of --full or --practical; practical mode emits no theorem manifest")
    if args.practical:
        require(not args.print_manifest, "--practical cannot emit a theorem child manifest")
        digest, mutations = practical_audit()
        sys.stdout.write(
            "rank-six order-nine practical audit: pins passed; segment 0 exact replay passed\n"
            f"practical_audit_sha256: {digest}\n"
            f"rejected_hostile_mutations: {mutations}\n"
            "nonclaim: practical mode is not theorem evidence and emits no child manifest\n")
        return 0
    manifest, digest, mutations = audit()
    if args.print_manifest:
        sys.stdout.write(canonical_bytes(manifest).decode("ascii"))
    sys.stdout.write(report(digest, mutations))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (IndexError, KeyError, OSError, OverflowError, TypeError, ValueError,
            ZeroDivisionError) as error:
        raise RuntimeError(f"fail-closed malformed input: {error}") from error
