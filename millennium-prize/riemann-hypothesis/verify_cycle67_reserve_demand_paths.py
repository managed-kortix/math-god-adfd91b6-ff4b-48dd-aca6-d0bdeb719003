#!/usr/bin/env python3
"""Verify finite Cycle 67 reserve and demand paths at the eleven hard starts.

The reserve is computed from the complete restricted Gram matrix and the
optimal staircase norm W_M.  The demand is computed separately from the
Cycle 52 quantities V_D, N_U, the complete projection, and W_M.  Only after
both paths are complete is S=A(R-Theta) compared with the stored finite scan.
This is a finite diagnostic and makes no claim about RH.
"""

import argparse
import gzip
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from flint import arb, arb_mat, ctx

from verify_cycle63_complete_tail import CompleteTailVerifier


HARD_WINDOWS = (
    (39, 42),
    (40, 42),
    (95, 103),
    (96, 103),
    (99, 102),
    (100, 102),
    (219, 231),
    (220, 231),
    (221, 231),
    (222, 226),
    (226, 230),
)
CERTIFICATE = Path("cycle42-data/local-arb-certificate.jsonl.gz")
CERTIFICATE_SHA256 = (
    "25ea8a6d71c7202d0a9ddc7e098c90daf61a694b74271eabfbe26434512aee7e"
)


@dataclass(frozen=True)
class DemandComponents:
    V_D: object
    N_U: object
    projection: object
    W_M: object


@dataclass(frozen=True)
class ReserveComponents:
    D_norm: object
    projection: object
    W_M: object


@dataclass(frozen=True)
class ReserveDemandRow:
    M: int
    B: int
    A: object
    reserve: object
    theta: object
    direct_S: object
    factored_S: object
    reserve_components: ReserveComponents
    components: DemandComponents
    reserve_payment: object | None
    demand_increment: object | None
    rank_one_verified: bool
    identity_verified: bool


@dataclass(frozen=True)
class ReserveDemandPath:
    M: int
    first_success: int
    rows: tuple


def _quadratic_solve(matrix, left, right=None):
    if right is None:
        right = left
    left_column = arb_mat([[value] for value in left])
    right_column = arb_mat([[value] for value in right])
    return (left_column.transpose() * matrix.solve(right_column))[0, 0]


def load_surplus_certificate(root=None, verify_digest=True):
    """Load the Cycle 42 half-surplus balls and optionally check their hash."""
    base = Path(__file__).resolve().parent if root is None else Path(root)
    path = base / CERTIFICATE
    digest = hashlib.sha256()
    rows = {}
    with gzip.open(path, "rb") as handle:
        for line in handle:
            digest.update(line)
            record = json.loads(line)
            rows[record["n"]] = arb(record["half_surplus"])
    if verify_digest and digest.hexdigest() != CERTIFICATE_SHA256:
        raise ValueError(f"certificate digest mismatch: {path}")
    return rows


