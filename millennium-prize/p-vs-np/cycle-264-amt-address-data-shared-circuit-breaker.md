# Cycle 264: frozen AMT address/data gadget and shared-circuit breaker

## Frozen finite gadget

Work over the fan-in-two basis `B={AND,XOR,NOT}` with constants and count every
gate. Freeze two address slices (`t=2`), one address bit `a`, data bits `x_1,x_2`,
and payload bits `y_1,...,y_8`. Put

\[
 H(y)=\bigwedge_{r=1}^8 y_r,
 \qquad f_i(x,y)=H(y)\mathbin{XOR}x_i,
\]

and freeze the literal address/data multiplexer

\[
 D(a,x,y)=f_{1+a}(x,y)
          =H(y)\mathbin{XOR}
            \bigl(x_1\mathbin{XOR}
              (a\mathbin{AND}(x_1\mathbin{XOR}x_2))\bigr).       \tag{264.1}
\]

There is no truth-table coordinate carrying a separate choice of which
component-complexity test is to be applied: the only address is an ordinary
input of the completed Boolean function. This is the smallest power-of-two
instance of the Cycle 208 disjoint-slice address/data proposal with enough
payload variables to make its conservative additive lower bound fail by a
whole gate.

## Exact component costs

Any circuit whose output depends essentially on `k` distinct inputs has at
least `k-1` binary gates. Indeed, in the subgraph consisting of paths from
those inputs to the output, unary gates never merge source components and each
binary gate can reduce their number by at most one. Thus at least `k-1` binary
merges are necessary.

The function `H` depends essentially on all eight `y` inputs and a binary AND
tree uses seven gates, so

\[
 C_B(H)=7.                                                       \tag{264.2}
\]

Each `f_i` depends essentially on the eight payload inputs and on `x_i`.
The same merge bound gives eight gates, and an AND tree followed by one XOR
attains it. Hence

\[
 C_B(f_1)=C_B(f_2)=8.                                          \tag{264.3}
\]

In particular, even the deliberately weakened component accounting used in
Cycle 208 gives

\[
 \sum_{i=1}^2(C_B(H)-1)=2(7-1)=12.                             \tag{264.4}
\]

## Shared circuit

Equation (264.1) is an explicit eleven-gate circuit: seven AND gates compute
`H`, three gates compute

\[
 x_1\mathbin{XOR}(a\mathbin{AND}(x_1\mathbin{XOR}x_2)),
\]

and one final XOR combines the results. Therefore

\[
 C_B(D)\le 11<12=\sum_{i=1}^2(C_B(H)-1).                       \tag{264.5}
\]

The strict inequality is already a one-gate contradiction to the conservative
direct-sum lower bound. Against the exact component sum, the same circuit saves
at least five gates:

\[
 C_B(D)\le11<16=C_B(f_1)+C_B(f_2).                             \tag{264.6}
\]

The circuit computes the seven-gate payload core once and shares it across
both address values. Restricting `a` recovers each component and therefore
certifies only `C_B(D)>=8`; it cannot certify either additive lower bound.

This is also a witness against rigidity quantified over every unqueried
component choice: such a statement must hold at the explicit admissible pair
`(f_1,f_2)`, where its claimed additive value is at least `12` but the displayed
circuit has size `11`. Consequently no maximization used to account for the
unqueried component can establish a uniform direct-sum claim for this gadget;
the pointwise claim already fails at one member of the maximization domain.

## Stop decision

`P264-AMT-GADGET SHARED-CIRCUIT BREAKER: the frozen two-slice address/data
gadget violates its conservative additive lower bound by one gate (11 < 12),
and violates exact component additivity by five gates (11 < 16).`

The breaker retires this literal multiplexer/direct-sum implementation. It does
not refute the abstract `AMT(n,s,m)` template or every possible anti-sharing
gadget, and it proves no MCSP lower bound, unrestricted circuit lower bound, or
`P != NP` statement.
