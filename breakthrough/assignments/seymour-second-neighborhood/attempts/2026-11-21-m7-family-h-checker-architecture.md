# Independent checker architecture for order-18 family H

## Status and exact scope

This note freezes an integration-ready **formula-identity checker and exact
q-incidence census** for the two mixed-witness family-H CNFs.  It does not
retain or certify an UNSAT proof.  Therefore it is not a family-H elimination,
an order-18 result, an `m=7` result, or a result on Seymour's conjecture.

The intended family-H chain is

```text
v -> q -> r,
```

where `q,r` are the two outdegree-nine vertices, `v` is a low robust witness
for deleting `q`, and `q` is the high robust witness for deleting `r`.  The
normalization is

```text
v=0, q=1,
A=N+(v)={1,...,8},
B=N++(v)={9,...,15},
C={16,17},
```

with the two exhaustive locations

```text
case A: r=2 in A,
case B: r=9 in B.
```

The checker deliberately does not import `snc_cnf.py` or an eventual
family-H producer.  It reconstructs the variable order and every clause from
scratch.  The census likewise imports no producer or row generator.

Files:

```text
experiments/check_m7_family_h_cnf.py
experiments/m7_family_h_census_check.py
experiments/test_m7_family_h_checker_mutations.py
experiments/test_m7_family_h_census.py
```

## 1. Reconstructed CNF contract

For each ordered pair `i,j`, the checker allocates:

```text
a_i_j : i -> j,
q_i_j : j is an exact second outneighbor of i,
p_i_k_j : a_i_k AND a_k_j,
r_i_j : OR_k p_i_k_j.
```

It reconstructs all of the following, in exact clause order.

1. **Oriented-pair trichotomy.**  Loops and digons are forbidden.  For each
   unordered pair, `h_i_j` is biconditional to neither arc being present.
   Together these clauses admit exactly forward arc, reverse arc, or hole.
2. **Exact second neighborhood.**  Every `p` is an AND gate, every `r` is the
   exact OR of all allowed two-walk intermediaries, and
   `q_i_j <-> r_i_j AND NOT a_i_j`.  Direct outneighbors never count as exact
   second neighbors.
3. **Global degree/badness envelope.**  Exact unary counters impose outdegree
   eight or nine, positive deficit at most two, and the exact high mask
   `{q,r}`.  Thus every vertex is globally strict-bad in the encoded
   relaxation.
4. **Exactly seven holes.**  An exact unary counter is applied to all 153
   biconditional hole variables.
5. **Exact low-root layers.**  Units impose `N+(v)=A` and `N++(v)=B`.  The
   standard support clauses impose `A -> B` coverage, and units forbid
   `A -> C`.
6. **V-Rob.**  For each `b in B`, at least one vertex of `A\{q}` points to
   `b`.  This is exactly preservation of the old `N++(v)=B` after deleting
   `q`.
7. **Q-Rob.**  The chain unit `q->r` is present.  For every
   `x notin {q,r}`, `q_x` implies a two-walk `q->k->x` with
   `k notin {q,r,x}`.  This is exactly preservation of every surviving old
   exact second neighbor after deleting `r`.
8. **q-status sorting.**  Within each of the three uniform blocks, adjacent
   clauses sort the pair statuses `O<I<H`.

Both reconstructions have exactly

```text
variables = 23,310
clauses   = 90,451
sorting clauses = 24.
```

### Deliberate relaxation

An actual high witness `q` is tight, so `d++(q)=8`.  The formula allows either
seven or eight exact second neighbors at `q`, as permitted by the global
deficit-in-`{1,2}` envelope.  This only enlarges the model class and is safe
for a future UNSAT reduction.  Full arc minimality, unrelated deletion
witnesses, and strong connectivity are also omitted.

## 2. Strict formula envelope

The checker supports exactly two explicit envelopes:

```text
--envelope mapped
--envelope bare
```

`mapped` requires the complete canonical sequence
`c var <id> <name>` before the header.  `bare` forbids comments and starts with
the header.  There is intentionally no auto-detection.  Both then require:

- ASCII with LF newlines and one final newline;
- no tabs, blank lines, duplicate headers, leading-zero integers, or irregular
  spaces;
