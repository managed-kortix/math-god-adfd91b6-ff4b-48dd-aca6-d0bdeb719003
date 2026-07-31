#!/usr/bin/env python3
"""Fail-closed fixture audit for rank-four kernels 9--12.

This is a finite incidence ledger, not a DNN or numerical certificate.  It
regenerates all physical bundle rows, quotients only by genuine kernel
automorphisms, checks the 282 recorded incidence records, and freezes the exact
list of 96 rows left in the target residual fixture.
"""

import argparse
import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from itertools import combinations, permutations, product
from pathlib import Path


HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "fixtures" / "rank-four-five-vertex-orbits.json"
PAIRS = tuple(combinations(range(5), 2))
PAIR_NAMES = tuple(f"{u}{v}" for u, v in PAIRS)
KERNELS = (
    (0, 0, 1, 2, 1, 0, 2, 2, 0, 0),
    (0, 0, 1, 2, 1, 1, 1, 1, 1, 0),
    (0, 0, 1, 2, 1, 1, 1, 2, 0, 0),
    (0, 1, 1, 1, 1, 1, 1, 0, 1, 1),
)
EXPECTED_PHYSICAL = (108, 192, 144, 256)
EXPECTED_AUTOMORPHISMS = (2, 2, 1, 8)
EXPECTED_ORBITS = (63, 120, 144, 51)
EXPECTED_CERTIFICATES = 282
EXPECTED_RESIDUALS = 96
# Digest of canonical JSON, including its final LF.
EXPECTED_SHA256 = "d43a7c9e1e50a3381043a0c6c5b4ed019c5c858264f0f5b572c5a28a326c8245"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def relabel(row, permutation):
    require(len(row) == len(PAIRS), "row width changed")
    require(tuple(sorted(permutation)) == tuple(range(5)), "invalid permutation")
    lookup = dict(zip(PAIRS, row))
    return tuple(lookup[tuple(sorted((permutation[u], permutation[v])))]
                 for u, v in PAIRS)


def automorphisms(kernel):
    return tuple(permutation for permutation in permutations(range(5))
                 if relabel(kernel, permutation) == kernel)


def physical_rows(kernel):
    return tuple(product(*(range(multiplicity + 1) for multiplicity in kernel)))


def canonical_row(kernel, row):
    return min(relabel(row, permutation) for permutation in automorphisms(kernel))


def bundle_record(kernel, row):
    result = []
    for name, multiplicity, odd in zip(PAIR_NAMES, kernel, row):
        if multiplicity:
            result.append({"edge": name, "multiplicity": multiplicity,
                           "odd": odd, "even": multiplicity - odd})
        else:
            require(odd == 0, "nonedge has nonzero physical incidence")
    return result


def orbit_members(kernel, representative):
    return sorted({relabel(representative, permutation)
                   for permutation in automorphisms(kernel)})


def row_record(kernel_number, kernel, row):
    return {
        "kernel": kernel_number,
        "row": list(row),
        "bundles": bundle_record(kernel, row),
        "automorphism_orbit": [list(member)
                               for member in orbit_members(kernel, row)],
    }


def all_orbit_records():
    all_records = []
    kernel_ledger = []
    for offset, kernel in enumerate(KERNELS):
        kernel_number = offset + 9
        group = automorphisms(kernel)
        rows = physical_rows(kernel)
        representatives = tuple(sorted({canonical_row(kernel, row) for row in rows}))
        kernel_ledger.append({
            "kernel": kernel_number,
            "code": list(kernel),
            "physical_rows": len(rows),
            "automorphisms": len(group),
            "orbits": len(representatives),
        })
        all_records.extend(row_record(kernel_number, kernel, row)
                           for row in representatives)

    return kernel_ledger, all_records


def target_certificate_keys():
    """Return the immutable 282-key incidence table recorded by the fixture."""
    fixture = load_fixture()
    require(fixture.get("schema") == "rank-four-five-vertex-orbit-ledger-v1",
            "cannot read certificate keys from a foreign fixture schema")
    records = fixture.get("incidence_certificates")
    require(isinstance(records, list), "fixture certificate table is malformed")
    keys = tuple((record["kernel"], tuple(record["row"])) for record in records)
    require(len(keys) == EXPECTED_CERTIFICATES and len(set(keys)) == len(keys),
            "fixture certificate-key table is not exact")
    return frozenset(keys)


def regenerate_payload(certificate_keys=None):
    kernel_ledger, all_records = all_orbit_records()
    if certificate_keys is None:
        certificate_keys = target_certificate_keys()

    # Membership in the historical 282-table is immutable fixture data, not a
    # reconstructed mathematical success predicate.  Every stored incidence is
    # nevertheless rebuilt independently from its key.
    certificates = [record for record in all_records
                    if (record["kernel"], tuple(record["row"])) in certificate_keys]
    residuals = [record for record in all_records
                 if (record["kernel"], tuple(record["row"])) not in certificate_keys]
    return {
        "schema": "rank-four-five-vertex-orbit-ledger-v1",
        "scope": "finite incidence fixture only; no numerical certificate claim",
        "pair_order": list(PAIR_NAMES),
        "kernels": kernel_ledger,
        "orbit_total": len(all_records),
        "incidence_certificate_total": len(certificates),
        "residual_total": len(residuals),
        "incidence_certificates": certificates,
        "residuals": residuals,
    }


