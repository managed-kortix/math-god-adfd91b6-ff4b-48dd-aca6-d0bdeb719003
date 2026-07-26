#!/usr/bin/env python3
"""Exact colored cluster-partition audit for rank-ten cactus residuals."""

from __future__ import annotations

from fractions import Fraction


TRIANGLE_MARGIN = {1: 0, 2: 1, 3: 2, 4: 3, 5: 2, 6: 1, 7: 0, 8: 0, 9: 0}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def partitions(triangles, distinguished, minimum=(0, 0)):
    result = []
    for triangle_count in range(triangles + 1):
        for distinguished_count in range(distinguished + 1):
            part = (triangle_count, distinguished_count)
            if sum(part) == 0 or part < minimum:
                continue
            if part == (triangles, distinguished):
                result.append((part,))
                continue
            for rest in partitions(
                triangles - triangle_count,
                distinguished - distinguished_count,
                part,
            ):
                result.append((part,) + rest)
    return result


def triangle_bound(triangles):
    return Fraction(TRIANGLE_MARGIN[triangles]), True


def tq_bound(part):
    triangles, q_count = part
    rank = triangles + q_count
    if q_count == 0:
        return triangle_bound(triangles)
    if triangles == 0:
        return Fraction(-1), False
    if triangles == 1:
        return Fraction(0), True
    if rank in (2, 3):
        return Fraction(0), False
    return Fraction(0), True


def tpp_bound(part):
    triangles, pentagons = part
    rank = triangles + pentagons
    if pentagons == 0:
        return triangle_bound(triangles)
    if part == (0, 1):
        return Fraction(-1, 4), False
    if part == (1, 1):
        return Fraction(3, 4), True
    if part == (0, 2):
        return Fraction(0), True
    if part == (1, 2):
        return Fraction(3, 2), True
    if rank in (2, 3):
        return Fraction(0), False
    return Fraction(0), True


def audit(triangles, distinguished, bound):
    all_rows = partitions(triangles, distinguished)
    proper_rows = tuple(row for row in all_rows if len(row) > 1)
    structural = []
    for row in proper_rows:
        entries = tuple(bound(part) for part in row)
        total = sum((value for value, _ in entries), Fraction())
        strict = any(strict for _, strict in entries)
        if not (total > 0 or (total == 0 and strict)):
            structural.append(row)
    return tuple(all_rows), proper_rows, tuple(structural)


def main():
    t9q = audit(9, 1, tq_bound)
    t8pp = audit(8, 2, tpp_bound)
    require(tuple(map(len, t9q)) == (97, 96, 4), "T^9Q partition census changed")
    require(tuple(map(len, t8pp)) == (181, 180, 10), "T^8PP partition census changed")

    expected_t9q = (
        ((0, 1),) + ((1, 0),) * 9,
        ((0, 1), (1, 0), (1, 0), (7, 0)),
        ((0, 1), (1, 0), (8, 0)),
        ((0, 1), (9, 0)),
    )
    expected_t8pp = (
        ((0, 1), (0, 1)) + ((1, 0),) * 8,
        ((0, 1), (0, 1), (1, 0), (7, 0)),
        ((0, 1), (0, 1), (8, 0)),
        ((0, 1),) + ((1, 0),) * 6 + ((2, 1),),
        ((0, 1),) + ((1, 0),) * 5 + ((3, 1),),
        ((0, 1),) + ((1, 0),) * 4 + ((4, 1),),
        ((0, 1),) + ((1, 0),) * 3 + ((5, 1),),
        ((0, 1),) + ((1, 0),) * 2 + ((6, 1),),
        ((0, 1), (1, 0), (7, 1)),
        ((0, 1), (8, 1)),
    )
    require(t9q[2] == expected_t9q, "T^9Q structural rows changed")
    require(t8pp[2] == expected_t8pp, "T^8PP structural rows changed")

    print("T^9Q partitions: 97 total, 96 proper, 92 direct, 4 structural")
    for row in t9q[2]:
        print(" ", row)
    print("T^8PP partitions: 181 total, 180 proper, 170 direct, 10 structural")
    for row in t8pp[2]:
        print(" ", row)
    print("exact disconnected endpoints: A_9|Q, T^8P|P, P|A_8|P")


if __name__ == "__main__":
    main()
