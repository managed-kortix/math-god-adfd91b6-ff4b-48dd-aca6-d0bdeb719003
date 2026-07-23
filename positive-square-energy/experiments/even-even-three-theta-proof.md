# Even--even--three theta graphs

## Theorem

For all positive integers `r,s`,

`s^+(Theta(2r,2s,3))>|V(Theta(2r,2s,3))|`.

## Decomposition and variational ratio

Let the two even paths form the even cycle `C_N`, where `N=2r+2s`.  Write
the length-three ear as `u-x-y-v`; the cycle vertices `u,v` lie in the same
bipartition class.  On the common `N+2` dimensional space put

`A_0=A(C_N) direct_sum A(K_2)`

and let `B` be the symmetric adjacency matrix of the matching edges `ux,vy`.
Then the theta adjacency matrix is `A=A_0+B`.

Let `P=A(C_N)_+`, let `Q=A(K_2)_+=(1/2)J_2`, and put

`X_0=P direct_sum Q=(A_0)_+`, `S=tr(X_0^2)=N+1`.

For `t>=0`, define the PSD congruence witness

`X_t=(I+tB)X_0(I+tB)`.

For any nonzero PSD `X` with `tr(AX)>0`, scaling `X` in the standard
variational identity gives

`s^+(A)>=tr(AX)^2/tr(X^2)`.                              (1)

Write `a=P_uu=P_vv` and `b=P_uv`.  Exact block multiplication gives

`tr(AX_t)=S+(2+4a)t+2bt^2`,                             (2)

`tr(X_t^2)=S+(6+8a+8b)t^2+(1+2a^2+2b^2)t^4`.          (3)

The odd powers in (3) vanish by the cycle/K2 block parity.  The identities
`(P^2)_uu=(P^2)_vv=1` follow because the even cycle has `s^+=N` and is
vertex-transitive.

## Uniform parameter bounds

Since `P=(A(C_N)+|A(C_N)|)/2`,

`a=(1/2)|A(C_N)|_uu`.

The spectrum of `A(C_N)^2` lies in `[0,4]`, so
`sqrt(A(C_N)^2)>=A(C_N)^2/2`; as `(A(C_N)^2)_uu=2`, this gives `a>=1/2`.
Jensen/Cauchy--Schwarz for the spectral measure gives
`|A(C_N)|_uu<=sqrt(2)`, hence `a<=1/sqrt(2)`.  Finally the `{u,v}` principal
minor of `P` is PSD, so `|b|<=a`.

## Fixed choice t=1/3

Let `U=tr(AX_{1/3})` and `D=tr(X_{1/3}^2)`.  To prove the target via (1), it
suffices to show

`E=U^2-(S+1)D>0`.

Clearing the denominator gives

`81E=-2Sa^2+144Sa-2Sb^2-36Sb-28S`

`     +142a^2+48ab+72a+2b^2-48b-19`.                  (4)

On `1/2<=a<=1/sqrt(2)` and `-a<=b<=a`, the coefficient of `S` in (4) is
positive.  Since `S=N+1>=5`, substitute `S=5` to obtain

`81E>=132a^2+48ab+792a-8b^2-228b-159`.

For fixed `a`, this decreases with `b` throughout `[-a,a]`, so its minimum is
at `b=a`.  Hence

`81E>=172a^2+564a-159>=166>0`,

where the final minimum is at `a=1/2`.  Therefore (1) gives

`s^+(A)>S+1=N+2=|V(Theta(2r,2s,3))|`.

## Independent objective form and audits

Direct expansion in the unscaled square-energy variational objective gives

`2tr(AX_t)-tr(X_t^2)-(N+1)`

`=(8a+4)t-(8a+4b+6)t^2-(1+2a^2+2b^2)t^4`.

At `t=1/3` the gain beyond the two required units is at least `25/81` by the
same box bounds.  Four independent audits reproduced (2)--(4). Exact SymPy
matrix calculations for every same-color orbit of `C4,C6,C8,C10` agreed
coefficient-for-coefficient; the smallest ratio margin was `166/533` at the
`C4` case.
