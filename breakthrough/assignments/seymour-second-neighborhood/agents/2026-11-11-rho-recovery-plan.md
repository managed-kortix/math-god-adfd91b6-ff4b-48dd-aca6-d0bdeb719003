# Recovery plan for the 18 missing `m=8`, `rho=0..3` aggregate LRATs — 2026-11-11

## Scope and audit verdict

This is a bounded recovery audit in the frozen Seymour breakthrough lane. It is
**not** a closure statement for `m=8`, order 18, or Seymour's conjecture.

### Exact repository anchor

The report working tree was rebased neither by inference nor by a synthetic
cherry-pick. Before the final audit pass, the 33,389-byte thin bundle
`afcdda7-bridge-from-cc61b3dc-and-964faf4.bundle` was checked against SHA-256
`0835be28580603442eecea387052a397174b4c64e1cbe2b5abccc8c6d3bf119a`,
then verified by `git bundle verify`. It advertises
`afcdda76ac926e74a194eb594840c5f7003e7449`, whose tree is
`be5a2ee57d4ff9aaed8d191640bcad0202bc1b0f` and whose two parents are
`022eed95029f2c5aa5b9bfd998cd0f42337bc719` and
`cc61b3dc4d46a0330253bac31c0d598421850864`. This report is the sole working-
tree addition above that exact merged snapshot. The anchor records provenance;
it does not approve a merge, lane-state change, or closure claim.

The September source tip is
`cc61b3dc4d46a0330253bac31c0d598421850864` on
`origin/45a63659-bb8c-4524-86d8-c52dde0362b5`. The three rho certificate
reports and their deterministic emitters survive there, but none of the 18 CNFs
or LRATs was committed. The repository-wide artifact forensics found no one of
the 36 frozen CNF/LRAT SHA-256 identities as a raw Git blob or as an XZ-decoded
Git blob. Therefore historical object recovery from the present Git database is
not available; the bounded paths are deterministic regeneration, explicit
replacement certificates, or rigorous human proofs for particular shards.

The exact missing matrix is `3+4+5+6=18` rows:

- `rho=3`, `k=0..2` (`e=2` residual holes);
- `rho=2`, `k=0..3` (`e=3`);
- `rho=1`, `k=0..4` (`e=4`);
- `rho=0`, `k=0..5` (`e=5`).

Here `k` is the exact number of residual missing pairs inside
`T={0,...,15}`; the other `e-k` residual holes lie between `B` and `C`.
Each formula has 30,981 variables and 171,942--171,944 clauses. Together the
rows partition only the rooted order-18, eight-hole, vertex-minimal then
arc-minimal normal form encoded by `snc_cnf.py`.

A bounded local audit regenerated all 18 CNFs byte-exactly, ran the complete
small-order semantic mutation suite, and regenerated/checker-verified eight
representative LRATs. All eight representative LRATs equal their old reported
SHA-256 identities. This is strong toolchain evidence, not recovery of the ten
unregenerated rows and not permission to infer them without proof bytes.

## Frozen producer and checker provenance

Use source bytes from the September tip, not the stale checked-out branch:

| file | Git blob at `cc61b3dc...` | bytes | SHA-256 of bytes |
|---|---|---:|---|
| `snc_cnf.py` | `170cddb7075aa4cbd6e288949110deb762da23b8` | 7,969 | `adab04953d3697ec004e28ad145dda5b0f04d07ee8dd20d95655f6e32877d68e` |
| `rho3_shards.py` | `6f38e51805212d822d9dc6ccefd82c01602cfc79` | 1,229 | `8be3d17370f0cbb708bf48364f8e3e3fadf6a50f6a20aa566a4aa3913fd03846` |
| `rho2_shards.py` | `dc03b32b3331a5f10de1f14116b425ef21a52ae9` | 1,220 | `91e9500ef36a83d295d9f1b02f6380a84d3e9b8c0f40faf17237ea75bc52111d` |
| `rho_low_shards.py` | `155cc47fcec3129145dd3e72bd45b793d4c1f1d6` | 1,375 | `fbb074b447fd63a5da190f82f9ae75ca66c83ef6266618ce9ab65db3e75ead7e` |
| `test_cnf_semantics.py` | `3259132e526542be1d2769c7c778343c2cb1e68c` | 9,376 | `46ae5f7bb6c0d5c61d84f037617b1efc53680fadf1ffc6c4513cbc8aedc626af` |

