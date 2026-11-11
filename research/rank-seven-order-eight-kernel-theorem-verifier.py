#!/usr/bin/env python3
"""Fail-closed gate for the rank-seven/order-eight single-block theorem.

The gate composes pinned read-only exact certificate replays with the rank-seven
analytic reduction and the final induced-territory proof.  Full mode also
regenerates the exhaustive kernel fixture and complete order-eight parity/coarse
census, and freshly exact-replays all 29,000 direct-rational witness records.
The base-owner bridge reports four historical producer roots; the direct-pack
replay discharges one, leaving exactly three master-level producer trust roots.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import importlib.util
import lzma
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, NamedTuple, NoReturn

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = ROOT / "positive-square-energy" / "experiments"
HEPTACYCLIC = ROOT / "positive-square-energy" / "heptacyclic-general"
SELF = Path(__file__).resolve()

BASE = EXPERIMENTS / "rank7_order8_typed_precedence_bridge.py"
STRUCTURAL = EXPERIMENTS / "rank7_order8_structural_exact_verifier.py"
PACKETS = EXPERIMENTS / "verify_rank7_order8_packet_chain.py"
POST_XII = EXPERIMENTS / "rank7_order8_post_xii_shared_packet_lane.py"
SEMANTIC_CENSUS = EXPERIMENTS / "rank7_order8_semantic_census.py"
DIRECT_PACKS = EXPERIMENTS / "rank7_order8_direct_rational_pack_auditor.py"
EXACT_RATIONAL_ENGINE = EXPERIMENTS / "rank7_order8_exact_rational.py"
EXACT_RATIONAL_BASE = EXPERIMENTS / "rank6_order10_cubic_exact_rational.py"
PAYLOAD_FREE_LANES = EXPERIMENTS / "rank7_order8_payload_free_lanes.py"
ATOM_RECOGNIZER = EXPERIMENTS / "rank7_order7_symbolic_atom_recognizer.py"
CENSUS_PRODUCER = EXPERIMENTS / "rank7_order8_exact_residual_census.py"
KERNEL_CENSUS = ROOT / "research" / "rank-seven-kernel-frontier-census.py"
RANK_SIX_CENSUS = ROOT / "research" / "rank-six-kernel-census-verifier.py"
SINGLETON_RECONSTRUCTION = (ROOT / "research" /
                            "rank-seven-order-eight-singleton-reconstruction-verifier.py")
FINITE = ROOT / "research" / "tricyclic-finite-rational-certificates-verifier.py"
K4 = EXPERIMENTS / "k4_all_odd_exact_verify.py"
DOUBLED_TRIANGLE = ROOT / "research" / "doubled-triangle-all-length-certificate.py"

# Conservative callable closure below the imported rank-six exact engine.  These
# branches are not exercised by the committed all-MODE_SHARED direct packs, but
# they remain accepted callable source and therefore belong to the fail-closed
# Python registry rather than being excused as currently unreachable.
RANK_SIX_FRONTIER = EXPERIMENTS / "rank6_order10_cubic_frontier_census.py"
RANK_SIX_ATOM_SEARCH = EXPERIMENTS / "rank6_orders8_10_atom_ledger_search.py"
RANK_SIX_ORDER8 = EXPERIMENTS / "rank6_order8_sparse_pipeline.py"
RANK_SIX_ORDER9 = EXPERIMENTS / "rank6_order9_sparse_witness.py"
PENTACYCLIC = ROOT / "pentacyclic" / "research"
ORDER8_VECTOR_ENGINE = PENTACYCLIC / "order8-dim8-rational-canonical-frontiers-experiment.py"
ORDER7_VECTOR_ENGINE = PENTACYCLIC / "order7-dim7-rational-gram-experiment.py"
ORDER8_TETRA_CENSUS = PENTACYCLIC / "order8-cubic-tetra-census-experiment.py"
ORDER7_TETRA_CENSUS = PENTACYCLIC / "order7-tetra-census-experiment.py"

CENSUS_MANIFEST = EXPERIMENTS / "rank7_order8_exact_residual_census_manifest.json"
SELECTED_INDICES = EXPERIMENTS / "rank7_order8_rational_search_indices.json"
FINITE_OWNERS = EXPERIMENTS / "rank7_order8_packet_spectral_owners.json.xz"
SOURCE_REPORT = EXPERIMENTS / "rank7_order8_twelfth_induced_packet_gram_family.json"
COMBINED_LEDGER = EXPERIMENTS / "rank7_order8_combined_owner_ledger.json"
RANK_SIX_FIXTURE = ROOT / "research" / "fixtures" / "rank-six-kernels.json"
RANK_SEVEN_FIXTURE = ROOT / "research" / "fixtures" / "rank-seven-kernel-frontier-census.json"
RANK_FIVE_FIXTURE = ROOT / "research" / "fixtures" / "rank-five-kernels.json"
RANK_SIX_FRONTIER_ARTIFACT = EXPERIMENTS / "rank6_order10_cubic_frontier_census.json"
RANK_SIX_ATOM_ARTIFACT = EXPERIMENTS / "rank6_orders8_10_atom_ledger_classification.json"
ORDER8_TETRA_ARTIFACT = PENTACYCLIC / "order8-cubic-tetra-census.json"
ORDER7_TETRA_ARTIFACT = PENTACYCLIC / "order7-tetra-census.json"
REMOVABLE_EAR = HEPTACYCLIC / "rank-seven-removable-ear-census-theorem.md"
POST_REPORT = EXPERIMENTS / "rank7_order8_post_xii_shared_packet_lane.json"
POST_SOURCE = (EXPERIMENTS /
               "rank7_order8_after_twelfth_induced_packet_gram_family_remainder.jsonl.xz")
POST_OWNERS = EXPERIMENTS / "rank7_order8_post_xii_shared_packet_owners.jsonl.xz"
SINGLETON = EXPERIMENTS / "rank7_order8_after_post_xii_shared_packet_remainder.jsonl.xz"
REDUCTION = HEPTACYCLIC / "rank-seven-single-block-structural-theorem.md"
TERRITORY = HEPTACYCLIC / "rank-seven-order-eight-final-two-k4-territory.md"
TRICYCLIC_TEX = ROOT / "all-tricyclic-graphs" / "paper.tex"
TRICYCLIC_PDF = ROOT / "all-tricyclic-graphs" / "paper.pdf"
TRICYCLIC_AUDIT = ROOT / "all-tricyclic-graphs" / "HOSTILE_AUDIT.md"
TRICYCLIC_README = ROOT / "all-tricyclic-graphs" / "README.md"
GRAM = ROOT / "research" / "tricyclic-gram-obstruction-verifier.py"
COARSE_ENGINE = EXPERIMENTS / "rank7_parity_coarse_digest_census.py"

# The dependency trust boundary has three pairwise-disjoint categories.
# Category 1 is executed/imported by full replay.  Category 2 is a conservative
# fixed-path callable-body closure below the imported rank-six engine; it is
# pinned and AST-audited but is not described as executed or environment-pinned.
# Category 3 is documentary and is never imported by this gate.
EXECUTED_PYTHON_SHA256 = {
    "base_verifier": "f99c94d3781539fba444f91bedf6c6bba14ba96f0541e51d8c8d0877220eba03",
    "structural_verifier": "46851a4aa58d0b0ed0a3f63d0b0839755c057c0c4c671acf204011bd312b9415",
    "packet_verifier": "4410a45fb514831a0828e9064d091f0c6ee1ff17d037ee4cf611af0e4f3f7a87",
    "post_xii_verifier": "a8903c69287a531d5a4aa62fa514318daad0583c3690a7dcb20d62384ac60fd1",
    "semantic_census_verifier": "1b8c690cdd6992e0727ffd9853814edf0552ac2731f0529843a0c6a097f72495",
    "census_producer": "c55b037dbfd6dcf6971e1a1738e9cc507ff0fc7f0a9e76d0cda548e73e22e9a5",
    "direct_pack_verifier": "8c731b74a58e573500c4e4666742d726a2be8063d122ed2dfe9c29fde32e2b59",
    "exact_rational_engine": "0577103afb8be3f9f90d0635a37266281c9496a5b5d1d3349cb0c74ccdc1b8e5",
    "exact_rational_base": "fb419856225aeb513285ae5467233b1cccc096b9632170c6bbfac905abf08827",
    "payload_free_lanes": "278884b76bf490dc55f92a3c775565a74c3a94f67cf62178378af8899eff239c",
    "atom_recognizer": "10de4fb714c15756341a7dbddb5a4da9f8ce5e0393aacc9e9434d619ebce9734",
    "kernel_census_verifier": "220b2a10b8328509897bd7a130837058541f007e83365ddf1719d084baae86ca",
    "rank_six_census_verifier": "325b78066b626a00deaceb6a026377dd7f898a906c63c597f77831548585e1ee",
    "singleton_reconstruction_verifier": "51aa44bbf67e0c01aef186bee7c9bd547e5c1b63eeb1af33df5378a92d3b7c42",
    "finite_verifier": "fe272e94ee5d1ad549fe29b498f785df9fc298352ccfb3e67a1e4967461fde16",
    "k4_verifier": "0e4ef323a076c807a5aba0c80f0e385e5c3cee18ebd4d7e249928b345e6745a4",
    "doubled_triangle_verifier": "a27981b5bf6381edf6a8760477e6c99828bc9934d1d135d488670c35493b199d",
}
EXECUTED_PYTHON_PATHS = {
    "base_verifier": BASE,
    "structural_verifier": STRUCTURAL,
    "packet_verifier": PACKETS,
    "post_xii_verifier": POST_XII,
    "semantic_census_verifier": SEMANTIC_CENSUS,
    "census_producer": CENSUS_PRODUCER,
    "direct_pack_verifier": DIRECT_PACKS,
    "exact_rational_engine": EXACT_RATIONAL_ENGINE,
    "exact_rational_base": EXACT_RATIONAL_BASE,
    "payload_free_lanes": PAYLOAD_FREE_LANES,
    "atom_recognizer": ATOM_RECOGNIZER,
    "kernel_census_verifier": KERNEL_CENSUS,
    "rank_six_census_verifier": RANK_SIX_CENSUS,
    "singleton_reconstruction_verifier": SINGLETON_RECONSTRUCTION,
    "finite_verifier": FINITE,
    "k4_verifier": K4,
    "doubled_triangle_verifier": DOUBLED_TRIANGLE,
}

CALLABLE_PYTHON_SHA256 = {
    "rank_six_frontier_census": "536981d000d417b7edaa94461ad3bfa6540c1f400e560c244eec585cae0000de",
    "rank_six_atom_search": "6b39d2d1b33d251e505b4b79bd3a4703a440407119c803a26afa1266a2c9461f",
    "rank_six_order8_pipeline": "3b262613edfee4961fe990675c9a7003d595ed58c2b034d928c99daee1345f42",
    "rank_six_order9_witness": "0b916f2844acb878ca33f9203db8ac6cb2b165fe417f3a0b6625cf1776b0d4a6",
    "order8_vector_engine": "dc0676b6feae4c555ace842a3bf278c3e438ffe84e848b37e727ba5233d1a565",
    "order7_vector_engine": "0d7acde3eec194772dd00f7e4897e0355e2347482c8e0fdfce26f9e8473394cc",
    "order8_tetra_census": "a512746954054455fbd46745748dcb46d656fde62492bad56e011a8efa1dbb67",
    "order7_tetra_census": "8433f2b06c000ef1bfd777a536fb370a1eaf9ac1aaf0a9bf640816d26857e64a",
}
CALLABLE_PYTHON_PATHS = {
    "rank_six_frontier_census": RANK_SIX_FRONTIER,
    "rank_six_atom_search": RANK_SIX_ATOM_SEARCH,
    "rank_six_order8_pipeline": RANK_SIX_ORDER8,
    "rank_six_order9_witness": RANK_SIX_ORDER9,
    "order8_vector_engine": ORDER8_VECTOR_ENGINE,
    "order7_vector_engine": ORDER7_VECTOR_ENGINE,
    "order8_tetra_census": ORDER8_TETRA_CENSUS,
    "order7_tetra_census": ORDER7_TETRA_CENSUS,
}

# Exactly the fixed data admitted by the conservative category-2 policy.  The
# order-ten census is included because the generic residual_rows callable body
# has a fixed census.OUTPUT read.  Caller-selected caches and argparse-only
# --verify/results/cache paths are deliberately not fixed-path edges.
CALLABLE_DATA_SHA256 = {
    "rank_six_fixture": "5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476",
    "rank_six_atom_artifact": "cc20f4c684ef269297cd7c1d2bc888508fdc31f16cc26e8cb1c2e86792052059",
    "rank_six_frontier_artifact": "9398293928c8ad8dfe53788f89921a3d6764a2d31eba9ec17b5e00b6578397b5",
    "rank_five_fixture": "027c84d6dd777a29b3dc93389ab30b5d43f6507eddceb4ea286f1240da95b884",
    "order8_tetra_artifact": "096a3ec3213bdf02f322a33790c84b206cd65b9a665220dbd76067de25947488",
    "order7_tetra_artifact": "a9a05f50cf3db61cf104cd88c966f11064671d7b8027a83d065721e8b395d8b1",
}
CALLABLE_DATA_PATHS = {
    "rank_six_fixture": RANK_SIX_FIXTURE,
    "rank_six_atom_artifact": RANK_SIX_ATOM_ARTIFACT,
    "rank_six_frontier_artifact": RANK_SIX_FRONTIER_ARTIFACT,
    "rank_five_fixture": RANK_FIVE_FIXTURE,
    "order8_tetra_artifact": ORDER8_TETRA_ARTIFACT,
    "order7_tetra_artifact": ORDER7_TETRA_ARTIFACT,
}

# Category-1 fixed data closure: master-level linkage inputs plus every fixed
# source-artifact receiver discovered in the executed Python registry.  Some
# bytes are also authenticated inside children; duplicating their pins here
# makes every observed fixed read resolve mechanically to one registry record.
EXECUTED_DATA_SHA256 = {
    "census_manifest": "5d41e78a2f688f4c3064cb88f1d6d475008d36c84f892edc4cba28ade424fe98",
    "selected_indices": "245cceaab164ba9c2a604d0db8b09a65598fd52084b1df2363911c6d1d4d3a59",
    "rank_seven_fixture": "a241139ab54ce4cce1ab3812887359edb241c0abfb1018e804b4a5f86762cfd5",
    "finite_owners": "f9f23e0a28d33b6b9c79441fbbdd445ea71ce84a8f9cd033015e7ebd9e7622cf",
    "post_xii_source_report": "dc4e868dae60db6b9504b2288f983ef1d98cbfa36245178e95f778fa277293c5",
    "post_xii_report": "2d94c557a8a74845098d5ced351acb474e6f950ffb9072919db11e95e7b3cdb0",
    "combined_owner_ledger": "5700803dd3989853440291423a6cae736978125cbcf3a13ffa89281e7b5ea84e",
    "post_xii_remainder": "bbadc801837908ada49cdb53a83fb1afa46a5a240a77ecb18c66fbb0a06a6340",
}
EXECUTED_DATA_PATHS = {
    "census_manifest": CENSUS_MANIFEST,
    "selected_indices": SELECTED_INDICES,
    "rank_seven_fixture": RANK_SEVEN_FIXTURE,
    "finite_owners": FINITE_OWNERS,
    "post_xii_source_report": SOURCE_REPORT,
    "post_xii_report": POST_REPORT,
    "combined_owner_ledger": COMBINED_LEDGER,
    "post_xii_remainder": SINGLETON,
}

DOCUMENTARY_PROOF_SHA256 = {
    "removable_ear_theorem": "f50afbd13f29e9374969b69087a73d5f1b6b3ef8c6b18bb08b46ebd97cee6a2e",
    "rank_seven_reduction": "f1daf9109f4843aa2db149c974fb21c847bb6f8144275201aebabed7fe4ea516",
    "singleton_territory": "9d7385473e5a2f32700f44aed86e7a06039012932b75f6812c28717c04b25238",
    "tricyclic_tex": "13f8f8c7996c0f58f764c52b4a5b915132038e2ce38d3e56285f1bf952990fc1",
    "tricyclic_pdf": "57c876516e891cd74b016da495ed26200a137cd073296961b3170c95e84a76cc",
    "tricyclic_audit": "6e5bee956c412454fd9dc59e020b5dfe35205c336a6c0e740aea96f0f90fa92f",
    "tricyclic_readme": "4de20b0a78f7598dc8172a118eaf178272494a9ee13cfbabc3fbabfa688a3f15",
    "gram_verifier_not_executed": "aeec6f4471a0a78b6807275217ee22e9909f07a8e356d8126c03ea175d9a8126",
    "coarse_networkx_engine_not_loaded": "d285a1c29cace4cb30882662e786cf1e5086ebc579676a3aa114a18e2365b2a5",
}
DOCUMENTARY_PROOF_PATHS = {
    "removable_ear_theorem": REMOVABLE_EAR,
    "rank_seven_reduction": REDUCTION,
    "singleton_territory": TERRITORY,
    "tricyclic_tex": TRICYCLIC_TEX,
    "tricyclic_pdf": TRICYCLIC_PDF,
    "tricyclic_audit": TRICYCLIC_AUDIT,
    "tricyclic_readme": TRICYCLIC_README,
    "gram_verifier_not_executed": GRAM,
    "coarse_networkx_engine_not_loaded": COARSE_ENGINE,
}


# Declared local dependency-edge oracle.  Locations are exact AST spans
# ``(lineno, col_offset, end_lineno, end_col_offset)`` in the named source.
# Every observed edge is normalized with both registry keys and repository paths.
EDGE_DYNAMIC = "dynamic-import"
EDGE_READ = "fixed-read"
CAT_EXECUTED_PYTHON = "executed-python"
CAT_EXECUTED_DATA = "executed-data"
CAT_CALLABLE_PYTHON = "callable-unreached-python"
CAT_CALLABLE_DATA = "callable-unreached-data"
POLICY_EXECUTED = "executed-full-replay"
POLICY_CALLABLE = "conservative-callable-body"
Span = tuple[int, int, int, int]


class EdgeRecord(NamedTuple):
    kind: str
    source_key: str
    source_path: str
    target_key: str
    target_path: str
    target_category: str
    location: Span
    call_policy: str
    provenance: str


# One dynamic loader helper can have several admitted fixed callers.  The site
# table therefore intentionally contains repeated loader spans with distinct
# targets/provenance.  Read sites are direct fixed receivers.
EDGE_SITE_POLICY = (
    ("semantic_census_verifier", (29, 11, 30, 90), EDGE_DYNAMIC),
    ("semantic_census_verifier", (39, 10, 39, 36), EDGE_READ),
    ("kernel_census_verifier", (32, 11, 32, 86), EDGE_DYNAMIC),
    ("kernel_census_verifier", (176, 16, 176, 35), EDGE_READ),
    ("singleton_reconstruction_verifier", (206, 26, 206, 46), EDGE_READ),
    ("singleton_reconstruction_verifier", (220, 27, 220, 48), EDGE_READ),
    ("singleton_reconstruction_verifier", (238, 26, 238, 46), EDGE_READ),
    ("direct_pack_verifier", (115, 11, 115, 61), EDGE_DYNAMIC),
    ("exact_rational_engine", (56, 11, 56, 61), EDGE_DYNAMIC),
    ("exact_rational_engine", (74, 10, 74, 35), EDGE_READ),
    ("payload_free_lanes", (69, 11, 69, 92), EDGE_DYNAMIC),
    ("post_xii_verifier", (168, 11, 168, 94), EDGE_DYNAMIC),
    ("exact_rational_base", (50, 11, 50, 86), EDGE_DYNAMIC),
    ("exact_rational_base", (229, 15, 229, 100), EDGE_DYNAMIC),
    ("exact_rational_base", (211, 25, 211, 61), EDGE_READ),
    ("exact_rational_base", (75, 45, 75, 77), EDGE_READ),
    ("rank_six_frontier_census", (48, 10, 48, 29), EDGE_READ),
    ("rank_six_atom_search", (38, 11, 38, 61), EDGE_DYNAMIC),
    ("rank_six_atom_search", (417, 16, 417, 37), EDGE_READ),
    ("rank_six_order8_pipeline", (64, 10, 64, 29), EDGE_READ),
    ("rank_six_order8_pipeline", (348, 11, 348, 92), EDGE_DYNAMIC),
    ("rank_six_order9_witness", (52, 11, 52, 61), EDGE_DYNAMIC),
    ("rank_six_order9_witness", (63, 10, 63, 29), EDGE_READ),
    ("order8_vector_engine", (207, 11, 207, 81), EDGE_DYNAMIC),
    ("order7_vector_engine", (240, 11, 240, 81), EDGE_DYNAMIC),
    ("order8_tetra_census", (38, 10, 38, 29), EDGE_READ),
    ("order8_tetra_census", (184, 10, 184, 31), EDGE_READ),
    ("order7_tetra_census", (79, 10, 79, 29), EDGE_READ),
    ("order7_tetra_census", (154, 10, 154, 31), EDGE_READ),
)



# Generic dynamic loader parameters are resolved from these exact caller nodes.
# Each tuple is (source, loader span, caller span, positional argument index,
# provenance label).  Targets are never stored here.
DYNAMIC_CALLER_POLICY = (
    ("direct_pack_verifier", (115, 11, 115, 61), (303, 13, 303, 72), 1,
     "audit_and_replay/load_module"),
    ("direct_pack_verifier", (115, 11, 115, 61), (408, 13, 408, 74), 1,
     "self_test/load_module"),
    ("exact_rational_engine", (56, 11, 56, 61), (63, 7, 63, 54), 1,
     "module initialization/load_module"),
    ("exact_rational_engine", (56, 11, 56, 61), (69, 17, 69, 69), 1,
     "lanes_module/load_module"),
    ("rank_six_atom_search", (38, 11, 38, 61), (305, 17, 305, 78), 1,
     "residuals_by_order/load"),
    ("rank_six_atom_search", (38, 11, 38, 61), (309, 17, 309, 77), 1,
     "residuals_by_order/load"),
    ("rank_six_atom_search", (38, 11, 38, 61), (313, 18, 313, 86), 1,
     "residuals_by_order/load"),
    ("rank_six_order9_witness", (52, 11, 52, 61), (59, 7, 59, 57), 1,
     "module initialization/load_module"),
    ("rank_six_order9_witness", (52, 11, 52, 61), (89, 13, 89, 67), 1,
     "load_engine/load_module"),
)

# Dynamic loader sites excluded by exact span.  This producer is imported with
# a pure injected stdlib engine, so its legacy NetworkX loader is documentary.
DYNAMIC_SITE_EXCLUSIONS = {
    ("census_producer", (54, 11, 54, 87)):
        "legacy engine excluded by injected pure-engine execution policy",
}

# Exact caller/default policy: the order-ten atom search calls residual_rows
# without cache_path, so its line-61 caller-selected read is unreachable.  The
# hostile oracle mutates this actual call, not this declaration.
DEFAULT_CALL_POLICY = (
    ("rank_six_atom_search", 316, "exact_rational_base",
     "residual_rows", "cache_path", None),
)

# True variable-input reads are outside the fixed-path edge set.  Every exclusion
# is frozen by source, exact call span, and exact AST expression; no unresolved
# fixed receiver is suppressed by this policy.
EXCLUDED_READ_POLICY = (
    ("structural_verifier", (163, 8, 163, 32),
     "(HERE / name).read_bytes()"),
    ("exact_rational_base", (61, 44, 61, 67), "cache_path.read_bytes()"),
    ("exact_rational_base", (861, 34, 861, 63), "args.verify_pack.read_bytes()"),
    ("rank_six_frontier_census", (466, 14, 466, 38), "args.verify.read_bytes()"),
    ("rank_six_order8_pipeline", (746, 30, 746, 59),
     "args.verify_pack.read_bytes()"),
    ("rank_six_order9_witness", (142, 44, 142, 67), "cache_path.read_bytes()"),
    ("order8_vector_engine", (331, 29, 331, 68),
     "args.verify.read_text(encoding='ascii')"),
    ("order7_vector_engine", (375, 29, 375, 68),
     "args.verify.read_text(encoding='ascii')"),
)



# Initialized after the derivation helpers below.
DEPENDENCY_EDGE_POLICY: tuple[EdgeRecord, ...]

ARTIFACT_SHA256 = {
    "post_report": "2d94c557a8a74845098d5ced351acb474e6f950ffb9072919db11e95e7b3cdb0",
    "post_source_xz": "de3fa584558684d6ffd8485b31707fc20f2fdb550d68c4a91116feda6b4464e6",
    "post_source_raw": "a6fb784238ae4d04b9e90d34939dc7658724684a9262eb7237f2197cc686c918",
    "post_owners_xz": "9e50f7eb752f1a03eedf395550328c755216346badb5df77ae1b0fe03ef411e0",
    "post_owners_raw": "8ae95c887177a0c4a3db346e063249518f876e16a06f11fcf07d1e0ea3b84e07",
    "post_remainder_xz": "bbadc801837908ada49cdb53a83fb1afa46a5a240a77ecb18c66fbb0a06a6340",
    "post_remainder_raw": "619ec23ae2435f06140ff94a98b56acc16571c71206fab132c71cdecc950229b",
}

CHILD_OUTPUT_SHA256 = {
    "base": "fd5a5bc5434af1e8c1f82da7f69b5c71e6b8234826d73bdc4c08e3c7cfd874fa",
    "structural": "412fbe20b7435c19897363cd3263f7b4080b79886e5cd811a4ecdbb6a147ad57",
    "packets": "0d15bd6d6addc534b160ae624555620e37a76a3e023d2c2f04e9696d23f3dd78",
    "finite": "86f4ad87b1cc5a84817d630f2fb448045ce207d345c185c7b96bf38895c4a617",
    "k4": "cb5434669fd3aacea9ca07e7a4d75f076a63a19f718806b394234996f52b95f7",
    "doubled_triangle": "a0b9311d8173972c4ac529c326366391ae5df9928079824ff5c0a6c601848222",
    "semantic_census": "5e8b566f541aab9362d71cbf46f51f90a8c0161c148cb11a7698b77b7f4fa1a2",
    "direct_packs": "9b19cb82ab4b462052840406272d24715bf28de2503efa387a6dc648c6f66ce2",
    "kernel_census": "1c22c2cfa9f83e1eed455b244a3b1ab899b75df36ee1241fd2d71873ef807acf",
    "singleton_reconstruction": "ee9f17f37c4bc0c507ba70145e10194943f251c8046b85bda4cc138a5682ea49",
}

CERTIFICATE_SHA256 = {
    "base_hostile_audit": "0dcb739c00f7b06f54a9430b8dede9019ac6c0a1abd57c5a1322b4229723f398",
    "tricyclic_finite": "6d499af761ffa7317a431e5150dac59317618f508896be2c3ed77b250b43c901",
    "tricyclic_k4": "b0c4ed64a12ccabe0a8a38cb9fdb85622d8f7c2d07bdf53f75eb1700a684fa39",
    "tricyclic_doubled_triangle": "b293eef0d7742da6ecd2c7af35882be14e97811922493121900e65a6705f01e8",
}

SINGLETON_ROW = [
    416536, 416987, 6832,
    [[0, 3, 1], [0, 6, 1], [0, 7, 1], [1, 2, 1], [1, 4, 1], [1, 5, 1],
     [2, 4, 1], [2, 5, 1], [3, 6, 1], [3, 7, 1], [4, 5, 1], [4, 7, 1],
     [5, 6, 1], [6, 7, 1]],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1], 2,
]
OWNER_COUNTS = {
    "payload_free": 605,
    "direct_rational": 29000,
    "scalar_sos_exclusive": 194351,
    "typed_diagonal_exclusive": 185309,
    "boundary_rescue": 296,
    "structural_I_III": 245,
    "packet_IV_XII": 29013,
    "post_XII_packets": 54597,
    "singleton_territory": 1,
}
EXPECTED_CHAIN = (83856, 83611, 54598, 1)
BASE_TRUST_ROOTS = (
    "payload-free recognizer semantics",
    "raw scalar-SOS membership semantics (only its report and exclusive set are pinned)",
    "the 492,812 expensive typed searches behind the receipts",
)
# The historical base child predates the fresh direct-pack replay and honestly
# reports the fourth item.  It is validated as history, not propagated as a
# master trust root.
HISTORICAL_BASE_REPORT_ROOTS = BASE_TRUST_ROOTS + (
    "29,000 direct-rational witness packs",
)
DIRECT_INPUT_SHA256 = {
    "atom_recognizer": "10de4fb714c15756341a7dbddb5a4da9f8ce5e0393aacc9e9434d619ebce9734",
    "combined_owner_indices": "1dacaf02fc546c634ba879bdd1af49774040d963e09a40331bba77bdff50c6d5",
    "combined_owner_ledger": "5700803dd3989853440291423a6cae736978125cbcf3a13ffa89281e7b5ea84e",
    "exact_rational_base": "fb419856225aeb513285ae5467233b1cccc096b9632170c6bbfac905abf08827",
    "exact_rational_engine": "0577103afb8be3f9f90d0635a37266281c9496a5b5d1d3349cb0c74ccdc1b8e5",
    "lane_union_report": "ca60c847f59d0d0c52fe411944852f3134debc39384f88daae95be67d84b32a9",
    "payload_free_lanes": "278884b76bf490dc55f92a3c775565a74c3a94f67cf62178378af8899eff239c",
    "rational_search_indices": "245cceaab164ba9c2a604d0db8b09a65598fd52084b1df2363911c6d1d4d3a59",
    "residual_cache": "0e31fb87d7bfa8e01d8cf168240cb2cc164673628f2c22b9e14347186cea7502",
    "residual_manifest": "5d41e78a2f688f4c3064cb88f1d6d475008d36c84f892edc4cba28ade424fe98",
}
DIRECT_ASSERT_FREE_SHA256 = {
    name: DIRECT_INPUT_SHA256[name]
    for name in ("atom_recognizer", "exact_rational_base",
                 "exact_rational_engine", "payload_free_lanes")
}
DIRECT_RECEIPT_SCHEMA = (
    "rank-seven-order-eight-direct-pack-exact-replay-v1"
)
DIRECT_RECEIPT_KEYS = {
    "assert_free_source_sha256", "coverage", "execution_semantics",
    "input_sha256", "owner_linkage", "pack_receipts",
    "residual_cache_raw_sha256", "schema", "status",
}
DIRECT_COVERAGE = {
    "gap_free_row_range": [0, 29000],
    "mode_shared_rows": 29000,
    "packs": 25,
    "scheduler_manifests": 24,
    "targets": 435000,
}
DIRECT_OWNER_FIELDS = [
    "stream_index", "source_index", "global_kernel", "support",
    "multiplicities", "parity_row", "orbit_size",
]
DIRECT_EXECUTION_SEMANTICS = (
    "fresh_canonical_decode_and_exact_fraction_replay"
)
DIRECT_OWNER_STREAM_SHA256 = (
    "ede7aac3df4343e116d7c197b4e9869ea851794735ee90e1cc72883d8571d35b"
)
DIRECT_CACHE_RAW_SHA256 = (
    "b56459cb832370340c7d44c1dca77e97adb59192f9f2703df739f048c25e3d30"
)
SEMANTIC_ACTION_EQUIVALENCE_RECEIPT = {
    "action_count_histogram": [[1, 2554], [2, 1166], [4, 229], [6, 4],
                               [8, 41], [12, 9], [14, 1], [16, 9],
                               [24, 1], [32, 1]],
    "audit_kind": "prior-exact-legacy-versus-stdlib-action-tuple-equality",
    "kernels": 4015,
    "transcript_sha256":
        "807a3bb1220e620fe9dd1c872c055c1419f585030a3791abfe15e205219cd75c",
}
EXPECTED_POST_RECEIPT = {
    "hostile_mutations_rejected": 11,
    "owned": 54597,
    "owner_artifact_sha256": ARTIFACT_SHA256["post_owners_xz"],
    "remainder_artifact_sha256": ARTIFACT_SHA256["post_remainder_xz"],
    "remaining": 1,
    "report_sha256": ARTIFACT_SHA256["post_report"],
}
POST_PROOF_RECEIPT_SHA256 = (
    "1dbd2337043e283e4b8913b89151da6b000cbc516a822f3b5f24bbf94e89eb4b"
)

Json = Any


def fail(message: str) -> NoReturn:
    raise RuntimeError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest(path: Path) -> str:
    return sha256(path.read_bytes())


def canonical_bytes(value: Json) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def strict_json(raw: bytes, label: str, *, canonical: bool = True) -> Json:
    def pairs(items: list[tuple[str, Json]]) -> dict[str, Json]:
        result: dict[str, Json] = {}
        for key, value in items:
            require(type(key) is str and key not in result,
                    f"{label}: duplicate or non-string key")
            result[key] = value
        return result

    try:
        value = json.loads(
            raw.decode("ascii"), object_pairs_hook=pairs,
            parse_constant=lambda token: fail(f"{label}: non-finite token {token}"),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"{label}: invalid JSON") from error
    if canonical:
        require(raw == canonical_bytes(value), f"{label}: noncanonical JSON")
    return value


def exact_int(value: Json, label: str, minimum: int = 0) -> int:
    require(type(value) is int and value >= minimum, f"{label}: invalid exact integer")
    return value


def audit_pinned_registry(paths: dict[str, Path], pins: dict[str, str],
                          label: str) -> None:
    require(set(paths) == set(pins), f"{label} registry keys changed")
    for name, path in paths.items():
        require(path.is_file(), f"missing {label} dependency: {name}")
        require(digest(path) == pins[name], f"{label} bytes changed: {name}")


def audit_source_pins() -> None:
    """Audit exact, pairwise-disjoint executed/callable/documentary registries."""
    categories = (
        set(EXECUTED_PYTHON_PATHS.values()) | set(EXECUTED_DATA_PATHS.values()),
        set(CALLABLE_PYTHON_PATHS.values()) | set(CALLABLE_DATA_PATHS.values()),
        set(DOCUMENTARY_PROOF_PATHS.values()),
    )
    require(all(categories[left].isdisjoint(categories[right])
                for left in range(3) for right in range(left + 1, 3)),
            "executed/callable/documentary registries overlap")
    require(len(CALLABLE_PYTHON_PATHS) == 8 and len(CALLABLE_DATA_PATHS) == 6,
            "callable closure is not exactly eight Python and six data files")
    audit_pinned_registry(EXECUTED_PYTHON_PATHS, EXECUTED_PYTHON_SHA256,
                          "executed Python")
    audit_pinned_registry(EXECUTED_DATA_PATHS, EXECUTED_DATA_SHA256,
                          "executed data")
    audit_pinned_registry(CALLABLE_PYTHON_PATHS, CALLABLE_PYTHON_SHA256,
                          "callable Python")
    audit_pinned_registry(CALLABLE_DATA_PATHS, CALLABLE_DATA_SHA256,
                          "callable data")
    audit_pinned_registry(DOCUMENTARY_PROOF_PATHS, DOCUMENTARY_PROOF_SHA256,
                          "documentary proof")


def _python_registry_paths() -> dict[str, Path]:
    return {**EXECUTED_PYTHON_PATHS, **CALLABLE_PYTHON_PATHS}


def _category_maps(category_overrides: dict[str, str] | None = None
                   ) -> tuple[dict[str, str], dict[str, Path]]:
    """Return all labels but only the public Python source domain.

    The frozen hostile-audit adapter builds syntax trees from
    ``_python_registry_paths()`` and requires this second return value to be that
    same mapping.  Fixed data remain category-labelled targets; the pure
    observation routine augments the Python paths with their separately pinned
    data registry before resolving edges.
    """
    categories = {}
    all_paths = {}
    for category, registry in (
        (CAT_EXECUTED_PYTHON, EXECUTED_PYTHON_PATHS),
        (CAT_EXECUTED_DATA, EXECUTED_DATA_PATHS),
        (CAT_CALLABLE_PYTHON, CALLABLE_PYTHON_PATHS),
        (CAT_CALLABLE_DATA, CALLABLE_DATA_PATHS),
    ):
        for name, path in registry.items():
            require(name not in categories and path not in all_paths.values(),
                    "dependency category registry collision")
            categories[name] = category
            all_paths[name] = path
    for name, category in (category_overrides or {}).items():
        require(name in categories and category in {
            CAT_EXECUTED_PYTHON, CAT_EXECUTED_DATA,
            CAT_CALLABLE_PYTHON, CAT_CALLABLE_DATA,
        }, "invalid dependency category override")
        categories[name] = category
    python_paths = _python_registry_paths()
    require(set(python_paths) ==
            set(EXECUTED_PYTHON_PATHS) | set(CALLABLE_PYTHON_PATHS) and
            all(all_paths[name] == path for name, path in python_paths.items()),
            "public Python registry changed during category derivation")
    return categories, python_paths


def _call_name(call: ast.Call) -> str:
    function = call.func
    if isinstance(function, ast.Name):
        return function.id
    if isinstance(function, ast.Attribute):
        return function.attr
    return ""


def _span(node: ast.AST) -> Span:
    return (node.lineno, node.col_offset, node.end_lineno, node.end_col_offset)


def _repo_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def _policy_for(source: str, target: str, categories: dict[str, str]) -> str:
    return (POLICY_CALLABLE if
            (categories[source] == CAT_CALLABLE_PYTHON or
             categories[target] in {CAT_CALLABLE_PYTHON, CAT_CALLABLE_DATA})
            else POLICY_EXECUTED)


def _edge_record(kind: str, source: str, target: str, location: Span,
                 provenance: str, categories: dict[str, str],
                 paths: dict[str, Path]) -> EdgeRecord:
    return EdgeRecord(kind, source, _repo_path(paths[source]), target,
                      _repo_path(paths[target]), categories[target], location,
                      _policy_for(source, target, categories), provenance)


def _format_edge(record: EdgeRecord) -> str:
    return ("EdgeRecord(kind={0.kind!r},source={0.source_key!r},"
            "source_path={0.source_path!r},target={0.target_key!r},"
            "target_path={0.target_path!r},target_category={0.target_category!r},"
            "location={0.location!r},"
            "call_policy={0.call_policy!r},provenance={0.provenance!r})"
            ).format(record)


def _format_edge_difference(missing: set[EdgeRecord],
                            surplus: set[EdgeRecord]) -> str:
    key = lambda record: tuple(record)
    missing_text = "[" + ",".join(_format_edge(record)
                                    for record in sorted(missing, key=key)) + "]"
    surplus_text = "[" + ",".join(_format_edge(record)
                                    for record in sorted(surplus, key=key)) + "]"
    return f"dependency edge mismatch; missing={missing_text}; surplus={surplus_text}"


def _node_at(tree: ast.AST, span: Span, kinds: tuple[type[ast.AST], ...],
             expression: str | None = None) -> ast.AST | None:
    matches = [node for node in ast.walk(tree)
               if isinstance(node, kinds) and _span(node) == span and
               (expression is None or ast.unparse(node) == expression)]
    require(len(matches) <= 1, f"ambiguous AST span: {span}")
    return matches[0] if matches else None


def _module_assignments(tree: ast.AST) -> dict[str, ast.AST]:
    """Return single-name module assignments, rejecting ambiguous rebinding."""
    result: dict[str, ast.AST] = {}
    ambiguous = set()
    for statement in getattr(tree, "body", ()):
        if isinstance(statement, ast.Assign):
            targets = statement.targets
            value = statement.value
        elif isinstance(statement, ast.AnnAssign):
            targets = (statement.target,)
            value = statement.value
        else:
            continue
        if value is None:
            continue
        for target in targets:
            if not isinstance(target, ast.Name):
                continue
            if target.id in result:
                ambiguous.add(target.id)
            else:
                result[target.id] = value
    for name in ambiguous:
        result.pop(name, None)
    return result


def _path_value(expression: ast.AST, assignments: dict[str, ast.AST],
                source_path: Path, seen: frozenset[str] = frozenset()) -> Path | None:
    """Resolve a deliberately small, deterministic constant Path expression set."""
    if isinstance(expression, ast.Name):
        if expression.id == "__file__":
            return source_path.resolve()
        if expression.id in seen or expression.id not in assignments:
            return None
        return _path_value(assignments[expression.id], assignments, source_path,
                           seen | {expression.id})
    if isinstance(expression, ast.Constant) and isinstance(expression.value, str):
        return Path(expression.value)
    if isinstance(expression, ast.Call) and len(expression.args) == 1 and not expression.keywords:
        function = expression.func
        is_path = ((isinstance(function, ast.Name) and function.id == "Path") or
                   (isinstance(function, ast.Attribute) and function.attr == "Path" and
                    ((isinstance(function.value, ast.Name) and
                      function.value.id == "pathlib") or
                     (isinstance(function.value, ast.Call) and
                      isinstance(function.value.func, ast.Name) and
                      function.value.func.id == "__import__" and
                      len(function.value.args) == 1 and
                      isinstance(function.value.args[0], ast.Constant) and
                      function.value.args[0].value == "pathlib"))))
        if is_path:
            return _path_value(expression.args[0], assignments, source_path, seen)
    if isinstance(expression, ast.Attribute):
        base = _path_value(expression.value, assignments, source_path, seen)
        if base is None:
            return None
        if expression.attr == "parent":
            return base.parent
        if expression.attr == "resolve":
            return None
    if (isinstance(expression, ast.Call) and not expression.args and
            not expression.keywords and isinstance(expression.func, ast.Attribute) and
            expression.func.attr == "resolve"):
        base = _path_value(expression.func.value, assignments, source_path, seen)
        return None if base is None else base.resolve()
    if isinstance(expression, ast.Subscript) and isinstance(expression.value, ast.Attribute):
        attribute = expression.value
        if attribute.attr == "parents":
            base = _path_value(attribute.value, assignments, source_path, seen)
            index = expression.slice
            if (base is not None and isinstance(index, ast.Constant) and
                    type(index.value) is int and index.value >= 0):
                try:
                    return base.parents[index.value]
                except IndexError:
                    return None
    if isinstance(expression, ast.BinOp) and isinstance(expression.op, ast.Div):
        left = _path_value(expression.left, assignments, source_path, seen)
        right = _path_value(expression.right, assignments, source_path, seen)
        if left is not None and right is not None:
            return left / right
    return None


def _receiver_target(receiver: ast.AST, source: str, tree: ast.AST,
                     paths: dict[str, Path]) -> str | None:
    """Resolve aliases, qualified module paths, and constant Path joins to a key."""
    if (isinstance(receiver, ast.Attribute) and receiver.attr == "OUTPUT" and
            isinstance(receiver.value, ast.Name) and receiver.value.id == "census" and
            source == "exact_rational_base"):
        return "rank_six_frontier_artifact"
    assignments = _module_assignments(tree)
    # This verifier selects ROOT through an environment/candidate branch; its
    # registered constants are nevertheless exact and resolve from that ROOT.
    if source == "singleton_reconstruction_verifier":
        assignments["ROOT"] = ast.parse(repr(str(ROOT)), mode="eval").body
    value = _path_value(receiver, assignments, paths[source])
    if value is None:
        return None
    resolved = value.resolve()
    matches = [name for name, path in paths.items() if path.resolve() == resolved]
    require(len(matches) <= 1, f"ambiguous registered dependency path: {resolved}")
    return matches[0] if matches else None


def _literal_keyword(call: ast.Call, name: str) -> ast.AST | None:
    for keyword in call.keywords:
        if keyword.arg == name:
            return keyword.value
    return None


def _is_path_like_expression(expression: ast.AST, tree: ast.AST) -> bool:
    if isinstance(expression, ast.Name):
        return expression.id.isupper() or expression.id in _module_assignments(tree)
    if isinstance(expression, ast.Attribute):
        return _is_path_like_expression(expression.value, tree)
    if isinstance(expression, ast.Subscript):
        return _is_path_like_expression(expression.value, tree)
    if isinstance(expression, ast.BinOp) and isinstance(expression.op, ast.Div):
        return (_is_path_like_expression(expression.left, tree) or
                (isinstance(expression.right, ast.Constant) and
                 isinstance(expression.right.value, str)))
    if isinstance(expression, ast.Call):
        return (_call_name(expression) in {"Path", "resolve"} or
                (isinstance(expression.func, ast.Attribute) and
                 _is_path_like_expression(expression.func.value, tree)))
    return False


def _unresolved_record(kind: str, source: str, location: Span,
                       expression: ast.AST, categories: dict[str, str],
                       paths: dict[str, Path], provenance: str) -> EdgeRecord:
    return EdgeRecord(kind, source, _repo_path(paths[source]),
                      "<unresolved-local-target>", "<unresolved>", "<unresolved>",
                      location,
                      (POLICY_CALLABLE if categories[source] == CAT_CALLABLE_PYTHON
                       else POLICY_EXECUTED), provenance)




def _dynamic_caller_records(source: str, loader_span: Span,
                            trees: dict[str, ast.AST], categories: dict[str, str],
                            paths: dict[str, Path]) -> set[EdgeRecord]:
    records = set()
    policies = [policy for policy in DYNAMIC_CALLER_POLICY
                if policy[0] == source and policy[1] == loader_span]
    for _source, _loader, caller_span, argument_index, label in policies:
        expected_name = "load" if source == "rank_six_atom_search" else "load_module"
        matches = [node for node in ast.walk(trees[source])
                   if isinstance(node, ast.Call) and node.lineno == caller_span[0] and
                   _call_name(node) == expected_name]
        require(len(matches) == 1,
                f"dynamic caller policy site changed: {source}:{caller_span[0]}:")
        caller = matches[0]
        require(len(caller.args) > argument_index,
                f"dynamic caller argument missing: {source}:{caller_span[0]}:")
        actual_span = _span(caller)
        require(actual_span == caller_span,
                f"dynamic caller span changed: {source}:{caller_span}:{actual_span}")
        argument = caller.args[argument_index]
        target = _receiver_target(argument, source, trees[source], paths)
        provenance = f"{label}@{actual_span}/{ast.unparse(argument)}"
        if target is None:
            records.add(_unresolved_record(EDGE_DYNAMIC, source, loader_span,
                                           argument, categories, paths, provenance))
        else:
            records.add(_edge_record(EDGE_DYNAMIC, source, target, loader_span,
                                     provenance, categories, paths))
    return records


def _derive_observed_records(trees: dict[str, ast.AST], categories: dict[str, str],
                             paths: dict[str, Path]) -> set[EdgeRecord]:
    """Derive edges from Python trees with privately pinned fixed-data targets."""
    python_paths = _python_registry_paths()
    require(paths == python_paths and set(trees) == set(python_paths),
            "observation domain is not the exact public Python registry")
    data_paths = {**EXECUTED_DATA_PATHS, **CALLABLE_DATA_PATHS}
    require(set(categories) == set(python_paths) | set(data_paths) and
            set(python_paths).isdisjoint(data_paths) and
            set(data_paths) == set(EXECUTED_DATA_SHA256) | set(CALLABLE_DATA_SHA256),
            "fixed-data observation registry changed")
    paths = {**python_paths, **data_paths}
    admitted_sites = set(EDGE_SITE_POLICY)
    result = set()
    for source, tree in trees.items():
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            location = _span(node)
            if _call_name(node) == "spec_from_file_location":
                if (source, location) in DYNAMIC_SITE_EXCLUSIONS:
                    continue
                if (source, location, EDGE_DYNAMIC) in admitted_sites:
                    caller_records = _dynamic_caller_records(
                        source, location, trees, categories, paths)
                    if caller_records:
                        result.update(caller_records)
                        continue
                path_argument = node.args[1] if len(node.args) > 1 else None
                if path_argument is None:
                    result.add(_unresolved_record(
                        EDGE_DYNAMIC, source, location, ast.Constant(None),
                        categories, paths,
                        f"observed-qualified-call/{ast.unparse(node)}"))
                    continue
                target = _receiver_target(path_argument, source, tree, paths)
                provenance = f"observed-qualified-call/{ast.unparse(node)}"
                if target is None:
                    result.add(_unresolved_record(EDGE_DYNAMIC, source, location,
                                                  path_argument, categories, paths,
                                                  provenance))
                else:
                    result.add(_edge_record(EDGE_DYNAMIC, source, target, location,
                                            provenance, categories, paths))
                continue
            if (_call_name(node) not in {"read_bytes", "read_text"} or
                    not isinstance(node.func, ast.Attribute)):
                continue
            receiver = node.func.value
            target = _receiver_target(receiver, source, tree, paths)
            if target is None:
                # All syntactically path-like receivers either resolve to the
                # pinned registry, match an exact variable-input exclusion, or
                # become an explicit unresolved surplus.  There is no catch-all
                # nonclosure suppression.
                if not _is_path_like_expression(receiver, tree):
                    continue
                if any(source == excluded_source and location == excluded_span and
                       ast.unparse(node) == excluded_expression
                       for excluded_source, excluded_span, excluded_expression
                       in EXCLUDED_READ_POLICY):
                    continue
                result.add(_unresolved_record(
                    EDGE_READ, source, location, receiver, categories, paths,
                    f"observed-unresolved-fixed-receiver/{ast.unparse(receiver)}"))
                continue
            result.add(_edge_record(
                EDGE_READ, source, target, location,
                f"observed-fixed-receiver/{ast.unparse(receiver)}",
                categories, paths))

    # A non-None cache_path at the real call site activates the callee line-61
    # fixed read and carries both caller and callee spans in provenance.
    for caller, call_line, callee, function_name, parameter, expected_default in DEFAULT_CALL_POLICY:
        matches = [node for node in ast.walk(trees[caller])
                   if isinstance(node, ast.Call) and node.lineno == call_line and
                   _call_name(node) == function_name]
        require(len(matches) == 1,
                f"call-policy expression changed: {caller}:{call_line}:{function_name}")
        call = matches[0]
        call_span = _span(call)
        argument = _literal_keyword(call, parameter)
        observed_default = (expected_default if argument is None else
                            argument.value if isinstance(argument, ast.Constant) else
                            "<supplied>")
        if observed_default == expected_default:
            continue
        target = _receiver_target(argument, caller, trees[caller], paths)
        require(target is not None,
                f"call-policy target is not a registered fixed path: {caller}:{call_span}")
        callee_read = next(node for node in ast.walk(trees[callee])
                           if isinstance(node, ast.Call) and
                           _span(node) == (61, 44, 61, 67) and
                           ast.unparse(node) == "cache_path.read_bytes()")
        provenance = (f"caller {caller}@{call_span} supplies {parameter}="
                      f"{ast.unparse(argument)}; callee {callee}@{_span(callee_read)} "
                      "cache_path.read_bytes")
        result.add(_edge_record(EDGE_READ, callee, target, _span(callee_read),
                                provenance, categories, paths))
    return result


def _audit_excluded_read_policy(trees: dict[str, ast.AST]) -> None:
    # Presence is audited here; exact-expression admission is performed only in
    # _derive_observed_records.  Thus a same-span expression mutation is not
    # silently excluded: it remains visible as a resolved/unresolved surplus.
    for source, location, _expression in EXCLUDED_READ_POLICY:
        matches = [node for node in ast.walk(trees[source])
                   if isinstance(node, ast.Call) and _span(node) == location]
        require(len(matches) == 1,
                f"excluded-read policy site changed: {source}:{location}")


DEPENDENCY_EDGE_POLICY = (
    EdgeRecord(*('dynamic-import', 'direct_pack_verifier', 'positive-square-energy/experiments/rank7_order8_direct_rational_pack_auditor.py', 'exact_rational_engine', 'positive-square-energy/experiments/rank7_order8_exact_rational.py', 'executed-python', (115, 11, 115, 61), 'executed-full-replay', 'audit_and_replay/load_module@(303, 13, 303, 72)/ENGINE_PATH')),
    EdgeRecord(*('dynamic-import', 'direct_pack_verifier', 'positive-square-energy/experiments/rank7_order8_direct_rational_pack_auditor.py', 'exact_rational_engine', 'positive-square-energy/experiments/rank7_order8_exact_rational.py', 'executed-python', (115, 11, 115, 61), 'executed-full-replay', 'self_test/load_module@(408, 13, 408, 74)/ENGINE_PATH')),
    EdgeRecord(*('dynamic-import', 'exact_rational_base', 'positive-square-energy/experiments/rank6_order10_cubic_exact_rational.py', 'rank_six_atom_search', 'positive-square-energy/experiments/rank6_orders8_10_atom_ledger_search.py', 'callable-unreached-python', (229, 15, 229, 100), 'conservative-callable-body', "observed-qualified-call/importlib.util.spec_from_file_location('rank6_order10_stream_atom', ATOM_SEARCH_PATH)")),
    EdgeRecord(*('dynamic-import', 'exact_rational_base', 'positive-square-energy/experiments/rank6_order10_cubic_exact_rational.py', 'rank_six_frontier_census', 'positive-square-energy/experiments/rank6_order10_cubic_frontier_census.py', 'callable-unreached-python', (50, 11, 50, 86), 'conservative-callable-body', "observed-qualified-call/importlib.util.spec_from_file_location('rank6_order10_census', CENSUS_PATH)")),
    EdgeRecord(*('dynamic-import', 'exact_rational_engine', 'positive-square-energy/experiments/rank7_order8_exact_rational.py', 'exact_rational_base', 'positive-square-energy/experiments/rank6_order10_cubic_exact_rational.py', 'executed-python', (56, 11, 56, 61), 'executed-full-replay', 'module initialization/load_module@(63, 7, 63, 54)/BASE_PATH')),
    EdgeRecord(*('dynamic-import', 'exact_rational_engine', 'positive-square-energy/experiments/rank7_order8_exact_rational.py', 'payload_free_lanes', 'positive-square-energy/experiments/rank7_order8_payload_free_lanes.py', 'executed-python', (56, 11, 56, 61), 'executed-full-replay', 'lanes_module/load_module@(69, 17, 69, 69)/LANES_PATH')),
    EdgeRecord(*('dynamic-import', 'kernel_census_verifier', 'research/rank-seven-kernel-frontier-census.py', 'rank_six_census_verifier', 'research/rank-six-kernel-census-verifier.py', 'executed-python', (32, 11, 32, 86), 'executed-full-replay', "observed-qualified-call/importlib.util.spec_from_file_location('rank_six_census', RANK_SIX_PROGRAM)")),
    EdgeRecord(*('dynamic-import', 'order7_vector_engine', 'pentacyclic/research/order7-dim7-rational-gram-experiment.py', 'order7_tetra_census', 'pentacyclic/research/order7-tetra-census-experiment.py', 'callable-unreached-python', (240, 11, 240, 81), 'conservative-callable-body', "observed-qualified-call/importlib.util.spec_from_file_location('order7_census', CENSUS_SCRIPT)")),
    EdgeRecord(*('dynamic-import', 'order8_vector_engine', 'pentacyclic/research/order8-dim8-rational-canonical-frontiers-experiment.py', 'order8_tetra_census', 'pentacyclic/research/order8-cubic-tetra-census-experiment.py', 'callable-unreached-python', (207, 11, 207, 81), 'conservative-callable-body', "observed-qualified-call/importlib.util.spec_from_file_location('order8_census', CENSUS_SCRIPT)")),
    EdgeRecord(*('dynamic-import', 'payload_free_lanes', 'positive-square-energy/experiments/rank7_order8_payload_free_lanes.py', 'atom_recognizer', 'positive-square-energy/experiments/rank7_order7_symbolic_atom_recognizer.py', 'executed-python', (69, 11, 69, 92), 'executed-full-replay', "observed-qualified-call/importlib.util.spec_from_file_location('rank7_order8_atom_core', ATOM_RECOGNIZER)")),
    EdgeRecord(*('dynamic-import', 'post_xii_verifier', 'positive-square-energy/experiments/rank7_order8_post_xii_shared_packet_lane.py', 'exact_rational_engine', 'positive-square-energy/experiments/rank7_order8_exact_rational.py', 'executed-python', (168, 11, 168, 94), 'executed-full-replay', "observed-qualified-call/importlib.util.spec_from_file_location('rank7_order8_post_xii_engine', ENGINE_PATH)")),
    EdgeRecord(*('dynamic-import', 'rank_six_atom_search', 'positive-square-energy/experiments/rank6_orders8_10_atom_ledger_search.py', 'exact_rational_base', 'positive-square-energy/experiments/rank6_order10_cubic_exact_rational.py', 'executed-python', (38, 11, 38, 61), 'conservative-callable-body', "residuals_by_order/load@(313, 18, 313, 86)/HERE / 'rank6_order10_cubic_exact_rational.py'")),
    EdgeRecord(*('dynamic-import', 'rank_six_atom_search', 'positive-square-energy/experiments/rank6_orders8_10_atom_ledger_search.py', 'rank_six_order8_pipeline', 'positive-square-energy/experiments/rank6_order8_sparse_pipeline.py', 'callable-unreached-python', (38, 11, 38, 61), 'conservative-callable-body', "residuals_by_order/load@(305, 17, 305, 78)/HERE / 'rank6_order8_sparse_pipeline.py'")),
    EdgeRecord(*('dynamic-import', 'rank_six_atom_search', 'positive-square-energy/experiments/rank6_orders8_10_atom_ledger_search.py', 'rank_six_order9_witness', 'positive-square-energy/experiments/rank6_order9_sparse_witness.py', 'callable-unreached-python', (38, 11, 38, 61), 'conservative-callable-body', "residuals_by_order/load@(309, 17, 309, 77)/HERE / 'rank6_order9_sparse_witness.py'")),
    EdgeRecord(*('dynamic-import', 'rank_six_order8_pipeline', 'positive-square-energy/experiments/rank6_order8_sparse_pipeline.py', 'order8_vector_engine', 'pentacyclic/research/order8-dim8-rational-canonical-frontiers-experiment.py', 'callable-unreached-python', (348, 11, 348, 92), 'conservative-callable-body', "observed-qualified-call/importlib.util.spec_from_file_location('rank6_order8_vector_engine', ENGINE_PATH)")),
    EdgeRecord(*('dynamic-import', 'rank_six_order9_witness', 'positive-square-energy/experiments/rank6_order9_sparse_witness.py', 'order7_vector_engine', 'pentacyclic/research/order7-dim7-rational-gram-experiment.py', 'callable-unreached-python', (52, 11, 52, 61), 'conservative-callable-body', 'load_engine/load_module@(89, 13, 89, 67)/ENGINE_PATH')),
    EdgeRecord(*('dynamic-import', 'rank_six_order9_witness', 'positive-square-energy/experiments/rank6_order9_sparse_witness.py', 'rank_six_order8_pipeline', 'positive-square-energy/experiments/rank6_order8_sparse_pipeline.py', 'callable-unreached-python', (52, 11, 52, 61), 'conservative-callable-body', 'module initialization/load_module@(59, 7, 59, 57)/BASE_PATH')),
    EdgeRecord(*('dynamic-import', 'semantic_census_verifier', 'positive-square-energy/experiments/rank7_order8_semantic_census.py', 'census_producer', 'positive-square-energy/experiments/rank7_order8_exact_residual_census.py', 'executed-python', (29, 11, 30, 90), 'executed-full-replay', "observed-qualified-call/importlib.util.spec_from_file_location('order8_census_comparator_source', HERE / 'rank7_order8_exact_residual_census.py')")),
    EdgeRecord(*('fixed-read', 'exact_rational_base', 'positive-square-energy/experiments/rank6_order10_cubic_exact_rational.py', 'rank_six_atom_artifact', 'positive-square-energy/experiments/rank6_orders8_10_atom_ledger_classification.json', 'callable-unreached-data', (211, 25, 211, 61), 'conservative-callable-body', 'observed-fixed-receiver/ATOM_FIXTURE_PATH')),
    EdgeRecord(*('fixed-read', 'exact_rational_base', 'positive-square-energy/experiments/rank6_order10_cubic_exact_rational.py', 'rank_six_frontier_artifact', 'positive-square-energy/experiments/rank6_order10_cubic_frontier_census.json', 'callable-unreached-data', (75, 45, 75, 77), 'conservative-callable-body', 'observed-fixed-receiver/census.OUTPUT')),
    EdgeRecord(*('fixed-read', 'exact_rational_engine', 'positive-square-energy/experiments/rank7_order8_exact_rational.py', 'selected_indices', 'positive-square-energy/experiments/rank7_order8_rational_search_indices.json', 'executed-data', (74, 10, 74, 35), 'executed-full-replay', 'observed-fixed-receiver/INDICES_PATH')),
    EdgeRecord(*('fixed-read', 'kernel_census_verifier', 'research/rank-seven-kernel-frontier-census.py', 'rank_seven_fixture', 'research/fixtures/rank-seven-kernel-frontier-census.json', 'executed-data', (176, 16, 176, 35), 'executed-full-replay', 'observed-fixed-receiver/OUTPUT')),
    EdgeRecord(*('fixed-read', 'order7_tetra_census', 'pentacyclic/research/order7-tetra-census-experiment.py', 'order7_tetra_artifact', 'pentacyclic/research/order7-tetra-census.json', 'callable-unreached-data', (154, 10, 154, 31), 'conservative-callable-body', 'observed-fixed-receiver/ARTIFACT')),
    EdgeRecord(*('fixed-read', 'order7_tetra_census', 'pentacyclic/research/order7-tetra-census-experiment.py', 'rank_five_fixture', 'research/fixtures/rank-five-kernels.json', 'callable-unreached-data', (79, 10, 79, 29), 'conservative-callable-body', 'observed-fixed-receiver/SOURCE')),
    EdgeRecord(*('fixed-read', 'order8_tetra_census', 'pentacyclic/research/order8-cubic-tetra-census-experiment.py', 'order8_tetra_artifact', 'pentacyclic/research/order8-cubic-tetra-census.json', 'callable-unreached-data', (184, 10, 184, 31), 'conservative-callable-body', 'observed-fixed-receiver/ARTIFACT')),
    EdgeRecord(*('fixed-read', 'order8_tetra_census', 'pentacyclic/research/order8-cubic-tetra-census-experiment.py', 'rank_five_fixture', 'research/fixtures/rank-five-kernels.json', 'callable-unreached-data', (38, 10, 38, 29), 'conservative-callable-body', 'observed-fixed-receiver/SOURCE')),
    EdgeRecord(*('fixed-read', 'rank_six_atom_search', 'positive-square-energy/experiments/rank6_orders8_10_atom_ledger_search.py', 'rank_six_atom_artifact', 'positive-square-energy/experiments/rank6_orders8_10_atom_ledger_classification.json', 'callable-unreached-data', (417, 16, 417, 37), 'conservative-callable-body', 'observed-fixed-receiver/ARTIFACT')),
    EdgeRecord(*('fixed-read', 'rank_six_frontier_census', 'positive-square-energy/experiments/rank6_order10_cubic_frontier_census.py', 'rank_six_fixture', 'research/fixtures/rank-six-kernels.json', 'callable-unreached-data', (48, 10, 48, 29), 'conservative-callable-body', 'observed-fixed-receiver/SOURCE')),
    EdgeRecord(*('fixed-read', 'rank_six_order8_pipeline', 'positive-square-energy/experiments/rank6_order8_sparse_pipeline.py', 'rank_six_fixture', 'research/fixtures/rank-six-kernels.json', 'callable-unreached-data', (64, 10, 64, 29), 'conservative-callable-body', 'observed-fixed-receiver/SOURCE')),
    EdgeRecord(*('fixed-read', 'rank_six_order9_witness', 'positive-square-energy/experiments/rank6_order9_sparse_witness.py', 'rank_six_fixture', 'research/fixtures/rank-six-kernels.json', 'callable-unreached-data', (63, 10, 63, 29), 'conservative-callable-body', 'observed-fixed-receiver/SOURCE')),
    EdgeRecord(*('fixed-read', 'semantic_census_verifier', 'positive-square-energy/experiments/rank7_order8_semantic_census.py', 'rank_seven_fixture', 'research/fixtures/rank-seven-kernel-frontier-census.json', 'executed-data', (39, 10, 39, 36), 'executed-full-replay', 'observed-fixed-receiver/KERNEL_SOURCE')),
    EdgeRecord(*('fixed-read', 'singleton_reconstruction_verifier', 'research/rank-seven-order-eight-singleton-reconstruction-verifier.py', 'census_manifest', 'positive-square-energy/experiments/rank7_order8_exact_residual_census_manifest.json', 'executed-data', (220, 27, 220, 48), 'executed-full-replay', 'observed-fixed-receiver/MANIFEST')),
    EdgeRecord(*('fixed-read', 'singleton_reconstruction_verifier', 'research/rank-seven-order-eight-singleton-reconstruction-verifier.py', 'rank_seven_fixture', 'research/fixtures/rank-seven-kernel-frontier-census.json', 'executed-data', (206, 26, 206, 46), 'executed-full-replay', 'observed-fixed-receiver/FIXTURE')),
    EdgeRecord(*('fixed-read', 'singleton_reconstruction_verifier', 'research/rank-seven-order-eight-singleton-reconstruction-verifier.py', 'selected_indices', 'positive-square-energy/experiments/rank7_order8_rational_search_indices.json', 'executed-data', (238, 26, 238, 46), 'executed-full-replay', 'observed-fixed-receiver/INDICES')),
    EdgeRecord(*('fixed-read', 'base_verifier', 'positive-square-energy/experiments/rank7_order8_typed_precedence_bridge.py', 'finite_owners', 'positive-square-energy/experiments/rank7_order8_packet_spectral_owners.json.xz', 'executed-data', (556, 19, 556, 50), 'executed-full-replay', 'observed-fixed-receiver/FINITE_OWNERS_PATH')),
    EdgeRecord(*('fixed-read', 'direct_pack_verifier', 'positive-square-energy/experiments/rank7_order8_direct_rational_pack_auditor.py', 'combined_owner_ledger', 'positive-square-energy/experiments/rank7_order8_combined_owner_ledger.json', 'executed-data', (148, 17, 148, 41), 'executed-full-replay', 'observed-fixed-receiver/LEDGER_PATH')),
    EdgeRecord(*('fixed-read', 'post_xii_verifier', 'positive-square-energy/experiments/rank7_order8_post_xii_shared_packet_lane.py', 'post_xii_report', 'positive-square-energy/experiments/rank7_order8_post_xii_shared_packet_lane.json', 'executed-data', (466, 17, 466, 36), 'executed-full-replay', 'observed-fixed-receiver/OUTPUT')),
    EdgeRecord(*('fixed-read', 'post_xii_verifier', 'positive-square-energy/experiments/rank7_order8_post_xii_shared_packet_lane.py', 'post_xii_report', 'positive-square-energy/experiments/rank7_order8_post_xii_shared_packet_lane.json', 'executed-data', (627, 26, 627, 45), 'executed-full-replay', 'observed-fixed-receiver/OUTPUT')),
    EdgeRecord(*('fixed-read', 'post_xii_verifier', 'positive-square-energy/experiments/rank7_order8_post_xii_shared_packet_lane.py', 'post_xii_report', 'positive-square-energy/experiments/rank7_order8_post_xii_shared_packet_lane.json', 'executed-data', (692, 30, 692, 49), 'executed-full-replay', 'observed-fixed-receiver/OUTPUT')),
    EdgeRecord(*('fixed-read', 'post_xii_verifier', 'positive-square-energy/experiments/rank7_order8_post_xii_shared_packet_lane.py', 'post_xii_source_report', 'positive-square-energy/experiments/rank7_order8_twelfth_induced_packet_gram_family.json', 'executed-data', (196, 10, 196, 36), 'executed-full-replay', 'observed-fixed-receiver/SOURCE_REPORT')),
    EdgeRecord(*('fixed-read', 'singleton_reconstruction_verifier', 'research/rank-seven-order-eight-singleton-reconstruction-verifier.py', 'post_xii_remainder', 'positive-square-energy/experiments/rank7_order8_after_post_xii_shared_packet_remainder.jsonl.xz', 'executed-data', (201, 36, 201, 58), 'executed-full-replay', 'observed-fixed-receiver/SINGLETON')),
)


def audit_dependency_edges(
        source_text_overrides: dict[str, str] | None = None,
        category_overrides: dict[str, str] | None = None) -> int:
    """Pure bidirectional AST edge oracle, independent of all byte pins."""
    sources = _python_registry_paths()
    source_text_overrides = source_text_overrides or {}
    require(set(source_text_overrides) <= set(sources),
            "source override names a non-Python dependency")
    categories, paths = _category_maps(category_overrides)
    trees = {}
    for name, path in sources.items():
        text = source_text_overrides.get(name)
        if text is None:
            text = path.read_text("ascii")
        try:
            trees[name] = ast.parse(text, filename=f"<{name}>")
            trees[name]._baseline_line_count = len(path.read_text("ascii").splitlines())
        except (SyntaxError, TypeError, ValueError) as error:
            raise RuntimeError(f"dependency source is not parseable: {name}") from error

    _audit_excluded_read_policy(trees)
    expected = set(DEPENDENCY_EDGE_POLICY)
    observed = _derive_observed_records(trees, categories, paths)
    missing, surplus = expected - observed, observed - expected
    require(not missing and not surplus, _format_edge_difference(missing, surplus))
    require(len(CALLABLE_PYTHON_PATHS) == 8 and len(CALLABLE_DATA_PATHS) == 6,
            "callable closure cardinality changed")
    return len(observed)


def audit_no_asserts() -> int:
    """AST-audit exactly both Python categories plus this orchestrator."""
    checked = (SELF, *EXECUTED_PYTHON_PATHS.values(), *CALLABLE_PYTHON_PATHS.values())
    require(len(set(checked)) == len(checked), "Python registries duplicate a path")
    for path in checked:
        try:
            tree = ast.parse(path.read_text("ascii"), filename=str(path))
        except (OSError, UnicodeError, SyntaxError) as error:
            raise RuntimeError(f"cannot parse runtime source: {path.name}") from error
        require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)),
                f"optimization-removable assert in {path.name}")
    return len(checked)


def audit_post_artifacts() -> dict[str, Json]:
    report_raw = POST_REPORT.read_bytes()
    source_xz = POST_SOURCE.read_bytes()
    owner_xz = POST_OWNERS.read_bytes()
    remainder_xz = SINGLETON.read_bytes()
    require(sha256(report_raw) == ARTIFACT_SHA256["post_report"],
            "post-XII report bytes changed")
    require(sha256(source_xz) == ARTIFACT_SHA256["post_source_xz"],
            "post-XII source artifact changed")
    require(sha256(owner_xz) == ARTIFACT_SHA256["post_owners_xz"],
            "post-XII owner artifact changed")
    require(sha256(remainder_xz) == ARTIFACT_SHA256["post_remainder_xz"],
            "post-XII remainder artifact changed")
    try:
        source_raw = lzma.decompress(source_xz, format=lzma.FORMAT_XZ)
        owner_raw = lzma.decompress(owner_xz, format=lzma.FORMAT_XZ)
        remainder_raw = lzma.decompress(remainder_xz, format=lzma.FORMAT_XZ)
    except lzma.LZMAError as error:
        raise RuntimeError("invalid post-XII XZ artifact") from error
    require(sha256(source_raw) == ARTIFACT_SHA256["post_source_raw"] and
            sha256(owner_raw) == ARTIFACT_SHA256["post_owners_raw"] and
            sha256(remainder_raw) == ARTIFACT_SHA256["post_remainder_raw"],
            "post-XII raw stream identity changed")
    require(len(source_raw.splitlines()) == 54598 and
            len(owner_raw.splitlines()) == 54597 and
            len(remainder_raw.splitlines()) == 1,
            "post-XII stream count changed")
    report = strict_json(report_raw, "post-XII report")
    require(type(report) is dict and set(report) == {
        "accepted_denominator_histogram", "certificate", "claim_boundary",
        "classification_stream_sha256", "full_theorem", "generation_runtime",
        "owned_orbit_total", "owned_physical_total", "owned_target_total",
        "owner_stream", "partition_identity", "reduced_remainder_stream",
        "remaining_orbit_total", "remaining_physical_total", "remaining_target_total",
        "scan_complete", "schema", "scope", "search", "source_orbit_total",
        "source_physical_total", "source_report", "source_stream", "targets_per_row",
    }, "post-XII report schema changed")
    require(report["schema"] ==
            "rank-seven-order-eight-post-xii-global-shared-packet-lane-v1" and
            report["full_theorem"] is False and report["scan_complete"] is True and
            report["source_orbit_total"] == 54598 and
            report["owned_orbit_total"] == 54597 and
            report["owned_target_total"] == 818955 and
            report["remaining_orbit_total"] == 1 and
            report["remaining_target_total"] == 15 and
            report["targets_per_row"] == 15 and
            report["partition_identity"] == "54598 = 54597 + 1",
            "post-XII report accounting changed")
    require(report["source_stream"] == {
        "artifact_sha256": ARTIFACT_SHA256["post_source_xz"],
        "path": POST_SOURCE.name,
        "raw_sha256": ARTIFACT_SHA256["post_source_raw"],
        "record_total": 54598,
    } and report["owner_stream"] == {
        "artifact_sha256": ARTIFACT_SHA256["post_owners_xz"],
        "path": POST_OWNERS.name,
        "raw_sha256": ARTIFACT_SHA256["post_owners_raw"],
        "record_total": 54597,
    } and report["reduced_remainder_stream"] == {
        "artifact_sha256": ARTIFACT_SHA256["post_remainder_xz"],
        "path": SINGLETON.name,
        "raw_sha256": ARTIFACT_SHA256["post_remainder_raw"],
        "record_total": 1,
    }, "post-XII report stream links changed")
    singleton = strict_json(remainder_raw, "singleton remainder")
    require(singleton == SINGLETON_ROW, "singleton six-field row changed")
    return report


def audit_selected_stream_linkage() -> None:
    """Bind the 492,812-row search cache to the semantically replayed census.

    The selected index list is itself a historical payload-free producer output
    (and therefore not freshly derived here).  This audit checks its exact
    order-preserving projection into every committed census chunk, then checks
    every decoded cache field against that projected row and kernel support.
    """
    manifest_path = EXPERIMENTS / "rank7_order8_exact_residual_census_manifest.json"
    indices_raw = SELECTED_INDICES.read_bytes()
    indices = strict_json(indices_raw, "selected residual indices")
    require(indices_raw == canonical_bytes(indices) and type(indices) is dict and
            set(indices) == {"manifest_sha256", "schema", "selected_chunks",
                             "source_indices"} and
            indices["schema"] == "rank-seven-order-eight-rational-search-indices-v1" and
            indices["manifest_sha256"] == sha256(manifest_path.read_bytes()) and
            indices["selected_chunks"] == list(range(8)),
            "selected-index contract changed")
    wanted = indices["source_indices"]
    require(type(wanted) is list and len(wanted) == 492812 and
            all(type(value) is int for value in wanted) and
            all(left < right for left, right in zip(wanted, wanted[1:])),
            "selected indices are not an exact increasing 492,812-row projection")

    manifest = strict_json(manifest_path.read_bytes(), "residual manifest")
    residuals: list[tuple[int, int, tuple[int, ...], tuple[int, ...], tuple[int, ...], int]] = []
    selected_position = 0
    source_offset = 0
    pairs = tuple((u, v) for u in range(8) for v in range(u + 1, 8))
    for chunk_info in manifest["chunks"]:
        stored = (EXPERIMENTS / chunk_info["path"]).read_bytes()
        require(sha256(stored) == chunk_info["artifact_sha256"],
                "selected linkage: census chunk bytes changed")
        raw = lzma.decompress(stored, format=lzma.FORMAT_XZ)
        require(sha256(raw) == chunk_info["raw_sha256"],
                "selected linkage: census chunk raw bytes changed")
        chunk = strict_json(raw, chunk_info["path"])
        kernels = {}
        for kernel in chunk["kernels"]:
            edges = tuple(tuple(edge) for edge in kernel["edges"])
            require(kernel["order_kernel"] not in kernels,
                    "selected linkage: duplicate kernel index")
            kernels[kernel["order_kernel"]] = edges
        for local_index, record in enumerate(chunk["residuals"]):
            source_index = source_offset + local_index
            if selected_position == len(wanted) or wanted[selected_position] != source_index:
                continue
            edges = kernels[record["order_kernel"]]
            support = tuple(pairs.index((u, v)) for u, v, _ in edges)
            residuals.append((record["global_kernel"], source_index, support,
                              tuple(edge[2] for edge in edges), tuple(record["row"]),
                              record["orbit_size"]))
            selected_position += 1
        source_offset += len(chunk["residuals"])
    require(source_offset == 493417 and selected_position == len(wanted) and
            len(residuals) == 492812,
            "selected linkage: incomplete census projection")

    cache_path = EXPERIMENTS / "rank7_order8_rational_search_cache.r7o8c.xz"
    cache_stored = cache_path.read_bytes()
    require(sha256(cache_stored) ==
            "0e31fb87d7bfa8e01d8cf168240cb2cc164673628f2c22b9e14347186cea7502",
            "selected linkage: cache stored bytes changed")
    cache_raw = lzma.decompress(cache_stored, format=lzma.FORMAT_XZ)
    require(sha256(cache_raw) ==
            "b56459cb832370340c7d44c1dca77e97adb59192f9f2703df739f048c25e3d30",
            "selected linkage: cache raw bytes changed")
    require(cache_raw[:6] == b"R7O8C1" and
            cache_raw[6:38].hex() ==
            "53c64c930846c92d8a4f35e5c228c60afb4c56c1a35009cfec60eaf2ffba6ee3" and
            cache_raw[38:70] == hashlib.sha256(cache_raw[70:]).digest(),
            "selected linkage: cache header or internal payload digest changed")
    position = 70

    def uvarint() -> int:
        nonlocal position
        value = 0
        shift = 0
        while True:
            require(position < len(cache_raw) and shift <= 63,
                    "selected linkage: truncated or overlong cache varint")
            byte = cache_raw[position]
            position += 1
            value |= (byte & 0x7f) << shift
            if byte < 0x80:
                require(shift == 0 or byte != 0,
                        "selected linkage: noncanonical cache varint")
                return value
            shift += 7

    require(uvarint() == len(residuals), "selected linkage: cache row total changed")
    transcript = hashlib.sha256()
    for stream_index, expected in enumerate(residuals):
        global_kernel = uvarint()
        source_index = uvarint()
        width = uvarint()
        support = []
        multiplicities = []
        parity = []
        for _ in range(width):
            support.append(uvarint())
            multiplicities.append(uvarint())
            parity.append(uvarint())
        orbit_size = uvarint()
        observed = (global_kernel, source_index, tuple(support),
                    tuple(multiplicities), tuple(parity), orbit_size)
        require(observed == expected,
                f"selected linkage: cache/census mismatch at row {stream_index}")
        transcript.update(canonical_bytes([stream_index, *observed]))
    require(position == len(cache_raw) and transcript.hexdigest() ==
            "3742dbaa935d462c9d6be5e1de4b199264b5c8411d85b2c5b12b57d290e52ba8",
            "selected linkage: cache projection transcript changed")


def audit_math_sources() -> None:
    reduction = REDUCTION.read_text("ascii")
    required_reduction = (
        "2<=|V(K)|<=12",
        "F(c)={c} union {c+2e_i:1<=i<=p}.",
        "Assume also that regenerated target keys are the disjoint union of checked",
        "one-vertex additivity of `kappa` and `kappa(T)=|E(T)|`",
        "s^+(G)>=|V(G)|",
        "claim that the resulting finite rank-seven ledger has been enumerated or",
    )
    require(all(fragment in reduction for fragment in required_reduction),
            "rank-seven reduction contract changed")

    territory = TERRITORY.read_text("ascii")
    required_territory = (
        "A = {0,3,6,7},        B = {1,2,4,5}",
        "P_74", "P_65", "No parity hypothesis", "stream index `416536`",
        "residual source\nindex `416987`", "global kernel `6832`", "orbit size two",
        "03,06,07,12,14,15,24,25,36,37,45,47,56,67",
        "(1,1,1,1,1,1,1,1,1,1,1,1,0,1)",
        "|E(G[U])| = |V(G[U])| + 2", "The same calculation applies to `G[W]`",
        "s+(G) >= s+(G[U]) + s+(G[W])",
        "No edge monotonicity", "No connector debit", "No DNN gluing",
    )
    require(all(fragment in territory for fragment in required_territory),
            "singleton territory proof contract changed")

    tricyclic = TRICYCLIC_TEX.read_text("ascii")
    required_tricyclic = (
        "Every finite simple connected graph $G$ with $|V(G)|=n$ and",
        "$|E(G)|=n+2$ satisfies",
        "\\begin{lemma}[Induced superadditivity]\\label{lem:super}",
        "\\splus(G)\\geq\\sum_{j=1}^r\\splus(G[V_j])",
        "\\kappa$ is",
        "additive under one-vertex sums and $\\kappa(T)=|E(T)|$ for a tree",
        "\\begin{proof}[Proof of Theorem~\\ref{thm:main}]",
    )
    require(all(fragment in tricyclic for fragment in required_tricyclic),
            "tricyclic imported theorem contract changed")


def run_child(name: str, path: Path, arguments: tuple[str, ...],
              expected_output: str | None, optimized: bool) -> bytes:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(("-B", str(path), *arguments))
    completed = subprocess.run(command, check=False, capture_output=True,
                               cwd=ROOT, env={**__import__("os").environ,
                                             "ORDER8_ROOT": str(ROOT),
                                             "PYTHONDONTWRITEBYTECODE": "1"})
    require(completed.returncode == 0, f"child failed: {name}/{optimized}")
    require(completed.stderr == b"", f"child wrote stderr: {name}/{optimized}")
    if expected_output is not None:
        require(sha256(completed.stdout) == expected_output,
                f"child output changed: {name}/{optimized}")
    return completed.stdout


def validate_base(raw: bytes) -> None:
    payload = strict_json(raw, "base bridge output", canonical=False)
    require(type(payload) is dict and payload.get("schema") ==
            "rank-seven-order-eight-base-owner-bridge-audit-v1" and
            payload.get("status") == "passed" and
            payload.get("audit_sha256") == CERTIFICATE_SHA256["base_hostile_audit"] and
            payload.get("hostile_mutations_rejected") == 15 and
            payload.get("base_exclusive_counts") == {
                "direct-rational": 29000, "remaining": 84152,
                "scalar-sos": 194351, "typed-diagonal": 185309,
            } and payload.get("boundary_rescue_total") == 296 and
            payload.get("boundary_remainder_total") == 83856 and
            tuple(payload.get("digest_pinned_not_recomputed", ())) ==
            HISTORICAL_BASE_REPORT_ROOTS,
            "base bridge receipt changed")


def validate_direct_packs(raw: bytes) -> None:
    """Validate the complete deterministic child receipt, not only its hash.

    The child strict-decodes and canonically re-encodes the pinned 492,812-row
    cache, then exact-replays the 29,000 selected witnesses and checks the
    selected-owner fields against those decoded rows.  It does not independently
    rematerialize those source tuples from the census chunks.
    """
    payload = strict_json(raw, "direct-pack replay output")
    require(type(payload) is dict and set(payload) == DIRECT_RECEIPT_KEYS,
            "direct-pack receipt schema changed")
    require(payload["schema"] == DIRECT_RECEIPT_SCHEMA and
            payload["status"] == "passed" and
            payload["coverage"] == DIRECT_COVERAGE and
            payload["execution_semantics"] == DIRECT_EXECUTION_SEMANTICS and
            payload["input_sha256"] == DIRECT_INPUT_SHA256 and
            payload["assert_free_source_sha256"] == DIRECT_ASSERT_FREE_SHA256 and
            payload["residual_cache_raw_sha256"] == DIRECT_CACHE_RAW_SHA256,
            "direct-pack aggregate receipt changed")
    linkage = payload["owner_linkage"]
    require(type(linkage) is dict and set(linkage) == {
                "field_set", "owner_row_stream_sha256",
                "replay_row_stream_sha256", "selected_owner_indices", "status"
            } and linkage["field_set"] == DIRECT_OWNER_FIELDS and
            linkage["owner_row_stream_sha256"] == DIRECT_OWNER_STREAM_SHA256 and
            linkage["replay_row_stream_sha256"] == DIRECT_OWNER_STREAM_SHA256 and
            linkage["selected_owner_indices"] == "exactly_list(range(29000))" and
            linkage["status"] == "field-for-field-identical",
            "direct-pack owner linkage changed")

    receipts = payload["pack_receipts"]
    require(type(receipts) is list and len(receipts) == 25,
            "direct-pack receipt count changed")
    spec = importlib.util.spec_from_file_location("direct_pin_reader", DIRECT_PACKS)
    require(spec is not None and spec.loader is not None,
            "cannot load pinned direct-pack registry")
    expected = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(expected)
    packs = getattr(expected, "EXPECTED_PACKS", None)
    require(type(packs) is tuple and len(packs) == 25,
            "direct-pack source registry changed after source pin")
    cursor = rows = targets = scheduler_manifests = 0
    hex_digits = frozenset("0123456789abcdef")
    for index, (receipt, pack) in enumerate(zip(receipts, packs)):
        name, interval, raw_digest, stored_digest, scheduler, scheduler_digest = pack
        require(type(receipt) is dict and set(receipt) == {
                    "authentication", "owner_row_stream_sha256", "path",
                    "raw_sha256", "record_binding_stream_sha256",
                    "replay_row_stream_sha256", "row_range", "rows",
                    "shared_rows", "targets", "xz_sha256",
                }, f"direct-pack receipt {index} schema changed")
        start, stop = interval
        authentication = (
            {"kind": "pinned-baseline-sha256"}
            if scheduler is None else
            {"kind": "scheduler-result", "path": scheduler,
             "sha256": scheduler_digest}
        )
        width = stop - start
        require(start == cursor and stop > start and
                receipt["authentication"] == authentication and
                receipt["path"] == name and
                receipt["raw_sha256"] == raw_digest and
                receipt["xz_sha256"] == stored_digest and
                receipt["row_range"] == [start, stop] and
                receipt["rows"] == width and receipt["shared_rows"] == width and
                receipt["targets"] == 15 * width and
                receipt["owner_row_stream_sha256"] ==
                    receipt["replay_row_stream_sha256"] and
                all(type(receipt[key]) is str and len(receipt[key]) == 64 and
                    set(receipt[key]) <= hex_digits for key in (
                        "owner_row_stream_sha256", "replay_row_stream_sha256",
                        "record_binding_stream_sha256")),
                f"direct-pack receipt {index} changed")
        cursor = stop
        rows += width
        targets += 15 * width
        scheduler_manifests += scheduler is not None
    require((cursor, rows, targets, scheduler_manifests) ==
            (29000, 29000, 435000, 24),
            "direct-pack receipts are not the exact gap-free replay partition")


def validate_kernel_census(raw: bytes) -> None:
    text = raw.decode("ascii")
    require(text == (
        "rank-seven kernel census: exact exhaustive audit passed\n"
        "status: complete-proved-removable-ear-exhaustion\n"
        "canonical_counts_n2_to_n12: 1,6,47,233,914,2270,4015,4495,3396,1391,365\n"
        "canonical_total: 17133\n"
        "degree_multisets: 58\n"
        "canonical_payload_sha256: "
        "a241139ab54ce4cce1ab3812887359edb241c0abfb1018e804b4a5f86762cfd5\n"
    ), "kernel-census regeneration receipt changed")


def validate_singleton_reconstruction(raw: bytes) -> None:
    payload = strict_json(raw, "singleton reconstruction output")
    require(payload == {
        "automorphisms": 16,
        "decomposition": {"A": [0, 3, 6, 7], "B": [1, 2, 4, 5],
                          "connectors": [[4, 7], [5, 6]]},
        "frontiers_checked": 15,
        "induced_ranks": [3, 3],
        "parity_orbit": 2,
        "row": [416536, 416987, 6832, "edges/parity-bound", 2],
        "source_residuals": 493417,
        "status": "passed",
        "tree_connector_scenarios_checked": 5,
    }, "singleton reconstruction receipt changed")


def validate_post(raw: bytes) -> None:
    payload = strict_json(raw, "post-XII child output")
    require(type(payload) is dict and set(payload) ==
            set(EXPECTED_POST_RECEIPT) | {"audit_seconds"},
            "post-XII child receipt schema changed")
    seconds = payload.pop("audit_seconds")
    require(type(seconds) is float and seconds >= 0, "post-XII runtime malformed")
    require(payload == EXPECTED_POST_RECEIPT, "post-XII child receipt changed")


def run_children(full: bool) -> tuple[int, int]:
    """Execute the release children, or use exact prior-output pins in quick mode."""
    expected_receipts = {
        "base": "fd5a5bc5434af1e8c1f82da7f69b5c71e6b8234826d73bdc4c08e3c7cfd874fa",
        "structural": "412fbe20b7435c19897363cd3263f7b4080b79886e5cd811a4ecdbb6a147ad57",
        "packets": "0d15bd6d6addc534b160ae624555620e37a76a3e023d2c2f04e9696d23f3dd78",
        "finite": "86f4ad87b1cc5a84817d630f2fb448045ce207d345c185c7b96bf38895c4a617",
        "k4": "cb5434669fd3aacea9ca07e7a4d75f076a63a19f718806b394234996f52b95f7",
        "doubled_triangle": "a0b9311d8173972c4ac529c326366391ae5df9928079824ff5c0a6c601848222",
        "semantic_census": "5e8b566f541aab9362d71cbf46f51f90a8c0161c148cb11a7698b77b7f4fa1a2",
        "direct_packs": "9b19cb82ab4b462052840406272d24715bf28de2503efa387a6dc648c6f66ce2",
        "kernel_census": "1c22c2cfa9f83e1eed455b244a3b1ab899b75df36ee1241fd2d71873ef807acf",
        "singleton_reconstruction": "ee9f17f37c4bc0c507ba70145e10194943f251c8046b85bda4cc138a5682ea49",
    }
    require(CHILD_OUTPUT_SHA256 == expected_receipts,
            "child output receipt registry changed")
    if not full:
        # Quick mode is a true integration gate: source bytes, artifacts, schemas,
        # ASTs, and proof text were checked above.  These exact output digests are
        # receipts from prior independent normal/-O executions; no expensive
        # semantic child is rerun here.
        return 0, 0

    children = (
        ("base", BASE, ("--hostile",), CHILD_OUTPUT_SHA256["base"], validate_base),
        ("structural", STRUCTURAL, (), CHILD_OUTPUT_SHA256["structural"], None),
        ("packets", PACKETS, (), CHILD_OUTPUT_SHA256["packets"], None),
        ("finite", FINITE, (), CHILD_OUTPUT_SHA256["finite"], None),
        ("k4", K4, (), CHILD_OUTPUT_SHA256["k4"], None),
        ("doubled_triangle", DOUBLED_TRIANGLE, (),
         CHILD_OUTPUT_SHA256["doubled_triangle"], None),
        ("kernel_census", KERNEL_CENSUS, (),
         CHILD_OUTPUT_SHA256["kernel_census"], validate_kernel_census),
        ("semantic_census", SEMANTIC_CENSUS, (),
         CHILD_OUTPUT_SHA256["semantic_census"], None),
        ("direct_packs", DIRECT_PACKS, (),
         CHILD_OUTPUT_SHA256["direct_packs"], validate_direct_packs),
        ("singleton_reconstruction", SINGLETON_RECONSTRUCTION, (),
         CHILD_OUTPUT_SHA256["singleton_reconstruction"], validate_singleton_reconstruction),
    )
    executions = 0
    for name, path, arguments, output_digest, validator in children:
        outputs = []
        for optimized in (False, True):
            output = run_child(name, path, arguments, output_digest, optimized)
            outputs.append(output)
            executions += 1
            if validator is not None:
                validator(output)
        require(outputs[0] == outputs[1], f"normal/-O child output differs: {name}")
    post_outputs = []
    for optimized in (False, True):
        output = run_child("post_xii", POST_XII, ("--audit", "--hostile"),
                           None, optimized)
        validate_post(output)
        post_outputs.append(output)
        executions += 1
    # Runtime is deliberately excluded; all proof fields are compared exactly.
    left = strict_json(post_outputs[0], "normal post-XII output")
    right = strict_json(post_outputs[1], "optimized post-XII output")
    left.pop("audit_seconds")
    right.pop("audit_seconds")
    require(left == right, "normal/-O post-XII proof receipts differ")
    require(sha256(canonical_bytes(left)) == POST_PROOF_RECEIPT_SHA256,
            "post-XII proof receipt digest changed")
    return len(children) + 1, executions


def audit_accounting(report: dict[str, Json]) -> None:
    require(sum(OWNER_COUNTS.values()) == 493417,
            "global owner identity does not sum to 493417")
    require(OWNER_COUNTS == {
        "payload_free": 605, "direct_rational": 29000,
        "scalar_sos_exclusive": 194351, "typed_diagonal_exclusive": 185309,
        "boundary_rescue": 296, "structural_I_III": 245,
        "packet_IV_XII": 29013, "post_XII_packets": 54597,
        "singleton_territory": 1,
    }, "global owner partition changed")
    require(EXPECTED_CHAIN == (83856, 83611, 54598, 1),
            "remainder chain changed")
    require(report["source_orbit_total"] == EXPECTED_CHAIN[2] and
            report["remaining_orbit_total"] == EXPECTED_CHAIN[3],
            "post-XII report is not the final link in the chain")


def manifest(full: bool, child_count: int, executions: int,
             ast_sources: int) -> dict[str, Json]:
    return {
        "schema": "rank-seven-order-eight-kernel-theorem-v1",
        "evidence_kind": "complete-exact-certificate-chain-relative-to-pinned-base-producers",
        "scope": {
            "graph": "finite-simple-connected",
            "rank": 7,
            "kernel_order": 8,
            "block_scope": "exactly-one-positive-rank-cyclic-block",
        },
        "exact_owner_partition": OWNER_COUNTS,
        "coarse_residual_total": 493417,
        "remainder_chain": list(EXPECTED_CHAIN),
        "targets_per_residual": 15,
        "singleton_row": SINGLETON_ROW,
        "base_producer_trust_roots": list(BASE_TRUST_ROOTS),
        "verification_mode": (
            "full-read-only-replay-with-kernel-census-regeneration-and-direct-pack-exact-replay"
            if full else "quick-pinned-artifact-gate"
        ),
        "child_receipt_sha256": CHILD_OUTPUT_SHA256,
        "direct_pack_replay_contract": {
            "coverage": DIRECT_COVERAGE,
            "execution_semantics": DIRECT_EXECUTION_SEMANTICS,
            "owner_linkage_fields": DIRECT_OWNER_FIELDS,
            "owner_replay_stream_sha256": DIRECT_OWNER_STREAM_SHA256,
            "source_rows": (
                "strict-decodes-and-canonically-re-encodes-pinned-492812-row-cache;"
                "does-not-rematerialize-cache-rows-from-census-chunks"
            ),
        },
        "semantic_action_equivalence_receipt": SEMANTIC_ACTION_EQUIVALENCE_RECEIPT,
        "post_xii_proof_receipt_sha256": POST_PROOF_RECEIPT_SHA256,
        "quick_mode_boundary": (
            None if full else
            "pins child sources, prior exact normal/-O output receipts, artifacts, schemas, "
            "singleton bytes, ASTs, and proof texts; it does not rerun semantic child replays"
        ),
        "orchestrated_children": child_count,
        "child_executions": executions,
        "assert_free_ast_sources": ast_sources,
        "all_lengths": True,
        "all_physical_parities": True,
        "rooted_trees": True,
        "theorem_gate_eligible": True,
        "conclusion": "s+(G)>=|V(G)|",
        "nonclaims": [
            "kernel orders nine through twelve",
            "rank-seven multiblock graphs",
            "all connected heptacyclic graphs",
            "fresh rerun of the three residual pinned base producer searches",
            "rematerialization of the direct-replay cache rows from census chunks",
        ],
        "dependency_categories": {
            "executed_python_sha256": EXECUTED_PYTHON_SHA256,
            "executed_data_sha256": EXECUTED_DATA_SHA256,
            "callable_unreached_python_sha256": CALLABLE_PYTHON_SHA256,
            "callable_unreached_data_sha256": CALLABLE_DATA_SHA256,
            "documentary_sha256": DOCUMENTARY_PROOF_SHA256,
        },
        "dependency_edge_policy": DEPENDENCY_EDGE_POLICY,
        "artifact_sha256": ARTIFACT_SHA256,
        "certificate_sha256": CERTIFICATE_SHA256,
    }


def audit(full: bool) -> dict[str, Json]:
    audit_source_pins()
    audit_dependency_edges()
    ast_sources = audit_no_asserts()
    report = audit_post_artifacts()
    audit_selected_stream_linkage()
    audit_math_sources()
    audit_accounting(report)
    child_count, executions = run_children(full)
    return manifest(full, child_count, executions, ast_sources)


def expect_rejection(action: Any, label: str,
                     exact_substrings: tuple[str, ...] = ()) -> str:
    try:
        action()
    except (KeyError, OSError, RuntimeError, TypeError, ValueError,
            UnicodeError, lzma.LZMAError) as error:
        message = str(error)
        for expected in exact_substrings:
            require(message.count(expected) == 1,
                    f"hostile rejection misattributed: {label}: expected exactly "
                    f"once {expected!r}; observed {message!r}")
        return message
    fail(f"hostile mutation accepted: {label}")


def hostile_self_checks() -> int:
    count = 0
    payload = strict_json(POST_REPORT.read_bytes(), "post report hostile seed")
    mutations = (
        lambda value: value.__setitem__("source_orbit_total", 54597),
        lambda value: value.__setitem__("owned_orbit_total", 54596),
        lambda value: value.__setitem__("remaining_orbit_total", 2),
        lambda value: value.__setitem__("targets_per_row", True),
        lambda value: value["owner_stream"].__setitem__("raw_sha256", "0" * 64),
        lambda value: value["reduced_remainder_stream"].__setitem__("record_total", 0),
        lambda value: value.__setitem__("full_theorem", True),
    )
    for mutation in mutations:
        changed = deepcopy(payload)
        mutation(changed)
        expect_rejection(lambda changed=changed: _validate_mutated_report(changed),
                         "mutated post report")
        count += 1
    bad_row = deepcopy(SINGLETON_ROW)
    bad_row[0] = 416987
    expect_rejection(lambda: _validate_singleton(bad_row), "stream/source index swap")
    count += 1
    bad_row = deepcopy(SINGLETON_ROW)
    bad_row[4][12] = 1
    expect_rejection(lambda: _validate_singleton(bad_row), "singleton parity")
    count += 1
    bad_counts = dict(OWNER_COUNTS)
    bad_counts["post_XII_packets"] -= 1
    expect_rejection(lambda: _validate_counts(bad_counts), "owner omission")
    count += 1
    expect_rejection(lambda: strict_json(b'{"a":1,"a":2}\n', "duplicate"),
                     "duplicate JSON key")
    count += 1
    expect_rejection(lambda: strict_json(b'{"a": 1}\n', "noncanonical"),
                     "noncanonical JSON")
    count += 1

    # Exercise the pure AST oracle itself; byte pins are intentionally bypassed.
    # Appending preserves every pre-existing source location.
    source_text = {name: path.read_text("ascii")
                   for name, path in _python_registry_paths().items()}
    source = "rank_six_order8_pipeline"
    source_path = _repo_path(_python_registry_paths()[source])
    append_line = len(source_text[source].splitlines()) + 1

    injected_import = (source_text[source] +
                       "importlib.util.spec_from_file_location('hostile', ENGINE_PATH)\n")
    import_span = (append_line, 0, append_line, 62)
    import_surplus = EdgeRecord(
        EDGE_DYNAMIC, source, source_path, "order8_vector_engine",
        _repo_path(ORDER8_VECTOR_ENGINE), CAT_CALLABLE_PYTHON, import_span,
        POLICY_CALLABLE,
        "observed-qualified-call/importlib.util.spec_from_file_location('hostile', "
        "ENGINE_PATH)")
    expect_rejection(
        lambda: audit_dependency_edges(source_text_overrides={source: injected_import}),
        "undeclared dynamic import edge",
        ("missing=[]; surplus=[" + _format_edge(import_surplus) + "]",))
    count += 1

    # This single appended line simultaneously exercises alias closure, a
    # qualified read call, and resolution of SOURCE's constant Path-join chain.
    injected_read = source_text[source] + "HOSTILE_FIXED = SOURCE; HOSTILE_FIXED.read_bytes()\n"
    read_span = (append_line, 24, append_line, 50)
    read_surplus = EdgeRecord(
        EDGE_READ, source, source_path, "rank_six_fixture",
        _repo_path(RANK_SIX_FIXTURE), CAT_CALLABLE_DATA, read_span,
        POLICY_CALLABLE,
        "observed-fixed-receiver/HOSTILE_FIXED")
    expect_rejection(
        lambda: audit_dependency_edges(source_text_overrides={source: injected_read}),
        "undeclared fixed read edge",
        ("missing=[]; surplus=[" + _format_edge(read_surplus) + "]",))
    count += 1

    # An unregistered constant Path join is an explicit unresolved surplus,
    # never silently omitted from the local fixed-read candidate set.
    injected_unknown = (source_text[source] +
                        "HOSTILE_UNKNOWN = HERE / 'not-registered.bin'; "
                        "HOSTILE_UNKNOWN.read_bytes()\n")
    unknown_span = (append_line, 47, append_line, 75)
    unknown_surplus = EdgeRecord(
        EDGE_READ, source, source_path, "<unresolved-local-target>",
        "<unresolved>", "<unresolved>", unknown_span, POLICY_CALLABLE,
        "observed-unresolved-fixed-receiver/HOSTILE_UNKNOWN")
    expect_rejection(
        lambda: audit_dependency_edges(source_text_overrides={source: injected_unknown}),
        "unresolved fixed read edge",
        ("missing=[]; surplus=[" + _format_edge(unknown_surplus) + "]",))
    count += 1

    # Mutate one existing generic loader caller on its own line.  The frozen
    # expected record remains exact_rational_base; AST resolution derives the
    # payload-free target, exposing one missing and one surplus record.
    loader_source = "exact_rational_engine"
    loader_old = "load_module(\"rank7_order8_r10_base\", BASE_PATH)"
    loader_new = "load_module(\"rank7_order8_r10_base\", OTHER_PTH)"
    alias_old = "BASE_PATH = HERE / \"rank6_order10_cubic_exact_rational.py\""
    alias_new = alias_old + "; OTHER_PTH = LANES_PATH"
    require(source_text[loader_source].count(loader_old) == 1 and
            source_text[loader_source].count(alias_old) == 1,
            "loader-target hostile seed changed")
    loader_changed = source_text[loader_source].replace(alias_old, alias_new, 1)
    loader_changed = loader_changed.replace(loader_old, loader_new, 1)
    loader_missing = next(record for record in DEPENDENCY_EDGE_POLICY
                          if record.source_key == loader_source and
                          record.target_key == "exact_rational_base")
    loader_surplus = EdgeRecord(
        EDGE_DYNAMIC, loader_source, _repo_path(EXACT_RATIONAL_ENGINE),
        "payload_free_lanes", _repo_path(PAYLOAD_FREE_LANES),
        CAT_EXECUTED_PYTHON, (56, 11, 56, 61), POLICY_EXECUTED,
        "module initialization/load_module@(63, 7, 63, 54)/OTHER_PTH")
    expect_rejection(
        lambda: audit_dependency_edges(
            source_text_overrides={loader_source: loader_changed}),
        "existing loader target movement",
        ("missing=[" + _format_edge(loader_missing) + "]",
         "surplus=[" + _format_edge(loader_surplus) + "]"))
    count += 1

    # Same-line substitution of an existing fixed receiver must independently
    # derive the changed registered target (not inherit the expected by site).
    read_source = "rank_six_order8_pipeline"
    fixed_old = "raw = SOURCE.read_bytes()"
    fixed_new = "raw = ENGINE_PATH.read_bytes()"
    require(source_text[read_source].count(fixed_old) == 1,
            "fixed-target hostile seed changed")
    fixed_changed = source_text[read_source].replace(fixed_old, fixed_new, 1)
    fixed_missing = next(record for record in DEPENDENCY_EDGE_POLICY
                         if record.source_key == read_source and
                         record.kind == EDGE_READ)
    fixed_surplus = EdgeRecord(
        EDGE_READ, read_source, _repo_path(RANK_SIX_ORDER8),
        "order8_vector_engine", _repo_path(ORDER8_VECTOR_ENGINE),
        CAT_CALLABLE_PYTHON, (64, 10, 64, 34), POLICY_CALLABLE,
        "observed-fixed-receiver/ENGINE_PATH")
    expect_rejection(
        lambda: audit_dependency_edges(
            source_text_overrides={read_source: fixed_changed}),
        "existing fixed-read target movement",
        ("missing=[" + _format_edge(fixed_missing) + "]",
         "surplus=[" + _format_edge(fixed_surplus) + "]"))
    count += 1

    # An exact variable-input exclusion is not a site-wide escape hatch.  Keep
    # the pre-existing span unchanged while replacing HERE/name by an
    # unregistered fixed Path alias; it must appear as an unresolved surplus.
    excluded_source = "structural_verifier"
    excluded_old = "raw=(HERE/name).read_bytes()"
    excluded_new = "raw=(HERE/NOPE).read_bytes()"
    require(len(excluded_old) == len(excluded_new) and
            source_text[excluded_source].count(excluded_old) == 1,
            "excluded-read hostile seed changed")
    excluded_changed = source_text[excluded_source].replace(
        excluded_old, excluded_new, 1)
    excluded_surplus = EdgeRecord(
        EDGE_READ, excluded_source, _repo_path(STRUCTURAL),
        "<unresolved-local-target>", "<unresolved>", "<unresolved>",
        (163, 8, 163, 32), POLICY_EXECUTED,
        "observed-unresolved-fixed-receiver/HERE / NOPE")
    expect_rejection(
        lambda: audit_dependency_edges(
            source_text_overrides={excluded_source: excluded_changed}),
        "exact excluded read receiver movement",
        ("missing=[]; surplus=[" + _format_edge(excluded_surplus) + "]",))
    count += 1

    # Caller location/provenance is frozen independently.  A one-column shift
    # of the real call leaves source lines unchanged and must fail on the exact
    # declared caller span rather than being rediscovered by line/name alone.
    caller_span_source = "exact_rational_engine"
    caller_span_old = "base = load_module(\"rank7_order8_r10_base\", BASE_PATH)"
    caller_span_new = "base =  load_module(\"rank7_order8_r10_base\", BASE_PATH)"
    require(source_text[caller_span_source].count(caller_span_old) == 1,
            "caller-span hostile seed changed")
    caller_span_changed = source_text[caller_span_source].replace(
        caller_span_old, caller_span_new, 1)
    expect_rejection(
        lambda: audit_dependency_edges(
            source_text_overrides={caller_span_source: caller_span_changed}),
        "dynamic caller span movement",
        ("dynamic caller span changed: exact_rational_engine:"
         "(63, 7, 63, 54):(63, 8, 63, 55)",))
    count += 1

    original = next(record for record in DEPENDENCY_EDGE_POLICY
                    if record.source_key == "exact_rational_base" and
                    record.target_key == "rank_six_frontier_artifact")
    moved = original._replace(target_category=CAT_EXECUTED_DATA,
                              call_policy=POLICY_EXECUTED)
    expect_rejection(
        lambda: audit_dependency_edges(
            category_overrides={"rank_six_frontier_artifact": CAT_EXECUTED_DATA}),
        "dependency category movement",
        ("missing=[" + _format_edge(original) + "]",
         "surplus=[" + _format_edge(moved) + "]"))
    count += 1

    # Mutate the real caller on the same line; the untouched callee/default
    # policy now derives an interprocedural fixed-read surplus at callee line 61.
    caller = "rank_six_atom_search"
    old_call = "order10.residual_rows(census10)"
    new_call = "order10.residual_rows(census10, cache_path=ARTIFACT)"
    require(source_text[caller].count(old_call) == 1,
            "call-policy hostile seed changed")
    weakened = source_text[caller].replace(old_call, new_call, 1)
    call_span = (316, 17, 316, 69)
    callee_span = (61, 44, 61, 67)
    call_provenance = (
        f"caller {caller}@{call_span} supplies cache_path=ARTIFACT; "
        f"callee exact_rational_base@{callee_span} cache_path.read_bytes")
    call_surplus = EdgeRecord(
        EDGE_READ, "exact_rational_base", _repo_path(EXACT_RATIONAL_BASE),
        "rank_six_atom_artifact", _repo_path(RANK_SIX_ATOM_ARTIFACT),
        CAT_CALLABLE_DATA, callee_span, POLICY_CALLABLE, call_provenance)
    expect_rejection(
        lambda: audit_dependency_edges(source_text_overrides={caller: weakened}),
        "call-policy weakening",
        ("missing=[]; surplus=[" + _format_edge(call_surplus) + "]",))
    count += 1
    return count


def _validate_mutated_report(report: dict[str, Json]) -> None:
    require(report == strict_json(POST_REPORT.read_bytes(), "pinned post report"),
            "post report mutation")


def _validate_singleton(row: Json) -> None:
    require(row == SINGLETON_ROW, "singleton row mutation")


def _validate_counts(counts: dict[str, int]) -> None:
    require(counts == OWNER_COUNTS and sum(counts.values()) == 493417,
            "owner count mutation")


def output_text(full: bool, rejected: int, manifest_digest: str) -> str:
    mode = "full" if full else "quick"
    return "\n".join((
        "rank-seven order-eight kernel theorem gate: exact audit passed",
        f"mode={mode} scope=single-positive-rank-block kernel_order=8 rank=7",
        "owners=493417 partition=605+29000+194351+185309+296+245+29013+54597+1",
        "remainders=83856->83611->54598->1 singleton=[416536,416987,6832,...,2]",
        "all_lengths=true all_parities=true rooted_trees=true theorem_gate=eligible",
        "trust_boundary=three residual pinned base producer outputs; direct packs freshly exact-replayed",
        "conclusion=s+(G)>=|V(G)| for rank-seven kernel order eight only",
        "nonclaim=no orders 9-12, no multiblock, no all-heptacyclic conclusion",
        f"hostile_mutations_rejected={rejected}",
        f"child_manifest_sha256={manifest_digest}",
    )) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true",
                        help=("run every semantic child in normal and -O, including "
                              "kernel/census regeneration, 29,000 direct-pack exact "
                              "replays, and 54,597 post-XII packet replays"))
    parser.add_argument("--print-manifest", action="store_true")
    parser.add_argument("--optimized-master-child", action="store_true",
                        help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        result = audit(args.full)
        rejected = hostile_self_checks()
        require(rejected == 21, "hostile mutation count changed")
        raw_manifest = canonical_bytes(result)
        text = output_text(args.full, rejected, sha256(raw_manifest))
        if not args.optimized_master_child and not sys.flags.optimize:
            command = [sys.executable, "-O", "-B", str(SELF),
                       "--optimized-master-child"]
            if args.full:
                command.append("--full")
            if args.print_manifest:
                command.append("--print-manifest")
            child = subprocess.run(command, check=False, capture_output=True, cwd=ROOT,
                                   env={**__import__("os").environ,
                                        "PYTHONDONTWRITEBYTECODE": "1"})
            require(child.returncode == 0 and child.stderr == b"",
                    "optimized master child failed")
            expected = (raw_manifest if args.print_manifest else b"") + text.encode("ascii")
            require(child.stdout == expected, "normal/-O master output differs")
        if args.print_manifest:
            sys.stdout.buffer.write(raw_manifest)
        sys.stdout.write(text)
        return 0
    except (KeyError, OSError, RuntimeError, TypeError, ValueError,
            UnicodeError, lzma.LZMAError) as error:
        sys.stderr.write(f"rank-seven order-eight kernel theorem: FAIL CLOSED: {error}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
