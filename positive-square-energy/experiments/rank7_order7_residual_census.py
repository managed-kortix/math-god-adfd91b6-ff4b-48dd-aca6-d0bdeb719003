#!/usr/bin/env python3
"""Exact sparse residual-orbit census for rank-seven order-seven kernels."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import lzma
import multiprocessing
import os
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE_ENGINE = HERE / "rank7_parity_coarse_digest_census.py"
OUTPUT = HERE / "rank7_order7_residual_census.json.xz"
SCHEMA = "rank-seven-order-seven-exact-residual-census-v1"
ORDER = 7
RANK = 7
PATH_COUNT = ORDER + RANK - 1
FRONTIERS_PER_RESIDUAL = PATH_COUNT + 1


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def load_source_engine():
    spec = importlib.util.spec_from_file_location("rank7_order7_coarse", SOURCE_ENGINE)
    require(spec is not None and spec.loader is not None, "cannot load coarse engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def census_kernel(item):
    engine = load_source_engine()
    global_index, local_index, order, edges = item
    require(order == ORDER, "wrong order item")
    actions = engine.automorphism_actions(order, edges)
    orbit_sizes = {}
    for row in itertools.product(*(range(multiplicity + 1) for _, _, multiplicity in edges)):
        representative = min(engine.apply_action(row, action) for action in actions)
        orbit_sizes[representative] = orbit_sizes.get(representative, 0) + 1
    residuals = []
    for row in sorted(orbit_sizes):
        if engine.is_coarse_residual(order, edges, row):
            residuals.append([list(row), orbit_sizes[row]])
    return {
        "global_kernel": global_index,
        "order_kernel": local_index,
        "edges": [list(edge) for edge in edges],
        "automorphisms": len(actions),
        "physical_rows": sum(orbit_sizes.values()),
        "parity_orbits": len(orbit_sizes),
        "coarse_residuals": len(residuals),
    }, residuals


def regenerate(jobs, progress):
    engine = load_source_engine()
    source_raw = engine.SOURCE.read_bytes()
    items = tuple(item for item in engine.source_kernels() if item[2] == ORDER)
    require(len(items) == 2270, "order-seven kernel count changed")
    if jobs == 1:
        results = map(census_kernel, items)
        pool = None
    else:
        pool = multiprocessing.get_context("fork").Pool(jobs)
        results = pool.imap(census_kernel, items, chunksize=1)
    kernels = []
    residuals = []
    residual_digest = hashlib.sha256()
    try:
        for position, (ledger, local) in enumerate(results, 1):
            kernels.append(ledger)
            for row, orbit_size in local:
                record = {
                    "source_index": len(residuals),
                    "global_kernel": ledger["global_kernel"],
                    "order_kernel": ledger["order_kernel"],
                    "row": row,
                    "orbit_size": orbit_size,
                }
                residual_digest.update(canonical_bytes(record))
                residuals.append(record)
            if progress:
                print(f"[{position}/{len(items)}] K{ledger['global_kernel']} "
                      f"orbits={ledger['parity_orbits']} residuals={len(local)}", flush=True)
    finally:
        if pool is not None:
            pool.close()
            pool.join()
    return {
        "schema": SCHEMA,
        "status": "exact-sparse-residual-census-search-open",
        "full_theorem": False,
        "rank": RANK,
        "order": ORDER,
        "dimension": ORDER,
        "budget": [RANK - 1, 1],
        "path_count": PATH_COUNT,
        "frontiers_per_residual": FRONTIERS_PER_RESIDUAL,
        "frontier_policy": "canonical plus every one-coordinate length-plus-two target",
        "source_sha256": hashlib.sha256(source_raw).hexdigest(),
        "kernel_total": len(kernels),
        "physical_row_total": sum(row["physical_rows"] for row in kernels),
        "parity_orbit_total": sum(row["parity_orbits"] for row in kernels),
        "coarse_certified_total": (sum(row["parity_orbits"] for row in kernels)
                                     - len(residuals)),
        "coarse_residual_total": len(residuals),
        "frontier_target_total": len(residuals) * FRONTIERS_PER_RESIDUAL,
        "residual_stream_sha256": residual_digest.hexdigest(),
        "kernels": kernels,
        "residuals": residuals,
    }


def read_artifact(path):
    stored = path.read_bytes()
    raw = lzma.decompress(stored) if path.suffix == ".xz" else stored
    payload = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(payload), "census is not canonical JSON")
    return payload, raw, stored


def verify(payload):
    require(payload["schema"] == SCHEMA and payload["full_theorem"] is False,
            "wrong census schema")
    require((payload["rank"], payload["order"], payload["dimension"],
             payload["budget"], payload["path_count"], payload["kernel_total"])
            == (7, 7, 7, [6, 1], 13, 2270), "census scope changed")
    require(payload["coarse_certified_total"] + payload["coarse_residual_total"]
            == payload["parity_orbit_total"], "coarse partition changed")
    require(payload["frontiers_per_residual"] == 14 and
            payload["frontier_target_total"] == 14 * payload["coarse_residual_total"],
            "frontier total changed")
    require(len(payload["kernels"]) == 2270 and
            len(payload["residuals"]) == payload["coarse_residual_total"],
            "materialization is incomplete")
    digest = hashlib.sha256()
    for index, record in enumerate(payload["residuals"]):
        require(record["source_index"] == index, "residual order changed")
        ledger = payload["kernels"][record["order_kernel"] - 1]
        require(record["global_kernel"] == ledger["global_kernel"] and
                len(record["row"]) == len(ledger["edges"]), "residual source changed")
        require(all(0 <= odd <= edge[2] for odd, edge in zip(record["row"], ledger["edges"])),
                "nonphysical residual row")
        digest.update(canonical_bytes(record))
    require(digest.hexdigest() == payload["residual_stream_sha256"],
            "residual stream digest changed")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", type=int, default=min(16, os.cpu_count() or 1))
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    if args.verify is not None:
        payload, raw, stored = read_artifact(args.verify)
    else:
        require(args.jobs >= 1 and args.output.parent.is_dir(), "bad jobs or output parent")
        payload = regenerate(args.jobs, args.progress)
        verify(payload)
        raw = canonical_bytes(payload)
        stored = lzma.compress(raw, preset=6) if args.output.suffix == ".xz" else raw
        args.output.write_bytes(stored)
    verify(payload)
    print(f"kernels={payload['kernel_total']} physical={payload['physical_row_total']} "
          f"orbits={payload['parity_orbit_total']}")
    print(f"residuals={payload['coarse_residual_total']} "
          f"targets={payload['frontier_target_total']}")
    print(f"raw_sha256={hashlib.sha256(raw).hexdigest()} "
          f"artifact_sha256={hashlib.sha256(stored).hexdigest()}")
    print("full_theorem=false")


if __name__ == "__main__":
    main()
