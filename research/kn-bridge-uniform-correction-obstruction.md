# Exact obstruction to a graph-independent bridge restoration constant

For `n>=2`, let `G_n` be obtained from two disjoint copies of `K_n` by adding
one edge between distinguished vertices, and put

`Delta_n=s^+(G_n)-2s^+(K_n)`.

Then

`0<Delta_n<4/n`,

so `inf_n Delta_n=0`.  In particular, although restoration of a bridge is
strict, there is no graph-independent positive additive correction
`s^+(X+uv+Y)>=s^+(X)+s^+(Y)+c` valid for all connected rooted sides: for
any `c>0`, choose an integer `n>4/c`.

The smallest member is `G_2=P_4`, on four vertices, and `Delta_2=1`.  The
first member whose two sides both have positive cyclomatic rank is `G_3`, two
triangles joined by a bridge; there `Delta_3=2(sqrt(2)-1)`.  No one finite
member disproves every `c>0`; the obstruction is the full unbounded family.

This is an obstruction only to a **uniform constant**.  It does not refute the
root-local leverage correction
`Delta >= (Pi_X)_{uu}(Pi_Y)_{vv}`, and it does not by itself settle the
fixed-rank heptacyclic `1+6` orientation problem: the ranks of the two sides in
this family grow with `n`.

## Characteristic polynomial

Partition each copy of `K_n` into its distinguished vertex and its other
`n-1` vertices.  Symmetric and antisymmetric combinations of the two copies
reduce the nontrivial spectrum to

`[[ 1, sqrt(n-1)], [sqrt(n-1), n-2]]`

and

`[[-1, sqrt(n-1)], [sqrt(n-1), n-2]]`.

All remaining `2n-4` eigenvalues are `-1`.  Hence, exactly,

`chi_Gn(x)=(x+1)^(2n-4)`
`          *(x^2-(n-1)x-1)`
`          *(x^2-(n-3)x-(2n-3))`.

Each quadratic has one positive and one negative root.  The positive roots are

`a_n=(n-1+sqrt((n-1)^2+4))/2`,
`b_n=(n-3+sqrt((n+1)^2-4))/2`.

Since `s^+(K_n)=(n-1)^2`,

`Delta_n=a_n^2+b_n^2-2(n-1)^2`.

Strict positivity has the following self-contained variational certificate.
For every real symmetric `H`,

` s^+(H)=max_{X positive semidefinite}(2 tr(HX)-tr(X^2))`.

For block-diagonal `A direct_sum B`, let `R=A_+ direct_sum B_+`, let
`Pi,Omega` be the positive spectral projectors, and let `C` contain the one
bridge in its two off-diagonal blocks.  Put

`K=(Pi direct_sum Omega) C (Pi direct_sum Omega)`.

The positive-semidefinite trial matrix `R+K_+` improves the displayed
objective over `R` by exactly `tr(K_+^2)`.  For a bridge `uv`, the nonzero
singular value calculation gives

`tr(K_+^2)=(Pi)_{uu}(Omega)_{vv}`.

For `A=B=A(K_n)`, both projectors are `(1/n)J`.  Therefore, exactly,

`Delta_n >= 1/n^2>0`.

## Exact upper bound

For `n>=3`, use

`sqrt((n-1)^2+4)`
` < (n-1)+2/(n-1)-2/(n-1)^3+4/(n-1)^5`,

`sqrt((n+1)^2-4)`
` < (n+1)-2/(n+1)-2/(n+1)^3`.

Both right-hand sides are positive.  Squaring and subtracting the respective
radicands gives, exactly,

`4(5n^4-20n^3+26n^2-12n+5)/(n-1)^10>0`

and

`4(2n^2+4n+3)/(n+1)^6>0`.

(The first numerator is also
`5(n-1)^4-4(n-1)^2+4>0`.)  Thus both radical inequalities are
rigorous.  Substitution in the radical expression for `Delta_n`
gives

`4/n-Delta_n`
` > 2(3n-1)(n^5-2n^4+n^3-2n^2-2)`
`   /(n(n-1)^4(n+1)^3)`.

The numerator is positive for `n>=3`: putting `m=n-3>=0`,

`n^5-2n^4+n^3-2n^2-2`
` =m^5+13m^4+67m^3+169m^2+204m+88`.

For `n=2`, direct substitution gives `Delta_2=1<2=4/n`.  Thus the bound is
exactly certified for every integer `n>=2` and forces `Delta_n -> 0`.

## Reproduction

Run `python3 research/kn-bridge-uniform-correction-obstruction.py`.  The script
uses only integer and `Fraction` arithmetic; dyadic square-root enclosures are
used as an independent check for `2<=n<=100`.
