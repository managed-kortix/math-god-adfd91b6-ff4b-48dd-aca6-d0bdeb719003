# Cycle 45: primary-source audit for moving Möbius dispersion

## Question and verdict

For a fixed nondegenerate compact interval \(I\Subset(0,2)\), Cycle 45 asks
for a reverse or coercive estimate at the scale

\[
 D_a(I)=\sum_{q\in S_a(I)}
 \left|\beta_a(q)+\sum_{d\in\mathcal D_a}\mu(d)W_a(q,d)\right|^2
 \gg (\log a)^{-3}.
 \tag{45.L1}
\]

Equivalently, one seeks the signed two-parameter packet inequality (11.3) of
`moving-gram-kernel-audit-2026-11-25.md`.  No checked primary source proves
(45.L1), a retained-fraction estimate for this finite moving transform, or a
reverse large-sieve inequality that would imply it.  This is a negative
literature finding, not a proof that no such theorem exists.

The closest results either identify individual Vasyunin kernel entries, give
upper cancellation estimates in a different geometry, or concern global
Nyman--Beurling approximation.  None prevents the off-diagonal cancellation
of the fixed Möbius vector in (45.L1).

## Primary sources and applicability

### Fractional-part autocorrelation

L. Báez-Duarte, M. Balazard, B. Landreau, and E. Saias, “Étude de
l’autocorrélation multiplicative de la fonction ‘partie fractionnaire’,”
*Ramanujan Journal* **9** (2005), 215--240,
[arXiv:math/0306251](https://arxiv.org/abs/math/0306251),
[doi:10.1007/s11139-005-0834-4](https://doi.org/10.1007/s11139-005-0834-4).

For

\[
 A(\lambda)=\int_0^\infty \{t\}\{\lambda t\}\,\frac{dt}{t^2},
\]

Propositions 85--89 establish continuity, the dilation identity
\(A(\lambda)=\lambda A(1/\lambda)\), a Mellin transform, and the rational
Vasyunin formula for the full autocorrelation \(A\).  Identification of the
restricted entry \(W_a(q,d)\) additionally uses the independently derived
truncation correction in equation (3.2) of the moving-kernel dossier.  The
source contains no Möbius-weighted moving-row mean square and no lower bound
of the form (45.L1).

### Möbius--Vasyunin sums

H. Maier and M. Th. Rassias, “Estimates of sums related to the
Nyman--Beurling criterion for the Riemann Hypothesis,” *Journal of Number
Theory* **188** (2018), 96--120,
[arXiv:1705.09921](https://arxiv.org/abs/1705.09921),
[doi:10.1016/j.jnt.2017.12.012](https://doi.org/10.1016/j.jnt.2017.12.012).
Their Theorem 1.1 assumes

\[
 0<\delta<D/2,\qquad k^{2\delta}\le B\le k^D,
 \qquad k^{-\delta}\le\eta\le1,
\]

and proves a fixed-denominator linear upper estimate of the form

\[
 \sum_{Bk\le h<(1+\eta)Bk}\mu(h)g(h/k)
 =O\!\left((\eta Bk)^{1-\beta(\delta,D)}\right).
\]

There is a substantive rational-value problem in the displayed definition

\[
 g(x)=\sum_{\ell\ge1}\frac{1-2\{\ell x\}}{\ell}.
\]

If \(x=p/q\) is reduced, then the coefficients are \(q\)-periodic and

\[
 \sum_{\ell=1}^{q}\bigl(1-2\{\ell p/q\}\bigr)=1.
\]

Consequently

\[
 \sum_{\ell\le X}\frac{1-2\{\ell p/q\}}{\ell}
 =\frac1q\log X+O_{p,q}(1)\longrightarrow+\infty.
\]

For the centered periodic Bernoulli function

\[
 B_1^*(x)=
 \begin{cases}
  \{x\}-\tfrac12,&x\notin\mathbb Z,\\
  0,&x\in\mathbb Z,
 \end{cases}
 \qquad
 g^*(x)=-2\sum_{\ell\ge1}\frac{B_1^*(\ell x)}{\ell},
\]

one instead has, in the Vasyunin normalization used in the moving-kernel
dossier,

\[
 g^*(p/q)=-\frac{\pi}{q}V(p,q),
\]

and

\[
 \sum_{\ell\le X}\frac{1-2\{\ell p/q\}}{\ell}
 =\frac1qH_{\lfloor X/q\rfloor}+g^*(p/q)+o(1)
 =\frac{\log X+\gamma-\log q-\pi V(p,q)}q+o(1).
\]

The checked Maier--Rassias arXiv text writes the divergent ordinary series
while evaluating it at rational \(h/k\); it does not state a rational
regularization that resolves this mismatch.  Its displayed theorem should
therefore be used only after explicitly identifying and verifying the intended
centered-sawtooth, Estermann, or Vasyunin normalization.  Under such an
interpretation it remains an upper bound for one linear sum with fixed
denominator, not a lower bound for the moving two-parameter square (45.L1).

H. Maier and M. Th. Rassias, “Explicit estimates of sums related to the
Nyman--Beurling criterion for the Riemann Hypothesis,” *Journal of Functional
Analysis* **276** (2019), 3832--3857,
[arXiv:1806.05070](https://arxiv.org/abs/1806.05070),
[doi:10.1016/j.jfa.2018.06.022](https://doi.org/10.1016/j.jfa.2018.06.022).
Their Theorem 2.1, under its explicit definitions of \(D,C,v_0,z_0\), proves

\[
 \sum_{k^D\le n<2k^D}\mu(n)g(n/k)
 \ll_\varepsilon k^{D-z_0+\varepsilon}.
\]

This is again fixed-\(k\), linear, and upper-only.

### Uniform Möbius cancellation

H. Davenport, “On Some Infinite Series Involving Arithmetical Functions
(II),” *Quarterly Journal of Mathematics* os-**8** (1937), 313--320,
[doi:10.1093/qmath/os-8.1.313](https://doi.org/10.1093/qmath/os-8.1.313).
This is the Part II citation and DOI.  In modern notation, Davenport's
estimate

\[
 \sup_{\alpha\in\mathbb R}
 \left|\sum_{n\le N}\mu(n)e(\alpha n)\right|
 \ll_A N(\log N)^{-A}
\]

is an upper-cancellation theorem.  Abel summation transfers it to a scalar
weight \(v_n\) only with control of

\[
 |v_N|+\sum_{n<N}|v_{n+1}-v_n|.
\]

More complicated moving families require a separate uniform decomposition.
The theorem provides neither an \(\Omega\)-bound nor a reverse estimate for
the \(a\)-dependent moving kernel in (45.L1).

B. Green and T. Tao, “The Möbius function is strongly orthogonal to
nilsequences,” *Annals of Mathematics* **175** (2012), 541--566,
[arXiv:0807.1736](https://arxiv.org/abs/0807.1736),
[doi:10.4007/annals.2012.175.2.3](https://doi.org/10.4007/annals.2012.175.2.3).
This is also an upper-orthogonality theorem, with explicit dependence on the
complexity and Lipschitz norm.  It cannot be applied silently and uniformly
to the moving Vasyunin family, and it supplies no lower bound.

### Correlations and reciprocal phases

K. Matomäki, M. Radziwiłł, and T. Tao, “An averaged form of Chowla's
conjecture,” *Algebra & Number Theory* **9** (2015), 2167--2196,
[arXiv:1503.05121](https://arxiv.org/abs/1503.05121),
[doi:10.2140/ant.2015.9.2167](https://doi.org/10.2140/ant.2015.9.2167).
Their principal statement is an averaged additive-shift upper estimate for
Liouville; immediately after Theorem 1.6 they note that the same argument
gives Theorem 1.1 with Liouville replaced by Möbius.  The weights in (45.L1)
depend on support, ratios, gcd data, and Vasyunin kernels, not only on an
additive difference.  No direct specialization gives the needed coercivity.

W. Duke, J. Friedlander, and H. Iwaniec, “Bilinear forms with Kloosterman
fractions,” *Inventiones Mathematicae* **128** (1997), 23--43,
[doi:10.1007/s002220050135](https://doi.org/10.1007/s002220050135); and
S. Bettin and V. Chandee, “Trilinear forms with Kloosterman fractions,”
*Advances in Mathematics* **328** (2018), 1234--1262,
[arXiv:1502.00769](https://arxiv.org/abs/1502.00769),
[doi:10.1016/j.aim.2018.01.026](https://doi.org/10.1016/j.aim.2018.01.026).
These theorems give absolute upper bounds for specified bilinear or trilinear
reciprocal-phase forms.  Applying them here would first require a proved
cotangent expansion, dyadic decomposition, and treatment of the relevant
coprimality restrictions and coefficient norms.  Neither theorem by itself
gives a lower or coercive estimate for the fixed Möbius vector.

### Global Nyman--Beurling bounds

J.-F. Burnol, “A Lower Bound in an Approximation Problem Involving the Zeros
of the Riemann Zeta Function,” *Advances in Mathematics* **170** (2002),
56--70, [arXiv:math/0103058](https://arxiv.org/abs/math/0103058),
[doi:10.1006/aima.2001.2066](https://doi.org/10.1006/aima.2001.2066).
If \(D(\lambda)\) is the infimum distance over the continuous
Nyman--Beurling space \(B_\lambda\), Burnol proves

\[
 \liminf_{\lambda\to0}D(\lambda)\sqrt{\log(1/\lambda)}
 \ge
 \left(
 \sum_{\substack{\rho:\Re\rho=1/2\\
                   \rho\ \mathrm{distinct}}}
 \frac{m_\rho^2}{|\rho|^2}
 \right)^{1/2}.
\]

Burnol notes that if RH fails the left side is \(+\infty\), so the statement is
conventionally unconditional.  Because \(D(\lambda)\) is an infimum, the
global lower bound also bounds every admissible individual approximant from
below.  It does not decompose that error by coefficient vector, moving dyadic
block, row set, or the correlation dispersion \(D_a(I)\), and therefore does
not imply (45.L1).

S. Bettin, J. B. Conrey, and D. W. Farmer, “An optimal choice of Dirichlet
polynomials for the Nyman--Beurling criterion,” *Proceedings of the Steklov
Institute of Mathematics* **280** (2013), Suppl. 2, 30--36,
[arXiv:1211.5191](https://arxiv.org/abs/1211.5191),
[doi:10.1134/S0081543813030036](https://doi.org/10.1134/S0081543813030036).
Their theorem concerns the particular tapered Möbius polynomial \(V_N\), is
global, and assumes RH together with

\[
 \sum_{|\Im\rho|\le T}|\zeta'(\rho)|^{-2}
 \ll T^{3/2-\delta}.
\]

As the paper states, this hypothesis implicitly assumes simple nontrivial
zeros.  The theorem does not imply a moving-row lower bound.

### Other directly relevant recent sources

H. Maier and M. Th. Rassias, “The error for the second moment of cotangent
sums related to the Riemann Hypothesis,”
[arXiv:1806.00772](https://arxiv.org/abs/1806.00772).  Their Theorem 1.1 claims,
for prime \(q\), an unweighted residue-class second moment

\[
 \frac1{q-1}\sum_{a=1}^{q-1}c_0(a/q)^2
 =H_1q^2+E(q),\qquad E(q)\ge Cq(\log q)^2.
\]

This has neither the fixed Möbius vector nor the moving support kernel in
(45.L1).

W. Ehm, “On certain Gram matrices and their associated series,”
[arXiv:2405.06349v2](https://arxiv.org/abs/2405.06349v2).  This gives exact
global Gram formulas and decompositions; Section 8 sets aside the
Möbius-inversion error as a major challenge and labels its asymptotic
discussion tentative.  It does not prove (45.L1).

A. Pyvovarov, “A few remarks on the Báez-Duarte Criterion,”
[arXiv:2607.12084v4](https://arxiv.org/abs/2607.12084v4), dated November 21,
2026.  This studies exponentially damped global Möbius approximants and an
RH-equivalent norm criterion.  It gives no unconditional moving-block lower
bound.

## Search scope and safe conclusion

**Negative search finding as of 2026-11-25.** Searches of arXiv, zbMATH,
Crossref/OpenAlex, and the forward citation chains of Maier--Rassias, Burnol,
Bettin--Conrey--Farmer, and Ehm located no theorem implying (45.L1).  This is
not a proof of nonexistence.


Exact Vasyunin identities determine the moving matrix entries.  The directly
relevant Möbius, nilsequence, Chowla, and Kloosterman-fraction results provide
upper cancellation in different geometries.  Burnol and
Bettin--Conrey--Farmer concern global Nyman--Beurling approximation.  No
checked result supplies the reverse/coercive estimate

\[
 D_a(I)\gg(\log a)^{-3}
\]

or prevents the near-total off-diagonal cancellation of the actual moving
Möbius--Vasyunin transform.  The Cycle 45 arithmetic checkpoint therefore
remains open.
