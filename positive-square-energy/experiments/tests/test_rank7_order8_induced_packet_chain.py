#!/usr/bin/env python3
"""Fast hostile identity tests for order-eight packet lanes VII--XI."""

from __future__ import annotations

import hashlib
import importlib.util
import lzma
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
if str(EXPERIMENTS) not in sys.path:
    sys.path.insert(0, str(EXPERIMENTS))

ORDINALS = ("seventh", "eighth", "ninth", "tenth", "eleventh")
EXPECTED = {
    "seventh": (76085, 6817, 69268),
    "eighth": (69268, 4219, 65049),
    "ninth": (65049, 3765, 61284),
    "tenth": (61284, 2731, 58553),
    "eleventh": (58553, 2167, 56386),
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(ordinal):
    path = EXPERIMENTS / f"rank7_order8_{ordinal}_induced_packet_gram_family.py"
    spec = importlib.util.spec_from_file_location(f"audit_{ordinal}", path)
    require(spec is not None and spec.loader is not None, f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def raw_identity(module, info, label):
    path = EXPERIMENTS / info["path"]
    require(module.lane.file_sha256(path) == info["artifact_sha256"],
            f"{label} compressed digest changed")
    digest = hashlib.sha256()
    total = 0
    with lzma.open(path, "rb") as stream:
        for raw in stream:
            payload = module.structural.strict_json(raw, path.name)
            require(raw == module.lane.canonical_bytes(payload),
                    f"{label} has noncanonical row")
            digest.update(raw)
            total += 1
    require(total == info["record_total"] and digest.hexdigest() == info["raw_sha256"],
            f"{label} raw identity changed")


def main():
    previous_remainder = None
    for ordinal in ORDINALS:
        module = load(ordinal)
        raw = module.OUTPUT.read_bytes()
        report = module.structural.strict_json(raw, module.OUTPUT.name)
        require(raw == module.lane.canonical_bytes(report), f"{ordinal} report noncanonical")
        source, target, remainder = EXPECTED[ordinal]
        require(report["full_theorem"] is True and
                report["scanned_remainder_total"] == source and
                report["owned_orbit_total"] == target and
                report["remaining_target_family_total"] == 0 and
                report["remaining_remainder_total"] == remainder,
                f"{ordinal} theorem counts changed")
        require(report["owned_target_total"] == 15 * target,
                f"{ordinal} target multiplier changed")
        require(report["source_report"]["path"] == module.SOURCE_REPORT.name and
                report["source_report"]["sha256"] ==
                hashlib.sha256(module.SOURCE_REPORT.read_bytes()).hexdigest(),
                f"{ordinal} source report changed")
        if previous_remainder is not None:
            require(module.SOURCE_STREAM == previous_remainder,
                    f"{ordinal} chain link changed")
        raw_identity(module, report["owner_stream"], f"{ordinal} owners")
        raw_identity(module, report["reduced_remainder_stream"], f"{ordinal} remainder")
        previous_remainder = module.REMAINDER
    print("rank7 order8 packet chain hostile identity audit: PASS")


if __name__ == "__main__":
    main()
