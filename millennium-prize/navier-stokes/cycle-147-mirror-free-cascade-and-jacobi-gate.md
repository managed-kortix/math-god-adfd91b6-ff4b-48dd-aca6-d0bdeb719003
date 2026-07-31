# Cycle 147: an infinite mirror-free designated cascade

Cycle 146 left open the possibility that Fourier reality forces a comparable
mirror sideband at every efficient transfer.  That is false in three
dimensions.  Reality fixes the conjugated mirror polarization, but equal-radius
inputs admit exact one-sided Leray cancellation.

For nonparallel frequencies `k,l` and divergence-free polarizations `a,b`, put

\[
F_+=P_{k+l}\big((a\cdot l)b+(b\cdot k)a\big),
\]

\[
F_-=P_{k-l}\big(-(a\cdot l)\bar b+(\bar b\cdot k)a\big).
\]

An exact projection argument gives the dichotomy

\[
|k|\ne|l|,\quad F_-=0\quad\Longrightarrow\quad F_+=0.
\]

For equal radii, however, there are abundant polarizations with

\[
F_-=0,\qquad F_+\ne0.
\]

For example,

\[
k=(1,0,0),\quad l=(0,1,0),
\quad a=(0,1,1),\quad b=(1,0,1)
\]

gives `F_-=0` and `F_+=(0,0,2)`.

This local phenomenon extends to an exact infinite integer-frequency designated
cascade.  Let

\[
R(x,y,z)=(z,x,y),\qquad q_0=(1,2,3),
\]

and recursively set

\[
p_n=Rq_n,
\qquad q_{n+1}=q_n+p_n=(I+R)q_n.
\]

Then

\[
|q_n|=|p_n|,
\]

so every stage lies on the mirror-killing locus.  The first shells are

\[
\begin{array}{c|c|c|c}
n&q_n&p_n&|q_n|^2\\ \hline
0&(1,2,3)&(3,1,2)&14\\
1&(4,3,5)&(5,4,3)&50\\
2&(9,7,8)&(8,9,7)&194\\
3&(17,16,15)&(15,17,16)&770\\
4&(32,33,31)&(31,32,33)&3074
\end{array}
\]

The mirror differences satisfy

\[
d_n=q_n-p_n,
\qquad |d_n|^2=6,
\]

while the intended radii grow without bound.

Let

\[
N_n=q_n\times p_n.
\]

At the first stage take

\[
a_0=(32,-1,-10),
\qquad b_0=(-6,8,5).
\]

At every later stage use

\[
a_n=N_{n-1},
\qquad b_n=RN_{n-1}.
\]

These are divergence-free at `q_n,p_n`.  Exact Leray projection gives

\[
P_{q_n-p_n}F_-=0,
\]

while

\[
P_{q_n+p_n}F_+
\]

and its polarization is parallel to `N_n`, making it admissible as the next
stage's active input.  Thus every designated mirror vanishes and every intended
edge is nonzero for arbitrary depth.

This refutes mirror branching as a universal all-depth cascade tax.  It does
not construct a closed Euler subsystem: if all pumps and rails are populated
simultaneously, nonadjacent cross-interactions generate additional frequencies.
The remaining obstruction, if any, must quantify these global cross-edge
outputs, not individual mirrors.

Cycle 147 also tested a Jacobi/Gram route.  The divergence-free vector-field
bracket satisfies exact diamond identities, but the Euler quadratic map is its
metric-dependent symmetric coadjoint operator.  A quadratic map does not
determine a unique antisymmetric bracket lift, so Jacobi alone imposes no new
constraint on observable cascade-transfer coefficients.  Gram rank identities
are relevant only after proving that all measured couplings factor through one
shared rank-three channel; sums of channels evade the naive determinant.
Neither identity currently yields a quantitative circuit cost.

The surviving gate is global: for the simultaneous mirror-free chain, compute
the complete cross-edge convolution and decide whether scale-uniform intended
gain forces a budgetable accumulated off-circuit or viscous cost.  Any useful
bound must include all generated modes and resist recursive completion.

Reproduce the designated cascade with

```sh
python3 millennium-prize/navier-stokes/verify_cycle147_mirror_free_cascade.py
```

This is an exact instantaneous triad-chain construction, not an invariant
Navier--Stokes solution, a blowup construction, or a regularity theorem.
