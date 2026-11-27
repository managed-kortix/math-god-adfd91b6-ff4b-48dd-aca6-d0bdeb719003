#!/usr/bin/env python3
"""Exact-rational certificate that a physical prefix kernel is not completely monotone."""

from __future__ import annotations

import hashlib
import os
import platform
import stat
import sys
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path

TERMS = 200
DIGITS = 36
REQUIRED_PYTHON = "3.12.13"
SCRIPT_PATH = Path(__file__).resolve()


def require(condition: bool, label: str, *details: object) -> None:
    if not condition:
        raise RuntimeError((label,) + details)


@dataclass(frozen=True)
class Interval:
    lo: Q
    hi: Q

    def __post_init__(self) -> None:
        require(self.lo <= self.hi, "reversed interval", self.lo, self.hi)

    @staticmethod
    def point(value: int | Q) -> "Interval":
        value = Q(value)
        return Interval(value, value)

    def __add__(self, other: object) -> "Interval":
        rhs = as_interval(other)
        return Interval(self.lo + rhs.lo, self.hi + rhs.hi)

    __radd__ = __add__

    def __neg__(self) -> "Interval":
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other: object) -> "Interval":
        return self + (-as_interval(other))

    def __rsub__(self, other: object) -> "Interval":
        return as_interval(other) - self

    def __mul__(self, other: object) -> "Interval":
        rhs = as_interval(other)
        products = (
            self.lo * rhs.lo,
            self.lo * rhs.hi,
            self.hi * rhs.lo,
            self.hi * rhs.hi,
        )
        return Interval(min(products), max(products))

    __rmul__ = __mul__

    def reciprocal(self) -> "Interval":
        require(not (self.lo <= 0 <= self.hi), "division interval contains zero")
        return Interval(min(1 / self.lo, 1 / self.hi),
                        max(1 / self.lo, 1 / self.hi))

    def __truediv__(self, other: object) -> "Interval":
        return self * as_interval(other).reciprocal()

    def __rtruediv__(self, other: object) -> "Interval":
        return as_interval(other) / self


def as_interval(value: object) -> Interval:
    if isinstance(value, Interval):
        return value
    if isinstance(value, (int, Q)):
        return Interval.point(value)
    raise TypeError(type(value))


def log_interval(value: Q, terms: int = TERMS) -> Interval:
    """Enclose log(value) by the exact atanh series and its geometric tail."""
    value = Q(value)
    require(value > 0, "log argument must be positive", value)
    if value == 1:
        return Interval.point(0)
    if value < 1:
        return -log_interval(1 / value, terms)
    z = (value - 1) / (value + 1)
    require(0 < z < 1, "invalid atanh parameter", value, z)
    partial = 2 * sum(
        (z ** (2 * j + 1)) / (2 * j + 1) for j in range(terms)
    )
    remainder = (
        2 * z ** (2 * terms + 1)
        / ((2 * terms + 1) * (1 - z * z))
    )
    require(remainder > 0, "nonpositive remainder", value, remainder)
    return Interval(partial, partial + remainder)


def prefix_cell(q: int, d: int, n: int) -> Interval:
    """Literal complete-cell integral of rho_q rho_d over [1,n+1]."""
    total = Interval.point(0)
    for k in range(1, n + 1):
        fq, fd = k // q, k // d
        total += (
            Q(1, q * d)
            - (Q(fd, q) + Q(fq, d)) * log_interval(Q(k + 1, k))
            + Q(fq * fd) * (Q(1, k) - Q(1, k + 1))
        )
    return total


def certify_same(left: Interval, right: Interval, label: str) -> None:
    require(max(left.lo, right.lo) <= min(left.hi, right.hi),
            "independent enclosures are disjoint", label, left, right)


