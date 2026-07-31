# Cycle 163: PEL-stable kernels versus the antilinear graph

This note imposes the PEL condition omitted from the unrestricted symplectic
count in Cycle 161.  The answer changes sharply: at inert primes the completely
adapted stratum is empty, while at split primes it is nonempty but much smaller
than the unrestricted adapted stratum.

## Setup

Use the Cycle 151 fiber

\[
A_0=E_i^3\times E_i^3,
\qquad Q_1=\operatorname{diag}(1,1,1),
\qquad Q_2=\operatorname{diag}(1,1,3),
\]

with `O=Z[i]` acting in the standard way on the first block and in the
conjugate way on the second.  Let

\[
\Gamma=\{(x,x):x\in E_i^3\},\qquad J(x,x)=(ix,-ix).
\]

Fix a prime `p>=5`.  Then the polarization is prime to `p`, `Gamma[p]` is a
nondegenerate symplectic six-space, and
`Gamma[p] cap J Gamma[p]=0`.  Let `K` be an `O/pO`-stable maximal isotropic
subspace of `A_0[p]`.  Put

\[
D=K\cap\Gamma[p],\qquad d=\dim_{F_p}D,
\qquad \eta_p(K)=p^{3-d}.
\]

Write `e` for the Weil pairing and define on `Gamma[p]`

\[
\omega(x,y)=e(x,y),\qquad s(x,y)=e(x,Jy).
\]

Under `Gamma[p]=W perp U`, where `W=E_i[p]^2` consists of the first two
coordinates and `U=E_i[p]` is the third coordinate, multiplication by nonzero
scalars does not affect the following normal forms:

\[
\omega=2\omega_W\perp4\omega_U,
\qquad s=0_W\perp(-2)q_U,
\]

where `q_U` is the symmetric plane represented by `X^2+Y^2`.  Thus `W` is the
four-dimensional radical of `s`; the plane `q_U` is hyperbolic when
`p=1 mod 4` and anisotropic when `p=3 mod 4`.

## Exact finite-module theorem

**Theorem.** With the setup above:

1. `D` is simultaneously totally isotropic for `omega` and `s`, and `d<=3`.
   Conversely, if an `F_p`-subspace `D` has both properties, then
   `OD=D+JD` is an `O/pO`-stable isotropic subspace.  The PEL kernels having
   intersection exactly `D` are exactly the maximal `O/pO`-stable isotropic
   extensions of `OD` whose residual part in `(OD)^perp/OD` is transverse to
   the image of `Gamma[p]`.  This is a bijective classification, including
   every intersection stratum.

2. If `p=3 mod 4` is inert, then `d<=2`.  Hence

   \[
   \boxed{\eta_p(K)\ge p}.
   \]

   Equality holds precisely when `D` is a Lagrangian plane in `W`.  For every
   such `D`, the quotient `(OD)^perp/OD` is a hyperbolic Hermitian plane over
   `F_(p^2)` and has exactly `p+1` isotropic `F_(p^2)`-lines.  Consequently

   \[
   \boxed{N^{PEL}_{\eta=p}(p)=(p+1)^2(p^2+1)},
   \qquad
   \boxed{N^{PEL}_{\eta=1}(p)=0}.
   \]

3. If `p=1 mod 4` is split, then `eta=1` occurs.  Let `ell_+` and `ell_-` be
   the two isotropic lines of the hyperbolic symmetric plane `(U,q_U)`.  The
   completely adapted kernels are exactly

   \[
   \boxed{K_{L,\epsilon}=O(L\oplus\ell_\epsilon)
   =(L\oplus\ell_\epsilon)\oplus
     J(L\oplus\ell_\epsilon)},
   \]

   where `L` ranges over the Lagrangian planes of the symplectic four-space
   `W` and `epsilon` ranges over `{+,-}`.  In particular,

   \[
   \boxed{N^{PEL}_{\eta=1}(p)=2(p+1)(p^2+1)}.
   \]

