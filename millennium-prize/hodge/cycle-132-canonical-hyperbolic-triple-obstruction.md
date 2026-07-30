# Cycle 132: the canonical hyperbolic triple is obstructed modulo four

There is a unique orthogonal-group orbit of ordered isotropic pairs

\[
z^tz=w^tw=0,\qquad z^tw=1
\]

in `F_32^3`.  Hence the associated three-plane configuration containing the
explicit alpha-visible Hermitian plane is canonical up to symmetry, rather than
the output of a triple census.  Its genuine scheme-theoretic union nevertheless
fails the first mixed-characteristic lifting gate.

Take

\[
z=(1,0,1)^t,\qquad w=(0,1,1)^t,
\]

and

\[
T=L_A\cup L_{A(I+zz^t)}\cup L_{A(I+ww^t)}.
\]

The first plane meets each neighbor in a line; the two neighbors meet at the
common triple point.  In the spanning `P^4`, write

\[
y=Ax+(Az)s+(Aw)r,
\]

and put

\[
U=x_0+x_2,\qquad V=x_1+x_2.
\]

The reduced union has Hilbert--Burch ideal

\[
I_T=(s(s+U),\ sr,\ r(r+V)).
\]

Its quotient dimensions are

\[
h^0(O_T(1),O_T(2),O_T(3),O_T(33))=(5,12,22,1717).
\]

The quadratic-generator syzygy map is a `44 x 36` matrix of rank `18`, so the
normal space inside `P^4` has dimension `18`.  The spanning-hyperplane direction
adds five columns, giving the complete embedded normal map

\[
M_T:k^{23}\longrightarrow H^0(O_T(33))\simeq k^{1717}.
\]

Using genuine Teichmüller-coordinate `W_2(F_32)` arithmetic, restriction of the
standard degree-33 Fermat lift gives a divided remainder `h_T` with 215 nonzero
coefficients.  Exact sparse elimination yields

\[
\boxed{\operatorname{rank}M_T=23},\qquad
\boxed{\operatorname{rank}[M_T\mid h_T]=24}.
\]

The new augmented pivot is

\[
x_1^{16}x_2^{17}.
\]

Therefore `h_T` is not in the normal image and the canonical triple does not
lift as an embedded flat union to the standard Fermat model modulo four.

The exceptional character remains visible.  In the verifier's `F_32` encoding,
the three component coefficients are

\[
P_\alpha(A)=14,\qquad P_\alpha(B_z)=29,\qquad
P_\alpha(B_w)=15,
\]

whose sum is

\[
28\ne0.
\]

Thus failure is genuinely at the nonlinear lifting gate, not at visibility.

This result covers the unique hyperbolic-pair orbit of triples containing
`L_A`.  It does not obstruct other incidence types, nonreduced structures,
rationally equivalent Chow cycles, derived objects, or the Hodge conjecture.
An embedded `W_2` survivor would still require a correct relative all-order
obstruction theory, formal effectivity, mixed-characteristic algebraization,
and rational comparison of the target character orbit.

Reproduce with

```sh
python3 millennium-prize/hodge/verify_cycle132_hyperbolic_triple.py
```

No Hodge or Millennium solution is claimed.
