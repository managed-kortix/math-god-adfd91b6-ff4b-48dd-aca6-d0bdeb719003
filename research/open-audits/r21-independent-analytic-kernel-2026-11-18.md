# R21 independent analytic kernel and finite replay

Date: 2026-11-18. Status: **NONPROMOTIONAL SOURCE AUDIT**.

Write `sigma(X)=s+(X)-|V(X)|`. The exact cited source calls the class a
**connected triangular block graph** and defines this to mean that every
cyclic block is a literal `C3`, with bridge blocks and arbitrary finite
attached trees allowed. Every such graph is a cactus; below “triangular
cactus” is only shorthand for that exact class. It does **not** mean a generic
block graph with arbitrary clique blocks.

## Minimal independent kernel

The analytic inputs needed by the `R21` territory ledgers have the following
acyclic dependency graph.

1. **Packing-two sign and triangular territories.** The sign theorem in
   `packing-two-square-energy/paper.tex` says `D=s+-s->0` when every cycle is
   `3 mod 4` and the vertex-disjoint cycle packing number is at most two.
   Corollary `cor:triangular-block`, using the preceding maximum-packing
   territory lemma, specializes exactly to a connected triangular block graph:
   each induced territory is connected, cyclic, has packing number one, and
   still has only `C3` cycles. Hence

   ```text
   s+(H_i)>s-(H_i),  s+(H_i)+s-(H_i)=2|E(H_i)|,
   |E(H_i)|>=|V(H_i)|,
   ```

   so `sigma(H_i)>0`; induced-subgraph superadditivity gives
   `sigma(H)>0`. The same sign theorem applied directly to a connected cactus
   with exactly two triangular blocks gives `|E|=|V|+1`, hence `sigma>1`,
   uniformly over the bridge connector and all attached trees.

2. **The independent `A4` base.** If four triangles form one shared-cut
   cluster and their packing number is at most two, the same sign theorem and
   `|E|=|V|+3` give `sigma(A4)>3`. Packing number four is incompatible with
   one shared-cut cluster. In the remaining packing-three incidence, the
   triangle intersection graph is the central-triangle/three-petal star. The
   structural classification and direct matching injection in Proposition 4.11
   of the packing-two source prove

   ```text
   sum(j=0..3) Z(G-V(T_j)) > 4 Z(F),
   Im Psi = -2 sum(j=0..3) Z(G-V(T_j)) + 8 Z(F) < 0.
   ```

   Coulson's identity again gives `D>0`, hence `sigma(A4)>3`. This narrow
   extraction does not use the other, disconnected-cluster branches of that
   proposition.

3. **Shared-triangle leaf opening.** Lemma `lem:triangle-recurrence` in
   `all-heptacyclic-cacti/paper.tex` opens a private vertex of an
   incidence-leaf triangle. The opened induced territory is a nonempty tree
   of exact credit `-1`; the complement is an `A_(r-1)` packet. Therefore

   ```text
   sigma(A_r) >= sigma(A_(r-1)) - 1.
   ```

   Strictness from the independent base propagates exactly as

   ```text
   b4=3  ->  b5=2  ->  b6=1,
   sigma(A4)>3, sigma(A5)>2, sigma(A6)>1.
   ```

   **Circularity audit:** this recurrence occurs before the heptacyclic main
   theorem and does not invoke it. Its proof uses only induced
   superadditivity, the private-opening lemma, and the `A4` base supplied by
   the packing-two sign theorem plus the central-triangle matching injection.
   It does not use the heptacyclic conclusion or a qualitative rank-five or
   rank-six theorem.

