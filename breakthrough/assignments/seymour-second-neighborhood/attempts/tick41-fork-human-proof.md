# Tick 41: human elimination of the fork hole shape

Use the isolated-root `m=9,k=4` normal form. The shape-independent argument of
tick 38 gives at least four A' predecessor sources of the common C-dominators:

```
|P|>=4.                                             (1)
```

Suppose the four T-holes are

```
01, 02, 03, 14.
```

For a source a, put `S={a} union N_T+(a)`. At least two vertices outside S are
inaccessible by a T-two-walk. If inaccessible t has q(t) holes into S, then its
`9-q(t)` present pairs into S all point outward from t. Thus `q(t)>=1`, and
exact outdegree leaves only `q(t)-1` outgoing slots outside S.

No inaccessible triple exists. Every triple except 123 and 234 contains a
vertex with no hole into the complementary fork vertices. In 123, vertices 2
and 3 each have one crossing hole but their present pair needs an outgoing
endpoint; 234 is the same saturated obstruction. Hence exactly two vertices
are inaccessible.

The complete feasible packet table is

```
packet   possible S intersect {0,1,2,3,4}
P01      {2,4}, {3,4}, {2,3,4}
P04      {1,2}, {1,3}, {1,2,3}
P12      {0,4}, {0,3,4}
P13      {0,4}, {0,2,4}.
```

All other pairs either leave an endpoint with no crossing hole or give two
saturated endpoints joined by a present pair. Each packet reconstructs S from
a saturated global row:

```
P01: S=N+(1) union {4},
P04: S=N+(4) union {1},
P12: S=N+(2) union {0},
P13: S=N+(3) union {0}.                           (2)
```

Thus each packet supports at most one source, since one closed outneighborhood
cannot have two sources without a digon.

The membership-sensitive forced orientations are:

```
P01: 1->2 iff 2 in S; 1->3 iff 3 in S;
     at least one of 2,3 lies in S.
P04: 4->2 iff 2 in S; 4->3 iff 3 in S;
     at least one of 2,3 lies in S.
P12: 1->2 and 2->4.
P13: 1->3 and 3->4.                               (3)
```

All four packet types cannot coexist. P12 and P13 force `1->2` and `1->3`, so
the P01 equivalences force both 2 and 3 into its S. More decisively, P12 forces
`2->4` and P13 forces `3->4`. The P04 equivalences then force both 2 and 3
outside its S, contradicting the requirement that at least one lies inside.
Therefore at most three packet types, hence at most three sources, coexist:

```
|P|<=3.                                             (4)
```

This contradicts (1). The fork hole shape is impossible uniformly in rho.
This is a restricted shape elimination, not an order-18 result or SNC proof.
