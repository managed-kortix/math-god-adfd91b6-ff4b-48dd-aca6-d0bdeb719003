#!/usr/bin/env python3
"""Rigorous finite audit of the Cycle 48 coherent weighted-mean channel.

For every 2 <= M < B <= max_n, this program forms the physical vectors F_n
with the restricted Vasyunin Gram matrix, then certifies the weighted mean,
anchor reserve, dispersion, terminal budget, and coherent-channel ratio

    R = (W ||bar F||^2 - <F_M, bar F>) / (S - V).

Thus Q = (S - V) (1 - R).  All logarithms, Gram entries, contractions, and
comparisons use Arb balls through python-flint; no floating-point surrogate is
used.  The default cutoff is 128.  Use ``--max-n 512`` for the larger audit.
"""

import argparse
from dataclasses import dataclass

from flint import arb, ctx

from certify_complete_gram import RestrictedGram, mobius_sieve


@dataclass
class Bounds:
    """Certified enclosure of the minimum and maximum of a finite family."""

    minimum_lower: object = None
    minimum_upper: object = None
    maximum_lower: object = None
    maximum_upper: object = None
    minimum_lower_at: tuple = None
    minimum_upper_at: tuple = None
    maximum_lower_at: tuple = None
    maximum_upper_at: tuple = None

    def add(self, value, pair):
        lo, hi = value.lower(), value.upper()
        if self.minimum_lower is None or lo < self.minimum_lower:
            self.minimum_lower, self.minimum_lower_at = lo, pair
        if self.minimum_upper is None or hi < self.minimum_upper:
            self.minimum_upper, self.minimum_upper_at = hi, pair
        if self.maximum_lower is None or lo > self.maximum_lower:
            self.maximum_lower, self.maximum_lower_at = lo, pair
        if self.maximum_upper is None or hi > self.maximum_upper:
            self.maximum_upper, self.maximum_upper_at = hi, pair

    def report(self, name):
        print(
            f"{name}: min in [{self.minimum_lower}, {self.minimum_upper}] "
            f"(bound witnesses {self.minimum_lower_at}, {self.minimum_upper_at})"
        )
        print(
            f"{name}: max in [{self.maximum_lower}, {self.maximum_upper}] "
            f"(bound witnesses {self.maximum_lower_at}, {self.maximum_upper_at})"
        )


def physical_cross_table(max_n, mu, logs, gram):
    """Return exact-formula Arb enclosures for all <F_m,F_n> and <F_m,D_n>.

    For fixed m, first contract F_m against every rho_b.  Prefixing those
    contractions gives every cross inner product in O(1) additional work per
    n.  This is algebraically the direct RestrictedGram contraction, not a
    polarization of precomputed energies.
    """
    zero = arb(0)
    cross = [[zero for _ in range(max_n + 1)] for _ in range(max_n + 1)]
    anchor_d = [[zero for _ in range(max_n + 1)] for _ in range(max_n + 1)]
    active = [a for a in range(1, max_n + 1) if mu[a]]

    for m in range(2, max_n + 1):
        lm = logs[m]
        coefficients = {
            a: mu[a] * (1 - logs[a] / lm) for a in active if a <= m
        }
        f_chi = arb(1)
        for a, coefficient in coefficients.items():
            f_chi += coefficient * gram.chi_cross(a)

        rho_cross = [zero for _ in range(max_n + 1)]
        for b in active:
            value = gram.chi_cross(b)
            for a, coefficient in coefficients.items():
                value += coefficient * gram.entry(a, b)
            rho_cross[b] = value

        plain_prefix = arb(0)
        log_prefix = arb(0)
        for n in range(1, max_n + 1):
            if mu[n]:
                plain_prefix += mu[n] * rho_cross[n]
                log_prefix += mu[n] * logs[n] * rho_cross[n]
            if n >= m:
                value = f_chi + plain_prefix - log_prefix / logs[n]
                cross[m][n] = value
                cross[n][m] = value
                anchor_d[m][n] = log_prefix

    return cross, anchor_d


def require_identity(name, pair, residual):
    if not residual.contains(0):
        raise AssertionError(f"{name} failed at {pair}: residual {residual}")


def require_positive(name, pair, value):
    if not value > 0:
        raise AssertionError(f"{name} is not certified positive at {pair}: {value}")


