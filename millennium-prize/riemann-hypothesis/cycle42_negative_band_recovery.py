#!/usr/bin/env python3
"""Certified Cycle 42 arithmetic for the observed finite H episodes."""

import argparse

from flint import arb, ctx

from cycle41_h_event_analysis import h_event_rows


OBSERVED_EPISODES = ((2, 3), (39, 41), (95, 101), (219, 227))


def beta(n):
    log_n = arb(n).log()
    log_next = arb(n + 1).log()
    return (log_next - log_n) / (log_n * log_next ** 2)


def maximal_signed_suffix_debt(values, p, q):
    """Return max(0, -sum_[a,q) beta_n H_n) and a maximizing start."""
    suffix = arb(0)
    debt = arb(0)
    witness = q
    for a in range(q - 1, p - 1, -1):
        suffix += beta(a) * values[a]
        candidate = -suffix
        if candidate > debt:
            debt = candidate
            witness = a
    return debt, witness


def first_payment(values, q, debt):
    """Find the first negative-free endpoint whose signed gain pays debt."""
    gain = arb(0)
    for n in range(q, max(values) + 1):
        if values[n] < 0:
            raise ValueError(f"payment window meets negative H at {n}")
        gain += beta(n) * values[n]
        if gain >= debt:
            return n + 1, gain
    return None, gain


def impulse_budget(values, rows, p, t):
    """Abelize H_q-H_(q-1) over [p,t) into initial, drift, and J terms."""
    by_q = {row["q"]: row for row in rows}
    tails = {}
    running = arb(0)
    for n in range(t - 1, p - 1, -1):
        running += beta(n)
        tails[n] = running
    initial = tails[p] * values[p]
    drift = arb(0)
    impulse = arb(0)
    for q in range(p + 1, t):
        row = by_q[q]
        drift += tails[q] * row["drift"]
        impulse += tails[q] * (row["linear"] + row["diagonal"])
    return initial, drift, impulse


def episode_records(values, rows, episodes=OBSERVED_EPISODES):
    records = []
    for p, q in episodes:
        debt, witness = maximal_signed_suffix_debt(values, p, q)
        t, gain = first_payment(values, q, debt)
        initial, drift, impulse = impulse_budget(values, rows, p, t)
        records.append({
            "p": p,
            "q": q,
            "t": t,
            "debt": debt,
            "debt_witness": witness,
            "gain": gain,
            "margin": gain - debt,
            "beta_ratio": beta(p) / beta(t - 1),
            "initial": initial,
            "drift": drift,
            "impulse": impulse,
            "residual": initial + drift + impulse,
        })
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=240)
    parser.add_argument("--bits", type=int, default=192)
    args = parser.parse_args()
    ctx.prec = args.bits
    values, rows = h_event_rows(args.max_n, args.bits)
    print("CERTIFIED FINITE DIAGNOSTIC ONLY; NOT AN ASYMPTOTIC THEOREM OR RH PROOF")
    print(" p   q   t witness debt gain margin beta[p]/beta[t-1]")
    for record in episode_records(values, rows):
        print(
            f'{record["p"]:3d} {record["q"]:3d} {record["t"]:3d} '
            f'{record["debt_witness"]:7d} {record["debt"].str(12):>18s} '
            f'{record["gain"].str(12):>18s} {record["margin"].str(12):>18s} '
            f'{record["beta_ratio"].str(12):>18s}'
        )
        print(
            "    recurrence: initial={} drift={} impulse={} residual={}".format(
                record["initial"].str(12), record["drift"].str(12),
                record["impulse"].str(12), record["residual"].str(12),
            )
        )


if __name__ == "__main__":
    main()
