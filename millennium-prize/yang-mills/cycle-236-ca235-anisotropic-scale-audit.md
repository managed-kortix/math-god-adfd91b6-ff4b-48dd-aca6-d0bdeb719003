# Cycle 236: hostile `CA235` anisotropic scale audit

## Decision

`CA235 FAIL`.

The terminal `BR235 PASS` theorem is an explicit finite-spatial-lattice,
strong-coupling spectral-gap theorem. It advances no named quantifier in the
official Clay statement. No anisotropic Hamiltonian continuum theorem can use
its certified parameter region along the Yang--Mills cutoff-removal trajectory:
anisotropy can convert the Euclidean temporal lattice into Hamiltonian time,
but it does not convert the electric-dominated strong-coupling ratio into the
magnetic-dominated weak-coupling ratio required as the spatial cutoff vanishes.

## 1. Exact theorem being tested

For the dimensionless Kogut--Susskind operator

\[
 K_\lambda=C+\lambda W,
 \qquad \lambda={2\over g^4},
\]

Cycle 235 proves, on each admissible finite periodic spatial torus,

\[
 0\leq\lambda\leq\lambda_*,\qquad
 \lambda_*={1\over8(15970360332)^{416}},
 \qquad
 \Delta(K_\lambda)\geq
 \gamma_*={\log3-1\over56\log15970360332}.
 \tag{236.1}
\]

Restoring the standard Hamiltonian energy normalization gives

\[
 H_{a,g}={g^2\over2a}K_{2/g^4},
 \qquad
 \Delta(H_{a,g})\geq {g^2\over2a}\gamma_*              \tag{236.2}
\]

only when `2/g^4<=lambda_*`. Equivalently,

\[
 g\geq g_*:=\left({2\over\lambda_*}\right)^{1/4}
 =\bigl(16(15970360332)^{416}\bigr)^{1/4}.               \tag{236.3}
\]

Thus the certificate is confined to a fixed, extremely large bare-coupling
half-line. Constants conventionally introduced by a fixed anisotropy only
replace `lambda` by `c_xi/g^4` with `0<c_xi<infinity`; they do not change the
inverse fourth power or the conclusion.

## 2. Exact scale mismatch

Let `a_k->0` be a proposed spatial cutoff-removal sequence for four-dimensional
Yang--Mills. The required ultraviolet trajectory has `g_k->0`, hence

\[
 \lambda_k={2\over g_k^4}\longrightarrow\infty.          \tag{236.4}
\]

The certified set in (236.1) is the closed bounded interval
`[0,lambda_*]`. Therefore, by the definition of divergence, there is a finite
`k_0` such that

\[
 k\geq k_0\quad\Longrightarrow\quad
 \lambda_k>\lambda_* .                                   \tag{236.5}
\]

The theorem applies to at most a finite initial segment of any continuum
sequence and to no cofinal subsequence. This is a domain mismatch, not merely a
poor numerical constant. Replacing `lambda_*` by any finite strong-coupling
radius leaves (236.5) unchanged.

The dimensional prefactor in (236.2) cannot repair the mismatch. Multiplying a
dimensionless lower bound by `g_k^2/(2a_k)` is valid only after establishing
that the bound applies at `lambda_k`; (236.5) removes that premise. Moreover,
even a cofinal physical-energy lower bound would not construct a nontrivial OS
limit or identify its continuum Hamiltonian spectrum.

## 3. Anisotropic Hamiltonian audit

There are only three possible uses of anisotropy, and none transfers (236.1).

1. **Temporal continuum at fixed spatial lattice.** Sending the temporal
   spacing to zero derives or studies the Kogut--Susskind Hamiltonian on a
   fixed spatial lattice. Cycle 235 already concerns that Hamiltonian. The
   operation neither sends the spatial spacing to zero nor changes
   `lambda=2/g^4`, so it reaches no theory on `R^4`.
2. **Fixed finite anisotropy during spatial cutoff removal.** A finite positive
   anisotropy factor changes normalization by finite constants. Along `g_k->0`
   the magnetic/electric ratio still diverges, so the finite certified interval
   and the continuum trajectory are eventually disjoint.
3. **Cutoff-dependent singular anisotropy.** Choosing an anisotropy factor that
   tends to zero fast enough to keep a redefined coefficient small does not
   invoke Cycle 235 for the target Hamiltonian. Either the common energy
   rescaling restores the same divergent physical magnetic/electric ratio, or
   the limiting action suppresses spatial curvature and is not isotropic
   four-dimensional Yang--Mills. A theorem identifying such a singular family
   with a nontrivial Euclidean-invariant OS Yang--Mills limit would itself have
   to supply the missing scale-uniform comparison, tightness, restoration of
   symmetry, and spectral transfer. No such theorem is among the Cycle 235
   hypotheses or conclusions.

Consequently there is no anisotropic Hamiltonian continuum theorem to which
the finite-lattice certificate is a verified premise. Any proposed theorem
that assumes a gap uniformly along the weak-coupling trajectory would assume
the missing bridge rather than derive it from `BR235`.

## 4. Named Clay quantifier audit

The official target asks, for every compact simple `G`, for a nontrivial quantum
Yang--Mills theory on `R^4` satisfying Wightman/OS-strength axioms and having a
Hamiltonian gap `Delta>0`. The Cycle 235 result proves none of the following
named quantified obligations:

1. cutoff removal and existence on `R^4`;
2. nontriviality of the continuum theory;
3. Wightman/OS axioms, including reconstruction and Euclidean symmetry;
4. a positive spectral gap for the reconstructed continuum Hamiltonian;
5. the required statement for every compact simple gauge group.

Its finite-volume uniformity concerns the exponent of a lattice estimate at
fixed small `lambda`; it is not any one of these continuum quantifiers.

## 5. `CA235` scoring

1. **Physical scaling: `FAIL`.** The only certified couplings satisfy
   `lambda<=lambda_*`, while every ultraviolet sequence has
   `lambda_k->infinity`.
2. **Non-equivalent production lemma: `FAIL`.** There is no scale-uniform
   weak-coupling estimate for OS tightness, nontriviality, symmetry restoration,
   or positive physical mass.
3. **Finite falsifier: `FAIL` for admission.** Cycle 235 has exact finite
   checks for its boundary expansion, but no finite block with an analytic
   complement bound testing a continuum production lemma.
4. **Official transfer: `FAIL`.** There is no implication to a named Clay
   quantifier; the domain disjointness in (236.5) blocks even the first use of
   the lattice gap on a cofinal cutoff sequence.

Under the frozen rule, terminal `BR235 PASS` plus `CA235 FAIL` preserves the
explicit lattice theorem, closes further boundary-polymer work as a main-funnel
activity, and triggers portfolio rotation. Re-entry requires materially new
weak-coupling continuum input satisfying all four `CA235` tests.

No continuum Yang--Mills theory or mass gap is claimed.
