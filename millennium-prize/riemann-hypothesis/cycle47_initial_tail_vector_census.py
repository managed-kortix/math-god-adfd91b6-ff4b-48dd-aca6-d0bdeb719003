#!/usr/bin/env python3
"""Fail-closed outward-Arb census for the finite Cycle 47 P/T vectors.

At theta=2/5 this reconstructs every squarefree physical row on the six
finite dyadic blocks a=32,...,1024 and the closed intervals [1,2] and
[1,3/2].  It certifies three paths to P, two paths to hat_c, two paths to T,
the energy decomposition, the one-dimensional orthogonal projection, and the
12 Cycle 45 D rows.

This is a finite computational certificate only.  It proves no convergence,
asymptotic lower bound, moving-projection theorem, Riemann-hypothesis result,
or implication for any untested scale.
"""

from __future__ import annotations

import hashlib
from fractions import Fraction
import json
import os
from pathlib import Path
import platform
import stat
import sys
import types

# The canonical command supplies -I -B.  Set this again before any bound local
# source is executed, then verify the actual interpreter flags below.
sys.dont_write_bytecode = True

RH_DIR = Path(__file__).resolve().parent
WORKSPACE = RH_DIR.parent.parent
SCRIPT_PATH = Path(__file__).resolve()

BITS = 192
STARTS = (32, 64, 128, 256, 512, 1024)
INTERVALS = (
    ("[1,2]", Fraction(1), Fraction(2)),
    ("[1,3/2]", Fraction(1), Fraction(3, 2)),
)
THETA = Fraction(2, 5)
MAX_N = 2 * max(STARTS)
IDENTITY_EXPONENT = BITS // 2
DIGITS = 40

LOCAL_MODULES = (
    "certify_complete_gram",
    "cycle45_runtime",
    "cycle43_divisor_admission_multiprobe",
    "cycle44_boundary_envelope_scan",
    "cycle45_dispersion_census",
)
BOOTSTRAP_SHADOWS = (
    "argparse", "fractions", "hashlib", "json", "math", "os", "pathlib",
    "platform", "stat", "sys", "types", "flint",
)

# This is the complete local source/input closure reached by DispersionData and
# require_exact_runtime.  Python sources are captured and executed from these
# bytes only after every hash and competing-import check passes.
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
    RH_DIR / "cycle45-dispersion-census-results.json":
        "6db00e23d47a409b905535dec0c88a1ad684e8daf95e62b3c6d25593c6d09f66",
}


def fail(label: str, *details: object) -> None:
    raise RuntimeError((label,) + details)


def require(condition: bool, label: str, *details: object) -> None:
    if not condition:
        fail(label, *details)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def _reject_import_artifacts(name: str, *, bound_source: bool) -> None:
    candidates = [
        RH_DIR / name,
        RH_DIR / f"{name}.pyc",
        RH_DIR / f"{name}.pyo",
    ]
    if not bound_source:
        candidates.append(RH_DIR / f"{name}.py")
    for path in candidates:
        if path.exists():
            fail("competing local import artifact", path)

    cache = RH_DIR / "__pycache__"
    if cache.exists():
        matches = tuple(cache.glob(f"{name}.*.pyc")) + \
            tuple(cache.glob(f"{name}.*.pyo"))
        if matches:
            fail("competing local bytecode artifact", matches)

    for suffix in (".so", ".pyd", ".dll", ".dylib"):
        matches = tuple(RH_DIR.glob(f"{name}*{suffix}"))
        if matches:
            fail("competing local extension artifact", matches)