The reports were introduced by commits `34f8a4a2...` (rho 3), `4797faac...`
(rho 2), and `9d3bdce...` (rho 0/1). Their surviving metadata freezes only
"CaDiCaL 1.7.3, `--lrat --no-binary`, pinned `lrat-check`". It does **not**
freeze the historical rho solver binary, compiler, build date, environment,
seed, restart/phase controls, LRAT byte lengths, compressor, or run timings.
Those omissions matter for historical identity.

The bounded replay used:

```text
CaDiCaL version/source  1.7.3 / 38e073b389a877b0a0d3c91136d2443ab95fdeba
local binary            1,002,216 bytes
local binary SHA-256    ba21819a2496c321abf044e5adb67601c4c7b70d049e9e052414ef0f73876b14
local ELF build ID      2a06e2bee2fe5e3e8d590ed8021bb60471618de5
compiler/options        g++ 13.3.0 / -Wall -Wextra -O3 -DNDEBUG
lrat-check source       2e3b2dc0ecf938addbd779d42877b6ed69d9a985
lrat-check binary       22,064 bytes
checker SHA-256         e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8
checker ELF build ID    7a498bdc75d1b089388abb7f8629bb3aec38526e
Python / XZ             3.12.13 / 5.4.5
host                    Linux 6.8.0-88-generic x86_64, 2 vCPU, about 4 GB RAM
```

The solver binary hash is build-dependent. A companion session recorded a
canary with another build of the same source: 1,002,216 bytes, SHA-256
`73328ec7c7ab7b2b3a03708f9e6983daf07b2af3adca5825f016b1c26dc28571`,
not the later B7 ledger's historical
`108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292`.
Its exact producer/checker/compressor commands were:

```sh
"$CADICAL" --lrat --no-binary -q --restart=false --phase=false --seed=3 \
  leaf-488.cnf leaf-488.lrat
"$LRAT_CHECK" leaf-488.cnf leaf-488.lrat
xz -3 -c leaf-488.lrat > leaf-488.lrat.xz
```

The recorded identities were CNF 10,707,683 bytes,
`73aec08bea37b86d396310d0db0dc292913632f824d79ce1a4e56ff5b6f7cae5`;
LRAT 49,446,991 bytes,
`0eb73d1141da0e3a8c0b1722023742dd0d58fd72a930572a7c4f481aabc530fc`;
and XZ 9,097,380 bytes,
`cea716c418dfca593141549d5e0a282e2d3a6c7f9c0916538a46239d228d2f06`.
Those equal the frozen B7 leaf-488 ledger, and checker
`e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8`
returned `c VERIFIED`. This canary was recorded in the companion session, not
rerun in this rho sandbox. It supports the frozen-source build as a practical
rho producer, but it does not turn `73328e...`, `ba218...`, or B7's
`108d10...` into the undocumented historical rho binary.

## Exact 18-row identity ledger

`CNF bytes` below were measured by fresh deterministic regeneration and match
the frozen hashes. `Old LRAT SHA-256` is the reported historical identity. An
LRAT byte count appears only where this audit actually regenerated that proof;
the three old descriptions "23, 226, 517 MB" were rounded prose, not a complete
size ledger.

