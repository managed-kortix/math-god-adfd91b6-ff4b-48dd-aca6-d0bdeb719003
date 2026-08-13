#!/usr/bin/env python3
"""Fail-closed master for the complete rank-seven multiblock theorem."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "research/fixtures/heptacyclic-multiblock-owner-ledger.json"
LEDGER_SHA256 = "5e118f91c7be63070161ac3788ed445b882bfb026c97a8cd9c47651c8fccc4af"
SOURCES = {
    "theorem": (ROOT / "positive-square-energy/heptacyclic-general/complete-multiblock-theorem.md",
                "53b361452b569da2a641b46afe3f75849c8aab99dc228c4d9c45705e38723a08"),
    "debit-ledger": (ROOT / "positive-square-energy/heptacyclic-general/rank-seven-multiblock-debit-ledger.md",
                     "7637b48974e130b4baa34d64e5fc284394d762364ca514e9158dbdd6e0c78c73"),
    "two-debit": (ROOT / "positive-square-energy/heptacyclic-general/two-debit-induced-piece-theorem.md",
                  "29304b8c920c6efd43d05ce0e8f2c21f44e2656ded0c3ce69ea79b5271454213"),
    "nested": (ROOT / "positive-square-energy/heptacyclic-general/nested-induced-piece-packet-theorem.md",
               "c5e93adcdc87aa41d524c04bfb6e1b78cb47628fa5053066b0d47ba741df50d8"),
    "r31-frontier": (ROOT / "positive-square-energy/heptacyclic-general/r31-s-doubled-c4-three-triangle-frontier.md",
                     "0a0c245994e00fd271e62391c8ecc0f8b0407f5969d2e98742eecd1de8b559bd"),
    "r31-c4": (ROOT / "positive-square-energy/heptacyclic-general/r31-s-c4-marked-four-triangle-theorem.md",
               "78344337226ae5c5b42645dd563390eec9eb462824e78fd4e42d7fa54051309d"),
    "r31-d3": (ROOT / "positive-square-energy/heptacyclic-general/r31-s-d3-diamond-territory-packet.md",
               "b89fcdb4272fb410a9e1ce72204f732f192a88407d02d865bd52d38013b28279"),
    "r511-k22": (ROOT / "positive-square-energy/heptacyclic-general/r511-k22-last-multiblock-key.md",
                 "b6c5c8a91326295bfafb83e7aacf3c761183de23ec316cf0e120c0f7fcba842f"),
    "r61": (ROOT / "positive-square-energy/heptacyclic-general/r61-one-credit-boundary-reduction.md",
            "4e5e519dc52630b00cae618f2d80aeb27251bb2c6af8874e59a94d3850b6c9f4"),
    "r61-k223": (ROOT / "positive-square-energy/heptacyclic-general/r61-k223-marked-cycle-packet.md",
                 "698c6b25f5ad76ad94a66b31bd30990e2a7e9246e9a53dc99b53992e67ee670b"),
}
CHILDREN = {
    "rank-seven-two-debit": ("rank-seven-two-debit-induced-piece-verifier.py",
        "f37e31be0d7888d43a7d8f752642fde04a71f1e1abc5317e94da7e0d7436a501",
        "0ac8b98c0abf5487577a65fabe386434f52d9bc05706bff146102a23f5ecace2"),
    "rank-seven-nested": ("rank-seven-nested-induced-piece-verifier.py",
        "f9e7d023c72c786d32b381b55e30b0826aad14a1a518c8459516f05e12868ad7",
        "d19e6d5961a47cc47ab14cf6308c7b90948ee64860a1119e969514395d3aec5d"),
    "r31-s-marked-cut": ("r31-s-doubled-c4-marked-cut-verifier.py",
        "95373442b786f269c52165d325f7c81a2110a3e41cb7220fb97a11f1f70ed658",
        "1f5cf00d63ae3b8c96e6f34b7292ff3abdd24422b2b73a2a42233a69c7ac7d8e"),
    "r31-s-c4": ("r31-s-c4-marked-four-triangle-verifier.py",
        "d405f644467ab59e615a4cf6fdf5ada1a3ba8c21eadcd1ee7035b3fa37d159e0",
        "15c8a1e8880762ce0fb8ad314f026a877982098ebade9f58fc6b8a574a118804"),
    "r31-s-d3": ("r31-s-d3-diamond-packet-verifier.py",
        "257f646e3089a0d6d5be109af8d5ab5c11caffe1efb9ee1adf5eab3033ce0f10",
        "c8bf4b784a5b65343d69ba62b4d3c5555682f76fcf0c9ffe84d6db86a8b74fa9"),
    "r511-k22": ("r511-k22-last-multiblock-key-verifier.py",
        "c76ad76df0db79d2a4acc2a7cc16c7d924d0d322064bf612e5a4078b7e1b0c93",
        "a8149532f0f5b92ff33bb6657df302e3ffda8ea6d177a61676c5fd206082df56"),
    "r61-k110": ("r61-k110-shared-cut-packet-verifier.py",
        "be0552093f21fc53359e1f558ce6620414809923369dff7336964f3b4a5d7518",
        "1a40d38acc8ee94ae69f4031cf85c7dafa6d87d6885120b744df54e242cabb5e"),
    "r61-k223": ("r61-k223-marked-cycle-packet-verifier.py",
        "5098c37f0e92f93f59d62e8fadba0252cc2e9031c7d6a2db22ae5827861fe0cf",
        "6c524958405426a1b8cdfdc3c4542c920490383e8734fda0bbde391ca686b78c"),
}
PACKET_KEYS = (
    "R21", "R221", "R31-S", "R31-K", "R321", "R322", "R331-S", "R331-K",
    "R41", "R421", "R43", "R511-K5e", "R511-K22", "R511-K71",
    "R52-K22", "R52-K71", "R61-K110-0", "R61-K110-1", "R61-K223",
)
PARTITIONS = {
    (7,), (6, 1), (5, 2), (5, 1, 1), (4, 3), (4, 2, 1), (4, 1, 1, 1),
    (3, 3, 1), (3, 2, 2), (3, 2, 1, 1), (3, 1, 1, 1, 1),
    (2, 2, 2, 1), (2, 2, 1, 1, 1), (2, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 1, 1, 1),
}
EXPECTED_ROWS = {
    (1, 1, 1, 1, 1, 1, 1): ("rank-uniform-cactus-theorem", ()),
    (2, 1, 1, 1, 1, 1): ("exact-dnn-sieve-plus-packets", ("R21",)),
    (2, 2, 1, 1, 1): ("exact-dnn-sieve-plus-packets", ("R221",)),
    (2, 2, 2, 1): ("exact-dnn", ()),
    (3, 1, 1, 1, 1): ("exact-dnn-sieve-plus-packets", ("R31-S", "R31-K")),
    (3, 2, 1, 1): ("exact-dnn-sieve-plus-packets", ("R321",)),
    (3, 2, 2): ("exact-dnn-sieve-plus-packets", ("R322",)),
    (3, 3, 1): ("exact-dnn-sieve-plus-packets", ("R331-S", "R331-K")),
    (4, 1, 1, 1): ("exact-dnn-sieve-plus-packets", ("R41",)),
    (4, 2, 1): ("exact-dnn-sieve-plus-packets", ("R421",)),
    (4, 3): ("exact-dnn-sieve-plus-packets", ("R43",)),
    (5, 1, 1): ("exact-dnn-sieve-plus-packets",
                ("R511-K5e", "R511-K22", "R511-K71")),
    (5, 2): ("exact-dnn-sieve-plus-packets", ("R52-K22", "R52-K71")),
    (6, 1): ("shared-gram-plus-structural-packets",
             ("R61-K110-0", "R61-K110-1", "R61-K223")),
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def digest(path):
    return digest_bytes(path.read_bytes())


def integer_partitions(total, maximum=None):
    if total == 0:
        return {()}
    maximum = total if maximum is None else min(total, maximum)
    return {(first,) + suffix for first in range(maximum, 0, -1)
            for suffix in integer_partitions(total - first, first)}


def load_ledger():
    require(digest(LEDGER) == LEDGER_SHA256, "owner ledger digest changed")
    try:
        return json.loads(LEDGER.read_text(encoding="ascii"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"cannot load owner ledger: {error}") from error


def check_sources():
    require(set(SOURCES) == {"theorem", "debit-ledger", "two-debit", "nested",
            "r31-frontier", "r31-c4", "r31-d3", "r511-k22", "r61", "r61-k223"},
            "source registry changed")
    for name, (path, expected) in SOURCES.items():
        require(path.is_file(), f"missing source: {name}")
        require(digest(path) == expected, f"source digest changed: {name}")


def audit(payload):
    check_sources()
    require(integer_partitions(7) == PARTITIONS, "partition generation changed")
    require(payload["schema"] == "heptacyclic-multiblock-owner-ledger-v1", "schema changed")
    require(payload["scope"] == {
        "block_predicate": "at-least-two-positive-rank-cyclic-blocks",
        "graph": "finite-simple-connected",
        "includes": ["arbitrary-legal-subdivisions", "arbitrary-block-cut-incidence",
                     "arbitrary-bridge-connectors", "repeated-or-nested-cuts",
                     "arbitrary-finite-rooted-trees"],
        "rank": 7,
    }, "theorem scope changed")
    require(payload["excluded_partitions"] == [[7]], "single-block exclusion changed")
    require(payload["conclusion"] == {"bound": "|V(G)|", "quantity": "s+(G)",
            "relation": ">=", "statement": "s+(G)>=|V(G)|", "strict": False},
            "conclusion changed")
    rows = payload["rows"]
    row_partitions = [tuple(row["partition"]) for row in rows]
    require(len(rows) == 14 and len(set(row_partitions)) == 14, "row ledger is not unique")
    require(set(row_partitions) == PARTITIONS - {(7,)}, "non-(7) rows are not exhaustive")
    actual_rows = {}
    for row in rows:
        require(set(row) == {"direct_owner", "packet_keys", "partition"},
                "row fields changed")
        actual_rows[tuple(row["partition"])] = (row["direct_owner"], tuple(row["packet_keys"]))
    require(actual_rows == EXPECTED_ROWS, "exact row dispositions changed")
    flattened = [key for row in rows for key in row["packet_keys"]]
    require(tuple(payload["packet_keys"]) == PACKET_KEYS, "packet key registry changed")
    require(len(flattened) == len(set(flattened)), "packet key has two partition owners")
    require(set(flattened) == set(PACKET_KEYS), "partition packet ownership is not exact")
    require(payload["final_residual"] == [], "final owner residual is not empty")
    require(payload["owner_rules"] == {
        "boundary_cut": "upstream-only",
        "nested_demands": "one-complete-first-boundary-territory",
        "positive_connectors": "actual-bridge-split-only",
        "rooted_descendants": "follow-unique-first-owner",
    }, "owner rules changed")

    owners = payload["verifier_owners"]
    require(set(owners) == set(CHILDREN), "child scope registry changed")
    primary = [key for keys in owners.values() for key in keys if ":" not in key]
    require(set(primary) == set(PACKET_KEYS), "packet verifier ownership is not exhaustive")
    require(len(primary) == len(set(primary)), "packet key has multiple primary verifiers")
    require(owners["r31-s-c4"] == ["R31-S:C4"] and
            owners["r31-s-d3"] == ["R31-S:D3"], "R31-S subpacket scopes changed")
    require(set(owners["rank-seven-nested"]) == {
        "R21", "R221", "R31-K", "R321", "R322", "R41", "R421",
        "R511-K5e", "R511-K71"}, "nested historical closed set changed")
    require(set(owners["rank-seven-two-debit"]) == {
        "R331-S", "R331-K", "R43", "R52-K22", "R52-K71"},
        "two-debit closed set changed")


def run_children():
    outputs = {}
    for name, (filename, source_digest, output_digest) in CHILDREN.items():
        path = ROOT / "research" / filename
        require(path.is_file() and digest(path) == source_digest,
                f"child source changed: {name}")
        mode_outputs = []
        for optimized in (False, True):
            command = [sys.executable]
            if optimized:
                command.append("-O")
            command.extend((str(path), "--optimized-child"))
            completed = subprocess.run(command, capture_output=True, check=False)
            require(completed.returncode == 0, f"child failed: {name}/{optimized}")
            require(completed.stderr == b"", f"child wrote stderr: {name}/{optimized}")
            require(digest_bytes(completed.stdout) == output_digest,
                    f"child output changed: {name}/{optimized}")
            mode_outputs.append(completed.stdout)
        require(mode_outputs[0] == mode_outputs[1], f"child mode outputs differ: {name}")
        outputs[name] = mode_outputs[0]
    return outputs


def expect_rejection(payload, mutation):
    changed = deepcopy(payload)
    mutation(changed)
    try:
        audit(changed)
    except (RuntimeError, KeyError, TypeError):
        return
    raise RuntimeError("hostile mutation accepted")


def hostile_tests(payload):
    mutations = (
        lambda value: value["rows"].pop(),
        lambda value: value["rows"].append({"partition": [7], "direct_owner": "packet",
                                             "packet_keys": []}),
        lambda value: value["excluded_partitions"].clear(),
        lambda value: value["scope"].update(block_predicate="all-heptacyclic"),
        lambda value: value["conclusion"].update(strict=True),
        lambda value: value["packet_keys"].remove("R511-K22"),
        lambda value: value["rows"][4]["packet_keys"].remove("R31-S"),
        lambda value: value["verifier_owners"]["r61-k223"].append("R61-K110-0"),
        lambda value: value["verifier_owners"]["r31-s-c4"].clear(),
        lambda value: value["final_residual"].append("R31-S"),
        lambda value: value["owner_rules"].update(boundary_cut="both-sides"),
    )
    for mutation in mutations:
        expect_rejection(payload, mutation)
    return len(mutations)


def main():
    payload = load_ledger()
    audit(payload)
    outputs = run_children()
    rejected = hostile_tests(payload)
    output = (
        "heptacyclic multiblock master verifier: exact audit passed\n"
        "partition scope: 14 non-(7) partitions; excluded single-block partition: (7)\n"
        f"owner ledger: {len(PACKET_KEYS)} packet keys; final residual: empty\n"
        f"packet verifiers: {len(outputs)}; executions: {2 * len(outputs)} normal/-O\n"
        f"hostile mutations rejected: {rejected}\n"
        "conclusion: s+(G)>=|V(G)| for connected rank-seven multiblock graphs only\n"
        "status: COMPLETE MULTIBLOCK THEOREM; NO ALL-HEPTACYCLIC CLAIM"
    )
    if "--optimized-master-child" not in sys.argv and not sys.flags.optimize:
        child = subprocess.run([sys.executable, "-O", __file__, "--optimized-master-child"],
                               check=True, capture_output=True, text=True)
        require(child.stdout.rstrip() == output, "normal/optimized master output mismatch")
    print(output)


if __name__ == "__main__":
    main()
