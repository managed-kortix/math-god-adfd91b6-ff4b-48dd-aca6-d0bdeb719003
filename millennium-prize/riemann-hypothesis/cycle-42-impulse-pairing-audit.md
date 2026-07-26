# Cycle 42: exact impulse pairs and hostile pairing audit

## Scope and conclusion

Let

\[
 H_q-H_{q-1}=-d_q+J_q,
 \qquad d_q:=\Delta C_q\|U_{q-1}\|^2>0,
\tag{42.1}
\]

with the Cycle 41 definitions. This note tests whether every `mu(q)=+1`
impulse can be paired deterministically with a subsequent `mu(r)=-1` impulse
so as to prove weighted `H` recovery.

The proposed least-prime-factor map `q -> 2q/p`, where `p` is the least prime
factor of `q`, is falsified algebraically: on its stated domain it preserves
`mu=+1` and never produces a subsequent `mu=-1` event. A chronological LIFO
pairing reproduces the five visible finite trigger/compensator pairs and their
paired impulse sums are positive. It nevertheless has 43 negative pair sums
among 66 pairs through 240. More fundamentally, positivity of `J_q+J_r` alone
does not imply weighted recovery: all radial drifts, intervening impulses, the
incoming level, and the decreasing recovery weight remain in the exact formula.

Thus bare sign pairing is falsified as a sufficient deterministic lemma. A
valid replacement must prove a complete weighted packet inequality, not merely
match Mobius signs.

## 1. Exact two-impulse formula

Put

\[
 A_t:=L_t\langle D_{t-1},\rho_t\rangle
       -C_t\langle U_{t-1},\rho_t\rangle,
 \qquad
 E_t:=L_t(L_{t+1}-L_t)G_{t,t}>0.
\tag{42.2}
\]

At a squarefree event,

\[
 \boxed{J_t=2\mu(t)A_t-E_t.}
\tag{42.3}
\]

Therefore, for `q<r`, `mu(q)=+1`, and `mu(r)=-1`,

\[
 \boxed{J_q+J_r=2(A_q-A_r)-E_q-E_r.}
\tag{42.4}
\]

This short formula is exact but does not display the dependence of the second
correlation on the first event and on all intervening events. To open it, define
the vectors immediately before `q`,

\[
 U^-:=U_{q-1},\qquad D^-:=D_{q-1},
\]

and the intervening increment

\[
 Z_{q,r}:=\sum_{q<s<r}\mu(s)\rho_s,
 \qquad
 Y_{q,r}:=\sum_{q<s<r}\mu(s)L_s\rho_s.
\tag{42.5}
\]

Then

\[
 U_{r-1}=U^-+\rho_q+Z_{q,r},
 \qquad D_{r-1}=D^-+L_q\rho_q+Y_{q,r},
\]

and hence

\[
\boxed{\begin{aligned}
J_q+J_r={}&2\big[L_q\langle D^-,\rho_q\rangle
                    -C_q\langle U^-,\rho_q\rangle\big]\\
&-2\big[L_r\langle D^-,\rho_r\rangle
                    -C_r\langle U^-,\rho_r\rangle\big]\\
&-2(L_rL_q-C_r)G_{q,r}\\
&-2\sum_{q<s<r}\mu(s)(L_rL_s-C_r)G_{s,r}\\
&-E_q-E_r.
\end{aligned}}
\tag{42.6}
\]

No term in (42.6) has a sign determined solely by `mu(q)=+1` and `mu(r)=-1`.
In particular, opposite Mobius signs reverse the two linear contractions, but
they do not make the complete pair nonnegative.

## 2. Exact pair interval and weighted recovery formulas

Summing the recurrence through the second event gives

\[
\boxed{
 H_r-H_{q-1}=J_q+J_r
 +\sum_{q<s<r}J_s
 -\sum_{t=q}^{r}d_t.}
\tag{42.7}
\]

Even if there are no intervening squarefree events, a positive impulse pair
must pay the strictly positive drift `sum d_t`. If intervening events exist,
their complete impulses cannot be discarded.

The exact half-strength recovery criterion uses

\[
 \beta_n={\log(1+1/n)\over L_nL_{n+1}^2}>0,
 \qquad
 \mathcal R(a,b)=\sum_{a\le n<b}\beta_nH_n.
\tag{42.8}
\]

Writing `X_t=J_t-d_t` and

\[
 B_t^{(b)}:=\sum_{n=t}^{b-1}\beta_n,
\]

substitution of `H_n=H_{a-1}+sum_(a<=t<=n)X_t` gives the exact triangular
formula

\[
\boxed{
 \mathcal R(a,b)
 =H_{a-1}B_a^{(b)}
  +\sum_{t=a}^{b-1}B_t^{(b)}(J_t-d_t).}
\tag{42.9}
\]

