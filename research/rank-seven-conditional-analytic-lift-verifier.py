#!/usr/bin/env python3
"""Fail-closed contract audit for the conditional rank-seven analytic lift."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROOF = (ROOT / "positive-square-energy/heptacyclic-general"
         / "rank-seven-single-block-structural-theorem.md")
PROOF_SHA256 = "f1daf9109f4843aa2db149c974fb21c847bb6f8144275201aebabed7fe4ea516"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def audit():
    raw = PROOF.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == PROOF_SHA256,
            "analytic lift proof digest changed")
    text = raw.decode("ascii")
    required = (
        "2<=|V(K)|<=12",
        "F(c)={c} union {c+2e_i:1<=i<=p}.",
        "excess at most six",
        "s^+(G)>=|V(G)|`.",
        "claim that the resulting finite rank-seven ledger has been enumerated or",
    )
    require(all(fragment in text for fragment in required),
            "conditional lift contract text changed")
    return {
        "schema": "rank-seven-conditional-analytic-lift-v1",
        "evidence_kind": "conditional-analytic-implication",
        "rank": 7,
        "budget": 6,
        "kernel_orders": [2, 12],
        "finite_premise": (
            "every canonical-plus-coordinate key has an exact budget-six owner"
        ),
        "length_lift": "fixed-parity coordinatewise path lengthening",
        "attachments": "arbitrary finite rooted trees at branch or subdivision vertices",
        "conclusion_if_premise_discharged": "s+(G)>=|V(G)|",
        "finite_premise_discharged": False,
        "global_claim": False,
        "proof_sha256": PROOF_SHA256,
    }


def main():
    try:
        manifest = audit()
    except (OSError, RuntimeError, UnicodeError) as error:
        sys.stderr.write(f"rank-seven conditional analytic lift: FAIL CLOSED: {error}\n")
        return 1
    if "--print-manifest" in sys.argv:
        sys.stdout.write(canonical_bytes(manifest).decode("ascii"))
    sys.stdout.write("rank-seven conditional analytic lift: exact contract audit passed; "
                     "budget=6; global_claim=false; finite_premise_discharged=false\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
