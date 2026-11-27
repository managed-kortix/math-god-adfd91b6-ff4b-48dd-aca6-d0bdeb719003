#!/usr/bin/env python3
"""Fail-closed Cycle 49 exact finite complete-prefix certificate.

At theta=2/5 this standalone verifier certifies the exact finite split

    B_a(q) = Pplus_a(q) + Smu_a(q)

and independent finite Abel forms for both summands.  It also reconstructs the
physical complete-prefix contraction at (a,q)=(218,327), and the physical
aggregate on a=301, I0=[1,3/2].

This is a finite certificate.  Asymptotics are untested.  It proves no
asymptotic estimate, eventual sign, positive liminf, moving-projection theorem,
completed-square budget, or consequence for the Riemann hypothesis.
"""

from __future__ import annotations

# Capture the complete local closure before importing any third-party package.
# Only isolated CPython standard-library modules are used during preflight.
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
THETA = Fraction(2, 5)
ALPHA_FLOOR = Fraction(1, 1_000_000)
DECLARED_SCALES = (218, 301)
COUNTEREXAMPLE = (218, 327)
AGGREGATE_SCALE = 301
MAX_N = 2 * max(DECLARED_SCALES)
IDENTITY_EXPONENT = BITS // 2

_RAW_SCRIPT_PATH = Path(__file__)
SCRIPT_PATH = _RAW_SCRIPT_PATH.resolve()
RH_DIR = SCRIPT_PATH.parent
WORKSPACE = RH_DIR.parent.parent
SOURCE_ANCESTOR_PATH = RH_DIR / "cycle47_complete_prefix_census.py"
EXPECTED_INPUT_SHA256 = {
    SOURCE_ANCESTOR_PATH:
        "49f128e0e411f03e6d646ddbee5e4b2a13a4da2bc11bc5e6705e356404625928",
}

SHADOW_NAMES = (
    "fractions", "hashlib", "math", "os", "pathlib", "platform", "stat",
    "sys", "flint",
)


def fail(label: str, *details: object) -> None:
    raise RuntimeError((label,) + details)


def require(condition: bool, label: str, *details: object) -> None:
    if not condition:
        fail(label, *details)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _safe_regular_file(path: Path) -> None:
    metadata = path.stat()
    mode = metadata.st_mode
    require(stat.S_ISREG(mode), "closure member is not a regular file", path)
    require(metadata.st_nlink == 1,
            "closure member has multiple hard links", path,
            metadata.st_nlink)
    require(not (mode & (stat.S_IWGRP | stat.S_IWOTH)),
            "closure member is group/world writable", path, oct(mode))


def _reject_repository_import_artifacts() -> None:
    for item in sys.path:
        if not item:
            continue
        resolved = Path(item).resolve()
        require(not (resolved == WORKSPACE or WORKSPACE in resolved.parents),
                "repository appears on isolated sys.path", resolved)

    roots = (RH_DIR, RH_DIR.parent, WORKSPACE)
    for root in roots:
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


def _capture_closure() -> tuple[bytes, dict[Path, bytes], str, str]:
    require(sys.flags.isolated and sys.flags.safe_path,
            "run with isolated Python (-I)", sys.flags)
    require(sys.flags.dont_write_bytecode,
            "run with bytecode disabled (-B)", sys.flags)
    require(sys.flags.optimize == 0, "optimized Python is forbidden", sys.flags)
    require(sys.flags.no_user_site, "user site must be disabled", sys.flags)
    require(os.environ.get("LC_ALL") == "C",
            "LC_ALL must equal C for canonical serialization")
    require(os.environ.get("PYTHONDONTWRITEBYTECODE") == "1",
            "PYTHONDONTWRITEBYTECODE must equal 1")
    require(not os.environ.get("PYTHONPYCACHEPREFIX"),
            "PYTHONPYCACHEPREFIX must be unset")
    require(not _RAW_SCRIPT_PATH.is_symlink(),
            "certificate source symlink is forbidden", _RAW_SCRIPT_PATH)
    require(SCRIPT_PATH.name == "cycle49_exact_prefix_certificate.py",
            "unexpected certificate filename", SCRIPT_PATH)
    _safe_regular_file(SCRIPT_PATH)
    _reject_repository_import_artifacts()
    require("flint" not in sys.modules,
            "flint was imported before closure capture")

    script_bytes = SCRIPT_PATH.read_bytes()
    script_sha = sha256_bytes(script_bytes)
    captured: dict[Path, bytes] = {}
    manifest_lines = [f"{SCRIPT_PATH.relative_to(WORKSPACE)} {script_sha}"]
    for path, expected in EXPECTED_INPUT_SHA256.items():
        require(not path.is_symlink(), "closure input symlink is forbidden", path)
        require(path.is_file(), "missing closure input", path)
        _safe_regular_file(path)
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

