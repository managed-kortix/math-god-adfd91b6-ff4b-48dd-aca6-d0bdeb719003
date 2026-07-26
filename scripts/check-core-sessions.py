#!/usr/bin/env python3
"""Fail-closed audit of the exactly-three autonomous research roots."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "CORE_SESSIONS.json"


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--strict-running",
        action="store_true",
        help="require every registered core to report running",
    )
    args = parser.parse_args()

    registry = json.loads(REGISTRY.read_text())
    cores = registry.get("cores", [])
    if len(cores) != 3:
        raise SystemExit(f"registry must contain exactly three cores, found {len(cores)}")
    ids = [core["session_id"] for core in cores]
    if len(set(ids)) != 3:
        raise SystemExit("registered core session IDs are not unique")

    sessions = json.loads(run("kortix", "sessions", "status", "--all", "--json"))
    by_id = {session["session_id"]: session for session in sessions}
    failures: list[str] = []
    report = []
    for core in cores:
        session = by_id.get(core["session_id"])
        if not session:
            failures.append(f"missing registered {core['lane']} core {core['session_id']}")
            continue
        if session.get("agent") != "math-god":
            failures.append(f"{core['lane']} core is agent {session.get('agent')!r}")
        if session.get("name") != core["name"]:
            failures.append(
                f"{core['lane']} core name is {session.get('name')!r}, "
                f"expected {core['name']!r}"
            )
        if args.strict_running and session.get("status") != "running":
            failures.append(f"{core['lane']} core status is {session.get('status')!r}")
        report.append({
            "lane": core["lane"],
            "session_id": core["session_id"],
            "expected_name": core["name"],
            "actual_name": session.get("name"),
            "status": session.get("status"),
            "agent": session.get("agent"),
        })

    extra_math_roots = [
        session for session in sessions
        if session.get("status") == "running"
        and session.get("agent") == "math-god"
        and session.get("session_id") not in ids
    ]
    if extra_math_roots:
        failures.append(
            "unregistered running math-god roots: "
            + ", ".join(session["session_id"] for session in extra_math_roots)
        )

    print(json.dumps({
        "registered_cores": report,
        "extra_running_math_god_roots": extra_math_roots,
        "ordinary_running_sessions": [
            {key: session.get(key) for key in ("session_id", "name", "agent", "status")}
            for session in sessions
            if session.get("status") == "running" and session.get("agent") != "math-god"
        ],
        "ok": not failures,
        "failures": failures,
    }, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
