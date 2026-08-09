#!/usr/bin/env python3
"""Fail-closed completion gate for the order-nine rank-six proof architecture."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPERIMENTS = ROOT / "positive-square-energy" / "experiments"
AUDITOR_PATH = EXPERIMENTS / "rank6_order9_pack_auditor.py"
DEFAULT_MANIFEST = EXPERIMENTS / "rank6_order9_search_manifest.json"
EXPECTED_CENSUS = {
    "kernel_interval": [971, 1132],
    "kernel_total": 162,
    "physical_total": 1726000,
    "parity_orbit_total": 1108126,
    "coarse_certified_total": 921831,
    "coarse_residual_total": 186295,
    "frontier_target_total": 2794425,
}
EXPECTED_FRONTIERS_PER_RESIDUAL = 15
EXPECTED_SYMBOLIC_DECOMPOSITIONS = 82
EXPECTED_SYMBOLIC_TARGETS = 388


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def completion_payload(manifest_path, exact=True):
    require(manifest_path.is_file(), "manifest is missing")
    auditor = load_module("rank6_order9_completion_pack_auditor", AUDITOR_PATH)
    report, complete = auditor.audit(manifest_path, exact=exact)

    require(report["census"] == EXPECTED_CENSUS, "order-nine census changed")
    require(report["residual_total"] == EXPECTED_CENSUS["coarse_residual_total"],
            "residual universe differs from census")
    require(report["symbolic_decomposition_total"] == EXPECTED_SYMBOLIC_DECOMPOSITIONS,
            "symbolic decomposition census changed")
    require(report["covered_target_total"] ==
            report["covered_residual_range"][1] * EXPECTED_FRONTIERS_PER_RESIDUAL,
            "covered target arithmetic changed")
    require(report["missing_target_total"] ==
            report["missing_residual_total"] * EXPECTED_FRONTIERS_PER_RESIDUAL,
            "missing target arithmetic changed")
    require(report["exact_certified_target_total"] + report["uncertified_target_total"] ==
            report["covered_target_total"], "covered ownership is not exhaustive")
    require(report["disjoint_rational_owner_target_total"] +
            report["disjoint_symbolic_owner_target_total"] ==
            report["exact_certified_target_total"], "target ownership is not disjoint")

    coverage_complete = (
        report["covered_residual_range"] == [0, EXPECTED_CENSUS["coarse_residual_total"]]
        and report["missing_residual_total"] == 0
        and report["covered_target_total"] == EXPECTED_CENSUS["frontier_target_total"]
        and report["missing_target_total"] == 0
    )
    ownership_complete = (
        exact
        and report["exact_audit"] is True
        and report["replay_scope"] == "full-manifest"
        and report["theorem_gate_eligible"] is True
        and report["uncertified_target_total"] == 0
        and report["exact_certified_target_total"] == EXPECTED_CENSUS["frontier_target_total"]
        and report["symbolic_owned_target_total"] == EXPECTED_SYMBOLIC_TARGETS
    )
    ready = complete and coverage_complete and ownership_complete
    require(ready == (report["status"] == "complete"),
            "auditor status disagrees with completion gate")

    manifest_raw = manifest_path.read_bytes()
    return {
        "schema": "rank-six-order-nine-master-coverage-v1",
        "status": "ready" if ready else "blocked_incomplete_coverage",
        "ready_for_theorem_promotion": ready,
        "theorem_claimed": False,
        "manifest": str(manifest_path),
        "manifest_sha256": hashlib.sha256(manifest_raw).hexdigest(),
        "census": report["census"],
        "coverage": {
            "covered_residual_range": report["covered_residual_range"],
            "residual_total": report["residual_total"],
            "missing_residual_total": report["missing_residual_total"],
            "covered_target_total": report["covered_target_total"],
            "target_total": EXPECTED_CENSUS["frontier_target_total"],
            "missing_target_total": report["missing_target_total"],
        },
        "ownership": {
            "rational_targets": report["disjoint_rational_owner_target_total"],
            "symbolic_only_targets": report["disjoint_symbolic_owner_target_total"],
            "certified_targets": report["exact_certified_target_total"],
            "uncertified_covered_targets": report["uncertified_target_total"],
            "symbolic_dictionary_targets": report["symbolic_owned_target_total"],
            "unexpected_unresolved_targets": 0,
            "complete_disjoint_ownership": ownership_complete,
        },
        "lift_contract": {
            "lengths": "canonical-plus-one-coordinate frontier and fixed-parity monotonicity",
            "attachments": "one-vertex-sum lift for arbitrary finite rooted trees",
        },
    }, ready


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--digest-only", action="store_true",
                        help="audit identities and coverage without accepting completion")
    args = parser.parse_args()
    payload, ready = completion_payload(args.manifest, exact=not args.digest_only)
    sys.stdout.write(canonical_bytes(payload).decode("ascii"))
    return 0 if ready else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (IndexError, KeyError, OSError, OverflowError, TypeError, ValueError,
            ZeroDivisionError) as error:
        raise RuntimeError(f"fail-closed malformed input: {error}") from error
