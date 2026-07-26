# Packet surplus ledger for opening cycles in hexacyclic residuals

## Scope

Put

`sigma(H)=s+(H)-|V(H)|`, `T=C3`, `P=C5`, and `Q=Cq` for
`q=1 mod 4`. Write

`delta_q=sec(pi/q)-1`, and `delta=delta_5=sqrt(5)-2`.

This note records exact symbolic **proof margins** already available in the
bicyclic, tricyclic, tetracyclic, and pentacyclic cactus papers. Its purpose is
budgeting induced tree territories created by opening cycles in a hexacyclic
residual. It makes no hexacyclic theorem claim, no optimality claim for any
constant, and no claim that the listed incidence conditions exhaust a
hexacyclic residual.

If an induced territory `F` is a nonempty tree, then `sigma(F)=-1`. Thus a
packet certificate `sigma(H)>c` pays `k` opened-tree territories whenever
`c>=k`, leaving `sigma(G)>c-k>=0`; equality `c=k` is enough because the packet
bound is strict. A non-strict bound `sigma(H)>=c` pays `k` only when `c>k`.
Costs add only after an actual vertex partition into induced territories.

All quoted packet estimates allow arbitrary trees attached at arbitrary
vertices. Bridge-separated packet sums allow arbitrary connector trees,
provided cuts are made on actual bridge edges. A split cycle must be divided
into proper consecutive intervals, with each off-core tree assigned wholly to
the interval or packet containing its unique core attachment.

## Atomic packets from the bicyclic and tricyclic papers

The following are the reusable units. A bar denotes bridge-separated induced
territories, not merely a formal partition of the cycle multiset.

| Packet or packet sum | Incidence hypothesis | Certified surplus | Tree costs paid |
|---|---|---:|:---:|
| `T` | triangular unicyclic cactus | `>0` | 0 |
| `Q` | unicyclic, `q=1 mod 4` | `>=-delta_q=1-sec(pi/q)` | 0 |
| `TT` | arbitrary incidence and connector | `>1` | 1 |
| `TQ` | arbitrary incidence and connector | `>1-delta_q=2-sec(pi/q)` | 0 |
| `PP`, shared | the pentagons have one common vertex | `>=1-4/(3sqrt(13))` | 0 |
| `PP`, disjoint | vertex-disjoint pentagons joined by a nontrivial connector | `>5-2sqrt(5)` | 0 |
| `RR...R` | `r` cycles, all lengths `3 mod 4`, cycle-packing number at most two | `>r-1` | `r-1` |
| `TTQ` | the two triangles share a cut vertex; `q=1 mod 4` | `>2-delta_q=3-sec(pi/q)` | 1 |
| `TPP` | all three cycles form one shared-cut cluster | `>6-2sqrt(5)` | 1 |
| `P|TP` | bridge-separated `P` and mixed bicyclic packet | `>1-2delta=5-2sqrt(5)` | 0 |

The generic statements "every bicyclic cactus has `sigma>=0`" and "every
tricyclic cactus has `sigma>=0`" carry no opening credit. Likewise, strict
surplus of an isolated triangular packet is not a fixed positive credit: with
large tree attachments it cannot be charged against any positive fraction of
an opening cost.

Two useful exact specializations are

- `sigma(TTT)>2` for a connected all-triangle cluster with packing number at
  most two; this pays two openings;
- `sigma(TTTT)>3` for a connected four-triangle shared-cut cluster, including
  the central-triangle/three-petal packing-three incidence; this pays three
  openings.

For an all-`3 mod 4` packet with packing number at most two, the same formula
gives `sigma>r-1` without requiring every cycle to be triangular. The packing
hypothesis is essential.

## Tetracyclic packets that pay openings

The tetracyclic paper supplies a generic strict bound `sigma(H)>0`, which by
itself pays no tree cost. The following residual incidences have stronger
quantitative certificates. These are the rows of the existing tetracyclic
ledger whose margin is at least one.

### Cycle multiset `TTTQ`

