# Bounded-demand separator with `TP`, `PP`, and `TPP` terminals: next obstruction

**Date:** 2026-07-26

## 1. Verdict

Adding the proved connected `TP`, `PP`, and `TPP` packets to the terminal list
repairs the rank-one counterexample `P-x-T-y-P`, but it still does not make the
rank-uniform separator assertion true for the labelled router operation of
Theorem 3.1 in
`research/rank-uniform-triangular-router-interface-theorem-2026-07-26.md`.

The next obstruction has two triangles and two pentagon interfaces. Its
triangular incidence tree and marks are

```text
T_0 - x - T_1,

             a:A
            /
       x -- T_0
            \
             b:B
```

where `a` and `b` are the two distinct private vertices of `T_0`, and `A,B`
are labelled interfaces whose remote cyclic blocks are pentagons `P_A,P_B`.
The third vertex of `T_0` is the common cut `x`; `T_1` is the other triangle
at `x`. Arbitrary connector remnants and off-hull trees may be present and do
not change the ownership argument.

Under the established distinct-owner router transition there are only two
router sequences: do nothing, or split `T_0`. The first leaves a `TTPP`
territory, which is not one of the added terminals. The second is forced to
leave the retained cyclic packet, private-interface trees, and remote packets

```text
T, E_A, P_A, E_B, P_B.
```

Each `E_i` is the private interval and connector remnant charged by Theorem
3.1(5), while `P_i` is charged separately. Its state is
`(p,e,c,t)=(2,2,0,1)`. It is not accepted: the strict triangular
flag cannot pay either fixed pentagonal deficit, and the two pentagons are not
a single `PP` territory. Thus the terminal amendment alone is false.

This obstruction is minimal in positive triangular rank. Rank one is exactly
a `TP`, `PP`, or `TPP` base according to the number and ownership of the
pentagonal demands; in the two-demand case relevant here, the unsplit packet is
`TPP`. Hence rank two is the first rank at which an extra triangle can be
locked through the cut owned by the demanded triangle.

## 2. Precise corrected candidate being tested

Call a **standard labelled router step** the operation in Theorem 3.1: at a
triangle with two or three distinct occupied ports, partition its vertices
into the same number of nonempty proper consecutive intervals, one interval
and one resulting territory for each occupied port. Interfaces coinciding at
one port remain together, but interfaces at distinct ports have distinct
owners. The router triangle is not retained.

The natural terminal amendment of Candidate Lemma S is:

> Repeated standard labelled router steps produce an accepting ledger state,
> a nonnegative `PP` territory plus a strict triangular territory, or a proved
> locked packet, where the locked list now explicitly includes connected
> `TP`, `PP`, and `TPP` packets.

Here `TP`, `PP`, and `TPP` refer to the complete cyclic profile of the
territory; arbitrary trees and connector remnants attached inside that
territory are allowed. A larger `T^rPP` territory is not silently renamed
`TPP`.

The last qualification is necessary. Otherwise every finite example could be
declared a bounded-rank terminal and the assertion would have no inductive
content.

## 3. Exhaustion of the rank-two obstruction

Let `I` have cycle nodes `T_0,T_1`, one cut node `x`, and incidence edges
`T_0x,T_1x`. Put the two labelled marks at distinct private ports `a,b` of
`T_0`.

### Lemma 3.1

`T_1` is never a standard labelled router.

**Proof.** Its active territory has only the incidence port `x`. It has no
labelled private port. Thus it has one occupied port, whereas Theorem 3.1
requires two or three. QED.

### Lemma 3.2

If `T_0` is split, the split and all cyclic owners are forced.

**Proof.** Its three occupied ports are `x,a,b`. A triangle has exactly three
vertices, so the only partition into three nonempty proper consecutive
intervals is the three-singleton partition. The `x` singleton owns the entire
incidence branch containing `T_1`; the `a` and `b` singletons own the connector
remnants leading to `P_A` and `P_B`, respectively. Distinct ports have distinct
owners by the definition of a standard step. Therefore the retained cyclic
packet is `T`; the other local territories are the naked trees `E_A,E_B`, and
the remote packets are `P_A,P_B`. QED.

