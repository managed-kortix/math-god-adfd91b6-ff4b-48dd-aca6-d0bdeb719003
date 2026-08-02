# Cycle 263: publication-gate literature audit for `Sha(43a1/Q)=0`

## Decision

**NO-GO for publication, author contact, OCB action, or X announcement.**

The algebraic statement

\[
 \Sha(43a1/\mathbf Q)=0
\]

is a valid curve-specific theorem if the Cycle 261--262 certificates are
accepted. It is not a Millennium Prize result and this audit finds no
defensible publication novelty. The result is a routine low-conductor
specialization of the classical Gross--Zagier--Kolyvagin method, with the
remaining prime `2` handled by an ordinary full 2-descent. Public databases
have long recorded all of the curve data needed to recognize and run this
calculation, and standard Sage functionality exposes the Kolyvagin bound as a
general computation.

No searched source was found that prints the literal sentence
`Sha(43a1/Q)=0` as a named theorem. That narrow bibliographic fact is not a
novelty basis: a result need not have been stated curve-by-curve to be an
immediate, routinely computable specialization of a published general
theorem.

Under `research/procedural/PUBLICATION.md`, stop before every external action.
The repository may retain the internally generated `sha-43a1/` reproducibility
paper required by the research contract, but it is not a preprint submission or
announcement package. Do not create a publication-manifest row, OCB submission
or resolution report, email thread, or X post. No external action was taken.

## 1. Exact scope audited

The curve is

\[
 E: y^2+y=x^3+x^2,
\]

with Cremona label `43a1` and LMFDB label `43.a1`. The audited statement is
only the vanishing of the algebraic Tate--Shafarevich group of this one curve
over `Q`. It does not establish BSD for a family, the full BSD leading-term
formula even for this curve by a new method, or any part of the universal
Birch--Swinnerton-Dyer conjecture required by the Millennium problem.

## 2. What the established literature already supplies

### Kolyvagin's general theorem

V. A. Kolyvagin, "On the structure of Shafarevich--Tate groups," in
*Algebraic Geometry* (Chicago, 1989), LNM 1479 (1991), 94--121, DOI
`10.1007/BFb0086267`, gives the Heegner-point Euler-system bound. The exact
convenient formulation used here is B. Cha, "Vanishing of some cohomology
groups and bounds for the Shafarevich--Tate groups of elliptic curves,"
*J. Number Theory* 111 (2005), 154--178, DOI
`10.1016/j.jnt.2004.08.009`, Theorem 3:

\[
 \operatorname{ord}_p\#\Sha(E/K)\leq 2m_p
\]

for an odd prime `p` when the maximal-order Heegner point has infinite order
and the residual representation is `GL_2(F_p)`. Cycle 262 checks the theorem
text and records that this formulation does not exclude `p | D_K` or `p | N`.

For `K=Q(sqrt(-7))`, the conductor prime `43` splits. The project certificates
identify the normalized Heegner point with `P=(0,0)`, prove
`E(K)_free=ZP`, and prove full residual image for every prime. Thus `m_p=0`
for every odd `p`, so the published theorem gives

\[
 \Sha(E/K)[p^\infty]=0
 \quad\text{for every odd }p.
\]

Restriction--corestriction injects the odd-primary part over `Q` into that
over the quadratic field, proving the same odd-primary vanishing over `Q`.

### The remaining 2-primary part

A complete 2-descent computes

\[
 \dim_{\mathbf F_2}\operatorname{Sel}^{(2)}(E/\mathbf Q)=1,
 \qquad \operatorname{rank}E(\mathbf Q)=1,
 \qquad E(\mathbf Q)[2]=0.
\]

The Kummer exact sequence therefore gives `Sha(E/Q)[2]=0`. Kolyvagin's
theorem also gives finiteness of `Sha(E/Q)` in analytic rank one. A nonzero
finite 2-primary group has nonzero 2-torsion, so the entire 2-primary part is
zero. Combining this with the odd-primary result proves the displayed
curve-specific theorem.

This is standard descent plus Kolyvagin. The elaborate exact CM and residual
image certificates in the repository reduce software and normalization trust
boundaries; they do not create a new general arithmetic mechanism.

## 3. Database and software record

The LMFDB `43.a1` page and its underlying-data record currently give:

- equation `[0,1,1,0,0]`, conductor `43`, and discriminant `-43`;
- rank and analytic rank `1`, trivial torsion, and generator `(0,0)`;
- Tamagawa product `1`, modular degree `2`, and Manin constant `1`;
- `nonmax_primes=[]`, meaning maximal mod-prime image at every prime;
- database field `sha=1` and analytic value `sha_an=1.000...`.

The reliability page is decisive about interpretation. For positive-rank
curves the database's analytic order of Sha is computed approximately and
rounded; it is not by itself a proof that the algebraic group vanishes. The
same distinction applies to Cremona's BSD table: its `43 A 1` row records
analytic order `1.0`, while the table documentation says positive-rank values
are approximate. These records are strong prior evidence and show that the
answer has long been expected, but they are not the final algebraic argument.

