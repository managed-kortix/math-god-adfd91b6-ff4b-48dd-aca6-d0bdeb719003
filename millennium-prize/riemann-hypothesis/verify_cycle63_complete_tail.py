#!/usr/bin/env python3
"""Certify Cycle 63 complete-tail and boundary Schur values.

The complete restricted fractional-part Gram entries come from the finite
Vasyunin formula in ``certify_complete_gram``.  Integrals over ``(1, M)`` are
then subtracted cell by cell, with exact integer/rational coefficients and Arb
logarithms.  The result is a finite computation for fixed windows, not an
asymptotic theorem and not a claim about the Riemann hypothesis.
"""

import argparse
from dataclasses import dataclass

from flint import arb, arb_mat, ctx

from certify_complete_gram import RestrictedGram, mobius_sieve


WINDOWS = ((98, 99), (219, 231), (220, 231), (222, 226))


@dataclass(frozen=True)
class CompleteTailResult:
    M: int
    B: int
    omega_infinity: object
    boundary_schur: object
    full_R: object
    direct_full_R: object
    identity_residual: object


class CompleteTailVerifier:
    """Reusable complete restricted Gram data for several fixed windows."""

    def __init__(self, limit=231, bits=256):
        if limit < 2:
            raise ValueError("limit must be at least 2")
        if bits < 80:
            raise ValueError("bits must be at least 80")
        ctx.prec = bits
        self.limit = limit
        self.bits = bits
        self.mu = mobius_sieve(limit)
        self.logs = [arb(0)] + [arb(n).log() for n in range(1, limit + 2)]
        self.gram = RestrictedGram()

    def _coefficients(self, kind, index=None):
        if kind == "rho":
            return 0, {index: arb(1)}
        stop = index
        if kind == "U":
            return 1, {a: arb(self.mu[a]) for a in range(1, stop + 1)
                       if self.mu[a]}
        if kind == "D":
            return 0, {a: self.mu[a] * self.logs[a]
                       for a in range(1, stop + 1) if self.mu[a]}
        raise ValueError(f"unknown vector kind: {kind}")

    def _complete_inner(self, left, right):
        left_chi, left_rho = left
        right_chi, right_rho = right
        value = arb(left_chi * right_chi)
        if left_chi:
            value += left_chi * sum(
                (coefficient * self.gram.chi_cross(a)
                 for a, coefficient in right_rho.items()), arb(0)
            )
        if right_chi:
            value += right_chi * sum(
                (coefficient * self.gram.chi_cross(a)
                 for a, coefficient in left_rho.items()), arb(0)
            )
        for a, coefficient_a in left_rho.items():
            value += coefficient_a * sum(
                (coefficient_b * self.gram.entry(a, b)
                 for b, coefficient_b in right_rho.items()), arb(0)
            )
        return value

    def _cell_affine(self, vector, k):
        chi, coefficients = vector
        slope = sum((coefficient / a for a, coefficient in coefficients.items()),
                    arb(0))
        intercept = arb(chi) - sum(
            (coefficient * (k // a) for a, coefficient in coefficients.items()),
            arb(0),
        )
        return slope, intercept

    def _prefix_inner(self, left, right, M):
        value = arb(0)
        for k in range(1, M):
            a, b = self._cell_affine(left, k)
            c, d = self._cell_affine(right, k)
            lam = self.logs[k + 1] - self.logs[k]
            tau = arb(1) / (k * (k + 1))
            value += a * c + (a * d + b * c) * lam + b * d * tau
        return value

    def _tail_inner(self, left, right, M):
        return self._complete_inner(left, right) - self._prefix_inner(left, right, M)

    @staticmethod
    def _quadratic_solve(matrix, left, right=None):
        if right is None:
            right = left
        left_column = arb_mat([[value] for value in left])
        right_column = arb_mat([[value] for value in right])
        return (left_column.transpose() * matrix.solve(right_column))[0, 0]

    def _boundary_data(self, M):
        ell = sum((self.mu[a] * self.logs[a] / a for a in range(1, M)), arb(0))
        psi = arb(0)
        weighted_psi = arb(0)
        W = arb(0)
        for k in range(1, M):
            psi -= sum((self.mu[a] * self.logs[a]
                        for a in range(1, k + 1) if k % a == 0), arb(0))
            lam = self.logs[k + 1] - self.logs[k]
            tau = arb(1) / (k * (k + 1))
            weighted_psi += psi * lam
            W += psi * psi * tau
        c_M = weighted_psi / (M - 1)
        W -= weighted_psi * weighted_psi / (M - 1)
        return ell, c_M, W

    def compute(self, M, B):
        """Return complete-tail, boundary, and exact full residual values."""
        if not (2 <= M < B <= self.limit + 1):
            raise ValueError("require 2 <= M < B <= limit + 1")
        U = self._coefficients("U", M - 1)
        D = self._coefficients("D", M - 1)
        basis = [U] + [self._coefficients("rho", q) for q in range(M, B)]
        size = len(basis)

        A = arb_mat(size, size)
        complete_A = arb_mat(size, size)
        for i, left in enumerate(basis):
            for j in range(i, size):
                complete = self._complete_inner(left, basis[j])
                tail = complete - self._prefix_inner(left, basis[j], M)
                complete_A[i, j] = complete_A[j, i] = complete
                A[i, j] = A[j, i] = tail

        b = [self._tail_inner(vector, D, M) for vector in basis]
        d = self._tail_inner(D, D, M)
        omega = d - self._quadratic_solve(A, b)

        ell, c_M, W = self._boundary_data(M)
        boundary_row = [
            sum((arb(self.mu[a]) / a for a in range(1, M)), arb(0))
        ] + [arb(1) / q for q in range(M, B)]
        u_norm = self._quadratic_solve(A, boundary_row)
        sigma_u = self._quadratic_solve(A, boundary_row, b)
        defect = ell + c_M - sigma_u
        boundary = defect * defect / (arb(1) / (M - 1) + u_norm)
        full_R = omega + boundary

        complete_b = [self._complete_inner(vector, D) for vector in basis]
        complete_d = self._complete_inner(D, D)
        direct = complete_d - W - self._quadratic_solve(complete_A, complete_b)
        return CompleteTailResult(
            M, B, omega, boundary, full_R, direct, full_R - direct
        )


def complete_tail_values(windows=WINDOWS, bits=256):
    """Compute all requested windows while sharing the Vasyunin cache."""
    windows = tuple(windows)
    verifier = CompleteTailVerifier(max(B - 1 for _, B in windows), bits)
    return tuple(verifier.compute(M, B) for M, B in windows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", type=int, default=256)
    args = parser.parse_args()
    print("CERTIFIED FINITE DIAGNOSTIC ONLY; NO RH CLAIM")
    print(" window          Omega_infinity        boundary_Schur                full_R")
    for row in complete_tail_values(bits=args.bits):
        if not row.identity_residual.contains(0):
            raise ArithmeticError(
                f"full R identity failed for [{row.M},{row.B}): "
                f"{row.identity_residual}"
            )
        print(
            f"[{row.M:3d},{row.B:3d}) {row.omega_infinity.str(20):>24s} "
            f"{row.boundary_schur.str(20):>24s} {row.full_R.str(20):>24s}"
        )


if __name__ == "__main__":
    main()
