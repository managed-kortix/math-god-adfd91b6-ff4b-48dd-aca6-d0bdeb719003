#!/usr/bin/env python3
"""Standalone fail-closed certificate for the compatible Cycle 50 delta gauge.

At theta=2/5, a=3, M=2a-1=5, and physical row q=3, this 256-bit
Arb certificate independently assembles the exact finite compatible gauges

    W_B(q,d) = sum_{n=max(q,d)}^M alpha(q,n)
        [(log(d)/log(n)) P(q,n,d) - eta(n) a(q,n)/d],

    W_C^delta(q,d) = sum_{n=max(q,d)}^M alpha(q,n)
        [(log(d)/log(n)-eta(n)) G(q,d)
         - eta(n) 1_{d=1} g(q)],

where P is the [1,n+1] prefix cell integral, G is the complete restricted
fractional-part Gram entry (full Vasyunin minus exactly 1/(qd)), g is the
complete affine cross term, and every temporal sum includes n=M=5.

The certificate checks the finite cumulative-floor collapse that produces W_B,
checks W_C^delta against the original full contraction after the affine source
is moved into d=1, checks W_C^delta-W_B against the exact tail formula, retains
all columns d=1,...,5 in the selected Mobius contractions, and certifies both:

* the negative d=3,5 principal determinant of sym(W_B^T W_C^delta); and
* the positive physical selected contraction B*C.

This is a finite certificate only. It proves no asymptotic statement, no
eventual physical sign, and no consequence for the Riemann hypothesis.
"""

from __future__ import annotations

# Capture and validate the local closure before the first third-party import.
import hashlib
import os
import platform
import stat
import sys
from fractions import Fraction
from math import gcd
from pathlib import Path

BITS = 256
DIGITS = 64
IDENTITY_EXPONENT = BITS // 2
THETA = Fraction(2, 5)
A = 3
M = 2 * A - 1
Q = 3
CURRENT_COLUMNS = (3, 5)
ALL_COLUMNS = tuple(range(1, M + 1))
DIRECT_GRAM_CELLS = 100_000

_RAW_SCRIPT_PATH = Path(__file__)
SCRIPT_PATH = _RAW_SCRIPT_PATH.resolve()
RH_DIR = SCRIPT_PATH.parent
WORKSPACE = RH_DIR.parent.parent
SHADOW_NAMES = (
    "fractions", "hashlib", "math", "os", "pathlib", "platform", "stat",
    "sys", "flint",
)
REQUIRED_RUNTIME = {
    "python": "3.12.13",
    "python_flint": "0.9.0",
    "flint": "3.6.0",
}


def fail(label: str, *details: object) -> None:
    raise RuntimeError((label,) + details)


def require(condition: bool, label: str, *details: object) -> None:
    if not condition:
        fail(label, *details)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_regular_file(path: Path) -> None:
    metadata = path.stat()
    mode = metadata.st_mode
    require(stat.S_ISREG(mode), "closure member is not a regular file", path)
    require(metadata.st_nlink == 1, "closure member has multiple hard links",
            path, metadata.st_nlink)
    require(not (mode & (stat.S_IWGRP | stat.S_IWOTH)),
            "closure member is group/world writable", path, oct(mode))


def reject_repository_import_artifacts() -> None:
    for item in sys.path:
        if not item:
            continue
        resolved = Path(item).resolve()
        require(not (resolved == WORKSPACE or WORKSPACE in resolved.parents),
                "repository appears on isolated sys.path", resolved)

    for root in (RH_DIR, RH_DIR.parent, WORKSPACE):
        for name in SHADOW_NAMES:
            for candidate in (
                root / name,
                root / f"{name}.py",
                root / f"{name}.pyc",
                root / f"{name}.pyo",
            ):
                require(not candidate.exists(),
                        "competing repository import shadow", candidate)
            for suffix in (".so", ".pyd", ".dll", ".dylib"):
                matches = tuple(root.glob(f"{name}*{suffix}"))
                require(not matches, "competing repository extension shadow",
                        matches)

    caches = tuple(RH_DIR.rglob("__pycache__"))
    bytecode = tuple(RH_DIR.rglob("*.pyc")) + tuple(RH_DIR.rglob("*.pyo"))
    require(not caches, "repository __pycache__ is forbidden", caches)
    require(not bytecode, "repository bytecode is forbidden", bytecode)


