#!/usr/bin/env python3
"""Fail-closed verifier for the rank-seven two-debit induced-piece theorem."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "research/fixtures/rank-seven-two-debit-induced-piece-ledger.json"
FIXTURE_SHA256 = "08f347f8c3c04dfbd641ca1922b09fbee5c5c58c28332d8fbb4b9b61ea7c6272"
SOURCES = {
    "theorem": (
        ROOT / "positive-square-energy/heptacyclic-general/two-debit-induced-piece-theorem.md",
        "29304b8c920c6efd43d05ce0e8f2c21f44e2656ded0c3ce69ea79b5271454213",
    ),
    "k22": (
        ROOT / "pentacyclic/research/order5-kernel-family-theorem.json",
        "4d8b826b397dc269c7853b8bd386d00bf469282b52720b8dac96d850e9e616d8",
    ),
    "k71": (
        ROOT / "pentacyclic/research/order6-kernel-family-theorem.json",
        "69b236b014aef58c037c610ca01fa62ad82601f7bb34153939ec4ddd3b5f364d",
    ),
}
EXPECTED_KEYS = ("R331-S", "R331-K", "R43", "R52-K22", "R52-K71")
EXPECTED_REMAINING = (
    "R21", "R221", "R31-S", "R31-K", "R321", "R322", "R41", "R421",
    "R511-K5e", "R511-K22", "R511-K71",
)
EXPECTED_TARGETS = {"R52-K22": 4, "R52-K71": 9}
EXPECTED_CHANNELS = {
    "R331-S": ("separate", "repeated-cut", "nested"),
    "R331-K": ("separate", "repeated-cut", "nested"),
    "R43": ("opened-owner", "retained-owner"),
    "R52-K22": ("opened-owner", "retained-owner"),
    "R52-K71": ("opened-owner", "retained-owner"),
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


def check_sources(sources=None):
    if sources is None:
        sources = SOURCES
    require(set(sources) == {"theorem", "k22", "k71"}, "source key set changed")
    for name, (path, expected) in sources.items():
        require(path.is_file(), f"missing source: {name}")
        require(digest(path) == expected, f"source digest changed: {name}")


def regenerate_structural_targets(sources=None):
    if sources is None:
        sources = SOURCES
    k22 = load_json(sources["k22"][0])
    k22_records = [record for record in k22["records"]
                   if record["method"] == "structural_attached_k4"]
    require(len(k22_records) == 4, "K22 structural target count changed")
    require({record["kernel"] for record in k22_records} == {22},
            "K22 structural target kernel changed")
    require({record["frontier"] for record in k22_records} == {None, 0},
            "K22 structural frontiers changed")
    require(len({tuple(record["row"]) for record in k22_records}) == 2,
            "K22 structural parity rows changed")

    k71 = load_json(sources["k71"][0])
    k71_records = [record for record in k71["closure_records"]
                   if record["method"] == "structural_triangle_plus_attached_k4"]
    require(len(k71_records) == 9, "K71 structural target count changed")
    require({record["kernel"] for record in k71_records} == {71},
            "K71 structural target kernel changed")
    require({record["frontier"] for record in k71_records} == {None, 5, 6},
            "K71 structural frontiers changed")
    require(len({tuple(record["row"]) for record in k71_records}) == 3,
            "K71 structural parity rows changed")
    return {"R52-K22": len(k22_records), "R52-K71": len(k71_records)}


def audit_family(record):
    common = {
        "key", "partition", "anchor", "anchor_credit_strictly_greater_than",
        "physical_owner", "demands", "channels", "worst_debits",
        "total_credit_strictly_greater_than",
    }
    allowed = common | {"boundary_refinement", "structural_targets"}
    require(set(record) <= allowed and common <= set(record),
            f"{record.get('key')} family fields changed")
    key = record["key"]
    require(type(record["anchor_credit_strictly_greater_than"]) is int,
            f"{key} anchor threshold is not exact")
    require(record["anchor_credit_strictly_greater_than"] == 2,
            f"{key} lost the strict two-credit anchor")
    require(tuple(record["channels"]) == EXPECTED_CHANNELS[key],
            f"{key} owner channels changed")
    require(all(type(value) is int and value in (-1, 0)
                for value in record["worst_debits"]), f"{key} debit is invalid")
    require(len(record["worst_debits"]) <= 2, f"{key} exceeds two debits")
    total = record["anchor_credit_strictly_greater_than"] + sum(record["worst_debits"])
    require(total == record["total_credit_strictly_greater_than"],
            f"{key} strict debit arithmetic changed")
    require(total >= 0, f"{key} packet does not close")

    if key.startswith("R331"):
        require(record["partition"] == [3, 3, 1] and len(record["demands"]) == 2,
                f"{key} rank/demand ledger changed")
        require(record["worst_debits"] == [-1, -1], f"{key} worst debits changed")
    elif key == "R43":
        require(record["partition"] == [4, 3], "R43 partition changed")
        require(record.get("boundary_refinement") ==
                "actual-K4-minus-cut-is-actual-K3", "R43 actual-K3 packet lost")
        require(record["worst_debits"] == [-1, 0], "R43 owner debit changed")
    else:
        require(record["partition"] == [5, 2], f"{key} partition changed")
        require(record.get("structural_targets") == EXPECTED_TARGETS[key],
                f"{key} structural target ledger changed")


def synthetic_owner_partition(key, channel):
    anchor = {(key, "anchor", index) for index in range(4)}
    owner = {(key, "owner", index) for index in range(2)}
    vertices = anchor | owner
    territories = [set(anchor), set(owner)]

    demands = 2 if key.startswith("R331") else 1
    entry_cuts = []
    for demand in range(demands):
        if channel == "repeated-cut":
            cut = (key, "anchor", 0)
        elif channel == "nested" and demand == 1:
            cut = (key, "demand", 0, 1)
        elif channel == "opened-owner":
            cut = (key, "owner", 0)
        else:
            cut = (key, "anchor", min(demand, 3))
        entry_cuts.append(cut)
        require(cut in vertices, f"{key}/{channel} entry cut has no upstream owner")

        downstream = {(key, "demand", demand, index) for index in range(1, 4)}
        descendants = {(key, "descendant", demand, index) for index in range(1, 4)}
        vertices |= downstream | descendants
        piece = downstream | descendants
        if channel == "opened-owner":
            territories[1] |= piece
        elif channel == "nested" and demand == 1:
            territories[-1] |= piece
        else:
            territories.append(piece)

    union = set().union(*territories)
    require(union == vertices, f"{key}/{channel} omitted an owner or descendant")
    require(sum(map(len, territories)) == len(union),
            f"{key}/{channel} duplicated an owner or boundary cut")
    require(all(cut in union and sum(cut in piece for piece in territories) == 1
                for cut in entry_cuts), f"{key}/{channel} cut ownership changed")
    return len(vertices)


def audit(payload=None, sources=None):
    if payload is None:
        require(digest(FIXTURE) == FIXTURE_SHA256, "owner ledger digest changed")
        payload = load_json(FIXTURE)
    check_sources(sources)
    require(payload["schema"] == "rank-seven-two-debit-induced-piece-ledger-v1",
            "schema changed")
    require(payload["scope"] == "bridge-free-heptacyclic-multiblock-post-dnn-residual",
            "scope changed")
    records = payload["families"]
    require(len(records) == 5, "family count changed")
    require(tuple(record["key"] for record in records) == EXPECTED_KEYS,
            "closed family order or key set changed")
    for record in records:
        audit_family(record)

    rules = payload["owner_rules"]
    require(rules == {
        "boundary_cut": "upstream-only",
        "nested_demands": "one-complete-first-boundary-territory",
        "rooted_descendants": "follow-unique-owner",
        "positive_connectors": "removed-by-bridge-split",
        "maximum_negative_units": 2,
    }, "owner rules changed")
    require(tuple(payload["closed_keys"]) == EXPECTED_KEYS, "closed keys changed")
    require(tuple(payload["remaining_registry_keys"]) == EXPECTED_REMAINING,
            "remaining owner registry changed")
    require(set(payload["closed_keys"]).isdisjoint(payload["remaining_registry_keys"]),
            "closed and open registries overlap")

    targets = regenerate_structural_targets(sources)
    require(targets == EXPECTED_TARGETS, "regenerated structural targets changed")
    owner_cases = 0
    owner_vertices = 0
    for key, channels in EXPECTED_CHANNELS.items():
        for channel in channels:
            owner_vertices += synthetic_owner_partition(key, channel)
            owner_cases += 1
    require(owner_cases == 12, "owner case count changed")
    return owner_cases, owner_vertices


def expect_rejection(payload, mutation):
    changed = deepcopy(payload)
    mutation(changed)
    try:
        audit(changed)
    except (AuditError, KeyError):
        return
    raise AuditError("hostile mutation accepted")


def hostile_tests(payload):
    mutations = (
        lambda value: value["families"].pop(),
        lambda value: value["families"][0].update(worst_debits=[-1]),
        lambda value: value["families"][1].update(anchor_credit_strictly_greater_than=3),
        lambda value: value["families"][2].pop("boundary_refinement"),
        lambda value: value["families"][3].update(structural_targets=5),
        lambda value: value["families"][4].update(worst_debits=[-1, -1]),
        lambda value: value["owner_rules"].update(boundary_cut="both-sides"),
        lambda value: value["closed_keys"].remove("R43"),
        lambda value: value["remaining_registry_keys"].append("R43"),
    )
    for mutation in mutations:
        expect_rejection(payload, mutation)
    return len(mutations)


def main():
    require(digest(FIXTURE) == FIXTURE_SHA256, "owner ledger digest changed")
    payload = load_json(FIXTURE)
    owner_cases, owner_vertices = audit(payload)
    rejected = hostile_tests(payload)
    output = ("rank-seven two-debit induced-piece verifier: exact audit passed\n"
              "closed keys: R331-S, R331-K, R43, R52-K22, R52-K71\n"
              "structural targets: K22=4 K71=9\n"
              f"owner channels: {owner_cases}; synthetic vertices audited: {owner_vertices}\n"
              f"hostile mutations rejected: {rejected}\n"
              "status: five residual owner families CLOSED")
    if "--optimized-child" not in sys.argv and not sys.flags.optimize:
        child = subprocess.run([sys.executable, "-O", __file__, "--optimized-child"],
                               check=True, capture_output=True, text=True)
        require(child.stdout.rstrip() == output, "normal/optimized output mismatch")
    print(output)


if __name__ == "__main__":
    main()
