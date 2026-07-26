# Tick 45: human elimination of all three-hole shapes

Work in the isolated-root `m=9,k=3` normal form. There are eleven arcs from B
to C. Let K be the B vertices dominating both C vertices, `x=|K|`, and let P be
the union of their A' predecessor sets, `r=|P|`. Then `x in {4,5}`. The exact
B-row identity and three-hole budget give

```
C(x,2) <= x(r-2)+3-Q,                             (1)
```

where `Q=sum_{b in K}1[b->z]>=0`. Hence

```
r>=3, and r>=4 if x=5.                            (2)
```

For a source `a in P`, put `S={a} union N_T+(a)`. Both C vertices are exact
second neighbors through a common dominator, so badness forces at least two
vertices outside S to be inaccessible by a T-two-walk. If inaccessible t has
q(t) holes into S, exact degree eight leaves `q(t)-1` outgoing slots outside S.
For an inaccessible set J,

```
C(|J|,2)-e_h(J) <= sum_{t in J}(q(t)-1).          (3)
```

With only three holes, (3) excludes three inaccessible vertices. Thus every
source has exactly one saturated inaccessible pair.

The five simple three-edge graphs form an exhaustive shape partition, checked
independently on all `C(15,3)=455` edge triples by
`experiments/test_m9_k3_shapes.py`.

## Matching

If the holes form `3K2`, each inaccessible vertex uses its unique matching hole
into S and dominates the other eight members of S. Two inaccessible vertices
therefore have no outgoing slot for their mutual present pair. Equivalently,
their pair would have to be a second hole incident with one endpoint. Impossible.

## `P3 + K2`

For holes `01,12,34`, the only packets are P13 and P14. Their exact rows are

```
P13: N+(3)=S\{4}, N+(1)=(S\{0,2}) union {3};
P14: N+(4)=S\{3}, N+(1)=(S\{0,2}) union {4}.
```

Each label reconstructs S and supports at most one source. Hence `r<=2`,
contradicting (2).

## Four-vertex path

For holes `01,12,23`, the only packets are P02, P12, P13. Saturation forces

```
P02: 2->0 and 0->3;
P12: 2->0 and 1->3;
P13: 1->3 and 3->0.
```

Each packet has a saturated endpoint that reconstructs S. P02 and P13 force
opposite orientations of 03, so at most two labels and sources coexist. Again
`r<=2`, contrary to (2).

## Claw

For holes `01,02,03`, center plus leaf leaves the leaf with no crossing hole.
Two inaccessible leaves each have one crossing hole and are saturated, but
their mutual pair is present. Thus no packet and no source exists.

## Triangle

Let the holes form a triangle H=`{h0,h1,h2}`. The three possible packets are
the three pairs in H. Each supports at most one source. If fewer than three
labels occur then `r<=2`, contradicting (2). Thus all three occur, forcing
`r=3` and consequently `x=4`.

For the packet whose included triangle vertex is hi, write its closed source
set as `S_i=R_i union {hi}`. The other two triangle vertices are inaccessible
and saturated, so their global outneighborhoods equal `R_i`. Comparing the
three packet identities gives

```
N+(h0)=N+(h1)=N+(h2)=R,                           (4)
S_i=R union {hi}.                                  (5)
```

The source of packet i cannot lie in R: equation (4) would give `hi->a`, while
source membership in `S_i` gives `a->hi`. Hence the source is hi itself. Thus

```
P=H subset A'.                                     (6)
```

Every `b in K` has a predecessor in P. Since every source hi has
outneighborhood R, this puts `K subset R`, and in fact all three hi dominate
every b in K. Therefore `p_b=3` for every b. No triangle hole meets K, so
`h_b=0` and there is no hole internal to K. The B-row identity becomes

```
d_B+(b)=1-q_b <=1.
```

But all `C(4,2)=6` pairs internal to K are present and contribute one B-arc,
whereas

```
6 <= sum_{b in K}d_B+(b) <=4,
```

a contradiction.

Thus every three-hole shape is impossible, uniformly for `rho=0,1,2,3`. The
entire isolated-root `m=9,k=3` strip is human-eliminated. This is not an
order-18 theorem and not a proof of SNC.
