#!/usr/bin/env python3
"""Memory-bounded order-ten aggregation and payload-free owner audit."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
CORE_PATH = HERE / "rank7_order11_structural_owner_manifest.py"
ORDER = 10
RANK = 7
PATH_COUNT = 16
TARGETS_PER_RESIDUAL = 17
KERNEL_TOTAL = 3396
SCHEMA = "rank-seven-order-ten-structural-owner-manifest-v1"


def load_core():
    spec = importlib.util.spec_from_file_location("rank7_order10_owner_manifest_core",
                                                  CORE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load structural owner manifest core")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.ORDER = ORDER
    module.RANK = RANK
    module.PATH_COUNT = PATH_COUNT
    module.TARGETS_PER_RESIDUAL = TARGETS_PER_RESIDUAL
    module.KERNEL_TOTAL = KERNEL_TOTAL
    module.SCHEMA = SCHEMA
    return module


def print_totals(payload, prefix):
    print(f"{prefix}: kernels={payload['kernel_total']} physical={payload['physical_row_total']} "
          f"orbits={payload['parity_orbit_total']}")
    print(f"residual_orbits={payload['coarse_residual_total']} "
          f"residual_physical={payload['coarse_residual_physical_total']} "
          f"targets={payload['frontier_target_total']}")
    print(f"payload_free_owned_orbits={payload['payload_free_owned_orbit_total']} "
          f"remainder_orbits={payload['remainder_orbit_total']} "
          f"remainder_physical={payload['remainder_physical_total']}")
    print("full_theorem=false")


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    build = subparsers.add_parser("build")
    build.add_argument("chunks", nargs="+", type=Path)
    build.add_argument("--output", required=True, type=Path)
    verify = subparsers.add_parser("verify")
    verify.add_argument("manifest", type=Path)
    args = parser.parse_args()
    core = load_core()

    if args.command == "build":
        core.require(args.output.parent.is_dir(), "output parent does not exist")
        payload = core.scan(core.ordered_paths(args.chunks), args.output)
        args.output.write_bytes(core.canonical_bytes(payload))
        print_totals(payload, "order-ten manifest built")
        return 0

    raw = args.manifest.read_bytes()
    expected = json.loads(raw.decode("ascii"))
    core.require(raw == core.canonical_bytes(expected),
                 "manifest is not canonical ASCII JSON")
    core.require(expected.get("schema") == SCHEMA and
                 expected.get("full_theorem") is False,
                 "wrong manifest schema or theorem boundary")
    paths = [args.manifest.parent / row["path"] for row in expected["chunks"]]
    actual = core.scan(paths, args.manifest)
    core.require(core.canonical_bytes(actual) == raw, "regenerated manifest differs")
    print_totals(actual, "order-ten manifest verified")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, OSError, RuntimeError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        sys.stderr.write(f"order-ten structural owner audit: FAIL CLOSED: {error}\n")
        raise SystemExit(1)
