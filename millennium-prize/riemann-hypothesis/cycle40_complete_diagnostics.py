#!/usr/bin/env python3
"""Certified finite diagnostics for local kappa and half-strength surplus.

Every reported numerical datum is an Arb enclosure. Plot coordinates use ball
midpoints only and are visual aids, not certificates.
"""

import argparse
import csv
import json
from pathlib import Path

from flint import arb, ctx

from certify_complete_gram import complete_energies, weighted_prefixes


def local_diagnostics(energies):
    rows = []
    for n in range(2, max(energies)):
        log_n = arb(n).log()
        log_next = arb(n + 1).log()
        weight = 1 - log_n / log_next
        decrement = energies[n] - energies[n + 1]
        half_surplus = decrement - weight * energies[n]
        kappa = decrement / (2 * weight * energies[n])
        rows.append({
            "n": n,
            "P_n": energies[n],
            "log_n_P_n": log_n * energies[n],
            "weight": weight,
            "decrement": decrement,
            "kappa_n": kappa,
            "kappa_minus_half": kappa - arb(1) / 2,
            "half_surplus": half_surplus,
        })
    return rows


def cumulative_diagnostics(energies):
    """Scan every start and every later endpoint for half-surplus excursions."""
    limit = max(energies)
    weighted = weighted_prefixes(energies)
    rows = []
    for a in range(2, limit):
        minimum = None
        minimum_stop = None
        first_recovery = None
        for b in range(a + 1, limit + 1):
            # weighted_prefixes stores twice the half-strength block cost.
            surplus = energies[a] - energies[b] - (
                weighted[b] - weighted[a]
            ) / 2
            if minimum is None or float(surplus.mid()) < float(minimum.mid()):
                minimum = surplus
                minimum_stop = b
            if first_recovery is None and surplus >= 0:
                first_recovery = b
        rows.append({
            "start": a,
            "worst_stop": minimum_stop,
            "worst_half_surplus": minimum,
            "first_recovery": first_recovery,
            "recovery_length": (
                None if first_recovery is None else first_recovery - a
            ),
        })
    return rows


def interval_text(value, digits=40):
    return value.str(digits)


def write_csv(path, rows, interval_fields):
    fieldnames = list(rows[0])
    with path.open("w", newline="", encoding="ascii") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({
                key: interval_text(value) if key in interval_fields else value
                for key, value in row.items()
            })


def enclosing_extreme(items, key, mode):
    if mode == "min":
        lower = min(item[key].lower() for item in items)
        upper = min(item[key].upper() for item in items)
    else:
        lower = max(item[key].lower() for item in items)
        upper = max(item[key].upper() for item in items)
    return arb((lower + upper) / 2, (upper - lower) / 2)


def certified_extreme_witness(items, key, mode):
    """Return a unique certified extremizer, or fail on overlapping balls."""
    order = sorted(
        items,
        key=lambda item: float(item[key].mid()),
        reverse=(mode == "max"),
    )
    candidate = order[0]
    if mode == "min":
        certified = all(candidate[key].upper() < item[key].lower()
                        for item in order[1:])
    else:
        certified = all(candidate[key].lower() > item[key].upper()
                        for item in order[1:])
    if not certified:
        raise RuntimeError(f"{key} has no unique certified {mode}imizer")
    return candidate


def consecutive_runs(indices):
    runs = []
    for value in indices:
        if not runs or value != runs[-1][-1] + 1:
            runs.append([value])
        else:
            runs[-1].append(value)
    return [[run[0], run[-1]] for run in runs]