def _preflight_source_closure() -> tuple[dict[str, bytes], dict[Path, bytes]]:
    require(sys.flags.isolated and sys.flags.safe_path, "run with python -I")
    require(sys.flags.dont_write_bytecode, "run with python -B")
    require(sys.flags.optimize == 0, "optimized Python is forbidden")
    require(not os.environ.get("PYTHONPYCACHEPREFIX"),
            "PYTHONPYCACHEPREFIX must be unset")
    mode = SCRIPT_PATH.stat().st_mode
    require(not (mode & (stat.S_IWGRP | stat.S_IWOTH)),
            "certificate source must not be group/world writable",
            SCRIPT_PATH, oct(mode))

    for name in LOCAL_MODULES:
        _reject_import_artifacts(name, bound_source=True)
    for name in BOOTSTRAP_SHADOWS:
        _reject_import_artifacts(name, bound_source=False)

    all_bytes: dict[Path, bytes] = {}
    sources: dict[str, bytes] = {}
    for path, expected in EXPECTED_SHA256.items():
        require(path.is_file(), "missing bound input", path)
        mode = path.stat().st_mode
        require(not (mode & (stat.S_IWGRP | stat.S_IWOTH)),
                "bound input must not be group/world writable", path,
                oct(mode))
        captured = path.read_bytes()
        observed = sha256_bytes(captured)
        require(observed == expected, "bound input hash mismatch", path,
                observed, expected)
        all_bytes[path] = captured
        if path.suffix == ".py":
            sources[path.stem] = captured
    return sources, all_bytes


_BOUND_SOURCES, _BOUND_INPUT_BYTES = _preflight_source_closure()

# Import the external numerical package while the repository is absent from
# sys.path under -I.  Its exact version and nonlocal origin are checked twice.
import flint  # noqa: E402
from flint import arb, ctx  # noqa: E402

_FLINT_ORIGIN = Path(flint.__file__).resolve()
require(_FLINT_ORIGIN != RH_DIR and RH_DIR not in _FLINT_ORIGIN.parents,
        "local flint shadow loaded", _FLINT_ORIGIN)


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
DispersionData = _BOUND_MODULES["cycle45_dispersion_census"].DispersionData
arb_sum = _BOUND_MODULES["cycle45_dispersion_census"].arb_sum
mobius_sieve = _BOUND_MODULES["certify_complete_gram"].mobius_sieve
require_exact_runtime = _BOUND_MODULES["cycle45_runtime"].require_exact_runtime


def verify_runtime_and_inputs() -> None:
    script_mode = SCRIPT_PATH.stat().st_mode
    require(not (script_mode & (stat.S_IWGRP | stat.S_IWOTH)),
            "certificate source permissions changed", SCRIPT_PATH,
            oct(script_mode))
    # Re-read after execution of captured bytes.  An in-process mutation cannot
    # silently change either the declared input or the later artifact replay.
    for path, expected in EXPECTED_SHA256.items():
        require(path.is_file(), "missing bound input on second check", path)
        mode = path.stat().st_mode
        require(not (mode & (stat.S_IWGRP | stat.S_IWOTH)),
                "bound input permissions changed", path, oct(mode))
        observed = sha256_file(path)
        require(observed == expected, "bound input hash mismatch on second check",
                path, observed, expected)
        require(path.read_bytes() == _BOUND_INPUT_BYTES[path],
                "bound input bytes changed after capture", path)

    require(sys.implementation.name == "cpython",
            "unexpected Python implementation", sys.implementation.name)
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
    runtime = require_exact_runtime()
    require(runtime == {
        "python": "3.12.13",
        "python_flint": "0.9.0",
        "flint": "3.6.0",
    }, "runtime dictionary mismatch", runtime)


def require_arb(value: arb, label: str) -> arb:
    require(isinstance(value, arb), "not an Arb value", label, type(value))
    require(value.is_finite(), "nonfinite Arb value", label, value)
    return value


def interval(value: arb, digits: int = DIGITS) -> str:
    return require_arb(value, "serialized interval").str(digits)


def identity_ceiling() -> arb:
    return arb(2) ** (-IDENTITY_EXPONENT)


def certify_zero(value: arb, label: str) -> arb:
    require_arb(value, label)
    require(value.contains(0), "identity ball excludes zero", label, value)
    upper = require_arb(abs(value).upper(), label + " absolute upper")
    ceiling = identity_ceiling()
    # Compare directed endpoints, not overlapping balls.  This remains a
    # strict finite width policy even if a future value approaches the limit.
    require(upper.upper() <= ceiling.lower(), "identity ball too wide", label,
            value, ceiling)
    return upper