# First third-party import.  All local bytes are already bound and the
# repository is absent from the isolated import path.
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


def certify_negative(value: arb, label: str) -> arb:
    require_arb(value, label)
    require(value < 0, "negative sign false or unresolved", label, value)
    return value


# ---------------------------------------------------------------------------
# Standalone restricted fractional-part Gram evaluator.
# ---------------------------------------------------------------------------


class RestrictedGram:
    """Evaluate <rho_a,rho_b> on L^2([1,infinity),dt/t^2)."""

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
        # Exact restricted-space correction.  It must not be dropped.
        restricted = full - arb(1) / (a * b)
        self._entries[key] = restricted
        return restricted

    @staticmethod
    def chi_cross(a: int) -> arb:
        return (arb(a).log() + 1 - arb.const_euler()) / a


# ---------------------------------------------------------------------------
# Independent exact arithmetic tables.
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

        for n in range(1, limit + 1):
            convolution = sum(self.mu[d] for d in range(1, n + 1)
                              if n % d == 0)
            require(convolution == (1 if n == 1 else 0),
                    "Mobius divisor convolution failed", n, convolution)

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

        lambda_error = arb(0)
        psi_error = arb(0)
        c_error = arb(0)
        h_error = arb(0)
        for n in range(1, limit + 1):
            lambda_from_mu = -arb_sum(
                self.mu[d] * self.logs[d] for d in range(1, n + 1)
                if n % d == 0
            )
            lambda_error += certify_zero(
                lambda_from_mu - self.Lambda[n],
                f"von Mangoldt divisor convolution n={n}",
            )
            psi_direct = arb_sum(self.Lambda[k] for k in range(1, n + 1))
            psi_error += certify_zero(
                self.psi[n] - psi_direct, f"psi direct prefix n={n}"
            )
            c_direct = arb_sum(
                self.Lambda[k] * (self.logs[n] - self.logs[k])
                for k in range(2, n)
            )
            c_error += certify_zero(
                self.C[n] - c_direct, f"C temporal versus direct n={n}"
            )
            if n < limit:
                h_n = 1 + self.ell[n] - self.logs[n] * arb_fraction(self.m[n])
                h_next = (
                    1 + self.ell[n + 1]
                    - self.logs[n + 1] * arb_fraction(self.m[n + 1])
                )
                delta_n = self.logs[n + 1] - self.logs[n]
                h_error += certify_zero(
                    h_n - h_next - delta_n * arb_fraction(self.m[n]),
                    f"endpoint h difference n={n}",
                )
        self.error_totals = {
            "lambda_convolution": certify_error_total(
                lambda_error, "all Lambda convolution errors"
            ),
            "psi_direct": certify_error_total(
                psi_error, "all psi direct-prefix errors"
            ),
            "C_direct": certify_error_total(
                c_error, "all C direct-prefix errors"
            ),
            "h_difference": certify_error_total(
                h_error, "all endpoint h difference errors"
            ),
        }


# ---------------------------------------------------------------------------
# Exact finite complete-prefix split and its two Abel formulas.
# ---------------------------------------------------------------------------


