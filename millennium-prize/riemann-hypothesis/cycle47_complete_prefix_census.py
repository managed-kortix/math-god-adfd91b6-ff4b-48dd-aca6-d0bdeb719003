#!/usr/bin/env python3
"""Fail-closed finite complete-prefix two-generator Arb census.

For theta=2/5, I0=[1,3/2], and a=32,...,1024, this standalone
certificate reconstructs the complete-prefix vectors Y_a,V_a,H_a and the
physical de-signed vector hat_c_a=Y_a+V_a+H_a.  It certifies the ordinary
rank-two projection only after an outward-positive Gram determinant.

This is a finite certificate.  It proves no asymptotic estimate, positive
liminf, moving-projection theorem, completed-square budget, or consequence for
the Riemann hypothesis.
"""

from __future__ import annotations

# Only isolated CPython standard-library modules are imported before the local
# closure is captured.  No third-party package or repository Python module is
# imported until preflight has rejected shadows and captured every local input.
import hashlib
import json
import os
import platform
import stat
import sys
from fractions import Fraction
from math import gcd
from pathlib import Path


BITS = 192
DIGITS = 48
STARTS = (32, 64, 128, 256, 512, 1024)
THETA = Fraction(2, 5)
MAX_N = 2 * max(STARTS)
IDENTITY_EXPONENT = BITS // 2
DIRECT_GRAM_CELLS = 100_000
DIRECT_GRAM_PAIRS = ((39, 26), (227, 229), (2017, 2039))

_RAW_SCRIPT_PATH = Path(__file__)
SCRIPT_PATH = _RAW_SCRIPT_PATH.resolve()
RH_DIR = SCRIPT_PATH.parent
WORKSPACE = RH_DIR.parent.parent
REFERENCE_PATH = RH_DIR / "cycle45-dispersion-census-results.json"
ENVIRONMENT_PATH = RH_DIR / "cycle45-dispersion-environment.json"

EXPECTED_INPUT_SHA256 = {
    REFERENCE_PATH:
        "6db00e23d47a409b905535dec0c88a1ad684e8daf95e62b3c6d25593c6d09f66",
    ENVIRONMENT_PATH:
        "a88cfbecae577f3cfb206769458113494b5bb2b4b783fdd4e46b71542434456b",
}

SHADOW_NAMES = (
    "argparse", "dataclasses", "fractions", "hashlib", "json", "math",
    "os", "pathlib", "platform", "stat", "sys", "types", "flint",
)


def fail(label: str, *details: object) -> None:
    raise RuntimeError((label,) + details)


def require(condition: bool, label: str, *details: object) -> None:
    if not condition:
        fail(label, *details)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _safe_mode(path: Path) -> int:
    mode = path.stat().st_mode
    require(stat.S_ISREG(mode), "closure member is not a regular file", path)
    require(not (mode & (stat.S_IWGRP | stat.S_IWOTH)),
            "closure member is group/world writable", path, oct(mode))
    return mode


def _reject_repository_import_artifacts() -> None:
    # Under -I the repository must not occur on sys.path.  Reject direct
    # shadows anyway, and reject every bytecode cache in this dossier.
    roots = (RH_DIR, RH_DIR.parent, WORKSPACE)
    for item in sys.path:
        if not item:
            continue
        resolved = Path(item).resolve()
        require(not (resolved == WORKSPACE or WORKSPACE in resolved.parents),
                "repository appears on isolated sys.path", resolved)

    for root in roots:
        for name in SHADOW_NAMES:
            candidates = (
                root / name,
                root / f"{name}.py",
                root / f"{name}.pyc",
                root / f"{name}.pyo",
            )
            for candidate in candidates:
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


def _capture_closure() -> tuple[bytes, dict[Path, bytes], str, str]:
    require(sys.flags.isolated and sys.flags.safe_path,
            "run with isolated Python (-I)", sys.flags)
    require(sys.flags.dont_write_bytecode,
            "run with bytecode disabled (-B)", sys.flags)
    require(sys.flags.optimize == 0, "optimized Python is forbidden", sys.flags)
    require(sys.flags.no_user_site, "user site must be disabled", sys.flags)
    require(os.environ.get("LC_ALL") == "C",
            "LC_ALL must equal C for canonical serialization")
    require(not os.environ.get("PYTHONPYCACHEPREFIX"),
            "PYTHONPYCACHEPREFIX must be unset")
    require(os.environ.get("PYTHONDONTWRITEBYTECODE") == "1",
            "PYTHONDONTWRITEBYTECODE must equal 1")
    require(not _RAW_SCRIPT_PATH.is_symlink(),
            "certificate source symlink is forbidden", _RAW_SCRIPT_PATH)
    require(SCRIPT_PATH.name == "cycle47_complete_prefix_census.py",
            "unexpected certificate filename", SCRIPT_PATH)
    _safe_mode(SCRIPT_PATH)
    _reject_repository_import_artifacts()
    require("flint" not in sys.modules,
            "flint was imported before closure capture")

    script_bytes = SCRIPT_PATH.read_bytes()
    script_sha = sha256_bytes(script_bytes)
    captured: dict[Path, bytes] = {}
    manifest_lines = [
        f"{SCRIPT_PATH.relative_to(WORKSPACE)} {script_sha}"
    ]
    for path, expected in EXPECTED_INPUT_SHA256.items():
        require(not path.is_symlink(), "closure input symlink is forbidden", path)
        require(path.is_file(), "missing closure input", path)
        _safe_mode(path)
        data = path.read_bytes()
        observed = sha256_bytes(data)
        require(observed == expected, "closure input hash mismatch", path,
                observed, expected)
        captured[path] = data
        manifest_lines.append(f"{path.relative_to(WORKSPACE)} {observed}")
    closure_sha = sha256_bytes(("\n".join(manifest_lines) + "\n").encode("ascii"))
    return script_bytes, captured, script_sha, closure_sha


