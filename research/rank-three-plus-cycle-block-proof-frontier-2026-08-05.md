# Rank-three block plus one cycle: block-additive proof and frontier

**Date:** 2026-08-05

## Result

Let `G` be a finite simple connected graph whose positive-rank cyclic blocks
are one rank-three 2-connected block `B` and one cycle `Q=C_q`. The two blocks
may share a cut vertex or be joined through arbitrary bridge blocks, and
arbitrary finite rooted trees may be attached at arbitrary vertices. Then

```text
s+(G) >= |V(G)|.
```

Thus the complete block-rank `3+1` part of the tetracyclic problem is closed.
There is no remaining graph family in this block partition. What remains open
inside this argument is only the classification of equality: several DNN
certificates meet an auxiliary boundary, so this note does not assert a global
strict inequality.

## 1. Why the tricyclic theorem alone is insufficient

Write

```text
sigma(H)=s+(H)-|V(H)|.
```

The tricyclic theorem gives only `sigma(B)>=0` uniformly over subdivisions and
rooted trees. A hostile cycle `C_q`, `q=1 mod 4`, can have negative credit; in
particular

```text
sigma(C5)=2-sqrt(5)<0.
```

Consequently the formal ledger `sigma(B)+sigma(C5)` does not close the case.
Nor may a bridge cut manufacture a positive margin in `B`: the weak
tricyclic conclusion has no reserve with which to pay the pentagon. The proof
must retain the quantitative DNN excess of the rank-three block, except in a
small set of structural packets.

## 2. The block-additive DNN budget

For an edge-containing graph `H`, let `kappa(H)` be the optimized LTZ/DNN
constant. We use

```text
s-(H) <= kappa(H),
kappa(H1 vee_z H2)=kappa(H1)+kappa(H2),
kappa(T)=|E(T)| for every tree T.
```

If a suppressed kernel edge is replaced by a path of length `l` and its
endpoint correlation is `r`, exact path elimination assigns the excess

```text
f_l(r)=l tan^2(acos((-1)^l r)/(2l)).
```

For fixed endpoint correlation and parity, `f_(l+2)(r)<=f_l(r)`, strictly
away from the zero-angle case. Hence finite physical parity certificates at
the first simple lengths cover all subdivisions.

Let `B` have `L` edges and let a correlation certificate give path excess
`e_B`, so that

```text
kappa(B) <= L+e_B.
```

Since `B` has rank three, `|V(B)|=L-2`. For the cycle put

```text
kappa(C_q)=q+epsilon_q,
epsilon_q=0                                      if q is even,
epsilon_q=q tan^2(pi/(2q))                       if q is odd.
```

Let all bridge blocks and rooted-tree edges outside `B` and `Q` total `t`.
Block additivity gives

```text
kappa(G) <= L+q+t+e_B+epsilon_q.
```

The entire graph has

```text
|E(G)|=L+q+t,             |V(G)|=L+q+t-3.
```

Therefore

```text
e_B+epsilon_q <= 3                                      (DNN gate)
```

implies

```text
s+(G)=2|E(G)|-s-(G)
     >=2|E(G)|-kappa(G)
     >=|V(G)|.
```

This is the useful extra unit: the tricyclic block by itself has excess budget
two, while the full rank-`3+1` graph has budget three. Connector location and
tree shape disappear exactly, not approximately, by one-vertex additivity.

For odd cycles, `epsilon_3=1`; the sequence decreases through odd lengths;
and for every hostile `q=1 mod 4`, necessarily `q>=5`,

```text
epsilon_q <= epsilon_5=5-2sqrt(5)<3/5.
```

## 3. Exhaustive rank-three sieve

Suppress maximal degree-two paths inside `B`. The resulting loopless
2-connected rank-three multigraph is exactly one of:

1. four parallel edges between two branch vertices;
2. a triangle with two adjacent sides doubled;
3. a four-cycle with two opposite sides doubled;
4. `K4`.

The complete tricyclic physical ledgers and fixed-parity monotonicity give the
following exhaustive sieve. A long path means a nonunit path in the all-odd
`K4` switching class.

| rank-three kernel/state | certified `e_B` | disposition with one cycle |
|---|---:|---|
| four-path kernel, every simple row | `<=2` | DNN gate except favorable structural boundary handled below |
| doubled triangle outside class `111` | `<=2` | DNN gate |
| doubled triangle class `111`, a parallel path noncanonical | `<229/120` or `<31/20` | DNN gate |
| doubled triangle class `111`, canonical pairs | `<221/100` | DNN gate for even/hostile cycles; favorable packet if needed |
| doubled `C4` outside class `111` | `<=2` | DNN gate |
| doubled `C4` class `111`, a doubled path noncanonical | `<1862/1000` or `<1662/1000` | DNN gate |
| doubled `C4` class `111`, canonical pairs | `<9/4` | DNN gate for even/hostile cycles; favorable packet if needed |
| `K4`, non-all-odd | `<5/3` | DNN gate |
| all-odd `K4`, at least three long paths | `<=2` | DNN gate |
| all-odd `K4`, two opposite long paths | `<=24-16sqrt(2)<2` | DNN gate |
| all-odd `K4`, two adjacent long paths | `<71/40` | DNN gate |
| all-odd `K4`, one long path | `<12/5` | DNN gate for even/hostile cycles; favorable packet if needed |
| unsubdivided `K4` | exact DNN excess `3` | even cycle by DNN; every odd cycle by induced packet |

