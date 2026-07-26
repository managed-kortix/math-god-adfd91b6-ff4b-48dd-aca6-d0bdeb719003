# Induced-packet audit of the 20 shared `{3,3,5,5}` cores

## Verdict

The proposed claim is **false for the stated known-credit table**. Exhausting
all vertex partitions of the canonical 13-vertex cores gives positive credit
for 18 of the 20 types. Type 5 has numerical credit zero with a strict packet,
so it still proves `s+(G)>n`. Type 1, the four-cycle bouquet, has optimum
credit `-1` (strict) and is not certified by these packet bounds.

Thus the search gives phase-free induced-packet certificates for 19 types if
strict zero is accepted as the desired strict inequality, but not for all 20.
In particular, this computation does not replace the weighted phase
certificate for the bouquet and proves no theorem beyond the finite audit.

## Credit table used

For a connected induced component `H` of order `h`, credit means the proved
lower bound on `s+(H)-h`. The implementation uses only the bounds already
recorded in `all-tricyclic-cacti/paper.tex`:

| induced cycle content | credit | strict? |
|:---|:---|:---:|
| tree | `-1` | no |
| one or two triangles, no pentagon | `r-1`, where `r=1,2` | yes |
| one pentagon, no triangle | `2-sqrt(5)` | no |
| one triangle and one pentagon | `3-sqrt(5)` | yes |
| two pentagons, no triangle | `0` | no |

The last line is the general bicyclic-cactus bound. The triangular line is the
packing-at-most-two phase bound translated via `m=h-1+r`. No unproved packet
estimate is inserted.

Scores are represented exactly as `a+b*sqrt(5)` and compared by integer
squaring with sign checks. Floating-point values are printed only for
readability.

## Exhaustion

The driver imports the existing canonical census rather than making another
list of cores. That census independently agrees under exact graph isomorphism
and canonical colored-cycle coding and supplies exactly 20 types.

For each core, every nonempty vertex subset is inspected. A subset is
admissible when its induced graph is connected and its complete induced cycle
content matches a row of the table. A subset dynamic program then considers
every admissible set partition, anchoring each transition at the least
remaining vertex to avoid ordering duplicates.

This also exhausts arbitrary, possibly disconnected induced packets: split
each such packet into its connected components. The components remain induced,
their credits add, and this connected refinement is one of the dynamic
program's partitions. In a cactus, an induced cycle must be one of the listed
original cycle blocks, so testing which canonical cycles are wholly contained
finds the complete cycle content. The script additionally checks this count
against the induced cyclomatic number.

## Best certificates

Canonical cycles are `T0,T1,P2,P3`; their explicit vertex tuples are printed
on each type line by the driver. Each row below gives the explicit core vertex
subsets in the optimum partition, followed in parentheses by their induced
cycle contents. `none` denotes a tree component.