_SCRIPT_BYTES, _CAPTURED_INPUTS, _SCRIPT_SHA256, _CLOSURE_SHA256 = \
    _capture_closure()

# This is the first third-party import.  The repository is absent from
# sys.path, local shadows were rejected, and all local bytes are already bound.
import flint  # noqa: E402
from flint import arb, ctx  # noqa: E402

_FLINT_ORIGIN = Path(flint.__file__).resolve()
require(not (_FLINT_ORIGIN == WORKSPACE or WORKSPACE in _FLINT_ORIGIN.parents),
        "repository flint shadow loaded", _FLINT_ORIGIN)


REQUIRED_RUNTIME = {
    "python": "3.12.13",
    "python_flint": "0.9.0",
    "flint": "3.6.0",
}


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
    require(os.environ.get("LC_ALL") == "C",
            "LC_ALL changed after startup", os.environ.get("LC_ALL"))
    for name, module in tuple(sys.modules.items()):
        if name != "flint" and not name.startswith("flint."):
            continue
        origin = getattr(module, "__file__", None)
        if origin is None:
            continue
        resolved = Path(origin).resolve()
        require(not (resolved == WORKSPACE or WORKSPACE in resolved.parents),
                "repository flint component loaded", name, resolved)


def verify_environment_manifest() -> None:
    try:
        payload = json.loads(_CAPTURED_INPUTS[ENVIRONMENT_PATH].decode("ascii"))
    except Exception as exc:
        raise RuntimeError("cannot parse bound environment manifest") from exc
    declared = {
        "python": payload["python"]["version"],
        "python_flint": payload["python_packages"]["python-flint"],
        "flint": payload["native_libraries"]["FLINT"],
    }
    require(payload["python"]["implementation"] == "CPython",
            "environment implementation changed", payload["python"])
    require(declared == REQUIRED_RUNTIME,
            "environment manifest version mismatch", declared,
            REQUIRED_RUNTIME)


verify_runtime()
verify_environment_manifest()
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


def certify_error_total(value: arb, label: str) -> arb:
    require_arb(value, label)
    require(value >= 0, "negative/unresolved error total", label, value)
    ceiling = identity_ceiling()
    require(value.upper() <= ceiling.lower(),
            "summed identity errors exceed fail-closed ceiling", label, value,
            ceiling)
    return value


def certify_positive(value: arb, label: str) -> arb:
    require_arb(value, label)
    require(value > 0, "positive sign false or unresolved", label, value)
    return value


def certify_nonnegative(value: arb, label: str) -> arb:
    require_arb(value, label)
    require(value >= 0, "nonnegative sign false or unresolved", label, value)
    return value


# ---------------------------------------------------------------------------
# Standalone restricted fractional-part Gram evaluator.
# ---------------------------------------------------------------------------


class RestrictedGram:
    """Evaluate <rho_a,rho_b> in L^2([1,infinity),dt/t^2).

    The finite Vasyunin cotangent formula first gives the full-space value;
    the exact restricted correction -1/(ab) is then retained.
    """

    def __init__(self) -> None:
        self._vasyunin: dict[tuple[int, int], arb] = {}
        self._cotangent_rows: dict[int, tuple[arb, ...]] = {}
        self._entries: dict[tuple[int, int], arb] = {}
        self.pi = arb.pi()
        self.c0 = (2 * self.pi).log() - arb.const_euler()

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
        d = gcd(a, b)
        p, q = a // d, b // d
        lcm = a * b // d
        full = (
            arb(q - p) * (arb(p) / q).log()
            + arb(p + q) * self.c0
            - self.pi * (self.vasyunin(p, q) + self.vasyunin(q, p))
        ) / (2 * lcm)
        restricted = full - arb(1) / (a * b)
        self._entries[key] = restricted
        return restricted

    @staticmethod
    def chi_cross(a: int) -> arb:
        return (arb(a).log() + 1 - arb.const_euler()) / a


def direct_gram_checks() -> tuple[dict[str, object], ...]:
    """Bracket three cotangent entries by literal reciprocal-cell sums."""
    prefixes = [arb(0) for _ in DIRECT_GRAM_PAIRS]
    for k in range(1, DIRECT_GRAM_CELLS + 1):
        log_ratio = (arb(k + 1) / k).log()
        reciprocal_gap = arb(1) / k - arb(1) / (k + 1)
        for index, (a, b) in enumerate(DIRECT_GRAM_PAIRS):
            floor_a = k // a
            floor_b = k // b
            prefixes[index] += (
                arb(1) / (a * b)
                - (arb(floor_a) / b + arb(floor_b) / a) * log_ratio
                + arb(floor_a * floor_b) * reciprocal_gap
            )
    tail = arb(1) / (DIRECT_GRAM_CELLS + 1)
    gram = RestrictedGram()
    results = []
    for pair, prefix in zip(DIRECT_GRAM_PAIRS, prefixes, strict=True):
        value = gram.entry(*pair)
        upper = prefix + tail
        require(prefix.upper() <= value.lower(),
                "direct Gram lower bracket failed", pair, prefix, value)
        require(value.upper() <= upper.lower(),
                "direct Gram upper bracket failed", pair, value, upper)
        results.append({"pair": pair, "prefix": prefix,
                        "cotangent": value, "tail": tail})
    return tuple(results)


