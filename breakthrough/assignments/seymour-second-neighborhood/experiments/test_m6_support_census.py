#!/usr/bin/env python3
"""Regression tests for the frozen six-edge support census."""

import os
import subprocess

HERE = os.path.dirname(__file__)
PAYLOAD = os.path.join(HERE, "m6-support-census.txt")

commands = [
    ["python3", os.path.join(HERE, "m6_support_census.py"), "--check", PAYLOAD],
    ["python3", os.path.join(HERE, "check_m6_support_census.py"), PAYLOAD],
]
for command in commands:
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0, (command, result.stdout, result.stderr)
    print(result.stdout.strip())
print("PASS m6 support census")
