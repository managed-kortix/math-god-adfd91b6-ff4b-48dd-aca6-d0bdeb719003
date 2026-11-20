# Cycle 293 candidate: quadratic actions on quaternionic isotypic supports

## Status

This is the algebra-embedding layer of the outstanding abelian-fourfold support census. It is independent of the unvetted Type-II discriminant formulas in preserved Cycle 292. It does not prove compatibility of a multiplicity-one action with a positive involution, calculate its Weil discriminant, identify its actual Hodge group, or prove any Hodge-conjecture case.

Let `F` be totally real, let `D/F` be a quaternion algebra, let `K=Q(sqrt(-d))` be imaginary quadratic, and set `L=FK`. Since `F` is totally real, `F intersect K=Q`, so `L/F` is a quadratic field extension.

## Embedding criterion

There is a unital `Q`-algebra embedding

`K -> M_m(D)`

if and only if either

1. `D tensor_F L` is split, or
2. `m` is even.

All such embeddings are conjugate by `M_m(D)^x`.

### Proof

Because `F` is central, a unital `Q`-embedding of `K` extends uniquely to a unital `F`-embedding

`L=F tensor_Q K -> M_m(D)`.

Conversely, restriction gives the original action.

If `D_L` is split, the standard maximal-subfield criterion for quaternion algebras gives an `F`-embedding `L -> D`; diagonal repetition gives an embedding into `M_m(D)` for every `m`.

If `m=2s`, no splitting assumption is needed: map `sqrt(-d)` to `s` diagonal copies of

`[[0,-d],[1,0]] in M_2(F) subset M_2(D)`.

For necessity in the remaining case, suppose `D_L` is division and let `V=D^m` be the right `D`-module on which `M_m(D)=End_D(V)` acts. An embedding of `L` makes `V` an `(L,D)`-bimodule, hence a module over the division algebra

`L tensor_F D^op = D_L^op`.

As an `L`-vector space, `V` has dimension `2m`; as a module over the four-dimensional `L`-division algebra `D_L^op`, its `L`-dimension is divisible by four. Therefore `m` is even.

Finally, `L/F` is separable and `M_m(D)` is central simple over `F`, so Skolem--Noether conjugates any two `F`-embeddings of `L`. This also conjugates the corresponding `K` actions.

Equivalently, the general central-simple embedding criterion here is

`ind(D_L) | m`.

The index is one or two, giving exactly the alternatives above.

A concrete parity-wall example is useful. Let `D=(-1,-1)_Q`, ramified exactly at `2` and infinity, and let `K=Q(sqrt(-7))`. Since the discriminant `-7` is `1 mod 8`, the prime `2` splits in `K`; the invariant `1/2` therefore survives at both primes above `2`, so `D tensor K` is still division. There is no embedding `K -> D`, whereas the displayed `2 by 2` block gives `K -> M_2(D)`. In contrast, `Q(i)` embeds directly in `D`, so the split case permits every multiplicity.

## Low-dimensional consequences

Let `X` be a simple quaternionic abelian variety with `End^0(X)=D` and consider the isotypic support `X^m` inside an abelian variety of dimension at most four.

- For a quaternionic surface `X`, `m=1` requires `D_L` split, while `m=2` always admits the action.
- For a quaternionic fourfold, only `m=1` fits, so `D_L` must split.
- No higher multiplicity quaternionic support fits in dimension four.

For `m=2`, the universal doubling construction gives more than the algebra action. Starting from any polarization on `X`, use on the multiplicity space

`J=[[0,-d],[1,0]],   R=diag(1,d)`.

Then `R^-1 J^t R=-J`, so the polarization modified by the positive matrix `R` is `K`-compatible. If `X` is a surface, `X^2` has balanced signature `(2,2)` and trivial signed Weil discriminant. Thus decomposable quaternionic surface squares belong to the discriminant-one locus regardless of whether `K` embeds in `D` itself.

For `m=1`, splitting is only the algebraic gate. Type II versus Type III positive-involution constraints, signatures, and discriminants remain separate. In particular this note neither accepts nor rejects preserved Cycle 292's claims for simple II(1), II(2), or Type III fourfolds.

## Why this helps but does not finish the census

The lemma reduces every quaternionic matrix-embedding row to a local splitting test plus one parity bit. The still-open part of the Cycle 292 census is precisely the multiplicity-one geometry: enumerate all simple quaternionic supports in dimension at most four, determine which embedded `K` actions are stable under a positive Rosati involution, calculate the signed determinant class, and attach the actual rational Hodge packet and parametrized Hodge circle. No conclusion about mixed Hodge tensors follows from the embedding criterion alone.
