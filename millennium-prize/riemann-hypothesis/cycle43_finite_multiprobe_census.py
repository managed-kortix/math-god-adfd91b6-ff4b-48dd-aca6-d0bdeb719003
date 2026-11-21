#!/usr/bin/env python3
"""Bounded 192-bit Arb census for the Cycle 43 multiprobe diagnostic.

The default census is the consecutive first-recovery chain whose starts are
2,...,255 and whose endpoints are all at most 256.  The cap is explicit and
small enough for reproducible exact-ball computation.  Families are fixed
before verdicts are inspected: affine {0}, fixed divisors {1} and {3}, the
small fixed families {0,1}, {0,3}, {1,3}, {0,1,3}, all squarefree admissions
inside the current block, and a midpoint-greedy family.  Every pass/fail
verdict and every reported margin is evaluated with Arb balls.  Midpoints are
used only to order greedy choices and to choose descriptive extrema after all
signs have been certified.

This is a finite census, not an asymptotic theorem and not an RH result.
"""

import argparse
import json
from pathlib import Path

from flint import arb, ctx

from certify_complete_gram import complete_energies
from cycle40_complete_diagnostics import cumulative_diagnostics
from cycle43_divisor_admission_multiprobe import (
    AFFINE,
    CompensatedBlock,
    certified_sign,
    interval_text,
    jsonable,
)

DEFAULT_CAP = 256
FAMILY_ORDER = (
    "affine_only",
    "divisor_1_only",
    "divisor_3_only",
    "affine_plus_1",
    "affine_plus_3",
    "divisors_1_3",
    "affine_plus_1_3",
    "current_admissions",
    "greedy",
)


def classify_margin(margin):
    sign = certified_sign(margin)
    if sign > 0:
        return "PASS"
    if sign < 0:
        return "FAIL"
    return "PASS_EQ"


def safe_certificate(block, family):
    """Return an Arb certificate; rank zero is handled without matrix solve."""
    family = tuple(family)
    if family:
        result = block.certificate(family)
    else:
        margin = -block.negative_budget
        result = {
            "family": family,
            "rank": 0,
            "projection": arb(0),
            "determinant": arb(1),
            "margin": margin,
            "verdict": classify_margin(margin),
        }
    result = dict(result)
    result["projection_fraction_of_budget"] = (
        result["projection"] / block.negative_budget
    )
    result["margin_fraction_of_budget"] = result["margin"] / block.negative_budget
    result["margin_fraction_of_positive"] = (
        result["margin"] / block.positive_energy
    )
    return result


def fixed_families(block):
    labels = set(block.labels)

    def present(*labels_):
        return tuple(label for label in labels_ if label in labels)

    return {
        "affine_only": present(AFFINE),
        "divisor_1_only": present(1),
        "divisor_3_only": present(3),
        "affine_plus_1": present(AFFINE, 1),
        "affine_plus_3": present(AFFINE, 3),
        "divisors_1_3": present(1, 3),
        "affine_plus_1_3": present(AFFINE, 1, 3),
        "current_admissions": tuple(
            label for label in block.labels
            if block.start <= label < block.stop
        ),
    }


def recovery_blocks(energies, cap):
    rows = cumulative_diagnostics(energies)
    blocks = []
    for row in rows:
        endpoint = row["first_recovery"]
        if endpoint is None:
            raise RuntimeError(
                f"start {row['start']} has no first recovery by cap {cap}"
            )
        blocks.append((row["start"], endpoint))
    expected = list(range(2, cap))
    if [start for start, _ in blocks] != expected:
        raise RuntimeError("first-recovery starts are not the complete range")
    return blocks, rows