def capture_closure() -> tuple[bytes, str, str]:
    require(sys.flags.isolated and sys.flags.safe_path,
            "run with isolated Python (-I)", sys.flags)
    require(sys.flags.dont_write_bytecode,
            "run with bytecode disabled (-B)", sys.flags)
    require(sys.flags.optimize == 0, "optimized Python is forbidden", sys.flags)
    require(sys.flags.no_user_site, "user site must be disabled", sys.flags)
    require(os.environ.get("LC_ALL") == "C", "LC_ALL must equal C")
    require(os.environ.get("PYTHONDONTWRITEBYTECODE") == "1",
            "PYTHONDONTWRITEBYTECODE must equal 1")
    require(not os.environ.get("PYTHONPYCACHEPREFIX"),
            "PYTHONPYCACHEPREFIX must be unset")
    require(not _RAW_SCRIPT_PATH.is_symlink(),
            "certificate source symlink is forbidden", _RAW_SCRIPT_PATH)
    require(SCRIPT_PATH.name == "cycle50_delta_gauge_obstruction.py",
            "unexpected certificate filename", SCRIPT_PATH)
    safe_regular_file(SCRIPT_PATH)
    reject_repository_import_artifacts()
    require("flint" not in sys.modules,
            "flint imported before closure capture")
    script_bytes = SCRIPT_PATH.read_bytes()
    script_sha = sha256_bytes(script_bytes)
    manifest = (
        f"{SCRIPT_PATH.relative_to(WORKSPACE)} {script_sha}\n"
    ).encode("ascii")
    return script_bytes, script_sha, sha256_bytes(manifest)


_SCRIPT_BYTES, SCRIPT_SHA256, CLOSURE_SHA256 = capture_closure()

# First third-party import. The repository is absent from the isolated path.
import flint  # noqa: E402
from flint import arb, ctx  # noqa: E402

FLINT_ORIGIN = Path(flint.__file__).resolve()
require(not (FLINT_ORIGIN == WORKSPACE or WORKSPACE in FLINT_ORIGIN.parents),
        "repository flint shadow loaded", FLINT_ORIGIN)


def verify_runtime() -> None:
    observed = {
        "python": platform.python_version(),
        "python_flint": flint.__version__,
        "flint": flint.__FLINT_VERSION__,
    }
    require(sys.implementation.name == "cpython",
            "unexpected Python implementation", sys.implementation.name)
    require(observed == REQUIRED_RUNTIME, "runtime version mismatch", observed,
            REQUIRED_RUNTIME)
    require(sys.flags.isolated and sys.flags.safe_path,
            "Python isolation flags changed", sys.flags)
    require(sys.flags.dont_write_bytecode and sys.flags.optimize == 0,
            "Python bytecode/optimization flags changed", sys.flags)
    require(os.environ.get("LC_ALL") == "C", "LC_ALL changed after startup")
    require(os.environ.get("PYTHONDONTWRITEBYTECODE") == "1",
            "PYTHONDONTWRITEBYTECODE changed after startup")
    require(not os.environ.get("PYTHONPYCACHEPREFIX"),
            "PYTHONPYCACHEPREFIX changed after startup")
    for name, module in tuple(sys.modules.items()):
        if name != "flint" and not name.startswith("flint."):
            continue
        origin = getattr(module, "__file__", None)
        if origin is None:
            continue
        resolved = Path(origin).resolve()
        require(not (resolved == WORKSPACE or WORKSPACE in resolved.parents),
                "repository flint component loaded", name, resolved)


verify_runtime()
ctx.prec = BITS
require(ctx.prec == BITS, "cannot set requested Arb precision", ctx.prec, BITS)


