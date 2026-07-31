# The six-path rank-five block

## Theorem

Let `B` be the union of six internally vertex-disjoint paths with common
terminals `a,b` and positive integer lengths `l_1,...,l_6`. Suppose that `B`
is simple, equivalently that at most one `l_i` is one. If `G` is obtained from
`B` by attaching arbitrary trees, each at a single vertex, then

`s^+(G)>|V(G)|`.

Thus every simple subdivision of the six-dipole, including every parity and
every permitted direct-terminal-edge case, satisfies the pentacyclic target.

## DNN correlation constant

For a graph `H`, define

`kappa(H)=sup {4(sum_{uv in E(H)} sqrt(M_uv))^2/<J,M> : M psd, M>=0}`.

Its exact correlation dual is

`kappa(H)=min {sum_{uv in E(H)} 2/(1-C_uv) : C psd, C_vv=1}`.       (1)

A summand with `C_uv=1` has value `+infinity`. For completeness, weak duality
follows from weighted Cauchy--Schwarz and

`<J,M>-sum_{uv in E(H)}2(1-C_uv)M_uv`
` =<C,M>+2 sum_{uv notin E(H), u<v}(1-C_uv)M_uv>=0`.

The reverse inequality is the standard conic dual obtained by normalizing
`<J,M>=1`, using

`(sum_e sqrt(x_e))^2=min_{a_e>0, sum a_e=1} sum_e x_e/a_e`,

and `(S_+ intersect N)^*=S_++N`, with boundary points obtained by limits.
The LTZ/DNN estimate and the one-vertex-sum rule are

`s^-(H)<=kappa(H)`,                                                (2)

`kappa(H_1 vee H_2)=kappa(H_1)+kappa(H_2)`.                         (3)

To see (3) directly from (1), restrict a feasible correlation matrix to the
two summands for one inequality. For the other, realize optimal Gram vectors
with the common vertex vector fixed and put the two orthogonal complements in
orthogonal subspaces. In particular, `kappa(T)=|E(T)|` for every tree `T`.

## Exact elimination of all six paths

Fix `C_ab=cos(theta)`, where `0<=theta<=pi`. On a path
`v_0...v_l`, realize `C` by unit vectors `p_j` and set `q_j=(-1)^j p_j`.
If `alpha_j` is the angle between `q_{j-1}` and `q_j`, then

`2/(1-C_{v_{j-1}v_j})=sec^2(alpha_j/2)`.

The angle between the transformed endpoint vectors is

`beta_l=theta` for even `l`, and `beta_l=pi-theta` for odd `l`.      (4)

The spherical triangle inequality gives `sum_j alpha_j>=beta_l`.
Because `sec^2(t/2)` is increasing and strictly convex on `[0,pi)`, Jensen's
inequality gives

`sum_{j=1}^l sec^2(alpha_j/2)>=l sec^2(beta_l/(2l))`.               (5)

Equality is attained by equally spacing the transformed vectors on a shortest
planar arc. These constructions are compatible for all six paths: use the
same terminal vectors `p_a,p_b`, use the appropriate endpoint `(-1)^l p_b`
after alternating signs, and place every internal vector in the same plane.
Their joint Gram matrix is positive semidefinite. Consequently, with
`L=sum_i l_i`, (1) and (5) give the exact formula

`kappa(B)=min_{0<=theta<=pi} [`
` sum_{l_i even} l_i sec^2(theta/(2l_i))`
` +sum_{l_i odd} l_i sec^2((pi-theta)/(2l_i))]`

`          =L+min_{0<=theta<=pi} Phi(theta)`,                      (6)

where

`Phi(theta)=sum_{l_i even} l_i tan^2(theta/(2l_i))`
`           +sum_{l_i odd} l_i tan^2((pi-theta)/(2l_i))`.          (7)

## Six-term tangent lemma

**Lemma.** For positive integers `l_1,...,l_6`, at most one of which is one,

`min_{0<=theta<=pi} Phi(theta)<4`.                                 (8)

**Proof.** Put `x=theta/2`, so `0<=x<=pi/2`, and define

`h_s(y)=s tan^2(y/s)`.

For fixed `0<y<=pi/2` and `s>=2`, `h_s(y)` is strictly decreasing in `s`.
Indeed, with `z=y/s`, one has `0<z<=pi/4` and

`d h_s(y)/ds=tan(z)sec^2(z)(sin(z)cos(z)-2z)<0`,                   (9)

since `0<sin(z)cos(z)<z<2z`. At `y=0` the required non-strict comparison
follows by continuity. Hence an even length can be replaced by two and an odd
length greater than one can be replaced by three to obtain an upper bound.

First suppose no length is one, and let `e` be the number of even lengths.
Then

`Phi(2x)<=F_e(x):=2e tan^2(x/2)`
`                    +3(6-e)tan^2((pi/2-x)/3)`.                   (10)

