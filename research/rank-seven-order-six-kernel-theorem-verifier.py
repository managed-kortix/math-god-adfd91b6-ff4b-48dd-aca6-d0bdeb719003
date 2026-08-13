#!/usr/bin/env python3
"""Fail-closed theorem wrapper for the completed rank-seven order-six lane."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "positive-square-energy/experiments/rank7_order6_exact_frontier.py"
CENSUS = ROOT / "positive-square-energy/experiments/rank7_order6_exact_frontier.json"
CHUNK = ROOT / "positive-square-energy/experiments/rank7_order6_dim6_chunk_0000_1517.json"
AGGREGATE = ROOT / "positive-square-energy/experiments/rank7_order6_dim6_aggregate.json"
DIGESTS = {
    ENGINE: "6e84dbf7b86fdfb41b5c9b4025424d4be4e561a116e4b81289271dd67fda5e4b",
    CENSUS: "941f6cf2b35a65f76183c1282c20e7662919f7e0380cdd88a55ff5cdc75c94d1",
    CHUNK: "6779df73ff72d38d1776f776f38821d9fb591a89de5b7d63d16be46bb7fab93f",
    AGGREGATE: "3ef27a6b7003b26f4ca7205e07d29cb975bd8a85b8bf654314dcad19023ab315",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def locked_json(path):
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == DIGESTS[path], f"digest changed: {path.name}")
    value = json.loads(raw.decode("ascii"))
    require(raw == (json.dumps(value, sort_keys=True, separators=(",", ":"),
                               allow_nan=False) + "\n").encode("ascii"),
            f"noncanonical JSON: {path.name}")
    return value


def load_engine():
    require(hashlib.sha256(ENGINE.read_bytes()).hexdigest() == DIGESTS[ENGINE],
            "order-six engine digest changed")
    spec = importlib.util.spec_from_file_location("rank7_order6_exact", ENGINE)
    require(spec is not None and spec.loader is not None, "cannot load order-six engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def audit():
    engine = load_engine()
    census = locked_json(CENSUS)
    chunk = locked_json(CHUNK)
    aggregate = locked_json(AGGREGATE)
    engine.verify_census(census)
    engine.verify_chunk(chunk, CENSUS)
    require(aggregate == {
        "census_sha256": DIGESTS[CENSUS],
        "chunks": [{"path": CHUNK.name, "range": [0, 1517],
                    "sha256": DIGESTS[CHUNK]}],
        "exact_residual_total": 1517,
        "exact_target_total": 19721,
        "full_theorem": False,
        "residual_total": 1517,
        "schema": "rank-seven-order-six-dim6-rational-aggregate-v1",
        "status": "complete-exact-frontier-cover",
        "symbolic_equality_geometry_counts": {
            "six-mixed-pairs": 1,
            "tetrahedron-plus-three-mixed-pairs": 1,
        },
        "target_total": 19721,
        "unresolved_geometry_counts": {},
        "unresolved_residual_total": 0,
        "unresolved_source_indices": [],
        "unresolved_target_total": 0,
    }, "aggregate scope or exact partition changed")


def main():
    try:
        audit()
    except (OSError, RuntimeError, TypeError, ValueError, KeyError) as error:
        sys.stderr.write(f"rank-seven order-six theorem: FAIL CLOSED: {error}\n")
        return 1
    sys.stdout.write(
        "rank-seven order-six kernel theorem: exact audit passed\n"
        "order=6; kernels=914; residual_orbits=1517; frontier_targets=19721\n"
        "conclusion=s+(G)>=|V(G)| for rank-seven kernel order six only\n"
        "nonclaim=orders 7-12, multiblock graphs, all connected heptacyclic graphs\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
