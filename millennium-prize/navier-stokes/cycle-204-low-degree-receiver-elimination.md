# Cycle 204: low-degree terminal-receiver elimination

## Frozen subsystem

Let the four terminal frequencies be

\[
 r_{\epsilon,\delta}=(\epsilon T,\delta Y,0),
 \qquad \epsilon,\delta\in\{\pm1\},
\]

where `0<S<T` and `Y!=0`.  Write the eight scalar terminal-derivative
variables as the two divergence-free coordinates at these four frequencies:

\[
 v_{\epsilon,\delta}
   =(\delta Ya_{\epsilon,\delta},
     -\epsilon Ta_{\epsilon,\delta},
     b_{\epsilon,\delta}).                                      \tag{1}
\]

No Fourier-reality relation is used in the elimination.  It therefore works
over the complex numbers and, a fortiori, on the Fourier-real locus.

For each terminal, pair it with the extreme pump having the same horizontal
sign,

\[
 p_\epsilon=(\epsilon S,0,0),\qquad u_{p_\epsilon}=g_\epsilon e_2,
 \qquad g_\epsilon\ne0.
\]

The target frequency is

\[
 q_{\epsilon,\delta}
   =(\epsilon(T+S),\delta Y,0).
\]

Ignoring the harmless common Fourier scalar, the two ordered interactions
before Leray projection sum to

\[
 w_{\epsilon,\delta}
 =g_\epsilon\bigl(
   a_{\epsilon,\delta}Y^2,
   \epsilon\delta a_{\epsilon,\delta}Y(S-T),
   \delta b_{\epsilon,\delta}Y\bigr).                           \tag{2}
\]

This is the eight-variable linear part of the second-jet closure equations.

## Exact elimination

Instead of writing the rational Leray matrix, test (2) against a basis of
`q_(epsilon,delta)^perp`.  The vectors

\[
 e_3,
 \qquad t_{\epsilon,\delta}
   =(-\delta Y,\epsilon(T+S),0)
\]

give the two closure rows

\[
 g_\epsilon\delta Y b_{\epsilon,\delta}=0,                     \tag{3}
\]

\[
 -g_\epsilon\delta Y
   \bigl(Y^2+T^2-S^2\bigr)a_{\epsilon,\delta}=0.                \tag{4}
\]

Here

\[
 Y^2+T^2-S^2>0
\]

over the real frozen frequency data because `0<S<T`.  Thus (3)--(4) imply

\[
 a_{\epsilon,\delta}=b_{\epsilon,\delta}=0
 \quad\hbox{for all }\epsilon,\delta.                           \tag{5}
\]

Equivalently, after ordering each pair as `(a,b)`, the eight-by-eight
coefficient matrix is block diagonal and has determinant

\[
 \pm (g_+g_-)^4Y^8\bigl(Y^2+T^2-S^2\bigr)^4\ne0.               \tag{6}
\]

Consequently these rows contradict every nonzero terminal-derivative
normalization.  In ideal language, if `L(a,b)=1` is any normalized nonzero
linear terminal functional, (3)--(4) first put all eight variables in the
closure ideal and then give `1=L(a,b)` in that ideal.  For the Cycle 177 seed
`T=8`, `S=6`, and `Y=1`, the nontrivial scalar is

\[
 Y^2+T^2-S^2=29.
\]

The seeded derivative is in the `e_3` coordinate, so already one row of (3)
contradicts its normalization.

## Scope check for the full Cycle 203 gate

This is an immediate obstruction only when the displayed target coefficients
contain the terminal--extreme-pump interactions alone, as in the terminal
receiver subsystem.  It must not be silently promoted to a certificate for the
full helper-mode ideal of Cycle 203.  That gate allows arbitrary initial modes
throughout `S\K_0`.  In its concrete support there is, for example, an axial
helper at `(12,0,0)`, and

\[
 (12,0,0)+(2,1,0)=(14,1,0)=(8,1,0)+(6,0,0).
\]

Hence the full equation at `(14,1,0)` has additional helper--seed terms.  The
eight-variable block (3)--(4) is a valid low-degree elimination pivot, but not
by itself an element of the unrestricted full ideal.  A complete obstruction
now needs one of the following exact continuations:

1. derive earlier exterior equations forcing the contaminating axial/helper
   coefficients to zero;
2. eliminate those coefficients and recover a nonzero multiple of the block
   determinant (6); or
3. retain the helper terms and exhibit a different low-degree combination
   yielding the terminal normalization contradiction.

Thus the receiver-only closure is linearly impossible before any Groebner
calculation, while infeasibility of the entire Cycle 203 completion system
remains open.  No Navier--Stokes regularity result is claimed.

Run the exact arithmetic check with

```sh
python3 millennium-prize/navier-stokes/verify_cycle204_receiver_elimination.py
```