# ---------------------------------------------------------------------------
# Two exact, independent arithmetic-table constructions.
# ---------------------------------------------------------------------------


def factorization(n: int) -> dict[int, int]:
    require(isinstance(n, int) and n >= 1, "invalid factorization input", n)
    factors: dict[int, int] = {}
    x = n
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
    if any(exponent > 1 for exponent in factors.values()):
        return 0
    return -1 if len(factors) % 2 else 1


def trial_prime_power_base(n: int) -> int | None:
    if n < 2:
        return None
    factors = factorization(n)
    if len(factors) != 1:
        return None
    return next(iter(factors))


def linear_mobius(limit: int) -> tuple[int, ...]:
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


def enumerated_prime_power_bases(limit: int) -> tuple[int | None, ...]:
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(limit ** 0.5) + 1):
        if is_prime[p]:
            for multiple in range(p * p, limit + 1, p):
                is_prime[multiple] = False
    bases: list[int | None] = [None] * (limit + 1)
    for p in range(2, limit + 1):
        if not is_prime[p]:
            continue
        power = p
        while power <= limit:
            require(bases[power] is None,
                    "integer is a power of two distinct primes", power,
                    bases[power], p)
            bases[power] = p
            power *= p
    return tuple(bases)


class ArithmeticTables:
    def __init__(self, limit: int) -> None:
        self.limit = limit
        mu_trial = (0,) + tuple(trial_mu(n) for n in range(1, limit + 1))
        mu_linear = linear_mobius(limit)
        require(mu_trial == mu_linear,
                "trial and linear Mobius tables disagree")
        base_trial = (None,) + tuple(
            trial_prime_power_base(n) for n in range(1, limit + 1)
        )
        base_enumerated = enumerated_prime_power_bases(limit)
        require(base_trial == base_enumerated,
                "trial and enumerated prime-power tables disagree")
        self.mu = mu_trial
        self.prime_power_base = base_trial

        # Exact integer divisor-convolution audit of every Mobius sign.
        for n in range(1, limit + 1):
            convolution = sum(self.mu[d] for d in range(1, n + 1)
                              if n % d == 0)
            expected = 1 if n == 1 else 0
            require(convolution == expected,
                    "Mobius divisor convolution failed", n, convolution,
                    expected)

        self.logs = [arb(0)] + [arb(n).log() for n in range(1, limit + 2)]
        self.Lambda = [arb(0) for _ in range(limit + 1)]
        for n in range(2, limit + 1):
            base = self.prime_power_base[n]
            if base is not None:
                self.Lambda[n] = self.logs[base]

        self.psi = [arb(0) for _ in range(limit + 1)]
        running = arb(0)
        for n in range(1, limit + 1):
            running += self.Lambda[n]
            self.psi[n] = running

        self.C = [arb(0) for _ in range(limit + 1)]
        for r in range(2, limit + 1):
            self.C[r] = (
                self.C[r - 1]
                + self.psi[r - 1] * (self.logs[r] - self.logs[r - 1])
            )

        self.psi_weight_prefix = [arb(0) for _ in range(limit + 1)]
        running = arb(0)
        for k in range(1, limit + 1):
            running += self.psi[k] / (k * (k + 1))
            self.psi_weight_prefix[k] = running

        self.m = [Fraction(0) for _ in range(limit + 1)]
        self.ell = [arb(0) for _ in range(limit + 1)]
        m_running = Fraction(0)
        ell_running = arb(0)
        for n in range(1, limit + 1):
            if self.mu[n]:
                m_running += Fraction(self.mu[n], n)
                ell_running += self.mu[n] * self.logs[n] / n
            self.m[n] = m_running
            self.ell[n] = ell_running

        lambda_convolution_error = arb(0)
        c_direct_error = arb(0)
        psi_direct_error = arb(0)
        for n in range(1, limit + 1):
            lambda_from_mu = -arb_sum(
                self.mu[d] * self.logs[d] for d in range(1, n + 1)
                if n % d == 0
            )
            lambda_convolution_error += certify_zero(
                lambda_from_mu - self.Lambda[n],
                f"von Mangoldt divisor convolution n={n}",
            )
            psi_direct = arb_sum(self.Lambda[m] for m in range(1, n + 1))
            psi_direct_error += certify_zero(
                self.psi[n] - psi_direct, f"psi direct prefix n={n}"
            )
            c_direct = arb_sum(
                self.Lambda[m] * (self.logs[n] - self.logs[m])
                for m in range(2, n)
            )
            c_direct_error += certify_zero(
                self.C[n] - c_direct, f"C temporal versus direct n={n}"
            )
        self.error_totals = {
            "lambda_convolution": certify_error_total(
                lambda_convolution_error, "all Lambda convolution errors"
            ),
            "psi_direct": certify_error_total(
                psi_direct_error, "all psi direct-prefix errors"
            ),
            "C_direct": certify_error_total(
                c_direct_error, "all C direct-prefix errors"
            ),
        }


