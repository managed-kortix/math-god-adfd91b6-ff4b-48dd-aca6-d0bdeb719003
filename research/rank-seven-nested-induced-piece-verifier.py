#!/usr/bin/env python3
"""Fail-closed verifier for the rank-seven nested induced-piece packets."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "research/fixtures/rank-seven-nested-induced-piece-manifest.json"
MANIFEST_SHA256 = "62d821de00cbd915a06ac935b3e037517557f5fc4757078471775e11f5ee658a"
SOURCES = {
    "theorem": (
        ROOT / "positive-square-energy/heptacyclic-general/nested-induced-piece-packet-theorem.md",
        "c45de1b0232ca22437f87a83cf52c37009e141fdc1b0e77aaf0d062811014495",
    ),
    "ledger": (
        ROOT / "positive-square-energy/heptacyclic-general/rank-seven-multiblock-debit-ledger.md",
        "8ad85b9c6f5440f1fd62d5a812e8b1a84394867def0e6b62394d42d0f259e84c",
    ),
    "two-debit": (
        ROOT / "positive-square-energy/heptacyclic-general/two-debit-induced-piece-theorem.md",
        "29304b8c920c6efd43d05ce0e8f2c21f44e2656ded0c3ce69ea79b5271454213",
    ),
    "k5e-sieve": (
        ROOT / "pentacyclic/research/all-odd-k5e-territory-sieve.py",
        "047a472d4e1af46850198dc68b5780f98b930618f79b51174f11460afcc0334d",
    ),
    "k71-fixture": (
        ROOT / "pentacyclic/research/order6-kernel-family-theorem.json",
        "69b236b014aef58c037c610ca01fa62ad82601f7bb34153939ec4ddd3b5f364d",
    ),
}
INPUT_KEYS = (
    "R21", "R221", "R31-S", "R31-K", "R321", "R322", "R41", "R421",
    "R511-K5e", "R511-K22", "R511-K71",
)
CLOSED_KEYS = (
    "R21", "R221", "R31-K", "R321", "R322", "R41", "R421",
    "R511-K5e", "R511-K71",
)
RETURNED_KEYS = ("R31-S", "R511-K22")
EARLIER_CLOSED = (
    "R331-S", "R331-K", "R43", "R52-K22", "R52-K71", "R61",
)
EXPECTED_PARTITIONS = {
    (7,), (6, 1), (5, 2), (5, 1, 1), (4, 3), (4, 2, 1),
    (4, 1, 1, 1), (3, 3, 1), (3, 2, 2), (3, 2, 1, 1),
    (3, 1, 1, 1, 1), (2, 2, 2, 1), (2, 2, 1, 1, 1),
    (2, 1, 1, 1, 1, 1), (1, 1, 1, 1, 1, 1, 1),
}


class AuditError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise AuditError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="ascii"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise AuditError(f"cannot load {path.name}: {error}") from error


def load_python(path):
    spec = importlib.util.spec_from_file_location("rank7_k5e_sieve", path)
    require(spec is not None and spec.loader is not None, "cannot load K5e sieve")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def integer_partitions(total, maximum=None):
    if total == 0:
        return {()}
    maximum = total if maximum is None else min(maximum, total)
    return {
        (first,) + suffix
        for first in range(maximum, 0, -1)
        for suffix in integer_partitions(total - first, first)
    }


def check_sources(sources=None):
    sources = SOURCES if sources is None else sources
    require(set(sources) == {"theorem", "ledger", "two-debit", "k5e-sieve", "k71-fixture"},
            "source key set changed")
    for name, (path, expected) in sources.items():
        require(path.is_file(), f"missing source: {name}")
        require(digest(path) == expected, f"source digest changed: {name}")


def regenerate_structural_targets(sources=None):
    sources = SOURCES if sources is None else sources
    sieve = load_python(sources["k5e-sieve"][0])
    counts, residual_orbits = sieve.audit()
    require(len(residual_orbits) == 16, "K5e residual orbit count changed")
    k5e = {name: counts[name] for name in ("complete-k4", "favorable-theta")}
    require(k5e == {"complete-k4": 53, "favorable-theta": 640},
            "K5e structural targets changed")

    fixture = load_json(sources["k71-fixture"][0])
    records = [record for record in fixture["closure_records"]
               if record["method"] == "structural_triangle_plus_attached_k4"]
    require(len(records) == 9, "K71 structural target count changed")
    require({record["kernel"] for record in records} == {71}, "K71 kernel changed")
    require({record["frontier"] for record in records} == {None, 5, 6},
            "K71 frontiers changed")
    return k5e, len(records)


def synthetic_owner_partition(key, channel, demands):
    anchor = {(key, "anchor", index) for index in range(4)}
    owner = {(key, "owner", index) for index in range(2)}
    vertices = anchor | owner
    pieces = [set(anchor), set(owner)]
    first_downstream = None
    cuts = []
    for demand in range(demands):
        if channel == "opened-owner":
            cut = (key, "owner", 0)
        elif channel == "repeated-cut":
            cut = (key, "anchor", 0)
        elif channel in ("nested", "intermediate-cycle") and demand:
            require(first_downstream is not None, f"{key}/{channel} has no parent demand")
            cut = min(first_downstream)
        else:
            cut = (key, "anchor", demand % 4)
        require(cut in vertices, f"{key}/{channel} cut has no upstream owner")
        cuts.append(cut)
        side = {(key, "demand", demand, index) for index in range(1, 4)}
        descendants = {(key, "descendant", demand, index) for index in range(1, 3)}
        vertices |= side | descendants
        complete = side | descendants
        if first_downstream is None:
            first_downstream = complete
        if channel == "opened-owner":
            pieces[1] |= complete
        elif channel in ("nested", "intermediate-cycle") and demand:
            pieces[-1] |= complete
        else:
            pieces.append(complete)
    union = set().union(*pieces)
    require(union == vertices, f"{key}/{channel} omitted a vertex")
    require(sum(map(len, pieces)) == len(union), f"{key}/{channel} duplicated a vertex")
    require(all(sum(cut in piece for piece in pieces) == 1 for cut in cuts),
            f"{key}/{channel} duplicated a boundary cut")
    return len(vertices)


def audit(payload=None, sources=None):
    if payload is None:
        require(digest(MANIFEST) == MANIFEST_SHA256, "manifest digest changed")
        payload = load_json(MANIFEST)
    check_sources(sources)
    require(integer_partitions(7) == EXPECTED_PARTITIONS, "partition census changed")
    require(payload["schema"] == "rank-seven-nested-induced-piece-owner-manifest-v1",
            "schema changed")
    require(payload["scope"] == "bridge-free-heptacyclic-multiblock-post-r61-post-two-debit",
            "scope changed")
    require(tuple(payload["input_keys"]) == INPUT_KEYS, "input owner registry changed")
    records = payload["families"]
    require(tuple(record["key"] for record in records) == INPUT_KEYS,
            "typed family order changed")
    require(len({record["key"] for record in records}) == 11, "duplicate typed key")

    k5e, k71 = regenerate_structural_targets(sources)
    proved = []
    returned = []
    owner_cases = owner_vertices = 0
    common = {"key", "partition", "owner_type", "anchor_threshold",
              "negative_territories", "channels", "status"}
    for record in records:
        key = record["key"]
        require(common <= set(record), f"{key} missing typed field")
        require(type(record["anchor_threshold"]) is int and
                type(record["negative_territories"]) is int, f"{key} has inexact demand")
        supported = record["anchor_threshold"] >= record["negative_territories"]
        require(record["status"] == ("closed" if supported else "open"),
                f"{key} status disagrees with typed demand")
        if supported:
            proved.append(key)
        else:
            returned.append(key)
            require(record.get("obstruction"), f"{key} open row lacks obstruction")
        demands = max(1, record["negative_territories"])
        for channel in record["channels"]:
            require(channel in {"opened-owner", "retained-owner", "separate",
                                "repeated-cut", "nested", "intermediate-cycle"},
                    f"{key} has unknown owner channel")
            owner_vertices += synthetic_owner_partition(key, channel, demands)
            owner_cases += 1

    require(tuple(proved) == CLOSED_KEYS, "maximal proved subset changed")
    require(tuple(returned) == RETURNED_KEYS, "returned key set changed")
    require(tuple(payload["closed_keys"]) == CLOSED_KEYS, "closed manifest changed")
    require(tuple(payload["returned_keys"]) == RETURNED_KEYS, "returned manifest changed")
    require(k5e == records[8]["structural_targets"], "K5e typed targets changed")
    require(k71 == records[10]["structural_targets"], "K71 typed targets changed")
    require(payload["owner_rules"] == {
        "boundary_cut": "upstream-only",
        "nested_demands": "one-complete-first-boundary-territory",
        "rooted_descendants": "follow-unique-first-owner",
        "positive_connectors": "removed-by-bridge-split",
    }, "owner rules changed")
    require(set(CLOSED_KEYS).isdisjoint(RETURNED_KEYS), "closed/open overlap")
    require(set(CLOSED_KEYS) | set(RETURNED_KEYS) == set(INPUT_KEYS),
            "owner registry is not exhaustive")
    require(len(EARLIER_CLOSED) + len(CLOSED_KEYS) == 15,
            "combined closed-family accounting changed")
    return owner_cases, owner_vertices


def expect_rejection(payload, mutation):
    changed = deepcopy(payload)
    mutation(changed)
    try:
        audit(changed)
    except (AuditError, KeyError, IndexError):
        return
    raise AuditError("hostile mutation accepted")


def hostile_tests(payload):
    mutations = (
        lambda value: value["families"].pop(),
        lambda value: value["families"][2].update(status="closed"),
        lambda value: value["families"][3].update(anchor_threshold=2),
        lambda value: value["families"][6].update(negative_territories=4),
        lambda value: value["families"][8]["structural_targets"].update(**{"complete-k4": 54}),
        lambda value: value["families"][9].pop("obstruction"),
        lambda value: value["families"][10].update(structural_targets=8),
        lambda value: value["owner_rules"].update(boundary_cut="both-sides"),
        lambda value: value["closed_keys"].append("R511-K22"),
        lambda value: value["returned_keys"].remove("R31-S"),
    )
    for mutation in mutations:
        expect_rejection(payload, mutation)
    return len(mutations)


def main():
    require(digest(MANIFEST) == MANIFEST_SHA256, "manifest digest changed")
    payload = load_json(MANIFEST)
    owner_cases, owner_vertices = audit(payload)
    rejected = hostile_tests(payload)
    output = (
        "rank-seven nested induced-piece verifier: exact audit passed\n"
        "newly closed keys: R21, R221, R31-K, R321, R322, R41, R421, R511-K5e, R511-K71\n"
        "returned keys: R31-S, R511-K22\n"
        "structural targets: K5e=53+640 K71=9\n"
        f"owner channels: {owner_cases}; synthetic vertices audited: {owner_vertices}\n"
        f"hostile mutations rejected: {rejected}\n"
        "status: maximal supported subset CLOSED; full multiblock theorem OPEN"
    )
    if "--optimized-child" not in sys.argv and not sys.flags.optimize:
        child = subprocess.run([sys.executable, "-O", __file__, "--optimized-child"],
                               check=True, capture_output=True, text=True)
        require(child.stdout.rstrip() == output, "normal/optimized output mismatch")
    print(output)


if __name__ == "__main__":
    main()
