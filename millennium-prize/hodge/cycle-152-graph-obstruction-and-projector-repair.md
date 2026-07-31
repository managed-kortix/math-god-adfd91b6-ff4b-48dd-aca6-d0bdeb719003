# Cycle 152: the diagonal is rank-six obstructed while its Weil projection is horizontal

Cycle 151's special algebraic seed survives two necessary repairs.  First, the
normalized pure coefficients are the conjugate pair `-i/8,+i/8`, rather than
literal real coefficients in conjugate complex bases.  Second, algebraicity of
the rational Weil projector is established by spectral interpolation in an
actual algebraic endomorphism, not by formally exterior-powering a complex
eigenspace projector.

Take `u=2+i`.  On

\[
\bigwedge^pW\otimes\bigwedge^{6-p}\bar W
\]

its action has eigenvalue

\[
\lambda_p=(2+i)^p(2-i)^{6-p}.
\]

These seven values are distinct.  The rational polynomial

\[
q(t)=-\frac{(68381t+10391779)(t-125)
(t^2-150t+15625)(t^2+70t+15625)}
{930187500000000000}
\]

equals one on `lambda_0,lambda_6` and zero on the other five sectors.
Therefore `q(Gamma_u)` is a rational algebraic correspondence inducing the
Weil projector on `H^6`.  The projected diagonal is consequently a rational
algebraic class, and its transform under `1+i` spans the exceptional plane.

The deformation gate is negative for the graph itself.  Let

\[
Q=\operatorname{diag}(1,1,3).
\]

The nine-dimensional PEL tangent is parametrized by `B in M_3(C)` with
off-diagonal Beltrami blocks

\[
\mu_B=\begin{pmatrix}0&B\\Q^{-1}B^t&0\end{pmatrix}.
\]

Restricting to the diagonal and projecting to its normal bundle gives the exact
embedded obstruction

\[
\boxed{\rho_\Gamma(B)=Q^{-1}B^t-B.}
\]

It has

\[
\boxed{\operatorname{rank}\rho_\Gamma=6},
\qquad
\boxed{\dim\ker\rho_\Gamma=3},
\]

with kernel spanned by `E00`, `E01+E10`, and `E11`.  The tempting six-
dimensional symmetric kernel applies only when both polarization blocks agree;
it is incorrect for the `(1,1,3)` second block while keeping the graph
unweighted.

Contraction of the full graph class has the same rank-six map and kernel.  By
contrast, contraction of its pure Weil projection vanishes in all nine PEL
directions: the determinant class remains Hodge throughout the Weil component.
Thus projection discards precisely the balanced components detecting failure
of the actual graph to remain holomorphic.

For the rational projector combination of transformed graphs, all nine
semiregularity/Hodge obstructions cancel.  This cancellation occurs only after
mapping the separate embedded obstruction spaces into cohomology.  It does not
make the componentwise graph obstructions vanish, nor does a rational
difference of cycles define a new effective Chow point.  A separate effective
representative or perfect complex with the same projected class could still
have another local germ, but none is constructed here.

Principle B and motivated deformation likewise transport absolute/motivated
status, not algebraicity.  Promoting the flat class from this special fiber is
exactly the variational Hodge problem.

Reproduce with

```sh
python3 millennium-prize/hodge/verify_cycle152_graph_deformation.py
```

This closes the diagonal-graph deformation ansatz at first order while
preserving the special-fiber algebraic seed.  It does not settle generic
algebraicity or the Hodge conjecture.
