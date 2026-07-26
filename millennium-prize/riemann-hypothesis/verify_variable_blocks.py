#!/usr/bin/env python3
"""Exact finite-prefix verifier for the abstract variable-block theorem.

All arithmetic is performed with ``fractions.Fraction``.  A successful finite
check verifies the hypotheses and quantitative estimate on the supplied block
prefix; divergence of an infinite weight sequence remains an analytic
hypothesis and cannot be certified from finite data.
"""

from dataclasses import dataclass
from fractions import Fraction
from numbers import Integral, Rational


def _fraction(value, name):
    if isinstance(value, bool) or not isinstance(value, Rational):
        raise TypeError(f"{name} must be an exact rational number")
    if isinstance(value, Integral):
        return Fraction(int(value))
    return Fraction(value.numerator, value.denominator)


@dataclass(frozen=True)
class Block:
    """The half-open integer block ``[left, right)``."""

    left: int
    right: int

    def __post_init__(self):
        if (
            isinstance(self.left, bool)
            or isinstance(self.right, bool)
            or not isinstance(self.left, int)
            or not isinstance(self.right, int)
        ):
            raise TypeError("block endpoints must be integers")
        if self.left < 0 or self.right <= self.left:
            raise ValueError("a block must satisfy 0 <= left < right")


@dataclass(frozen=True)
class BlockCheck:
    block: Block
    decrement: Fraction
    weighted_energy: Fraction
    slack: Fraction


@dataclass(frozen=True)
class VariableBlockPrefix:
    start: int
    end: int
    kappa: Fraction
    checks: tuple
    total_weight: Fraction
    total_weighted_energy: Fraction
    total_decrement: Fraction
    endpoint_decrement: Fraction
    aggregate_slack: Fraction


def verify_variable_block_prefix(values, weights, blocks, kappa):
    """Verify one exact prefix of a chained variable-block certificate.

    ``values[n]`` is ``P_n`` and ``weights[n]`` is ``w_n``.  The blocks must
    form an exact chain: the right endpoint of each block is the left endpoint
    of the next.  Every required value and weight must be present.  Extra map
    entries are ignored, which permits checking a prefix of a larger data set.

    Returns exact per-block and aggregate data.  Raises ``ValueError`` when a
    theorem hypothesis or block inequality fails.
    """
    blocks = tuple(blocks)
    if not blocks:
        raise ValueError("at least one block is required")
    if not all(isinstance(block, Block) for block in blocks):
        raise TypeError("blocks must contain Block instances")
    for previous, current in zip(blocks, blocks[1:]):
        if current.left != previous.right:
            relation = "overlap" if current.left < previous.right else "gap"
            raise ValueError(
                f"blocks must form an exact chain; {relation} between "
                f"[{previous.left}, {previous.right}) and "
                f"[{current.left}, {current.right})"
            )

    kappa = _fraction(kappa, "kappa")
    if kappa <= 0:
        raise ValueError("kappa must be positive")

    start, end = blocks[0].left, blocks[-1].right
    exact_values = {}
    for n in range(start, end + 1):
        if n not in values:
            raise ValueError(f"missing P_{n}")
        exact_values[n] = _fraction(values[n], f"P_{n}")
        if exact_values[n] < 0:
            raise ValueError(f"P_{n} must be nonnegative")

    exact_weights = {}
    for n in range(start, end):
        if n not in weights:
            raise ValueError(f"missing w_{n}")
        exact_weights[n] = _fraction(weights[n], f"w_{n}")
        if exact_weights[n] < 0:
            raise ValueError(f"w_{n} must be nonnegative")

    checks = []
    for block in blocks:
        decrement = exact_values[block.left] - exact_values[block.right]
        weighted_energy = sum(
            (exact_weights[n] * exact_values[n]
             for n in range(block.left, block.right)),
            Fraction(0),
        )
        slack = decrement - kappa * weighted_energy
        if slack < 0:
            raise ValueError(
                f"block [{block.left}, {block.right}) fails by {-slack}"
            )
        checks.append(BlockCheck(block, decrement, weighted_energy, slack))

    total_weight = sum(
        (exact_weights[n] for n in range(start, end)), Fraction(0)
    )
    total_weighted_energy = sum(
        (check.weighted_energy for check in checks), Fraction(0)
    )
    total_decrement = sum(
        (check.decrement for check in checks), Fraction(0)
    )
    endpoint_decrement = exact_values[start] - exact_values[end]
    if total_decrement != endpoint_decrement:
        raise AssertionError("internal error: chained decrements did not telescope")

    return VariableBlockPrefix(
        start=start,
        end=end,
        kappa=kappa,
        checks=tuple(checks),
        total_weight=total_weight,
        total_weighted_energy=total_weighted_energy,
        total_decrement=total_decrement,
        endpoint_decrement=endpoint_decrement,
        aggregate_slack=total_decrement - kappa * total_weighted_energy,
    )
