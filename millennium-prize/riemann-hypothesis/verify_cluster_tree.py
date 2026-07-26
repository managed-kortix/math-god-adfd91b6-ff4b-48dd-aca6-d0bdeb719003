#!/usr/bin/env python3
"""Finite certified 1D cluster-tree prototype for the RH tail kernel.

This is deliberately a finite realization: both frequencies and coefficients
are explicit ``Fraction`` objects, and no claim is made about an infinite
frequency limit or RH.  Dense leaves use direct Arb Si/Ci kernel evaluation.
Admissible far leaves use the separated-kernel theorem implemented in
``verify_separated_kernel.py`` and propagate its entrywise remainder with the
exact local coefficient l1 masses.
"""

import argparse
import math
from dataclasses import dataclass
from fractions import Fraction

from flint import acb, arb, ctx

from verify_separated_kernel import ball, direct_d, theorem_bounds


@dataclass(frozen=True)
class Cluster:
    indices: tuple
    left: object = None
    right: object = None


@dataclass
class Stats:
    dense_leaves: int = 0
    compressed_leaves: int = 0
    dense_entries: int = 0
    compressed_entries: int = 0
    ordered_entries: int = 0
    rank_sum: int = 0
    max_rank: int = 0
    theorem_radius: object = None

    def __post_init__(self):
        self.theorem_radius = arb(0)


def build_cluster(indices, leaf_size):
    indices = tuple(indices)
    if len(indices) <= leaf_size:
        return Cluster(indices)
    cut = len(indices) // 2
    return Cluster(
        indices,
        build_cluster(indices[:cut], leaf_size),
        build_cluster(indices[cut:], leaf_size),
    )


def geometry(frequencies, rows, cols):
    A = [frequencies[i] for i in rows]
    B = [frequencies[j] for j in cols]
    amin, amax, bmin, bmax = A[0], A[-1], B[0], B[-1]
    a0, b0 = (amin + amax) / 2, (bmin + bmax) / 2
    H = (amax - amin + bmax - bmin) / 2
    return a0, b0, a0 - b0, a0 + b0, H


def admissible(frequencies, left, right, eta):
    """Orient the block as A=right, B=left and test H/d0 <= eta."""
    _, _, d0, _, H = geometry(frequencies, right.indices, left.indices)
    return H < d0 and H <= eta * d0


def inverse_coefficients(Q, center, n, p):
    """Coefficients of the degree-p endpoint amplitude polynomial."""
    q, c = ball(Q), ball(center)
    coefficients = []
    for j in range(p + 1):
        value = acb(0)
        for k in range(n + 1):
            m = k + 1
            value -= (
                math.factorial(m)
                * (-1) ** j
                * math.comb(m + j - 1, j)
                / (acb(0, 1) ** m * q ** (m + 1) * c ** (m + j))
            )
        coefficients.append(value)
    return coefficients


def channel_form(Q, frequencies, coefficients, rows, cols, x0, y0, center, n, p, sign):
    """Evaluate one separated channel from signed polynomial moments."""
    alpha = inverse_coefficients(Q, center, n, p)
    left_moments = []
    right_moments = []
    for degree in range(p + 1):
        left_moments.append(sum(
            ball(coefficients[i])
            * (acb(0, 1) * Q * ball(frequencies[i])).exp()
            * ball(frequencies[i] - x0) ** degree
            for i in rows
        ))
        right_moments.append(sum(
            ball(coefficients[j])
            * (acb(0, sign) * Q * ball(frequencies[j])).exp()
            * ball(frequencies[j] - y0) ** degree
            for j in cols
        ))

    total = acb(0)
    for degree in range(p + 1):
        polynomial_moment = acb(0)
        for left_degree in range(degree + 1):
            right_degree = degree - left_degree
            factor = math.comb(degree, left_degree)
            if sign == -1 and right_degree % 2:
                factor = -factor
            polynomial_moment += (
                factor * left_moments[left_degree] * right_moments[right_degree]
            )
        total += alpha[degree] * polynomial_moment
    return total.real


def compressed_form(Q, frequencies, coefficients, rows, cols, n, p):
    """Bilinear form of the rank <= 2(p+1) approximation to K_Q."""
    a0, b0, d0, s0, _ = geometry(frequencies, rows, cols)
    difference = channel_form(
        Q, frequencies, coefficients, rows, cols, a0, b0, d0, n, p, -1
    )
    summation = channel_form(
        Q, frequencies, coefficients, rows, cols, a0, b0, s0, n, p, 1
    )
    return (difference - summation) / 2