def serialize(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"


def load_fixture(path=FIXTURE):
    require(path.is_file(), f"missing fixture: {path}")
    with path.open("r", encoding="ascii") as handle:
        value = json.load(handle)
    require(isinstance(value, dict), "fixture root is not an object")
    return value


def audit(payload=None, expected_digest=EXPECTED_SHA256):
    fixture = load_fixture() if payload is None else payload
    generated = regenerate_payload(target_certificate_keys())
    require(fixture == generated, "fixture differs from independent regeneration")
    require(tuple(row["physical_rows"] for row in fixture["kernels"])
            == EXPECTED_PHYSICAL, "physical-row ledger changed")
    require(tuple(row["automorphisms"] for row in fixture["kernels"])
            == EXPECTED_AUTOMORPHISMS, "automorphism ledger changed")
    require(tuple(row["orbits"] for row in fixture["kernels"])
            == EXPECTED_ORBITS, "orbit ledger changed")
    require(fixture["orbit_total"] == sum(EXPECTED_ORBITS) == 378,
            "five-vertex orbit total changed")
    certificates = fixture["incidence_certificates"]
    residuals = fixture["residuals"]
    require(len(certificates) == fixture["incidence_certificate_total"]
            == EXPECTED_CERTIFICATES, "incidence-certificate count changed")
    require(len(residuals) == fixture["residual_total"] == EXPECTED_RESIDUALS,
            "residual count changed")

    seen = set()
    for record in certificates:
        require(set(record) == {"kernel", "row", "bundles", "automorphism_orbit"},
                "incidence-certificate schema changed")
        kernel = KERNELS[record["kernel"] - 9]
        row = tuple(record["row"])
        require(row == canonical_row(kernel, row), "certificate row is not canonical")
        require(record["bundles"] == bundle_record(kernel, row),
                "physical bundle certificate changed")
        require(record["automorphism_orbit"] == [list(member) for member in
                orbit_members(kernel, row)], "automorphism incidence changed")
        key = (record["kernel"], row)
        require(key not in seen, "duplicate certificate row")
        seen.add(key)
    for record in residuals:
        require(set(record) == {"kernel", "row", "bundles", "automorphism_orbit"},
                "residual schema changed")
        kernel = KERNELS[record["kernel"] - 9]
        row = tuple(record["row"])
        require(row == canonical_row(kernel, row), "residual row is not canonical")
        require(record["bundles"] == bundle_record(kernel, row),
                "residual physical bundle record changed")
        require(record["automorphism_orbit"] == [list(member) for member in
                orbit_members(kernel, row)], "residual automorphism incidence changed")
        key = (record["kernel"], row)
        require(key not in seen, "certificate/residual overlap")
        seen.add(key)
    require(len(seen) == 378, "ledger is not an exact disjoint partition")

    serial = serialize(fixture)
    digest = hashlib.sha256(serial.encode("ascii")).hexdigest()
    require(expected_digest == EXPECTED_SHA256, "digest policy was mutated")
    require(digest == expected_digest, "fixture digest changed")
    return digest


def expect_rejected(action, label):
    try:
        action()
    except (IndexError, KeyError, RuntimeError, TypeError, ValueError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_self_checks():
    baseline = regenerate_payload(target_certificate_keys())
    mutations = []

    def add(label, mutate):
        candidate = deepcopy(baseline)
        mutate(candidate)
        mutations.append((label, candidate))

    add("deleted orbit", lambda value: value["residuals"].pop())
    add("duplicated orbit", lambda value: value["residuals"].append(
        deepcopy(value["residuals"][-1])))
    add("noncanonical row", lambda value: value["residuals"][0]["row"].reverse())
    add("changed bundle odd count", lambda value: value["incidence_certificates"][0]
        ["bundles"][0].__setitem__("odd", 1))
    add("lost orbit member", lambda value: value["incidence_certificates"][0]
        ["automorphism_orbit"].pop())
    add("certificate promoted", lambda value: value["incidence_certificates"].append(
        deepcopy(value["residuals"][0])))
    add("numerical claim injected", lambda value: value.__setitem__("maximum_cost", 3))
    add("pair order changed", lambda value: value["pair_order"].reverse())
    for label, candidate in mutations:
        expect_rejected(lambda candidate=candidate: audit(candidate), label)
    expect_rejected(lambda: audit(baseline, "0" * 64), "digest mutation")
    return len(mutations) + 1


def optimized_output():
    command = [sys.executable, "-O", str(Path(__file__).resolve()), "--emit"]
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    require(completed.returncode == 0, "python -O verifier failed")
    return completed.stdout


def report(digest, mutations):
    lines = (
        "five-vertex rank-four orbit fixture: exact audit passed",
        "kernels: 9,10,11,12",
        "physical_rows_by_kernel: 108,192,144,256 (total 700)",
        "automorphism_orbits_by_kernel: 63,120,144,51 (total 378)",
        "fixture_partition: 282 incidence certificates + 96 explicit residuals",
        "claim_scope: finite incidence data only; no numerical certificate claim",
        f"fixture_sha256: {digest}",
        f"rejected_hostile_mutations: {mutations}",
    )
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-fixture", action="store_true")
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check-optimized", action="store_true")
    args = parser.parse_args()
    if args.write_fixture:
        require(FIXTURE.is_file(), "writing requires an existing target fixture")
        FIXTURE.parent.mkdir(parents=True, exist_ok=True)
        FIXTURE.write_text(serialize(regenerate_payload(target_certificate_keys())),
                           encoding="ascii")
        print(hashlib.sha256(FIXTURE.read_bytes()).hexdigest())
        return 0
    digest = audit()
    mutations = hostile_self_checks()
    require(mutations == 9, "hostile mutation count changed")
    output = report(digest, mutations)
    if (args.check_optimized or (not args.emit and sys.flags.optimize == 0)):
        require(optimized_output() == output, "normal and python -O output differ")
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
