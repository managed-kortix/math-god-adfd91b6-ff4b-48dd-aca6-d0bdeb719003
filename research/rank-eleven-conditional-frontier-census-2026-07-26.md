# Conditional rank-eleven cactus frontier census

**Date:** 2026-07-26

## Status

This is next-target research only. It assumes, as a conditional packet input,
the rank-ten cactus conclusion for connected induced territories of rank at
most ten. It makes no rank-eleven theorem claim and does not certify global
bridge ownership, router replacement, or analytic closure.

The fail-closed companion program is

```bash
python3 research/rank-eleven-conditional-frontier-census.py
python3 -O research/rank-eleven-conditional-frontier-census.py
```

It uses exact `Fraction` ledgers and explicit `RuntimeError` guards rather than
`assert`. The frozen census is therefore still checked under `python -O`.

## 1. Sharp-DNN residuals

For rank `r`, the sharp cactus DNN estimate is

```text
sigma(G) >= r-1-sum_i epsilon_(l_i),
epsilon_l = 0                         for even l,
epsilon_l = l tan^2(pi/(2l))          for odd l.
```

Put `T=C3`, `P=C5`, and let `Q` be any cycle. The established exact DNN
classification uses

```text
epsilon_3=1,
a=epsilon_5=5-2sqrt(5),
3a<2, 2a>1, epsilon_5+epsilon_7<1.
```

If `k` cycles are nontriangles, then
`sum epsilon_i <= (r-k)+ka`. A nonpositive DNN margin forces
`k(1-a)<=1`, hence `k<=2`; for `k=2`, only two pentagons remain. Thus at
rank eleven the complete sharp-DNN residual list is

```text
T^10Q,  q>=3, including Q=T,
T^9PP.
```

Their margins are respectively `-epsilon_q<=0` and
`1-2epsilon_5=4sqrt(5)-9<0`, so both genuinely lie beyond DNN alone. This
derivation does not use the conditional rank-ten input.

## 2. Conditional colored partitions

The partition ledger continues the rank-ten ledger and conditionally enters
every connected rank-ten packet as strict positive. In particular `A_10>0` is
conditional. The exact audit is

| residual | all partitions | proper | direct | structural |
|---|---:|---:|---:|---:|
| `T^10Q` | 139 | 138 | 133 | 5 |
| `T^9PP` | 267 | 266 | 253 | 13 |

The five `T^10Q` structural rows are

```text
Q|T|T|T|T|T|T|T|T|T|T
Q|T|T|T|T^7
Q|T|T|T^8
Q|T|T^9
Q|T^10
```

The thirteen `T^9PP` rows are

```text
P|P|T|T|T|T|T|T|T|T|T
P|P|T|T|T^7
P|P|T|T^8
P|P|T^9
P|T|T|T|T|T|T|T|T^2P
P|T|T|T|T|T|T|T^3P
P|T|T|T|T|T|T^4P
P|T|T|T|T|T^5P
P|T|T|T|T^6P
P|T|T|T^7P
P|T|T^8P
P|T^2P|T^7
P|T^9P
```

The new disconnected minimal row is `P|T^2P|T^7`, with component ranks
`1+3+7=11`. Its scalar ledger is only `-1/4+0+0`; it is not closed by the
conditional ordinary packet sum.

## 3. Fully shared `T^10Q`

Counts by shared-cut number are

| `Q` capacity | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 1 | 14 | 116 | 615 | 2167 | 5018 | 7431 | 6614 | 3141 | 598 | 25715 |
| 4 | 1 | 14 | 116 | 624 | 2208 | 5166 | 7732 | 7000 | 3398 | 672 | 26931 |
| 5 | 1 | 14 | 116 | 624 | 2215 | 5192 | 7805 | 7112 | 3493 | 704 | 27276 |
| 6 | 1 | 14 | 116 | 624 | 2215 | 5197 | 7819 | 7144 | 3525 | 719 | 27374 |
| 7 | 1 | 14 | 116 | 624 | 2215 | 5197 | 7822 | 7151 | 3536 | 725 | 27401 |
| 8 | 1 | 14 | 116 | 624 | 2215 | 5197 | 7822 | 7153 | 3539 | 728 | 27409 |
| 9 | 1 | 14 | 116 | 624 | 2215 | 5197 | 7822 | 7153 | 3540 | 729 | 27411 |
| `>=10` | 1 | 14 | 116 | 624 | 2215 | 5197 | 7822 | 7153 | 3540 | 730 | 27412 |

