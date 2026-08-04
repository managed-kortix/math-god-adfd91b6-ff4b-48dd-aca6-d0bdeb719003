# Hexacyclic multiblock theorem: exhaustive ledger and hostile audit

## 1. Statement and conventions

For a connected graph `X`, put

`sigma(X)=s^+(X)-|V(X)|`.

**Theorem.** Every finite simple connected graph `G` of cyclomatic rank six
with at least two positive-rank cyclic blocks satisfies

`s^+(G)>=|V(G)|`.

Arbitrary bridge connectors and arbitrary finite rooted trees are included.
The proof below is an exhaustive block-rank proof; it does not address the
single positive-rank block case.

Write `T=C3`, `P=C5`, `D=Theta(1,2,2)`,

`p=epsilon(P)=5-2sqrt(5)`,
`d=Delta(D)=(sqrt(17)-1)/2`.

For cycles, `epsilon(C3)=1`, every nontriangle has excess at most `p`, and
every odd cycle of length at least seven has excess below `2/5`. For a
bicyclic block, `Delta<=d`; `Delta>1` occurs exactly for
`Theta(1,2,r)`, and `Delta>2-p` occurs only for `D`. The exact rank-three
ledger has two kinds of rows: the actual `K4`, of DNN excess three, and the
canonical structural rows `S3`, each of excess below `12/5`; every other row
has excess at most two. The exact rank-four ledger has direct rows of excess at
most three and exactly two structural no-long states. Their six `K4` support
paths use the regular tetrahedron Gram: the even-extra state has excess below
`18/5`, and the odd-extra state has excess below `19/6`. The exact rank-five
ledger has direct rows of excess at most four and exactly three structural
families: all-odd `K5-e`, kernel 22, and kernel 71. For all-odd `K5-e`, the
all-unit correlation certificate and fixed-parity monotonicity give excess at
most `2sqrt(7)-1`. K22 and K71 retain an actual attached `K4` under precisely
their certified structural descendants.

The two nontriangle gates just quoted are exact inequalities (use `p<3/5`):

`E(S4)+epsilon(Q1)+epsilon(Q2)`
` < max(18/5+6/5,19/6+6/5)=24/5<5` if `Q1,Q2 != T`,           (1)

`2sqrt(7)-1+p<5`.                                              (2)

For (1), the six unit support paths cost three. The canonical even extra path
costs `4-2sqrt(3)<3/5`, while the odd extra path costs below `1/6`; these are
the exact two-state certificates from the complete rank-four ledger, not an
inference from the tetracyclic spectral theorem. For (2), squaring the positive
quantities reduces it to `sqrt(7)-sqrt(5)<1/2`; squaring once more gives
`529<560`. These facts, the theta bounds, and the `12/5` bound are the only
numerical inputs to the sieve.

## 2. The eleven partitions

Block additivity makes the positive cyclic-block ranks an integer partition of
six. The complete ledger is

| number | block-rank partition | DNN/structural output before owner closure |
|---:|---|---|
| 1 | `1+1+1+1+1+1` | closed by the rank-uniform cactus theorem |
| 2 | `2+1+1+1+1` | `Theta(1,2,r)+T^4`; `D+T^3+P` |
| 3 | `2+2+1+1` | `D+D+T^2` |
| 4 | `2+2+2` | DNN: `3d<5` |
| 5 | `3+1+1+1` | `S3+T^3`; `K4+Q1+Q2+Q3` with `sum epsilon(Qi)>2` |
| 6 | `3+2+1` | pre-sieve `K4+Theta(1,2,r)+T` and `K4+D+P`; all other rows DNN |
| 7 | `3+3` | pre-sieve `K4+K4` and `K4+S3`; all other rows DNN |
| 8 | `4+1+1` | `S4+Q1+Q2` with at least one `Qi=T`; nontriangle pairs satisfy (1) |
| 9 | `4+2` | pre-sieve `S4+Theta`; direct rows DNN |
| 10 | `5+1` | direct rows are DNN at excess at most five (including equality with `T`); structural all-odd `K5-e+T`; structural `K22+Q` and `K71+Q` for arbitrary `Q`; nontriangle K5e rows satisfy (2) |
| 11 | `6` | single-block program, outside this theorem |

