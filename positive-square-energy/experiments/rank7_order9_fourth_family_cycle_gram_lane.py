#!/usr/bin/env python3
"""Exact typed SOS/cycle-space Gram lane for the fourth order-nine family."""

from __future__ import annotations

from pathlib import Path

import rank7_order9_next_family_cycle_gram_lane as lane

HERE = Path(__file__).resolve().parent


def main():
    lane.PRIOR_REPORT = HERE / "rank7_order9_third_family_cycle_gram_lane.json"
    lane.OUTPUT = HERE / "rank7_order9_fourth_family_cycle_gram_lane.json"
    lane.OWNER_STREAM = HERE / "rank7_order9_fourth_family_cycle_gram_owners.jsonl.xz"
    lane.SCHEMA = "rank-seven-order-nine-fourth-family-cycle-gram-lane-v1"
    lane.SCOPE = "exact typed SOS/cycle-space Gram ownership of the fourth-largest after-SOS family"
    lane.TARGET = ((2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1), (4, 3, 5), 4, 2)
    lane.EXPECTED_TARGET_TOTAL = 16183
    lane.EXPECTED_PRIOR_REMAINDER = 269743
    lane.main()


if __name__ == "__main__":
    main()
