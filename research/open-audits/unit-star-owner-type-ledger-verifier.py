#!/usr/bin/env python3
"""Fail-closed bookkeeping audit for the hostile unit-star center ledger.

This script verifies only the finite owner-type classification.  It does not
re-prove any cited spectral theorem.
"""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NOTE = ROOT / "research/open-audits/unit-star-structural-owner-partition-2026-11-21.md"
R61 = ROOT / "positive-square-energy/heptacyclic-general/r61-one-credit-boundary-reduction.md"
PHYSICAL = ROOT / "positive-square-energy/heptacyclic-general/physical-hull-bridge-reduction/theorem-note.md"


def fail(message: str) -> None:
    raise RuntimeError(message)


def partitions(n: int, cap: int | None = None):
    if type(n) is not int or n < 0:
        fail("partition input must be a nonnegative exact integer")
    if cap is None or cap > n:
        cap = n
    if n == 0:
        yield ()
        return
    for first in range(cap, 0, -1):
        for tail in partitions(n - first, first):
            yield (first,) + tail


EXPECTED = {
    2: {
        (2,): ("SINGLE_BLOCK_R2", "OPEN"),
        (1, 1): ("CACTUS", "CLOSED"),
    },
    3: {
        (3,): ("SINGLE_BLOCK_R3_DIRECT_OR_STRUCT", "OPEN"),
        (2, 1): ("MULTIBLOCK_R21", "OPEN"),
        (1, 1, 1): ("CACTUS", "CLOSED"),
    },
    4: {
        (4,): ("SINGLE_BLOCK_R4_DIRECT_OR_STRUCT", "OPEN"),
        (3, 1): ("MULTIBLOCK_R31", "OPEN"),
        (2, 2): ("MULTIBLOCK_R22", "OPEN"),
        (2, 1, 1): ("MULTIBLOCK_R211", "OPEN"),
        (1, 1, 1, 1): ("CACTUS", "CLOSED"),
    },
    5: {
        (5,): ("SINGLE_BLOCK_R5_DIRECT_OR_STRUCT", "OPEN"),
        (4, 1): ("MULTIBLOCK_R41", "OPEN"),
        (3, 2): ("MULTIBLOCK_R32", "OPEN"),
        (3, 1, 1): ("MULTIBLOCK_R311", "OPEN"),
        (2, 2, 1): ("MULTIBLOCK_R221", "OPEN"),
        (2, 1, 1, 1): ("MULTIBLOCK_R2111", "OPEN"),
        (1, 1, 1, 1, 1): ("CACTUS", "CLOSED"),
    },
    6: {
        (6,): ("SINGLE_BLOCK_R6_DIRECT_OR_K110_K223", "OPEN"),
        (5, 1): ("MULTIBLOCK_R51", "OPEN"),
        (4, 2): ("MULTIBLOCK_R42", "OPEN"),
        (4, 1, 1): ("MULTIBLOCK_R411", "OPEN"),
        (3, 3): ("MULTIBLOCK_R33", "OPEN"),
        (3, 2, 1): ("MULTIBLOCK_R321", "OPEN"),
        (3, 1, 1, 1): ("MULTIBLOCK_R3111", "OPEN"),
        (2, 2, 2): ("MULTIBLOCK_R222", "OPEN"),
        (2, 2, 1, 1): ("MULTIBLOCK_R2211", "OPEN"),
        (2, 1, 1, 1, 1): ("MULTIBLOCK_R21111", "OPEN"),
        (1, 1, 1, 1, 1, 1): ("CACTUS", "CLOSED"),
    },
}

STRUCTURAL_SINGLE_BLOCK = {
    3: {
        "doubled_triangle_111_first_simple",
        "doubled_c4_eight_anchor_first_simple",
        "all_odd_k4_zero_or_one_long",
    },
    4: {"kernel8_two_no_long_states"},
    5: {
        "all_odd_k5e_actual_k4_or_favorable_theta",
        "k22_four_structural_targets",
        "k71_nine_structural_targets",
    },
    6: {"k110_all_unit", "k110_one_long", "k223_canonical_all_unit"},
}

REQUIRED_NOTE_PHRASES = (
    "all physical R61 bridge arms `OPEN`",
    "two distinct bridge endpoints `x,y`",
    "shared-cut DNN gate",
    "counterexample to the proposed owner-partition route",
    "not to `s^+(G)>=|V(G)|`",
)

REQUIRED_PHYSICAL_PHRASES = (
    "qualitative statement `sigma(R)>0` with no numerical lower bound does **not**",
    "Superadditivity yields only",
    "This is a genuinely new analytic obligation.",
)

REQUIRED_STALE_R61_PHRASE = "The cyclic hull contains an actual bridge."
REQUIRED_SHARED_R61_PHRASES = (
    "The hull is bridge-free, `B` and `Q` meet at a shared cut `x`",
    "Exact shared-cut K110 packet",
    "Shared-Gram proof",
)


