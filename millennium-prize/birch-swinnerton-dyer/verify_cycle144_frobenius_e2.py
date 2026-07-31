#!/usr/bin/env python3
"""Exact integer audit of the Cycle 144 Frobenius/E2 certificate."""

P = 7
N = 8
M = P ** N
A, B, C, D = 3443986, 4648947, 124425, 2320812
EXPECTED_ALPHA = 3795817
EXPECTED_S2 = 2509791
EXPECTED_E2 = 4471315


def unit_root():
    alpha = 4
    modulus = P
    for _ in range(1, N):
        new_modulus = modulus * P
        lifts = [
            alpha + digit * modulus for digit in range(P)
            if ((alpha + digit * modulus) ** 2
                + 3 * (alpha + digit * modulus) + P) % new_modulus == 0
        ]
        assert len(lifts) == 1
        alpha = lifts[0]
        modulus = new_modulus
    return alpha


def main():
    assert (A + D + 3) % M == 0
    assert (A * D - B * C - P) % M == 0
    alpha = unit_root()
    assert alpha == EXPECTED_ALPHA
    s2 = B * pow(alpha - A, -1, M) % M
    assert s2 == EXPECTED_S2
    assert (A * s2 + B - alpha * s2) % M == 0
    assert (C * s2 + D - alpha) % M == 0
    e2 = (1 - 12 * s2) % M
    assert e2 == EXPECTED_E2
    print("Cycle 144 Frobenius/E2 certificate")
    print("modulus =", M)
    print("unit root =", alpha)
    print("sigma parameter s2 =", s2)
    print("E2 =", e2)
    print("all exact checks passed")


if __name__ == "__main__":
    main()
