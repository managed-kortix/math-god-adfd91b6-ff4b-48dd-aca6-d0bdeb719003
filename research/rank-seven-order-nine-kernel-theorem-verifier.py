#!/usr/bin/env python3
"""Fail-closed master gate for the rank-seven/order-nine single-block theorem.

``--quick`` authenticates the complete registered code/data/proof inventory and
runs inexpensive contract checks, but is deliberately theorem-ineligible.
``--full`` additionally runs the exact census reconstruction together with all
precedence-ordered structural predicates and then replays every downstream
persisted certificate, induced-transfer classification, and obstruction Gram.

The master never treats a stored execution transcript, a caller-supplied
snapshot, a mode label, or aggregate sums as proof.  Eligibility comes only
from successful child executions on the currently pinned bytes.  All accepted
arithmetic is integral or rational; historical binary64 diagnostics are parsed
only inside certificate replayers and are never proof inputs.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import itertools
import json
import lzma
import os
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, NoReturn

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "research"
EXPERIMENTS = ROOT / "positive-square-energy" / "experiments"
HEPTACYCLIC = ROOT / "positive-square-energy" / "heptacyclic-general"

STRUCTURAL = EXPERIMENTS / "rank7_order9_structural_semantic_replayer.py"
UPSTREAM = EXPERIMENTS / "rank7_order9_upstream_owner_replayer.py"
CYCLE = EXPERIMENTS / "rank7_order9_cycle_gram_engine.py"
CYCLE_SOURCE = EXPERIMENTS / "rank7_order9_unowned_stratifier.py"
STRUCTURAL_SCANNER = EXPERIMENTS / "rank7_order9_structural_owners.py"
TRANSFER = HERE / "rank-seven-order-nine-induced-partition-transfer-verifier.py"
OBSTRUCTION = HERE / "rank-seven-order-nine-obstruction-branch-gram-verifier.py"
ANALYTIC_LIFT = HERE / "rank-seven-conditional-analytic-lift-verifier.py"
CENSUS_PRODUCER = EXPERIMENTS / "rank7_orders9_12_exact_residual_census.py"
COARSE_ENGINE = EXPERIMENTS / "rank7_parity_coarse_digest_census.py"
STRUCTURAL_OWNER = EXPERIMENTS / "rank7_order12_structural_owners.py"
ATOM_RECOGNIZER = EXPERIMENTS / "rank7_order7_symbolic_atom_recognizer.py"
COARSE_ATOM = HERE / "rank-seven-orders2-4-kernel-theorem-verifier.py"
KERNEL_FIXTURE = HERE / "fixtures" / "rank-seven-kernel-frontier-census.json"

STRUCTURAL_NOTE = HEPTACYCLIC / "rank-seven-single-block-structural-theorem.md"
COARSE_ATOM_NOTE = HEPTACYCLIC / "rank-seven-orders2-4-kernel-theorem.md"
TRANSFER_NOTE = HEPTACYCLIC / "rank-seven-order-nine-induced-partition-transfer.md"
OBSTRUCTION_NOTE = HEPTACYCLIC / "rank-seven-order-nine-obstruction-branch-gram-theorem.md"
BICYCLIC = ROOT / "all-bicyclic-graphs" / "paper.tex"
TRICYCLIC = ROOT / "all-tricyclic-graphs" / "paper.tex"
TETRACYCLIC = ROOT / "all-tetracyclic-graphs" / "paper.tex"

SCHEMA = "rank-seven-order-nine-kernel-theorem-master-v2"
Json = Any

PYTHON_PINS = {
    STRUCTURAL: "34b43bd2c5a6b9b487c841f74e524f06dd1adb16328c3b321b6510bd9d2987b8",
    UPSTREAM: "f8d05d43a31b10058cf37176ceaa14c2562b1e845495ebc210232db0fce6f56c",
    CYCLE: "f9267ac9b2d41a4a09254e71e66f39fd78ffaadd334a4761c44c1a51ca59072e",
    CYCLE_SOURCE: "be64c55437421cac434c0b610dac62784e89a0e9a9fc2b401139c98dc266de76",
    STRUCTURAL_SCANNER: "bca85e48a018e7b7c998216e6e14dca38db82e4970709e51571de3aee2d089c7",
    TRANSFER: "4b9cb58aeb68b869b9c254a21ae7bd3cf18fc7360e7afb0a47fd8e570c40b2fe",
    OBSTRUCTION: "21acdb25b08b89ce9a5241932bc23d5fbdfec4c76333ab50c78d9371cf79e0b8",
    ANALYTIC_LIFT: "55e7d67a670f22a7b872b122f3aadcd2036ba922993f5faac1c5b72e2232e611",
    CENSUS_PRODUCER: "c6dcc792c7899c3f494a3beb521c94da972a01a392cd77be78b0956bbee3b921",
    COARSE_ENGINE: "d285a1c29cace4cb30882662e786cf1e5086ebc579676a3aa114a18e2365b2a5",
    STRUCTURAL_OWNER: "ffd76058b58344ea066777bdfd6d29eaed154c8d8d243d2c37ddf942f9558c45",
    ATOM_RECOGNIZER: "10de4fb714c15756341a7dbddb5a4da9f8ce5e0393aacc9e9434d619ebce9734",
    COARSE_ATOM: "7332b98f7f0780faff038e758451bb53cdebbb6f4c90c3f0785649be5064ec7d",
}

CHUNK_SPECS = (
    ("2712d3b761b7518ee6481d767410408673da825c9a31ec17d5a17784926da812", "ececc24e071cc31b0678de01a1ffb0787f804354b00239f221006a9bffaccdc1", "ebc040006305390d28ae4f21b2072a66e2af8ef9cd7933d5e400dba6cc3ff47d", "55d425a40ff56de801564a9d602ad801b35ac9b3e0781b3c64cd5d2f0b5c47bf", "3291a0530787f18c7fb665df4b97ff0f7c61329113e93ae07ec1f7f8a8ef977e", "06caa86cb4dffa5b126348729afab7c01e7b6bc3068e252fc73dbb271d64c74f", "fa973b7a9702fef4ccbdefff5cf55dad910838f244ad46c72e97c51dfb134ff9"),
    ("6e4f63314b9f0dfb04fd9ecfd4b4c658fe306e31db6aaaa64b63e883afc099f0", "b49b1973f2d946e6c4b8a6ff295d0ce19c4d3c67cccb58014588a9edf12b7d7e", "6af96ac219d946e7bf631ccda7410bda3d2a8093711bdb1a43a0f87bd62e29dc", "94fbc591e59a43742c54aef1e694e2b213b90545f1f38f5700fe3922c2c2709e", "b0016a038f779f991b5487b340aa96d29804b6edb2a959dedbf65bfe21ea3904", "181151408ec32bac838dab03daf10689774db0cb9d7ab8c7540e78b7b48d3c9f", "41a43fbccc98dad484a3d73b569a6d8017b71b8577136c2dc0e6186fc5d6d723"),
    ("43c09e2ed2f38946e02efe095b7ff1621a48f98a1456ade7f8ebe19df51e3537", "5401fe71437f9f61cb3a6b09d480ac87dab2aab2f639dc954c1d3376ace2aad2", "7d109b0d4702e9f654ae9c4312136d88cd8b29aba8de7ad4f8b1d616a2aacb2b", "426f0d4db1b9e5bfed9dbdedfbb7e221102cb722b2dff9158307fb65a03b04f2", "3362ad6118b68c43ca291dbd98c24a5064a9a62de49e5854ac1f91454bc33f44", "8e5db504618536dffdc4e5a02b9073c8072e121118de1998ff13fa2e42f90c61", "86d301406134e1f56de677f41c0709c1ad708c9a001dbf03507efd55bf2d6210"),
    ("6159cf8336b5c88cdeba6ca08bfc101fbe4f9d6051a24ff88bd899304feaa60f", "197d33ce7afbddcd777e0f4c8af09a32ab4348d80c5d45ab061b24f0261da943", "d0cb1f8018cf646c17d322efa2a3b8fdfc9dad452a43d638e9d89aa7c8137374", "46b4acb4da1017413fc3d4b09fc4d32491b71f99817648bd5d612d440f8f8243", "66a2b59f136e1b8c7ab52ec0565955da1fad2983e281b4e9cbc489579d03bd02", "92b3cdeee21f08c0aeac5077d0e94c49ddb7193997b5e484bafbb0533c404b87", "ba116ca3d41239ea068b5b58cd111b9d44c10e19b832d03c380089117d084fc5"),
    ("8ae1b27ca907a081962626a43d0847f84a33a0f38d3e5cb605c741db029a1528", "8f172ae6231229769d6f4a6aa299207512d2347fc26a207fa15b708cc8c391db", "708c6b03c55c6e47545342746adf86bca91d416ed5ab75b0b576b057e55ecbb5", "e460fd14fc571d6468b5b9bc50f96a405e67dbc32f25bceefa2bcc2fc50a2a3a", "7d37c8ad2680646bdcafa2043cec860dd0b5355322f4c68e27d2fce5df971b4c", "d6babe283110b16697924f409a93d0b8abccdb1673b1e484910a70da9f72c1c2", "bd6ccb85269e743b635526d293d213d955d8a1765e95e49e1c137ce17d34e352"),
    ("d56e9117bb04e508177693f383aa31a3e3928254f544a4c4842e41c7a54ff94b", "4ce0e726bf6aaa32ae0167bb9bbc5b0c6ccb186cb6cc4092afe8c3634a0f1163", "6cf90f2086bb21cc8d59f73906dab8de53a33837a27f8fd88703cff4f5400985", "93ac72a3fb3347b4366d0f7702455e8584992877ef75c7f5f2246e0f3263c7f8", "84b001439c0758b8ea5bbd77e795acf2381727208d13c12a1a3b42a0f360fc0b", "1eefa52623aa5d40a353b88eadc54318e176f2e11c5aa5a59bbe02321c656f0c", "62f879bf8b289deb99d6df3745dd7c2d164a9aa441f4f89799c29221fb3011db"),
    ("6b9a46b712003412da9c53caa14dfdf80e14a95c152e1a1b215c87f420273842", "ca45002a215f82891a7d96c350a4b1b534174a3dfea8904dac6e4ce8baa5486d", "808e8c663a1d2568a1461d958908e43fd617fe00b1d5a22e6a3e4a4cf2632b6d", "2c65804fc70b6784b8279086ae0926535ec7c6cc036e7d83a5a25f845281a891", "0006b8da42d7de6b04b7d2b5821735aaaac2690bf7432419d13a0249e027af24", "a73a581e8565e7dcc0b4f8eaad0fdcf81b1fab31984e2dfc3948c1dd644747bb", "59a53ab0671664cafd43667587b3ef911c3056ca2dca799340fa7eca841df8f2"),
    ("e94b21dc4cc7e9dd0b88e3ca70f7a455cbc8373f3a0eb06c2f2ab7bbc0728392", "fe3912a744743d7d1c14ddfee8c0104dd34466d169f63abfc4b2550039c019ef", "1a70dd560c75f92460047c1af93b50832d9db17345118537ef207bff7a20df49", "9880385c8a2d8224e1d9baa4084b5f1baf18f0511601566d84815e376339807f", "4bd50cc03d1a04e0df576d9dba578cb048407ebbd98bcb34bba4751bb80ec666", "d0539aebac9c875c0b8d6d25cbef45ea8eb5f834ede8ba596fda38ab39694132", "8a5579f6b608b69e8223b6f24127e511614f9424141a12ec75198453b82c40f5"),
)
CENSUS_FILES = (
    "rank7_order9_census_0000_0562.json.xz", "rank7_order9_census_0562_1124.json.xz",
    "rank7_order9_census_1124_1686.json.xz", "rank7_order9_census_1686_2248.json.xz",
    "rank7_order9_census_2248_2810.json.xz", "rank7_order9_census_2810_3372.json.xz",
    "rank7_order9_census_3372_3934.json.xz", "rank7_order9_census_3934_4495.json.xz",
)
DATA_PINS = {
    KERNEL_FIXTURE: "a241139ab54ce4cce1ab3812887359edb241c0abfb1018e804b4a5f86762cfd5",
    EXPERIMENTS / "rank7_order9_exact_residual_census_manifest.json": "9ece0464ae31dbc6c2e5b715be054c7191bc5c12a0f6efaf008ac0e6641baf1f",
    EXPERIMENTS / "rank7_order9_structural_owner_manifest.json": "8097c55f455cf68e27e29b571ef5cd94e17057290d1f211fb3ecf81949f98366",
}
for _index, (_raw, _census, _report, _class_raw, _class_xz,
             _remainder_raw, _remainder_xz) in enumerate(CHUNK_SPECS):
    DATA_PINS[EXPERIMENTS / CENSUS_FILES[_index]] = _census
    _prefix = (EXPERIMENTS / "rank7_order9_structural_owner_scheduler" / "results" /
               f"chunk-{_index:02d}")
    DATA_PINS[Path(f"{_prefix}.json")] = _report
    DATA_PINS[Path(f"{_prefix}.classification.jsonl.xz")] = _class_xz
    DATA_PINS[Path(f"{_prefix}.remainder.jsonl.xz")] = _remainder_xz
DATA_PINS.update({
    EXPERIMENTS / "rank7_order9_typed_sos_owner_manifest.json": "76e80ac1e1aa5c3277883b8df43ab514fc196c1f8049544d254614a4e4375274",
    EXPERIMENTS / "rank7_order9_typed_sos_owners.jsonl.xz": "093a814275058b4ec2b1cfc7198bd3d49cac572c5ef90974d2103b201a79bcf6",
    EXPERIMENTS / "rank7_order9_after_sos_remainder.jsonl.xz": "2a45b69d495e65c47d4b3c668572b0b7922e808c905c501c97e513df47d05089",
    EXPERIMENTS / "rank7_order9_dominant_family_gram_lane.json": "7346c593bd98880ca9599f44ae26c69d20225342d361804740742caccdc75169",
    EXPERIMENTS / "rank7_order9_dominant_family_gram_owners.jsonl.xz": "5d41ae256f123a6fa6a31bed226b069ea070e52aaf50199c06d0dbfd0b914de9",
    EXPERIMENTS / "rank7_order9_third_family_cycle_gram_lane.json": "af5a3ae40631936c8b7360cd376838c340e62e0c55d01734f110072f20b83585",
    EXPERIMENTS / "rank7_order9_third_family_cycle_gram_owners.jsonl.xz": "9955f46b32f0b714f6c3b6b19778cd93f72bdb05ccd3c6e881a79bab288a77bf",
    EXPERIMENTS / "rank7_order9_fourth_family_cycle_gram_lane.json": "3f5d3c168b7b13ec58321063de52f0e387fd2b1ae6fbd919ee5aecfbba4404ce",
    EXPERIMENTS / "rank7_order9_fourth_family_cycle_gram_owners.jsonl.xz": "6423fd051a754ba0c810f79a51e83391926c2049ccf20c8cef0ad4c2a4e3867d",
})
EXPECTED_DATA_PATHS = frozenset(DATA_PINS)

DOCUMENT_PINS = {
    STRUCTURAL_NOTE: "f1daf9109f4843aa2db149c974fb21c847bb6f8144275201aebabed7fe4ea516",
    TRANSFER_NOTE: "3069961fe0937eabf3281685bcc04dd4e77de20150ddd49b57f1fa0eeb6c58ad",
    OBSTRUCTION_NOTE: "69d9a6d7a061ee8b9ef029d560799f51e19c3d6c199da9258f5929f684862899",
    BICYCLIC: "56a2b521ed0fee18d7e34ebb330e5b181e00979805fca951398f7a33d35b19da",
    TRICYCLIC: "13f8f8c7996c0f58f764c52b4a5b915132038e2ce38d3e56285f1bf952990fc1",
    TETRACYCLIC: "7d8174e64095e5cccf90776ccac92d2dd2ca3f73d500e2518461f5dfb907b93b",
    COARSE_ATOM_NOTE: "25e84efe5cba507e3ad0287a83505b544bbb8b40a401f7a45373d025b1bff399",
}

STRUCTURAL_FAST_OUTPUT_SHA256 = "cf8cebf6a9b0ccd4360eaaad57c10c0c5a5b058104aa583d4ac855a5717af552"
UPSTREAM_OUTPUT_SHA256 = "8975de0c41137973452e5699cd4eb339f520b7a8f8863a06e9d5f2a74192425b"
CYCLE_OUTPUT_SHA256 = "aa0f11d2a5f7e2bd49bba6d93bdd6b97de03eace705a98fd4c8cf7b636a6fb24"
TRANSFER_OUTPUT_SHA256 = "70154fd4dbded871ae77ffdc6a8ffdf7dc23ac86b8411aba983a90029fb642cd"
OBSTRUCTION_OUTPUT_SHA256 = "9e9bacf32b73627db45c092acfa785d1aafe465e4c8743f7054f74cf967d9770"
COARSE_ATOM_OUTPUT_SHA256 = "019aeb2fc058b61cebd2a98a0ee0025b345cca4b18fb706369a92e1f5ca81a02"

RESIDUAL_ORBITS = 2_835_895
RESIDUAL_PHYSICAL = 3_518_609
PARITY_ORBITS = 65_167_570
PARITY_PHYSICAL = 81_885_688
COARSE_ORBITS = 62_331_675
TARGETS_PER_RESIDUAL_ORBIT = 16
COARSE_TARGET_EQUIVALENT = TARGETS_PER_RESIDUAL_ORBIT * COARSE_ORBITS
RESIDUAL_TARGETS = TARGETS_PER_RESIDUAL_ORBIT * RESIDUAL_ORBITS
PARITY_TARGET_EQUIVALENT = TARGETS_PER_RESIDUAL_ORBIT * PARITY_ORBITS
COARSE_KERNEL_FIELDS = {
    "automorphisms", "coarse_certified_orbits", "coarse_residual_orbits",
    "coarse_residual_physical_rows", "edges", "global_kernel", "order_kernel",
    "parity_orbits", "physical_rows", "support_edges",
}
COARSE_ATOM_CONTRACT = {
    "atom_proof_scope": "47 order-four kernels; reusable exact tetrahedral inequalities only",
    "application_scope": "all 4,495 order-nine kernels and their parity orbits",
    "branch_vectors": "equal within a color; regular tetrahedron across colors",
    "different_color_scaled_cost": {
        "odd_positive": "18*m+10-13*o",
        "odd_zero": "18*m",
        "scale": 30,
    },
    "same_color_legal_iff": "o=0",
    "budget_scaled": 180,
    "colorings": "restricted-growth set partitions into at most four colors",
    "application_predicate":
        "minimum_crossing_18m[support] <= 180-10*|support|+13*sum(o)",
    "owner_semantics":
        "one retained branch Gram per parity orbit; fixed-parity coordinatewise path lengthening",
    "attachments": "arbitrary finite rooted trees by one-vertex additivity",
    "target_equivalent_is_bookkeeping_only": True,
    "coarse_owner_keys_materialized": False,
}
PARTITION_ORBITS = {"structural": 2_450_066, "sos": 113_309, "gram": 2_795,
                    "transfer": 268_110, "obstruction": 1_615}
PARTITION_PHYSICAL = {"structural": 3_076_384, "sos": 134_899, "gram": 3_204,
                      "transfer": 302_177, "obstruction": 1_945}
STRUCTURAL_CALLS = {"balanced-rank-one": 2_835_895, "signed-imbalance-psd": 2_834_382,
                    "simplex-mixed-atom": 2_831_563, "generalized-ray": 2_831_150}
STRUCTURAL_PASSES = {"balanced-rank-one": 1_513, "signed-imbalance-psd": 2_819,
                     "simplex-mixed-atom": 413, "generalized-ray": 2_445_321}
CENSUS_RAW_SHA256 = tuple(item[0] for item in CHUNK_SPECS)
SOURCE_IDENTITY = {
    "encoding": "sha256(concatenated canonical JSON [source_index,global_kernel,order_kernel,row,orbit_size] lines)",
    "source_index_encoding": "sha256(concatenated ASCII decimal source_index plus newline)",
    "source_index_range": [0, RESIDUAL_ORBITS],
    "universe_orbit_total": RESIDUAL_ORBITS,
    "universe_physical_total": RESIDUAL_PHYSICAL,
    "universe_source_index_sha256": "e3d0066cdcb88cec40ce67e50f1252064f8532a876b17d88ee9f5a283146c86a",
    "universe_key_sha256": "cf1ff383eaf48c64d02cf106a6a5c7cd8420fbed3f68194962ef335c8adc12c4",
    "owner_orbit_total": PARTITION_ORBITS["structural"],
    "owner_physical_total": PARTITION_PHYSICAL["structural"],
    "owner_source_index_sha256": "42380a735ddd66e819adf1c58bb19c039fdc6033bae80172903a49fba0ee12be",
    "owner_key_sha256": "48b5094918a3e921167ed4f3bc2397edb8c003a410262151752569f78ca4b8e2",
    "remainder_orbit_total": 385_829,
    "remainder_physical_total": 442_225,
    "remainder_source_index_sha256": "7d87a4a548a0d613f39ebf657e350ab7a8a6c22e055d20b0d959bd27441a322a",
    "remainder_key_sha256": "0442d023ca3401f692fcb7866129ad83758753027dcac373a16da3b170c53a3e",
    "partition_validated": True,
}
STRUCTURAL_FIELDS = {
    "automorphism_recomputations", "base_identity", "burnside_recomputations",
    "census_chunks_reconstructed", "census_coarse_certified_total_reconstructed",
    "census_coarse_residual_physical_total_reconstructed",
    "census_coarse_residual_total_reconstructed", "census_fixture_sha256",
    "census_frontier_target_total_reconstructed", "census_generate_chunk_calls",
    "census_kernels_reconstructed", "census_parity_orbit_total_reconstructed",
    "census_physical_row_total_reconstructed", "census_producer_loads",
    "census_producer_sha256", "census_reconstructed_raw_chunk_sha256",
    "census_reconstructed_raw_sha256", "census_reconstruction",
    "census_reconstruction_chunks", "census_reconstruction_eligible",
    "census_reconstruction_generate_calls", "census_reconstruction_kernel_total",
    "census_reconstruction_requested", "census_reconstruction_residual_orbit_total",
    "census_reconstruction_residual_physical_total", "census_residual_rows_reconstructed",
    "census_source_adapter", "census_source_engine_sha256", "chunk_total", "chunks",
    "classification_rows", "classification_stream_sha256", "combined_replay_eligible",
    "complete", "exclusive_owner_orbit_counts", "exclusive_owner_physical_counts",
    "full_theorem", "generalized_three_ray_calls", "generalized_three_ray_passes",
    "mixed_radix_canonicality_validated", "mode", "orbit_recomputations",
    "ordered_complement_validated", "owner_orbit_total", "owner_physical_total",
    "per_kernel_residual_ledgers_validated", "predicate_call_total", "predicate_calls",
    "predicate_pass_total", "predicate_passes", "predicate_replay_eligible",
    "predicate_unowned_rows", "read_only", "recognition_calls",
    "recognition_calls_definition", "remainder_orbit_total", "remainder_physical_total",
    "remainder_stream_sha256", "row_recognition_calls", "row_zip_total", "schema",
    "source_identity", "status", "stored_generalized_witnesses", "trust_boundary", "writes",
}
CHUNK_FIELDS = {"census_artifact_sha256", "census_raw_sha256", "chunk_index",
                "classification_artifact_sha256", "classification_sha256", "kernel_range",
                "remainder_artifact_sha256", "remainder_rows", "remainder_sha256",
                "report_sha256", "rows", "source_range"}
UPSTREAM_FIELDS = {"arithmetic", "combined_sos_dominant_physical", "dominant_family",
                   "read_only", "schema", "sos", "sos_owner_physical", "status"}
UPSTREAM_SOS_FIELDS = {"after_sos_orbits", "exclusive_owner_orbits",
                       "exclusive_owner_physical", "owner_key_sha256", "owner_orbits",
                       "owner_physical", "owner_targets", "structural_remainder_orbits"}
UPSTREAM_DOMINANT_FIELDS = {"owner_key_sha256", "owner_orbits", "owner_physical",
                            "owner_targets"}
CYCLE_RESULT_FIELDS = {"artifact_sha256", "physical_total", "raw_sha256", "record_total",
                       "target_total"}
TRANSFER_FIELDS = {"analytic_dependencies_authenticated", "applicable_kernels",
                   "canonical_kernel_types", "canonical_short_obstruction_rows",
                   "coordinate_long_frontiers", "deletion_choice_counts", "kernel_transfer_types",
                   "obstruction_kernels", "obstruction_orbits", "obstruction_physical",
                   "partition_owned_orbits", "partition_owned_physical", "post_lane_orbits",
                   "post_lane_physical", "represented_obstruction_kernels",
                   "short_targets_per_row", "source_orbits_recomputed", "target_orbits",
                   "target_physical"}

# Independently fixed totals for the eight order-nine kernel chunks.  These are
# deliberately per-kernel-ledger totals, not a digest of nonexistent materialized
# coarse-owner keys.
COARSE_CHUNK_TOTALS = (
    (8_865_408, 7_344_514, 7_040_481, 304_033, 359_892),
    (9_088_128, 7_535_184, 7_215_044, 320_140, 381_394),
    (10_265_504, 7_976_294, 7_636_963, 339_331, 428_984),
    (11_272_480, 9_063_052, 8_651_241, 411_811, 505_387),
    (9_894_872, 7_741_634, 7_412_160, 329_474, 415_542),
    (11_815_008, 9_267_632, 8_862_238, 405_394, 514_439),
    (10_541_984, 8_787_940, 8_409_322, 378_618, 447_736),
    (10_142_304, 7_451_320, 7_104_226, 347_094, 465_235),
)


def fail(message: str) -> NoReturn:
    raise RuntimeError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def canonical_bytes(value: Json) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("ascii")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def exact_sha256(value: Json, label: str) -> str:
    require(type(value) is str and len(value) == 64 and
            all(character in "0123456789abcdef" for character in value),
            f"{label}: invalid SHA-256")
    return value


def exact_int(value: Json, label: str, minimum: int = 0) -> int:
    require(type(value) is int and value >= minimum, f"{label}: invalid exact integer")
    return value


def exact_fields(value: Json, fields: set[str], label: str) -> dict[str, Json]:
    require(type(value) is dict and set(value) == fields, f"{label}: exact schema changed")
    return value


def strict_json(raw: bytes, label: str) -> Json:
    def pairs(items: list[tuple[str, Json]]) -> dict[str, Json]:
        result: dict[str, Json] = {}
        for key, value in items:
            require(type(key) is str and key not in result, f"{label}: duplicate/non-string key")
            result[key] = value
        return result

    def reject_number(token: str) -> NoReturn:
        fail(f"{label}: floating-point/nonstandard number rejected: {token}")

    try:
        value = json.loads(raw.decode("ascii"), object_pairs_hook=pairs,
                           parse_float=reject_number, parse_constant=reject_number)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"{label}: invalid JSON") from error
    require(raw == canonical_bytes(value), f"{label}: noncanonical JSON")
    return value


def parse_one_json(output: bytes, label: str) -> Json:
    return strict_json(output, label)


def audit_pins() -> dict[str, str]:
    registries = (PYTHON_PINS, DATA_PINS, DOCUMENT_PINS)
    require(all(set(left).isdisjoint(right) for index, left in enumerate(registries)
                for right in registries[index + 1:]), "dependency registries overlap")
    require(frozenset(DATA_PINS) == EXPECTED_DATA_PATHS and len(DATA_PINS) == 44,
            "complete data registry path set changed")
    require(len(PYTHON_PINS) == 13 and len(DOCUMENT_PINS) == 7 and len(CHUNK_SPECS) == 8,
            "dependency registry cardinality changed")
    observed = {}
    for path, expected in {**PYTHON_PINS, **DATA_PINS, **DOCUMENT_PINS}.items():
        exact_sha256(expected, f"registered digest for {path.name}")
        require(path.is_file(), f"missing dependency: {path.relative_to(ROOT)}")
        digest = sha256(path.read_bytes())
        require(digest == expected, f"dependency bytes changed: {path.relative_to(ROOT)}")
        observed[path.relative_to(ROOT).as_posix()] = digest
    return observed


def audit_no_asserts() -> int:
    paths = (Path(__file__).resolve(), *PYTHON_PINS)
    require(len(set(paths)) == len(paths), "Python source registry duplicates a path")
    for path in paths:
        tree = ast.parse(path.read_text("ascii"), filename=str(path))
        require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)),
                f"optimization-removable assert in {path.name}")
    return len(paths)


def audit_coarse_source_contract(
        contract: dict[str, Json] | None = None,
        atom_source: str | None = None,
        producer_source: str | None = None) -> dict[str, Json]:
    """Bind the reusable atom separately from its order-nine application.

    The orders2--4 child audits the exact tetrahedral inequalities on its own 47
    order-four kernels.  It is not represented as having scanned order nine.
    Order-nine ownership is instead reconstructed by the separately pinned
    producer/source-engine/fixture bytes and checked per kernel below.
    """
    require(sha256(COARSE_ATOM_NOTE.read_bytes()) == DOCUMENT_PINS[COARSE_ATOM_NOTE],
            "coarse atom note changed")
    contract = COARSE_ATOM_CONTRACT if contract is None else contract
    atom_source = COARSE_ATOM.read_text("ascii") if atom_source is None else atom_source
    producer_source = (CENSUS_PRODUCER.read_text("ascii") if producer_source is None
                       else producer_source)
    atom_fragments = (
        "if coloring[u] == coloring[v]:\n            if odd:\n                return None",
        "Fraction(1, 2) + (odd - 1) * Fraction(1, 6)",
        "(multiplicity - odd) * Fraction(3, 5)",
        "Fraction(1241, 6859) < Fraction(1, 3)",
        "Fraction(7, 13) ** 2 < Fraction(1, 3)",
        "fixed-parity coordinatewise lift",
        "arbitrary rooted trees at branch or subdivision vertices",
    )
    producer_fragments = (
        "BUDGET_SCALED = 180",
        "def restricted_colorings(order, limit=4):",
        "crossing = colors[:, u] != colors[:, v]",
        "costs[crossing] += np.int16(18 * multiplicity)",
        "support = np.bitwise_or.reduce(np.where(nonzero, support_bits, 0), axis=1)",
        "threshold = BUDGET_SCALED - 10 * np.bitwise_count(support) + 13 * odd_sum",
        "selected = minimum[support] > threshold",
        '"coarse_certified_orbits": expected_orbits - residual_orbit_count',
    )
    require(all(fragment in atom_source for fragment in atom_fragments),
            "coarse atom exact semantic source contract changed")
    require(all(fragment in producer_source for fragment in producer_fragments),
            "order-nine coarse-sieve source contract changed")
    require(contract == {
        "atom_proof_scope": "47 order-four kernels; reusable exact tetrahedral inequalities only",
        "application_scope": "all 4,495 order-nine kernels and their parity orbits",
        "branch_vectors": "equal within a color; regular tetrahedron across colors",
        "different_color_scaled_cost": {
            "odd_positive": "18*m+10-13*o", "odd_zero": "18*m", "scale": 30},
        "same_color_legal_iff": "o=0", "budget_scaled": 180,
        "colorings": "restricted-growth set partitions into at most four colors",
        "application_predicate":
            "minimum_crossing_18m[support] <= 180-10*|support|+13*sum(o)",
        "owner_semantics":
            "one retained branch Gram per parity orbit; fixed-parity coordinatewise path lengthening",
        "attachments": "arbitrary finite rooted trees by one-vertex additivity",
        "target_equivalent_is_bookkeeping_only": True,
        "coarse_owner_keys_materialized": False,
    }, "coarse owner semantic contract changed")

    # Exact algebra linking the atom table to the vectorized baseline/threshold
    # form.  Same-color with positive odd support is intentionally absent.
    for multiplicity in range(1, 16):
        for odd in range(multiplicity + 1):
            crossing_atom = (18 * multiplicity if odd == 0 else
                             18 * multiplicity + 10 - 13 * odd)
            baseline = 18 * multiplicity
            correction = 0 if odd == 0 else 10 - 13 * odd
            require(crossing_atom == baseline + correction,
                    "coarse atom/sieve scaled algebra changed")
            require((odd == 0) is (not bool(odd)),
                    "same-color odd-support legality changed")
    return deepcopy(contract)


def validate_coarse_application_chunks() -> dict[str, Json]:
    """Recheck stored per-kernel coarse/residual complement ledgers exactly."""
    ranges = ((0, 562), (562, 1124), (1124, 1686), (1686, 2248),
              (2248, 2810), (2810, 3372), (3372, 3934), (3934, 4495))
    previous_kernel = 0
    totals = [0, 0, 0, 0, 0]
    kernel_total = 0
    for chunk_index, (filename, expected_range, expected_totals) in enumerate(
            zip(CENSUS_FILES, ranges, COARSE_CHUNK_TOTALS, strict=True)):
        path = EXPERIMENTS / filename
        stored = path.read_bytes()
        require(sha256(stored) == DATA_PINS[path],
                f"coarse chunk {chunk_index}: artifact changed")
        try:
            raw = lzma.decompress(stored)
        except lzma.LZMAError as error:
            raise RuntimeError(f"coarse chunk {chunk_index}: invalid XZ") from error
        payload = strict_json(raw, f"coarse chunk {chunk_index}")
        kernels = payload.get("kernels")
        residuals = payload.get("residuals")
        require(type(kernels) is list and type(residuals) is list and
                payload.get("kernel_range") == list(expected_range) and
                payload.get("kernel_total") == len(kernels) == expected_range[1] - expected_range[0],
                f"coarse chunk {chunk_index}: scope/ledger changed")
        chunk_totals = [0, 0, 0, 0, 0]
        residual_by_kernel: dict[int, list[int]] = {}
        residual_mass_by_kernel: dict[int, int] = {}
        for record in residuals:
            require(type(record) is dict and
                    set(record) == {"global_kernel", "order_kernel", "orbit_size", "row"} and
                    type(record["order_kernel"]) is int and type(record["orbit_size"]) is int and
                    record["orbit_size"] >= 1,
                    f"coarse chunk {chunk_index}: malformed residual record")
            residual_by_kernel.setdefault(record["order_kernel"], []).append(record["orbit_size"])
            residual_mass_by_kernel[record["order_kernel"]] = (
                residual_mass_by_kernel.get(record["order_kernel"], 0) + record["orbit_size"])
        for ledger in kernels:
            exact_fields(ledger, COARSE_KERNEL_FIELDS,
                         f"coarse chunk {chunk_index} kernel ledger")
            local_kernel = ledger["order_kernel"]
            require(type(local_kernel) is int and local_kernel == previous_kernel + 1,
                    f"coarse chunk {chunk_index}: kernel order changed")
            previous_kernel = local_kernel
            for key in ("physical_rows", "parity_orbits", "coarse_certified_orbits",
                        "coarse_residual_orbits", "coarse_residual_physical_rows"):
                exact_int(ledger[key], f"coarse chunk {chunk_index} kernel {local_kernel}.{key}")
            require(ledger["parity_orbits"] == ledger["coarse_certified_orbits"] +
                    ledger["coarse_residual_orbits"] and
                    len(residual_by_kernel.get(local_kernel, ())) ==
                    ledger["coarse_residual_orbits"] and
                    residual_mass_by_kernel.get(local_kernel, 0) ==
                    ledger["coarse_residual_physical_rows"],
                    f"coarse chunk {chunk_index} kernel {local_kernel}: complement changed")
            values = (ledger["physical_rows"], ledger["parity_orbits"],
                      ledger["coarse_certified_orbits"], ledger["coarse_residual_orbits"],
                      ledger["coarse_residual_physical_rows"])
            chunk_totals = [left + right for left, right in zip(chunk_totals, values, strict=True)]
        require(tuple(chunk_totals) == expected_totals and
                payload.get("physical_row_total") == chunk_totals[0] and
                payload.get("parity_orbit_total") == chunk_totals[1] and
                payload.get("coarse_certified_total") == chunk_totals[2] and
                payload.get("coarse_residual_total") == chunk_totals[3] == len(residuals) and
                payload.get("coarse_residual_physical_total") == chunk_totals[4],
                f"coarse chunk {chunk_index}: aggregate/per-kernel ledgers disagree")
        totals = [left + right for left, right in zip(totals, chunk_totals, strict=True)]
        kernel_total += len(kernels)
    require(previous_kernel == kernel_total == 4495 and tuple(totals) ==
            (PARITY_PHYSICAL, PARITY_ORBITS, COARSE_ORBITS, RESIDUAL_ORBITS,
             RESIDUAL_PHYSICAL), "global coarse/residual complement changed")
    return {"kernel_total": kernel_total, "per_kernel_complements_validated": True,
            "physical_rows": totals[0], "parity_orbits": totals[1],
            "coarse_owner_orbits": totals[2], "residual_orbits": totals[3],
            "residual_physical_rows": totals[4],
            "coarse_owner_keys_materialized": False}


def run_coarse_atom() -> dict[str, Json]:
    command = child_command(COARSE_ATOM, ())
    completed = subprocess.run(command, check=False, capture_output=True,
                               env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    require(completed.returncode == 0 and completed.stderr == b"" and
            sha256(completed.stdout) == COARSE_ATOM_OUTPUT_SHA256,
            "coarse atom exact normal/-O audit changed")
    lines = completed.stdout.decode("ascii").splitlines()
    require(lines == [
        "rank-seven orders2-4 kernel theorem: exact hostile audit passed",
        "direct_kernel_census: counts=1+6+47=54",
        "physical_parity_rows=9253 parity_orbits=7017",
        "canonical_plus_coordinate_targets=76933",
        "max_excess_by_order=2:6 3:6 4:28/5",
        "scope: every simple subdivision; arbitrary rooted-tree attachments",
        "conclusion: s+(G)>=|V(G)| for rank-seven kernel orders 2 through 4",
        "nonclaim: orders 5-12, multiblock graphs, and all connected heptacyclic graphs",
        "exact_manifest_sha256: 3c26a7d8f2be15df7c532ad7aa7ba44ec137f70ebda9f16a487a0dc825499ed7",
        "rejected_hostile_mutations: 8",
    ], "coarse atom exact output contract changed")
    return {"proof_scope": "orders2-4 atom audit; 47 order-four kernels",
            "application_scope": "not an order-nine row scan",
            "source_sha256": PYTHON_PINS[COARSE_ATOM],
            "note_sha256": DOCUMENT_PINS[COARSE_ATOM_NOTE],
            "output_sha256": COARSE_ATOM_OUTPUT_SHA256,
            "normal_O_byte_identity": "enforced by child"}


def expected_chunks() -> list[dict[str, Json]]:
    rows = (304033, 320140, 339331, 411811, 329474, 405394, 378618, 347094)
    remainder_rows = (57142, 59824, 51059, 40164, 53754, 30780, 41548, 51558)
    ranges = ((0, 562), (562, 1124), (1124, 1686), (1686, 2248),
              (2248, 2810), (2810, 3372), (3372, 3934), (3934, 4495))
    cursor = 0
    result = []
    for index, pin in enumerate(CHUNK_SPECS):
        item = {"chunk_index": index, "kernel_range": list(ranges[index]),
                "source_range": [cursor, cursor + rows[index]], "rows": rows[index],
                "census_raw_sha256": pin[0], "census_artifact_sha256": pin[1],
                "report_sha256": pin[2], "classification_sha256": pin[3],
                "classification_artifact_sha256": pin[4],
                "remainder_rows": remainder_rows[index], "remainder_sha256": pin[5],
                "remainder_artifact_sha256": pin[6]}
        result.append(item)
        cursor += rows[index]
    require(cursor == RESIDUAL_ORBITS, "expected chunk rows changed")
    return result


def validate_structural(result: Json, *, predicates: bool, census: bool) -> None:
    exact_fields(result, STRUCTURAL_FIELDS, "structural result")
    require(result["schema"] == "rank-seven-order-nine-structural-semantic-replay-v1" and
            result["status"] == "passed" and result["complete"] is True and
            result["full_theorem"] is False and result["read_only"] is True and
            result["writes"] == 0 and result["chunk_total"] == 8,
            "structural identity changed")
    require(result["base_identity"] == {
        "coarse_certified_total": COARSE_ORBITS, "coarse_residual_physical_total": RESIDUAL_PHYSICAL,
        "coarse_residual_total": RESIDUAL_ORBITS, "frontier_target_total": RESIDUAL_ORBITS * 16,
        "identity_validated": True, "kernel_total": 4495, "parity_orbit_total": PARITY_ORBITS,
        "physical_row_total": PARITY_PHYSICAL}, "structural base identity changed")
    require(type(result["chunks"]) is list and len(result["chunks"]) == 8 and
            all(type(item) is dict and set(item) == CHUNK_FIELDS for item in result["chunks"]) and
            result["chunks"] == expected_chunks(), "structural chunk vector changed")
    require(result["exclusive_owner_orbit_counts"] == STRUCTURAL_PASSES and
            result["exclusive_owner_physical_counts"] == {
                "balanced-rank-one": 1593, "generalized-ray": 3_071_139,
                "signed-imbalance-psd": 3185, "simplex-mixed-atom": 467} and
            result["owner_orbit_total"] == PARTITION_ORBITS["structural"] and
            result["owner_physical_total"] == PARTITION_PHYSICAL["structural"] and
            result["remainder_orbit_total"] == 385_829 and
            result["remainder_physical_total"] == 442_225 and
            result["row_zip_total"] == result["classification_rows"] == RESIDUAL_ORBITS and
            result["classification_stream_sha256"] ==
                "6813439803f5feda9183d194fd8d1a2d3032861c7f7155d5ed02050f416c2f71" and
            result["remainder_stream_sha256"] ==
                "0442d023ca3401f692fcb7866129ad83758753027dcac373a16da3b170c53a3e" and
            result["orbit_recomputations"] == RESIDUAL_ORBITS and
            result["automorphism_recomputations"] == result["burnside_recomputations"] == 4495 and
            result["mixed_radix_canonicality_validated"] is True and
            result["ordered_complement_validated"] is True and
            result["per_kernel_residual_ledgers_validated"] is True and
            result["source_identity"] == SOURCE_IDENTITY and
            result["stored_generalized_witnesses"] == 0,
            "structural exact partition/source identity changed")
    require(result["census_producer_sha256"] == PYTHON_PINS[CENSUS_PRODUCER] and
            result["census_source_engine_sha256"] == PYTHON_PINS[COARSE_ENGINE] and
            result["census_fixture_sha256"] == DATA_PINS[KERNEL_FIXTURE] and
            result["census_source_adapter"] ==
                "pinned fixture order plus local exact weighted-automorphism actions",
            "structural census source identity changed")
    zero_calls = {key: 0 for key in STRUCTURAL_CALLS}
    if predicates:
        require(result["predicate_replay_eligible"] is True and
                result["recognition_calls"] == result["row_recognition_calls"] == RESIDUAL_ORBITS and
                result["predicate_calls"] == STRUCTURAL_CALLS and
                result["predicate_call_total"] == sum(STRUCTURAL_CALLS.values()) and
                result["predicate_passes"] == STRUCTURAL_PASSES and
                result["predicate_pass_total"] == PARTITION_ORBITS["structural"] and
                result["predicate_unowned_rows"] == 385_829 and
                result["generalized_three_ray_calls"] == STRUCTURAL_CALLS["generalized-ray"] and
                result["generalized_three_ray_passes"] == STRUCTURAL_PASSES["generalized-ray"],
                "structural full predicate vector changed")
    else:
        require(result["predicate_replay_eligible"] is False and
                result["recognition_calls"] == result["row_recognition_calls"] == 0 and
                result["predicate_calls"] == result["predicate_passes"] == zero_calls and
                result["predicate_call_total"] == result["predicate_pass_total"] == 0 and
                result["predicate_unowned_rows"] == 0 and
                result["generalized_three_ray_calls"] == result["generalized_three_ray_passes"] == 0,
                "structural non-predicate mode laundered replay")
    zero_reconstruction = {
        "census_producer_loads": 0, "census_generate_chunk_calls": 0,
        "census_reconstruction_generate_calls": 0, "census_chunks_reconstructed": 0,
        "census_reconstruction_chunks": 0, "census_kernels_reconstructed": 0,
        "census_reconstruction_kernel_total": 0, "census_residual_rows_reconstructed": 0,
        "census_reconstruction_residual_orbit_total": 0,
        "census_physical_row_total_reconstructed": 0,
        "census_parity_orbit_total_reconstructed": 0,
        "census_coarse_certified_total_reconstructed": 0,
        "census_coarse_residual_total_reconstructed": 0,
        "census_coarse_residual_physical_total_reconstructed": 0,
        "census_reconstruction_residual_physical_total": 0,
        "census_frontier_target_total_reconstructed": 0,
    }
    if census:
        require(result["census_reconstruction"] is True and
                result["census_reconstruction_requested"] is True and
                result["census_reconstruction_eligible"] is True and
                result["census_producer_loads"] == 1 and
                result["census_generate_chunk_calls"] ==
                    result["census_reconstruction_generate_calls"] == 8 and
                result["census_chunks_reconstructed"] ==
                    result["census_reconstruction_chunks"] == 8 and
                result["census_kernels_reconstructed"] ==
                    result["census_reconstruction_kernel_total"] == 4495 and
                result["census_residual_rows_reconstructed"] ==
                    result["census_reconstruction_residual_orbit_total"] == RESIDUAL_ORBITS and
                result["census_physical_row_total_reconstructed"] == PARITY_PHYSICAL and
                result["census_parity_orbit_total_reconstructed"] == PARITY_ORBITS and
                result["census_coarse_certified_total_reconstructed"] == COARSE_ORBITS and
                result["census_coarse_residual_total_reconstructed"] == RESIDUAL_ORBITS and
                result["census_coarse_residual_physical_total_reconstructed"] ==
                    result["census_reconstruction_residual_physical_total"] == RESIDUAL_PHYSICAL and
                result["census_frontier_target_total_reconstructed"] == RESIDUAL_ORBITS * 16 and
                result["census_reconstructed_raw_chunk_sha256"] ==
                    result["census_reconstructed_raw_sha256"] == list(CENSUS_RAW_SHA256),
                "fresh census execution/hash vector changed")
    else:
        require(result["census_reconstruction"] is False and
                result["census_reconstruction_requested"] is False and
                result["census_reconstruction_eligible"] is False and
                result["census_reconstructed_raw_chunk_sha256"] == [] and
                result["census_reconstructed_raw_sha256"] == [] and
                all(result[key] == value for key, value in zero_reconstruction.items()),
                "structural non-census mode laundered reconstruction")
    require(result["combined_replay_eligible"] is (predicates and census) and
            result["mode"] == ({(False, False): "authenticated-stored-stream-zip",
                                (True, True): "fresh-census-plus-fresh-full-predicate-replay"}
                               [(predicates, census)]),
            "structural mode/combined eligibility changed")


def validate_upstream(result: Json) -> None:
    exact_fields(result, UPSTREAM_FIELDS, "upstream result")
    sos = exact_fields(result["sos"], UPSTREAM_SOS_FIELDS, "upstream SOS")
    dominant = exact_fields(result["dominant_family"], UPSTREAM_DOMINANT_FIELDS,
                            "upstream dominant")
    require(result == {
        "arithmetic": "fractions.Fraction", "combined_sos_dominant_physical": 136072,
        "dominant_family": {"owner_key_sha256":
            "2d264fcf673d21f2200fbfddc1833b1f87f6f2351ee220e96b62db21d2ba7c11",
            "owner_orbits": 1128, "owner_physical": 1173, "owner_targets": 18048},
        "read_only": True, "schema": "rank-seven-order-nine-upstream-owner-replay-v1",
        "sos": {"after_sos_orbits": 272520,
            "exclusive_owner_orbits": {"scalar-sos": 7796, "typed-sos": 105513},
            "exclusive_owner_physical": {"scalar-sos": 10958, "typed-sos": 123941},
            "owner_key_sha256": "e79f723c4cfb47dde6a922067c684bb425f8e84422e1973cfefc54ee4ad86465",
            "owner_orbits": 113309, "owner_physical": 134899, "owner_targets": 1812944,
            "structural_remainder_orbits": 385829},
        "sos_owner_physical": 134899, "status": "exact-upstream-owner-replay-passed"},
        "upstream exact replay vector changed")
    require(sos["after_sos_orbits"] + sos["owner_orbits"] == 385829 and
            dominant["owner_orbits"] == 1128, "upstream complement chain changed")


def validate_cycle(result: Json) -> None:
    exact_fields(result, {"third", "fourth"}, "cycle result")
    expected = {
        "third": {"artifact_sha256": "9955f46b32f0b714f6c3b6b19778cd93f72bdb05ccd3c6e881a79bab288a77bf",
                  "physical_total": 748, "raw_sha256":
                  "2f35c2a76ce054be0d5b2ed18c0bfd77f163c1429af35ca48b91313ba77d0154",
                  "record_total": 631, "target_total": 10096},
        "fourth": {"artifact_sha256": "6423fd051a754ba0c810f79a51e83391926c2049ccf20c8cef0ad4c2a4e3867d",
                   "physical_total": 1283, "raw_sha256":
                   "a347d2d7891609156692d0bf0614783d79a9b84c6f4e0902ef6672f1cb4c96f5",
                   "record_total": 1036, "target_total": 16576}}
    require(all(type(result[key]) is dict and set(result[key]) == CYCLE_RESULT_FIELDS
                for key in result) and result == expected, "cycle exact replay vector changed")


def validate_transfer(result: Json) -> None:
    exact_fields(result, TRANSFER_FIELDS, "transfer result")
    require(result == {
        "analytic_dependencies_authenticated": False, "applicable_kernels": 4022,
        "canonical_kernel_types": {"2-cross-4": 1122, "3-cross-2": 400,
                                   "3-cross-3": 1689, "4-cross-2": 811},
        "canonical_short_obstruction_rows": 1615, "coordinate_long_frontiers": 24225,
        "deletion_choice_counts": {"6": 216, "7": 208, "8": 49},
        "kernel_transfer_types": {"2-cross-4": 23913, "3-cross-2": 51251,
                                  "3-cross-3": 104224, "4-cross-2": 88722},
        "obstruction_kernels": 473, "obstruction_orbits": 1615,
        "obstruction_physical": 1945, "partition_owned_orbits": 268110,
        "partition_owned_physical": 302177, "post_lane_orbits": 269725,
        "post_lane_physical": 304122, "represented_obstruction_kernels": 115,
        "short_targets_per_row": {"1": 697, "2": 513, "3": 245, "4": 160},
        "source_orbits_recomputed": 272520,
        "target_orbits": {"cubic-vertex-long-incidence": 22742,
                          "cubic-vertex-short-incidence": 3098, "partition": 4289760},
        "target_physical": {"cubic-vertex-long-incidence": 27402,
                            "cubic-vertex-short-incidence": 3718, "partition": 4834832}},
        "induced transfer exact output changed")


def validate_obstruction(result: Json) -> None:
    require(result == {"all_descendant_rows": 1615, "all_descendant_targets": 25840,
        "direct_exact_cost": [607593754, 122731245], "direct_rows": 1,
        "frontier_physical_rows": 1945, "frontier_rows": 1615,
        "represented_kernels": 115, "switched_three_ray_max_scaled_charge": 360,
        "switched_three_ray_rows": 1614, "witness_stream_sha256":
        "912058dbc7f22d33bd777c4b848aaba7168f8dd280a1605871403eb22a213d4c"},
        "obstruction exact output changed")


def child_command(path: Path, arguments: tuple[str, ...]) -> list[str]:
    command = [sys.executable, "-B"]
    if sys.flags.optimize:
        command.append("-O")
    return [*command, str(path), *arguments]


def run_child(name: str, path: Path, arguments: tuple[str, ...], output_sha256: str | None,
              validator, report_line: str | None = None) -> dict[str, Json]:
    require(path in PYTHON_PINS and sha256(path.read_bytes()) == PYTHON_PINS[path],
            f"child source changed: {name}")
    command = child_command(path, arguments)
    environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    completed = subprocess.run(command, check=False, capture_output=True, env=environment)
    require(completed.returncode == 0 and completed.stderr == b"", f"child failed: {name}")
    if output_sha256 is not None:
        exact_sha256(output_sha256, f"{name} output pin")
        require(sha256(completed.stdout) == output_sha256, f"child output changed: {name}")
    if report_line is None:
        result = parse_one_json(completed.stdout, name)
    else:
        lines = completed.stdout.splitlines(keepends=True)
        require(len(lines) == 2 and lines[1] == (report_line + "\n").encode("ascii"),
                f"{name}: report line changed")
        result = strict_json(lines[0], name)
    validator(result)
    return {"name": name, "arguments": list(arguments),
            "source_sha256": PYTHON_PINS[path], "output_sha256": sha256(completed.stdout),
            "result": result}


def source_kernels_stdlib() -> dict[int, tuple[int, tuple[tuple[int, int, int], ...]]]:
    raw = KERNEL_FIXTURE.read_bytes()
    require(sha256(raw) == DATA_PINS[KERNEL_FIXTURE], "cycle kernel fixture changed")
    payload = strict_json(raw, "cycle kernel fixture")
    require(type(payload) is dict and
            tuple(payload["counts_by_order_n2_to_n12"]) ==
            (1, 6, 47, 233, 914, 2270, 4015, 4495, 3396, 1391, 365),
            "cycle kernel counts changed")
    kernels = {}
    local = 0
    for global_index, record in enumerate(payload["kernels"], 1):
        require(type(record) is dict and type(record.get("n")) is int and
                type(record.get("code")) is list and
                len(record["code"]) == record["n"] * (record["n"] - 1) // 2 and
                all(type(value) is int and value >= 0 for value in record["code"]),
                "cycle kernel fixture record malformed")
        if record["n"] != 9:
            continue
        local += 1
        edges = tuple((u, v, multiplicity)
                      for (u, v), multiplicity in zip(
                          itertools.combinations(range(9), 2), record["code"], strict=True)
                      if multiplicity)
        kernels[local] = (global_index, edges)
    require(len(kernels) == 4495, "cycle order-nine kernel count changed")
    return kernels


def cycle_authenticated_source(module) -> tuple[Json, ...]:
    report, report_sha = module.strict_canonical_json(module.SOURCE_REPORT, "SOS owner report")
    source_info = report["updated_remainder_stream"]
    require(source_info["path"] == module.SOURCE_STREAM.name and
            module.file_sha256(module.SOURCE_STREAM) == source_info["artifact_sha256"],
            "cycle after-SOS artifact changed")
    digest = hashlib.sha256()
    records = {}
    physical = 0
    previous_source_index = -1
    with lzma.open(module.SOURCE_STREAM, "rb") as stream:
        for raw in stream:
            record = module.strict_json(raw, module.SOURCE_STREAM.name)
            require(raw == module.canonical_bytes(record) and type(record) is list and
                    len(record) == 5 and type(record[0]) is int and
                    record[0] > previous_source_index and record[0] not in records and
                    type(record[1]) is int and type(record[2]) is int and
                    type(record[3]) is list and
                    all(type(value) is int and value >= 0 for value in record[3]) and
                    type(record[4]) is int and record[4] > 0,
                    "cycle source row malformed, duplicate, or out of order")
            previous_source_index = record[0]
            records[record[0]] = record
            physical += record[4]
            digest.update(raw)
    require(len(records) == source_info["record_total"] and
            digest.hexdigest() == source_info["raw_sha256"],
            "cycle after-SOS source identity changed")
    kernels = source_kernels_stdlib()
    from collections import Counter
    strata = Counter()
    physical_strata = Counter()
    for record in records.values():
        expected_global, edges = kernels[record[2]]
        require(record[1] == expected_global, "cycle source kernel reference changed")
        key = module.family(edges, tuple(record[3]))
        strata[key] += 1
        physical_strata[key] += record[4]
    return (None, kernels, report_sha, source_info, records, physical, strata, physical_strata)


def run_cycle() -> dict[str, Json]:
    import importlib.util
    require(sha256(CYCLE.read_bytes()) == PYTHON_PINS[CYCLE], "cycle source changed")
    spec = importlib.util.spec_from_file_location("rank7_order9_master_cycle", CYCLE)
    require(spec is not None and spec.loader is not None, "cannot load cycle verifier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    authenticated = cycle_authenticated_source(module)
    result = {}
    all_indices = set()
    for name in ("third", "fourth"):
        lane = module.HISTORICAL_LANES[name]
        replay = module.replay_owner_stream(lane["owners"], lane["target"], lane,
                                            lane["report"], authenticated)
        report = module.strict_json(lane["report"].read_bytes(), lane["report"].name)
        if name == "third":
            require(report["prior_lane"] == {"owned_orbit_total": 1018,
                    "remainder_total": 270374,
                    "report_sha256": "79a0fd27298125d9ac1a776b9b144f5cafb3e55e03d0c4615eb5c0d3f026b921"} and
                    report["remaining_remainder_total"] == 269743,
                    "historical missing-1018 metadata changed")
        else:
            require(report["prior_lane"] == {"owned_orbit_total": 631,
                    "remainder_total": 269743,
                    "report_sha256": module.HISTORICAL_LANES["third"]["report_sha256"]} and
                    report["remaining_remainder_total"] == 268707,
                    "fourth historical chain metadata changed")
        indices = set()
        previous_source_index = -1
        with lzma.open(lane["owners"], "rb") as stream:
            for raw in stream:
                payload = module.strict_json(raw, lane["owners"].name)
                require(type(payload) is list and len(payload) == 4 and
                        type(payload[0]) is list and len(payload[0]) == 5 and
                        type(payload[0][0]) is int,
                        "historical cycle owner row malformed")
                record = payload[0]
                require(record[0] > previous_source_index and record[0] not in indices and
                        record[0] not in all_indices,
                        "historical cycle streams overlap or are out of order")
                previous_source_index = record[0]
                indices.add(record[0])
        all_indices.update(indices)
        result[name] = replay
    validate_cycle(result)
    raw = canonical_bytes(result)
    require(sha256(raw) == CYCLE_OUTPUT_SHA256, "cycle output digest changed")
    return {"name": "third-fourth-cycle-grams", "arguments": ["third", "fourth"],
            "source_sha256": PYTHON_PINS[CYCLE], "output_sha256": sha256(raw), "result": result}


def validate_target_accounting(coarse_orbits: int = COARSE_ORBITS,
                               residual_orbits: int = RESIDUAL_ORBITS) -> dict[str, Json]:
    exact_int(coarse_orbits, "coarse owner orbit total")
    exact_int(residual_orbits, "residual orbit total")
    require(coarse_orbits == COARSE_ORBITS and residual_orbits == RESIDUAL_ORBITS and
            coarse_orbits + residual_orbits == PARITY_ORBITS and
            COARSE_TARGET_EQUIVALENT == 997_306_800 and
            RESIDUAL_TARGETS == 45_374_320 and
            PARITY_TARGET_EQUIVALENT == 1_042_681_120 and
            COARSE_TARGET_EQUIVALENT + RESIDUAL_TARGETS == PARITY_TARGET_EQUIVALENT,
            "coarse/residual target-equivalent accounting changed")
    return {
        "coarse_owner_orbits": coarse_orbits,
        "residual_orbits": residual_orbits,
        "parity_orbits": PARITY_ORBITS,
        "targets_per_residual_frontier": TARGETS_PER_RESIDUAL_ORBIT,
        "coarse_target_equivalent": COARSE_TARGET_EQUIVALENT,
        "residual_frontier_targets": RESIDUAL_TARGETS,
        "parity_target_equivalent": PARITY_TARGET_EQUIVALENT,
        "semantics": (
            "coarse_target_equivalent is bookkeeping only: one retained branch Gram per "
            "coarse orbit directly covers all same-parity descendants; it is not a set of "
            "materialized frontier certificates or keys"),
        "coarse_owner_key_digest": None,
    }


def validate_partition(orbits: dict[str, int] | None = None,
                       physical: dict[str, int] | None = None) -> None:
    orbits = PARTITION_ORBITS if orbits is None else orbits
    physical = PARTITION_PHYSICAL if physical is None else physical
    require(type(orbits) is dict and set(orbits) == set(PARTITION_ORBITS) and
            all(type(value) is int and value >= 0 for value in orbits.values()) and
            type(physical) is dict and set(physical) == set(PARTITION_PHYSICAL) and
            all(type(value) is int and value >= 0 for value in physical.values()),
            "partition schemas changed")
    require(sum(orbits.values()) == RESIDUAL_ORBITS and
            sum(physical.values()) == RESIDUAL_PHYSICAL and
            COARSE_ORBITS + RESIDUAL_ORBITS == PARITY_ORBITS,
            "base partition arithmetic changed")
    require(orbits == {"structural": 2_450_066, "sos": 113_309,
            "gram": 1128 + 631 + 1036, "transfer": 268_110, "obstruction": 1615} and
            RESIDUAL_ORBITS - orbits["structural"] == 385829 and
            385829 - orbits["sos"] == 272520 and
            272520 - orbits["gram"] == 269725 and
            269725 == orbits["transfer"] + orbits["obstruction"],
            "precedence orbit complements changed")
    require(physical == {"structural": 3_076_384, "sos": 134_899,
            "gram": 1173 + 748 + 1283, "transfer": 302_177, "obstruction": 1945} and
            RESIDUAL_PHYSICAL - physical["structural"] == 442225 and
            442225 - physical["sos"] == 307326 and
            307326 - physical["gram"] == 304122 and
            304122 == physical["transfer"] + physical["obstruction"],
            "precedence physical complements changed")


def validate_analytic_sources() -> dict[str, Json]:
    completed = subprocess.run(child_command(ANALYTIC_LIFT, ("--print-manifest",)),
                               check=False, capture_output=True,
                               env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    require(completed.returncode == 0 and completed.stderr == b"", "analytic lift failed")
    lines = completed.stdout.splitlines(keepends=True)
    require(len(lines) == 2 and lines[1] ==
            b"rank-seven conditional analytic lift: exact contract audit passed; budget=6; global_claim=false; finite_premise_discharged=false\n",
            "analytic lift report changed")
    manifest = strict_json(lines[0], "analytic lift")
    require(manifest == {"attachments":
            "arbitrary finite rooted trees at branch or subdivision vertices", "budget": 6,
            "conclusion_if_premise_discharged": "s+(G)>=|V(G)|",
            "evidence_kind": "conditional-analytic-implication", "finite_premise":
            "every canonical-plus-coordinate key has an exact budget-six owner",
            "finite_premise_discharged": False, "global_claim": False,
            "kernel_orders": [2, 12], "length_lift":
            "fixed-parity coordinatewise path lengthening", "proof_sha256":
            DOCUMENT_PINS[STRUCTURAL_NOTE], "rank": 7,
            "schema": "rank-seven-conditional-analytic-lift-v1"},
            "analytic lift contract changed")
    # The order-nine master discharges only its bounded order-nine premise.  The
    # child remains globally conditional, so false/false above is required.
    return manifest


def hostile_self_checks() -> int:
    count = 0
    for raw, label in ((b'{"x":1,"x":2}\n', "duplicate JSON"),
                       (b'{"x":1.0}\n', "floating JSON")):
        try:
            strict_json(raw, label)
        except RuntimeError:
            count += 1
        else:
            fail(f"hostile mutation accepted: {label}")
    for value, label in ((True, "boolean integer"), (-1, "negative integer")):
        try:
            exact_int(value, label)
        except RuntimeError:
            count += 1
        else:
            fail(f"hostile mutation accepted: {label}")
    synthetic = {key: None for key in STRUCTURAL_FIELDS - {"chunks"}}
    try:
        validate_structural(synthetic, predicates=True, census=True)
    except RuntimeError:
        count += 1
    else:
        fail("hostile status-only structural payload accepted")
    changed = deepcopy(PARTITION_ORBITS)
    changed["gram"] -= 1
    try:
        validate_partition(changed, PARTITION_PHYSICAL)
    except RuntimeError:
        count += 1
    else:
        fail("hostile orbit gap accepted")
    bad_upstream = {"schema": "rank-seven-order-nine-upstream-owner-replay-v1"}
    try:
        validate_upstream(bad_upstream)
    except RuntimeError:
        count += 1
    else:
        fail("hostile partial upstream payload accepted")
    bad_cycle = {"third": {"record_total": 631}, "fourth": {"record_total": 1036}}
    try:
        validate_cycle(bad_cycle)
    except RuntimeError:
        count += 1
    else:
        fail("hostile partial cycle payload accepted")
    # Count-preserving swaps must fail even though the global sum is unchanged.
    swapped = deepcopy(PARTITION_ORBITS)
    swapped["structural"] -= 1
    swapped["sos"] += 1
    try:
        validate_partition(swapped, PARTITION_PHYSICAL)
    except RuntimeError:
        count += 1
    else:
        fail("hostile count-preserving residual-lane swap accepted")
    # Coarse omission cannot be laundered into the residual side.
    try:
        validate_target_accounting(COARSE_ORBITS - 1, RESIDUAL_ORBITS + 1)
    except RuntimeError:
        count += 1
    else:
        fail("hostile count-preserving coarse/residual swap accepted")
    semantic_mutations = (
        ("plus-ten", lambda contract: contract["different_color_scaled_cost"].__setitem__(
            "odd_positive", "18*m-10-13*o")),
        ("minus-thirteen-o", lambda contract: contract["different_color_scaled_cost"].__setitem__(
            "odd_positive", "18*m+10+13*o")),
        ("budget-180", lambda contract: contract.__setitem__("budget_scaled", 181)),
        ("same-color-positive-odd", lambda contract: contract.__setitem__(
            "same_color_legal_iff", "any o")),
        ("retained-Gram-downgrade", lambda contract: contract.__setitem__(
            "owner_semantics", "canonical target only")),
    )
    for label, mutate in semantic_mutations:
        hostile = deepcopy(COARSE_ATOM_CONTRACT)
        mutate(hostile)
        try:
            audit_coarse_source_contract(hostile)
        except RuntimeError:
            count += 1
        else:
            fail(f"hostile coarse semantic mutation accepted: {label}")
    producer_mutations = (
        ("producer-plus-ten", "- 10 * np.bitwise_count(support)",
         "+ 10 * np.bitwise_count(support)"),
        ("producer-minus-thirteen-o", "+ 13 * odd_sum", "- 13 * odd_sum"),
        ("producer-budget", "BUDGET_SCALED = 180", "BUDGET_SCALED = 181"),
    )
    original_producer = CENSUS_PRODUCER.read_text("ascii")
    for label, old, new in producer_mutations:
        hostile = original_producer.replace(old, new, 1)
        require(hostile != original_producer, f"hostile setup failed: {label}")
        try:
            audit_coarse_source_contract(producer_source=hostile)
        except RuntimeError:
            count += 1
        else:
            fail(f"hostile coarse producer mutation accepted: {label}")
    original_atom = COARSE_ATOM.read_text("ascii")
    hostile_atom = original_atom.replace("if odd:\n                return None",
                                         "if False:\n                return None", 1)
    require(hostile_atom != original_atom, "hostile atom setup failed")
    try:
        audit_coarse_source_contract(atom_source=hostile_atom)
    except RuntimeError:
        count += 1
    else:
        fail("hostile same-color positive-odd source mutation accepted")
    return count


def quick_manifest(dependencies: dict[str, str], analytic: dict[str, Json],
                   coarse_contract: dict[str, Json],
                   coarse_application: dict[str, Json],
                   coarse_atom: dict[str, Json],
                   target_accounting: dict[str, Json]) -> dict[str, Json]:
    return {"schema": SCHEMA, "evidence_kind": "fail-closed-authentication-only",
            "mode": "quick", "theorem_eligible": False, "global_claim": False,
            "reason": "quick mode does not execute the exact finite theorem partition",
            "dependency_sha256": dependencies, "analytic_contract": analytic,
            "coarse_atom_contract": coarse_contract,
            "coarse_atom_audit": coarse_atom,
            "stored_coarse_application_ledger": coarse_application,
            "target_accounting": target_accounting,
            "residual_partition_orbits": PARTITION_ORBITS,
            "residual_partition_physical": PARTITION_PHYSICAL,
            "full_requirements": ["fresh order-nine coarse/residual reconstruction",
                "fresh combined census and structural predicate replay",
                "exact scalar/typed-SOS and dominant Gram replay",
                "exact third/fourth Gram replay", "induced transfer gate",
                "obstruction branch-Gram gate"]}


def full_manifest(dependencies: dict[str, str], analytic: dict[str, Json],
                  coarse_contract: dict[str, Json], coarse_application: dict[str, Json],
                  coarse_atom: dict[str, Json], target_accounting: dict[str, Json],
                  structural: dict[str, Json], downstream: list[dict[str, Json]]) -> dict[str, Json]:
    return {"schema": SCHEMA, "evidence_kind": "current-process-exact-theorem-gate",
            "mode": "full", "theorem_eligible": True, "global_claim": False,
            "scope": {"kernel": "loopless 2-connected rank-seven multigraph of order nine",
                "realization": "finite simple positive-length subdivision; at most one unit path per parallel class",
                "block_scope": "exactly one positive-rank cyclic block",
                "attachments": "finite one-root/disjoint rooted trees at branch or subdivision vertices"},
            "conclusion": "s+(G)>=|V(G)|",
            "base_universe": {"kernel_total": 4495, "physical_rows": PARITY_PHYSICAL,
                "parity_orbits": PARITY_ORBITS, "coarse_owner_orbits": COARSE_ORBITS,
                "residual_orbits": RESIDUAL_ORBITS, "residual_physical": RESIDUAL_PHYSICAL},
            "coarse_atom_contract": coarse_contract,
            "coarse_atom_audit": coarse_atom,
            "fresh_coarse_application_ledger": coarse_application,
            "target_accounting": target_accounting,
            "precedence": ["structural", "sos", "dominant-gram", "third-cycle-gram",
                           "fourth-cycle-gram", "transfer", "obstruction"],
            "residual_partition_orbits": PARTITION_ORBITS,
            "residual_partition_physical": PARTITION_PHYSICAL,
            "structural_combined_replay": structural, "downstream_exact_replays": downstream,
            "dependency_sha256": dependencies, "analytic_contract": analytic,
            "analytic_dependency_sha256": {"structural_reduction": DOCUMENT_PINS[STRUCTURAL_NOTE],
                "coarse_tetrahedral_atom_note": DOCUMENT_PINS[COARSE_ATOM_NOTE],
                "induced_transfer_note": DOCUMENT_PINS[TRANSFER_NOTE],
                "obstruction_note": DOCUMENT_PINS[OBSTRUCTION_NOTE],
                "rank_two_theorem": DOCUMENT_PINS[BICYCLIC],
                "rank_three_theorem": DOCUMENT_PINS[TRICYCLIC],
                "rank_four_theorem": DOCUMENT_PINS[TETRACYCLIC]},
            "excluded_scope": ["kernel orders other than nine",
                "multiple positive-rank cyclic blocks", "non-simple or looped realizations",
                "STATE or project-global promotion"]}


def audit(full: bool) -> dict[str, Json]:
    validate_partition()
    target_accounting = validate_target_accounting()
    require(hostile_self_checks() == 19, "hostile self-check count changed")
    dependencies = audit_pins()
    require(audit_no_asserts() == len(PYTHON_PINS) + 1, "AST source count changed")
    analytic = validate_analytic_sources()
    coarse_contract = audit_coarse_source_contract()
    coarse_atom = run_coarse_atom()
    coarse_application = validate_coarse_application_chunks()
    if not full:
        return quick_manifest(dependencies, analytic, coarse_contract, coarse_application,
                              coarse_atom, target_accounting)
    structural = run_child("structural-combined", STRUCTURAL,
                           ("--full-rescan", "--reconstruct-census"), None,
                           lambda result: validate_structural(result, predicates=True, census=True))
    require(structural["result"]["combined_replay_eligible"] is True,
            "combined structural replay is ineligible")
    upstream = run_child("upstream-sos-dominant", UPSTREAM, (), UPSTREAM_OUTPUT_SHA256,
                         validate_upstream)
    cycle = run_cycle()
    transfer = run_child("induced-transfer", TRANSFER, (), TRANSFER_OUTPUT_SHA256,
                         validate_transfer,
                         "rank-seven order-nine induced-partition transfer verifier: PASS")
    obstruction = run_child("obstruction-branch-gram", OBSTRUCTION, (),
                            OBSTRUCTION_OUTPUT_SHA256, validate_obstruction,
                            "rank-seven order-nine obstruction branch-Gram verifier: PASS")
    require(structural["result"]["census_coarse_certified_total_reconstructed"] ==
            coarse_application["coarse_owner_orbits"] and
            structural["result"]["census_coarse_residual_total_reconstructed"] ==
            coarse_application["residual_orbits"] and
            structural["result"]["per_kernel_residual_ledgers_validated"] is True,
            "fresh census and independent coarse application ledgers disagree")
    coarse_application = {**coarse_application,
                          "fresh_producer_reconstruction_validated": True,
                          "producer_sha256": PYTHON_PINS[CENSUS_PRODUCER],
                          "source_engine_sha256": PYTHON_PINS[COARSE_ENGINE],
                          "fixture_sha256": DATA_PINS[KERNEL_FIXTURE]}
    return full_manifest(dependencies, analytic, coarse_contract, coarse_application,
                         coarse_atom, target_accounting, structural,
                         [upstream, cycle, transfer, obstruction])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--quick", action="store_true", help="authenticate only; never theorem-eligible")
    modes.add_argument("--full", action="store_true", help="run every exact theorem gate")
    parser.add_argument("--print-manifest", action="store_true")
    args = parser.parse_args(argv)
    try:
        manifest = audit(full=args.full)
    except (ImportError, KeyError, OSError, RuntimeError, TypeError, ValueError,
            UnicodeError, json.JSONDecodeError, lzma.LZMAError) as error:
        sys.stderr.write(f"rank-seven order-nine master: FAIL CLOSED: {error}\n")
        return 1
    if args.print_manifest:
        sys.stdout.buffer.write(canonical_bytes(manifest))
    if manifest["theorem_eligible"]:
        sys.stdout.write("rank-seven order-nine kernel theorem: exact full audit passed\n")
    else:
        sys.stdout.write("rank-seven order-nine master: quick authentication only; theorem blocked\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
