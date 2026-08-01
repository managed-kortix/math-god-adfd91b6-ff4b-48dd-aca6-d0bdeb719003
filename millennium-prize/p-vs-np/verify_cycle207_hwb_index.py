#!/usr/bin/env python3
"""Dependency-free verifier for the all-order HWB INDEX construction."""

import argparse
from dataclasses import dataclass
from itertools import combinations, product
from math import comb
from typing import Iterable, Iterator, Sequence


@dataclass(frozen=True)
class MinorCertificate:
    m: int
    prefix: tuple[int, ...]
    suffix: tuple[int, ...]
    base_weight: int
    data: tuple[int, ...]
    compensators: tuple[int, ...]
    query_weights: tuple[int, ...]


def hwb(bits: Sequence[int]) -> int:
    """Evaluate HWB with one-based addressing and HWB(0,...,0)=0."""
    weight = sum(bits)
    return 0 if weight == 0 else bits[weight - 1]


def construct_certificate(m: int, prefix: Iterable[int]) -> MinorCertificate:
    """Construct the Cycle 206 INDEX_m minor for one midpoint partition."""
    if m < 1:
        raise ValueError("m must be positive")
    size = 8 * m
    prefix_tuple = tuple(sorted(prefix))
    if len(prefix_tuple) != 4 * m or len(set(prefix_tuple)) != 4 * m:
        raise ValueError("prefix must contain exactly 4m distinct indices")
    if not prefix_tuple or prefix_tuple[0] < 1 or prefix_tuple[-1] > size:
        raise ValueError("prefix indices must lie in [1,8m]")

    prefix_set = set(prefix_tuple)
    candidates_0 = tuple(i for i in prefix_tuple if m <= i <= 5 * m)
    candidates_1 = tuple(i for i in prefix_tuple if 3 * m <= i <= 7 * m)
    if len(candidates_0) >= m:
        base_weight = m
        data = candidates_0[:m]
    elif len(candidates_1) >= m:
        base_weight = 3 * m
        data = candidates_1[:m]
    else:
        raise AssertionError("counterpartition: neither address interval works")

    data_set = set(data)
    compensators = tuple(i for i in prefix_tuple if i not in data_set)[:m]
    suffix = tuple(i for i in range(1, size + 1) if i not in prefix_set)
    query_weights = tuple(i - base_weight for i in data)
    certificate = MinorCertificate(
        m, prefix_tuple, suffix, base_weight, data, compensators, query_weights
    )
    verify_certificate_structure(certificate)
    return certificate


def verify_certificate_structure(certificate: MinorCertificate) -> None:
    """Check the construction symbolically, without enumerating 2^m rows."""
    m = certificate.m
    prefix = set(certificate.prefix)
    suffix = set(certificate.suffix)
    data = set(certificate.data)
    compensators = set(certificate.compensators)
    assert len(prefix) == len(suffix) == 4 * m
    assert prefix.isdisjoint(suffix)
    assert prefix | suffix == set(range(1, 8 * m + 1))
    assert len(data) == len(compensators) == m
    assert data.isdisjoint(compensators)
    assert data | compensators <= prefix
    assert certificate.base_weight in (m, 3 * m)
    assert len(certificate.query_weights) == m
    assert len(set(certificate.query_weights)) == m
    assert all(0 <= weight <= 4 * m for weight in certificate.query_weights)
    assert tuple(i - certificate.base_weight for i in certificate.data) == (
        certificate.query_weights
    )

    # Every data/compensator pair contributes one. The optional fixed ones
    # contribute 2m, so every prefix row has the declared constant weight.
    fixed_ones = certificate.base_weight - m
    unpaired = prefix - data - compensators
    assert fixed_ones in (0, 2 * m)
    assert len(unpaired) == 2 * m
    assert fixed_ones <= len(unpaired)
    for addressed_index, suffix_weight in zip(
        certificate.data, certificate.query_weights
    ):
        assert certificate.base_weight + suffix_weight == addressed_index


