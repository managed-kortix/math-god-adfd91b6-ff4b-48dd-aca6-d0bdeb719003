# Cycle 210: additional-primary scout for `D=-1499`

Let

\[
A=433\mathrm a1^{(-1499)}:
y^2+xy+y=x^3-46813x-3372156843.
\]

## Verdict

The feasible additional prime is

\[
\boxed{p=11}.
\]

The exact one-prime Kurihara certificate at the Kolyvagin prime `ell=661`,
with primitive root `eta=2`, is

\[
\widetilde\delta^{(1)}_{661}(A)=203746\equiv4\pmod {11}.
\]

This is computed from exact PARI modular symbols for the level-433 base curve
and the quadratic-twist identity used in Cycles 187--188.  Every symbol
denominator encountered is an 11-adic unit.  The globally minimal differential
comparison for the `-1499` twist is `kappa_1499=1`.

Exact point counting gives

\[
a_{661}(A)=2,\qquad \#A(\mathbf F_{661})=660,
\]

so `661=1 mod 11` and `a_661=661+1 mod 11`.  The Cycle 195 rational point
reduces to `(612,238)` and has order `165`; its image in
`A(F_661)/11A(F_661)` is therefore nonzero.  Since `v_11(660)=1`, that quotient
has dimension one over `F_11`.

Under Kim, arXiv:2203.12159v6, Theorems 1.8 and 1.10, the same rank-one
argument as Cycle 209 gives

\[
\operatorname{Sel}(\mathbf Q,A[11])\simeq\mathbf F_{11},
\qquad \Sha(A/\mathbf Q)[11^\infty]=0.
\]

## Hypothesis audit

| item | `p=3` | `p=5` | `p=11` |
|---|---:|---:|---:|
| good reduction | yes | yes | yes |
| `a_p(A)` | `-2` | `-4` | `4` |
| `#A(F_p)` | `6` | `10` | `8` |
| ordinary (`a_p` is a `p`-unit) | yes | yes | yes |
| nonanomalous (`p` does not divide `#A(F_p)`) | no | no | yes |
| Kim's stated range `p>=5` | no | yes | yes |
| Tamagawa numbers are `p`-units (`1,2`) | yes | yes | yes |
| outcome | excluded | blocked | feasible |

Thus `p=3` is outside the theorem's `p>=5` range and is also anomalous;
`p=5` is anomalous.  Neither is a clean application of the Cycle 209 theorem
packet.  At `p=11`, good ordinarity and nonanomalousness follow from
`#A(F_11)=8`.

Residual surjectivity at 11 follows without a division-field computation.  At
`433`, multiplicative type `I_1` gives a nontrivial transvection modulo 11.
At the good prime `5`, the twist is unramified with quadratic value `+1`, and
the Frobenius polynomial has trace `-4`, determinant `5`, and discriminant
`7 mod 11`, a nonsquare.  The standard subgroup classification then gives
`SL_2(F_11)` in the image; the cyclotomic determinant is onto, hence the image
is `GL_2(F_11)`.  The Tamagawa factors are `c_433=1`, `c_1499=2`, and good
reduction at 11 makes Kim's semistable Manin condition applicable.

The exact root number is `-1`, so the zero-prime Kurihara value vanishes.  The
nonzero one-prime value therefore has minimal support one.  Gross--Zagier--
Kolyvagin supplies finiteness of `Sha`, as in Cycle 209.

BSTW `corA'` also applies at 11: `11` is ordinary, `11` does not divide the
conductor, the residual representation is absolutely irreducible and ramified
at `433`, and the analytic rank is one.  Since torsion and Tamagawa factors are
11-adic units, it additionally gives

\[
v_{11}\!\left(\frac{L'(1,A)}{\Omega_A R(A/\mathbf Q)}\right)=0.
\]

Both deductions retain the external theorem trust boundaries documented in
Cycle 209.  The modular-symbol producer is PARI `msfromell`; the calculation is
exact but is not an implementation-independent modular-symbol replay.

Reproduce with

```sh
gp -fq millennium-prize/birch-swinnerton-dyer/cycle210_D1499_p11_kurihara.gp
```

The computation evaluates `660*1498` exact base modular symbols and can take
several minutes.  This excludes only the 11-primary part in addition to the
previously certified 7-primary part; it does not prove full `Sha=1`.