def audit(max_n=128, bits=192):
    if max_n < 3:
        raise ValueError("max_n must be at least 3")
    if bits < 80:
        raise ValueError("bits must be at least 80")

    ctx.prec = bits
    mu = mobius_sieve(max_n)
    logs = [arb(0)] + [arb(n).log() for n in range(1, max_n + 2)]
    gram = RestrictedGram()
    cross, anchor_d = physical_cross_table(max_n, mu, logs, gram)

    weights = [arb(0) for _ in range(max_n + 1)]
    for n in range(2, max_n + 1):
        weights[n] = 1 - logs[n] / logs[n + 1]

    tracked = {
        name: Bounds() for name in (
            "cross", "W", "E", "mean_energy", "anchor_mean", "S", "V",
            "Q", "S_minus_V", "coherent_deficit", "R"
        )
    }
    sign_counts = {
        "coherent_deficit_negative": 0,
        "coherent_deficit_positive": 0,
        "R_negative": 0,
        "R_positive": 0,
        "R_less_than_1": 0,
    }
    identity_count = 0
    pair_count = 0

    for m in range(2, max_n):
        p_m = cross[m][m]
        require_positive("P_M", (m, m), p_m)
        W = arb(0)
        E = arb(0)
        norm_sum = arb(0)
        anchor_sum = arb(0)
        variance_online = arb(0)
        reserve_plain = arb(0)
        reserve_weighted = arb(0)

        for b in range(m, max_n + 1):
            w = weights[b]
            old_W = W
            old_norm_sum = norm_sum
            cross_with_old_sum = arb(0)
            for n in range(m, b):
                cross_with_old_sum += weights[n] * cross[n][b]

            W += w
            E += w * cross[b][b]
            anchor_sum += w * cross[m][b]
            norm_sum += 2 * w * cross_with_old_sum + w * w * cross[b][b]
            if b > m:
                displacement = (
                    cross[b][b] - 2 * cross_with_old_sum / old_W
                    + old_norm_sum / (old_W * old_W)
                )
                variance_online += w * old_W / W * displacement

            h = 1 / logs[b] - 1 / logs[b + 1]
            atomic_reserve = -anchor_d[m][b]
            reserve_plain += h * atomic_reserve
            reserve_weighted += h * atomic_reserve * W

            if b == m:
                continue

            pair = (m, b)
            pair_count += 1
            mean_energy = norm_sum / (W * W)
            anchor_mean = anchor_sum / W
            S = p_m - anchor_mean
            V = E - W * mean_energy
            Q = p_m - E
            S_formula = reserve_plain - reserve_weighted / W
            coherent_deficit = W * mean_energy - anchor_mean
            reserve_after_dispersion = S - V

            require_positive("W", pair, W)
            require_positive("E", pair, E)
            require_positive("mean energy", pair, mean_energy)
            require_positive("anchor-mean inner product", pair, anchor_mean)
            require_positive("S", pair, S)
            require_positive("V", pair, V)
            require_positive("S-V", pair, reserve_after_dispersion)
            require_positive("Q", pair, Q)

            R = coherent_deficit / reserve_after_dispersion
            if not R < 1:
                raise AssertionError(f"R < 1 is not certified at {pair}: {R}")

            residuals = (
                ("mean norm", norm_sum - W * W * mean_energy),
                ("weighted variance", V - variance_online),
                ("energy split", E - W * mean_energy - V),
                ("anchor reserve", S - S_formula),
                ("terminal decomposition",
                 Q - S + V - anchor_mean + W * mean_energy),
                ("coherent ratio", Q - reserve_after_dispersion * (1 - R)),
            )
            for name, residual in residuals:
                require_identity(name, pair, residual)
                identity_count += 1

            values = {
                "cross": cross[m][b], "W": W, "E": E,
                "mean_energy": mean_energy, "anchor_mean": anchor_mean,
                "S": S, "V": V, "Q": Q,
                "S_minus_V": reserve_after_dispersion,
                "coherent_deficit": coherent_deficit, "R": R,
            }
            for name, value in values.items():
                tracked[name].add(value, pair)

            if coherent_deficit < 0:
                sign_counts["coherent_deficit_negative"] += 1
            elif coherent_deficit > 0:
                sign_counts["coherent_deficit_positive"] += 1
            else:
                raise AssertionError(
                    f"coherent deficit sign is unresolved at {pair}: {coherent_deficit}"
                )
            if R < 0:
                sign_counts["R_negative"] += 1
            elif R > 0:
                sign_counts["R_positive"] += 1
            else:
                raise AssertionError(f"R sign is unresolved at {pair}: {R}")
            sign_counts["R_less_than_1"] += 1

    expected = (max_n - 2) * (max_n - 1) // 2
    if pair_count != expected:
        raise AssertionError(f"pair count {pair_count} != {expected}")

    print(f"Cycle 48 coherent-channel audit: max_n={max_n}, bits={bits}")
    print(f"certified pairs: {pair_count}; identity checks: {identity_count}")
    print("sign counts:", ", ".join(f"{k}={v}" for k, v in sign_counts.items()))
    for name in tracked:
        tracked[name].report(name)
    return pair_count, identity_count, sign_counts, tracked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=128)
    parser.add_argument("--bits", type=int, default=192)
    args = parser.parse_args()
    audit(args.max_n, args.bits)


if __name__ == "__main__":
    main()
