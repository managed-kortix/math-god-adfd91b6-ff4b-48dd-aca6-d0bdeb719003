# Cycle 185: the actual two-point mod-seven Kummer group for `433a1`

Let

\[
 E:y^2+xy=x^3+1,\qquad P=(0,1),\qquad Q=(-1,1),
\]

and put `K=Q(E[7])` and `L=K(7^-1 P,7^-1 Q)`. The maximal-group hypothesis
used in Cycles 141 and 184 is true:

\[
\boxed{\operatorname{Gal}(L/\mathbf Q)
 \simeq (E[7]\oplus E[7])\rtimes\operatorname{GL}_2(\mathbf F_7).}
\tag{185.1}
\]

Its order is `7^4(7^2-1)(7^2-7)=4,840,416`.

## Residual-image audit

The integral invariants of the displayed minimal equation are `c4=1` and
`Delta=-433`. Thus reduction at 433 is multiplicative and `v_433(Delta)=1`.
The standard Tate-curve inertia formula says that tame inertia on `E[7]`
contains a transvection `U=[[1,1],[0,1]]`; its off-diagonal entry is nonzero
because `7` does not divide `v_433(Delta)`.

Direct point counting gives `#E(F_3)=6`, hence `a_3=-2`. A Frobenius matrix `A`
at 3 has trace `5`, determinant `3`, and discriminant `6`, a nonsquare modulo
seven. An exhaustive check over all 42 matrices with this trace and determinant
proves `<U,A>=GL_2(F_7)` for every possible relative placement. This is an exact
surjectivity certificate, not a database assertion.

## Independence in the exact Kummer quotient

Exact finite-field arithmetic gives

\[
 Q-5P=7(1,1)\text{ in }E(\mathbf F_{29}),\qquad
 Q-4P=7(7,32)\text{ in }E(\mathbf F_{113}).
\]

Moreover `#E(F_29)=28` and `P` has order 7, while `#E(F_113)=112` and `P` has
order 112. Thus `[P]` generates `E(F_ell)/7E(F_ell)` at each prime. The
localization rows of `P,Q` are `(1,5)` and `(1,4)`, with determinant `6 mod 7`.
If `aP+bQ` belonged to `7E(Q)`, both localizations would vanish, forcing
`a=b=0 mod 7`. Thus `P,Q` are independent in the exact quotient
`E(Q)/7E(Q)`. No rank upper bound, saturation assertion, or Kurihara theorem is
needed here.

## Maximal Kummer kernel

Write `V=E[7]` and `G=Gal(K/Q)=GL(V)`. Kummer theory embeds `Gal(L/K)` as a
`G`-submodule `N` of `V^2`. Restriction on rational Kummer classes is injective:

\[
 E(\mathbf Q)/7E(\mathbf Q)\longrightarrow H^1(K,V)^G.
\]

Indeed the kernel in inflation-restriction is `H^1(G,V)`, which vanishes by
Sah's lemma: the central scalar `2I` has `2I-I=I` invertible on `V`.
Consequently no nonzero linear combination of `P,Q` becomes seven-divisible
over `K`.

The `G`-submodules of `V^2=V tensor F_7^2` are `V tensor W` for subspaces `W`
of the multiplicity space. A proper submodule has a nonzero annihilator. Under
the Kummer pairing this says that a nonzero combination `aP+bQ` becomes
divisible by seven over `K`, a contradiction. Hence `Gal(L/K)=V^2`.

Choosing division points embeds `Gal(L/Q)` in `V^2 semidirect GL(V)`. Its
projection and kernel are both full, so it equals the ambient group. This proves
(185.1), including the semidirect-product assertion.

Reproduce every finite calculation with

```sh
python3 millennium-prize/birch-swinnerton-dyer/verify_cycle185_actual_kummer_group.py
```

The non-enumerative inputs are the standard Tate-curve inertia formula,
inflation-restriction, Sah's lemma, and the elementary Kummer pairing. A formal
proof-assistant certificate would need to encode those theorem invocations; no
division-polynomial splitting field or computer algebra database is needed.
