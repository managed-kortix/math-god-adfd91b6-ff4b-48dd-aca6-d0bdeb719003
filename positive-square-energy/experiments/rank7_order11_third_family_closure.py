#!/usr/bin/env python3
"""Close the two third-family failures by stronger exact rational Grams."""

from pathlib import Path

import rank7_order11_leading_family_closure as closure


HERE = Path(__file__).resolve().parent


def configure():
    closure.SCAN_PATH = HERE / "rank7_order11_third_family_defect_transport_gram_lane.json"
    closure.FAILURES_PATH = HERE / "rank7_order11_third_family_defect_transport_gram_failures.jsonl.xz"
    closure.SOURCE_REMAINDER_PATH = HERE / "rank7_order11_after_third_family_defect_transport_remainder.jsonl.xz"
    closure.OWNER_PATH = HERE / "rank7_order11_third_family_closure_owners.json.xz"
    closure.REMAINDER_PATH = HERE / "rank7_order11_after_third_family_closure_remainder.jsonl.xz"
    closure.REPORT_PATH = HERE / "rank7_order11_third_family_closure.json"
    closure.SCHEMA = "rank-seven-order-eleven-third-family-closure-v1"
    closure.OWNER_SCHEMA = "rank-seven-order-eleven-third-family-stronger-rational-gram-owners-v1"
    closure.RESCUE_OWNER_METHOD = "stronger-direct-spectral-packet-rational-gram"
    closure.EXPECTED_FAILURES = 2
    closure.EXPECTED_FAMILY = 297397
    closure.FAMILY_LABEL = "third"
    closure.STATUS = "third-family-completely-closed"
    closure.SCOPE = "all 297397 rows in the third-largest order-eleven defect-transport family"
    closure.CLAIM_BOUNDARY = "the third-largest 297397-row family is completely theorem-owned; rows outside this family remain in the exact updated global remainder"


def main():
    configure()
    closure.main()


if __name__ == "__main__":
    main()