All counts are counts of actual subgroup kernels, not orbit counts.  The total
number of PEL maximal isotropic kernels is

\[
N^{PEL}_{all}(p)=
\begin{cases}
(p+1)(p^3+1)(p^5+1),&p\equiv3\pmod4,\\
\displaystyle\sum_{r=0}^6{6\brack r}_p,&p\equiv1\pmod4.
\end{cases}
\]

Thus the exact inert density of the smallest possible eta stratum and the exact
split density of the adapted stratum are obtained by dividing the displayed
counts by the corresponding total.

## Proof

If `x,y` lie in `D`, then `x,Jy` lie in the isotropic space `K`, because `K`
is PEL-stable.  Therefore both `omega(x,y)` and `s(x,y)` vanish.  Also
`D cap JD=0`, so `D+JD` has dimension `2d` inside the six-dimensional `K`;
hence `d<=3`.  The same calculation proves that `OD` is isotropic whenever
`D` is isotropic for both forms.  Passing to its symplectic orthogonal quotient
gives the extension classification in part 1; transversality is exactly the
condition that the intersection with `Gamma[p]` does not increase.

Suppose `p` is inert.  The projection of any `s`-isotropic subspace to `U` is
totally isotropic for the anisotropic plane `q_U`, so it is zero.  Thus
`D subset W`.  Since `W` is symplectic of dimension four, `d<=2`; equality
means exactly that `D` is Lagrangian in `W`.  There are
`(p+1)(p^2+1)` such planes.  For each one, maximal PEL extensions are the
isotropic lines of the residual hyperbolic Hermitian plane.  Their number is
`p+1`.  A larger intersection would contradict the already proved bound, so
all these extensions have intersection exactly `D`.  This proves part 2.

Now suppose `p` is split and `d=3`.  Since `D cap W` is isotropic in the
symplectic four-space `W`, it has dimension at most two.  The image of `D` in
`U` is isotropic for `q_U`, so it has dimension at most one.  Dimension three
forces both bounds to be equalities.  Put `L=D cap W`; then `L` is Lagrangian
in `W`, and the image is one of `ell_+`, `ell_-`.  If a lift of its generator
is `u+w`, `omega`-orthogonality to `L` gives `w in L`, so changing the lift
shows

\[
D=L\oplus\ell_\epsilon.
\]

Conversely every such direct sum is isotropic for both forms.  Since it has
dimension three, `OD=D+JD` already has dimension six and is the unique maximal
PEL isotropic extension.  A symplectic four-space has
`(p+1)(p^2+1)` Lagrangians, and the split plane has two isotropic lines, giving
the asserted count.

At an inert prime, PEL kernels are Hermitian Lagrangians in a split
six-dimensional Hermitian space, giving the first total count.  At a split
prime, `O/pO=F_p times F_p`; a stable Lagrangian is determined by an arbitrary
`r`-space in one eigenspace and its annihilator in the other, giving the sum of
Gaussian coefficients.

## Consequences and scope

- The unrestricted Cycle 161 count
  `(p+1)^2(p^2+1)^2(p^3+1)^2` for `eta=1` cannot be used after imposing PEL
  stability.  At split primes only `2(p+1)(p^2+1)` kernels survive; at inert
  primes none survive.
- Inert PEL transport forces the normalized graph class to have integral
  denominator at least `p`, by Cycle 162's exact denominator theorem.  Thus no
  bounded-eta family can use unbounded inert prime support.
- Split primes still admit `eta=1` kernels at every good split prime, so PEL
  stability alone does not force eta to grow and does not close the dense
  Hecke-transport route.
- This is a prime-torsion theorem.  It does not classify `p^e`-kernels, where
  elementary divisors and integral Hermitian lattices are required.  It also
  supplies no equidistribution, Hecke-density, dominating Chow component, or
  Hodge-conjecture result.

Check the exact count identities with

```sh
python3 millennium-prize/hodge/verify_cycle163_pel_antilinear_kernels.py
```
