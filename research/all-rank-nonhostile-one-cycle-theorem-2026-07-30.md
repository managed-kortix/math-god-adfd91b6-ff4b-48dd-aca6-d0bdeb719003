# All-rank nonhostile one-cycle cactus theorem

**Date:** 2026-07-30

## 1. Statement

For a finite simple graph `H`, write

```text
s+(H) = sum_{lambda>0} lambda^2,
s-(H) = sum_{lambda<0} lambda^2,
sigma(H) = s+(H)-|V(H)|.
```

where the sums run over the adjacency eigenvalues of `H` with multiplicity.

**Theorem.** Let `G` be a connected cactus whose cyclic blocks consist of
`r>=1` triangles and one distinguished block `Q=C_q`. Bridges, the incidence
pattern of the cyclic blocks, and trees attached at arbitrary vertices are
unrestricted. If either

1. `q` is even, or
2. `q=3 mod 4`,

then

```text
sigma(G)>0.
```

When `q=3`, the distinguished block is simply one more triangle, so the
theorem is the all-triangular case. No assertion is made here when
`q=1 mod 4`.

The proof uses the grouped Sachs expansion, signed Coulson identity,
induced-subgraph superadditivity, and maximum-packing territory lemma proved
self-containedly in `packing-two-square-energy/paper.tex` (respectively
Lemma `sachs`, Lemma `coulson`, equation `superadditivity`, and Lemma
`cycle-territories`). The earlier rank-uniform triangular application and its
warning about lost cycle credits are recorded in
`research/arbitrary-r-shared-triangle-uniform-surplus-2026-07-26.md`. The
present argument supplies the mixed triangle/even-cycle packing-one step and
then applies exactly that territory mechanism.

## 2. Packing-one mixed-phase lemma

Call a cycle favorable if its length is `3 mod 4`.

**Lemma 1 (packing-one mixed phase).** Let `H` be a finite graph with cycle
packing number one. Suppose every cycle of `H` is favorable except possibly
for even cycles. If `H` contains at least one favorable cycle, then

```text
s+(H)>s-(H).
```

In particular, the lemma applies when the cyclic blocks of a cactus `H`
consist of one or more triangles and at most one even cycle.

**Proof.** For `t>0`, put

```text
Z_F(t) = sum_j m_j(F)t^(|V(F)|-2j) > 0,
Psi_H(t) = i^(-|V(H)|) det(itI-A(H)),
```

where `m_j(F)` is the number of `j`-edge matchings of `F`. The Sachs formula
grouped by pairwise vertex-disjoint cycle collections is

```text
Psi_H(t)
  = sum_Ccal (product over C in Ccal of (-2 i^(-|C|)))
      Z_(H-V(Ccal))(t).                                      (2.1)
```

This is Lemma `sachs` of `packing-two-square-energy/paper.tex`. Since the
cycle packing number is one, only the empty collection and singleton cycle
collections occur in (2.1). For a favorable cycle `C`,

```text
-2 i^(-|C|) = -2i,
```

whereas this factor is real for every even cycle. Consequently

```text
Im Psi_H(t)
  = -2 sum_(C favorable cycle of H) Z_(H-V(C))(t) < 0         (2.2)
```

for every `t>0`. The strict inequality uses both the existence of a favorable
cycle and positivity of every matching carrier. Thus even-cycle singleton
terms can change only the real part; they cannot cancel the favorable
imaginary part.

If the adjacency eigenvalues are `lambda_1,...,lambda_h`, then

```text
Psi_H(t) = product_j (t+i lambda_j).
```

Hence

```text
Theta_H(t) = sum_j arctan(lambda_j/t)
```

is a continuous argument of `Psi_H(t)` tending to zero as `t` tends to
infinity. By (2.2), `Psi_H(t)` remains in the open lower half-plane. Its
principal argument is therefore continuous and belongs to `(-pi,0)`; its
difference from `Theta_H` is a constant multiple of `2pi`, and the limit at
infinity shows that constant is zero. Thus `Theta_H(t)<0` for every `t>0`.
The signed Coulson identity, Lemma `coulson` of
`packing-two-square-energy/paper.tex`, is

```text
s+(H)-s-(H) = -(4/pi) integral_0^infinity t Theta_H(t) dt.
```

The integral is convergent there, and its integrand has strict negative sign.
Therefore `s+(H)>s-(H)`. QED.

The same proof with no even cycles is the packing-one favorable-cycle lemma.
Although the more general favorable theorem in
`packing-two-square-energy/paper.tex` permits packing number two, only the
packing-one form is needed below.

## 3. Maximum-packing territories

We restate the exact facts needed from Lemma `cycle-territories` of
`packing-two-square-energy/paper.tex`, including the points on which the final
strictness depends.

**Lemma 2 (maximum-packing Voronoi territories).** Let `X` be connected and
let `C_1,...,C_k` be a maximum-cardinality family of pairwise vertex-disjoint
cycles. Order this family, assign each vertex `v` to the lexicographically
least pair

```text
(d_X(v,V(C_i)),i),
```

