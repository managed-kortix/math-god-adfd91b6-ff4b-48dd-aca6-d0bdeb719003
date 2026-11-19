#!/usr/bin/env python3
"""Compose all 53 certified profiles and close all 322 clean B7-l5 parents."""

import argparse
import math
from pathlib import Path
import subprocess
import sys

import check_m6_b7_l5_profile_root_cardinality as census

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def audit():
    import verify_m6_b7_l5_profile_root_cardinality_certificates as certificates

    metadata, rows = certificates.load_ledger()
    certificates.verify_bindings(metadata)
    certificates.artifact_paths(rows)
    certificates.verify_artifact_identities(rows)
    profiles = census.derive()
    if tuple(int(row["position"]) for row in rows) != tuple(range(53)) or len(profiles) != 53:
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
    if len(states) != 30 or len(parents) != 322 or state_parent_incidences != 1920 or \
            sum(len(profile[7]) for profile in profiles) != 3387:
        raise RuntimeError("independent 53-profile/322-parent composition changed")
    print("PASS closure=53/53 profiles disjoint=yes exhaustive=yes")
    print("PASS parents=322 states=30 state_parent_incidences=1920 profiles=53 profile_parent_incidences=3387")
    print("PASS implication=entire-clean-B7-l5-parent-campaign-closed other-residual-groups=not-claimed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checker", type=Path)
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    audit()
    if args.replay:
        if args.checker is None:
            parser.error("--replay requires --checker")
        verifier = HERE / "verify_m6_b7_l5_profile_root_cardinality_certificates.py"
        subprocess.run([sys.executable, str(verifier), "--checker", str(args.checker.resolve(strict=True))], check=True)
        audit()


if __name__ == "__main__":
    main()