def dense_block_form(Q, frequencies, coefficients, rows, cols, diagonal):
    """Direct Arb bilinear form, including internal diagonal-block symmetry."""
    total = arb(0)
    if diagonal:
        for position, i in enumerate(rows):
            total += ball(coefficients[i] ** 2) * direct_d(Q, frequencies[i], frequencies[i]) / 2
            for j in rows[position + 1:]:
                total += ball(coefficients[i] * coefficients[j]) * direct_d(
                    Q, frequencies[i], frequencies[j]
                )
    else:
        for i in rows:
            for j in cols:
                total += ball(coefficients[i] * coefficients[j]) * direct_d(
                    Q, frequencies[i], frequencies[j]
                ) / 2
    return total


def direct_form(Q, frequencies, coefficients):
    return dense_block_form(
        Q, frequencies, coefficients, tuple(range(len(frequencies))), (), True
    )


def channel_weight(u, d, alpha, i, j):
    """Exact coefficient of the shared symmetric kernel entry (i,j)."""
    return u[i] * d[j] + d[i] * u[j] - alpha * d[i] * d[j]


def direct_two_channel_form(Q, frequencies, u, d, alpha):
    total = arb(0)
    for i in range(len(frequencies)):
        total += ball(channel_weight(u, d, alpha, i, i)) * direct_d(
            Q, frequencies[i], frequencies[i]
        ) / 2
        for j in range(i + 1, len(frequencies)):
            total += ball(channel_weight(u, d, alpha, i, j)) * direct_d(
                Q, frequencies[i], frequencies[j]
            )
    return total


