# Exact baseline experiments

Commands (Python 3 and Node.js 18+):

```sh
python3 test_verifiers.py
python3 exhaustive_crosscheck.py --max-n 5
python3 verify_set.py certificate.txt
node verify_matrix.js certificate.txt
~/mathenv/bin/python direct_smt.py --n 17 --b-size 6 --timeout-ms 300000
~/mathenv/bin/python direct_smt.py --n 18 --b-size 6 --missing 3 --minimality --timeout-ms 900000
```

Exit status is 0 only for a valid counterexample, 1 for a valid oriented graph
which is not a counterexample, and 2 for malformed input. `verify_set.py` uses
adjacency sets; `verify_matrix.js` has an independent parser and directly scans
a Boolean matrix. The exhaustive oracle compares every neighborhood set, not
only the final decision. Exhaustion is a regression test and is not claimed as
progress toward proving the universal conjecture.

`direct_smt.py` is a baseline exact SMT search. It fixes a minimum-degree-eight
root with six or seven exact second neighbors and imposes deficit exactly one or
two at every vertex. A `sat` adjacency projection is not trusted until both
external verifiers pass. An `unknown` result has no mathematical force, and an
`unsat` result is not a proof artifact unless independently certified.

`--minimality` adds proved necessary conditions for a globally vertex-minimal,
then arc-minimal counterexample: every vertex has a tight in-neighbor witness,
and every present arc satisfies the exact gain/lost-second-endpoint deletion
inequality. These are not part of an unrestricted fixed-order model.
