# Exact DNN reduction for theta-plus-cycle block graphs

Let the cyclic blocks be `Theta(a,b,c)` and `C_q`, joined through any block
tree, with arbitrary rooted trees. Put `L=a+b+c` and let t be the number of
bridge edges. Then `n=L+q+t-2`, `m=n+2`.

The exact elliptope/path formula gives

`kappa(Theta)=L+Delta(a,b,c)`,

where

`Delta=min_theta [sum_even l tan^2(theta/(2l))
 +sum_odd l tan^2((pi-theta)/(2l))]`.

Also `kappa(C_q)=q+epsilon_q`, where epsilon is zero for even q and
`epsilon_q=q tan^2(pi/(2q))` for odd q. One-vertex additivity and
`kappa(K2)=1` therefore give

`kappa(G)=n+2+Delta+epsilon_q`,

so `s^+(G)>=n+2-Delta-epsilon_q`.

The elementary monotonicity of `h_s(x)=s tan^2(x/s)` yields the exact residual
classification:

- `Delta>1` iff the sorted theta lengths are `(1,2,r)`, `r>=2`;
- the maximum is `Delta(1,2,2)=(sqrt(17)-1)/2`;
- away from `(1,2,2)`, every `(1,2,r)` has `Delta<4/3`;
- `epsilon_3=1`, `epsilon_5=5-2sqrt(5)<2/3`, and
  `epsilon_q<2/5` for odd `q>=7`.

Consequently DNN proves `s^+(G)>=n` except exactly

1. `Theta(1,2,r)` plus `C_3`, for `r>=2`;
2. `Theta(1,2,2)` plus `C_5`.

The list is independent of cut/root locations and all tree attachments. These
are failures of this exact DNN threshold, not counterexamples. A direct rooted
packet or another spectral argument is needed only for these residuals.

Warning: `D(X vee Y)>=D(X)+D(Y)` is false. A proposed generic root-phase lemma
is also false. Neither can close these rows.