class ExactPrefixScale:
    def __init__(self, a: int, arithmetic: ArithmeticTables) -> None:
        require(a in DECLARED_SCALES, "undeclared scale", a)
        self.a = a
        self.M = 2 * a - 1
        self.stop = 2 * a
        self.arithmetic = arithmetic
        self.gram = RestrictedGram()
        self.theta = arb_fraction(THETA)
        self.tau = 1 - 2 * self.theta
        self.squarefree = tuple(
            d for d in range(1, self.stop) if arithmetic.mu[d] != 0
        )
        self.rows = tuple(
            q for q in range(a, self.stop)
            if arithmetic.mu[q] != 0 and 2 * q <= 3 * a
        )
        require(self.rows, "empty physical row set", a)
        require(self.rows == tuple(
            q for q in range(a, 3 * a // 2 + 1)
            if trial_mu(q) != 0
        ), "closed physical row set mismatch", a)

        self.delta: dict[int, arb] = {}
        self.w: dict[int, arb] = {}
        self.A: dict[int, arb] = {}
        self.eta: dict[int, arb] = {}
        self.kappa: dict[int, arb] = {}
        self.s: dict[int, arb] = {}
        self.R: dict[int, arb] = {}
        self.h: dict[int, arb] = {}
        for n in range(a, self.stop + 1):
            log_n = arithmetic.logs[n]
            self.h[n] = (
                1 + arithmetic.ell[n]
                - log_n * arb_fraction(arithmetic.m[n])
            )
            if n == self.stop:
                continue
            self.delta[n] = arithmetic.logs[n + 1] - log_n
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
        for n in range(self.M, a - 1, -1):
            log_n = arithmetic.logs[n]
            self.B2[n] = self.B2[n + 1] + self.kappa[n] / log_n ** 2
            self.B1[n] = (
                self.B1[n + 1] + self.kappa[n] * self.eta[n] / log_n
            )
            self.B0[n] = (
                self.B0[n + 1] + self.kappa[n] * self.eta[n] ** 2
            )

    def b(self, q: int, n: int) -> arb:
        return self.arithmetic.logs[q] / self.arithmetic.logs[n] - self.eta[n]

    def alpha(self, q: int, n: int) -> arb:
        return self.kappa[n] * self.b(q, n)

    def aterm(self, q: int, n: int) -> arb:
        return arb(n) / q - (arb(n + 1) / q).log()

    def ppacket(self, q: int, n: int) -> arb:
        ar = self.arithmetic
        weighted = ar.psi_weight_prefix[n] - ar.psi_weight_prefix[q - 1]
        return ar.C[n + 1] / q - weighted

    def B_direct(self, q: int) -> arb:
        ar = self.arithmetic
        return arb_sum(
            self.alpha(q, n) * (
                self.aterm(q, n) * self.R[n]
                + (ar.C[n + 1] - n) / (q * ar.logs[n])
                + (
                    (arb(n + 1) / q).log()
                    - (ar.psi_weight_prefix[n] - ar.psi_weight_prefix[q - 1])
                ) / ar.logs[n]
            )
            for n in range(q, self.stop)
        )

    def Pplus_direct(self, q: int) -> arb:
        ar = self.arithmetic
        return arb_sum(
            self.alpha(q, n) * self.ppacket(q, n) / ar.logs[n]
            for n in range(q, self.stop)
        )

    def Smu_direct(self, q: int) -> arb:
        return arb_sum(
            self.alpha(q, n) * self.aterm(q, n) * self.s[n]
            for n in range(q, self.stop)
        )

    def sigma(self, q: int) -> list[arb]:
        ar = self.arithmetic
        Sigma = [arb(0) for _ in range(self.stop + 1)]
        for m in range(self.M, q - 1, -1):
            Sigma[m] = Sigma[m + 1] + self.alpha(q, m) / ar.logs[m]
        return Sigma

    def Pplus_abel(self, q: int, Sigma: list[arb]) -> arb:
        ar = self.arithmetic
        answer = ar.C[q] * Sigma[q] / q
        for m in range(q, self.stop):
            coefficient = self.delta[m] / q - arb(1) / (m * (m + 1))
            answer += ar.psi[m] * coefficient * Sigma[m]
        return answer

    def Smu_abel(self, q: int, Sigma: list[arb]) -> arb:
        ar = self.arithmetic
        u: dict[int, arb] = {}
        omega: dict[int, arb] = {}
        for n in range(q, self.stop):
            alpha = self.alpha(q, n)
            aterm = self.aterm(q, n)
            u[n] = alpha * aterm * (1 - self.eta[n]) / self.delta[n]
            omega[n] = alpha * aterm / ar.logs[n]
            if n == q:
                omega[n] += u[n]
            else:
                omega[n] += u[n] - u[n - 1]

        answer = -(1 - arb(1) / q) * Sigma[q]
        answer += arb_sum(
            (self.delta[m] - arb(1) / q) * Sigma[m]
            for m in range(q, self.stop)
        )
        answer += arb_sum(omega[n] * self.h[n]
                          for n in range(q, self.stop))
        answer -= u[self.M] * self.h[self.stop]
        return answer

    def split_row(self, q: int) -> dict[str, arb]:
        require(q in self.rows, "row is outside declared physical set", self.a, q)
        alpha_error = arb(0)
        alpha_floor = arb_fraction(ALPHA_FLOOR)
        require(q < self.stop, "empty temporal row", self.a, q)
        for n in range(q, self.stop):
            alpha = self.alpha(q, n)
            certify_positive(alpha, f"alpha>0 a={self.a} q={q} n={n}")
            require(alpha > alpha_floor,
                    "declared uniform alpha floor false or unresolved",
                    self.a, q, n, alpha, alpha_floor)
            alpha_error += certify_zero(
                alpha - self.kappa[n] * self.b(q, n),
                f"alpha definition a={self.a} q={q} n={n}",
            )

        Sigma = self.sigma(q)
        B = self.B_direct(q)
        Pplus = self.Pplus_direct(q)
        Smu = self.Smu_direct(q)
        Pplus_abel = self.Pplus_abel(q, Sigma)
        Smu_abel = self.Smu_abel(q, Sigma)
        return {
            "B": B,
            "Pplus": Pplus,
            "Smu": Smu,
            "Pplus_abel": Pplus_abel,
            "Smu_abel": Smu_abel,
            "alpha_definition_error": certify_error_total(
                alpha_error, f"all alpha definition errors a={self.a} q={q}"
            ),
            "B_split_error": certify_zero(
                B - Pplus - Smu,
                f"B=Pplus+Smu a={self.a} q={q}",
            ),
            "Pplus_abel_error": certify_zero(
                Pplus - Pplus_abel,
                f"Pplus direct versus Abel a={self.a} q={q}",
            ),
            "Smu_abel_error": certify_zero(
                Smu - Smu_abel,
                f"Smu direct versus Abel a={self.a} q={q}",
            ),
        }

    def physical_hat_H(self, q: int, B: arb) -> tuple[arb, arb]:
        ar = self.arithmetic
        spatial_u = arb(0)
        spatial_d = arb(0)
        index = 0
        hat = arb(0)
        H = arb(0)
        g_q = self.gram.chi_cross(q)
        for n in range(q, self.stop):
            while index < len(self.squarefree) and self.squarefree[index] <= n:
                d = self.squarefree[index]
                gram_qd = self.gram.entry(q, d)
                spatial_u += ar.mu[d] * gram_qd
                spatial_d += ar.mu[d] * ar.logs[d] * gram_qd
                index += 1
            K_qn = (
                spatial_d / ar.logs[n]
                - self.eta[n] * (g_q + spatial_u)
            )
            alpha_qn = self.alpha(q, n)
            B_qn = (
                self.aterm(q, n) * self.R[n]
                + (ar.C[n + 1] - n) / (q * ar.logs[n])
                + (
                    (arb(n + 1) / q).log()
                    - (ar.psi_weight_prefix[n] - ar.psi_weight_prefix[q - 1])
                ) / ar.logs[n]
            )
            hat += alpha_qn * K_qn
            H += alpha_qn * (K_qn - B_qn)
        certify_zero(hat - B - H,
                     f"physical hat=B+H a={self.a} q={q}")
        return hat, H

    def physical_hat_column(self, q: int) -> arb:
        ar = self.arithmetic
        log_q = ar.logs[q]
        answer = -self.gram.chi_cross(q) * (
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
            answer += ar.mu[d] * self.gram.entry(q, d) * temporal
        return answer


def verify_closure_unchanged() -> None:
    verify_runtime()
    require(ctx.prec == BITS, "Arb precision changed", ctx.prec, BITS)
    _safe_regular_file(SCRIPT_PATH)
    require(SCRIPT_PATH.read_bytes() == _SCRIPT_BYTES,
            "certificate source mutated after capture", SCRIPT_PATH)
    require(sha256_bytes(_SCRIPT_BYTES) == _SCRIPT_SHA256,
            "captured certificate source hash changed")
    for path, expected in EXPECTED_INPUT_SHA256.items():
        _safe_regular_file(path)
        current = path.read_bytes()
        require(current == _CAPTURED_INPUTS[path],
                "bound input mutated after capture", path)
        require(sha256_bytes(current) == expected,
                "bound input hash changed after capture", path)
    _reject_repository_import_artifacts()


def main() -> None:
    arithmetic = ArithmeticTables(MAX_N)
    scale218 = ExactPrefixScale(218, arithmetic)
    scale301 = ExactPrefixScale(301, arithmetic)
    require(COUNTEREXAMPLE[1] in scale218.rows,
            "counterexample row excluded by physical row rule", COUNTEREXAMPLE)
    require(len(scale301.rows) == 93,
            "unexpected a=301 physical row count", len(scale301.rows))

    # Every declared physical row gets alpha positivity, the direct split, and
    # both independent finite Abel identities.  No sampled-row inference.
    rows218 = {q: scale218.split_row(q) for q in scale218.rows}
    rows301 = {q: scale301.split_row(q) for q in scale301.rows}
    alpha_positive_cells = (
        sum(scale218.stop - q for q in scale218.rows)
        + sum(scale301.stop - q for q in scale301.rows)
    )
    require(alpha_positive_cells == 31_847,
            "unexpected declared alpha-positive cell count",
            alpha_positive_cells)

    q_counter = COUNTEREXAMPLE[1]
    counter = rows218[q_counter]
    counter_hat, counter_H = scale218.physical_hat_H(q_counter, counter["B"])
    counter_hat_column = scale218.physical_hat_column(q_counter)
    counter_hat_path_error = certify_zero(
        counter_hat - counter_hat_column,
        "counterexample temporal versus coefficient-index physical hat",
    )
    certify_negative(counter["B"], "counterexample B<0")
    certify_positive(counter_H, "counterexample H>0")
    certify_positive(counter_hat, "counterexample hat>0")
    certify_negative(counter["B"] * counter_hat,
                     "counterexample B*hat<0")
    certify_negative(counter["B"] * counter_H,
                     "counterexample B*H<0")

    # Complete physical aggregate at a=301, over the exact 93 closed-I0 rows.
    H301: dict[int, arb] = {}
    hat301: dict[int, arb] = {}
    hat_path_error301 = arb(0)
    for q in scale301.rows:
        hat, H = scale301.physical_hat_H(q, rows301[q]["B"])
        column = scale301.physical_hat_column(q)
        hat_path_error301 += certify_zero(
            hat - column,
            f"a=301 temporal versus coefficient-index physical hat q={q}",
        )
        hat301[q] = hat
        H301[q] = H
    hat_path_error301 = certify_error_total(
        hat_path_error301, "a=301 all physical hat path errors"
    )

    p = arb_sum(rows301[q]["B"] ** 2 for q in scale301.rows)
    BH = arb_sum(rows301[q]["B"] * H301[q] for q in scale301.rows)
    H2 = arb_sum(H301[q] ** 2 for q in scale301.rows)
    D = arb_sum(hat301[q] ** 2 for q in scale301.rows)
    certify_positive(p, "a=301 p=||B||^2>0")
    certify_negative(BH, "a=301 <B,H><0")
    certify_positive(D, "a=301 D>0")
    gamma = (p + BH) / p
    certify_positive(gamma, "a=301 gamma>0")
    Qcp = (p + BH) ** 2 / p
    certify_positive(Qcp, "a=301 Qcp>0")
    aggregate_energy_error = certify_zero(
        D - (p + 2 * BH + H2), "a=301 D=p+2BH+H2"
    )
    aggregate_projection_error = certify_zero(
        Qcp - gamma ** 2 * p, "a=301 Qcp=gamma^2*p"
    )
    aggregate_dot_error = certify_zero(
        arb_sum(rows301[q]["B"] * hat301[q] for q in scale301.rows)
        - (p + BH),
        "a=301 <B,hat>=p+BH",
    )

    split_errors = certify_error_total(
        arb_sum(row["B_split_error"] for row in rows218.values())
        + arb_sum(row["B_split_error"] for row in rows301.values()),
        "all declared B split errors",
    )
    pplus_errors = certify_error_total(
        arb_sum(row["Pplus_abel_error"] for row in rows218.values())
        + arb_sum(row["Pplus_abel_error"] for row in rows301.values()),
        "all declared Pplus Abel errors",
    )
    smu_errors = certify_error_total(
        arb_sum(row["Smu_abel_error"] for row in rows218.values())
        + arb_sum(row["Smu_abel_error"] for row in rows301.values()),
        "all declared Smu Abel errors",
    )
    alpha_errors = certify_error_total(
        arb_sum(row["alpha_definition_error"] for row in rows218.values())
        + arb_sum(row["alpha_definition_error"] for row in rows301.values()),
        "all declared alpha definition errors",
    )

    verify_closure_unchanged()

    lines: list[str] = []
    emit = lines.append
    emit("RH CYCLE 49 EXACT FINITE PREFIX CERTIFICATE: PASS")
    emit("scope=160 finite physical rows at a=218,301 on closed I0=[1,3/2]; asymptotics untested; no RH inference")
    emit(f"source={SCRIPT_PATH.relative_to(WORKSPACE)}")
    emit(f"source_sha256={_SCRIPT_SHA256}")
    emit(f"captured_closure_manifest_sha256={_CLOSURE_SHA256}")
    emit("source_capture=certificate and all local inputs are read and SHA-256-bound before first third-party import")
    emit("runtime=CPython-3.12.13 python-flint-0.9.0 FLINT-3.6.0")
    emit("trusted_runtime_boundary=versions are pinned; interpreter/wheel/native-library binaries, OS, hardware, and uv launcher are not binary-attested")
    emit(f"arb_precision_bits={BITS} identity_error_ceiling={interval(identity_ceiling(), 18)}")
    emit("canonical_command=rm -f /tmp/cycle49-exact-prefix-certificate.out && env -u PYTHONPYCACHEPREFIX PYTHONDONTWRITEBYTECODE=1 LC_ALL=C uv run --isolated --no-project --python 3.12.13 --with python-flint==0.9.0 python -I -B millennium-prize/riemann-hypothesis/cycle49_exact_prefix_certificate.py > /tmp/cycle49-exact-prefix-certificate.out && cmp /tmp/cycle49-exact-prefix-certificate.out millennium-prize/riemann-hypothesis/cycle49-exact-prefix-certificate.out")
    emit("parameters=theta=2/5 scales=218,301 temporal_endpoint=M=2a-1 I0=[1,3/2]")
    emit("row_rule=squarefree q with a<=q<2a and 2q<=3a; both I0 endpoints closed")
    emit("definitions=aterm(q,n)=n/q-log((n+1)/q); s_n=ell_n/L_n-eta_n*m_n; ppacket(q,n)=C[n+1]/q-sum_{k=q}^n psi(k)/(k(k+1))")
    emit("split=B=sum_n alpha*(aterm*R+(C[n+1]-n)/(qL_n)+j/L_n)=Pplus+Smu; Pplus=sum_n alpha*ppacket/L_n; Smu=sum_n alpha*aterm*s_n")
    emit("abel_checks=Pplus and Smu each checked against independent finite suffix-summation formulas including -u(q,M)h_(2a)")
    emit("physical_terms=affine -eta_n*chi retained; restricted Gram correction -1/(qd) retained; every Mobius sign retained")
    emit(f"bound_inputs_sha256=PASS count={len(EXPECTED_INPUT_SHA256)}")
    for path, expected in EXPECTED_INPUT_SHA256.items():
        emit(f"input_sha256 {path.relative_to(WORKSPACE)} {expected}")
    for label, value in arithmetic.error_totals.items():
        emit(f"arithmetic_identity_error_sum_upper {label}={interval(value, 18)}")
    emit(f"finite_row_checks=PASS rows_a218=67 rows_a301=93 alpha_positive_cells={alpha_positive_cells} alpha_uniform_floor=1/1000000 B_split_rows=160 Pplus_Abel_rows=160 Smu_Abel_rows=160")
    emit(f"identity_error_sums_upper alpha_definition={interval(alpha_errors, 18)} B_split={interval(split_errors, 18)} Pplus_Abel={interval(pplus_errors, 18)} Smu_Abel={interval(smu_errors, 18)}")
    emit("counterexample a=218 q=327 alpha_certified_gt=1/1000000")
    for label in ("B", "Pplus", "Smu", "Pplus_abel", "Smu_abel"):
        emit(f"  {label} {interval(counter[label])}")
    emit(f"  H {interval(counter_H)}")
    emit(f"  hat {interval(counter_hat)}")
    emit(f"  B_times_hat {interval(counter['B'] * counter_hat)}")
    emit(f"  B_times_H {interval(counter['B'] * counter_H)}")
    emit(f"  physical_hat_path_error_upper {interval(counter_hat_path_error, 18)}")
    emit("counterexample_signs=PASS B<0 H>0 hat>0 B*hat<0 B*H<0")
    emit("aggregate a=301 I0=[1,3/2] rows=93 p_definition=||B||^2 BH_definition=<B,H> gamma=(p+BH)/p Qcp=(p+BH)^2/p")
    emit(f"  p {interval(p)}")
    emit(f"  BH {interval(BH)}")
    emit(f"  gamma {interval(gamma)}")
    emit(f"  D {interval(D)}")
    emit(f"  Qcp {interval(Qcp)}")
    emit(f"  H2 {interval(H2)}")
    emit(f"  physical_hat_path_error_sum_upper {interval(hat_path_error301, 18)}")
    emit(f"  aggregate_energy_error_upper {interval(aggregate_energy_error, 18)}")
    emit(f"  aggregate_projection_error_upper {interval(aggregate_projection_error, 18)}")
    emit(f"  aggregate_dot_error_upper {interval(aggregate_dot_error, 18)}")
    emit("aggregate_signs=PASS p>0 BH<0 gamma>0 D>0 Qcp>0")
    emit("finite_only_disclaimer=Asymptotics are untested. No untested scale, eventual sign, asymptotic lower bound, positive liminf, moving-projection theorem, completed-square budget, or Riemann-hypothesis conclusion is certified.")
    emit("ASYMPTOTICS_UNTESTED")
    emit("ALL_DECLARED_CHECKS_PASS")

    verify_closure_unchanged()
    sys.stdout.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
