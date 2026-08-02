# Cycle 251: Hamiltonian equal-energy rearrangement with an `L^3` gap

## Status: EXACT KINEMATIC EXISTENCE

There is no mapping-class obstruction to the static Cycle 250 endpoint test.
There exist a smooth mean-zero vorticity `omega` on `T^2` and a smooth
Hamiltonian diffeomorphism `eta` such that, with

\[
 \widetilde\omega=\omega\circ\eta^{-1},
\]

one has exactly

\[
 \|\widetilde\omega\|_{\dot H^{-1}}
 =\|\omega\|_{\dot H^{-1}},
 \qquad
 \frac{\|K\omega\|_3}{\|K\widetilde\omega\|_3}>2.       \tag{251.1}
\]

In particular, `eta` is area preserving and isotopic to the identity. The
proof does not factor the Cycle 250 matrix into toral shears. Instead it uses
weak, or in-measure, approximation of its action by localized Hamiltonian
rearrangements and then retunes the one continuous amplitude. Uniform
approximation is impossible for the mapping-class reason, but uniform
approximation is not needed by either norm in (251.1).

This remains kinematic only. The Hamiltonian isotopy generating `eta` is an
externally prescribed incompressible isotopy and is not shown to satisfy the
self-induced Euler equation.

## Hamiltonian weak-density lemma

We use the following surface rearrangement lemma.

**Lemma 251.1 (finite-observable Hamiltonian approximation).** Let `(M,mu)` be
a closed connected symplectic surface, let `Phi` be a smooth
measure-preserving diffeomorphism, and let `f_1,...,f_r` be continuous
functions. For every `1<=q<infinity` and every `delta>0`, there is
`h in Ham(M)` such that

\[
 \|f_j\circ h-f_j\circ\Phi\|_{L^q}<\delta
 \quad(1\le j\le r).                                  \tag{251.2}
\]

The same `h` works for every linear combination of the `f_j`, with the
corresponding triangle-inequality bound.

Here is the finite construction behind the lemma. Partition the common range
of the vector observable `f=(f_1,...,f_r)` into cubes `C_alpha` of diameter
`rho`, choosing their boundaries to have null pullback. The source and target
atoms

\[
 A_\alpha=(f\circ\Phi)^{-1}(C_\alpha),\qquad
 D_\alpha=f^{-1}(C_\alpha)
\]

have equal area because `Phi` preserves measure. By inner regularity and the
surface disc basis, subdivide each pair into finitely many correspondingly
labelled, pairwise disjoint, equal-area smooth discs, leaving total area less
than `rho`. The equal individual areas can be arranged by cutting sufficiently
small source and target discs to one common list of areas.

Finite families of labelled disjoint discs with matching areas on a connected
symplectic surface can be carried to one another by a Hamiltonian
diffeomorphism. This follows inductively from the relative area-preserving disc
extension theorem: join the next pair by a thin path in the complement of the
already fixed discs, move it through a tubular neighborhood by a compactly
supported Hamiltonian, and apply Moser correction inside the target disc.
Fragmentation handles the finitely many path crossings before the induction.
On every paired source disc, `f(h(x))` and `f(Phi(x))` lie in the same range
cube. On the discarded set the error is at most
`2 max_j ||f_j||_infinity`. Thus

\[
 \|f_j\circ h-f_j\circ\Phi\|_q^q
 \le rho^q+2^q\|f_j\|_\infty^q rho,
\]

and smoothing the disc and tube boundaries changes only another arbitrarily
small set. Sending `rho` to zero proves (251.2). All local motions have zero
flux, so their finite composition is Hamiltonian. This proof also shows why the
lemma is convergence in measure rather than `C^0` convergence.

For completeness, if a sequence of identity-isotopic maps converged uniformly
to a toral automorphism within less than the injectivity radius, the short
geodesics between corresponding images would give a homotopy. Hence the limit
would act trivially on `H_1(T^2;Z)`. The nontrivial Cycle 250 matrix cannot be
obtained that way. Lemma 251.1 concentrates the required topological cuts in a
set of vanishing area and therefore does not contradict this obstruction.

## Robust Cycle 250 seed

Use all notation and normalizations of Cycle 250. Thus

\[
 B=B_N=\begin{pmatrix}1&N\\N&N^2+1\end{pmatrix},
 \quad L=(1+N^2)^{1/2},
\]

and

\[
 \omega^t(x,y)=F_\varepsilon'(x)+tG'(-Nx+y).           \tag{251.3}
\]

