# Cycle 182: exact `q`-collision certificate specification

## Bounded verdict

No exact collision can be reconstructed from the committed Cycle 181 report.
It contains the definition of `c(q,ell)` and the collision criterion, but it
does not name a governing field `L`, a fixed auxiliary prime `ell`, two twist
primes, modular-symbol output, or Frobenius-class data.  There is also no Cycle
182 raw script or data file in the repository, and the present environment has
neither PARI/GP nor Sage.  Consequently this cycle records the exact finite
certificate needed to verify a future collision; it does not invent missing
values or claim a collision.

## Claim represented by a certificate

Fix

\[
 E=433\mathrm a1:y^2+xy=x^3+1,\qquad p=7,
\]

a finite Galois extension `L/Q`, and one auxiliary prime `ell`.  Put

\[
 L'=L\,\mathbf Q(\zeta_{8\cdot7\cdot433\cdot\ell}).
\]

A zero/nonzero collision certificate consists of primes `q_0,q_1` for which

\[
 \operatorname{Frob}_{q_0}(L')=
 \operatorname{Frob}_{q_1}(L')
\]

as conjugacy classes, both pairs `(q_i,ell)` are in the stated admissible
packet, and, using one primitive root `eta` modulo `ell`,

\[
 c_\eta(q_0,\ell)=0,\qquad c_\eta(q_1,\ell)\ne0\pmod 7.
\]

This refutes factorization of `c` through the named field `L`; it does not
refute governance by every finite extension.  The zero/nonzero assertion is
unchanged by unit rescaling of either modular-symbol line.

## Required committed artifacts

The certificate is complete only when all of the following are committed.

1. **Manifest.** A machine-readable JSON file records `L`, `ell`, `eta`,
   `q_0`, `q_1`, the software versions, command lines, SHA-256 hashes of every
   input and output, and the exact admissibility predicate being tested.
2. **Governing field.** Give defining polynomials for `L` and `L'`, proofs or
   machine certificates that the represented extensions are Galois, explicit
   embeddings needed for the compositum, the finite ramification set, and an
   explicit model of `Gal(L'/Q)` with stable conjugacy-class labels.
3. **Frobenius witnesses.** For each `q_i`, certify unramifiedness and identify
   Frobenius in the explicit Galois model.  Factorization type of one defining
   polynomial is insufficient in general: distinct conjugacy classes can have
   the same permutation cycle type.  Supply a class-separating resolvent,
   explicit residue-field action, or another exact class-identification
   witness.  The verifier must check equality of conjugacy classes, not merely
   equality of labels printed by unrelated runs.  For the two-point Kummer
   field, equality of residual `GL_2(F_7)` classes is also insufficient.  The
   witness must identify the centralizer orbit of the affine Kummer pair in
   `(E[7]/(A-I)E[7])^2`, with explicit basis and lift comparison maps.  In the
   nonidentity-unipotent packet this reduces to equality of the zero/ordered
   projective localization row, as proved in Cycle 184.
4. **Twist records.** Record
   `D_q=q` for `q=1 mod 4` and `D_q=-q` for `q=3 mod 4`, the global minimal
   model of `E^(D_q)`, the change of variables from the generated twist, its
   discriminant, and conductor `433*q^2`.
5. **Normalization records.** Record the exact `msfromell(E_q,1)` convention,
   the positive Neron period convention, Manin and real-component factors, and
   enough output to identify the integral plus modular-symbol lattice.  A
   decimal period is diagnostic only and is not certificate input.
6. **Raw symbols.** For every `a=1,...,ell-1` and each `q_i`, store the exact
   rational value
   `[a/ell]^+_(E^(D_q))`, its numerator and denominator, and the discrete log
   `j_a=log_eta(a) mod 7`.  Every denominator must be prime to seven.
7. **Derived sums.** Store the seven exact grouped sums
   \[
     S_j(q)=\sum_{\substack{1\le a<\ell\\j_a=j}}
       [a/\ell]^+_{E^{(D_q)}}\quad(0\le j<7)
   \]
   and verify
   \[
     c_\eta(q,\ell)=\sum_{j=0}^6 jS_j(q)\pmod7.
   \]
   The raw rows, grouped sums, and final residues must be cross-checked in an
   independent dependency-free verifier.
8. **Admissibility.** Verify primality and distinctness; coprimality with
   `2*7*433`; `ell=1 mod 7`; primitivity of `eta`; and
   \[
     a_\ell(E^{(D_q)})=(D_q/\ell)a_\ell(E)
       \equiv\ell+1\pmod7.
   \]
   If the packet also asserts a root number, transverse Selmer switch,
   Tamagawa condition, residual-image condition, ordinarity, nonanomalousness,
   local torsion, or Kurihara primitivity, each must have a separately named
   exact witness.  They must not be inferred from the collision itself.

## Reproducible producer

The producer should be a pinned PARI/GP script, following the exact-symbol
pattern of `cycle135_433a1_kurihara.gp`:

```text
E_q = exact global minimal model of E^(D_q)
[M_q,x_q] = msfromell(E_q,1)
for a=1..ell-1:
    s_a = mseval(M_q,x_q,[oo,a/ell])
    require 7 does not divide denominator(s_a)
    j_a = znlog(Mod(a,ell),Mod(eta,ell)) % 7
    emit q,a,numerator(s_a),denominator(s_a),j_a
emit exact grouped sums and sum_a (s_a mod 7)*j_a mod 7
```

Pin the PARI/GP release and the elliptic-curve/modular-symbol data package if
separate.  The script must fail closed on model, conductor, primitive-root,
integrality, row-count, grouped-sum, or expected-residue mismatch.  Printed
terminal output without the producer and raw exact rows is not reproducible.

## Independent verification layers

The final packet has three logically separate checks.

- **Arithmetic replay:** rerun the pinned producer and compare byte hashes of
  raw exact rows and grouped outputs.
- **Dependency-free reduction:** parse the committed integers, check all
  denominators modulo seven, recompute the seven grouped sums and both `c`
  residues, and require exactly one residue to vanish.
- **Galois verification:** independently validate the field representation,
  unramifiedness, both Frobenius witnesses, and conjugacy in `Gal(L'/Q)`.

The second layer verifies the reduction of supplied modular symbols but cannot
establish that those rationals are the true symbols.  The first layer supplies
that dependency.  Neither layer verifies the Frobenius claim; that is the
third layer.  A certificate is accepted only if all three pass.

## Missing inputs for this cycle

The Cycle 181 report supplies none of `L`, `ell`, `q_0`, `q_1`, raw symbol
rows, exact output hashes, or class-separating Frobenius witnesses.  Therefore
there is presently no exact `q` collision to persist or verify.  The next
bounded computation is to choose one explicitly represented candidate `L`,
search at fixed `ell`, and commit the first complete packet satisfying this
specification.

No BSD case, density theorem, or finite-governance nonfactorization theorem is
claimed.
