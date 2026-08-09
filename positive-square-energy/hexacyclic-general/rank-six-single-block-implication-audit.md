# Audit of the rank-six single-block implication

## Verdict

The implication from a complete exact canonical-plus-coordinate DNN witness
family to

`s^+(G) >= |V(G)|`

is valid, including simultaneous arbitrary subdivisions and rooted trees based
at internal subdivision vertices, provided the hypotheses below are stated
explicitly. No graph contraction or subdivision monotonicity of `s^+` is used.

The important hidden restriction is that the realized graph is simple. The
suppressed kernel may be a multigraph, but its replacement paths must form a
simple graph. Also, a canonical witness by itself is not enough on a residual
parity row: every one-coordinate frontier must be owned, except where a
separate exact rule proves the omitted coordinate targets.

## Exact finite premise

Let `K` be a loopless 2-connected multigraph of cyclomatic rank six and minimum
degree at least three. Write its physical edges as `e_1,...,e_p`. A realization
`B(l)` replaces `e_i` by a path of positive length `l_i`, with distinct
replacement paths internally vertex-disjoint. Assume `B(l)` is simple.

For every physical parity orbit, choose its canonical simple vector `c` as
follows on each parallel class of multiplicity `m` containing `o` odd paths:

```text
o=0:  (2,...,2),
o>0:  (1,3,...,3,2,...,2),
```

where there are `o` odd coordinates and `m-o` even coordinates. The exact
finite premise needed for the implication is:

1. every parity orbit is accounted for;
2. a coarse-owned orbit has one feasible branch Gram certificate of DNN excess
   at most five at `c`; and
3. every residual orbit has an exact feasible certificate of excess at most
   five for every member of

   `F(c)={c} union {c+2e_i:1<=i<=p}`.

It is harmless for different frontier members to use different Grams. Symbolic
records may replace rational records, but only if their exact physical path
ledger, positive semidefiniteness, denominator signs, and excess bound are
verified. If a symbolic record owns only selected coordinates, all other
coordinates still need ordinary records or another exact owner.

## From a Gram-chain witness to the DNN bound

For a finite simple graph `X`, use

`kappa(X)=min_C sum_(uv in E(X)) 2/(1-C_uv)`,

where `C` ranges over correlation matrices. Represent `C` by unit vectors
`x_v`. On a path `v_0...v_j`, set `y_h=(-1)^h x_{v_h}` and
`q_h=<y_{h-1},y_h>`. Since `C_(v_(h-1),v_h)=-q_h`, each edge contributes

`2/(1-C_uv)=2/(1+q_h)=1+(1-q_h)/(1+q_h)`.

Consequently an exact chain witness with all `1+q_h>0` and total excess at most
five proves

`kappa(B(l)) <= |E(B(l))|+5`.                                  (A)

The witness is only required to be feasible; it need not minimize `kappa`.

For fixed branch endpoint correlation `r`, exact elimination of a length-`j`
path gives the least possible excess

`f_j(r)=j tan^2(acos((-1)^j r)/(2j))`.                          (B)

For a fixed parity, `(-1)^j r` is unchanged when `j` is replaced by `j+2`.
Writing `beta=acos((-1)^j r)` and `z=beta/(2j)`, differentiation of
`j tan^2(beta/(2j))` shows that its derivative has the sign of
`sin(z)cos(z)-2z`, which is nonpositive for `0<=z<pi/2` and is negative away
from `z=0`. The endpoint case with infinite cost is also monotone in the
extended sense. Thus

`f_(j+2)(r) <= f_j(r)`.                                        (C)

This use of (C) remains valid when the stored witness is not an equal-arc
minimizer: retain its branch vectors, discard the old internal vectors on the
lengthened path, and install an optimal equal-arc chain. Its new cost is at
most the old path's minimum and hence at most the cost of the discarded
feasible chain. Internal path vectors for different physical edges may be
placed in separate additional dimensions, so all replacements are compatible
with the common branch Gram.

## Why the frontier covers every simple subdivision

Fix a simple realization length vector `l` in the parity orbit represented by
`c`. In a parallel class, simplicity permits at most one length-one path. After
permuting indistinguishable parallel kernel edges, the odd lengths of `l`
difference `l_i-c_i` is even. Hence `c<=l` coordinatewise.

If `l=c`, use the canonical witness. Otherwise choose any coordinate `i` for
which `l_i>=c_i+2`. Then

`c+2e_i <= l`.

Use the exact witness for `c+2e_i` and apply (C), one coordinate at a time, to
reach `l`. This proves (A) for arbitrary simultaneous lengthening, not just for
subdividing one physical edge.

