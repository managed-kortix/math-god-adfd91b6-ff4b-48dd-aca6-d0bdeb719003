# Cycle 49: exact finite complete-prefix certificate

## Status

`cycle49_exact_prefix_certificate.py` is a standalone, fail-closed certificate
for the exact finite complete-prefix split on the closed physical interval

\[
I_0=[1,3/2],\qquad \theta=2/5.
\]

It checks all 67 physical rows at \(a=218\) and all 93 physical rows at
\(a=301\). It does not sample rows and extrapolate. It certifies 160 finite
rows and 31,847 finite \((q,n)\) cells in total.

**Asymptotics are untested.** The certificate proves no eventual sign,
asymptotic lower bound, positive liminf, moving-projection theorem,
completed-square budget, or consequence for the Riemann hypothesis.

## Exact finite identities

Put \(M=2a-1\), \(L_n=\log n\), and

\[
\mathfrak a_{q,n}=\frac nq-\log\frac{n+1}{q},
\qquad
s_n=\frac{\ell_n}{L_n}-\eta_nm_n,
\]

\[
\mathcal P_{q,n}
 =\frac{C_{n+1}}q-
   \sum_{k=q}^{n}\frac{\psi(k)}{k(k+1)}.
\]

For every declared physical row, the verifier constructs

\[
P_a^+(q)=\sum_{n=q}^{M}
 \frac{\alpha_{q,n}}{L_n}\mathcal P_{q,n},
\qquad
S_a^\mu(q)=\sum_{n=q}^{M}
 \alpha_{q,n}\mathfrak a_{q,n}s_n,
\]

and directly certifies

\[
\boxed{B_a(q)=P_a^+(q)+S_a^\mu(q)}.
\]

For

\[
\Sigma(q,m)=\sum_{n=m}^{M}\frac{\alpha_{q,n}}{L_n},
\qquad
\delta_m=L_{m+1}-L_m,
\]

it independently certifies

\[
P_a^+(q)=\frac{C_q}{q}\Sigma(q,q)
 +\sum_{m=q}^{M}\psi(m)
  \left(\frac{\delta_m}{q}-\frac1{m(m+1)}\right)\Sigma(q,m).
\]

Define

\[
\mathfrak h_n=1+\ell_n-L_nm_n,
\quad
u(q,n)=\frac{\alpha_{q,n}\mathfrak a_{q,n}(1-\eta_n)}{\delta_n},
\]

\[
\omega(q,q)=u(q,q)+
 \frac{\alpha_{q,q}\mathfrak a_{q,q}}{L_q},
\]

and, for \(n>q\),

\[
\omega(q,n)=u(q,n)-u(q,n-1)
 +\frac{\alpha_{q,n}\mathfrak a_{q,n}}{L_n}.
\]

The second independent Abel check is

\[
\begin{aligned}
S_a^\mu(q)={}&-
 \left(1-\frac1q\right)\Sigma(q,q)
 +\sum_{m=q}^{M}\left(\delta_m-\frac1q\right)\Sigma(q,m)\\
&+\sum_{n=q}^{M}\omega(q,n)\mathfrak h_n
 -u(q,M)\mathfrak h_{2a}.
\end{aligned}
\]

The endpoint \(\mathfrak h_{2a}\) is retained. It is not treated as an
extra temporal summand.

## Fail-closed boundary

The certificate:

1. runs only under `python -I -B`, with `LC_ALL=C` and bytecode disabled;
2. captures its own source and the bound Cycle 47 ancestor before importing
   `flint`;
3. rejects repository import shadows, bytecode caches, symlinks, and
   group/world-writable closure files;
4. pins CPython 3.12.13, python-flint 0.9.0, and FLINT 3.6.0;
5. uses 192-bit Arb interval arithmetic;
6. requires strict outward signs such as `value > 0` or `value < 0`;
7. requires every identity ball to contain zero and to lie below the declared
   \(2^{-96}\) error ceiling;
8. rechecks the source/input closure before emitting the buffered result.

The interpreter, wheel, native-library binaries, OS, hardware, and `uv`
launcher are version-pinned but not binary-attested.

The physical reconstruction preserves the affine term
\(-\eta_n\chi\), every Möbius sign, the full Vasyunin kernel, and the exact
restricted-space correction \(-1/(qd)\).

## Certified finite sign defects

At \((a,q)=(218,327)\), the independent run certifies

```text
B   [-5.27819898090004597635960939462029962653636997373e-5 +/- 2.99e-53]
H   [ 5.38346223769557724209891931359588891858711128926e-5 +/- 2.68e-54]
hat [ 1.05263256795531265739309918975589292050741315533e-6 +/- 2.51e-54]
```

Thus

\[
B<0,\qquad H>0,\qquad \widehat c>0,
\qquad B\widehat c<0,\qquad BH<0.
\]

This is a finite physical row counterexample to the corresponding universal
pointwise sign rules. It is not an eventual or asymptotic counterexample.

At \(a=301\), over all 93 physical rows, put

\[
p=\lVert B\rVert^2,
\quad BH=\langle B,H\rangle,
\quad \gamma=\frac{p+BH}{p},
\quad Q_{\rm cp}=\frac{(p+BH)^2}{p}.
\]

The verifier certifies

```text
p     [ 7.10523809552302445904393305282208524650025861406e-6 +/- 3.54e-54]
BH    [-7.23735938504519259972417148087648328689540177963e-8 +/- 2.77e-56]
gamma [ 0.989814050862552491921837671308355037444574153078 +/- 2.62e-49]
D     [ 7.07938720457846598204258198477787274250897615554e-6 +/- 1.84e-54]
Qcp   [ 6.96122810156797559412001493198552613067378424531e-6 +/- 4.83e-54]
```

In particular, \(p>0\) and \(BH<0\). This disproves a universal finite
aggregate nonnegative-cross-term rule. It does not settle any eventual sign.

## Canonical replay

From the repository root:

```bash
rm -f /tmp/cycle49-exact-prefix-certificate.out && \
env -u PYTHONPYCACHEPREFIX PYTHONDONTWRITEBYTECODE=1 LC_ALL=C \
uv run --isolated --no-project --python 3.12.13 \
  --with python-flint==0.9.0 \
  python -I -B \
  millennium-prize/riemann-hypothesis/cycle49_exact_prefix_certificate.py \
  > /tmp/cycle49-exact-prefix-certificate.out && \
cmp /tmp/cycle49-exact-prefix-certificate.out \
  millennium-prize/riemann-hypothesis/cycle49-exact-prefix-certificate.out
```

The canonical output ends with

```text
counterexample_signs=PASS B<0 H>0 hat>0 B*hat<0 B*H<0
aggregate_signs=PASS p>0 BH<0 gamma>0 D>0 Qcp>0
ASYMPTOTICS_UNTESTED
ALL_DECLARED_CHECKS_PASS
```

## Artifact hashes

These hashes are also reported by the canonical artifact where applicable:

```text
cycle49_exact_prefix_certificate.py
  4c06a780b89193689b3ad95bf952a707b9e52a92c87f8dded27e8c1b182956e5

captured closure manifest
  9f52dd36ad5b1a6c93d43c808cc8024ed28d6c6d0ca05678850c3a2e1666e455

cycle49-exact-prefix-certificate.out
  56bf4731608a70de2e3eff87d647a56c74f2681585d0a75dafdc216ddb38f732

bound cycle47_complete_prefix_census.py
  49f128e0e411f03e6d646ddbee5e4b2a13a4da2bc11bc5e6705e356404625928
```
