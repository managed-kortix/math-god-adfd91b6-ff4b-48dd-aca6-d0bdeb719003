#!/usr/bin/env python3
"""Fail-closed exact primitives for the Cycle 212 validation architecture."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from fractions import Fraction
from math import factorial, isqrt
from pathlib import Path


def q(value) -> Fraction:
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    if not isinstance(value, str) or not value or value.strip() != value:
        raise ValueError(f"invalid rational literal: {value!r}")
    return Fraction(value)


@dataclass(frozen=True)
class Interval:
    lo: Fraction
    hi: Fraction

    def __post_init__(self):
        if self.lo > self.hi:
            raise ValueError("reversed interval")

    @classmethod
    def point(cls, value):
        value = q(value)
        return cls(value, value)

    def __add__(self, other):
        other = as_interval(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-as_interval(other))

    def __rsub__(self, other):
        return as_interval(other) - self

    def __mul__(self, other):
        other = as_interval(other)
        products = (
            self.lo * other.lo,
            self.lo * other.hi,
            self.hi * other.lo,
            self.hi * other.hi,
        )
        return Interval(min(products), max(products))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = as_interval(other)
        if other.lo <= 0 <= other.hi:
            raise ValueError("interval division by a set containing zero")
        return self * Interval(1 / other.hi, 1 / other.lo)

    def square(self):
        if self.lo <= 0 <= self.hi:
            return Interval(Fraction(0), max(self.lo * self.lo, self.hi * self.hi))
        values = (self.lo * self.lo, self.hi * self.hi)
        return Interval(min(values), max(values))

    def subset(self, other) -> bool:
        other = as_interval(other)
        return other.lo <= self.lo and self.hi <= other.hi

    def abs_upper(self) -> Fraction:
        return max(abs(self.lo), abs(self.hi))


def as_interval(value) -> Interval:
    return value if isinstance(value, Interval) else Interval.point(value)


@dataclass(frozen=True)
class CInterval:
    re: Interval
    im: Interval

    @classmethod
    def point(cls, re=0, im=0):
        return cls(Interval.point(re), Interval.point(im))

    def __add__(self, other):
        other = as_cinterval(other)
        return CInterval(self.re + other.re, self.im + other.im)

    __radd__ = __add__

    def __neg__(self):
        return CInterval(-self.re, -self.im)

    def __sub__(self, other):
        return self + (-as_cinterval(other))

    def __mul__(self, other):
        other = as_cinterval(other)
        return CInterval(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )

    __rmul__ = __mul__

    def scale(self, scalar):
        return CInterval(self.re * scalar, self.im * scalar)

    def subset(self, other) -> bool:
        other = as_cinterval(other)
        return self.re.subset(other.re) and self.im.subset(other.im)

    def conjugate(self):
        return CInterval(self.re, -self.im)


def as_cinterval(value) -> CInterval:
    return value if isinstance(value, CInterval) else CInterval.point(value)


def sqrt_interval(value: Interval, denominator_bits: int = 96) -> Interval:
    if value.lo < 0 or denominator_bits < 1:
        raise ValueError("sqrt requires a nonnegative interval and positive precision")
    scale = 1 << denominator_bits

    def lower_sqrt(x):
        if x == 0:
            return Fraction(0)
        n = (x.numerator * scale * scale) // x.denominator
        return Fraction(isqrt(n), scale)

    def upper_sqrt(x):
        low = lower_sqrt(x)
        return low if low * low == x else low + Fraction(1, scale)

    return Interval(lower_sqrt(value.lo), upper_sqrt(value.hi))


Mode = tuple[int, int]


def retained_modes(cutoff: int) -> tuple[Mode, ...]:
    if cutoff < 1:
        raise ValueError("cutoff must be positive")
    return tuple(
        (a, b)
        for a in range(-cutoff, cutoff + 1)
        for b in range(-cutoff, cutoff + 1)
        if (a, b) != (0, 0)
    )


def vorticity_rhs(boxes: dict[Mode, CInterval], viscosity: Fraction) -> dict[Mode, CInterval]:
    if viscosity <= 0 or (0, 0) in boxes:
        raise ValueError("positive viscosity and zero-free mode map required")
    output = {}
    for k in boxes:
        value = boxes[k].scale(-viscosity * (k[0] * k[0] + k[1] * k[1]))
        for p, omega_p in boxes.items():
            qmode = (k[0] - p[0], k[1] - p[1])
            omega_q = boxes.get(qmode)
            if omega_q is None:
                continue
            p2 = p[0] * p[0] + p[1] * p[1]
            coefficient = Fraction(p[1] * qmode[0] - p[0] * qmode[1], p2)
            value = value + (omega_p * omega_q).scale(coefficient)
        output[k] = value
    return output


def check_reality(boxes: dict[Mode, CInterval]) -> None:
    if set(boxes) != {(-k[0], -k[1]) for k in boxes}:
        raise ValueError("mode set is not symmetric")
    for k, value in boxes.items():
        if not value.conjugate().subset(boxes[(-k[0], -k[1])]):
            raise ValueError(f"Fourier reality box failure at {k}")


def check_picard_box(entry, enclosure, remainder, viscosity, step, endpoint):
    if step <= 0 or set(entry) != set(enclosure) or set(remainder) != set(enclosure):
        raise ValueError("incompatible Picard data")
    check_reality(enclosure)
    rhs = vorticity_rhs(enclosure, viscosity)
    derivative = {k: rhs[k] + remainder[k] for k in enclosure}
    time_interval = Interval(Fraction(0), step)
    for k in enclosure:
        tube = entry[k] + CInterval(
            derivative[k].re * time_interval,
            derivative[k].im * time_interval,
        )
        end = entry[k] + derivative[k].scale(step)
        if not tube.subset(enclosure[k]):
            raise ValueError(f"Picard tube inclusion fails at {k}")
        if not end.subset(endpoint[k]):
            raise ValueError(f"endpoint inclusion fails at {k}")
    return derivative


def geometric_tail_sum(cap: Fraction, rho: Fraction, first_shell: int, power: int = 0) -> Fraction:
    """Upper bound sum_(n>=first) n^power cap rho^-n for power 0 or 1."""
    if cap < 0 or rho <= 1 or first_shell < 1 or power not in (0, 1):
        raise ValueError("invalid geometric tail parameters")
    r = 1 / rho
    if power == 0:
        return cap * r**first_shell / (1 - r)
    return cap * r**first_shell * (first_shell - (first_shell - 1) * r) / (1 - r) ** 2


def _finite_geometric_moments(x: Fraction, first: int, last: int) -> tuple[Fraction, Fraction]:
    """Return sum x^a and sum a*x^a on an inclusive finite integer range."""
    if first > last:
        return Fraction(0), Fraction(0)
    mass = Fraction(0)
    moment = Fraction(0)
    power = x**first
    for index in range(first, last + 1):
        mass += power
        moment += index * power
        power *= x
    return mass, moment


def _tail_pair_moment(x: Fraction, cap_start: int, target_shell: int) -> Fraction:
    """Bound sum b*x^(a+b) over a,b>=cap_start and a+b>=target_shell."""
    m = max(0, target_shell - 2 * cap_start)
    one_minus_x = 1 - x
    sum_0 = x**m / one_minus_x
    sum_1 = x**m * (Fraction(m, 1) / one_minus_x + x / one_minus_x**2)
    sum_2 = x**m * (
        Fraction(m * m, 1) / one_minus_x
        + 2 * m * x / one_minus_x**2
        + x * (1 + x) / one_minus_x**3
    )
    # For s=(a-L)+(b-L), sum over the s+1 pairs of b is
    # (s+1)(s+2L)/2.
    return x ** (2 * cap_start) * (
        sum_2 + (2 * cap_start + 1) * sum_1 + 2 * cap_start * sum_0
    ) / 2


def shell_convolution_bound(
    target_shell: int,
    head: dict[int, Fraction],
    cap: Fraction,
    rho: Fraction,
    cap_start: int,
    unresolved_cutoff: int = 0,
) -> Fraction:
    """Rational l-infinity shell bound for the vorticity convolution.

    ``head[a]`` bounds the full mass on shell ``a`` for 1 <= a < cap_start,
    while the remaining masses obey z_a <= cap*rho^-a.  If
    ``unresolved_cutoff`` is positive, only pairs with at least one shell above
    that cutoff are included; this gives a retained-mode remainder bound.
    """
    if target_shell < 1 or cap < 0 or rho <= 1 or cap_start < 1:
        raise ValueError("invalid shell convolution parameters")
    if set(head) != set(range(1, cap_start)):
        raise ValueError("shell head must contain exactly 1,...,cap_start-1")
    if any(value < 0 for value in head.values()):
        raise ValueError("shell masses must be nonnegative")
    if unresolved_cutoff < 0 or unresolved_cutoff >= cap_start:
        raise ValueError("unresolved cutoff must lie below cap_start")

    x = 1 / rho
    result = Fraction(0)

    # Ordered head-head pairs.  The factor 2 follows from
    # |p^perp.q|/|p|_2^2 <= 2 |q|_infinity/|p|_infinity.
    for a, mass_a in head.items():
        for b, mass_b in head.items():
            if abs(a - b) <= target_shell <= a + b:
                if unresolved_cutoff and a <= unresolved_cutoff and b <= unresolved_cutoff:
                    continue
                result += 2 * Fraction(b, a) * mass_a * mass_b

    # One head and one capped shell.  Triangle geometry restricts the capped
    # index to a finite interval.  In the reverse ordering use 1/a <= 1/L.
    for h, mass_h in head.items():
        first = max(cap_start, abs(target_shell - h))
        last = target_shell + h
        tail_mass, tail_moment = _finite_geometric_moments(x, first, last)
        result += 2 * mass_h * cap * (
            tail_moment / h + Fraction(h, cap_start) * tail_mass
        )

    # For two capped shells, discard only |a-b|<=n and retain a+b>=n.
    # This leaves a closed rational geometric second moment.
    result += Fraction(2, cap_start) * cap * cap * _tail_pair_moment(
        x, cap_start, target_shell
    )
    return result


@dataclass(frozen=True)
class ShellComparisonCertificate:
    finite_margins: tuple[Fraction, ...]
    ray_coefficients: tuple[Fraction, Fraction, Fraction]


def check_dissipative_shell_cap(
    head: dict[int, Fraction],
    cap: Fraction,
    rho: Fraction,
    cap_start: int,
    viscosity: Fraction,
    initial_shells: dict[int, Fraction] | None = None,
) -> ShellComparisonCertificate:
    """Verify inward inequalities for every face z_n=cap*rho^-n, n>=L.

    ``initial_shells`` is either omitted when domination is inherited from the
    preceding slab or is the finite list of nonzero initial tail shells; omitted
    indices in that list are asserted to have zero mass.
    """
    viscosity = q(viscosity)
    cap = q(cap)
    rho = q(rho)
    head = {index: q(value) for index, value in head.items()}
    if viscosity <= 0 or cap <= 0:
        raise ValueError("positive viscosity and tail cap required")
    if initial_shells is not None:
        for index, value in initial_shells.items():
            value = q(value)
            if index < cap_start or value < 0 or value > cap * rho ** (-index):
                raise ValueError(f"initial tail domination fails at shell {index}")

    x = 1 / rho
    margins = []
    for index in range(cap_start, 2 * cap_start):
        face = cap * x**index
        margin = viscosity * index * index * face - shell_convolution_bound(
            index, head, cap, rho, cap_start
        )
        if margin < 0:
            raise ValueError(f"tail face is not inward at shell {index}")
        margins.append(margin)

    # From n=2L onward, the normalized convolution bound is exactly a quadratic
    # in n.  Recover it at three rational points and prove its margin is
    # nonnegative on the complete real ray (hence on every integer shell).
    ray_start = 2 * cap_start
    normalized = []
    for index in range(ray_start, ray_start + 3):
        bound = shell_convolution_bound(index, head, cap, rho, cap_start)
        normalized.append(bound / (cap * x**index))
    q2 = (normalized[2] - 2 * normalized[1] + normalized[0]) / 2
    q1 = normalized[1] - normalized[0] - q2
    q0 = normalized[0]
    a = viscosity - q2
    b = 2 * viscosity * ray_start - q1
    c = viscosity * ray_start * ray_start - q0
    if a < 0 or c < 0:
        raise ValueError("dissipative tail ray has a negative leading or endpoint margin")
    if a == 0:
        if b < 0:
            raise ValueError("dissipative tail ray decreases without bound")
    elif b < 0 and 4 * a * c < b * b:
        raise ValueError("dissipative tail ray has a negative interior minimum")
    return ShellComparisonCertificate(tuple(margins), (a, b, c))


def low_mode_tail_remainder_bound(
    target_shell: int,
    retained_cutoff: int,
    head: dict[int, Fraction],
    cap: Fraction,
    rho: Fraction,
    cap_start: int,
) -> Fraction:
    """Bound one retained coefficient's omitted nonlinear remainder in modulus."""
    if target_shell > retained_cutoff:
        raise ValueError("target shell is not retained")
    return shell_convolution_bound(
        target_shell, head, cap, rho, cap_start, unresolved_cutoff=retained_cutoff
    )


