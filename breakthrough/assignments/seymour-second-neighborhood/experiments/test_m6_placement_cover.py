#!/usr/bin/env python3
"""Exact regression test for the frozen m=6 rooted-cell placement cover."""

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAYLOAD = HERE / "m6-placement-cover.txt"
COMMANDS = [
    [sys.executable, str(HERE / "m6_placement_cover.py"), "--check", str(PAYLOAD)],
    [sys.executable, str(HERE / "check_m6_placement_cover.py"), str(PAYLOAD)],
]

for command in COMMANDS:
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError((command, result.stdout, result.stderr))
    print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())
print("PASS m6 rooted-cell placement cover")