def certify_two_channel_tree(
    Q, frequencies, u, d, alpha, leaf_size=4, eta=Fraction(3, 5), n=3, p=5
):
    """Certify 2 u^T K d-alpha d^T K d with shared kernel errors."""
    if Q <= 0 or leaf_size < 1 or not 0 < eta < 1 or n < 0 or p < 0:
        raise ValueError("need Q>0, leaf_size>=1, 0<eta<1, and n,p>=0")
    if len(frequencies) != len(u) or len(u) != len(d) or not frequencies:
        raise ValueError("frequency and channel lengths must agree")
    if list(frequencies) != sorted(frequencies) or len(set(frequencies)) != len(frequencies):
        raise ValueError("frequencies must be strictly increasing")
    if any(not isinstance(x, Fraction) or x <= 0 for x in frequencies):
        raise ValueError("frequencies must be positive Fractions")
    if (any(not isinstance(c, Fraction) for c in tuple(u) + tuple(d))
            or not isinstance(alpha, Fraction)):
        raise ValueError("channels and alpha must be Fractions")

    if all(channel_weight(u, d, alpha, i, j) == 0
           for i in range(len(frequencies)) for j in range(len(frequencies))):
        return arb(0), Stats()

    root = build_cluster(range(len(frequencies)), leaf_size)
    stats = Stats()

    def approximate(rows, cols):
        return two_channel_compressed(rows, cols)

    def two_channel_compressed(rows, cols):
        # The same approximate kernel is used in all channel terms, so their
        # signed centers combine before any absolute value.
        if all(channel_weight(u, d, alpha, i, j) == 0 for i in rows for j in cols):
            return arb(0)
        return (
            compressed_form_bilinear(u, d, rows, cols)
            + compressed_form_bilinear(d, u, rows, cols)
            - ball(alpha) * compressed_form_bilinear(d, d, rows, cols)
        )

    def compressed_form_bilinear(left_coeff, right_coeff, rows, cols):
        a0, b0, d0, s0, _ = geometry(frequencies, rows, cols)
        difference = channel_form_bilinear(
            left_coeff, right_coeff, rows, cols, a0, b0, d0, -1
        )
        summation = channel_form_bilinear(
            left_coeff, right_coeff, rows, cols, a0, b0, s0, 1
        )
        return (difference - summation) / 2

    def channel_form_bilinear(left_coeff, right_coeff, rows, cols, x0, y0, center, sign):
        coeff = inverse_coefficients(Q, center, n, p)
        left_moments = [sum(
            ball(left_coeff[i]) * (acb(0, 1) * Q * ball(frequencies[i])).exp()
            * ball(frequencies[i] - x0) ** degree for i in rows
        ) for degree in range(p + 1)]
        right_moments = [sum(
            ball(right_coeff[j]) * (acb(0, sign) * Q * ball(frequencies[j])).exp()
            * ball(frequencies[j] - y0) ** degree for j in cols
        ) for degree in range(p + 1)]
        total = acb(0)
        for degree in range(p + 1):
            moment = acb(0)
            for ld in range(degree + 1):
                rd = degree - ld
                factor = math.comb(degree, ld) * (-1 if sign == -1 and rd % 2 else 1)
                moment += factor * left_moments[ld] * right_moments[rd]
            total += coeff[degree] * moment
        return total.real

    def dense(rows, cols, diagonal):
        total = arb(0)
        if diagonal:
            for pos, i in enumerate(rows):
                total += ball(channel_weight(u, d, alpha, i, i)) * direct_d(
                    Q, frequencies[i], frequencies[i]
                ) / 2
                for j in rows[pos + 1:]:
                    total += ball(channel_weight(u, d, alpha, i, j)) * direct_d(
                        Q, frequencies[i], frequencies[j]
                    )
        else:
            for i in rows:
                for j in cols:
                    total += ball(channel_weight(u, d, alpha, i, j)) * direct_d(
                        Q, frequencies[i], frequencies[j]
                    ) / 2
        return total

    def visit(left, right, diagonal):
        if not diagonal and admissible(frequencies, left, right, eta):
            rows, cols = right.indices, left.indices
            _, _, d0, s0, H = geometry(frequencies, rows, cols)
            far, amp = theorem_bounds(Q, d0, s0, H, n, p)
            # This exact local shared-error weight can be much smaller than
            # separately bounding the three channel products.
            weight = sum(abs(channel_weight(u, d, alpha, i, j)) for i in rows for j in cols)
            local_radius = (far + amp) * ball(weight) / 2
            rank = 2 * (p + 1)
            stats.compressed_leaves += 1
            stats.compressed_entries += len(rows) * len(cols)
            stats.ordered_entries += 2 * len(rows) * len(cols)
            stats.rank_sum += rank
            stats.max_rank = max(stats.max_rank, rank)
            stats.theorem_radius += 2 * local_radius
            return 2 * (approximate(rows, cols) + arb(0, local_radius))
        if (diagonal and left.left is None) or (
            not diagonal and left.left is None and right.left is None
        ):
            rows, cols = left.indices, right.indices
            stats.dense_leaves += 1
            stored = len(rows) * (len(rows) + 1) // 2 if diagonal else len(rows) * len(cols)
            stats.dense_entries += stored
            stats.ordered_entries += len(rows) ** 2 if diagonal else 2 * len(rows) * len(cols)
            value = dense(rows, cols, diagonal)
            return value if diagonal else 2 * value
        if diagonal:
            return visit(left.left, left.left, True) + visit(left.left, left.right, False) + visit(left.right, left.right, True)
        if right.left is None or (left.left is not None and len(left.indices) >= len(right.indices)):
            return visit(left.left, right, False) + visit(left.right, right, False)
        return visit(left, right.left, False) + visit(left, right.right, False)

    enclosure = visit(root, root, True)
    if stats.ordered_entries != len(frequencies) ** 2:
        raise AssertionError("two-channel partition multiplicity failure")
    return enclosure, stats


