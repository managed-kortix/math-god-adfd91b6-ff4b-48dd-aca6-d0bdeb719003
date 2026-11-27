#!/usr/bin/env python3
"""Standalone fail-closed certificate for a compatible floor-gauge obstruction.

At theta=2/5, this 192-bit Arb certificate:

* reconstructs the physical prefix, tail, and full contractions directly from
  Z_n=-eta_n chi+sum_{d<=n} mu(d)b_d(n)rho_d;
* reconstructs the same three vectors from one compatible floor gauge, using
  sum_{d<=n}mu(d)floor(n/d)=1;
* checks both paths at a=3 and a=8; and
* proves at a=3 that the d=3,5 principal minor of the symmetrized
  prefix/full coefficient kernel is negative.

The fractional-part functions are rho_d(t)={t/d} on [1,infinity), the Hilbert
weight is dt/t^2, and every temporal sum ends at M=2a-1.  The restricted Gram
entry is computed as the full Vasyunin entry minus exactly 1/(qd).

This finite certificate proves no sign for a selected Mobius quadratic form at
other scales, no asymptotic estimate, and no consequence for RH.
"""

from __future__ import annotations

# Capture the local closure before the first third-party import.
import hashlib
import os
import platform
import stat
import sys
from fractions import Fraction
from math import gcd
from pathlib import Path

BITS = 192
DIGITS = 48
SCALES = (3, 8)
THETA = Fraction(2, 5)
OBSTRUCTION_SCALE = 3
OBSTRUCTION_ROW = 3
OBSTRUCTION_COLUMNS = (3, 5)
IDENTITY_EXPONENT = BITS // 2

_RAW_SCRIPT_PATH = Path(__file__)
SCRIPT_PATH = _RAW_SCRIPT_PATH.resolve()
RH_DIR = SCRIPT_PATH.parent
WORKSPACE = RH_DIR.parent.parent

REQUIRED_RUNTIME = {
    "python": "3.12.13",
    "python_flint": "0.9.0",
    "flint": "3.6.0",
}


def require(condition: bool, label: str, *details: object) -> None:
    if not condition:
        raise RuntimeError((label,) + details)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def capture_closure() -> tuple[str, str]:
    require(sys.flags.isolated and sys.flags.safe_path,
            "run with isolated Python (-I)", sys.flags)
    require(sys.flags.dont_write_bytecode,
            "run with bytecode disabled (-B)", sys.flags)
    require(sys.flags.optimize == 0 and sys.flags.no_user_site,
            "unsafe Python flags", sys.flags)
    require(os.environ.get("LC_ALL") == "C", "LC_ALL must equal C")
    require(not os.environ.get("PYTHONPYCACHEPREFIX"),
            "PYTHONPYCACHEPREFIX must be unset")
    require(os.environ.get("PYTHONDONTWRITEBYTECODE") == "1",
            "PYTHONDONTWRITEBYTECODE must equal 1")
    require(not _RAW_SCRIPT_PATH.is_symlink(), "source symlink is forbidden")
    require(SCRIPT_PATH.name == "cycle50_floor_gauge_obstruction.py",
            "unexpected certificate filename", SCRIPT_PATH)
    mode = SCRIPT_PATH.stat().st_mode
    require(stat.S_ISREG(mode), "certificate source is not regular")
    require(not (mode & (stat.S_IWGRP | stat.S_IWOTH)),
            "certificate source is group/world writable", oct(mode))
    for item in sys.path:
        if not item:
            continue
        resolved = Path(item).resolve()
        require(not (resolved == WORKSPACE or WORKSPACE in resolved.parents),
                "repository appears on isolated sys.path", resolved)
    for candidate in (
        WORKSPACE / "flint", WORKSPACE / "flint.py",
        RH_DIR / "flint", RH_DIR / "flint.py",
    ):
        require(not candidate.exists(), "repository flint shadow", candidate)
    require("flint" not in sys.modules,
            "flint imported before closure capture")
    script_sha = sha256_bytes(SCRIPT_PATH.read_bytes())
    manifest = (
        f"{SCRIPT_PATH.relative_to(WORKSPACE)} {script_sha}\n"
    ).encode("ascii")
    return script_sha, sha256_bytes(manifest)


SCRIPT_SHA256, CLOSURE_SHA256 = capture_closure()

import flint  # noqa: E402
from flint import arb, ctx  # noqa: E402

FLINT_ORIGIN = Path(flint.__file__).resolve()
require(not (FLINT_ORIGIN == WORKSPACE or WORKSPACE in FLINT_ORIGIN.parents),
        "repository flint shadow loaded", FLINT_ORIGIN)
