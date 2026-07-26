# Rooted hostile-cycle guard absorption at every rank

## 1. Result

For a graph `G`, write

`s+(G)=sum_{lambda>0} lambda^2`, `s-(G)=sum_{lambda<0} lambda^2`,

and

`sigma(G)=s+(G)-|V(G)|`.

Let `A` be a connected cactus whose cyclic blocks are `h>=1` triangles.
Distinguish an arbitrary vertex `r` of `A`. Let `Q=C_q`, where
`q=4k+1>=5`, and form `G` in either of the following ways:

1. identify a vertex of `Q` with `r`; or
2. join a vertex of `Q` to `r` by a path of positive length.

Arbitrary finite trees may be attached at arbitrary vertices of the resulting
cactus. In case 2, the internal vertices of the joining path may also carry
arbitrary trees. Put

`delta_q=sec(pi/q)-1`.

**Theorem 1 (rooted all-rank guard absorption).** Every such `G` satisfies

`sigma(G)>1-delta_q>0`.                                         (1.1)

More precisely, `G` has an induced vertex partition

`V(G)=V(H_0) disjoint union V(H_1) disjoint union ... disjoint union V(H_t)`

for which

`sigma(H_0)>1-delta_q`                                          (1.2)

and

`sigma(H_j)>0` for `j>=1`.                                      (1.3)

Here `H_0` contains `Q`, the joining path, the root `r`, and at least one
triangle. Thus the conclusion is uniform in `h`; it does not spend one unit
for every triangle opened from the cluster.

The same proof does not require the triangles to form one shared-cut cluster.
Connectedness of the triangular cactus and a distinguished attachment root
are enough. The shared-cluster formulation is therefore a special case.

This proves the bridge/root clause of the proposed locked-cluster absorption
lemma. It also proves the common-root configuration consisting of one hostile
cycle and an arbitrary triangular cluster. It does not address the separate
two-pentagon common-cut problem.

## 2. Rooted characteristic polynomials

For a rooted graph `(X,x)`, put

`p_X(z)=det(zI-A(X))`, `p_X^o(z)=p_(X-x)(z)`.

If `(X,x)` and `(Y,y)` are coalesced by identifying `x` and `y`, the standard
rooted coalescence formula is

`p_(X dot Y)=p_X p_Y^o+p_X^o p_Y-z p_X^o p_Y^o`.                (2.1)

If instead one adds the bridge `xy`, then

`p_(X+xy+Y)=p_X p_Y-p_X^o p_Y^o`.                              (2.2)

Both identities follow by separating determinant terms according to the use
of the common root or bridge. Iterating (2.2) gives the usual continuant for a
joining path. These formulas show that all information exported by a rooted
lobe is carried by the pair `(p_X,p_X^o)`, or by the quotient
`p_X/p_X^o` away from its poles.

Cauchy interlacing says that the zeros of `p_X^o` interlace those of `p_X`.
Equivalently, `p_X/p_X^o` is a real-rooted Nevanlinna quotient, and deleting
the root changes each inertia index by at most one. This controls winding and
rules out poles on the open positive imaginary axis. It does not by itself
give the sign or size of the signed square energy: the residues and the
locations of all interlacing roots still vary with arbitrary rooted trees.
The proof below keeps the exact rooted characteristic polynomial but uses its
Sachs expansion, where every required coefficient is positive.

## 3. The packing-one rooted packet

The analytic core is stronger than a one-triangle packet.

**Lemma 2 (one hostile cycle plus a packing-one triangular lobe).** Let `H` be
a connected cactus whose cyclic blocks are one copy of `Q=C_q`,
`q=1 mod 4`, and `a>=1` triangles. Assume that no two triangles of `H` are
vertex-disjoint. The hostile cycle may meet the triangular part at a cut
vertex or may be joined to it by a path. Allow arbitrary attached trees. Then

`s+(H)-s-(H)>-2 delta_q`,                                       (3.1)

and hence

`sigma(H)>a-delta_q>=1-delta_q>0`.                              (3.2)

**Proof.** Let `S=V(Q)`. Take as spine the union of all cyclic blocks and the
minimal paths joining them. Every component off the spine is a tree with one
attachment. For a branch directed toward the spine, define its matching
message by

`Q_(u->v)(t)=Z_(T_(u->v))(t)/Z_(T_(u->v)-u)(t)`.

The matching split at `u` gives

`Q_(u->v)(t)=t+sum_w 1/Q_(w->u)(t)>=t`.                         (3.3)

Consequently every spine vertex has an effective activity

`alpha_v(t)=t+y_v(t)`, with `y_v(t)>=0`,                        (3.4)

