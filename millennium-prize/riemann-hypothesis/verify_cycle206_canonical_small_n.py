#!/usr/bin/env python3
"""Exact rational audit for the cycle-206 N=1 canonical-system scout."""

from fractions import Fraction


def xi_disk_bound(omega: Fraction, radius: Fraction) -> Fraction:
    """Return the proved bound for |xi(s)| on |s-(1/2+omega)| <= radius."""
    if omega <= 0:
        raise ValueError("omega must be positive")
    if radius < 0:
        raise ValueError("radius must be nonnegative")
    center = Fraction(1, 2) + omega
    size = center + radius
    alpha = max((center + radius) / 2, (1 - center + radius) / 2)
    if not 0 <= alpha < 3:
        raise ValueError("the elementary exponential majorant requires 0 <= alpha < 3")
    return Fraction(1, 2) + size * (size + 1) / (19 * (3 - alpha))


def certificate() -> dict[str, Fraction]:
    omega = Fraction(1)
    disk_radius = Fraction(1)
    h = Fraction(1, 4)

    target_value_bound = xi_disk_bound(omega, disk_radius)
    target_derivative_bound = xi_disk_bound(omega, disk_radius + 1)
    target_kernel_bound = (
        target_value_bound * target_derivative_bound / 3
    )

    # Here 2*h*disk_radius = 1/2 and exp(1/2) < sum_{n>=0}(1/2)^n = 2.
    endpoint_kernel_bound = 2 * h / 3
    uniform_error_bound = target_kernel_bound + endpoint_kernel_bound

    return {
        "omega": omega,
        "disk_radius": disk_radius,
        "h_11": h,
        "h_22": h,
        "target_value_bound": target_value_bound,
        "target_derivative_bound": target_derivative_bound,
        "target_kernel_bound": target_kernel_bound,
        "endpoint_kernel_bound": endpoint_kernel_bound,
        "uniform_error_bound": uniform_error_bound,
    }


def main() -> None:
    values = certificate()
    expected = {
        "target_value_bound": Fraction(203, 266),
        "target_derivative_bound": Fraction(221, 190),
        "target_kernel_bound": Fraction(44863, 151620),
        "endpoint_kernel_bound": Fraction(1, 6),
        "uniform_error_bound": Fraction(70133, 151620),
    }
    for name, expected_value in expected.items():
        if values[name] != expected_value:
            raise RuntimeError(f"{name}: got {values[name]}, expected {expected_value}")
    if values["uniform_error_bound"] >= Fraction(1, 2):
        raise RuntimeError("the certified uniform error is not below 1/2")

    print("cycle-206 exact N=1 certificate")
    for name, value in values.items():
        print(f"{name}={value} (~{float(value):.12g})")
    print("PASS: uniform kernel error < 1/2 on |z|,|w| <= 1")


if __name__ == "__main__":
    main()