def certify_positive(value: arb, label: str) -> arb:
    require_arb(value, label)
    require(value > 0, "positive sign unresolved or false", label, value)
    return value


def arb_fraction(value: Fraction) -> arb:
    return arb(value.numerator) / value.denominator


def add_error(total: arb, value: arb, label: str) -> arb:
    return total + certify_zero(value, label)


# ---------------------------------------------------------------------------
# Exact arithmetic independent of the imported Mobius sieve.
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


def exact_mu(n: int) -> int:
    factors = factorization(n)
    if any(exponent > 1 for exponent in factors.values()):
        return 0
    return -1 if len(factors) % 2 else 1


def prime_power_base(n: int) -> int | None:
    if n < 2:
        return None
    factors = factorization(n)
    if len(factors) != 1:
        return None
    return next(iter(factors))


def exact_arithmetic_tables() -> tuple[tuple[int, ...], tuple[int | None, ...]]:
    imported = mobius_sieve(MAX_N)
    mu = (0,) + tuple(exact_mu(n) for n in range(1, MAX_N + 1))
    bases = (None,) + tuple(
        prime_power_base(n) for n in range(1, MAX_N + 1)
    )
    for n in range(1, MAX_N + 1):
        require(imported[n] == mu[n], "independent Mobius mismatch", n,
                imported[n], mu[n])
        base = bases[n]
        if base is not None:
            require(factorization(n) == {base: factorization(n)[base]},
                    "prime-power classifier mismatch", n, base)
            require(factorization(base) == {base: 1},
                    "Lambda base is not prime", n, base)
    return mu, bases


# ---------------------------------------------------------------------------
# Bound Cycle 45 artifact and exact formula reconstructions.
# ---------------------------------------------------------------------------


def load_cycle45_reference() -> dict[tuple[int, str], tuple[arb, int]]:
    try:
        payload = json.loads(
            _BOUND_INPUT_BYTES[RH_DIR / "cycle45-dispersion-census-results.json"]
            .decode("ascii")
        )
    except Exception as exc:
        raise RuntimeError("cannot parse bound Cycle 45 artifact") from exc

    require(payload.get("scope") == (
        "certified finite diagnostic only; no convergence, asymptotic lower "
        "bound, or RH claim"
    ), "Cycle 45 scope changed", payload.get("scope"))
    require(payload.get("arb_precision_bits") == 192,
            "Cycle 45 precision changed", payload.get("arb_precision_bits"))
    require(payload.get("theta") == "2/5", "Cycle 45 theta changed")
    require(payload.get("starts") == list(STARTS), "Cycle 45 starts changed")
    require(len(payload.get("rows", ())) == 12, "Cycle 45 row count changed")

    refs: dict[tuple[int, str], tuple[arb, int]] = {}
    for row in payload["rows"]:
        raw_I = row.get("I")
        if raw_I == [1.0, 2.0]:
            name = "[1,2]"
        elif raw_I == [1.0, 1.5]:
            name = "[1,3/2]"
        else:
            fail("unexpected Cycle 45 interval", raw_I)
        key = (row["a"], name)
        require(key not in refs, "duplicate Cycle 45 row", key)
        value = arb(row["D"])
        require_arb(value, f"Cycle 45 D {key}")
        require(value > 0, "Cycle 45 D is not certified positive", key, value)
        rank = row.get("rank")
        require(isinstance(rank, int) and rank > 0,
                "invalid Cycle 45 row rank", key, rank)
        refs[key] = (value, rank)
    expected_keys = {(a, name) for a in STARTS for name, _, _ in INTERVALS}
    require(set(refs) == expected_keys, "Cycle 45 row keys changed",
            set(refs), expected_keys)
    return refs


