# Cycle 263: `Sha(43a1/Q)=0`

## Theorem

Let

\[
 E/\mathbf Q:\quad y^2+y=x^3+x^2.
\]

This is the optimal curve `43a1`. Then

\[
 \Sha(E/\mathbf Q)=0. \tag{263.1}
\]

This is a curve-specific Shafarevich--Tate-group theorem. It does not prove an
exact leading-term formula, a rank statement for a family, or any of the full
claims in the Birch--Swinnerton-Dyer conjecture.

## Inputs already certified

Put `K=Q(sqrt(-7))` and `P=(0,0)`. The following four inputs are independent
parts of the `43a1` packet.

1. The conductor is `43`, the discriminant of `K` is `-7`, and `43` splits in
   `K`; hence the classical Heegner hypothesis holds.
2. Cycle 261's exact formal-`q` and resultant certificate proves, with the
   stated strong-Weil and differential normalization, that the maximal-order
   Heegner point is literally

   \[
    y_K=P. \tag{263.2}
   \]

3. The Mordell--Weil certificate proves

   \[
    E(K)_{\rm tors}=0,\qquad E(K)_{\rm free}=\mathbf ZP. \tag{263.3}
   \]

   Therefore `y_K` has infinite order and, for every prime `p`, the largest
   integer `m_p` for which `y_K` lies in `p^{m_p}E(K)` modulo `p`-torsion
   is

   \[
    m_p=0. \tag{263.4}
   \]

4. Cycle 261 proves for every rational prime `p` that

   \[
    \operatorname{Gal}(\mathbf Q(E[p])/\mathbf Q)
      \simeq \operatorname{GL}_2(\mathbf F_p). \tag{263.5}
   \]

   This includes the ramified prime `p=7` and the bad multiplicative prime
   `p=43`.

## Exact Kolyvagin theorem used

The precise accessible citation is B. Cha, "Vanishing of some cohomology
groups and bounds for the Shafarevich--Tate groups of elliptic curves,"
*Journal of Number Theory* 111 (2005), no. 1, 154--178,
DOI `10.1016/j.jnt.2004.08.009`, journal page 155. After defining `m` as the
largest integer such that `y_K` belongs to `p^m E(K)` modulo `p`-torsion, Cha
quotes the following result verbatim up to replacing the printed prime symbol
by `p` and `Ш` by `Sha`:

> **Theorem 3 (Kolyvagin).** Suppose that `y_K` is of infinite order. Assume
> that `p` is an odd prime. If the Galois group
> `Gal(Q(E[p])/Q)` is isomorphic to `GL_2(Z/pZ)`, then
> `ord_p |Sha(E/K)| <= 2m`.

The standing context on journal pages 154--155 is a modular elliptic curve of
conductor `N`, an imaginary quadratic field of fundamental discriminant other
than `-3,-4`, the Heegner hypothesis, and the maximal-order Heegner point.
There is no hypothesis in Theorem 3 that `p` not divide the quadratic
discriminant or the conductor, and no good-reduction hypothesis at `p`.
Cha attributes the theorem to V. A. Kolyvagin, "On the structure of
Shafarevich--Tate groups," in *Algebraic Geometry* (Chicago, IL, 1989), LNM
1479, Springer, 1991, 94--121, DOI `10.1007/BFb0086267`. The distinction from
Cha's locally restricted Theorem 21 is audited in Cycle 262.

For every odd prime `p`, (263.2)--(263.5) discharge every hypothesis and give

\[
 \operatorname{ord}_p|\Sha(E/K)|\leq 2m_p=0.
\]

Thus

\[
 \Sha(E/K)[p^\infty]=0\qquad(p\text{ odd}). \tag{263.6}
\]

In particular, `p=7` and `p=43` require no separate Selmer computation:
Kolyvagin Theorem 3 applies at both primes through full residual
surjectivity.

## Restriction--corestriction

