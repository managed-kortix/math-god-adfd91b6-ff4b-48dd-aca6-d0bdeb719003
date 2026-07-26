# Exact rank-ten cactus frontier census

**Date:** 2026-07-26

## Status and scope

This note re-derives the sharp-DNN rank-ten frontier and records an exact
finite census of its colored shared-cut cluster partitions and fully shared
incidence trees. The companion certificate is

```bash
python3 research/rank-ten-cactus-frontier-census.py
python3 -O research/rank-ten-cactus-frontier-census.py
```

Both invocations end with the same `PASS` line. The program uses exact
`fractions.Fraction` ledger arithmetic and explicit fail-closed checks; no
verification condition is implemented with `assert`, so `python -O` cannot
disable it.

This is a frontier census, not a rank-ten cactus theorem. `SAFE` below means
that the entered lower-rank packet ledger certifies an ordinary one-cycle
split of the abstract incidence tree. Structural partition rows and fully
shared exceptions still require graph-level routing, ownership, realization,
and analytic closure.

## 1. Sharp-DNN residuals

For a rank-`r` cactus with cycle lengths `l_i`, the sharp DNN estimate is

```text
sigma(G) >= r-1-sum_i epsilon_(l_i),
epsilon_l = 0                         for even l,
epsilon_l = l tan^2(pi/(2l))          for odd l.
```

Let `T=C3`, `P=C5`, and let `Q` denote an arbitrary cycle. The exact all-rank
classification already proved in the rank-nine residual note uses

```text
epsilon_3=1,
a=epsilon_5=5-2sqrt(5),
3a<2,  2a>1,  epsilon_5+epsilon_7<1.
```

If `k` cycles are nontriangles, then

```text
sum epsilon_i <= (r-k)+ka.
```

Nonpositive DNN margin forces `k(1-a)<=1`, hence `k<=2`. For `k=2`, exact
monotonicity and `epsilon_5+epsilon_7<1<2epsilon_5` leave only two pentagons.
At `r=10`, the complete residual list is therefore

```text
T^9Q,   q>=3, including Q=T,
T^8PP.
```

Conversely their DNN margins are `-epsilon_q<=0` and
`1-2epsilon_5=4sqrt(5)-9<0`, respectively, so both families genuinely remain
on the DNN frontier.

## 2. Exact colored cluster partitions

A colored cluster type is a pair `(t,d)`, where `t` is its triangle count and
`d` is its number of distinguished cycles: `Q` for `T^9Q`, or pentagons for
`T^8PP`. A partition is an unordered nondecreasing tuple of nonzero types.
The one-part partition is the fully shared case; every proper partition is a
disconnected shared-cut cluster pattern.

The packet ledger is the rank-nine continuation:

```text
A_t:   >0,>1,>2,>3,>2,>1,>0,>0,>0 for t=1,...,9;
Q:     >=-1;  TQ>0;  TTQ>=0;  higher mixed lower ranks >0;
P:     >=-1/4; TP>3/4; PP>0; TPP>3/2;
generic mixed ranks 2 or 3 >=0; established higher lower ranks >0.
```

All additions and strict/non-strict comparisons are exact. The census is:

| residual | all partitions | proper | direct | structural |
|---|---:|---:|---:|---:|
| `T^9Q` | 97 | 96 | 92 | 4 |
| `T^8PP` | 181 | 180 | 170 | 10 |

Writing `T=(1,0)`, `Q=(0,1)` in the first family and `P=(0,1)` in the second,
the four `T^9Q` structural rows are

```text
Q|T|T|T|T|T|T|T|T|T
Q|T|T|T^7
Q|T|T^8
Q|T^9
```

The ten `T^8PP` structural rows are

```text
P|P|T|T|T|T|T|T|T|T
P|P|T|T^7
P|P|T^8
P|T|T|T|T|T|T|T^2P
P|T|T|T|T|T|T^3P
P|T|T|T|T|T^4P
P|T|T|T|T^5P
P|T|T|T^6P
P|T|T^7P
P|T^8P
```

These are ledger residuals, not ten asserted graph obstructions. Reduced-tree
pruning may identify or close endpoint families only after actual bridge
connectors and territory ownership are restored.

## 3. Fully shared `T^9Q`

The objects are color-preserving bipartite trees with ten cycle nodes and
uncolored cut nodes. Every cut has degree at least two; cycle capacities are
`deg(T)<=3` and `deg(Q)<=q`. Exhaustive cycle-leaf insertion is quotiented by
a center-rooted colored-tree code. Since `Q` can meet at most the other nine
cycles, structural counts stabilize at capacity nine.

Counts by number `c` of cut nodes are:

