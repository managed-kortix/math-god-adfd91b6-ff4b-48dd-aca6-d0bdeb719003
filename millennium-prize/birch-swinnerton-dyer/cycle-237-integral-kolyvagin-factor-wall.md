# Cycle 237: integral Gross--Zagier--Kolyvagin factor audit

## Verdict

For the frozen data

\[
 A=433\mathrm a1^{(-1499)},\qquad
 K=\mathbf Q(\sqrt{-115}),\qquad
 N_A=433\cdot1499^2,
\]

the literature does not provide the single effective all-prime integer
`C_A` required by `HK236`:

\[
 \#\Sha(A/\mathbf Q)\mid (C_A I_A)^2,
 \qquad I_A=[A(\mathbf Q)_{\rm free}:\mathbf Z y_K].       \tag{237.1}
\]

The exact applicable results are prime-by-prime. Cha gives (237.1) with no
extra odd factor away from `5,23,1499`, and the already certified 2-descent
handles `2`. The original surjective Kolyvagin theorem can also cover each of
`5,23,1499`, but the repository does not contain a proof of residual
surjectivity for this twist at any of those three primes. Consequently the
present literature packet does not isolate `1499` as an unconditional or
structural exception, and an integer `C_A` satisfying (237.1) cannot yet be
printed.

This is `HK236 WALL`, not `FAIL`: the Heegner datum is valid, but checkpoint
item 2 asks for more than the available integral theorem packet supplies.
The exact modular-symbol computation in the companion integral-trace audit
certifies `L(A^{chi_K},1) != 0`. Together with the certified simple zero of
`L(A,s)`, Gross--Zagier makes `y_K` non-torsion. The remaining gaps discussed
here are residual-image and integral-index issues, not rank-zero
nonvanishing.

## Normalized Heegner point and passage from `K` to `Q`

Fix the optimal parametrization

\[
 \pi:X_0(N_A)\longrightarrow A,\qquad \pi(\infty)=0,
\]

and the CM point `x_1` attached to the ideal of norm `N_A` in `O_K`. Put

\[
 y_K=\operatorname {Tr}_{H/K}(\pi(x_1)).                 \tag{237.2}
\]

This definition is integral: `x_1` is an algebraic point, `pi` is a morphism,
and the trace is the elliptic-curve group trace. There is no coordinate or
modular-symbol denominator in (237.2). The exact splitting checks already in
Cycle 209 prove the classical Heegner hypothesis. The certified analytic rank
of `A` is one, while the required nonzero rank-zero twist value makes
`rank A(K)=1`; since `A(Q)` already has rank one, the inclusion of free
lattices `A(Q)_{free} -> A(K)_{free}` has finite index. It need not be an
integral equality. The quotient is killed by `2`: modulo torsion, conjugation
acts trivially on the one-dimensional rational Mordell--Weil space, and
`R+conj(R)` is rational. Therefore the two Heegner indices have the same
`p`-adic valuation for every odd `p`, which is exactly what the odd-primary
bound needs. No equality of integral indices is asserted. Restriction

\[
 \Sha(A/\mathbf Q)[p^\infty]\longrightarrow
 \Sha(A/K)[p^\infty]
\]

is injective for odd `p`, because its kernel is killed by `[K:Q]=2`.

## Exact integral theorem packet

The usable unconditional upper bound is the following combination.

1. Kolyvagin, as stated in Cha, *J. Number Theory* 111 (2005), Theorem 3:
   if `p` is odd, `y_K` is non-torsion, and
   `Gal(Q(A[p])/Q)=GL_2(F_p)`, then

   \[
    \operatorname {ord}_p\#\Sha(A/K)
       \le 2\operatorname {ord}_p[A(K):\mathbf Z y_K].   \tag{237.3}
   \]

2. Cha, loc. cit., Theorem 21: surjectivity in (237.3) may be replaced by
   irreducibility of `A[p]`, provided `p` is unramified in `K` and `A` has
   good or multiplicative reduction at `p`.

3. Kolyvagin's exact formula, in the notation used by Jetchev, is

   \[
    \#\Sha(A/K)[p^\infty]=p^{2(m_0-m_\infty)},           \tag{237.4}
   \]

   where `m_0=ord_p[A(K)_{free}:Zy_K]`. Jetchev, *Compositio Math.* 144
   (2008), Theorem 1.4 and Corollary 1.5, assumes `p` prime to `N_A` and
   residual surjectivity and proves

   \[
    m_\infty\ge \max_{q\mid N_A}\operatorname {ord}_p(c_q).
                                                                    \tag{237.5}
   \]

   In particular (237.3) follows in Jetchev's range; the Tamagawa correction
   improves the upper bound rather than enlarging it. Jetchev does not apply
   at either conductor prime `433` or `1499`.

4. Burungale--Castella--Grossi--Skinner, *Non-vanishing of Kolyvagin
   systems and Iwasawa theory*, arXiv:2312.09301v2 (2026), Theorem B, proves
   under its good-ordinary, split-at-`p`, surjective, `p`-optimal and integral
   anticyclotomic-main-conjecture hypotheses that

   \[
    m_\infty=\sum_{q\mid N_A}\operatorname {ord}_p(c_q). \tag{237.6}
   \]

   This is an exact primitivity formula, but it is not an all-prime theorem:
   it assumes `p` is a good ordinary prime and splits in `K`. It therefore
   does not repair the additive prime `p=1499`.