### Theorem 3.3 (next minimal obstruction)

The marked rank-two object above has no successful standard router sequence
under the amended `TP`/`PP`/`TPP` terminal list.

**Proof.** An empty sequence retains both triangles and both demanded
pentagons, so its cyclic profile is `TTPP`, not `TP`, `PP`, or `TPP`.

For a nonempty sequence, Lemma 3.1 says that the first router must be `T_0`.
Lemma 3.2 gives `T,E_A,P_A,E_B,P_B`. No resulting territory has a router:
the first has one triangle and no demand mark, while each other territory has
no triangle. Thus the sequence ends. The two pentagons have distinct owners,
so there is no `PP` terminal. There is no mixed terminal because no retained
triangle shares an owner with a pentagon.

The ledger has two separately charged pentagonal deficits, two naked interface
trees, no integer triangular credit, and one merely strict triangular packet:

```text
(p,e,c,t)=(2,2,0,1).
```

Theorem 4.1 does not accept this state. In particular, qualitative strictness
has no uniform positive margin and cannot pay `2 delta`. This exhausts all
sequences.

For minimality, triangular rank zero is outside the router assertion. At rank
one the same two distinct private demands and the triangle form the proved
connected `TPP` terminal before any split. Therefore no lower positive rank
can exhibit this failure. QED.

## 4. Why `PP` does not already repair it

There is a tempting nonstandard partition: give the edge `ab` to one territory
and the vertex `x` to the other. The `ab` territory, both connector remnants,
and both remote pentagons form one induced `PP` territory; the `x` territory
owns `T_1` and is strict triangular.
Analytically this is perfect:

```text
sigma(PP territory) >= 0,
sigma(T_1 territory) > 0.
```

But this is not a transition of Theorem 3.1. It coalesces two distinct labelled
ports into one owner, while the theorem assigns one territory to each port.
Consequently it cannot be used as though it were already covered by the proved
local router theorem.

This observation identifies the exact correction needed locally.

## 5. Required new transition

A viable all-rank theorem must add a **demand-coalescing triangle transition**:

* if two demanded private ports of a triangle are adjacent, their connecting
  edge may be one interval and one owner;
* the remaining vertex may own one incidence branch;
* the first territory is certified as a `PP` terminal after its two remote
  pentagons and connector remnants are included;
* the second territory contains the entire incidence branch and all trees
  rooted there.

For the obstruction this gives `PP+T`, hence strict positivity. The transition
is graph-theoretically sound in this local configuration: `{a,b}` and `{x}`
are disjoint proper consecutive intervals, every connector follows its marked
endpoint, and the incidence branch follows `x`. Both territories are connected,
induced, disjoint, and exhaustive.

It is nevertheless a genuinely new automaton transition. Before using it in an
arbitrary-rank induction one must prove its owner rule when additional active
branches and earlier nested splits are present, and enlarge the finite state to
remember a paired-demand owner. The old state `(p,e,c,t)` does not distinguish
two separate pentagons from one certified `PP` territory unless that fact is
encoded in `t` by an external convention.

A sufficient finite extension is

```text
(p,e,c,t,q),
q in {0,1},
```

where `q=1` means that the two demands have been coalesced into one certified
nonnegative `PP` territory. This gives at most `144` arithmetic states. Its
acceptance rule includes `q=t=1`, while all old rules remain unchanged. This
state extension is finite and rank-independent, but no global claim is made
here that every marked incidence tree reaches an accepting state.

## 6. Rigorous status

```text
original Candidate Lemma S: false at rank one;
adding TP/PP/TPP terminals only: false at rank two;
next minimal obstruction: two triangles at one cut, with two distinct
  private pentagon interfaces on the same triangle;
missing local operation: coalescence of two demanded ports into one PP owner;
all-rank theorem after adding that operation: open.
```

The exact finite transition exhaustion is reproduced by
`research/bounded-demand-separator-next-obstruction.py`.
