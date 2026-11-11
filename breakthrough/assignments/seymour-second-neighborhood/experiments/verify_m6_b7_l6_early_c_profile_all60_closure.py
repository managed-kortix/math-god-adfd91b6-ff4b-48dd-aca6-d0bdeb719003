#!/usr/bin/env python3
"""Compose certified packages and prove all 60 early C-profile cells closed."""

import argparse
import hashlib
from pathlib import Path
import subprocess
import sys

import check_m6_b7_l6_early_c_profile_census as census_check
import verify_m6_b7_l6_c_to_b_31_orbit_certificates as direct
import verify_m6_b7_l6_early_c_profile_scout_unsat_certificates as fast
import verify_m6_b7_l6_early_c_profile_remaining_scout_unsat_certificates as remaining
import verify_m6_b7_l6_exact_pair_hall_cardinality_strengthening_certificates as one_high_cert
import verify_m6_b7_l6_one_high_profile_closure as one_high
import verify_m6_b7_l6_two_high_profile_root_cardinality_certificates as two_high

HERE = Path(__file__).resolve().parent
DIRECT = {34, 35}
ONE_HIGH = {3, 11, 23, 25, 28, 47, 49, 54}
TWO_HIGH = {12, 13, 14, 15, 16, 17, 36, 37, 38, 39, 40, 41, 42, 43, 55, 56, 57, 58, 59}
FAST = set(fast.SCOPE)
REMAINING = set(remaining.SCOPE)


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def metadata(path):
    result = {}
    for line in path.read_text(encoding="ascii").splitlines()[1:]:
        fields = line.split("\t")
        if fields[0] == "columns":
            break
        if len(fields) == 2:
            result[fields[0]] = fields[1]
    return result


def audit():
    packages = (FAST, REMAINING, DIRECT, ONE_HIGH, TWO_HIGH)
    if any(packages[i] & packages[j] for i in range(len(packages)) for j in range(i + 1, len(packages))):
        raise RuntimeError("closure package scopes overlap")
    if set().union(*packages) != set(range(60)) or tuple(sorted(TWO_HIGH)) != two_high.producer.SCOPE:
        raise RuntimeError("closure package scopes do not exhaust 60 profiles")
    fast_meta = metadata(fast.LEDGER)
    remaining_meta = metadata(remaining.LEDGER)
    direct_meta = metadata(HERE / "m6-b7-l6-c-to-b-31-orbit-certificates.tsv")
    if fast_meta.get("scope-orbits") != ",".join(f"{i:02d}" for i in fast.SCOPE) or \
            remaining_meta.get("scope-orbits") != ",".join(f"{i:02d}" for i in remaining.SCOPE) or \
            direct_meta.get("scope") != "frozen-B7-l6-ordered-C-to-B-(3,1)-only":
        raise RuntimeError("direct certificate package scope changed")
    one_bound, one_rows = one_high_cert.load_ledger()
    one_high_cert.verify_bindings(one_bound)
    one_high_cert.artifact_paths(one_rows)
    two_bound, two_rows = two_high.load_ledger()
    two_high.verify_bindings(two_bound)
    two_high.artifact_paths(two_rows)
    orbits = census_check.derive()
    parents = {member[0] for orbit in orbits for member in orbit[7]}
    states = {orbit[1] for orbit in orbits}
    incidences = sum(len(orbit[7]) for orbit in orbits)
    if len(orbits) != 60 or len(parents) != 42 or len(states) != 30 or incidences != 544:
        raise RuntimeError("independent parent/state/orbit census changed")
    for orbit in orbits:
        census_check.check_parent_support_closure(orbit[7])
    census_manifest = HERE / "m6-b7-l6-early-c-profile-census.tsv"
    expected_census = (10271, "985a558c3b831994ed2febbb3e4569cf7df4869919f897c3ab6e0e96dbdce5f9")
    if identity(census_manifest) != expected_census:
        raise RuntimeError("authoritative census identity changed")
    print("PASS closure=60/60 packages=31+2+8+19 disjoint=yes exhaustive=yes")
    print("PASS parents=42 states=30 orbits=60 orbit_parent_incidences=544 S7_permutations=5040")
    print("PASS implication=entire-clean-B7-l6-parent-campaign-closed other-residual-B7-groups=not-claimed")


def replay(checker):
    commands = (
        [sys.executable, str(fast.__file__), "--checker", str(checker)],
        [sys.executable, str(remaining.__file__), "--checker", str(checker)],
        [sys.executable, str(direct.__file__), "--checker", str(checker)],
        [sys.executable, str(one_high_cert.__file__), "--checker", str(checker)],
        [sys.executable, str(two_high.__file__), "--checker", str(checker)],
    )
    for command in commands:
        subprocess.run(command, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checker", type=Path)
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    audit()
    if args.replay:
        if args.checker is None:
            parser.error("--replay requires --checker")
        replay(args.checker.resolve(strict=True))
        audit()


if __name__ == "__main__":
    main()
