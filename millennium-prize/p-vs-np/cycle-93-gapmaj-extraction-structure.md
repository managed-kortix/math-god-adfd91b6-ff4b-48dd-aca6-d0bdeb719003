# Cycle 93: structure of constructive GapMaj extraction

## Symmetric subclass theorem

Let the strict promised boundary weights be
\[
 \ell_n=\lceil n(1/2-\varepsilon)\rceil-1,
 \qquad
 u_n=\lfloor n(1/2+\varepsilon)\rfloor+1.
\]
For any randomized adaptive `q=o(epsilon^-2)` query algorithm whose majority
answer is constant on each of these two Hamming layers, one of
\[
 L_n=1^{\ell_n}0^{n-\ell_n},\qquad
 U_n=1^{u_n}0^{n-u_n}
\]
is an error for infinitely many lengths.  This includes permutation-invariant
algorithms.  The proof compares the two without-replacement transcript laws:
\[
 d_{TV}(T_{\ell_n},T_{u_n})=O(\varepsilon\sqrt q)=o(1).
\]
If both layer-majority answers were correct, their output distributions would
be separated by at least `1/3`, a contradiction.  Infinite pigeonhole chooses
one fixed side for infinitely many lengths.

If the boundary indices are computable in polylogarithmic time from binary
`n`, the corresponding canonical strings form polylogtime-uniform depth-zero
`AC0` families.  CJSW's weaker assumption that `1/epsilon` is computable in
`poly(1/epsilon)` time does not by itself establish this extra uniformity.

For a deterministic adaptive algorithm whose entire execution is
polylogarithmic, the classical adversarial transcript can similarly be
completed canonically to opposite promised layers, giving an algorithm-
dependent uniform depth-zero error.  Small uniformly enumerable random support
also works when the union of the all-zero-path query sets leaves enough free
coordinates.  These are exact restricted constructive theorems, not the CJSW
hypothesis.

## Exact semantic structure

For an arbitrary randomized depth-`q` query algorithm,
\[
 m_A(x)=\mathbb E_r T_r(x)
\]
is a convex combination of depth-`q` decision trees and hence a multilinear
polynomial of degree at most `q`.  Its semantic majority is a degree-`q`
polynomial threshold function.  Moreover
\[
 \sum_i \operatorname{Inf}^{(1)}_i(m_A)\le q.
\]
Thresholding destroys these influence bounds without a margin: random
one-coordinate sampling has a linear mean but semantic majority equal to full
majority.

The hypergeometric minimax dual gives an explicit hard orbit
\[
 \{\pi L_n,\pi U_n:\pi\in S_n\}
\]
and proves that some orbit point is an error.  Symmetrizing `A` makes a
canonical representative hard only for the symmetrized algorithm; transferring
back requires selecting a good permutation.  Conditional expectations over
permutations and private coins can encode counting, so this is precisely the
missing uniform selector.

Generic low-degree-PTF generators do not close the gap.  Here
`q=o(epsilon^-2)` can still be `(log n)^omega(1)`, the generic
`THR o AND_q` representation has size `n^O(q)`, and known generators neither
give the needed parameters nor automatically have plain uniform-`AC0` output.

## Rotation gate

Canonical strings, symmetry, minimax, low degree, bounded influence, limited
independence, and symmetrization all stop at the same extraction boundary.
The exact remaining statement is an algorithm-dependent uniform selector for
the dense semantic error set of every unrestricted randomized adaptive query
algorithm.  That assertion is the constructive lower bound itself, not a
consequence of ordinary query hardness.  No `P != NP` result is claimed.
