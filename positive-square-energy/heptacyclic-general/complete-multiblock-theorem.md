# Heptacyclic multiblock program: exact reduction with one open packet

## Current status and scope

For a connected graph `X`, put

`sigma(X)=s^+(X)-|V(X)|`.

The target statement is:

> If `G` is a finite simple connected graph of cyclomatic rank seven with at
> least two positive-rank cyclic blocks, then `s^+(G)>=|V(G)|`.

The intended scope includes arbitrary legal subdivisions, arbitrary block-cut
incidence, arbitrary bridge connectors, repeated or nested attachment cuts,
and arbitrary finite rooted-tree attachments.  The partition `(7)` is outside
this multiblock program.

**Status: open.**  The exact owner reduction leaves one key, `R31-S`.  Its
finite doubled-`C4` orbit transport and its `C4` subpacket are verified, but the
analytic `D3` subpacket is not.  Therefore this note is not a theorem and makes
no all-multiblock or all-heptacyclic conclusion.

## Block split and ownership contract

Cyclomatic rank is additive over positive-rank blocks, so their ranks form one
of the fifteen integer partitions of seven.  Exactly fourteen have at least
two parts.  If the cyclic hull contains an actual bridge, deleting it gives
two connected induced sides of positive ranks at most six, owned by the
completed lower-rank theorems.  Otherwise all retained incidences are through
shared cuts.

Every packet assigns vertices before charging credit:

1. a shared boundary cut belongs to the upstream territory only;
2. a boundary-open block contributes its cut-deleted downstream side, all path
   remnants there, and all descendants rooted away from the cut;
3. a structural opening takes the opened internal vertex and its complete
   physical owner class;
4. nested demands remain one complete first-boundary territory until an
   explicit later opening; an intermediate cut is never copied; and
5. every rooted tree, connector remnant, and deeper descendant follows its
   unique first physical owner.

## Exact fourteen-partition ledger

The exact DNN sieve is recorded in
`rank-seven-multiblock-debit-ledger.md`.  The bridge-free packet registry is:

| partition | disposition after the exact DNN gate |
|---|---|
| `1^7` | rank-uniform cactus theorem |
| `2+1^5` | `R21` |
| `2+2+1^3` | `R221` |
| `2+2+2+1` | DNN |
| `3+1^4` | `R31-S`, `R31-K` |
| `3+2+1+1` | `R321` |
| `3+2+2` | `R322` |
| `3+3+1` | `R331-S`, `R331-K` |
| `4+1^3` | `R41` |
| `4+2+1` | `R421` |
| `4+3` | `R43` |
| `5+1+1` | `R511-K5e`, `R511-K22`, `R511-K71` |
| `5+2` | `R52-K22`, `R52-K71` |
| `6+1` | `R61-K110-0`, `R61-K110-1`, `R61-K223` |

There are nineteen packet keys.  The two-debit theorem closes

`R331-S, R331-K, R43, R52-K22, R52-K71`.

The nested induced-piece theorem closes

`R21, R221, R31-K, R321, R322, R41, R421, R511-K5e, R511-K71`.

The later exact packets close `R511-K22` and all three `R61` keys.  In
`R31-S`, balanced marked records and the `C4` one-sided records are closed.
The `D3` one-sided records are not.  Hence the authoritative final residual is
exactly

`{R31-S}`.                                                    (1)

## Why `R31-S` is still open

The physical first-simple doubled-`C4` exceptional set consists of eight rows,
one genuine kernel-automorphism orbit, split as four switching-class-`110` and
four switching-class-`111` rows.  Every physical owner, exact symbolic
connector path, cut/open position, path remnant, and decorated rooted
block-cut record is transported recordwise.  The census on every target is

`110 = 54 balanced + 28 C4 + 28 D3`.

Every first non-simple doubled member has one of two exact DNN routes, with
bounds `1862/1000<2` or `1662/1000<2`, so no arbitrary-length orbit is omitted.
This finite transport result is only a prerequisite.

The 28 `D3` records require the uniform inequality

`sigma(Theta(1,2,2)+T^3)>3`.

The old diagnostic checks only the imaginary Sachs activity coefficients.  It
does not prove the claimed real-part implication, control the continuous phase,
or establish the signed Coulson area bound.  That executable therefore exits
nonzero, and no verifier owns `R31-S:D3`.

## Fail-closed audit

From the repository root run

```text
python3 research/heptacyclic-multiblock-master-verifier.py
python3 -O research/heptacyclic-multiblock-master-verifier.py
```

Both invocations authenticate the exact fourteen-partition ledger, run every
closed packet and finite prerequisite in normal and optimized mode, reject
hostile scope/ownership mutations, print `open residual: R31-S`, and exit with
status `1`.  The nonzero exit is intentional.  A passing `COMPLETE` receipt or
an empty residual would contradict (1).