def make_plots(path, local, cumulative):
    import matplotlib.pyplot as plt

    plt.rcParams.update({
        "font.family": "DejaVu Serif",
        "axes.facecolor": "#f7f1e5",
        "figure.facecolor": "#eee4d2",
        "axes.edgecolor": "#24352f",
        "axes.labelcolor": "#24352f",
        "xtick.color": "#24352f",
        "ytick.color": "#24352f",
    })
    fig, axes = plt.subplots(3, 1, figsize=(12, 11), constrained_layout=True)
    ns = [row["n"] for row in local]
    kappas = [float(row["kappa_n"].mid()) for row in local]
    colors = ["#a33b20" if value < 0.5 else "#276653" for value in kappas]
    axes[0].scatter(ns, kappas, c=colors, s=7, alpha=0.8, linewidths=0)
    axes[0].axhline(0.5, color="#172a3a", linewidth=1.2, linestyle="--")
    axes[0].set_ylabel(r"midpoint of $\kappa_n$")
    axes[0].set_title("Cycle 40 certified complete-P diagnostics (plot uses Arb midpoints)")

    surplus = [float(row["half_surplus"].mid()) for row in local]
    axes[1].plot(ns, surplus, color="#2f5d62", linewidth=0.75)
    axes[1].axhline(0, color="#172a3a", linewidth=1)
    axes[1].set_yscale("symlog", linthresh=1e-7)
    axes[1].set_ylabel("unit half surplus midpoint")

    starts = [row["start"] for row in cumulative]
    depths = [float(row["worst_half_surplus"].mid()) for row in cumulative]
    axes[2].plot(starts, depths, color="#a33b20", linewidth=0.8)
    axes[2].axhline(0, color="#172a3a", linewidth=1)
    axes[2].set_yscale("symlog", linthresh=1e-7)
    axes[2].set_xlabel("start a")
    axes[2].set_ylabel("minimum cumulative surplus midpoint")
    fig.savefig(path, dpi=180)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-N", type=int, default=2048)
    parser.add_argument("--bits", type=int, default=192)
    parser.add_argument("--output-dir", type=Path, default=Path("cycle40-data"))
    parser.add_argument("--no-plot", action="store_true")
    args = parser.parse_args()
    if args.max_N < 3:
        parser.error("--max-N must be at least 3")

    ctx.prec = args.bits
    args.output_dir.mkdir(parents=True, exist_ok=True)
    energies = complete_energies(args.max_N, args.bits)
    local = local_diagnostics(energies)
    cumulative = cumulative_diagnostics(energies)

    write_csv(
        args.output_dir / "local-unit-kappa.csv",
        local,
        set(local[0]) - {"n"},
    )
    write_csv(
        args.output_dir / "cumulative-half-surplus.csv",
        cumulative,
        {"worst_half_surplus"},
    )

    weakest_kappa = certified_extreme_witness(local, "kappa_n", "min")
    strongest_kappa = certified_extreme_witness(local, "kappa_n", "max")
    deepest = certified_extreme_witness(
        cumulative, "worst_half_surplus", "min"
    )
    longest = max(
        (row for row in cumulative if row["recovery_length"] is not None),
        key=lambda row: row["recovery_length"],
    )
    negative_units = [row for row in local if row["half_surplus"] < 0]
    unresolved_units = [
        row for row in local if not row["half_surplus"] < 0
        and not row["half_surplus"] >= 0
    ]
    negative_starts = [
        row for row in cumulative if row["worst_half_surplus"] < 0
    ]
    tail = [row for row in local if row["n"] >= 227]
    weakest_tail = certified_extreme_witness(tail, "kappa_n", "min")
    closest = min(local, key=lambda row: abs(float(row["kappa_minus_half"].mid())))
    summary = {
        "scope": "certified finite diagnostic only; no theorem or RH claim",
        "max_N": args.max_N,
        "arb_precision_bits": args.bits,
        "interval_format": "python-flint Arb balls",
        "unit_count": len(local),
        "certified_negative_unit_count": len(negative_units),
        "sign_unresolved_unit_count": len(unresolved_units),
        "weakest_local_kappa": {
            "n": weakest_kappa["n"],
            "interval": interval_text(enclosing_extreme(local, "kappa_n", "min")),
        },
        "strongest_local_kappa": {
            "n": strongest_kappa["n"],
            "interval": interval_text(enclosing_extreme(local, "kappa_n", "max")),
        },
        "closest_local_kappa_to_half": {
            "n": closest["n"],
            "interval": interval_text(closest["kappa_n"]),
        },
        "weakest_local_kappa_from_227": {
            "n": weakest_tail["n"],
            "interval": interval_text(
                enclosing_extreme(tail, "kappa_n", "min")
            ),
        },
        "deepest_cumulative_excursion": {
            "start": deepest["start"],
            "stop": deepest["worst_stop"],
            "interval": interval_text(enclosing_extreme(
                cumulative, "worst_half_surplus", "min"
            )),
        },
        "longest_first_recovery": {
            "start": longest["start"],
            "stop": longest["first_recovery"],
            "length": longest["recovery_length"],
        },
        "starts_without_recovery_by_boundary": [
            row["start"] for row in cumulative if row["first_recovery"] is None
        ],
        "certified_negative_unit_indices": [row["n"] for row in negative_units],
        "certified_negative_unit_runs": consecutive_runs(
            [row["n"] for row in negative_units]
        ),
        "starts_with_negative_cumulative_excursion": [
            row["start"] for row in negative_starts
        ],
        "negative_cumulative_start_runs": consecutive_runs(
            [row["start"] for row in negative_starts]
        ),
    }
    with (args.output_dir / "summary.json").open("w", encoding="ascii") as handle:
        json.dump(summary, handle, indent=2)
        handle.write("\n")
    if not args.no_plot:
        make_plots(args.output_dir / "diagnostics.png", local, cumulative)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