def materialize_minor(certificate: MinorCertificate) -> tuple[tuple[int, ...], ...]:
    """Build and directly evaluate the complete 2^m by m communication minor."""
    m = certificate.m
    size = 8 * m
    prefix = set(certificate.prefix)
    data = set(certificate.data)
    compensators = set(certificate.compensators)
    unpaired = tuple(sorted(prefix - data - compensators))
    fixed_ones = certificate.base_weight - m
    columns = []
    for suffix_weight in certificate.query_weights:
        column = [0] * size
        for index in certificate.suffix[:suffix_weight]:
            column[index - 1] = 1
        assert all(column[index - 1] == 0 for index in certificate.data)
        columns.append(column)
    assert len({tuple(column) for column in columns}) == m

    matrix = []
    for word in product((0, 1), repeat=m):
        row_bits = [0] * size
        for bit, data_index, compensator in zip(
            word, certificate.data, certificate.compensators
        ):
            row_bits[data_index - 1] = bit
            row_bits[compensator - 1] = 1 - bit
        for index in unpaired[:fixed_ones]:
            row_bits[index - 1] = 1
        assert sum(row_bits) == certificate.base_weight

        outputs = []
        for column, suffix_weight in zip(columns, certificate.query_weights):
            completed = [a | b for a, b in zip(row_bits, column)]
            assert sum(completed) == certificate.base_weight + suffix_weight
            outputs.append(hwb(completed))
        assert tuple(outputs) == word
        matrix.append(tuple(outputs))

    result = tuple(matrix)
    assert len(result) == 2**m
    assert len(set(result)) == 2**m
    return result


def midpoint_partitions(m: int) -> Iterator[tuple[int, ...]]:
    return combinations(range(1, 8 * m + 1), 4 * m)


def exhaustive_check(max_m: int) -> int:
    checked = 0
    for m in range(1, max_m + 1):
        count = 0
        for prefix in midpoint_partitions(m):
            try:
                certificate = construct_certificate(m, prefix)
                materialize_minor(certificate)
            except (AssertionError, ValueError) as error:
                print(f"COUNTERPARTITION m={m} P={list(prefix)}: {error}")
                return 1
            count += 1
        expected = comb(8 * m, 4 * m)
        assert count == expected
        checked += count
        print(f"exhaustive m={m} N={8 * m}: {count} partitions, all verified")
    print(f"exhaustive total: {checked} midpoint partitions; no counterpartition")
    return 0


def representative_partitions(m: int) -> tuple[tuple[int, ...], ...]:
    size = 8 * m
    low = tuple(range(1, 4 * m + 1))
    high = tuple(range(4 * m + 1, size + 1))
    odd = tuple(range(1, size + 1, 2))
    scattered = tuple(sorted(((i + 3 * m) % size) + 1 for i in range(4 * m)))
    return low, high, odd, scattered


def constructive_check(max_m: int) -> None:
    checked = 0
    for m in range(1, max_m + 1):
        for prefix in representative_partitions(m):
            construct_certificate(m, prefix)
            checked += 1
    print(
        f"constructive general check: {checked} certificates through "
        f"m={max_m} (N={8 * max_m}); all structural identities verified"
    )


def parse_partition(text: str) -> tuple[int, ...]:
    try:
        return tuple(int(part) for part in text.split(",") if part)
    except ValueError as error:
        raise argparse.ArgumentTypeError("partition must be comma-separated integers") from error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--max-m",
        type=int,
        default=2,
        help="exhaustively enumerate midpoint partitions for 1 <= m <= MAX_M",
    )
    parser.add_argument(
        "--general-max-m",
        type=int,
        default=64,
        help="structurally check representative partitions through this m",
    )
    parser.add_argument(
        "--partition",
        type=parse_partition,
        help="also verify one comma-separated, one-based midpoint prefix",
    )
    args = parser.parse_args()
    if args.max_m < 0 or args.general_max_m < 1:
        parser.error("--max-m must be nonnegative and --general-max-m positive")

    if exhaustive_check(args.max_m):
        return 1
    constructive_check(args.general_max_m)
    if args.partition is not None:
        if len(args.partition) % 4:
            parser.error("the supplied partition must have size 4m")
        m = len(args.partition) // 4
        certificate = construct_certificate(m, args.partition)
        if m <= 16:
            materialize_minor(certificate)
            mode = "complete minor"
        else:
            mode = "structural certificate"
        print(
            f"supplied partition m={m}: {mode} verified; "
            f"r={certificate.base_weight}, data={list(certificate.data)}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
