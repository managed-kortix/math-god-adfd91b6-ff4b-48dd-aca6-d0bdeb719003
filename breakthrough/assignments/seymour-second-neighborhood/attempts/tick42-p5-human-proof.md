# Tick 42: human elimination of the five-vertex path hole shape

Suppose the four T-holes form the path

```
01, 12, 23, 34.
```

As before, the shape-independent B-row count gives `|P|>=4`. For each source,
the inaccessible-capacity argument shows that exactly two path vertices are
inaccessible. For a set J of three inaccessible vertices, the present pairs
inside J consume at least `3-e_h(J)` outgoing slots, while the available slots
are the number of crossing holes minus three. This would require at least six
holes when internal and crossing holes are combined, but the path has four.

The exact surviving inaccessible-pair labels are

```
02, 03, 12, 13, 14, 23, 24.                       (1)
```

Pairs 01 and 34 leave an endpoint without a crossing hole; pair 04 has two
saturated endpoints joined by a present pair.

Orient the six present pairs on the path support by Boolean variables

```
A=[0->2], B=[0->3], C=[0->4],
D=[1->3], E=[1->4], F=[2->4].
```

Exact degree-eight rows give the following necessary and sufficient conditions
for each packet label:

```
02: !A and B and (C=F)
03: A and !B and C and !D
12: !A and D and (E=F)
13: (!B and (D or E)) or (B and !D and E)
14: !C and D and E and !F
23: !D and F and (A=B)
24: !E and F and (A=C).                             (2)
```

For example, in packet 02, path vertices 1 and 3 lie in S. Vertex 0 is
saturated, forcing `2->0` and `0->3`; vertex 4 lies in both inaccessible rows
or neither, giving `C=F`. The equality clauses in 12, 23, and 24 have the same
origin. Packet 13 has three possible support intersections `{0,2}`, `{2,4}`,
and `{0,2,4}`; resolving the orientation of its present internal pair gives
exactly the disjunction displayed in (2).

Every label supports at most one source. Except for 13, a saturated inaccessible
row reconstructs S immediately. For 13, the global values of B,D,E identify
which of the three support intersections occurs; the tail of the oriented pair
13 is saturated and reconstructs the remaining seven vertices of S. A fixed S
cannot support two sources without a digon.

Finally, no assignment to the six orientation bits satisfies three conditions
in (2). This is a transparent 64-case Boolean check, implemented independently
in `experiments/check_p5_packets.py`. Equivalently, splitting on `(D,F)` and
substituting the remaining four bits leaves only compatible pairs and no
triple. The check prints

```
PASS assignments=64 maximum=2
```

Therefore at most two packet labels, and hence at most two predecessor sources,
coexist:

```
|P|<=2<4,
```

a contradiction. The P5 hole shape is impossible uniformly in rho. This is a
restricted shape elimination, not an order-18 result or SNC proof.
