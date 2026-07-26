# Bounded scout checkpoints — cycle 28

These are exact bounded checkpoints for the five non-main Millennium routes.
They do not resolve any Millennium problem and do not alter the active RH
funnel.

## Birch--Swinnerton-Dyer

If `L_5(T)=c_0+c_1T+c_2T^2+...` and `T=6^s-1`, then

\[
 {d\over ds}L_5(6^s-1)|_{s=0}=c_1\log_5 6,
\]

\[
 {d^2\over ds^2}L_5(6^s-1)|_{s=0}
 =(c_1+2c_2)(\log_5 6)^2.
\]

Thus a second-derivative valuation does not certify cyclotomic order two.
One must prove `c_0=c_1=0` and then `c_2!=0` in the power-series coordinate.

## Hodge conjecture

For the Fermat cubic plane, the degree-three cokernel of

\[
 H^0(\mathcal O_P(1)^3)\xrightarrow{(u^2,v^2,w^2)}H^0(\mathcal O_P(3))
\]

is exactly the line spanned by `uvw`.  Hence the coefficient of `uvw` in the
restricted deformation is the explicit first-order local equation for the
plane-incidence divisor.

## Navier--Stokes

If the pressure has finite Fourier support `S`, then

\[
 3\int p\,u\cdot\nabla|u|
 =-3\sum_{k\in S}ik\,\widehat p(k)\cdot\widehat{|u|u}(-k).
\]

Only those finitely many coefficients of the unprojected field `|u|u` are
needed.  Projection onto the original velocity triad is invalid unless `S` is
contained in that triad.

## P versus NP

Dense encoding of six-vertex graphs has input length `15`, so the target size
is `225`.  Arbitrary labels on `h` examples admit a De Morgan circuit of size
at most

\[
 3(h-1)+\min(15,h-1).
\]

This is at most `225` for every `h<=71`.  Therefore no antichecker with at most
71 six-vertex examples can refute every size-225 circuit.

## Yang--Mills mass gap

Let `T` be multiplication by `x` on `L^2([0,1])`.  Its spectrum reaches one,
so `-log T` has no positive gap.  Nevertheless every finite-dimensional
subspace `F` satisfies

\[
 \max_{f\in F,\ \|f\|=1}\langle f,Tf\rangle<1.
\]

Compactness gives a maximizer, while equality would require a nonzero `L^2`
function supported at `x=1`.  Hence strict contraction on every finite trial
space does not imply a full-operator mass gap.
