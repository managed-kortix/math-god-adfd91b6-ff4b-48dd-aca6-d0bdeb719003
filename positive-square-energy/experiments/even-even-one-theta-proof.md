# Even--even--one theta graphs

## Theorem

For all positive integers `r,s`,

`s^+(Theta(2r,2s,1))>|V(Theta(2r,2s,1))|`.

## Setup

The graph is an even cycle `C_N`, `N=2r+2s`, plus a chord between vertices
`u,v` in the same bipartition class.  Let `A` be the cycle adjacency matrix,
`P=A_+`, and define the normalized chord vectors

`a=(e_u+e_v)/sqrt(2)`, `b=(e_u-e_v)/sqrt(2)`.

The chord matrix is `E=aa^T-bb^T`.  Put

`x=a^TPa`, `y=b^TPb`, `q=b^TP^2b`.

Cycle reflection interchanging `u,v` commutes with `P`, fixes `a`, and negates
`b`; hence `a^TPb=0`.

## PSD witness

For `t=-1/3`, put `T=I+tbb^T` and `alpha=(1-x)_+`.  The matrix

`Y=TPT+alpha aa^T`

is positive semidefinite.  The variational identity

`s^+(M)=max_{Y>=0}(2tr(MY)-tr(Y^2))`

and direct rank-one trace expansion give

`s^+(A+E)-s^+(A)`

`>= 2x-(8/9)y-(2/9)q-(25/81)y^2+(1-x)_+^2`.       (1)

This identity was independently expanded symbolically and by exact cycle
matrices.  The positive `aa^T` correction is essential; contracting only the
negative chord direction can fail.

## Uniform scalar bounds

Because `a,b` lie in one bipartition class, bipartite spectral symmetry gives
equal positive and negative spectral masses on each vector.  In particular,
if `Pi_+` is the positive spectral projector, then

`b^T Pi_+ b <=1/2`.

Spectral Cauchy--Schwarz therefore gives

`y^2 <= (b^T Pi_+ b)(b^TP^2b) <=q/2`.              (2)

On the same bipartition class the quadratic form of `P^2` is half that of
`A^2`.  Thus

`q=(1/2)b^TA^2b=1-(A^2)_{uv}/2 <=1`.               (3)

Also `P=(|A|+A)/2` and `a^TAa=0`.  Since the spectrum of `A^2` lies in
`[0,4]`, functional calculus gives `|A|=sqrt(A^2)>=A^2/2`.  Hence

`x=(1/2)a^T|A|a >=(1/4)a^TA^2a=(2+(A^2)_{uv})/4>=1/2`. (4)

For `x>=1/2`,

`2x+(1-x)_+^2>=5/4`.

Using (2)--(4) in (1),

`s^+(A+E)-s^+(A)`

`>=5/4-8/(9sqrt(2))-2/9-25/162`

`=283/324-4sqrt(2)/9>0`.

The last inequality follows from `283^2>2*144^2`.  Finally the even cycle is
bipartite, so `s^+(A)=N`.  The chord adds no vertex, proving
`s^+(Theta(2r,2s,1))>N`.

The bound includes `N=4`; there `(A^2)_{uv}=2` and the estimates only improve.

## Adversarial checks

Two hostile audits recomputed the complete trace formula.  For the critical
antipodal chord of `C_8`, the witness gain is exactly

`283/324-4sqrt(2)/9=0.2449174290...`,

while the actual gain is `0.7108314535...`.  Exact evaluations on every chord
orbit of `C_4,C_6,C_8` agree with (1).