Gross--Zagier is needed to prove that (237.2) is non-torsion from
`L'(A/K,1) != 0`; it does not add a positive integer error factor to
(237.3). Its differential and period normalizations matter when computing
the height or identifying `y_K`, but not after the integral point (237.2) and
its Mordell--Weil index have been fixed.

## Complete factor ledger

The proposed omnibus `C_A` conflates several logically different quantities.
For this curve and field they audit as follows.

| source | exact contribution | status for `A,K` |
|---|---:|---|
| Tamagawa at `433` | `c_433=1` | no contribution |
| Tamagawa at `1499` | `c_1499=2` | no odd contribution; the 2-part is already killed by descent |
| Manin constant | no factor in (237.3); `p`-unit when Jetchev applies | not a source of an odd upper-bound factor |
| modular parametrization | choose the optimal quotient and `pi(infinity)=0` | fixes `y_K`; no denominator |
| CM units | `O_K^times={+1,-1}` since `D_K=-115` | no `3`-unit anomaly; any convention must still be fixed in Gross--Zagier |
| class number/trace | `h_K=2`, absorbed in the literal trace (237.2) | no denominator if the trace, rather than an averaged trace, is used |
| rational torsion | trivial | no factor |
| `K`-rational torsion | index is taken modulo torsion | irreducibility supplies `A(K)[p]=0` in Cha's range; no blanket torsion computation is used |
| residual image | irreducibility is enough in Cha; surjectivity is needed for (237.4)--(237.6) | exceptional support is explicit once the rational isogeny/image computation is certified |
| ramification of `K` | Cha requires `p` not dividing `115` | excludes `p=5,23` from Cha, though a direct surjective Kolyvagin theorem may cover them after image verification |
| reduction at `p` | Cha allows good or multiplicative reduction | excludes additive `p=1499` from Cha, but not from Kolyvagin's surjective Theorem 3 |
| good ordinary and split | required by the 2026 refined theorem | useful only prime by prime; not an all-prime factor |
| Heegner-system content | `m_infinity` in (237.4) | nonnegative, so discarding it gives the upper bound; it is not an unknown positive multiplier |
| local finite/singular maps | built into Kolyvagin's theorem under its hypotheses | no separately printed denominator in (237.3) |
| restriction `Q -> K` | kernel killed by `2` | injective on every odd-primary part |
| prime `2` | outside the odd-prime theorems | `Sha(A/Q)[2^infty]=0` already certified |

The Manin constant, periods, CM-unit convention, and modular degree are
essential for an exact Gross--Zagier height and for proving a numerical value
of `I_A`. They are not arbitrary multiplicative losses in Kolyvagin's bound.
Similarly, Tamagawa numbers occur through the subtractive primitivity term
`m_infinity`; replacing them by an unexplained positive factor in `C_A`
would be safe but would not be the exact theorem.

## Curve-specific consequence

The exact isogeny computation reports that the rational isogeny class of the
underlying non-CM curve is a singleton. A reducible `E[p]` would give a
rational cyclic `p`-isogeny; twisting preserves such an isogeny, and a
prime-degree self-isogeny cannot occur for a non-CM curve. Thus, provided the
singleton computation is treated as certified and complete, `A[p]` is
irreducible for every odd `p`. This implication proves irreducibility only;
it does not prove residual surjectivity. Cha's Theorem 21 therefore yields

\[
 p\ne5,23,1499,\quad p\text{ odd}
 \quad\Longrightarrow\quad
 \operatorname {ord}_p\#\Sha(A/\mathbf Q)
 \le 2\operatorname {ord}_p(I_A).                       \tag{237.7}
\]

The primes `5` and `23` are excluded from Cha because they ramify in `K`, and
`1499` is excluded from Cha because the reduction is additive. All three can
instead be covered by the original Kolyvagin theorem after residual
surjectivity is certified: Cha's statement of Theorem 3 imposes neither
`p` unramified in `K` nor semistable reduction at `p`. Accordingly additive
reduction does not make `1499` a structural exception to the combined
literature packet.

With only the currently recorded image evidence, the justified support
implication is

\[
 p\mid\#\Sha(A/\mathbf Q)
 \Longrightarrow p\mid I_A\quad\hbox{or}\quad p\in\{5,23,1499\}. \tag{237.8}
\]

If residual surjectivity is certified at `5,23,1499`, the exceptional set in
(237.8) is empty and every prime divisor of `#Sha(A/Q)` divides `I_A`. Checks
only at `5,23` do not justify the former claim with sole exception `1499` as a
structural theorem; they merely leave `1499` as the last unchecked image.

## Terminal wall

The current obstruction is not a theorem-imposed additive-prime exponent.
It is the absence of certified residual-image computations at the three
primes outside Cha's range. A direct Selmer computation could also handle any
one of these primary groups, but is not forced by the literature if
surjectivity is established.

Therefore `C_A` is not yet effective from the audited artifacts in the sense
required by `HK236`, but the reason previously stated was too strong. The
non-circular repair is to certify the three residual images and then apply
Kolyvagin prime by prime, or to retain (237.8) and compute the remaining
primary groups directly. Under the frozen rule, the requested exact integer
divisibility still terminates at `WALL`.
