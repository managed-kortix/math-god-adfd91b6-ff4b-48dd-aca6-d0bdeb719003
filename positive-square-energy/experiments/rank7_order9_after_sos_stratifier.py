#!/usr/bin/env python3
"""Authenticate and stratify the exact order-nine remainder after SOS lanes."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import lzma
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "rank7_order9_unowned_stratifier.py"
OWNER_REPORT_PATH = HERE / "rank7_order9_typed_sos_owner_manifest.json"
DEFAULT_OUTPUT = HERE / "rank7_order9_after_sos_stratification.json"
SCHEMA = "rank-seven-order-nine-after-sos-stratification-v1"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_base():
    spec = importlib.util.spec_from_file_location("rank7_order9_after_sos_base", BASE_PATH)
    require(spec is not None and spec.loader is not None, "cannot load stratification base")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def concentration(counts, total):
    ranked = sorted(counts.values(), reverse=True)
    result = {
        "class_total": len(ranked),
        "largest_class_orbit_total": ranked[0] if ranked else 0,
        "herfindahl_numerator": sum(value * value for value in ranked),
        "herfindahl_denominator": total * total if total else 1,
    }
    for width in (1, 10, 100, 1000):
        result[f"top_{width}_orbit_total"] = sum(ranked[:width])
    return result


def scan(report_path, top):
    base = load_base()
    report, report_sha256 = base.strict_canonical_json(report_path, "typed SOS owner report")
    stream_info = report["updated_remainder_stream"]
    stream_path = report_path.parent / stream_info["path"]
    require(base.file_sha256(stream_path) == stream_info["artifact_sha256"],
            "updated remainder artifact changed")
    kernels = base.kernel_dictionary(base.load_scan_engine())
    names = ("kernel", "support", "parity", "signed_degree", "graph",
             "dominant_family", "joint")
    counts = {name: Counter() for name in names}
    physical = {name: Counter() for name in names}
    descriptions = {name: {} for name in names}
    raw_digest = hashlib.sha256()
    orbit_total = physical_total = 0
    with lzma.open(stream_path, "rb") as rows:
        for raw in rows:
            try:
                record = json.loads(raw.decode("ascii"))
            except (UnicodeDecodeError, json.JSONDecodeError) as error:
                raise RuntimeError("cannot parse updated remainder row") from error
            require(raw == canonical_bytes(record) and len(record) == 5,
                    "noncanonical updated remainder row")
            _, global_kernel, order_kernel, raw_row, orbit_size = record
            expected_global, edges = kernels[order_kernel]
            require(global_kernel == expected_global, "updated remainder kernel changed")
            support, parity, graph = base.graph_data(edges, tuple(raw_row), 9)
            signed_degree = {
                "signed_imbalance_degree_partition":
                    parity["signed_imbalance_degree_partition"],
                "absolute_imbalance_degree_partition":
                    parity["absolute_imbalance_degree_partition"],
            }
            dominant = {
                "multiplicity_partition": support["multiplicity_partition"],
                "bundle_types": parity["bundle_types"],
                "cycle_rank": graph["cycle_rank"],
                "triangle_total": graph["triangle_total"],
            }
            payloads = {
                "kernel": {"global_kernel": global_kernel,
                           "edges": [list(edge) for edge in edges]},
                "support": support,
                "parity": parity,
                "signed_degree": signed_degree,
                "graph": graph,
                "dominant_family": dominant,
                "joint": {"support": support, "parity": parity,
                          "signed_degree": signed_degree, "graph": graph},
            }
            for name, payload in payloads.items():
                key = (f"k-{global_kernel:04d}" if name == "kernel" else
                       base.signature_id(name[0], payload))
                counts[name][key] += 1
                physical[name][key] += orbit_size
                descriptions[name].setdefault(key, payload)
            raw_digest.update(raw)
            orbit_total += 1
            physical_total += orbit_size
    require(orbit_total == stream_info["record_total"] == report["remaining_total"] and
            raw_digest.hexdigest() == stream_info["raw_sha256"],
            "updated remainder stream authentication failed")
    top_strata = {}
    for name in names:
        keys = sorted(counts[name], key=lambda key: (-counts[name][key],
                                                     -physical[name][key], key))
        top_strata[name] = [
            {"id": key, "orbit_total": counts[name][key],
             "physical_total": physical[name][key], "signature": descriptions[name][key]}
            for key in keys[:top]
        ]
    return {
        "schema": SCHEMA,
        "full_theorem": orbit_total == 0,
        "scope": "exact structural stratification of failures after scalar and typed-diagonal SOS ownership",
        "owner_report_sha256": report_sha256,
        "remainder_stream": {**stream_info},
        "unowned_orbit_total": orbit_total,
        "unowned_physical_total": physical_total,
        "unowned_target_total": orbit_total * 16,
        "concentration": {name: concentration(counts[name], orbit_total) for name in names},
        "top_strata": top_strata,
        "claim_boundary": "these are finite-grid failures, not mathematical nonexistence obstructions",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner-report", type=Path, default=OWNER_REPORT_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--top", type=int, default=50)
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    require(args.top > 0 and args.output.parent.is_dir(), "invalid output or top count")
    raw = canonical_bytes(scan(args.owner_report, args.top))
    if args.audit:
        require(args.output.read_bytes() == raw, "stratification does not reproduce byte-for-byte")
    else:
        args.output.write_bytes(raw)
    print(f"sha256={hashlib.sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()
