# Complete all-odd `K5-e` theorem

## Scope

Let the missing edge of `K5-e` be `ab`, and call the other branch vertices
`x,y,z`.  Every one of the nine branch paths is odd and may carry arbitrary
rooted-tree attachments.  A path is unit if its length is one and long
otherwise.  This note gives a complete proof using:

1. the regular-simplex DNN certificate when sufficiently many paths are long;
2. deletion of one of the degree-three branch territories `a,b`, retaining an
   actual complete `K4` packet; and
3. deletion of one of the degree-four branch territories `x,y,z`, retaining a
   favorable `Theta(1,2,2)` subdivision; and
4. sixteen exact rational path-vector certificates for the residual orbits.

No step assigns credit greater than one to an arbitrary attached all-odd `K4`
subdivision.  The `K4` structural branch is used only when the retained six
paths are all unit, so the retained graph is an actual attached `K4`.  The
sixteen residual symmetry types are closed directly by exact DNN witnesses.

Put `sigma(H)=s^+(H)-|V(H)|`.  Every deleted branch territory consists of the
branch vertex, the interiors of its incident paths, and all rooted branches
owned there.  It is a nonempty induced tree and has `sigma=-1`.  Its complement
is induced and connected.  Unit incident paths merely cross the partition and
cause no ownership ambiguity.

## Four or more long paths

Assign the five branch vertices the regular four-simplex Gram matrix, with
off-diagonal correlation `-1/4`.  A unit odd path costs

`(1-1/4)/(1+1/4)=3/5`.

For a long odd path, fixed-parity monotonicity reduces to length three, whose
cost is

`c=3 tan^2(acos(1/4)/6)<1/4`.                         (1)

For an exact check, put `t=cos(acos(1/4)/3)`.  The triple-angle polynomial is
strictly increasing above `1/2`, and its value at `11/13` is
`-253/2197<1/4`; hence `t>11/13`.  The half-angle identity then gives (1).
If `q>=4` paths are long, the total excess is strictly below

`(9-q)3/5+q/4 <= 5(3/5)+4(1/4)=4`.

This proves every state with at least four long paths without a structural
packet and without changing any physical path parity.

## Degree-three territories

Delete the territory of `a`.  The complement is the attached all-odd `K4`
subdivision on `b,x,y,z`; deleting `b` gives the symmetric alternative on
`a,x,y,z`.  Use this channel only when all six retained paths are unit.  The
complement is then an actual attached `K4`, for which the established Sachs
packet gives `sigma>2`.  Therefore

`sigma(G)>2-1>0`.                                           (2)

This is deliberately narrower than claiming `sigma>1` for every attached
all-odd `K4` subdivision.  If a retained `K4` path is long, the general
all-odd `K4` theorem supplies the target but not the extra unit needed to pay
the deleted tree, so this branch of the split stops.

The two degree-three choices are genuinely useful: a state closes whenever
all its nonunit paths are incident with `a`, or whenever all are incident with
`b`.  Choose the endpoint from this physical path placement, then route every
attachment by its unique owner; no cut vertex or rooted branch is assigned to
both sides.

## Degree-four territories

Delete the territory of a center, say `z`.  The complement on `a,b,x,y` is a
theta with three branch paths

`P_xy`, `P_xa+P_ay`, `P_xb+P_by`.

Its two odd cycles have lengths

`l_xy+l_xa+l_ay`, `l_xy+l_xb+l_by`.                         (3)

If both lengths in (3) are `3 mod 4`, the attached favorable-theta packet has
`sigma>1` and pays the one deleted tree strictly.  The same test is made after
deleting `x` and `y`, and the center is chosen according to the physical path
residues.  This is the path-length half of the split; parity alone is
insufficient because all cycles in (3) are odd.

Encode each path, in the order

`ax,ay,az,bx,by,bz,xy,xz,yz`,

by `0` for unit, `1` for long of length `3 mod 4`, and `2` for long of length
`1 mod 4`.  For a proposed center deletion, a cycle in (3) is favorable
exactly when an even number of its three entries equal `1`.  Longer paths of
the same residue do not change this territory decision.

## Exact ledger

There are `3^9=19683` residue/unit states.  Apply the cases in this order:

| disposition | states |
|:---|---:|
| at least four long: regular simplex | `18848` |
| retained actual `K4` after deleting `a` or `b` | `53` |
| favorable theta after deleting `x`, `y`, or `z` | `640` |
| residual | `142` |

The full automorphism group is `S_3 x S_2`: degrees force every automorphism to
preserve the degree-three pair `{a,b}` and the degree-four triple `{x,y,z}`, and
every permutation within those two sets preserves `K5-e`.  Thus the twelve
maps used here are all graph automorphisms, not merely a convenient subgroup.
The 142 residual states form exactly 16 orbits: two with two long paths and
fourteen with three long paths.  Their canonical words are

