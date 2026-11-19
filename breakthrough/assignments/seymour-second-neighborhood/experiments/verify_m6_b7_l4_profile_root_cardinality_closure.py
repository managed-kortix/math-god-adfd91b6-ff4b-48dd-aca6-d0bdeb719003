#!/usr/bin/env python3
"""Compose all 40 certified profiles and close all 1,649 clean B7-l4 parents."""

import argparse
import math
from pathlib import Path
import subprocess
import sys

import check_m6_b7_l4_profile_root_cardinality as census

HERE = Path(__file__).resolve().parent


def audit():
    import verify_m6_b7_l4_profile_root_cardinality_certificates as certificates

    metadata, rows = certificates.load_ledger()
    certificates.verify_bindings(metadata)
    certificates.artifact_paths(rows)
    certificates.verify_artifact_identities(rows)
    profiles = census.derive()
    if tuple(int(row["position"]) for row in rows) != tuple(range(40)) or len(profiles) != 40:
        raise RuntimeError("certificate/profile composition scope changed")
    states, orbit_parameters = {}, {}
    for profile in profiles:
        state_ordinal, state, intersection, orbit_size, members = profile[1], profile[3], profile[4], profile[6], profile[7]
        if state_ordinal in states and states[state_ordinal] != members:
            raise RuntimeError("one state has inconsistent parent support")
        states[state_ordinal] = members
        orbit_parameters.setdefault(state_ordinal, []).append((intersection, orbit_size, state[3]))
    for parameters in orbit_parameters.values():
        left, right = parameters[0][2]
        expected = census.independent_orbits(left, right)
        if tuple((t, size) for t, size, _ in parameters) != expected or sum(size for _, size in expected) != \
                math.comb(7, left) * math.comb(7, right):
            raise RuntimeError("one state does not exhaust its exact S7 row-pair orbits")
    parents = {(accepted, cover) for profile in profiles for accepted, cover, _ in profile[7]}
    state_parent_incidences = sum(len(members) for members in states.values())
    if len(states) != 28 or len(parents) != 1649 or state_parent_incidences != 10036 or \
            sum(len(profile[7]) for profile in profiles) != 14464:
        raise RuntimeError("independent 40-profile/1649-parent composition changed")
    print("PASS closure=40/40 profiles disjoint=yes exhaustive=yes")
    print("PASS parents=1649 states=28 state_parent_incidences=10036 profiles=40 profile_parent_incidences=14464")
    print("PASS implication=entire-clean-B7-l4-parent-campaign-closed other-residual-groups=not-claimed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checker", type=Path)
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    audit()
    if args.replay:
        if args.checker is None:
            parser.error("--replay requires --checker")
        verifier = HERE / "verify_m6_b7_l4_profile_root_cardinality_certificates.py"
        subprocess.run([sys.executable, str(verifier), "--checker", str(args.checker.resolve(strict=True))], check=True)
        audit()


if __name__ == "__main__":
    main()