def outward_decimal(value: Q, digits: int, upper: bool) -> str:
    scale = 10 ** digits
    if upper:
        integer = -((-value.numerator * scale) // value.denominator)
    else:
        integer = (value.numerator * scale) // value.denominator
    sign = "-" if integer < 0 else ""
    body = str(abs(integer)).rjust(digits + 1, "0")
    return f"{sign}{body[:-digits]}.{body[-digits:]}"


def main() -> None:
    require(sys.flags.isolated and sys.flags.safe_path,
            "run with isolated Python (-I)", sys.flags)
    require(sys.flags.dont_write_bytecode, "run with bytecode disabled (-B)")
    require(sys.flags.optimize == 0 and sys.flags.no_user_site,
            "unsafe Python flags", sys.flags)
    require(platform.python_version() == REQUIRED_PYTHON,
            "Python version mismatch", platform.python_version())
    require(os.environ.get("LC_ALL") == "C", "LC_ALL must equal C")
    require(os.environ.get("PYTHONDONTWRITEBYTECODE") == "1",
            "PYTHONDONTWRITEBYTECODE must equal 1")
    require(not os.environ.get("PYTHONPYCACHEPREFIX"),
            "PYTHONPYCACHEPREFIX must be unset")
    require(not Path(__file__).is_symlink(), "source symlink is forbidden")
    mode = SCRIPT_PATH.stat().st_mode
    require(stat.S_ISREG(mode), "certificate source is not regular")
    require(not (mode & (stat.S_IWGRP | stat.S_IWOTH)),
            "certificate source is group/world writable", oct(mode))
    script_sha = hashlib.sha256(SCRIPT_PATH.read_bytes()).hexdigest()

    log2 = log_interval(Q(2))
    log3 = log_interval(Q(3))
    log4 = log_interval(Q(4))
    log5 = log_interval(Q(5))
    log6 = log_interval(Q(6))
    log7 = log_interval(Q(7))
    log_7_5 = log_interval(Q(7, 5))

    # Closed forms, independently checked against literal complete cells.
    p4_closed = Q(5, 14) + log4 / 5 + log5 / 4 - 9 * log7 / 20
    p6_closed = Q(47, 210) + log5 / 6 + log6 / 5 - 11 * log7 / 30
    p4 = prefix_cell(5, 4, 6)
    p6 = prefix_cell(5, 6, 6)
    certify_same(p4, p4_closed, "P_5,6(4)")
    certify_same(p6, p6_closed, "P_5,6(6)")

    # H(m)=sum_{r<=6/m} Lambda(r)P_{5,6}(mr), so
    # D^3 H(2)=log(2)P(4)+(log(3)-3log(2))P(6).
    d3_h = log2 * p4 + (log3 - 3 * log2) * p6
    eta6 = Q(1, 5) / (Q(1, 5) + log6 / log7)
    a_5_6 = Q(6, 5) - log_7_5
    c = eta6 * log6 * a_5_6
    d3_k = d3_h + c / 20

    require(p4.lo > 0 and p6.lo > 0, "prefix Gram entry sign unresolved")
    require(c.lo > 0, "affine correction sign unresolved")
    require(d3_k.lo > Q(-1, 100), "lower target bound failed", d3_k)
    require(d3_k.hi < Q(-1, 125), "upper target bound failed", d3_k)

    print("certificate=physical-prefix-kernel-complete-monotonicity-failure")
    print("canonical_command=rm -f /tmp/cycle50-kernel-shape-counterexample.out && env -u PYTHONPYCACHEPREFIX PYTHONDONTWRITEBYTECODE=1 LC_ALL=C uv run --isolated --no-project --python 3.12.13 python -I -B millennium-prize/riemann-hypothesis/cycle50_kernel_shape_counterexample.py > /tmp/cycle50-kernel-shape-counterexample.out && cmp /tmp/cycle50-kernel-shape-counterexample.out millennium-prize/riemann-hypothesis/cycle50-kernel-shape-counterexample.out")
    print(f"runtime=CPython-{platform.python_version()} exact_stdlib_fraction")
    print(f"script_sha256={script_sha}")
    print("parameters=theta=2/5 a=4 q=5 n=6 difference=D^3_at_m=2")
    print(f"log_enclosure=atanh_series exact_fraction terms={TERMS}")
    print(
        "D3K_interval=["
        + outward_decimal(d3_k.lo, DIGITS, upper=False)
        + ","
        + outward_decimal(d3_k.hi, DIGITS, upper=True)
        + "]"
    )
    print("certified=-1/100<D3K<-1/125<0")
    print("scope=finite physical counterexample only; no prefix-norm or RH consequence")
    print("status=PASS")


if __name__ == "__main__":
    main()