| rho | k | clauses | CNF bytes | CNF SHA-256 | old LRAT SHA-256 | measured LRAT bytes / present status |
|---:|---:|---:|---:|---|---|---|
| 3 | 0 | 171,943 | 11,158,389 | `2a232c2478c3c609241ed2d2c47b755127d95100ac57e39acee2a4a8e7339a5f` | `4d0c419d993ab28fffb9bba622977e85bb27916838a67aae7ce96776ca2497ef` | 23,574,012; regenerated exact, VERIFIED |
| 3 | 1 | 171,944 | 11,158,397 | `329489edf5c75fd194a171d8b60341ac587720f838cb189d4cb85cf0172c4202` | `e8109fe5adfcf81a558e973dfd6b5d7182ebf736f78fea4bd6c191c9cee14620` | 236,514,931; regenerated exact, VERIFIED |
| 3 | 2 | 171,944 | 11,158,397 | `55e88baba98fb79dc22562fa7e0205e8d0b33600aa1c7574fdc7236875cdfe31` | `060c19a3b412550d4cebcff78280c5e3e00c92a32fac7aa79e52af2d9d2b335a` | 541,652,957; regenerated exact, VERIFIED |
| 2 | 0 | 171,943 | 11,165,649 | `965155d8cf5b4d1f709ae32aa03ca5ff1428f9439734308b2a8a07420fba3356` | `4b5c0d8a348362a6119a0779e2a0f1829fbd305b7036ff06e4ffb713dfa03de7` | 29,169,899; regenerated exact, VERIFIED |
| 2 | 1 | 171,944 | 11,165,657 | `7668b01c3b44af56944c54e5547d4165e697a7e994c10f9d3cbdbb65fa1e1cf4` | `ffc49229e5d412849763ecd52f82f3cd9e4fab10c2ee850ff11f2f8d0948618d` | not regenerated; missing |
| 2 | 2 | 171,944 | 11,165,657 | `ea398e47f6080e20c6d7a92afce731186a73b0af1b84274ce24804959e250ba4` | `963c4800207a69cf725215024470ce167eb8112cb6387ce22bf5b3cc7c146e5d` | not regenerated; missing |
| 2 | 3 | 171,944 | 11,165,657 | `6ae22517d92e7d3bd2bcec3faf6d7f18ef020cd6934ffd8dd71f218f825a665e` | `604653aaf40bf4f49aefe6a32f51bebe820c378babf869c2393aaccc51f24e20` | 611,813,162; regenerated exact, VERIFIED |
| 1 | 0 | 171,943 | 11,165,649 | `5575e7ac8a1b581c903b0de201678e92cad89ba5c474c1d9aa63dc1834d735b1` | `9fb8804705e768adc4f19e6c76cca889db5ac2e7783e14688a2565195286439c` | 28,695,789; regenerated exact, VERIFIED |
| 1 | 1 | 171,944 | 11,165,657 | `a4e32a35d451511b30c08a843c7ee20cbdcd5c2d3d9f097d79ab86816a4eade6` | `6bae77afbdc60ff6f050f90b78d4d9aaf18697292c86008f2c8326940c601729` | not regenerated; missing |
| 1 | 2 | 171,944 | 11,165,657 | `df79c9d341a6099a333746ed2c0b287dfbfdaafb6b252f511915ec8e34f1793e` | `37c97b15b549985139df3bdbe3e0922c6c519668708e7f3cffbe40393c4b7330` | not regenerated; missing |
| 1 | 3 | 171,944 | 11,165,657 | `96609557ab05c2611b8d8d2503002f685a8468444a83ab8ecf83b9d329eb9fa4` | `54fbe724b1646a861cef4e6b6be0eb00b9f6c9944dc23d43e7f9097c63501adc` | not regenerated; missing |
| 1 | 4 | 171,944 | 11,165,657 | `931d6ba85afb32e36dc428549dfc0e40b9f6c2ac5f0af08967a8d61b630bbd98` | `62301e906f97be1f668bcefe0c2707b632643905d2e1a9d1317e995a80b1d95f` | 2,522,983,470; regenerated exact, VERIFIED |
| 0 | 0 | 171,942 | 11,165,641 | `8f7810e49cf1e1b159cb2af40adbb01b6e03d5b0c060fe5c552214cb3a7989cc` | `32b8df9a1093c73c806d8ba6e7b5d8846bdfd903e88bc41bfe748b35a2465a58` | 20,376,558; regenerated exact, VERIFIED |
| 0 | 1 | 171,943 | 11,165,649 | `917c78e08bb9206788bd0e2febe8bcd13597841671651c1a4f6b81b37af0fb5e` | `cb05379ca96a417bf4e2efecb102f9a74077aa41ec156e433e720e6900c2af68` | not regenerated; missing |
| 0 | 2 | 171,943 | 11,165,649 | `b8edf2118dbe28e6ad5f97d667dd165a78a294016e3cd3e15d85a56673182f9c` | `e49ce46c19cb029c41d213ee1c6ffaae1b7336de6e5b5e97cb57d2701f03ff85` | not regenerated; missing |
| 0 | 3 | 171,943 | 11,165,649 | `6672088b2a17c7ad21a21416a70e7f1e406596d848453ec3efddd51d33de2743` | `e7c036a9934b975765d21192059226b0062b86fcca679c4dc4868f6959b3d169` | not regenerated; missing |
| 0 | 4 | 171,943 | 11,165,649 | `280c770eda43770a39d53b545eb045f0dc2a6d9a960052e7823b60db345712f1` | `a632bb2c3b5b6dc35626d0988d895ccdd194677582eff78e216eb1e6e8617347` | not regenerated; missing |
| 0 | 5 | 171,943 | 11,165,649 | `228780d9a7de83905fded0a38603f0bf1610f9e90b05e1f4aaf16a185362bd44` | `725a692dfeeb63adeb45f515f106cee212c55f88e8f11652858318d472d66e22` | attempted only; 3,306,012,672-byte truncated output is invalid and must be discarded |

