# Cycle 262: decisive Kolyvagin Theorem 3 literature audit for `43a1`

## Verdict

**PASS.** The published Kolyvagin inequality quoted as Theorem 3 by Cha
covers both exceptional-looking primes in the packet:

- `p=7`, although `7` ramifies in `K=Q(sqrt(-7))`; and
- `p=43`, although `E=43a1` has bad multiplicative reduction at `43`.

Theorem 3 has neither the condition `p` not dividing `D_K` nor a good-reduction
condition at `p`. Its extra prime-specific hypothesis is full residual
surjectivity. Cycle 261 proves that hypothesis for every prime, including `7`
and `43`. Consequently no direct `7`- or `43`-Selmer computation is required
to apply this published inequality.

This conclusion concerns the Kolyvagin inequality only. It uses the separate
Cycle 261 certificates that the normalized maximal-order Heegner point is
`y_K=P=(0,0)` and that `E(K)_free=ZP`; those give the index exponent `m_p=0`.

## Exact published statement

The source is B. Cha, "Vanishing of some cohomology groups and bounds for the
Shafarevich--Tate groups of elliptic curves," *Journal of Number Theory* 111
(2005), no. 1, 154--178, DOI `10.1016/j.jnt.2004.08.009`.

On journal page 155, Cha first defines `m` to be the largest integer for which
`y_K` belongs to `p^m E(K)` "modulo `p`-torsion points." The displayed theorem
is:

> **Theorem 3 (Kolyvagin).** Suppose that `y_K` is of infinite order. Assume
> that `p` is an odd prime. If the Galois group
> `Gal(Q(E[p])/Q)` is isomorphic to `GL_2(Z/pZ)`, then
> `ord_p |Sha(E/K)| <= 2m`.

The symbols in the scan are `ell` and `Ш(E/K)` rather than `p` and
`Sha(E/K)`. The transcription above changes only those typographical symbols.
There is no omitted clause after "odd prime" in the displayed statement.

The standing context immediately preceding Theorem 3, on journal pages
154--155, is:

1. `E/Q` is a modular elliptic curve of conductor `N`;
2. `K=Q(sqrt(D))` is imaginary quadratic with fundamental discriminant
   `D != -3,-4`;
3. every prime divisor of `N` splits in `K` (the Heegner hypothesis);
4. `y_K` is the maximal-order Heegner point in `E(K)`.

None of these standing conditions says that `p` is unramified in `K`, that
`p` does not divide `N`, or that `E` has good reduction at `p`.

Cha attributes the result to V. A. Kolyvagin, "On the structure of
Shafarevich--Tate groups," in *Algebraic Geometry* (Chicago, IL, 1989),
Lecture Notes in Mathematics 1479, Springer, 1991, pp. 94--121, DOI
`10.1007/BFb0086267`. A publisher preview of the original chapter, pp. 94--95,
confirms the same modular-Heegner setup and defines Kolyvagin's set `B(E)` by
surjectivity of the relevant Galois representation; it does not impose a
condition excluding primes dividing `D` or `N` there. Cha's paper is the
accessible published source for the exact inequality and hypotheses above.

## Why Cha Theorem 21 is different

Cha's Theorem 21 appears on journal page 173. Its exact additional local
hypotheses are that `p` does not divide `D` and that `E` has good or
multiplicative reduction at `p`; it then replaces residual surjectivity by
residual irreducibility and concludes the same inequality.

Those restrictions belong to Cha's weaker-image extension, not to the quoted
Kolyvagin Theorem 3. Cha's proof explicitly explains their role: `p` is then
unramified in `K`, linear disjointness transfers irreducibility from `Q` to
`K`, and Cha's Assumption 1 supplies the cohomology vanishing used to replace
Kolyvagin's surjectivity argument.

Therefore:

| prime | Theorem 3 | Theorem 21 | decisive route |
|---|---|---|---|
| `7` | applies after residual surjectivity | does not apply because `7 | D_K` | Theorem 3 |
| `43` | applies after residual surjectivity | also applies: `43` is unramified in `K`, reduction is multiplicative, and `E[43]` is irreducible | either; Theorem 3 is enough |

Jetchev's later refinement is not needed here. D. Jetchev, "Global
divisibility of Heegner points and Tamagawa numbers," *Compositio Mathematica*
144 (2008), Theorem 1.4 and Corollary 1.5, assumes `p` does not divide `N`, so
it cannot be the citation at `p=43`.

## Curve-specific discharge

For the displayed curve and field:

1. `N=43`, `D_K=-7`, and `(-7/43)=1`, so the sole conductor prime splits and
   the maximal-order Heegner hypothesis holds.
2. The exact CM certificate identifies the normalized Heegner point as
   `y_K=P=(0,0)`.
3. The Mordell--Weil certificate proves `E(K)_tors=0` and
   `E(K)_free=ZP`. Hence, for every prime `p`, the largest `m_p` with
   `y_K in p^(m_p)E(K)` modulo torsion is exactly `0`.
4. Cycle 261 proves
   `Gal(Q(E[p])/Q)=GL_2(F_p)` for every prime. At `p=7` it uses a Frobenius
   nonsquare-discriminant witness, the `I_1` inertia transvection at `43`,
   Dickson's classification, and the cyclotomic determinant. At `p=43` it
   additionally audits the wild characteristic-43 Tate-curve argument:
   `v_43(Delta_min)=1` makes the Tate parameter non-43rd-power and supplies a
   nontrivial unipotent in the residual image.

Applying Theorem 3 separately at `p=7` and `p=43` now gives

\[
 \operatorname{ord}_7 |\Sha(E/K)|\leq 0,
 \qquad
 \operatorname{ord}_{43}|\Sha(E/K)|\leq 0.
\]

Thus `Sha(E/K)[7^infty]=0` and `Sha(E/K)[43^infty]=0`. Odd-primary
restriction from `Q` to `K` is injective by restriction--corestriction, so the
same vanishing follows over `Q` at both primes.

## Source anchors

- Cha, journal p. 155: definition of `m` and exact Theorem 3 inequality.
- Cha, journal p. 173: exact hypotheses and conclusion of Theorem 21.
- Cha, journal pp. 173--175: explanation that Kolyvagin's surjectivity input
  occurs in Proposition 2 and Cha's cohomology theorem permits the
  irreducibility replacement under Theorem 21's local hypotheses.
- Cha, journal p. 178: full bibliographic identification of Kolyvagin's 1991
  chapter.
- Kolyvagin, LNM 1479, pp. 94--95: original modular-Heegner setup and the
  surjective-prime set `B(E)`; DOI `10.1007/BFb0086267`.

Stable publisher records:

- `https://doi.org/10.1016/j.jnt.2004.08.009`
- `https://doi.org/10.1007/BFb0086267`

The result is therefore not conditional on a direct finite Selmer
calculation at `7` or `43`. If residual surjectivity had failed, the required
substitute would have been a certified computation of the relevant
`p`-primary Selmer group over `K` (or enough finite-level Selmer data plus a
control/finiteness argument to prove `Sha(E/K)[p^infty]=0`), not merely a
`p`-descent over `Q`; that fallback is unnecessary here.
