# Multiple triangles against a rooted hostile pentagon: exact Sachs obstruction

## Verdict

Let `A` be a connected triangular cactus, let `r` be a vertex of `A`, and
coalesce `r` with a vertex of a hostile pentagon `P=C5`. Arbitrary rooted trees
may be attached to the resulting cactus. The packing-one proof cannot be
extended merely by replacing each matching carrier by a positive signless
matching polynomial and grouping by the number of selected triangles.

The exact grouped Sachs formula has alternating real and imaginary sums. With
six triangles, its real part can be negative and its imaginary part positive
near `t=0`; the normalized characteristic polynomial then lies in the second
quadrant even though its continuous Coulson argument lies on the sheet below,
near `-3 pi/2`. Thus both ingredients used by the packing-one proof fail:

1. the real part need not be positive; and
2. the continuous argument need not be the principal arctangent.

This is an obstruction to a positivity-only whole-territory phase proof, not a
counterexample to positive square energy and not a counterexample to the
possible inequality `Theta_G(t)<theta_5(t)` on the correctly unwrapped sheet.
Nor can the retracted rooted Voronoi argument fill the gap: maximum cycle
packing does not force its territories to have packing one.

## 1. Exact grouped formula

After eliminating off-spine trees, all vertex activities are positive and all
deleted-core matching partitions below are positive. The same formulas hold
without tree elimination by using ordinary signless matching polynomials.

For `j>=0`, define

```text
A_j(t)=sum Z_(G-V(C_1)-...-V(C_j))(t),
```

where the sum is over all collections of `j` pairwise vertex-disjoint
triangles and does not select `P`. Define

```text
B_j(t)=sum Z_(G-V(P)-V(C_1)-...-V(C_j))(t),
```

where the selected triangles are also disjoint from `P`. Empty sums are zero.
Every nonzero `A_j` and `B_j` is strictly positive for `t>0`.

A triangle has Sachs multiplier `-2i`, while `P` has multiplier `+2i`.
Consequently the normalized characteristic polynomial is exactly

```text
Psi_G(t)=sum_j (-2i)^j A_j(t)+2i sum_j (-2i)^j B_j(t)
        =R(t)+i I(t),

R(t)=sum_(k>=0) (-4)^k [A_(2k)(t)+4B_(2k+1)(t)],
I(t)=2 sum_(k>=0) (-4)^k [B_(2k)(t)-A_(2k+1)(t)].       (1.1)
```

Formula (1.1) records all signs and cancellations. Positivity of the matching
polynomials does not imply positivity of either displayed alternating sum.
Packing one truncates (1.1) to

```text
R=A_0+4B_1>0,             I=2(B_0-A_1),
```

which is precisely the special structure used in the existing rooted packet
argument. Packing two already introduces `-4A_2` and `-8(B_2-A_3)`; higher
packing introduces successive powers of `-4`.

For comparison, the isolated pentagon is

```text
Psi_P(t)=Z_5(t)+2i,       Z_5(t)=t^5+5t^3+5t,
theta_5(t)=atan(2/Z_5(t)) in (0,pi/2).                    (1.2)
```

When `R>0`, comparison with (1.2) reduces to the familiar cross-product
inequality `I Z_5<2R` if `I>0`, and is automatic if `I<=0`. There is no such
one-chart reduction when `R` changes sign and the argument winds.

## 2. A six-triangle exact obstruction

Take the six triangles

```text
T1=(0,1,2),   T2=(0,3,4),   T3=(3,5,6),
T4=(5,7,8),   T5=(3,9,10),  T6=(6,11,12),
```

and coalesce `P=(0,13,14,15,16)` at the root `0`. This is a connected cactus
with six triangular blocks and one pentagonal block. No attached trees are
needed.

The grouped matching sums are

```text
A0=t^17+23t^15+198t^13+829t^11+1822t^9+2085t^7
   +1146t^5+263t^3+17t,
A1=6t^14+92t^12+516t^10+1346t^8+1670t^6+884t^4+168t^2+6,
A2=9t^11+92t^9+327t^7+471t^5+236t^3+33t,
A3=5t^8+33t^6+62t^4+29t^2+3,
A4=t^5+3t^3+t,

B0=t^12+14t^10+63t^8+116t^6+87t^4+22t^2+1,
B1=4t^9+30t^7+70t^5+54t^3+10t,
B2=3t^6+13t^4+11t^2+1,
B3=t^3+t.
```

There are no other nonzero groups. Substitution in (1.1) gives

```text
R=t^17+23t^15+198t^13+793t^11+1470t^9+897t^7
  -442t^5-433t^3-75t,

I=-12t^14-182t^12-1004t^10-2526t^8-2868t^6
  -1202t^4-148t^2+6.                                    (2.1)
```

Hence, as `t` decreases to zero,

```text
R(t)=-75t+O(t^3)<0,       I(t)=6+O(t^2)>0.                (2.2)
```

The principal argument of `Psi_G(t)` therefore tends to `pi/2`. In particular,
it is positive and larger than the isolated pentagon's principal argument for
all sufficiently small `t`, since

```text
theta_5(t)=pi/2-(5/2)t+O(t^3),
Arg_principal Psi_G(t)=pi/2+(25/2)t+O(t^3).
```

Thus the principal phase comparison itself is false near zero. More
importantly, this principal value is not the continuous Coulson branch. The
exact characteristic polynomial is

```text
x^17-23x^15-12x^14+198x^13+182x^12-793x^11-1004x^10
+1470x^9+2526x^8-897x^7-2868x^6-442x^5+1202x^4
+433x^3-148x^2-75x-6.                                    (2.3)
```

An exact Sturm count applied to (2.3) gives inertia `(n+,n-,n0)=(7,10,0)`.
Therefore

```text
lim_(t downarrow 0) Theta_G(t)=(pi/2)(n+-n-)=-3pi/2.       (2.4)
```

The branch starting at `Theta_G(infinity)=0` has crossed the negative real
axis and equals the principal argument minus `2pi` near zero. Any proof that
sets `Theta_G=atan(I/R)` or uses positivity of `R` has therefore lost one full
winding.

For completeness, the direct cross product also displays cancellation:

```text
I(t)Z_5(t)-2R(t)
=-12t^19-244t^17-2020t^15-8852t^13-22104t^11
 -31112t^9-22292t^7-5860t^5+156t^3+180t.                 (2.5)
```

It has both positive and negative coefficients. Thus coefficientwise matching
positivity cannot prove the desired comparison even after the real and
imaginary parts are cross-multiplied.

## 3. Correct conclusion

The following stronger whole-packet statement is not established by this
calculation:

```text
Theta_G(t)<theta_5(t) for every t>0,
```

where `Theta_G` is continuously unwrapped from infinity. The six-triangle
example is compatible with that inequality because its small-`t` branch is
near `-3pi/2`, not near `+pi/2`. Proving it would require a winding-sensitive
argument, such as a control of every negative-real-axis crossing or a
matrix/rooted continued-fraction theorem. It cannot follow from the signs of
the individual matching carriers in (1.1).

Accordingly, the valid general phase theorem currently available is only the
packing-one rooted packet. For the six-triangle shared-cluster problem, the
separate exact marked-incidence reduction in
`research/octacyclic-rooted-six-triangle-finite-reduction-2026-07-26.md`
certifies 107 of 111 rooted orbits and leaves four explicit kernels. The
all-rank Voronoi extension has been retracted, so neither that extension nor a
single whole-territory phase theorem may presently be used to close those four
kernels.

The requested restriction to at most six triangles does not rescue the
positivity-only approach: the obstruction above already occurs at six.
