# Cycle 264: minimal shifted-return endomorphism test

## Frozen model

Work over `K=Q(i)` with two vertices `F_0,F_1` and the compressed Ext algebra
of Cycle 241:

\[
 \operatorname {Ext}^*(F_i,F_i)=\Lambda(a_1,\ldots,a_6),
 \qquad \operatorname {Ext}^3(F_i,F_j)=K^8\quad(i\ne j),
\]

with all other cross Ext groups zero and normalized products

\[
 x_{10,s}x_{01,t}=\delta_{st}\omega _0,
 \qquad x_{01,t}x_{10,s}=-\delta_{st}\omega _1.
\]

This is frozen as the strict minimal `A_infinity`/DG model with `m_1=0`,
`m_2` equal to the displayed Yoneda algebra, and `m_n=0` for `n>=3`.

Freeze `A=F_0[0]`, `B=F_1[2]`, and `C=F_0[4]`. Both
`x=x_(01,0):A->B` and `y=x_(10,0):B->C` have total degree one. The two-arrow
matrix `x+y` is not Maurer--Cartan because `yx=omega_0`. The minimal valid DG
object retaining the complete return in its total endomorphism complex is

\[
 T=(A\oplus B\oplus C,Q),\qquad Q=x:A\longrightarrow B.
\]

Here `Q^2=0`, while `y` remains a degree-one endomorphism of `T`.

## Total endomorphism complex

The verifier constructs all 352 basis elements in `End^*(T)`. Same-support
blocks contain all 64 exterior monomials and cross blocks contain the eight
degree-three generators. For homogeneous `f`,

\[
 d_{End}(f)=Qf-(-1)^{|f|}fQ.
\]

The JSON artifact gives every graded dimension, exact differential rank, and
cohomology dimension, computed by rational row reduction. It also verifies
`d_End^2=0` on the complete complex.

The support-return top class is killed:

\[
 d_{End}(y)=Qy+yQ=yx=\omega _0:A\longrightarrow C.
\]

Thus the return occurs as an actual differential, not merely as the curvature
of the invalid two-arrow candidate.

## Diagonal obstruction survives

Let `alpha=a_1a_2` and take the cell-diagonal degree-two cocycle

\[
 O=\alpha|_A+\alpha|_B+\alpha|_C.
\]

Products of a positive-degree self class with a cross class vanish because
they would lie in cross Ext above degree three. Hence `d_End(O)=0`.

Define `lambda_A` to extract the coefficient of `alpha:A->A`. Construction of
the entire map `d_End:End^1(T)->End^2(T)` gives

\[
 \lambda_A d_{End}=0,
 \qquad \lambda_A(O)=1.
\]

Therefore `lambda_A` is a chain-level dual cocycle proving `[O]` is nonzero in
`H^2 End(T)`. The diagonal `Ext^2` obstruction survives, although the
cell-off-diagonal top return `omega_0:A->C` is the boundary `d(y)`.

This is exactly the bounded `H264-KI-MIN` mechanism test and stops at this
three-cell, two-vertex model. It is not `KI240 PASS`, does not decide arbitrary
finite packets or retracts, and makes no Hodge-conjecture claim.

## Exact verification

Run

```sh
python3 millennium-prize/hodge/verify_cycle264_ki_min.py
python3 millennium-prize/hodge/verify_cycle264_ki_min.py --check
```

The first command deterministically writes `cycle264_ki_min.json`; the second
checks byte-for-byte reproduction and all embedded algebraic assertions.