The eight completed samples total 4,014,780,778 raw LRAT bytes. This is not an
estimate of the 18-row total; it is a strict measured subtotal. The aborted
`rho=0,k=5` file has no terminal newline, no UNSAT exit, and no checker
acceptance. Its SHA-256 `3399c71f...c26f40f7` is merely the identity of a
truncated by-product, not a certificate and not a lower bound on the final
proof size in any semantic sense.

### Restricted status matrix

The classifications below describe only this bounded recovery audit. They do
not edit or ratify the old certificate ledgers.

| class | exact rows | count | audit meaning |
|---|---|---:|---|
| `HUMAN_LEMMA_AUDITED` | every `rho=0,1,2,3` with `k=0,1` | 8 | eliminated by the conditional uniform lemma below; normal-form reduction remains an external dependency |
| `HISTORICAL_LRAT_REGENERATED_AND_REPLAYED` | `(3,0),(3,1),(3,2),(2,0),(2,3),(1,0),(1,4),(0,0)` | 8 | exact old LRAT SHA-256 reproduced; exact frozen CNF; checker exit 0 and one literal `c VERIFIED` on fresh final replay |
| `ARTIFACT_NOT_REGENERATED` | `(2,1),(2,2),(1,1),(1,2),(1,3),(0,1),(0,2),(0,3),(0,4)` | 9 | historical hash is recorded, but no raw proof was regenerated in this audit |
| `INVALID_TRUNCATED_OUTPUT` | `(0,5)` | 1 | 3,306,012,672-byte interrupted by-product; no UNSAT completion and no checker acceptance |

These classes overlap by design: five rows, `(3,0),(3,1),(2,0),(1,0),(0,0)`,
have both a human elimination and an exact replayed LRAT; three human-covered
rows, `(2,1),(1,1),(0,1)`, still lack regenerated historical artifacts. Thus
`8+8+9+1` must not be summed as a partition. The disjoint artifact partition is
8 replayed, 9 not regenerated, and 1 invalid partial output.

## What the bounded rerun established

### CNF determinism and encoding tests

All 18 fresh CNFs reproduced the frozen byte counts and hashes above in about
0.60--0.62 seconds each. The independent mutation suite returned:

```text
PASS exact thresholds through length 8
PASS exact mu2 linkage through width 8
PASS CNF semantics n=1..4, total graphs=760
PASS robust witness semantics cases=3003
PASS arc-minimal deletion semantics cases=7860
```

These tests are valuable encoder regression checks, not an independent proof of
the entire order-18 reduction or of shard coverage. Hostile acceptance still
requires a separate mathematical audit that the normal-form hypotheses imply
exactly the encoded constraints and that the `k` partitions are exhaustive and
disjoint.

### Eight exact historical identities reproduced

Commands used `cadical --lrat --no-binary -q CNF LRAT` followed by
`lrat-check CNF LRAT`. Every completed checker returned exit 0 and
`c VERIFIED`. Measured wall times on the 2-vCPU/4-GB sandbox were:

| row | solve seconds | check seconds | LRAT bytes |
|---|---:|---:|---:|
| rho 3, k 0 | 2.800 | 0.645 | 23,574,012 |
| rho 3, k 1 | 47.365 | 4.474 | 236,514,931 |
| rho 3, k 2 | 135.257 | 10.083 | 541,652,957 |
| rho 2, k 0 | 3.651 | 0.769 | 29,169,899 |
| rho 2, k 3 | 139.506 | 11.350 | 611,813,162 |
| rho 1, k 0 | 3.677 | 0.747 | 28,695,789 |
| rho 1, k 4 | 829.673 | 48.439 | 2,522,983,470 |
| rho 0, k 0 | 1.662 | 0.584 | 20,376,558 |

The exact-hash matches show that the current source build reproduces old output
for diverse easy and hard rows, including a 2.52-GB proof. They do not prove
that every remaining row will match; compare every output rather than assuming.

