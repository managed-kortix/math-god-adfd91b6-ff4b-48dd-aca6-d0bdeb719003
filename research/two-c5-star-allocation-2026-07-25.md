# Two C5 blocks with pendant stars: what the quotient proves

## Scope

Let `H` be a fixed graph with vertices `1,...,h`.  At vertex `i`, attach
`t_i` new pendant leaves, where `t_i` is a nonnegative integer.  Write
`G(H,t)` for the resulting graph, `T=sum_i t_i`, and

`F_H(t)=s^+(G(H,t))-|V(G(H,t))|`.

The intended core is a handcuff made from two `C5` blocks, including a shared
vertex or a connector path.  This note records the exact finite-dimensional
reduction, tests the proposed allocation/relocation principle, and separates
what is proved from what remains conjectural.

## Exact quotient theorem

**Theorem 1 (star compression).**  Let `R={i:t_i>0}` and let `D_t` be the
`h` by `|R|` matrix whose column indexed by `i in R` is `sqrt(t_i)e_i`.  Set

`B_H(t) = [[A(H),D_t],[D_t^T,0]]`.

Then

`spec A(G(H,t)) = spec B_H(t) union {0^(T-|R|)}`,

and consequently

`F_H(t)=s^+(B_H(t))-h-T`.                                      (1)

*Proof.*  For each occupied root `i`, decompose the coordinates on its
`t_i` leaves into the normalized all-ones vector and its orthogonal
complement.  The latter has dimension `t_i-1` and is killed by the adjacency
matrix.  On the former, the edge from the root has matrix entry `sqrt(t_i)`.
The resulting orthogonal decomposition gives the displayed spectrum and (1).

Thus arbitrary star allocation is an exact integer optimization with square-
root edge weights.  It is not, however, an ordinary equitable quotient when
several zero cells are retained; the symmetric divisor above is the useful
form.

## Variational structure, and why convexity does not solve allocation

For every real symmetric matrix `M`,

`s^+(M)=max_{X>=0} {2 tr(XM)-tr(X^2)}`.                        (2)

Indeed, diagonalize `M` and use von Neumann's trace inequality to take an
optimizer diagonal in the same eigenbasis.  Each scalar problem is
`max_{x>=0}(2 lambda x-x^2)=lambda_+^2`, attained at `x=lambda_+`.
For `B=B_H(t)`, block multiplication also gives

`B^2 = [[A^2+diag(t), A D_t],[D_t^T A, D_t^T D_t]]`.           (3)

The quotient itself is affine in the variables `sqrt(t_i)`, not in `t_i`, and
the optimizing positive part in (2) changes with `t`.  Formula (3) likewise
has diagonal terms affine in `t` but off-diagonal terms containing
`sqrt(t_i)`.  Hence these formulas supply neither convexity nor concavity of
`F_H` on an allocation simplex.  In particular, no Jensen or majorization
argument follows merely from the quotient.

## Exact counterexample to concentration at the connector middle

The strongest natural interpretation of "move all pendant edges toward the
connector middle" is false even within the two-C5 star class.

Let `H=C5-P5-C5`, meaning that the distinguished cycle vertices are joined by
a path of four edges.  Its three internal connector vertices are `a,b,c`, in
that order.  Attach two leaves.

- `G_split`: one leaf at `a` and one leaf at `c`;
- `G_mid`: two leaves at the middle vertex `b`.

Both graphs have 15 vertices.  Exact quotient determinants factor as

`chi_split(x)=x(x^2-x-3)(x^2+x-1)^2`
`             *(x^3-4x+2)(x^5-x^4-5x^3+4x^2+4x-2)`,

whereas

`chi_mid(x)=(x-1)(x^2+x-1)^2(x^3-4x-1)`
`           *(x^6-x^5-8x^4+7x^3+15x^2-10x-2)`.

Rational Sturm isolation of their positive roots, followed by squaring the
positive isolating intervals, gives

`0.578583996213 < F_H(split) < 0.578583996221`,

`0.684416018213 < F_H(mid)   < 0.684416018223`.

Therefore relocating both pendant edges from the two connector shoulders to
the connector middle **increases** `s^+-n` by more than `0.1058`.  The proposed
global branch relocation is not a valid monotone transformation.

