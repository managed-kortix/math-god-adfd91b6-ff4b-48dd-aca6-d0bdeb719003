# Cycle 114: portfolio and selector gate

The first post-Navier candidate was transcript-conditioned permutation-orbit
extraction for the CJSW GapMaj magnification theorem.  It is now retired at an
exact finite obstruction.

For a randomized adaptive query algorithm, a complete transcript cylinder has
a well-defined private-coin mass independent of all unqueried coordinates.  On
a fixed Hamming layer, conditioning on that transcript leaves the uniform
distribution on its completion orbit.  Consequently an individually heavy
wrong transcript transfers its wrong mass pointwise to the entire orbit.  This
is exact, but general algorithms can disperse wrong mass among exponentially
many compatible transcripts.

For three-bit random-coordinate majority, transporting a permutation back to a
canonical weight-one or weight-two representative transports the seed as
`j=pi^{-1}(i)`.  Requiring this transported seed to remain uniform fixes the
error mass at exactly `1/3`: error is precisely the event `j=1`.  The rational
dual certificate is `(y1,y2,y3)=(1,0,0)`.  Conditioning entirely onto errors
while preserving the seed law would require the same linear form to equal both
`1` and `1/3`.  Preserving only the physical seed allows the permutation to
encode the bad seed and is the forbidden quantifier swap.

More generally, conditional-expectation orbit descent must evaluate the full
randomized error potential.  Even a zero-query algorithm can encode an
arbitrary circuit in its random-tape output, so exact potential evaluation
contains a counting threshold.  Query sparsity alone does not provide the
uniform selector.  The CJSW quantifiers remain

\[
 \forall A\;\exists R_A\;\exists^\infty n,
\]

not eventual success, and a wrong execution is not a semantic refutation of a
bounded-error randomized algorithm.

## Other scouts

- Sparse-NP magnification is full reach, but padding Exact-3SAT turns a mildly
  superlinear padded lower bound back into a superpolynomial unrestricted
  payload lower bound.  A native sparse family and junk-robust invariant are
  still missing.
- BSD `p`-primary packets cannot determine prime-to-`p` factors of the complex
  leading term; the determinant-line comparison is the missing refined BSD or
  ETNC bridge itself.
- RH Stieltjes--Hankel positivity reconstructs positive support of the squared
  zero spectrum and is therefore another exact RH-equivalent criterion.
- A cutoff-uniform Yang--Mills sum-of-squares identity would imply a lattice
  gap, but one-plaquette `SU(2)` already gives a fixed-spin truncation tail of
  norm `1/g^2`; both representation cutoff and physical support must diverge.
- The proposed Fermat dodecic Hodge orbit
  `(1,1,8,8,9,9)` is indeed a four-dimensional rational `(2,2)` orbit and has
  no proper zero-sum coordinate block.  It is nevertheless prior work:
  Shioda's 1979 theorem verifies the relevant semigroup condition for every
  degree at most `20`, including degree `12`.  It is not a new Hodge case.

The next Hodge scout must begin beyond Shioda's covered degrees and pass the
primary-source gate before any explicit-cycle search.  No Millennium result is
claimed.
