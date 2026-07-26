# m=9 isolated-root k=3 shape certificates

For rho 0 and 1, the aggregate shard is partitioned by the five possible
unlabeled three-edge T-hole graphs. The shape classifier is independently
validated by `test_m9_k3_shapes.py`. Every shard below was solved by CaDiCaL
1.7.3 and independently accepted by the pinned LRAT checker.

|rho|shape|CNF SHA-256|LRAT SHA-256|
|---:|---|---|---|
|0|matching|`7348c45104da03dcb688be534985c334f4f848e6a8c8b59687cbb39591100fbe`|`ee1f3d35fa808a1651ba15546bc22d59ebed0438a4da48df028842f103489a0c`|
|0|p3_edge|`1eb5b8f832b8298c194d5c9baec7853c9d0f7b78634d77435a436a0e4c61e7f7`|`19050e1fee422b5f591a32dbceefbdb972c2147dd6bf5c646150cdcb3c29062d`|
|0|p4|`3292a0fbf75b80bcbf73e3e4e6ebc455503f8017f3ae88e56f2ab504a891a989`|`87e47b56b29c0ccb0cec55f1459cd4e0f71b4b185f251af043caa16073b868b2`|
|0|claw|`85691283047fbe08efc326a9b1f702391185e2bd8dc739215ab3ce3d0216186e`|`41c8ac22f5091d0184bb2733b8fb8ee53999870b36761337de2d42204ebeb1b6`|
|0|triangle|`aaa4d32e14ad3257e78267f34aa296541760eb6139bb96b3ae14623fc5d83432`|`c2b63ddbcaaed9c17edbae4e5e00085afd62f78628da04f5f0ae425276f1a956`|
|1|matching|`eaca164af995d90791246125ab44eef876597579c50493b139cf830a18058c82`|`f9a607dc9208d27c9d1677319a3f58d094f647dd65cc3ee611108898f86d613f`|
|1|p3_edge|`9b9a7480c3d037dd3efe180958ae4551a3178a5adb577c4ac979a19303e0fffa`|`7b2750959d48b23d811ab58d3173f6897a697fe0192a600388058795ba817bb7`|
|1|p4|`4aeb1c58a9d5f7ec9948744cdc49c613f65448371a167e87eedd66a5ebb7e7d7`|`4b4af82b0ea3691493f8c48f9ee34f2e9c3c07962eb720e89c8956dcaf0a70ff`|
|1|claw|`c91b147576e241468d2b97bc0513e38aa8de6544b70db7adbc804c26078c933c`|`9a0bc129520eef45d8e52c398683e6b6ce3b01cf715b4b6f6fcf9ac3ef11b4ad`|
|1|triangle|`bfd97c5a3a4c20162bee4db1689383e326160c9012a7dd7c904b3d5cdfc7f7be`|`cf7c3712b496d3bd6c6633dba16c38f1b53b880394d11c92af8a1eba74960e16`|

The rho 2 and 3 aggregate k=3 shards were separately LRAT-verified. Hence the
entire k=3 strip is eliminated in the exact minimal-counterexample model.