| type | incidence | optimum induced packets | total credit |
|---:|:---|:---|:---|
| 1 | `0123` | `{9}` (`none`); `{5}` (`none`); `{0,1,2,3,4,6,7,8,10,11,12}` (`T0,T1`) | `-1`, strict |
| 2 | `012+03` | `{1,9,10,11,12}` (`P3`); `{0,2,3,4,5,6,7,8}` (`T1,P2`) | `5-2sqrt(5)`, strict |
| 3 | `012+23` | `{5,9,10,11,12}` (`P3`); `{0,1,2,3,4,6,7,8}` (`T0,T1`) | `3-sqrt(5)`, strict |
| 4 | `012+23` | `{6,9,10,11,12}` (`P3`); `{0,1,2,3,4,5,7,8}` (`T0,T1`) | `3-sqrt(5)`, strict |
| 5 | `023+01` | `{1,5,6,7,8,9,10,11,12}` (`P2,P3`); `{0,2,3,4}` (`T1`) | `0`, strict |
| 6 | `01+02+03` | `{1,5,6,7,8}` (`P2`); `{0,2,3,4,9,10,11,12}` (`T1,P3`) | `5-2sqrt(5)`, strict |
| 7 | `01+02+13` | `{1,5,6,7,8}` (`P2`); `{0,2,3,4,9,10,11,12}` (`T1,P3`) | `5-2sqrt(5)`, strict |
| 8 | `01+02+23` | `{5,9,10,11,12}` (`P3`); `{0,1,2,3,4,6,7,8}` (`T0,T1`) | `3-sqrt(5)`, strict |
| 9 | `01+02+23` | `{6,9,10,11,12}` (`P3`); `{0,1,2,3,4,5,7,8}` (`T0,T1`) | `3-sqrt(5)`, strict |
| 10 | `023+12` | `{3,4,5}` (`T1`); `{0,1,2,6,7,8,9,10,11,12}` (`T0,P3`) | `3-sqrt(5)`, strict |
| 11 | `02+03+12` | `{3,4,5}` (`T1`); `{0,1,2,6,7,8,9,10,11,12}` (`T0,P3`) | `3-sqrt(5)`, strict |
| 12 | `02+12+23` | `{3,4,5}` (`T1`); `{0,1,2,6,7,8,9,10,11,12}` (`T0,P3`) | `3-sqrt(5)`, strict |
| 13 | `02+12+23` | `{3,4,5}` (`T1`); `{0,1,2,6,7,8,9,10,11,12}` (`T0,P3`) | `3-sqrt(5)`, strict |
| 14 | `023+12` | `{3,4,5}` (`T1`); `{0,1,2,6,7,8,9,10,11,12}` (`T0,P3`) | `3-sqrt(5)`, strict |
| 15 | `02+03+12` | `{3,4,5}` (`T1`); `{0,1,2,6,7,8,9,10,11,12}` (`T0,P3`) | `3-sqrt(5)`, strict |
| 16 | `02+12+23` | `{3,4,5}` (`T1`); `{0,1,2,6,7,8,9,10,11,12}` (`T0,P3`) | `3-sqrt(5)`, strict |
| 17 | `02+12+23` | `{3,4,5}` (`T1`); `{0,1,2,6,7,8,9,10,11,12}` (`T0,P3`) | `3-sqrt(5)`, strict |
| 18 | `02+13+23` | `{3,4,5}` (`T1`); `{0,1,2,6,7,8,9,10,11,12}` (`T0,P2`) | `3-sqrt(5)`, strict |
| 19 | `02+13+23` | `{3,4,5}` (`T1`); `{0,1,2,6,7,8,9,10,11,12}` (`T0,P2`) | `3-sqrt(5)`, strict |
| 20 | `02+13+23` | `{3,4,5}` (`T1`); `{0,1,2,6,7,8,9,10,11,12}` (`T0,P2`) | `3-sqrt(5)`, strict |

The positive numerical credits are
`5-2sqrt(5)=0.527864045...` and
`3-sqrt(5)=0.763932022...`.

## Why the bouquet fails

In type 1 all four cycles share vertex `0`. Only the packet receiving `0` can
retain any cycle. If it retains both triangles, their triangular credit is
`+1`, but breaking each pentagon leaves at least one nonempty tree component,
for total credit at most `1-1-1=-1`. The exhaustive search checks every
alternative, including a retained pentagon or mixed pair, and finds none is
better. The optimum is `-1`, with strictness inherited from the two-triangle
packet.

## Arbitrary attached trees

The certificate partitions extend over arbitrary trees attached to core
vertices. For every core root `v`, assign the entire off-core rooted branch,
excluding no branch vertices, to the unique packet containing `v`. Every core
vertex belongs to exactly one packet, so there is no case in which a branch
root is "removed" without a destination: removal is only relative to the other
packets. This extension preserves each packet's induced cycle content and the
credit in the table, whose bounds already allow arbitrary tree attachments.

## Reproduction

Run:

```sh
python positive-square-energy/experiments/c3_c3_c5_c5_induced_packet_partitions.py
```

The script prints the canonical cycles, every optimum packet's vertex subset,
cycle content, rule, exact credit, strictness, and the number of admissible DP
transitions. It asserts the 20-core census and the complete score profile. The
expected final line is:

```text
SUMMARY exact_positive=18/20 strict_target=19/20 minimum_score=-1 minimum_decimal=-1.000000000000
```

Here `exact_positive` applies the literal `credit>0` test. `strict_target`
also counts exact zero when at least one packet bound is strict, which still
proves `s+>n`. Only type 1 fails even the latter interpretation.
