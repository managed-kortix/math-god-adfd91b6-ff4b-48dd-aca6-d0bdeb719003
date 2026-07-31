# Cycle 181: conductor dependence and the finite-Frobenius gate

## Verdict

The derived coordinate proposed in Cycle 178 can be defined exactly, but it is
not presently justified as a function on Frobenius classes in one fixed finite
extension. Its modular symbol belongs to the quadratic twist itself, whose
level is `433 q^2`; after the standard twist formula it uses base-curve modular
symbols of denominator divisible by `q`. Thus the usual fixed residual Selmer
governing field may control the localization functional `lambda_q`, but it does
not, without a new theorem, control the Kurihara coordinate.

Conductor growth is an obstruction to the proposed proof, not by itself a
proof of nonfactorization: a globally defined quantity can accidentally be
Frobenian. This note gives the precise coordinate and an exact collision
criterion. A collision disproves a named finite extension. Ruling out every
finite extension requires collisions along a cofinal sequence of finite
Galois extensions; one finite computation cannot establish that universal
statement.

## The prime-twist family

Put

\[
 E=433\mathrm a1:y^2+xy=x^3+1,\qquad p=7,
\]

and, for an odd prime `q` not dividing `2*7*433`, let

\[
 D_q=\begin{cases}q,&q\equiv1\pmod4,\\-q,&q\equiv3\pmod4.\end{cases}
\]

This convention removes the ambiguity in the phrase "prime quadratic twist."
Let `chi_q=(D_q/.)`, let `E_q=E^(D_q)`, and let
`f_q=f_E tensor chi_q`. At every such good prime `q`,

\[
 N(E_q)=433q^2.                                      \tag{181.1}
\]

Any narrower root-number or local packet is obtained by imposing the specified
congruence/Frobenius conditions on `q`; it does not alter the definition below.

Let `ell` be a prime not dividing `2*7*433*q` such that

\[
 \ell\equiv1\pmod7,\qquad
 a_\ell(E_q)=\chi_q(\ell)a_\ell(E)\equiv \ell+1\pmod7.       \tag{181.2}
\]

These are the one-prime Kurihara conditions used here. Any application of a
published Kolyvagin-system theorem must separately check its stronger
admissibility, residual-image, Tamagawa, ordinarity, nonanomalous, and local
torsion hypotheses.

## Exact definition of `c(q,ell)`

Let `V_q^+` be the rational plus modular-symbol line of `f_q`, with integral
lattice `M_q^+`. Normalize its rational generator by the positive Neron period
of a specified global minimal model of `E_q`, with the same endpoint and sign
convention as `msfromell` in Cycles 135 and 171, and write

\[
 [r]^+_q=x_q^+([r]-[\infty])\in\mathbf Q.                    \tag{181.3}
\]

Thus `x_q^+` is characterized by

\[
 2\pi i\int_\delta f_q(z)\,dz
 =x_q^+(\delta)\Omega_{E_q}^+
  +x_q^-(\delta)i\Omega_{E_q}^- .                            \tag{181.4}
\]

Before reduction modulo seven one must verify that the Manin and real-component
factors and every symbol occurring below are 7-integral. This is not a uniform
consequence of the Cycle 135 calculation for the untwisted curve.

Let `G_ell=(Z/ell Z)^x`, let `I_ell` be the augmentation ideal of
`F_7[G_ell]`, and define the residual Mazur--Tate element

\[
 \overline\theta_{q,\ell}
  =\sum_{a\in G_\ell}\overline{[a/\ell]^+_q}\,\sigma_a
  \in\mathbf F_7[G_\ell].                                  \tag{181.5}
\]

Choose a primitive root `eta_ell` and write
`log_etaell(a) in F_7` for the discrete logarithm modulo `ell-1`, reduced
modulo seven. The map

\[
 d_{\eta_\ell}:I_\ell/I_\ell^2\longrightarrow\mathbf F_7,
 \qquad \sigma_a-1\longmapsto\log_{\eta_\ell}(a)             \tag{181.6}
\]

