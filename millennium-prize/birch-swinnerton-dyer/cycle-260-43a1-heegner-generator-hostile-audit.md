# Cycle 260: hostile audit of the `43a1`, `D_K=-7` Heegner argument

## Verdict

The proposed deduction

\[
 E=43\mathrm a1,\quad K=\mathbf Q(\sqrt{-7}),\quad
 y_K\text{ generates }E(\mathbf Q)
 \quad\Longrightarrow\quad \Sha(E/\mathbf Q)=0
\]

is **not promoted**. The curve and Heegner-hypothesis inputs pass, and the
prime-by-prime Kolyvagin strategy is mathematically viable. The committed
packet does not, however, prove the exact normalized Heegner-point identity,
does not certify all residual hypotheses required to cover every odd prime,
and does not contain an independently replayed proof-enabled 2-descent
certificate. These are proof gaps, not evidence that the expected conclusion
is false.

In particular, the database value `sha=1`, the rounded analytic BSD quotient,
and PARI's `ellheegner` recognition are not used as proofs. No BSD assertion is
made.

## Exact curve and field data

The Cremona/LMFDB curve `43a1` is

\[
 E:[0,1,1,0,0],\qquad y^2+y=x^3+x^2.                 \tag{260.1}
\]

Exact PARI arithmetic gives

\[
 N_E=43,\qquad \Delta_{\min}=-43,
\]

with nonsplit multiplicative type `I_1` and Tamagawa number `c_43=1`.
The point

\[
 P=(0,0)                                                   \tag{260.2}
\]

is non-torsion; the recorded Mordell--Weil data say
`E(Q)=Z P` and `E(Q)_tors=0`. The exact group operations
`2P=(-1,-1)` and `3P=(1,-2)` are consistency checks, not a proof that `P` is
saturated. A rigorous use of the generator statement must cite or reproduce a
complete Mordell--Weil/descent certificate rather than the database record.

For

\[
 K=\mathbf Q(\sqrt{-7})=\mathbf Q(a),\qquad a^2-a+2=0,
\]

the fundamental discriminant is `D_K=-7`, the class number is one, and the
only ramified rational prime is `7`. The conductor prime splits because

\[
 \left(\frac{-7}{43}\right)=1,
 \qquad 37^2\equiv-7\pmod {4\cdot43}.                    \tag{260.3}
\]

Thus the classical `X_0(43)` Heegner hypothesis holds for the maximal order of
`K`. There is no coprimality problem: `gcd(7,43)=1`.

## The unproved Heegner index

Fix the optimal parametrization

\[
 \pi:X_0(43)\longrightarrow E,
 \qquad \pi(\infty)=0,
\]

and define `y_K` with the literal Kolyvagin/Cha normalization as the trace from
the Hilbert class field to `K` of the maximal-order CM point. Since `h_K=1`,
this trace has one summand, but that fact does not identify its image under
`pi`.

PARI 2.15.4 returns

```text
ellheegner(ellinit([0,1,1,0,0])) = [0,0]
```

and its computed canonical height agrees numerically with that of `P`. This is
a floating modular-integration and point-recognition computation. It does not
constitute an exact algebraic evaluation of `pi` at the CM point, a directed
elliptic-logarithm isolation, or an audit of the sign/base-point convention.
Therefore this packet does not prove

\[
 y_K=\pm P,
 \quad [E(K)_{\rm free}:\mathbf Z y_K]=1,
 \quad\text{or even the corresponding odd-primary index statement}. \tag{260.4}
\]

This is the first terminal gap. It cannot be replaced by the analytic BSD
quotient or by rounding a Gross--Zagier height ratio.

## Primary Kolyvagin theorem audit

The primary statements were checked directly in Byungchul Cha, *J. Number
Theory* **111** (2005), 154--178, DOI
`10.1016/j.jnt.2004.08.009`:

- Cha's quoted Kolyvagin Theorem 3 applies to every odd prime `p` when `y_K`
  is non-torsion and `Gal(Q(E[p])/Q)=GL_2(F_p)`. Its displayed statement does
  not exclude primes dividing `D_K` or `N_E` and gives
  `ord_p #Sha(E/K) <= 2m_p`.
- Cha's Theorem 21 replaces surjectivity by irreducibility only when
  `p` does not divide `D_K` and `E` has good or multiplicative reduction at
  `p`.
- Jetchev, *Compositio Math.* **144** (2008), Theorem 1.4 and Corollary 1.5,
  assumes `p` does not divide `N_E` and residual surjectivity. It is not the
  theorem to use at `p=43`, although Cha's Theorem 21 can cover `43` because
  the reduction is multiplicative and `43` is unramified in `K`.

Consequently the exact odd-prime ledger is:

