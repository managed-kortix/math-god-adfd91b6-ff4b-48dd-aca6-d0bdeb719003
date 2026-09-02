#!/usr/bin/env python3
"""Close the sole fourth-family failure by a stronger exact rational Gram."""

import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
ENGINE_PATH = HERE / "rank7_order11_leading_family_closure.py"


def load_engine():
    spec = importlib.util.spec_from_file_location("order11_fourth_closure_engine", ENGINE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load order-eleven closure engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


closure = load_engine()


def configure():
    closure.SCAN_PATH = HERE / "rank7_order11_fourth_family_defect_transport_gram_lane.json"
    closure.FAILURES_PATH = HERE / "rank7_order11_fourth_family_defect_transport_gram_failures.jsonl.xz"
    closure.SOURCE_REMAINDER_PATH = HERE / "rank7_order11_after_fourth_family_defect_transport_remainder.jsonl.xz"
    closure.OWNER_PATH = HERE / "rank7_order11_fourth_family_closure_owners.json.xz"
    closure.REMAINDER_PATH = HERE / "rank7_order11_after_fourth_family_closure_remainder.jsonl.xz"
    closure.REPORT_PATH = HERE / "rank7_order11_fourth_family_closure.json"
    closure.SCHEMA = "rank-seven-order-eleven-fourth-family-closure-v1"
    closure.OWNER_SCHEMA = "rank-seven-order-eleven-fourth-family-stronger-rational-gram-owners-v1"
    closure.RESCUE_OWNER_METHOD = "stronger-direct-spectral-packet-rational-gram"
    closure.EXPECTED_FAILURES = 1
    closure.EXPECTED_FAMILY = 283644
    closure.FAMILY_LABEL = "fourth"
    closure.STATUS = "fourth-family-completely-closed"
    closure.SCOPE = "all 283644 rows in the fourth-largest order-eleven defect-transport family"
    closure.CLAIM_BOUNDARY = "the fourth-largest 283644-row family is completely theorem-owned; rows outside this family remain in the exact updated global remainder"
    closure.PRIOR_CLOSURE_OWNER_PATHS = (
        HERE / "rank7_order11_third_family_closure_owners.json.xz",
    )


def main():
    configure()
    closure.main()


if __name__ == "__main__":
    main()