is the Kurihara derivative. Equivalently, the linear functional
`D_etaell:F_7[G_ell]->F_7` defined by
`D_etaell(sigma_a)=log_etaell(a)` restricts to (181.6) on `I_ell` and kills the
constant group-ring element. Applying it to (181.5) gives the scalar proposed
in Cycle 178:

\[
 \boxed{
 c_{\eta_\ell}(q,\ell)
   =\sum_{a\in G_\ell}
     \overline{[a/\ell]^+_q}\,
     \overline{\log_{\eta_\ell}(a)}\in\mathbf F_7.}
                                                               \tag{181.7}
\]

This is the normalized one-prime Kurihara number
`tilde-delta_ell^(1)(E_q)` in the conventions of Cycle 135. Replacing the
primitive root multiplies (181.7) by an element of `F_7^x`. Replacing a
primitive generator of the integral modular-symbol line does the same.
Consequently its zero/nonzero value is canonical; equality of two nonzero
scalars is meaningful only after the primitive-root and determinant-line
trivializations have been fixed.

An invariant formulation keeps

\[
 \mathfrak c(q,\ell)\in
 (M_q^+/7M_q^+)\otimes_{\mathbf F_7}(I_\ell/I_\ell^2)         \tag{181.8}
\]

and applies chosen bases only at the end. A statement about the pair
`(lambda_q,c(q,ell))` in "common determinant lines" must provide an explicit
isomorphism from (181.8) to the determinant line in which `lambda_q` is
measured. No such explicit-reciprocity isomorphism was constructed in Cycle
178, so formula (178.1) remains a candidate rather than a theorem.

## Where the conductor enters

For a primitive quadratic character `chi_q`, the elementary twist identity is

\[
 2\pi i\int_r^{i\infty}(f_E\otimes\chi_q)(z)\,dz
 =\frac1{\tau(\chi_q)}
   \sum_{u\bmod q}\chi_q(u)
   2\pi i\int_{r+u/q}^{i\infty}f_E(z)\,dz,                  \tag{181.9}
\]

up to the harmless conjugation convention for the Gauss sum. At `r=a/ell`,
the symbols on the right have endpoints

\[
 \frac{aq+u\ell}{q\ell}.                                   \tag{181.10}
\]

Thus (181.7) can be rewritten using the fixed form `f_E`, but not using a fixed
finite set of its modular symbols: the denominator acquires every new prime
`q`. Equivalently, on the twist side the newform level is `433q^2` by
(181.1). The period ratio `tau(chi_q) Omega_E^+/Omega_{E_q}^+`, the integral
symbol lattice, and the reduction modulo seven also vary with `q` and must be
controlled in any reduction of (181.9).

This gives the precise separation:

1. `lambda_q` is obtained by evaluating finitely many fixed residual Selmer or
   Kummer classes at `q`, so standard governing-field arguments can make it a
   Frobenius function after all local comparisons are proved.
2. `c(q,ell)` evaluates a varying-level automorphic object. It is not the trace
   of Frobenius of a fixed finite Galois representation supplied by the Selmer
   governing field.
3. Neither fact proves that `c` cannot accidentally factor through a finite
   quotient. Such factorization is an additional arithmetic theorem, not a
   formal consequence of modular-symbol or Kolyvagin-system theory.

## Finite-governance criterion

Let `A` be a specified set of admissible ordered pairs `(q,ell)`. For a finite
Galois extension `L/Q`, unramified at `q` and `ell`, say that the scalar
coordinate is `L`-Frobenian if there is a conjugacy-invariant function

\[
 F_L:\operatorname{Gal}(L/\mathbf Q)^\#\times
     \operatorname{Gal}(L/\mathbf Q)^\#\longrightarrow\mathbf F_7          \tag{181.11}
\]

such that

\[
 c(q,\ell)=F_L(\operatorname{Frob}_q,\operatorname{Frob}_\ell)              \tag{181.12}
\]

