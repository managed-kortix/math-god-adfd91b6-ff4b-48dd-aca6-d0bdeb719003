#!/usr/bin/env python3
"""Layered fail-closed verifier for the order-eight rank-six kernel theorem."""

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
KERNEL_FIXTURE = HERE / "fixtures" / "rank-six-kernels.json"
CENSUS_PROGRAM = EXPERIMENTS / "rank6_order8_orbit_frontier_census.py"
CENSUS_FIXTURE = EXPERIMENTS / "rank6_order8_orbit_frontier_census.json"
PACK_AUDITOR = EXPERIMENTS / "rank6_order8_pack_auditor.py"
PACK_MANIFEST = EXPERIMENTS / "rank6_order8_search_manifest.json"
SYMBOLIC_PROGRAM = EXPERIMENTS / "rank6_order8_symbolic_recognizers.py"
SYMBOLIC_FIXTURE = EXPERIMENTS / "rank6_order8_symbolic_templates.json"
AUDIT_TRANSCRIPT = EXPERIMENTS / "rank6_order8_exact_audit_transcript.json"

DEPENDENCIES = {
    "kernel_fixture": (KERNEL_FIXTURE,
        "5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476"),
    "census_program": (CENSUS_PROGRAM,
        "83527bb0b5dba2cd19040fc23c3c9f02fe4c6bed21620eb1ca7c571b70cb3407"),
    "census_fixture": (CENSUS_FIXTURE,
        "724fdb337b7bb9225b1a8691c28e131ae1c8de7dc38bb13a5adbb98c1f92218e"),
    "pack_auditor": (PACK_AUDITOR,
        "f55352a99317c6b420c59d27f3236f78f6376607813c111c08a6159933d73f00"),
    "pack_manifest": (PACK_MANIFEST,
        "dd97ff3059cd637177171cb5d335cc17889a3714459522232e8110c5d79da469"),
    "symbolic_program": (SYMBOLIC_PROGRAM,
        "755dd24b9e3f129dc6cd4fe590c4c13031bd22c41054ca29082981e3f5d909fe"),
    "symbolic_fixture": (SYMBOLIC_FIXTURE,
        "2f457374d9627bd27339a0988aa47149db825dd0cba050c71ac9accfa3f72b95"),
    "audit_transcript": (AUDIT_TRANSCRIPT,
        "7cb0675f251ed07ad99c72a3be4482b87383e6fc2d4a819dcf064a2849cb3a4f"),
}
EXPECTED_SCOPE = "order=8;rank=6;kernels=K646-K970;single-nontrivial-block"
EXPECTED_CONCLUSION = "kappa(B)<=|E(B)|+5;therefore s+(G)>=|V(G)| after rooted-tree lift"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def strict_json(path, label):
    def reject_constant(value):
        raise ValueError(f"nonstandard JSON constant in {label}: {value}")

    raw = path.read_bytes()
    try:
        payload = json.loads(raw.decode("ascii"), parse_constant=reject_constant)
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
        require(actual == expected, f"dependency digest changed: {name}")
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


def audit_exact_frontier(full=False):
    auditor = load_module("rank6_order8_pack_for_master", PACK_AUDITOR)
    transcript_raw, transcript = auditor.authenticate_transcript(PACK_MANIFEST, AUDIT_TRANSCRIPT)
    transcript_report = validate_frontier_report(transcript["report"])
    if not full:
        return transcript_report, hashlib.sha256(transcript_raw).hexdigest()

    report, complete = auditor.audit(PACK_MANIFEST, exact=True)
    require(complete, "exhaustive exact frontier is incomplete")
    validate_frontier_report(report)
    reproduced = auditor.canonical_bytes(auditor.transcript_payload(PACK_MANIFEST, report))
    require(reproduced == transcript_raw,
            "exhaustive audit does not reproduce the authenticated transcript")
    return report, hashlib.sha256(transcript_raw).hexdigest()


def audit(full=False):
    validate_registry()
    dependencies = audit_dependencies()
    census_digest, census = audit_census()
    frontier, transcript_digest = audit_exact_frontier(full)
    rational_targets = frontier["covered_target_total"] - frontier["unresolved_target_total"]
    require(rational_targets == 1441808, "rational target total changed")
    manifest = {
        "schema": "rank-six-order-eight-kernel-theorem-master-v1",
        "scope": EXPECTED_SCOPE,
        "kernel_fixture_sha256": dependencies["kernel_fixture"],
        "dependencies": dependencies,
        "census": {
            "fixture_sha256": census_digest,
            "kernels": census["kernel_total"],
            "physical_rows": census["physical_total"],
            "automorphism_orbits": census["orbit_total"],
            "coarse_orbits": census["tetrahedral_certified_total"],
            "residual_orbits": census["tetrahedral_residual_total"],
        },
        "frontier": {
            "targets": frontier["covered_target_total"],
            "rational_targets": rational_targets,
            "symbolic_targets": frontier["symbolic_certified_target_total"],
            "complete_disjoint_ownership": True,
            "exact_audit_transcript_sha256": transcript_digest,
        },
        "length_scope": "arbitrary positive simple-subdivision lengths via same-parity monotonicity",
        "attachments": "arbitrary finite rooted trees at branch or subdivision vertices",
        "conclusion": EXPECTED_CONCLUSION,
        "excluded_claims": [
            "order-nine or order-ten rank-six kernels",
            "multiblock or all connected hexacyclic graphs",
        ],
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


def report(digest, mutations, full):
    return "\n".join((
        f"rank-six order-eight kernel theorem: {'exhaustive' if full else 'authenticated'} exact audit passed",
        "census: kernels=325 physical=1598512 orbits=1045292 coarse=942304 residual=102988",
        "frontier: total=1441832 rational=1441808 symbolic=24 complete=true",
        "lengths: arbitrary same-parity lengthening from canonical-plus-coordinate targets",
        "attachments: arbitrary rooted trees at branch and subdivision vertices",
        "conclusion: s+(G)>=|V(G)| for the order-eight single-block class",
        "nonclaim: no order-nine, order-ten, multiblock, or all-hexacyclic conclusion",
        f"exact_dependency_manifest_sha256: {digest}",
        f"rejected_hostile_mutations: {mutations}",
        f"verification_layer: {'full-exhaustive-replay' if full else 'fast-authenticated-transcript'}",
    )) + "\n"


def optimized_output():
    completed = subprocess.run(
        (sys.executable, "-O", str(Path(__file__).resolve()), "--emit"),
        check=False, capture_output=True, text=True)
    require(completed.returncode == 0, "python -O master verifier failed")
    require(completed.stderr == "", "python -O master verifier wrote stderr")
    return completed.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--print-manifest", action="store_true")
    parser.add_argument("--full", action="store_true",
                        help="replay all 1,441,832 exact target audits")
    args = parser.parse_args()
    require(not (args.full and args.emit), "--full and --emit are incompatible")
    manifest, digest = audit(args.full)
    mutations = hostile_self_checks()
    require(mutations == 15, "hostile mutation count changed")
    output = report(digest, mutations, args.full)
    if not args.emit and not args.full and sys.flags.optimize == 0:
        require(optimized_output() == output, "normal and python -O output differ")
    if args.print_manifest:
        sys.stdout.write(canonical_bytes(manifest).decode("ascii"))
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