require(platform.python_version() == REQUIRED_RUNTIME["python"],
        "Python version mismatch", platform.python_version())
require(flint.__version__ == REQUIRED_RUNTIME["python_flint"],
        "python-flint version mismatch", flint.__version__)
require(flint.__FLINT_VERSION__ == REQUIRED_RUNTIME["flint"],
        "FLINT version mismatch", flint.__FLINT_VERSION__)
ctx.prec = BITS
require(ctx.prec == BITS, "cannot set requested Arb precision", ctx.prec)


def require_arb(value: arb, label: str) -> arb:
    require(isinstance(value, arb), "value is not Arb", label, type(value))
    require(value.is_finite(), "nonfinite Arb value", label, value)
    return value


def interval(value: arb) -> str:
    return require_arb(value, "serialized interval").str(
        DIGITS, radius=True, more=True
    )


def arb_fraction(value: Fraction) -> arb:
    return arb(value.numerator) / value.denominator


def certify_zero(value: arb, label: str) -> arb:
    require_arb(value, label)
    require(value.contains(0), "identity ball excludes zero", label, value)
    upper = require_arb(abs(value).upper(), label + " absolute upper")
    ceiling = arb(2) ** (-IDENTITY_EXPONENT)
    require(upper.upper() <= ceiling.lower(),
            "identity ball exceeds fail-closed ceiling", label, value, ceiling)
    return upper


def certify_positive(value: arb, label: str) -> arb:
    require_arb(value, label)
    require(value > 0, "positive sign false or unresolved", label, value)
    return value


def certify_negative(value: arb, label: str) -> arb:
    require_arb(value, label)
    require(value < 0, "negative sign false or unresolved", label, value)
    return value


def mobius(n: int) -> int:
    require(isinstance(n, int) and n >= 1, "invalid Mobius argument", n)
    remaining = n
    result = 1
    prime = 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            remaining //= prime
            result = -result
            if remaining % prime == 0:
                return 0
            while remaining % prime == 0:
                remaining //= prime
        prime += 1
    if remaining > 1:
        result = -result
    return result


class RestrictedGram:
    """Exact-formula Arb evaluator of <rho_a,rho_b> on [1,infinity)."""

    def __init__(self) -> None:
        self.pi = arb.pi()
        self.c0 = (2 * self.pi).log() - arb.const_euler()
        self._cotangent_rows: dict[int, tuple[arb, ...]] = {}
        self._vasyunin: dict[tuple[int, int], arb] = {}
        self._entries: dict[tuple[int, int], arb] = {}

    def vasyunin(self, p: int, q: int) -> arb:
        if q == 1:
            return arb(0)
        p %= q
        sign = 1
        if p > q // 2:
            p = q - p
            sign = -1
        key = (p, q)
        if key not in self._vasyunin:
            if q not in self._cotangent_rows:
                self._cotangent_rows[q] = tuple(
                    (self.pi * k / q).cot() / q for k in range(1, q)
                )
            row = self._cotangent_rows[q]
            self._vasyunin[key] = sum(
                (arb((k * p) % q) * row[k - 1] for k in range(1, q)),
                arb(0),
            )
        return sign * self._vasyunin[key]

    def entry(self, a: int, b: int) -> arb:
        require(a >= 1 and b >= 1, "invalid Gram indices", a, b)
        key = (min(a, b), max(a, b))
        if key in self._entries:
            return self._entries[key]
        divisor = gcd(a, b)
        p, q = key[0] // divisor, key[1] // divisor
        lcm = key[0] * key[1] // divisor
        full = (
            arb(q - p) * (arb(p) / q).log()
            + arb(p + q) * self.c0
            - self.pi * (self.vasyunin(p, q) + self.vasyunin(q, p))
        ) / (2 * lcm)
        restricted = full - arb(1) / (a * b)
        self._entries[key] = restricted
        return restricted

    @staticmethod
    def chi_cross(q: int) -> arb:
        return (arb(q).log() + 1 - arb.const_euler()) / q