def require_arb(value: arb, label: str) -> arb:
    require(isinstance(value, arb), "value is not Arb", label, type(value))
    require(value.is_finite(), "nonfinite Arb value", label, value)
    return value


def interval(value: arb, digits: int = DIGITS) -> str:
    return require_arb(value, "serialized interval").str(
        digits, radius=True, more=True
    )


def arb_sum(values) -> arb:
    return sum(values, arb(0))


def arb_fraction(value: Fraction) -> arb:
    return arb(value.numerator) / value.denominator


def identity_ceiling() -> arb:
    return arb(2) ** (-IDENTITY_EXPONENT)


def certify_zero(value: arb, label: str) -> arb:
    require_arb(value, label)
    require(value.contains(0), "identity ball excludes zero", label, value)
    upper = require_arb(abs(value).upper(), label + " absolute upper")
    ceiling = identity_ceiling()
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


def factorization(n: int) -> dict[int, int]:
    require(isinstance(n, int) and n >= 1, "invalid factorization input", n)
    factors: dict[int, int] = {}
    remaining = n
    prime = 2
    while prime * prime <= remaining:
        while remaining % prime == 0:
            factors[prime] = factors.get(prime, 0) + 1
            remaining //= prime
        prime += 1
    if remaining > 1:
        factors[remaining] = factors.get(remaining, 0) + 1
    return factors


def mobius_factorization(n: int) -> int:
    factors = factorization(n)
    if any(exponent > 1 for exponent in factors.values()):
        return 0
    return -1 if len(factors) % 2 else 1


def mobius_divisor_recurrence(limit: int) -> tuple[int, ...]:
    mu = [0] * (limit + 1)
    mu[1] = 1
    for n in range(2, limit + 1):
        mu[n] = -sum(mu[d] for d in range(1, n) if n % d == 0)
    return tuple(mu)