Choose `epsilon` and then `N` with strict slack, so that at
`t_*=a/b` the Cycle 250 estimate gives

\[
 \frac{\|K\omega^{t_*}\|_3}
 {\|K(\omega^{t_*}\circ B)\|_3}>2+3\gamma             \tag{251.4}
\]

for some `gamma>0`. This is possible because the lower bound tends first to
`R_epsilon>2` as `N` tends to infinity, and `epsilon` may be made smaller so
that `R_epsilon` is arbitrarily large.

Continuity in `t` supplies `sigma in (0,1)` such that (251.4), with
`2+2 gamma` on the right, holds throughout

\[
 I=[t_-,t_+],\qquad t_\pm=(1\pm\sigma)t_*.             \tag{251.5}
\]

Define the signed energy defect for the exact matrix action by

\[
 Q_B(t)=\|K(\omega^t\circ B)\|_2^2-\|K\omega^t\|_2^2.
\]

Cycle 250 computes it exactly:

\[
 Q_B(t)=(L^{-2}-1)(a^2-t^2b^2).                       \tag{251.6}
\]

Consequently `Q_B(t_-)<0<Q_B(t_+)`, with two nonzero margins.

## Replacement by one Hamiltonian map

Apply Lemma 251.1 to `Phi=B` and the two smooth observables

\[
 f_1=F_\varepsilon'(x),\qquad f_2=G'(-Nx+y).
\]

Choose `h in Ham(T^2)` so close in (251.2), with `q=2`, that uniformly for
`t in I`,

\[
 \|\omega^t\circ h-\omega^t\circ B\|_2<\delta.        \tag{251.7}
\]

The operator `K=grad^perp Delta^{-1}` maps mean-zero `L^2` continuously to
`H^1`, and on `T^2`, `H^1` embeds continuously into every finite `L^p`.
Composition by either area-preserving map preserves the mean. It follows from
(251.7), uniformly on `I`, that

\[
 \begin{aligned}
 K(\omega^t\circ h)&\longrightarrow K(\omega^t\circ B)
 &&\text{in }L^2,\\
 K(\omega^t\circ h)&\longrightarrow K(\omega^t\circ B)
 &&\text{in }L^3                                      \tag{251.8}
 \end{aligned}
\]

as `delta` tends to zero through the lemma. Notice that no derivative of `h`
enters these estimates.

Take `delta` small enough that the signed endpoint margins in (251.6) persist:

\[
 Q_h(t_-):=\|K(\omega^{t_-}\circ h)\|_2^2
            -\|K\omega^{t_-}\|_2^2<0,
\]

\[
 Q_h(t_+):=\|K(\omega^{t_+}\circ h)\|_2^2
            -\|K\omega^{t_+}\|_2^2>0.                \tag{251.9}
\]

The same choice, made smaller if necessary, preserves from (251.4)-(251.5)
the uniform strict estimate

\[
 \frac{\|K\omega^t\|_3}{\|K(\omega^t\circ h)\|_3}
 >2+\gamma \qquad(t\in I).                            \tag{251.10}
\]

The denominator is uniformly separated from zero because its matrix-model
counterpart is nonzero on the compact interval and (251.8) is uniform.

Since `Q_h(t)` is continuous, (251.9) and the intermediate value theorem give
some `t_h in (t_-,t_+)` for which

\[
 Q_h(t_h)=0.                                           \tag{251.11}
\]

Finally set

\[
 \omega=\omega^{t_h},\qquad \eta=h^{-1}.
\]

The inverse of a Hamiltonian diffeomorphism is Hamiltonian, and
`omega circ eta^{-1}=omega circ h`. Equation (251.11) is the exact
homogeneous `H^-1` equality, while (251.10) gives the strict factor-two
velocity ratio. This proves (251.1).

## Scope

The result repairs exactly the mapping-class defect in Cycle 250 and shows
that no static obstruction follows from requiring identity isotopy, or even
Hamiltonian isotopy. It is nonconstructive only in the existence choices in
Lemma 251.1 and the intermediate-value parameter `t_h`; both produce finite
smooth objects, not limiting endpoint maps.

It does not repair the decisive dynamical defect. If `eta_s` is the Hamiltonian
isotopy produced above, its generator is not shown to equal
`K[omega circ eta_s^{-1}]`. Therefore this is still not an Euler orbit, an
inviscid-limit seed, or a Navier--Stokes result.
