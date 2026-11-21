# Cycle 293 candidate: universal Weil structures on even self-products

## Status

This is a self-contained candidate construction, pending independent audit, that consolidates the even-multiplicity rows of the outstanding abelian-fourfold support census. It is not a Hodge-conjecture theorem: it constructs a Weil-type action and computes its ordinary Hermitian discriminant, but says nothing about algebraicity of Weil classes or mixed tensors.

## Theorem

Let `(X,lambda)` be any polarized complex abelian variety of dimension `g`, let `K=Q(eta)` with `eta^2=-d`, `d>0`, and let `r>=1`. Then `A=X^{2r}` admits

1. a unital action `K -> End^0(A)`;
2. a polarization whose Rosati involution restricts to complex conjugation on `K`;
3. balanced signature `(gr,gr)` on `H^{1,0}(A)`; and
4. ordinary Weil discriminant class `(-1)^(gr)` in `Q^x/N_{K/Q}(K^x)`; in particular, it is trivial for abelian fourfolds, where `gr=2`.

All data are explicit.

## Construction and Rosati check

On each pair of multiplicity coordinates put

`J=[[0,-d],[1,0]],     R=diag(1,d)`.

Use `r` diagonal copies. Then `J^2=-dI`, so `eta -> J` defines the action. Relative to the product polarization, replace the identity multiplicity matrix by the positive symmetric rational matrix `R`. After clearing a positive rational denominator this is a polarization. Its Rosati involution on multiplicity matrices is

`T |-> R^{-1} T^t R`,

and direct multiplication gives

`R^{-1}J^tR=-J`.

Thus Rosati acts as `eta -> -eta`. The two complex eigenvalues of each `J` occur once on the multiplicity pair, so each occurs on `H^{1,0}` with multiplicity `gr`.

This also records an important qualification: an algebra embedding need not be compatible with a preassigned product polarization. For `d=2`, no rational `2 by 2` matrix skew under ordinary transpose can square to `-2I`; thus the displayed `2 by 2` block requires the modified positive matrix `R`. This does not assert necessity for all embeddings in higher multiplicity dimensions.

## Exact discriminant computation

Let `W=H_1(X,Q)`, let `S` be the alternating matrix of the original polarization, and identify the multiplicity space with `K^r` using the basis `(1,eta)` on each pair. Up to a positive rational scalar, the new alternating form is

`E(w tensor u,w' tensor v)=E_X(w,w') Tr_{K/Q}(bar(u)v)`.

Following van Geemen's convention,

`H(x,y)=E(x,eta y)+eta E(x,y)`

is conjugate-linear in the first variable and `K`-linear in the second. Hence, up to the harmless rational factor coming from whether the trace is normalized by two,

`H(w tensor u,w' tensor v)=eta E_X(w,w') bar(u)v`.

Its `K`-dimension is `N=2gr`. In a rational basis of `W` and the standard `K`-basis of `K^r`,

`det_K(H)=eta^N det(S)^r`

up to a rational `N`th power. Write `N=2q`, so `q=gr`. Since `det(S)=Pf(S)^2`,

`det_K(H)=(-1)^q d^q Pf(S)^(2r)`.

The last two factors are norms: `d^q=N_{K/Q}(eta^q)` and `Pf(S)^(2r)=N_{K/Q}(Pf(S)^r)`. Therefore the ordinary Weil discriminant used by van Geemen is exactly the class

`[det_K(H)]=[(-1)^q]=[(-1)^(gr)]`.

This sign is essential. Norms from an imaginary quadratic field are positive, so `[-1]` is nontrivial. Thus the general even self-product has trivial discriminant exactly when `gr` is even; for an abelian fourfold `2gr=4`, this always holds. An earlier draft incorrectly inserted a signed-determinant convention and thereby claimed triviality in all dimensions; that claim is retracted.

## Census consequence

For any isotypic support `X^m`, every even `m=2r` is automatically admitted at the algebra-action, compatible-polarization, and balanced-signature gates, without any assumption on `End^0(X)`. Its constructed discriminant is `[(-1)^(r dim(X))]`.

For an orthogonal product of independently doubled supports, multiplicativity of the Hermitian determinant gives the explicit formula

`delta(direct_sum_i X_i^(2r_i))=[(-1)^(sum_i r_i dim(X_i))]`.

Consequently:

- `E^4` has class `[(-1)^2]=[1]` for this construction;
- in `E_1^2 x E_2^2`, each doubled elliptic factor contributes `[-1]`, and their product is `[+1]`; this is global cancellation, not factorwise triviality;
- `S^2` for an arbitrary abelian surface `S` has class `[(-1)^2]=[1]`;
- for a mixed product `E^2 x B`, the doubled elliptic factor contributes `[-1]`; global discriminant one requires `B` itself to carry a separately `K`-compatible balanced polarization with `delta(B)=[-1]`. A unital `K` action on `B` alone is insufficient.

More generally, if the total product is an abelian fourfold and every support uses this doubling construction, then `sum_i r_i dim(X_i)=2`, so the global class is one. The theorem does not classify odd multiplicities or mixed products in which another factor uses a different action or polarization. Those require an internal quadratic action in the relevant endomorphism algebra and a separate positive-involution/signature/discriminant analysis. Nor does the construction establish the actual Hodge group, graph independence, or algebraicity of the resulting exceptional classes.
