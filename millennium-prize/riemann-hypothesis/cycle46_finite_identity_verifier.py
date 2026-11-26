#!/usr/bin/env python3
"""Fail-closed read-only verifier for the finite RH Cycle 46 identities.

Scope:
  * exact squarefree fixed-P grouping and adjoining-prime identities;
  * outward-Arb grouped diagonals at a=64, I=[1,3/2];
  * outward-Arb first-period/tail reconstruction at a=512, q=742;
  * exact Fraction/formal-log convolution and Abel tests.

This is a finite identity/counterexample certificate.  It proves no asymptotic
retention estimate, moving-projection theorem, or RH consequence.
"""

from __future__ import annotations

import hashlib
from fractions import Fraction
from math import gcd
import os
from pathlib import Path
import platform
import sys
import types

# The certified command runs Python with -I -B.  Isolated/safe-path mode keeps
# repository shadows out of bootstrap imports; -B forbids bytecode writes.
sys.dont_write_bytecode = True

RH_DIR = Path(__file__).resolve().parent
WORKSPACE = RH_DIR.parent.parent
LOCAL_MODULES = (
    "certify_complete_gram",
    "cycle45_runtime",
    "cycle43_divisor_admission_multiprobe",
    "cycle44_boundary_envelope_scan",
    "cycle45_dispersion_census",
)
BOOTSTRAP_SHADOWS = (
    "hashlib", "fractions", "math", "os", "pathlib", "platform",
    "sys", "types", "flint",
)

BITS = 256
A_GROUP = 64
I_LO = Fraction(1, 1)
I_HI = Fraction(3, 2)
A_COUNTEREXAMPLE = 512
Q_COUNTEREXAMPLE = 742
FORMAL_CONVOLUTION_LIMIT = 160
FORMAL_ABEL_LIMIT = 120

# Bind the complete local source closure used by the imported Cycle 45 data
# object.  Preflight runs before those modules are imported or executed.
EXPECTED_SHA256 = {
    RH_DIR / "cycle45_dispersion_census.py":
        "9f24a6630a8804996590732d8a6f6389557a296eacb7daedc5fc56cb38152ade",
    RH_DIR / "certify_complete_gram.py":
        "9b87a6e35cbb7adf5041442410e74346aa79c2a29d495df1a9ee93c17b35c9b8",
    RH_DIR / "cycle45_runtime.py":
        "78840c42dec562ff177a7b54ca4e223f9d9d3d300c6029f2909a9d7467d6ec31",
    RH_DIR / "cycle43_divisor_admission_multiprobe.py":
        "ba3453913affeaa9c99aea24c10d67cee6dfbd8635f67ff86dfa2975e18811c3",
    RH_DIR / "cycle44_boundary_envelope_scan.py":
        "d94ecc10c941668d0f5e335527ffe5c9524a6ab0a8df748425e5f67d445cac5b",
    RH_DIR / "cycle45-dispersion-environment.json":
        "a88cfbecae577f3cfb206769458113494b5bb2b4b783fdd4e46b71542434456b",
}


def _reject_import_artifacts(name: str, *, bound_source: bool) -> None:
    candidates = [
        RH_DIR / name,
        RH_DIR / f"{name}.pyc",
        RH_DIR / f"{name}.pyo",
    ]
    # A LOCAL_MODULES source is the one canonical, hash-bound artifact loaded
    # below.  Bootstrap names have no allowed local source at all.
    if not bound_source:
        candidates.append(RH_DIR / f"{name}.py")
    for path in candidates:
        if path.exists():
            raise RuntimeError(("competing local import artifact", path))

    cache = RH_DIR / "__pycache__"
    if cache.exists():
        matches = tuple(cache.glob(f"{name}.*.pyc")) + \
            tuple(cache.glob(f"{name}.*.pyo"))
        if matches:
            raise RuntimeError(("competing local bytecode artifact", matches))

    for suffix in (".so", ".pyd", ".dll", ".dylib"):
        matches = tuple(RH_DIR.glob(f"{name}*{suffix}"))
        if matches:
            raise RuntimeError(("competing local extension artifact", matches))


