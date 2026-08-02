# Cycle 265: bounded continuation of H264-KI-MIN

## Question and verdict

Remain inside the strict two-vertex compressed Ext algebra frozen in
`H264-KI-MIN`; in fact, use only the self algebra at `F_0`. The explicit
dual-cocycle mechanism from the valid three-cell object does **not** extend to
every strict finite twisted complex. A two-cell contractible packet makes the
same cell-diagonal degree-two class exact.

This is a counterexample only to the proposed universal survival mechanism in
the compressed model. It is not a `KI240` counterexample: the packet is the
zero object, has zero Grothendieck class, and carries no projector of class
`xi`.

## Exact counterpacket

Work over `K=Q(i)` and put

\[
 A=F_0[0],\qquad B=F_0[-1],\qquad T=(A\oplus B,Q),
 \qquad Q=1_{F_0}:A\longrightarrow B.
\]

With the convention

\[
 \operatorname {Hom}^d(F_i[r],F_j[s])
 =\operatorname {Ext}^{d-r+s}(F_i,F_j),
\]

the unit `Q` has total degree one. In the cell order `A<B` it is strictly
upper triangular, and `Q^2=0`, so `T` is a valid finite strict twisted
complex. Let

\[
 h=1_{F_0}:B\longrightarrow A.
\]

Then `|h|=-1` and

\[
 Qh+hQ=1_T.                                                     \tag{265.1}
\]

Thus the packet is contractible.

Take the same self-Ext class `alpha=a_1a_2` used in `H264-KI-MIN` and form

\[
 O=\alpha|_A+\alpha|_B\in\operatorname {End}^2(T).
\]

The class is a cocycle because the even natural diagonal action of `alpha`
commutes with `Q`. Define the degree-one endomorphism

\[
 G=\alpha h:B\longrightarrow A.
\]

The endomorphism differential is

\[
 d(f)=Qf-(-1)^{|f|}fQ.
\]

Since `|G|=1`, exact matrix multiplication gives

\[
 d(G)=QG+GQ=\alpha|_B+\alpha|_A=O.                              \tag{265.2}
\]

Hence `[O]=0` in `H^2 End(T)`. More generally, (265.1) contracts the whole
endomorphism complex: for a homogeneous closed `f`, the degree `|f|-1` map
`(-1)^{|f|}fh` is a primitive up to the equivalent left/right sign
convention. Direct exact row reduction confirms that every cohomology group of
`End(T)` vanishes.

## Why the H264 functional does not continue

Let `lambda_A` extract the coefficient of `alpha:A->A`, exactly as in the
three-cell test. Equation (265.2) gives

\[
 \lambda_A(dG)=1.
\]

Therefore `lambda_A` is not a dual cocycle on this packet. The difference is
visible at the first filtration step: the scalar unit arrow `Q` has a reverse
degree-minus-one contraction, and composing that contraction with `alpha`
lands in degree one. In `H264-KI-MIN`, the only twisting arrow was cross-vertex
and a positive self class times a cross class vanished, so no analogous
degree-one primitive could hit the extracted `alpha` coefficient.

A trace argument cannot repair the universal claim. The contractible pair has
opposite cohomological parity, so the graded trace of the diagonal packet is
`str(O)=alpha-alpha=0`; equation (265.2) is correspondingly compatible with
the fact that graded traces kill commutators.

## Sharp scope

The universal assertion over **all** strict finite twisted complexes is false
unless one first cancels scalar contractible pairs or imposes a minimality
hypothesis. This packet says nothing about survival on every finite minimal
packet; opposite cross arrows and self-Ext twisting terms still make that a
separate problem. No `KI240` or Hodge-conjecture claim is made.

## Exact verification

Run

```sh
python3 millennium-prize/hodge/verify_cycle265_h264_continuation.py
python3 millennium-prize/hodge/verify_cycle265_h264_continuation.py --check
```

The verifier constructs all 256 basis elements of `End(T)`, checks `Q^2=0`,
`d^2=0`, equation (265.2), the failure of the H264 coefficient functional, and
zero cohomology by exact rational row reduction.
