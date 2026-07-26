#!/usr/bin/env python3
"""Exact-integer certificate for the Cycle 52 hostile 12-window."""


def main() -> None:
    start = 47_255_689_915
    divisors = [7**2, 2**2, 3**2, 103**2, 43**2, 2**6,
                29**2, 17**2, 13**2, 2**2, 5**2, 3**3]
    for offset, divisor in enumerate(divisors):
        value = start + offset
        assert value % divisor == 0, (offset, value, divisor)
        # Every listed divisor contains a prime square.
        assert divisor in (64, 27) or int(divisor**0.5) ** 2 == divisor
    print("certified 12 consecutive nonsquarefree integers")
    print("start:", start)
    for offset, divisor in enumerate(divisors):
        print(offset, start + offset, divisor)


if __name__ == "__main__":
    main()
