#!/usr/bin/env python3
"""Hostile tests for the exact marked-deletion topology/provenance mapper."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from collections import Counter
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
MAPPER = HERE / "rank-seven-order-nine-marked-deletion-mapper.py"
PILOT = HERE / "rank-seven-order-nine-marked-deletion-pilot-map.json"
FULL = HERE / "rank-seven-order-nine-marked-deletion-full-summary.json"


def load_mapper():
    spec = importlib.util.spec_from_file_location(
        "rank_seven_order_nine_marked_deletion_mapper", MAPPER
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load(path):
    return json.loads(path.read_bytes().decode("ascii"))


def test_pilot_reproduces_and_all_maps_are_unique_before_owner_import():
    mapper = load_mapper()
    payload = mapper.build("pilot")
    raw = mapper.canonical_bytes(payload)
    assert raw == PILOT.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == (
        "6c90f9a55034c4e22d1003a9c6c0f1f1e5603265c63b712b7a80077984e0259d"
    )
    assert payload["summary"]["case_total"] == 82
    assert payload["summary"]["mapping_status_counts"] == {
        "mapped-single-rank-six-kernel": 82
    }
    assert payload["summary"]["fixture_kernel_counts"] == {
        "354": 13, "436": 11, "452": 8, "479": 30,
        "490": 15, "491": 2, "866": 2, "872": 1,
    }
    assert all(record["owner_import"] == {
        "attempted": False, "reason": "topology/provenance stage only"
    } for record in payload["records"])
    assert all(
        record["rank_six_fixture_mapping"]["full_isomorphism"]
              ["canonical_parity_isomorphism_candidate_count"] >= 1
        for record in payload["records"]
    )
    assert all(
        len(record["rank_six_fixture_mapping"]["both_marked_provenance_tuples"]) == 2
        for record in payload["records"]
    )


def test_durable_80_residual_distribution_is_preserved():
    payload = load(PILOT)
    residual = [record for record in payload["records"]
                if record["case_kind"] ==
                "finite-favorable-cycle-residual-coordinate-target"]
    assert len(residual) == 80
    assert Counter(
        (record["rank_six_fixture_mapping"]["fixture_order"],
         record["rank_six_fixture_mapping"]["fixture_kernel"])
        for record in residual
    ) == Counter({
        (8, 866): 2,
        (7, 479): 30,
        (7, 490): 15,
        (7, 354): 12,
        (7, 436): 11,
        (7, 452): 8,
        (7, 491): 2,
    })
    assert all(record["source_target"]["same_parity_increment_pairs"].count(1) == 1
               for record in residual)


def test_hostile_78714_occurrences_1_and_13_have_exact_marked_lifts():
    payload = load(PILOT)
    hostile = {record["deleted_physical_path"]["path_index"]: record
               for record in payload["records"]
               if record["case_kind"] ==
               "hostile-two-coordinate-descendant-deletion"}
    assert set(hostile) == {1, 13}
    expected_lengths = [1, 3, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 3, 2]
    assert all(record["source_target"]["length_vector"] == expected_lengths
               for record in hostile.values())

    first = hostile[1]["rank_six_fixture_mapping"]
    assert (first["fixture_order"], first["fixture_kernel"]) == (8, 872)
    assert first["both_marked_provenance_tuples"] == [
        ["path", 9, 1], ["branch", 7]
    ]

    thirteenth = hostile[13]["rank_six_fixture_mapping"]
    assert (thirteenth["fixture_order"], thirteenth["fixture_kernel"]) == (7, 354)
    assert thirteenth["both_marked_provenance_tuples"] == [
        ["path", 6, 3], ["path", 6, 1]
    ]
    marked = thirteenth["marked_provenance"]
    assert [row["selected_target_transformed_index"] for row in marked] == [1, 0]
    lift = thirteenth["target_selection"]["descendant_lift"]["paths"][6]
    assert lift["selected_transformed_vertex_run_lengths"] == [3, 3]
    assert lift["actual_to_selected_transformed_index"] == [0, 0, 0, 1, 1, 1]


def test_full_summary_is_all_1615_rows_and_fail_closed_on_multiblocks():
    payload = load(FULL)
    assert payload["scope"] == "full"
    assert payload["records"] is None
    assert payload["source_frontier"] == {
        "orbit_rows": 1615,
        "physical_paths_per_row": 15,
        "physical_rows": 1945,
        "represented_order9_kernels": 115,
    }
    summary = payload["summary"]
    assert summary["case_total"] == 1615 * 15
    assert summary["mapping_status_counts"] == {
        "mapped-single-rank-six-kernel": 18353,
        "multiblock-or-nonsingleblock-rank-six-topology": 5872,
    }
    assert summary["positive_block_rank_profile_counts"] == {
        "3+3": 444, "4+1+1": 575, "4+2": 630,
        "5+1": 4223, "6": 18353,
    }
    assert summary["fixture_order_counts"] == {
        "7": 7909, "8": 8961, "9": 1483,
    }
    assert summary["owner_import_attempted"] is False


def test_opposite_parity_and_ambiguous_fixture_identity_are_rejected(monkeypatch):
    mapper = load_mapper()
    with pytest.raises(RuntimeError, match="same-parity descendant"):
        mapper.validate_target(((0, 0, 0, 1, 1),), [2], 0)

    fixtures = mapper.RankSixFixtures.load()
    first = fixtures.rows[0]
    adjacency = mapper.fixture_graph(first)
    duplicate = mapper.RankSixFixtures(fixtures.rows)
    duplicate.by_invariant[mapper.graph_invariant(adjacency)].append(
        (9999, first, adjacency)
    )
    with pytest.raises(RuntimeError, match="identity is nonunique"):
        duplicate.identify(tuple(("b", i) for i in range(first["n"])),
                           adjacency,
                           tuple({"nodes": (("b", u), ("b", v)), "edges": (0,)}
                                 for (u, v), multiplicity in zip(
                                     mapper.pair_index(first["n"])[0],
                                     first["code"], strict=True)
                                 for _ in range(multiplicity)))
