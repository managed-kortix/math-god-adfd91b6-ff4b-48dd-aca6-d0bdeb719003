# Cycle 224: exact 2D triad-chain scout and finite-support obstruction

## Scope and convention

On the normalized-Haar `2 pi` torus write the real vorticity as

\[
 \omega(x)=\sum_{k\ne0}\omega_k e^{ik\cdot x},\qquad
 \omega_{-k}=\overline{\omega_k},
\]

and use `k^perp=(k_2,-k_1)` and `u_k=i k^perp omega_k/|k|^2`. The ordered
Euler coefficient is `-det(p,q)/|p|^2`. Pairing the two orders gives the
symmetrized Euler
coefficient is the rational number

\[
 C(p,q)={p\wedge q\over2}
 \left({1\over |q|^2}-{1\over |p|^2}\right),\qquad
 \dot\omega_k=\sum_{p+q=k}C(p,q)\omega_p\omega_q.       \tag{224.1}
\]

The scout enumerates connected unions of three active integer triads in the
box `[-2,2]^2`, retaining the first 60 canonical supports. For each support it
constructs (224.1) over `Q`, checks the energy and enstrophy identities
coefficient by coefficient, and only then uses RK4 and spatial quadrature to
rank integer coefficient vectors in `[-2,2]`. Floating output is a locator, not
a certificate for Euler or for an `L^3` inequality.

## Best bounded observation

The strongest tested five-orbit support was

\[
 S_+=\{(0,1),(1,0),(1,1),(2,1),(2,2)\},
\]

with representative vorticities

\[
 (0,-2,-2-i,-2-2i,-1+2i).
\]

The exact ten-mode ODE is stored term by term in the JSON artifact. Its
quadratic energy
`E=(1/2) sum_k |omega_k|^2/|k|^2` and enstrophy
`Z=(1/2) sum_k |omega_k|^2` have identically zero derivatives. A finer replay
with time step `0.0015` and a `32 x 32` spatial grid observes an `L^3`
oscillation ratio above `1.07`, not above two. The original bounded screen saw
`1.0798703462`; it found no factor-two candidate.

## Exact full-Euler leakage test

Deleting the Galerkin projection at time zero gives eight nonzero exterior
launch modes (four conjugate pairs). In particular,

\[
 \dot\omega_{(1,2)}={7\over2}-7i,\quad
 \dot\omega_{(3,1)}=-{16\over5}-{16\over5}i,
\]
\[
 \dot\omega_{(3,2)}=-{29\over10}+{44\over5}i,\quad
 \dot\omega_{(4,3)}=-{9\over10}+{3\over10}i.          \tag{224.2}
\]

Thus the located oscillation is not an exact full-Euler trajectory even to
first order. The leakage conclusion is algebraic over `Q`, independent of the
floating integration.

## Architecture obstruction

There is also an exact obstruction to repairing this by asking for a finite
universally invariant Fourier support. Let `S=-S` be finite and require the
Euler quadratic map to preserve fields supported in `S` for every assignment
of their coefficients. Whenever `p,q in S` are noncollinear and
`|p| != |q|`, (224.1) is nonzero and therefore `p+q in S`. By symmetry replace
`q` by `-q` so that `p dot q >= 0`. Then `p+nq` and `q` remain noncollinear and
have unequal lengths for every `n>=1`, so closure inductively puts every
`p+nq` in `S`, a contradiction. Hence every pair in `S` is either collinear or
has equal length.
If two noncollinear modes occur, comparison with each of them forces every mode
onto their common circle; otherwise all modes are collinear. In both cases
every coefficient (224.1) vanishes. Therefore every finite universal
Euler-invariant Fourier architecture has identically stationary vorticity and
constant velocity `L^3`.

This obstruction does not exclude a finite initial packet followed by a
rigorously enclosed infinite tail, nor a support invariant only on a special
algebraic coefficient subvariety. It does show that exact finite closure cannot
upgrade the Galerkin observation into a nontrivial Euler orbit. The requested
bounded campaign therefore returns the architecture obstruction, not a
candidate above two and not a Navier--Stokes or Millennium result.

## Reproduction

```sh
python millennium-prize/navier-stokes/scout_2d_triad_chains.py \
  --bound 2 --length 3 --support-limit 60 --starts 8 \
  --steps 1000 --dt 0.003 \
  --output millennium-prize/navier-stokes/cycle224-triad-chain-screen.json
python millennium-prize/navier-stokes/verify_cycle224_triad_chain.py
```
