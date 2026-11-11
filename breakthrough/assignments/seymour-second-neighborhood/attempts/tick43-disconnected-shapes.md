# Tick 43: elimination of the three disconnected four-hole shapes

This closes the remaining `m=9,k=4` hole shapes. Throughout, the
shape-independent B-row argument of tick 38 gives at least four A' predecessor
sources of common C-dominators:

```
|P|>=4.                                             (1)
```

For a source a, put `S={a} union N_T+(a)`. Badness supplies at least two
vertices inaccessible by a T-two-walk. If inaccessible t has q(t) holes into
S, then all `9-q(t)` present pairs into S point outward from t, leaving exactly
`q(t)-1` outgoing slots outside S. For an inaccessible set J this implies

```
C(|J|,2)-e_h(J) <= sum_{t in J}(q(t)-1).           (2)
```

For three vertices, (2) would require at least six internal-or-crossing holes,
but only four exist. Thus every source has exactly two inaccessible vertices.

The finite support calculation below is independently reproduced by
`experiments/check_disconnected_packets.py`. It enumerates every orientation of
present support pairs, every inaccessible pair I, and every support cut
`R=S intersect H`; it imposes all forced positive arcs and the at-most remaining
support capacity. Every vertex outside H is hole-isolated. Such a vertex cannot
lie outside S while inaccessible, and all non-inaccessible support-isolated
vertices are determined by the source row; equivalently the saturated support
calculation has cut multiplicity one. Thus the unique R together with the fixed
global rows reconstructs S. Hence each label supports at most one source.

## `P4 + K2`

Let the holes be `01,12,23,45`. Exactly seven packet labels survive:

```
02, 12, 13, 14, 15, 24, 25.
```

On the eleven present support pairs, write

```
A=02 B=03 C=04 D=05 E=13 F=14 G=15 H=24 I=25 J=34 K=35,
```

where a bit is one when the smaller endpoint points to the larger. Exact
saturation gives

```
02: !A & B & (C=H) & (D=I)
12: !A & E & (F=H) & (G=I)
13: !B & E & (F=J) & (G=K)
14: !C & F & G & !H & (E!=J)
15: !D & F & G & !I & (E!=K)
24: !F & H & I & !J & (A=C)
25: !G & H & I & !K & (A=D).                       (3)
```

The compatibility graph of (3) has maximum cliques

```
{02,14,15}, {13,24,25},
```

and no four labels coexist. Thus `|P|<=3`, contradicting (1).

## `2P3`

Let the holes be `01,12,34,45`. Exactly five labels survive:

```
04, 13, 14, 15, 24.
```

The exact support-cut census checks all `2^11=2048` orientations. The four
noncentral labels `04,13,15,24` are pairwise incompatible; central label 14 may
coexist with one of them but, because the global orientation selects a unique
support cut, supports only one source. Therefore at most two labels and sources
coexist:

```
|P|<=2.                                             (4)
```

The bound is sharp at packet level but contradicts (1).

## `P3 + 2K2`

Let the holes be `01,12,34,56`. The only packets are

```
P13, P14, P15, P16.
```

For `x in {3,4,5,6}`, with matching-hole mate `x*`, packet P1x forces

```
0,2,x* in S,
N+(x)=S\{x*},
N+(1)=(S\{0,2}) union {x}.                        (5)
```

Thus each packet reconstructs S. If P1x and P1y coexist and xy is present,
equation (5) forces both `x->y` and `y->x`. Hence compatibility occurs only
along holes 34 or 56. The packet graph is two disjoint edges, so

```
|P|<=2,                                             (6)
```

again contradicting (1). This explains the tick-35 local breaker: one sharp
packet exists, but comparison of its complete saturated row across sources
prevents four predecessor classes.

Therefore all three disconnected residual four-hole shapes are impossible
uniformly in rho. Together with the written proofs in ticks 30 and 38--42, this
leaves only the two star-like profiles, which are proved separately in tick 44.
