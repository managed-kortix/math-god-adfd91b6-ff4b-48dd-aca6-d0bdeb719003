#!/usr/bin/env python3
"""Exact no-optimization Gram sieve for every cubic order-ten residual.

For a parity row put s_uv = multiplicity_uv - 2 odd_uv and

    G = I + S/3.

The cubic degree identity gives sum_v |s_uv| <= 3, so G is a rational
symmetric diagonally dominant correlation matrix and hence is PSD.  The path
cost is bounded by (1-t)/(L(1+t)), where t=(-1)^L G_uv.  This script audits
that formula, including every canonical-plus-two frontier, using Fraction.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
STREAM_PATH = HERE / "rank6_order10_cubic_exact_rational.py"
ATOM_PATH = HERE / "rank6_orders8_10_atom_ledger_classification.json"
EXPECTED = {
    "residual_total": 125457,
    "certified_residuals": 824,
    "strictly_certified_residuals": 822,
    "certified_targets": 13184,
    "simplex_atom_residuals": 108,
    "structural_atom_overlap": 0,
    "combined_fast_lane_residuals": 932,
    "combined_fast_lane_targets": 14912,
    "worst_cost": [10, 1],
}
F = Fraction


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def path_bound(correlation, length):
    transformed = -correlation if length & 1 else correlation
    require(-1 < transformed <= 1, "structural Gram produced an antipodal path")
    return (1 - transformed) / (length * (1 + transformed))


def audit_row(stream, census, source):
    gram = [[F(int(u == v)) for v in range(stream.ORDER)]
            for u in range(stream.ORDER)]
    absolute_rows = [0] * stream.ORDER
    for dense, multiplicity, odd in zip(source[2], source[3], source[4]):
        u, v = census.PAIRS[dense]
        signed_imbalance = multiplicity - 2 * odd
        gram[u][v] = gram[v][u] = F(signed_imbalance, 3)
        absolute_rows[u] += abs(signed_imbalance)
        absolute_rows[v] += abs(signed_imbalance)
    require(max(absolute_rows) <= 3, "cubic diagonal-dominance identity failed")
    require(all(gram[u][u] == 1 and
                sum(abs(gram[u][v]) for v in range(stream.ORDER) if v != u) <= 1
                for u in range(stream.ORDER)), "Gram is not diagonally dominant")

    canonical = []
    extended = []
    for _, _, u, v, length in stream.path_ledger(census, source):
        canonical.append(path_bound(gram[u][v], length))
        extended.append(path_bound(gram[u][v], length + 2))
    base = sum(canonical, F())
    targets = (base,) + tuple(base - old + new
                              for old, new in zip(canonical, extended))
    require(all(frontier <= base for frontier in targets),
            "plus-two frontier increased the structural bound")
    return targets


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def main():
    stream = load(STREAM_PATH, "rank6_order10_structural_stream")
    census = stream.load_census_module()
    residuals = stream.residual_rows(census)
    certified = 0
    strictly_certified = 0
    target_total = 0
    structural_indices = set()
    worst = F()
    worst_indices = []
    for index, source in enumerate(residuals):
        targets = audit_row(stream, census, source)
        local_worst = max(targets)
        if local_worst <= stream.BUDGET:
            certified += 1
            target_total += len(targets)
            structural_indices.add(index)
        if local_worst < stream.BUDGET:
            strictly_certified += 1
        if local_worst > worst:
            worst = local_worst
            worst_indices = [index]
        elif local_worst == worst:
            worst_indices.append(index)
    atom_payload = json.loads(ATOM_PATH.read_text("ascii"))
    atom_indices = set()
    for record in atom_payload["decompositions"]:
        if record["order"] != stream.ORDER:
            continue
        index = record["source_index"]
        require(0 <= index < len(residuals) and
                record["kernel"] == residuals[index][0] and
                tuple(record["row"]) == residuals[index][4],
                "simplex atom fixture does not match residual stream")
        atom_indices.add(index)
    combined = structural_indices | atom_indices
    payload = {
        "schema": "rank-six-order-ten-structural-gram-sieve-v1",
        "formula": "G=I+(multiplicity-2*odd)/3 on support",
        "psd_proof": "symmetric diagonal dominance from cubic weighted degree three",
        "path_upper_bound": "(1-t)/(L*(1+t)), t=(-1)^L*G_uv",
        "residual_total": len(residuals),
        "targets_per_residual": stream.PATH_COUNT + 1,
        "certified_residuals": certified,
        "strictly_certified_residuals": strictly_certified,
        "certified_targets": target_total,
        "simplex_atom_residuals": len(atom_indices),
        "structural_atom_overlap": len(structural_indices & atom_indices),
        "combined_fast_lane_residuals": len(combined),
        "combined_fast_lane_targets": len(combined) * (stream.PATH_COUNT + 1),
        "worst_cost": [worst.numerator, worst.denominator],
        "worst_source_indices": worst_indices,
    }
    for key, value in EXPECTED.items():
        require(payload[key] == value, f"structural census changed at {key}: {payload[key]}")
    encoded = canonical_bytes(payload)
    print(encoded.decode("ascii"), end="")
    print(f"sha256={hashlib.sha256(encoded).hexdigest()}")


if __name__ == "__main__":
    main()
