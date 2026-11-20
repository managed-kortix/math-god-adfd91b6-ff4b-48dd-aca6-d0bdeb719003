# Cycle 293: a real-center matrix-embedding filter

Scope: one necessary-and-sufficient algebra embedding filter for the outstanding Cycle 292 support census. This is elementary algebra, not a completed census, new Hodge case, or Millennium resolution.

## Lemma
Let F be a totally real number field, let d in Q_{>0}, put K=Q(sqrt(-d)), and let m>=1. There is a unital Q-algebra embedding K -> M_m(F) if and only if m is even.

Indeed x^2+d is irreducible over F: a root would square to a negative number in every real embedding. Given the embedding, its image J satisfies J^2=-d I. Thus F^m becomes a vector space over the quadratic field L=F[x]/(x^2+d), so m=2 dim_L F^m. Conversely, for m=2r, take r diagonal copies of [[0,-d],[1,0]]. This defines a unital embedding. The same argument shows every such J is conjugate under GL_m(F) to that block matrix, by choosing an L-basis and expanding it to an F-basis.

For a simple abelian variety X whose full rational endomorphism algebra End^0(X)=F is a totally real field, End^0(X^m)=M_m(F). Therefore an imaginary quadratic field can act on X^m through its rational endomorphism algebra only with even m. Within an abelian fourfold this leaves, for such an isotypic support, only (dim X,m)=(1,2),(1,4),(2,2). A simple threefold or fourfold whose full rational endomorphism algebra is a totally real field cannot acquire this action merely by occurring as an isotypic support of total dimension at most four.

## Product qualification
Let A be isogenous to its genuine isotypic decomposition product_i X_i^{m_i}, where every X_i is simple, the X_i are pairwise nonisogenous, and every m_i>=1. If K acts through the rational endomorphism algebra of A, composing K -> End^0(A)=product_i M_{m_i}(End^0 X_i) with each coordinate remains unital and hence injective, because K is a field. Consequently the even-m condition applies separately to each support whose full endomorphism algebra is a totally real field, not just to their total multiplicity. Conversely, algebra embeddings on all factors give an embedding into the product, but do not automatically give a polarization compatible with K, Weil signature, discriminant, Hodge-group independence, or algebraic mixed tensors.

This filter does not apply to quaternionic endomorphism algebras or to CM centers: x^2+d can split over a CM center, and quaternionic supports admit additional actions. In particular neither Type-II row from Cycle 292 is deleted. The filter is a preliminary coordinate restriction, not a replacement for rational packet/Tits descent or exact Hodge-circle transport.

## Exact finite artifact
`cycle-293-real-center-filter.py` verifies the block polynomial identity with integer matrices for 1<=r<=4 and 1<=d<=11 and enumerates all dimension/multiplicity pairs up to total dimension four. No floating-point calculation or external dependency is used. The general proof is the vector-space argument above; finite enumeration is only a regression check.

## Next obstruction
For each surviving real-center square support one must still specify the actual rational H^1 packet and its projected Hodge circle, then test every possible rational adjoint graph against quaternionic rows. No graph is discharged by the parity filter alone.