def _preflight_source_closure() -> dict[str, bytes]:
    if not sys.flags.isolated or not sys.flags.safe_path:
        raise RuntimeError("run with python -I")
    if not sys.flags.dont_write_bytecode:
        raise RuntimeError("run with python -B")
    if sys.flags.optimize != 0:
        raise RuntimeError("optimized Python is forbidden")
    if os.environ.get("PYTHONPYCACHEPREFIX"):
        raise RuntimeError("PYTHONPYCACHEPREFIX must be unset")

    for name in LOCAL_MODULES:
        _reject_import_artifacts(name, bound_source=True)
    for name in BOOTSTRAP_SHADOWS:
        _reject_import_artifacts(name, bound_source=False)

    sources: dict[str, bytes] = {}
    for path, expected in EXPECTED_SHA256.items():
        if not path.is_file():
            raise RuntimeError(("missing bound input", path))
        source = path.read_bytes()
        observed = hashlib.sha256(source).hexdigest()
        if observed != expected:
            raise RuntimeError(("bound input hash mismatch", path,
                                observed, expected))
        if path.suffix == ".py":
            sources[path.stem] = source
    return sources


_BOUND_SOURCES = _preflight_source_closure()

# Import the external numerical package while no repository path is exposed.
import flint  # noqa: E402
from flint import arb, ctx  # noqa: E402

_flint_origin = Path(flint.__file__).resolve()
if _flint_origin == RH_DIR or RH_DIR in _flint_origin.parents:
    raise RuntimeError(("local flint shadow loaded", _flint_origin))


def _exec_bound_module(name: str) -> types.ModuleType:
    path = RH_DIR / f"{name}.py"
    source = _BOUND_SOURCES[name]
    module = types.ModuleType(name)
    module.__file__ = str(path)
    module.__package__ = ""
    module.__loader__ = None
    module.__spec__ = None
    sys.modules[name] = module
    try:
        code = compile(source, str(path), "exec", dont_inherit=True,
                       optimize=0)
        exec(code, module.__dict__)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return module


_BOUND_MODULES = {name: _exec_bound_module(name) for name in LOCAL_MODULES}
mobius_sieve = _BOUND_MODULES["certify_complete_gram"].mobius_sieve
DispersionData = _BOUND_MODULES["cycle45_dispersion_census"].DispersionData
arb_sum = _BOUND_MODULES["cycle45_dispersion_census"].arb_sum
require_exact_runtime = _BOUND_MODULES["cycle45_runtime"].require_exact_runtime


def fail(label: str, *details: object) -> None:
    raise RuntimeError((label,) + details)


def require(condition: bool, label: str, *details: object) -> None:
    if not condition:
        fail(label, *details)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_inputs() -> None:
    # Repeat hashes after executing the already captured bytes so any
    # in-process source mutation also aborts before a certificate is printed.
    for path, expected in EXPECTED_SHA256.items():
        require(path.is_file(), "missing bound input", path)
        observed = sha256_file(path)
        require(observed == expected, "bound input hash mismatch",
                path, observed, expected)
    require(platform.python_version() == "3.12.13",
            "unexpected Python version", platform.python_version())
    require(flint.__version__ == "0.9.0", "unexpected python-flint",
            flint.__version__)
    require(flint.__FLINT_VERSION__ == "3.6.0", "unexpected FLINT",
            flint.__FLINT_VERSION__)
    require(sys.flags.isolated and sys.flags.safe_path,
            "Python isolation flags changed", sys.flags)
    require(sys.flags.dont_write_bytecode and sys.flags.optimize == 0,
            "Python bytecode/optimization flags changed", sys.flags)


def require_arb(value: arb, label: str) -> arb:
    require(isinstance(value, arb), "not an Arb value", label, type(value))
    require(value.is_finite(), "nonfinite Arb value", label, value)
    return value


