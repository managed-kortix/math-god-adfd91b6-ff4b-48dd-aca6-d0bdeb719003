#!/usr/bin/env python3
"""Certified finite Cycle 45 correlation-dispersion census.

For fixed theta=2/5 on [a,2a), reconstruct the de-signed correlations

    hat_c(q) = mu(q)c_q = beta(q) + sum_{d<2a} mu(d) W(q,d),

where W is unsigned.  Compute D, the diagonal comparison Delta, and their
normalised scales using outward Arb arithmetic.  Every identity check fails
closed.  This is finite diagnostic code only, not an asymptotic or RH result.
"""

import argparse
from fractions import Fraction
import json
from pathlib import Path

from flint import arb, ctx

from certify_complete_gram import RestrictedGram, mobius_sieve
from cycle43_divisor_admission_multiprobe import CompensatedBlock
from cycle44_boundary_envelope_scan import set_fixed_theta

THETA_NUMERATOR = 2
THETA_DENOMINATOR = 5
DEFAULT_STARTS = (32, 64, 128, 256, 512, 1024)
DEFAULT_INTERVALS = ("1,2", "1,3/2")


def arb_sum(values):
    return sum(values, arb(0))


def interval_text(value, digits=25):
    return value.str(digits)


def parse_fraction(text):
    return Fraction(text.strip())


def parse_interval(text):
    parts = text.split(",")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("interval must be LO,HI")
    lo, hi = (parse_fraction(part) for part in parts)
    if not (0 < lo < hi <= 2):
        raise argparse.ArgumentTypeError("require 0 < LO < HI <= 2")
    return lo, hi


def interval_json(interval):
    return [float(interval[0]), float(interval[1])]


def squarefree_rows(data, interval):
    lo, hi = interval
    return [
        q for q in data.squarefree
        if lo <= Fraction(q, data.start) <= hi
    ]


class DispersionData:
    """Exact-formula Arb reconstruction, with unsigned W cached by row."""

    def __init__(self, start, bits):
        if start < 2:
            raise ValueError("start must be at least 2")
        if bits < 128:
            raise ValueError("bits must be at least 128")
        ctx.prec = bits
        self.start = start
        self.stop = 2 * start
        self.theta = arb(THETA_NUMERATOR) / THETA_DENOMINATOR
        self.tau = 1 - 2 * self.theta
        self.mu = mobius_sieve(self.stop)
        self.gram = RestrictedGram()
        self.logs = [arb(0)] + [
            arb(n).log() for n in range(1, self.stop + 2)
        ]
        self.w = {}
        self.A = {}
        self.eta = {}
        for n in range(self.start, self.stop):
            ratio = self.logs[n] / self.logs[n + 1]
            self.w[n] = 1 - ratio
            self.A[n] = 1 + ratio - 2 * self.theta
            self.eta[n] = self.tau / self.A[n]
            if not self.A[n] > 0:
                raise RuntimeError(f"unresolved/nonpositive A at n={n}")
        self.squarefree = [d for d in range(1, self.stop) if self.mu[d]]
        self._W = {}
        self._beta = {}

    def b(self, q, n):
        return self.logs[q] / self.logs[n] - self.eta[n]

    def H(self, q, d):
        return arb_sum(
            self.w[n] * self.A[n] * self.b(q, n) * self.b(d, n)
            for n in range(max(self.start, q, d), self.stop)
        )

    def H0(self, q):
        return arb_sum(
            self.w[n] * self.A[n] * self.eta[n] * self.b(q, n)
            for n in range(max(self.start, q), self.stop)
        )

    def W(self, q, d):
        """Unsigned W(q,d): no outer mu(q) or mu(d) factor."""
        key = (min(q, d), max(q, d))
        if key not in self._W:
            # H and the spatial Gram are symmetric, so one cache entry serves
            # both orientations.  This matters for the full a=1024 census.
            self._W[key] = self.gram.entry(q, d) * self.H(q, d)
        return self._W[key]

    def beta(self, q):
        if q not in self._beta:
            g_q = (self.logs[q] + 1 - arb.const_euler()) / q
            self._beta[q] = -g_q * self.H0(q)
        return self._beta[q]

    def signed_W_sum(self, q, lo=1, hi=None):
        if hi is None:
            hi = self.stop
        return arb_sum(
            self.mu[d] * self.W(q, d)
            for d in self.squarefree if lo <= d < hi
        )

    def hat_c(self, q):
        return self.beta(q) + self.signed_W_sum(q)

    def direct_hat_c(self, q):
        """Direct X contraction for mu(q)c_q, independent of beta+sum(mu W)."""
        total = arb(0)
        for n in range(max(self.start, q), self.stop):
            spatial = -self.eta[n] * self.gram.chi_cross(q)
            spatial += arb_sum(
                self.mu[d] * self.b(d, n) * self.gram.entry(q, d)
                for d in self.squarefree if d <= n
            )
            total += self.w[n] * self.A[n] * self.b(q, n) * spatial
        return total


def verify_all_rows(data, bits):
    """Check the normalization identities once for all squarefree bulk rows."""
    rows = [q for q in data.squarefree if data.start <= q < data.stop]
    block = CompensatedBlock(data.start, data.stop, bits)
    set_fixed_theta(block, data.theta)
    max_direct = arb(0)
    max_existing = arb(0)
    for q in rows:
        hat = data.hat_c(q)
        direct_error = hat - data.direct_hat_c(q)
        existing_error = hat - data.mu[q] * block.correlation(q)
        if not direct_error.contains(0):
            raise RuntimeError(("direct identity failed", data.start, q,
                                direct_error))
        if not existing_error.contains(0):
            raise RuntimeError(("existing probe identity failed", data.start,
                                q, existing_error))
        if abs(direct_error).upper() > max_direct:
            max_direct = abs(direct_error).upper()
        if abs(existing_error).upper() > max_existing:
            max_existing = abs(existing_error).upper()
    return max_direct, max_existing