def certify_tree(Q, frequencies, coefficients, leaf_size=4, eta=Fraction(3, 5), n=3, p=5):
    if Q <= 0 or leaf_size < 1 or not 0 < eta < 1 or n < 0 or p < 0:
        raise ValueError("need Q>0, leaf_size>=1, 0<eta<1, and n,p>=0")
    if len(frequencies) != len(coefficients) or not frequencies:
        raise ValueError("need equally sized nonempty frequency and coefficient vectors")
    if list(frequencies) != sorted(frequencies) or len(set(frequencies)) != len(frequencies):
        raise ValueError("frequencies must be strictly increasing")
    if any(not isinstance(x, Fraction) or x <= 0 for x in frequencies):
        raise ValueError("frequencies must be positive Fractions")
    if any(not isinstance(c, Fraction) for c in coefficients):
        raise ValueError("coefficients must be Fractions")

    root = build_cluster(range(len(frequencies)), leaf_size)
    stats = Stats()

    def visit(left, right, diagonal):
        if not diagonal and admissible(frequencies, left, right, eta):
            rows, cols = right.indices, left.indices
            _, _, d0, s0, H = geometry(frequencies, rows, cols)
            far, amp = theorem_bounds(Q, d0, s0, H, n, p)
            l1_rows = sum(abs(coefficients[i]) for i in rows)
            l1_cols = sum(abs(coefficients[j]) for j in cols)
            local_radius = (far + amp) * ball(l1_rows * l1_cols) / 2
            rank = 2 * (p + 1)
            stats.compressed_leaves += 1
            stats.compressed_entries += len(rows) * len(cols)
            stats.ordered_entries += 2 * len(rows) * len(cols)
            stats.rank_sum += rank
            stats.max_rank = max(stats.max_rank, rank)
            stats.theorem_radius += 2 * local_radius
            return 2 * (compressed_form(
                Q, frequencies, coefficients, rows, cols, n, p
            ) + arb(0, local_radius))

        if (diagonal and left.left is None) or (
            not diagonal and (left.left is None and right.left is None)
        ):
            rows, cols = left.indices, right.indices
            stats.dense_leaves += 1
            stored = len(rows) * (len(rows) + 1) // 2 if diagonal else len(rows) * len(cols)
            stats.dense_entries += stored
            stats.ordered_entries += len(rows) ** 2 if diagonal else 2 * len(rows) * len(cols)
            value = dense_block_form(Q, frequencies, coefficients, rows, cols, diagonal)
            return value if diagonal else 2 * value

        if diagonal:
            return (
                visit(left.left, left.left, True)
                + visit(left.left, left.right, False)
                + visit(left.right, left.right, True)
            )
        if right.left is None or (left.left is not None and len(left.indices) >= len(right.indices)):
            return visit(left.left, right, False) + visit(left.right, right, False)
        return visit(left, right.left, False) + visit(left, right.right, False)

    enclosure = visit(root, root, True)
    if stats.ordered_entries != len(frequencies) ** 2:
        raise AssertionError("leaf partition does not have exact symmetry multiplicity")
    return enclosure, stats


def finite_realization(size):
    """Return an explicit deterministic rational test realization."""
    pool = sorted({
        Fraction(p, q)
        for q in range(5, 5 + 3 * size)
        for p in range(1, 4 * q + 1)
        if Fraction(1, 4) <= Fraction(p, q) <= 4
    })
    step = max(1, len(pool) // size)
    frequencies = tuple(pool[i * step] for i in range(size))
    coefficients = tuple(
        Fraction((-1) ** i * (1 + i % 5), (i + 2) * (1 + i % 3))
        for i in range(size)
    )
    return frequencies, coefficients


def run_realization(size, Q, leaf_size, eta, n, p):
    frequencies, coefficients = finite_realization(size)
    enclosure, stats = certify_tree(Q, frequencies, coefficients, leaf_size, eta, n, p)
    dense = direct_form(Q, frequencies, coefficients)
    if not enclosure.contains(dense):
        raise AssertionError(
            f"cluster-tree enclosure {enclosure} does not contain dense Arb result {dense}"
        )
    if not stats.compressed_leaves or not stats.dense_leaves:
        raise AssertionError("test realization did not exercise both leaf types")
    print(
        f"finite realization: N={size} rational frequencies, Q={Q}, "
        f"coefficient vector=rational"
    )
    print(
        f"leaves: dense={stats.dense_leaves}, compressed={stats.compressed_leaves}; "
        f"stored entries dense={stats.dense_entries}, compressed={stats.compressed_entries}"
    )
    print(
        f"ranks: max={stats.max_rank}, sum={stats.rank_sum}; "
        f"theorem radius={float(stats.theorem_radius.upper()):.8g}"
    )
    print(
        f"global center={enclosure.mid()}; radius={enclosure.rad()}; "
        f"dense direct={dense}; contained=yes"
    )
    return enclosure, dense, stats


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", type=int, default=192)
    parser.add_argument("--size", type=int, default=48)
    parser.add_argument("--Q", type=int, default=64)
    parser.add_argument("--leaf-size", type=int, default=4)
    parser.add_argument("--eta", type=Fraction, default=Fraction(3, 5))
    parser.add_argument("--n", type=int, default=3)
    parser.add_argument("--p", type=int, default=5)
    args = parser.parse_args()
    if (
        args.bits < 80 or args.size < 4 or args.Q <= 0 or args.leaf_size < 1
        or not 0 < args.eta < 1 or args.n < 0 or args.p < 0
    ):
        parser.error("need bits>=80, size>=4, Q>0, leaf-size>=1, 0<eta<1, n,p>=0")
    ctx.prec = args.bits
    run_realization(args.size, args.Q, args.leaf_size, args.eta, args.n, args.p)
    print("finite certified cluster-tree comparison passed")


if __name__ == "__main__":
    main()