All seven parity counts are discharged by the following witnesses:

| `e` | test point | value or strict comparison |
|---:|:---:|:---|
| `0` | `x=pi/2` | `F_0=0` |
| `1` | `x=pi/2` | `F_1=2` |
| `2` | just left of `pi/2` | `F_2(pi/2)=4` and `F_2'(pi/2)=8>0` |
| `3` | `x=0` | `F_3=3` |
| `4` | `x=0` | `F_4=2` |
| `5` | `x=0` | `F_5=1` |
| `6` | `x=0` | `F_6=0` |

For `e=2`, direct differentiation gives

`F_2'(pi/2)=4 tan(pi/4)sec^2(pi/4)=8`.

Thus differentiability and the positive left-endpoint derivative imply
`F_2(pi/2-delta)=4-8delta+o(delta)<4` for all sufficiently small positive
`delta`. Every no-unit parity case therefore has a test point at which
`Phi<4`.

Now suppose exactly one length is one. It is odd, and its contribution is

`tan^2((pi-2x)/2)=cot^2 x`.

Let `e` be the number of even lengths among the other five. By (9),

`Phi(2x)<=Q_e(x):=cot^2 x+2e tan^2(x/2)`
`                 +3(5-e)tan^2((pi/2-x)/3)`.                      (11)

At `x=pi/2`, `Q_0=0` and `Q_1=2`. For `2<=e<=4`, test `x=pi/3`. The exact
first two contributions are `1/3` and `2e/3`, while

`3 tan^2(pi/18)<1/3`,                                             (12)

because `tan(pi/18)<tan(pi/12)=2-sqrt(3)<1/3`; the last inequality is
equivalent to `sqrt(3)>5/3`, whose square is `3>25/9`. Therefore

`Q_e(pi/3)<1/3+2e/3+(5-e)/3=(6+e)/3<4` for `2<=e<=4`.             (13)

For `e=5` there is no remaining odd term, and direct evaluation gives

`Q_5(pi/3)=1/3+10/3=11/3<4`.                                     (14)

This exhausts all six unit-case parity counts and proves (8).

## Completion

The six-path core has `L` edges and

`|V(B)|=2+sum_i(l_i-1)=L-4`.                                      (15)

Equations (6) and (8) give

`kappa(B)<L+4`.                                                    (16)

Suppose the attached trees have altogether `t` edges. Iterating (3) gives
`kappa(G)=kappa(B)+t<L+4+t`; each rooted tree also adds exactly its number of
edges to the vertex count. Hence `|E(G)|=L+t` and `|V(G)|=L-4+t`. Since
`s^+(G)+s^-(G)=tr(A(G)^2)=2|E(G)|`, (2) yields

`s^+(G)=2|E(G)|-s^-(G)`
`       >=2(L+t)-kappa(G)`
`       >L-4+t=|V(G)|`.

## Hostile self-check

1. **Rank and threshold.** Six paths have cyclomatic rank
   `L-(L-4)+1=5`; therefore the required DNN excess is four, not five.
2. **Simplicity.** Internal vertex-disjointness prevents every collision except
   parallel direct `a-b` edges. Thus simplicity is exactly the condition that
   at most one length equals one.
3. **Parity convention.** Alternating signs send the far endpoint to `p_b` for
   even length and `-p_b` for odd length, producing respectively `theta` and
   `pi-theta` in (4). Reversing these two would invalidate the unit term.
4. **Attainability.** Pathwise Jensen lower bounds alone would not prove (6).
   The common planar Gram realization above proves simultaneous attainment,
   including mixtures of even and odd paths.
5. **Monotonic replacement.** Formula (9) is used only for even `l>=2` and odd
   `l>=3`; the unique `l=1` term is retained exactly. Equality at `y=0` causes
   no problem because every displayed witness itself gives a strict bound, or
   the `e=2` derivative supplies one.
6. **Case exhaustion.** Without a unit edge, `e=0,...,6`. With one unit edge,
   the unit is odd and the remaining even count is `e=0,...,5`. Both complete
   ranges are explicitly covered.
7. **Derivative direction.** `F_2'(pi/2)=8>0`; moving left, not right, lowers
   `F_2` below four while remaining inside `[0,pi/2]`.
8. **Trees.** The conclusion uses one-vertex sums only. It covers arbitrary
   rooted trees attached at individual vertices, but does not silently claim
   the same formula for an external subgraph meeting the core in two vertices.
9. **Strictness.** The tangent lemma is strict in every permitted length case,
   so `kappa(B)<L+4`; no equality inference from the non-strict LTZ bound is
   needed.

This is the six-path analogue of the five-path theorem: the exact multipath
elimination is unchanged, while the tangent threshold rises from three to four
and the parity ledger expands by one path.
