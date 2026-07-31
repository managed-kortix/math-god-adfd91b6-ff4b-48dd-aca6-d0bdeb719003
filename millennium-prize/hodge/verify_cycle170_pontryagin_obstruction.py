#!/usr/bin/env python3
"""Exact Pontryagin-square check for the Cycle 169 projector cycle."""


COEFFICIENTS = (
    317131927490234375,
    -2073948378906250,
    12564289203125,
    -56707735500,
    27598945,
    3626326,
    -68381,
)


def gaussian_multiply(x, y):
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def gaussian_norm(x):
    return x[0] * x[0] + x[1] * x[1]


def main():
    powers = [(1, 0)]
    for _ in range(6):
        powers.append(gaussian_multiply(powers[-1], (2, 1)))

    assert powers == [
        (1, 0),
        (2, 1),
        (3, 4),
        (2, 11),
        (-7, 24),
        (-38, 41),
        (-117, 44),
    ]

    square_coefficient = 0
    for i in range(7):
        for j in range(i + 1, 7):
            difference = (
                powers[i][0] - powers[j][0],
                powers[i][1] - powers[j][1],
            )
            square_coefficient += (
                2
                * COEFFICIENTS[i]
                * COEFFICIENTS[j]
                * gaussian_norm(difference) ** 3
            )

    expected = -104188231402289079266552000000000000
    assert square_coefficient == expected
    assert square_coefficient < 0

    print("Cycle 170 Pontryagin obstruction")
    print(f"powers of 2+i: {powers}")
    print(f"coefficient of [A] in Z*Z: {square_coefficient}")
    print("negative coefficient excludes every effective representative")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
