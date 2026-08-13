#!/usr/bin/env python3
"""Exact, chunkable rank-seven residual census for kernel orders 9--12.

This is the order-eight Boolean-lattice sieve with two vectorized changes:

* all set partitions into at most four cells are generated once per order;
* mixed-radix rows and automorphism images are processed as integer arrays.

The latter is especially effective at order twelve, where cubicity bounds the
support by eighteen and keeps both the 2^support SOS table and each kernel's
physical row space small.  Chunk files materialize residual orbits and carry a
complete per-kernel ledger, Burnside check, and residual-stream digest.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import lzma
import os
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
SOURCE_ENGINE = HERE / "rank7_parity_coarse_digest_census.py"
SOURCE_SHA256 = "a241139ab54ce4cce1ab3812887359edb241c0abfb1018e804b4a5f86762cfd5"
RANK = 7
BUDGET_SCALED = 180
ORDER_KERNEL_TOTALS = {9: 4495, 10: 3396, 11: 1391, 12: 365}
CHUNK_SCHEMA = "rank-seven-orders9-12-exact-residual-census-chunk-v1"
MANIFEST_SCHEMA = "rank-seven-orders9-12-exact-residual-census-manifest-v1"
COLOR_CACHE: dict[int, np.ndarray] = {}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def load_engine():
    spec = importlib.util.spec_from_file_location("rank7_orders9_12_source", SOURCE_ENGINE)
    require(spec is not None and spec.loader is not None, "cannot load source engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    require(module.SOURCE_SHA256 == SOURCE_SHA256, "rank-seven kernel source pin changed")
    return module


def restricted_colorings(order, limit=4):
    """Return restricted-growth strings for partitions into at most four cells."""
    cached = COLOR_CACHE.get(order)
    if cached is not None:
        return cached
    rows = []
    colors = [0] * order

    def visit(position, maximum):
        if position == order:
            rows.append(colors.copy())
            return
        for color in range(min(maximum + 1, limit - 1) + 1):
            colors[position] = color
            visit(position + 1, max(maximum, color))

    visit(1, 0)
    result = np.asarray(rows, dtype=np.uint8)
    COLOR_CACHE[order] = result
    return result


def coarse_sieve(order, edges):
    """Return min weighted crossing cost for every required support mask."""
    colors = restricted_colorings(order)
    count = len(colors)
    masks = np.zeros(count, dtype=np.uint32)
    costs = np.zeros(count, dtype=np.int16)
    for index, (u, v, multiplicity) in enumerate(edges):
        crossing = colors[:, u] != colors[:, v]
        masks[crossing] |= np.uint32(1 << index)
        costs[crossing] += np.int16(18 * multiplicity)
    infinity = np.int16(32767)
    minimum = np.full(1 << len(edges), infinity, dtype=np.int16)
    np.minimum.at(minimum, masks, costs)
    # Superset-minimum SOS transform, vectorized over contiguous bit blocks.
    for bit in range(len(edges)):
        block = 1 << bit
        view = minimum.reshape(-1, block << 1)
        np.minimum(view[:, :block], view[:, block:], out=view[:, :block])
    return minimum


def mixed_radix(edges):
    radices = np.asarray([multiplicity + 1 for _, _, multiplicity in edges],
                         dtype=np.uint32)
    strides = np.empty(len(radices), dtype=np.uint32)
    product = 1
    for index, radix in enumerate(radices):
        strides[index] = product
        product *= int(radix)
    return radices, strides, product


def action_cycles(action):
    unseen = set(range(len(action)))
    cycles = []
    while unseen:
        value = min(unseen)
        cycle = []
        while value in unseen:
            unseen.remove(value)
            cycle.append(value)
            value = action[value]
        cycles.append(cycle)
    return cycles


def burnside_orbits(edges, actions):
    total = 0
    for action in actions:
        fixed = 1
        for cycle in action_cycles(action):
            multiplicities = {edges[index][2] for index in cycle}
            require(len(multiplicities) == 1, "action changes edge multiplicity")
            fixed *= multiplicities.pop() + 1
        total += fixed
    require(total % len(actions) == 0, "nonintegral Burnside orbit count")
    return total // len(actions)


def decode_codes(codes, radices, strides):
    return ((codes[:, None] // strides[None, :]) % radices[None, :]).astype(np.uint8)


def residual_orbits(edges, actions, minimum, batch_size):
    radices, strides, physical_rows = mixed_radix(edges)
    support_bits = (np.uint32(1) << np.arange(len(edges), dtype=np.uint32))[None, :]
    action_arrays = [np.asarray(action, dtype=np.intp) for action in actions]
    residuals = []
    residual_physical = 0
    orbit_mass = 0
    orbit_count = 0
    for start in range(0, physical_rows, batch_size):
        stop = min(start + batch_size, physical_rows)
        codes = np.arange(start, stop, dtype=np.uint32)
        rows = decode_codes(codes, radices, strides)
        nonzero = rows != 0
        support = np.bitwise_or.reduce(np.where(nonzero, support_bits, 0), axis=1)
        odd_sum = rows.sum(axis=1, dtype=np.int16)
        threshold = BUDGET_SCALED - 10 * np.bitwise_count(support) + 13 * odd_sum
        selected = minimum[support] > threshold
        if not np.any(selected):
            continue
        selected_codes = codes[selected]
        selected_rows = rows[selected]
        residual_physical += len(selected_codes)
        canonical = selected_codes.copy()
        stabilizers = np.zeros(len(selected_codes), dtype=np.uint16)
        for action in action_arrays:
            images = (selected_rows[:, action].astype(np.uint32)
                      * strides[None, :]).sum(axis=1, dtype=np.uint32)
            np.minimum(canonical, images, out=canonical)
            stabilizers += images == selected_codes
        owners = canonical == selected_codes
        owner_rows = selected_rows[owners]
        owner_stabilizers = stabilizers[owners]
        sizes = len(actions) // owner_stabilizers
        require(np.all(sizes * owner_stabilizers == len(actions)),
                "nonintegral orbit-stabilizer result")
        orbit_count += len(owner_rows)
        orbit_mass += int(sizes.sum(dtype=np.uint64))
        residuals.extend((row.tolist(), int(size))
                         for row, size in zip(owner_rows, sizes, strict=True))
    require(orbit_mass == residual_physical, "residual orbits do not partition residual rows")
    return physical_rows, orbit_count, residual_physical, residuals


def order_items(engine, order):
    items = tuple(item for item in engine.source_kernels() if item[2] == order)
    require(len(items) == ORDER_KERNEL_TOTALS[order], f"order-{order} kernel count changed")
    return items


def census_kernel(engine, item, batch_size):
    global_index, local_index, order, edges = item
    actions = engine.automorphism_actions(order, edges)
    minimum = coarse_sieve(order, edges)
    physical, residual_orbit_count, residual_physical, residuals = residual_orbits(
        edges, actions, minimum, batch_size)
    expected_orbits = burnside_orbits(edges, actions)
    ledger = {
        "global_kernel": global_index,
        "order_kernel": local_index,
        "edges": [list(edge) for edge in edges],
        "support_edges": len(edges),
        "automorphisms": len(actions),
        "physical_rows": physical,
        "parity_orbits": expected_orbits,
        "coarse_certified_orbits": expected_orbits - residual_orbit_count,
        "coarse_residual_orbits": residual_orbit_count,
        "coarse_residual_physical_rows": residual_physical,
    }
    return ledger, residuals


def generate_chunk(order, start, stop, batch_size, progress=False):
    engine = load_engine()
    items = order_items(engine, order)
    require(0 <= start < stop <= len(items), "invalid half-open chunk range")
    kernels = []
    residuals = []
    digest = hashlib.sha256()
    for position, item in enumerate(items[start:stop], start):
        ledger, local = census_kernel(engine, item, batch_size)
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
                  f"support={ledger['support_edges']} orbits={ledger['parity_orbits']} "
                  f"residuals={len(local)}", flush=True)
    path_count = order + RANK - 1
    return {
        "schema": CHUNK_SCHEMA,
        "status": "complete-exact-residual-orbit-chunk",
        "full_theorem": False,
        "rank": RANK,
        "order": order,
        "budget": [RANK - 1, 1],
        "path_count": path_count,
        "frontiers_per_residual": path_count + 1,
        "kernel_range": [start, stop],
        "source_sha256": SOURCE_SHA256,
        "kernel_total": len(kernels),
        "physical_row_total": sum(row["physical_rows"] for row in kernels),
        "parity_orbit_total": sum(row["parity_orbits"] for row in kernels),
        "coarse_certified_total": sum(row["coarse_certified_orbits"] for row in kernels),
        "coarse_residual_total": len(residuals),
        "coarse_residual_physical_total": sum(
            row["coarse_residual_physical_rows"] for row in kernels),
        "frontier_target_total": (path_count + 1) * len(residuals),
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
    order = payload["order"]
    require(order in ORDER_KERNEL_TOTALS, "order outside 9--12")
    start, stop = payload["kernel_range"]
    require(0 <= start < stop <= ORDER_KERNEL_TOTALS[order], "bad chunk range")
    require(payload["kernel_total"] == stop - start == len(payload["kernels"]),
            "incomplete kernel ledger")
    require(payload["coarse_residual_total"] == len(payload["residuals"]),
            "incomplete residual materialization")
    require(payload["coarse_certified_total"] + payload["coarse_residual_total"]
            == payload["parity_orbit_total"], "coarse partition mismatch")
    require(payload["frontier_target_total"] == (order + RANK)
            * payload["coarse_residual_total"], "frontier total mismatch")
    ledgers = {row["order_kernel"]: row for row in payload["kernels"]}
    digest = hashlib.sha256()
    previous = None
    for record in payload["residuals"]:
        ledger = ledgers.get(record["order_kernel"])
        require(ledger is not None and record["global_kernel"] == ledger["global_kernel"],
                "residual references wrong kernel")
        require(len(record["row"]) == len(ledger["edges"]), "residual width changed")
        require(all(type(value) is int and 0 <= value <= edge[2]
                    for value, edge in zip(record["row"], ledger["edges"], strict=True)),
                "nonphysical residual row")
        code = 0
        stride = 1
        for value, edge in zip(record["row"], ledger["edges"], strict=True):
            code += value * stride
            stride *= edge[2] + 1
        key = (record["order_kernel"], code)
        require(previous is None or previous < key, "residual stream is not strictly ordered")
        previous = key
        digest.update(canonical_bytes(record))
    require(digest.hexdigest() == payload["residual_stream_sha256"],
            "residual stream digest mismatch")


def aggregate(paths, output):
    payloads = []
    for path in paths:
        payload, raw, stored = read_payload(path)
        verify_chunk(payload)
        payloads.append((payload, path, raw, stored))
    require(payloads, "no chunks supplied")
    order = payloads[0][0]["order"]
    require(all(row[0]["order"] == order for row in payloads), "mixed-order manifest")
    payloads.sort(key=lambda row: row[0]["kernel_range"][0])
    cursor = 0
    chunks = []
    total_keys = ("kernel_total", "physical_row_total", "parity_orbit_total",
                  "coarse_certified_total", "coarse_residual_total",
                  "coarse_residual_physical_total", "frontier_target_total")
    totals = {key: 0 for key in total_keys}
    for payload, path, raw, stored in payloads:
        require(payload["kernel_range"][0] == cursor, "chunk gap or overlap")
        cursor = payload["kernel_range"][1]
        for key in total_keys:
            totals[key] += payload[key]
        chunks.append({
            "path": os.path.relpath(path, output.parent),
            "kernel_range": payload["kernel_range"],
            "coarse_residual_total": payload["coarse_residual_total"],
            "raw_sha256": hashlib.sha256(raw).hexdigest(),
            "artifact_sha256": hashlib.sha256(stored).hexdigest(),
        })
    require(cursor == ORDER_KERNEL_TOTALS[order], "chunks do not cover the order")
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "status": "complete-exact-residual-orbit-decomposition",
        "full_theorem": False,
        "rank": RANK,
        "order": order,
        "budget": [RANK - 1, 1],
        "path_count": order + RANK - 1,
        "frontiers_per_residual": order + RANK,
        "source_sha256": SOURCE_SHA256,
        **totals,
        "chunks": chunks,
    }
    output.write_bytes(canonical_bytes(manifest))
    return manifest


def self_test():
    old_path = HERE / "rank7_order8_exact_residual_census.py"
    spec = importlib.util.spec_from_file_location("rank7_order8_reference", old_path)
    require(spec is not None and spec.loader is not None, "cannot load order-eight reference")
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    engine = load_engine()
    probes = [item for item in engine.source_kernels() if item[2] == 8][:4]
    for item in probes:
        _, _, order, edges = item
        reference = np.asarray(old.coarse_sieve(edges), dtype=np.int16)
        require(np.array_equal(coarse_sieve(order, edges), reference),
                f"vectorized sieve disagrees at K{item[0]}")
    item = next(item for item in engine.source_kernels() if item[2] == 12)
    ledger, residuals = census_kernel(engine, item, 65536)
    require(ledger["coarse_residual_orbits"] == len(residuals),
            "order-twelve residual count mismatch")
    print(f"order8_reference_kernels={len(probes)} order12_kernel=K{item[0]} "
          f"orbits={ledger['parity_orbits']} residuals={len(residuals)} status=passed")


def print_totals(payload, raw=None, stored=None):
    print(f"order={payload['order']} kernels={payload['kernel_total']} "
          f"physical={payload['physical_row_total']} orbits={payload['parity_orbit_total']}")
    print(f"residuals={payload['coarse_residual_total']} "
          f"targets={payload['frontier_target_total']}")
    if raw is not None:
        print(f"raw_bytes={len(raw)} compressed_bytes={len(stored)} "
              f"raw_sha256={hashlib.sha256(raw).hexdigest()} "
              f"artifact_sha256={hashlib.sha256(stored).hexdigest()}")
    print("full_theorem=false")


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    census = subparsers.add_parser("census")
    census.add_argument("--order", type=int, choices=ORDER_KERNEL_TOTALS, required=True)
    census.add_argument("--start", type=int, required=True)
    census.add_argument("--stop", type=int, required=True)
    census.add_argument("--batch-size", type=int, default=262144)
    census.add_argument("--output", type=Path, required=True)
    census.add_argument("--progress", action="store_true")
    verify = subparsers.add_parser("verify")
    verify.add_argument("artifact", type=Path)
    combine = subparsers.add_parser("aggregate")
    combine.add_argument("chunks", nargs="+", type=Path)
    combine.add_argument("--output", type=Path, required=True)
    subparsers.add_parser("self-test")
    args = parser.parse_args()
    if args.command == "self-test":
        self_test()
        return
    if args.command == "verify":
        payload, raw, stored = read_payload(args.artifact)
        verify_chunk(payload)
        print_totals(payload, raw, stored)
        return
    if args.command == "aggregate":
        require(args.output.parent.is_dir(), "output parent does not exist")
        print_totals(aggregate(args.chunks, args.output))
        return
    require(args.batch_size >= 1, "batch size must be positive")
    require(args.output.parent.is_dir(), "output parent does not exist")
    payload = generate_chunk(args.order, args.start, args.stop, args.batch_size, args.progress)
    verify_chunk(payload)
    raw = canonical_bytes(payload)
    stored = lzma.compress(raw, preset=6) if args.output.suffix == ".xz" else raw
    args.output.write_bytes(stored)
    print_totals(payload, raw, stored)


if __name__ == "__main__":
    main()
