# K4 subdivisions satisfy the conjecture

**CORRECTION**: The MaxCut-based proof below is INVALID.  The claim
`s+(G) >= MaxCut(G)` is false in general — an explicit 15-vertex
counterexample exists with `s+ ≈ 39.94 < 40 = MaxCut`.  The K4-
subdivision theorem itself remains computationally supported (all
15,625 subdivisions with path lengths 1-5 pass, min surplus 1.461)
but requires a new proof.  The combinatorial bound `MaxCut >= m-2 = n`
for K4 subdivisions is correct; only the spectral bridge `s+ >= MaxCut`
fails.

## Theorem

Every subdivision of K_4 satisfies `s^+(G) >= |V(G)|`.

## Proof

**Spectral MaxCut bound.** For every graph H,

`s^+(H) >= MaxCut(H)`.

This follows from the PSD variational formula.  Let C be the bipartite
adjacency matrix of a cut.  Since C is bipartite, `s^+(C) = |E(C)|` (the
cut size).  Using `X = C_+` in `s^+(A) = max_{X>=0} [2tr(AX)-tr(X^2)]`
and the identity `<C, C_+> = 0` for the off-diagonal cut matrix gives
`s^+(A) >= s^+(C) = cut_size`.

**Signed K4 lemma.** For every parity assignment `p: E(K4) -> F_2`,
there exists a vertex labeling `x: V(K4) -> F_2` such that at most 2 of
the 6 edges have `x_i + x_j != p_{ij}`.

Proof: choose a labeling maximizing the number of satisfied constraints.
If at most 3 are satisfied, maximality under vertex flips forces each
vertex to have `deg_sat >= 2`, giving `|E_sat| >= 4`, contradiction.

**Construction.** For a K4-subdivision with path lengths `l_{ij}`,
assign branch signs satisfying at least 4 of 6 parity constraints
`x_i XOR x_j = l_{ij} mod 2`.  Alternate signs along each path.  At most
2 edges fail to cross.  Since `m = n+2` for tricyclic graphs,

`MaxCut(G) >= m - 2 = n`.

Therefore `s^+(G) >= n`.

**NOTE**: This spectral step is INCORRECT.  The identity `<C, C_+> = 0`
does not hold; the cross-term `tr(R, C_+) = tr(R, |C|/2)` can be
negative.  See correction above.

## Remark

The key identity is `tau(G) <= 2 = m - n` for K4-subdivisions.  This
means the spectral MaxCut bound `s^+ >= m - tau` directly gives the
result without any positive surplus.  The same approach works for any
tricyclic graph with `tau <= m - n = 2`.

More generally, `s^+(G) >= m - tau(G)` (the weaker bound that held
through n=9) combined with `tau(G) <= m - n` proves Conjecture 1.2
whenever the edge-bipartization number is at most the cyclomatic
excess.
## Generalization and obstruction

The bound `tau(G) <= m - n` holds iff G contains an even cycle.  For
odd cacti (graphs whose every cycle is odd), `tau = m - n + 1` and
`MaxCut = n - 1`, so the MaxCut approach gives `s+ >= n - 1`, one unit
short.

However, all four tricyclic 2-connected kernels (4-path theta, doubled
triangle, K4, doubled C4) always contain an even cycle in any
subdivision, so `tau <= 2 = m - n` and the MaxCut proof works for all
of them.  The obstruction is specifically graphs whose block structure
consists entirely of odd cycles (odd cacti).

For odd cacti with `m = n + k`, the MaxCut bound gives `s+ >= n - 1`.
The missing unit must come from spectral surplus beyond MaxCut.  The
existing bare bicyclic theorem (which covers odd handcuffs, odd
bridge dumbbells, and odd figure-eights) provides this surplus for
`k = 1`.  For `k >= 2`, the odd cactus case remains the key
obstruction to the full MaxCut route.

The friendship graph `F_{k+1}` (k+1 triangles sharing one vertex)
has `m = n + k`, `tau = k + 1`, `MaxCut = n - 1`.  But direct
computation shows `s+ > n` for all tested cases, so the spectral
surplus beyond MaxCut is always positive.
## Odd cactus approach

For odd cacti (no even cycle), `tau = m-n+1` and `MaxCut = n-1`.  The
MaxCut bound gives `s+ >= n-1`, one unit short.  The missing unit must
come from spectral surplus beyond MaxCut.

### P3 removal for long cycles

If the cactus has a terminal cycle of length `>= 5` with three
consecutive degree-2 non-cut vertices, the improved P3 removal lemma
gives `s+ >= s+(G-v) + 17/16 >= (n-1) + 17/16 > n` by induction.
Base case: two odd cycles (bicyclic, already proved).

### Triangle cacti

The friendship graph `F_r` (r triangles sharing one vertex) has exact
spectrum with `s+(F_r) = (6r-1+sqrt(8r+1))/2 > 2r+1 = n`, surplus ~r.
Triangles are spectrally generous.  But P3 removal fails because every
induced P3 contains the cut vertex.

### Remaining obstruction

The general odd cactus case with triangle blocks needs either:
- a direct spectral argument for triangle cacti (friendship formula
  suggests it should be easy)
- a strengthened removal lemma guaranteeing a safe endpoint
- a congruence witness exploiting the star structure

For friendship graphs the exact formula already proves the result.
The general triangle cactus reduces to friendship-type cores by
block-cut tree decomposition.
