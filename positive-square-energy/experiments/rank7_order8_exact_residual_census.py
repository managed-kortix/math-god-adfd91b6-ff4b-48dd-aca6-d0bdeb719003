#!/usr/bin/env python3
"""Exact, chunkable residual-orbit census for rank-seven order-eight kernels.

The coarse test is reduced exactly to a subset-minimum table.  For a coloring
let C be its crossing support.  A parity row r with support S is certified
precisely when some at-most-four-color cut C contains S and

    18 * sum(m_e for e in C) + 10 * |S| - 13 * sum(r) <= 180.

All minima over supersets are computed by a Boolean-lattice SOS pass.  Orbit
materialization uses mixed-radix integer rows and the full support
automorphism group.  A Burnside count independently checks every kernel's
materialized orbit count.  Chunks are self-contained and aggregation requires
an exact, gap-free partition of the 4,015 kernels.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import lzma
import math
import os
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE_ENGINE = HERE / "rank7_parity_coarse_digest_census.py"
DEFAULT_AGGREGATE = HERE / "rank7_order8_exact_residual_census_manifest.json"
ORDER = 8
RANK = 7
KERNEL_TOTAL = 4015
BUDGET_SCALED = 180
PATH_COUNT = ORDER + RANK - 1
FRONTIERS_PER_RESIDUAL = PATH_COUNT + 1
CHUNK_SCHEMA = "rank-seven-order-eight-exact-residual-census-chunk-v1"
AGGREGATE_SCHEMA = "rank-seven-order-eight-exact-residual-census-manifest-v1"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def load_engine():
    spec = importlib.util.spec_from_file_location("rank7_order8_source", SOURCE_ENGINE)
    require(spec is not None and spec.loader is not None, "cannot load source engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def restricted_colorings(n, limit=4):
    """Generate every set partition into at most limit unlabeled colors."""
    colors = [0] * n

    def visit(position, maximum):
        if position == n:
            yield tuple(colors)
            return
        for color in range(min(maximum + 1, limit - 1) + 1):
            colors[position] = color
            yield from visit(position + 1, max(maximum, color))

    yield from visit(1, 0)


def coarse_sieve(edges):
    """Return minimum multiplicity crossing cost for every required support."""
    support_count = len(edges)
    infinity = 10 ** 9
    minimum = [infinity] * (1 << support_count)
    for colors in restricted_colorings(ORDER):
        crossing = 0
        base = 0
        for index, (u, v, multiplicity) in enumerate(edges):
            if colors[u] != colors[v]:
                crossing |= 1 << index
                base += 18 * multiplicity
        if base < minimum[crossing]:
            minimum[crossing] = base
    # minimum[mask] becomes min{b(C): C contains mask}.
    for bit in range(support_count):
        flag = 1 << bit
        for mask in range(1 << support_count):
            if not mask & flag and minimum[mask | flag] < minimum[mask]:
                minimum[mask] = minimum[mask | flag]
    return tuple(minimum)


def mixed_radix(edges):
    radices = tuple(multiplicity + 1 for _, _, multiplicity in edges)
    strides = []
    product = 1
    for radix in radices:
        strides.append(product)
        product *= radix
    return radices, tuple(strides), product


def decode_row(code, radices):
    values = []
    odd_support = 0
    odd_sum = 0
    for index, radix in enumerate(radices):
        code, value = divmod(code, radix)
        values.append(value)
        if value:
            odd_support |= 1 << index
            odd_sum += value
    return tuple(values), odd_support, odd_sum


def transformed_code(row, action, strides):
    return sum(row[source] * strides[target] for target, source in enumerate(action))


def burnside_orbits(edges, actions):
    total = 0
    for action in actions:
        cycles = []
        unseen = set(range(len(action)))
        while unseen:
            start = min(unseen)
            cycle = []
            value = start
            while value in unseen:
                unseen.remove(value)
                cycle.append(value)
                value = action[value]
            cycles.append(cycle)
        fixed = 1
        for cycle in cycles:
            multiplicities = {edges[index][2] for index in cycle}
            require(len(multiplicities) == 1, "action changes an edge multiplicity")
            fixed *= multiplicities.pop() + 1
        total += fixed
    require(total % len(actions) == 0, "nonintegral Burnside orbit count")
    return total // len(actions)


def census_kernel(engine, item):
    global_index, local_index, order, edges = item
    require(order == ORDER, "wrong-order kernel")
    actions = engine.automorphism_actions(order, edges)
    radices, strides, physical_rows = mixed_radix(edges)
    expected_orbits = burnside_orbits(edges, actions)
    minimum = coarse_sieve(edges)
    seen = bytearray(physical_rows)
    residuals = []
    orbit_count = 0
    orbit_mass = 0
    for code in range(physical_rows):
        if seen[code]:
            continue
        row, odd_support, odd_sum = decode_row(code, radices)
        orbit = {transformed_code(row, action, strides) for action in actions}
        representative = min(orbit)
        require(representative == code, "mixed-radix orbit traversal lost canonical order")
        for image in orbit:
            seen[image] = 1
        orbit_count += 1
        orbit_mass += len(orbit)
        threshold = BUDGET_SCALED - 10 * odd_support.bit_count() + 13 * odd_sum
        if minimum[odd_support] > threshold:
            residuals.append([list(row), len(orbit)])
    require(orbit_mass == physical_rows, "orbit materialization is not a partition")
    require(orbit_count == expected_orbits, "Burnside/materialization disagreement")
    ledger = {
        "global_kernel": global_index,
        "order_kernel": local_index,
        "edges": [list(edge) for edge in edges],
        "automorphisms": len(actions),
        "physical_rows": physical_rows,
        "parity_orbits": orbit_count,
        "coarse_residuals": len(residuals),
    }
    return ledger, residuals


def order_items(engine):
    items = tuple(item for item in engine.source_kernels() if item[2] == ORDER)
    require(len(items) == KERNEL_TOTAL, "order-eight kernel count changed")
    return items


def generate_chunk(start, stop, progress=False):
    engine = load_engine()
    items = order_items(engine)
    require(0 <= start < stop <= len(items), "invalid half-open chunk range")
    kernels = []
    residuals = []
    digest = hashlib.sha256()
    for position, item in enumerate(items[start:stop], start):
        ledger, local = census_kernel(engine, item)
        kernels.append(ledger)
        for row, orbit_size in local:
            record = {
                "global_kernel": ledger["global_kernel"],
                "order_kernel": ledger["order_kernel"],
                "row": row,
                "orbit_size": orbit_size,
            }
            digest.update(canonical_bytes(record))
            residuals.append(record)
        if progress:
            print(f"[{position + 1}/{stop}] K{ledger['global_kernel']} "
                  f"orbits={ledger['parity_orbits']} residuals={len(local)}", flush=True)
    return {
        "schema": CHUNK_SCHEMA,
        "status": "complete-exact-residual-orbit-chunk",
        "full_theorem": False,
        "rank": RANK,
        "order": ORDER,
        "budget": [RANK - 1, 1],
        "path_count": PATH_COUNT,
        "frontiers_per_residual": FRONTIERS_PER_RESIDUAL,
        "kernel_range": [start, stop],
        "source_sha256": engine.SOURCE_SHA256,
        "kernel_total": len(kernels),
        "physical_row_total": sum(row["physical_rows"] for row in kernels),
        "parity_orbit_total": sum(row["parity_orbits"] for row in kernels),
        "coarse_certified_total": sum(row["parity_orbits"] - row["coarse_residuals"]
                                      for row in kernels),
        "coarse_residual_total": len(residuals),
        "frontier_target_total": FRONTIERS_PER_RESIDUAL * len(residuals),
        "residual_stream_sha256": digest.hexdigest(),
        "kernels": kernels,
        "residuals": residuals,
    }


def read_payload(path):
    stored = path.read_bytes()
    raw = lzma.decompress(stored) if path.suffix == ".xz" else stored
    payload = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(payload), f"{path} is not canonical JSON")
    return payload, raw, stored


def verify_chunk(payload):
    require(payload["schema"] == CHUNK_SCHEMA and payload["full_theorem"] is False,
            "wrong chunk schema")
    start, stop = payload["kernel_range"]
    require(0 <= start < stop <= KERNEL_TOTAL and payload["kernel_total"] == stop - start,
            "bad chunk range")
    require(len(payload["kernels"]) == stop - start, "incomplete kernel ledger")
    require(len(payload["residuals"]) == payload["coarse_residual_total"],
            "incomplete residual materialization")
    require(payload["coarse_certified_total"] + payload["coarse_residual_total"]
            == payload["parity_orbit_total"], "coarse partition mismatch")
    require(payload["frontier_target_total"] == FRONTIERS_PER_RESIDUAL
            * payload["coarse_residual_total"], "frontier total mismatch")
    digest = hashlib.sha256()
    ledgers = {row["order_kernel"]: row for row in payload["kernels"]}
    for record in payload["residuals"]:
        ledger = ledgers.get(record["order_kernel"])
        require(ledger is not None and record["global_kernel"] == ledger["global_kernel"],
                "residual references the wrong kernel")
        require(len(record["row"]) == len(ledger["edges"]), "residual row width changed")
        require(all(type(value) is int and 0 <= value <= edge[2]
                    for value, edge in zip(record["row"], ledger["edges"])),
                "nonphysical residual row")
        digest.update(canonical_bytes(record))
    require(digest.hexdigest() == payload["residual_stream_sha256"],
            "residual stream digest mismatch")


def aggregate(paths, output):
    chunks = []
    cursor = 0
    totals = {key: 0 for key in ("kernel_total", "physical_row_total", "parity_orbit_total",
                                 "coarse_certified_total", "coarse_residual_total",
                                 "frontier_target_total")}
    for path in sorted(paths, key=lambda value: read_payload(value)[0]["kernel_range"][0]):
        payload, raw, stored = read_payload(path)
        verify_chunk(payload)
        require(payload["kernel_range"][0] == cursor, "chunk gap or overlap")
        cursor = payload["kernel_range"][1]
        for key in totals:
            totals[key] += payload[key]
        chunks.append({
            "path": os.path.relpath(path, output.parent),
            "kernel_range": payload["kernel_range"],
            "raw_sha256": hashlib.sha256(raw).hexdigest(),
            "artifact_sha256": hashlib.sha256(stored).hexdigest(),
            "coarse_residual_total": payload["coarse_residual_total"],
        })
    require(cursor == KERNEL_TOTAL, "chunks do not cover all order-eight kernels")
    manifest = {
        "schema": AGGREGATE_SCHEMA,
        "status": "complete-exact-residual-orbit-decomposition",
        "full_theorem": False,
        "rank": RANK,
        "order": ORDER,
        "budget": [RANK - 1, 1],
        "path_count": PATH_COUNT,
        "frontiers_per_residual": FRONTIERS_PER_RESIDUAL,
        "source_sha256": load_engine().SOURCE_SHA256,
        **totals,
        "chunks": chunks,
    }
    output.write_bytes(canonical_bytes(manifest))
    return manifest


def verify_manifest(payload, manifest_path):
    require(payload["schema"] == AGGREGATE_SCHEMA and payload["full_theorem"] is False,
            "wrong aggregate schema")
    cursor = 0
    totals = {key: 0 for key in ("kernel_total", "physical_row_total", "parity_orbit_total",
                                 "coarse_certified_total", "coarse_residual_total",
                                 "frontier_target_total")}
    for record in payload["chunks"]:
        require(record["kernel_range"][0] == cursor, "manifest chunk gap or overlap")
        cursor = record["kernel_range"][1]
        path = manifest_path.parent / record["path"]
        chunk, raw, stored = read_payload(path)
        verify_chunk(chunk)
        require(chunk["kernel_range"] == record["kernel_range"] and
                chunk["coarse_residual_total"] == record["coarse_residual_total"],
                "manifest chunk metadata changed")
        require(hashlib.sha256(raw).hexdigest() == record["raw_sha256"] and
                hashlib.sha256(stored).hexdigest() == record["artifact_sha256"],
                "manifest chunk digest changed")
        for key in totals:
            totals[key] += chunk[key]
    require(cursor == KERNEL_TOTAL, "manifest does not cover all kernels")
    require(all(payload[key] == value for key, value in totals.items()),
            "manifest totals changed")


def self_test():
    engine = load_engine()
    sources = engine.source_kernels()
    selected = list(sources[:12])
    selected.extend(item for item in sources if item[2] == ORDER and len(selected) < 24)
    for item in selected:
        _, _, order, edges = item
        minimum = coarse_sieve(edges)
        radices, _, total = mixed_radix(edges)
        probes = range(total) if total <= 512 else range(0, total, max(1, total // 127))
        for code in probes:
            row, support, odd_sum = decode_row(code, radices)
            threshold = BUDGET_SCALED - 10 * support.bit_count() + 13 * odd_sum
            sieve = minimum[support] > threshold
            require(sieve == engine.is_coarse_residual(order, edges, row),
                    f"coarse sieve disagreement at K{item[0]} row {row}")
    require(len(selected) == 24 and sum(item[2] == ORDER for item in selected) == 12,
            "self-test scope changed")
    print(f"self_test_kernels={len(selected)} order8_kernels=12 status=passed")


def print_totals(payload, raw=None, stored=None):
    print(f"kernels={payload['kernel_total']} physical={payload['physical_row_total']} "
          f"orbits={payload['parity_orbit_total']}")
    print(f"residuals={payload['coarse_residual_total']} "
          f"targets={payload['frontier_target_total']}")
    if raw is not None:
        print(f"raw_sha256={hashlib.sha256(raw).hexdigest()} "
              f"artifact_sha256={hashlib.sha256(stored).hexdigest()}")
    print("full_theorem=false")


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    census = subparsers.add_parser("census")
    census.add_argument("--start", type=int, required=True)
    census.add_argument("--stop", type=int, required=True)
    census.add_argument("--output", type=Path, required=True)
    census.add_argument("--progress", action="store_true")
    verify = subparsers.add_parser("verify")
    verify.add_argument("artifact", type=Path)
    verify_manifest_parser = subparsers.add_parser("verify-manifest")
    verify_manifest_parser.add_argument("manifest", type=Path)
    combine = subparsers.add_parser("aggregate")
    combine.add_argument("chunks", nargs="+", type=Path)
    combine.add_argument("--output", type=Path, default=DEFAULT_AGGREGATE)
    subparsers.add_parser("self-test")
    args = parser.parse_args()

    if args.command == "self-test":
        self_test()
        return
    if args.command == "census":
        require(args.output.parent.is_dir(), "output parent does not exist")
        payload = generate_chunk(args.start, args.stop, args.progress)
        verify_chunk(payload)
        raw = canonical_bytes(payload)
        stored = lzma.compress(raw, preset=6) if args.output.suffix == ".xz" else raw
        args.output.write_bytes(stored)
        print_totals(payload, raw, stored)
        return
    if args.command == "verify":
        payload, raw, stored = read_payload(args.artifact)
        verify_chunk(payload)
        print_totals(payload, raw, stored)
        return
    if args.command == "verify-manifest":
        payload, raw, stored = read_payload(args.manifest)
        verify_manifest(payload, args.manifest)
        print_totals(payload, raw, stored)
        return
    require(args.output.parent.is_dir(), "output parent does not exist")
    payload = aggregate(args.chunks, args.output)
    print_totals(payload)


if __name__ == "__main__":
    main()
