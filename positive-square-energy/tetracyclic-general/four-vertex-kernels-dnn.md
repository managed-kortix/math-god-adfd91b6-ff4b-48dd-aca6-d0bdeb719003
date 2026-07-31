# Four-vertex rank-four kernels: complete exact ledger

## Theorem

Let `B` be a simple subdivision of one of the five four-vertex kernels

`(0,1,2,1,2,1)`, `(0,1,2,2,1,1)`, `(0,1,2,2,2,0)`,
`(0,1,2,3,1,0)`, or `(1,1,1,1,1,2)`,

in edge order `01,02,03,12,13,23`. Attach arbitrary rooted trees at arbitrary
vertices. Then the resulting graph `G` satisfies

`s^+(G)>=|V(G)|`.

The exact ledger below proves this statement. It first certifies 340 of the 342
physical parity rows directly. A complete long/unit antichain then discharges
the remaining two rows by six strict planar Gram classes, a regular-simplex
class, and the established attached-`K4` structural packet.

## The physical ledger

For kernel multiplicities `m`, let `q_e` be the number of physically odd paths
in bundle `e`. Thus `0<=q_e<=m_e`. Direct Cartesian enumeration gives

| kernel | rows |
|:---|---:|
| `(0,1,2,1,2,1)` | `72` |
| `(0,1,2,2,1,1)` | `72` |
| `(0,1,2,2,2,0)` | `54` |
| `(0,1,2,3,1,0)` | `48` |
| `(1,1,1,1,1,2)` | `96` |
| total | `342` |

The old switching-orbit packet directly certifies 270 physical rows after its
Gram matrices are transported back to the original physical costs. The exact
row patch certifies 70 more rows. It consists of 42 rational planar
automorphism-orbit certificates and one exact boundary matrix; each is checked
against the physical row, never against a switched parity row. The largest
patched excess is at most three.

Exactly two rows remain after those direct certificates:

`(kernel 4, q=(1,1,1,1,1,1))`,

`(kernel 4, q=(1,1,1,1,1,2))`.

They are not silently counted as outputs of the rational planar search. They
are handled by the independent exhaustive certificate in the next section.

## Complete residual antichain

Write the last kernel as a `K4` support with a second `23` path. In both
residual rows all five singleton bundles are odd. Choose an odd `23` path for
the `K4` support and let `T` be the internal vertices of the other `23` path,
together with every rooted tree based at those vertices. The other path has an
internal vertex: in row `111111` it is even and hence has length at least two;
in row `111112` both paths are odd, but simplicity permits at most one direct
`23` edge, so one of them has odd length at least three and is chosen as the
deleted path.

The induced graph `T` is a nonempty tree, so `sigma(T)=-1`. Its induced
complement is an all-odd subdivision of `K4`, with all remaining rooted-tree
attachments retained. Induced superadditivity therefore gives exactly

`sigma(G) >= sigma(K4_all_odd_packet) + sigma(T)`

`          = sigma(K4_all_odd_packet) - 1`.

The strengthened attached all-odd `K4` estimate needed here is established by
the attached-`K4` Sachs packet:

`sigma(actual attached K4 packet)>2`.                    (1)

Thus the no-long support state has total surplus greater than `2-1=1`, and is
strictly closed. For every subdivided support state we use the following exact
monotone classification. A support path is `unit` at length one and `long` at
odd length at least three. The second distinguished `23` path is canonical
even length two in row `111111` and canonical odd length three in row `111112`.

The standalone verifier regenerates all `2*2^6=128` binary states. Equivalently,
the stabilizer of the distinguished unordered pair `23` has order four and the
128 states form exactly 56 stabilizer orbits. The complete eight-class
coordinatewise antichain is:

| class | states | disposition |
|:---|---:|:---|
| even extra, at least two long | `57` | regular-simplex DNN |
| odd extra, at least two long | `57` | regular-simplex DNN |
| even extra, one long: distinguished/opposite/adjacent | `1/1/4` | three planar Gram classes |
| odd extra, one long: distinguished/opposite/adjacent | `1/1/4` | three planar Gram classes |
| even extra, no long | `1` | actual attached `K4` packet plus tree |
| odd extra, no long | `1` | actual attached `K4` packet plus tree |

For the regular-simplex class every support unit path costs `1/2`, and every
support long path costs strictly less than `1/6`. If at least two support paths
are long, their total support cost is therefore at most `7/3`. On the extra
`23` path, the even canonical cost is `4-2sqrt(3)<3/5`, while the odd canonical
cost is strictly below `1/6`. Hence both totals are strictly below three.
Longer same-parity paths only decrease the cost.

The six one-long frontier Gram matrices are planar. With `theta_i=k_i*pi/d`,
their exact vector data are

| extra parity | long support edge | `d` | `(k_0,k_1,k_2,k_3)` |
|:---|:---|---:|:---|
| even | distinguished `23` | `5` | `(0,3,6,7)` |
| even | opposite to `23` | `5` | `(0,1,4,7)` |
| even | adjacent to `23` | `5` | `(0,3,9,6)` |
| odd | distinguished `23` | `7` | `(0,4,8,10)` |
| odd | opposite to `23` | `3` | `(0,0,2,4)` |
| odd | adjacent to `23` | `5` | `(0,4,1,7)` |

Each matrix is PSD without a numerical eigenvalue test: it is explicitly the
Gram matrix of the four planar unit vectors
`(cos(theta_i),sin(theta_i))`. The verifier evaluates every path angle from
these vectors and proves the total is strictly below three using only exact
`Fraction` arithmetic. It proves `333/106<pi<355/113` from Machin's identity
and alternating rational arctangent series, then uses 20-term alternating
Taylor bounds for sine and cosine on `[0,8/5]`; positivity of every cosine
denominator is checked before division. This is a rigorous interval proof for
the standard denominators `3,5,7`, not a decimal check.

Every state with two or more long support coordinates coordinatewise dominates
the regular-simplex `q=2` class. Every state with exactly one long coordinate
is one of the six listed frontier classes under the distinguished-`23`
stabilizer. The only two states with no long coordinate are structural and use
(1). This proves exhaustion and leaves no unclassified numerical row.

The earlier simplex discharge was invalid. For the quarter-angle convention
used by the verifier,

`r=(1-6t^2+t^4)/(1+t^2)^2`.

Thus regular-simplex correlation `r=-1/3` gives `t^2=2-sqrt(3)`, not `1/3`;
indeed `t^2=1/3` gives `r=-1/2`. The claimed costs `1/3` and `2/3`, and hence
the budgets `8/3` and `7/3`, do not follow from a regular-simplex Gram matrix.

## Fail-closed audit

`research/rank-four-four-vertex-theorem-verifier.py` imports the original base
audit and the exact row patch, independently reconstructs all 342 physical
rows, and checks the disjoint status ledger

`342 = 270 base + 70 patch + 2 independently discharged`.

For the old two-row frontier it enumerates all 128 binary states and all 56
stabilizer orbits, verifies the six exact planar classes and the simplex class,
and checks the two structural no-long states. Eight hostile mutations are
rejected, including deletion of the distinguished-`23` class, duplication,
wrong parity or relation, malformed angle data, and a false high-cost witness.
Run

```text
python research/rank-four-four-vertex-theorem-verifier.py
python -O research/rank-four-four-vertex-theorem-verifier.py
```

Both commands exit zero with byte-identical output. Python `assert` is not used
for any acceptance condition; normal and optimized execution therefore apply
the same fail-closed checks.
