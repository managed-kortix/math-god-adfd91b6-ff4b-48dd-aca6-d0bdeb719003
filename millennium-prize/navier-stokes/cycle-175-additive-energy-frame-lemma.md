# Cycle 175: an additive-energy/frame lemma for full off-circuit output

The desired lower bound is valid under an explicit restricted-isometry package.
Scale separation by itself does not supply that package.  In particular, an
additive-energy count controls frequency collisions but says nothing about
cancellation between Leray-polarized vectors at one collision frequency.

Fix a finite symmetric circuit support `S` and a set `D` of designated unordered
input pairs.  Let `X` be a set of unordered off-circuit pairs

\[
 e=\{p,q\},\qquad p,q\in S,\qquad p+q\notin S,
\]

disjoint from `D`.  Reality-related copies are counted only once.  For a
divergence-free Fourier field `u`, write

\[
 z_e=\omega_{p+q}^{1/2}\,
 P_{p+q}\big((u_p\cdot q)u_q+(u_q\cdot p)u_p\big),
 \qquad e=\{p,q\},
\]

where `omega_k>0` is the chosen critical output weight and `u` is supported in
`S`.  Define the synthesis
map

\[
 (T_Xz)_k=\sum_{e\in X:\,p_e+q_e=k}z_e
\]

and the complete weighted off-circuit Leray output

\[
 \mathcal O_S(u)=
 \sum_{k\notin S}\omega_k
 \left|P_k\sum_{p+q=k}
 (u_p\cdot q)u_q\right|^2.
\]

Here the inner sum is over ordered pairs, as in the Fourier convolution.  The
two ordered terms associated with a selected unordered pair `e={p,q}` are
exactly the symmetrized vector defining `z_e` (and the coincident case `p=q` is
excluded from `X`).  Thus `O_S(u)` contains every signed convolution pair, not
merely the selected set `X`.

## Exact lemma

**Lemma (conditional linear off-circuit tax).**  Suppose that for constants
`alpha>0`, `A>=1`, `rho<alpha/sqrt(A)`, and `C_0>=0`, independent of the depth
`L`, the following hold.

1. **Many charged witnesses:** there is `X_0 subset X` such that

   \[
   |X_0|\ge L-C_0,
   \qquad |z_e|\ge\alpha\quad(e\in X_0).
   \]

2. **Bounded additive multiplicity:** for every output `k`,

   \[
   m_X(k):=|\{e\in X:p_e+q_e=k\}|\le A.
   \]

3. **Polarized collision frame bound:** for every `k` in the selected output
   set and all coefficients `c_e`,

   \[
   \left|\sum_{e:p_e+q_e=k}c_e\widehat z_e\right|^2
   \ge {1\over A}\sum_{e:p_e+q_e=k}|c_e|^2,
   \qquad \widehat z_e={z_e\over|z_e|}.
   \]

4. **Full-convolution robustness:** set

   \[
   y_k=\omega_k^{1/2}P_k\sum_{p+q=k}(u_p\cdot q)u_q,
   \qquad r=y-T_Xz.
   \]

   Thus `r_k` is the coherently summed weighted contribution of every
   unselected signed convolution term, including collisions and recursively
   populated correction modes.  Assume

   \[
   \left(\sum_k|r_k|^2\right)^{1/2}
   \le\rho\sqrt{|X_0|}.
   \]

Then

\[
 \boxed{
 \mathcal O_S(u)\ge
 \left({\alpha\over\sqrt A}-\rho\right)^2(L-C_0).
 }
\]

In particular this is `cL-C`, with

\[
 c=\left({\alpha\over\sqrt A}-\rho\right)^2,
 \qquad C=cC_0.
\]

**Proof.**  The frame bound, grouped by equal output frequency, gives

\[
 \|T_Xz\|_{\ell^2_k}^2
 \ge {1\over A}\sum_{e\in X_0}|z_e|^2
 \ge {\alpha^2\over A}|X_0|.
\]

The complete off-circuit output is `T_Xz+r`.  The reverse triangle inequality
and robustness therefore give

\[
 \mathcal O_S(u)^{1/2}
 \ge\|T_Xz\|_2-\|r\|_2
 \ge\left({\alpha\over\sqrt A}-\rho\right)\sqrt{|X_0|}.
\]