For a coarse-owned row, the same argument starts at `c`, because the one coarse
branch Gram already has excess at most five and every coordinate is only
lengthened within its parity. For a residual row, the canonical target alone
does not justify this step if equality occurs at `c`: the `p` coordinate
frontiers are what prevent an unsupported inference that the canonical
equality Gram extends with the required bound.

Automorphism quotienting creates no additional assumption if the verifier
retains a physical edge ordering. Relabel the branch Gram and physical path
ledger by a kernel automorphism, and permute indistinguishable members of each
parallel class before making the coordinatewise comparison.

## Rooted-tree lift, including internal roots

Let `L=|E(B)|`. Subdivision preserves cyclomatic rank, so connectedness and
rank six give

`|V(B)|=L-5`.                                                   (D)

The correlation definition gives the one-vertex-sum identity

`kappa(H_1 vee H_2)=kappa(H_1)+kappa(H_2)`.                    (E)

For the upper bound in (E), glue feasible unit-vector representations at the
common vector and put their orthogonal complements in mutually orthogonal
subspaces. For the lower bound, restrict any feasible correlation matrix to
each summand. Also `kappa(T)=|E(T)|` for a tree: every edge term is at least one,
and assigning the two bipartition classes the vectors `u` and `-u` attains one
on every edge.

Now attach finite rooted trees, otherwise vertex-disjoint from the core and
from one another, by identifying each root with an arbitrary vertex of `B`.
Let their total number of edges be `t`. Iterating (E), regardless of whether a
root is a branch vertex or an internal subdivision vertex, gives

`kappa(G)=kappa(B)+t <= L+5+t`.                                (F)

The weaker inequality in (F) is sufficient. No attachment is contracted, and
the root's degree in `B` is irrelevant to the one-vertex-sum identity.

For a finite simple graph the DNN/LTZ inequality and adjacency trace identity
are

`s^-(G)<=kappa(G)`,  `s^+(G)+s^-(G)=tr(A(G)^2)=2|E(G)|`.

Since `|E(G)|=L+t` and, by (D), `|V(G)|=L-5+t`, (F) yields

```text
s^+(G) >= 2(L+t)-(L+5+t)
         = L-5+t
         = |V(G)|.
```

## Assumptions that must not be suppressed

1. **Simplicity of the realization.** The kernel is allowed to have parallel
   edges, but `B` and the final `G` must be finite simple graphs. Simplicity is
   used both in the canonical parallel-class vector and in
   `tr(A^2)=2|E|` with the ordinary adjacency matrix.
2. **Physical subdivision model.** Replacement paths have positive integral
   lengths, are internally vertex-disjoint, and meet only at their prescribed
   branch endpoints. Otherwise the path objective does not separate by kernel
   edges and cyclomatic rank need not remain six.
3. **Complete coordinate ownership.** For each residual parity source, all
   `p+1` targets must be certified or exactly reassigned. A null search result,
   a canonical symbolic tag, or target counts without set equality is not this
   premise.
4. **Parity is fixed during monotonicity.** Lengths are increased by two. There
   is no claimed monotonicity under a one-edge subdivision, which changes the
   transformed endpoint sign.
5. **Trees are genuine one-vertex attachments.** Each attached component meets
   the existing graph only in its root. A connector meeting the core in two
   vertices is not a rooted-tree attachment and is not covered by (E).
6. **Single cyclic block.** The proof starts with one rank-six 2-connected
   kernel realization. It does not combine several cyclic blocks of total rank
   six; that requires a separate block-tree ownership theorem, even though
   `kappa` itself is additive at cut vertices.
7. **No graph-contraction premise.** Contractions appearing in symbolic
   equality templates mean equal or signed-equal vectors in a quotient Gram
   description. They do not authorize contracting edges of `G`, and the proof
   uses no spectral monotonicity under contraction.

## Failure modes rather than a graph counterexample

Under the exact finite premise and the assumptions above, there is no gap in
the implication and hence no counterexample to this implication stage. Two
nearby broader claims are not established:

- If non-simple subdivisions are admitted, the canonical domination argument
  can fail because two parallel physical paths may both have length one.
  Moreover, for a multiplicity-weighted adjacency matrix,
  `tr(A^2)` is generally `2 sum m_uv^2`, not `2|E|`; the final displayed
  calculation is therefore not the stated proof.
- If only canonical witnesses are known for a residual row, they do not alone
  cover all same-parity descendants. Path monotonicity compares optimal path
  costs while holding the branch Gram fixed; a canonical cost-five Gram may
  have no slack for a required nonzero extension. The one-coordinate witness
  family, or an exact symbolic extension rule, is essential.

Thus the correct audited conclusion is conditional and precise: exhaustive
exact ownership of the canonical-plus-coordinate universe proves the weak
positive square-energy inequality for every finite simple rank-six
single-block realization and every collection of genuine rooted-tree
attachments, including attachments based at internal subdivision vertices.