Cremona's generator data records the exact rank-one generator for `43a1`.
LMFDB states that rank and generator computations here use rigorous standard
algorithms, and that mod-prime images are rigorously computed using the
published Sutherland and Zywina algorithms.

Sage's public Tate--Shafarevich-group interface makes the status especially
clear:

1. `EllipticCurve('43a1').sha().an_padic(5)` is an explicit documentation
   example returning `1 + O(5)`; the documentation calls this value
   conjectural, so it is evidence rather than the proof.
2. `bound_kolyvagin(D=...)` is a general routine returning the possible prime
   divisors of algebraic Sha and the odd Heegner index. Its documented
   algorithm applies Kolyvagin's theorem, includes `2` separately, and adds
   non-surjective residual primes. For the certified `D=-7`, odd index one,
   and empty non-surjective list here, the general computation leaves only
   `2`; the full 2-descent removes it.
3. `two_selmer_bound()` is the standard companion computation of the
   2-torsion rank of Sha once the Mordell--Weil rank is determined.

Accordingly, the theorem is not merely consistent with a rounded BSD quotient:
it is computable by a standard, publicly documented Kolyvagin-plus-descent
workflow.

## 4. Curve-specific literature search

The bounded search performed on 2026-08-02 checked:

- LMFDB's curve page, underlying data, source page, and reliability page;
- Cremona's online elliptic-curve data documentation, BSD table, and
  generator table;
- Kolyvagin's original chapter and Cha's explicit published bound;
- Sage's current Tate--Shafarevich documentation and source implementation;
- exact-label and exact-equation metadata queries through arXiv, OpenAlex,
  and Crossref.

Exact-label metadata searches for `43a1` produced unrelated uses of the same
string and no curve-specific mathematics paper. No located primary paper
advertised the literal vanishing statement for this label. Search engines and
metadata indexes are incomplete, equation notation varies, and old tables are
not fully text-indexed, so this is not an exhaustive priority search and must
not be stated as proof that no such printed sentence exists.

The stronger and publication-relevant fact is positive rather than negative:
the general proof route is classical, the curve has been in published
low-conductor tables since the 1990s, and modern public software directly
implements the relevant bound. A curve-label specialization with no new
method, obstruction, family theorem, or unexpectedly nontrivial group has
negligible novelty even if no author bothered to print the final sentence.

## 5. Publication-gate application

`PUBLICATION.md` requires both an exact sourced novelty check and a complete,
independently reproducible publication package before any external action.
This candidate fails earlier on significance and novelty:

| destination/action | decision | reason |
|---|---|---|
| manuscript, preprint, or journal | **NO** | routine single-curve specialization; no new method or broader theorem |
| X announcement | **NO** | policy reserves X for a finished theorem worth announcing; this would misframe standard low-conductor arithmetic as a discovery |
| author/expert contact | **NO** | no novel major result, correction, or unresolved source question justifies consuming an outreach thread |
| OCB submission/report | **NO** | not an exact full resolution of BSD; a one-curve case is not a Millennium kill |
| publication manifest row | **NO** | no eligible external result or package is being advanced |
| internal retention | **YES** | retain the arithmetic packet as a reproducibility and theorem-application case study |

The repository now contains an internal `paper.tex` and built `paper.pdf`, and
an independent hostile referee accepted the argument after editorial repairs.
That packaging does not cure absent novelty and does not alter the external
no-go decision.

## 6. Final classification

Record:

`ROUTINE/KNOWN-IN-PRACTICE -- ALGEBRAIC VANISHING FOLLOWS FROM CLASSICAL`
`KOLYVAGIN PLUS FULL 2-DESCENT; NO LITERAL CURVE-SPECIFIC PRINTED THEOREM`
`LOCATED; NO NOVELTY CLAIM; NO PUBLICATION, CONTACT, OCB, OR X ACTION.`

## Source anchors

- LMFDB curve: `https://www.lmfdb.org/EllipticCurve/Q/43/a/1`
- LMFDB underlying data: `https://www.lmfdb.org/EllipticCurve/Q/data/43.a1`
- LMFDB reliability: `https://www.lmfdb.org/EllipticCurve/Q/Reliability`
- LMFDB sources: `https://www.lmfdb.org/EllipticCurve/Q/Source`
- Cremona data documentation: `https://johncremona.github.io/ecdata/`
- Cremona BSD table: `https://raw.githubusercontent.com/JohnCremona/ecdata/master/allbsd/bsd.1-1000`
- Kolyvagin: `https://doi.org/10.1007/BFb0086267`
- Cha: `https://doi.org/10.1016/j.jnt.2004.08.009`
- Sage Sha documentation:
  `https://doc.sagemath.org/html/en/reference/arithmetic_curves/sage/schemes/elliptic_curves/sha_tate.html`
- Sage implementation:
  `https://github.com/sagemath/sage/blob/develop/src/sage/schemes/elliptic_curves/sha_tate.py`
- Internal theorem-text audit:
  `cycle-262-43a1-kolyvagin-theorem3-literature-audit.md`
- Internal arithmetic packet: `43a1/README.md`
- Publication policy: `../../../research/procedural/PUBLICATION.md`
