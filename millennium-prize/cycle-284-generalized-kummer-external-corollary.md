# Cycle 284: version-pinned generalized-Kummer external corollary

## Scope and status

A post-Cycle-283 source update changes one Hodge special-family record.  This
cycle audits only the literal composition of two recent external preprints:

1. Salvatore Floccari and Lie Fu, *On the Hodge conjecture for hyper-Kähler
   varieties of generalized Kummer type of dimension divisible by four*,
   [`arXiv:2610.31740v1`](https://arxiv.org/abs/2610.31740v1), submitted
   2026-10-22;
2. Josiah Foster, *The Lefschetz standard conjectures for 4d-dimensional
   Kummer-type hyper-Kaehler varieties*,
   [`arXiv:2512.04114v2`](https://arxiv.org/abs/2512.04114v2), revised
   2026-10-27.

The result below is an immediate **external corollary** of their stated
results.  It is not proved by this repository, is not claimed as novel, and is
not a resolution of the Clay Hodge conjecture.  Both inputs are very recent
preprints.  The audit checks theorem matching and exposed dependencies; it is
not an independent line-by-line certification of the two long proofs.

PDFs downloaded from the versioned arXiv URLs on 2026-11-03 had the following
checksums:

```text
863e0d69c8367051d283094e345cd129d80eebd29a356f19ea77f45801d5f7e7  2610.31740v1.pdf  (49 pages)
074610ad87cd45d08373b39b4e8f592eecb488c38780d254604a9144ecdafdd7  2512.04114v2.pdf  (47 pages)
```

## Exact external corollary

Let `d,r >= 1`, and let `K` be a projective complex irreducible holomorphic
symplectic manifold of generalized Kummer deformation type with

```text
dim_C K = 4d.
```

Then, at the level of the cited theorem statements, the rational Hodge
conjecture holds for `K^r` in every codimension.  Equivalently, for every
`0 <= p <= 4dr`, the cycle-class map is surjective:

```text
CH^p(K^r)_Q -> H^(2p)(K^r,Q) intersect H^(p,p)(K^r,C).
```

Floccari--Fu also imply that `K` is motivated by its third intermediate
Jacobian.

## Literal theorem composition

### Foster supplies the full Lefschetz standard conjecture

Foster's Conjecture 1.1 is the full Lefschetz standard conjecture: in each
allowed degree the inverse hard-Lefschetz isomorphism is induced by a rational
algebraic self-correspondence.  His Theorem 1.7, restated and proved as Theorem
8.15, says:

> Let `Z` be a projective IHSM of generalized Kummer type of complex dimension
> `4d`, `d >= 1`. Then the Lefschetz Standard Conjecture 1.1 holds for `Z`.

Thus it supplies `B(K)` for every projective target in the stated deformation
class, not merely for a seed variety or in one cohomological degree.

### Floccari--Fu consume exactly that hypothesis

Floccari--Fu Theorem 1.4 says:

> Let `K` be a hyper-Kähler variety of `Kum^n`-type, for some `n >= 2` even,
> and let `J` denote the third intermediate Jacobian of `K`. Assume that the
> Lefschetz standard conjecture holds for `K`. Then `K` is motivated by `J`,
> and the Hodge conjecture holds for `K` and all of its powers.

For generalized-Kummer type, their convention is

```text
dim_C K = 2n.
```

If Foster's target has dimension `4d`, then `n=2d`, which is even and at least
`2`.  Therefore

```text
Foster Theorem 8.15 => B(K)
                         +
2n=4d => n=2d even       +
Floccari--Fu Theorem 1.4
                         => HC(K^r) for every r>=1 and every codimension.
```

No prime condition remains.  The requirement that `n+1` be prime belongs to
Floccari--Fu Theorem 1.2 and Corollary 1.3, not to Theorem 1.4.

## Hostile dependency audit

Four disjoint checks were run: theorem composition, hidden hypotheses,
precedence/status, and comparison with the official Clay quantifiers.  The
composition survived the following specific attacks.

1. **Former semiregularity contingency.** Floccari--Fu v1 predates Foster v2 by
   five days.  Its Remark 1.5 accurately describes Foster v1 as conditional on
   a semiregularity conjecture, but Foster v2 explicitly says that the
   contingency condition has been dropped.  Foster v2 Theorem 2.18 proves the
   analytic deformation statement used in the final argument.  Remark 1.5 is
   chronologically stale relative to v2; it is not a residual hypothesis in
   Theorem 8.15.
2. **Fourier--Mukai, stability, and polarization assumptions.** These appear in
   Foster's general Theorem 1.8/9.2 and in the construction of a seed kernel.
   The specialized Theorem 8.15 discharges them in its proof and quantifies
   over every projective generalized-Kummer-type target of dimension `4d`.
   They are not additional assumptions on `K` in the composed corollary.
3. **Degree range.** Foster's Conjecture 1.1 is the full Lefschetz standard
   conjecture, not a degree-two fragment.  Floccari--Fu require it for `K`
   alone and conclude the Hodge conjecture for every self-power; they do not
   separately assume the standard conjectures for every `K^r`.
4. **Coefficients and base field.** The correspondences, motives, and Hodge
   classes are rational, and the varieties are complex and projective.  This
   matches the rational Clay formulation on this restricted class.
5. **Revision status.** At the 2026-11-03 cutoff, arXiv shows only v1 for
   Floccari--Fu and v2 as Foster's latest version.  No correction, withdrawal,
   or theorem-specific public criticism was located in the bounded status
   check.  This is not a substitute for refereeing.

A bounded search of the two papers, version histories, author pages, public
citation records, and exact-title/status results did not locate the combined
unconditional statement written explicitly elsewhere.  This is only
`DERIVED-NOT-FOUND`, not a global novelty claim.  Since the deduction is direct
substitution and modus ponens, it must be cited as an external dependency
synthesis rather than as a theorem of this project.

## Exact Clay boundary

The official conjecture quantifies over **every** smooth projective complex
variety `Y`, every codimension `p`, and every rational `(p,p)` class on `Y`.
The external corollary proves the desired surjectivity only for

```text
Y = K^r,
K projective of generalized Kummer deformation type,
dim_C K = 4d,
d,r >= 1.
```

It does not cover, among many other missing classes:

- arbitrary smooth projective varieties;
- generalized-Kummer-type bases of dimensions `4d+2` by this composition;
- other hyper-Kähler deformation types;
- mixed products of distinct generalized-Kummer-type varieties;
- arbitrary abelian varieties, hypersurfaces, complete intersections, or
  varieties of general type; or
- any reduction placing the motive of every smooth projective variety in the
  tensor category generated by this class.

Unbounded dimension inside one deformation family does not approach the
universal variety quantifier.  The Clay Hodge conjecture remains open.

## Relation to the stopped PEL/graph route

This external corollary supplies none of the missing finite data in the stopped
quartic-CM/PEL route: no cycle on the retained abelian sixfold, no common-model
PEL representatives, no chain-level Atiyah--Kodaira--Spencer map, and no
semiregularity certificate for the retained graph object.

Floccari--Fu use the fact that the generalized-Kummer motive is generated by
its third intermediate Jacobian, an abelian fourfold of Weil type, together
with already known Hodge results for powers of that Jacobian.  This implication
runs from the abelian input to `K`; it does not reverse to prove the Hodge
conjecture for an unrelated quartic-CM abelian sixfold.  Accordingly the new
source supersedes any need to prove the same `4d` generalized-Kummer endpoint
by the stopped route, but it neither repairs nor reopens that route.

## Disposition

Record the exact external family and retain deliberate wait.

- No project paper is created: this is not our theorem.
- No publication or announcement workflow is triggered.
- No stopped route is reopened.
- A future source revision must be re-audited against the exact versioned
  statements above.
- Hodge re-entry still requires an independently supplied, finitely gated
  object with an official-facing implication beyond already covered special
  families.

Record:

`FLOCCARI--FU 2610.31740v1 THEOREM 1.4 PLUS FOSTER 2512.04114v2 THEOREM 8.15
LITERALLY COMPOSE; RATIONAL HODGE HOLDS EXTERNALLY FOR ALL SELF-POWERS OF EVERY
PROJECTIVE GENERALIZED-KUMMER-TYPE IHSM OF COMPLEX DIMENSION 4d; VERSION-PINNED
EXTERNAL COROLLARY ONLY; NO NOVELTY OR OWNERSHIP CLAIM; UNIVERSAL CLAY
QUANTIFIER UNTOUCHED; STOPPED PEL/GRAPH ROUTE NOT REOPENED; NO PUBLICATION AND
NO MILLENNIUM CLAIM.`
