#!/usr/bin/env python3
"""Focused entry point for the post-XII lane's read-only hostile audit."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
LANE_PATH = EXPERIMENTS / "rank7_order8_post_xii_shared_packet_lane.py"
if str(EXPERIMENTS) not in sys.path:
    sys.path.insert(0, str(EXPERIMENTS))

spec = importlib.util.spec_from_file_location("post_xii_lane_tested", LANE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load post-XII lane")
lane = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lane)

result = lane.audit(hostile=True)
if result["owned"] + result["remaining"] != lane.SOURCE_TOTAL:
    raise RuntimeError("hostile audit partition is incomplete")
if result["hostile_mutations_rejected"] != 11:
    raise RuntimeError("hostile mutation suite did not run completely")
result["status"] = "PASS"
print(json.dumps(result, sort_keys=True, separators=(",", ":")))
