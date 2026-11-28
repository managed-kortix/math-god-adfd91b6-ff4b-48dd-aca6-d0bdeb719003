#!/usr/bin/env python3
"""Standalone fail-closed 256-bit Arb certificate at theta=2/5, a=10.

This finite certificate proves only the declared four-row determinant sign,
the equality of two algebraically distinct finite reconstructions of B_10,
and one exact-rational finite Mobius cancellation. It proves no asymptotic
statement and no consequence for RH.
"""
from __future__ import annotations

# Capture and validate the local closure before importing any third party code.
import hashlib
import importlib.metadata
import os
import platform
import stat
import sys
from fractions import Fraction
from itertools import permutations
from pathlib import Path

BITS = 256
DIGITS = 65
IDENTITY_EXPONENT = 170
A = 10
M = 2 * A - 1
ROWS = (10, 11, 13, 14, 15)
MINOR_ROWS = (10, 11, 14, 15)
THETA = Fraction(2, 5)
PACKET_RANGE = tuple(range(8, 16))
PACKET_INPUT = {m: Fraction(1) for m in PACKET_RANGE}
PACKET_INPUT[13] = Fraction(5767, 2037)


_RAW_SCRIPT_PATH = Path(__file__)
SCRIPT_PATH = _RAW_SCRIPT_PATH.resolve()
WORKSPACE = SCRIPT_PATH.parents[2]
EXPECTED_RELATIVE = Path("millennium-prize/riemann-hypothesis/cycle52_a10_cell_nonclosure_certificate.py")


def require(condition: bool, label: str, *details: object) -> None:
    if not condition:
        raise RuntimeError((label,) + details)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def capture_closure() -> tuple[bytes, str, str]:
    require(sys.flags.isolated and sys.flags.safe_path,
            "run with isolated Python (-I)", sys.flags)
    require(sys.flags.dont_write_bytecode, "run with -B", sys.flags)
    require(sys.flags.optimize == 0 and sys.flags.no_user_site,
            "unsafe Python flags", sys.flags)
    require(os.environ.get("LC_ALL") == "C", "LC_ALL must equal C")
    require(os.environ.get("PYTHONDONTWRITEBYTECODE") == "1",
            "PYTHONDONTWRITEBYTECODE must equal 1")
    require(not os.environ.get("PYTHONPYCACHEPREFIX"),
            "PYTHONPYCACHEPREFIX must be unset")
    require(not _RAW_SCRIPT_PATH.is_symlink(), "source symlink forbidden")
    require(SCRIPT_PATH.relative_to(WORKSPACE) == EXPECTED_RELATIVE,
            "unexpected source path", SCRIPT_PATH)
    mode = SCRIPT_PATH.stat().st_mode
    require(stat.S_ISREG(mode), "source is not a regular file")
    require(not mode & (stat.S_IWGRP | stat.S_IWOTH),
            "source is group/world writable", oct(mode))
    for item in sys.path:
        if item:
            resolved = Path(item).resolve()
            require(not (resolved == WORKSPACE or WORKSPACE in resolved.parents),
                    "repository appears on isolated sys.path", resolved)
    for candidate in (
        WORKSPACE / "flint", WORKSPACE / "flint.py",
        SCRIPT_PATH.parent / "flint", SCRIPT_PATH.parent / "flint.py",
    ):
        require(not candidate.exists(), "repository flint shadow", candidate)
    require("flint" not in sys.modules, "flint imported before closure capture")
    source = SCRIPT_PATH.read_bytes()
    source_sha = sha256_bytes(source)
    manifest = (f"{SCRIPT_PATH.relative_to(WORKSPACE)} {source_sha}\n").encode()
    return source, source_sha, sha256_bytes(manifest)


_SOURCE_BYTES, SOURCE_SHA256, CLOSURE_SHA256 = capture_closure()

import flint  # noqa: E402
from flint import arb, ctx  # noqa: E402

FLINT_ORIGIN = Path(flint.__file__).resolve()
require(not (FLINT_ORIGIN == WORKSPACE or WORKSPACE in FLINT_ORIGIN.parents),
        "repository flint shadow loaded", FLINT_ORIGIN)
require(sys.implementation.name == "cpython", "unexpected Python implementation",
        sys.implementation.name)
require(platform.python_version() == "3.12.13", "unexpected CPython",
        platform.python_version())
require(importlib.metadata.version("python-flint") == "0.9.0",
        "unexpected python-flint")
require(flint.__FLINT_VERSION__ == "3.6.0", "unexpected FLINT")
ctx.prec = BITS
require(ctx.prec == BITS, "could not set Arb precision")


def require_arb(value: arb, label: str) -> arb:
    require(isinstance(value, arb), "non-Arb value", label, type(value))
    require(value.is_finite(), "nonfinite Arb value", label, value)
    return value


