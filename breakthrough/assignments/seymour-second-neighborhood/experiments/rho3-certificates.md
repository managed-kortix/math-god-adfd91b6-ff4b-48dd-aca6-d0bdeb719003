# Rho-3 exact shards

This is an independently checked computational regression result, not yet the
preferred human proof. Labels are `v=0`, `r=1`, `A=1..8`, `B=9..15`,
`C={16,17}`, and `T=0..15`. The three values of `k` exhaust the placement of
the two residual holes in the row `(p,rho,e)=(6,3,2)`.

Generate, solve, and check each shard with:

```sh
python3 rho3_shards.py K rho3-kK.cnf
cadical --lrat --no-binary -q rho3-kK.cnf rho3-kK.lrat
lrat-check rho3-kK.cnf rho3-kK.lrat
```

All three checker runs returned `c VERIFIED` (checker exit 0). Exact identities:

| k | variables | clauses | CNF SHA-256 | LRAT SHA-256 |
|---|---:|---:|---|---|
| 0 | 30981 | 171943 | `2a232c2478c3c609241ed2d2c47b755127d95100ac57e39acee2a4a8e7339a5f` | `4d0c419d993ab28fffb9bba622977e85bb27916838a67aae7ce96776ca2497ef` |
| 1 | 30981 | 171944 | `329489edf5c75fd194a171d8b60341ac587720f838cb189d4cb85cf0172c4202` | `e8109fe5adfcf81a558e973dfd6b5d7182ebf736f78fea4bd6c191c9cee14620` |
| 2 | 30981 | 171944 | `55e88baba98fb79dc22562fa7e0205e8d0b33600aa1c7574fdc7236875cdfe31` | `060c19a3b412550d4cebcff78280c5e3e00c92a32fac7aa79e52af2d9d2b335a` |

The semantic mutation suite independently checks exact thresholds, second
neighborhoods, robust witnesses, and arc-minimal clauses. The proof files are
large (23, 226, and 517 MB uncompressed), so deterministic regeneration is the
canonical public artifact until a compact human proof or smaller proof core is
finished.