A final serialized replay rechecked all eight retained `(CNF,LRAT)` pairs with
the 22,064-byte checker at source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, binary SHA-256
`e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8`.
For every row, checker exit was 0, stderr was empty, and stdout contained
exactly one line `c VERIFIED`. The exact replay manifest fields
`rho,k,cnf_bytes,cnf_sha256,lrat_bytes,lrat_sha256,checker_rc,verified_lines,
checker_wall_ns` have SHA-256
`1b4ada96b21f9110dc44d8b31a47b74a875b5adff3f4a41ac533c2c7541a46d0`.
That manifest hash authenticates this audit's small replay record; the raw
4.014-GB LRATs remain deliberately untracked and are not smuggled into this
commit.

## Historical identity versus a valid replacement

These are different audit outcomes and must never be merged:

1. **Historical identity recovered/regenerated:** regenerated CNF hash equals
   the frozen CNF hash, LRAT hash equals the old reported LRAT hash, and the
   exact checker verifies it. This recovers the reported proof byte identity.
   Because the rho reports omitted LRAT byte counts and solver-binary identity,
   also record newly measured bytes and actual producer provenance rather than
   retroactively inventing historical metadata.
2. **Valid replacement certificate:** regenerated CNF hash equals the frozen
   CNF hash, a different LRAT is accepted by the authenticated checker, and the
   new LRAT's bytes/hash/toolchain/command are frozen in a new replacement
   ledger. It proves the same formula UNSAT but does **not** recover the old
   SHA-256 identity. Keep the old report immutable and label the substitution.
3. **Unacceptable:** solver exit 20 without retained proof; hash equality
   without checker replay; a proof checked against a nonidentical CNF; a timed-
   out/truncated LRAT; or editing the old hash table to the new value.

A different LRAT identity is unsurprising if options, compiler behavior, or
solver build change. Conversely, exact identity is strong reproducibility
information but does not replace semantic auditing of the CNF/reduction.

## Prioritized exact recovery procedure

### Priority 0 — preserve and preflight

1. Work in a disposable directory materialized from `cc61b3dc...`; do not alter
   lane state, notebook claims, or old certificate reports.
2. Record source commit/blob identities, OS/CPU, Python, compiler, CaDiCaL
   version/source/binary SHA-256 and bytes, checker source/binary SHA-256 and
   bytes, full command lines, start/stop times, exit codes, and available disk.
3. Re-run `test_cnf_semantics.py`; require all five PASS lines above.
4. Generate all 18 CNFs first. Refuse to invoke the solver unless variables,
   clauses, bytes, and SHA-256 equal the exact ledger row.
5. Keep each job in its own directory and write metadata atomically. Never
   reuse a partial `.lrat`; delete or quarantine it before retry.

### Priority 1 — uniform `k<=1` human reduction, hostile-audited

The notebook summarizes the low-rho extension. The following quantified lemma
spells out the dependency and the equality cases. It covers the eight rows

```text
(rho,k) = (0,0),(1,0),(2,0),(3,0),(0,1),(1,1),(2,1),(3,1).
```

**Lemma (uniform tournament/one-hole elimination).** Let `D` be in the frozen
rooted order-18, `m=8`, vertex-minimal then arc-minimal normal form. Thus

```text
A=N_D+(v),                 |A|=8,
B=N_D++(v),                |B|=7,
C=V(D)\({v} union A union B),  |C|=2,
T=D[{v} union A union B],  |T|=16,
```

there is a unique vertex `r in A` with `d_D+(r)=9`, every other vertex has
outdegree eight, no arc goes from `A` to `C`, and every `b in B` has a
predecessor in `A'=A\{r}`. Put `rho=e(C,B)`, let `e=5-rho`, and suppose exactly
`k in {0,1}` of the `e` residual holes lie in `T` (the other `e-k` lie between
`B` and `C`). Then `D` cannot be a counterexample.

**Proof.** Let

```text
K={b in B : b->c for both c in C}.
```

There are 14 unordered B--C pairs. Exactly `e-k` are holes and exactly `rho`
of the present pairs point from C to B. Consequently

```text
e(B,C) directed from B to C = 14-(e-k)-rho = 9+k.     (1)
```

If `x=|K|`, the seven B vertices contribute at most `7+x` arcs from B to C:
each contributes at most one unless it lies in K. Equation (1) therefore gives

