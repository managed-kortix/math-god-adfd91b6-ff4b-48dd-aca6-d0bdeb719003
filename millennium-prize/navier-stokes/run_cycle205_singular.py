#!/usr/bin/env python3
"""Run and log the reproducible Cycle 205 Singular campaign."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[1]
LOG = ROOT / "cycle205_singular.log"
MANIFEST = ROOT / "cycle205_manifest.json"
PRIMES = (32003, 32009, 32027, 32029, 32051)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command):
    completed = subprocess.run(
        command,
        cwd=WORKSPACE,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return completed.returncode, completed.stdout


def main():
    commands = [
        ["python3", "millennium-prize/navier-stokes/generate_cycle204_s2_system.py", "--check"],
        ["python3", "millennium-prize/navier-stokes/generate_cycle205_singular.py", "--check"],
        ["Singular", "-q", "millennium-prize/navier-stokes/cycle205_full_qq.sing"],
    ]
    commands.extend([
        ["Singular", "-q", f"millennium-prize/navier-stokes/cycle205_mod_{prime}.sing"]
        for prime in PRIMES
    ])
    commands.extend([
        ["Singular", "-q", "millennium-prize/navier-stokes/cycle205_reduced_qq.sing"],
        ["Singular", "-q", "millennium-prize/navier-stokes/cycle205_full_certificate_qq.sing"],
    ])

    started = datetime.now(timezone.utc).isoformat()
    sections = [
        "Cycle 205 exact Singular campaign",
        f"started_utc={started}",
        f"host={platform.platform()}",
        "",
    ]
    records = []
    failed = False
    for command in commands:
        returncode, output = run(command)
        command_text = " ".join(command)
        sections.extend([f"$ {command_text}", output.rstrip(), f"exit={returncode}", ""])
        records.append({"command": command, "exit": returncode})
        failed |= returncode != 0

    report = ROOT / "cycle-205-singular-unit-ideal.md"
    artifacts = sorted(
        [INPUT for INPUT in (ROOT / "cycle204_s2_equations.json", ROOT / "cycle204_s2_support.json")]
        + list(ROOT.glob("cycle205_*.sing"))
        + [ROOT / "cycle205_linear_reduction.json", Path(__file__).resolve(), ROOT / "generate_cycle205_singular.py", report]
    )
    manifest = {
        "schema": "cycle205-singular-manifest-v1",
        "started_utc": started,
        "host": platform.platform(),
        "commands": records,
        "artifacts": [
            {
                "path": str(path.relative_to(WORKSPACE)),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in artifacts
        ],
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="ascii")
    sections.extend([
        "manifest_sha256=" + sha256(MANIFEST),
        f"completed_utc={datetime.now(timezone.utc).isoformat()}",
        "status=" + ("FAIL" if failed else "PASS"),
    ])
    LOG.write_text("\n".join(sections) + "\n", encoding="ascii")
    print(f"wrote {LOG.name} sha256={sha256(LOG)}")
    print(f"wrote {MANIFEST.name} sha256={sha256(MANIFEST)}")
    if failed:
        raise SystemExit("Cycle 205 campaign failed; inspect log")


if __name__ == "__main__":
    main()