- exact dimensions and literal range;
- exact reconstructed clause sequence;
- exact canonical bytes.

A future manifest must bind one envelope, rather than treating mapped and bare
files as byte-identical.  Proof replay remains a separate obligation.

## 3. Exact 168-row census

For `x != q`, classify the pair with `q` as

```text
O : q -> x,
I : x -> q,
H : q--x is a hole.
```

The distinguished statuses are fixed:

```text
v : I,
r : O,
C vertices : I or H.
```

The two cases have blocks

```text
case A: G1=A\{q,r}, |G1|=6; G2=B,       |G2|=7;
case B: G1=A\{q},   |G1|=7; G2=B\{r},   |G2|=6.
```

Write `(o_i,i_i,h_i)` for a block's status multiplicities and `h_C` for
the number of C holes.  The exact row constraints are

```text
o_1+o_2=8,
h_1+h_2+h_C<=7.
```

The first equation follows because `q->r` is the ninth outarc.  The second is
exactly the global seven-hole upper bound on the q-incident subset.  Direct
integer enumeration independently yields, in either case,

```text
168 status orbits.
```

Their labelled multiplicity is

```text
sum multinomial(|G1|; o1,i1,h1)
  * multinomial(|G2|; o2,i2,h2)
  * binomial(2,h_C)
= 164,736.
```

The census also exhausts all `3^13 * 2^2` candidate labelled block words,
filters the exact family-H rows, and obtains the same 164,736 directly.

The historical 330-row generator was a strict overcover:

```text
168 actual rows with v->q
+ 162 impossible rows with v-q a hole
= 330.
```

Only the 168 actual rows belong to family H.

## 4. Sorting is a valid canonicalization

Use `O<I<H`.  For consecutive block labels `u,w`, the clauses are

```text
-not a_qw OR a_qu,
-not a_wq OR a_qu OR a_uq.
```

A truth table over the nine ordered status pairs proves that these accept
exactly the six nondecreasing pairs and reject exactly

```text
(I,O), (H,O), (H,I).
```

The checker then exhausts every valid labelled q-incidence row.  Stable sorting
constructs an explicit permutation in each of

```text
S_G1 x S_G2 x S_C.
```

It verifies that this permutation preserves the row key and reaches the unique
sorted status word.  Conversely, block permutations preserve status counts.
Thus sorting is a valid transversal for q-status-count orbits.  This does not
claim a unique representative for full graph-isomorphism orbits.

The whole unsorted family-H formula is invariant under the same block group:
all root-set units, degree/hole constraints, exact-distance definitions,
V-Rob, Q-Rob, and the distinguished `q->r` chain are quantified uniformly on
these blocks.  Hence adding sorting cannot discard a satisfying graph up to
allowed relabelling.

## 5. Fail-closed audits

All checks use explicit `if`/exception logic; no correctness condition uses
Python `assert`.  The tests run every baseline in normal and optimized Python
and require identical output.

The semantic self-audit independently truth-tables or exhausts:

- AND and OR gates;
- the exact-distance-two biconditional;
- oriented-pair trichotomy;
- exact unary counters through width four, including all auxiliary assignments;
- the deficit-two linkage for every relevant degree pair at width seventeen;
- Q-Rob versus exact second-neighborhood equality after deletion on all
  four-vertex oriented graphs with `q->r`.

Hostile candidates alter dimensions, envelope form, newlines, clause count,
loops/digons, exact-N++ linkage, high mask, hole cardinality, V-Rob, `q->r`,
Q-Rob, and sorting.  Every mutation is rejected in both normal and `python -O`
execution.

## 6. Reproduction commands

From `experiments/`:

```sh
python3 -B m7_family_h_census_check.py
python3 -O -B m7_family_h_census_check.py
python3 -B test_m7_family_h_census.py
python3 -B test_m7_family_h_checker_mutations.py

python3 -B check_m7_family_h_cnf.py CASE_A.cnf \
  --case A --envelope mapped
python3 -O -B check_m7_family_h_cnf.py CASE_B.cnf \
  --case B --envelope mapped
```

The checker output includes formula dimensions and SHA-256, but a durable
certificate package must separately bind source identities, the selected
envelope, CNF hashes, proof hashes, pinned solver/checker binaries, and fresh
proof-checker output.
