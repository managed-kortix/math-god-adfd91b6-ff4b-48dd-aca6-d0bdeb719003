# R21 literal-cycle typing certificate

Date: 2026-11-14. Status: **NONPROMOTIONAL / narrow fail-closed typing gate**.

## What this certificate does—and does not do

This artifact types only an adjacency-authenticated rank-seven `R21` profile.
Its input graph must be finite, connected, undirected, and simple. Tarjan
edge-block decomposition must recover exactly one positive-rank block that is
literally `D=Theta(1,2,2)=K4-e` and exactly five positive-rank blocks that are
literal simple cycles. Four of the cycle blocks must be literal `C3` blocks;
the fifth is a literal `C_q`. Rank-zero bridge blocks and one-root acyclic
attachments may be present, but no declared block label is evidence for a
physical type.

The exact DNN closure budget for this six-block rank-seven profile is six:

```text
Delta(D) + 4 epsilon(C3) + epsilon(C_q) <= 6.                 (1)
```

Equality in (1) is closed. Therefore the **DNN-open** predicate is the strict
complement

```text
Delta(D) + 4 epsilon(C3) + epsilon(C_q) > 6.                  (2)
```

The companion verifier accepts neither `>= 6` nor any other budget. It also
checks the equivalent debit data: six positive-rank blocks, debit allowance
`k-1=5`, and rank partition `2+1+1+1+1+1`.

This certificate does not prove an R21 packet, a bridge dispatch, a territory
partition, or the rank-seven theorem. It does not promote a symbolic residual
registry to a physical row. In particular, the token `D+T^4+P` in the
rank-seven ledger is only a symbolic registry entry. The conclusion `P=C5`
below is available only after the input adjacency has passed the literal block
gate and the strict predicate (2).

## Exact classification

Put

```text
d = Delta(1,2,2) = (sqrt(17)-1)/2,
epsilon_3 = 1,
epsilon_5 = 5-2sqrt(5).
```

The left side of (2) is `d+4+epsilon_q`.

### `q=3` is retained, but it is the other R21 family

Here every one of the five cycle blocks is a literal triangle. Moreover

```text
d+5-6 = (sqrt(17)-3)/2 > 0
```

because `17>9`. Thus `q=3` is DNN-open. It is typed as `D+T^5`, a member of the
`Theta(1,2,r)+T^5` family with `r=2`; it is not silently discarded and is not
renamed `D+T^4+P`.

### `q=5` survives

For a literal `C5`,

```text
d+4+epsilon_5-6 = (sqrt(17)+5-4sqrt(5))/2.
```

Both sides of `sqrt(17)+5 > 4sqrt(5)` are positive. After squaring, the
inequality is `10sqrt(17)>38`, or `sqrt(17)>19/5`; squaring again is valid and
gives the integer check `425>361`. Hence the margin is strictly positive and
the adjacency-authenticated row is `D+T^4+P(C5)`.

The source manuscript's final theta-cycle paragraph writes
`sqrt(17)+7>4sqrt(5)`. That sentence is not used here: it is not the algebraic
reduction of the displayed threshold. The verifier instead checks the exact
source identities for `d` and `epsilon_5` and performs the correct `+5`
integer proof above.

### Every `q>=4`, `q!=5`, is DNN-closed

If `q` is even, `epsilon_q=0` and

```text
d+4-6 = (sqrt(17)-5)/2 < 0
```

because `17<25`.

If `q>=7` is odd, the pinned source gives `epsilon_q<2/5`. Also

```text
d < 8/5
```

because this is equivalent to `sqrt(17)<21/5`, whose squared integer check is
`425<441`. Consequently

```text
d+4+epsilon_q < 8/5+4+2/5 = 6.
```

These two parity classes exhaust all `q>=4` other than five. They fail the
strict DNN-open predicate; they are accepted as literal physical profiles but
classified as DNN-closed, not rejected as malformed graphs.

## Provenance and physical authentication

The verifier pins full byte length, SHA-256, Git-blob SHA-1, and uniquely
occurring semantic tokens for:

1. `all-tricyclic-graphs/paper.tex`: literal block alternatives, definitions
   of `Delta` and `epsilon`, the exact value of `Delta(1,2,2)`, odd-cycle
   monotonicity, the exact `C3/C5` values, the `<2/5` tail, and even-cycle zero;
2. `positive-square-energy/heptacyclic-general/
   rank-seven-multiblock-debit-ledger.md`: the rank-seven debit identity,
   six-block budget, exact `R21` predicate, symbolic residual line, and the
   rule that equality is closed; and
3. `positive-square-energy/hexacyclic-general/
   multiblock-items1-7-combined-theorem-audit.md`: the historical notation
   `T=C3`, `P=C5`, `D=Theta(1,2,2)` and cycle bounds. This third source is a
   notation receipt only, never a substitute for adjacency authentication.

For a submitted certificate, the verifier ignores names such as `T`, `P`, and
`D` until it has reconstructed maximal edge blocks from the graph itself. It
then requires:

* one rank-two block with four vertices, five edges, degree multiset
  `(2,2,3,3)`, adjacent degree-three branch vertices, and two degree-two
  vertices each adjacent to both branches;
* five rank-one blocks, each with `|E|=|V|>=3` and internal degree two at every
  vertex; and
* cycle lengths either `(3,3,3,3,3)` or `(3,3,3,3,q)` with `q>=4`.

Thus subdividing a required `T`, subdividing `D`, adding a chord to the alleged
`C_q`, supplying only symbolic labels, changing the claimed family, changing
source bytes/tokens, or changing strict `>6` to non-strict `>=6` fails closed.
The executable carries explicit hostile mutations for each of these cases,
authenticates a permitted one-root tree fixture, rejects an extra cyclic block
hidden behind a bridge route, and compares its normal and `python -O` reports
byte for byte.

## Scope blockers

* This is a type theorem conditional on the pinned DNN inputs, not a new
  derivation of the elliptope/path formula.
* No symbolic `P` occurrence authenticates a physical pentagon.
* No claim is made for a subdivided theta, a non-cycle rank-one declaration,
  a different block inventory, or a non-strict residual predicate.
* No `STATE`, theorem-master, publication, or lane-control file is changed.
