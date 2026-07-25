# Shared-vertex `C3 vee C_{4k+1}`: a continuant phase reduction

## Theorem

Let `G` have core `C3 vee C_q`, where `q=4k+1>=5`, and allow an arbitrary
rooted tree at every core vertex.  Then

`s^+(G) >= n+1-(sec(pi/q)-1)=n+2-sec(pi/q)>n`.                 (T)

Eliminate the trees by matching BP.  Every core activity then has the form
`t+y`, with `y>=0`, and the whole imaginary-axis characteristic function has
an irrelevant positive real factor.

Write `K(x_1,...,x_r)` for the path continuant

`K()=1`, `K(x_1)=x_1`,

`K(x_1,...,x_r)=x_r K(x_1,...,x_{r-1})+K(x_1,...,x_{r-2})`.       (1)

For a lobe whose noncommon vertices have activities `x_1,...,x_r`, put

`A_r=K(x_1,...,x_r)`,

`B_r=K(x_2,...,x_r)+K(x_1,...,x_{r-1})`.                         (2)

Thus `A_r` is the matching partition when the common vertex is unavailable,
and `B_r` is the sum of the two partitions obtained by matching the common
vertex along one of its incident lobe edges.

For the triangle (`r=2`) these specialize to

`A_3=uv+1`, `B_3=u+v`.                                          (3)

For the long lobe (`r=q-1`) write `A_q,B_q`.  If `a` is the common-vertex
activity, the real matching carrier is

`R=a A_3 A_q+B_3 A_q+A_3 B_q`.                                  (4)

The two Sachs multipliers are `-2i` for the triangle and `+2i` for `C_q`.
Consequently

`Psi_G/K_tree=R+2i(A_3-A_q)`.                                    (5)

This corrects the sign that is easy to lose in this mixed-phase case.

## Bare-cycle comparison

Put `k_0=1`, `k_1=t`, and

`k_r=t k_{r-1}+k_{r-2}`.                                        (6)

The bare `C_q` quantities are

`alpha_q=k_{q-1}`,

`beta_q=2k_{q-2}`,

`c_q=t alpha_q+beta_q=Z_{C_q}(t)`.                               (7)

The key coefficientwise lemma is

`F_q:=R-c_q(A_3-A_q) in N[t,y_0,...,y_{q+1}]`,                   (8)

after substituting `a,u,v,x_j=t+y_j`.  Formula (8) immediately gives, when
`A_3>A_q`,

`2(A_3-A_q)/R <= 2/c_q`;                                         (9)

when `A_3<=A_q`, the left side is nonpositive.  Hence (8) implies the uniform
phase comparison

`Arg Psi_G(t) <= arctan(2/c_q)=Arg Psi_{C_q}(t)`.                 (10)

The arguments are the continuous ones tending to zero at infinity.  The
right side lies in the first quadrant, while the bouquet argument is allowed
to become negative.  Thus no false fixed-half-plane assertion is needed.

Integrating (10) in the signed Coulson identity gives

`s^+(G)-s^-(G) >= s^+(C_q)-s^-(C_q)=-2 delta_q`,                 (11)

where `delta_q=q-s^+(C_q)`.  Since the bouquet has `m=n+1`,

`s^+(G)>=n+1-delta_q>n`.                                        (12)

The final strict inequality uses the elementary cycle calculation

`delta_q=q-s^+(C_q)=sec(pi/q)-1 in (0,1)`.                       (13)

Indeed,

`s^+(C_{4k+1})=4+8 sum_{j=1}^k cos^2(2 pi j/(4k+1))`.

Summing the cosines and putting `a=pi/(2q)` gives

`delta_q=4 cos(a)sin(3a)/sin(4a)-3=sec(pi/q)-1`.

## Coefficientwise proof

The lemma has a short uniform proof.  Let `alpha=alpha_q`, `beta=beta_q`, and

`H=(a+c_q)A_3+B_3`.

Since every long-lobe activity is `t+y_j`, expansion of the matching
partitions gives coefficientwise

`A_q-alpha >=_coeff 0`, `B_q-beta >=_coeff 0`.                 (14)

Using `c_q=t alpha+beta`, rearrange (8) exactly as

`F_q=(A_q-alpha)H`

`    +alpha[(a+c_q-t)A_3+B_3]`

`    +A_3(B_q-beta)`.                                          (15)

Every factor on the right has nonnegative coefficients after `a=t+y_0`,
because `a+c_q-t=y_0+c_q`.  This proves (8) coefficientwise for every
`q>=3`; no residue-class assumption enters the algebra.  The condition
`q=1 mod 4` is used only for the Sachs sign in (5).

## Uniform recurrence

For bare paths, separate parity by setting `x=t^2`,

`E_m(x)=k_{2m}(t)`, `O_m(x)=k_{2m+1}(t)/t`.

Both sequences obey the positive continuant recurrence

`X_m=(x+2)X_{m-1}-X_{m-2}`,                                    (16)

with

`E_0=1, E_1=x+1`, `O_0=1, O_1=x+2`.

Equivalently, the bare cycle carriers obey the four-step recurrence

`c_{r+4}=(t^4+4t^2+2)c_r-c_{r-4}`.                              (17)

At the all-bare point, (8) collapses by direct algebra to the useful product

`F_q(t,0,...,0)=alpha_q(c_q+2t)`.                               (18)

Indeed, with `A_3=t^2+1` and `B_3=2t`, subtracting
`c_q(A_3-alpha_q)` from (4) cancels everything except (18).

Thus the uniform certificate is not an SOS in squares but the three-term
nonnegative decomposition (15).  The continuant recurrence proves the two
coefficientwise differences in (14), while (16) or (17) tracks the bare
carriers.  This form remains stable as `q` increases; direct full expansion
does not.

## Exact symbolic evidence

Full integer expansion of (8) gives:

| `q` | nonzero terms | minimum coefficient | maximum coefficient |
|---:|---:|---:|---:|
| 5 | 293 | 1 | 26 |
| 9 | 6623 | 1 | 806 |
| 13 | 136073 | 1 | 31846 |

There are no negative or zero listed coefficients.  The constant-in-`y`
parts agree with (18):

`q=5:  t^9+8t^7+23t^5+26t^3+7t`,

`q=9:  t^17+16t^15+105t^13+364t^11+717t^9+806t^7+492t^5+140t^3+11t`,

`q=13: t^25+24t^23+253t^21+1540t^19+5985t^17+15504t^15`

`      +27134t^13+31846t^11+24400t^9+11608t^7+3143t^5+406t^3+15t`.

The finite checks are therefore corroboration rather than the proof.  The
uniform proof is the exact decomposition (15), together with continuant
coefficientwise monotonicity.
