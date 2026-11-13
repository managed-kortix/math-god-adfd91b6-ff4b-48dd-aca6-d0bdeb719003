# `R31-S:D3` independent exact rooted-tree scout

## Scope and outcome

This is a counterexample-search note, not a closure note.  It addresses the
open packet

`D=Theta(1,2,2)` plus three legally incident triangular blocks,

with arbitrary finite rooted trees attached at any of the ten vertices of the
bare incidence hull.  Write `sigma(G)=s^+(G)-|V(G)|`; the target is
`sigma(G)>3`.

No counterexample was found.  The strongest complete exact result obtained is:

> For each of the 14 one-side incidence records, and every assignment of an
> unlabeled rooted tree to each labelled core vertex with at most four
> non-root attachment vertices in total, `sigma(G)>3`.

This finite statement covers 27,664 labelled-site graphs.  Exact integer
characteristic polynomials give 7,797 distinct polynomial/order classes.  At
24-bit dyadic Sturm precision, all 7,797 classes have a strictly positive
certified margin.  The minimum certified lower endpoint occurs for

`('direct3', ('x','x','x'))`,

with one pendant leaf at core vertices `A` and `B` and a two-leaf star rooted
at `x`.  Its characteristic polynomial is

`x^14-18x^12-10x^11+87x^10+70x^9-151x^8-132x^7`
`+114x^6+94x^5-39x^4-22x^3+6x^2`,

and the exact Sturm enclosure is

`sigma in [958026290839775317,958026414427488911] / 144115188075855872`,

so

`sigma-3 in [525680726612207701,525680850199921295] / 144115188075855872`.

The lower margin endpoint is about `3.64764`; the decimal is only a summary of
the displayed rational certificate.

A separate complete floating-point census through eight attachment vertices
(6,674,892 graphs) found a monotonically decreasing low pattern.  Its smallest
sample was the all-at-`x` direct record with leaves at `A,B,z` and a five-leaf
star at `x`, numerically `sigma approximately 6.3208225562`.  Exact
characteristic-polynomial/Sturm recomputation of the 200 numerical low-tail
rows certified all 49 distinct polynomial/order classes.  For the numerical
minimizer,

`sigma-3 >= 250914257973829148728471 / 75557863725914323419136 > 0`.

The complete eight-vertex census itself remains **numeric scouting**, not an
exact proof for all 6,674,892 rows; only its selected 200-row low tail was
exactly recomputed.

## Independent record and tree census

The program regenerates rather than imports the old D3 diagnostic's records.
For owner set `{A,B,x}`, requiring the interior owner `x` gives:

- 6 three-direct records;
- 5 chain-of-two plus direct records;
- 2 fork records;
- 1 chain-of-three record.

Thus there are 14 one-side records (28 after reflection).  Each bare graph has
10 vertices and 14 edges.  Rooted attachments are canonical tuples of sorted
child trees.  The generated counts for rooted-tree orders 1 through 9 are

`1,1,2,4,9,20,48,115,286`.

A bound `B` means that the sum of non-root vertices over all ten attached
rooted trees is at most `B`; a root with several branches is represented as
one rooted tree.  Therefore this is exhaustive for the stated finite bound,
not a sampling of tree shapes.

## Exact method

For an attachment `T_v` rooted at core vertex `v`, set

`d_v(x)=phi(T_v-v;x)` and `c_v(x)=phi(T_v;x)-x d_v(x)`.

The program computes

`phi_G(x) = sum_(S subseteq A) phi_(H-S)(x)`
`           product_(v in S)c_v(x) product_(v in A-S)d_v(x)`,

where `H` is the ten-vertex incidence hull and `A` is the set of nontrivial
attachment sites.  Core-minor characteristic polynomials are computed over
the integers via traces and Newton identities.  Selected rows are independently
cross-checked against a full adjacency-matrix characteristic polynomial.

For each integer characteristic polynomial the code:

1. computes exact squarefree multiplicity layers over `Fraction`;
2. isolates every positive root by a rational Sturm sequence and dyadic
   bisection;
3. squares rational interval endpoints and includes root multiplicities;
4. subtracts the exact graph order to enclose `sigma`.

The complete `B<=4` run performed 40 full-adjacency/coalescence polynomial
cross-checks.  The 200 selected `B<=8` low-tail rows all received that direct
cross-check.  Exact cospectral deduplication is performed only after the
integer polynomial and order are known; class multiplicities sum back to the
full graph count.

## Additional hostile pattern checks

Exact equal-star family checks attached `k` pendant leaves at **each** of all
ten core vertices of `('direct3',('x','x','x'))`.  For `k=10,20,50,100`, exact
Sturm certificates still give `sigma>3`; the certified surplus intervals move
from approximately `5.09415` down to `4.37169`.  This is useful stress evidence
that margins can decay substantially under large attachments.  It is not a
proof for every `k` or every rooted tree.

Floating-point-only searches also included random rooted recursive trees with
up to 100 extra vertices and weighted star allocations up to one million
leaves.  They found no candidate at or below 3.  These searches are not
certificates and are not encoded as theorem evidence.

## Reproduction

From repository commit `82eb0b1dbd17d12789c8465b38e5d18eb6897b4a`:

```text
python3 -m py_compile research/r31-s-d3-exact-tree-scout.py
python3 research/r31-s-d3-exact-tree-scout.py --mode exact --print-records
python3 research/r31-s-d3-exact-tree-scout.py \
  --mode exact --extra 4 --bits 24 --direct-checks 40 \
  --keep-certificates 40 \
  --output research/fixtures/r31-s-d3-exact-tree-b4-certificate.json
python3 research/r31-s-d3-exact-tree-scout.py \
  --mode numeric --extra 8 --keep 200 \
  --output research/fixtures/r31-s-d3-numeric-tree-b8-scout.json
python3 research/r31-s-d3-exact-tree-scout.py \
  --mode exact --extra 8 --bits 32 \
  --tail-input research/fixtures/r31-s-d3-numeric-tree-b8-scout.json \
  --direct-checks 200 --keep-certificates 200 \
  --output research/fixtures/r31-s-d3-exact-tree-b8-low-tail-certificate.json
python3 research/r31-s-d3-exact-tree-scout.py \
  --mode stars --bits 24 --star-k 10,20,50,100 \
  --output research/fixtures/r31-s-d3-equal-stars-exact-certificate.json
```

The exact complete `B<=4` run took about 9m38s in this sandbox.  The complete
numeric `B<=8` run took about 14m39s; the exact 200-row tail replay took about
8s.  Timings are environmental, not part of the certificates.

## What this does not prove

A bounded census cannot prove the arbitrary-rooted-tree theorem.  The observed
margin decreases as the attachment bound grows, so the finite minimum is not a
uniform lower bound.  Nothing here establishes the missing phase implication,
a general positive decomposition, or a uniform DNN/Gram estimate.  Therefore
`R31-S:D3` remains open, and these files must not be treated as a closure owner.
