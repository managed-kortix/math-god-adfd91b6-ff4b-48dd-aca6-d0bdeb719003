#!/usr/bin/env python3
"""Fail-closed Arb certificate for the Cycle-52 smooth-span finite audit.

This program evaluates the exact finite complete-prefix residual from Cycle 49
on the physical squarefree rows at a=8192 and a=16384.  It certifies the
orthogonal energy captured by span{1,q/a,log(q/a)} using an Arb Gram solve.
The result is finite only and makes no asymptotic or RH claim.
"""
from __future__ import annotations

import hashlib
import importlib.metadata
import platform
from pathlib import Path

import flint
from flint import arb, arb_mat, ctx

SCRIPT_PATH = Path(__file__).resolve()
BITS = 256
ctx.prec = BITS
SCALES = (8192, 16384)
C = arb(6) / 5
TAU = C - 1


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sieve(limit: int):
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
    lam = [arb(0) for _ in range(limit + 1)]
    for p in primes:
        value = p
        logp = arb(p).log()
        while value <= limit:
            lam[value] = logp
            value *= p
    return mu, lam


def require_runtime() -> None:
    observed = (
        platform.python_version(),
        importlib.metadata.version("python-flint"),
        flint.__FLINT_VERSION__,
    )
    required = ("3.12.13", "0.9.0", "3.6.0")
    if observed != required:
        raise RuntimeError(("wrong runtime", observed, required))
    if ctx.prec != BITS:
        raise RuntimeError(("wrong Arb precision", ctx.prec, BITS))


def ball_sum(values):
    return sum(values, arb(0))


