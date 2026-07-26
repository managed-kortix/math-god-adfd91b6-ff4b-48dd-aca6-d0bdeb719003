# Tick 44: the two star-like four-hole shapes

This supplies the two shape proofs that were previously only asserted in the
notebook.

## Four-star `K1,4`

Let the holes be `h-li` for four leaves `l1,...,l4`. Choose one A' predecessor
a of a common C-dominator and put `S={a} union N_T+(a)`. As in tick 38,
badness forces at least two vertices outside S to be inaccessible by a T-two-
walk. An inaccessible vertex t must have at least one hole into S.

If h and a leaf li are both inaccessible, li has no hole into S, impossible.
If two leaves li,lj are inaccessible, h must lie in S and each leaf has exactly
one crossing hole. Both leaves are therefore saturated by their eight forced
outneighbors in S, but their mutual pair is present and needs an outgoing
endpoint. This is impossible. Thus no two inaccessible vertices exist,
contradicting badness. The four-star shape is impossible.

## Claw plus disjoint edge

Let the holes be

```
01,02,03,45,
```

with claw center 0. The shape-independent B-row count gives `|P|>=4` sources.
For any source, the standard four-hole capacity inequality excludes three
inaccessible vertices, so exactly two occur.

Two claw leaves are saturated and joined by a present pair; center plus leaf
leaves the leaf without a crossing hole; 45 leaves both endpoints without a
crossing hole; and a claw leaf paired with 4 or 5 gives two saturated endpoints
joined presently. The only packets are therefore P04 and P05.

For P04, vertex 5 and at least two claw leaves lie in S. Vertex 4 has its unique
crossing hole 45 and is saturated, so

```
S=N+(4) union {5}.
```

Thus all P04 occurrences reconstruct the same S and support at most one source.
Symmetrically P05 satisfies

```
S=N+(5) union {4}
```

and supports at most one source. Hence `|P|<=2`, contradicting `|P|>=4`.

Both star-like shapes are impossible uniformly in rho. Together with ticks 30
and 38--43, this covers all eleven four-edge shape profiles and human-eliminates
the entire isolated-root `n=18,m=9,k=4` strip. This is not an elimination of
all order-18 branches and not a proof of SNC.