# ---------------------------------------------------------------------------
# Complete-prefix formulas on I0=[1,3/2].
# ---------------------------------------------------------------------------


class CompletePrefixScale:
    def __init__(self, a: int, arithmetic: ArithmeticTables) -> None:
        require(a in STARTS, "undeclared scale", a)
        self.a = a
        self.stop = 2 * a
        self.arithmetic = arithmetic
        self.gram = RestrictedGram()
        self.theta = arb_fraction(THETA)
        self.tau = 1 - 2 * self.theta
        self.squarefree = tuple(
            d for d in range(1, self.stop) if arithmetic.mu[d] != 0
        )
        # Closed I0.  The integer inequality avoids any floating endpoint.
        self.rows = tuple(
            q for q in range(a, self.stop)
            if arithmetic.mu[q] != 0 and 2 * q <= 3 * a
        )
        require(self.rows, "empty physical row set", a)
        require(self.rows == tuple(
            q for q in range(a, 3 * a // 2 + 1)
            if trial_mu(q) != 0
        ), "closed physical row set mismatch", a)

        self.w: dict[int, arb] = {}
        self.A: dict[int, arb] = {}
        self.eta: dict[int, arb] = {}
        self.kappa: dict[int, arb] = {}
        self.s: dict[int, arb] = {}
        self.R: dict[int, arb] = {}
        for n in range(a, self.stop):
            log_n = arithmetic.logs[n]
            ratio = log_n / arithmetic.logs[n + 1]
            self.w[n] = 1 - ratio
            self.A[n] = 1 + ratio - 2 * self.theta
            certify_positive(self.A[n], f"A_n a={a} n={n}")
            self.eta[n] = self.tau / self.A[n]
            self.kappa[n] = self.w[n] * self.A[n]
            m_n = arb_fraction(arithmetic.m[n])
            self.s[n] = arithmetic.ell[n] / log_n - self.eta[n] * m_n
            self.R[n] = self.s[n] + 1 / log_n

        self.B2 = [arb(0) for _ in range(self.stop + 1)]
        self.B1 = [arb(0) for _ in range(self.stop + 1)]
        self.B0 = [arb(0) for _ in range(self.stop + 1)]
        for n in range(self.stop - 1, a - 1, -1):
            log_n = arithmetic.logs[n]
            self.B2[n] = self.B2[n + 1] + self.kappa[n] / log_n ** 2
            self.B1[n] = (
                self.B1[n + 1]
                + self.kappa[n] * self.eta[n] / log_n
            )
            self.B0[n] = (
                self.B0[n + 1]
                + self.kappa[n] * self.eta[n] ** 2
            )

    def b(self, d: int, n: int) -> arb:
        return self.arithmetic.logs[d] / self.arithmetic.logs[n] - self.eta[n]

    def alpha(self, q: int, n: int) -> arb:
        return self.kappa[n] * self.b(q, n)

    def a_term(self, q: int, n: int) -> arb:
        return arb(n) / q - (arb(n + 1) / q).log()

    def j_direct(self, q: int, n: int) -> arb:
        ar = self.arithmetic
        weighted_psi = (
            ar.psi_weight_prefix[n] - ar.psi_weight_prefix[q - 1]
        )
        return (arb(n + 1) / q).log() - weighted_psi

    def j_abel(self, q: int, n: int) -> arb:
        ar = self.arithmetic
        return (
            (arb(n + 1) / q).log()
            - ar.psi[q - 1] / q
            - arb_sum(ar.Lambda[m] / m for m in range(q, n + 1))
            + ar.psi[n] / (n + 1)
        )

    def B_closed(self, q: int, n: int) -> arb:
        ar = self.arithmetic
        E = ar.C[n + 1] - n
        return (
            self.a_term(q, n) * self.R[n]
            + E / (q * ar.logs[n])
            + self.j_direct(q, n) / ar.logs[n]
        )

    def B_abel(self, q: int, n: int) -> arb:
        ar = self.arithmetic
        E = ar.C[n + 1] - n
        return (
            self.a_term(q, n) * self.R[n]
            + E / (q * ar.logs[n])
            + self.j_abel(q, n) / ar.logs[n]
        )

    def B_cells(self, q: int, n: int) -> arb:
        """Literal cells from the affine and every signed Mobius coefficient."""
        ar = self.arithmetic
        slope = arb(0)
        jumps = [arb(0) for _ in range(n + 1)]
        for d in self.squarefree:
            if d > n:
                break
            coefficient = ar.mu[d] * self.b(d, n)
            slope += coefficient / d
            for k in range(d, n + 1, d):
                jumps[k] += coefficient

        # Z_n=-eta_n*chi+sum_{d<=n} mu(d)b_d(n)rho_d.
        intercept = -self.eta[n]
        total = arb(0)
        rho_slope = arb(1) / q
        for k in range(1, n + 1):
            intercept -= jumps[k]
            rho_intercept = -arb(k // q)
            log_ratio = (arb(k + 1) / k).log()
            reciprocal_gap = arb(1) / k - arb(1) / (k + 1)
            total += (
                rho_slope * slope
                + (rho_slope * intercept + rho_intercept * slope) * log_ratio
                + rho_intercept * intercept * reciprocal_gap
            )
        return total

    def hat_coefficient_index(self, q: int) -> arb:
        """beta(q)+sum_d mu(d)W(q,d), with no hidden outer Mobius sign."""
        ar = self.arithmetic
        log_q = ar.logs[q]
        total = -self.gram.chi_cross(q) * (
            log_q * self.B1[q] - self.B0[q]
        )
        for d in self.squarefree:
            j = max(q, d)
            log_d = ar.logs[d]
            temporal = (
                log_q * log_d * self.B2[j]
                - (log_q + log_d) * self.B1[j]
                + self.B0[j]
            )
            total += ar.mu[d] * self.gram.entry(q, d) * temporal
        return total

    def deterministic_B_checks(self) -> tuple[dict[str, object], ...]:
        selected_q = (self.rows[0], self.rows[len(self.rows) // 2],
                      self.rows[-1])
        require(len(set(selected_q)) == 3,
                "first/middle/last row selectors are not distinct", self.a,
                selected_q)
        checks = []
        for q in selected_q:
            middle_n = (q + self.stop - 1) // 2
            selected_n = (q, middle_n, self.stop - 1)
            require(q < middle_n < self.stop - 1,
                    "temporal midpoint is not interior", self.a, q, middle_n)
            for n in selected_n:
                require(q <= n < self.stop and n < 2 * q,
                        "complete-prefix endpoint precondition failed",
                        self.a, q, n)
                closed = self.B_closed(q, n)
                cells = self.B_cells(q, n)
                abel = self.B_abel(q, n)
                cell_error = certify_zero(
                    closed - cells,
                    f"B closed versus direct cells a={self.a} q={q} n={n}",
                )
                abel_error = certify_zero(
                    closed - abel,
                    f"B closed versus Abel a={self.a} q={q} n={n}",
                )
                checks.append({
                    "q": q,
                    "n": n,
                    "B": closed,
                    "cell_error": cell_error,
                    "abel_error": abel_error,
                })
        require(len(checks) == 9, "unexpected deterministic B check count",
                self.a, len(checks))
        return tuple(checks)

    def vectors(self) -> tuple[dict[int, arb], dict[int, arb],
                               dict[int, arb], dict[int, arb],
                               dict[str, arb]]:
        """Temporal-prefix K path, plus an independent coefficient-index path."""
        ar = self.arithmetic
        Y: dict[int, arb] = {}
        V: dict[int, arb] = {}
        H: dict[int, arb] = {}
        hat: dict[int, arb] = {}
        recombination_error = arb(0)
        coefficient_error = arb(0)
        diagonal_error = arb(0)

        for q in self.rows:
            expected_diagonal = self.gram.c0 / q - arb(1) / (q * q)
            diagonal_error += certify_zero(
                self.gram.entry(q, q) - expected_diagonal,
                f"restricted Gram diagonal a={self.a} q={q}",
            )

            spatial_u = arb(0)
            spatial_d = arb(0)
            index = 0
            y_q = arb(0)
            v_q = arb(0)
            h_q = arb(0)
            c_q = arb(0)
            g_q = self.gram.chi_cross(q)

            for n in range(q, self.stop):
                while (index < len(self.squarefree)
                       and self.squarefree[index] <= n):
                    d = self.squarefree[index]
                    gram_qd = self.gram.entry(q, d)
                    spatial_u += ar.mu[d] * gram_qd
                    spatial_d += ar.mu[d] * ar.logs[d] * gram_qd
                    index += 1

                K_qn = (
                    spatial_d / ar.logs[n]
                    - self.eta[n] * (g_q + spatial_u)
                )
                B_qn = self.B_closed(q, n)
                E = ar.C[n + 1] - n
                alpha_qn = self.alpha(q, n)
                y_q += alpha_qn * E / (q * ar.logs[n])
                v_q += alpha_qn * (
                    self.a_term(q, n) * self.R[n]
                    + self.j_direct(q, n) / ar.logs[n]
                )
                h_q += alpha_qn * (K_qn - B_qn)
                c_q += alpha_qn * K_qn

            Y[q] = y_q
            V[q] = v_q
            H[q] = h_q
            hat[q] = c_q
            recombination_error += certify_zero(
                y_q + v_q + h_q - c_q,
                f"all-row Y+V+H=hat_c a={self.a} q={q}",
            )
            column_hat = self.hat_coefficient_index(q)
            coefficient_error += certify_zero(
                c_q - column_hat,
                f"temporal versus coefficient-index hat_c a={self.a} q={q}",
            )

        errors = {
            "YVH_recombination": certify_error_total(
                recombination_error,
                f"all-row Y+V+H errors a={self.a}",
            ),
            "hat_temporal_vs_columns": certify_error_total(
                coefficient_error,
                f"all-row temporal/column hat errors a={self.a}",
            ),
            "restricted_Gram_diagonal": certify_error_total(
                diagonal_error,
                f"all-row restricted Gram diagonal errors a={self.a}",
            ),
        }
        return Y, V, H, hat, errors


# ---------------------------------------------------------------------------
# Bound Cycle 45 D rows and rank-safe two-generator projection.
# ---------------------------------------------------------------------------


def load_cycle45_reference() -> dict[int, tuple[arb, int]]:
    try:
        payload = json.loads(_CAPTURED_INPUTS[REFERENCE_PATH].decode("ascii"))
    except Exception as exc:
        raise RuntimeError("cannot parse bound Cycle 45 D artifact") from exc
    require(payload.get("scope") == (
        "certified finite diagnostic only; no convergence, asymptotic lower "
        "bound, or RH claim"
    ), "Cycle 45 scope changed", payload.get("scope"))
    require(payload.get("arb_precision_bits") == 192,
            "Cycle 45 precision changed", payload.get("arb_precision_bits"))
    require(payload.get("theta") == "2/5", "Cycle 45 theta changed")
    require(payload.get("starts") == list(STARTS),
            "Cycle 45 starts changed", payload.get("starts"))
    require(payload.get("runtime") == {
        "python": "3.12.13",
        "python_flint": "0.9.0",
        "flint": "3.6.0",
        "python_implementation": "cpython",
        "generator": "cycle45_dispersion_census.py",
        "generator_sha256":
            "9f24a6630a8804996590732d8a6f6389557a296eacb7daedc5fc56cb38152ade",
        "environment_manifest": "cycle45-dispersion-environment.json",
        "environment_manifest_sha256": EXPECTED_INPUT_SHA256[ENVIRONMENT_PATH],
    }, "Cycle 45 runtime metadata changed", payload.get("runtime"))
    require(len(payload.get("rows", ())) == 12,
            "Cycle 45 artifact row count changed")

    references: dict[int, tuple[arb, int]] = {}
    for row in payload["rows"]:
        if row.get("I") != [1.0, 1.5]:
            continue
        a = row.get("a")
        require(a in STARTS and a not in references,
                "unexpected/duplicate Cycle 45 I0 row", a)
        D = require_arb(arb(row["D"]), f"Cycle 45 D a={a}")
        certify_positive(D, f"Cycle 45 D positivity a={a}")
        rank = row.get("rank")
        require(isinstance(rank, int) and rank > 0,
                "invalid Cycle 45 rank", a, rank)
        references[a] = (D, rank)
    require(tuple(sorted(references)) == STARTS,
            "Cycle 45 I0 rows incomplete", tuple(sorted(references)))
    return references


def gram_data(Y: dict[int, arb], V: dict[int, arb], H: dict[int, arb],
              hat: dict[int, arb], rows: tuple[int, ...], a: int,
              cycle45_D: arb, cycle45_rank: int) -> dict[str, object]:
    require(len(rows) == cycle45_rank,
            "Cycle 45 row rank not reproduced", a, len(rows), cycle45_rank)

    YY = arb_sum(Y[q] * Y[q] for q in rows)
    YV = arb_sum(Y[q] * V[q] for q in rows)
    YH = arb_sum(Y[q] * H[q] for q in rows)
    VV = arb_sum(V[q] * V[q] for q in rows)
    VH = arb_sum(V[q] * H[q] for q in rows)
    HH = arb_sum(H[q] * H[q] for q in rows)
    D = arb_sum(hat[q] * hat[q] for q in rows)
    zY = arb_sum(Y[q] * hat[q] for q in rows)
    zV = arb_sum(V[q] * hat[q] for q in rows)
    z2 = zY ** 2 + zV ** 2
    trG = YY + VV
    detG = YY * VV - YV ** 2

    certify_positive(YY, f"||Y||^2 a={a}")
    certify_positive(VV, f"||V||^2 a={a}")
    certify_positive(trG, f"trG a={a}")
    certify_positive(D, f"D a={a}")
    certify_positive(z2, f"||z||^2 a={a}")

    # No inverse, adjugate quotient, or projection coefficient is formed until
    # strict outward positivity of detG certifies rank two.  Any unresolved or
    # rank-deficient case aborts rather than guessing a pseudoinverse/rank.
    certify_positive(detG, f"detG rank-two certificate a={a}")
    numerator = VV * zY ** 2 - 2 * YV * zY * zV + YY * zV ** 2
    certify_positive(numerator, f"rank-two projection numerator a={a}")
    Q2 = numerator / detG
    certify_positive(Q2, f"Q2 a={a}")
    lambda_Y = (VV * zY - YV * zV) / detG
    lambda_V = (YY * zV - YV * zY) / detG
    residual_direct = arb_sum(
        (hat[q] - lambda_Y * Y[q] - lambda_V * V[q]) ** 2
        for q in rows
    )
    D_minus_Q2 = D - Q2
    certify_nonnegative(D_minus_Q2, f"D-Q2 a={a}")
    certify_nonnegative(residual_direct, f"direct residual norm^2 a={a}")
    certify_nonnegative(Q2 - z2 / trG, f"trace lower bound a={a}")

    vector_gram_error = certify_zero(
        D - (YY + VV + HH + 2 * (YV + YH + VH)),
        f"D versus full Y,V,H Gram a={a}",
    )
    z_error = certify_zero(
        zY - (YY + YV + YH), f"zY versus vector Gram a={a}"
    ) + certify_zero(
        zV - (YV + VV + VH), f"zV versus vector Gram a={a}"
    )
    projection_error = certify_zero(
        D_minus_Q2 - residual_direct,
        f"projection Pythagoras a={a}",
    )
    orthogonality_error = certify_zero(
        arb_sum(Y[q] * (hat[q] - lambda_Y * Y[q] - lambda_V * V[q])
                for q in rows),
        f"projection residual orthogonal to Y a={a}",
    ) + certify_zero(
        arb_sum(V[q] * (hat[q] - lambda_Y * Y[q] - lambda_V * V[q])
                for q in rows),
        f"projection residual orthogonal to V a={a}",
    )
    for label, value in (
        ("vector_Gram", vector_gram_error),
        ("z_from_Gram", z_error),
        ("projection_Pythagoras", projection_error),
        ("projection_orthogonality", orthogonality_error),
    ):
        certify_error_total(value, f"{label} error a={a}")

    require(cycle45_D.contains(D),
            "bound Cycle 45 D does not contain reconstruction", a, D,
            cycle45_D)
    overlap = D.intersection(cycle45_D)
    require_arb(overlap, f"Cycle 45 D overlap a={a}")

    L = arb(a).log()
    L3 = L ** 3
    L6 = L ** 6
    return {
        "a": a,
        "rows": len(rows),
        "YY": YY,
        "YV": YV,
        "YH": YH,
        "VV": VV,
        "VH": VH,
        "HH": HH,
        "D": D,
        "zY": zY,
        "zV": zV,
        "z2": z2,
        "trG": trG,
        "detG": detG,
        "Q2": Q2,
        "D_minus_Q2": D_minus_Q2,
        "Q2_over_D": Q2 / D,
        "L3_Q2": L3 * Q2,
        "L3_trG": L3 * trG,
        "L6_z2": L6 * z2,
        "trace_lower_bound": z2 / trG,
        "lambda_Y": lambda_Y,
        "lambda_V": lambda_V,
        "residual_direct": residual_direct,
        "cycle45_D": cycle45_D,
        "cycle45_overlap": overlap,
        "projection_errors": {
            "vector_Gram": vector_gram_error,
            "z_from_Gram": z_error,
            "projection_Pythagoras": projection_error,
            "projection_orthogonality": orthogonality_error,
        },
    }


def verify_closure_unchanged() -> None:
    verify_runtime()
    require(ctx.prec == BITS, "Arb precision changed", ctx.prec, BITS)
    _safe_mode(SCRIPT_PATH)
    require(SCRIPT_PATH.read_bytes() == _SCRIPT_BYTES,
            "certificate source mutated after capture", SCRIPT_PATH)
    require(sha256_bytes(_SCRIPT_BYTES) == _SCRIPT_SHA256,
            "captured certificate source hash changed")
    for path, expected in EXPECTED_INPUT_SHA256.items():
        _safe_mode(path)
        current = path.read_bytes()
        require(current == _CAPTURED_INPUTS[path],
                "bound input mutated after capture", path)
        require(sha256_bytes(current) == expected,
                "bound input hash changed after capture", path)
    _reject_repository_import_artifacts()


def main() -> None:
    arithmetic = ArithmeticTables(MAX_N)
    direct_gram = direct_gram_checks()
    references = load_cycle45_reference()

    all_rows = []
    for a in STARTS:
        scale = CompletePrefixScale(a, arithmetic)
        B_checks = scale.deterministic_B_checks()
        Y, V, H, hat, path_errors = scale.vectors()
        data = gram_data(
            Y, V, H, hat, scale.rows, a,
            references[a][0], references[a][1],
        )
        B_cell_total = certify_error_total(
            arb_sum(item["cell_error"] for item in B_checks),
            f"all deterministic B cell errors a={a}",
        )
        B_abel_total = certify_error_total(
            arb_sum(item["abel_error"] for item in B_checks),
            f"all deterministic B Abel errors a={a}",
        )
        data["B_checks"] = B_checks
        data["path_errors"] = path_errors
        data["B_cell_total"] = B_cell_total
        data["B_abel_total"] = B_abel_total
        data["selected_rows"] = (
            scale.rows[0], scale.rows[len(scale.rows) // 2], scale.rows[-1]
        )
        all_rows.append(data)

    require(len(all_rows) == len(STARTS),
            "unexpected scale result count", len(all_rows))
    verify_closure_unchanged()

    lines: list[str] = []
    emit = lines.append
    emit("RH CYCLE 47 COMPLETE-PREFIX TWO-GENERATOR CENSUS: PASS")
    emit("scope=6 finite outward-Arb rows on fixed closed I0=[1,3/2]; no asymptotic or RH inference")
    emit(f"source={SCRIPT_PATH.relative_to(WORKSPACE)}")
    emit(f"source_sha256={_SCRIPT_SHA256}")
    emit(f"captured_closure_manifest_sha256={_CLOSURE_SHA256}")
    emit("self_hash_binding=the output embeds the captured source SHA-256 and canonical replay is byte-compared")
    emit("local_source_closure=standalone certificate only; no repository Python module is imported")
    emit("runtime=CPython-3.12.13 python-flint-0.9.0 FLINT-3.6.0")
    emit("trusted_runtime_boundary=versions are pinned; interpreter/wheel/native-library binaries, OS, hardware, and uv launcher are not binary-attested")
    emit(f"arb_precision_bits={BITS} identity_error_ceiling={interval(identity_ceiling(), 18)}")
    emit("canonical_command=rm -f /tmp/cycle47-complete-prefix-census.out && env -u PYTHONPYCACHEPREFIX PYTHONDONTWRITEBYTECODE=1 LC_ALL=C uv run --isolated --no-project --python 3.12.13 --with python-flint==0.9.0 python -I -B millennium-prize/riemann-hypothesis/cycle47_complete_prefix_census.py > /tmp/cycle47-complete-prefix-census.out && cmp /tmp/cycle47-complete-prefix-census.out millennium-prize/riemann-hypothesis/cycle47-complete-prefix-census.out")
    emit("parameters=theta=2/5 I0=[1,3/2] starts=32,64,128,256,512,1024 temporal_endpoint=2a-1")
    emit("row_rule=squarefree q with a<=q<2a and 1<=q/a<=3/2, both interval endpoints closed")
    emit("normalization=hat_c(q)=mu(q)c(q) on physical squarefree rows; no extra outer Mobius sign")
    emit("affine_and_restricted_terms=Z_n retains -eta_n*chi; Gram retains exact -1/(qd) restricted correction")
    emit("definitions=B(q,n)=integral_[1,n+1] rho_q Z_n dt/t^2; hat_c=Y+V+H; H retains K(q,n)-B(q,n)")
    emit("rank_policy=ordinary 2x2 inverse/adjugate quotient is formed only after detG>0 is outward-certified; otherwise abort")
    emit("path_checks=PASS deterministic B direct-cells and Abel; all-row Y+V+H; temporal versus coefficient-index hat_c; projection Pythagoras")
    emit(f"exact_arithmetic_tables=PASS range=1..{MAX_N} Mobius=trial_factorization_vs_linear_sieve Lambda=trial_prime_power_vs_Eratosthenes_enumeration")
    for label, value in arithmetic.error_totals.items():
        emit(f"arithmetic_identity_error_sum_upper {label}={interval(value, 18)}")
    emit(f"offdiagonal_direct_cell_Gram=PASS pairs={len(direct_gram)} cells={DIRECT_GRAM_CELLS} tail_bound=1/{DIRECT_GRAM_CELLS + 1} independent_formula_shared_Arb_backend")
    for item in direct_gram:
        a, b = item["pair"]
        emit(
            f"direct_Gram pair=({a},{b}) prefix={interval(item['prefix'], 24)} "
            f"cotangent={interval(item['cotangent'], 24)} "
            f"tail={interval(item['tail'], 18)}"
        )
    emit(f"bound_inputs_sha256=PASS count={len(EXPECTED_INPUT_SHA256)}")
    for path, expected in EXPECTED_INPUT_SHA256.items():
        emit(f"input_sha256 {path.relative_to(WORKSPACE)} {expected}")

    for row in all_rows:
        a = row["a"]
        emit(f"row a={a} I0=[1,3/2] rows={row['rows']} certified_rank=2")
        emit(
            "  deterministic_B_policy="
            f"q_first_middle_last={row['selected_rows']} "
            "n=q,floor((q+2a-1)/2),2a-1 final_cell=[n,n+1)"
        )
        for check in row["B_checks"]:
            emit(
                f"  B_check q={check['q']} n={check['n']} "
                f"B={interval(check['B'])} "
                f"closed_minus_cells_abs_upper={interval(check['cell_error'], 18)} "
                f"closed_minus_Abel_abs_upper={interval(check['abel_error'], 18)}"
            )
        emit(
            "  identity_error_sums_upper "
            f"B_cells={interval(row['B_cell_total'], 18)} "
            f"B_Abel={interval(row['B_abel_total'], 18)} "
            + " ".join(
                f"{label}={interval(value, 18)}"
                for label, value in row["path_errors"].items()
            )
            + " "
            + " ".join(
                f"{label}={interval(value, 18)}"
                for label, value in row["projection_errors"].items()
            )
        )
        for label in (
            "D", "Q2", "D_minus_Q2", "Q2_over_D", "L3_Q2",
            "detG", "trG", "L3_trG", "z2", "L6_z2",
            "trace_lower_bound",
        ):
            emit(f"  {label} {interval(row[label])}")
        emit("  vector_Gram_order=Y2,YV,YH,V2,VH,H2")
        for label in ("YY", "YV", "YH", "VV", "VH", "HH"):
            emit(f"  {label} {interval(row[label])}")
        emit(f"  zY {interval(row['zY'])}")
        emit(f"  zV {interval(row['zV'])}")
        emit(f"  projection_lambda_Y {interval(row['lambda_Y'])}")
        emit(f"  projection_lambda_V {interval(row['lambda_V'])}")
        emit(f"  residual_direct2 {interval(row['residual_direct'])}")
        emit(f"  cycle45_D {interval(row['cycle45_D'])}")
        emit(f"  cycle45_D_overlap {interval(row['cycle45_overlap'])}")

    emit("cycle45_D_artifact_overlap=PASS count=6 policy=bound_artifact_contains_each_reconstruction")
    emit("complete_prefix_checks=PASS B_checks=54 all_physical_rows=613 temporal_and_coefficient_index_paths=613")
    emit("finite_only_disclaimer=These six finite, nonmonotone diagnostics certify no untested scale, asymptotic lower bound, positive liminf, moving-projection theorem, completed-square budget, or Riemann-hypothesis conclusion.")
    emit("NO_ASYMPTOTIC_INFERENCE")
    emit("ALL_DECLARED_CHECKS_PASS")

    # Check once more immediately before emitting the buffered artifact.
    verify_closure_unchanged()
    sys.stdout.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
