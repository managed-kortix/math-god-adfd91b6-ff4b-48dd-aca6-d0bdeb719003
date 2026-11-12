#!/usr/bin/env python3
"""Read-only trust-boundary replay for the rank-seven/order-nine owner streams.

``verify_stored_semantic_zip`` is the fast mode.  It authenticates every pinned
input and zips all 2,835,895 census rows to the eight classification streams and
their ordered remainder complements.  It validates row identity, order,
counts, physical mass, lanes, stored details, and all global digests.  It does
*not* call an ownership predicate and therefore is not a semantic owner replay.

``replay_all_predicates`` first performs that complete zip and then freshly
runs the precedence-ordered exact recognizer on every row.  In particular it
reruns ``generalized_three_ray_owner`` wherever the first three lanes fail;
the stored generalized-ray detail contains no state witness and is never used
as one.  This slow mode is the semantic owner replay intended for a master
gate.  Both modes are read-only, use exact integer/Fraction arithmetic through
the pinned existing engine, and fail closed.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import lzma
import sys
from collections import Counter
from pathlib import Path
from typing import Any, NoReturn

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CENSUS_PRODUCER = HERE / "rank7_orders9_12_exact_residual_census.py"
SOURCE_ENGINE = HERE / "rank7_parity_coarse_digest_census.py"
OWNER_ENGINE = HERE / "rank7_order12_structural_owners.py"
ATOM_RECOGNIZER = HERE / "rank7_order7_symbolic_atom_recognizer.py"
KERNEL_FIXTURE = ROOT / "research/fixtures/rank-seven-kernel-frontier-census.json"
CENSUS_MANIFEST = HERE / "rank7_order9_exact_residual_census_manifest.json"
OWNER_MANIFEST = HERE / "rank7_order9_structural_owner_manifest.json"
RESULTS = HERE / "rank7_order9_structural_owner_scheduler/results"

ORDER = 9
RANK = 7
PATH_COUNT = 15
FRONTIERS = 16
KERNEL_TOTAL = 4495
PARITY_ORBIT_TOTAL = 65_167_570
COARSE_CERTIFIED_TOTAL = 62_331_675
RESIDUAL_TOTAL = 2_835_895
RESIDUAL_PHYSICAL_TOTAL = 3_518_609
OWNER_TOTAL = 2_450_066
OWNER_PHYSICAL_TOTAL = 3_076_384
REMAINDER_TOTAL = 385_829
REMAINDER_PHYSICAL_TOTAL = 442_225
LANES = (
    "balanced-rank-one",
    "signed-imbalance-psd",
    "simplex-mixed-atom",
    "generalized-ray",
)
EXPECTED_OWNER_COUNTS = {
    "balanced-rank-one": 1513,
    "generalized-ray": 2_445_321,
    "signed-imbalance-psd": 2819,
    "simplex-mixed-atom": 413,
}
EXPECTED_OWNER_PHYSICAL = {
    "balanced-rank-one": 1593,
    "generalized-ray": 3_071_139,
    "signed-imbalance-psd": 3185,
    "simplex-mixed-atom": 467,
}
EXPECTED_PROFILES = {
    "mixed-0/simplex-4-4": 87,
    "mixed-0/simplex-5": 267,
    "mixed-3/simplex-4": 56,
    "mixed-6/simplex-none": 3,
}
PINS = {
    CENSUS_PRODUCER: "c6dcc792c7899c3f494a3beb521c94da972a01a392cd77be78b0956bbee3b921",
    SOURCE_ENGINE: "d285a1c29cace4cb30882662e786cf1e5086ebc579676a3aa114a18e2365b2a5",
    OWNER_ENGINE: "ffd76058b58344ea066777bdfd6d29eaed154c8d8d243d2c37ddf942f9558c45",
    ATOM_RECOGNIZER: "10de4fb714c15756341a7dbddb5a4da9f8ce5e0393aacc9e9434d619ebce9734",
    KERNEL_FIXTURE: "a241139ab54ce4cce1ab3812887359edb241c0abfb1018e804b4a5f86762cfd5",
    CENSUS_MANIFEST: "9ece0464ae31dbc6c2e5b715be054c7191bc5c12a0f6efaf008ac0e6641baf1f",
    OWNER_MANIFEST: "8097c55f455cf68e27e29b571ef5cd94e17057290d1f211fb3ecf81949f98366",
}
CHUNK_SPECS = (
    # census raw, census XZ, chunk report, classification raw, classification XZ,
    # remainder raw, remainder XZ
    ("2712d3b761b7518ee6481d767410408673da825c9a31ec17d5a17784926da812",
     "ececc24e071cc31b0678de01a1ffb0787f804354b00239f221006a9bffaccdc1",
     "ebc040006305390d28ae4f21b2072a66e2af8ef9cd7933d5e400dba6cc3ff47d",
     "55d425a40ff56de801564a9d602ad801b35ac9b3e0781b3c64cd5d2f0b5c47bf",
     "3291a0530787f18c7fb665df4b97ff0f7c61329113e93ae07ec1f7f8a8ef977e",
     "06caa86cb4dffa5b126348729afab7c01e7b6bc3068e252fc73dbb271d64c74f",
     "fa973b7a9702fef4ccbdefff5cf55dad910838f244ad46c72e97c51dfb134ff9"),
    ("6e4f63314b9f0dfb04fd9ecfd4b4c658fe306e31db6aaaa64b63e883afc099f0",
     "b49b1973f2d946e6c4b8a6ff295d0ce19c4d3c67cccb58014588a9edf12b7d7e",
     "6af96ac219d946e7bf631ccda7410bda3d2a8093711bdb1a43a0f87bd62e29dc",
     "94fbc591e59a43742c54aef1e694e2b213b90545f1f38f5700fe3922c2c2709e",
     "b0016a038f779f991b5487b340aa96d29804b6edb2a959dedbf65bfe21ea3904",
     "181151408ec32bac838dab03daf10689774db0cb9d7ab8c7540e78b7b48d3c9f",
     "41a43fbccc98dad484a3d73b569a6d8017b71b8577136c2dc0e6186fc5d6d723"),
    ("43c09e2ed2f38946e02efe095b7ff1621a48f98a1456ade7f8ebe19df51e3537",
     "5401fe71437f9f61cb3a6b09d480ac87dab2aab2f639dc954c1d3376ace2aad2",
     "7d109b0d4702e9f654ae9c4312136d88cd8b29aba8de7ad4f8b1d616a2aacb2b",
     "426f0d4db1b9e5bfed9dbdedfbb7e221102cb722b2dff9158307fb65a03b04f2",
     "3362ad6118b68c43ca291dbd98c24a5064a9a62de49e5854ac1f91454bc33f44",
     "8e5db504618536dffdc4e5a02b9073c8072e121118de1998ff13fa2e42f90c61",
     "86d301406134e1f56de677f41c0709c1ad708c9a001dbf03507efd55bf2d6210"),
    ("6159cf8336b5c88cdeba6ca08bfc101fbe4f9d6051a24ff88bd899304feaa60f",
     "197d33ce7afbddcd777e0f4c8af09a32ab4348d80c5d45ab061b24f0261da943",
     "d0cb1f8018cf646c17d322efa2a3b8fdfc9dad452a43d638e9d89aa7c8137374",
     "46b4acb4da1017413fc3d4b09fc4d32491b71f99817648bd5d612d440f8f8243",
     "66a2b59f136e1b8c7ab52ec0565955da1fad2983e281b4e9cbc489579d03bd02",
     "92b3cdeee21f08c0aeac5077d0e94c49ddb7193997b5e484bafbb0533c404b87",
     "ba116ca3d41239ea068b5b58cd111b9d44c10e19b832d03c380089117d084fc5"),
    ("8ae1b27ca907a081962626a43d0847f84a33a0f38d3e5cb605c741db029a1528",
     "8f172ae6231229769d6f4a6aa299207512d2347fc26a207fa15b708cc8c391db",
     "708c6b03c55c6e47545342746adf86bca91d416ed5ab75b0b576b057e55ecbb5",
     "e460fd14fc571d6468b5b9bc50f96a405e67dbc32f25bceefa2bcc2fc50a2a3a",
     "7d37c8ad2680646bdcafa2043cec860dd0b5355322f4c68e27d2fce5df971b4c",
     "d6babe283110b16697924f409a93d0b8abccdb1673b1e484910a70da9f72c1c2",
     "bd6ccb85269e743b635526d293d213d955d8a1765e95e49e1c137ce17d34e352"),
    ("d56e9117bb04e508177693f383aa31a3e3928254f544a4c4842e41c7a54ff94b",
     "4ce0e726bf6aaa32ae0167bb9bbc5b0c6ccb186cb6cc4092afe8c3634a0f1163",
     "6cf90f2086bb21cc8d59f73906dab8de53a33837a27f8fd88703cff4f5400985",
     "93ac72a3fb3347b4366d0f7702455e8584992877ef75c7f5f2246e0f3263c7f8",
     "84b001439c0758b8ea5bbd77e795acf2381727208d13c12a1a3b42a0f360fc0b",
     "1eefa52623aa5d40a353b88eadc54318e176f2e11c5aa5a59bbe02321c656f0c",
     "62f879bf8b289deb99d6df3745dd7c2d164a9aa441f4f89799c29221fb3011db"),
    ("6b9a46b712003412da9c53caa14dfdf80e14a95c152e1a1b215c87f420273842",
     "ca45002a215f82891a7d96c350a4b1b534174a3dfea8904dac6e4ce8baa5486d",
     "808e8c663a1d2568a1461d958908e43fd617fe00b1d5a22e6a3e4a4cf2632b6d",
     "2c65804fc70b6784b8279086ae0926535ec7c6cc036e7d83a5a25f845281a891",
     "0006b8da42d7de6b04b7d2b5821735aaaac2690bf7432419d13a0249e027af24",
     "a73a581e8565e7dcc0b4f8eaad0fdcf81b1fab31984e2dfc3948c1dd644747bb",
     "59a53ab0671664cafd43667587b3ef911c3056ca2dca799340fa7eca841df8f2"),
    ("e94b21dc4cc7e9dd0b88e3ca70f7a455cbc8373f3a0eb06c2f2ab7bbc0728392",
     "fe3912a744743d7d1c14ddfee8c0104dd34466d169f63abfc4b2550039c019ef",
     "1a70dd560c75f92460047c1af93b50832d9db17345118537ef207bff7a20df49",
     "9880385c8a2d8224e1d9baa4084b5f1baf18f0511601566d84815e376339807f",
     "4bd50cc03d1a04e0df576d9dba578cb048407ebbd98bcb34bba4751bb80ec666",
     "d0539aebac9c875c0b8d6d25cbef45ea8eb5f834ede8ba596fda38ab39694132",
     "8a5579f6b608b69e8223b6f24127e511614f9424141a12ec75198453b82c40f5"),
)
SCHEMA = "rank-seven-order-nine-structural-semantic-replay-v1"
Json = Any


def fail(message: str) -> NoReturn:
    raise RuntimeError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_bytes(value: Json) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")


def strict_json(raw: bytes, label: str, canonical: bool = True) -> Json:
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
        raise RuntimeError(f"{label}: invalid strict JSON") from error
    if canonical:
        require(raw == canonical_bytes(value), f"{label}: noncanonical JSON")
    return value


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_pinned(path: Path, expected: str) -> bytes:
    raw = path.read_bytes()
    require(sha256(raw) == expected, f"pinned bytes changed: {path.name}")
    return raw


def read_xz_json(path: Path, artifact_digest: str, raw_digest: str) -> dict[str, Json]:
    stored = read_pinned(path, artifact_digest)
    try:
        raw = lzma.decompress(stored, format=lzma.FORMAT_XZ)
    except lzma.LZMAError as error:
        raise RuntimeError(f"invalid XZ artifact: {path.name}") from error
    require(sha256(raw) == raw_digest, f"raw digest changed: {path.name}")
    value = strict_json(raw, path.name)
    require(type(value) is dict, f"{path.name}: top-level object required")
    return value


def read_jsonl_xz(path: Path, artifact_digest: str, raw_digest: str) -> list[Json]:
    stored = read_pinned(path, artifact_digest)
    try:
        raw = lzma.decompress(stored, format=lzma.FORMAT_XZ)
    except lzma.LZMAError as error:
        raise RuntimeError(f"invalid XZ artifact: {path.name}") from error
    require(sha256(raw) == raw_digest, f"raw digest changed: {path.name}")
    require(raw.endswith(b"\n"), f"{path.name}: missing final newline")
    rows = []
    for line_number, line in enumerate(raw.splitlines(keepends=True), 1):
        value = strict_json(line, f"{path.name}:{line_number}")
        require(type(value) is list, f"{path.name}:{line_number}: list required")
        rows.append(value)
    return rows


def audit_pins() -> None:
    for path, expected in PINS.items():
        read_pinned(path, expected)


def expected_detail(owner: Any, atom: Any, lane: str, edges: tuple[tuple[int, int, int], ...],
                    row: tuple[int, ...]) -> tuple[Json, bool]:
    """Replay one stored lane predicate and return canonical detail plus acceptance."""
    if lane == "balanced-rank-one":
        return None, owner.balanced_rank_one(edges, row)
    if lane == "signed-imbalance-psd":
        witness = owner.signed_imbalance_certificate(edges, row)
        return (None if witness is None else
                [witness[0], witness[1].numerator, witness[1].denominator]), witness is not None
    if lane == "simplex-mixed-atom":
        records = (() if not owner.atom_profile_candidate(edges, row) else
                   tuple(item for item in atom.recognize(edges, row)
                         if item["status"] == "exact-equality-owner"))
        profiles = sorted({
            (item["profile"]["mixed"], tuple(item["profile"]["simplex_widths"]))
            for item in records
        })
        return [[mixed, list(widths)] for mixed, widths in profiles], bool(records)
    require(lane == "generalized-ray", f"unknown lane: {lane}")
    # The stored detail has no states.  Acceptance comes only from a fresh
    # search; independently recompute and validate the returned exact witness.
    witness = owner.generalized_three_ray_witness(edges, row)
    accepted = (witness is not None and
                owner.three_ray_witness_cost(edges, row, witness) is not None and
                owner.three_ray_witness_cost(edges, row, witness) <= 18 * (RANK - 1))
    return ["signed-three-ray"], accepted


def _load_common() -> tuple[dict[str, Json], dict[str, Json]]:
    audit_pins()
    census_manifest = strict_json(read_pinned(CENSUS_MANIFEST, PINS[CENSUS_MANIFEST]),
                                  CENSUS_MANIFEST.name)
    owner_manifest = strict_json(read_pinned(OWNER_MANIFEST, PINS[OWNER_MANIFEST]),
                                 OWNER_MANIFEST.name)
    require(type(census_manifest) is dict and type(owner_manifest) is dict,
            "manifest top-level objects required")
    require(census_manifest.get("schema") ==
            "rank-seven-orders9-12-exact-residual-census-manifest-v1" and
            census_manifest.get("status") == "complete-exact-residual-orbit-decomposition" and
            census_manifest.get("full_theorem") is False and
            (census_manifest.get("rank"), census_manifest.get("order"),
             census_manifest.get("path_count"), census_manifest.get("frontiers_per_residual"),
             census_manifest.get("kernel_total")) ==
            (RANK, ORDER, PATH_COUNT, FRONTIERS, KERNEL_TOTAL),
            "census manifest scope changed")
    require(census_manifest.get("parity_orbit_total") == PARITY_ORBIT_TOTAL and
            census_manifest.get("coarse_certified_total") == COARSE_CERTIFIED_TOTAL and
            census_manifest.get("coarse_residual_total") == RESIDUAL_TOTAL and
            census_manifest.get("coarse_residual_physical_total") == RESIDUAL_PHYSICAL_TOTAL and
            PARITY_ORBIT_TOTAL == COARSE_CERTIFIED_TOTAL + RESIDUAL_TOTAL,
            "base census identity changed")
    require(owner_manifest.get("schema") ==
            "rank-seven-order-nine-structural-owner-coverage-v1" and
            owner_manifest.get("status") ==
            "complete-exact-streaming-payload-free-owner-scan" and
            owner_manifest.get("full_theorem") is False and
            (owner_manifest.get("rank"), owner_manifest.get("order"),
             owner_manifest.get("path_count"), owner_manifest.get("frontiers_per_residual")) ==
            (RANK, ORDER, PATH_COUNT, FRONTIERS),
            "owner manifest scope changed")
    require(owner_manifest.get("scanned_residual_total") == RESIDUAL_TOTAL and
            owner_manifest.get("exclusive_owner_orbit_counts") == EXPECTED_OWNER_COUNTS and
            owner_manifest.get("exclusive_owner_physical_counts") == EXPECTED_OWNER_PHYSICAL and
            owner_manifest.get("atom_profile_owner_counts") == EXPECTED_PROFILES and
            owner_manifest.get("payload_free_owned_orbit_total") == OWNER_TOTAL and
            owner_manifest.get("payload_free_owned_physical_total") == OWNER_PHYSICAL_TOTAL and
            owner_manifest.get("remainder_orbit_total") == REMAINDER_TOTAL and
            owner_manifest.get("remainder_physical_total") == REMAINDER_PHYSICAL_TOTAL,
            "owner manifest exact ledger changed")
    return census_manifest, owner_manifest


def _verify(*, replay_predicates: bool, progress: bool = False,
            chunk_limit: int | None = None) -> dict[str, Json]:
    census_manifest, owner_manifest = _load_common()
    census_records = census_manifest.get("chunks")
    owner_records = owner_manifest.get("chunks")
    require(type(census_records) is list and type(owner_records) is list and
            len(census_records) == len(owner_records) == len(CHUNK_SPECS),
            "eight-chunk ledger changed")
    require(chunk_limit is None or type(chunk_limit) is int and
            1 <= chunk_limit <= len(CHUNK_SPECS), "invalid test-only chunk limit")
    selected = len(CHUNK_SPECS) if chunk_limit is None else chunk_limit

    owner = atom = None
    if replay_predicates:
        owner = load_module(OWNER_ENGINE, "rank7_order9_semantic_owner")
        owner.ORDER = ORDER
        owner.RANK = RANK
        owner.PATH_COUNT = PATH_COUNT
        owner.TARGETS_PER_ROW = FRONTIERS
        owner.BUDGET = owner.F(RANK - 1)
        atom = load_module(ATOM_RECOGNIZER, "rank7_order9_semantic_atom")
        atom.ORDER = ORDER
        atom.PATH_COUNT = PATH_COUNT
        atom.BUDGET = RANK - 1

    counts = Counter({lane: 0 for lane in LANES})
    masses = Counter({lane: 0 for lane in LANES})
    profiles: Counter[str] = Counter()
    predicate_calls = Counter({lane: 0 for lane in LANES})
    predicate_passes = Counter({lane: 0 for lane in LANES})
    global_classification = hashlib.sha256()
    global_remainder = hashlib.sha256()
    source_cursor = 0
    remainder_count = remainder_mass = 0
    kernel_cursor = 0
    independent_totals = Counter()
    receipts = []

    for chunk_index in range(selected):
        pin = CHUNK_SPECS[chunk_index]
        census_spec = census_records[chunk_index]
        owner_spec = owner_records[chunk_index]
        require(type(census_spec) is dict and type(owner_spec) is dict,
                f"chunk {chunk_index}: malformed manifest ledger")
        start, stop = census_spec.get("kernel_range", [None, None])
        require(start == kernel_cursor and owner_spec.get("kernel_range") == [start, stop],
                f"chunk {chunk_index}: kernel ranges gap, overlap, or disagree")
        kernel_cursor = stop
        census_path = (HERE / census_spec.get("path", "")).resolve()
        require(census_path.parent == HERE.resolve(),
                f"chunk {chunk_index}: census path escapes experiment directory")
        report_path = RESULTS / f"chunk-{chunk_index:02d}.json"
        report_raw = read_pinned(report_path, pin[2])
        report = strict_json(report_raw, report_path.name)
        require(type(report) is dict and
                report.get("schema") == "rank-seven-order-nine-structural-owner-chunk-v1" and
                report.get("full_theorem") is False and
                report.get("chunk_index") == chunk_index and
                report.get("kernel_range") == [start, stop] and
                report.get("source_range") ==
                [source_cursor, source_cursor + census_spec.get("coarse_residual_total", -1)] and
                report.get("census_path") == census_path.name and
                report.get("census_artifact_sha256") == pin[1] and
                report.get("owner_engine_sha256") == PINS[OWNER_ENGINE] and
                report.get("atom_recognizer_sha256") == PINS[ATOM_RECOGNIZER] and
                report.get("manifest_sha256") == PINS[CENSUS_MANIFEST],
                f"chunk {chunk_index}: report identity changed")
        require(census_spec.get("raw_sha256") == pin[0] and
                census_spec.get("artifact_sha256") == pin[1] and
                owner_spec.get("artifact_sha256") == pin[1],
                f"chunk {chunk_index}: census digest ledgers disagree")
        census = read_xz_json(census_path, pin[1], pin[0])
        classification_path = RESULTS / f"chunk-{chunk_index:02d}.classification.jsonl.xz"
        remainder_path = RESULTS / f"chunk-{chunk_index:02d}.remainder.jsonl.xz"
        require(report.get("classification_stream") == {
                    "path": classification_path.name,
                    "sha256": pin[3], "artifact_sha256": pin[4]},
                f"chunk {chunk_index}: classification receipt changed")
        require(report.get("remainder_stream") == {
                    "path": remainder_path.name,
                    "sha256": pin[5], "artifact_sha256": pin[6]},
                f"chunk {chunk_index}: remainder receipt changed")
        classifications = read_jsonl_xz(classification_path, pin[4], pin[3])
        remainders = read_jsonl_xz(remainder_path, pin[6], pin[5])
        residuals = census.get("residuals")
        kernels_raw = census.get("kernels")
        require(type(residuals) is list and type(kernels_raw) is list,
                f"chunk {chunk_index}: census arrays malformed")
        require(len(residuals) == len(classifications) ==
                census_spec.get("coarse_residual_total") ==
                report.get("scanned_residual_total") == owner_spec.get("scanned_residual_total"),
                f"chunk {chunk_index}: row counts disagree")
        require(census.get("schema") ==
                "rank-seven-orders9-12-exact-residual-census-chunk-v1" and
                census.get("full_theorem") is False and
                census.get("status") == "complete-exact-residual-orbit-chunk" and
                (census.get("rank"), census.get("order"), census.get("path_count"),
                 census.get("frontiers_per_residual"), census.get("kernel_range")) ==
                (RANK, ORDER, PATH_COUNT, FRONTIERS, [start, stop]),
                f"chunk {chunk_index}: census scope changed")
        require(census.get("coarse_certified_total") + census.get("coarse_residual_total") ==
                census.get("parity_orbit_total"),
                f"chunk {chunk_index}: base partition identity changed")
        independent_totals.update({
            "kernel_total": census.get("kernel_total"),
            "physical_row_total": census.get("physical_row_total"),
            "parity_orbit_total": census.get("parity_orbit_total"),
            "coarse_certified_total": census.get("coarse_certified_total"),
            "coarse_residual_total": census.get("coarse_residual_total"),
            "coarse_residual_physical_total": census.get("coarse_residual_physical_total"),
            "frontier_target_total": census.get("frontier_target_total"),
        })
        kernels = {}
        previous_kernel = start
        for item in kernels_raw:
            require(type(item) is dict and type(item.get("order_kernel")) is int and
                    item["order_kernel"] not in kernels,
                    f"chunk {chunk_index}: malformed or duplicate kernel")
            edges_raw = item.get("edges")
            require(type(edges_raw) is list, f"chunk {chunk_index}: malformed edges")
            edges = tuple(tuple(edge) for edge in edges_raw)
            require(all(len(edge) == 3 and all(type(value) is int for value in edge) and
                        0 <= edge[0] < edge[1] < ORDER and edge[2] > 0 for edge in edges) and
                    sum(edge[2] for edge in edges) == PATH_COUNT,
                    f"chunk {chunk_index}: nonphysical kernel edges")
            kernels[item["order_kernel"]] = (item["global_kernel"], edges)
        require(len(kernels) == stop - start,
                f"chunk {chunk_index}: incomplete kernel ledger")

        local_counts = Counter({lane: 0 for lane in LANES})
        local_masses = Counter({lane: 0 for lane in LANES})
        local_profiles: Counter[str] = Counter()
        local_remainder_count = local_remainder_mass = 0
        remainder_iterator = iter(remainders)
        next_remainder = next(remainder_iterator, None)
        previous_key = None
        census_digest = hashlib.sha256()
        local_classification = hashlib.sha256()
        local_remainder = hashlib.sha256()

        for local_index, (residual, classification) in enumerate(
                zip(residuals, classifications, strict=True)):
            source_index = source_cursor + local_index
            require(type(residual) is dict and set(residual) == {
                        "global_kernel", "orbit_size", "order_kernel", "row"},
                    f"chunk {chunk_index} row {local_index}: residual fields changed")
            local_kernel = residual["order_kernel"]
            require(type(local_kernel) is int and local_kernel in kernels and
                    residual["global_kernel"] == kernels[local_kernel][0],
                    f"chunk {chunk_index} row {local_index}: bad kernel reference")
            edges = kernels[local_kernel][1]
            row_raw = residual["row"]
            orbit_size = residual["orbit_size"]
            require(type(row_raw) is list and len(row_raw) == len(edges) and
                    all(type(value) is int and 0 <= value <= edge[2]
                        for value, edge in zip(row_raw, edges, strict=True)) and
                    type(orbit_size) is int and orbit_size >= 1,
                    f"chunk {chunk_index} row {local_index}: nonphysical row")
            code = 0
            stride = 1
            for value, edge in zip(row_raw, edges, strict=True):
                code += value * stride
                stride *= edge[2] + 1
            key = (local_kernel, code)
            require(previous_key is None or previous_key < key,
                    f"chunk {chunk_index} row {local_index}: census order/uniqueness changed")
            previous_key = key
            census_digest.update(canonical_bytes(residual))
            expected_key = [source_index, residual["global_kernel"], local_kernel,
                            row_raw, orbit_size]
            require(type(classification) is list and len(classification) == 7 and
                    classification[:5] == expected_key,
                    f"chunk {chunk_index} row {local_index}: classification/census zip failed")
            lane, detail = classification[5:]
            require(lane is None or lane in LANES,
                    f"chunk {chunk_index} row {local_index}: unknown lane")
            encoded_classification = canonical_bytes(classification)
            local_classification.update(encoded_classification)
            global_classification.update(encoded_classification)
            if lane is None:
                require(detail is None and next_remainder == expected_key,
                        f"chunk {chunk_index} row {local_index}: ordered complement mismatch")
                encoded_remainder = canonical_bytes(next_remainder)
                local_remainder.update(encoded_remainder)
                global_remainder.update(encoded_remainder)
                next_remainder = next(remainder_iterator, None)
                local_remainder_count += 1
                local_remainder_mass += orbit_size
            else:
                local_counts[lane] += 1
                local_masses[lane] += orbit_size
                if lane == "balanced-rank-one":
                    require(detail is None,
                            f"chunk {chunk_index} row {local_index}: bad balanced detail")
                elif lane == "signed-imbalance-psd":
                    require(type(detail) is list and len(detail) == 3 and
                            all(type(value) is int for value in detail) and detail[0] > 0 and
                            detail[2] > 0,
                            f"chunk {chunk_index} row {local_index}: bad imbalance detail")
                elif lane == "simplex-mixed-atom":
                    require(type(detail) is list and detail,
                            f"chunk {chunk_index} row {local_index}: bad atom detail")
                    for mixed, widths in detail:
                        require(type(mixed) is int and type(widths) is list and
                                all(type(width) is int for width in widths),
                                f"chunk {chunk_index} row {local_index}: bad atom profile")
                        local_profiles[f"mixed-{mixed}/simplex-"
                                       f"{'-'.join(map(str, widths)) or 'none'}"] += 1
                else:
                    require(detail == ["signed-three-ray"],
                            f"chunk {chunk_index} row {local_index}: bad generalized detail")

            if replay_predicates:
                row = tuple(row_raw)
                observed_lane = None
                observed_detail: Json = None
                for candidate in LANES:
                    predicate_calls[candidate] += 1
                    candidate_detail, accepted = expected_detail(owner, atom, candidate,
                                                                 edges, row)
                    if accepted:
                        predicate_passes[candidate] += 1
                        observed_lane, observed_detail = candidate, candidate_detail
                        break
                require((observed_lane, observed_detail) == (lane, detail),
                        f"chunk {chunk_index} row {local_index}: fresh predicate replay differs")

        require(next_remainder is None,
                f"chunk {chunk_index}: remainder stream has trailing rows")
        require(census_digest.hexdigest() == census.get("residual_stream_sha256"),
                f"chunk {chunk_index}: census residual digest changed")
        require(local_classification.hexdigest() == pin[3] and
                local_remainder.hexdigest() == pin[5],
                f"chunk {chunk_index}: raw stream digest changed during zip")
        require(dict(local_counts) == report.get("exclusive_owner_orbit_counts") and
                dict(local_masses) == report.get("exclusive_owner_physical_counts") and
                dict(sorted(local_profiles.items())) == report.get("atom_profile_owner_counts") and
                local_remainder_count == report.get("remainder_orbit_total") and
                local_remainder_mass == report.get("remainder_physical_total"),
                f"chunk {chunk_index}: freshly counted report ledger differs")
        expected_owner_counts = {lane: value for lane, value in local_counts.items() if value}
        expected_owner_masses = {lane: value for lane, value in local_masses.items() if value}
        require(expected_owner_counts == owner_spec.get("exclusive_owner_orbit_counts") and
                expected_owner_masses == owner_spec.get("exclusive_owner_physical_counts") and
                local_remainder_count == owner_spec.get("remainder_orbit_total") and
                local_remainder_mass == owner_spec.get("remainder_physical_total"),
                f"chunk {chunk_index}: aggregate owner ledger differs")
        counts.update(local_counts)
        masses.update(local_masses)
        profiles.update(local_profiles)
        remainder_count += local_remainder_count
        remainder_mass += local_remainder_mass
        source_cursor += len(residuals)
        receipts.append({
            "chunk_index": chunk_index,
            "kernel_range": [start, stop],
            "source_range": report["source_range"],
            "rows": len(residuals),
            "classification_sha256": pin[3],
            "remainder_rows": local_remainder_count,
            "remainder_sha256": pin[5],
        })
        if progress:
            print(f"chunk={chunk_index} rows={source_cursor} generalized="
                  f"{counts['generalized-ray']} remainder={remainder_count}",
                  file=sys.stderr, flush=True)

    complete = selected == len(CHUNK_SPECS)
    if complete:
        require(kernel_cursor == KERNEL_TOTAL and source_cursor == RESIDUAL_TOTAL,
                "chunk union does not cover the residual universe")
        expected_totals = {
            "kernel_total": KERNEL_TOTAL,
            "physical_row_total": census_manifest["physical_row_total"],
            "parity_orbit_total": PARITY_ORBIT_TOTAL,
            "coarse_certified_total": COARSE_CERTIFIED_TOTAL,
            "coarse_residual_total": RESIDUAL_TOTAL,
            "coarse_residual_physical_total": RESIDUAL_PHYSICAL_TOTAL,
            "frontier_target_total": RESIDUAL_TOTAL * FRONTIERS,
        }
        require(dict(independent_totals) == expected_totals,
                "independent chunk totals differ from the census manifest")
        require(PARITY_ORBIT_TOTAL == COARSE_CERTIFIED_TOTAL + source_cursor,
                "fresh base identity failed")
        require(dict(counts) == EXPECTED_OWNER_COUNTS and
                dict(masses) == EXPECTED_OWNER_PHYSICAL and
                dict(sorted(profiles.items())) == EXPECTED_PROFILES and
                sum(counts.values()) == OWNER_TOTAL and
                sum(masses.values()) == OWNER_PHYSICAL_TOTAL and
                source_cursor == OWNER_TOTAL + remainder_count and
                RESIDUAL_PHYSICAL_TOTAL == OWNER_PHYSICAL_TOTAL + remainder_mass,
                "fresh ownership/complement accounting differs")
        require(global_classification.hexdigest() ==
                owner_manifest["classification_stream_sha256"] and
                global_remainder.hexdigest() == owner_manifest["remainder_stream_sha256"],
                "global stream digests differ")
        if replay_predicates:
            # A None classification means every predicate failed; accepted lanes
            # alone therefore sum to OWNER_TOTAL, not the full residual universe.
            require(dict(predicate_passes) == EXPECTED_OWNER_COUNTS,
                    "fresh predicate pass ledger differs")
            require(predicate_calls["balanced-rank-one"] == RESIDUAL_TOTAL and
                    predicate_calls["generalized-ray"] ==
                    EXPECTED_OWNER_COUNTS["generalized-ray"] + REMAINDER_TOTAL,
                    "fresh predicate call ledger differs")

    mode = "fresh-full-predicate-replay" if replay_predicates else "authenticated-stored-stream-zip"
    return {
        "schema": SCHEMA,
        "status": "passed",
        "mode": mode,
        "full_theorem": False,
        "read_only": True,
        "writes": 0,
        "complete": complete,
        "trust_boundary": (
            "all stored census/classification/remainder rows are authenticated and zipped; "
            "ownership predicates are not called in this mode"
            if not replay_predicates else
            "all stored rows are authenticated and zipped, then every precedence-ordered exact "
            "ownership predicate is freshly replayed; stored generalized detail is not a witness"
        ),
        "base_identity": {
            "kernel_total": (KERNEL_TOTAL if complete else independent_totals["kernel_total"]),
            "physical_row_total": independent_totals["physical_row_total"],
            "parity_orbit_total": (PARITY_ORBIT_TOTAL if complete else
                                   independent_totals["parity_orbit_total"]),
            "coarse_certified_total": (COARSE_CERTIFIED_TOTAL if complete else
                                       independent_totals["coarse_certified_total"]),
            "coarse_residual_total": source_cursor,
            "coarse_residual_physical_total":
                independent_totals["coarse_residual_physical_total"],
            "frontier_target_total": independent_totals["frontier_target_total"],
            "identity_validated": complete,
        },
        "chunk_total": selected,
        "row_zip_total": source_cursor,
        "classification_rows": source_cursor,
        "classification_stream_sha256": global_classification.hexdigest(),
        "exclusive_owner_orbit_counts": dict(counts),
        "exclusive_owner_physical_counts": dict(masses),
        "owner_orbit_total": sum(counts.values()),
        "owner_physical_total": sum(masses.values()),
        "remainder_orbit_total": remainder_count,
        "remainder_physical_total": remainder_mass,
        "remainder_stream_sha256": global_remainder.hexdigest(),
        "ordered_complement_validated": True,
        "recognition_calls": source_cursor if replay_predicates else 0,
        "predicate_calls": dict(predicate_calls),
        "predicate_passes": dict(predicate_passes),
        "generalized_three_ray_calls": predicate_calls["generalized-ray"],
        "generalized_three_ray_passes": predicate_passes["generalized-ray"],
        "stored_generalized_witnesses": 0,
        "chunks": receipts,
    }


def verify_stored_semantic_zip(*, progress: bool = False,
                               _chunk_limit: int | None = None) -> dict[str, Json]:
    """Authenticate and zip every stored row without claiming predicate replay."""
    return _verify(replay_predicates=False, progress=progress, chunk_limit=_chunk_limit)


def replay_all_predicates(*, progress: bool = False,
                          _chunk_limit: int | None = None) -> dict[str, Json]:
    """Run the full read-only semantic replay, including fresh ray searches."""
    return _verify(replay_predicates=True, progress=progress, chunk_limit=_chunk_limit)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full-rescan", action="store_true",
                        help="freshly rerun every precedence-ordered ownership predicate")
    parser.add_argument("--progress", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = (replay_all_predicates(progress=args.progress) if args.full_rescan else
                  verify_stored_semantic_zip(progress=args.progress))
        sys.stdout.buffer.write(canonical_bytes(result))
        return 0
    except (KeyError, OSError, RuntimeError, TypeError, ValueError,
            UnicodeError, lzma.LZMAError) as error:
        sys.stderr.write(f"rank-seven order-nine structural replay: FAIL CLOSED: {error}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
