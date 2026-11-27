#!/usr/bin/env python3
"""Fail-closed audit of the rank-seven multiblock reduction.

The bridge-free packet registry is empty only after registered bridge
dispatch.  For a nontrivial positive hull, imported physical unit-star and
R61 single-block owners leave two typed outer rows.  The one-positive-hull
multiblock physical-bridge forest remains open and unauthenticated.  This
master therefore exits nonzero; a zero exit must never be mistaken for a
theorem receipt.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "research/fixtures/heptacyclic-multiblock-owner-ledger.json"
LEDGER_SHA256 = "548977e22a31e5bbcb9ed9ac0424c5fa9720e8db157dab2ca82550de74a5bcb1"
SOURCES = {
    "theorem": (ROOT / "positive-square-energy/heptacyclic-general/complete-multiblock-theorem.md",
                "bef80fb78a5b085dc5959b15ac0efc6e0c05093d4af9f722d2007f6b21118d75"),
    "debit-ledger": (ROOT / "positive-square-energy/heptacyclic-general/rank-seven-multiblock-debit-ledger.md",
                     "f45d60cbeefdf523e5aab053af708a388687f05b64a3d569bd1ddda885396ac2"),
    "physical-hull-owner-overlay": (ROOT / "positive-square-energy/heptacyclic-general/rank-seven-physical-hull-owner-overlay.md",
                                    "b0fe17dcd2f520caf912f66cc53747cc7b5e2b6ac772a1b087f9bbff9065e89c"),
    "physical-hull-reduction": (ROOT / "positive-square-energy/heptacyclic-general/physical-hull-bridge-reduction/theorem-note.md",
                                "e09bdcfd99f85b4660678b1dbc70538bea6de0624b500ede8eae38eae9e639de"),
    "physical-unit-star": (ROOT / "positive-square-energy/heptacyclic-general/physical-unit-star-dnn-theorem.md",
                           "4b01acc39533fe53391157851a06f5c7b07013f2532f449725c120f931ca814e"),
    "physical-unit-star-manifest": (ROOT / "research/fixtures/physical-unit-star-dnn-theorem-manifest.json",
                                    "577ba7fa46737e58a89050b9da7bb1b87e29f7bd273e0c767390165230965c98"),
    "r61-physical-single-block": (ROOT / "positive-square-energy/heptacyclic-general/r61-physical-single-block-theorem.md",
                                  "b649c2c4622d7b4474faebd7f0cd0f9217f3b4dc449fe6beaed536fc7738bb6e"),
    "r61-physical-manifest": (ROOT / "research/fixtures/r61-physical-single-block-theorem-manifest.json",
                              "b43dc1e7a450aac5af66b1fd6a7c23ff6bf2a5ddbcc9bd4a2b8b9c2333f709fe"),
    "universal-hull-k2": (ROOT / "positive-square-energy/heptacyclic-general/universal-hull-k2-theorem.md",
                          "c469a4991df034b040f6aee49f1e81b8513a18e59f86edf3c38ee4c318b0e9a5"),
    "two-debit": (ROOT / "positive-square-energy/heptacyclic-general/two-debit-induced-piece-theorem.md",
                  "5c663bf627633c7ef6b35e12f1900a5b3868e22259b161f8f0e4cb2f7f796550"),
    "nested": (ROOT / "positive-square-energy/heptacyclic-general/nested-induced-piece-packet-theorem.md",
               "79b44180ff2d3ca44b5537e2913709fa6c2334b2e475990b34508475592a000b"),
    "r31-frontier": (ROOT / "positive-square-energy/heptacyclic-general/r31-s-doubled-c4-three-triangle-frontier.md",
                     "9575016821113e7873a26de25dda36c48c53309f29fcab89dbde50c7c017aa18"),
    "r31-physical": (ROOT / "positive-square-energy/heptacyclic-general/r31-s-physical-shared-triangle-closure.md",
                     "0e90be4f08d75e1f4517c0f3d7e2ba84841feb3dbd39bb1b045ac6dbb3761bf1"),
    "r31-c4": (ROOT / "positive-square-energy/heptacyclic-general/r31-s-c4-marked-four-triangle-theorem.md",
               "78344337226ae5c5b42645dd563390eec9eb462824e78fd4e42d7fa54051309d"),
    "r31-d3-open": (ROOT / "positive-square-energy/heptacyclic-general/r31-s-d3-diamond-territory-packet.md",
                    "3ec59040eeadb6e5f99bd2f2dc7f46babb78a24ab3dfd12ba30bdb5dfd419d51"),
    "r511-k22": (ROOT / "positive-square-energy/heptacyclic-general/r511-k22-last-multiblock-key.md",
                 "b6c5c8a91326295bfafb83e7aacf3c761183de23ec316cf0e120c0f7fcba842f"),
    "r61": (ROOT / "positive-square-energy/heptacyclic-general/r61-one-credit-boundary-reduction.md",
            "96ca1526c8ee1a60fd9cbf42e8ce9bc20eae2911ec0f133448ee0ce69dc1d5cb"),
    "r61-k223": (ROOT / "positive-square-energy/heptacyclic-general/r61-k223-marked-cycle-packet.md",
                 "698c6b25f5ad76ad94a66b31bd30990e2a7e9246e9a53dc99b53992e67ee670b"),
}
CHILDREN = {
    "universal-hull-k2": ("universal-hull-k2-verifier.py",
        "d35b9ce0d466f9ad535cfc6c116c6803656465f505215ba14e44914f18682fe1",
        "5f91e157c4fa1f0c941d526499743c159d807d193691a2080a261e0594e8964a"),
    "physical-unit-star": ("physical-unit-star-dnn-theorem-verifier.py",
        "359bcbb3bad8a6fe1cb61cb036ee74494be0af530896e812755790211a74e323",
        "a61fe6244f77c7c99fe8029e525f0f352c44cf87df1aa48f8f6935fe122681e6"),
    "r61-physical-single-block": ("r61-physical-single-block-theorem-verifier.py",
        "1fbd042e0019277fae927c06959047afd40be59eecbfe42454c17441255f0e51",
        "46d17cc6f689eb872a8f8f8949f2255a131fc3a31ba5a4431909a6543ba3d94f"),
    "rank-seven-two-debit": ("rank-seven-two-debit-induced-piece-verifier.py",
        "d7e6006ee1010e1647e725776461882fc825676dad4a63f2bdf64ce53ad4c412",
        "beee5bb2c4fb30a5ed309ece930919f0d91399a5aebcf13b954eb3a867660448"),
    "rank-seven-nested": ("rank-seven-nested-induced-piece-verifier.py",
        "e60d37e72abfa9dfd4ef0e60dd6e8a36651a5a652e378a3b2dbd1e82859466ab",
        "d19e6d5961a47cc47ab14cf6308c7b90948ee64860a1119e969514395d3aec5d"),
    "r31-s-marked-cut": ("r31-s-doubled-c4-marked-cut-verifier.py",
        "b14e7544bd8f5298fd425c68228e5fb4f5c49071dd3a7ec773ee5de610630c71",
        "676f2be24fda77b0642f7cf243385c84d9bd92266a74b73178c185a697bf3eed"),
    "r31-s-c4": ("r31-s-c4-marked-four-triangle-verifier.py",
        "d405f644467ab59e615a4cf6fdf5ada1a3ba8c21eadcd1ee7035b3fa37d159e0",
        "15c8a1e8880762ce0fb8ad314f026a877982098ebade9f58fc6b8a574a118804"),
    # Imported byte-for-byte from standalone commit
    # 937ec059a3819fb87517b014012f9397b529c1d1.  This combinatorial parent
    # universe gate runs before the independent analytic/adjacency verifier.
    "r31-s-parent-gate": ("r31-s-physical-parent-gate-verifier.py",
        "05c070f7552b804d9ca23a8987bc83e8547105266ca0f2e7756dd5034136f09c",
        "639bc54bcaf764c807f636ac10ce001f8cb2ff52375f34f5efea5c86b6b5dcdd"),
    "r31-s-physical": ("r31-s-physical-parent-verifier.py",
        "a8e73f0e749705558aefa21bb6e0cdc361be8a3a437d0d889fb50a9c41b26bb9",
        "e2da1bdd114c8770765b3c0b36938fb7d6cc2e25fe249304a80241bb1d4e9f2f"),
    "r511-k22": ("r511-k22-last-multiblock-key-verifier.py",
        "15325973275aef32b93df32a32dd5b9afaeb2d1c95a6d11dc510312e2761907c",
        "a8149532f0f5b92ff33bb6657df302e3ffda8ea6d177a61676c5fd206082df56"),
    "r61-k110": ("r61-k110-shared-cut-packet-verifier.py",
        "dd866270f8285b7ff7c82e845e3f46e14e89bc7012241652f3a9a6dbe4baec1b",
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
    require(set(SOURCES) == {"theorem", "debit-ledger", "physical-hull-owner-overlay",
            "physical-hull-reduction",
            "physical-unit-star", "physical-unit-star-manifest",
            "r61-physical-single-block", "r61-physical-manifest",
            "universal-hull-k2", "two-debit", "nested", "r31-frontier",
            "r31-physical", "r31-c4", "r31-d3-open", "r511-k22", "r61",
            "r61-k223"}, "source registry changed")
    for name, (path, expected) in SOURCES.items():
        require(path.is_file(), f"missing source: {name}")
        require(digest(path) == expected, f"source digest changed: {name}")


def audit(payload):
    check_sources()
    require(integer_partitions(7) == PARTITIONS, "partition generation changed")
    require(payload["schema"] == "heptacyclic-multiblock-owner-ledger-v4", "schema changed")
    require(payload["scope"] == {
        "block_predicate": "at-least-two-positive-rank-cyclic-blocks",
        "graph": "finite-simple-connected",
        "includes": ["arbitrary-legal-subdivisions", "arbitrary-block-cut-incidence",
                     "repeated-or-nested-cuts", "arbitrary-finite-rooted-trees"],
        "excludes": ["open-nontrivial-positive-hull-rows",
                     "one-positive-hull-multiblock-physical-bridge-forest"],
        "rank": 7,
    }, "registered theorem scope changed")
    require(payload["excluded_partitions"] == [[7]], "single-block exclusion changed")
    require(payload["conclusion"] == {"bound": "|V(G)|", "quantity": "s+(G)",
            "relation": ">=", "statement": "s+(G)>=|V(G)|", "strict": False},
            "conclusion changed")
    rows = payload["rows"]
    row_partitions = [tuple(row["partition"]) for row in rows]
    require(len(rows) == 14 and len(set(row_partitions)) == 14,
            "bridge-free row ledger is not unique")
    require(set(row_partitions) == PARTITIONS - {(7,)},
            "bridge-free non-(7) rows are not exhaustive")
    actual_rows = {}
    for row in rows:
        require(set(row) == {"direct_owner", "packet_keys", "partition"},
                "row fields changed")
        actual_rows[tuple(row["partition"])] = (row["direct_owner"], tuple(row["packet_keys"]))
    require(actual_rows == EXPECTED_ROWS, "exact bridge-free row dispositions changed")
    flattened = [key for row in rows for key in row["packet_keys"]]
    require(tuple(payload["packet_keys"]) == PACKET_KEYS, "packet key registry changed")
    require(len(flattened) == len(set(flattened)), "packet key has two partition owners")
    require(set(flattened) == set(PACKET_KEYS), "partition packet ownership is not exact")
    require(payload["bridge_free_packet_residual"] == [],
            "bridge-free packet residual is not empty")
    require("final_residual" not in payload and
            "unoriented_bridge_cases" not in payload,
            "obsolete global bridge residual was reintroduced")
    require("hull_bridge_owner_slices" not in payload and
            "remaining_unoriented_bridge_cases" not in payload,
            "obsolete generic bridge registry was reintroduced")

    overlay = payload["physical_hull_owner_overlay"]
    require(set(overlay) == {"axis", "domain", "finite_census_claim",
            "open_rows", "owners", "route_obstruction"},
            "physical hull overlay fields changed")
    require(overlay["axis"] ==
            "all-global-bridge quotient; restricted here to nontrivial positive hull",
            "physical hull overlay axis changed")
    require(overlay["domain"] == {
        "positive_hull": "at-least-two-positive-weight-quotient-vertices",
        "one_positive_hull_excluded": True,
    }, "physical hull overlay domain changed")
    require(overlay["finite_census_claim"] is False,
            "outer rows were laundered into a finite census")
    owners_by_name = {owner["owner"]: owner for owner in overlay["owners"]}
    require(len(owners_by_name) == 3 and set(owners_by_name) == {
            "universal-hull-k2", "PHYSICAL-UNIT-STAR-DNN",
            "R61-PHYSICAL-SINGLE-BLOCK"}, "physical hull owner set changed")
    require(owners_by_name["universal-hull-k2"] == {
        "owner": "universal-hull-k2",
        "scope": {"exactly_two_positive_blocks": True,
                  "partitions": [[4, 3], [5, 2]],
                  "requires": "physical-K2-on-positive-block-path"},
        "conclusion_by_partition": {"4+3": "sigma>=0", "5+2": "sigma>0"},
    }, "universal hull-K2 owner changed")
    require(owners_by_name["PHYSICAL-UNIT-STAR-DNN"] == {
        "owner": "PHYSICAL-UNIT-STAR-DNN", "conclusion": "sigma>0",
        "scope": {
            "reduced_positive_hull": "hostile-unit-leaf-star",
            "center_component": "arbitrary-connected-bridge-free-rank-c",
            "closed_center_ranks": [0, 1, 2, 3, 4],
            "closed_c5_condition": "max(q_1,q_2)>=9",
            "ports": "arbitrary-repeated-or-coincident",
            "restored_zero_rank_material":
                "arbitrary-physical-bridge-chains-branching-and-finite-tree-payloads",
        },
    }, "physical unit-star owner scope changed")
    require(owners_by_name["R61-PHYSICAL-SINGLE-BLOCK"] == {
        "owner": "R61-PHYSICAL-SINGLE-BLOCK", "conclusion": "sigma>=0",
        "scope": {
            "reduced_positive_hull": "one hostile unit arm at center rank 6",
            "center_component": "exactly-one-positive-rank-cyclic-block",
            "separator": "one-actual-bridge",
            "ports": "arbitrary-vertices-on-both-sides",
            "tree_attachments": "arbitrary-finite-rooted-trees",
        },
    }, "physical R61 owner scope changed")
    require(overlay["open_rows"] == [
        {"center_rank": 5,
         "center_component": "arbitrary-bridge-free-rank-five-center",
         "center_positive_rank_cyclic_block_count": "at-least-two",
         "hostile_arm_cycles": [5, 5], "status": "OPEN_ROW_SPECIFIC_PROOF"},
        {"center_rank": 6, "center_block_count": "at-least-two-positive",
         "hostile_arms": 1, "status": "OPEN_ROW_SPECIFIC_PROOF"},
    ], "exact nontrivial-hull open rows changed")
    require(overlay["route_obstruction"] == {
        "row": "c=5,(C5,C5)",
        "universal_center_excess_required": "4sqrt(5)-4",
        "multiblock_center": "K4 vee C3 vee C3",
        "example_center_positive_block_profile": [3, 1, 1],
        "exact_center_excess": 5,
        "meaning": "universal-all-center-DNN-threshold-fails-not-graph-counterexample",
    }, "c=5 route obstruction changed")

    require(payload["one_positive_hull_multiblock_lane"] == {
        "axis": "number of positive all-global-bridge quotient components",
        "condition": ("unique rank-seven bridge-free component has at least "
                      "two positive-rank cyclic blocks"),
        "physical_hull_reduction_status":
            "OUTSIDE_NONTRIVIAL_HULL_HYPOTHESIS",
        "actual_bridge_forest": "MAY_BE_PRESENT",
        "bridge_free_packet_residual_relevance":
            "CONDITIONAL_ON_REGISTERED_PACKET_SPECIFIC_BRIDGE_DISPATCH",
        "all_19_owner_transport_theorem": "ABSENT",
        "census": "UNAUTHENTICATED",
        "forbid_finite_residual": True,
        "status": "OPEN",
    }, "one-positive-hull open lane changed")
    require(type(payload["one_positive_hull_multiblock_lane"]) is dict and
            payload["one_positive_hull_multiblock_lane"]["census"] ==
            "UNAUTHENTICATED",
            "one-positive-hull lane was laundered into a finite residual")
    require(payload["owner_rules"] == {
        "boundary_cut": "upstream-only",
        "nested_demands": "one-complete-first-boundary-territory",
        "positive_connectors": "packet-specific-oriented-dispatch-required",
        "rooted_descendants": "follow-unique-first-owner",
    }, "owner rules changed")

    owners = payload["verifier_owners"]
    require(set(owners) == set(CHILDREN) - {
        "r31-s-parent-gate", "universal-hull-k2", "physical-unit-star",
        "r61-physical-single-block"}, "child scope registry changed")
    require(not ({"universal-hull-k2", "physical-unit-star",
                  "r61-physical-single-block"} & set(owners)),
            "physical overlay was laundered into packet-key ownership")
    primary = [key for keys in owners.values() for key in keys if ":" not in key]
    require(set(primary) == set(PACKET_KEYS),
            "bridge-free packet verifier ownership is not exhaustive")
    require(len(primary) == len(set(primary)), "packet key has multiple primary verifiers")
    require(owners["r31-s-physical"] == ["R31-S"],
            "physical R31-S gate is not its primary closure owner")
    require(owners["r31-s-c4"] == ["R31-S:C4"] and
            owners["r31-s-marked-cut"] == ["R31-S:orbit-prerequisite"],
            "R31-S subordinate prerequisite scopes changed")
    require("r31-s-d3" not in owners,
            "synthetic R31-S:D3 diagnostic was assigned a closure owner")
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
    def overlay_owner(value, name):
        return next(owner for owner in value["physical_hull_owner_overlay"]["owners"]
                    if owner["owner"] == name)

    mutations = (
        lambda value: value["rows"].pop(),
        lambda value: value["rows"].append({"partition": [7], "direct_owner": "packet",
                                             "packet_keys": []}),
        lambda value: value["excluded_partitions"].clear(),
        lambda value: value["scope"].update(block_predicate="all-heptacyclic"),
        lambda value: value["scope"]["includes"].append("arbitrary-bridge-connectors"),
        lambda value: value["scope"]["excludes"].clear(),
        lambda value: value["conclusion"].update(strict=True),
        lambda value: value["packet_keys"].remove("R511-K22"),
        lambda value: value["rows"][4]["packet_keys"].remove("R31-S"),
        lambda value: value["verifier_owners"]["r61-k223"].append("R61-K110-0"),
        lambda value: value["verifier_owners"]["r31-s-physical"].clear(),
        lambda value: value["verifier_owners"].update(**{"r31-s-d3": ["R31-S"]}),
        lambda value: value["bridge_free_packet_residual"].append("R31-S"),
        lambda value: value.update(final_residual=["R31-S"]),
        lambda value: value["physical_hull_owner_overlay"]["domain"].update(
            one_positive_hull_excluded=False),
        lambda value: value["physical_hull_owner_overlay"].update(
            finite_census_claim=True),
        lambda value: overlay_owner(value, "universal-hull-k2")["scope"][
            "partitions"].pop(),
        lambda value: overlay_owner(value, "PHYSICAL-UNIT-STAR-DNN")["scope"].update(
            reduced_positive_hull="arbitrary-nontrivial-positive-hull"),
        lambda value: overlay_owner(value, "PHYSICAL-UNIT-STAR-DNN")["scope"][
            "closed_center_ranks"].append(5),
        lambda value: overlay_owner(value, "PHYSICAL-UNIT-STAR-DNN")["scope"].update(
            closed_c5_condition="all hostile arms"),
        lambda value: overlay_owner(value, "R61-PHYSICAL-SINGLE-BLOCK")["scope"].update(
            center_component="arbitrary-rank-six-center"),
        lambda value: value["physical_hull_owner_overlay"]["open_rows"].pop(),
        lambda value: value["physical_hull_owner_overlay"]["open_rows"][0].update(
            center_positive_rank_cyclic_block_count=2),
        lambda value: value["physical_hull_owner_overlay"]["open_rows"][0].update(
            center_positive_block_profile=[1, 1]),
        lambda value: value["physical_hull_owner_overlay"]["open_rows"][0].update(
            status="CLOSED"),
        lambda value: value["physical_hull_owner_overlay"]["route_obstruction"].update(
            meaning="graph-counterexample"),
        lambda value: value["one_positive_hull_multiblock_lane"].update(status="CLOSED"),
        lambda value: value["one_positive_hull_multiblock_lane"].update(
            bridge_free_packet_residual_relevance="OWNED_BY_19_PACKET_KEYS"),
        lambda value: value["one_positive_hull_multiblock_lane"].update(census=[]),
        lambda value: value["one_positive_hull_multiblock_lane"].update(
            all_19_owner_transport_theorem="PRESENT"),
        lambda value: value["one_positive_hull_multiblock_lane"].update(
            actual_bridge_forest="ABSENT"),
        lambda value: value["one_positive_hull_multiblock_lane"].pop(
            "actual_bridge_forest"),
        lambda value: value["one_positive_hull_multiblock_lane"].update(
            finite_residual=[]),
        lambda value: value["verifier_owners"].update(
            **{"physical-unit-star": ["R511-K22"]}),
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
        "heptacyclic multiblock master audit: typed fail-closed reduction passed\n"
        "partition scope: 14 non-(7) positive-block partitions; partition (7) excluded\n"
        f"bridge-free owner ledger: {len(PACKET_KEYS)} packet keys; packet residual: empty after registered bridge dispatch\n"
        "nontrivial physical hull overlay: unit-star DNN and R61 single-block owners authenticated\n"
        "open nontrivial-hull rows: c=5 arbitrary multiblock rank-five center with (C5,C5); c=6 multiblock center\n"
        "one-positive-hull multiblock bridge forest: OPEN; census: UNAUTHENTICATED\n"
        f"closed/prerequisite verifiers: {len(outputs)}; "
        f"executions: {2 * len(outputs)} normal/-O\n"
        f"hostile mutations rejected: {rejected}\n"
        "pinned physical-hull structural source: e09bdcfd99f85b4660678b1dbc70538bea6de0624b500ede8eae38eae9e639de\n"
        "conclusion: NOT ESTABLISHED for all connected rank-seven multiblock graphs\n"
        "status: OPEN; FAIL CLOSED PENDING TWO NONTRIVIAL-HULL ROWS AND ONE-POSITIVE-HULL BRIDGE-FOREST TRANSPORT"
    )
    if "--optimized-master-child" not in sys.argv and not sys.flags.optimize:
        child = subprocess.run([sys.executable, "-O", __file__, "--optimized-master-child"],
                               check=False, capture_output=True, text=True)
        require(child.returncode == 1, "optimized master did not fail closed")
        require(child.stderr == "", "optimized master wrote stderr")
        require(child.stdout.rstrip() == output, "normal/optimized master output mismatch")
    print(output)
    raise SystemExit(1)


if __name__ == "__main__":
    main()
