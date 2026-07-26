#!/usr/bin/env python3
"""Certified finite audit of proposed pairings for the Cycle 41 H impulses."""

import argparse
from collections import deque

from flint import arb, ctx

from certify_complete_gram import RestrictedGram, mobius_sieve
from cycle41_h_event_analysis import factorization, h_event_rows


def least_prime_factor(n):
    return factorization(n)[0][0]


def replacement_map(q):
    """Return 2q/p, where p is the least prime factor of squarefree q."""
    return 2 * q // least_prime_factor(q)


def chronological_pairs(rows, newest=False):
    """Pair each -1 event with an unpaired preceding +1 event."""
    waiting = deque()
    pairs = []
    for row in rows:
        if row["mu_q"] == 1:
            waiting.append(row["q"])
        elif row["mu_q"] == -1 and waiting:
            pairs.append(((waiting.pop() if newest else waiting.popleft()), row["q"]))
    return pairs, tuple(waiting)


def fifo_pairs(rows):
    return chronological_pairs(rows, newest=False)


def lifo_pairs(rows):
    return chronological_pairs(rows, newest=True)


def pair_formula(q, r, mu, logs, gram):
    """Return direct and fully opened values of J_q+J_r for mu(q)=1, mu(r)=-1."""
    if not (q < r and mu[q] == 1 and mu[r] == -1):
        raise ValueError("pair must satisfy q < r, mu(q)=1, mu(r)=-1")

    c_q = logs[q] * logs[q + 1]
    c_r = logs[r] * logs[r + 1]
    e_q = logs[q] * (logs[q + 1] - logs[q]) * gram.entry(q, q)
    e_r = logs[r] * (logs[r + 1] - logs[r]) * gram.entry(r, r)

    u_q = gram.chi_cross(q)
    d_q = arb(0)
    u_r_old = gram.chi_cross(r)
    d_r_old = arb(0)
    for a in range(1, q):
        if mu[a]:
            u_q += mu[a] * gram.entry(a, q)
            d_q += mu[a] * logs[a] * gram.entry(a, q)
            u_r_old += mu[a] * gram.entry(a, r)
            d_r_old += mu[a] * logs[a] * gram.entry(a, r)

    a_q = logs[q] * d_q - c_q * u_q
    a_r_open = logs[r] * d_r_old - c_r * u_r_old
    a_r_open += (logs[r] * logs[q] - c_r) * gram.entry(q, r)
    for s in range(q + 1, r):
        if mu[s]:
            a_r_open += mu[s] * (logs[r] * logs[s] - c_r) * gram.entry(s, r)

    u_r = gram.chi_cross(r)
    d_r = arb(0)
    for a in range(1, r):
        if mu[a]:
            u_r += mu[a] * gram.entry(a, r)
            d_r += mu[a] * logs[a] * gram.entry(a, r)
    a_r = logs[r] * d_r - c_r * u_r

    direct = (2 * a_q - e_q) + (-2 * a_r - e_r)
    opened = 2 * (a_q - a_r_open) - e_q - e_r
    return direct, opened


def sign(value):
    if value > 0:
        return "+"
    if value < 0:
        return "-"
    if value.is_zero():
        return "0"
    return "?"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=240)
    parser.add_argument("--bits", type=int, default=192)
    args = parser.parse_args()
    ctx.prec = args.bits

    mu = mobius_sieve(args.max_n)
    logs = [arb(0)] + [arb(n).log() for n in range(1, args.max_n + 2)]
    gram = RestrictedGram()
    _, rows = h_event_rows(args.max_n, args.bits)
    by_q = {row["q"]: row for row in rows}

    print("CERTIFIED FINITE AUDIT ONLY; NOT AN ASYMPTOTIC THEOREM OR RH PROOF")
    print("\nreplacement q -> 2q/p on selected mu=+1 triggers:")
    for q in (39, 95, 219, 221, 226):
        image = replacement_map(q)
        relation = "same" if image == q else "earlier" if image < q else "later"
        print(f"q={q:3d}, p={least_prime_factor(q):3d}, image={image:3d}, "
              f"mu(image)={mu[image]:2d}, location={relation}")

    pairs, waiting = lifo_pairs(rows)
    selected = [(q, r) for q, r in pairs if q in (39, 95, 219, 221, 226)]
    print("\nLIFO chronological pairs for selected triggers:")
    for q, r in selected:
        direct, opened = pair_formula(q, r, mu, logs, gram)
        if not direct.overlaps(opened):
            raise AssertionError(f"opened pair formula failed at {(q, r)}")
        j_q = by_q[q]["linear"] + by_q[q]["diagonal"]
        j_r = by_q[r]["linear"] + by_q[r]["diagonal"]
        print(f"({q:3d},{r:3d}): sign Jq={sign(j_q)}, Jr={sign(j_r)}, "
              f"Jq+Jr={direct.str(18)} [{sign(direct)}]")

    negative = []
    for q, r in pairs:
        direct, _ = pair_formula(q, r, mu, logs, gram)
        if direct < 0:
            negative.append((q, r, direct))
    print(f"\nLIFO pairs through {args.max_n}: {len(pairs)}; unpaired +1 events: {len(waiting)}")
    print(f"negative paired impulse sums: {len(negative)}")
    for q, r, value in negative[:8]:
        print(f"hostile ({q:3d},{r:3d}): Jq+Jr={value.str(18)}")


if __name__ == "__main__":
    main()
