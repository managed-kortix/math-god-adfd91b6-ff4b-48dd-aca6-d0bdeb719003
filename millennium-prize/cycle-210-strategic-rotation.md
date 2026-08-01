# Cycle 210: portfolio selection after the BSD primary gates

## Decision

Select Navier--Stokes as the next main funnel, but only for the universal
critical-norm amplification gate below. Do not continue the `D=-1499` campaign
by testing additional isolated primes. Cycles 209--210 exclude the 7- and
11-primary parts of `Sha` for one rank-one twist, but another successful prime
would still leave infinitely many primary parts and would supply neither a
uniform family theorem nor the refined BSD leading-term formula.

The selected statement is

\[
 \sup_{0\leq t<T_*}\|u(t)\|_{L^3(\mathbb T^3)}
 \leq 2\|u(0)\|_{L^3(\mathbb T^3)}.                    \tag{210.1}
\]

Here `u` is every mean-zero smooth periodic Navier--Stokes solution, with fixed
positive viscosity, on its maximal smooth interval `[0,T_*)`. If (210.1) is
proved, the endpoint `L^infinity_t L^3_x` continuation theorem gives the
periodic existence alternative in the Clay statement. The factor two is not
canonical; it is frozen so that the statement has a strict finite falsifier.
The statement is stronger than regularity and is not reconstructed from
regularity, which permits data-dependent critical-norm amplification.

## Six-lane comparison

Use the Cycle 206 tuple

\[
 L=(\hbox{barrier crossing},\hbox{non-equivalence},
       \hbox{finite falsifiability},\hbox{official transfer}).
\]

| lane | score | present reason |
|---|---|---|
| Navier--Stokes | `(1,1,1,1)` | (210.1) is a separated sufficient lemma, one certified trajectory can refute it, and a proof transfers by endpoint continuation |
| Hodge | `(1,1,1,0)` | a symbolic weighted-Pfaffian audit could close the last named linkage escape, but would still be another negative architecture result with no replacement production family |
| BSD | `(0,1,1,0)` | each further Kurihara prime is exact but excludes only one primary part for one curve; the missing leverage is uniform primary control or the refined determinant-line bridge |
| P versus NP | `(0,1,1,0)` | finite asymmetric-MCSP instances are exact, but anti-sharing at MMW entropy scale already asks for a new unrestricted-circuit mechanism and lacks the relational update-time transfer |
| RH | `(1,0,0,1)` | shifted canonical endpoint exhaustion and the current Nyman--Beurling decay target are RH-strength rather than separated finite production lemmas |
| Yang--Mills | `(0,1,1,0)` | fixed physical blocks are exact, but do not control moving vacuum-complement states or construct the OS continuum limit |

Navier wins lexicographically. This does not assert that (210.1) is plausible;
its value is that the same precise statement has full leverage if proved and a
global, finitely checkable rejection criterion if false.

## Exact first gate

Embed two-dimensional solutions in `T^3`, independent of `x_3`, and write the
initial velocity as `u_0=nabla^perp psi`. Freeze

\[
 K=\{(1,0),(0,1),(1,1),(2,1),(1,2)\}
\]

and

\[
 \psi(x,y)=\sum_{k\in K}(a_k\cos(k\cdot x)+b_k\sin(k\cdot x)),
 \qquad a_k,b_k\in\{-2,-1,0,1,2\}.
\]

Discard the zero field, scalar duplicates, and fields whose nonlinear
vorticity interaction vanishes identically. Work in the amplitude-rescaled
equation with effective viscosities

\[
 \mu\in\{1,1/2,1/4,1/8,1/16,1/32,1/64\}
\]

and checkpoint times `T=j/16`, `1<=j<=64`. This is a finite declared campaign;
symmetry reduction may shorten it but may not add unrecorded samples.

There are exactly two passing outcomes.

1. **Falsifier.** Give one named `(a,b,mu,T)` and a directed interval
   certificate for the full two-dimensional Navier--Stokes PDE on `[0,T]`
   proving

   \[
     \|u(T)\|_3>2\|u(0)\|_3.                         \tag{210.2}
   \]

   The certificate must bound unresolved Fourier modes, time-discretization
   error, and both spatial integrals. A Galerkin trajectory, floating-point
   ratio, or projected `|u|u` calculation is not accepted. Since a 2D solution
   is also a 3D periodic solution, (210.2) refutes (210.1) globally.
2. **Finite-family exclusion.** For every retained grid member and every listed
   `mu`, give interval PDE enclosures on `[0,4]` and certify
   `||u(t)||_3<=2||u(0)||_3` on each time slab, including between checkpoint
   times. This retires only the frozen family and parameter box. It is not
   evidence for (210.1) outside the box.

Candidate screening may use floating point, but only one of these fail-closed
outputs closes the gate. The preferred validator uses the 2D vorticity equation
and a posteriori Fourier-tail estimates; conversion back to velocity and the
`L^3` cubature must use directed rational or ball bounds.

## Rotation rule

If a falsifier is certified, retire the universal factor-two lemma and return
to portfolio discovery; do not optimize a larger constant unless an independent
argument supplies a uniform constant with official transfer. If the finite
family is excluded, enlarge the ansatz only after identifying a structural
reason that the new modes can create greater critical-norm transfer. Do not
resume isolated BSD primary checks unless a uniformity theorem makes one finite
calculation control infinitely many primes or curves.

No Navier--Stokes regularity result, BSD formula, or Millennium solution is
claimed.
