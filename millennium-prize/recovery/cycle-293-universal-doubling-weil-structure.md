# Cycle 293 candidate: universal discriminant-one Weil structures on even self-products

## Status

This is a self-contained construction that consolidates the even-multiplicity rows of the outstanding abelian-fourfold support census. It is not a Hodge-conjecture theorem: it constructs a Weil-type action and computes its elementary signed discriminant, but says nothing about algebraicity of Weil classes or mixed tensors.

## Theorem

Let `(X,lambda)` be any polarized complex abelian variety of dimension `g`, let `K=Q(eta)` with `eta^2=-d`, `d>0`, and let `r>=1`. Then `A=X^{2r}` admits

1. a unital action `K -> End^0(A)`;
2. a polarization whose Rosati involution restricts to complex conjugation on `K`;
3. balanced signature `(gr,gr)` on `H^{1,0}(A)`; and
4. trivial signed Weil discriminant in `Q^x/N_{K/Q}(K^x)`.

All data are explicit.

## Construction and Rosati check

On each pair of multiplicity coordinates put

`J=[[0,-d],[1,0]],     R=diag(1,d)`.

Use `r` diagonal copies. Then `J^2=-dI`, so `eta -> J` defines the action. Relative to the product polarization, replace the identity multiplicity matrix by the positive symmetric rational matrix `R`. After clearing a positive rational denominator this is a polarization. Its Rosati involution on multiplicity matrices is

`T |-> R^{-1} T^t R`,

and direct multiplication gives

`R^{-1}J^tR=-J`.

Thus Rosati acts as `eta -> -eta`. The two complex eigenvalues of each `J` occur once on the multiplicity pair, so each occurs on `H^{1,0}` with multiplicity `gr`.

This also records an important qualification: an algebra embedding need not be compatible with a preassigned product polarization. For `d=2`, a rational matrix skew under ordinary transpose cannot square to `-2I`; the modified positive matrix `R` is essential.

## Exact discriminant computation

Let `W=H_1(X,Q)`, let `S` be the alternating matrix of the original polarization, and identify the multiplicity space with `K^r` using the basis `(1,eta)` on each pair. Up to a positive rational scalar, the new alternating form is

`E(w tensor u,w' tensor v)=E_X(w,w') Tr_{K/Q}(u bar(v))`.

With the convention `E=Tr_{K/Q}(eta h)`, its associated Hermitian form is, again up to a rational scalar,

`h(w tensor u,w' tensor v)=eta^{-1} E_X(w,w') u bar(v)`.

Its `K`-dimension is `N=2gr`. In a rational basis of `W` and the standard `K`-basis of `K^r`,

`det_K(h)=eta^{-N} det(S)^r`

up to a rational `N`th power. Write `N=2q`, so `q=gr`. Since `det(S)=Pf(S)^2`, the signed determinant is

`(-1)^{N(N-1)/2} det_K(h)
 = (-1)^q eta^{-2q} Pf(S)^{2r}
 = d^{-q} Pf(S)^{2r}`

up to a rational even power. This is

`N_{K/Q}(eta^{-q} Pf(S)^r)`

up to the same harmless rational norm (the displayed expression uses `N(eta)=d`; signs cancel in the signed convention). Hence the signed Weil discriminant is one. Changing between the standard determinant conventions only inserts the already displayed signed factor.

## Census consequence

For any isotypic support `X^m`, every even `m` is automatically admitted at the algebra-action, compatible-polarization, balanced-signature, and discriminant-one gates, without any assumption on `End^0(X)`. In an abelian fourfold this universally handles

- `E^4`;
- `E_1^2 x E_2^2` factorwise;
- `S^2` for an arbitrary abelian surface `S`;
- and an `E^2` coordinate inside a mixed product, provided every other coordinate separately carries the same unital `K` action.

It does not classify odd multiplicities. Those require an internal quadratic action in the relevant endomorphism algebra and a separate positive-involution/signature/discriminant analysis. Nor does the construction establish the actual Hodge group, graph independence, or algebraicity of the resulting exceptional classes.