class Scale:
    def __init__(self, a: int) -> None:
        self.a = a
        self.stop = 2 * a
        self.maximum = self.stop - 1
        self.mu = [0] + [mobius(n) for n in range(1, self.stop + 1)]
        self.logs = [arb(0)] + [arb(n).log() for n in range(1, self.stop + 2)]
        self.squarefree = tuple(
            d for d in range(1, self.stop) if self.mu[d] != 0
        )
        self.rows = tuple(
            q for q in range(a, 3 * a // 2 + 1) if self.mu[q] != 0
        )
        require(self.rows, "empty physical row set", a)
        self.theta = arb_fraction(THETA)
        self.tau = 1 - 2 * self.theta
        self.gram = RestrictedGram()
        self.eta: dict[int, arb] = {}
        self.kappa: dict[int, arb] = {}
        for n in range(a, self.stop):
            ratio = self.logs[n] / self.logs[n + 1]
            w = 1 - ratio
            A = 1 + ratio - 2 * self.theta
            certify_positive(A, f"A_n a={a} n={n}")
            self.eta[n] = self.tau / A
            self.kappa[n] = w * A

    def b(self, d: int, n: int) -> arb:
        return self.logs[d] / self.logs[n] - self.eta[n]

    def alpha(self, q: int, n: int) -> arb:
        return self.kappa[n] * self.b(q, n)


def prefix_cell(q: int, d: int, n: int) -> arb:
    """Literal integral of rho_q rho_d over [1,n+1], cell by cell."""
    total = arb(0)
    for k in range(1, n + 1):
        fq = k // q
        fd = k // d
        log_ratio = (arb(k + 1) / k).log()
        reciprocal_gap = arb(1) / k - arb(1) / (k + 1)
        total += (
            arb(1) / (q * d)
            - (arb(fd) / q + arb(fq) / d) * log_ratio
            + arb(fq * fd) * reciprocal_gap
        )
    return total


def affine_prefix(q: int, n: int) -> arb:
    """Literal integral of rho_q chi over [1,n+1], checked cellwise."""
    cells = arb(0)
    for k in range(1, n + 1):
        fq = k // q
        cells += (
            arb(1) / q * (arb(k + 1) / k).log()
            - arb(fq) * (arb(1) / k - arb(1) / (k + 1))
        )
    # Here q<=n<2q for every physical row and temporal index used below.
    closed = (arb(n + 1).log() - 1) / q + arb(1) / (n + 1)
    certify_zero(cells - closed, f"affine-prefix cells q={q} n={n}")
    return cells


def divisor_identity(scale: Scale, n: int) -> None:
    value = sum(scale.mu[d] * (n // d) for d in range(1, n + 1))
    require(value == 1, "Mobius floor identity failed", scale.a, n, value)


def floor_columns(scale: Scale, q: int, d: int) -> tuple[arb, arb, arb]:
    """Return prefix, tail, and full columns in one compatible floor gauge.

      W_B^F(q,d)=sum_n alpha [b_d(n)P_n(q,d)
                         -eta_n floor(n/d)P_n(q,0)],
      W_H^F(q,d)=sum_n alpha [b_d(n)T_n(q,d)
                         -eta_n floor(n/d)T_n(q,0)],
      W_C^F(q,d)=sum_n alpha [b_d(n)G(q,d)
                         -eta_n floor(n/d)g_q].

    Every sum begins at n=max(q,d) and ends at 2a-1.
    """
    wb = arb(0)
    wh = arb(0)
    wc = arb(0)
    gq = scale.gram.chi_cross(q)
    for n in range(max(q, d), scale.stop):
        alpha = scale.alpha(q, n)
        p = prefix_cell(q, d, n)
        p0 = affine_prefix(q, n)
        g = scale.gram.entry(q, d)
        t = g - p
        t0 = gq - p0
        count = n // d
        bdn = scale.b(d, n)
        wb += alpha * (bdn * p - scale.eta[n] * count * p0)
        wh += alpha * (bdn * t - scale.eta[n] * count * t0)
        wc += alpha * (bdn * g - scale.eta[n] * count * gq)
    certify_zero(wb + wh - wc,
                 f"column prefix+tail=full a={scale.a} q={q} d={d}")
    return wb, wh, wc


def direct_temporal(scale: Scale, q: int) -> tuple[arb, arb, arb]:
    """Reconstruct prefix, tail, full directly from the original Z_n."""
    direct_b = arb(0)
    direct_h = arb(0)
    direct_c = arb(0)
    gq = scale.gram.chi_cross(q)
    for n in range(q, scale.stop):
        p0 = affine_prefix(q, n)
        prefix = -scale.eta[n] * p0
        tail = -scale.eta[n] * (gq - p0)
        full = -scale.eta[n] * gq
        for d in scale.squarefree:
            if d > n:
                break
            coefficient = scale.mu[d] * scale.b(d, n)
            p = prefix_cell(q, d, n)
            g = scale.gram.entry(q, d)
            prefix += coefficient * p
            tail += coefficient * (g - p)
            full += coefficient * g
        alpha = scale.alpha(q, n)
        direct_b += alpha * prefix
        direct_h += alpha * tail
        direct_c += alpha * full
    certify_zero(direct_b + direct_h - direct_c,
                 f"direct temporal recombination a={scale.a} q={q}")
    return direct_b, direct_h, direct_c


def certify_scale(a: int) -> tuple[Scale, dict[tuple[int, int], tuple[arb, arb, arb]]]:
    scale = Scale(a)
    for n in range(a, scale.stop):
        divisor_identity(scale, n)
    columns: dict[tuple[int, int], tuple[arb, arb, arb]] = {}
    maximum_residual = arb(0)
    for q in scale.rows:
        selected_b = arb(0)
        selected_h = arb(0)
        selected_c = arb(0)
        for d in scale.squarefree:
            packet = floor_columns(scale, q, d)
            columns[q, d] = packet
            mu = scale.mu[d]
            selected_b += mu * packet[0]
            selected_h += mu * packet[1]
            selected_c += mu * packet[2]
        direct_b, direct_h, direct_c = direct_temporal(scale, q)
        residuals = (
            selected_b - direct_b,
            selected_h - direct_h,
            selected_c - direct_c,
            selected_b + selected_h - selected_c,
        )
        labels = ("prefix", "tail", "full", "selected recombination")
        for label, residual in zip(labels, residuals, strict=True):
            error = certify_zero(residual, f"{label} identity a={a} q={q}")
            if error > maximum_residual:
                maximum_residual = error
    print(
        f"scale={a} rows={','.join(map(str, scale.rows))} "
        f"columns={len(scale.squarefree)} "
        f"max_identity_residual={interval(maximum_residual)}"
    )
    return scale, columns


def certify_obstruction(scale: Scale, columns) -> None:
    require(scale.a == OBSTRUCTION_SCALE, "wrong obstruction scale")
    require(scale.rows == (OBSTRUCTION_ROW,), "obstruction row set changed",
            scale.rows)
    q = OBSTRUCTION_ROW
    d1, d2 = OBSTRUCTION_COLUMNS
    b1, _, c1 = columns[q, d1]
    b2, _, c2 = columns[q, d2]
    wedge = b1 * c2 - b2 * c1
    determinant = -(wedge * wedge) / 4
    certify_negative(wedge, "two-column prefix/full wedge")
    certify_negative(determinant, "symmetrized cross-kernel determinant")
    direct_determinant = (
        (b1 * c1) * (b2 * c2)
        - ((b1 * c2 + b2 * c1) / 2) ** 2
    )
    certify_zero(direct_determinant - determinant,
                 "principal determinant algebra")
    print(f"obstruction_scale={scale.a} row={q} columns={d1},{d2}")
    print(f"b_{d1}={interval(b1)}")
    print(f"c_{d1}={interval(c1)}")
    print(f"b_{d2}={interval(b2)}")
    print(f"c_{d2}={interval(c2)}")
    print(f"wedge={interval(wedge)}")
    print(f"principal_determinant={interval(determinant)}")


def main() -> None:
    print("certificate=cycle50-compatible-floor-gauge-obstruction")
    print("canonical_command=rm -f /tmp/cycle50-floor-gauge-obstruction.out && env -u PYTHONPYCACHEPREFIX PYTHONDONTWRITEBYTECODE=1 LC_ALL=C uv run --isolated --no-project --python 3.12.13 --with python-flint==0.9.0 python -I -B millennium-prize/riemann-hypothesis/cycle50_floor_gauge_obstruction.py > /tmp/cycle50-floor-gauge-obstruction.out && cmp /tmp/cycle50-floor-gauge-obstruction.out millennium-prize/riemann-hypothesis/cycle50-floor-gauge-obstruction.out")
    print(f"precision_bits={BITS}")
    print(
        "runtime="
        f"CPython-{platform.python_version()} "
        f"python-flint-{flint.__version__} FLINT-{flint.__FLINT_VERSION__}"
    )
    print(f"script_sha256={SCRIPT_SHA256}")
    print(f"closure_sha256={CLOSURE_SHA256}")
    print("theta=2/5")
    print("gauge=single compatible floor gauge")
    print("restricted_gram=full Vasyunin minus exact 1/(qd)")
    print("domains=physical squarefree rows x squarefree columns 1<=d<=2a-1")
    obstruction_scale = None
    obstruction_columns = None
    for a in SCALES:
        scale, columns = certify_scale(a)
        if a == OBSTRUCTION_SCALE:
            obstruction_scale = scale
            obstruction_columns = columns
    require(obstruction_scale is not None and obstruction_columns is not None,
            "obstruction scale was not evaluated")
    certify_obstruction(obstruction_scale, obstruction_columns)
    print("scope=finite exact identities and interval-certified obstruction only")
    print("result=PASS")


if __name__ == "__main__":
    main()