def run_scale(a: int, mu, lam, logs):
    M = 2 * a - 1
    psi = [arb(0) for _ in range(M + 2)]
    csum = [arb(0) for _ in range(M + 2)]
    mrecip = [arb(0) for _ in range(M + 2)]
    ell = [arb(0) for _ in range(M + 2)]
    pweight = [arb(0) for _ in range(M + 2)]
    for n in range(1, M + 2):
        psi[n] = psi[n - 1] + lam[n]
        mrecip[n] = mrecip[n - 1] + arb(mu[n]) / n
        ell[n] = ell[n - 1] + arb(mu[n]) * logs[n] / n
        pweight[n] = pweight[n - 1] + psi[n] / (n * (n + 1))
        if n >= 2:
            csum[n] = csum[n - 1] + psi[n - 1] * (logs[n] - logs[n - 1])

    # Suffix coefficients for the exact normal form.  For x=log q,
    # alpha_{q,n}/L_n=p_n*x+r_n and
    # R_{q,n}=x*T_n+Astar_n/q+P_{q-1}+Dstar_n.
    names = ("pT", "rT", "pD", "rD", "p", "r", "pA", "rA")
    suffix = {name: [arb(0) for _ in range(M + 2)] for name in names}
    for n in range(M, a - 1, -1):
        Ln = logs[n]
        w = 1 - Ln / logs[n + 1]
        An = C - w
        eta = TAU / An
        pn = w * An / (Ln * Ln)
        rn = -w * TAU / Ln
        Tn = ell[n] - eta * Ln * mrecip[n]
        Astar = csum[n + 1] + n * Tn
        Dstar = -pweight[n] - Tn * logs[n + 1]
        values = {
            "pT": pn * Tn, "rT": rn * Tn,
            "pD": pn * Dstar, "rD": rn * Dstar,
            "p": pn, "r": rn,
            "pA": pn * Astar, "rA": rn * Astar,
        }
        for name in names:
            suffix[name][n] = suffix[name][n + 1] + values[name]

    rows = [q for q in range(a, 3 * a // 2 + 1) if mu[q] != 0]
    basis = [[], [], []]
    B = []
    for q in rows:
        x = logs[q]
        value = (
            x * x * suffix["pT"][q]
            + x * (suffix["rT"][q] + suffix["pD"][q]
                   + pweight[q - 1] * suffix["p"][q]
                   + suffix["pA"][q] / q)
            + suffix["rD"][q]
            + pweight[q - 1] * suffix["r"][q]
            + suffix["rA"][q] / q
        )
        u = arb(q) / a
        basis[0].append(arb(1))
        basis[1].append(u)
        basis[2].append(u.log())
        B.append(value)

    # Independently replay the unsummed Cycle-49 residual at five rows.  This
    # checks the suffix implementation against the defining temporal formula
    # without turning the full O(a) certificate into an O(a^2) computation.
    check_indices = sorted({0, len(rows) // 4, len(rows) // 2,
                            3 * len(rows) // 4, len(rows) - 1})
    crosscheck_sum_abs = arb(0)
    for index in check_indices:
        q = rows[index]
        x = logs[q]
        direct = arb(0)
        for n in range(q, M + 1):
            Ln = logs[n]
            w = 1 - Ln / logs[n + 1]
            An = C - w
            eta = TAU / An
            alpha = w * An * (x / Ln - eta)
            aterm = arb(n) / q - (arb(n + 1) / q).log()
            jterm = (arb(n + 1) / q).log() - (pweight[n] - pweight[q - 1])
            Eterm = csum[n + 1] - n
            residual = (Eterm / q + jterm
                        + aterm * (1 + ell[n] - eta * Ln * mrecip[n]))
            direct += alpha / Ln * residual
        difference = direct - B[index]
        if not difference.contains(0):
            raise ArithmeticError(("suffix/direct mismatch", a, q, difference))
        crosscheck_sum_abs += abs(difference)

    gram = arb_mat(3, 3)
    moment = arb_mat(3, 1)
    for i in range(3):
        moment[i, 0] = ball_sum(basis[i][k] * B[k] for k in range(len(rows)))
        for j in range(3):
            gram[i, j] = ball_sum(
                basis[i][k] * basis[j][k] for k in range(len(rows))
            )
    leading2 = gram[0, 0] * gram[1, 1] - gram[0, 1] * gram[1, 0]
    determinant = gram.det()
    if not gram[0, 0].lower() > 0 or not leading2.lower() > 0:
        raise ArithmeticError(("Gram leading minors not certified positive",
                               gram[0, 0], leading2))
    if not determinant.lower() > 0 or determinant.contains(0):
        raise ArithmeticError(f"Gram determinant not certified positive: {determinant}")
    try:
        coefficients = gram.solve(moment)
    except ZeroDivisionError as exc:
        raise ArithmeticError("certified Gram solve failed") from exc
    projected = (moment.transpose() * coefficients)[0, 0]
    total = ball_sum(value * value for value in B)
    residual = total - projected
    capture = projected / total
    omitted = residual / total
    if not total.lower() > 0 or not projected.lower() > 0 or not residual.lower() > 0:
        raise ArithmeticError(("energy sign not certified", total, projected, residual))
    if not capture.lower() > 0 or not capture.upper() < 1:
        raise ArithmeticError(("capture outside (0,1)", capture))
    if not omitted.lower() > 0 or not omitted.upper() < 1:
        raise ArithmeticError(("omitted ratio outside (0,1)", omitted))
    if a == 8192 and not capture.upper() < arb("0.77"):
        raise ArithmeticError(("failed a=8192 breakdown gate", capture))
    if a == 16384 and not capture.upper() < arb("0.43"):
        raise ArithmeticError(("failed a=16384 breakdown gate", capture))
    row_sha = hashlib.sha256(
        ",".join(map(str, rows)).encode("ascii")
    ).hexdigest()
    return (rows, row_sha, leading2, determinant, total, projected, residual,
            capture, omitted, len(check_indices), crosscheck_sum_abs)


def main() -> None:
    require_runtime()
    ctx.prec = BITS
    maximum = 2 * max(SCALES) + 1
    mu, lam = sieve(maximum)
    logs = [arb(0)] + [arb(n).log() for n in range(1, maximum + 1)]
    print("scope=finite Arb smooth-span audit only; no asymptotic/RH inference")
    print(f"python={platform.python_version()} "
          f"python-flint={importlib.metadata.version('python-flint')} "
          f"FLINT={flint.__FLINT_VERSION__} precision_bits={ctx.prec}")
    print("theta=2/5 C=6/5 I0=[1,3/2] basis=(1,q/a,log(q/a)) M=2a-1")
    print(f"source_sha256={sha256_file(SCRIPT_PATH)}")
    for a in SCALES:
        (rows, row_sha, leading2, det, total, projected, residual, capture,
         omitted, check_count, crosscheck_sum_abs) = run_scale(a, mu, lam, logs)
        print(f"a={a} rows={len(rows)} direct_crosschecks={check_count}")
        print(f"row_csv_sha256={row_sha}")
        print(f"crosscheck_sum_abs={crosscheck_sum_abs.str(20, radius=True)}")
        print(f"gram_leading_minor_2={leading2.str(40, radius=True)}")
        print(f"gram_det={det.str(40, radius=True)}")
        print(f"total_energy={total.str(40, radius=True)}")
        print(f"projected_energy={projected.str(40, radius=True)}")
        print(f"residual_energy={residual.str(40, radius=True)}")
        print(f"capture={capture.str(40, radius=True)}")
        print(f"omitted={omitted.str(40, radius=True)}")
    print("PASS certified Gram solves and finite breakdown gates capture<0.77,0.43")


if __name__ == "__main__":
    main()
