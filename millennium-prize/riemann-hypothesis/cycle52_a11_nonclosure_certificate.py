#!/usr/bin/env python3
"""Standalone fail-closed Arb certificate for finite a=11 nonclosure.

Run:
  env LC_ALL=C PYTHONDONTWRITEBYTECODE=1 \
    uv run --isolated --no-project --python 3.12.13 \
    --with python-flint==0.9.0 python -I -B cycle52_a11_nonclosure_certificate.py
"""
from itertools import permutations
import importlib.metadata
import sys
import flint
from flint import arb, ctx

BITS = 256
ctx.prec = BITS


def require(ok, msg):
    if not ok:
        raise SystemExit("FAIL-CLOSED: " + msg)


def ball(x, digits=60):
    require(isinstance(x, arb), "non-Arb serialization")
    return x.str(digits, radius=True)


def sieve(limit):
    mu = [0] * (limit + 1)
    composite = [False] * (limit + 1)
    primes = []
    mu[1] = 1
    for n in range(2, limit + 1):
        if not composite[n]:
            primes.append(n)
            mu[n] = -1
        for p in primes:
            if n * p > limit:
                break
            composite[n * p] = True
            if n % p == 0:
                mu[n * p] = 0
                break
            mu[n * p] = -mu[n]
    return mu, primes


def det_leibniz(A):
    n = len(A)
    require(all(len(row) == n for row in A), "non-square determinant input")
    ans = arb(0)
    for p in permutations(range(n)):
        inversions = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = arb(-1 if inversions & 1 else 1)
        for i in range(n):
            term *= A[i][p[i]]
        ans += term
    return ans


def main():
    require(ctx.prec == BITS, "could not set Arb precision")
    require(sys.version_info[:3] == (3, 12, 13), "unexpected CPython")
    require(importlib.metadata.version("python-flint") == "0.9.0",
            "unexpected python-flint")
    require(flint.__FLINT_VERSION__ == "3.6.0", "unexpected FLINT")

    a = 11
    M = 2 * a - 1
    N = 2 * a + 3
    C = arb(6) / 5       # theta=2/5
    tau = C - 1
    mu, primes = sieve(N)
    logs = [arb(0)] + [arb(n).log() for n in range(1, N + 2)]
    Lambda = [arb(0)] * (N + 1)
    for p in primes:
        pp = p
        while pp <= N:
            Lambda[pp] = logs[p]
            pp *= p

    psi = [arb(0)] * (N + 1)
    Cr = [arb(0)] * (N + 2)
    mrec = [arb(0)] * (N + 1)
    ell = [arb(0)] * (N + 1)
    Pi = [arb(0)] * (N + 1)
    for n in range(1, N + 1):
        psi[n] = psi[n - 1] + Lambda[n]
        mrec[n] = mrec[n - 1] + arb(mu[n]) / n
        ell[n] = ell[n - 1] + arb(mu[n]) * logs[n] / n
        Pi[n] = Pi[n - 1] + psi[n] / (n * (n + 1))
        if n >= 2:
            Cr[n] = Cr[n - 1] + psi[n - 1] * (logs[n] - logs[n - 1])

    # All physical squarefree rows in [a, floor(3a/2)].
    rows = [q for q in range(a, 3 * a // 2 + 1) if mu[q] != 0]
    require(rows == [11, 13, 14, 15], f"unexpected exact row set: {rows}")

    direct = []
    normal = []
    for q in rows:
        x = logs[q]
        Bd = arb(0)
        Bn = arb(0)
        for n in range(q, M + 1):
            L = logs[n]
            w = 1 - L / logs[n + 1]
            An = C - w
            eta = tau / An
            alpha = w * An * (x / L - eta)
            aqn = arb(n) / q - (arb(n + 1) / q).log()
            jqn = (arb(n + 1) / q).log() - (Pi[n] - Pi[q - 1])
            E = Cr[n + 1] - n
            # Direct Cycle-49 canonical residual:
            residual = E / q + jqn + aqn * (1 + ell[n] - eta * L * mrec[n])
            Bd += alpha * residual / L
            # Algebraically expanded normal form:
            T = ell[n] - eta * L * mrec[n]
            p = w * An / (L * L)
            r = -w * tau / L
            Astar = Cr[n + 1] + n * T
            Dstar = -Pi[n] - T * logs[n + 1]
            Bn += (p * x + r) * (x * T + Astar / q + Pi[q - 1] + Dstar)
        require((Bd - Bn).contains(0), f"direct/normal balls disjoint at q={q}")
        require(abs(Bd - Bn).upper() < arb(2) ** -170,
                f"direct/normal discrepancy too wide at q={q}: {ball(Bd-Bn)}")
        direct.append(Bd)
        normal.append(Bn)

    # Rows q; columns exactly (1, q/11, log(q/11), B_11(q)).
    A_direct = [[arb(1), arb(q) / a, (arb(q) / a).log(), B]
                for q, B in zip(rows, direct)]
    A_normal = [[arb(1), arb(q) / a, (arb(q) / a).log(), B]
                for q, B in zip(rows, normal)]
    D_direct = det_leibniz(A_direct)
    D_normal = det_leibniz(A_normal)
    require(D_direct > 0 and not D_direct.contains(0),
            "direct determinant not certified positive: " + ball(D_direct))
    require(D_normal > 0 and not D_normal.contains(0),
            "normal determinant not certified positive: " + ball(D_normal))
    require((D_direct - D_normal).contains(0), "determinant cross-check balls disjoint")

    print("CPython=3.12.13 python-flint=0.9.0 FLINT=3.6.0 Arb_bits=256")
    print("theta=2/5 C=6/5 tau=1/5 a=11 M=21")
    print("rows=[11,13,14,15]")
    print("columns=[1,q/11,log(q/11),B_11(q)]")
    for q, Bd, Bn in zip(rows, direct, normal):
        print(f"B_direct[{q}]={ball(Bd)}")
        print(f"B_normal[{q}]={ball(Bn)}")
        print(f"direct_minus_normal[{q}]={ball(Bd-Bn)}")
    print("det_direct=" + ball(D_direct))
    print("det_normal=" + ball(D_normal))
    print("det_direct_minus_normal=" + ball(D_direct-D_normal))
    print("certified_sign=positive")
    print("conclusion=B_11_not_in_span{1,q/11,log(q/11)}_on_exact_physical_rows")


if __name__ == "__main__":
    main()
