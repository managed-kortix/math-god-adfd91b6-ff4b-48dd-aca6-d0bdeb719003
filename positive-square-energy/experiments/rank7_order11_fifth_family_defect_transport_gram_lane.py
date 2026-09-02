#!/usr/bin/env python3
"""Exact cached defect-transport Gram scan of the fifth order-eleven family."""

from pathlib import Path

import rank7_order11_next_family_defect_transport_gram_lane as lane


HERE = Path(__file__).resolve().parent


def main():
    lane.SOURCE_REPORT = HERE / "rank7_order11_fourth_family_defect_transport_gram_lane.json"
    lane.SOURCE_STREAM = HERE / "rank7_order11_after_fourth_family_defect_transport_remainder.jsonl.xz"
    lane.PRIOR_SEGMENT_DIRECTORIES = (
        HERE / "rank7_order11_defect_transport_gram_scan",
        HERE / "rank7_order11_next_family_defect_transport_gram_scan",
        HERE / "rank7_order11_third_family_defect_transport_gram_scan",
        HERE / "rank7_order11_fourth_family_defect_transport_gram_scan",
    )
    lane.EXPECTED_CACHE_SEED_ROWS = 1201173
    lane.OUTPUT = HERE / "rank7_order11_fifth_family_defect_transport_gram_lane.json"
    lane.OWNERS = HERE / "rank7_order11_fifth_family_defect_transport_gram_owners.jsonl.xz"
    lane.FAILURES = HERE / "rank7_order11_fifth_family_defect_transport_gram_failures.jsonl.xz"
    lane.REMAINDER = HERE / "rank7_order11_after_fifth_family_defect_transport_remainder.jsonl.xz"
    lane.SEGMENTS = HERE / "rank7_order11_fifth_family_defect_transport_gram_scan"
    lane.SCHEMA = "rank-seven-order-eleven-fifth-family-defect-transport-gram-lane-v1"
    lane.SCOPE = "full exact cached defect-transport/cycle Gram replay of the fifth-largest order-eleven remainder family"
    lane.PARAMETER_CACHE_DESCRIPTION = "accepted rational parameters keyed by exact local-type signature, seeded from all four complete prior-family scans"
    lane.TARGET = ((2,) + (1,) * 15, (5, 1, 10), 6, 2)
    lane.EXPECTED_SOURCE_TOTAL = 10193464
    lane.EXPECTED_TARGET_TOTAL = 282073
    lane.main()


if __name__ == "__main__":
    main()