Consequently a proposed pair `(q,r)` contributes `B_q^(b)J_q+B_r^(b)J_r`,
not a common multiple of `J_q+J_r`. Since `q<r` implies
`B_q^(b)>B_r^(b)`, the earlier impulse receives the larger coefficient. For
the observed pattern `J_q<0<J_r`, this weighting is adverse. Formula (42.9)
also retains every drift with a negative sign and the incoming level
`H_(a-1)`. A theorem based only on nonnegative unweighted pair sums therefore
cannot imply recovery.

A sufficient paired lemma would instead have to partition all events and prove
the complete inequality

\[
 H_{a-1}B_a^{(b)}
 +\sum_{(q,r)}\big(B_q^{(b)}J_q+B_r^{(b)}J_r\big)
 +\sum_{t\ \mathrm{unpaired}}B_t^{(b)}J_t
 \ge \sum_{t=a}^{b-1}B_t^{(b)}d_t.
\tag{42.10}
\]

This is a weighted packet estimate of essentially the same strength as the
Cycle 41 band-recovery target; sign matching alone does not establish it.

## 3. Least-prime-factor map is not the requested pairing

Let `q` be squarefree with `mu(q)=+1`, so `omega(q)` is even, and let `p` be
its least prime factor. Set `T(q)=2q/p`.

- If `p=2`, then `T(q)=q`.
- If `p>2`, then `2` does not divide `q`; `T(q)` replaces the prime factor `p`
  by `2`. It is squarefree, has the same number of prime factors, and therefore
  `mu(T(q))=mu(q)=+1`.
- In the second case `T(q)<q`; in the first case it is fixed. Thus it is never
  a subsequent event with Mobius sign `-1`.
- Applying `T` to an odd `q` gives an even fixed point, so `T(T(q))=T(q)`, not
  `q`. The map is idempotent after one step, not an involution on this domain.

For the five certified negative-band triggers,

\[
 39\mapsto26,\quad95\mapsto38,\quad219\mapsto146,
 \quad221\mapsto34,\quad226\mapsto226,
\]

and every image again has `mu=+1`. This is a complete algebraic falsification,
not merely a finite counterexample.

## 4. Certified examples and hostile audit

A natural local rule pairs each `mu=-1` event with the most recent unpaired
`mu=+1` event (chronological LIFO). The complete restricted Vasyunin Gram
certificate at 192 bits gives:

| pair `(q,r)` | certified `J_q+J_r` | sign |
|---|---:|:---:|
| `(39,41)` | `[0.0150301366736463551 +/- 1.66e-20]` | `+` |
| `(95,97)` | `[0.0113811936621851588 +/- 3.00e-20]` | `+` |
| `(221,222)` | `[0.00249050867885788948 +/- 3.94e-21]` | `+` |
| `(219,223)` | `[0.00836103117102805176 +/- 2.03e-21]` | `+` |
| `(226,227)` | `[0.00241411992506519424 +/- 1.65e-21]` | `+` |

These explain the visible local compensation but do not prove a rule. In the
same deterministic LIFO audit through 240, 43 of 66 paired sums are strictly
negative and seven positive-sign events remain unmatched at the cutoff.
Representative certified hostile pairs are

| pair `(q,r)` | certified `J_q+J_r` |
|---|---:|
| `(14,19)` | `[-0.0839846942794921003 +/- 3.80e-20]` |
| `(26,29)` | `[-0.00803976685026945108 +/- 5.5e-23]` |
| `(21,30)` | `[-0.142793944744975515 +/- 2.16e-19]` |
| `(35,37)` | `[-0.00422933261141368889 +/- 3.63e-21]` |
| `(38,42)` | `[-0.00185639805183729232 +/- 3.98e-21]` |
| `(46,47)` | `[-0.00725718548182874128 +/- 1.47e-21]` |

The hostile examples falsify nonnegativity for the strongest obvious local
chronological rule. FIFO pairing is no remedy: for example it pairs `(39,47)`
and `(95,107)`, whose certified sums are respectively about `-0.09769` and
`-0.01416`. Nor does a future existence matching by sign settle the issue:
such a matching still needs quantitative bounds on pair distance, complete
Gram correlations, intervening events, radial drift, and beta distortion.

## 5. Reproduction

Run the audit and focused tests with

```text
uv run --with python-flint python cycle42_impulse_pairing_audit.py \
  --max-n 240 --bits 192
uv run --with python-flint python -m unittest -v \
  test_cycle42_impulse_pairing_audit.py test_cycle41_h_event_analysis.py
```

The tests verify (42.6) against direct complete-Gram impulses for every FIFO
and LIFO pair through 240, certify the least-prime map's sign and direction on
the five band triggers, and fix the stated LIFO trigger pairs. These are finite
certificates plus an exact algebraic obstruction; they are not an asymptotic
Mobius theorem and make no RH claim.
