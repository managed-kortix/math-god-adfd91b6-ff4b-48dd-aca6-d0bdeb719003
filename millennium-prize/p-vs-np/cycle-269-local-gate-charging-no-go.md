# Cycle 269: finite no-go for additive local gate charging

## Question after the shared multiplexer

Work over the fan-in-two basis `B={AND,XOR,NOT}` with constants, counting every
gate. For `t=2^q`, let

\[
 D(f_1,\ldots,f_t)(a,x)=f_a(x),\qquad a\in\{0,1\}^q.             \tag{269.1}
\]

The address restrictions are semantically disjoint components, but an
unrestricted circuit may share gates among them. The Cycle 264 circuit showed
that ordinary circuit size is not additive. This note asks whether a local
allocation of gates could nevertheless certify an additive lower bound.

## A permissive charging model

Fix a circuit `Gamma` for (269.1). A **unit-capacity component charging** is any
collection of nonnegative real numbers

\[
 q_{i,g}\quad (1\le i\le t,\ g\text{ a gate of }\Gamma)
\]

such that

\[
 \sum_{i=1}^t q_{i,g}\le1                                      \tag{269.2}
\]

for every gate. The charge assigned to component `i` is
`Q_i=\sum_g q_{i,g}`. No locality, integrality, computability, or invariance
condition is imposed: the charges may inspect the entire circuit and all its
restrictions. Thus a breaker for this fractional omniscient model also breaks
every genuinely local rule satisfying the same unit gate budget.

For a nonnegative slack `delta`, call such a rule **`delta`-adequate** if it can
always arrange

\[
 Q_i\ge C_B(f_i)-\delta\qquad(1\le i\le t).                    \tag{269.3}
\]

Summing (269.2) and (269.3) gives the necessary inequality

\[
 \sum_{i=1}^t(C_B(f_i)-\delta)\le |\Gamma|.                    \tag{269.4}
\]

This is the entire gate-charging interface: a method that permits a gate to
pay full unit cost independently to several components has already abandoned
additive charging against physical circuit size.

## Finite breaker family

Let `k>=2`, use payload variables `y_1,...,y_k` and distinct data variables
`x_1,...,x_t`, and set

\[
 H_k(y)=\bigwedge_{r=1}^k y_r,\qquad
 f_i(x,y)=H_k(y)\mathbin{XOR}x_i.                              \tag{269.5}
\]

Every `f_i` has `k+1` essential variables. The binary-merge lower bound and an
AND tree followed by one XOR therefore give the exact value

\[
 C_B(f_i)=k.                                                    \tag{269.6}
\]

A binary tree of two-to-one multiplexers computes `x_a` in `3(t-1)` gates,
using

\[
 \operatorname{MUX}(b,u,v)=v\mathbin{XOR}
       (b\mathbin{AND}(u\mathbin{XOR}v)).
\]

Computing `H_k` once and applying one final XOR gives a circuit `Gamma_(k,t)`
for all the addressed components with

\[
 |\Gamma_{k,t}|=(k-1)+3(t-1)+1=k+3t-3.                        \tag{269.7}
\]

Consequently (269.4) would require

\[
 t(k-\delta)\le k+3t-3.                                       \tag{269.8}
\]

This proves the following bounded obstruction.

**Finite additive-slack breaker.** For every fixed `delta>=0`, every power of
two `t>=2`, and every integer

\[
 k>3+\frac{t\delta}{t-1},                                      \tag{269.9}
\]

the explicit finite circuit `Gamma_(k,t)` admits no unit-capacity component
charging satisfying (269.3). In particular:

- exact component calibration (`delta=0`) already fails at `t=2,k=4`, because
  the two components have total exact cost `8` while the shared circuit has
  seven gates;
- the Cycle 264 conservative calibration gives each component only
  `C_B(f_i)-2`; its smallest member in this family is `t=2,k=8`, where required
  charge `12` exceeds the eleven available gate units.

The obstruction is not caused by an unfortunate deterministic assignment of
the shared gates. Even arbitrary fractional and globally optimized charges
cannot meet the budgets.

## Constant-factor version

Suppose instead that a proposed additive potential is unit-capacity and assigns
each addressed component at least `alpha C_B(f_i)`, for a universal constant
`alpha>0`. The same circuit forces

\[
 \alpha\le \frac1t+\frac{3t-3}{tk}.                            \tag{269.10}
\]

Given any `alpha>0`, choose a power of two `t>2/alpha` and then a finite
`k>2(3t-3)/(t\alpha)`. The right side of (269.10) is then smaller than `alpha`.
Hence no positive constant-factor calibration can be additive over all numbers
of address components under a unit gate budget. Each failure has a finite
explicit witness; no asymptotic circuit lower bound is used.

## What remains possible

The theorem rules out local gate accounting that is simultaneously dominated
by physical gate count, additive across all address restrictions, and
calibrated to ordinary component circuit complexity with fixed additive slack
or positive constant factor. It does not rule out:

- a nonadditive measure that explicitly subtracts or quotients a common core;
- a syntactically restricted circuit model in which cross-component sharing is
  forbidden or bounded;
- an anti-sharing gadget with independently proved component-specific
  transformations;
- a measure calibrated to a different property rather than to `C_B(f_i)`.

`P269-LOCAL-CHARGE BREAKER: unit-capacity local gate charging cannot recover an
additive ordinary-complexity measure on disjoint address components; the
explicit family defeats every fixed additive slack and every positive universal
constant-factor calibration.`

This is a bounded structural no-go for one proof interface. It proves no MCSP
lower bound, unrestricted circuit lower bound, or `P != NP` statement.
