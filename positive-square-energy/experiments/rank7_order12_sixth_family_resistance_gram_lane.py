#!/usr/bin/env python3
"""Exact typed/cycle/effective-resistance Gram lane for the sixth order-twelve family."""

from pathlib import Path

import rank7_order12_next_family_resistance_gram_lane as lane


HERE = Path(__file__).resolve().parent


def main():
    lane.SOURCE_REPORT = HERE / "rank7_order12_fifth_family_resistance_gram_lane.json"
    lane.SOURCE_STREAM = HERE / "rank7_order12_after_fifth_family_resistance_gram_remainder.jsonl.xz"
    lane.OUTPUT_PATH = HERE / "rank7_order12_sixth_family_resistance_gram_lane.json"
    lane.OWNER_STREAM = HERE / "rank7_order12_sixth_family_resistance_gram_owners.jsonl.xz"
    lane.REMAINDER_STREAM = HERE / "rank7_order12_after_sixth_family_resistance_gram_remainder.jsonl.xz"
    lane.SCHEMA = "rank-seven-order-twelve-sixth-family-resistance-gram-lane-v1"
    lane.SCOPE = "full exact typed/cycle/effective-resistance Gram replay of the sixth-largest order-twelve family"
    lane.TARGET = ((2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
                   (7, 3, 5), 4, 1, 0)
    lane.EXPECTED_SOURCE_TOTAL = 122191
    lane.EXPECTED_TARGET_TOTAL = 5976
    lane.main()


if __name__ == "__main__":
    main()
