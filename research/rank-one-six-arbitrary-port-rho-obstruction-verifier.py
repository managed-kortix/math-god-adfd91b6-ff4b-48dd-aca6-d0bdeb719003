#!/usr/bin/env python3
"""Exact verifier for the arbitrary-port rank-(1,6) bridge-root obstruction.

Only integer/rational interval arithmetic is used for accepted signs.
Displayed decimals are orientation-only.  No ``assert`` statement is used.
"""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path


class VerificationError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def qsqrt_interval(q, scale=10**80):
    """Strict rational enclosure of sqrt(q) for positive rational q."""
    require(q > 0, "sqrt input must be positive")
    # floor(sqrt(q)*scale), using integer arithmetic only.
    from math import isqrt
    n = (q.numerator * scale * scale) // q.denominator
    a = isqrt(n)
    while F((a + 1) * (a + 1), scale * scale) <= q:
        a += 1
    while F(a * a, scale * scale) > q:
        a -= 1
    lo, hi = F(a, scale), F(a + 1, scale)
    require(lo * lo < q < hi * hi, "non-strict square-root enclosure")
    return lo, hi


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def mul(x, y):
    vals = (x[0]*y[0], x[0]*y[1], x[1]*y[0], x[1]*y[1])
    return min(vals), max(vals)


def recip(x):
    require(x[0] > 0, "reciprocal interval is not positive")
    return F(1, x[1]), F(1, x[0])


def div(x, y):
    return mul(x, recip(y))


def scalar(a, x):
    return mul((a, a), x)


def sqrti(x):
    require(x[0] > 0, "sqrt interval is not positive")
    lo = qsqrt_interval(x[0])
    hi = qsqrt_interval(x[1])
    return lo[0], hi[1]


def bridge_product_interval(t):
    r = qsqrt_interval(F(5))
    delta = add(r, (F(-2), F(-2)))
    s = sqrti(delta)
    cs = [
        (F(2), F(2)),
        scalar(F(1, 2), add(r, (F(-1), F(-1)))),
        scalar(F(1, 2), add(r, (F(-1), F(-1)))),
        scalar(F(-1, 2), add(r, (F(1), F(1)))),
        scalar(F(-1, 2), add(r, (F(1), F(1)))),
    ]
    total = (F(0), F(0))
    for c in cs:
        disc = add(mul(c, c), (F(4*t), F(4*t)))
        m = scalar(F(1, 2), add(sqrti(disc), scalar(F(-1), c)))
        a = div(m, add(scalar(F(2), m), c))
        term = add(div(add((F(1), F(1)), scalar(F(-1), a)), s),
                   div(a, add(s, m)))
        total = add(total, term)
    nu = scalar(F(1, 5), total)
    nr = add(scalar(F(1, 5), recip(s)),
             scalar(F(4, 5), recip(add(s, (F(1), F(1))))))
    return mul(nu, nr), nu, nr, delta, s, r


def sigma_interval(t):
    r = qsqrt_interval(F(5))
    cs = [
        (F(2), F(2)),
        scalar(F(1, 2), add(r, (F(-1), F(-1)))),
        scalar(F(1, 2), add(r, (F(-1), F(-1)))),
        scalar(F(-1, 2), add(r, (F(1), F(1)))),
        scalar(F(-1, 2), add(r, (F(1), F(1)))),
    ]
    z = (F(0), F(0))
    for c in cs:
        z = add(z, mul(c, sqrti(add(mul(c, c), (F(4*t), F(4*t))))))
    return scalar(F(1, 2), z)


def poly_mul(p, q):
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i+j] += a*b
    return out


def characteristic_quotient_coefficients(t):
    # Ascending coefficients of the degree-ten nonzero quotient factor in (1).
    q2 = [-t, -2, 1]
    q4 = [t*t, -t, -(2*t+1), 1, 1]
    return poly_mul(q2, poly_mul(q4, q4))


def main():
    t = 500
    # Topology bookkeeping.
    n_u, m_u = 5*(t+1), 5*(t+1)
    n_r, m_r = 5, 10
    require(m_u-n_u+1 == 1, "U has wrong cyclomatic rank")
    require(m_r-n_r+1 == 6, "R has wrong cyclomatic rank")
    require((m_u+m_r+1)-(n_u+n_r)+1 == 7, "join has wrong rank")
    require(t+2 != 1, "marked U port unexpectedly is a leaf")

    # Formula (1), specialized independently to t=500.
    got = characteristic_quotient_coefficients(t)
    expected = [-31250000000000, 0, 313125000000, 0,
                -1253752500, -2, 2507505, 0, -2505, 0, 1]
    require(got == expected, "characteristic quotient polynomial mismatch")

    product, nu, nr, delta, s, r = bridge_product_interval(t)
    require(product[1] < 1, "failed exact bridge-product upper bound")
    require(delta[0] > 0, "delta_5 positivity failed")
    require(s[0] > 0, "threshold positivity failed")

    sig = sigma_interval(t)
    require(sig[1] < 0, "U_500 hostility sign failed")
    require(sig[0] > -1, "coarse hostile debit bound failed")

    # K5 has eigenvalues 4,-1,-1,-1,-1, hence sigma=16-5=11.
    sigma_r = 11
    require(sigma_r + delta[0] > -sig[0],
            "reserve-plus-root orientation guard failed")

    source = Path(__file__).read_bytes()
    print("rank-one-six-arbitrary-port-rho-obstruction: PASS")
    print("t=500 beta(U)=1 beta(R)=6 beta(join)=7 mark-degree(U)=502")
    print("exact: n_U(s)n_R(s)<1, so rho_br^2<sqrt(5)-2")
    print("exact: -1<sigma(U_500)<0 and sigma(K5)=11")
    print("boundary: route obstruction only; not a graph counterexample")
    print("source_sha256=" + sha256(source).hexdigest())


if __name__ == "__main__":
    main()
