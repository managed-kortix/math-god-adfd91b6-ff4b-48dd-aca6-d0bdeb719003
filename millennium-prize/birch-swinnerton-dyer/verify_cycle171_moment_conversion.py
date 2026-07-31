#!/usr/bin/env python3
"""Exact finite audit of the Cycle 171 normalization scalar."""


def padic_log_one_plus_p(p: int, precision: int) -> int:
    modulus = p**precision
    value = 0
    for k in range(1, 8 * precision):
        denominator = k
        valuation = 0
        while denominator % p == 0:
            denominator //= p
            valuation += 1
        if k - valuation >= precision:
            continue
        term = p ** (k - valuation) * pow(denominator, -1, modulus)
        value = (value + (term if k % 2 else -term)) % modulus
    return value


def main() -> None:
    p = 7
    precision = 6
    modulus = p**precision

    alpha = 3795817 % modulus
    assert (alpha * alpha + 3 * alpha + p) % modulus == 0

    log8 = padic_log_one_plus_p(p, precision + 4)
    log_unit = (log8 // p) % modulus
    assert log8 % (p**8) == 1157779
    assert (log8 * log8) % (p**8) == 3389918

    moment = 76676
    regulator_unit = 50931
    log_square_unit = log_unit * log_unit % modulus
    normalized_regulator = regulator_unit * pow(log_square_unit, -1, modulus) % modulus
    ordinary_euler_square = (1 - pow(alpha, -1, modulus)) ** 2 % modulus
    taylor_coefficient = moment * pow(2, -1, modulus) % modulus

    assert log_square_unit == 69182
    assert normalized_regulator == 91398
    assert ordinary_euler_square == 22779
    assert taylor_coefficient == 38338
    assert normalized_regulator * ordinary_euler_square % modulus == taylor_coefficient

    print("Cycle 171 ordinary moment/derivative conversion")
    print(f"log_7(8) mod 7^8 = {log8 % (p**8)}")
    print(f"log_7(8)^2 mod 7^8 = {(log8 * log8) % (p**8)}")
    print(f"M2/2 mod 7^6 = {taylor_coefficient}")
    print(f"(1-alpha^-1)^2 mod 7^6 = {ordinary_euler_square}")
    print("PASS: period, coordinate, Euler-factor, and regulator packets agree")


if __name__ == "__main__":
    main()
