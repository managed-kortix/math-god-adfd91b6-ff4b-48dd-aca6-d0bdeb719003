# Cycle 246: terminal wall for weight and punctured-support repair

## Verdict

Neither proposed alternative closes the finite twisted-complex obstruction.

1. A shift, cell, bar, or combined weight filtration does not make the vertex
   Atiyah class a permanent cycle because the exact shifted return
   `F_i[0] -> F_j[2] -> F_i[4]` contributes in total degree two.
2. Global punctured restriction removes every cross return and preserves the
   graph normal `H^1`, but passing from vanishing of the raw obstruction to the
   class `c_k rho_k(v)` requires an unconstructed comparison map. Additive or
   traced supported Chern characters do not provide it.

Thus the spectral-sequence/weight plus leading generic-support program reaches

\[
 \boxed{\text{terminal WALL for these methods}.}
\]

This is a wall for the proposed proof architecture, not a counterexample to the
finite twisted-complex theorem. The theorem and `KI240` remain `INCOMPLETE`,
not `FAIL`.

## Exact weight obstruction

For distinct graph generators, cross Ext is concentrated in degree three. With

\[
 \operatorname {Hom}^d(F_i[r],F_j[s])
 =\operatorname {Ext}^{d-r+s}(F_i,F_j),
\]

each arrow in

\[
 F_i[0]\longrightarrow F_j[2]\longrightarrow F_i[4]              \tag{246.1}
\]

has total degree one. For normalized dual cross classes `x` and `y`, the actual
Yoneda products are

\[
 yx=\omega_i,\qquad xy=-\omega_j,                                 \tag{246.2}
\]

with nonzero self `Ext^6` classes. After the shifts, (246.2) has total degree
two, exactly the degree of the Atiyah obstruction.

A filtration can assign positive weight to (246.1), but this only relocates
the term to a later differential or extension. Grouping by support makes it a
same-vertex term; grouping by shifted cells makes it positive filtration;
adding bar length changes its page. None forces (246.2) to vanish. Moreover,
the two arrows by themselves do not define a twisted complex because their
square is nonzero, so (246.1) is a counter-path to the survival proof rather
than a bad packet. Deciding actual cancellation requires the chain-level or
minimal `A_infinity` differential, the Atiyah cocycle, and its boundary maps.

This is terminal for every argument whose only new input is a reweighting of
the known Ext grading.

## What global punctured support proves

Fix a graph `G_k` and set

\[
 V_k=A_0\setminus\bigcup_{\ell\ne k}G_\ell,
 \qquad G_k^\circ=G_k\cap V_k.
\]

The graph intersections are finite, so depth on the smooth threefold gives

\[
 H^1(G_k,N_{G_k/A_0})
 \xrightarrow{\sim}
 H^1(G_k^\circ,N_{G_k^\circ/V_k}).                               \tag{246.3}
\]

For a finite graph twisted complex `D`, restriction to `V_k` kills all other
vertices, all cross maps, and all shifted cross returns. Its generic Euler
multiplicity is `c_k`. These are genuine advances over restriction to a small
affine generic open.

They do not prove the desired implication. One still needs

\[
 o_v(D|_{V_k})=0
 \quad\Longrightarrow\quad
 c_k\rho_k(v)=0
 \text{ in }H^1(G_k^\circ,N).                                    \tag{246.4}
\]

Equation (246.4) is the finite-cell version of the punctured-support comparison
problem.

## Why the leading generic-support argument stops

On a direct sum of shifted `O_(G_k^circ)` cells, the formal leading normal
supertrace is

\[
 \sum_a(-1)^{r_a}\rho_k(v)=c_k\rho_k(v).                          \tag{246.5}
\]

The missing step is to prove that (246.5) descends from the raw endomorphism
complex of an arbitrary twisted differential to the punctured normal `H^1` and
sends raw coboundaries to zero. Saying that twisting corrections are
commutators assumes precisely this compatibility: the conormal edge must be a
chain map for the twisted endomorphism differential and for all transferred
higher operations.

Ordinary or supported Chern characters do not supply the missing map. Their
Atiyah traces are additive and factor through supported `K_0`; after HKR or
semiregularity they land in Hodge or local-cohomology targets. The known split
object already shows that such traced data can vanish while the raw Atiyah
obstruction is nonzero. Identifying the traced leading boundary with the
untraced normal class (246.5) is additional input, not a consequence of
devissage, generic multiplicity, or depth.

Restricting the domain to finite `O_G`-cell objects makes the desired statement
narrower than the full arbitrary-perfect-complex `PSC` lemma, but does not
construct the comparison. No cited theorem in the current dossier gives the
needed chain map or injectivity. Therefore the Cycle 245 repair is conditional.

## Terminal rule

Do not continue with another filtration, another page indexing, or a traced
supported invariant. This route may reopen only with one of the following
genuinely new inputs:

1. an explicit chain-level map from the twisted raw endomorphism complex to
   punctured normal cohomology, with a proof that the Atiyah cocycle maps to
   `c_k rho_k(v)`;
2. a full minimal `A_infinity` calculation proving the relevant obstruction is
   a permanent class for every finite packet; or
3. an explicit finite all-nine-zero packet, which would give `KI240 FAIL`.

Absent one of these, the finite theorem and `KI240` remain `INCOMPLETE`. No
Hodge-conjecture result is claimed.
