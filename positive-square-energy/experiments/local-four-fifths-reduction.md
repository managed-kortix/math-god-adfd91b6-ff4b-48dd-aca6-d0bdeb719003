# Local four-fifths reduction for the weighted-theta witness

This note proves a uniform local-moment bound.  It reduces the `k=6/7`
root-congruence inequality to a purely unrooted bare-surplus theorem.  The
bare-surplus theorem is strongly supported but remains unproved, so this note
is not a proof of the weighted-theta extension.

Let `A` be a simple-theta adjacency matrix, `P=A_+`, and fix a root `v`.  Put

`a=P_vv`, `q=(P^2)_vv`, `d=deg(v)`, `tau=(A^3)_vv`.

The `k=6/7` witness loss is

`L=2q/49+36a/49+169a^2/2401`.                                  (1)

We prove uniformly that `L<4/5`.

## A global quadratic majorant for `x_+`

For every `t>0`, put

`V_t(x)=t/4+x/2+x^2/(4t)`.

For `x<=0`, `V_t(x)-x_+=(x+t)^2/(4t)`; for `x>=0`, it is
`(x-t)^2/(4t)`.  Hence `V_t(x)>=x_+` on the entire real line.  Functional
calculus and `A_vv=0` give

`a <= t/4+d/(4t)`.

Use `t=7/4` at a branch root and `t=3/2` at an internal root.  Thus

`a<=97/112` if `d=3`, and `a<=17/24` if `d=2`.                  (2)

## A cubic majorant for `x_+^2`

On `[-3,3]`,

`U(x)=1/5+x/2+x^2/2+x^3/9 >= x_+^2`.                           (3)

This is checked exactly by splitting at zero.  On `[-3,0]`, `U` is positive;
its critical points are `(-3+-sqrt(6))/2`, where its values reduce to positive
radicals.  On `[0,3]`, the critical points of `U-x^2` are
`(3+-sqrt(3))/2`, and the values are positive.  The accompanying exact script
uses Sturm/root isolation rather than decimals.

Every theta has spectrum in `[-3,3]`, so functional calculus gives

`q <= 1/5+d/2+tau/9`.                                          (4)

Here `tau` is twice the number of triangles through the root.  The exhaustive
simple-theta local states are

`(d,tau)=(3,0),(3,2),(3,4),(2,0),(2,2)`.

Substituting (2)--(4) into (1), which is increasing in `a,q`, gives exact
strict margins below `4/5`.  The worst state is a branch root on two triangles:

`4/5-L >= 31684811/1355316480 > 0`.                            (5)

All five rational checks are reproduced by
`local_four_fifths_certificate.py`.

## Conditional consequence

If a simple theta satisfies

`s^+(Theta)-|Theta| >= 4/5`,                                   (6)

then (5) and the root-congruence witness prove

`s^+(A(Theta)-E_vv/2)>|Theta|`

for every root `v`.

The only observed failures of (6), through exhaustive path length 60 and
targeted long-ear searches through length 1500, are

`Theta(2,2,3)`, `Theta(2,3,3)`, and `Theta(1,4,4)`.

All three are already directly exact-certified for the weighted endpoint.
Thus proving the bare-surplus theorem

`s^+(Theta)-|Theta|>=4/5`

outside exactly those three graphs would complete the one-tree weighted-theta
extension.

Equivalently, because a theta has `m=n+1`, the remaining theorem is

`tr(A|A|)>=-2/5`                                                (7)

outside those three graphs.  This signed-square form cancels the extensive
path bulk and is the preferred target for a Chebyshev/phase proof.

The first observed nonexceptional value is branch-independent and occurs at
`Theta(2,3,6)`, with bare surplus about `0.8175697325`; this leaves a genuine
gap of about `0.01757` above `4/5`.  This observation is not a proof.

## Rejected cubic

The tempting polynomial `1/2+x/2+x^3/9` is **not** a majorant for `x_+`:
at `x=-3` it equals `-4`.  It must not be used.  The sum-of-squares quadratic
`V_t` above is the valid replacement.