This table replaces the former seven-family claim. In particular,
`K4+K4`, `K4+Theta(1,2,r)+T`, and `K4+D+P` may not be erased by calling the
old seven rows exhaustive.

Here are the exact empty-row checks. Besides `3d<5`, a rank-three row other
than `K4` in partition `3+2+1` has

`E+Delta+epsilon < 12/5+d+1 < 5`,                             (3)

because `sqrt(17)<21/5`. Two non-`K4` rank-three rows have total excess below
`24/5`; direct rank-four plus rank-two has excess at most `3+d<5`; and direct
rank-five plus a cycle has excess at most five. In `3+2+1`, the `K4` inequality
is `3+Delta+epsilon>5`; the exact theta-cycle classification gives precisely
`Theta(1,2,r)+T` and `D+P`. Thus no nontriangle theta row other than `D+P`
is omitted. The analogous elementary cycle sums give exactly the two rows in
partition 2 and the one row in partition 3.

The rank-five direct bound in partition `5+1` is nonstrict. In particular, a
direct rank-five equality certificate of excess four together with a triangle
of excess one has total excess exactly five. This is accepted by the DNN
inequality and proves `s^+(G)>=|V(G)|`, but it does not prove strictness. It is
a closed direct row and contributes no packet residual. All strict inequalities
below are retained only for the packet and pre-sieve rows where they are
actually proved.

## 3. Structural pre-sieve owners

The rows marked `pre-sieve` are proof rows, not DNN rows. They are closed
before the residual packet subtraction.

**K4 anchor lemma.** Keep an attached actual `K4` as an induced anchor. It has
`sigma>2`. Root the block-cut incidence tree there. With at most two external
cyclic demands, each first boundary contributes either an intact positive-rank
territory of credit greater than `-1`, a higher-rank territory of nonnegative
credit, or one cycle-minus-cut tree of credit `-1`. Nested demands stay in one
complete first-boundary territory. Hence there are at most two negative units,
shared cuts are retained only by the anchor, and the inequality is strict.

This proves all incidences of `K4+Theta+Q`, including
`K4+Theta(1,2,r)+T` and `K4+D+P`. It also proves `K4+K4` and `K4+S3`, where
there is only one external demand. Actual bridges cause no difficulty: take
the complete descendant side, which has lower rank and nonnegative credit.

**Rank-four opening lemma.** A structural `S4` opening assigns its internal
path vertex and complete owner class to one induced territory `R`. If `R`
contains an external cyclic block, it is an intact positive-rank territory and
the rank-at-most-five complement is nonnegative; the routed triangular case is
strict. Otherwise `R` is one nonempty tree. The retained rank-three packet has
credit greater than two. For `S4+Theta`, treat the theta at its first boundary:
it costs at most one unit, including nested or repeated-cut incidence. Thus

`sigma(G)>2-1-1=0`.

This closes the omitted partition `4+2` structural row. The same owner rule is
used for the triangle-containing `4+1+1` packets below. These arguments define
the vertex partition before charging credit: an opened vertex takes all its
owned descendants, a boundary cut stays upstream, and no shared cut is copied.

## 4. Exact residual after the pre-sieve

After Sections 2--3, the complete residual is the following disjoint ledger of
packet templates:

| id | partition | packet |
|---:|---|---|
| A | `2+1^4` | `Theta(1,2,r)+T^4`, `r>=2` |
| B | `2+1^4` | `D+T^3+P` |
| C | `2+2+1+1` | `D+D+T^2` |
| D | `3+1+1+1` | canonical `S3+T^3` |
| E | `3+1+1+1` | actual `K4+Q1+Q2+Q3`, `sum epsilon(Qi)>2` |
| F | `4+1+1` | structural `S4+Q1+Q2`, at least one `Qi=T` |
| G | `5+1` | favorable-theta structural all-odd `K5-e+T` |
| H | `5+1` | structural kernel `K22+Q`, arbitrary cycle `Q` |
| I | `5+1` | structural kernel `K71+Q`, arbitrary cycle `Q` |

