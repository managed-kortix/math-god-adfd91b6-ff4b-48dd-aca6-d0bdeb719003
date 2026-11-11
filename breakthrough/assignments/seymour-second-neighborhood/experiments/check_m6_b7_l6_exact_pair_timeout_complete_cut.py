#!/usr/bin/env python3
"""Independent semantic checker for the frozen TIMEOUT complete-cut census."""

import argparse
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import check_m6_b7_l6_early_c_certificate_residual_exact_pair_singleton_parent as source
import m6_b7_l6_early_c_inaccessible_pair_orbits as pair_source
import m6_b7_l6_exact_pair_timeout_complete_cut as producer

HERE = Path(__file__).resolve().parent
CENSUS = HERE / f"{producer.PREFIX}.tsv"
SCOUT = HERE / f"{producer.PREFIX}-scout-10s.json"
A = frozenset(range(9))
B = frozenset(range(9, 16))
C = frozenset((16, 17))


def derive():
    _, memberships = source.derive()
    statuses = source.json.loads(source.SCOUT.read_text(encoding="ascii"))["rows"]
    rows = []
    for status in statuses:
        if status["status"] != "TIMEOUT":
            continue
        ordinal = status["membership"]
        cell, (_, child), parent = memberships[ordinal]
        profile = child[2]
        low = pair_source.low_vertex(profile[3])
        holes = source.independent_projection(child, parent)
        pair = frozenset(child[3])
        nonout = pair_source.nonoutneighbors(low, profile[3], profile[5], holes)
        out = frozenset(range(18)) - {low} - nonout
        forced, loads = [], []
        for endpoint in sorted(pair):
            load = 0
            for target in sorted(out):
                hole = tuple(sorted((endpoint, target))) in holes
                load += hole
                if not hole:
                    forced.append((endpoint, target))
            loads.append(load)
        low_load = sum(tuple(sorted((low, v))) in holes for v in range(18) if v != low)
        pair_hole = int(tuple(sorted(pair)) in holes)
        other_load = 6 - low_load - sum(loads) - pair_hole
        if ordinal == 0:
            key, epsilon, b_count, chi = "exceptional-membership000", "-", "-", "-"
        else:
            a = tuple(pair & A)
            c = tuple(pair & C)
            if len(a) != 1 or len(c) != 1:
                raise RuntimeError("independent A-C packet classification failed")
            epsilon = pair_hole
            b_count = len(out & B)
            chi = loads[sorted(pair).index(c[0])]
            key = f"epsilon{epsilon}-b{b_count}-chi{chi}"
        rows.append({"membership": ordinal, "cell": cell, "profile": child[1],
                     "parent": parent, "low": low, "pair": tuple(sorted(pair)),
                     "out": tuple(sorted(out)), "forced": tuple(forced), "loads": tuple(loads),
                     "low_load": low_load, "pair_hole": pair_hole, "other_load": other_load,
                     "epsilon": epsilon, "b": b_count, "chi": chi, "class": key})
    return tuple(rows)


def check(path=CENSUS):
    rows = derive()
    expected = producer.payload(rows)
    actual = path.read_bytes()
    if actual != expected:
        raise RuntimeError("complete-cut census differs from independent reconstruction")
    if len(rows) != 33 or Counter(row["class"] == "exceptional-membership000" for row in rows) != Counter({False: 32, True: 1}):
        raise RuntimeError("33/32/1 scope identity failed")
    for row in rows:
        holes_in_support = sum(row["loads"])
        if len(row["forced"]) != 2 * len(row["out"]) - holes_in_support:
            raise RuntimeError("forced complete-cut cardinality failed")
        if row["low_load"] + holes_in_support + row["pair_hole"] + row["other_load"] != 6:
            raise RuntimeError("independent hole-load identity failed")
    classes = defaultdict(list)
    for row in rows:
        classes[row["class"]].append(row["membership"])
    print(f"PASS memberships=33 A_C_packets=32 classes={len(classes)} "
          f"sha256={hashlib.sha256(actual).hexdigest()}")


def check_scout(path=SCOUT):
    semantic = derive()
    raw = path.read_bytes()
    data = json.loads(raw.decode("ascii"))
    if raw != (json.dumps(data, sort_keys=True, indent=2) + "\n").encode("ascii"):
        raise RuntimeError("ten-second scout is not canonical ASCII JSON")
    census_data = producer.payload(semantic)
    expected_header = {"schema": f"{producer.PREFIX}-scout-v1",
                       "seconds_per_membership": 10, "jobs": 2,
                       "solver": source.SOLVER_PATH,
                       "solver_bytes": source.SOLVER_IDENTITY[0],
                       "solver_sha256": source.SOLVER_IDENTITY[1],
                       "solver_version": source.SOLVER_IDENTITY[2],
                       "census_bytes": len(census_data),
                       "census_sha256": hashlib.sha256(census_data).hexdigest()}
    if any(data.get(key) != value for key, value in expected_header.items()) or \
            set(data) != set(expected_header) | {"status_sequence_sha256", "rows"}:
        raise RuntimeError("ten-second scout provenance differs")
    memberships = source.derive()[1]
    singleton_hashes = source.load_hashes()
    rows = data["rows"]
    if len(rows) != len(semantic):
        raise RuntimeError("ten-second scout scope is not exhaustive")
    for position, (record, row) in enumerate(zip(semantic, rows)):
        member = memberships[record["membership"]]
        expected = {"membership": record["membership"], "class": record["class"],
                    "job": position % 2,
                    "cnf_sha256": singleton_hashes[source.producer.membership_key(member)][1]}
        if set(row) != set(expected) | {"status", "seconds"} or any(
                row.get(key) != value for key, value in expected.items()):
            raise RuntimeError(f"ten-second scout row differs: {position}")
        seconds = row.get("seconds")
        if row.get("status") not in ("SAT", "UNSAT", "TIMEOUT") or \
                isinstance(seconds, bool) or not isinstance(seconds, (int, float)) or \
                not math.isfinite(seconds) or (row["status"] == "TIMEOUT" and not 10 <= seconds <= 11) or \
                (row["status"] != "TIMEOUT" and not 0 <= seconds < 10):
            raise RuntimeError(f"invalid ten-second status/timing: {position}")
    sequence = "".join({"SAT": "S", "UNSAT": "U", "TIMEOUT": "T"}[row["status"]]
                       for row in rows)
    digest = hashlib.sha256(sequence.encode("ascii")).hexdigest()
    totals = Counter(row["status"] for row in rows)
    if data["status_sequence_sha256"] != digest:
        raise RuntimeError("ten-second status sequence hash differs")
    print(f"PASS scout totals={dict(sorted(totals.items()))} status_sha256={digest} "
          f"scout_sha256={hashlib.sha256(raw).hexdigest()}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("census", type=Path, nargs="?", default=CENSUS)
    parser.add_argument("--scout", action="store_true")
    args = parser.parse_args()
    check(args.census)
    if args.scout:
        check_scout()


if __name__ == "__main__":
    main()
