#!/usr/bin/env python3
"""Exact audit of the full characteristic-factor decomposition for C5--Cq."""

import sympy as s


x = s.symbols("x")
PERSISTENT = s.Poly(x**2+x-1, x)


def cycle(n: int) -> tuple[s.Poly, s.Poly]:
    charpoly = s.Poly(2*(s.chebyshevt(n, x/2)-1), x)
    vertex_minor = s.Poly(s.chebyshevu(n-1, x/2), x)
    return charpoly, vertex_minor


def moving(q: int) -> s.Poly:
    d = (q+7)//2
    pattern = [(0, 1), (1, -2), (2, -1), (3, 4), (4, -3),
               (5, 1), (7, 1), (8, -2), (9, 1)]
    return s.Poly(sum(coefficient*s.chebyshevu(d-offset, x/2)
                      for offset, coefficient in pattern if d >= offset), x)


def adjacency_charpoly(q: int) -> s.Poly:
    n = q+5
    matrix = s.zeros(n)
    for offset, length in [(0, 5), (5, q)]:
        for i in range(length):
            j = (i+1) % length
            matrix[offset+i, offset+j] = matrix[offset+j, offset+i] = 1
    matrix[0, 5] = matrix[5, 0] = 1
    return s.Poly(matrix.charpoly(x).as_expr(), x)


def main() -> None:
    p5, m5 = cycle(5)
    assert p5 == s.Poly((x-2)*(x**2+x-1)**2, x)
    assert m5 == s.Poly((x**2-x-1)*(x**2+x-1), x)

    # The stable nine-term formula starts at q=9; q=3,5,7 are already in the
    # separate exact small-case gate.
    for q in range(9, 42, 2):
        pq, mq = cycle(q)
        k = (q-1)//2
        retained = s.Poly(s.chebyshevu(k, x/2)+s.chebyshevu(k-1, x/2), x)
        assert pq == s.Poly((x-2)*retained.as_expr()**2, x)

        bridge = p5*pq-m5*mq
        factorization = PERSISTENT*retained*moving(q)
        assert bridge == factorization
        assert bridge.degree() == q+5
        # Direct determinant check guards the bridge cofactor sign convention.
        assert bridge == adjacency_charpoly(q)

    # The persistent factor has one positive root rho=(-1+sqrt(5))/2 and
    # contributes rho^2=(3-sqrt(5))/2. The retained factor contributes exactly
    # half the Cq positive energy after deleting the Perron root 2.
    rho = (-1+s.sqrt(5))/2
    assert s.expand(rho**2-(3-s.sqrt(5))/2) == 0

    print("PASS full C5--Cq factor audit for odd q=9..41")
    print("chi = (x^2+x-1) R_q S_q, degs 2+(q-1)/2+(q+7)/2=q+5")
    print("PASS p_q=(x-2)R_q^2 and retained positive energy=(s+(Cq)-4)/2")
    print("General identities are Laurent-certified in c5_moment_formulas.py")


if __name__ == "__main__":
    main()