for every pair in `A`, after fixed scalar trivializations. Here `G^#` denotes
conjugacy classes. For the invariant coordinate (181.8), (181.11) must instead
take values in one fixed line and include specified comparison isomorphisms.

**Proposition 181.1 (collision criterion).** The coordinate `c` is
`L`-Frobenian if and only if it is constant on every nonempty fibre of

\[
 (q,\ell)\longmapsto
 (\operatorname{Frob}_q(L),\operatorname{Frob}_\ell(L))       \tag{181.13}
\]

on `A`. In particular, two admissible pairs with the same two Frobenius classes
and different `c` values disprove factorization through `L`.

This is elementary but fixes the quantifiers missing from the earlier gate. It
also shows that one collision only refutes the named `L`. There is no largest
finite extension containing all possible finite governing data.

**Corollary 181.2 (universal nonfactorization test).** Choose a cofinal tower
`L_1 subset L_2 subset ...` of finite Galois extensions, meaning that every
finite Galois extension of `Q` embeds in some `L_i`. No finite Galois extension
governs `c` exactly if and only if, for every `i`, there are admissible pairs in
one fibre of (181.13) for `L_i` on which `c` differs.

The tower is a logical test, not a finite algorithm. Conversely, agreement on
any finite sample proves no factorization theorem, since a further finite
extension can separate all primes in that sample.

## A practical same-Frobenius collision

To test a proposed field `L`, fix one auxiliary prime `ell` and compare two
twist primes. Form

\[
 L'=L\,\mathbf Q(\zeta_{8\cdot7\cdot433\cdot\ell}).          \tag{181.14}
\]

Choose `q_1` and `q_2`, away from the ramification set, in the same Frobenius
class of `L'`. The cyclotomic factor keeps their congruence classes at
`2,7,433` fixed and, through `q_i mod ell`, keeps
`chi_{q_i}(ell)` fixed. Hence the root-number packet, the elementary local
conditions, and condition (181.2) for the fixed `ell` agree whenever they are
encoded by those congruences. Check any remaining twist-local and primitivity
hypotheses directly.

Now compute (181.7) with the same primitive root of `ell`. If

\[
 c(q_1,\ell)=0,\qquad c(q_2,\ell)\ne0,                       \tag{181.15}
\]

then the collision is independent of all unit choices and disproves
`L`-Frobenianity. Unequal nonzero values also work after the modular-symbol
lines have been canonically identified. Using the same `ell` avoids comparing
different augmentation lines and is therefore the cleanest experiment.

The experiment must record `D_q`, the minimal twist model, conductor, Manin and
period normalization, the exact rational modular symbols, their 7-integrality,
the primitive root, both Frobenius classes, and every admissibility check.

## The theorem that would revive the route

A valid positive result must be stronger than finite-state notation:

> **Required theorem.** There is an explicitly named finite Galois extension
> `L/Q`, a fixed determinant line `Delta`, comparison isomorphisms from the
> twist modular-symbol and Selmer lines to `Delta`, and a conjugacy-invariant
> map on `Gal(L/Q)^# x Gal(L/Q)^#` whose value is exactly
> `(lambda_q,c(q,ell))` for every pair in a specified admissible packet. All
> local twist comparisons, 7-integrality, Manin/period factors, and Kurihara
> primitivity hypotheses hold uniformly on that packet.

Only after this theorem is proved does Chebotarev apply to the decorated pair.
Surjectivity or nonvanishing on a positive-density packet, explicit reciprocity
to the twisted Selmer bound, and a rank-one converse remain separate gates.
The separate note `cycle-181-frobenian-decorated-transition.md` gives the
conditional Chebotarev bookkeeping and states the additional balanced-fiber
hypothesis needed for the candidate `288/343` relative density.

At present neither this theorem nor a universal collision sequence is known.
The finite-governing-extension claim is therefore unresolved, while the naive
inference from the fixed Selmer governing field to the varying-twist Kurihara
coordinate is rejected.

No BSD case or certificate-density theorem is claimed.
