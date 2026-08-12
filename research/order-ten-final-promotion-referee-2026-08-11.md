# Order-ten final promotion referee report (2026-08-11)

## Verdict and scope

The final order-ten promotion is sound for the exact narrow scope

`order=10;rank=6;kernels=K1133-K1198;single-positive-rank-cyclic-block`.

This verdict accepts the repository's segmented-execution semantics: the 23
receipts are records emitted after independent exact chunk replays, while their
digests authenticate identities and bytes but do not prove that execution took
place. The aggregate remains explicitly an index with `exact_proof=false`.
Nothing in this report promotes multiblock graphs, all connected hexacyclic
graphs, `STATE.md`, or any project-global status.

## Final artifact authentication

The final manifest is canonical ASCII JSON with SHA-256
`5162243e0535ca41f72fa0c7bd27e6ee240d485567e56b8c8dfbcf3a4ecbf3b6`.
It binds 23 distinct XZ chunks in manifest order, with contiguous ranges from
`[0,10000)` through `[121582,125457)`, union `[0,125457)`, 16 targets per
residual, and 2,007,312 targets.

All 23 receipts in
`positive-square-energy/experiments/rank6_order10_chunk_replays/final/` were
authenticated against the final manifest, current auditor, transitive
dependencies, compressed chunk bytes, embedded chunk ranges, key-stream
digests, ownership-stream digests, and exact-report contracts. Regenerating the
aggregate from those receipts produced bytes identical to the stored
`aggregate.json`, whose SHA-256 is
`8c48944fc4a657241ed6519b05acb2af0efefee56064f680f92bad9ddc7bcabf`.

The receipt totals are:

| quantity | total |
|:--|--:|
| covered targets | 2,007,312 |
| exact certified targets | 2,007,312 |
| disjoint rational owners | 2,006,272 |
| disjoint symbolic-only owners | 1,040 |
| uncertified targets | 0 |
| unresolved targets after symbolic ownership | 0 |
| all symbolically owned targets | 14,912 |
| symbolically owned targets also certified numerically | 13,872 |

Thus the final owner partition is disjoint and exhaustive:
`2,006,272 + 1,040 = 2,007,312`. The wider symbolic owner set consists of the
824 structural rows and 108 atom rows (14,912 target keys); most of those keys
also have rational pack certificates. The separate 692-key atom-profile
dictionary is not the same quantity as the wider structural-plus-atom owner
set.

## Symbolic and wire-format audit

The 125,457 pack records have the following exact mode census:

| mode | rows |
|:--|--:|
| shared rational | 125,166 |
| K1133 template | 8 |
| structural | 51 |
| atom | 14 |
| balanced rank one | 218 |
| fallback | 0 |
| unresolved | 0 |

The symbolic ledger regenerated 178 decompositions: 18
`mixed-1/simplex-3-4`, 152 `mixed-2/simplex-4`, and 8
`mixed-5/simplex-none`. The corresponding profile-key union has 692 keys. The
pack auditor separately verifies K1133 templates, diagonal-dominance structural
records, atom classifications, and balanced signed rank-one records.

Every final XZ chunk was decompressed and decoded as `R10G1`; all 125,457
records re-encoded byte-for-byte to the original raw stream. This checks the
magic, kernel-source digest, canonical unsigned and signed varints, mode bytes,
shared denominators, stereographic parameter widths, fallback bitmap grammar,
record count, embedded start, and absence of trailing bytes. The stored and raw
size and SHA-256 bindings also matched the manifest.

## Arbitrary-length and tree lift

The pinned analytic owner, canonical manifest, and proof note passed in normal
and optimized Python modes. Its finite frontier is
`F(c)={c} union {c+2e_i}`. After permutation within a parallel class, every
allowed simple realization has the same parity and coordinatewise dominates
either `c` or one `c+2e_i`. The exact path excess

`f_j(r)=j tan^2(acos((-1)^j r)/(2j))`

is nonincreasing under `j -> j+2`; therefore one selected frontier witness
lifts under arbitrary simultaneous same-parity coordinate lengthening. This is
an arbitrary-length simple-subdivision argument, not a canonical-only or
one-coordinate-only inference.

For a rank-six core with `L` edges, `|V(B)|=L-5`. Genuine one-vertex-sum
additivity of `kappa`, together with `kappa(T)=|E(T)|`, permits arbitrary finite
rooted trees meeting the existing graph only at one root. The audited finite
bound `kappa(B)<=L+5` then gives `s+(G)>=|V(G)|`. Connectors meeting the core
twice, nonsimple realizations, and multiple positive-rank cyclic blocks remain
excluded.

## Mutation results

The promotion owner passed in both normal and `python3 -O` segmented modes and
reported 20 built-in hostile rejections. Additional referee mutations gave:

| mutation | result |
|:--|:--|
| omit any pinned dependency | rejected |
| widen scope to all connected graphs | rejected |
| weaken theorem conclusion to readiness | rejected |
| forge aggregate `exact_proof=true` | rejected |
| truncate aggregate coverage | rejected |
| omit or duplicate a receipt | rejected |
| alter a receipt owner total | rejected |
| alter receipt proof semantics | rejected |
| add uncertified targets | rejected |
| encode a nonminimal varint in an `R10G1` stream | rejected by canonical exact decode |
| alter a receipt mode count or descriptive symbolic-owned total in isolation | accepted by the receipt authenticator, but rejected end-to-end by the aggregate's pinned receipt digest |

The last row is a hardening observation rather than a promotion failure. The
standalone receipt authenticator validates the fields needed for exact range and
owner completeness but does not recompute every descriptive report subtotal.
The final promotion nevertheless pins the aggregate digest, and the aggregate
pins every complete receipt digest; the referee also independently summed these
fields. Likewise, ordinary pack decoding permits a nonminimal varint, but the
final streams are byte-canonical and all raw stream digests are pinned.

## Reproduction record

The following checks passed:

```text
aggregate authentication and byte-identical regeneration: PASS
23 receipt authentication: PASS
all 23 R10G1 canonical re-encodings: PASS
segmented promotion owner, normal mode: PASS
segmented promotion owner, python3 -O: PASS
conditional analytic lift, normal mode: PASS
conditional analytic lift, python3 -O: PASS
order-ten fragment and Gram-template unit tests (7 tests): PASS
```

A fresh monolithic full replay was started but did not finish within the
30-minute referee command limit, so this report does not claim a new monolithic
execution. That does not weaken the stated segmented-evidence verdict: every
final segment has its own authenticated exact-execution receipt, and the
promotion owner consumes precisely that pinned 23-receipt generation.
