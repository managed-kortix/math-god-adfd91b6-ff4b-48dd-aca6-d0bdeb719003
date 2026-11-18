# A rank-(1,6) bridge-gain obstruction

Date: 2026-11-18. Status: **NONPROMOTIONAL COUNTERFAMILY**.

## Claim boundary

This note gives a connected finite simple rank-(1,6) family whose one-edge
positive-square-energy gain is strictly less than `2/3`. It therefore rules out
`2/3` as a universal lower bound for such bridge gains.

It does **not** prove a lower bound for arbitrary rank-(1,6) bridges, classify
any packet-specific residual frontier, or close any bridge-dispatch lane. In
particular, although the limiting gain below is larger than

`delta_5=sqrt(5)-2`,

that limiting comparison says nothing by itself about the finite members of
the family and must not be used to pay a pentagon deficit. The exact finite
certificate recorded here is an upper bound, not a lower bound.

Throughout,

`s+(X)=sum_{lambda_i(A_X)>0} lambda_i(A_X)^2`.

Zeros are excluded; there is no replacement of the positive projector `P_+`
by the nonnegative projector `P_{>=0}`.

## The family

For an integer `t>=1`, let `H_t` be a `C_5` with `t` new leaves adjacent to one
cycle vertex `a`. Mark one of those leaves `u`. Let `K=K_5`, mark any vertex
`v`, and let `G_t` be obtained from the disjoint union of `H_t` and `K` by the
single new edge `uv`.

Then

* `H_t` and `K` are connected, induced in `G_t`, and joined by exactly one
  bridge;
* `beta(H_t)=|E(H_t)|-|V(H_t)|+1=1`;
* `beta(K)=10-5+1=6`; and
* `s+(K)=4^2=16`.

Define the bridge gain

`Gamma_t=s+(G_t)-s+(H_t)-s+(K)`.

The exact conclusions are

`Gamma_10<2/3`,                                                     (1)

and

`lim_{t->infinity} Gamma_t=3-alpha^2<2/3`,                         (2)

where `alpha` is the unique negative root of

`f(x)=x^3-3x^2-5x+3`.

Thus even one finite member refutes the proposed universal `2/3` bound; the
limit identifies the persistent obstruction and is not needed for that
refutation.

## Exact characteristic polynomials

Put

`q(x)=x^2+x-1`,

`p_t(x)=x^4-x^3-(t+3)x^2+(t+2)x+t`,                               (3)

and

`g_t(x)=x^7-4x^6-(t+5)x^5+(4t+19)x^4+(3t+5)x^3`
`       -(11t+15)x^2+(4-2t)x+3t-3`.                              (4)

The characteristic polynomials are

`chi_{H_t}(x)=x^(t-1) q(x) p_t(x)`,                               (5)

and, for `t>=2`,

`chi_{G_t}(x)=x^(t-2)(x+1)^3 q(x) g_t(x)`.                        (6)

For `t=1`, `g_1(x)` has a factor `x`, which cancels the formal `x^(-1)`:

`chi_{G_1}(x)=(x+1)^3 q(x) g_1(x)/x`.                             (7)

These formulas can be derived without a numerical determinant. For `H_t`, use
the equitable cells

`{a}, {the two neighbours of a on C_5}, {the two remaining cycle vertices},`
`{the t leaves}`.

The corresponding divisor matrix is

```
[0 2 0 t]
[1 0 1 0]
[0 1 1 0]
[1 0 0 0],
```

and `det(xI-Q_H)=p_t(x)`. The antisymmetric cycle subspace contributes `q`,
and leaf differences contribute `x^(t-1)`.

For `G_t`, split the marked leaf from the other `t-1` leaves, and split the
marked vertex of `K_5` from its other four vertices. In the cell order

`{a}, {near cycle pair}, {far cycle pair}, {u},`
`{other leaves}, {v}, {other K_5 vertices}`,

an equitable divisor is

```
[0 2 0 1 t-1 0 0]
[1 0 1 0   0 0 0]
[0 1 1 0   0 0 0]
[1 0 0 0   0 1 0]
[1 0 0 0   0 0 0]
[0 0 0 1   0 0 4]
[0 0 0 0   0 1 3].
```

Direct exact expansion gives `det(xI-Q_G)=g_t(x)`. The same antisymmetric
cycle subspace contributes `q`, the three-dimensional sum-zero subspace of the
unmarked `K_5` vertices contributes `(x+1)^3`, and the unmarked-leaf difference
subspace contributes `x^(t-2)` when `t>=2`. This proves (5)--(7). The companion
verifier also constructs the full adjacency matrices for `t=1,2,3,4` and
checks the factorizations directly.

## Exact finite obstruction

At `t=10`, Sturm isolation gives the two positive roots of `p_10` in

`(15215/10000,15216/10000)` and
`(35011/10000,35012/10000)`,

and the four positive roots of `g_10` in

`(4476/10000,4477/10000)`,
`(15233/10000,15234/10000)`,
`(34930/10000,34931/10000)`, and
`(40636/10000,40637/10000)`.

