# Cycle 266: minimal cancellation and failure of minimal H264 survival

## Verdict

In the strict compressed graph Ext algebra, every finite strict twisted complex
is strictly isomorphic to a direct sum

\[
 C\cong C_{\min}\oplus K,
\]

where the twisting matrix of `C_min` has no scalar-unit entries and `K` is a
finite direct sum of elementary two-cell unit cones.  The minimal summand is
unique up to (noncanonical) strict isomorphism.  Endomorphism cohomology, and
every functorial obstruction class in it, is unchanged by deleting `K`.

This reduction does not rescue universal H264 survival.  There is a two-cell,
one-vertex, noncontractible minimal twisted complex on which the H264
diagonal class `alpha=a_1a_2` is exact.

## Complete smallest-packet census

Two cells are the smallest possible nonzero connected packet. Normalize the
source to `F_i[0]` and write the target as `F_j[s]`. A twisting entry `q` has
total degree one precisely when its Ext degree is `1+s`. Since a two-by-two
strictly upper-triangular matrix squares to zero, every nonzero such `q`
satisfies the complete Maurer--Cartan equation; there are no higher products
with two composable twisting entries.

For `i=j`, minimality removes only `Ext^0=K1`, which would have `s=-1` and be
the scalar unit cone. The complete nonunit self-arrow strata are

| arrow space | target shift `s` | dimension |
|---|---:|---:|
| `Ext^1(F_i,F_i)` | 0 | 6 |
| `Ext^2(F_i,F_i)` | 1 | 15 |
| `Ext^3(F_i,F_i)` | 2 | 20 |
| `Ext^4(F_i,F_i)` | 3 | 15 |
| `Ext^5(F_i,F_i)` | 4 | 6 |
| `Ext^6(F_i,F_i)` | 5 | 1 |

Each row denotes the full punctured affine coefficient space, not a sample of
basis arrows. In particular the census includes all self `Ext^1` arrows at
equal shift. For `i!=j`, the only cross group is `Ext^3(F_i,F_j)=K^8`, so the
single cross stratum is

\[
 q\in K^8\setminus\{0\}:F_i[0]\longrightarrow F_j[2].             \tag{266.1}
\]

This includes both shifted cross directions after interchanging the two
vertices. Thus the table and (266.1) exhaust every connected two-cell minimal
Maurer--Cartan packet in the frozen two-vertex compressed algebra, up to common
shift. The first stratum capable of the requested diagonal `Ext^2` cancellation
is the self-`Ext^2`, shift-one row, and it does so exactly below.

## Finite cancellation theorem

Let `A` be the strict compressed category of Cycle 241.  Thus

\[
 A(F_i,F_i)=\Lambda(a_1,\ldots,a_6),\qquad
 A(F_i,F_j)=\operatorname {Ext}^3(F_i,F_j)\quad(i\ne j),
\]

with zero internal differential.  Let `J` be the ideal consisting of all
positive-degree self classes and all cross-vertex classes.  Then

\[
 A/J=\prod_i K1_{F_i}.
\]

Call a finite strict twisted complex minimal when every entry of its twisting
matrix lies in `J`; equivalently, its twisting matrix has no nonzero scalar
multiple of a vertex unit.

**Theorem 266.A (finite unit cancellation).**  Every finite strict twisted
complex `C` over `A` admits a strict isomorphism

\[
 C\cong C_{\min}\oplus
 \bigoplus_{\nu=1}^N
 \left(F_{i_\nu}[r_\nu]\xrightarrow{1}F_{i_\nu}[r_\nu-1]\right). \tag{266.2}
\]

The number of cells decreases by two at every cancellation, so the procedure
terminates.  Any two resulting minimal complexes are strictly isomorphic.

**Proof.** Reduce the Maurer--Cartan matrix `Q` modulo `J`.  Its only possible
entries are scalar units

\[
 F_i[r]\longrightarrow F_i[r-1],
\]

