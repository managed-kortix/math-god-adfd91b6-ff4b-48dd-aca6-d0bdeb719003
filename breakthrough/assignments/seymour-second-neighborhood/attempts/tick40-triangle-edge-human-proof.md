# Tick 40: human elimination of triangle plus a disjoint hole

Again use the shape-independent predecessor lower bound from tick 38:

```
|P|>=4.                                             (1)
```

Suppose the four T-holes are

```
xy, xz, yz, ef,
```

a triangle and a disjoint edge. Fix a source `a in P`, write
`S={a} union N_T+(a)`, and let I be its inaccessible vertices. The standard
argument gives at least two inaccessible vertices and, for each one, at least
one crossing hole into S.

Exactly two packet families survive.

1. **TT:** `I={x,y}` consists of two triangle vertices. The third vertex z is
   in S. Both inaccessible vertices have one crossing hole and are saturated:

   ```
   N+(x)=N+(y)=S\{z}.                              (2)
   ```

2. **TE:** `I={x,e}` consists of one triangle vertex and one endpoint of the
   disjoint edge. The other triangle vertices y,z and the edge mate f all lie
   in S. Exact degree gives

   ```
   N+(e)=S\{f},
   N+(x)=(S\{y,z}) union {e}.                      (3)
   ```

   Indeed, e is saturated by its eight forced outneighbors in S, so the present
   pair xe points `x->e`; x then has its seven forced outneighbors in
   `S\{y,z}` plus e.

The pair `{e,f}` is impossible because neither endpoint has a crossing hole.
No packet has three inaccessible vertices: a TE pair already forces the other
two triangle vertices and the edge mate into S, while adding an edge endpoint
to a TT pair violates endpoint packing with a saturated triangle endpoint.

Each of the three TT labels supports at most one source, because (2) recovers S
from either fixed triangle row. All TE labels using e collectively support at
most one source because `S=N+(e) union {f}`, independently of which triangle
vertex is inaccessible; similarly there is at most one TE source using f.

Finally, two distinct TT labels exclude every TE source. Two TT labels share a
triangle vertex; for instance `{x,y}` and `{x,z}`. Equation (2) then gives

```
N+(x)=N+(y)=N+(z).                                 (4)
```

If a TE packet `{t,e}` existed, (3) would force `t->e` and force e to dominate
the other two triangle vertices. But (4) turns `t->e` into an arc from every
triangle vertex to e. In particular, each of those other two vertices both
points to e by (4) and is dominated by e through (3), producing a digon.

Thus, if at least two TT labels occur, there are no TE sources and at most the
three TT labels. If at most one TT label occurs, there is at most that source
plus one source for each of e and f. In all cases

```
|P|<=3,                                             (5)
```

contradicting (1). Therefore the triangle-plus-disjoint-edge hole shape is
impossible uniformly in rho.

This is a restricted shape elimination inside `n=18,m=9,k=4`, not an order-18
elimination and not a proof of SNC.