| Shared-cut cluster incidence | Additional incidence condition | Certified surplus | Costs paid |
|---|---|---:|:---:|
| `T|T|T|Q` | a reduced-cluster-tree edge makes a `TQ / TT` two-two split | `>2-delta_q=3-sec(pi/q)` | 1 |
| `TT|T|Q` | none | `>2-delta_q=3-sec(pi/q)` | 1 |
| `TQ|T|T` | the path between singleton triangles avoids the `TQ` node | `>2-delta_q=3-sec(pi/q)` | 1 |
| `TTT|Q` | none; open a private non-entry vertex of `Q` inside the proof | `>1` | 1 |
| `TT|TQ` | none | `>2-delta_q=3-sec(pi/q)` | 1 |
| `TTQ|T` | the triangles in `TTQ` share a cut | `>2-delta_q=3-sec(pi/q)` | 1 |
| `TTQ|T` | internal incidence is `T-Q-T` at distinct cuts | `>1` | 1 |
| fully shared | some two designated triangles share a cut | `>1` | 1 |

The first, second, third, fifth, and shared-triangle sixth rows have unused
fractional credit `>1-delta_q=2-sec(pi/q)` after one external opening. The
rows with bound `>1` have only strict zero left after that opening.

The following `TTTQ` incidences are not one-cost certificates in the present
ledger: four singleton clusters without a two-two split; `TQ|T|T` when the
`TQ` node lies on the singleton-triangle path; and the fully shared
three-distinct-`Q`-petal incidence. Their recorded margins are respectively
`>1-delta_q`, `>1-delta_q`, and `>0`.

### Cycle multiset `TTPP`

| Shared-cut cluster incidence | Additional incidence condition | Certified surplus | Costs paid |
|---|---|---:|:---:|
| `TTP|P` | the two triangles in `TTP` share a cut | `>2-2delta=6-2sqrt(5)` | 1 |
| `TPP|T` | none | `>6-2sqrt(5)` | 1 |
| `TT|PP` | none | `>1` | 1 |
| `TP|TP` | none | `>2(1-delta)=6-2sqrt(5)` | 1 |
| `TT|P|P` | either reduced-tree path position | `>1` or `>6-2sqrt(5)` | 1 |
| `PP|T|T` | the path between the triangles avoids the `PP` node | `>1` | 1 |
| `TP|T|P` | the singleton `T-P` path avoids the `TP` node | `>6-2sqrt(5)` | 1 |
| `T|T|P|P` | some reduced-tree edge gives `TP / TP` or `TT / PP` | `>6-2sqrt(5)` or `>1` | 1 |

No row here pays two external openings: `6-2sqrt(5)<2`. The exact unused
credit after one opening in the stronger rows is

`5-2sqrt(5)=1-2delta`.

The current ledger does not pay one cost in the distinct-cut `T-P-T` version
of `TTP|P`, the hostile path positions in `PP|T|T` and `TP|T|P`, a
four-singleton incidence without a two-two split, or either fully shared
`TTPP` alternative. Their exact recorded margins are among
`3-sqrt(5)`, `5-2sqrt(5)`, and strict zero.

## Pentacyclic packets with concentrated credit

The generic pentacyclic conclusion `sigma(H)>0` has no external opening
credit. For a hexacyclic argument one must retain the stronger packet sum used
inside the proof. The following rows are the directly reusable quantitative
ones.

### Cycle multiset `TTTTQ`

Assume `q=1 mod 4`; even and `3 mod 4` cycles are nonhostile but are not
assigned a negative `delta_q` charge here.

| Shared-cut cluster incidence | Certified surplus | Costs paid |
|---|---:|:---:|
| `TTTT|Q` | `>3-delta_q=4-sec(pi/q)` | 2 |
| `TTT|TQ` | `>3-delta_q=4-sec(pi/q)` | 2 |
| `TTQ|TT` | `>1` | 1 |
| `TTT|T|Q` | `>2-delta_q=3-sec(pi/q)` | 1 |
| `TT|TT|Q` | `>2-delta_q=3-sec(pi/q)` | 1 |
| `TT|TQ|T` | `>2-delta_q=3-sec(pi/q)` | 1 |

The first two rows pay two costs because `delta_q<1`. Their exact remainder
after two costs is `>1-delta_q=2-sec(pi/q)`. None of these rows pays three
costs uniformly.

The direct rows `TT|T|T|Q` and `TQ|T|T|T` have only
`>1-delta_q`; `TTQ|T|T` has only a nonnegative tricyclic packet plus strict
triangles. The `TTTTQ` rows containing an undifferentiated positive
tetracyclic packet, and the all-singleton leaf argument, provide strict
positivity but no fixed opening credit.