def block_record(start, stop, bits):
    block = CompensatedBlock(start, stop, bits)
    certificates = {
        name: safe_certificate(block, family)
        for name, family in fixed_families(block).items()
    }
    greedy_family, greedy_trace = block.greedy_family()
    certificates["greedy"] = safe_certificate(block, greedy_family)
    if certificates["greedy"]["verdict"] not in ("PASS", "PASS_EQ"):
        raise RuntimeError(f"greedy pool did not certify [{start},{stop})")
    return {
        "start": start,
        "stop": stop,
        "length": stop - start,
        "theta": block.theta,
        "candidate_probe_count": len(block.labels),
        "positive_energy": block.positive_energy,
        "negative_budget": block.negative_budget,
        "residual": block.residual,
        "residual_fraction_of_budget": block.residual / block.negative_budget,
        "residual_fraction_of_positive": block.residual / block.positive_energy,
        "families": certificates,
        "greedy_ordering": "Arb midpoint gains; verdicts use Arb balls",
        "greedy_trace": greedy_trace,
    }


def midpoint_key(value):
    return float(value.mid())


def extrema(rows, accessor):
    smallest = min(rows, key=lambda row: midpoint_key(accessor(row)))
    largest = max(rows, key=lambda row: midpoint_key(accessor(row)))
    return smallest, largest


def family_summary(rows, name):
    verdicts = [row["families"][name]["verdict"] for row in rows]
    failures = [
        row for row, verdict in zip(rows, verdicts)
        if verdict == "FAIL"
    ]
    equalities = [
        row for row, verdict in zip(rows, verdicts)
        if verdict == "PASS_EQ"
    ]
    smallest, largest = extrema(
        rows, lambda row: row["families"][name]["margin_fraction_of_budget"]
    )
    first = failures[0] if failures else None
    return {
        "pass_count": verdicts.count("PASS"),
        "pass_equality_count": len(equalities),
        "fail_count": len(failures),
        "first_certified_failure": (
            None if first is None else {
                "start": first["start"],
                "stop": first["stop"],
                "length": first["length"],
                "family": first["families"][name]["family"],
                "projection": first["families"][name]["projection"],
                "budget": first["negative_budget"],
                "margin": first["families"][name]["margin"],
                "margin_fraction_of_budget": (
                    first["families"][name]["margin_fraction_of_budget"]
                ),
            }
        ),
        "smallest_margin_fraction_of_budget": {
            "start": smallest["start"],
            "stop": smallest["stop"],
            "interval": smallest["families"][name][
                "margin_fraction_of_budget"
            ],
        },
        "largest_margin_fraction_of_budget": {
            "start": largest["start"],
            "stop": largest["stop"],
            "interval": largest["families"][name][
                "margin_fraction_of_budget"
            ],
        },
    }