def validate(registry, structural, note_text, r61_text, physical_text):
    if type(registry) is not dict or type(structural) is not dict:
        fail("registry containers must be exact dictionaries")

    generated = {c: set(partitions(c)) for c in range(2, 7)}
    if set(registry) != set(generated):
        fail("rank-key mismatch")

    total = 0
    closed = 0
    opened = 0
    for c in range(2, 7):
        if set(registry[c]) != generated[c]:
            fail(f"partition-key mismatch at center rank {c}")
        for key, record in registry[c].items():
            if type(key) is not tuple or any(type(x) is not int for x in key):
                fail("partition keys must contain exact integers")
            if type(record) is not tuple or len(record) != 2:
                fail("owner records must be exact pairs")
            owner, disposition = record
            if type(owner) is not str or type(disposition) is not str:
                fail("owner records must contain exact strings")
            expected_disposition = "CLOSED" if all(x == 1 for x in key) else "OPEN"
            if disposition != expected_disposition:
                fail(f"fail-closed disposition mismatch at {(c, key)}")
            if disposition == "CLOSED" and owner != "CACTUS":
                fail("only the cactus owner may close this finite ledger")
            total += 1
            closed += disposition == "CLOSED"
            opened += disposition == "OPEN"

    if (total, closed, opened) != (28, 5, 23):
        fail(f"wrong 28-row split: {(total, closed, opened)}")

    if structural != STRUCTURAL_SINGLE_BLOCK:
        fail("single-block structural-owner registry mismatch")

    for phrase in REQUIRED_NOTE_PHRASES:
        if phrase not in note_text:
            fail(f"note lost required scope phrase: {phrase}")
    for phrase in REQUIRED_PHYSICAL_PHRASES:
        if phrase not in physical_text:
            fail(f"physical-hull dependency lost required warning: {phrase}")
    if REQUIRED_STALE_R61_PHRASE not in r61_text:
        fail("the audited stale R61 sentence was not found")
    for phrase in REQUIRED_SHARED_R61_PHRASES:
        if phrase not in r61_text:
            fail(f"R61 shared-cut artifact missing: {phrase}")

    return total, closed, opened


def hostile_mutations(note_text, r61_text, physical_text):
    attacks = []

    x = copy.deepcopy(EXPECTED)
    del x[4][(2, 1, 1)]
    attacks.append((x, STRUCTURAL_SINGLE_BLOCK, note_text, r61_text, physical_text))

    x = copy.deepcopy(EXPECTED)
    x[6][(6,)] = (x[6][(6,)][0], "CLOSED")
    attacks.append((x, STRUCTURAL_SINGLE_BLOCK, note_text, r61_text, physical_text))

    x = copy.deepcopy(EXPECTED)
    x[2][(2,)] = (x[2][(2,)][0], "CLOSED")
    attacks.append((x, STRUCTURAL_SINGLE_BLOCK, note_text, r61_text, physical_text))

    x = copy.deepcopy(EXPECTED)
    x[3][(1, 1, 1)] = ("DIRECT_DNN", "CLOSED")
    attacks.append((x, STRUCTURAL_SINGLE_BLOCK, note_text, r61_text, physical_text))

    y = copy.deepcopy(STRUCTURAL_SINGLE_BLOCK)
    y[6].remove("k110_one_long")
    attacks.append((EXPECTED, y, note_text, r61_text, physical_text))

    y = copy.deepcopy(STRUCTURAL_SINGLE_BLOCK)
    y[5].add("invented_generic_k4_owner")
    attacks.append((EXPECTED, y, note_text, r61_text, physical_text))

    bad_note = note_text.replace("all physical R61 bridge arms `OPEN`", "all physical R61 bridge arms `CLOSED`", 1)
    attacks.append((EXPECTED, STRUCTURAL_SINGLE_BLOCK, bad_note, r61_text, physical_text))

    bad_note = note_text.replace("counterexample to the proposed owner-partition route", "counterexample to the graph theorem", 1)
    attacks.append((EXPECTED, STRUCTURAL_SINGLE_BLOCK, bad_note, r61_text, physical_text))

    bad_r61 = r61_text.replace(REQUIRED_STALE_R61_PHRASE, "[deleted stale sentence]", 1)
    attacks.append((EXPECTED, STRUCTURAL_SINGLE_BLOCK, note_text, bad_r61, physical_text))

    bad_physical = physical_text.replace(REQUIRED_PHYSICAL_PHRASES[0], "Qualitative strictness suffices.", 1)
    attacks.append((EXPECTED, STRUCTURAL_SINGLE_BLOCK, note_text, r61_text, bad_physical))

    rejected = 0
    for attack in attacks:
        try:
            validate(*attack)
        except RuntimeError:
            rejected += 1
        else:
            fail("hostile mutation was accepted")
    return rejected


def main():
    note_text = NOTE.read_text(encoding="utf-8")
    r61_text = R61.read_text(encoding="utf-8")
    physical_text = PHYSICAL.read_text(encoding="utf-8")

    total, closed, opened = validate(
        EXPECTED, STRUCTURAL_SINGLE_BLOCK, note_text, r61_text, physical_text
    )
    rejected = hostile_mutations(note_text, r61_text, physical_text)

    registry_payload = []
    for c in range(2, 7):
        for key in sorted(EXPECTED[c], reverse=True):
            owner, disposition = EXPECTED[c][key]
            registry_payload.append([c, list(key), owner, disposition])
    digest = hashlib.sha256(
        json.dumps(registry_payload, separators=(",", ":"), sort_keys=False).encode("utf-8")
    ).hexdigest()

    print("unit-star owner-type ledger: ACCEPT")
    print(f"center ranks: 2,3,4,5,6")
    print(f"partition rows: {total} = cactus_closed {closed} + noncactus_open {opened}")
    print("single-block structural ranks: 3,4,5,6")
    print("R61 physical bridge: OPEN; shared-cut packets only")
    print(f"hostile mutations rejected: {rejected}")
    print(f"registry sha256: {digest}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"unit-star owner-type ledger: REJECT: {exc}", file=sys.stderr)
        raise SystemExit(1)
