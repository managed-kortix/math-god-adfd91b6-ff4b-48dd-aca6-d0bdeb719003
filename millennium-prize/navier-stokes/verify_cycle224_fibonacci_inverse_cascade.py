#!/usr/bin/env python3
"""Exact bookkeeping for the Cycle 224 finite 2D Euler packet."""

from fractions import Fraction as F


def add(p, q):
    return (p[0] + q[0], p[1] + q[1])


def neg(p):
    return (-p[0], -p[1])


def det(p, q):
    return p[0] * q[1] - p[1] * q[0]


def norm2(p):
    return p[0] * p[0] + p[1] * p[1]


def ordered_euler_coefficient(p, q):
    """Cycle 212 coefficient for k_perp=(k2,-k1)."""
    return F(-det(p, q), norm2(p))


def canonical_convolution(omega):
    result = {}
    for p, omega_p in omega.items():
        for q, omega_q in omega.items():
            r = add(p, q)
            if r != (0, 0):
                result[r] = result.get(r, F(0)) + ordered_euler_coefficient(p, q) * omega_p * omega_q
    return {r: value for r, value in result.items() if value}


def main():
    fib = [0, 1]
    for _ in range(8):
        fib.append(fib[-1] + fib[-2])
    k = {j: (fib[j + 1], fib[j]) for j in range(1, 9)}
    expected_norm2 = [2, 5, 13, 34, 89, 233, 610, 1597]
    assert [norm2(k[j]) for j in range(1, 9)] == expected_norm2
    assert all(add(k[j], k[j + 1]) == k[j + 2] for j in range(1, 7))

    signs = {1: -1, 2: -1}
    for j in range(1, 7):
        signs[j + 2] = -det(k[j], k[j + 1]) * signs[j] * signs[j + 1]
    assert [signs[j] for j in range(1, 9)] == [-1, -1, 1, 1, 1, -1, -1, -1]

    amplitudes = {
        j: F(signs[j], 16) if j <= 6 else F(signs[j]) for j in range(1, 9)
    }
    omega = {}
    for j in range(1, 9):
        omega[k[j]] = amplitudes[j]
        omega[neg(k[j])] = amplitudes[j]

    convolution = canonical_convolution(omega)
    paired_convolution = {}
    modes = list(omega)
    for i, p in enumerate(modes):
        for q in modes[i + 1:]:
            r = add(p, q)
            if r == (0, 0):
                continue
            coefficient = -det(p, q) * (F(1, norm2(p)) - F(1, norm2(q)))
            paired_convolution[r] = paired_convolution.get(r, F(0)) + coefficient * omega[p] * omega[q]
    paired_convolution = {r: value for r, value in paired_convolution.items() if value}
    assert paired_convolution == convolution
    leakage = {r: value for r, value in convolution.items() if r not in omega}

    assert len(leakage) == 60
    leakage_l1 = sum(abs(value) for value in leakage.values())
    leakage_l2_sq = sum(value * value for value in leakage.values())
    leakage_hminus1_sq = sum(
        value * value / norm2(r) for r, value in leakage.items()
    )
    intended_hminus1_sq = sum(
        convolution[r] * convolution[r] / norm2(r) for r in omega
    )
    initial_enstrophy = sum(value * value for value in omega.values())
    assert leakage_l1 == F(78334784061659, 21979083259520)
    assert leakage_l2_sq == F(
        63086613807192553004774156621,
        65312429645588943997069230080,
    )
    assert leakage_hminus1_sq == F(
        302948011971805436487777307554270959230223553631407,
        341276900629764981757462405902609933481946700351078400,
    )
    assert intended_hminus1_sq == F(
        68002292498686558323,
        59106271172478682350288896,
    )
    assert initial_enstrophy == F(259, 64)

    rates = []
    for j in range(1, 7):
        low, middle, high = k[j], k[j + 1], k[j + 2]
        d = det(low, middle)
        product = amplitudes[j] * amplitudes[j + 1] * amplitudes[j + 2]
        low_rate = -4 * d * (F(1, norm2(middle)) - F(1, norm2(high))) * product
        middle_rate = -4 * d * (F(1, norm2(high)) - F(1, norm2(low))) * product
        high_rate = -4 * d * (F(1, norm2(low)) - F(1, norm2(middle))) * product
        assert low_rate > 0 and middle_rate < 0 and high_rate > 0
        assert low_rate + middle_rate + high_rate == 0
        assert (
            low_rate / norm2(low)
            + middle_rate / norm2(middle)
            + high_rate / norm2(high)
            == 0
        )
        isolated = {
            mode: amplitudes[index]
            for index, rail in ((j, low), (j + 1, middle), (j + 2, high))
            for mode in (rail, neg(rail))
        }
        isolated_rhs = canonical_convolution(isolated)
        assert (
            4 * amplitudes[j] * isolated_rhs[low],
            4 * amplitudes[j + 1] * isolated_rhs[middle],
            4 * amplitudes[j + 2] * isolated_rhs[high],
        ) == (low_rate, middle_rate, high_rate)
        rates.append((j, low_rate, middle_rate, high_rate))

    print("Cycle 224 instantaneous isolated-triad upscale-biased packet")
    print("frequencies =", [k[j] for j in range(1, 9)])
    print("amplitudes =", [str(amplitudes[j]) for j in range(1, 9)])
    print("signed pair-enstrophy rates (low, middle, high) =")
    for row in rates:
        print(row[0], *(str(value) for value in row[1:]))
    print("exterior nonzero modes =", len(leakage))
    print("leakage l1 =", leakage_l1)
    print("leakage l2 squared =", leakage_l2_sq)
    print("leakage H^-1 squared =", leakage_hminus1_sq)
    print("intended H^-1 forcing squared =", intended_hminus1_sq)
    print("leakage/intended H^-1 forcing ratio =", leakage_hminus1_sq / intended_hminus1_sq)
    print("initial sum |omega_m|^2 =", initial_enstrophy)
    print("unit-enstrophy amplitude scale squared =", F(1, initial_enstrophy))
    print("canonical ordered/pair-symmetrized convolution cross-test passed")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