def interval(value: arb) -> str:
    return require_arb(value, "serialization").str(
        DIGITS, radius=True, more=True
    )


def arb_fraction(value: Fraction) -> arb:
    return arb(value.numerator) / value.denominator


def certify_zero(value: arb, label: str) -> arb:
    require_arb(value, label)
    require(value.contains(0), "identity ball excludes zero", label, value)
    bound = abs(value).upper()
    ceiling = arb(2) ** -IDENTITY_EXPONENT
    require(bound.upper() < ceiling.lower(),
            "identity ball exceeds ceiling", label, value, ceiling)
    return bound


def certify_positive(value: arb, label: str) -> arb:
    require_arb(value, label)
    require(value > 0 and not value.contains(0),
            "positive sign false or unresolved", label, value)
    return value


def factorization(n: int) -> dict[int, int]:
    require(isinstance(n, int) and n >= 1, "bad factorization input", n)
    x = n
    factors: dict[int, int] = {}
    p = 2
    while p * p <= x:
        while x % p == 0:
            factors[p] = factors.get(p, 0) + 1
            x //= p
        p += 1
    if x > 1:
        factors[x] = factors.get(x, 0) + 1
    return factors


def trial_mu(n: int) -> int:
    factors = factorization(n)
    return 0 if any(e > 1 for e in factors.values()) else (-1) ** len(factors)


def linear_mu(limit: int) -> tuple[int, ...]:
    mu = [0] * (limit + 1)
    composite = [False] * (limit + 1)
    primes: list[int] = []
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
    return tuple(mu)


def prime_power_base(n: int) -> int | None:
    factors = factorization(n)
    return next(iter(factors)) if n >= 2 and len(factors) == 1 else None


def arb_sum(values) -> arb:
    answer = arb(0)
    for value in values:
        answer += value
    return answer


CELL_LOGS: list[arb] = []


def rho_rho_cell(q: int, d: int, k: int) -> arb:
    """Literal integral over [k,k+1] of rho_q rho_d dt/t^2."""
    fq, fd = k // q, k // d
    log_ratio = CELL_LOGS[k + 1]
    reciprocal_gap = arb(1) / k - arb(1) / (k + 1)
    return (
        arb(1) / (q * d)
        - (arb(fd) / q + arb(fq) / d) * log_ratio
        + arb(fq * fd) * reciprocal_gap
    )


def rho_chi_cell(q: int, k: int) -> arb:
    """Literal integral over [k,k+1] of rho_q dt/t^2."""
    fq = k // q
    return (
        CELL_LOGS[k + 1] / q
        - arb(fq) * (arb(1) / k - arb(1) / (k + 1))
    )


def det_leibniz(matrix: list[list[arb]]) -> arb:
    n = len(matrix)
    require(n and all(len(row) == n for row in matrix),
            "non-square determinant input")
    answer = arb(0)
    for permutation in permutations(range(n)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(n) for j in range(i + 1, n)
        )
        term = arb(-1 if inversions & 1 else 1)
        for i in range(n):
            term *= matrix[i][permutation[i]]
        answer += term
    return answer


def verify_closure_unchanged() -> None:
    require(ctx.prec == BITS, "Arb precision changed")
    require(SCRIPT_PATH.read_bytes() == _SOURCE_BYTES,
            "source mutated after capture")
    require(sha256_bytes(_SOURCE_BYTES) == SOURCE_SHA256,
            "captured source hash changed")