```text
|K|>=k+2.                                             (2)
```

Fix arbitrary `b in K` and arbitrary `a in N_D^-(b) intersect A'`; the latter
set is nonempty by the normal form. For each `c in C`, `a->b->c`, while
`a->c` is forbidden because `a in A`. Hence both C vertices are exact second
neighbors of `a`.

Set

```text
X=N_T+(a),   S={a} union X.
```

Because `a!=r`, `d_D+(a)=8`; because no A vertex points to C, all eight
outneighbors of `a` lie in T. Thus `|X|=8`, `|S|=9`, and `T\S` has seven
vertices. Call `t in T\S` inaccessible if no directed two-walk from `a` to `t`
exists inside T. For every `x in X`, if the pair `xt` is present then it must be
oriented `t->x`, since `x->t` would give the two-walk `a->x->t`; also `t->a`
because `t notin X`. Therefore, if no T-hole joins `t` to S, then t dominates
all nine vertices of S and has outdegree at least nine. By the degree census,
any such unsupported inaccessible vertex is r. In particular there is at most
one unsupported inaccessible vertex.

A T-hole can support at most one inaccessible vertex for this fixed source:
if its endpoints are `u,w`, support requires one endpoint to be inaccessible
and the other to lie in S, so both endpoints cannot be inaccessible. Hence the
number `I` of inaccessible vertices in `T\S` obeys

```text
I<=1+k.                                               (3)
```

Every vertex of `T\S` that is accessible is an exact second neighbor of a in T:
it has a two-walk from a and is not an outneighbor of a. Thus a has exactly
`7-I` exact second neighbors in T, plus the two already found in C. Since a is
bad and `d_D+(a)=8`,

```text
(7-I)+2 < 8,  hence I>=2.                             (4)
```

For `k=0`, (3) and (4) contradict one another. This eliminates all four
`tournament` rows.

Now let `k=1`. Equations (3)--(4) force `I=2`: one inaccessible vertex is the
unsupported vertex r and the other is supported by the unique T-hole. The hole
cannot meet r. Indeed, support for the other inaccessible endpoint requires the
opposite endpoint of that hole to lie in S; if r were that opposite endpoint,
r would lie in S, contrary to r being inaccessible, while if r were the
supported endpoint it would not be unsupported. Therefore no T-hole joins r to
S. The preceding orientation rule gives `r->S`. Since `|S|=9`,
`d_D+(r)=9`, and r has no outarc to C,

```text
N_T+(r)=S={a} union N_T+(a).                          (5)
```

At most one `a in A'` can satisfy (5). If distinct `a,a'` did, then
`a' in {a} union N_T+(a)=N_T+(r)` forces `a->a'`, while
`a in {a'} union N_T+(a')=N_T+(r)` forces `a'->a`, impossible in an oriented
graph. Because b and a were arbitrary, every `A'` predecessor of every member
of K must therefore be the same vertex `a*`; nonemptiness gives the pointwise
identity

```text
N_D^-(b) intersect A'={a*}  for every b in K.          (6)
```

By (2), `|K|>=3`. The unique T-hole has at most two endpoints, so choose
`b in K` not incident with it. Then b has the following nine distinct
outneighbors:

```text
the two vertices of C;                                2
v, because v->b is false and the pair vb is present;  1
every vertex of A'\{a*};                              6
```

for the last six pairs, incidence with the sole T-hole was excluded, and (6)
forbids orientation toward b, so each is oriented from b. This contradicts
`d_D+(b)=8`. Thus all four one-hole rows are impossible as well. QED.

**Hostile audit.** The proof above was checked against the frozen labels and
normal-form hypotheses, not against the SAT result. The critical checks are:

1. the B--C count is exactly `9+k`, independent of rho after `e=5-rho` is
   substituted;
2. C vertices are exact, not merely weak, second neighbors because all
   `A->C` arcs are forbidden;
3. for a fixed source, one hole cannot support both endpoints: support puts its
   other endpoint in S while every inaccessible endpoint lies outside S;
4. badness gives `I>=2` because the accessible vertices are exactly outside
   `{a} union N_T+(a)`;
5. the unsupported vertex is forced to be the unique degree-nine r;
6. (5) holds as equality because r already has nine T-outneighbors and no
   C-outneighbors;
7. the sole-predecessor conclusion (6) is pointwise over every predecessor,
   not merely a common-predecessor statement; and
