# Cycle 127: spatial smearing preserves reflection positivity but is not a full UV regulator

Spatial-only, time-slice-local gauge smearing avoids the Cycle 126 obstruction:
it exactly preserves the positive-time observable algebra.  It nevertheless
leaves temporal-frequency contact divergences and therefore cannot by itself
regularize a complete four-dimensional local field algebra.

## Exact reflection-positivity lemma

Let `mu` be a reflection-positive lattice gauge measure, `theta` its time
reflection, and `A_+` its positive-half observable algebra.  Let `S` be a
deterministic smearing map such that

1. temporal links are unchanged;
2. every smeared spatial link uses only links on the same time slice;
3. `S` is gauge equivariant and orientation compatible;
4. `S theta = theta S`; and
5. pullback by `S` maps `A_+` into `A_+`.

Then for every `F in A_+`,

\[
\langle\theta(S^*F)\,S^*F\rangle_\mu\ge0.
\]

This is immediate because `S^*F` remains in the original positive algebra.
Equivalently, the pushed-forward measure is reflection positive on the image
algebra.  This does not assert positivity for a different measure obtained by
inserting smeared links into an action.

Mixed electric plaquettes must lie wholly inside the chosen positive slab.
Temporal-link smearing by spatial staples is excluded from the simple lemma
because it is not literally single-slice local.

## Exact free electric obstruction

For a transverse Maxwell polarization spatially heat-smeared at times `t_1`
and `t_2`, put `sigma=t_1+t_2`.  The momentum covariance contains

\[
e^{-\sigma|p|^2}P^T_{ij}(p)
\frac{p_0^2}{p_0^2+|p|^2}.
\]

Since

\[
\frac{p_0^2}{p_0^2+|p|^2}
=1-\frac{|p|^2}{p_0^2+|p|^2},
\]

the traced two-point distribution is

\[
C_T(\tau;\sigma)
=\frac{2}{(4\pi\sigma)^{3/2}}\delta(\tau)
-\int\frac{d^3p}{(2\pi)^3}|p|e^{-\sigma|p|^2-|p||\tau|}.
\]

At zero noncontact separation the smooth term is

\[
-\int\frac{d^3p}{(2\pi)^3}|p|e^{-\sigma|p|^2}
=-\frac1{4\pi^2\sigma^2}.
\]

With temporal lattice spacing `a_tau`,

\[
\delta(\tau)\longleftrightarrow\frac{\delta_{n0}}{a_\tau},
\]

so the zero-slice contact peak is exactly

\[
\frac{2}{(4\pi\sigma)^{3/2}a_\tau}.
\]

For equal heat times `sigma=2t`, this becomes

\[
\frac1{8\sqrt2\,\pi^{3/2}t^{3/2}a_\tau}.
\]

Thus fixed spatial smearing leaves a positive `a_tau^{-1}` divergence in a
physical electric channel.  It remains a legitimate distribution in time and
does not violate reflection positivity, but pointwise coincident electric
fields are not regulated.

The correct conclusion is narrow: slice-local spatial smearing is an exact
RP-preserving preprocessing and spatial compactness device, but not a
standalone UV regulator for a complete local Yang--Mills algebra.  An
independent temporal regulator, distributional composite renormalization, and
restoration of Euclidean covariance are still required.

Reproduce the constants with

```sh
python3 millennium-prize/yang-mills/verify_cycle127_spatial_smearing.py
```

No Yang--Mills or Millennium solution is claimed.
