#!/usr/bin/env python3
"""Exact simplex/apex and signed-cycle recognizer for order-nine residuals."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PIPELINE_PATH = ROOT / "positive-square-energy" / "experiments" / "rank6_order9_sparse_witness.py"
HELPERS_PATH = ROOT / "positive-square-energy" / "experiments" / "rank6_order8_symbolic_recognizers.py"
ARTIFACT = ROOT / "positive-square-energy" / "experiments" / "rank6_order9_symbolic_templates.json"
SCHEMA = "rank-six-order-nine-symbolic-templates-v1"
F = Fraction
EXPECTED_CLASSIFICATION_SHA256 = "fa388fbda325f2d712e70a711438782693ec6a3d820edecd2f4d7944fbe35033"
EXPECTED_ARTIFACT_SHA256 = "16bfd7e8a5df832a48eb9e09b07a1de48002c286b721defd1d93d17a78343880"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def reject_constant(value):
    raise ValueError(f"nonstandard JSON constant: {value}")


def edge_name(edge):
    return f"{edge[0]}{edge[1]}"


def pair(value):
    return [value.numerator, value.denominator]


def path_ledger(pipeline, support, multiplicities, row):
    paths = []
    for index, multiplicity, odd in zip(support, multiplicities, row):
        edge = pipeline.PAIRS[index]
        occurrence = 0
        if odd:
            paths.append((edge, occurrence, 1))
            occurrence += 1
            for _ in range(odd - 1):
                paths.append((edge, occurrence, 3))
                occurrence += 1
        for _ in range(multiplicity - odd):
            paths.append((edge, occurrence, 2))
            occurrence += 1
    require(len(paths) == pipeline.PATH_COUNT, "path ledger width changed")
    return tuple(paths)


def classify_targets(pipeline, source, gram, contractions):
    _, support, multiplicities, row, _, _, _ = source
    paths = path_ledger(pipeline, support, multiplicities, row)
    contraction_set = set(contractions)
    targets = [{"frontier": None, "relation": "eq", "cost": pair(pipeline.BUDGET)}]
    for coordinate, (edge, occurrence, length) in enumerate(paths):
        correlation = gram[edge[0]][edge[1]]
        transformed = correlation if length % 2 == 0 else -correlation
        is_contraction = edge in contraction_set
        if is_contraction:
            require(transformed == 1, "contraction coordinate has positive cost")
        else:
            require(transformed != 1, "unlisted zero-cost coordinate")
        targets.append({
            "frontier": coordinate,
            "edge": edge_name(edge),
            "occurrence": occurrence,
            "canonical_length": length,
            "canonical_local_cost_zero": is_contraction,
            "relation": "eq" if is_contraction else "lt",
        })
    require(len(targets) == pipeline.PATH_COUNT + 1, "frontier width changed")
    return targets


def exact_canonical_audit(pipeline, helpers, source, gram, contractions, geometry):
    _, support, multiplicities, row, _, _, _ = source
    helpers.audit_psd(gram)
    row_by_edge = {pipeline.PAIRS[index]: odd for index, odd in zip(support, row)}
    multiplicity_by_edge = {pipeline.PAIRS[index]: value
                            for index, value in zip(support, multiplicities)}
    contraction_set = set(contractions)
    total = F()
    positive_atoms = 0
    for edge, multiplicity in multiplicity_by_edge.items():
        correlation = gram[edge[0]][edge[1]]
        odd = row_by_edge[edge]
        if edge in contraction_set:
            transformed = -correlation if odd else correlation
            require(multiplicity == 1 and transformed == 1,
                    "invalid signed contraction atom")
            continue
        if multiplicity == 2:
            require(odd == 1 and abs(correlation) == F(1, 2),
                    "invalid mixed-pair atom")
            total += F(1)
        else:
            require(multiplicity == 1 and odd == 1 and
                    (-correlation) == F(1, 3), "invalid simplex odd atom")
            total += F(1, 2)
        positive_atoms += 1
    require(total == pipeline.BUDGET, "symbolic canonical cost is not five")
    if geometry == "signed-five-cycle":
        require(positive_atoms == 5, "signed-cycle atom count changed")
    else:
        require(positive_atoms == 8, "simplex/apex atom count changed")


def derive_payload():
    pipeline = load_module("rank6_order9_symbolic_pipeline", PIPELINE_PATH)
    helpers = load_module("rank6_order9_symbolic_helpers", HELPERS_PATH)
    require((pipeline.ORDER, pipeline.RANK, pipeline.PATH_COUNT) == (9, 6, 14),
            "pipeline scope changed")

    structures = []
    for source in pipeline.source_kernels():
        structures.extend(helpers.tetra_apex_structures(pipeline, source))
    by_kernel = {}
    for structure in structures:
        by_kernel.setdefault(structure["kernel"], []).append(structure)

    census, residuals = pipeline.census(collect_residuals=True)
    require(census["coarse_residual_total"] == 186295 and len(residuals) == 186295,
            "residual universe changed")
    require(census["frontier_target_total"] == 2794425,
            "frontier universe changed")

    records = []
    geometry_counts = {}
    classification_digest = hashlib.sha256()
    for source_index, source in enumerate(residuals):
        number, support, multiplicities, row, orbit_size, coarse_cost, cycle = source
        matches = []
        if cycle:
            gram, contractions = helpers.signed_cycle_gram(pipeline, source)
            matches.append(("signed-five-cycle", gram, contractions))
        for structure in by_kernel.get(number, ()):
            gram = helpers.recognize_tetra_apex_row(
                pipeline, structure, support, multiplicities, row)
            if gram is not None:
                matches.append(("tetrahedron-plus-apex", gram,
                                structure["contractions"]))
        require(len(matches) <= 1, "residual row has multiple symbolic geometries")
        if not matches:
            classification_digest.update(canonical_bytes([source_index, 0]))
            continue
        geometry, gram, contractions = matches[0]
        exact_canonical_audit(pipeline, helpers, source, gram, contractions, geometry)
        targets = classify_targets(pipeline, source, gram, contractions)
        record = {
            "source_index": source_index,
            "kernel": number,
            "row": list(row),
            "orbit_size": orbit_size,
            "coarse_cost_scaled": coarse_cost,
            "geometry": geometry,
            "contractions": [edge_name(edge) for edge in contractions],
            "targets": targets,
        }
        records.append(record)
        geometry_counts[geometry] = geometry_counts.get(geometry, 0) + 1
        classification_digest.update(canonical_bytes([source_index, 1, geometry]))

    equality = sum(target["relation"] == "eq" for record in records
                   for target in record["targets"])
    strict = sum(target["relation"] == "lt" for record in records
                 for target in record["targets"])
    return {
        "schema": SCHEMA,
        "status": "symbolic_equality_predictions_classified",
        "full_theorem": False,
        "scope": "all 186295 order-nine residual supports; no numerical or full search",
        "source_sha256": pipeline.SOURCE_SHA256,
        "residual_stream_sha256": "2a6f0c88d8c03116096e583235bec1688a64ee5c4af0e2f61114be73b5e31807",
        "classification_stream_sha256": classification_digest.hexdigest(),
        "rank": pipeline.RANK,
        "order": pipeline.ORDER,
        "kernel_interval": list(pipeline.KERNEL_INTERVAL),
        "residual_total": len(residuals),
        "frontier_universe_total": census["frontier_target_total"],
        "recognized_row_total": len(records),
        "recognized_target_total": equality + strict,
        "predicted_equality_target_total": equality,
        "strict_coordinate_frontier_total": strict,
        "geometry_counts": geometry_counts,
        "strictness_lemma": "same-parity lengthening by two strictly lowers positive path energy; contractions remain zero",
        "records": records,
    }


def validate_shape(payload):
    require(type(payload) is dict and payload["schema"] == SCHEMA,
            "bad artifact schema")
    require(payload["status"] == "symbolic_equality_predictions_classified" and
            payload["full_theorem"] is False, "bad theorem status")
    require((payload["rank"], payload["order"], payload["kernel_interval"],
             payload["residual_total"], payload["frontier_universe_total"]) ==
            (6, 9, [971, 1132], 186295, 2794425), "artifact scope changed")
    require(payload["source_sha256"] ==
            "5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476",
            "source commitment changed")
    require(payload["residual_stream_sha256"] ==
            "2a6f0c88d8c03116096e583235bec1688a64ee5c4af0e2f61114be73b5e31807",
            "residual commitment changed")
    require(payload["classification_stream_sha256"] == EXPECTED_CLASSIFICATION_SHA256,
            "classification commitment changed")
    for key in ("recognized_row_total", "recognized_target_total",
                "predicted_equality_target_total", "strict_coordinate_frontier_total"):
        require(type(payload[key]) is int and payload[key] >= 0, f"bad {key}")
    require(type(payload["records"]) is list and
            len(payload["records"]) == payload["recognized_row_total"],
            "record count changed")
    require(payload["recognized_target_total"] ==
            payload["predicted_equality_target_total"] +
            payload["strict_coordinate_frontier_total"], "target partition changed")
    require((payload["recognized_row_total"], payload["recognized_target_total"],
             payload["predicted_equality_target_total"],
             payload["strict_coordinate_frontier_total"], payload["geometry_counts"]) ==
            (10, 150, 50, 100, {"signed-five-cycle": 10}),
            "pinned symbolic classification changed")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", type=Path, default=ARTIFACT)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--optimized-child", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    derived = derive_payload()
    validate_shape(derived)
    if args.write:
        require(args.artifact.parent.is_dir(), "artifact parent is missing")
        args.artifact.write_bytes(canonical_bytes(derived))
    raw = args.artifact.read_bytes()
    stored = json.loads(raw.decode("ascii"), parse_constant=reject_constant)
    require(raw == canonical_bytes(stored), "artifact is not canonical JSON")
    require(hashlib.sha256(raw).hexdigest() == EXPECTED_ARTIFACT_SHA256,
            "artifact commitment changed")
    validate_shape(stored)
    require(stored == derived, "artifact differs from exact symbolic derivation")

    output = (f"residuals={stored['residual_total']} recognized_rows="
              f"{stored['recognized_row_total']} equality_targets="
              f"{stored['predicted_equality_target_total']} strict_frontiers="
              f"{stored['strict_coordinate_frontier_total']}\n"
              f"geometries={json.dumps(stored['geometry_counts'], sort_keys=True, separators=(',', ':'))}\n"
              f"artifact_sha256={hashlib.sha256(raw).hexdigest()}\n"
              "scope=SYMBOLIC_EQUALITY_CLASSIFICATION full_theorem=false")
    print(output)
    if __debug__ and not args.optimized_child:
        command = [sys.executable, "-O", str(Path(__file__).resolve()),
                   "--artifact", str(args.artifact), "--optimized-child"]
        completed = subprocess.run(command, check=True, capture_output=True, text=True)
        require(completed.stdout == output + "\n", "normal and -O verifier outputs differ")


if __name__ == "__main__":
    try:
        main()
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as error:
        raise RuntimeError(f"fail-closed malformed input: {error}") from error
