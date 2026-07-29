# Cycle 110: rigorous RM seed and symbolic contraction theorem

## Bring's curve supplies elementary RM data

Let Bring's genus-four curve be
\[
 C:\quad \sum_{i=1}^5x_i=\sum_{i=1}^5x_i^2
 =\sum_{i=1}^5x_i^3=0\subset\mathbf P^4.
\]
Inside the hyperplane `sum x_i=0`, this is a canonical `(2,3)` complete
intersection.  The quadric `sum x_i^2=0` is nondegenerate in characteristic
zero, so `C` has the required two geometric trigonal pencils.

Let `r=(12345)` act on `C` and its principally polarized Jacobian, and put
\[
 a=r+r^{-1}.
\]
On the four-dimensional standard representation `H^0(C,K_C)`, the eigenvalues
of `r` are the nontrivial fifth roots of unity.  Hence
\[
 a^2+a-1=0.
\]
The action is faithful on Jacobian endomorphisms, yielding an exact Rosati-
self-adjoint embedding `Q(sqrt(5)) -> End^0(J(C))`.  Set
\[
 f=a^2=1-a.
\]
Then
\[
 f^2-3f+1=0,\qquad f^{-1}=3-f,
\]
so `f` is an integral norm-one abelian-variety automorphism with `f^2!=1`.
This rigorously supplies the elementary RM-unit and two-pencil data.  It does
not supersede the heuristic HPS candidate as a full Markman instance:
`J(Bring)` is isogenous to a fourth power of an elliptic curve, is not simple,
and has endomorphism algebra much larger than `Q(sqrt(5))`.  Markman's generic
secant-space argument uses the simple, RM-only setting, so its nonzero Weil
projection cannot be imported without a new invariant calculation.

## Uniform rank theorem

Over any characteristic-zero field, let the RM eigenvalues on `H^(1,0)` be
\[
 (\lambda,\lambda,\lambda^{-1},\lambda^{-1}),
 \qquad \lambda^8\ne1,
\]
and let `q,N` be nonzero.  For
\[
 \Gamma=N\left(g^*\Theta-\frac q6(g^{-1})^*\Theta^3\right),
\]
the Chern-contraction map on
\[
 H^2(\mathcal O)\oplus H^1(T)\oplus H^0(\wedge^2T)
\]
has rank `20` and nullity `8`.

Indeed, put `a_i=lambda_i^2`, `c_i=lambda_i^-2`, and
`r_i=a_i/c_i=lambda_i^4`.  The middle and outer maps each split into six
two-column blocks.  Their determinants are nonzero multiples of `r_i-r_j` or
the corresponding complementary-pair difference.  Exactly two blocks in each
map have equal ratios and rank one; four have unequal ratios and rank two.
Thus both ranks equal `2*1+4*2=10`.

The exact verifier now includes arbitrary nonzero `q`, correct bivector
contraction order, and cancellation-safe sparse forms.  Its rational
specialization certifies a nonzero `20 x 20` minor, while the symbolic ratio
identities give the universal upper bound `20`; together these certify the
generic theorem.

## Remaining gate

The semiregularity problem remains separate from the elementary RM identities.
One must first find a rigorous seed satisfying Markman's full generic
endomorphism hypotheses, then instantiate the secant/gluing sheaf and prove
that its generalized Atiyah obstruction map has rank `20` and the verified
eight-dimensional Chern kernel.  Bring's extra endomorphisms prevent treating
it as that generic family seed without additional work.  No Hodge case is
claimed.