def main() -> None:
    global CELL_LOGS
    limit = M + 4
    mu_trial = (0,) + tuple(trial_mu(n) for n in range(1, limit + 1))
    mu = linear_mu(limit)
    require(mu == mu_trial, "independent Mobius tables disagree")
    for n in range(1, limit + 1):
        divisor_sum = sum(mu[d] for d in range(1, n + 1) if n % d == 0)
        require(divisor_sum == (1 if n == 1 else 0),
                "Mobius divisor convolution failed", n, divisor_sum)

    rows = tuple(q for q in range(A, 3 * A // 2 + 1) if mu[q] != 0)
    require(rows == ROWS, "unexpected closed physical row set", rows)
    require(tuple(q for q in rows if q in MINOR_ROWS) == MINOR_ROWS,
            "minor row order mismatch")

    logs = [arb(0)] + [arb(n).log() for n in range(1, limit + 2)]
    cell_logs = [arb(0)] * (limit + 2)
    for k in range(2, limit + 2):
        cell_logs[k] = (arb(k) / (k - 1)).log()
    CELL_LOGS = cell_logs
    Lambda = [arb(0)] * (limit + 1)
    for n in range(2, limit + 1):
        p = prime_power_base(n)
        if p is not None:
            Lambda[n] = logs[p]
        lambda_from_mu = -arb_sum(
            mu[d] * logs[d] for d in range(1, n + 1) if n % d == 0
        )
        certify_zero(lambda_from_mu - Lambda[n],
                     f"Lambda divisor identity n={n}")

    psi = [arb(0)] * (limit + 1)
    Cr = [arb(0)] * (limit + 2)
    mrec = [Fraction(0)] * (limit + 1)
    ell = [arb(0)] * (limit + 1)
    Pi = [arb(0)] * (limit + 1)
    for n in range(1, limit + 1):
        psi[n] = psi[n - 1] + Lambda[n]
        mrec[n] = mrec[n - 1] + Fraction(mu[n], n)
        ell[n] = ell[n - 1] + mu[n] * logs[n] / n
        Pi[n] = Pi[n - 1] + psi[n] / (n * (n + 1))
        if n >= 2:
            Cr[n] = Cr[n - 1] + psi[n - 1] * (logs[n] - logs[n - 1])

    C = 2 * (1 - arb_fraction(THETA))
    tau = C - 1
    cell_values: dict[int, arb] = {}
    residual_values: dict[int, arb] = {}
    path_error_sum = arb(0)

    for q in rows:
        B_cell = arb(0)
        B_residual = arb(0)
        for n in range(q, M + 1):
            L = logs[n]
            w = 1 - L / logs[n + 1]
            An = C - w
            certify_positive(w, f"w>0 q={q} n={n}")
            certify_positive(An, f"A_n>0 q={q} n={n}")
            eta = tau / An
            alpha = w * An * (logs[q] / L - eta)
            certify_positive(alpha, f"alpha>0 q={q} n={n}")

            # Independent literal fractional-part path. No psi, Pi, Cr,
            # mrec, ell, residual formula, or normal form enters this path.
            prefix_cell = -eta * arb_sum(
                rho_chi_cell(q, k) for k in range(1, n + 1)
            )
            for d in range(1, n + 1):
                if mu[d]:
                    P_qnd = arb_sum(
                        rho_rho_cell(q, d, k) for k in range(1, n + 1)
                    )
                    prefix_cell += (
                        mu[d] * (logs[d] / L - eta) * P_qnd
                    )
            B_cell += alpha * prefix_cell

            aqn = arb(n) / q - (arb(n + 1) / q).log()
            jqn = (arb(n + 1) / q).log() - (Pi[n] - Pi[q - 1])
            E = Cr[n + 1] - n
            residual = (
                E / q + jqn
                + aqn * (1 + ell[n] - eta * L * arb_fraction(mrec[n]))
            )
            B_residual += alpha * residual / L

        path_error_sum += certify_zero(
            B_cell - B_residual, f"cell/residual path q={q}"
        )
        cell_values[q] = B_cell
        residual_values[q] = B_residual

    def matrix(values: dict[int, arb]) -> list[list[arb]]:
        return [
            [arb(1), arb(q) / A, (arb(q) / A).log(), values[q]]
            for q in MINOR_ROWS
        ]

    determinants = {
        "cell": det_leibniz(matrix(cell_values)),
        "residual": det_leibniz(matrix(residual_values)),
    }
    for label, value in determinants.items():
        certify_positive(value, f"{label} determinant")
    path_error_sum += certify_zero(
        determinants["cell"] - determinants["residual"],
        "cell/residual determinant",
    )
    require(path_error_sum.upper() < (arb(2) ** -IDENTITY_EXPONENT).lower(),
            "summed path errors exceed ceiling", path_error_sum)

    # Exact-rational current-tail surrogate. For positive h_n, define
    # Gamma_m=(1/m)*sum_{n=m}^15 h_n. This has exactly the same positive,
    # strictly decreasing reciprocal-tail shape as the Cycle 52 current
    # transform, but is not asserted to come from a physical row test.
    packet: dict[int, Fraction] = {
        m: sum((PACKET_INPUT[n] for n in range(m, 16)), Fraction(0)) / m
        for m in PACKET_RANGE
    }
    packet_expected = {
        8: Fraction(10013, 8148), 9: Fraction(17989, 18333),
        10: Fraction(7976, 10185), 11: Fraction(1265, 2037),
        12: Fraction(5939, 12222), 13: Fraction(757, 2037),
        14: Fraction(1, 7), 15: Fraction(1, 15),
    }
    require(all(PACKET_INPUT[n] > 0 for n in PACKET_RANGE),
            "packet input is not positive", PACKET_INPUT)
    require(packet == packet_expected, "packet values changed", packet)
    packet_differences = {
        m: packet[m] - packet[m + 1] for m in range(8, 15)
    }
    require(all(packet[m] > packet[m + 1] > 0 for m in range(8, 15)),
            "packet is not positive and strictly decreasing", packet)
    require(packet[15] > 0, "terminal packet value is not positive")
    mobius_contraction = sum(
        (mu[m] * packet[m] for m in PACKET_RANGE), Fraction(0)
    )
    require(mobius_contraction == 0,
            "packet Mobius contraction is nonzero", mobius_contraction)
    reciprocal_prefix = {
        n: sum((Fraction(mu[m], m) for m in range(8, n + 1)), Fraction(0))
        for n in PACKET_RANGE
    }
    abel_contraction = sum(
        (PACKET_INPUT[n] * reciprocal_prefix[n] for n in PACKET_RANGE),
        Fraction(0),
    )
    require(abel_contraction == mobius_contraction == 0,
            "packet Abel identity failed", abel_contraction,
            mobius_contraction)
    require(reciprocal_prefix[13] == Fraction(-97, 1430),
            "unexpected reciprocal prefix at 13", reciprocal_prefix[13])
    other_terms = sum(
        (PACKET_INPUT[n] * reciprocal_prefix[n]
         for n in PACKET_RANGE if n != 13),
        Fraction(0),
    )
    exceptional_term = PACKET_INPUT[13] * reciprocal_prefix[13]
    require(other_terms == Fraction(5767, 30030),
            "unexpected nonexceptional Abel sum", other_terms)
    require(exceptional_term == -Fraction(5767, 30030),
            "unexpected exceptional Abel term", exceptional_term)

    verify_closure_unchanged()

    print("certificate=cycle52-a10-cell-nonclosure")
    print("canonical_command=rm -f /tmp/cycle52-a10-cell-nonclosure-certificate.out && env -u PYTHONPYCACHEPREFIX PYTHONDONTWRITEBYTECODE=1 LC_ALL=C uv run --isolated --no-project --python 3.12.13 --with python-flint==0.9.0 python -I -B millennium-prize/riemann-hypothesis/cycle52_a10_cell_nonclosure_certificate.py > /tmp/cycle52-a10-cell-nonclosure-certificate.out && cmp /tmp/cycle52-a10-cell-nonclosure-certificate.out millennium-prize/riemann-hypothesis/cycle52-a10-cell-nonclosure-certificate.out")
    print("scope=finite theta=2/5 a=10 certificate only; no asymptotic or RH inference")
    print("runtime=CPython-3.12.13 python-flint-0.9.0 FLINT-3.6.0 Arb_bits=256")
    print(f"source={SCRIPT_PATH.relative_to(WORKSPACE)}")
    print(f"source_sha256={SOURCE_SHA256}")
    print(f"closure_sha256={CLOSURE_SHA256}")
    print("trusted_runtime_boundary=versions pinned; interpreter/wheel/native-library binaries, OS, hardware, and uv launcher not binary-attested")
    print(f"identity_error_ceiling=2^-{IDENTITY_EXPONENT}")
    print("parameters=theta=2/5 C=6/5 tau=1/5 a=10 M=19")
    print("rows=[10,11,13,14,15]")
    print("minor_rows=[10,11,14,15]")
    print("columns=[1,q/10,log(q/10),B_10(q)]")
    print("B_cell_path=literal sum of direct fractional-part integrals over every [k,k+1], 1<=k<=n")
    for q in rows:
        print(f"B_cell[{q}]={interval(cell_values[q])}")
        print(f"B_residual[{q}]={interval(residual_values[q])}")
        print(f"cell_minus_residual[{q}]={interval(cell_values[q]-residual_values[q])}")
    for label in ("cell", "residual"):
        print(f"det_{label}={interval(determinants[label])}")
    print("det_cell_minus_residual=" + interval(
        determinants["cell"] - determinants["residual"]
    ))
    print("certified_minor_sign=positive")
    print("reciprocal_tail_input=" + ",".join(
        f"{m}:{PACKET_INPUT[m]}" for m in PACKET_RANGE
    ))
    print("reciprocal_tail_packet=" + ",".join(
        f"{m}:{packet[m]}" for m in PACKET_RANGE
    ))
    print("reciprocal_tail_differences=" + ",".join(
        f"{m}:{packet_differences[m]}" for m in range(8, 15)
    ))
    print("packet_properties=exact_rational positive strictly_decreasing")
    print("packet_mobius_contraction=0")
    print(f"packet_abel_other_terms={other_terms}")
    print(f"packet_abel_exceptional_term={exceptional_term}")
    print("packet_scope=abstract current-tail surrogate; no physical row-test realization claimed")
    print("conclusion=B_10_not_in_span{1,q/10,log(q/10)}_on_declared_five_rows")
    print("result=PASS")


if __name__ == "__main__":
    main()