def prefix_arithmetic(data: object, exact_mu_table: tuple[int, ...],
                      prime_bases: tuple[int | None, ...]):
    N = data.stop
    m_values = [Fraction(0) for _ in range(N)]
    ell_values = [arb(0) for _ in range(N)]
    Lambda = [arb(0) for _ in range(N)]
    m_now = Fraction(0)
    ell_now = arb(0)
    for n in range(1, N):
        mu_n = exact_mu_table[n]
        require(mu_n == data.mu[n], "per-scale Mobius mismatch", data.start,
                n, mu_n, data.mu[n])
        if mu_n:
            m_now += Fraction(mu_n, n)
            ell_now += mu_n * data.logs[n] / n
        m_values[n] = m_now
        ell_values[n] = ell_now
        base = prime_bases[n]
        if base is not None:
            Lambda[n] = data.logs[base]
    return m_values, ell_values, Lambda


def chebyshev_tables(data: object, Lambda: list[arb]) -> tuple[list[arb], arb]:
    N = data.stop
    psi = [arb(0) for _ in range(N)]
    C_abel = [arb(0) for _ in range(N)]
    psi_now = arb(0)
    for k in range(1, N):
        psi_now += Lambda[k]
        psi[k] = psi_now
        if k + 1 < N:
            C_abel[k + 1] = (
                C_abel[k]
                + psi_now * (data.logs[k + 1] - data.logs[k])
            )

    all_error = arb(0)
    for q in range(1, N):
        direct = arb_sum(
            Lambda[m] * (data.logs[q] - data.logs[m])
            for m in range(2, q)
        )
        all_error = add_error(
            all_error, C_abel[q] - direct,
            f"Lambda direct versus temporal Abel C, a={data.start}, q={q}",
        )
    return C_abel, all_error


def suffix_tables(data: object, m_values: list[Fraction],
                  ell_values: list[arb]):
    a = data.start
    N = data.stop
    kappa = [arb(0) for _ in range(N)]
    s = [arb(0) for _ in range(N)]
    R = [arb(0) for _ in range(N)]
    for n in range(a, N):
        m_n = arb_fraction(m_values[n])
        kappa[n] = data.w[n] * data.A[n]
        s[n] = ell_values[n] / data.logs[n] - data.eta[n] * m_n
        R[n] = s[n] + 1 / data.logs[n]

    names = ("B2", "B1", "B0", "S1", "S0", "R1", "R0")
    suffix = {name: [arb(0) for _ in range(N + 1)] for name in names}
    for n in range(N - 1, a - 1, -1):
        suffix["B2"][n] = suffix["B2"][n + 1] + \
            kappa[n] / data.logs[n] ** 2
        suffix["B1"][n] = suffix["B1"][n + 1] + \
            kappa[n] * data.eta[n] / data.logs[n]
        suffix["B0"][n] = suffix["B0"][n + 1] + \
            kappa[n] * data.eta[n] ** 2
        suffix["S1"][n] = suffix["S1"][n + 1] + \
            kappa[n] * s[n] / data.logs[n]
        suffix["S0"][n] = suffix["S0"][n + 1] + \
            kappa[n] * data.eta[n] * s[n]
        suffix["R1"][n] = suffix["R1"][n + 1] + \
            kappa[n] * R[n] / data.logs[n]
        suffix["R0"][n] = suffix["R0"][n + 1] + \
            kappa[n] * data.eta[n] * R[n]
    return kappa, s, R, suffix


