# Cycle 201B: clean-union smoothings cannot cancel the dense graph obstruction

## Question

Let

\[
 A_0=E_i^3\times E_i^3,
 \qquad T_0S=M_3(\mathbb C),
 \qquad Q=\operatorname {diag}(1,1,3),
\]

and consider a connected reduced codimension-three union

\[
 Z=\bigcup_{a=1}^r G_a\subset A_0
\]

of smooth graphs. The intersections may be clean and nontransverse. We ask
whether a smoothing of `Z`, with geometrically irreducible general support, can
project onto all nine PEL directions even though the individual graphs do not.

## Dense-open lemma for a clean union

Put

\[
 D_a=G_a\cap\bigcup_{b\ne a}G_b,
 \qquad U_a=G_a\setminus D_a.
\]

Assume `U_a` is dense in `G_a`, as it is for distinct graphs. Restriction of an
embedded first-order deformation to `U_a` gives a first-order deformation of
the single embedding `U_a subset A_0`. Consequently its base tangent `B` must
satisfy

\[
 \rho_a(B)|_{U_a}=0,                                               \tag{201B.1}
\]

where `rho_a` is the normal Kodaira--Spencer map of `G_a`.

For a clean union, the local smoothing module `T_Z^1` and the gluing terms in
the normal-complex description are supported on the multiple locus
`D=union D_a`. They can change matching along `D`, but restrict to zero on every
`U_a`. For these graph embeddings the normal obstruction is represented by a
constant homomorphism, so vanishing on the dense open is equivalent to
vanishing of the graph obstruction. Therefore

\[
 \boxed{
 \operatorname {im}\bigl(T_{[Z]}\operatorname {Hilb}(\mathcal A/S)
       \longrightarrow T_0S\bigr)
 \subseteq \bigcap_{a=1}^r\ker\rho_a.}                            \tag{201B.2}
\]

The same necessary inclusion holds for any Hilbert branch whose universal
subscheme remains reduced with these generic components. Passing from this
Hilbert statement to an arbitrary Chow branch requires care: the Hilbert-to-
Chow morphism need not identify tangent spaces at a reducible cycle. The
relative-Chow conclusion below applies to smoothing germs supplied by such an
embedded family, which is the architecture under test, not to every possible
Chow tangent at the same cycle point. Compatibility on `D` may make the actual
embedded image smaller.

Crucially, (201B.2) is unaffected by the general fiber. The general support may
be smooth, connected, and geometrically irreducible. At the reducible special
fiber, a first-order PEL tangent still restricts to every dense branch open.
Thus a smoothing parameter cannot transfer an obstruction from one graph to
another before the graph obstructions themselves vanish.

## Exact PEL image

For the scalar transformed graphs in the effective projector endpoints,

\[
 \rho_k(B)=Q^{-1}B^t-5^kB.                                       \tag{201B.3}
\]

Exact elimination from Cycles 169 and 197 gives

\[
 \dim\ker\rho_0=3,
 \qquad \ker\rho_k=0\quad(1\le k\le6).                           \tag{201B.4}
\]

Hence any connected clean union containing one of `G_1,...,G_6` has zero PEL
tangent image. Joining components, making their intersections nontransverse,
or smoothing the union to an irreducible cycle does not alter this conclusion.
In particular, if the positive and negative Cycle 169 endpoints are changed
only by connecting and cleanly smoothing their displayed graph components,

\[
 \boxed{\operatorname {im}(dp_+)=
        \operatorname {im}(dp_-)=
        \operatorname {im}(dp_+\times_S dp_-)=0.}                 \tag{201B.5}
\]

The smallest nontransverse pair is a less degenerate calibration. For
`G_0=Gamma_I` and `G_1=Gamma_D`, `D=diag(3,1,1)`,

\[
 \rho_0(B)=Q^{-1}B^t-B,
 \qquad \rho_1(B)=Q^{-1}B^t-DB.
\]

Their common kernel is one-dimensional. Thus every clean smoothing of this
connected union has PEL image of dimension at most one and PEL obstruction rank
at least eight. Its known irreducible smoothing `C_t times E_i^2` supplies no
cancellation beyond this bound.

## Signed endpoint equality does not cancel the raw obstruction

Suppose reduced clean unions `Z^+` and `Z^-` satisfy

\[
 [Z^+]-[Z^-]=D_0\alpha_0.
\]

The right side is horizontal, so after semiregularity the two endpoint
obstructions have equal cohomological images. This is not cancellation in the
relative pair space. Its base tangent is

\[
 \operatorname {im}(dp_+)\cap\operatorname {im}(dp_-),
\]

and each endpoint image separately obeys (201B.2). Signs are invisible to
these two embedded-deformation conditions. Equality of the signed class can
therefore cancel the cohomological trace while both effective supports remain
PEL-rigid.

Nor does a common effective graph bridge help. Adding the same clean graph
union `H` to both endpoints preserves their signed difference but imposes the
additional conditions `rho_G(B)=0` for every branch `G` of `H`. It can only
shrink the PEL image.

## Outcome

Connected codimension-three smoothings of reduced nontransverse graph unions
do not supply global obstruction cancellation. The obstruction is not the
existence of an irreducible smoothing; it is branchwise restriction at the
special fiber. This closes the reduced clean-union architecture before the
second-order gate.

A viable candidate must defeat the hypothesis behind (201B.2): it must be
support already generically irreducible at the special fiber, a generically
nonreduced or linked object whose differential is nonzero at every generic
branch, or genuinely new non-graph support with an individually rank-nine PEL
tangent image. Producing such a support at the fixed endpoint degrees, together
with an explicit rational-equivalence incidence, remains open. No Hodge-
conjecture result is claimed.