8. choosing b outside the two hole endpoints makes every one of the six final
   A' pairs present.

This is a restricted human lemma conditional on the frozen normal-form
reduction. It does not authenticate any absent LRAT, does not by itself audit
the reduction from an arbitrary counterexample, and does not close `m=8`.

Tick 22 additionally proves the `rho=3,k=2` subcase in which neither T-hole
meets r. The remaining r-incident subcase is computational; the precise human
gap is synchronization of predecessor classes when the other hole can support
opposite endpoints. No rigorous human elimination is preserved for the complete
high-`k` rho 0--2 rows. Solver-proof mining is a research aid, not a proof.

Even where the uniform lemma applies, retaining a regenerated LRAT is useful as
a regression oracle. Human replacement removes computational dependence only
if this lemma and the preceding normal-form reduction are independently
accepted.

### Priority 2 — finish the ten currently unregenerated rows in increasing risk

Do not infer difficulty monotonically from `k`; use capped discovery runs and
retain only completed certificates. A conservative queue is:

1. `rho2-k1`, `rho1-k1`, `rho0-k1` (human-replacement candidates and expected
   easy checks);
2. `rho2-k2`, `rho1-k2`, `rho0-k2`;
3. `rho1-k3`, `rho0-k3`;
4. `rho0-k4`;
5. `rho0-k5` last, with a large disk guard and no short outer timeout.

`rho0-k5` produced more than 3.306 GB before a bounded run was stopped, so
reserve substantially more than that for the raw proof plus temporary/checker
headroom. The present 84-GB free workspace is adequate for serialized jobs,
but a complete total-size forecast is unavailable. With only about 4 GB RAM,
serialize solver jobs and checker jobs; do not run two hard CaDiCaL instances
concurrently. Immediately check and hash each completed proof, then optionally
compress only after preserving raw identity metadata.

Eight measured completed rows consumed 19.39 minutes solver time plus 1.28
minutes checker time. This is a measured subtotal, not a total forecast. The
hardest completed row took 13.83 minutes and produced 2.52 GB; `rho0-k5` did not
finish within the bounded attempt. Budget at least hours, not minutes, for the
remaining serialized campaign and use per-job disk/RSS telemetry. No runtime
claim should be made for an unmeasured row.

### Priority 3 — independent replay and durable replacement ledger

For each completed row require, in order:

1. exact frozen CNF identity;
2. CaDiCaL exit 20 and terminal `s UNSATISFIABLE`;
3. LRAT file closed normally and hashed;
4. exact `lrat-check` exit 0 and literal `c VERIFIED`;
5. old-hash comparison yielding `HISTORICAL_IDENTITY` or
   `VALID_REPLACEMENT`;
6. a second replay from a freshly regenerated CNF, preferably on another host
   or independently rebuilt checker;
7. immutable metadata containing raw byte count/hash, not just prose MB;
8. if compressed, decompression hash/byte check and compressor provenance.

The final ledger must contain all 18 rows and an explicit status per row such
as `HUMAN_PROOF_CHECKED`, `HISTORICAL_LRAT_REPLAYED`,
`REPLACEMENT_LRAT_REPLAYED`, or `ARTIFACT_MISSING`. Completeness checks must
reject duplicate `(rho,k)` keys, missing keys, unknown extras, hash drift, and
checker logs without `VERIFIED`.

## Exact command skeleton

This regenerates source-controlled inputs and runs one row. Repeat only through
a manifest-driven 18-row loop with expected hashes; do not paste ad hoc names.

