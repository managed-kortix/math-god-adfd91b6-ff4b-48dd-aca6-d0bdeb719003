# Cycle 166: arbitrary split-prime eta-one chains

Arbitrarily long carried `eta=1` chains do exist. A completely adapted
split-prime kernel and its complementary isogeny already give an infinite
chain. Independent local copies of this construction give arbitrary composite
levels supported on good split primes. The chain keeps the Cycle 151
threefold, involution, and normalized Weil class, but it is periodic locally
up to polarized isomorphism and supplies no generic transport.

## One split-prime lattice

Let `A_0=V/Lambda_0` be the Cycle 151 sixfold, let `E_0` be its polarization
form, and let `U subset V` be the rational subspace defining the diagonal
threefold `Gamma`. Write `Delta_0=U cap Lambda_0`. The operators `J` and `t`
are respectively the prescribed `Z[i]` action and factor swap.

Fix a good split prime

\[
p\geq5,\qquad p\equiv1\pmod4.
\]

Choose one of the Cycle 163 kernels

\[
K=D\oplus JD\subset A_0[p],\qquad
D=L\oplus\ell_\epsilon\subset\Gamma[p],
\]

where `L` is Lagrangian in the four-dimensional radical and
`ell_epsilon` is one of the two isotropic lines in the residual hyperbolic
plane. Thus `K` is `Z[i]`-stable, Lagrangian, `t`-stable, and

\[
|K|=p^6,\qquad |K\cap\Gamma[p]|=|D|=p^3.
\]

If `widetilde K` is the inverse image of `K` under
`Lambda_0 -> Lambda_0/pLambda_0`, set

\[
\Lambda_1=\Lambda_0+{1\over p}\widetilde K,
\qquad E_1=pE_0.
\]

Here `(1/p)widetilde K` denotes the inverse image of `K` in
`p^{-1}Lambda_0`. Then `E_1` is integral on `Lambda_1`, and the identity on
`V` induces the polarized `p`-isogeny

\[
f_0:(V/\Lambda_0,E_0)\longrightarrow(V/\Lambda_1,E_1),
\qquad f_0^*E_1=pE_0.
\]

The carried diagonal has lattice

\[
U\cap\Lambda_1=\Delta_0+{1\over p}\widetilde D,
\]

where `widetilde D` is the inverse image of `D` in `Delta_0`. Consequently

\[
[U\cap\Lambda_1:\Delta_0]=p^3,
\qquad \eta_p(f_0,\Gamma)={p^3\over p^3}=1.
\]

Both `J` and `t` preserve `Lambda_1`; hence they descend, and the image of
`Gamma` is the `+1` threefold of the descended involution.

## Infinite integral chain

For every `r>=0` define

\[
\begin{aligned}
\Lambda_{2r}&=p^{-r}\Lambda_0,
&E_{2r}&=p^{2r}E_0,\\
\Lambda_{2r+1}&=p^{-r}\Lambda_1,
&E_{2r+1}&=p^{2r+1}E_0.
\end{aligned}
\]

There are inclusions `Lambda_n subset Lambda_(n+1)`, and the identity on `V`
gives

\[
f_n:A_n=V/\Lambda_n\longrightarrow A_{n+1}=V/\Lambda_{n+1},
\qquad f_n^*E_{n+1}=pE_n.
\]

Each quotient `Lambda_(n+1)/Lambda_n` has order `p^6`, is a PEL-stable
Lagrangian kernel, and is stable under the current involution. If
`Y_n=U/(U cap Lambda_n)`, then

\[
[U\cap\Lambda_{n+1}:U\cap\Lambda_n]=p^3.
\]

Thus every arrow is a split-prime completely adapted arrow:

\[
\boxed{\eta_p(f_n,Y_n)=1\quad\text{for every }n\geq0.}
\]

For odd-to-even arrows this is the complementary isogeny. Intrinsically, if
`f:A -> B` is the first arrow, there is a unique `g:B -> A` with `gf=[p]`.
It satisfies

\[
g^*L=pM,
\]

because pulling both sides back by `f` gives `p^2L` and pullback on
`NS(-)_Q` is injective. Moreover

