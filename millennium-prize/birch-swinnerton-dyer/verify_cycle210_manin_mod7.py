#!/usr/bin/env python3
"""Independent mod-7 Manin-symbol certificate for the D=-1499 twist sum."""

from fractions import Fraction


LEVEL = 433
PRIME = 7
TWIST_PRIME = 1499
AUXILIARY = 29


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def projective_index(c, d):
    c %= LEVEL
    d %= LEVEL
    require(c or d, "zero projective pair")
    return c * pow(d, -1, LEVEL) % LEVEL if d else LEVEL


def add_vector(target, source, scalar=1):
    for index, value in source.items():
        target[index] = (target.get(index, 0) + scalar * value) % PRIME
        if not target[index]:
            del target[index]


def cusp_vector(value):
    """Continued-fraction reduction of {infinity,value} to Manin symbols."""
    value = Fraction(value)
    quotients = []
    while value.denominator != 1:
        quotient = value.numerator // value.denominator
        quotients.append(quotient)
        value = 1 / (value - quotient)
    quotients.append(value.numerator)

    p_previous2, q_previous2 = 0, 1
    p_previous1, q_previous1 = 1, 0
    result = {}
    for quotient in quotients:
        p_current = quotient * p_previous1 + p_previous2
        q_current = quotient * q_previous1 + q_previous2
        determinant = p_current * q_previous1 - p_previous1 * q_current
        if determinant == 1:
            index = projective_index(q_current, q_previous1)
            sign = 1
        else:
            require(determinant == -1, "continued-fraction determinant failure")
            index = projective_index(q_previous1, q_current)
            sign = -1
        add_vector(result, {index: sign})
        p_previous2, q_previous2 = p_previous1, q_previous1
        p_previous1, q_previous1 = p_current, q_current
    return result


class RowReduction:
    def __init__(self):
        self.pivots = {}

    def add(self, row):
        row = {index: value % PRIME for index, value in row.items() if value % PRIME}
        while row:
            pivot = min(row)
            coefficient = row[pivot]
            if pivot not in self.pivots:
                inverse = pow(coefficient, -1, PRIME)
                self.pivots[pivot] = {
                    index: value * inverse % PRIME for index, value in row.items()
                }
                return
            add_vector(row, self.pivots[pivot], -coefficient)

    def nullspace(self):
        free = [index for index in range(LEVEL + 1) if index not in self.pivots]
        vectors = []
        for free_index in free:
            vector = [0] * (LEVEL + 1)
            vector[free_index] = 1
            for pivot in sorted(self.pivots, reverse=True):
                vector[pivot] = -sum(
                    value * vector[index]
                    for index, value in self.pivots[pivot].items()
                    if index != pivot
                ) % PRIME
            vectors.append(vector)
        return free, vectors


def manin_eigenspace():
    reduction = RowReduction()
    for index in range(LEVEL + 1):
        c, d = (index, 1) if index < LEVEL else (1, 0)
        reduction.add({index: 1, projective_index(d, -c): 1})
        reduction.add({
            index: 1,
            projective_index(d, -c - d): 1,
            projective_index(-c - d, c): 1,
        })

    # a_2=-1 follows by counting E(F_2) for y^2+xy=x^3+1.
    require(sum(1 for x in range(2) for y in range(2)
                if (y * y + x * y - x ** 3 - 1) % 2 == 0) + 1 == 4,
            "point count at 2 failed")
    # T_2 A(r)=A(r/2)+A((r+1)/2)+A(2r)=-A(r).
    for numerator in range(LEVEL):
        r = Fraction(numerator, LEVEL)
        row = {}
        for cusp in (r / 2, (r + 1) / 2, 2 * r, r):
            add_vector(row, cusp_vector(cusp))
        reduction.add(row)
    return reduction.nullspace()


def legendre(value):
    residue = pow(value, (TWIST_PRIME - 1) // 2, TWIST_PRIME)
    require(residue in (1, TWIST_PRIME - 1), "bad Legendre symbol")
    return 1 if residue == 1 else -1


def discrete_logs():
    result = {}
    value = 1
    for exponent in range(AUXILIARY - 1):
        require(value not in result, "2 is not primitive modulo 29")
        result[value] = exponent
        value = 2 * value % AUXILIARY
    require(value == 1 and len(result) == 28, "incomplete discrete logs")
    return result


def twist_rows(functional):
    rows = []
    for a in range(1, AUXILIARY):
        vector = {}
        for u in range(1, TWIST_PRIME):
            cusp = Fraction(a, AUXILIARY) + Fraction(u, TWIST_PRIME)
            add_vector(vector, cusp_vector(cusp), legendre(u))
        rows.append(sum(value * functional[index]
                        for index, value in vector.items()) % PRIME)
    return rows


def parity_lines(functionals):
    lines = {}
    for left in range(PRIME):
        for right in range(PRIME):
            if not (left or right):
                continue
            first = left or right
            inverse = pow(first, -1, PRIME)
            coefficients = (left * inverse % PRIME, right * inverse % PRIME)
            functional = [
                (coefficients[0] * functionals[0][index]
                 + coefficients[1] * functionals[1][index]) % PRIME
                for index in range(LEVEL + 1)
            ]
            even = True
            odd = True
            for numerator in range(1, 20):
                value = Fraction(numerator, 37)
                positive = sum(coefficient * functional[index]
                               for index, coefficient in cusp_vector(value).items()) % PRIME
                negative = sum(coefficient * functional[index]
                               for index, coefficient in cusp_vector(-value).items()) % PRIME
                even &= negative == positive
                odd &= negative == -positive % PRIME
            if even != odd:
                lines[1 if even else PRIME - 1] = (coefficients, functional)
    require(set(lines) == {1, PRIME - 1}, f"parity decomposition failed: {lines}")
    return lines


def main():
    free, functionals = manin_eigenspace()
    require(free == [425, 426] and len(functionals) == 2,
            f"unexpected eigenspace basis: free={free}")
    logs = discrete_logs()
    lines = parity_lines(functionals)
    candidates = []
    for sign in (1, PRIME - 1):
        coefficients, functional = lines[sign]
        rows = twist_rows(functional)
        delta = sum(logs[a] * rows[a - 1] for a in range(1, AUXILIARY)) % PRIME
        candidates.append((sign, coefficients, rows, delta))

    parities = [sign for sign, _, _, _ in candidates]
    coefficients = [value for _, value, _, _ in candidates]
    deltas = [delta for _, _, _, delta in candidates]
    require(parities == [1, PRIME - 1], f"unexpected parities: {parities}")
    require(deltas == [0, 3], f"unexpected parity-line deltas: {deltas}")
    print("Cycle 210 independent level-433 Manin-symbol certificate")
    print("relations=S,R; exact eigenvalue a_2=-1; eigenspace dimension=2")
    print(f"basis_free_columns={free}; parity_line_coefficients={coefficients}")
    print(f"parities={parities}; parity_line_delta_mod7={deltas}")
    print("odd line raw delta=3; Neron-period normalization unit 6 gives 4=(-150 mod 7)")
    print("INDEPENDENT_NONVANISHING_STATUS=PASS")
    print("INDEPENDENT_NORMALIZED_RESIDUE_STATUS=OPEN")


if __name__ == "__main__":
    main()