For the quadratic extension `K/Q`, restriction and corestriction preserve
local triviality and hence induce maps on Shafarevich--Tate groups. Their
composition is multiplication by the extension degree:

\[
 \operatorname{cor}_{K/\mathbf Q}\circ
 \operatorname{res}_{K/\mathbf Q}=[K:\mathbf Q]=2
 \quad\text{on }\Sha(E/\mathbf Q). \tag{263.7}
\]

If `p` is odd, multiplication by two is an automorphism of every
`p`-primary group. Therefore restriction is injective on
`Sha(E/Q)[p^infty]`. Equation (263.6) implies

\[
 \Sha(E/\mathbf Q)[p^\infty]=0\qquad(p\text{ odd}). \tag{263.8}
\]

No analogous injection is asserted at `p=2`; that prime is handled directly
over `Q`.

## The 2-primary part

The full multiplication-by-two descent certificate starts from the displayed
integral equation and proves

\[
 E(\mathbf Q)[2]=0,
 \qquad
 \operatorname{Sel}^{(2)}(E/\mathbf Q)
   =\langle\delta(P)\rangle\simeq\mathbf F_2. \tag{263.9}
\]

Concretely, the complete everywhere-locally-soluble cover basis has one
element,

\[
 V^2=U^4-2U^2+4U+1,
\]

and `(U,V)=(0,1)` maps to `-3P`, so its class is the nonzero Kummer class of
`P`. The Kummer exact sequence

\[
 0\longrightarrow E(\mathbf Q)/2E(\mathbf Q)
 \longrightarrow\operatorname{Sel}^{(2)}(E/\mathbf Q)
 \longrightarrow\Sha(E/\mathbf Q)[2]\longrightarrow0
\]

then gives

\[
 \Sha(E/\mathbf Q)[2]=0. \tag{263.10}
\]

Every nonzero 2-primary torsion group contains an element of order two: from
an element of order `2^n`, multiply by `2^{n-1}`. Hence (263.10) implies

\[
 \Sha(E/\mathbf Q)[2^\infty]=0. \tag{263.11}
\]

Combining (263.8) and (263.11) proves (263.1).

## Dependency graph and trust boundary

The proof depends on the following artifacts:

- `cycle-261-43a1-dminus7-exact-cm-certificate.md` and
  `43a1/verify_dminus7_cm_exact.gp` for the normalized identity `y_K=P`;
- `43a1/K-mordell-weil-certificate.md`, PARI full 2-descent on the `-7`
  twist, and eclib saturation for `E(K)=ZP`;
- `cycle-261-43a1-all-prime-residual-surjectivity.md` and
  `verify_cycle261_43a1_residual.py` for (263.5);
- `cycle-262-43a1-kolyvagin-theorem3-literature-audit.md` for the exact
  published theorem and its applicability at `7` and `43`; and
- `43a1/2descent-certificate.md` and `43a1/verify_43a1_2descent.gp` for
  (263.9)--(263.10).

The arithmetic verifiers use exact integer, rational, finite-field,
formal-series, class-group, local-solubility, and saturation algorithms. The
proof therefore trusts the cited theorems and the standard exact PARI/GP and
eclib implementations used by the retained transcripts. The CM certificate
also trusts PARI's modular-form and Taniyama-series constructors. The finite
residual-image checks are dependency-free Python, while their infinite tail
uses the cited semistable reducibility, Mazur torsion, Tate-curve inertia, and
Dickson subgroup theorems.

Magma scripts provide independent proof-enabled replays of the 2-descents and
the number-field Mordell--Weil calculation, but Magma is unavailable in the
present environment and no Magma transcript is claimed. Thus the theorem is
definitive within the explicitly stated theorem-backed PARI/eclib trust
boundary; a kernel-independent formalization would have to expand those
implementations' class-group, local-field, modular-symbol, height-bound, and
saturation algorithms into primitive independently checked certificates.
Database values, floating-point `ellheegner` recognition, numerical analytic
rank, and a numerical BSD quotient are not used.
