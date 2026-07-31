#!/usr/bin/env python3
"""Exact Appell--Humbert linear algebra for the Cycle 197 divisor gate."""

from fractions import Fraction


N = 6
Q = (Fraction(1), Fraction(1), Fraction(3))


def add(left, right):
    return (left[0] + right[0], left[1] + right[1])


def multiply(left, right):
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def scale(value, vector):
    return (value * vector[0], value * vector[1])


def matrix_multiply(left, right):
    rows = len(left)
    middle = len(right)
    columns = len(right[0])
    result = [[(Fraction(0), Fraction(0)) for _ in range(columns)] for _ in range(rows)]
    for i in range(rows):
        for k in range(middle):
            for j in range(columns):
                result[i][j] = add(result[i][j], multiply(left[i][k], right[k][j]))
    return result


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def rational_rank(rows):
    matrix = [list(row) for row in rows if any(row)]
    if not matrix:
        return 0
    row = 0
    columns = len(matrix[0])
    for column in range(columns):
        pivot = next((i for i in range(row, len(matrix)) if matrix[i][column]), None)
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        value = matrix[row][column]
        matrix[row] = [entry / value for entry in matrix[row]]
        for i in range(len(matrix)):
            if i == row or not matrix[i][column]:
                continue
            value = matrix[i][column]
            matrix[i] = [a - value * b for a, b in zip(matrix[i], matrix[row])]
        row += 1
        if row == len(matrix):
            break
    return row


def hermitian_basis():
    basis = []
    for i in range(N):
        matrix = [[(Fraction(0), Fraction(0)) for _ in range(N)] for _ in range(N)]
        matrix[i][i] = (Fraction(1), Fraction(0))
        basis.append(matrix)
    for i in range(N):
        for j in range(i + 1, N):
            for imaginary in (False, True):
                matrix = [[(Fraction(0), Fraction(0)) for _ in range(N)] for _ in range(N)]
                value = (Fraction(0), Fraction(1)) if imaginary else (Fraction(1), Fraction(0))
                matrix[i][j] = value
                matrix[j][i] = (value[0], -value[1])
                basis.append(matrix)
    assert len(basis) == 36
    return basis


def mu_basis():
    basis = []
    for i in range(3):
        for j in range(3):
            for imaginary in (False, True):
                value = (Fraction(0), Fraction(1)) if imaginary else (Fraction(1), Fraction(0))
                matrix = [[(Fraction(0), Fraction(0)) for _ in range(N)] for _ in range(N)]
                matrix[i][j + 3] = value
                matrix[j + 3][i] = scale(1 / Q[j], value)
                basis.append(matrix)
    assert len(basis) == 18
    return basis


def appell_humbert_equations():
    hermitian = hermitian_basis()
    rows = []
    for mu in mu_basis():
        products = [matrix_multiply(transpose(mu), matrix) for matrix in hermitian]
        for i in range(N):
            for j in range(i + 1, N):
                rows.append([product[i][j][0] - product[j][i][0] for product in products])
                rows.append([product[i][j][1] - product[j][i][1] for product in products])
    return rows


def polarization_coordinates():
    coordinates = [Fraction(0)] * 36
    coordinates[0:6] = [Fraction(1), Fraction(1), Fraction(1), Fraction(1), Fraction(1), Fraction(3)]
    return coordinates


def graph_obstruction_rank(norm):
    rows = []
    for output_i in range(3):
        for output_j in range(3):
            row = [Fraction(0)] * 9
            row[output_j * 3 + output_i] += 1 / Q[output_i]
            row[output_i * 3 + output_j] -= norm
            rows.append(row)
    return rational_rank(rows)


def main():
    equations = appell_humbert_equations()
    rank = rational_rank(equations)
    polarization = polarization_coordinates()
    assert all(sum(a * b for a, b in zip(row, polarization)) == 0 for row in equations)
    assert rank == 35

    obstruction_ranks = [graph_obstruction_rank(Fraction(5**k)) for k in range(7)]
    assert obstruction_ranks == [6, 9, 9, 9, 9, 9, 9]

    print("Cycle 197 Appell--Humbert gate")
    print("real dimension of Herm_6(C) = 36")
    print(f"full-PEL Appell--Humbert equation rank = {rank}")
    print("full-PEL invariant divisor-space dimension = 1")
    print("generator = diag(1,1,1,1,1,3)")
    print(f"graph-triple obstruction ranks for N(a)=5^k = {obstruction_ranks}")
    print("graph-triple common-base dimensions = [3, 0, 0, 0, 0, 0, 0]")
    print("rank-nine signed complete-intersection pair in these classes: NO")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