and all branch eliminations contribute one common positive real factor
`K(t)`. The same factor remains when a cyclic vertex is deleted: its incident
branches then contribute their full matching partitions. This is the
imaginary-axis version of iterating the rooted formulas (2.1)--(2.2).

For a graph `F` with positive vertex activities, let

`Z_F(alpha)=sum_M product_(v unmatched by M) alpha_v`.

Normalize the characteristic polynomial by

`Psi_H(t)=i^(-|V(H)|) p_H(it)=product_j(t+i lambda_j)`.

In the grouped Sachs expansion, a triangle has multiplier `-2i`, while `Q`
has multiplier `+2i`. Since no two triangles are vertex-disjoint, a Sachs
collection contains at most one triangle. It may additionally contain `Q`
when that triangle is disjoint from `Q`. Therefore, after division by `K(t)`,

`Psi_H(t)/K(t)=R+2i(B-A)`,                                     (3.5)

where

`B=Z_(spine-S)(alpha)>0`,

`A=sum_T Z_(spine-V(T))(alpha)>0`,                             (3.6)

the sum runs over all triangular blocks, and

`R=Z_spine(alpha)+4 sum_(T disjoint from Q)
                         Z_(spine-(S union V(T)))(alpha)>0`.    (3.7)

Formula (3.5) is also obtained directly from the rooted coalescence formulas:
the singleton triangular and hostile cycle terms have opposite imaginary
signs, while every admissible double-cycle term is positive real. The
packing-one hypothesis is exactly what excludes higher powers of `-2i`.

Let `Z_q(t)` be the bare signless matching partition of `C_q`. Partition the
matchings counted by `Z_spine(alpha)` according to whether they use an edge
between `S` and its complement. Matchings using no such edge factor, so

`Z_spine(alpha)=Z_Q(alpha|S) B+E`, with `E>=0`.                 (3.8)

By (3.4) and coefficientwise positivity,

`Z_Q(alpha|S)=Z_q(t)+L`, with `L>=0`.                           (3.9)

Combining (3.6)--(3.9) gives the strict rooted comparison

`R-Z_q(t)(B-A)`

` =E+LB+Z_q(t)A`

`   +4 sum_(T disjoint from Q)
          Z_(spine-(S union V(T)))(alpha)>0`.                  (3.10)

No lower bound on a tree message is used beyond positivity and
`alpha_v>=t`.

Since `R>0`, the continuous argument of `Psi_H(t)` that tends to zero at
infinity is

`Theta_H(t)=arctan(2(B-A)/R)`,                                 (3.11)

with values in `(-pi/2,pi/2)`. For the isolated hostile cycle,

`Psi_Q(t)=Z_q(t)+2i`,

so

`theta_q(t)=arctan(2/Z_q(t))`.                                 (3.12)

If `B-A<=0`, (3.11) is nonpositive and is strictly below (3.12). If
`B-A>0`, divide (3.10) by the positive quantity `R Z_q(t)`. In both cases,

`Theta_H(t)<theta_q(t)` for every `t>0`.                        (3.13)

The signed Coulson identity is

`s+(F)-s-(F)=-(4/pi) integral_0^infinity t Theta_F(t) dt`.      (3.14)

For `q=1 mod 4`, direct evaluation of the cycle eigenvalues gives

`s+(Q)-s-(Q)=-2(sec(pi/q)-1)=-2 delta_q`.                      (3.15)

Integrating the strict pointwise comparison (3.13) proves (3.1).

The cactus `H` has cyclomatic number `a+1`, hence
`|E(H)|=|V(H)|+a`. Using
`s+(H)+s-(H)=2|E(H)|` together with (3.1) gives

`s+(H)>|V(H)|+a-delta_q`,

which is (3.2). QED.

The proof covers an arbitrary joining-path length without a separate
continuant estimate. In (3.8), all connector dependence is already contained
in positive matching subpartitions. Root identification is the zero-length
coalescence case, and a bridge is the first case of (2.2).

## 4. Rooted Voronoi decomposition

We now remove the packing-one restriction without paying for split triangles.

Choose a maximum collection of pairwise vertex-disjoint triangles in the
triangular cactus `A`. Among its members, name as `T_0` one minimizing
`d_A(r,V(T))`, and name the others `T_1,...,T_t` arbitrarily. Assign each
vertex `v` of `A` to the lexicographically least pair

`(d_A(v,V(T_j)),j)`,

and let `A_j` be the induced graph on the vertices assigned to `j`. By the
choice and priority of `T_0`, the distinguished root `r` belongs to `A_0`:
its first distance coordinate is minimal at `T_0`, and index zero wins every
tie.

The standard shortest-path argument proves:

1. the `A_j` are connected induced subgraphs partitioning `V(A)`;
2. `A_j` contains `T_j`; and
3. the cycle packing number of `A_j` is one.