All endpoints are positive. The fixed factor `q` occurs on both sides of the
gain and cancels, while `(x+1)^3` and all powers of `x` contribute no positive
roots. Therefore, if `rho_1,rho_2` are the positive roots of `p_10` and
`eta_1,...,eta_4` are the positive roots of `g_10`, then

`Gamma_10=sum eta_i^2-sum rho_j^2-16`.

Using upper endpoints for the `eta_i` and lower endpoints for the `rho_j`
gives the exact rational upper bound

`Gamma_10 < 66392469/100000000 < 2/3`.                            (8)

The last comparison has positive gap

`2/3-66392469/100000000=822593/300000000`.

This proves (1) with rational arithmetic only.

## Audit of the limiting roots

Write

`r(x)=x^2-x-1`.

For fixed `x`, division of (3)--(4) by `t` gives coefficientwise convergence

`p_t(x)/t -> -r(x)`,                                             (9)

`g_t(x)/t -> -r(x)f(x)`.                                        (10)

The two roots of `r` and the three roots of `f` are real and simple:
`disc(r)=5`, `disc(f)=1616`, and `Res(r,f)=-41`. Choose pairwise disjoint
closed complex disks around these roots, with no zero of the relevant limit
polynomial on any boundary. Coefficientwise convergence is uniform on those
boundaries. Rouché's theorem therefore gives exactly one root, counted with
multiplicity, of the relevant normalized polynomial in each disk for all
sufficiently large `t`.

No other root can remain bounded. Otherwise a bounded sequence of remaining
roots would have a convergent subsequence; uniform convergence on compact sets
would make its limit a root of `r` or `r f`, hence put the sequence eventually
inside one of the disks that already contains exactly one root. Therefore
exactly two roots of `p_t` and exactly two roots of `g_t` escape every bounded
set. The divisor matrices are similar to symmetric quotient matrices (and the
polynomials are factors of real symmetric adjacency characteristic
polynomials), so all their roots are real. Finally, the sum of all roots and
the sum of the bounded limiting roots are both `1` for `p_t` and both `4` for
`g_t`; the two escaping roots consequently have sum tending to zero. They
cannot escape with the same sign. Thus the bounded roots converge, with
multiplicity, exactly as follows:

* the two bounded roots of `p_t` converge to the roots of `r`;
* five bounded roots of `g_t` converge to the roots of `r f`; and
* each polynomial has one positive and one negative escaping root.

For completeness, the escaping-root scale is also exact. Put `e=t^(-1/2)` and
`x=z/e`. After multiplying by the leading power of `e`, equations (3)--(4)
become

`P(e,z)=z^4-z^2+e(-z^3+z)+e^2(1-3z^2)+2e^3z`,                   (11)

and

`R(e,z)=z^7-z^5+e(-4z^6+4z^4)+e^2(-5z^5+3z^3)`
`       +e^3(19z^4-11z^2)+e^4(5z^3-2z)`
`       +e^5(3-15z^2)+4e^6z-3e^7`.                             (12)

At `(e,z)=(0,1)` both equations have a simple zero in `z` because the
`z`-derivative is `2`. The implicit-function theorem gives positive escaping
roots `lambda_p(t)=z_p(e)/e` and `lambda_g(t)=z_g(e)/e`. Substitution of
`z=1+a e+b e^2+O(e^3)` into either equation gives `a=0`, `b=1`. Hence

`z_p(e)=1+e^2+O(e^3)`, `z_g(e)=1+e^2+O(e^3)`,

so

`lambda_g(t)^2-lambda_p(t)^2 -> 0`.                              (13)

This audits the step that is lost if one merely divides by `t`: the positive
escaping roots do not leave a hidden constant in the gain.

Let the three roots of `f` be `alpha<0<gamma<delta`. From (9)--(13), the common
positive root of `r` cancels and

`lim Gamma_t=gamma^2+delta^2-16`.                                (14)

Vieta gives

`alpha+gamma+delta=3`, `alpha gamma+alpha delta+gamma delta=-5`,

and therefore

`alpha^2+gamma^2+delta^2=3^2-2(-5)=19`.

Equation (14) is exactly `3-alpha^2`.

There is exactly one negative root of `f`: its coefficient signs after
`x -> -x` have one sign change, while `f(-2)=-7<0<f(-3/2)=3/8`.
For `s=sqrt(7/3)`,

`f(-s)=-4+8sqrt(21)/9>0`,

since both terms are positive and `(8sqrt(21))^2=1344>1296=36^2`.
The unique negative crossing is therefore to the left of `-s`, so
`alpha^2>7/3`, and

`3-alpha^2<2/3`.

This proves (2).

One may also check exactly that this limiting number exceeds `delta_5`, but
that fact is deliberately not promoted: it is only a limit and supplies no
finite-`t` lower bound. The verifier checks the comparison solely as a
claim-boundary guard.

## Reproduction

Run:

```text
uv run --with sympy python research/rank-one-six-bridge-gain-obstruction-verifier.py
```

The script uses symbolic integer/rational arithmetic for polynomial identities,
Sturm root counts, and inequalities. Any displayed decimal is explicitly
labelled orientation-only and is not used in an accepted comparison.
