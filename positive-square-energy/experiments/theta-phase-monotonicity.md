# Exact pointwise phase monotonicity in the two short-base channels

This note packages the exact certificate for `c -> c+4` in
`Theta(2,3,c)` and `Theta(1,4,c)`.  It uses the definitions in
`theta-imaginary-phase.md`, without replacing the finite carrier by its
limit.

For a residue `r in {0,1,2,3}`, write `c=4+r+4k` and `q=z^k`.  The path
factor of the long path is then

`f_c=1-(-1)^r z^(4+r)q^4`.

The certificate reconstructs `N,P,Q` from the checked-in formulas and forms

`R=N^2+z(1+z)^2(P^2-zQ^2)`,

`T=2z(1+z)^2PQ`,

so that the phase carrier is `R+i sqrt(z)T`.  Replacing `c` by `c+4`
amounts to replacing `q` by `zq`.  Since `R>0`, the sign of the phase
difference is the sign of

`Delta=R(z,q)T(z,zq)-T(z,q)R(z,zq)`.                         (1)

## Exact factorizations

Every case has the form

`Delta=2q^2(z-1)^3(z+1)^10 C(z,q) B(z,q)`,                   (2)

where `C` is the following displayed product and `B` is a nonnegative
residual polynomial.  For the `(2,3)` family every `C` also contains
`(z^2-z+1)^2`; for `(1,4)` it instead contains `(z^2+1)^2`.

For `(2,3)` the remaining factors `C` are:

`r=0: -z^3(qz-1)(qz+1)(qz^2-1)(qz^2+1)(q^2z^2+1)(q^2z^4+1)`;

`r=1: -z^3(qz^2-1)(qz^2+1)(qz^3-1)(qz^3+1)(q^4z^5+1)(q^4z^9+1)`;

`r=2: z^4(q^2z^3-1)(q^2z^3+1)(q^2z^5-1)(q^2z^5+1)`;

`r=3: z^4(q^2z^5+1)(q^2z^7+1)(q^4z^7+1)(q^4z^11+1)`.

For `(1,4)` they are:

`r=0: z^2(qz-1)(qz+1)(qz^2-1)(qz^2+1)(q^2z^2+1)(q^2z^4+1)`;

`r=1: z^4(q^4z^5+1)(q^4z^9+1)`;

`r=2: -z^3(q^2z^3-1)(q^2z^3+1)(q^2z^5-1)(q^2z^5+1)`;

`r=3: -z^5(q^4z^7+1)(q^4z^11+1)`.

All factors have fixed strict signs on `0<z,q<1`.  The residuals `B` are
stored literally in `theta_phase_monotonicity_certificate.py`; the script
expands (2) and checks exact equality with (1).

## Bernstein positivity

For `B=sum a_(uv)z^u q^v` of bidegree `(d_z,d_q)`, the script independently
computes its tensor-product Bernstein coefficients on `[0,1]^2` by

`b_(ij)=sum_(u<=i,v<=j) a_(uv) C(i,u)/C(d_z,u) C(j,v)/C(d_q,v)`.

It expands the resulting Bernstein representation back to the original
power polynomial.  The exact audited statistics are:

| family | `c mod 4` | phase under `c -> c+4` | bidegree | coefficients | positive | zero | min | max |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| `(2,3)` | 0 | increasing | `(12,4)` | 65 | 65 | 0 | 1 | 8 |
| `(2,3)` | 1 | increasing | `(4,0)` | 5 | 5 | 0 | 1 | 2 |
| `(2,3)` | 2 | decreasing | `(14,4)` | 75 | 72 | 3 | 0 | 2 |
| `(2,3)` | 3 | decreasing | `(4,0)` | 5 | 5 | 0 | 1 | 2 |
| `(1,4)` | 0 | decreasing | `(14,4)` | 75 | 72 | 3 | 0 | 2 |
| `(1,4)` | 1 | decreasing | `(12,4)` | 65 | 65 | 0 | 1 | 8 |
| `(1,4)` | 2 | increasing | `(16,4)` | 85 | 85 | 0 | 1 | 8 |
| `(1,4)` | 3 | increasing | `(14,4)` | 75 | 72 | 3 | 0 | 2 |

Thus each `B` is nonnegative on the closed square and is positive in its
interior.  Combining this with the oriented factors proves the listed strict
phase directions pointwise for every `0<z<1` and every admissible `c`.

Finally, the certificate substitutes `q=z^k` for `k=1,2`, compares all five
interpolated polynomials `N,P,Q,R,T` against a separate direct integer-length
construction, compares (1) against the direct `c,c+4` cross product, and
checks its sign at the rational points `z=1/3,1/2,2/3`.  These checks guard
the interpolation, orientation, and residue bookkeeping independently of the
Bernstein argument.

Run with:

`python3 experiments/theta_phase_monotonicity_certificate.py`

It prints the table above and terminates with
`theta phase monotonicity certificate: PASS`.
