#!/usr/bin/env python3
"""Exact Laurent certificate for the C5--Cq moving-factor phase equation."""

import sympy as s


z, c, v = s.symbols("z c v")
A = z**8-z**7-2*z**6+2*z**5-z**4+z-1
B = z**8-z**7+z**4-2*z**3+2*z**2+z-1
PATTERN = [(0, 1), (1, -2), (2, -1), (3, 4), (4, -3),
           (5, 1), (7, 1), (8, -2), (9, 1)]


def main() -> None:
    # If d=(q+7)/2 and y=z^d, the nine-term Chebyshev-U expression has
    # numerator y*P-y^-1*Q.  Its zero equation is z^q=B/A.
    P = s.factor(sum(coefficient*z**(1-offset)
                     for offset, coefficient in PATTERN))
    Q = s.factor(sum(coefficient*z**(offset-1)
                     for offset, coefficient in PATTERN))
    assert s.factor(P-(z-1)*A/z**8) == 0
    assert s.factor(Q-(z-1)*B/z) == 0

    # On the unit circle B=-z^8 A(1/z), so B/A has modulus one.
    assert s.factor(B+z**8*A.subs(z, 1/z)) == 0

    # tan(q theta/2)=(B-A)/(i(B+A)).  Reduce the symmetric and
    # antisymmetric Laurent polynomials using c=cos(theta).
    numerator = s.factor((B-A)/z**4)
    numerator_c = 2*(4*c**2-2*c-1)
    assert s.rem(s.together(numerator-numerator_c).as_numer_denom()[0],
                 z**2-2*c*z+1, z) == 0

    # (B+A)/z^4 = 8 i sin(theta)(c-1)(4c^2+2c-1).
    # Squaring avoids adjoining i and sin(theta): D^2 equals the claimed
    # expression after sin^2(theta)=1-c^2.
    denominator = s.factor((B+A)/z**4)
    claimed_den2 = -64*(1-c**2)*(c-1)**2*(4*c**2+2*c-1)**2
    assert s.rem(s.expand((B+A)**2-claimed_den2*z**8),
                 z**2-2*c*z+1, z) == 0

    H2 = s.factor(numerator_c**2/(-claimed_den2))
    expected_H2 = s.factor((4*c**2-2*c-1)**2 /
                           (16*(1-c**2)*(c-1)**2*(4*c**2+2*c-1)**2))
    assert s.factor(H2-expected_H2) == 0

    # Differentiate delta=atan(H) along c=cos(theta), v=sin(theta), then
    # eliminate v^2=1-c^2. This recovers exactly the rational phase derivative
    # used by the independent Sturm and quadrature certificates.
    H = -(4*c**2-2*c-1)/(4*v*(c-1)*(4*c**2+2*c-1))
    Hprime = -v*s.diff(H, c)+c*s.diff(H, v)
    delta_prime = s.together(Hprime/(1+H**2))
    N = -4*(c-1)*(32*c**5-24*c**3+2*c+5)
    D = (256*c**8-256*c**7-576*c**6+576*c**5+384*c**4-
         400*c**3-60*c**2+92*c-17)
    residual = s.together(delta_prime-N/D).as_numer_denom()[0]
    assert s.factor(residual.subs(v**2, 1-c**2)) == 0

    # Fix the continuous atan branch exactly. As theta increases, c decreases:
    # H starts at +infinity, vanishes at cos(pi/5), equals -1/sqrt(3) at
    # pi/3, tends to -infinity at cos(2pi/5), and then returns from +infinity
    # to 1/4. Continuity therefore subtracts pi after that pole.
    sqrt5 = s.sqrt(5)
    c_zero = (1+sqrt5)/4
    c_pole = (-1+sqrt5)/4
    assert 1 > c_zero > s.Rational(1, 2) > c_pole > 0
    assert s.factor((4*c**2-2*c-1).subs(c, c_zero)) == 0
    assert s.factor((4*c**2+2*c-1).subs(c, c_pole)) == 0
    assert s.factor(H.subs({c: s.Rational(1, 2), v: s.sqrt(3)/2})+
                    1/s.sqrt(3)) == 0
    assert H.subs({c: 0, v: 1}) == s.Rational(1, 4)

    # With u=(q theta/2-delta)/pi, delta(0)=pi/2 and
    # delta(pi/2)=-pi+atan(1/4). Since |delta'|<10, u is strictly increasing
    # for q>=727. The positive band roots are exactly the integers 0..l+1 in
    # both odd residue classes q=4l+1 and q=4l+3.
    beta_lower, beta_upper = s.Rational(1, 13), s.Rational(1, 12)
    l = s.symbols("l", integer=True, nonnegative=True)
    # b=l+5/4-beta or l+7/4-beta, respectively.
    assert l+1 < l+s.Rational(5, 4)-beta_upper
    assert l+s.Rational(5, 4)-beta_lower < l+2
    assert l+1 < l+s.Rational(7, 4)-beta_upper
    assert l+s.Rational(7, 4)-beta_lower < l+2

    # Outlier uniqueness: B/A strictly decreases where A>0, while r^q
    # strictly increases. B is positive for r>1 and A has one root there.
    derivative_numerator = s.factor(s.together(s.diff(B/A, z))).as_numer_denom()[0]
    expected_derivative = -4*z*(z-1)**2*(z**10+2*z**8+2*z**6+5*z**5+
                                          2*z**4+2*z**2+1)
    assert derivative_numerator == expected_derivative
    shifted_B = s.Poly(s.expand(B.subs(z, z+1)), z)
    assert all(coefficient > 0 for coefficient in shifted_B.all_coeffs())
    roots_A = [(interval, multiplicity) for interval, multiplicity
               in s.Poly(A, z).intervals() if interval[1] > 1]
    assert len(roots_A) == 1 and roots_A[0][1] == 1
    assert A.subs(z, s.Rational(5, 3)) < 0

    print("PASS exact Laurent equation z^q=B(z)/A(z)")
    print("PASS tan(q theta/2)=H(theta), with")
    print("H=-(4c^2-2c-1)/(4 sin(theta)(c-1)(4c^2+2c-1))")
    print("PASS exact rational delta'(theta)=N(c)/D(c)")
    print("PASS continuous branch endpoints and positive-band integer count")
    print("PASS unique positive outlier parameter r>alpha>5/3")


if __name__ == "__main__":
    main()