```sh
set -euo pipefail
REPO=/workspace/math-god
SRC=cc61b3dc4d46a0330253bac31c0d598421850864
A=breakthrough/assignments/seymour-second-neighborhood
W=$(mktemp -d /workspace/rho-recovery.XXXXXX)
git -C "$REPO" archive "$SRC" "$A/experiments" | tar -x -C "$W"
E="$W/$A/experiments"
CADICAL=/absolute/path/to/cadical-1.7.3
LRAT_CHECK=/absolute/path/to/lrat-check
cd "$E"

# Preflight provenance and semantic tests.
sha256sum snc_cnf.py rho3_shards.py rho2_shards.py rho_low_shards.py \
  test_cnf_semantics.py "$CADICAL" "$LRAT_CHECK"
"$CADICAL" --version
PYTHONPATH=. python3 test_cnf_semantics.py

# Example rho=2,k=1. Refuse hash drift before solving.
mkdir -p "$W/jobs/rho2-k1"
python3 rho2_shards.py 1 "$W/jobs/rho2-k1/rho2-k1.cnf" \
  > "$W/jobs/rho2-k1/generate.stdout"
test "$(stat -c %s "$W/jobs/rho2-k1/rho2-k1.cnf")" = 11165657
test "$(sha256sum "$W/jobs/rho2-k1/rho2-k1.cnf" | awk '{print $1}')" = \
  7668b01c3b44af56944c54e5547d4165e697a7e994c10f9d3cbdbb65fa1e1cf4

rm -f "$W/jobs/rho2-k1/rho2-k1.lrat"
set +e
"$CADICAL" --lrat --no-binary -q \
  "$W/jobs/rho2-k1/rho2-k1.cnf" \
  "$W/jobs/rho2-k1/rho2-k1.lrat" \
  > "$W/jobs/rho2-k1/solve.stdout" \
  2> "$W/jobs/rho2-k1/solve.stderr"
solver_rc=$?
set -e
test "$solver_rc" = 20
grep -Fx 's UNSATISFIABLE' "$W/jobs/rho2-k1/solve.stdout"

"$LRAT_CHECK" "$W/jobs/rho2-k1/rho2-k1.cnf" \
  "$W/jobs/rho2-k1/rho2-k1.lrat" \
  > "$W/jobs/rho2-k1/check.stdout" \
  2> "$W/jobs/rho2-k1/check.stderr"
grep -Fx 'c VERIFIED' "$W/jobs/rho2-k1/check.stdout"
stat -c '%s  %n' "$W/jobs/rho2-k1/rho2-k1.lrat"
sha256sum "$W/jobs/rho2-k1/rho2-k1.lrat"

# Historical identity only if this succeeds. Otherwise preserve the verified
# output under a NEW replacement ledger; never rewrite the old report.
test "$(sha256sum "$W/jobs/rho2-k1/rho2-k1.lrat" | awk '{print $1}')" = \
  ffc49229e5d412849763ecd52f82f3cd9e4fab10c2ee850ff11f2f8d0948618d
```

Emitter commands for the complete matrix are exactly:

```sh
for k in 0 1 2;       do python3 rho3_shards.py "$k" "rho3-k$k.cnf"; done
for k in 0 1 2 3;     do python3 rho2_shards.py "$k" "rho2-k$k.cnf"; done
for k in 0 1 2 3 4;   do python3 rho_low_shards.py 1 "$k" "rho1-k$k.cnf"; done
for k in 0 1 2 3 4 5; do python3 rho_low_shards.py 0 "$k" "rho0-k$k.cnf"; done
```

## Hostile verification checklist

Reject the recovery if any answer is no:

- Is the assignment source exactly the September source tree, with recorded
  blob IDs, rather than an unreviewed merge or current stale checkout?
- Do all 18 CNFs match variables, clauses, bytes, and SHA-256 before solving?
- Did semantic mutation tests pass from the same materialization?
- Does every computational row retain a complete LRAT, solver exit 20, checker
  exit 0, and exact `c VERIFIED`?
- Was each proof checked against its own exact CNF, never a same-sized sibling?
- Are historical hash matches and new valid replacements labeled separately?
- Were partial files, especially the aborted 3.306-GB rho0-k5 output, excluded?
- Does an independent manifest checker prove the exact 18-key partition and
  reject omissions/duplicates?
- Are human replacements explicit proofs, not notebook summaries or inferred
  analogies, and have exact-distance and quantifier steps been audited?
- Is the scope stated only as the rooted order-18 `m=8` normal form, without an
  order-18 or universal Seymour claim?

## Recommended disposition

The cheapest defensible path is hybrid: retain the hostile-audited uniform
`k<=1` lemma above as a conditional human replacement for eight rows; retain
the eight already regenerated exact LRATs as regression evidence; regenerate
the ten currently unregenerated rows (or only the non-human-covered subset if
computational independence, rather than artifact restoration, is the goal); and create an
immutable 18-row replay ledger that distinguishes human proofs, exact historical
identities, and valid replacement proofs. Until every row has either an
independently checked human proof or a retained/replayed LRAT, the truthful
status is **rho aggregate proof artifacts partially regenerated; original
18-object set not recovered**.
