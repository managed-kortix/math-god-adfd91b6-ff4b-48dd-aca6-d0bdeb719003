# Cycle 293 candidate: Type-I matrix supports on the balanced Weil locus

## Status and scope

This is a candidate direct algebraic filter and construction, pending independent audit, for the totally-real-field (Albert Type I) part of the outstanding abelian-fourfold support census. It does **not** certify that Cycles 288/291/292 are correct, complete the rational packet census, prove a new Hodge-conjecture case, or resolve the Hodge conjecture. It deliberately does not alter `MILLENNIUM_STATE.md`.

Let `K=Q(eta)` with `eta^2=-d`, `d in Q_{>0}`, and let `F` be a totally real number field.

## 1. Unital embedding and conjugacy lemma

There is a unital `Q`-algebra embedding

`K -> M_m(F)`

if and only if `m` is even. When `m=2r`, all such embeddings are conjugate under `GL_m(F)`.

Proof. The polynomial `T^2+d` is irreducible over `F`: a root in `F` would have negative square under every real embedding. Scalar matrices from `F` commute with the image of `K`, so an embedding makes `F^m` a vector space over the field `L=F(eta)=F tensor_Q K`, of `F`-degree two. Hence `m=2 dim_L(F^m)` is even. Conversely, for `m=2r`, use `r` copies of

`J=[[0,-d],[1,0]]`, for which `J^2=-d I`.

Any two embeddings give two `L`-vector-space structures of the same dimension `r` on `F^m`. An `L`-linear isomorphism between them is an element of `GL_m(F)` conjugating one embedding to the other. This also shows why total reality matters: if `K` is already contained in the center, odd `m` is possible.

Let `A` have its genuine isotypic decomposition `A ~ product_i X_i^{m_i}`, where every `X_i` is simple, the `X_i` are pairwise nonisogenous, every `m_i>=1`, and `End^0(X_i)=F_i` is a totally real field. Then

`End^0(A)=product_i M_{m_i}(F_i)`.

Every coordinate of a unital embedding of the field `K` into this rational endomorphism algebra is itself unital, hence injective. Therefore every `m_i` is even separately. This is not merely a parity condition on their sum. Opposite-ring conventions do not change the conclusion because each `F_i` is commutative and `M_m(F_i)^op` is isomorphic to `M_m(F_i)`.

## 2. Compatible polarization exists, but need not be the fixed product polarization

Let `(X,lambda)` be polarized and suppose `F subset End^0(X)` is fixed pointwise by Rosati (as in the Type-I setting). On `A=X^{2r}`, let `K` act through the block matrix `J` above. Relative to the product polarization, choose the positive symmetric multiplicity matrix

`R=diag(1,d)`

on each block (and clear rational denominators by one positive integer). The resulting Rosati involution on multiplicity matrices is

`alpha |-> R^{-1} alpha^t R`,

and direct multiplication gives

`R^{-1} J^t R=-J`.

Thus Rosati induces complex conjugation on `K`, so the altered polarization is `K`-compatible. This qualification is essential. For example, with `d=2`, no rational `2 by 2` matrix can both be skew under the **standard** transpose involution and square to `-2I`: a rational skew matrix is `[[0,a],[-a,0]]` and its square is `-a^2 I`. The algebra embedding exists, but compatibility with that fixed product polarization does not.

On `H^{1,0}(A)`, the two eigenvalues of `J` each have multiplicity `gr`, where `g=dim X`. Hence the constructed action has balanced signature `(gr,gr)`.

## 3. Trivial discriminant for the constructed fourfolds

Assume `dim A=2gr=4`. Let `W=H_1(X,Q)` and let `S` be the rational alternating matrix of `lambda`; `dim_Q W=2g`. Identify the multiplicity space with `K^r`. Up to a harmless positive rational scale, the constructed alternating form is

`E(w tensor u, w' tensor v)=E_X(w,w') Tr_{K/Q}(u bar(v))`.

With the convention

`E(x,y)=Tr_{K/Q}(eta h(x,y))`,

the associated `K`-Hermitian form is

`h(w tensor u,w' tensor v)=eta^{-1} E_X(w,w') u bar(v)`.

It is Hermitian because both `eta^{-1}` and `E_X` change sign under conjugation/transposition. In a rational basis of `W` and the standard `K`-basis of `K^r`,

`det_K(h)=eta^{-4} det(S)^r`.

An alternating matrix has `det(S)=Pf(S)^2`; moreover `eta^{-4}=d^{-2}`. Therefore

`det_K(h)=(Pf(S)^r/d)^2=N_{K/Q}(Pf(S)^r/d)`.

The Weil discriminant class is consequently trivial for this constructed polarization. Since the fourfold has `K`-dimension four, the usual possible signed-determinant convention has the same sign here. This calculation establishes existence of a compatible discriminant-one structure; it is not a classification of every polarization.

## 4. Dimension-four Type-I inventory

For one consolidated Type-I isotypic support `X^m` of dimension at most four, the even-multiplicity condition leaves exactly

`(dim X,m)=(1,2),(1,4),(2,2)`.

If the whole abelian fourfold has only Type-I simple supports, consolidation and the requirement on every coordinate leave the following shapes:

1. `E^4`;
2. `E_1^2 x E_2^2` with `E_1,E_2` nonisogenous; under the displayed doubling construction each factor has class `[-1]`, while the global discriminant is one because `[-1]·[-1]=[1]`, not because either factor is trivial;
3. `S^2` for a simple Type-I abelian surface `S`.

Mixed products may combine a Type-I `E^2` support with a two-dimensional support of another Albert type; this note says nothing about that other coordinate. A simple Type-I threefold or fourfold, or a multiplicity-one Type-I surface, cannot acquire the required unital `K` action inside its own isotypic matrix algebra.

## 5. Remaining gates

This closes only an elementary matrix/polarization row. It does not establish:

- the exhaustive inventory for quaternionic or CM supports;
- the actual rational Hodge group or represented commutant for every special member;
- rational packet/Tits descent;
- equality of parametrized projected Hodge circles in a proposed Goursat graph;
- algebraicity of cross-support tensors;
- any new case of the Hodge conjecture.

The finite companion script checks the matrix, Rosati, determinant-square, and dimension-enumeration identities using exact rational/integer arithmetic. The proof above, not the finite check, establishes the general statements.
