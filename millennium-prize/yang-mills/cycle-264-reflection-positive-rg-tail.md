# Cycle 264: one-step reflection-positive `SU(2)` character-tail obstruction

## Frozen architecture

Work on a finite, simply connected two-dimensional square lattice with free
boundary and normalized Haar measure. The fine plaquette density is

\[
 f_\beta(U)=\exp\{\beta\operatorname {Tr}(U)/2\},\qquad \beta>0.
\]

Block by a factor two. Every coarse link is the ordered product of the two fine
links on the corresponding straight path, and the coarse measure is the exact
pushforward of the fine measure. Reflections are restricted to coarse lattice
reflection lines. This is the single architecture considered below; periodic
global sectors, higher-dimensional blocks, staples, and approximate decimations
are not substituted.

The pushforward is gauge equivariant and reflection positive. If `theta` is a
coarse reflection and `F` is supported in its positive half, then the pullback
`B*F` is supported in the corresponding fine positive half and commutes with
reflection. Hence

\[
 \langle F,\theta F\rangle_{B_*\mu_\beta}
 =\langle B^*F,\theta B^*F\rangle_{\mu_\beta}\geq0.       \tag{264.1}
\]

## Exact full tail

Put `d_j=2j+1`, where `j=0,1/2,1,...`, and use orthonormal `SU(2)` characters
`chi_j`. Peter--Weyl expansion gives

\[
 f_\beta(U)=F_0(\beta)
 \left[1+\sum_{j>0}d_jc_j(\beta)\chi_j(U)\right],
 \quad
 F_j(\beta)={2\over\beta}I_{2j+1}(\beta),
 \quad
 c_j(\beta)={I_{2j+1}(\beta)\over I_1(\beta)}.            \tag{264.2}
\]

All `c_j` are strictly positive. Character convolution satisfies

\[
 (d_j\chi_j)*(d_k\chi_k)=\delta_{jk}d_j\chi_j.           \tag{264.3}
\]

After axial-tree integration, the four fine faces inside a coarse square are
four convolutions. Up to the vacuum scalar, the exact blocked plaquette density
is therefore

\[
 q^{(2)}_\beta(U)
 =1+\sum_{j>0}d_jc_j(\beta)^4\chi_j(U).                  \tag{264.4}
\]

Equation (264.4), with every half-integral `j`, is the complete representation
tail; it is not a finite-channel closure. Writing `n=2j` and using the positive
series for `I_m` gives the fixed-`beta` majorant

\[
 c_{n/2}(\beta)
 \leq e^{\beta^2/4}{(\beta/2)^n\over(n+1)!},
\]

and consequently, for `N=2J`,

\[
 \sum_{j>J}d_jc_j(\beta)^4
 \leq e^{\beta^2}
 \sum_{n>N}(n+1){(\beta/2)^{4n}\over((n+1)!)^4}.         \tag{264.5}
\]

Thus the tail is absolutely summable at every fixed coupling, but (264.5) is
not uniform on the weak-coupling ray `beta -> infinity`.

The exact action rather than Boltzmann-factor coordinates is

\[
 S^{(2)}_\beta=-\sum_P\log q^{(2)}_\beta(U_P)+\text{constant},              \tag{264.6}
\]

and its entire single-plaquette character tail is

\[
 s_\ell^{(2)}(\beta)
 =-\int_{SU(2)}\log q^{(2)}_\beta(U)\chi_\ell(U)\,dU,
 \qquad \ell=0,1/2,1,\ldots .                              \tag{264.7}
\]

There are no omitted multi-plaquette polymer couplings in this free-boundary
two-dimensional architecture: tree integration makes the blocked measure the
product of (264.4) over coarse faces. Formula (264.7) is the complete loop
action tail for each face. This simplification is special to the frozen model
and is not asserted in four dimensions.

## Uniform weighted contraction fails

Let `c=(c_j)` denote normalized positive character coordinates. On this
architecture the exact RG map is diagonal:

\[
 (Rc)_j=c_j^4.                                             \tag{264.8}
\]

Consider any representation cutoff `J` and any diagonal weighted `ell^p` or
weighted supremum norm on its complement,

\[
 \|x\|_{w,p}=\|(w_jx_j)_{j>J}\|_p,
 \qquad 0<w_j<\infty,                                    \tag{264.9}
\]

where the weights may depend on `J` but not on the point being compared. No
constant `rho<1` can make `R` a Lipschitz contraction in (264.9) on a
reflection-positive domain containing the Wilson weak-coupling ray.

Indeed, choose any `k>J`. At a Wilson point, vary only its `k`th coefficient:

\[
 c^{(\epsilon)}_j=c_j(\beta)+\epsilon\,1_{j=k}.           \tag{264.10}
\]

For sufficiently small positive or negative `epsilon`, the corresponding class
density remains pointwise positive because the Wilson density has a positive
minimum and `chi_k` is bounded. Its character coefficients also remain
nonnegative. Thus both signs stay inside the usual reflection-positive
plaquette cone. Equations (264.8)--(264.10) give

\[
 \lim_{\epsilon\to0}
 {\|R(c^{(\epsilon)})-R(c)\|_{w,p}
  \over\|c^{(\epsilon)}-c\|_{w,p}}
 =4c_k(\beta)^3.                                          \tag{264.11}
\]

The same identity holds for every `p`, including infinity, because the
difference has one coordinate and its weight cancels. The fixed-order Bessel
asymptotic implies

\[
 c_k(\beta)={I_{2k+1}(\beta)\over I_1(\beta)}\longrightarrow1
 \quad(\beta\to\infty).                                  \tag{264.12}
\]

Hence (264.11) tends to `4`. It exceeds one once
`c_k(beta)>4^(-1/3)`. Since `k` can be chosen beyond every cutoff, the family

\[
 (J,k,\beta,\epsilon),\qquad k>J,\quad \beta\to\infty,
 \quad\epsilon\to0,                                      \tag{264.13}
\]

is a representation-tail family violating every finite positive diagonal
weight budget (264.9). Equivalently, in ultraviolet deviations `a_j=1-c_j`,

\[
 1-(1-a_j)^4=4a_j+O(a_j^2),                               \tag{264.14}
\]

so infrared blocking expands, rather than contracts, every sufficiently small
UV tail deviation.

This obstruction is stronger than failure of one proposed numerical weight:
changing diagonal representation weights cannot alter the scalar derivative
on a one-coordinate tail direction. It does not exclude a non-diagonal norm, a
coupling-dependent recentering, or a block map with additional smoothing; those
are different architectures and are outside this stopped scout.

## Decision

`Y264-RG-TAIL: VIOLATING TAIL FAMILY.` The frozen step is exactly
reflection-positive and its full character/action tail is (264.4)--(264.7), but
the induced complement has UV directional multiplier tending to four. It
therefore admits no representation-cutoff-uniform strict contraction in any of
the declared positive diagonal weighted norms. Stop this architecture. This is
a finite two-dimensional lattice obstruction and makes no continuum,
four-dimensional Yang--Mills, or mass-gap claim.