def run_census(cap=DEFAULT_CAP, bits=192):
    if cap < 4:
        raise ValueError("cap must be at least 4")
    if bits < 128:
        raise ValueError("bits must be at least 128")
    ctx.prec = bits
    energies = complete_energies(cap, bits)
    blocks, recovery_rows = recovery_blocks(energies, cap)
    rows = [block_record(start, stop, bits) for start, stop in blocks]

    positive = [row for row in rows if certified_sign(row["residual"]) >= 0]
    if len(positive) != len(rows):
        raise RuntimeError("a first-recovery block has negative compensated residual")

    residual_min, residual_max = extrema(
        rows, lambda row: row["residual_fraction_of_budget"]
    )
    rank_counts = {}
    for row in rows:
        rank = str(row["families"]["greedy"]["rank"])
        rank_counts[rank] = rank_counts.get(rank, 0) + 1
    max_rank = max(row["families"]["greedy"]["rank"] for row in rows)
    first_by_rank = {}
    for rank in range(max_rank + 1):
        match = next(
            (row for row in rows if row["families"]["greedy"]["rank"] == rank),
            None,
        )
        if match is not None:
            first_by_rank[str(rank)] = {
                "start": match["start"],
                "stop": match["stop"],
                "family": match["families"]["greedy"]["family"],
            }

    longest = max(recovery_rows, key=lambda row: row["recovery_length"])
    payload = {
        "scope": "certified finite census only; no asymptotic theorem or RH claim",
        "arb_precision_bits": bits,
        "cap": cap,
        "energy_range": [2, cap],
        "census_start_range": [2, cap - 1],
        "block_rule": (
            "for every start a, first b>a with Arb-certified nonnegative "
            "half-strength surplus, searched only through cap"
        ),
        "block_count": len(rows),
        "all_starts_recovered_by_cap": True,
        "longest_first_recovery": {
            "start": longest["start"],
            "stop": longest["first_recovery"],
            "length": longest["recovery_length"],
        },
        "theta_rule": "theta=1/(4 log(start)) independently on each block",
        "complete_gram": "restricted Vasyunin formula; no unit-cell cutoff",
        "fixed_families": {
            "affine_only": [0],
            "divisor_1_only": [1],
            "divisor_3_only": [3],
            "affine_plus_1": [0, 1],
            "affine_plus_3": [0, 3],
            "divisors_1_3": [1, 3],
            "affine_plus_1_3": [0, 1, 3],
            "current_admissions": "all squarefree d in [start,stop)",
            "greedy": "midpoint-greedy over affine plus every squarefree d<stop",
        },
        "verdict_policy": (
            "Arb sign only; unresolved signs and uncertified Gram determinants "
            "raise RuntimeError"
        ),
        "ordering_policy": (
            "floating conversion occurs only for deterministic greedy/extremum "
            "ordering; never for a pass/fail verdict"
        ),
        "family_summary": {
            name: family_summary(rows, name) for name in FAMILY_ORDER
        },
        "greedy_rank_counts": rank_counts,
        "first_greedy_block_by_rank": first_by_rank,
        "residual_scaling": {
            "smallest_residual_fraction_of_budget": {
                "start": residual_min["start"],
                "stop": residual_min["stop"],
                "interval": residual_min["residual_fraction_of_budget"],
            },
            "largest_residual_fraction_of_budget": {
                "start": residual_max["start"],
                "stop": residual_max["stop"],
                "interval": residual_max["residual_fraction_of_budget"],
            },
        },
        "blocks": rows,
    }
    return payload


def print_summary(payload):
    print("CERTIFIED FINITE CENSUS ONLY; NOT AN ASYMPTOTIC THEOREM OR RH PROOF")
    print(
        f"Arb precision={payload['arb_precision_bits']} bits; "
        f"complete energies=2..{payload['cap']}; "
        f"first-recovery starts=2..{payload['cap'] - 1}; "
        f"blocks={payload['block_count']}"
    )
    longest = payload["longest_first_recovery"]
    print(
        "longest first recovery: "
        f"[{longest['start']},{longest['stop']}) length={longest['length']}"
    )
    print("family: pass/fail; first failure; min/max normalized margin")
    for name in FAMILY_ORDER:
        item = payload["family_summary"][name]
        first = item["first_certified_failure"]
        first_text = "none" if first is None else (
            f"[{first['start']},{first['stop']})"
        )
        low = item["smallest_margin_fraction_of_budget"]
        high = item["largest_margin_fraction_of_budget"]
        print(
            f"  {name}: {item['pass_count']} pass, {item['fail_count']} fail; "
            f"first fail={first_text}; "
            f"min={interval_text(low['interval'], 14)} at "
            f"[{low['start']},{low['stop']}); "
            f"max={interval_text(high['interval'], 14)} at "
            f"[{high['start']},{high['stop']})"
        )
    print(f"greedy rank counts: {payload['greedy_rank_counts']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cap", type=int, default=DEFAULT_CAP)
    parser.add_argument("--bits", type=int, default=192)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    payload = run_census(args.cap, args.bits)
    print_summary(payload)
    if args.json:
        args.json.write_text(
            json.dumps(jsonable(payload), indent=2) + "\n", encoding="ascii"
        )


if __name__ == "__main__":
    main()