def analytic_velocity_bounds(
    omega: dict[Mode, CInterval], tail_cap: Fraction, tail_rho: Fraction, first_shell: int
) -> tuple[Fraction, Fraction, Fraction]:
    """Return retained-plus-tail bounds for |u|, ||grad u||, and one tail component."""
    if (0, 0) in omega:
        raise ValueError("analytic norm input contains the zero mode")
    velocity = Fraction(0)
    gradient = Fraction(0)
    for k, coefficient in omega.items():
        magnitude = sqrt_interval(coefficient.re.square() + coefficient.im.square()).hi
        length = sqrt_interval(Interval.point(k[0] * k[0] + k[1] * k[1])).lo
        if length <= 0:
            raise ValueError("failed to obtain a positive mode length bound")
        velocity += magnitude / length
        gradient += magnitude
    shell_mass = geometric_tail_sum(tail_cap, tail_rho, first_shell)
    tail_velocity = shell_mass / first_shell
    return velocity + tail_velocity, gradient + shell_mass, tail_velocity


PI_LO = Fraction(103993, 33102)
PI_HI = Fraction(104348, 33215)


def trig_interval(turns: Fraction, kind: str, degree: int = 18) -> Interval:
    """Enclose sin/cos(2*pi*turns) by Taylor arithmetic with rational remainder."""
    if kind not in ("sin", "cos") or degree < 2:
        raise ValueError("invalid trigonometric policy")
    turns -= turns.numerator // turns.denominator
    if turns > Fraction(1, 2):
        turns -= 1
    factor = 2 * turns
    if factor < 0:
        x = Interval(PI_HI * factor, PI_LO * factor)
    else:
        x = Interval(PI_LO * factor, PI_HI * factor)
    result = Interval.point(0)
    parity = 1 if kind == "sin" else 0
    for exponent in range(parity, degree + 1, 2):
        term = Interval.point(1)
        for _ in range(exponent):
            term = term * x
        sign = -1 if ((exponent - parity) // 2) % 2 else 1
        result = result + term * Fraction(sign, factorial(exponent))
    last_exponent = max(range(parity, degree + 1, 2))
    remainder_order = last_exponent + 1
    radius = max(abs(x.lo), abs(x.hi)) ** remainder_order / factorial(remainder_order)
    return result + Interval(-radius, radius)


def velocity_at_turns(omega: dict[Mode, CInterval], point: tuple[Fraction, Fraction], degree=18):
    ux = CInterval.point()
    uy = CInterval.point()
    for k, coefficient in omega.items():
        phase = k[0] * point[0] + k[1] * point[1]
        exponential = CInterval(trig_interval(phase, "cos", degree), trig_interval(phase, "sin", degree))
        k2 = k[0] * k[0] + k[1] * k[1]
        weighted = coefficient * exponential
        # i*k^perp = (i*k_y, -i*k_x), for omega = curl(u) = Delta(psi).
        ux = ux + weighted * CInterval.point(0, Fraction(k[1], k2))
        uy = uy + weighted * CInterval.point(0, Fraction(-k[0], k2))
    return ux.re, uy.re


def l3_cubature(
    omega,
    grid: int,
    uniform_u: Fraction,
    gradient_u: Fraction,
    tail_velocity_component: Fraction = Fraction(0),
    degree=18,
):
    if grid < 1 or uniform_u < 0 or gradient_u < 0 or tail_velocity_component < 0:
        raise ValueError("invalid cubature parameters")
    total = Interval.point(0)
    for a in range(grid):
        for b in range(grid):
            point = (Fraction(2 * a + 1, 2 * grid), Fraction(2 * b + 1, 2 * grid))
            ux, uy = velocity_at_turns(omega, point, degree)
            tail = Interval(-tail_velocity_component, tail_velocity_component)
            ux = ux + tail
            uy = uy + tail
            norm = sqrt_interval(ux.square() + uy.square())
            total = total + norm * norm * norm
    average = total / (grid * grid)
    sqrt_two_upper = Fraction(665857, 470832)
    cell_radius = sqrt_two_upper * PI_HI / grid
    error = 3 * uniform_u * uniform_u * gradient_u * cell_radius
    return Interval(max(Fraction(0), average.lo - error), average.hi + error)


def load_manifest(path: Path):
    try:
        data = json.loads(path.read_text(encoding="ascii"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load manifest: {exc}") from exc
    required = {"format", "mode", "normalization"}
    unknown = set(data) - required
    missing = required - set(data)
    if missing or unknown:
        raise ValueError(f"manifest keys missing={sorted(missing)} unknown={sorted(unknown)}")
    if data["format"] != "cycle212-component-v1":
        raise ValueError("unsupported manifest format")
    if data["normalization"] != "T2-2pi-normalized-vorticity-v1":
        raise ValueError("normalization mismatch")
    if data["mode"] == "full":
        raise ValueError("full mode unavailable: production shell comparison data is absent")
    if data["mode"] != "components":
        raise ValueError("mode must be components or full")
    return data


def self_test():
    x = Interval(Fraction(-1), Fraction(2))
    if x.square() != Interval(Fraction(0), Fraction(4)):
        raise RuntimeError("interval square self-test failed")
    root = sqrt_interval(Interval.point(2))
    if not root.lo * root.lo <= 2 <= root.hi * root.hi:
        raise RuntimeError("sqrt self-test failed")
    if not trig_interval(Fraction(0), "sin").subset(Interval.point(0)):
        raise RuntimeError("sine self-test failed")
    if not trig_interval(Fraction(0), "cos").subset(Interval.point(1)):
        raise RuntimeError("cosine self-test failed")

    modes = retained_modes(1)
    zero = {k: CInterval.point() for k in modes}
    wide = {k: CInterval(Interval(-1, 1), Interval(-1, 1)) for k in modes}
    check_picard_box(zero, wide, zero, Fraction(1), Fraction(1, 10), wide)

    selected = {k: CInterval.point() for k in modes}
    for k, value in {
        (1, 0): Fraction(-1, 2),
        (-1, 0): Fraction(-1, 2),
        (0, 1): Fraction(-1, 2),
        (0, -1): Fraction(-1, 2),
        (1, 1): Fraction(-1),
        (-1, -1): Fraction(-1),
    }.items():
        selected[k] = CInterval.point(value)
    check_reality(selected)
    uniform_u, gradient_u, tail_component = analytic_velocity_bounds(
        selected, Fraction(1, 100), Fraction(2), 2
    )
    cube = l3_cubature(
        selected, 4, uniform_u, gradient_u, tail_component, degree=20
    )
    if cube.lo < 0 or cube.lo > cube.hi:
        raise RuntimeError("cubature self-test failed")
    if geometric_tail_sum(Fraction(1), Fraction(2), 3) != Fraction(1, 4):
        raise RuntimeError("tail self-test failed")
    return cube


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    try:
        if args.manifest is not None:
            load_manifest(args.manifest)
        cube = self_test()
    except (ValueError, RuntimeError, ZeroDivisionError) as exc:
        parser.exit(1, f"FAIL CLOSED: {exc}\n")
    print("PASS COMPONENTS Cycle 212")
    print(
        "selected-datum coarse L3-cube enclosure recomputed "
        f"(lower={cube.lo}, upper numerator bits={cube.hi.numerator.bit_length()}, "
        f"upper denominator bits={cube.hi.denominator.bit_length()})"
    )
    print("NO PDE OR AMPLIFICATION CLAIM: production shell comparison data is absent")


if __name__ == "__main__":
    main()