def identity_ceiling() -> arb:
    # Reject broad zero-containing balls.  At 256 bits this is 2^-128.
    return arb(2) ** (-(BITS // 2))


def certify_zero(value: arb, label: str) -> arb:
    require_arb(value, label)
    require(value.contains(0), "identity ball excludes zero", label, value)
    upper = abs(value).upper()
    require_arb(upper, label + " absolute upper bound")
    ceiling = identity_ceiling()
    require(upper <= ceiling, "identity ball too wide", label, value,
            ceiling)
    return upper


def certify_positive(value: arb, label: str) -> arb:
    require_arb(value, label)
    require(value > 0, "positive sign unresolved or false", label, value)
    return value


def certify_negative(value: arb, label: str) -> arb:
    require_arb(value, label)
    require(value < 0, "negative sign unresolved or false", label, value)
    return value


def interval(value: arb, digits: int = 40) -> str:
    require_arb(value, "serialized interval")
    return value.str(digits)


def arb_fraction(value: Fraction) -> arb:
    return arb(value.numerator) / value.denominator


# ---------------------------------------------------------------------------
# Independent exact integer/Fraction arithmetic.
# ---------------------------------------------------------------------------


def factorization(n: int) -> dict[int, int]:
    require(isinstance(n, int) and n >= 1, "invalid factorization input", n)
    answer: dict[int, int] = {}
    x = n
    p = 2
    while p * p <= x:
        while x % p == 0:
            answer[p] = answer.get(p, 0) + 1
            x //= p
        p += 1
    if x > 1:
        answer[x] = answer.get(x, 0) + 1
    return answer


def exact_mu(n: int) -> int:
    factors = factorization(n)
    if any(exponent > 1 for exponent in factors.values()):
        return 0
    return -1 if len(factors) % 2 else 1


def is_prime(n: int) -> bool:
    return n >= 2 and factorization(n) == {n: 1}


def prime_power_base(n: int) -> int | None:
    if n < 2:
        return None
    factors = factorization(n)
    if len(factors) != 1:
        return None
    return next(iter(factors))


def divisors(n: int) -> tuple[int, ...]:
    return tuple(d for d in range(1, n + 1) if n % d == 0)


def rough_labels(N: int, P: int) -> tuple[int, ...]:
    return tuple(r for r in range(1, N)
                 if exact_mu(r) != 0 and gcd(r, P) == 1)


def add_map(target: dict, source: dict, scale: Fraction = Fraction(1)) -> None:
    for key, value in source.items():
        new_value = target.get(key, Fraction(0)) + scale * value
        if new_value:
            target[key] = new_value
        elif key in target:
            del target[key]


def grouped_formal_column(N: int, P: int, r: int) -> dict[int, Fraction]:
    require(exact_mu(P) != 0, "P is not squarefree", P)
    if not (1 <= r < N and exact_mu(r) != 0 and gcd(r, P) == 1):
        return {}
    answer: dict[int, Fraction] = {}
    for s in divisors(P):
        d = s * r
        if d < N:
            answer[d] = answer.get(d, Fraction(0)) + Fraction(exact_mu(s))
    return {key: value for key, value in answer.items() if value}


def canonical_pair(a: int, b: int) -> tuple[int, int]:
    return (a, b) if a <= b else (b, a)


def product_polynomial(left: dict[int, Fraction],
                       right: dict[int, Fraction]) -> dict[tuple[int, int], Fraction]:
    answer: dict[tuple[int, int], Fraction] = {}
    for d, x in left.items():
        for e, y in right.items():
            key = canonical_pair(d, e)
            answer[key] = answer.get(key, Fraction(0)) + x * y
    return {key: value for key, value in answer.items() if value}


def grouped_diagonal_polynomial(N: int, P: int) -> dict[tuple[int, int], Fraction]:
    answer: dict[tuple[int, int], Fraction] = {}
    for r in rough_labels(N, P):
        add_map(answer,
                product_polynomial(grouped_formal_column(N, P, r),
                                   grouped_formal_column(N, P, r)))
    return answer


def exact_grouping_and_increment_tests() -> tuple[int, int, int]:
    # First compare the imported sieve with an independent factorization.
    imported_mu = mobius_sieve(200)
    for n in range(1, 201):
        require(imported_mu[n] == exact_mu(n),
                "independent Mobius mismatch", n, imported_mu[n], exact_mu(n))

    grouping_cases = 0
    increment_cases = 0
    polynomial_cases = 0
    fixed_P = (1, 2, 3, 5, 6, 10, 15, 30)
    adjoining = ((1, 2), (1, 3), (2, 3), (2, 5),
                 (3, 2), (6, 5), (10, 3), (15, 2))

    for N in range(2, 65):
        expected = {d: Fraction(exact_mu(d))
                    for d in range(1, N) if exact_mu(d) != 0}
        for P in fixed_P:
            aggregate: dict[int, Fraction] = {}
            for r in rough_labels(N, P):
                add_map(aggregate, grouped_formal_column(N, P, r),
                        Fraction(exact_mu(r)))
            require(aggregate == expected, "formal squarefree grouping failed",
                    N, P, aggregate, expected)
            grouping_cases += 1

        for P, p in adjoining:
            require(is_prime(p) and P % p != 0 and exact_mu(P) != 0,
                    "invalid adjoining test fixture", P, p)
            Q = P * p
            for r in rough_labels(N, Q):
                lhs = grouped_formal_column(N, Q, r)
                rhs = grouped_formal_column(N, P, r).copy()
                add_map(rhs, grouped_formal_column(N, P, p * r), Fraction(-1))
                require(lhs == rhs, "formal adjoining-column identity failed",
                        N, P, p, r, lhs, rhs)
                increment_cases += 1

            lhs_poly = grouped_diagonal_polynomial(N, Q)
            add_map(lhs_poly, grouped_diagonal_polynomial(N, P), Fraction(-1))
            rhs_poly: dict[tuple[int, int], Fraction] = {}
            for r in rough_labels(N, Q):
                if p * r < N:
                    add_map(
                        rhs_poly,
                        product_polynomial(
                            grouped_formal_column(N, P, r),
                            grouped_formal_column(N, P, p * r),
                        ),
                        Fraction(-2),
                    )
            require(lhs_poly == rhs_poly,
                    "formal adjoining diagonal-increment identity failed",
                    N, P, p, lhs_poly, rhs_poly)
            polynomial_cases += 1

    return grouping_cases, increment_cases, polynomial_cases


def factor_vector(n: int) -> dict[int, Fraction]:
    return {p: Fraction(exponent)
            for p, exponent in factorization(n).items() if exponent}


def formal_add(left: dict, right: dict,
               scale: Fraction = Fraction(1)) -> dict:
    answer = left.copy()
    add_map(answer, right, scale)
    return answer


def formal_tensor(left: dict[int, Fraction],
                  right: dict[int, Fraction]) -> dict[tuple[int, int], Fraction]:
    answer: dict[tuple[int, int], Fraction] = {}
    for p, x in left.items():
        for r, y in right.items():
            key = (p, r)
            answer[key] = answer.get(key, Fraction(0)) + x * y
    return {key: value for key, value in answer.items() if value}


def exact_convolution_and_abel_tests() -> tuple[int, int, int]:
    mu = [0] + [exact_mu(n) for n in range(1, FORMAL_CONVOLUTION_LIMIT + 1)]
    convolution_cases = 0
    for k in range(1, FORMAL_CONVOLUTION_LIMIT + 1):
        # sum mu(d) floor(k/d) = 1.
        scalar = sum(mu[d] * (k // d) for d in range(1, k + 1))
        require(scalar == 1, "Mobius convolution failed", k, scalar)

        # -sum mu(d) log(d) floor(k/d) = psi(k), as a formal
        # coefficient identity in the symbols log(p).
        lhs: dict[int, Fraction] = {}
        for d in range(1, k + 1):
            add_map(lhs, factor_vector(d), Fraction(-mu[d] * (k // d)))
        rhs: dict[int, Fraction] = {}
        for m in range(2, k + 1):
            p = prime_power_base(m)
            if p is not None:
                rhs[p] = rhs.get(p, Fraction(0)) + 1
        require(lhs == rhs, "logarithmic Chebyshev convolution failed",
                k, lhs, rhs)
        convolution_cases += 1

    abel_cases = 0
    for q in range(1, FORMAL_ABEL_LIMIT + 1):
        # Formal version of
        # sum_{k<q} psi(k) log((k+1)/k)
        #   = sum_{m<q} Lambda(m) log(q/m).
        left: dict[tuple[int, int], Fraction] = {}
        psi: dict[int, Fraction] = {}
        for k in range(1, q):
            p = prime_power_base(k)
            if p is not None:
                psi[p] = psi.get(p, Fraction(0)) + 1
            log_ratio = formal_add(factor_vector(k + 1), factor_vector(k),
                                   Fraction(-1))
            add_map(left, formal_tensor(psi, log_ratio))

        right: dict[tuple[int, int], Fraction] = {}
        for m in range(2, q):
            p = prime_power_base(m)
            if p is None:
                continue
            log_ratio = formal_add(factor_vector(q), factor_vector(m),
                                   Fraction(-1))
            add_map(right, formal_tensor({p: Fraction(1)}, log_ratio))
        require(left == right, "formal first-period Abel telescope failed",
                q, left, right)
        abel_cases += 1

    # Also test the finite coprime-Mertens Abel identity with exact rational
    # weights.  This is independent of formal prime logarithms.
    coprime_abel_cases = 0
    for q in range(1, 21):
        for X in range(1, 31):
            weights = {r: Fraction(r * r + 3 * r + 1, 2 * r + 1)
                       for r in range(1, X + 1)}
            direct = sum((Fraction(exact_mu(r)) * weights[r]
                          for r in range(1, X + 1) if gcd(r, q) == 1),
                         Fraction(0))
            cumulative: dict[int, int] = {}
            total = 0
            for r in range(1, X + 1):
                if gcd(r, q) == 1:
                    total += exact_mu(r)
                cumulative[r] = total
            telescoped = Fraction(cumulative[X]) * weights[X]
            telescoped += sum(
                (Fraction(cumulative[r]) * (weights[r] - weights[r + 1])
                 for r in range(1, X)),
                Fraction(0),
            )
            require(direct == telescoped,
                    "exact coprime-Mertens Abel identity failed",
                    q, X, direct, telescoped)
            coprime_abel_cases += 1

    return convolution_cases, abel_cases, coprime_abel_cases


# ---------------------------------------------------------------------------
# Outward-Arb grouped diagonals and adjoining-prime identities.
# ---------------------------------------------------------------------------


def physical_rows(data: DispersionData) -> tuple[int, ...]:
    return tuple(q for q in data.squarefree
                 if I_LO <= Fraction(q, data.start) <= I_HI)


def arb_vector_zero(length: int) -> tuple[arb, ...]:
    return tuple(arb(0) for _ in range(length))


def add_arb_vectors(left: tuple[arb, ...], right: tuple[arb, ...],
                    scale: int = 1) -> tuple[arb, ...]:
    require(len(left) == len(right), "Arb vector length mismatch")
    return tuple(x + scale * y for x, y in zip(left, right))


def dot_arb(left: tuple[arb, ...], right: tuple[arb, ...]) -> arb:
    require(len(left) == len(right), "Arb dot-product length mismatch")
    return arb_sum(x * y for x, y in zip(left, right))


def grouped_arb_column(data: DispersionData, rows: tuple[int, ...],
                       P: int, r: int) -> tuple[arb, ...]:
    N = data.stop
    if not (1 <= r < N and data.mu[r] != 0 and gcd(r, P) == 1):
        return arb_vector_zero(len(rows))
    return tuple(
        arb_sum(exact_mu(s) * data.W(q, s * r)
                for s in divisors(P) if s * r < N)
        for q in rows
    )


def grouped_arb_data(data: DispersionData, rows: tuple[int, ...], P: int):
    groups = {r: grouped_arb_column(data, rows, P, r)
              for r in rough_labels(data.stop, P)}
    beta2 = arb_sum(data.beta(q) ** 2 for q in rows)
    delta = beta2 + arb_sum(dot_arb(vector, vector)
                            for vector in groups.values())
    certify_positive(delta, f"Delta P={P}")

    direct = tuple(
        arb_sum(data.mu[d] * data.W(q, d) for d in data.squarefree)
        for q in rows
    )
    grouped = arb_vector_zero(len(rows))
    for r, vector in groups.items():
        grouped = add_arb_vectors(grouped, vector, data.mu[r])
    all_error_upper_bound = arb(0)
    for index, (x, y) in enumerate(zip(direct, grouped)):
        upper = certify_zero(x - y, f"physical grouping P={P}, row={rows[index]}")
        # A sum of nonnegative outward upper bounds is itself an outward
        # upper bound for every individual error.  Avoid midpoint/max choices.
        all_error_upper_bound += upper
    return delta, groups, all_error_upper_bound


def verify_grouped_diagonals():
    data = DispersionData(A_GROUP, BITS)
    rows = physical_rows(data)
    require(rows, "empty grouped-diagonal row set")
    require(all(data.mu[q] != 0 for q in rows),
            "nonsquarefree physical row admitted")

    result = {}
    for P in (2, 6, 10):
        result[P] = grouped_arb_data(data, rows, P)

    delta2, groups2, err2 = result[2]
    delta6, groups6, err6 = result[6]
    delta10, groups10, err10 = result[10]

    down_gap = certify_positive(delta2 - delta6,
                                "adjoining 3 must decrease Delta: P=2 to 6")
    up_gap = certify_positive(delta10 - delta2,
                              "adjoining 5 must increase Delta: P=2 to 10")

    increment_errors = {}
    column_errors = {}
    for p, Q, deltaQ, groupsQ in (
            (3, 6, delta6, groups6),
            (5, 10, delta10, groups10)):
        all_column_error_upper_bound = arb(0)
        for r in rough_labels(data.stop, Q):
            rhs = groups2[r]
            if p * r < data.stop:
                rhs = add_arb_vectors(rhs, groups2[p * r], -1)
            for index, (x, y) in enumerate(zip(groupsQ[r], rhs)):
                upper = certify_zero(
                    x - y,
                    f"actual adjoining column 2->{Q}, r={r}, row={rows[index]}",
                )
                all_column_error_upper_bound += upper
        column_errors[Q] = all_column_error_upper_bound

        cross = arb_sum(
            dot_arb(groups2[r], groups2[p * r])
            for r in rough_labels(data.stop, Q) if p * r < data.stop
        )
        residual = (deltaQ - delta2) + 2 * cross
        increment_errors[Q] = certify_zero(
            residual, f"actual adjoining diagonal increment 2->{Q}"
        )

    return {
        "rows": rows,
        "delta2": delta2,
        "delta6": delta6,
        "delta10": delta10,
        "down_gap": down_gap,
        "up_gap": up_gap,
        "group_errors": (err2, err6, err10),
        "column_errors": column_errors,
        "increment_errors": increment_errors,
    }


# ---------------------------------------------------------------------------
# Outward-Arb first-period/tail reconstruction.
# ---------------------------------------------------------------------------


def verify_first_period_counterexample():
    data = DispersionData(A_COUNTEREXAMPLE, BITS)
    q = Q_COUNTEREXAMPLE
    N = data.stop
    require(q == 2 * 7 * 53, "counterexample factorization fixture changed", q)
    require(exact_mu(q) != 0 and data.mu[q] == exact_mu(q),
            "counterexample row is not squarefree", q, data.mu[q])
    require(data.start <= q < data.stop, "counterexample row outside block", q)

    # Exact rational m_n and outward-Arb logarithmic moment ell_n.
    m_prefix = [Fraction(0) for _ in range(N)]
    ell_prefix = [arb(0) for _ in range(N)]
    m_current = Fraction(0)
    ell_current = arb(0)
    for n in range(1, N):
        mu_n = exact_mu(n)
        require(mu_n == data.mu[n], "Mobius mismatch in counterexample", n)
        if mu_n:
            m_current += Fraction(mu_n, n)
            ell_current += mu_n * data.logs[n] / n
        m_prefix[n] = m_current
        ell_prefix[n] = ell_current

    # Formal von Mangoldt values evaluated as exact prime logarithms in Arb.
    Lambda = [arb(0) for _ in range(N)]
    for m in range(2, N):
        p = prime_power_base(m)
        if p is not None:
            Lambda[m] = data.logs[p]

    C_q = arb_sum(Lambda[m] * (data.logs[q] - data.logs[m])
                  for m in range(2, q))
    E_q = C_q - (q - 1)

    # Independent finite Abel evaluation of C_q.
    psi = arb(0)
    C_q_abel = arb(0)
    for k in range(1, q):
        psi += Lambda[k]
        C_q_abel += psi * (data.logs[k + 1] - data.logs[k])
    abel_numeric_error = certify_zero(C_q - C_q_abel,
                                      "numeric first-period Abel telescope")

    # Prefix spatial contractions provide K_{q,n}=<rho_q,Z_n> without using
    # beta+sum(mu W).  Each complete restricted Gram entry is an Arb enclosure.
    spatial_u = [arb(0) for _ in range(N)]
    spatial_d = [arb(0) for _ in range(N)]
    u_current = arb(0)
    d_current = arb(0)
    for d in range(1, N):
        mu_d = data.mu[d]
        if mu_d:
            gram = data.gram.entry(q, d)
            u_current += mu_d * gram
            d_current += mu_d * data.logs[d] * gram
        spatial_u[d] = u_current
        spatial_d[d] = d_current

    g_q = data.gram.chi_cross(q)
    P_chebyshev = arb(0)
    P_mertens = arb(0)
    P_direct = arb(0)
    P_abel = arb(0)
    T_direct = arb(0)
    hat_temporal = arb(0)
    all_cell_identity_error_upper_bound = arb(0)

    for n in range(q, N):
        L_n = data.logs[n]
        eta_n = data.eta[n]
        m_n = arb_fraction(m_prefix[n])
        ell_n = ell_prefix[n]
        s_n = ell_n / L_n - eta_n * m_n
        R_n = (ell_n + 1) / L_n - eta_n * m_n

        first_direct = arb(q - 1) / q * s_n + C_q / (q * L_n)
        first_split = E_q / (q * L_n) + arb(q - 1) / q * R_n
        first_abel = arb(q - 1) / q * s_n + C_q_abel / (q * L_n)
        upper = certify_zero(first_direct - first_split,
                             f"first-period split at n={n}")
        all_cell_identity_error_upper_bound += upper
        upper = certify_zero(first_direct - first_abel,
                             f"first-period Abel cell at n={n}")
        all_cell_identity_error_upper_bound += upper

        alpha = data.w[n] * data.A[n] * data.b(q, n)
        K_qn = spatial_d[n] / L_n - eta_n * (g_q + spatial_u[n])

        P_chebyshev += alpha * E_q / (q * L_n)
        P_mertens += alpha * arb(q - 1) / q * R_n
        P_direct += alpha * first_direct
        P_abel += alpha * first_abel
        T_direct += alpha * (K_qn - first_direct)
        hat_temporal += alpha * K_qn

    P_split = P_chebyshev + P_mertens
    P_errors = (
        certify_zero(P_direct - P_split, "aggregated first-period split"),
        certify_zero(P_direct - P_abel, "aggregated first-period Abel form"),
    )

    # Independent coefficient-index contraction and nested temporal contraction
    # from the committed finite formulas.
    hat_columns = data.hat_c(q)
    hat_nested = data.direct_hat_c(q)
    hat_errors = (
        certify_zero(hat_temporal - hat_columns,
                     "temporal versus coefficient-index hat_c"),
        certify_zero(hat_temporal - hat_nested,
                     "prefix versus nested temporal hat_c"),
        certify_zero(hat_temporal - (P_direct + T_direct),
                     "first-period plus tail recombination"),
    )

    certify_negative(P_chebyshev, "P_chebyshev sign")
    certify_positive(P_mertens, "P_mertens sign")
    certify_negative(P_direct, "P sign")
    certify_positive(T_direct, "T sign")
    certify_positive(hat_temporal, "hat_c sign")
    certify_negative(2 * P_direct * T_direct, "first/tail cross sign")
    certify_positive(P_direct ** 2 - hat_temporal ** 2,
                     "counterexample hat_c^2 < P^2")
    certify_positive(P_direct ** 2 + T_direct ** 2 - hat_temporal ** 2,
                     "counterexample hat_c^2 < P^2+T^2")

    energy_error = certify_zero(
        hat_temporal ** 2
        - (P_direct ** 2 + T_direct ** 2 + 2 * P_direct * T_direct),
        "first/tail energy decomposition",
    )

    return {
        "C_q": C_q,
        "E_q": E_q,
        "P_chebyshev": P_chebyshev,
        "P_mertens": P_mertens,
        "P": P_direct,
        "T": T_direct,
        "hat": hat_temporal,
        "P2": P_direct ** 2,
        "T2": T_direct ** 2,
        "cross": 2 * P_direct * T_direct,
        "hat2": hat_temporal ** 2,
        "ratio_hat2_P2": hat_temporal ** 2 / P_direct ** 2,
        "ratio_hat2_diagonal": (
            hat_temporal ** 2 / (P_direct ** 2 + T_direct ** 2)
        ),
        "abel_numeric_error": abel_numeric_error,
        "cell_identity_error": all_cell_identity_error_upper_bound,
        "P_errors": P_errors,
        "hat_errors": hat_errors,
        "energy_error": energy_error,
    }


def main() -> None:
    verify_inputs()
    runtime = require_exact_runtime()
    require(platform.python_version() == "3.12.13",
            "unexpected Python after runtime check", platform.python_version())
    require(runtime == {
        "python": "3.12.13",
        "python_flint": "0.9.0",
        "flint": "3.6.0",
    }, "runtime dictionary mismatch", runtime)
    ctx.prec = BITS

    grouping_cases, increment_cases, polynomial_cases = \
        exact_grouping_and_increment_tests()
    convolution_cases, abel_cases, coprime_abel_cases = \
        exact_convolution_and_abel_tests()
    grouped = verify_grouped_diagonals()
    first = verify_first_period_counterexample()

    script_hash = sha256_file(Path(__file__).resolve())
    print("RH CYCLE 46 FINITE FAIL-CLOSED VERIFIER: PASS")
    print("scope=finite identities and counterexamples only; no asymptotic/RH claim")
    print(f"source={Path(__file__).resolve().relative_to(WORKSPACE)}")
    print(f"source_sha256={script_hash}")
    print("runtime=CPython-3.12.13 python-flint-0.9.0 FLINT-3.6.0")
    print(f"arb_precision_bits={BITS} identity_ceiling={interval(identity_ceiling(), 12)}")
    print("bound_inputs_sha256=PASS count=" + str(len(EXPECTED_SHA256)))
    for path, expected in EXPECTED_SHA256.items():
        print(f"input_sha256 {path.relative_to(WORKSPACE)} {expected}")
    print(
        "exact_fixed_P=PASS grouping_cases=" + str(grouping_cases)
        + " adjoining_column_cases=" + str(increment_cases)
        + " adjoining_polynomial_cases=" + str(polynomial_cases)
    )
    print(
        "exact_first_period=PASS convolution_cases=" + str(convolution_cases)
        + " formal_abel_cases=" + str(abel_cases)
        + " coprime_abel_cases=" + str(coprime_abel_cases)
    )

    print(
        "grouped_diagonals a=64 I=[1,3/2] rows=" + str(len(grouped["rows"]))
    )
    print("Delta_P=2  " + interval(grouped["delta2"]))
    print("Delta_P=6  " + interval(grouped["delta6"]))
    print("Delta_P=10 " + interval(grouped["delta10"]))
    print("Delta_2-Delta_6 " + interval(grouped["down_gap"]))
    print("Delta_10-Delta_2 " + interval(grouped["up_gap"]))
    print("monotonicity_directions=PASS 2->6 decreases; 2->10 increases")
    print(
        "actual_grouping_all_abs_errors_sum_upper_bound="
        + interval(arb_sum(grouped["group_errors"]), 12)
    )
    print(
        "actual_increment_2_to_6_abs_error_upper="
        + interval(grouped["increment_errors"][6], 12)
    )
    print(
        "actual_increment_2_to_10_abs_error_upper="
        + interval(grouped["increment_errors"][10], 12)
    )

    print("first_period_counterexample a=512 q=742 factorization=2*7*53")
    print("C_q " + interval(first["C_q"]))
    print("E_q " + interval(first["E_q"]))
    print("P_chebyshev " + interval(first["P_chebyshev"]))
    print("P_mertens " + interval(first["P_mertens"]))
    print("P " + interval(first["P"]))
    print("T " + interval(first["T"]))
    print("hat_c " + interval(first["hat"]))
    print("P^2 " + interval(first["P2"]))
    print("T^2 " + interval(first["T2"]))
    print("2PT " + interval(first["cross"]))
    print("hat_c^2 " + interval(first["hat2"]))
    print("hat_c^2/P^2 " + interval(first["ratio_hat2_P2"]))
    print("hat_c^2/(P^2+T^2) " + interval(first["ratio_hat2_diagonal"]))
    print("counterexample_status=CONFIRMED; no numerical correction")
    print(
        "first_tail_all_abs_identity_errors_sum_upper_bound="
        + interval(arb_sum(
            (first["abel_numeric_error"], first["cell_identity_error"],
             *first["P_errors"], *first["hat_errors"], first["energy_error"])
        ), 12)
    )
    print("ALL_DECLARED_CHECKS_PASS")


if __name__ == "__main__":
    main()
