# attack plan — positive square energy

## Target

Conjecture 1.2 of arXiv:2506.07264v1: every connected n-vertex simple graph
with m >= n+1 satisfies s^+(G) >= n.

## Ranked lines of attack

1. **Sparse census beyond n=9.** Enumerate nonisomorphic connected graphs at
   n=10, beginning m=n+1 and increasing m. Float-screen s^+-n, retain a wide
   safety margin, then certify all near-minimizers by exact characteristic
   polynomial/root isolation. A counterexample is immediately certificate-shaped.
2. **Extremal family discovery.** Mine low-slack graphs for common cores,
   pendant-tree attachments, inertia, and equitable partitions; conjecture and
   prove a reduction or an infinite-family formula.
3. **Triangle-unicyclic bridge.** Although outside Conjecture 1.2 at m=n,
   understand the paper's bottleneck (Conjectures 9.1/9.4) to derive a gluing
   inequality robust under adding one edge.
4. **Local transformations.** Test whether leaf relocation, subdivision, or
   edge addition monotonically controls s^+ in the low-slack regime.

## Current line

Line 1: n=10,m=11 through 16 fully exact-certified in SymPy and independently
checked in PARI (412,523 graphs total). Fresh-reproduce m=16, then continue m=17.

## Next experiments

1. Fresh-process reproduce and preserve both compact m=16 summaries.
2. Screen and exact-certify the low tail of m=17.
3. Continue m=17,... slices while counts remain tractable, recording exact minima.
4. Compute structural fingerprints of the low-slack set (degree sequence,
   blocks, girth, diameter, number of positive eigenvalues).
5. Derive the characteristic polynomial and s^+ formula for the general
   dumbbell formed from two odd cycles joined by a bridge.

## Verification discipline

Numerical eigenvalues are search heuristics only. Any claimed inequality,
counterexample, or extremizer requires a standalone exact certificate, a fresh
process, a second engine, and statement/novelty checks.

## Retreat criteria

After roughly two weeks without either a new certified finite bound, a proved
structural lemma, or a promising extremal family despite census and theory
work, write a post-mortem and reconsider the queue.
