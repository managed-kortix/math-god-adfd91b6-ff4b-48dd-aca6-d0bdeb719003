#!/usr/bin/env python3
"""Focused entry point for the base-owner precedence bridge's hostile audit."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
BRIDGE_PATH = HERE.parent / "rank7_order8_typed_precedence_bridge.py"

spec = importlib.util.spec_from_file_location("typed_precedence_bridge_tested", BRIDGE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load typed precedence bridge")
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)

result = bridge.audit(hostile=True)
if result["status"] != "passed":
    raise RuntimeError("bridge did not pass")
if result["boundary_rescue_total"] != bridge.BOUNDARY_RESCUE_TOTAL:
    raise RuntimeError("boundary rescue total changed")
if result["boundary_remainder_total"] != bridge.BOUNDARY_REMAINDER_TOTAL:
    raise RuntimeError("boundary remainder total changed")
if result["hostile_mutations_rejected"] != 15:
    raise RuntimeError("hostile mutation suite did not run completely")
result["status"] = "PASS"
print(json.dumps(result, sort_keys=True, separators=(",", ":")))
