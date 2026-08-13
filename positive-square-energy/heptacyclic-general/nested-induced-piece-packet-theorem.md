# Rank-seven nested induced-piece packet theorem

## Statement

Put `sigma(H)=s^+(H)-|V(H)|`. After the actual-bridge split and the exact DNN
sieve in `rank-seven-multiblock-debit-ledger.md`, nine of the eleven remaining
owner keys have empty owner-sensitive residual:

`R21, R221, R31-K, R321, R322, R41, R421, R511-K5e, R511-K71`.      (1)

The proof is uniform over repeated owners, nested block-cut incidence,
arbitrary legal path lengths, and arbitrary rooted-tree attachments. The two
keys not asserted here are

`R31-S, R511-K22`.                                               (2)

Thus (1) is the maximal subset supported by the presently proved quantitative
packet library. This is a maximality statement about available certified
induced pieces, not a counterexample claim for either key in (2).

## Nested induced-piece rule

Root the bridge-free cyclic block-cut incidence tree at a retained packet.
For each selected demand, keep its entry cut upstream and take the complete
downstream side. If another selected demand is nested in that side, either keep
the complete first-boundary territory intact or make one explicit later
opening. In the latter case the intermediate cut remains in the first piece
and is not copied into the second. Every path remnant and every descendant
follows its first physical owner.

A complete first-boundary territory has credit at least `-1`: it is a nonempty
tree when all its cycles have been opened, has credit greater than `-1` when it
is unicyclic, and has nonnegative credit when its positive rank is at least two.
A selected triangular territory has positive credit. Consequently a strict
anchor of credit greater than `q` pays `q` tree-type territories, including
nested territories, strictly.

We also use the following triangular-cactus observation. A connected cactus
with at least two triangular blocks has credit greater than one. Form maximal
shared-cut clusters and cut the actual bridges of their reduced tree. A
cluster of `r>=2` triangles has credit greater than `r-1>=1`; if all clusters
are singletons, retain the bridge path between two nearest marked nodes as an
attached two-triangle territory of credit greater than one. Assign every
remaining component to one positive-rank side. This gives induced, disjoint,
exhaustive pieces and proves the observation. In particular it applies to six
triangles.

## Low-rank anchors

### `R21`

For `Theta(1,2,r)+T^5`, open an internal vertex of the long theta arm with its
complete owner class. If that class owns an external triangle it is a strict
triangular territory and the rank-at-most-six complement is nonnegative.
Otherwise it is one tree, while the complement is a six-triangle cactus of
credit greater than one. For `D+T^4+P`, use the same farthest-triangle and
`D+TT` selection as in the rank-six packet: the retained `D+TT` anchor has
credit greater than three and the pentagon and two remaining triangles occupy
at most three complete first-boundary territories. Hence both typed rows are
strict.

### `R221`

For `D+D+T^3`, boundary-open the second physical diamond. If `k` triangles lie
upstream, retain the `D+T^k` packet, of credit greater than `1+k`. The complete
downstream side is a tree only when it contains no triangle; otherwise it is
positive. A triangle between the diamonds or nested beyond another triangle
stays in that one downstream side. The worst ledger is `>1-1>0`.

### `R31-K`, `R321`, and `R322`

For `R31-K`, the exact excess predicate forces at least one of the four cycles
to be a triangle, since four nontriangles have total excess below three. Retain
that triangle with the actual `K4`; the established bridge-free `K4+T` packet
has credit greater than three. The other three demands cost at most one each;
nested demands remain one complete first-boundary side. Thus `>3-1-1-1>0`.

For `R321`, each typed residual contains a triangle. Apply the same terminal
allocation to `K4+Theta+T+Q`, with the theta and the other cycle as the two
nonselected demands. For `R322`, retain the actual `K4` and treat the two
diamonds at their first boundaries. The ordinary two-debit theorem gives
`>2-1-1>0`. These statements include a theta or diamond lying between the
anchor and another demand.

## Rank-four opening anchors

For a physical `S4` opening, let `R` be the complete opened owner class and
`F` the retained favorable rank-three packet. The exact residual gates for
both `R41` and `R421` supply an external triangle `T`. In `R421`, this follows
because the largest nontriangle cycle excess is `p=5-2sqrt(5)<3/5`, while
`d(S4)<3/5` and `Delta-1<3/5`, so a nontriangle cannot make their sum exceed
two.

If `T` follows `R`, that complete owner territory is strict and the complement
has rank at most six. Otherwise retain `T` with `F`; the established
actual-`K4+T` or four-triangle packet has credit greater than three. If another
cycle lies between `F` and `T`, open it once at its entry cut and keep the
complete downstream triangular territory, exactly as in the rank-six nested
repair.

For `R41`, charge the structural tree and the two unselected cycle boundaries:
`>3-1-1-1>0`. This covers both `T^3` and the even-state `T^2P` row. For `R421`,
charge the structural tree and the theta first boundary:
`>3-1-1>0`. Thus `R41` and `R421` are closed without importing the coarse S4
DNN debit.

## Rank-five structural anchors

### `R511-K5e`

The exact DNN gate leaves two triangles. Regenerate the all-odd `K5-e`
structural partition before choosing an owner. In each of the 53 actual-`K4`
states, retain the physical actual `K4` with one triangle; this anchor has
credit greater than three and pays the deleted owner tree and the other cycle
boundary. In each of the 640 favorable-theta states, retain the favorable theta
with one triangle; its credit is greater than two and pays the deleted center
tree and the other cycle boundary. If one triangle follows the deleted owner,
that owner territory is already strict. If the triangles are nested, open only
their first boundary. Hence every regenerated structural state closes.

### `R511-K71`

Regenerate the nine physical K71 structural targets. Their retained six unit
paths form an actual attached `K4`, of credit greater than two, and their
complementary owner `U` is favorable unicyclic and therefore positive. If an
external cycle follows `U`, retain its complete class. Otherwise each of the
two cycles contributes at most one first-boundary tree. The worst ledger is
`>2+0-1-1>0`. No path of the retained actual `K4` is lengthened.

## Maximality of the proved subset

The owner-typed manifest performs a fail-closed demand comparison. Every key
in (1) has a cited anchor whose strict integer threshold is at least its maximum
number of negative territories. The two returned keys fail that comparison for
specific physical subclasses:

1. `R31-S` contains the canonical doubled-`C4` class `111`. The certified
   retained packet with two triangles has only `sigma>1`; after its structural
   tree is paid, two further cycle boundaries remain. No certified packet
   supplies the missing two units.
2. `R511-K22` has an actual-`K4` anchor of credit greater than two, but its
   original opened tree and two arbitrary external cycle boundaries can require
   three negative units. Neither external cycle is forced to be triangular.

Therefore no larger subset can be accepted from the typed demands and the
currently pinned packet thresholds. A stronger doubled-`C4` multi-triangle
packet or a marked K22-plus-cycle packet would enlarge the theorem.

## Fail-closed artifacts

The persisted owner-typed manifest is
`research/fixtures/rank-seven-nested-induced-piece-manifest.json`. Run

```text
python3 research/rank-seven-nested-induced-piece-verifier.py
python3 -O research/rank-seven-nested-induced-piece-verifier.py
```

The verifier regenerates all fifteen partitions of seven, checks the exact
eleven-key input registry, regenerates the 53/640 all-odd `K5-e` structural
states and nine K71 targets, audits nested owner partitions, proves the maximal
nine-key subset from typed thresholds, and rejects hostile mutations. Together
with `R61` and the five earlier two-debit closures this leaves exactly the two
keys in (2); it does not yet prove the full multiblock theorem.
