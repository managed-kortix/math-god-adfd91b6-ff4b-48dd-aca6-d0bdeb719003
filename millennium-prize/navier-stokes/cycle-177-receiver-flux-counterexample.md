# Cycle 177: shared-pump receiver flux has sublinear critical cost

Populating the terminal outputs of the Cycle 176 collision block and measuring
actual cubic flux does not restore a linear critical-energy tax.  A common pump
can serve arbitrarily many independent horizontal layers.  After minimizing
over every amplitude, the complete `H^(1/2)` cost is `Theta(L^(2/3))` under
unit flux on every terminal receiver orbit.  The receivers do create an exact
undesignated convolution, computed below; it does not enter the designated
flux constraints.

## Shared-pump field

Fix `R>0` and distinct positive integers `Y_1,...,Y_L`.  This is the
`m=2` member of the Cycle 175/176 family.  Use the common pump orbit

\[
 p_\pm=(\pm R,0,0),\qquad u_{p_\pm}=b e_2,
\]

where `b>0`.  On layer `n`, put `K_n=(R^2+Y_n^2)^(1/2)` and populate the two
rail orbits by

\[
 u_{(-R,Y_n,0)}=a_ne_3,\qquad
 u_{(R,Y_n,0)}=-a_ne_3,
\]

with the negative frequencies fixed by reality.  The complete rail--pump
convolution has only the terminal pair on the positive layer,

\[
 S_{(-2R,Y_n,0)}=Y_na_nb e_3,\qquad
 S_{(2R,Y_n,0)}=-Y_na_nb e_3,                 \tag{1}
\]

where `N_k=iS_k` is the Fourier coefficient of `P(u dot grad u)` under the
chosen Fourier convention.  Populate these terminal outputs as receiver modes,

\[
 u_{(-2R,Y_n,0)}=ic_ne_3,\qquad
 u_{(2R,Y_n,0)}=-ic_ne_3,                    \tag{2}
\]

and again impose `u_{-k}=overline{u_k}`.  The phase in (2) is physical: it
turns the imaginary nonlinear coefficient into positive real energy transfer.
If `Q_n=(4R^2+Y_n^2)^(1/2)`, each of the two terminal frequency orbits has

\[
 \operatorname{Re}\langle N_k,u_k\rangle
   =Y_na_nbc_n.                              \tag{3}
\]

Thus the invariant unit-flux constraints are exactly

\[
 Y_na_nbc_n=1\qquad(1\le n\le L).            \tag{4}
\]

There are no hidden cross-layer terms.  Every rail and receiver is polarized
by `e_3` and every such frequency is planar, so all interactions among those
modes vanish.  Pump--pump interactions vanish as well.  Only interactions with
the common `e_2` pump survive.

## Full constrained `H^(1/2)` minimum

Count a reality orbit `[k]={k,-k}` once, with physical critical energy

\[
 E_c(u)=\sum_{[k]}2|k|\,|u_k|^2.
\]

The pump contributes `2Rb^2`.  Each layer has two rail orbits and two receiver
orbits, so the full energy, including the newly populated receivers, is

\[
 E_c=2Rb^2+\sum_{n=1}^L(4K_na_n^2+4Q_nc_n^2). \tag{5}
\]

For fixed `b`, (4) and weighted AM--GM give the exact layer minimum

\[
 \min_{a_nc_n=1/(Y_nb)}(4K_na_n^2+4Q_nc_n^2)
   ={8\sqrt{K_nQ_n}\over Y_nb},              \tag{6}
\]

attained at

\[
 a_n^2={1\over Y_nb}\sqrt{Q_n\over K_n},
 \qquad
 c_n^2={1\over Y_nb}\sqrt{K_n\over Q_n}.     \tag{7}
\]

Set

\[
 S_L=\sum_{n=1}^L{\sqrt{K_nQ_n}\over Y_n}.
\]

The remaining scalar minimization is

\[
 \min_{b>0}\left(2Rb^2+{8S_L\over b}\right).
\]

It is attained at `b^3=2S_L/R`, and hence

\[
 \boxed{\mathcal C_L
 =3\,2^{5/3}R^{1/3}S_L^{2/3}.}               \tag{8}
\]

For fixed `R` and any sequence `Y_n/R -> infinity`,

\[
 {\sqrt{K_nQ_n}\over Y_n}
 =\left((1+R^2/Y_n^2)(1+4R^2/Y_n^2)\right)^{1/4}
 \longrightarrow1.
\]

In particular, `R=1` and `Y_n=n` give `S_L=L+O(1)` and

\[
 \mathcal C_L=3\,2^{5/3}L^{2/3}(1+o(1))=o(L). \tag{9}
\]

This is an arbitrary-`L` counterexample to a universal linear `H^(1/2)` cost
deduced solely from unit actual cubic flux at every designated receiver.

## Undesignated complete convolution

The receiver modes cannot be omitted from the convolution.  On the positive
`Y_n` layer their Laurent coefficients are `ic_n A_(2R)`, while the common
pump is `b(z^(-R)+z^R)`.  Therefore

\[
 A_{2R}(z)(z^{-R}+z^R)
 =z^{-3R}+z^{-R}-z^R-z^{3R}.                 \tag{10}
\]

After multiplication by the derivative scalar `i`, the complete undesignated
nonlinearity on that layer is

\[
\begin{array}{c|c}
 k&N_k\\ \hline
 (-3R,Y_n,0)&-Y_nbc_ne_3\\
 (-R,Y_n,0)&-Y_nbc_ne_3\\
 ( R,Y_n,0)&\phantom{-}Y_nbc_ne_3\\
 ( 3R,Y_n,0)&\phantom{-}Y_nbc_ne_3.
\end{array}                                  \tag{11}
\]

The negative layer is its reality conjugate.  The two inner outputs in (11)
land on populated rail frequencies; the two outer outputs are outside the
field support.  There are no other terms.  By (4), every listed coefficient
has magnitude `Y_nbc_n=1/a_n`; thus the undesignated convolution is generally
large rather than depleted.  The construction disproves a linear input-energy
conclusion from the receiver-flux constraints alone, not a theorem that also
penalizes or dynamically controls all undesignated output.

This is an instantaneous Fourier-algebra and constrained-optimization
counterexample.  It is not an invariant subsystem, a Navier--Stokes solution,
a blowup construction, or a regularity result.

Run the full complex-convolution and optimization certificate with

```sh
python3 millennium-prize/navier-stokes/verify_cycle177_receiver_flux.py
```