Applying the existing exact ordinary-split SAFE ledger gives:

| `Q` ledger | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | SAFE total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `q=3` | 0 | 14 | 116 | 615 | 2167 | 5018 | 7431 | 6614 | 3141 | 598 | 25714 |
| `q=4` | 0 | 14 | 116 | 624 | 2208 | 5166 | 7732 | 7000 | 3398 | 672 | 26930 |
| `q=5` | 0 | 13 | 115 | 624 | 2215 | 5192 | 7805 | 7112 | 3493 | 704 | 27273 |
| `q=6` | 0 | 14 | 116 | 624 | 2215 | 5197 | 7819 | 7144 | 3525 | 719 | 27373 |
| `q=7` | 0 | 13 | 115 | 624 | 2215 | 5197 | 7822 | 7151 | 3536 | 725 | 27398 |
| `q=8` | 0 | 14 | 116 | 624 | 2215 | 5197 | 7822 | 7153 | 3539 | 728 | 27408 |
| `q=9` | 0 | 13 | 115 | 624 | 2215 | 5197 | 7822 | 7153 | 3540 | 729 | 27408 |
| `q=10` | 0 | 14 | 116 | 624 | 2215 | 5197 | 7822 | 7153 | 3540 | 730 | 27411 |
| hostile `q>=11` | 0 | 13 | 115 | 624 | 2215 | 5197 | 7822 | 7153 | 3540 | 730 | 27409 |

Here the canonical universe stabilizes once the `Q` incidence capacity reaches
ten. The separate last two rows apply the even-cycle and hostile odd-cycle
ledger entries to that same stabilized universe.

For `Q=T` and the entered even-cycle ledger, ordinary splits leave only the
common bouquet. Under the conservative hostile odd-cycle ledger they leave
three signatures, at one, two, and three cuts:

```text
X(Q()T()T()T()T()T()T()T()T()T()T())
T(X(Q())X(T()T()T()T()T()T()T()T()T()))
T(X(Q())X(T())X(T()T()T()T()T()T()T()T()))
```

Thus the saturated hostile census is `27412=27409+3`; for `q=10` it is
`27412=27411+1`. These rows are only ordinary-split exceptions; no closure is
asserted.

## 4. Fully shared `T^9PP`

The complete color-preserving census is

| | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 1 | 22 | 264 | 1790 | 7560 | 20080 | 33154 | 32369 | 16775 | 3497 | 115512 |
| conditional SAFE | 0 | 20 | 260 | 1788 | 7559 | 20080 | 33154 | 32369 | 16775 | 3497 | 115502 |
| exceptions | 1 | 2 | 4 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 10 |

Hence the ordinary-split decomposition is

```text
115512 = 115502 + 10.
```

Nine exception shapes continue the rank-ten bouquet/router ladder. The unique
new shape is the four-interface pentagon router

```text
P(X(P())X(T())X(T())X(T()T()T()T()T()T()T()))
```

Sacrificing its central degree-four pentagon produces branch profiles

```text
P, T, T, T^7
```

with branch ranks `(1,1,1,7)` and ledger `-1/4+0+0+0`. This is the new
minimal fully shared router obstruction. It has 11 cycle nodes, 4 cut nodes,
15 incidence vertices, and 14 incidence edges. It is not a theorem-level graph
obstruction: cyclic mark order, realizability, connector territories, and a
legal replacement remain unchecked.

## 5. Fail-closed boundary

The executable independently checks canonical signatures, color multisets,
tree connectivity, all cycle and cut capacities, frozen partition totals,
every cut-count total, complete exception-signature sets, SHA-256 digests of
every canonical universe and residual list, exact SAFE complements, and the
new router's unique degree-four pentagon and exact branch profiles. Any
mismatch raises `RuntimeError`.

The executable does not check global cactus synthesis, bridge remnants,
off-core attached trees, cyclic order at a shared cut, sequential router
ownership, packet realizability, or positivity of any replacement. `SAFE`
means only that the conditional lower-rank ledger finds an ordinary one-cycle
split. The output is an exact conditional research frontier, not a rank-eleven
result.