4. **Exactly six triangles.** Partition the six cyclic blocks into maximal
   shared-cut clusters. If a cluster has size at least two, its strict floor
   is one of

   ```text
   j:                 1  2  3  4  5  6
   sigma(A_j) > b_j:  0  1  2  3  2  1.
   ```

   Thus that territory contributes strictly more than one and every other
   cyclic territory is a connected triangular block graph (equivalently here,
   a triangular cactus) of positive credit. If all six
   clusters are singletons, retain the connector path between two nearest
   marked nodes; it is the two-triangle packet of credit `>1`, while the four
   remaining cyclic territories are connected triangular block graphs of
   positive credit.
   Consequently every connected cactus with exactly six triangular cyclic
   blocks has `sigma>1`. The physical reduced-tree/actual-bridge territory
   lemma is essential here; the integer-partition ledger alone does not prove
   ownership, inducedness, or exhaustiveness.

5. **Hostile `C5` one-root floor.** Lemma `lem:packets(2)` in
   `all-tricyclic-cacti/paper.tex` eliminates every attached tree by the exact
   branch recurrence, obtaining activities `a_v=t+y_v>=t`. Its phase
   comparison

   ```text
   Psi/K = Z_Cq(a)+2i,
   Arg(Psi/K) <= Arg(Z_Cq(t)+2i)
   (with the continuous arguments normalized to 0 at infinity),
   ```

   and Coulson integration prove, for a unicyclic `C_q` cactus with arbitrary
   tree attachments and `q=1 mod 4`,

   ```text
   s+ >= h-[sec(pi/q)-1].
   ```

   At `q=5`, `sec(pi/5)-1=sqrt(5)-2`, so

   ```text
   sigma >= 2-sqrt(5)=-(sqrt(5)-2)>-1.
   ```

   The first comparison is non-strict: bare `C5` has
   `s+(C5)=7-sqrt(5)` and attains equality. **Circularity audit:** the tree
   elimination and phase proof is inside the packet lemma, before and
   independent of the tricyclic main theorem.

These arrows contain no use of the heptacyclic main theorem, the tricyclic
main theorem, the rank-seven theorem, or an `R21` closure assertion. The
universal ingredients that remain theorem proofs, rather than finite
calculation, are the packing-two sign theorem, induced superadditivity,
maximum-packing and physical actual-bridge territory constructions, the
private leaf opening, and the tree-elimination/phase comparison.

## Finite verifier and trust boundary

Run from the repository root:

```text
python3 research/r21-independent-analytic-kernel-verifier.py
python3 -O research/r21-independent-analytic-kernel-verifier.py
```

The dependency-free standard-library verifier fails closed unless the exact
source bytes, byte lengths, line counts, and semantic tokens match. The three
source receipts are:

```text
9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791  44126 bytes  1043 lines  packing-two-square-energy/paper.tex
9323dc212d36b610a66e890df3a267242ae0800efcd445dd911575cc2bd9a4d1  31896 bytes   730 lines  all-heptacyclic-cacti/paper.tex
d928a56b0257936fcc326ddc2c85e40593117a7749b55502bb42379c805e71e8  17669 bytes   434 lines  all-tricyclic-cacti/paper.tex
```

The verifier then checks:

* source ordering and the absence of a main-theorem citation in the extracted
  recurrence and `C5` packet proof slices;
* the four-node intersection-graph classification (connected packing three
  forces `K1,3`), the central-star coefficient implication, and the exact
  recurrence `3 -> 2 -> 1`;
* all 11 integer partitions of six and the singleton nearest-pair ledger;
* the triangular-territory applications used by the owner-fibre ledgers;
* the exact `C5` characteristic-polynomial factorization, positive square
  energy, secant identity, and radical inequalities in `Q(sqrt(5))`.

On the pinned bytes, the normal and `python3 -O` runs are required to be
byte-identical; the tested output SHA-256 is recorded with the commit report.

This is a verifier of the **finite logical kernel and source receipts only**.
No finite run proves the universally quantified spectral sign theorem, the
territory lemmas, arbitrary attachments/connectors, private-opening validity,
or the tree-elimination phase theorem. It is not a proof of all `R21`, does
not promote a master theorem, and changes no state or publication file.
