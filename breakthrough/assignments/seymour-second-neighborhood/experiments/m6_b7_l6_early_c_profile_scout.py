#!/usr/bin/env python3
"""Reproduce the scout classification of the 58 uncertified early C orbits."""

import argparse
import hashlib
import json
from pathlib import Path

import m6_b7_l6_early_c_profile_census as census

HERE = Path(__file__).resolve().parent
SCHEMA = "m6-b7-l6-early-c-profile-scout-v1"
STATE_SCOUT = HERE / "m6-b7-l6-state-scout-30s.json"
HARD_SCOUT = HERE / "m6-b7-l6-hard-orbit-scout-20s.json"


def load_json(path):
    return json.loads(path.read_text(encoding="ascii"))


def payload():
    orbits = census.load_orbits()
    manifest = census.manifest_payload(orbits)
    state = load_json(STATE_SCOUT)
    hard = load_json(HARD_SCOUT)
    sequence = census.scout_sequence(orbits)
    if state.get("manifest_sha256") != census.SOURCE_IDENTITIES["state-manifest"][1]:
        raise RuntimeError("state scout is not bound to the frozen state manifest")
    state_rows = {row["leaf"]: row for row in state["rows"]}
    hard_rows = {(row["state_leaf"], row["intersection_t"]): row for row in hard["rows"]}
    rows = []
    sequence_by_orbit = {item[0]: item[1:] for item in sequence}
    for ordinal, orbit in enumerate(orbits):
        if ordinal in census.CERTIFIED:
            continue
        _, state_ordinal, state_key, _, intersection, _, _, members = orbit
        state_row = state_rows[state_ordinal]
        if state_row["status"] == "UNSAT":
            status, source = "UNSAT", "state-scout-observed-within-20s"
            source_cnf = state_row["cnf_sha256"]
        else:
            hard_row = hard_rows.get((state_ordinal, intersection))
            if hard_row is None:
                raise RuntimeError(f"missing hard scout row for orbit {ordinal}")
            status, source = hard_row["status"], "hard-orbit-scout-20s"
            source_cnf = hard_row["cnf_sha256"]
        rows.append({"orbit": ordinal, "key": orbit[0], "state": state_ordinal,
                     "state_key": state_key, "intersection_t": intersection,
                     "parents": len(members), "status": status, "source": source,
                      "source_cnf_sha256": source_cnf})
        if (status, source, source_cnf) != sequence_by_orbit[ordinal]:
            raise RuntimeError("scout projection differs from producer status sequence")
    if len(rows) != 58 or {row["orbit"] for row in rows} != set(range(60)) - {34, 35}:
        raise RuntimeError("scout is not exactly the 58 uncertified orbits")
    return {"schema": SCHEMA, "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
            "excluded_certified_orbits": [34, 35], "orbit_31_certified": False,
            "seconds_per_orbit": 20, "scout_unsat": 31, "scout_timeout": 27,
            "scout_sat": 0, "total_eliminated_including_certified": 33,
            "status_sequence_sha256": hashlib.sha256(census.scout_sequence_payload(sequence)).hexdigest(),
            "state_scout_bytes": STATE_SCOUT.stat().st_size,
            "state_scout_sha256": hashlib.sha256(STATE_SCOUT.read_bytes()).hexdigest(),
            "hard_scout_bytes": HARD_SCOUT.stat().st_size,
            "hard_scout_sha256": hashlib.sha256(HARD_SCOUT.read_bytes()).hexdigest(),
            "rows": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    data = payload()
    raw = (json.dumps(data, sort_keys=True, indent=2) + "\n").encode("ascii")
    if args.output:
        args.output.write_bytes(raw)
    if args.check and args.check.read_bytes() != raw:
        raise RuntimeError("scout artifact differs from exact reproduction")
    counts = {status: sum(row["status"] == status for row in data["rows"])
              for status in sorted({row["status"] for row in data["rows"]})}
    print(f"PASS scout=58 counts={counts} orbit31_certified=false sha256={hashlib.sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()