and `Q^2=0` says that these entries form a finite complex of multiplicity
spaces for each `(i,r)`.  Gaussian elimination splits that scalar complex into
its homology and elementary disks.  Lift the scalar basis changes to the full
cell packet.

For one disk, scale its pivot to `1` and use finite upper-triangular row and
column operations to clear every other entry incident with the pivot.  The
remaining twisting matrix is the usual Schur complement.  These operations
are conjugations by invertible degree-zero triangular matrices, and conjugation
preserves `Q^2=0`.  The pivot therefore splits as the displayed unit cone.
Iteration proves existence of (266.1), with a residual matrix whose scalar
reduction is zero.

For uniqueness, a strict isomorphism between two minimal packets reduces
modulo `J` to an isomorphism of their graded multiplicity spaces: the reduced
differentials are zero.  Its scalar matrix is invertible, and the remaining
positive-filtration correction is nilpotent on a finite triangular packet.
Hence the inverse is the finite geometric series.  Equivalently, the standard
minimal-complex argument says that a homotopy equivalence between minimal
packets is already a strict isomorphism.  This proves the theorem.

## Invariance of obstruction cohomology

Each elementary unit cone `K_nu` has a degree-minus-one contraction `h_nu`.
Consequently `End(K)`, `Hom(C_min,K)`, and `Hom(K,C_min)` are contractible.
For example, post- or precomposition with `h_nu`, with the standard Koszul
sign, contracts the corresponding Hom complex.  Therefore inclusion and
projection induce mutually inverse isomorphisms

\[
 H^*End(C)\cong H^*End(C_{\min}).                                  \tag{266.3}
\]

More precisely, if `u:C_min direct-sum K -> C` is the strict cancellation
isomorphism and `p,i` are projection and inclusion, then

\[
 [z]\longmapsto [p u^{-1}zu i]
\]

is (266.2).  Thus any obstruction cocycle natural under strict isomorphism and
homotopy equivalence, including the endomorphism-valued Atiyah obstruction
used in this lane, has the same vanishing or nonvanishing before and after
unit cancellation.  Its component on `K` is necessarily exact.  This is the
precise sense in which obstruction cohomology is invariant; an arbitrary
nonfunctorial choice of cell coefficient is not invariant.

## Minimal counterexample to H264 survival

Put `alpha=a_1a_2` and take

\[
 A=F_0[0],\qquad B=F_0[1],\qquad
 T=(A\oplus B,Q),\qquad Q=\alpha:A\longrightarrow B.              \tag{266.4}
\]

The shift convention gives

\[
 |Q|=2+0-1=1.
\]

The matrix is strictly upper triangular, so `Q^2=0`.  Its only twisting entry
lies in `J`, hence `T` is minimal.  Let

\[
 O=\alpha|_A+\alpha|_B\in End^2(T),\qquad
 G=1_{F_0}:B\longrightarrow A.
\]

Here `|G|=0+1-0=1`.  Exact matrix multiplication gives

\[
 d(G)=QG+GQ=\alpha|_B+\alpha|_A=O.                                \tag{266.5}
\]

Thus the same diagonal `Ext^2` class tested in H264 is exact on a minimal
complex.  The packet is not contractible: exact row reduction gives
`H^0 End(T)` of dimension `7`, so its identity is not a boundary.  It also has
no unit-arrow cell to cancel.

Therefore the exact conclusion is:

**Theorem 266.B.** Minimalization preserves obstruction cohomology, but the
H264 diagonal-dual survival statement does not extend to all finite minimal
twisted complexes.  The minimal packet (266.3) is a counterexample to that
universal mechanism.  It is not a `KI240` counterexample and makes no Hodge
conjecture claim; no class `xi` or relevant projector is asserted for this
two-cell packet.

## Exact verification

Run

```sh
python3 millennium-prize/hodge/verify_cycle266_minimal_counterexample.py
```

The verifier checks degrees, minimality, `Q^2=0`, equation (266.4), `d^2=0`,
and noncontractibility by exact rational row reduction of the full
256-dimensional endomorphism complex (`dim H^0=7`, `dim H^2=41`).
