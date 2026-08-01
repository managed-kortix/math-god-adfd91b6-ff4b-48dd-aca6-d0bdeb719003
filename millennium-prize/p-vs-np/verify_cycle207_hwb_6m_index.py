#!/usr/bin/env python3
"""Exact small-m verifier for the HWB_(6m) every-order INDEX_m minor."""

import argparse
from dataclasses import dataclass
from itertools import combinations, product
from math import comb
from typing import Iterable, Sequence


@dataclass(frozen=True)
class Certificate:
    m: int
    prefix: tuple[int, ...]
    suffix: tuple[int, ...]
    base_weight: int
    data: tuple[int, ...]
    compensators: tuple[int, ...]
    query_weights: tuple[int, ...]


def hwb(bits: Sequence[int]) -> int:
    weight = sum(bits)
    return 0 if weight == 0 else bits[weight - 1]


def construct(m: int, prefix: Iterable[int]) -> Certificate:
    if m < 1:
        raise ValueError("m must be positive")
    size = 6 * m
    prefix_tuple = tuple(sorted(prefix))
    if len(prefix_tuple) != 4 * m or len(set(prefix_tuple)) != 4 * m:
        raise ValueError("prefix must contain exactly 4m distinct coordinates")
    if prefix_tuple[0] < 1 or prefix_tuple[-1] > size:
        raise ValueError("prefix coordinates must lie in [1,6m]")

    prefix_set = set(prefix_tuple)
    first = tuple(i for i in prefix_tuple if m <= i <= 3 * m)
    second = tuple(i for i in prefix_tuple if 3 * m <= i <= 5 * m)
    if len(first) >= m:
        base_weight = m
        data = first[:m]
    elif len(second) >= m:
        base_weight = 3 * m
        data = second[:m]
    else:
        raise AssertionError("neither address interval contains m prefix coordinates")

    data_set = set(data)
    compensators = tuple(i for i in prefix_tuple if i not in data_set)[:m]
    suffix = tuple(i for i in range(1, size + 1) if i not in prefix_set)
    certificate = Certificate(
        m=m,
        prefix=prefix_tuple,
        suffix=suffix,
        base_weight=base_weight,
        data=data,
        compensators=compensators,
        query_weights=tuple(i - base_weight for i in data),
    )
    verify_structure(certificate)
    return certificate


def verify_structure(certificate: Certificate) -> None:
    m = certificate.m
    universe = set(range(1, 6 * m + 1))
    prefix = set(certificate.prefix)
    suffix = set(certificate.suffix)
    data = set(certificate.data)
    compensators = set(certificate.compensators)
    remainder = prefix - data - compensators

    assert len(prefix) == 4 * m
    assert len(suffix) == 2 * m
    assert prefix.isdisjoint(suffix) and prefix | suffix == universe
    assert len(data) == len(compensators) == m
    assert data.isdisjoint(compensators)
    assert data | compensators <= prefix
    assert len(remainder) == 2 * m
    assert certificate.base_weight in (m, 3 * m)
    assert len(set(certificate.query_weights)) == m
    assert all(0 <= weight <= 2 * m for weight in certificate.query_weights)
    assert tuple(i - certificate.base_weight for i in certificate.data) == (
        certificate.query_weights
    )


def materialize(certificate: Certificate) -> tuple[tuple[int, ...], ...]:
    m = certificate.m
    size = 6 * m
    prefix = set(certificate.prefix)
    data = set(certificate.data)
    compensators = set(certificate.compensators)
    remainder = tuple(sorted(prefix - data - compensators))
    fixed_ones = certificate.base_weight - m

    columns = []
    for query_weight in certificate.query_weights:
        column = [0] * size
        for index in certificate.suffix[:query_weight]:
            column[index - 1] = 1
        assert sum(column) == query_weight
        columns.append(column)
    assert len({tuple(column) for column in columns}) == m

    matrix = []
    for word in product((0, 1), repeat=m):
        row = [0] * size
        for bit, index, compensator in zip(
            word, certificate.data, certificate.compensators
        ):
            row[index - 1] = bit
            row[compensator - 1] = 1 - bit
        for index in remainder[:fixed_ones]:
            row[index - 1] = 1
        assert sum(row) == certificate.base_weight

        outputs = []
        for column, index in zip(columns, certificate.data):
            completed = [left | right for left, right in zip(row, column)]
            assert sum(completed) == index
            outputs.append(hwb(completed))
        assert tuple(outputs) == word
        matrix.append(tuple(outputs))

    result = tuple(matrix)
    assert len(result) == len(set(result)) == 2**m
    return result


def exhaustive_check(max_m: int) -> None:
    total = 0
    for m in range(1, max_m + 1):
        count = 0
        for prefix in combinations(range(1, 6 * m + 1), 4 * m):
            try:
                materialize(construct(m, prefix))
            except (AssertionError, ValueError) as error:
                raise AssertionError(
                    f"COUNTERPARTITION m={m} P={list(prefix)}: {error}"
                ) from error
            count += 1
        assert count == comb(6 * m, 4 * m)
        total += count
        print(f"exhaustive m={m} N={6 * m}: {count} cuts, all verified")
    print(f"exhaustive total: {total} cuts; no counterpartition")


def representative_check(max_m: int) -> None:
    count = 0
    for m in range(1, max_m + 1):
        size = 6 * m
        partitions = (
            tuple(range(1, 4 * m + 1)),
            tuple(range(2 * m + 1, size + 1)),
            tuple(i for i in range(1, size + 1) if i % 3 != 0),
            tuple(i for i in range(1, size + 1) if i % 3 != 1),
        )
        for prefix in partitions:
            construct(m, prefix)
            count += 1
    print(f"structural: {count} representative certificates through m={max_m}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-m", type=int, default=3)
    parser.add_argument("--general-max-m", type=int, default=64)
    args = parser.parse_args()
    if args.max_m < 0 or args.general_max_m < 1:
        parser.error("--max-m must be nonnegative and --general-max-m positive")
    exhaustive_check(args.max_m)
    representative_check(args.general_max_m)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
