#!/usr/bin/env python3
"""Arb certificate for P_N, <F_N,D_N>, and P_{N+1}-P_N.

Requires python-flint. Usage: python certify_restricted_jump.py N Q BITS
The omitted interval (0,1/Q) is enclosed by absolute coefficient bounds.
"""

import heapq
import sys

from flint import arb, ctx


def mobius_sieve(n):
    mu = [0] * (n + 1)
    composite = [False] * (n + 1)
    primes = []
    mu[1] = 1
    for i in range(2, n + 1):
        if not composite[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > n:
                break
            composite[i * p] = True
            if i % p == 0:
                mu[i * p] = 0
                break
            mu[i * p] = -mu[i]
    return mu


def widen(value, radius):
    return value + arb(0, str(radius.upper()))


def certify(N, Q, bits):
    assert N >= 2 and Q >= N
    ctx.prec = bits
    mu = mobius_sieve(N)
    logs = [arb(0)] + [arb(a).log() for a in range(1, N + 1)]
    L = logs[N]
    AF = sum(arb(mu[a]) / a * (1 - logs[a] / L) for a in range(1, N + 1))
    AD = sum(arb(mu[a]) * logs[a] / a for a in range(1, N + 1))
    P, C, R = AF * AF, AF * AD, AD * AD
    events = [(a, a) for a in range(1, N + 1) if mu[a]]
    heapq.heapify(events)
    floor_mu = 0
    floor_mulog = arb(0)
    for m in range(1, Q):
        while events and events[0][0] == m:
            _, a = heapq.heappop(events)
            floor_mu += mu[a]
            floor_mulog += mu[a] * logs[a]
            heapq.heappush(events, (m + a, a))
        BF = 1 - floor_mu + floor_mulog / L
        BD = -floor_mulog
        lr = (arb(m + 1) / m).log()
        length = arb(1) / m - arb(1) / (m + 1)
        P += AF * AF + 2 * AF * BF * lr + BF * BF * length
        C += AF * AD + (AF * BD + AD * BF) * lr + BF * BD * length
        R += AD * AD + 2 * AD * BD * lr + BD * BD * length
    MF = arb(1) + sum(abs(mu[a]) * (1 - logs[a] / L) for a in range(1, N + 1))
    MD = sum(abs(mu[a]) * logs[a] for a in range(1, N + 1))
    PI = widen(P, MF * MF / Q)
    CI = widen(C, MF * MD / Q)
    RI = widen(R, MD * MD / Q)
    h = 1 / L - 1 / arb(N + 1).log()
    delta = 2 * h * CI + h * h * RI
    for name, value in (("P", PI), ("cross", CI), ("D2", RI), ("increment", delta)):
        print(name, "in", value)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("usage: certify_restricted_jump.py N Q BITS")
    certify(*(int(x) for x in sys.argv[1:]))
