# Rejected route: one-edge additions via a safe-P3 reduction

## Hostile-audit status

**The claimed reduction below is not proved.**  Hostile audit found a fatal
scope error: deleting a degree-two non-cut vertex from a bare bicyclic graph
can leave a connected bicyclic graph with pendant tree pieces, whereas the
theorem available here covers the bare bicyclic graph itself, not arbitrary
attachments.  For example, in `Theta(5,2,2)` with the branch-vertex chord
added, deleting an internal vertex of the long path leaves pendant path pieces
on a smaller bicyclic core.  Connectivity and the edge count do not make that
graph bare.

The exact conditional statement is: if all three deletions in the induced
`P3` satisfy `s+(G-v)>=|G-v|`, then improved P3 removal gives the displayed
`n+1/16` bound.  The combinatorial bounds `|Theta|<=14`, `p+q<=12`, and
connector span at most three are valid only conditional on that missing
attached-bicyclic deletion theorem.  This file is retained as a dead-end record
and must not be cited as a theorem.

Write

`S(G)=s^+(G)` and `delta(G)=S(G)-|G|`.

The following is the useful reduction.  It proves all sufficiently long bare
theta cores and leaves a sharply localized cycle-pair obstruction.  It does
not use the weighted 2-core inequality, which is unsuitable here: its endpoint
already fails on the bridge `C5--C5`.

## Proposed safe-P3 lemma (unproved)

Let `H` be a connected bicyclic graph, let `e=xy` be a nonedge, and put
`G=H+e`.  Suppose `G` has three vertices inducing a `P3` such that, for every
one of the three vertices `v`,

1. `deg_G(v)=2`, and
2. `G-v` is connected.

The intended conclusion was

`S(H+e) >= |H|+1/16 > |H|`.

Indeed, improved P3 removal chooses one of the three vertices and gives

`S(G) >= S(G-v)+17/16`.

If `n=|H|`, then `G` has `n+2` edges.  For every allowed `v`, the graph `G-v`
is connected, has `n-1` vertices and `n` edges, and hence is bicyclic.  The
bare bicyclic theorem gives `S(G-v)>=n-1`, proving the claim.

Thus a counterexample can contain no induced P3 consisting entirely of
degree-two non-cut vertices of `G`.  Call such vertices safe.

## Bare theta consequence

Let `H=Theta(l_1,l_2,l_3)` be bare.  On path `i`, mark every internal endpoint
of `e`, and let `t_i` be the number of marks.  Every unmarked internal vertex
is safe: it still has degree two in `G`, and deleting it leaves the other two
theta paths connecting its two sides.  Therefore a counterexample has no run
of three consecutive unmarked internal vertices.  Splitting at the marks gives

`l_i-1 <= t_i+2(t_i+1)=3t_i+2`,

so

`l_i <= 3t_i+3`.

Since `t_1+t_2+t_3<=2`,

`|H|=l_1+l_2+l_3-1 <= 14`.

Consequently:

> For every bare theta graph `H` of order at least 15 and every nonedge `e`,
> `S(H+e)>|H|`.

This turns the bare-theta one-edge problem into an order-at-most-14 statement,
not an infinite weighted-theta problem.

There is also a complementary local-projector gate for the finite residue.
For `P=A(H)_+`, convexity of `M -> tr(M_+^2)` gives

`S(H+xy) >= S(H)+4P_xy`.

Hence it is enough to prove

`P_xy >= -delta(H)/4`.                                      (L)

Outside `Theta(2,2,3)`, `Theta(2,3,3)`, and `Theta(1,4,4)`, the bare theta
surplus theorem gives `delta(H)>=4/5`; thus the suspected uniform estimate
`P_xy>=-1/8` is more than sufficient, leaving surplus at least `3/10`.
The three exceptional thetas and all remaining theta orders are finite gates.

## Cycle-pair cores

Now let the bare 2-core consist of cycles `C_p,C_q` meeting at one vertex or
joined by a path.  Mark on each cycle its portal to the other cycle and every
endpoint of `e` lying on that cycle.  Every other cycle vertex is safe.  For a
cycle of length at least four, absence of a safe induced P3 says that every
cyclic run between marks has length at most two.  If `k` vertices of the cycle
are marked, this gives

`|C|<=3k`.

There are two compulsory portal marks and at most two additional edge-endpoint
marks across the two cycles.  Therefore every counterexample with both cycle
lengths at least four satisfies

`p+q<=12`.                                                   (C)

Triangles are finite exceptions to the cyclic-run argument because three
consecutive vertices induce `K3`, not `P3`.

For a dumbbell whose portals are joined by a path, project `x` and `y` onto
that connector, assigning a cycle vertex to its portal.  Every internal
connector vertex strictly between the two projections is safe: after its
deletion, the new edge reconnects the two sides.  Thus the safe-P3 lemma also
shows that a counterexample must have connector projection span at most three
edges.                                                        (D)

Notice that (D) bounds where the new edge can cross the connector, but not the
unused connector tails.  Those tails are the genuine one-parameter handcuff
residue; the weighted endpoint cannot remove them because of the exact
`C5--C5` obstruction.

## Tree attachments

The proposed argument would remain formally useful without assuming that `H`
is bare only if the missing deletion bound were supplied. On a
subdivided core link, however, every attachment-bearing vertex is an additional
mark.  If a link contains `a` such internal vertices and `t` internal endpoints
of `e`, the same count only gives

`l <= 3(a+t)+3`.

Since `a` is unbounded, this does not yield a finite weighted-core reduction.
This is a real limitation rather than missing bookkeeping: the weighted
handcuff endpoint is false, even though the corresponding unweighted graphs
can satisfy the desired inequality.

## Reduced target

Conditional on the missing attached-bicyclic deletion bound, a counterexample
would satisfy all of the following:

1. it has no safe induced `P3`;
2. if its core is theta, its bare core has order at most 14, or attachments
   mark every otherwise long core run;
3. if its core is a cycle pair, its two bare cycles satisfy the finite bound
   (C), while the edge has connector span at most three as in (D);
4. on the remaining graph/nonedge pair, the only local inequality needed for
   the tangent proof is (L).

The unresolved infinite object is therefore not a general weighted theta.  It
is the cycle-pair family with bounded cycle data, bounded edge span, and
possibly arbitrarily long unused connector or attachment tails, together with
the adaptive projector inequality (L).
