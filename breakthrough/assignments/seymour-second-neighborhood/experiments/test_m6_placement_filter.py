#!/usr/bin/env python3
"""Regression test for the frozen m=6 placement-only filter ledger."""

import subprocess
import sys
from pathlib import Path

from check_m6_placement_filter import exact_c_degrees
from m6_placement_filter import c_degree_feasible, classify, load_cover

HERE = Path(__file__).resolve().parent
LEDGER = HERE / "m6-placement-filter.txt"
COMMANDS = (
    [sys.executable, str(HERE / "m6_placement_filter.py"), "--check", str(LEDGER)],
    [sys.executable, str(HERE / "check_m6_placement_filter.py"), str(LEDGER)],
)

rows = load_cover(HERE / "m6-placement-cover.txt")
branch, support, word, holes = rows[17]
if not (branch == "B6" and support == 0 and word == "BCCC" and len(holes) == 6):
    raise RuntimeError("frozen row 17 is no longer B6 support 0 BCCC K4")
if not c_degree_feasible(branch, word, holes):
    raise RuntimeError("producer rejects feasible row 17 B6 BCCC K4")
if not exact_c_degrees(branch, word, holes):
    raise RuntimeError("independent checker rejects feasible row 17 B6 BCCC K4")
if classify(branch, word, holes) != 0:
    raise RuntimeError("row 17 B6 BCCC K4 must be accepted")
print("PASS row=17 branch=B6 placement=BCCC support=K4 feasible")

branch, support, word, holes = rows[0]
if not (branch == "B6" and support == 0 and word == "RBBB"):
    raise RuntimeError("frozen row 0 is no longer B6 support 0 RBBB")
if c_degree_feasible(branch, word, holes) or exact_c_degrees(branch, word, holes):
    raise RuntimeError("three hole-isolated C vertices and their present pairs were omitted")
print("PASS row=0 hole-isolated-C vertices included and present C pairs oriented")

for command in COMMANDS:
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError((command, result.stdout, result.stderr))
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())
print("PASS m6 placement-only filter")