The row counts behind this table are also exhaustive: `28` DNN rows and four
canonical structural rows for the doubled triangle; `28` DNN rows and eight
canonical structural rows for doubled `C4`; and `56` non-all-odd physical
rows plus the long/unit subsets of the all-odd `K4` class. Parallel paths are
never both assigned physical length one; switching labels organize rows but do
not alter their physical lengths.

## 4. Hostile cycles are absorbed quantitatively

Assume `q=1 mod 4`. Every ordinary DNN row has `e_B<=2`, and hence

```text
e_B+epsilon_q < 2+3/5 < 3.
```

The canonical rows that exceeded the old tricyclic budget have dedicated
planar Gram certificates:

```text
doubled triangle: e_B < 221/100,   e_B+epsilon_q < 281/100;
doubled C4:       e_B < 9/4,       e_B+epsilon_q < 57/20;
one-long K4:      e_B < 12/5,      e_B+epsilon_q < 3.
```

The last inequality is strict because both displayed constituent bounds are
strict. Thus even a hostile `C5` is absorbed in every one of these rows.

For the unsubdivided `K4`, the simplex DNN optimum has excess exactly three
and leaves no hostile reserve. Use induced territories instead. An attached
`K4` packet has `sigma>2`, by the grouped Sachs expansion: its triangle terms
put the normalized characteristic polynomial strictly in the lower
half-plane, while its four-cycle terms are real.

If an actual bridge separates `K4` from `Q`, cut it and assign the complete
connector to one side. The attached odd-unicyclic cycle packet satisfies

```text
sigma(Q packet) >= -(sec(pi/q)-1),
```

and `sec(pi/q)-1<1`; hence the two induced territories have total credit
strictly greater than one. If the blocks share a cut vertex `z`, give `z`, the
whole `K4`, and its rooted side to the first territory. Give `Q-z` and every
branch on that side to the second. The latter is one nonempty tree of credit
`-1`, so the total is `>2-1>0`. Every cut and attached branch has exactly one
owner.

This closes all hostile lengths, including `C5`. It is the key improvement
over attempting to add the weak tricyclic theorem to a negative cycle credit.

## 5. Even and favorable cycles

If `q` is even, `epsilon_q=0`. Every table row passes the DNN gate, including
the unsubdivided `K4` at its boundary `e_B=3`.

Now suppose `q=3 mod 4`. Whenever the displayed DNN gate passes, nothing more
is needed. In the remaining canonical structural rows, use the opening already
present in the tricyclic proof:

- open its designated internal path vertex in the canonical doubled-triangle
  or doubled-`C4` row;
- open an internal vertex of the unique long path in the one-long all-odd
  `K4` row;
- for the unsubdivided `K4`, retain the whole attached `K4` packet.

The opened vertex owns every component whose unique block-cut route first
meets `B` there; every rooted branch follows its root. If the opened territory
owns `Q`, it is a favorable unicyclic packet of positive credit, while the
complementary bicyclic packet has credit greater than one. If it does not own
`Q`, it is a nonempty tree of credit `-1`. The complement then contains three
favorable cycles. When their packing number is at most two, the grouped Sachs
half-plane theorem gives positive spectral asymmetry, hence tricyclic credit
greater than two. When their packing number is three, actual bridges separate
them into attached bicyclic and unicyclic favorable packets of credits greater
than one and greater than zero. These credits pay the opened tree strictly.

For the unsubdivided `K4`, a separating route leaves a favorable unicyclic
territory; at a shared cut `z`, the other territory is the tree `Q-z`. The
attached `K4` credit `>2` pays it. Thus every favorable-cycle incidence and
every connector length is covered.

## 6. Proof conclusion

The kernel classification is exhaustive. The sieve covers every physical
parity row and, by exact path monotonicity, every path length. The DNN gate
closes all direct rows and all hostile-cycle residual rows. The induced
openings close precisely the favorable structural rows and the unsubdivided
`K4` hostile boundary. One-vertex DNN additivity or explicit branch ownership
includes every bridge connector and every rooted tree. Therefore every graph
in the rank-`3+1` block partition satisfies `s+(G)>=|V(G)|`.

## 7. Frontier and audit boundary

**Closed:** arbitrary rank-three 2-connected block, arbitrary cycle length,
shared-cut or bridge-separated incidence, arbitrary connector trees, and
arbitrary rooted attachments.

**Not claimed:** strictness in every row, classification of equality, or a
proof that the DNN inequality is spectrally sharp when its excess equals three.

**Finite proof dependencies:** the rank-three physical Gram ledgers, their
exact rational inequalities, and the kernel switching censuses are imported
from `all-tricyclic-graphs/paper.tex` and its checked proof objects. The full
assembled argument appears in the `3+1` part of
`all-tetracyclic-graphs/paper.tex`. The exact verifiers audit the finite
certificate payloads; they do not machine-prove DNN duality, path monotonicity,
the kernel classification, Sachs/Coulson phase arguments, or induced
superadditivity.

No edge-addition monotonicity, numerical SDP evidence, switching of physical
path lengths, or unquantified tricyclic margin is used.