```text
000001100  001010000
000000111  000001101  000001102  000011001
000012010  001001100  001002100  001010002
001010010  001010020  001011000  001012000
001020100  001120000
```

The first line contains the two-long orbits.  The remaining lines contain the
three-long orbits.  In the displayed order their labeled orbit sizes are

`6,6,1,12,12,6,12,3,6,6,12,12,12,12,12,12`,

which sum to 142.  The standalone audit reconstructs every state, all five
territory tests, the full automorphism action, and the displayed counts:

```text
python3 pentacyclic/research/all-odd-k5e-territory-sieve.py
python3 -O pentacyclic/research/all-odd-k5e-territory-sieve.py
```

## Exact residual certificates

For each displayed canonical word, Table 1 below gives five rational
stereographic branch parameters and one rational parameter for every internal
path vector.  A parameter `t` denotes the unit vector

`u(t)=((1-t^2)/(1+t^2),2t/(1+t^2))`.

For an odd path, its terminal branch vector is negated.  More precisely, for
edge `e_i=pq`, orient it as in the coordinate order above and form

`V_i=(u(t_p),u(q_{i,1}),...,u(q_{i,l_i-1}),-u(t_q))`.       (4)

Empty internal lists are omitted from Table 1.  If `r` is the exact inner
product of two consecutive vectors in (4), that physical edge contributes
`(1-r)/(1+r)`.  Hence the exact representative cost is

`C=sum_i sum_j (1-<V_i[j],V_i[j+1]>)/(1+<V_i[j],V_i[j+1]>).` (5)

Table 2 records the reduced value of (5).  These two tables, the coordinate
order, and (4)--(5) are sufficient to check every entry using rational
arithmetic only.  The verifier performs precisely that calculation with
`Fraction` and rejects antipodal steps.

An entry `1` is realized at length three and an entry `2` at length five.
Fixed-parity path monotonicity therefore covers every longer path of the same
residue; unit entries stay unit.  Exact `S_3 x S_2` transport carries each
representative to every one of the 142 labeled residual states.  The verifier
transports the physical path-vector sequences, including orientation reversal,
and checks that their exact costs are unchanged.

## Exact certificate tables

In Table 1, `b=(t_a,t_b,t_x,t_y,t_z)`, and `i:[...]` lists the internal
parameters on `e_i`; every unlisted path has no internal parameter.

| state | branch tuple `b` | nonempty internal tuples |
|:---|:---|:---|
| `000001100` | `(0,17/64,-55/32,-193/64,43/32)` | `5:[-3/64,-23/64]; 6:[-43/64,-9/64]` |
| `001010000` | `(0,-47/64,203/64,-13/8,27/64)` | `2:[-13/32,-63/64]; 4:[-15/64,5/32]` |
| `000000111` | `(0,1/64,-535/8,-169/64,175/64)` | `6:[155/64,31/32]; 7:[-145/64,-15/16]; 8:[-21/16,-47/64]` |
| `000001101` | `(0,3/16,-55/32,-631/32,53/32)` | `5:[-1/16,-5/16]; 6:[-13/16,-21/64]; 8:[-81/32,-19/16]` |
| `000001102` | `(0,-11/64,113/64,-11333/32,-111/64)` | `5:[1/16,19/64]; 6:[27/32,3/8]; 8:[19/4,9/4,11/8,29/32]` |
| `000011001` | `(0,-17/64,87/64,-27/16,-207/64)` | `4:[0,9/32]; 5:[-5/64,7/64]; 8:[-43/64,-9/64]` |
| `000012010` | `(0,1/8,-209/64,21/16,-25/16)` | `4:[-9/64,-27/64]; 5:[7/32,5/16,13/32,33/64]; 7:[117/16,25/16]` |
| `001001100` | `(0,-1/64,1299/64,95/32,-9/16)` | `2:[23/64,27/32]; 5:[23/64,27/32]; 6:[-159/64,-15/16]` |
| `001002100` | `(0,3/32,-89/32,-345/16,33/64)` | `2:[-25/64,-57/64]; 5:[-5/32,-13/32,-23/32,-37/32]; 6:[-33/32,-25/64]` |
| `001010002` | `(0,1/16,-97/64,111/64,81/32)` | `2:[-1/8,-1/4]; 4:[-9/64,-11/32]; 8:[61/64,33/64,13/64,-3/32]` |
| `001010010` | `(0,31/64,-143/64,13/8,-31/32)` | `2:[9/32,19/32]; 4:[7/64,-7/32]; 7:[-42,41/16]` |
| `001010020` | `(0,29/64,-65/32,105/64,-71/64)` | `2:[1/4,17/32]; 4:[3/32,-15/64]; 7:[-5,129/8,3,49/32]` |
| `001011000` | `(0,-21/64,207/64,-101/64,11/32)` | `2:[-7/16,-69/64]; 4:[-1/64,9/32]; 5:[-23/32,-43/32]` |
| `001012000` | `(0,-1/4,203/64,-51/32,5/16)` | `2:[-29/64,-9/8]; 4:[1/32,19/64]; 5:[-31/64,-49/64,-37/32,-57/32]` |
| `001020100` | `(0,-35/64,71/4,-41/16,39/64)` | `2:[-23/64,-13/16]; 4:[-11/32,-5/32,1/64,13/64]; 6:[137/64,15/16]` |
| `001120000` | `(0,185/64,-177/64,93/64,-9/32)` | `2:[15/32,19/16]; 3:[11/8,3/4]; 4:[875/64,-337/64,-133/64,-75/64]` |

