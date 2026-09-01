# Rank-seven order-ten packet/Rayleigh pilot

The exact post-weighted remainder has 8,184,653 orbit rows.  A deterministic
evenly spaced pilot selects positions `floor(iN/1000)`, giving 1,000 rows,
1,342 physical rows, and 464 coarse structural signatures.

Every one of the seventeen canonical-plus-coordinate targets per row was tested
in this precedence:

1. an actual induced unit-edge `K5`, `K4`, or diamond with the exact
   tree/odd-unicyclic complement debit;
2. an induced theta whose complement is a disjoint union of bipartite
   unicyclic components;
3. an exact integer Rayleigh vector satisfying
   `(x^T A x)^2 > |V|(x^T x)^2` and `x^T A x>0`.

The exact result is zero owners in every lane: 0 packet targets, 0 theta
targets, and 0 Rayleigh targets among 17,000 tested targets.  Thus no structural
family is promoted and there is no strongest positive lane.  The only searched
family with an all-length and rooted-tree lift would have been the induced-theta
lane; it has exact pilot coverage `0/17,000`.  Actual clique/diamond packets
retain only non-anchor same-parity lift, while fixed Rayleigh vectors are finite
target certificates and do not lift through arbitrary subdivision.

This negative pilot is useful evidence against spending a full 8.18-million-row
pass on these direct lanes.  The non-scalar weighted-cycle Gram remains the
strongest persisted order-ten lane, with exact union coverage of 7,807 rows,
9,471 physical rows, and 132,719 canonical-plus-coordinate targets.

Artifacts:

- `experiments/rank7_order10_packet_rayleigh_pilot.py`
- `experiments/rank7_order10_packet_rayleigh_pilot.json`
- `experiments/rank7_order10_packet_rayleigh_pilot_owners.jsonl.xz`

Reproduce from the repository root with:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
python3 positive-square-energy/experiments/rank7_order10_packet_rayleigh_pilot.py \
  --pilot-size 1000 --audit
```

The canonical report SHA-256 is
`6003f61762abc9106a911fc8705e513a48df4cc175f4eba6391f9f059f163649`.
