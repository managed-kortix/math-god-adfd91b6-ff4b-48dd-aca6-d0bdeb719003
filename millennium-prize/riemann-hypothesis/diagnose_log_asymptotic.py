#!/usr/bin/env python3
"""Finite interval-aware fits of P_N = C/log(N) + D/log(N)^2.

This is a numerical diagnostic only. Finite regressions do not establish an
asymptotic expansion, an error term, or any implication for RH.
"""

import argparse
import math

from flint import arb, ctx

from certify_complete_gram import complete_energies, mobius_sieve


def tapered_mean(limit):
    mu = mobius_sieve(limit)
    logs = [arb(0)] + [arb(n).log() for n in range(1, limit + 1)]
    prefix_mu_over_n = arb(0)
    prefix_mu_log_over_n = arb(0)
    result = {}
    for n in range(1, limit + 1):
        if mu[n]:
            prefix_mu_over_n += arb(mu[n]) / n
            prefix_mu_log_over_n += arb(mu[n]) * logs[n] / n
        if n >= 2:
            result[n] = prefix_mu_over_n - prefix_mu_log_over_n / logs[n]
    return result


def midpoint(value):
    return float(value.mid())


def radius(value):
    return float(value.rad())


def fit_window(values, start, stop, scaled=False):
    rows = []
    s11 = arb(0)
    s12 = arb(0)
    s22 = arb(0)
    t1 = arb(0)
    t2 = arb(0)
    for n in range(start, stop + 1):
        log_n = arb(n).log()
        if scaled:
            x1 = arb(1)
            x2 = 1 / log_n
            y = log_n * values[n]
        else:
            x1 = 1 / log_n
            x2 = x1 * x1
            y = values[n]
        rows.append((x1, x2, y))
        s11 += x1 * x1
        s12 += x1 * x2
        s22 += x2 * x2
        t1 += x1 * y
        t2 += x2 * y

    determinant = s11 * s22 - s12 * s12
    c = (t1 * s22 - t2 * s12) / determinant
    d = (s11 * t2 - s12 * t1) / determinant
    residual_square_sum = arb(0)
    max_abs_residual = arb(0)
    ys = []
    for x1, x2, y in rows:
        residual = y - c * x1 - d * x2
        residual_square_sum += residual * residual
        absolute_residual = abs(residual)
        if absolute_residual.upper() > max_abs_residual.upper():
            max_abs_residual = absolute_residual
        ys.append(midpoint(y))

    a = midpoint(s11)
    b = midpoint(s12)
    dmat = midpoint(s22)
    trace = a + dmat
    gap = math.hypot(a - dmat, 2 * b)
    eigen_max = (trace + gap) / 2
    eigen_min = (trace - gap) / 2
    condition = eigen_max / eigen_min
    rss_mid = midpoint(residual_square_sum)
    mean_y = sum(ys) / len(ys)
    tss = sum((y - mean_y) ** 2 for y in ys)
    return {
        "count": len(rows),
        "c": c,
        "d": d,
        "rms": (residual_square_sum / len(rows)).sqrt(),
        "max_residual": max_abs_residual,
        "r2": 1 - rss_mid / tss,
        "condition": condition,
    }


def compact(value, digits=14):
    return value.str(digits, radius=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-N", type=int, default=2048)
    parser.add_argument("--bits", type=int, default=192)
    parser.add_argument(
        "--starts", default="32,64,128,256,512,1024",
        help="comma-separated lower endpoints; every fit ends at max-N",
    )
    args = parser.parse_args()
    starts = [int(item) for item in args.starts.split(",")]
    if min(starts) < 2 or max(starts) >= args.max_N:
        parser.error("fit starts must lie in [2, max-N)")

    ctx.prec = args.bits
    restricted = complete_energies(args.max_N, args.bits)
    means = tapered_mean(args.max_N)
    full = {n: restricted[n] + means[n] ** 2 for n in restricted}

    print("NONRIGOROUS ASYMPTOTIC DIAGNOSTIC; FINITE INPUT BALLS ARE CERTIFIED")
    print(f"precision={args.bits} bits; N=2..{args.max_N}; two unweighted OLS parameterizations")
    print("fit kind start count C D rms max-residual R2 cond(X'X)")
    fits = {}
    for fit_name, scaled in (("P-OLS", False), ("LP-OLS", True)):
        fits[fit_name] = {"restricted": {}, "full": {}}
        for kind, values in (("restricted", restricted), ("full", full)):
            for start in starts:
                fit = fit_window(values, start, args.max_N, scaled=scaled)
                fits[fit_name][kind][start] = fit
                print(
                    f"{fit_name} {kind} {start} {fit['count']} "
                    f"{compact(fit['c'])} {compact(fit['d'])} "
                    f"{compact(fit['rms'], 8)} "
                    f"{compact(fit['max_residual'], 8)} {fit['r2']:.10f} "
                    f"{fit['condition']:.6g}"
                )

    print("full-minus-restricted coefficient checks")
    print("fit start delta-C delta-D delta-D-minus-1")
    for fit_name in fits:
        for start in starts:
            delta_c = (fits[fit_name]["full"][start]["c"]
                       - fits[fit_name]["restricted"][start]["c"])
            delta_d = (fits[fit_name]["full"][start]["d"]
                       - fits[fit_name]["restricted"][start]["d"])
            print(
                f"{fit_name} {start} {compact(delta_c)} {compact(delta_d)} "
                f"{compact(delta_d - 1)}"
            )

    widest = max(
        radius(fit[key])
        for by_kind in fits.values()
        for by_start in by_kind.values()
        for fit in by_start.values()
        for key in ("c", "d")
    )
    print(f"largest reported coefficient interval radius <= {widest:.3e}")


if __name__ == "__main__":
    main()