| prime | usable theorem | missing curve-specific input |
|---|---|---|
| `p != 7`, odd, including `3` and `43` | Cha Theorem 21 | irreducibility of `E[p]`, plus `m_p=0` |
| `p=7` | Kolyvagin as quoted in Cha Theorem 3 | full residual surjectivity, plus `m_7=0` |

There is no separate conductor-prime exception at `43`: it is semistable and
Cha allows multiplicative reduction. There is no license to ignore the small
prime `3`; it must pass the same residual check. The ramified prime `7` cannot
be passed through Cha's irreducible theorem and requires the stronger
surjectivity hypothesis (or an independent 7-Selmer computation).

LMFDB currently records maximal mod-`p` image for every prime and no rational
isogenies. The latter proves residual irreducibility for every `p`, once the
completeness of the rational isogeny computation is certified; it does not by
itself prove surjectivity at `7`. The former is strong supporting database
evidence but no primary residual-image certificate or replayable group
calculation is committed here. Hence the all-odd-prime step remains open at
the artifact level.

There is a short potential repair specifically at `p=7`: type `I_1`
multiplicative reduction at `43` should supply a nontrivial transvection modulo
`7`, while Frobenius at `3` has characteristic polynomial with discriminant
`a_3^2-4*3=-8=6 mod 7`, a nonsquare. A cited subgroup-classification lemma,
together with a fully written tame-inertia argument and the surjective
cyclotomic determinant, should then prove `GL_2(F_7)`. Those theorem statements
and deductions are not yet committed as a proof, so this audit does not silently
promote the database image record.

If (260.4), the Mordell--Weil generator certificate, and these residual facts
were supplied, the cited theorem would give `Sha(E/K)[p^infty]=0` for every
odd `p`.

## Restriction and corestriction

For every odd `p`, restriction preserves local triviality and hence defines

\[
 \operatorname{res}:\Sha(E/\mathbf Q)[p^\infty]
 \longrightarrow\Sha(E/K)[p^\infty].
\]

Corestriction composed after restriction is multiplication by `[K:Q]=2`.
Therefore the kernel of restriction is killed by two, and restriction is
injective on every odd-primary subgroup. This transition is valid and needs
no assertion that the integral Mordell--Weil lattices over `Q` and `K` are
equal.

It proves nothing at `p=2`.

## The 2-primary gap

To eliminate the 2-primary part one needs an exact descent result, for example

\[
 \dim_{\mathbf F_2}\operatorname{Sel}_2(E/\mathbf Q)=1. \tag{260.5}
\]

Together with `rank E(Q)=1` and `E(Q)[2]=0`, the Kummer exact sequence would
then give `Sha(E/Q)[2]=0`. Once Kolyvagin supplies finiteness, any nonzero
finite 2-primary group has nonzero 2-torsion, so (260.5) would imply
`Sha(E/Q)[2^infty]=0`.

The concurrently supplied `43a1` packet now records PARI's
`ellrank(E,4,[P])=[1,1,0,...]` and a one-element `ell2cover(E)` basis, including
the quartic `x^4-2*x^2+4*x+1`. PARI documents this as a complete exact
2-descent, and this is materially stronger than a database rank value. The
packet itself correctly requests a proof-enabled Sage or Magma replay because
it does not expose and independently certify the class-group, unit-group, and
everywhere-local-solubility subcertificates. Under trust in PARI's exact
2-descent implementation, (260.5) and `Sha[2]=0` follow; under the present
hostile replay standard, the 2-primary step retains that explicit software
trust gap and is not promoted as a self-contained certificate.

## Required closure packet

The proposed theorem can be reconsidered only after all of the following are
committed:

1. an exact, convention-audited proof that the maximal-order `D=-7` Heegner
   point for the optimal parametrization is `+P` or `-P`;
2. an exact Mordell--Weil certificate that `P` generates `E(Q)` and the
   resulting index computation over `K`;
3. certified irreducibility for every odd `p != 7` and surjectivity at `p=7`
   (or direct primary Selmer substitutes), explicitly including `p=3,43`;
4. a proof-enabled independently replayed 2-descent proving (260.5), or an
   explicit acceptance of PARI's exact descent implementation as the theorem
   trust boundary.

Until then the rigorous status is `GAPS`: the classical setup is correct, but
`Sha(43a1/Q)=0` is not established by the audited packet. No BSD claim is made.

## Sources consulted

- B. Cha, “Vanishing of some cohomology groups and bounds for the
  Shafarevich--Tate groups of elliptic curves,” *JNT* 111 (2005), Theorems 3
  and 21.
- D. Jetchev, “Global divisibility of Heegner points and Tamagawa numbers,”
  *Compositio Math.* 144 (2008), Theorem 1.4 and Corollary 1.5.
- LMFDB records `43.a1` and `2.0.7.1`, used as database evidence and checked
  against exact PARI arithmetic, not as substitutes for the missing proofs.
