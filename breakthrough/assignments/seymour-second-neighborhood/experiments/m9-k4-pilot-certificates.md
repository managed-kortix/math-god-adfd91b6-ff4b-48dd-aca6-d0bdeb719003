# Cross-shape k4 pilot ledger

The deterministic selector `m9_k4_pilots.py` chooses one structurally feasible
cell per shape, alternating `kappa=5,6`, and within each pool maximizing
`(eta,lambda)` before canonical-key tie-breaking. All eleven selected CNFs were
solver-UNSAT and accepted by `lrat-check` in the execution environment. The
large LRATs were temporary and are not committed, so these rows are regression
observations rather than durable branch certificates. They do not change any
cell in the complete campaign from `UNRUN` to `UNSAT_VERIFIED`.

Toolchain:

- CaDiCaL 1.7.3 source commit
  `38e073b389a877b0a0d3c91136d2443ab95fdeba`; local binary SHA-256
  `5d8bdcbe5ac3dd205fc40b040f908565c1f3bafde8a838664c8c4189fd93ec1c`.
- `lrat-check` source commit
  `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`; binary SHA-256
  `e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8`.
- Solve command: `cadical --lrat --no-binary -q CELL.cnf CELL.lrat` (exit 20).
- Check command: `lrat-check CELL.cnf CELL.lrat` (exit 0, `c VERIFIED`).

Each row is `shape | CNF SHA-256 | LRAT SHA-256 | LRAT bytes`:

```text
c4              014b4f6433f88de0cc3c98c89e8e11098ecbeb2fcdf008a280184d0ce308b258 f69898e4e9d70d33e9f2db9cc83d447e1335f3723eaf114fdb4ef8790b04a55a 42484299
claw_edge       916f4636009d7c8ca43748a8dc734ae71464f2bf5c18299a8c810d95a88716b5 69b5d88f4de85d510628ebd31bc6916000d12136cece1bcbe749c2d272d28174 73893804
fork            99438ab2266767c81c84bbdd819ca54cb1622f1259885160c7affb74a34ea223 9749908dbde49d572c5d93a83bb3811ee9264feb84b20323cd95b1c0663221e5 49343738
four_matching   4c2fff9bacd5a8e058dedd8372b23a73d838e725c79ab2ffefd83f735cda0ae0 a3e003a799bb50b123c3b92247bbddfea7431eb7d3a421aa560f220e6cb1c57e 48096449
k1_4            72c15af875c8c9149df332eeb8eb1101286cb697a0bcbc26117b02c1876d5e84 dd6e5ed60223e529f9da8c484327ae6147fa204579d1b05e2a59681109fa4d4b 34336496
p3_two_edges    469d624f860c6b6b5a197fd4f91b579e393ede2fa8d65d066b1bfbc095132eaf 99dd3241a2458e42b0e39a40924089f43fa17b1aac9fe73c4d4bc60fcdae5632 161944186
p4_edge         0b029b04f696061335abd1386c8a3edeaf6e576bdce45a20e5d83a77787bef96 43cb1d09d6fb96adc3e5ceaf7881c2aa9fb56f45b1cb585db279beec72a2c192 244294629
p5              8657275b1e7115fac3430b22b77856d544527082723bec69f2cba6e34f07b8f7 231a8809e28b3fb2906467538de7cc6225e378869f5cafb9aad90fb70b0d9ff2 52691155
paw             2e9d16835dec5669a71d2e2f794462978c50c8050cd53f490c74e4ca79d3495c 424cc823fa85dd0b9f82c67c6e4566e86240d720b648f841597aa88933c5e282 57491399
triangle_edge   c76da4db033acc7062d9b1257f5a978a2ec53b35dd34680304ed2281bc15d492 2e62cbe49050b18c4499b593008172529ea096453d4fd04189a513a73f1dda9a 47033240
two_p3          6d16e20029a262ba2798631ba12b15fc6d3493ba15d8153a878275d8a2d5c13e 4b8fddeedd907c3b13d796f64cb80ec278c7ba1605305e7a509a8b9cfd7c9fb1 123836844
```

Regenerate the exact keys with:

```sh
python3 m9_k4_pilots.py m9-k4-cover.tsv
```

The next campaign must retain each LRAT in immutable content-addressed storage
and only then promote its ledger row. Hashes without available proof bytes do
not constitute a checkable UNSAT certificate.