For a fully shared `TTTTQ` incidence:

- if the four triangles are pairwise disjoint, incidence acyclicity forces
  four distinct triangular petals on `Q`; splitting `Q` gives four strict
  triangular packets but no uniform positive constant;
- if two triangles intersect and `q>=4`, opening one private vertex of `Q`
  leaves four triangular cycles whose packet sum is `>1`; that `>1` is already
  spent on the internal opening, so the resulting proof certifies only
  `sigma>0`, not another external cost;
- if the four surviving triangles themselves remain one connected shared-cut
  packet, the independent `TTTT` estimate `>3` is available, but that stronger
  incidence must be verified rather than inferred from "fully shared" before
  `Q` is opened.

### Cycle multiset `TTTPP`: disconnected clusters

| Shared-cut cluster incidence | Certified surplus | Costs paid |
|---|---:|:---:|
| `TTT|PP` | `>2` | 2 |
| `TPP|TT` | `>7-2sqrt(5)` | 2 |
| `TTT|P|P` | `>6-2sqrt(5)` | 1 |
| `TT|TP|P` | `>6-2sqrt(5)` | 1 |
| `TT|T|PP` | `>1` | 1 |
| `TPP|T|T` | `>6-2sqrt(5)` | 1 |
| `TP|TP|T` | `>6-2sqrt(5)` | 1 |

The `TTT|PP` row pays exactly two costs by strictness. The `TPP|TT` row leaves
the exact positive balance `>5-2sqrt(5)` after two costs. The one-cost rows
with margin `6-2sqrt(5)` leave `>5-2sqrt(5)`.

The rows `TTTP|P`, `TTP|TP`, `TTP|T|P`, `TT|T|P|P`, `TP|T|T|P`,
`PP|T|T|T`, and the all-singleton incidence do not uniformly pay one external
cost under the existing proof ledger. In particular, the entry-sensitive
repair of `TTTP|P` has worst recorded margin `>1-delta=3-sqrt(5)<1`, and the
repair of `TTP|T|P` includes a `TTP+T` outcome with only strict zero.

### Cycle multiset `TTTPP`: one shared-cut cluster

For the 36 incidence trees resolved by splitting one internal cycle, the
following exact branch-packet sums are available.

| Sacrificed internal cycle | Branch packets after the split | Certified branch surplus | External tree costs paid |
|---|---|---:|:---:|
| `T` | `PP+TT` | `>1` | 1 |
| `T` | `T+TPP` | `>6-2sqrt(5)` | 1 |
| `T` | `TP+TP` | `>6-2sqrt(5)` | 1 |
| `T` | `P+P+TT` | `>5-2sqrt(5)` | 0 |
| `T` | `P+T+TP` | `>5-2sqrt(5)` | 0 |
| `T` | `PP+T+T` | `>0` | 0 |
| `P` | `P+TTT` | `>2-delta=4-sqrt(5)` | 1 |
| `P` | `T+TTP` | `>0` | 0 |
| `P` | `TP+TT` | `>2-delta=4-sqrt(5)` | 1 |
| `P` | `P+T+TT` | `>1-delta=3-sqrt(5)` | 0 |
| `P` | `T+T+TP` | `>1-delta=3-sqrt(5)` | 0 |

The displayed cycle is split among the branch territories into proper path
intervals; it is not removed as a separate tree territory and therefore costs
no surplus unit. Thus every row with margin greater than one pays one later
tree opening. In particular, the two `4-sqrt(5)` rows leave
`>3-sqrt(5)>0` after one external opening. No row in this table pays two.

The four exceptional fully shared incidences require separate hypotheses:

1. At one cut incident with all five cycles, at cuts of degrees `(4,2)` with
   the specified three-triangle side, or at the `(3,2,2)` incidence retaining
   a connected three-triangle cluster, opening both leaf pentagons leaves a
   `TTT` packet of surplus `>2`. Both units are spent internally; no external
   cost remains.
2. In the pentagon-hub incidence, splitting the hub into branch packets
   `TP+T+T` gives `>1-delta=3-sqrt(5)<1`; the split itself costs no unit, but
   the margin still pays no external opening.

## Candidate hexacyclic uses

The DNN bookkeeping suggests that the hostile six-cycle multisets requiring
packet analysis begin with `TTTTTQ` and `TTTTPP`. This sentence is only a
work-planning observation; no reduction or exhaustiveness assertion is made
here. For these candidates, the safest inherited moves are:

| Hexacyclic local move | Required incidence after the opening | Inherited credit | Net certificate |
|---|---|---:|---:|
| Open one leaf cycle from `TTTTTQ` | pentacyclic remainder is `TTTT|Q` or `TTT|TQ` | `>3-delta_q` | `>2-delta_q` |
| Open two tree territories from `TTTTTQ` | same two packetizations | `>3-delta_q` | `>1-delta_q` |
| Open one leaf cycle from `TTTTPP` | remainder is `TTT|PP` | `>2` | `>1` |
| Open two tree territories from `TTTTPP` | remainder is `TTT|PP` | `>2` | `>0` |
| Open one leaf cycle from `TTTTPP` | remainder is `TPP|TT` | `>7-2sqrt(5)` | `>6-2sqrt(5)` |
| Open two tree territories from `TTTTPP` | remainder is `TPP|TT` | `>7-2sqrt(5)` | `>5-2sqrt(5)` |
| Sacrifice one cycle inside a pentacyclic shared `TTTPP` remainder, then open one external cycle | split branches are `P+TTT` or `TP+TT` | `>4-sqrt(5)` | `>3-sqrt(5)` |
| Open one leaf cycle from a residual leaving `TTT` | surviving triangles form one shared-cut cluster with packing at most two | `>2` | `>1` |
| Open two tree territories leaving `TTT` | same | `>2` | `>0` |
| Open up to three tree territories leaving `TTTT` | one connected four-triangle shared-cut cluster | `>3` | `>3-k` for `k<=3` |

The first six moves require the displayed **cluster partition**, not just the
cycle multiset of the pentacyclic remainder. The seventh requires one of the
two exact branch partitions after a legal consecutive-interval split. The last
three require concentration of the surviving triangles in the stated packet;
separate strict triangular territories cannot replace that concentration.

## Incidence checks required before charging a cost

1. **Retained shared-cut components.** Cycles joined through shared cut
   vertices cannot be assigned to different induced territories while both
   cycles are retained. Packet symbols must respect connected components of
   the retained shared-cut graph.
2. **Reduced-tree position.** A formal cluster multiset does not imply a
   desired packetization. For three or more separated clusters, verify the
   relevant path-avoidance or two-two-split condition in the reduced cluster
   tree, including genuine Steiner branches.
3. **Entry topology.** If a connector enters an internal cycle, record whether
   it enters at a private cycle vertex, a shared cut, or through an attached
   cycle. The `TTTP|P` and `TTP|T|P` repairs show that the margin can change
   with this entry data.
4. **Private opening vertex.** Opening `Q` while retaining its incident packet
   requires a vertex not used as a shared cyclic cut. The incidence-excess
   count must supply such a vertex; it is not automatic.
5. **Packing number.** Credits `>r-1` from the favorable-cycle phase estimate
   require cycle-packing number at most two. The special `TTTT` packing-three
   estimate applies only to its audited central-triangle/three-petal incidence.
6. **Cost ownership.** Opening a cycle by removing a private vertex and its
   rooted branches creates a separate tree territory and consumes one unit.
   Splitting a cycle among proper path intervals creates no separate tree cost,
   but its resulting packet margin may be charged only once.
7. **Strict versus uniform credit.** A strict `>0` packet can provide final
   strictness after all integer costs are exactly paid, but it cannot pay a
   positive missing fraction uniformly.

## Practical priority

For a future hexacyclic incidence census, label each prospective opening by
the pentacyclic packet left behind and attach one of three statuses:

- `2-cost`: `TTTT|Q`, `TTT|TQ`, `TTT|PP`, or `TPP|TT` under their exact
  incidence hypotheses;
- `1-cost`: any tetracyclic row marked one-cost above, the remaining listed
  pentacyclic rows, or a shared `TTTPP` cycle split whose branch sum exceeds
  one;
- `0-cost`: generic positive tetracyclic/pentacyclic remainders, strict
  singleton triangles, fully shared sacrifice proofs that already spend their
  packet credit, and every hostile path position explicitly excluded above.

This classification is a ledger for proof search only. Establishing a
hexacyclic result would still require an exact DNN residual reduction, a
color-preserving incidence census, induced-territory constructions for every
row, and separate treatment of any fully shared exceptions.
