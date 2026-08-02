#!/usr/bin/env python3
"""Evaluate the frozen C258-V1 gates from completed matrix entries."""

import argparse
import json
import os
from pathlib import Path


INDICES = (30, 36, 43, 44)


def load_entries(directory):
    entries = {}
    for index in INDICES:
        for n in (128, 256):
            for factor in (2, 4):
                path = directory / f"cycle258-v1-i{index}-N{n}-dt{factor}.json"
                row = json.loads(path.read_text(encoding="ascii"))
                entries[(index, n, factor)] = row
    return entries


def evaluate(entries):
    members = []
    for index in INDICES:
        get = lambda n, factor: entries[(index, n, factor)]
        fine_128 = get(128, 4)["cubature_4n"]
        fine_256 = get(256, 4)["cubature_4n"]
        checks = {
            "n256_step_halving": abs(get(256, 4)["cubature_4n"]["variation_ratio"] - get(256, 2)["cubature_4n"]["variation_ratio"]) <= 0.002,
            "fine_resolution": abs(fine_256["variation_ratio"] - fine_128["variation_ratio"]) <= 0.005,
            "cubature": max(get(n, factor)["cubature_variation_ratio_difference"] for n in (128, 256) for factor in (2, 4)) <= 0.001,
            "alias_replay": max(get(n, factor)["max_alias_replay_relative_rhs_discrepancy"] for n in (128, 256) for factor in (2, 4)) <= 1e-11,
            "conservation": max(d["relative_energy_drift"] for n in (128, 256) for factor in (2, 4) for d in get(n, factor)["endpoint_drifts"]) <= 1e-6 and max(d["relative_enstrophy_drift"] for n in (128, 256) for factor in (2, 4) for d in get(n, factor)["endpoint_drifts"]) <= 2e-5,
        }
        extrema_time_agreement = abs(fine_256["minimum"]["time"] - fine_128["minimum"]["time"]) <= 1.0 / 64.0 and abs(fine_256["maximum"]["time"] - fine_128["maximum"]["time"]) <= 1.0 / 64.0
        samples_128 = {row["time"]: row["l3_grid_4n"] for row in get(128, 4)["checkpoint_diagnostics"]}
        samples_256 = {row["time"]: row["l3_grid_4n"] for row in get(256, 4)["checkpoint_diagnostics"]}
        extrema_plateau = all(
            abs(samples[extrema_128[kind]["time"]] - samples[extrema_256[kind]["time"]]) <= 0.001
            for samples, extrema_128, extrema_256 in (
                (samples_128, fine_128, fine_256),
                (samples_256, fine_128, fine_256),
            )
            for kind in ("minimum", "maximum")
        )
        checks["extrema"] = extrema_time_agreement or extrema_plateau
        members.append({
            "family_index": index,
            "checks": checks,
            "passes_all_gates": all(checks.values()),
            "n256_step_halving_ratio_change": abs(get(256, 4)["cubature_4n"]["variation_ratio"] - get(256, 2)["cubature_4n"]["variation_ratio"]),
            "fine_n128_n256_ratio_change": abs(fine_256["variation_ratio"] - fine_128["variation_ratio"]),
            "max_cubature_ratio_change": max(get(n, factor)["cubature_variation_ratio_difference"] for n in (128, 256) for factor in (2, 4)),
            "max_alias_replay_relative_rhs_discrepancy": max(get(n, factor)["max_alias_replay_relative_rhs_discrepancy"] for n in (128, 256) for factor in (2, 4)),
            "max_relative_energy_drift": max(d["relative_energy_drift"] for n in (128, 256) for factor in (2, 4) for d in get(n, factor)["endpoint_drifts"]),
            "max_relative_enstrophy_drift": max(d["relative_enstrophy_drift"] for n in (128, 256) for factor in (2, 4) for d in get(n, factor)["endpoint_drifts"]),
            "fine_extrema": {"n128": {"minimum": fine_128["minimum"], "maximum": fine_128["maximum"]}, "n256": {"minimum": fine_256["minimum"], "maximum": fine_256["maximum"]}},
        })
    promoted = [row["family_index"] for row in members if row["passes_all_gates"]]
    return {"format": "C258-V1-decision", "numerical_only": True, "promotion": bool(promoted), "promoted_family_indices": promoted, "members": members}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = evaluate(load_entries(args.directory))
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="ascii")
    os.replace(temporary, args.output)


if __name__ == "__main__":
    main()
