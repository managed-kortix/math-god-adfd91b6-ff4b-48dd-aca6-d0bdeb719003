#!/usr/bin/env python3
"""Compose the 172 pair, prior 68 singleton, and new all33 certificates."""

import hashlib
from pathlib import Path

import m6_b7_l6_early_c_certificate_residual_exact_pair_singleton_parent as singleton
import m6_b7_l6_exact_pair_hall_cardinality_strengthening as cardinality
import verify_m6_b7_l6_exact_pair_hall_cardinality_strengthening_certificates as card_verify

HERE = Path(__file__).resolve().parent
PAIR_LEDGER = HERE / "m6-b7-l6-early-c-inaccessible-pair-scout-unsat-certificates.tsv"
PAIR_RESIDUAL = HERE / "m6-b7-l6-early-c-certificate-residual-exact-pair-orbits.tsv"
SINGLETON_LEDGER = HERE / "m6-b7-l6-early-c-certificate-residual-exact-pair-singleton-parent-scout-unsat-certificates.tsv"
ORBITS = (3, 11, 23, 25, 28, 47, 49, 54)


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


def main():
    bound, rows = card_verify.load_ledger()
    card_verify.verify_bindings(bound)
    card_verify.artifact_paths(rows)
    pair, residual = metadata(PAIR_LEDGER), metadata(PAIR_RESIDUAL)
    if pair.get("cover-children") != "192" or pair.get("certified-children") != "172" or \
            pair.get("scout-timeout") != "20" or residual.get("children") != "20" or \
            residual.get("cell-parent-memberships") != "101":
        raise RuntimeError("pair cover or residual cardinalities changed")
    if identity(PAIR_LEDGER) != (int(residual["certificate-ledger-bytes"]),
                                 residual["certificate-ledger-sha256"]):
        raise RuntimeError("residual cover does not bind the 172-pair ledger")
    prior = {int(value) for value in metadata(SINGLETON_LEDGER)["membership-ordinals"].split(",")}
    _, memberships = singleton.load_memberships()
    new = {row[0]["membership"] for row in cardinality.scope()}
    if len(prior) != 68 or len(new) != 33 or prior & new or prior | new != set(range(101)):
        raise RuntimeError("68+33 singleton subtraction is not disjoint and exhaustive")
    profiles = {memberships[index][1][1][1] for index in prior | new}
    if {member[0] for member in memberships} != set(range(20)) or profiles != set(ORBITS):
        raise RuntimeError("closure does not cover all residual cells/profile orbits")
    counts = {}
    for index, member in enumerate(memberships):
        bucket = counts.setdefault(member[1][1][1], [0, 0])
        bucket[index in new] += 1
    if sum(sum(values) for values in counts.values()) != 101:
        raise RuntimeError("profile accounting double-counted overlapping cover")
    print("PASS pair_cover=192 certified_pair_children=172 exact_residual_children=20")
    print("PASS singleton_memberships=101 prior68=68 new33=33 disjoint=yes exhaustive=yes")
    print("PASS closed_profile_orbits=" + ",".join(f"{value:02d}" for value in ORBITS))
    print("PASS profile_counts=" + ",".join(f"{profile:02d}:{values[0]}+{values[1]}"
                                              for profile, values in sorted(counts.items())))


if __name__ == "__main__":
    main()
