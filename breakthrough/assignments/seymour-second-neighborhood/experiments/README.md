# Exact baseline experiments

Commands (Python 3 and Node.js 18+):

```sh
python3 test_verifiers.py
python3 exhaustive_crosscheck.py --max-n 5
python3 verify_set.py certificate.txt
node verify_matrix.js certificate.txt
```

Exit status is 0 only for a valid counterexample, 1 for a valid oriented graph
which is not a counterexample, and 2 for malformed input. `verify_set.py` uses
adjacency sets; `verify_matrix.js` has an independent parser and directly scans
a Boolean matrix. The exhaustive oracle compares every neighborhood set, not
only the final decision. Exhaustion is a regression test and is not claimed as
progress toward proving the universal conjecture.