def census_row(data, interval, identity_errors):
    start = data.start
    L = data.logs[start]
    rows = squarefree_rows(data, interval)
    direct_error, existing_error = identity_errors

    hats = {q: data.hat_c(q) for q in rows}
    beta = {q: data.beta(q) for q in rows}
    signed_W = {q: hats[q] - beta[q] for q in rows}
    W2_by_q = {
        q: arb_sum(data.W(q, d) ** 2 for d in data.squarefree)
        for q in rows
    }

    D = arb_sum(hats[q] ** 2 for q in rows)
    beta2 = arb_sum(beta[q] ** 2 for q in rows)
    W2 = arb_sum(W2_by_q.values())
    Delta = beta2 + W2
    beta_cross = arb_sum(2 * beta[q] * signed_W[q] for q in rows)
    # Algebraically identical to 2 sum_{d<e} mu(d)mu(e)W(q,d)W(q,e),
    # while avoiding a cubic pair loop at a=1024.
    off_diagonal = arb_sum(
        signed_W[q] ** 2 - W2_by_q[q] for q in rows
    )
    recombination_error = D - (Delta + beta_cross + off_diagonal)
    if not recombination_error.contains(0):
        raise RuntimeError(("dispersion decomposition failed", start,
                            interval, recombination_error))

    cuts = (1, start // 2, start, 3 * start // 2, 2 * start)
    ranges = []
    for lo, hi in zip(cuts, cuts[1:]):
        unsigned_energy = arb_sum(
            data.W(q, d) ** 2
            for q in rows for d in data.squarefree if lo <= d < hi
        )
        signed = {
            q: data.signed_W_sum(q, lo, hi) for q in rows
        }
        ranges.append({
            "lo": lo,
            "hi": hi,
            "W2": interval_text(unsigned_energy),
            "signed_energy": interval_text(
                arb_sum(value ** 2 for value in signed.values())
            ),
            "signed_full_corr": interval_text(
                arb_sum(signed[q] * hats[q] for q in rows)
            ),
        })

    return {
        "a": start,
        "I": interval_json(interval),
        "rank": len(rows),
        "D": interval_text(D),
        "L3D": interval_text(L ** 3 * D),
        "Delta": interval_text(Delta),
        "L2Delta": interval_text(L ** 2 * Delta),
        "LD_over_Delta": interval_text(L * D / Delta),
        "beta2": interval_text(beta2),
        "W2": interval_text(W2),
        "beta_signedW_cross": interval_text(beta_cross),
        "signedW_offdiag": interval_text(off_diagonal),
        "recombination_error": interval_text(recombination_error),
        "direct_identity_max_error_ball": interval_text(direct_error),
        "existing_probe_identity_max_error_ball": interval_text(existing_error),
        "ranges": ranges,
    }


def run(starts=DEFAULT_STARTS, intervals=DEFAULT_INTERVALS, bits=192):
    parsed = [parse_interval(item) if isinstance(item, str) else item
              for item in intervals]
    rows = []
    for start in starts:
        data = DispersionData(start, bits)
        identity_errors = verify_all_rows(data, bits)
        rows.extend(
            census_row(data, interval, identity_errors)
            for interval in parsed
        )
    return {
        "scope": (
            "certified finite diagnostic only; no convergence, asymptotic "
            "lower bound, or RH claim"
        ),
        "anchor_commit": "4306d7ce",
        "arb_precision_bits": bits,
        "theta": "2/5",
        "starts": list(starts),
        "intervals": [interval_json(interval) for interval in parsed],
        "row_rule": "squarefree q with q/a in the closed declared interval",
        "normalization": {
            "W": "<rho_q,rho_d> H(q,d), unsigned in q and d",
            "beta": "-g_q H0(q)",
            "hat_c": "mu(q)c_q = beta(q) + sum_d mu(d)W(q,d)",
            "x_a": "(1,(mu(d))_d)",
            "M_a": ("rows q in S_a(I), affine column beta(q), "
                    "squarefree columns W(q,d)"),
            "D": "||M_a x_a||_2^2 = sum_{q in I} hat_c(q)^2",
            "Delta": ("||M_a||_F^2 = sum_{q in I}(beta(q)^2 + "
                      "sum_d W(q,d)^2)"),
        },
        "verdict_policy": "outward Arb intervals; failed identities abort",
        "rows": rows,
    }


def print_summary(payload):
    print("CERTIFIED FINITE DIAGNOSTIC ONLY; NOT AN ASYMPTOTIC/RH CLAIM")
    print(f"theta=2/5, Arb precision={payload['arb_precision_bits']} bits")
    for row in payload["rows"]:
        print(
            f"a={row['a']} I={row['I']} m={row['rank']} "
            f"D={row['D']} Delta={row['Delta']} "
            f"L*D/Delta={row['LD_over_Delta']} "
            f"L^3*D={row['L3D']} L^2*Delta={row['L2Delta']}"
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--starts", nargs="+", type=int,
                        default=DEFAULT_STARTS)
    parser.add_argument("--intervals", nargs="+",
                        default=DEFAULT_INTERVALS)
    parser.add_argument("--bits", type=int, default=192)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    payload = run(tuple(args.starts), tuple(args.intervals), args.bits)
    print_summary(payload)
    if args.json:
        args.json.write_text(json.dumps(payload, indent=2) + "\n",
                             encoding="ascii")


if __name__ == "__main__":
    main()
