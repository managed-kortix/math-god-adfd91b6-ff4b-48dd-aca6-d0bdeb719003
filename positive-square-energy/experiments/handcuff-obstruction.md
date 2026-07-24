# Handcuff graphs: spectral analysis and the weighted obstruction

## The bare handcuff characteristic polynomial

For odd cycles `C_p, C_q` joined by a path of `L` edges, the characteristic
polynomial is

`chi = R_p R_q D_{L-1} - (D_{p-1} R_q + R_p D_{q-1}) D_{L-2}`

`        + D_{p-1} D_{q-1} D_{L-3}`,                                  (1)

where `D_j = U_j(x/2)` is the path characteristic polynomial and
`R_m = D_m - D_{m-2} - 2` is the cycle characteristic polynomial.
With `D_{-1}=0`, this covers `L=1` (bridge dumbbell) and `L>=2`.

The spectrum splits as `chi = g_p g_q Psi`, where `g_p, g_q` are the
"dark" cycle-local factors and `Psi` is the reduced connector polynomial.
The dark eigenvalues survive from the unjoined cycles and are known
exactly.

## The bare surplus

The minimum surplus over all odd handcuffs with `p,q<=31, L<=20` is at
`C5--P3--C5` (two pentagons joined by a 3-edge path), with surplus about
`0.6146`.  No counterexample to `s^+ >= n` was found in exhaustive exact
search through path length 31 or floating search through 1000.

The surplus is always positive but does NOT always reach `4/5`.  Thus the
bare `4/5` threshold that worked for theta graphs fails for handcuffs.

## The weighted obstruction

The weighted endpoint `s^+(A - E_vv/2) >= n` is **false** for bridge
dumbbells.  For `C5--C5` at a bridge endpoint,

`s^+(A(C5-C5) - E_vv/2) ≈ 9.93 < 10 = n`.

This is an exact algebraic obstruction: the weighted characteristic
polynomial factors as `(1/2)(x^2+x-1)^2 g(x)` where `g` is a degree-6
polynomial with four positive roots.  Rational Sturm isolation gives
`s^+ < 62067729/6250000 < 10`.

Therefore the weighted one-tree extension does NOT generalize from theta
cores to all bicyclic cores.  The theta case is special because its bare
surplus reaches `4/5` (with three exceptions directly certified), but
dumbbell cores have smaller surplus and fail the weighted endpoint at
penalty `1/2`.

## Next target: bare handcuff theorem

The bare inequality `s^+(C_p--P_L--C_q) >= p+q+L-1` for odd `p,q` and
`L>=2` remains the active target.  The variational witness gives an exact
gain formula

`Phi(X_t) = s^+(D) + L_r t - Q_r t^2 - S_r t^4`,                (2)

where `D = A(C_p) ⊕ A(C_q) ⊕ A(P_{L-1})`, and `L_r, Q_r, S_r` are
explicit in terms of cycle and path resolvent entries.  The gain `G_r`
at the optimal `t` must exceed `1 - delta_p - delta_q` to reach `n`.
For `C5-C5`, the required gain is `2*sqrt(5)-3 ≈ 1.472`, while the
actual coupling gain is about `2.1`.