Table 2 gives the exact reduced costs; direct cross multiplication against
four proves every listed cost is strictly smaller than four.

| state | exact cost `C` |
|:---|:---|
| `000001100` | `23472183923982717639326831241647200327224528275292033452281/8511208227790834691864387837434169366308062016574069145600` |
| `001010000` | `91694087850909569249273914290465293179299498749158306369/26371331672194971750153524081392156985140748092047360000` |
| `000000111` | `62694914347913116722118720137562286883073177863378932966640416807538914437/32720125916489253322998683947243937414666417599673374547377490128558080000` |
| `000001101` | `232079307983422616226559548158400876042893821108452547170585596809/109798808112362682332054714026977315281882699220609318305025638400` |
| `000001102` | `356758661060340351573502366523759532133812469701951425830919518119620094300289829678551/182403620499638430223501170592507284068193703868745878964418759272486432561338567884800` |
| `000011001` | `287944224617281459997884340666480112326274402334033/99958999868452289805902811998185624544771563585536` |
| `000012010` | `637362473898456537184685641324184578630555443827725356281604855128049223601/240200920089903321099186420093997323623427877998372898390291071355981248000` |
| `001001100` | `42968157038092484935130368228748087892546330682553153030049209/21832585978950251217292179451785759763652507753285305344000000` |
| `001002100` | `7804352996274066073451789009750491598691663999261396006954079490832347/4409073777429933762512251573338773228207447608063420512692995200000000` |
| `001010002` | `37246488361337989476525453401684355872630871045605536262807006299/14038674045229769992936360189009886359359575189534261134413004800` |
| `001010010` | `294094663942144495812847244115333601964898733468180728221/125655081766557946201631063911124981579426538608034201600` |
| `001010020` | `459507478530004489397938536485216112206770539760661/220341593771940622415949641053266388802082570240000` |
| `001011000` | `18991480914772977113792787249057881973143945833934720093/6395109859518696503707487810752371377846993054842257408` |
| `001012000` | `975235031283773924629175653083602237793251090644400713035691609/345274890771839450248696870770388303746144640822940480975769600` |
| `001020100` | `23077759220216082094346734097075437598272171597402163655415850218128587942579/10322350225488594349027523953314961532245513793852584795899633553020450250752` |
| `001120000` | `3721746395652148087515055329353407891359125595773145804545073003323302715521/1231529049560151419371448763155089696427501140982076915709861695030988898304` |

## Theorem

Let `G` be obtained by attaching arbitrary rooted trees to a simple all-odd
subdivision `B` of `K5-e`.  Then one of the following holds:

1. the residue state lies in the simplex or residual-certificate class, and a
   DNN certificate gives `kappa(B)<=|E(B)|+4`; or
2. the state lies in the actual-`K4` or favorable-theta class, and the induced
   territory split proves `s^+(G)>=|V(G)|` directly.

In either case `s^+(G)>=|V(G)|`.  No universal bound
`kappa(B)<=|E(B)|+4` is asserted: it is false, already at the unsubdivided
all-odd `K5-e`, whose optimized excess is `2sqrt(7)-1>4`.

Indeed, the 19,683 unit/residue states split disjointly into 18,848 simplex
states, 53 actual-`K4` structural states, 640 favorable-theta structural states,
and 142 states covered by the sixteen rational certificates.  In the DNN
branch, tree additivity and `s^-(G)<=kappa(G)` give the spectral conclusion; in
the structural branch, (2) or its favorable-theta analogue gives it without a
DNN claim.  The all-unit state lies in the actual-`K4` branch, so the structural
endpoint case is explicit.

## Fail-closed artifacts

The deterministic certificate fixture is
`pentacyclic/research/all-odd-k5e-theorem.json`, with SHA-256

`35523cc3be872181e2f343a7e21936f82b14e4a6968896fc2dcfd5f545da1ee1`.

Run both interpreter modes:

```text
python3 pentacyclic/research/all-odd-k5e-theorem-verifier.py
python3 -O pentacyclic/research/all-odd-k5e-theorem-verifier.py
```

The verifier locks the territory-sieve source and fixture bytes, regenerates
the fixture from the sixteen embedded deterministic records, reruns the full
19,683-state ledger, checks exact physical costs and every automorphism
transport, and requires seven hostile mutations to fail by explicit exception.
Acceptance uses neither `assert`, floating point, numerical tolerance, nor an
unchecked result table.