class ReserveDemandVerifier(CompleteTailVerifier):
    """Share complete Vasyunin data across all short endpoint paths."""

    def __init__(self, limit=230, bits=192):
        super().__init__(limit, bits)
        self._complete_cache = {}
        self._W_cache = {}

    def _gram_system(self, basis):
        size = len(basis)
        matrix = arb_mat(size, size)
        for i, left in enumerate(basis):
            for j in range(i, size):
                value = self._complete_inner(left, basis[j])
                matrix[i, j] = matrix[j, i] = value
        return matrix

    def _complete_state(self, M, B):
        key = (M, B)
        if key in self._complete_cache:
            return self._complete_cache[key]
        U = self._coefficients("U", M - 1)
        D = self._coefficients("D", M - 1)
        basis = [U] + [self._coefficients("rho", q) for q in range(M, B)]
        matrix = self._gram_system(basis)
        d_cross = [self._complete_inner(vector, D) for vector in basis]
        if M not in self._W_cache:
            self._W_cache[M] = self._boundary_data(M)[2]
        state = (U, D, basis, matrix, d_cross, self._W_cache[M])
        self._complete_cache[key] = state
        return state

    def _packet_data(self, M, B, basis, matrix, D, W_M):
        A = arb(0)
        N_U = arb(0)
        weighted_T = {}
        weighted_T_norm = arb(0)
        R_coefficients = {}
        T_coefficients = {}

        for n in range(M, B):
            mu_n = self.mu[n]
            if mu_n:
                R_coefficients[n] = arb(mu_n)
                T_coefficients[n] = mu_n * self.logs[n]
            R_n = (0, dict(R_coefficients))
            T_n = (0, dict(T_coefficients))
            beta = ((self.logs[n + 1] - self.logs[n])
                    / (self.logs[n] * self.logs[n + 1] ** 2))
            weight = 1 - self.logs[n] / self.logs[n + 1]
            A += beta
            U_plus_R = (
                1,
                {
                    **basis[0][1],
                    **{
                        q: basis[0][1].get(q, arb(0)) + coefficient
                        for q, coefficient in R_coefficients.items()
                    },
                },
            )
            N_U += weight * self._complete_inner(U_plus_R, U_plus_R)
            weighted_T_norm += beta * self._complete_inner(T_n, T_n)
            for q, coefficient in T_coefficients.items():
                weighted_T[q] = weighted_T.get(q, arb(0)) + beta * coefficient

        bar_T = (0, {q: coefficient / A for q, coefficient in weighted_T.items()})
        V_D = weighted_T_norm - A * self._complete_inner(bar_T, bar_T)
        D_plus_bar_T = (D[0], dict(D[1]))
        for q, coefficient in bar_T[1].items():
            D_plus_bar_T[1][q] = D_plus_bar_T[1].get(q, arb(0)) + coefficient
        projection_cross = [
            self._complete_inner(vector, D_plus_bar_T) for vector in basis
        ]
        projection = _quadratic_solve(matrix, projection_cross)
        theta = (N_U - V_D) / A - projection - W_M
        return A, theta, DemandComponents(V_D, N_U, projection, W_M)

    def compute_path(self, M, stop, surpluses):
        """Compute every prefix [M,B), 1 <= B-M <= stop-M."""
        if not (3 <= M < stop <= self.limit + 1):
            raise ValueError("require 3 <= M < stop <= limit + 1")
        if any(n not in surpluses for n in range(M, stop)):
            raise ValueError("path is outside the surplus certificate")

        rows = []
        direct_S = arb(0)
        previous_reserve = None
        previous_theta = None
        for B in range(M + 1, stop + 1):
            U, D, basis, matrix, d_cross, W_M = self._complete_state(M, B)
            d_norm = self._complete_inner(D, D)
            reserve_projection = _quadratic_solve(matrix, d_cross)
            reserve = d_norm - W_M - reserve_projection
            A, theta, components = self._packet_data(
                M, B, basis, matrix, D, W_M
            )
            direct_S += surpluses[B - 1]
            factored_S = A * (reserve - theta)

            payment = None
            demand_increment = None
            rank_one_verified = True
            if previous_reserve is not None:
                old_basis = basis[:-1]
                old_matrix = self._gram_system(old_basis)
                new_row = basis[-1]
                row_cross = [
                    self._complete_inner(vector, new_row) for vector in old_basis
                ]
                row_norm = self._complete_inner(new_row, new_row)
                schur = row_norm - _quadratic_solve(old_matrix, row_cross)
                d_new = self._complete_inner(D, new_row)
                residual_cross = d_new - _quadratic_solve(
                    old_matrix, row_cross, d_cross[:-1]
                )
                payment = residual_cross * residual_cross / schur
                demand_increment = theta - previous_theta
                rank_one_verified = previous_reserve.overlaps(reserve + payment)

            rows.append(ReserveDemandRow(
                M, B, A, reserve, theta, direct_S, factored_S,
                ReserveComponents(d_norm, reserve_projection, W_M),
                components, payment, demand_increment, rank_one_verified,
                direct_S.overlaps(factored_S),
            ))
            previous_reserve = reserve
            previous_theta = theta
        return ReserveDemandPath(M, stop, tuple(rows))


def reserve_demand_paths(windows=HARD_WINDOWS, bits=192, verify_digest=True):
    """Compute the requested hard-start paths with shared Gram caches."""
    windows = tuple(windows)
    if not windows:
        raise ValueError("need at least one window")
    ctx.prec = bits
    surpluses = load_surplus_certificate(verify_digest=verify_digest)
    verifier = ReserveDemandVerifier(max(stop - 1 for _, stop in windows), bits)
    return tuple(verifier.compute_path(M, stop, surpluses) for M, stop in windows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", type=int, default=192)
    parser.add_argument("--skip-digest-check", action="store_true")
    args = parser.parse_args()
    if args.bits < 80:
        parser.error("--bits must be at least 80")

    paths = reserve_demand_paths(
        bits=args.bits, verify_digest=not args.skip_digest_check
    )
    print("CERTIFIED FINITE DIAGNOSTIC ONLY; NO RH CLAIM")
    print("window       r       reserve R          demand Theta             S")
    for path in paths:
        for row in path.rows:
            if not row.identity_verified or not row.rank_one_verified:
                raise ArithmeticError(f"path verification failed at [{row.M},{row.B})")
            payment = "-" if row.reserve_payment is None else row.reserve_payment.str(10)
            demand = "-" if row.demand_increment is None else row.demand_increment.str(10)
            print(
                f"[{row.M:3d},{row.B:3d}) {row.B-row.M:2d} "
                f"{row.reserve.str(14):>18s} {row.theta.str(14):>18s} "
                f"{row.direct_S.str(12):>16s}  dTheta={demand} pay={payment}"
            )


if __name__ == "__main__":
    main()