def census_scale(a: int, exact_mu_table: tuple[int, ...],
                 prime_bases: tuple[int | None, ...],
                 references: dict[tuple[int, str], tuple[arb, int]]):
    data = DispersionData(a, BITS)
    N = data.stop
    require(N == 2 * a, "unexpected dyadic stop", a, N)
    theta_expected = arb(THETA.numerator) / THETA.denominator
    require((data.theta - theta_expected).contains(0),
            "theta mismatch", a, data.theta, theta_expected)
    rows = tuple(q for q in data.squarefree if a <= q < N)
    require(rows, "empty full squarefree row set", a)
    require(rows == tuple(q for q in range(a, N) if exact_mu_table[q] != 0),
            "physical row set mismatch", a)

    m_values, ell_values, Lambda = prefix_arithmetic(
        data, exact_mu_table, prime_bases
    )
    C, abel_error = chebyshev_tables(data, Lambda)
    kappa, s, R, suffix = suffix_tables(data, m_values, ell_values)

    P_suffix: dict[int, arb] = {}
    P_temporal: dict[int, arb] = {}
    P_split: dict[int, arb] = {}
    F_cells: dict[int, list[arb]] = {}
    p_path_error = arb(0)

    for q in rows:
        log_q = data.logs[q]
        q_minus = arb(q - 1) / q
        c_over_q = C[q] / q
        p_suffix = (
            q_minus * (log_q * suffix["S1"][q] - suffix["S0"][q])
            + c_over_q * (log_q * suffix["B2"][q] - suffix["B1"][q])
        )
        p_psi = (C[q] - (q - 1)) / q * (
            log_q * suffix["B2"][q] - suffix["B1"][q]
        )
        p_mobius = q_minus * (
            log_q * suffix["R1"][q] - suffix["R0"][q]
        )
        p_split = p_psi + p_mobius

        direct = arb(0)
        cells: list[arb] = []
        for n in range(q, N):
            F_qn = q_minus * s[n] + C[q] / (q * data.logs[n])
            cells.append(F_qn)
            alpha_qn = kappa[n] * data.b(q, n)
            direct += alpha_qn * F_qn

        p_path_error = add_error(
            p_path_error, p_suffix - direct,
            f"P suffix versus direct temporal, a={a}, q={q}",
        )
        p_path_error = add_error(
            p_path_error, p_suffix - p_split,
            f"P suffix versus psi+Mobius split, a={a}, q={q}",
        )
        P_suffix[q] = p_suffix
        P_temporal[q] = direct
        P_split[q] = p_split
        F_cells[q] = cells

    # First hat_c path: temporal prefix K.  For each row q, increment the two
    # exact spatial contractions as n admits a new squarefree coefficient.
    hat_temporal: dict[int, arb] = {}
    T_direct: dict[int, arb] = {}
    t_path_error = arb(0)
    gram_diagonal_error = arb(0)
    squarefree = data.squarefree

    for q in rows:
        expected_diagonal = (
            ((2 * arb.pi()).log() - arb.const_euler()) / q
            - arb(1) / (q * q)
        )
        gram_diagonal_error = add_error(
            gram_diagonal_error,
            data.gram.entry(q, q) - expected_diagonal,
            f"restricted Gram diagonal, a={a}, q={q}",
        )

        spatial_u = arb(0)
        spatial_d = arb(0)
        index = 0
        while index < len(squarefree) and squarefree[index] < q:
            d = squarefree[index]
            gram = data.gram.entry(q, d)
            spatial_u += exact_mu_table[d] * gram
            spatial_d += exact_mu_table[d] * data.logs[d] * gram
            index += 1

        hat = arb(0)
        tail = arb(0)
        g_q = data.gram.chi_cross(q)
        for n in range(q, N):
            while index < len(squarefree) and squarefree[index] <= n:
                d = squarefree[index]
                gram = data.gram.entry(q, d)
                spatial_u += exact_mu_table[d] * gram
                spatial_d += exact_mu_table[d] * data.logs[d] * gram
                index += 1
            K_qn = (
                spatial_d / data.logs[n]
                - data.eta[n] * (g_q + spatial_u)
            )
            alpha_qn = kappa[n] * data.b(q, n)
            hat += alpha_qn * K_qn
            tail += alpha_qn * (K_qn - F_cells[q][n - q])
        hat_temporal[q] = hat
        T_direct[q] = tail

    # Second hat_c path: affine beta plus coefficient-index columns.  The
    # suffix B2/B1/B0 expansion is independent of the temporal prefix order.
    hat_columns: dict[int, arb] = {}
    hat_path_error = arb(0)
    for q in rows:
        log_q = data.logs[q]
        beta = -data.gram.chi_cross(q) * (
            log_q * suffix["B1"][q] - suffix["B0"][q]
        )
        hat = beta
        for d in squarefree:
            j = max(q, d)
            temporal_H = (
                log_q * data.logs[d] * suffix["B2"][j]
                - (log_q + data.logs[d]) * suffix["B1"][j]
                + suffix["B0"][j]
            )
            hat += exact_mu_table[d] * data.gram.entry(q, d) * temporal_H
        hat_path_error = add_error(
            hat_path_error, hat_temporal[q] - hat,
            f"hat temporal-prefix K versus beta+sum(mu W), a={a}, q={q}",
        )
        T_subtraction = hat - P_suffix[q]
        t_path_error = add_error(
            t_path_error, T_direct[q] - T_subtraction,
            f"T direct K-F versus subtraction, a={a}, q={q}",
        )
        # This also makes P+T=hat explicit per row, rather than relying only on
        # the later aggregate energy identity.
        t_path_error = add_error(
            t_path_error, P_suffix[q] + T_direct[q] - hat,
            f"row P+T recombination, a={a}, q={q}",
        )
        hat_columns[q] = hat

    results = []
    aggregate_error = arb(0)
    for name, lo, hi in INTERVALS:
        selected = tuple(q for q in rows if lo <= Fraction(q, a) <= hi)
        require(selected, "empty selected row set", a, name)

        P2 = arb_sum(P_suffix[q] ** 2 for q in selected)
        PT = arb_sum(P_suffix[q] * T_direct[q] for q in selected)
        T2 = arb_sum(T_direct[q] ** 2 for q in selected)
        D = arb_sum(hat_temporal[q] ** 2 for q in selected)
        Pc = arb_sum(P_suffix[q] * hat_temporal[q] for q in selected)
        certify_positive(P2, f"||P||^2, a={a}, I={name}")
        certify_positive(D, f"D, a={a}, I={name}")
        gamma = 1 + PT / P2
        # Intrinsic scalar requested in Cycle 47: projection of c=P+T onto P.
        projection_Q = Pc ** 2 / P2
        residual2 = arb_sum(
            (hat_temporal[q] - gamma * P_suffix[q]) ** 2
            for q in selected
        )
        certify_positive(residual2,
                         f"orthogonal residual norm^2, a={a}, I={name}")

        energy_error = D - (P2 + 2 * PT + T2)
        pc_error = Pc - (P2 + PT)
        orthogonality_error = arb_sum(
            P_suffix[q] * (hat_temporal[q] - gamma * P_suffix[q])
            for q in selected
        )
        projection_Q_error = projection_Q - gamma ** 2 * P2
        projection_error = D - (gamma ** 2 * P2 + residual2)
        for error, label in (
            (energy_error, "energy recombination"),
            (pc_error, "<P,c>=||P||^2+<P,T>"),
            (orthogonality_error, "orthogonal residual dot P"),
            (projection_Q_error, "intrinsic Q=gamma^2||P||^2"),
            (projection_error, "orthogonal projection energy"),
        ):
            aggregate_error = add_error(
                aggregate_error, error, f"{label}, a={a}, I={name}"
            )

        reference, reference_rank = references[(a, name)]
        require(len(selected) == reference_rank,
                "Cycle 45 row rank not reproduced", a, name, len(selected),
                reference_rank)
        require(reference.contains(D),
                "Cycle 45 D artifact does not contain reconstruction",
                a, name, D, reference)
        cycle45_overlap = D.intersection(reference)
        require_arb(cycle45_overlap, f"Cycle 45 overlap a={a}, I={name}")

        L3 = data.logs[a] ** 3
        results.append({
            "a": a,
            "I": name,
            "rows": len(selected),
            "P2": P2,
            "PT": PT,
            "gamma": gamma,
            "T2": T2,
            "D": D,
            "L3P2": L3 * P2,
            "Q": projection_Q,
            "L3Q": L3 * projection_Q,
            "residual2": residual2,
            "cycle45_D": reference,
            "cycle45_overlap": cycle45_overlap,
        })

    error_totals = {
        "lambda_abel": abel_error,
        "P_paths": p_path_error,
        "hat_paths": hat_path_error,
        "T_paths": t_path_error,
        "gram_diagonal": gram_diagonal_error,
        "aggregate": aggregate_error,
    }
    for label, value in error_totals.items():
        require_arb(value, f"error total {label}, a={a}")
        ceiling = identity_ceiling()
        require(value.upper() <= ceiling.lower(),
                "summed identity error exceeds ceiling", a, label, value,
                ceiling)
    return results, error_totals