These are nine packet templates, but they are not the entire sieve and are
not called nine exhaustive families. The pre-sieve rows in Section 3 are an
essential part of the exhaustive ledger.

Template E contains a triangle: three nontriangles have total excess at most
`3p<2`. Template F contains a triangle by the exact nontriangle gate (1), not
by owner reasoning. Template G contains a triangle because every nontriangle
is DNN-closed by (2). Templates H and I have no cycle-length restriction:
their owner-exact attached-`K4` closures pay the original structural territory
and one cycle boundary.

## 5. Packet closure

Templates A--D are closed owner-exactly in
`multiblock-items1-4-owner-exact-closure.md`. The proof opens the long theta
arm for A, retains `D+TT` for B, physically boundary-opens the second diamond
for C, and uses the canonical structural opening (including the separate
doubled-`C4` retained-packet theorem) for D.

Templates E--I are closed owner-exactly in
`multiblock-items5-7-owner-exact-closure.md`. For E, the actual `K4` credit
greater than two pays at most two first-boundary losses, with the guaranteed
triangle giving strictness. For F, the structural opening either routes the
triangle or retains it with the favorable rank-three anchor. If the other
cycle lies between the anchor and the triangle, it is boundary-opened once at
its entry cut; its downstream territory contains the intact triangle and is
strict. For G, delete the selected all-odd `K5-e` center and retain the
favorable theta with the external triangle. The attachment-uniform theorem

`favorable-theta-triangle-shared-cut-packet.md`

gives anchor credit greater than two at every physical shared cut, and pays
the one deleted owner tree strictly. A positive connector is cut at its first
actual bridge and is not silently absorbed into that packet.

For H, the retained actual `K4` has credit greater than two and pays the
original K22 owner tree plus at most one cycle-boundary tree. For I, the same
anchor pays the favorable K71 unicyclic side and at most one cycle boundary.
In both families the physical opening assigns every branch, path interior,
route, connector remnant, rooted tree, and deeper descendant to exactly one
owner. Thus arbitrary cycle length, common owners, nested incidence, and
positive connectors are included.

Every packet closure is uniform over repeated owners, nested cycles, positive bridge
connectors, and rooted-tree attachments. Therefore all nine packet templates
are empty after owner closure. Together with the DNN rows and the structural
pre-sieve rows, this proves the stated nonstrict theorem. The direct
rank-five-equality-plus-triangle row is already DNN-closed and leaves no
residual.

## 6. Fail-closed verifier and hostile self-audit

Run both interpreter modes:

```text
python3 research/hexacyclic-multiblock-ledger-verifier.py
python3 -O research/hexacyclic-multiblock-ledger-verifier.py
```

The verifier independently generates the eleven integer partitions, checks
their unique dispositions, checks the full pre-sieve and A--I key sets, and
regenerates the true rank-five structural ledger from the K5e sieve and the
K22/K71 theorem fixtures. It locks all owner, packet, and DNN-gate sources,
evaluates every displayed exact inequality, and requires all hostile mutations
to fail without using `assert`.

The hostile audit specifically rejects the following former failure modes.

1. Omitting `K4+K4`, either `K4+Theta+T` row, or the structural `4+2` row.
2. Treating A--I as the exhaustive sieve rather than the post-pre-sieve packet
   residual.
3. Importing a triangle into F or G without the nontriangle DNN inequalities.
4. Using the favorable-theta packet across a positive connector.
5. Duplicating an intermediate cycle cut in the nested F incidence.
6. Replacing a strict packet margin by a sum of unspecified positive margins.
7. Accepting a missing partition, changed source, weakened inequality, widened
   packet scope, or deleted owner in optimized Python mode.
8. Omitting K22 or K71, changing either arbitrary-cycle disposition, or losing
   an opened/retained owner route, connector, nested cycle, or descendant.
9. Promoting the global nonstrict conclusion to a strict conclusion, or
   returning the direct rank-five-equality-plus-triangle row as a residual.

Partition `6` remains outside the result. Thus this nonstrict theorem is
unconditional for the multiblock branch only and makes no claim about all
connected hexacyclic graphs. Strict conclusions remain valid for the individual
pre-sieve and packet rows whose displayed ledgers prove them.