and let `X_i` be induced by the vertices assigned to `i`. Then the `X_i` are
pairwise vertex-disjoint induced subgraphs whose vertex sets exhaust `V(X)`;
each `X_i` is connected, contains `C_i`, and has cycle packing number exactly
one.

**Justification.** A selected cycle is wholly in its own territory because
its vertices have distance zero from it and positive distance from every
other selected cycle. If `v` belongs to territory `i`, choose the predecessor
`u` on a shortest path from `v` to `C_i`. Integer distances and the fixed
tie-break imply that `u` is again assigned to `i`: against an earlier center
the inequality at `v` is strict, and against a later center equality at `u`
is won by `i`. Iteration gives a path inside `X_i` from `v` to `C_i`, proving
connectivity. Finally, if `X_i` contained two disjoint cycles, those two,
together with all selected `C_j` for `j!=i`, would form a packing of size
`k+1`. This contradicts maximum cardinality. This last replacement argument
requires a maximum packing, not merely a maximal one.

For later use, every cycle in an induced territory of a cactus is an original
cyclic block. Indeed, it is first of all a cycle of the original graph. Every
cycle lies in one block, and in a cactus each non-bridge block containing a
cycle is itself a cycle; hence the cycle equals that cyclic block. Taking an
induced subgraph cannot create a new cycle or turn a proper fragment of a
cyclic block into a cycle.

## 4. Choice of the maximum packing

We now apply Lemma 2 to `G`, but first choose its centers so that strictness
cannot be lost.

If `q=3 mod 4`, every cyclic block, including `Q`, is favorable. Every member
of every cycle packing is therefore favorable.

If `q` is even, there exists a maximum cycle packing containing a triangle.
To see this, start with any maximum packing `P`. If `P` already contains a
triangle, there is nothing to prove. If it contains no triangle, its only
possible member is the unique nontriangular cycle `Q`; because `G` has a
cycle, `|P|=1`. Replacing `Q` by any one of the `r>=1` triangular blocks gives
another packing of the same, hence maximum, cardinality. Fix such a maximum
packing and place a selected triangle first in the territory priority order.

Thus, in both parity cases, at least one selected center is favorable. More
specifically, in the even case at least one center is a triangle. This is all
that is required: the argument does not assume that a maximum packing retains
`Q`, and remains valid if `Q` is split among several territories.

## 5. Proof of the theorem

Form the induced territories `G_1,...,G_k` from the selected maximum packing.
Write `n_i=|V(G_i)|` and `m_i=|E(G_i)|`. Lemma 2 gives, for every `i`,

```text
G_i connected, G_i cyclic, and its cycle packing number is one. (5.1)
```

Because every induced-territory cycle is an original cactus block, the cycles
of `G_i` are among the given triangles and `Q`.

First suppose `q=3 mod 4`. Every `G_i` contains its favorable selected center,
and all its cycles are favorable. Lemma 1 gives

```text
s+(G_i)>s-(G_i).
```

Since `s+(G_i)+s-(G_i)=2m_i`, it follows that

```text
s+(G_i)>m_i>=n_i.                                  (5.2)
```

The last inequality is elementary but important: a connected `n_i`-vertex
graph containing a cycle has at least the `n_i-1` edges of a spanning tree and
at least one additional edge. This proof includes `q=3`: then all `r+1`
cyclic blocks are triangles, so every territory satisfies the same strict
favorable estimate.

Now suppose `q` is even. A territory containing a triangle satisfies Lemma 1,
even if it also contains `Q`, and hence satisfies the strict inequality (5.2).
A territory containing no triangle can only contain the original block `Q`.
There is at most one such territory. By (5.1) it contains `Q`; all its other
blocks are bridges, so it is connected and unicyclic. Therefore `m_i=n_i`.
Moreover, an even cycle with trees attached through bridges is bipartite, and
the adjacency spectrum of a bipartite graph is symmetric about zero. For this
even-only `Q` territory,

```text
s+(G_i)=s-(G_i)=m_i=n_i.                            (5.3)
```

By the packing choice in Section 4, at least one territory contains its
selected triangular center, so at least one territory has the strict estimate
(5.2); all remaining territories have either (5.2) or (5.3).

Finally, induced-subgraph positive square-energy superadditivity, equation
`superadditivity` of `packing-two-square-energy/paper.tex`, and exhaustion of
the vertex partition give

```text
s+(G) >= sum_i s+(G_i) > sum_i n_i = |V(G)|.
```

The strict sign comes from at least one favorable territory and cannot be
lost by an even-only territory, where equality is exact. Hence
`sigma(G)>0`, as claimed. QED.

## 6. Scope check

- Arbitrary shared cut vertices, bridge paths, and cyclic-block incidence are
  absorbed by graph distance in the maximum-packing territories.
- Arbitrary attached trees are ordinary vertices in the same exhaustive
  induced partition; no pruning or ownership convention is required.
- Split cyclic blocks contribute no hidden cycle: every territory cycle is an
  original complete cactus block.
- The proof uses only `m_i>=n_i`, except that the possible even-only territory
  has the sharper bipartite equality `s+=s-=m_i=n_i`.
- The theorem covers even `q`, every `q=3 mod 4`, and `q=3` explicitly. It
  deliberately makes no claim for the hostile residue `q=1 mod 4`.