def certify_integer_arithmetic() -> tuple[int, ...]:
    mu = mobius_divisor_recurrence(M)
    require(mu[1:] == tuple(mobius_factorization(n) for n in ALL_COLUMNS),
            "independent Mobius constructions disagree", mu)
    require(mu[1:] == (1, -1, -1, 0, -1),
            "unexpected Mobius table", mu)
    for k in ALL_COLUMNS:
        cumulative = sum(mu[d] * (k // d) for d in range(1, k + 1))
        require(cumulative == 1, "cumulative floor identity failed", k,
                cumulative)
        divisor = sum(mu[d] for d in range(1, k + 1) if k % d == 0)
        require(divisor == (1 if k == 1 else 0),
                "divisor Mobius identity failed", k, divisor)
    return mu


class RestrictedGram:
    """Evaluate <rho_a,rho_b> on [1,infinity) by Vasyunin formula."""

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
            self._vasyunin[key] = arb_sum(
                arb((k * p) % q) * row[k - 1] for k in range(1, q)
            )
        return sign * self._vasyunin[key]

    def entry(self, a: int, b: int) -> arb:
        require(isinstance(a, int) and isinstance(b, int) and a >= 1 and b >= 1,
                "invalid Gram indices", a, b)
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


def reciprocal_cell_prefix(q: int, d: int, cells: int) -> arb:
    """Literal integral of rho_q*rho_d over [1,cells+1]."""
    total = arb(0)
    for k in range(1, cells + 1):
        floor_q = k // q
        floor_d = k // d
        log_ratio = (arb(k + 1) / k).log()
        reciprocal_gap = arb(1) / k - arb(1) / (k + 1)
        total += (
            arb(1) / (q * d)
            - (arb(floor_d) / q + arb(floor_q) / d) * log_ratio
            + arb(floor_q * floor_d) * reciprocal_gap
        )
    return total


def certify_gram_brackets(gram: RestrictedGram) -> None:
    tail = arb(1) / (DIRECT_GRAM_CELLS + 1)
    for d in ALL_COLUMNS:
        prefix = reciprocal_cell_prefix(Q, d, DIRECT_GRAM_CELLS)
        value = gram.entry(Q, d)
        upper = prefix + tail
        require(prefix.upper() <= value.lower(),
                "direct Gram lower bracket failed", Q, d, prefix, value)
        require(value.upper() <= upper.lower(),
                "direct Gram upper bracket failed", Q, d, value, upper)


def prefix_cell(q: int, d: int, n: int) -> arb:
    """Literal integral of rho_q*rho_d over [1,n+1], cell by cell."""
    require(1 <= d <= n, "prefix cell column exceeds temporal endpoint", d, n)
    return reciprocal_cell_prefix(q, d, n)


def affine_prefix(q: int, n: int) -> arb:
    """Literal integral of rho_q*chi over [1,n+1], checked in closed form."""
    require(q <= n < 2 * q, "affine closed form outside one-reset range", q, n)
    cells = arb(0)
    for k in range(1, n + 1):
        floor_q = k // q
        cells += (
            arb(1) / q * (arb(k + 1) / k).log()
            - arb(floor_q) * (arb(1) / k - arb(1) / (k + 1))
        )
    closed = (arb(n + 1).log() - 1) / q + arb(1) / (n + 1)
    certify_zero(cells - closed, f"affine-prefix cells q={q} n={n}")
    return cells


def aterm(q: int, n: int) -> arb:
    require(q <= n < 2 * q, "aterm outside one-reset range", q, n)
    return arb(n) / q - (arb(n + 1) / q).log()


class FiniteScale:
    def __init__(self) -> None:
        self.theta = arb_fraction(THETA)
        self.tau = 1 - 2 * self.theta
        self.logs = [arb(0)] + [arb(n).log() for n in range(1, M + 2)]
        self.mu = certify_integer_arithmetic()
        self.gram = RestrictedGram()
        self.eta: dict[int, arb] = {}
        self.kappa: dict[int, arb] = {}
        for n in range(A, M + 1):
            ratio = self.logs[n] / self.logs[n + 1]
            weight = 1 - ratio
            factor = 1 + ratio - 2 * self.theta
            certify_positive(factor, f"A_n n={n}")
            self.eta[n] = self.tau / factor
            self.kappa[n] = weight * factor

    def b(self, d: int, n: int) -> arb:
        return self.logs[d] / self.logs[n] - self.eta[n]

    def alpha(self, q: int, n: int) -> arb:
        return self.kappa[n] * self.b(q, n)


def certify_prefix_collapse(scale: FiniteScale, n: int) -> None:
    """Check U_n(t)=m_n*t cellwise and the integrated collapse."""
    m_n = arb_sum(
        arb(scale.mu[d]) / d for d in range(1, n + 1)
    )
    for k in range(1, n + 1):
        floor_sum = sum(scale.mu[d] * (k // d) for d in range(1, n + 1))
        require(floor_sum == 1, "cellwise floor collapse failed", n, k,
                floor_sum)
        # On this cell, 1+sum mu(d){t/d} has slope m_n and zero intercept.
        intercept = 1 - floor_sum
        require(intercept == 0, "cellwise collapse intercept failed", n, k)
    lhs = affine_prefix(Q, n) + arb_sum(
        scale.mu[d] * prefix_cell(Q, d, n) for d in range(1, n + 1)
    )
    rhs = m_n * aterm(Q, n)
    certify_zero(lhs - rhs, f"integrated prefix collapse n={n}")


def assemble_column(scale: FiniteScale, d: int) -> tuple[arb, arb, arb]:
    """Return exact compatible W_B, W_C^delta, and W_H^delta columns."""
    require(d in ALL_COLUMNS, "invalid coefficient column", d)
    wb = arb(0)
    wc = arb(0)
    wh_formula = arb(0)
    g = scale.gram.entry(Q, d)
    gq = scale.gram.chi_cross(Q)
    for n in range(max(Q, d), M + 1):
        alpha = scale.alpha(Q, n)
        eta = scale.eta[n]
        log_ratio = scale.logs[d] / scale.logs[n]
        p = prefix_cell(Q, d, n)
        p0 = affine_prefix(Q, n)
        aa = aterm(Q, n)
        t = g - p
        wb += alpha * (log_ratio * p - eta * aa / d)
        wc += alpha * (
            (log_ratio - eta) * g
            - eta * (gq if d == 1 else arb(0))
        )
        wh_formula += alpha * (
            log_ratio * t
            - eta * g
            - eta * (gq if d == 1 else arb(0))
            + eta * aa / d
        )
    certify_zero(wc - wb - wh_formula,
                 f"delta tail column identity d={d}")
    return wb, wc, wh_formula


def direct_original_contractions(scale: FiniteScale) -> tuple[arb, arb, arb]:
    """Assemble B,C,H directly from original affine-plus-divisor vectors."""
    direct_b = arb(0)
    direct_c = arb(0)
    direct_h = arb(0)
    gq = scale.gram.chi_cross(Q)
    for n in range(Q, M + 1):
        eta = scale.eta[n]
        prefix = -eta * affine_prefix(Q, n)
        full = -eta * gq
        tail = -eta * (gq - affine_prefix(Q, n))
        for d in range(1, n + 1):
            coefficient = scale.mu[d] * scale.b(d, n)
            p = prefix_cell(Q, d, n)
            g = scale.gram.entry(Q, d)
            prefix += coefficient * p
            full += coefficient * g
            tail += coefficient * (g - p)
        alpha = scale.alpha(Q, n)
        direct_b += alpha * prefix
        direct_c += alpha * full
        direct_h += alpha * tail
    certify_zero(direct_b + direct_h - direct_c,
                 "direct original prefix+tail=full")
    return direct_b, direct_c, direct_h


def certify_output_state() -> dict[str, arb]:
    require(A == 3 and Q == 3 and M == 5, "declared finite state changed",
            A, Q, M)
    require(CURRENT_COLUMNS == (3, 5), "current columns changed",
            CURRENT_COLUMNS)
    scale = FiniteScale()
    for n in range(Q, M + 1):
        certify_prefix_collapse(scale, n)
    certify_gram_brackets(scale.gram)

    columns = {d: assemble_column(scale, d) for d in ALL_COLUMNS}
    selected_b = arb_sum(scale.mu[d] * columns[d][0] for d in ALL_COLUMNS)
    selected_c = arb_sum(scale.mu[d] * columns[d][1] for d in ALL_COLUMNS)
    selected_h = arb_sum(scale.mu[d] * columns[d][2] for d in ALL_COLUMNS)

    direct_b, direct_c, direct_h = direct_original_contractions(scale)
    certify_zero(selected_b - direct_b, "selected W_B equals original prefix")
    certify_zero(selected_c - direct_c,
                 "selected W_C_delta equals original full")
    certify_zero(selected_h - direct_h,
                 "selected W_H_delta equals original tail")
    certify_zero(selected_b + selected_h - selected_c,
                 "selected delta prefix+tail=full")

    # Explicitly retain and check the affine packet moved to d=1.
    affine_packet = arb_sum(
        -scale.alpha(Q, n) * scale.eta[n] * scale.gram.chi_cross(Q)
        for n in range(Q, M + 1)
    )
    d1_full = arb_sum(
        scale.alpha(Q, n) * (
            (scale.logs[1] / scale.logs[n] - scale.eta[n])
            * scale.gram.entry(Q, 1)
            - scale.eta[n] * scale.gram.chi_cross(Q)
        )
        for n in range(Q, M + 1)
    )
    certify_zero(columns[1][1] - d1_full,
                 "d=1 delta column including affine packet")
    certify_negative(affine_packet, "d=1 affine full packet sign")

    d1, d2 = CURRENT_COLUMNS
    b1, c1, _ = columns[d1]
    b2, c2, _ = columns[d2]
    wedge = b1 * c2 - b2 * c1
    determinant = -(wedge * wedge) / 4
    direct_determinant = (
        (b1 * c1) * (b2 * c2)
        - ((b1 * c2 + b2 * c1) / 2) ** 2
    )
    certify_zero(direct_determinant - determinant,
                 "principal determinant algebra")
    certify_negative(wedge, "current-column delta wedge")
    certify_negative(determinant,
                     "sym(W_B^T W_C_delta) principal determinant")

    physical_contraction = selected_b * selected_c
    certify_positive(physical_contraction,
                     "physical selected prefix/full contraction")

    return {
        "b1": b1,
        "c1": c1,
        "b2": b2,
        "c2": c2,
        "wedge": wedge,
        "determinant": determinant,
        "selected_b": selected_b,
        "selected_c": selected_c,
        "selected_h": selected_h,
        "physical_contraction": physical_contraction,
        "d1_affine_packet": affine_packet,
        "d1_wb": columns[1][0],
        "d1_wc": columns[1][1],
    }


def reread_and_verify_source() -> None:
    require(not _RAW_SCRIPT_PATH.is_symlink(),
            "certificate source became a symlink")
    safe_regular_file(SCRIPT_PATH)
    current = SCRIPT_PATH.read_bytes()
    require(current == _SCRIPT_BYTES, "certificate source changed during run")
    require(sha256_bytes(current) == SCRIPT_SHA256,
            "certificate source hash changed during run")
    reject_repository_import_artifacts()


def main() -> None:
    result = certify_output_state()
    reread_and_verify_source()
    print("certificate=cycle50-compatible-delta-gauge-obstruction")
    print("canonical_command=rm -f /tmp/cycle50-delta-gauge-obstruction.out && env -u PYTHONPYCACHEPREFIX PYTHONDONTWRITEBYTECODE=1 LC_ALL=C uv run --isolated --no-project --python 3.12.13 --with python-flint==0.9.0 python -I -B millennium-prize/riemann-hypothesis/cycle50_delta_gauge_obstruction.py > /tmp/cycle50-delta-gauge-obstruction.out && cmp /tmp/cycle50-delta-gauge-obstruction.out millennium-prize/riemann-hypothesis/cycle50-delta-gauge-obstruction.out")
    print(f"precision_bits={BITS}")
    print(
        "runtime="
        f"CPython-{platform.python_version()} "
        f"python-flint-{flint.__version__} FLINT-{flint.__FLINT_VERSION__}"
    )
    print(f"script_sha256={SCRIPT_SHA256}")
    print(f"closure_sha256={CLOSURE_SHA256}")
    print("parameters=theta=2/5 a=3 q=3 M=5 current_columns=3,5")
    print("gauge=compatible delta gauge W_B and W_C^delta")
    print("restricted_gram=full Vasyunin minus exact 1/(qd)")
    print("selected_columns=d=1,...,5 with d=1 affine packet retained")
    print(f"direct_gram_brackets=PASS cells={DIRECT_GRAM_CELLS} pairs=5 tail_bound=1/{DIRECT_GRAM_CELLS + 1}")
    print("finite_identities=PASS cumulative_floor_cells=12 integrated_prefix_collapses=3 delta_tail_columns=5 original_selected_contractions=3")
    print(f"d1_affine_packet={interval(result['d1_affine_packet'])}")
    print(f"d1_W_B={interval(result['d1_wb'])}")
    print(f"d1_W_C_delta={interval(result['d1_wc'])}")
    print(f"W_B_d3={interval(result['b1'])}")
    print(f"W_C_delta_d3={interval(result['c1'])}")
    print(f"W_B_d5={interval(result['b2'])}")
    print(f"W_C_delta_d5={interval(result['c2'])}")
    print(f"wedge={interval(result['wedge'])}")
    print(f"principal_determinant={interval(result['determinant'])}")
    print(f"selected_B={interval(result['selected_b'])}")
    print(f"selected_C_delta={interval(result['selected_c'])}")
    print(f"selected_H_delta={interval(result['selected_h'])}")
    print(f"physical_selected_contraction={interval(result['physical_contraction'])}")
    print("scope=finite exact identities and interval-certified signs only; no asymptotic or RH implication")
    print("result=PASS")


if __name__ == "__main__":
    main()