| `Q` capacity | `c=1` | `c=2` | `c=3` | `c=4` | `c=5` | `c=6` | `c=7` | `c=8` | `c=9` | total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 1 | 12 | 91 | 406 | 1178 | 2115 | 2250 | 1246 | 275 | 7574 |
| 4 | 1 | 12 | 91 | 412 | 1203 | 2187 | 2361 | 1340 | 306 | 7913 |
| 5 | 1 | 12 | 91 | 412 | 1208 | 2201 | 2393 | 1372 | 321 | 8011 |
| 6 | 1 | 12 | 91 | 412 | 1208 | 2204 | 2400 | 1383 | 327 | 8038 |
| 7 | 1 | 12 | 91 | 412 | 1208 | 2204 | 2402 | 1386 | 330 | 8046 |
| 8 | 1 | 12 | 91 | 412 | 1208 | 2204 | 2402 | 1387 | 331 | 8048 |
| `>=9` | 1 | 12 | 91 | 412 | 1208 | 2204 | 2402 | 1387 | 332 | 8049 |

For `Q=T` or the entered nonhostile-cycle ledger, every type except the one-cut
common bouquet is SAFE. Under the conservative hostile ledger,
the exact SAFE counts are:

| capacity regime | all | SAFE | exceptions by `c` |
|---|---:|---:|---|
| `q=3` | 7574 | 7573 | `1` at `c=1` |
| `q=4` | 7913 | 7912 | `1` at `c=1` |
| `q=5` | 8011 | 8008 | `1,1,1` at `c=1,2,3` |
| `q=6` | 8038 | 8037 | `1` at `c=1` |
| conservative capacity 7 (`q=7` is nonhostile) | 8046 | 8043 | `1,1,1` at `c=1,2,3` |
| `q=8` | 8048 | 8047 | `1` at `c=1` |
| saturated hostile ledger | 8049 | 8046 | `1,1,1` at `c=1,2,3` |

Actual hostility means `q=1 mod 4`. The saturated hostile row is a conservative
ledger regime on the stabilized capacity-nine universe and covers every actual
hostile `q>=9`; an even or `3 mod 4` cycle uses the stronger nonhostile ledger
and leaves only the common bouquet.

The three hostile exception signatures are

```text
c=1  X(Q()T()T()T()T()T()T()T()T()T())
c=2  T(X(Q())X(T()T()T()T()T()T()T()T()))
c=3  T(X(Q())X(T())X(T()T()T()T()T()T()T()))
```

They form the common hub followed by zero, one, or two short saturated
triangle-router refinements. No hostile-ledger exception occurs at `c>=4`.

## 4. Fully shared `T^8PP`

The complete color-preserving census is

| | `c=1` | `c=2` | `c=3` | `c=4` | `c=5` | `c=6` | `c=7` | `c=8` | `c=9` | total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 1 | 19 | 204 | 1155 | 3990 | 8135 | 9615 | 5843 | 1424 | 30386 |
| SAFE | 0 | 17 | 200 | 1154 | 3989 | 8135 | 9615 | 5843 | 1424 | 30377 |
| exceptions | 1 | 2 | 4 | 1 | 1 | 0 | 0 | 0 | 0 | 9 |

Thus the ordinary-split decomposition is exactly

```text
30386 = 30377 + 9.
```

The nine frozen canonical signatures are

```text
c=1  X(P()P()T()T()T()T()T()T()T()T())
c=2  P(X(P())X(T()T()T()T()T()T()T()T()))
c=2  T(X(P())X(P()T()T()T()T()T()T()T()))
c=3  P(X(P())X(T())X(T()T()T()T()T()T()T()))
c=3  T(X(P())X(P())X(T()T()T()T()T()T()T()))
c=3  T(X(P())X(P()T()T()T()T()T()T())X(T()))
c=3  X(T()T()T()T()T()T()T(X(P()))T(X(P())))
c=4  X(T()T()T()T()T()T(X(P()))T(X(P())X(T())))
c=5  X(T()T()T()T()T(X(P())X(T()))T(X(P())X(T())))
```

The first six include the common-cut bouquet, pentagon-router, and short
hub/router variants. The final three continue the symmetric two-arm ladder.
There are no ordinary-split exceptions with six or more cut nodes.

## 5. Exactness and fail-closed boundary

The certificate independently validates every generated representative:

1. unique canonical signature and exact requested color multiset;
2. connected bipartite tree structure and `|E|=|V|-1`;
3. cut degree at least two and every cycle capacity;
4. exact cut-count totals and SAFE/unresolved exhaustion;
5. all frozen partition totals, incidence totals, exception cut counts, and
   complete exception-signature sets; and
6. rank-nine generation regressions for `T^8Q` and `T^7PP`.

Any mismatch raises `RuntimeError`; checks remain live under optimization. The
program imports the established leaf-extension generator but does not call its
assert-based census driver. Its own validation and frozen outputs are the
authoritative checks for this artifact.

What is not certified is equally important. The program does not enumerate
cyclic mark order, off-core trees, bridge lengths, connector entries, induced
territory ownership, sequential router replacements, or analytic packet
proofs. It establishes the exact rank-ten finite frontier to be attacked; it
does not claim that the `4+10` structural cluster rows or the `3+9` fully
shared hostile exceptions are already closed.
