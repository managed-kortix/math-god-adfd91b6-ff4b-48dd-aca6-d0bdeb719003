#!/usr/bin/env python3
"""Exact typed/cycle/effective-resistance Gram lane for the third order-twelve family."""

from pathlib import Path

import rank7_order12_next_family_resistance_gram_lane as lane


HERE = Path(__file__).resolve().parent


def main():
    lane.SOURCE_REPORT = HERE / "rank7_order12_next_family_resistance_gram_lane.json"
    lane.SOURCE_STREAM = HERE / "rank7_order12_after_resistance_gram_remainder.jsonl.xz"
    lane.OUTPUT_PATH = HERE / "rank7_order12_third_family_resistance_gram_lane.json"
    lane.OWNER_STREAM = HERE / "rank7_order12_third_family_resistance_gram_owners.jsonl.xz"
    lane.REMAINDER_STREAM = HERE / "rank7_order12_after_third_family_resistance_gram_remainder.jsonl.xz"
    lane.SCHEMA = "rank-seven-order-twelve-third-family-resistance-gram-lane-v1"
    lane.SCOPE = "full exact typed/cycle/effective-resistance Gram replay of the next-largest unscanned order-twelve family"
    lane.TARGET = ((2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
                   (5, 3, 7), 4, 0, 0)
    lane.EXPECTED_SOURCE_TOTAL = 122473
    lane.EXPECTED_TARGET_TOTAL = 9040
    lane.main()


if __name__ == "__main__":
    main()