\[
\deg(g|_{f(\Gamma)})
={\deg([p]|_\Gamma)\over\deg(f|_\Gamma)}
={p^6\over p^3}=p^3,
\]

so the reverse arrow also has `eta=1`. It commutes with the PEL action and
intertwines the descended involution with `t`. This proves the same chain
without choosing lattice coordinates.

## Exact composite levels

Let

\[
F_N=f_{N-1}\cdots f_0:A_0\longrightarrow A_N.
\]

Then

\[
F_N^*E_N=p^N E_0,
\qquad |\ker F_N|=p^{6N},
\qquad \deg(F_N|_\Gamma)=p^{3N}.
\]

Equivalently, with composite level `m=p^N`,

\[
\boxed{|\ker F_N|=m^6},\qquad
\boxed{|\ker F_N\cap\Gamma[m]|=m^3},\qquad
\boxed{\eta_m(F_N,\Gamma)=1}.
\]

The middle equality is scheme-theoretic: it is the kernel of the restricted
isogeny `F_N|_Gamma`. Hence the composite kernel is a Lagrangian subgroup of
`A_0[m]`, including for `N>1`, where it must not be treated as a vector space
over a finite field. In the notation of Cycles 162--163 its residual coupled
graph has order `eta_m^2=1`; the kernel is fully split relative to the carried
threefold and its complementary factor.

For mixed levels, choose such a local lattice `Lambda_{1,p}` at each good split
prime `p`. Given exponents `e_p>=0`, prescribe the localized lattice by

\[
\Lambda(\mathbf e)_p=
\begin{cases}
p^{-e_p/2}\Lambda_{0,p},&e_p\text{ even},\\
p^{-(e_p-1)/2}\Lambda_{1,p},&e_p\text{ odd},
\end{cases}
\]

and take `Lambda(e)_l=Lambda_(0,l)` away from the finite support. The
intersection of these local lattices in `V(Q)` is a global `Z[i]`- and
`t`-stable lattice. With `m=prod_p p^{e_p}`, the form `mE_0` is integral and
has the required polarization type on it. Local index multiplication
gives a polarized isogeny `F_e` with

\[
F_{\mathbf e}^*E_{\mathbf e}=mE_0,
\qquad \deg F_{\mathbf e}=m^6,
\qquad \deg(F_{\mathbf e}|_\Gamma)=m^3,
\qquad \eta_m=1.
\]

Increasing one exponent by one gives a prime-level arrow of the same kind.
Therefore any finite or infinite word in good split primes defines a carried
`eta=1` chain, and every finite prefix gives its exact mixed composite level.
No prime-level orbit count is being extrapolated to `Z/p^e Z`; the statement
comes from the explicit integral local lattices and their global intersection.

## Carried cycle and obstruction to generic transport

At every stage the normalized pushforward is integral:

\[
p^{-3}(f_n)_*[Y_n]=[Y_{n+1}],
\qquad
m^{-3}(F_{\mathbf e})_*[\Gamma]=[Y_{\mathbf e}].
\]

The descended Weil projector therefore has nonzero value on `[Y_e]`. The
restricted polarization volume remains 16 and its polarization-isogeny degree
remains 256, as in Cycle 165.

The construction settles existence, but not globalization. At one fixed prime,

\[
(A_{2r},E_{2r})\simeq(A_0,E_0),\qquad
(A_{2r+1},E_{2r+1})\simeq(A_1,E_1)
\]

as polarized abelian varieties after scaling the lattice by `p^r`; thus the
one-prime chain alternates between two polarized isomorphism classes. In all
cases every carried `eta=1` chain remains in the closed restricted-volume 16
subthreefold locus audited in the other Cycle 166 note. Subject to the standard
generic-endomorphism theorem for this exact PEL component, that locus is proper
and no carried chain is Zariski dense. Unconditionally, the explicit periodic
chain itself produces neither a dominating Chow branch nor generic transport.
A requirement that the path discard the carried threefold is a different
problem and is not resolved by this construction. No Hodge-conjecture result
is claimed.
