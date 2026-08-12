# Rank-seven kernels of orders two through four

## Scope

Let `B` be a simple subdivision of a loopless 2-connected multigraph `K` of
minimum degree at least three, cyclomatic rank seven, and order at most four.
Rooted trees may be attached at arbitrary branch or subdivision vertices. This
note proves

`kappa(B) <= |E(B)|+6`

and consequently `s+(G)>=|V(G)|` after all such tree attachments. It makes no
claim about rank-seven kernels of orders five through twelve or about graphs
with more than one positive-rank block.

## Exact census

Write the multiplicities of `K` on the lexicographically ordered vertex pairs.
If `n=|V(K)|`, then `|E(K)|=n+6` and

`sum_v (deg(v)-2)=12`.

For each `n=2,3,4`, enumerate every partition of twelve into `n` positive
parts, add two to obtain the degree sequence, solve the integral incidence
equations on all unordered pairs, retain exactly the rows having no cut vertex,
and canonicalize under every vertex relabelling. This direct finite generation
gives respectively `1,6,47` kernels. It does not use the provisional
rank-six-ear generation of the higher-order frontier.

For a parallel class of multiplicity `m` with `o` odd paths, simplicity gives
the canonical lengths

```text
o=0: (2,...,2),
o>0: (1,3,...,3,2,...,2).
```

Every simple realization of the parity row is obtained, after permuting paths
inside each class, by adding nonnegative even amounts coordinatewise. The exact
finite ledger checks the canonical vector and every vector obtained by adding
two in one physical coordinate.

## Path atom

For fixed unit branch vectors with correlation `r`, a path of length `q` has
least excess

`f_q(r)=q tan^2(acos((-1)^q r)/(2q))`.

For fixed parity, `f_(q+2)(r)<=f_q(r)`. This follows by differentiating
`q tan^2(beta/(2q))`; the sign reduces to
`sin(z)cos(z)-2z<0` for `z>0`. Thus any certificate at a canonical or
one-coordinate target extends, with the same branch Gram, to every
coordinatewise larger same-parity vector.

## Order two: the eight-path atom

The unique kernel consists of eight parallel physical edges. Let
`theta=acos(r)` and put `x=theta/2`. If no path has length one and `e` paths are
even, shortening within parity gives

`Phi(2x)<=2e tan^2(x/2)+3(8-e)tan^2((pi/2-x)/3)`.

At `x=pi/2` this is `2e`, and at `x=0` it is `8-e`. Use the first endpoint for
`e<=3` and the second for `e>=3`; the resulting excess is at most six.

If one path has length one, let `e` be the number of even paths among the other
seven. The corresponding bound is

`cot^2(x)+2e tan^2(x/2)+3(7-e)tan^2((pi/2-x)/3)`.

For `e<=3`, `x=pi/2` gives `2e<=6`. For `e>=4`, use `x=pi/3` and
`3 tan^2(pi/18)<1/3`; the value is less than
`1/3+2e/3+(7-e)/3=(8+e)/3<=5`. These branch choices are retained under every
same-parity coordinate lengthening.

## Order three: the triangle atom

Use the regular triangle Gram, whose off-diagonal correlations are `-1/2`.
Every even canonical path has excess at most `2/3`: a length-two chain with
midpoint Gram

```text
[ 1    1/2 -1/2 ]
[ 1/2  1    1/2 ]
[-1/2  1/2  1   ]
```

is positive semidefinite and has that exact cost. Every odd canonical path has
excess at most `f_1(-1/2)=1/3`, by fixed-parity path monotonicity. There are
nine physical paths, so every parity row has excess at most `9(2/3)=6`.

## Order four: the tetrahedral coloring atom

Color the four branch vertices with four labels and assign equal vectors to
equal labels and regular-tetrahedron vectors, of correlation `-1/3`, to
different labels. A same-color pair is allowed only when its parallel class has
no odd path; all of its even paths then have zero excess.

For a different-color pair the following rational upper atoms suffice:

```text
first odd path:       1/2,
each further odd:    1/6,
each even path:      3/5.
```

The first value is `f_1(-1/3)`. The second follows from
`f_3(-1/3)<=1/6`: if `tan(alpha)=1/(3 sqrt(2))`, then
`cos(6 alpha)=1241/6859<1/3`, so `acos(1/3)/6<alpha`. For an even length-two
path, use a midpoint having correlation `7/13` with both transformed endpoints.
Its three-vector Gram is positive definite because `(7/13)^2<1/3`, and its
two edge costs total `2(1-7/13)/(1+7/13)=3/5`.

The exact verifier tries all `4^4` colorings for each physical parity orbit of
each of the 47 kernels. It checks that a legal coloring exists and that the
least displayed rational sum is at most `28/5<6`. It repeats the ownership
check for the canonical target and all ten one-coordinate-plus-two targets.

## Lift and conclusion

For every selected kernel, the verifier regenerates the full physical parity
set, quotients it by the full multigraph automorphism group, and checks every
canonical-plus-coordinate key. The atoms above give one retained branch Gram
at each key. The path atom then covers arbitrary simultaneous same-parity
lengthening; no parity-changing or spectral subdivision monotonicity is used.

If the core has `L` edges, rank seven gives `|V(B)|=L-6`. If attached rooted
trees contain `t` edges, one-vertex additivity and `kappa(T)=|E(T)|` give
`kappa(G)<=L+6+t`. Hence

`s+(G)>=2(L+t)-kappa(G)>=L-6+t=|V(G)|`.
