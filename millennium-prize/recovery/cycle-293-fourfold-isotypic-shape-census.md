# Cycle 293 candidate: exhaustive isotypic shapes for a fourfold with quadratic action

## Scope

This is a candidate exact isogeny-decomposition census, pending independent audit, at the level of a unital imaginary-quadratic action. It does not classify the action inside each matrix algebra, impose balanced signature or discriminant one, identify Hodge groups, or prove algebraicity of any Hodge class. It is therefore a skeleton for, not a completion of, the missing Cycle 292 support/packet census.

## Theorem

Let `K` be an imaginary quadratic field and let `A` be a complex abelian fourfold with a unital embedding `K -> End^0(A)`. Consolidate its simple isogeny supports:

`A ~ product_i X_i^(m_i)`,

where every `X_i` is simple, the `X_i` are pairwise nonisogenous, and every `m_i>=1`. Then, up to reordering, the isotypic dimension/multiplicity shape is exactly one of the following seven forms:

1. `X_4`, a simple fourfold;
2. `X_3 x E`, a simple threefold and an elliptic curve;
3. `S_1 x S_2`, two nonisogenous simple surfaces;
4. `S^2`, the square of a simple surface;
5. `S x E^2`, a simple surface and an elliptic square;
6. `E^4`;
7. `E_1^2 x E_2^2`, with nonisogenous elliptic curves.

In rows 1--3, every multiplicity-one support must itself admit `K` in its rational endomorphism algebra. In row 2 the elliptic curve has CM by `K`. In row 5 the surface must internally admit `K`, while the even elliptic support need not. Rows 4, 6, and 7 always admit at least one such rational endomorphism-algebra action by universal doubling; other actions may also occur. Polarization compatibility is a separate condition unless the explicit universal-doubling polarization is invoked.

## Proof

Semisimplicity of the isogeny category gives

`End^0(A)=product_i M_(m_i)(D_i)`,  where `D_i=End^0(X_i)`.

The composition of the unital field embedding with every product projection is unital and hence injective. Thus every support separately carries

`K -> M_(m_i)(D_i)`.

The underlying dimension partition of four is one of

`4`, `3+1`, `2+2`, `2+1+1`, or `1+1+1+1`,

with equal simple supports consolidated into multiplicities. The only issue is to rule out elliptic multiplicity patterns `3+1`, `2+1+1`, and `1+1+1+1` involving at least two odd supports.

For an elliptic curve `E`, its rational endomorphism algebra is either `Q` or an imaginary quadratic field `K'`. Suppose `m` is odd and `K -> M_m(End^0(E))`.

- If `End^0(E)=Q`, then `Q^m` would be a vector space over the quadratic field `K`, forcing `m` even, contradiction.
- If `End^0(E)=K'` and `K!=K'`, scalar extension makes `K'^m` a vector space over the quadratic field compositum `KK'/K'`, again forcing `m` even.

Hence an odd elliptic support must satisfy `End^0(E)=K`. Any two complex elliptic curves with rational CM field `K` are isogenous: their lattices are commensurable rank-one `K`-modules after scaling. Therefore two pairwise nonisogenous odd elliptic supports cannot both occur. Consolidating them yields precisely the seven listed shapes.

Conversely, this is a shape census rather than an existence assertion for every row. Rows 4, 6, and 7 have explicit universal-doubling actions. For rows containing odd supports, existence still depends on the stated internal embeddings.

## Balanced-signature refinement

A balanced fourfold action has total tangent multiplicities `(2,2)`. This adds the following necessary bookkeeping but does not classify the rows:

- in `X_3 x E`, the threefold must have multiplicities `(2,1)` or `(1,2)`, and the CM elliptic orientation is the complementary one;
- in `S_1 x S_2`, the two surface signatures must add to `(2,2)`;
- in `S x E^2`, the two support signatures must add to `(2,2)`;
- even-support rows admit an explicit balanced action, but CM centers can also permit nonconjugate unbalanced actions whose total may or may not balance.

The discriminant-one condition is multiplicative on the orthogonal direct sum of support Hermitian forms and remains a separate gate in every row.

## Remaining exact census columns

For each of these seven rows, a complete table must still record:

1. Albert type and actual internal embedding criterion for every odd support;
2. compatible positive involution and all possible signatures;
3. ordinary Hermitian determinant class in `Q^x/N(K^x)`;
4. actual rational Hodge group for every relevant special member;
5. the full rational `H^1` packet, represented commutant, and parametrized Hodge circle;
6. every same/cross-support rational adjoint graph;
7. the algebraicity mechanism for resulting mixed invariants.

No row passes columns 4--7 merely from this shape theorem.
