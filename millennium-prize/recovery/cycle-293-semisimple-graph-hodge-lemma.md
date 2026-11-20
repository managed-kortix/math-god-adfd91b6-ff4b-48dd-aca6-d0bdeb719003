# Cycle 293 candidate: an exact semisimple graph-to-Hodge lemma

## Status

This is a candidate independently reconstructed conditional lemma, pending independent audit, for the graph step in the untrusted Cycle 291/292 mixed-product route. It does not assert that any required graph exists, that the preserved support census is exhaustive, that its rational packets match, or that a new Hodge case follows. It applies to the **entire connected semisimple Hodge groups**, not automatically to one geometric Dynkin node or to a quotient with untracked complementary factors.

## Theorem

Let `(V_i,h_i)` be polarizable rational Hodge structures of weight one. Let

`G_i subset GL(V_i)`

be their connected Hodge groups and suppose both `G_i` are semisimple. Write `u_i:S^1 -> G_i,R` for the Hodge circle, `pi_i:G_i -> G_i^ad`, and let

`alpha:G_1^ad -> G_2^ad`

be a rational isomorphism satisfying equality of **parametrized** circles

`alpha_R pi_1 u_1 = pi_2 u_2`.

Let `tilde alpha:G_1^sc -> G_2^sc` be the unique lift. If

`V_1,Qbar ~= tilde alpha^* V_2,Qbar`

as `G_1,Qbar^sc`-modules, then `V_1` and `V_2` are isomorphic as rational Hodge structures. If `V_i=H_1(A_i,Q)` for complex abelian varieties, then `A_1` and `A_2` are isogenous.

## Proof

Let

`H=Hom_{G_1^sc}(V_1,tilde alpha^*V_2)`.

Invariant linear equations commute with characteristic-zero scalar extension, so

`H tensor_Q Qbar = Hom_{G_1,Qbar^sc}(V_1,Qbar,tilde alpha^*V_2,Qbar)`.

The assumed geometric module isomorphism is an invertible point of the right side. Hence the determinant restricted to the rational vector space `H` is a nonzero polynomial over `Q`. Because `Q` is infinite, that polynomial cannot vanish at every rational point of `H`; choose `f in H(Q)` with `det(f) != 0`. Thus `f` is a rational invertible intertwiner for the simply connected representations.

Let `X_i` be the derivative of `u_i` at the standard generator of `Lie(S^1)`. A central isogeny induces an isomorphism on Lie algebras. Differentiating the parametrized-circle equality and using the defining lift of `alpha` therefore gives

`d(tilde alpha)(tilde X_1)=tilde X_2`,

where `tilde X_i` is the unique lift of `X_i` to `Lie(G_i^sc)_R`. Differentiating the intertwining identity yields

`f d rho_1(X_1)=d rho_2(X_2) f`.

For a weight-one Hodge structure, `d rho_i(X_i)` is its complex structure `J_i`, up to the same fixed sign convention on both sides. Thus `fJ_1=J_2f`, so `f` preserves the Hodge decomposition. It is a rational Hodge isomorphism.

The functor `A -> H_1(A,Q)` from complex abelian varieties up to isogeny to polarizable rational Hodge structures of type `{(-1,0),(0,-1)}` is fully faithful. Therefore an invertible rational Hodge map comes from a quasi-isogeny; clearing denominators gives an isogeny.

## Consequences for the preserved route

Under these exact hypotheses, no separate additive “central correction” or represented-commutant calculation is needed after rational module matching: the derivative of the full parametrized adjoint Hodge circle already fixes the complex structure because a semisimple group and its adjoint have the same Lie algebra. Tits algebras and represented commutants remain relevant **upstream**, to decide whether a proposed rational adjoint graph and the required rational module matching actually exist. They cannot be discarded from the support/packet census.

For a graph involving only one quotient of a product Hodge group, the theorem does not apply to the whole `H^1` unless all complementary factors and their Hodge-circle components are also matched. In that weaker setting a commutant analysis may again be necessary.

## Necessity of the hypotheses

1. **Semisimplicity/full adjoint group.** For CM elliptic curves the Hodge groups are tori and their adjoint groups are trivial. Distinct nonisogenous CM elliptic curves therefore have identical trivial adjoint data, while their rational Hodge structures need not be isomorphic. The central Hodge component is invisible after adjoint projection.
2. **Parametrization, not just image.** Replacing a Hodge circle `u(z)` by `u(z)^(-1)` preserves its image but changes `J` to `-J`. A generic elliptic curve is not isogenous to its complex conjugate, so equality of circle images cannot force a rational Hodge isomorphism.
3. **Rational graph, not absolute root type.** An isomorphism of geometric Dynkin diagrams does not provide `alpha` over `Q`, and matching absolute highest weights does not by itself identify the pulled-back rational representations. Rational forms and Tits data enter before the determinant-open argument.
4. **Whole group, not an isolated node.** Equality on one adjoint factor leaves the derivative from every other factor uncontrolled.
5. **Invertibility.** A nonzero derived intertwiner is insufficient when multiplicities occur. The geometric hypothesis supplies an invertible point, and the determinant-open argument descends invertibility.

## Fail-closed application rule

A census row may use this lemma only after recording: (i) the actual connected semisimple Hodge groups, uniformly for the relevant special members; (ii) an actual rational isomorphism of their entire adjoint groups; (iii) equality of the parametrized adjoint Hodge circles; and (iv) geometric equivalence of the full pulled-back `H^1` modules. Missing any one item leaves the graph unresolved. No preserved Cycle 291/292 row is certified merely by this lemma.