This also shows that the finite-budget minimizer need not be a single star:
for this fixed core and total budget two, the symmetric two-root allocation is
strictly better than the middle star.  More generally, direct integer
enumeration on `C5-P_L-C5` for small budgets repeatedly selects a split between
the two connector shoulders once `L>=3`.

There is an even simpler warning against monotonicity in star size.  On the
path-two core `C5-P3-C5`, adding one leaf at a cycle vertex raises the surplus
from approximately `0.6522494768` to `0.7154186062`; adding leaves does not
uniformly decrease `s^+-n`.

## The rigorously identified sharp limiting family

Take `H=C5-P3-C5`, with one internal connector vertex `u`, and attach `t`
leaves at `u`.  Call the graph `G_t`; it has `t+11` vertices.  The quotient
characteristic polynomial is

`chi_t(x)=(x-2)(x^2+x-1)^3 Q_t(x)`,

`Q_t(x)=x^5-x^4-(t+5)x^3+(t+4)x^2+(3t+2)x-2t`.                (4)

**Theorem 2 (exact limiting upper bound on the global infimum).**

`lim_{t->infinity} (s^+(G_t)-|V(G_t)|)=5-2sqrt(5)`.            (5)

*Proof.*  Divide `Q_t` by `t`.  On compact sets it converges coefficientwise
to

`-x^3+x^2+3x-2=-(x-2)(x^2+x-1)`.

Three roots therefore converge, with multiplicity, to `2`,
`rho=(-1+sqrt(5))/2`, and the negative root of `x^2+x-1`.  The two remaining
roots are `+sqrt(t)+O(1)` and `-sqrt(t)+O(1)`.  Substitution in (4), first with
`x=sqrt(t)+a+O(t^-1/2)` and then to the next order, gives `a=0` and positive
root squared `t+2+o(1)`.  (The negative root has a different next-order term,
so the constant cannot be obtained by using only the sum of their squares.)
The fixed factors in (4) contribute positive
squares

`4 + 3 rho^2`,

and the bounded positive roots of `Q_t` contribute `4+rho^2+o(1)`.  Hence

`s^+(G_t)=t+10+4rho^2+o(1)`.

Since `rho^2=(3-sqrt(5))/2` and `|V(G_t)|=t+11`, subtraction yields
`5-2sqrt(5)+o(1)`.

Thus any universal lower bound over the two-C5 star class is at most
`5-2sqrt(5)`, and equality cannot be improved if the lower bound is true.

## What is not proved

The requested global statement

`F_H(t) >= 5-2sqrt(5)`                                        (6)

for every two-C5 connector core `H`, every connector length, and every integer
star allocation `t`, does **not** follow from quotient/interlacing or convexity.
The counterexample above disproves the concentration step that was meant to
reduce (6) to the one-middle-star family.  No counterexample to (6) was found,
but the present argument is not a proof of (6).

The numerically observed asymptotic picture is subtler than a unique middle
star.  For every connector length at least two, putting a very large total
number of leaves equally on the two connector shoulders approaches the same
constant in (5); for connector length two the shoulders coincide and this is
exactly the middle-star family.  Thus even asymptotic equality is not unique at
the level of connector length.

## Consequence for arbitrary attached trees

Classical grafting transformations for the adjacency spectral radius optimize
only the largest eigenvalue and use a positive Perron vector.  Positive square
energy is the sum of squares of *all* positive eigenvalues.  Its directional
derivative (away from zero eigenvalues) is

`d s^+(A)[E] = 2 tr(A_+ E)`,

and `A_+` need not have entrywise positive off-diagonal entries.  Perron-vector
edge-moving arguments therefore do not transfer.  The explicit star
relocation counterexample already rules out the required monotonicity in the
narrowest proposed class, so it cannot justify reducing arbitrary rooted trees
to connector stars.

## Bottom line

1. Arbitrary pendant stars reduce exactly to the finite matrix (1).
2. Allocation convexity/concentration is unavailable and the proposed
   connector-middle relocation is false.
3. The family `C5-P3-C5` with a growing middle star rigorously establishes the
   sharp candidate constant `5-2sqrt(5)` as an upper bound on the infimum.
4. The matching universal lower bound for all star allocations remains open;
   consequently no reduction from arbitrary attached trees is proved.
