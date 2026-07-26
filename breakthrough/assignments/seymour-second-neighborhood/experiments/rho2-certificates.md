# Rho-2 exact shards

The row `(p,rho,e)=(5,2,3)` is partitioned by the exact number `k=0,1,2,3`
of missing pairs in `T={0,...,15}`. The other `3-k` residual holes lie between
`B` and `C`. Generate each shard with `rho2_shards.py`; solve with CaDiCaL
`1.7.3 --lrat --no-binary`; check with the pinned `lrat-check`.

Every checker returned `c VERIFIED`:

| k | variables | clauses | CNF SHA-256 | LRAT SHA-256 |
|---|---:|---:|---|---|
| 0 | 30981 | 171943 | `965155d8cf5b4d1f709ae32aa03ca5ff1428f9439734308b2a8a07420fba3356` | `4b5c0d8a348362a6119a0779e2a0f1829fbd305b7036ff06e4ffb713dfa03de7` |
| 1 | 30981 | 171944 | `7668b01c3b44af56944c54e5547d4165e697a7e994c10f9d3cbdbb65fa1e1cf4` | `ffc49229e5d412849763ecd52f82f3cd9e4fab10c2ee850ff11f2f8d0948618d` |
| 2 | 30981 | 171944 | `ea398e47f6080e20c6d7a92afce731186a73b0af1b84274ce24804959e250ba4` | `963c4800207a69cf725215024470ce167eb8112cb6387ce22bf5b3cc7c146e5d` |
| 3 | 30981 | 171944 | `6ae22517d92e7d3bd2bcec3faf6d7f18ef020cd6934ffd8dd71f218f825a665e` | `604653aaf40bf4f49aefe6a32f51bebe820c378babf869c2393aaccc51f24e20` |

This certifies elimination only in the rooted order-18, eight-hole,
vertex-minimal then arc-minimal normal form encoded by `snc_cnf.py`.