def main() -> None:
    verify_runtime_and_inputs()
    ctx.prec = BITS
    exact_mu_table, prime_bases = exact_arithmetic_tables()
    references = load_cycle45_reference()

    all_results = []
    all_errors: dict[int, dict[str, arb]] = {}
    for a in STARTS:
        rows, errors = census_scale(
            a, exact_mu_table, prime_bases, references
        )
        all_results.extend(rows)
        all_errors[a] = errors

    require(len(all_results) == 12, "unexpected result row count",
            len(all_results))
    # The artifact must remain untouched throughout the expensive run too.
    verify_runtime_and_inputs()

    print("RH CYCLE 47 FINITE INITIAL/TAIL VECTOR CENSUS: PASS")
    print("scope=12 finite outward-Arb rows only; no convergence, asymptotic lower bound, moving-projection theorem, or RH claim")
    print(f"source={SCRIPT_PATH.relative_to(WORKSPACE)}")
    print(f"source_sha256={sha256_file(SCRIPT_PATH)}")
    print("runtime=CPython-3.12.13 python-flint-0.9.0 FLINT-3.6.0")
    print("canonical_command=env -u PYTHONPYCACHEPREFIX PYTHONDONTWRITEBYTECODE=1 uv run --isolated --no-project --python 3.12.13 --with python-flint==0.9.0 python -I -B millennium-prize/riemann-hypothesis/cycle47_initial_tail_vector_census.py > millennium-prize/riemann-hypothesis/cycle47-initial-tail-vector-census.out")
    print(f"theta=2/5 arb_precision_bits={BITS} identity_ceiling={interval(identity_ceiling(), 15)}")
    print("row_rule=squarefree q with q/a in the named closed interval")
    print("normalization=hat_c(q)=mu(q)c_q=beta(q)+sum_d(mu(d)W(q,d)); W has no hidden Mobius sign")
    print("definitions=P(q)=sum_n(alpha(q,n)F(q,n)); T(q)=sum_n(alpha(q,n)(K(q,n)-F(q,n))); c=P+T=hat_c")
    print("Q_definition=|<P,P+T>|^2/||P||^2=(||P||^2+<P,T>)^2/||P||^2")
    print("path_checks=PASS P:suffix,direct-temporal-F,psi+Mobius-split; hat_c:temporal-prefix-K,coefficient-index-beta+sum(mu*W); T:direct-K-minus-F,hat_c-minus-P")
    print(f"exact_arithmetic=PASS Mobius_and_Lambda_prime_power_range=1..{MAX_N}")
    print(f"bound_inputs_sha256=PASS count={len(EXPECTED_SHA256)}")
    for path, expected in EXPECTED_SHA256.items():
        print(f"input_sha256 {path.relative_to(WORKSPACE)} {expected}")

    for a in STARTS:
        errors = all_errors[a]
        joined = " ".join(
            f"{label}={interval(value, 15)}"
            for label, value in errors.items()
        )
        print(f"identity_error_sums_upper a={a} {joined}")

    for row in all_results:
        print(f"row a={row['a']} I={row['I']} rows={row['rows']}")
        for label in (
            "P2", "PT", "gamma", "T2", "D", "L3P2", "Q", "L3Q",
            "residual2",
        ):
            print(f"  {label} {interval(row[label])}")
        print(f"  cycle45_D {interval(row['cycle45_D'])}")
        print(f"  cycle45_D_overlap {interval(row['cycle45_overlap'])}")

    print("cycle45_D_rows_reproduced=PASS count=12 policy=bound_artifact_contains_reconstruction")
    print("finite_only_disclaimer=No untested scale, asymptotic, moving-projection, completed-square, or Riemann-hypothesis conclusion is certified.")
    print("ALL_DECLARED_CHECKS_PASS")


if __name__ == "__main__":
    main()