Square and use `|X_0|>=L-C_0`.  This proves the claim.  Notice that no estimate
may discard `r`: doing so would prove a bound for a partial convolution rather
than the requested full Leray output.

## How additive energy can provide the witnesses

Let `P={p_0,...,p_{L-1}}` and `Q={q_0,...,q_L}` be pump and rail frequencies.
For `G subset P x Q`, let

\[
 r_G(k)=|\{(p,q)\in G:p+q=k\}|,
 \qquad E_+(G)=\sum_k r_G(k)^2.
\]

If `G subset P x Q` is a set of charged non-designated pairs and every sum has
multiplicity at most `A`, then greedily retaining one pair from each occupied
sum gives

\[
 |X_0|\ge {|G|\over A}.
\]

Without an `L^\infty` multiplicity bound, Cauchy--Schwarz gives only

\[
 |\{p+q:(p,q)\in G\}|\ge {|G|^2\over E_+(G)}.
\]

Consequently `E_+(G)<=K|G|` yields linearly many distinct outputs.  For a
scale-separated chain, a useful arithmetic hypothesis is therefore

\[
 E_+(G)\le K|G|,
\]

or the stronger bounded-representation condition `r_G(k)<=A`.  Lacunarity can
prove these only after signed sums and the periodic low-order corrections have
been classified; ordinary radial separation alone does not exclude identities
such as binary carries.

Distinct sums make the frame bound automatic with `A=1`, because different
Fourier modes are orthogonal.  If collisions remain, additive energy supplies
only their number.  One separately needs a lower singular-value bound for the
vectors `widehat z_e` in each plane `k^perp`.  Since that plane is
two-dimensional, the displayed frame inequality cannot hold for three or more
arbitrary independent coefficients at one `k`; one must select at most two
well-angled witnesses or prove a phase-locked scalar sign condition.

## Assumptions still needing proof

The lemma isolates four genuinely independent gates.

- **Throughput-to-witness conversion.**  Unit designated critical throughput
  must imply `|z_e|>=alpha` on a linear number of non-designated pairs.  This is
  not a consequence of the designated edge gains: reciprocal amplitude gauges
  preserve designated products while redistributing cross products.  A useful
  sufficient hypothesis is a uniformly conditioned amplitude frame, for
  example bounded ratios of normalized rail amplitudes and bounded ratios of
  normalized pump amplitudes on all but `O(1)` stages.
- **Arithmetic uniqueness.**  Signed scale-separated sums must have bounded
  additive multiplicity after all reality copies are included.  Cycle 148's
  six-periodic corrections and carry identities show why this requires an exact
  classification rather than a lacunarity slogan.
- **Leray angle/phase control.**  At every retained collision, the projected
  vectors must obey a uniform lower frame bound.  Scalar additive energy cannot
  prevent exact vector cancellation.
- **Completion robustness.**  Contributions from all other pairs must be
  `ell^2`-small relative to the selected synthesis, or orthogonal to it.  This
  is the hardest assumption: recursive completion from Cycles 129 and 146 can
  introduce small modes with order-one forcing and can cancel exterior output
  to arbitrary fixed depth.

The first gate has a small exact algebraic core.  If designated normalization
gives positive products

\[
 x_i y_i=1
\]

and for each unordered pair `i<j` the two normalized cross witnesses obey

\[
 |z_{ij}^{+}|\ge\sigma x_i y_j,
 \qquad |z_{ij}^{-}|\ge\sigma x_j y_i,
\]

then

\[
 \max(|z_{ij}^{+}|,|z_{ij}^{-}|)\ge\sigma
\]

because `(x_i y_j)(x_j y_i)=1`.  This defeats reciprocal gauges pairwise and
produces at least one charged orientation per stage pair.  To use only `L-O(1)`
of them, it remains to select orientations whose output sums have bounded
additive energy and whose Leray vectors satisfy the frame condition.

## Verdict

The exact `cL-C` statement is therefore available as the lemma above, but only
conditionally.  Additive-energy estimates can establish a linear supply of
frequency channels; frame estimates can convert pairwise charges into an
`ell^2` output lower bound.  Neither tool controls the residual full
convolution.  Assuming completion robustness without deriving it would hide the
principal all-depth Navier--Stokes difficulty, and unit critical throughput
alone is presently insufficient to imply the lemma's hypotheses.

This is a proof architecture and assumption audit, not a Navier--Stokes
regularity theorem or a blowup construction.
