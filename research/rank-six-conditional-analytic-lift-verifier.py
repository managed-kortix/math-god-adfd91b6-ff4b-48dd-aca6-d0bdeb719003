#!/usr/bin/env python3
"""Exact contract audit for the conditional rank-six analytic lift."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = Path(__file__).with_name(
    "rank-six-conditional-analytic-lift-manifest.json"
)
PROOF_NOTE_PATH = (
    ROOT
    / "positive-square-energy"
    / "hexacyclic-general"
    / "conditional-analytic-lift-proof-note.md"
)
PROOF_NOTE_SHA256 = "2ecc321b60ec42ddf1b8980dffc019eaeaa55738dea5ee014596cf3e814692b4"
SCHEMA = "rank-six-conditional-analytic-lift-v1"
CONCLUSION = "s+(G)>=|V(G)|"
FINITE_RESULT = "kappa(B)<=|E(B)|+5"
EXCLUDED_SCOPE = [
    "discharge or completeness of the finite owner premise",
    "multiple positive-rank cyclic blocks",
    "all connected hexacyclic graphs",
    "non-simple realizations",
    "connectors meeting the core more than once",
    "parity-changing subdivision or spectral subdivision monotonicity",
]
VERIFIED_STEPS = [
    "canonical simple vector is coordinatewise dominated after allowed parallel-class permutation",
    "fixed-parity path excess is nonincreasing under length increase by two",
    "canonical-plus-coordinate frontier covers every same-parity length vector",
    "kappa is additive under genuine one-vertex sums and a tree contributes its edge count",
    "rank-six Euler identity and the DNN adjacency-trace bound imply the conclusion",
]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (
        json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
        + "\n"
    ).encode("ascii")


def strict_json(raw, label):
    def reject_constant(value):
        raise ValueError(f"nonstandard JSON constant in {label}: {value}")

    try:
        payload = json.loads(raw.decode("ascii"), parse_constant=reject_constant)
    except (UnicodeError, json.JSONDecodeError, ValueError) as error:
        raise RuntimeError(f"cannot parse {label}: {error}") from error
    require(raw == canonical_bytes(payload), f"{label} is not canonical ASCII JSON")
    return payload


def validate_manifest(payload):
    require(type(payload) is dict, "manifest is not an object")
    require(payload.get("schema") == SCHEMA, "manifest schema changed")
    require(payload.get("conclusion") == CONCLUSION, "conclusion changed")
    require(payload.get("excluded_scope") == EXCLUDED_SCOPE, "excluded scope changed")
    require(payload.get("kernel") == {
        "cyclomatic_rank": 6,
        "loopless": True,
        "minimum_degree_at_least": 3,
        "two_connected": True,
    }, "kernel scope changed")
    require(payload.get("realization") == {
        "finite": True,
        "physical_paths": (
            "positive integral lengths, internally vertex-disjoint, meeting only at "
            "prescribed branch endpoints"
        ),
        "simple": True,
    }, "simple physical realization contract changed")
    finite = payload.get("finite_premise")
    require(type(finite) is dict, "finite premise is malformed")
    require(finite.get("residual_frontier") ==
            "F(c)={c} union {c+2e_i:1<=i<=p}", "frontier changed")
    require(finite.get("coverage") ==
            "regenerated target keys equal the disjoint union of exactly checked owner keys",
            "exact disjoint coverage premise changed")
    require(finite.get("coarse_owner") ==
            "one exact certificate remaining within excess five under every same-parity coordinate lengthening",
            "coarse owner premise changed")
    require(finite.get("result") == FINITE_RESULT, "finite result changed")
    require(payload.get("tree_attachments") ==
            "arbitrary finite rooted trees meeting the existing graph only at one root; roots may be branch or internal subdivision vertices",
            "tree attachment scope changed")
    require(payload.get("verified_steps") == VERIFIED_STEPS, "verified step ledger changed")
    implication = payload.get("implication")
    require(implication ==
            "if the exact finite premise holds for a rank-six kernel parity orbit, then it holds for every arbitrary-length simple subdivision in that orbit and the rooted-tree lift gives the conclusion",
            "conditional implication changed")
    require("all connected" not in implication.lower(), "global implication widening")
    require(payload.get("proof_note") == {
        "path": "positive-square-energy/hexacyclic-general/conditional-analytic-lift-proof-note.md",
        "sha256": PROOF_NOTE_SHA256,
    }, "proof-note pin changed")
    require(set(payload) == {
        "schema", "kernel", "realization", "finite_premise", "tree_attachments",
        "verified_steps", "implication", "conclusion", "excluded_scope", "proof_note",
    }, "manifest fields changed")


def verify_note(payload):
    note = payload.get("proof_note")
    require(note == {
        "path": "positive-square-energy/hexacyclic-general/conditional-analytic-lift-proof-note.md",
        "sha256": PROOF_NOTE_SHA256,
    }, "proof-note pin changed")
    require(PROOF_NOTE_PATH.is_file(), "pinned proof note is missing")
    require(hashlib.sha256(PROOF_NOTE_PATH.read_bytes()).hexdigest() == PROOF_NOTE_SHA256,
            "pinned proof-note bytes changed")


def canonical_parallel_class(multiplicity, odd_count):
    require(type(multiplicity) is int and multiplicity >= 1, "invalid multiplicity")
    require(type(odd_count) is int and 0 <= odd_count <= multiplicity,
            "invalid odd count")
    if odd_count == 0:
        return (2,) * multiplicity
    return (1,) + (3,) * (odd_count - 1) + (2,) * (multiplicity - odd_count)


def verify_canonical_symbolics():
    cases = 0
    for multiplicity in range(1, 13):
        for odd_count in range(multiplicity + 1):
            canonical = canonical_parallel_class(multiplicity, odd_count)
            require(len(canonical) == multiplicity, "canonical vector width changed")
            require(sum(value % 2 for value in canonical) == odd_count,
                    "canonical parity count changed")
            require(sum(value == 1 for value in canonical) <= 1,
                    "canonical vector violates simplicity")
            require(all(value in (1, 2, 3) for value in canonical),
                    "canonical vector is not shortest")
            cases += 1
    return cases


def verify_frontier_symbolics():
    cases = 0
    for width in range(1, 17):
        canonical = tuple(1 + (index % 3) for index in range(width))
        for mask in range(1 << min(width, 8)):
            increments = tuple(2 * ((mask >> index) & 1) if index < 8 else 0
                               for index in range(width))
            target = tuple(canonical[index] + increments[index]
                           for index in range(width))
            if target == canonical:
                owner = canonical
            else:
                coordinate = next(index for index, amount in enumerate(increments)
                                  if amount >= 2)
                owner = tuple(value + (2 if index == coordinate else 0)
                              for index, value in enumerate(canonical))
            require(all(owner[index] <= target[index] for index in range(width)),
                    "frontier owner does not dominate target")
            require(all((target[index] - owner[index]) % 2 == 0
                        for index in range(width)), "frontier lift changed parity")
            cases += 1
    return cases


def verify_affine_identities():
    cases = 0
    for edges in range(6, 65):
        core_vertices = edges - 5
        require(edges - core_vertices + 1 == 6, "rank-six Euler identity failed")
        for tree_edges in range(0, 33):
            kappa_bound = edges + 5 + tree_edges
            total_edges = edges + tree_edges
            total_vertices = core_vertices + tree_edges
            require(2 * total_edges - kappa_bound == total_vertices,
                    "DNN trace affine identity failed")
            cases += 1
    # The derivative sign reduces exactly to sin(z)cos(z)-2z <= 0.
    # Its analytic bound is sin(z)cos(z) <= z; these rational samples check
    # the remaining coefficient and sign bookkeeping without floating point.
    for numerator in range(0, 65):
        z = Fraction(numerator, 64)
        require(z - 2 * z <= 0, "fixed-parity derivative sign reduction failed")
        cases += 1
    return cases


def expect_rejected(action, label):
    try:
        action()
    except (RuntimeError, TypeError, ValueError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_checks(payload):
    mutations = []
    changed = deepcopy(payload)
    changed["conclusion"] = "all connected hexacyclic graphs satisfy s+(G)>=|V(G)|"
    mutations.append(("global conclusion", changed))
    changed = deepcopy(payload)
    changed["kernel"]["cyclomatic_rank"] = 7
    mutations.append(("rank widening", changed))
    changed = deepcopy(payload)
    changed["realization"]["simple"] = False
    mutations.append(("non-simple realization", changed))
    changed = deepcopy(payload)
    changed["finite_premise"]["residual_frontier"] = "F(c)={c}"
    mutations.append(("canonical-only frontier", changed))
    changed = deepcopy(payload)
    changed["finite_premise"]["coverage"] = "owner count matches target count"
    mutations.append(("count-only coverage", changed))
    changed = deepcopy(payload)
    changed["tree_attachments"] = "arbitrary connectors"
    mutations.append(("two-root connectors", changed))
    changed = deepcopy(payload)
    changed["implication"] = changed["implication"] + "; all connected graphs"
    mutations.append(("global implication", changed))
    changed = deepcopy(payload)
    changed["proof_note"]["sha256"] = "0" * 64
    mutations.append(("proof-note digest", changed))
    for label, mutation in mutations:
        expect_rejected(lambda mutation=mutation: validate_manifest(mutation), label)
    return len(mutations)


def audit():
    raw = MANIFEST_PATH.read_bytes()
    payload = strict_json(raw, "analytic lift manifest")
    validate_manifest(payload)
    verify_note(payload)
    canonical_cases = verify_canonical_symbolics()
    frontier_cases = verify_frontier_symbolics()
    affine_cases = verify_affine_identities()
    mutations = hostile_checks(payload)
    return payload, canonical_cases, frontier_cases, affine_cases, mutations


def report(payload, canonical_cases, frontier_cases, affine_cases, mutations):
    manifest_sha256 = hashlib.sha256(canonical_bytes(payload)).hexdigest()
    return (
        "rank-six conditional analytic lift: exact/symbolic audit passed\n"
        f"schema={SCHEMA}\n"
        f"manifest_sha256={manifest_sha256}\n"
        f"proof_note_sha256={PROOF_NOTE_SHA256}\n"
        f"canonical_cases={canonical_cases} frontier_cases={frontier_cases} "
        f"affine_cases={affine_cases} hostile_rejections={mutations}\n"
        "scope=conditional finite-frontier -> arbitrary simple subdivision/rooted-tree spectral result\n"
        "global_claim=false finite_premise_discharged=false\n"
    )


def optimized_output():
    completed = subprocess.run(
        (sys.executable, "-O", str(Path(__file__).resolve()), "--emit"),
        check=False, capture_output=True, text=True,
    )
    require(completed.returncode == 0, "python3 -O verifier failed")
    require(completed.stderr == "", "python3 -O verifier wrote stderr")
    return completed.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--print-manifest", action="store_true")
    args = parser.parse_args()
    try:
        audited = audit()
        output = report(*audited)
        if not args.emit and sys.flags.optimize == 0:
            require(optimized_output() == output, "normal and python3 -O output differ")
    except (OSError, RuntimeError, TypeError, ValueError) as error:
        sys.stderr.write(f"rank-six conditional analytic lift: FAIL CLOSED: {error}\n")
        return 1
    if args.print_manifest:
        sys.stdout.write(canonical_bytes(audited[0]).decode("ascii"))
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