For the third item, two disjoint cycles in one territory, together with all
chosen triangles in the other territories, would enlarge the maximum packing.
Every cycle of an induced subgraph of a cactus is one of its original cyclic
blocks, so all cycles retained by `A_j` are triangles. Some unselected
triangles may be split by the partition; no cycle-count equality is asserted
or needed.

Form `H_0` by taking `A_0`, the hostile cycle, the root-to-cycle joining path,
and all tree branches attached to these vertices. Put every remaining branch
of `A` with the territory owning its attachment vertex, giving `H_j=A_j` with
those branches for `j>=1`. Components off the cyclic/connector spine have a
unique attachment in a cactus, so this assigns every vertex exactly once.
The `H_j` are induced. Edges crossing between territories are simply omitted,
as required by induced-subgraph square-energy superadditivity.

The triangular cycles retained by `H_0` have packing number one and include
`T_0`. Lemma 2 therefore gives

`sigma(H_0)>1-delta_q`.                                        (4.1)

For `j>=1`, every cycle of `H_j` is a triangle, its cycle packing number is
one, and it contains `T_j`. The one-phase Sachs argument places its normalized
characteristic polynomial strictly in the lower half-plane. Hence
`s+(H_j)>s-(H_j)`. If its cyclomatic number is `b_j>=1`, then

`sigma(H_j)>b_j-1>=0`.                                         (4.2)

Positive square energy is superadditive over induced vertex partitions:

`s+(G)>=sum_j s+(H_j)`.                                        (4.3)

Subtracting the partitioned vertex count and applying (4.1)--(4.2) yields

`sigma(G)>=sum_j sigma(H_j)>1-delta_q>0`,                       (4.4)

because `q>=5` implies `delta_q<1`. This proves Theorem 1.

## 5. DNN coupling and the all-rank ledger

The sharp cactus DNN estimate for a cactus with `h` triangles and one cycle
`Q` gives only

`sigma(G)>=h-(h epsilon_3+epsilon_q)=-epsilon_q`,               (5.1)

where `epsilon_3=1` and
`epsilon_q=q tan^2(pi/(2q))`. Thus the DNN certificate loses exactly one unit
on every triangle and remains negative at every rank.

The rooted packet proof supplies the missing coupling. It does not attempt to
recover all `h` DNN units. The Voronoi partition places one triangle in the
same packing-one characteristic-polynomial packet as `Q`; (3.10) turns their
opposite Sachs phases into the strict credit `1-delta_q`. Every other territory
is merely sign-positive. Consequently the guard ledger is rank-free:

`one rooted triangular guard - hostile demand delta_q > 0`.    (5.2)

This is stronger than adding an unrooted triangular surplus to a hostile
unicyclic lower bound. The latter is invalid because triangular packet surplus
has no known uniform positive constant. Equation (3.10) couples the two blocks
before integration and is uniform over every tree activity.

## 6. Inertia and interlacing audit

The proof is consistent with, but does not overclaim from, rooted inertia.

* Deleting a root changes `n+` and `n-` by at most one. This ensures that the
  rooted pairs in (2.1)--(2.2) have the expected interlacing behavior.
* Interlacing alone cannot compare `s+`: it controls eigenvalue order, not the
  sum of their positive squares after coalescence.
* The normalized polynomial in (3.5) has `R>0`, so it never crosses the
  imaginary axis as `t` varies over `(0,infinity)`. Thus its continuous
  argument is the principal arctangent in (3.11), with no hidden `2 pi`
  winding. This is the exact phase consequence that the coarse inertia data
  cannot provide.
* The strict term `Z_q(t)A` in (3.10) survives at every spectral scale. Hence
  strictness is not inferred from a limiting inertia count or from summing
  arbitrarily small positive territorial margins.

## 7. Scope and remaining obstruction

The rooted hostile-cycle inequality requested for an arbitrary connected
triangular cluster is therefore proved exactly, both for coalescence at the
distinguished root and for an arbitrary nonempty bridge path. It provides the
all-rank guard absorption needed for the residual family `T^h Q` whenever the
distinguished `Q` is attached to the triangular part at one rooted interface.

What remains outside this note is topological rather than analytic:

1. extracting such a one-root interface from every fully shared residual
   incidence without destroying the needed cycles; and
2. the residual `T^h P P` when two pentagons are locked at a common cyclic
   cut or must be handled through two labelled interfaces.

The old common-cut ownership obstruction still prevents a partition that
retains different cycles in different territories when all require the same
cut vertex. For one hostile cycle, Lemma 2 bypasses that obstruction by keeping
the entire packing-one rooted packet and comparing its characteristic phase
directly. A two-hostile-cycle analogue would contain additional positive and
negative real Sachs terms and is not implied by the present one-cycle
comparison.
