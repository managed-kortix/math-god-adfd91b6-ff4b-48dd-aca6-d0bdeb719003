#!/usr/bin/env python3
"""Read-only trust-boundary replay for the rank-seven/order-nine owner streams.

``verify_stored_semantic_zip`` is the fast mode.  It authenticates every pinned
input and zips all 2,835,895 census rows to the eight classification streams and
their ordered remainder complements.  It validates row identity, order,
counts, physical mass, lanes, stored details, and all global digests.  It does
*not* call an ownership predicate and therefore is not a semantic owner replay.
``reconstruct_census`` additionally invokes the pinned exact producer once per
chunk and requires each fresh canonical payload to equal the stored census.

``replay_all_predicates`` performs that complete zip while freshly running the
precedence-ordered exact recognizer on every row.  Wherever the first three
lanes fail, it calls ``generalized_three_ray_witness`` and exactly replays the
returned witness cost with ``three_ray_witness_cost``; the stored generalized
ray detail contains no state witness and is never used as one.  This slow mode
is the semantic owner replay intended for a master gate.  Both modes are
read-only, use exact integer/Fraction arithmetic through the pinned existing
engine, and fail closed.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import lzma
import math
import os
import stat
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Callable, NoReturn

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
PARTITION_STREAM_SCHEMA = "rank-seven-order-nine-structural-partition-stream-v1"
PARTITION_STREAM_HEADER = b"R7O9-STRUCTURAL-PARTITION-V1\n"
PARTITION_STREAM_TRAILER = b"\nEND-R7O9-STRUCTURAL-PARTITION-V1\n"
PARTITION_TAG_OWNER = ord("O")
PARTITION_TAG_REMAINDER = ord("R")
PARTITION_STREAM_BYTE_TOTAL = (len(PARTITION_STREAM_HEADER) + RESIDUAL_TOTAL +
                               len(PARTITION_STREAM_TRAILER))
PARTITION_STREAM_MANIFEST_FIELDS = {
    "schema", "replay_schema", "mode", "source_sha256", "producer_sha256",
    "source_engine_sha256", "owner_engine_sha256", "atom_recognizer_sha256",
    "record_total", "stream_byte_total", "stream_sha256", "owner_orbit_total",
    "owner_physical_total", "owner_source_index_sha256", "owner_key_sha256",
    "remainder_orbit_total", "remainder_physical_total",
    "remainder_source_index_sha256", "remainder_key_sha256", "replay",
    "replay_sha256",
}
Json = Any
KeySink = Callable[[str, tuple[int, int, int, tuple[int, ...], int]], None]

CENSUS_MANIFEST_FIELDS = {
    "budget", "chunks", "coarse_certified_total", "coarse_residual_physical_total",
    "coarse_residual_total", "frontier_target_total", "frontiers_per_residual",
    "full_theorem", "kernel_total", "order", "parity_orbit_total", "path_count",
    "physical_row_total", "rank", "schema", "source_sha256", "status",
}
CENSUS_MANIFEST_CHUNK_FIELDS = {
    "artifact_sha256", "coarse_residual_total", "kernel_range", "path", "raw_sha256",
}
OWNER_MANIFEST_FIELDS = {
    "atom_profile_owner_counts", "atom_recognizer_sha256", "chunks",
    "classification_stream_sha256", "exclusive_owner_orbit_counts",
    "exclusive_owner_physical_counts", "frontiers_per_residual", "full_theorem",
    "manifest_sha256", "order", "owner_engine_sha256", "path_count",
    "payload_free_owned_orbit_total", "payload_free_owned_physical_total",
    "payload_free_owned_target_total", "rank", "remainder_orbit_total",
    "remainder_physical_total", "remainder_stream_sha256", "remainder_target_total",
    "scanned_residual_total", "scanned_target_total", "schema", "scope", "status",
}
OWNER_MANIFEST_CHUNK_FIELDS = {
    "artifact_sha256", "exclusive_owner_orbit_counts", "exclusive_owner_physical_counts",
    "kernel_range", "path", "remainder_orbit_total", "remainder_physical_total",
    "scanned_residual_total",
}
CHUNK_REPORT_FIELDS = {
    "atom_profile_owner_counts", "atom_recognizer_sha256", "census_artifact_sha256",
    "census_path", "chunk_index", "classification_stream",
    "exclusive_owner_orbit_counts", "exclusive_owner_physical_counts", "full_theorem",
    "kernel_range", "manifest_sha256", "owner_engine_sha256", "remainder_orbit_total",
    "remainder_physical_total", "remainder_stream", "scanned_residual_total", "schema",
    "source_range",
}
STREAM_RECEIPT_FIELDS = {"artifact_sha256", "path", "sha256"}
CENSUS_CHUNK_FIELDS = {
    "budget", "coarse_certified_total", "coarse_residual_physical_total",
    "coarse_residual_total", "frontier_target_total", "frontiers_per_residual",
    "full_theorem", "kernel_range", "kernel_total", "kernels", "order",
    "parity_orbit_total", "path_count", "physical_row_total", "rank",
    "residual_stream_sha256", "residuals", "schema", "source_sha256", "status",
}
KERNEL_FIELDS = {
    "automorphisms", "coarse_certified_orbits", "coarse_residual_orbits",
    "coarse_residual_physical_rows", "edges", "global_kernel", "order_kernel",
    "parity_orbits", "physical_rows", "support_edges",
}
RESIDUAL_FIELDS = {"global_kernel", "orbit_size", "order_kernel", "row"}
FIXTURE_FIELDS = {
    "beta", "counts_by_order_n2_to_n12", "degree_multiset_counts", "encoding",
    "generator", "kernels", "minimum_degree", "orders", "schema", "status",
    "support_edge_counts",
}
FIXTURE_KERNEL_FIELDS = {"code", "n"}
EXPECTED_PREDICATE_CALLS = {
    "balanced-rank-one": RESIDUAL_TOTAL,
    "signed-imbalance-psd": RESIDUAL_TOTAL - EXPECTED_OWNER_COUNTS["balanced-rank-one"],
    "simplex-mixed-atom": (RESIDUAL_TOTAL - EXPECTED_OWNER_COUNTS["balanced-rank-one"] -
                           EXPECTED_OWNER_COUNTS["signed-imbalance-psd"]),
    "generalized-ray": EXPECTED_OWNER_COUNTS["generalized-ray"] + REMAINDER_TOTAL,
}
EXPECTED_PREDICATE_CALL_TOTAL = sum(EXPECTED_PREDICATE_CALLS.values())
CENSUS_TOTAL_FIELDS = (
    "kernel_total",
    "physical_row_total",
    "parity_orbit_total",
    "coarse_certified_total",
    "coarse_residual_total",
    "coarse_residual_physical_total",
    "frontier_target_total",
)

# Canonical identity streams are part of the replay contract, not dynamically
# trusted receipts.  Their encodings are documented in the returned result.
EXPECTED_SOURCE_IDENTITY = {
    "universe_source_index_sha256":
        "e3d0066cdcb88cec40ce67e50f1252064f8532a876b17d88ee9f5a283146c86a",
    "universe_key_sha256":
        "cf1ff383eaf48c64d02cf106a6a5c7cd8420fbed3f68194962ef335c8adc12c4",
    "owner_source_index_sha256":
        "42380a735ddd66e819adf1c58bb19c039fdc6033bae80172903a49fba0ee12be",
    "owner_key_sha256":
        "48b5094918a3e921167ed4f3bc2397edb8c003a410262151752569f78ca4b8e2",
    "remainder_source_index_sha256":
        "7d87a4a548a0d613f39ebf657e350ab7a8a6c22e055d20b0d959bd27441a322a",
    "remainder_key_sha256":
        "0442d023ca3401f692fcb7866129ad83758753027dcac373a16da3b170c53a3e",
}


def fail(message: str) -> NoReturn:
    raise RuntimeError(message)


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        fail(message)


def exact_int(value: Json, label: str, *, minimum: int | None = None) -> int:
    """Return an exact JSON integer, rejecting bool and numeric lookalikes."""
    require(type(value) is int, f"{label}: exact integer required")
    if minimum is not None:
        require(value >= minimum, f"{label}: integer below minimum {minimum}")
    return value


def exact_str(value: Json, label: str) -> str:
    require(type(value) is str, f"{label}: exact string required")
    return value


def exact_bool(value: Json, label: str) -> bool:
    require(type(value) is bool, f"{label}: exact boolean required")
    return value


def exact_int_list(value: Json, length: int, label: str,
                   *, minimum: int | None = None) -> list[int]:
    require(type(value) is list and len(value) == length,
            f"{label}: exact integer list required")
    for index, item in enumerate(value):
        exact_int(item, f"{label}[{index}]", minimum=minimum)
    return value


def exact_str_int_map(value: Json, keys: set[str] | None, label: str,
                      *, minimum: int = 0, allow_sparse: bool = False) -> dict[str, int]:
    require(type(value) is dict and all(type(key) is str for key in value),
            f"{label}: exact string-keyed counter required")
    if keys is not None:
        require(set(value).issubset(keys) if allow_sparse else set(value) == keys,
                f"{label}: exact counter keys required")
    for key, item in value.items():
        exact_int(item, f"{label}.{key}", minimum=minimum)
    return value


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_bytes(value: Json) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")


def strict_json(raw: bytes, label: str, canonical: bool = True) -> Json:
    """Parse canonical, duplicate-free, integer-only JSON.

    ``parse_float`` rejects the token before Python can round it or turn an
    overflowing exponent such as ``1e999`` into infinity.  The recursive walk
    is a second, parser-independent guard against every float entering a trust
    boundary (including values supplied by a monkey-patched decoder in tests).
    Booleans remain legal JSON scalars and are validated field-by-field.
    """
    def pairs(items: list[tuple[str, Json]]) -> dict[str, Json]:
        result: dict[str, Json] = {}
        for key, value in items:
            require(type(key) is str and key not in result,
                    f"{label}: duplicate or non-string key")
            result[key] = value
        return result

    def reject_float(token: str) -> NoReturn:
        fail(f"{label}: JSON floats are forbidden: {token}")

    def reject_constant(token: str) -> NoReturn:
        fail(f"{label}: nonstandard JSON constant: {token}")

    def validate_json_types(value: Json) -> None:
        require(type(value) in (dict, list, str, int, bool, type(None)),
                f"{label}: non-JSON value reached trust boundary")
        if type(value) is list:
            for item in value:
                validate_json_types(item)
        elif type(value) is dict:
            for item in value.values():
                validate_json_types(item)

    try:
        value = json.loads(
            raw.decode("ascii"), object_pairs_hook=pairs,
            parse_float=reject_float, parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"{label}: invalid strict JSON") from error
    validate_json_types(value)
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


def exact_fields(value: Json, fields: set[str], label: str) -> None:
    require(type(value) is dict and set(value) == fields, f"{label}: exact schema changed")


def update_index_digest(digest: Any, source_index: int) -> None:
    digest.update(f"{source_index}\n".encode("ascii"))


def update_key_digest(digest: Any, key: tuple[int, int, int, tuple[int, ...], int]) -> None:
    source_index, global_kernel, order_kernel, row, orbit_size = key
    digest.update(canonical_bytes(
        [source_index, global_kernel, order_kernel, list(row), orbit_size]))


class PartitionTagFileSink:
    """Write the exact O/R tag stream to a new private regular file.

    The stream has a fixed ASCII header, exactly one byte for each canonical
    source index in order, and a fixed ASCII trailer.  Full row keys never cross
    this transport boundary; the parent must independently zip the tags with an
    authenticated canonical-key source before it can use them.
    """

    def __init__(self, path: Path, label: str):
        self.path = path
        self.label = label
        self.digest = hashlib.sha256()
        self.byte_total = 0
        self.record_total = 0
        self.owner_orbit_total = 0
        self.owner_physical_total = 0
        self.owner_index_digest = hashlib.sha256()
        self.owner_key_digest = hashlib.sha256()
        self.remainder_orbit_total = 0
        self.remainder_physical_total = 0
        self.remainder_index_digest = hashlib.sha256()
        self.remainder_key_digest = hashlib.sha256()
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        flags |= getattr(os, "O_NOFOLLOW", 0)
        self.fd = os.open(path, flags, 0o600)
        metadata = os.fstat(self.fd)
        require(stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1 and
                stat.S_IMODE(metadata.st_mode) == 0o600,
                f"{label}: sink is not a private regular file")
        self._write(PARTITION_STREAM_HEADER)

    def _write(self, raw: bytes) -> None:
        require(type(raw) is bytes and bool(raw), f"{self.label}: invalid sink bytes")
        view = memoryview(raw)
        while view:
            written = os.write(self.fd, view)
            require(type(written) is int and written > 0,
                    f"{self.label}: short sink write")
            view = view[written:]
        self.digest.update(raw)
        self.byte_total += len(raw)

    def write_partition(self, partition: str,
                        key: tuple[int, int, int, tuple[int, ...], int]) -> None:
        source_index, global_kernel, order_kernel, row, orbit_size = key
        require(source_index == self.record_total and
                type(global_kernel) is int and global_kernel >= 1 and
                type(order_kernel) is int and order_kernel >= 1 and
                type(row) is tuple and bool(row) and
                all(type(value) is int and value >= 0 for value in row) and
                type(orbit_size) is int and orbit_size >= 1,
                f"{self.label}: malformed or nonconsecutive canonical key")
        if partition == "owner":
            tag = PARTITION_TAG_OWNER
            self.owner_orbit_total += 1
            self.owner_physical_total += orbit_size
            update_index_digest(self.owner_index_digest, source_index)
            update_key_digest(self.owner_key_digest, key)
        elif partition == "remainder":
            tag = PARTITION_TAG_REMAINDER
            self.remainder_orbit_total += 1
            self.remainder_physical_total += orbit_size
            update_index_digest(self.remainder_index_digest, source_index)
            update_key_digest(self.remainder_key_digest, key)
        else:
            fail(f"{self.label}: unknown key partition")
        self._write(bytes((tag,)))
        self.record_total += 1

    def close(self) -> dict[str, Json]:
        require(self.fd >= 0 and self.record_total == RESIDUAL_TOTAL,
                f"{self.label}: incomplete partition stream")
        self._write(PARTITION_STREAM_TRAILER)
        require(self.byte_total == PARTITION_STREAM_BYTE_TOTAL,
                f"{self.label}: partition stream framing changed")
        os.fsync(self.fd)
        metadata = os.fstat(self.fd)
        require(stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1 and
                stat.S_IMODE(metadata.st_mode) == 0o600 and
                metadata.st_size == self.byte_total,
                f"{self.label}: sink file changed before close")
        path_metadata = os.lstat(self.path)
        require(stat.S_ISREG(path_metadata.st_mode) and path_metadata.st_nlink == 1 and
                stat.S_IMODE(path_metadata.st_mode) == 0o600 and
                (path_metadata.st_dev, path_metadata.st_ino) ==
                (metadata.st_dev, metadata.st_ino),
                f"{self.label}: sink path was replaced")
        os.close(self.fd)
        self.fd = -1
        return {
            "record_total": self.record_total,
            "stream_byte_total": self.byte_total,
            "stream_sha256": self.digest.hexdigest(),
            "owner_orbit_total": self.owner_orbit_total,
            "owner_physical_total": self.owner_physical_total,
            "owner_source_index_sha256": self.owner_index_digest.hexdigest(),
            "owner_key_sha256": self.owner_key_digest.hexdigest(),
            "remainder_orbit_total": self.remainder_orbit_total,
            "remainder_physical_total": self.remainder_physical_total,
            "remainder_source_index_sha256": self.remainder_index_digest.hexdigest(),
            "remainder_key_sha256": self.remainder_key_digest.hexdigest(),
        }

    def abort(self) -> None:
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1
        try:
            metadata = os.lstat(self.path)
            if stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1:
                self.path.unlink()
        except FileNotFoundError:
            pass


def validate_sink_path(raw_path: str, label: str) -> Path:
    """Require a resolved new basename directly inside a private directory."""
    require(type(raw_path) is str and bool(raw_path), f"{label}: output path required")
    path = Path(raw_path)
    require(path.is_absolute() and path == path.resolve(strict=False),
            f"{label}: output path must be absolute and resolved")
    parent = path.parent
    parent_metadata = os.lstat(parent)
    require(stat.S_ISDIR(parent_metadata.st_mode) and
            stat.S_IMODE(parent_metadata.st_mode) == 0o700 and
            path.name not in ("", ".", "..") and not path.exists() and
            not path.is_symlink(),
            f"{label}: output parent/path is not a new private sink")
    return path


def emit_combined_partition_stream(output_path: str) -> dict[str, Json]:
    """Run the combined replay and emit one fixed-framing O/R tag stream."""
    output = validate_sink_path(output_path, "partition sink")
    sink = PartitionTagFileSink(output, "partition sink")
    try:
        replay = _verify(
            replay_predicates=True, reconstruct_census=True, progress=False,
            key_sink=sink.write_partition)
        require(replay["combined_replay_eligible"] is True and
                replay["complete"] is True and
                replay["row_zip_total"] == RESIDUAL_TOTAL,
                "combined replay did not become eligible")
        receipt = sink.close()
        require(receipt == {
            "record_total": RESIDUAL_TOTAL,
            "stream_byte_total": PARTITION_STREAM_BYTE_TOTAL,
            "stream_sha256": receipt["stream_sha256"],
            "owner_orbit_total": OWNER_TOTAL,
            "owner_physical_total": OWNER_PHYSICAL_TOTAL,
            "owner_source_index_sha256":
                EXPECTED_SOURCE_IDENTITY["owner_source_index_sha256"],
            "owner_key_sha256": EXPECTED_SOURCE_IDENTITY["owner_key_sha256"],
            "remainder_orbit_total": REMAINDER_TOTAL,
            "remainder_physical_total": REMAINDER_PHYSICAL_TOTAL,
            "remainder_source_index_sha256":
                EXPECTED_SOURCE_IDENTITY["remainder_source_index_sha256"],
            "remainder_key_sha256": EXPECTED_SOURCE_IDENTITY["remainder_key_sha256"],
        }, "partition stream ledger changed")
        manifest = {
            "schema": PARTITION_STREAM_SCHEMA,
            "replay_schema": SCHEMA,
            "mode": "fresh-census-plus-fresh-full-predicate-replay",
            "source_sha256": PINS[KERNEL_FIXTURE],
            "producer_sha256": PINS[CENSUS_PRODUCER],
            "source_engine_sha256": PINS[SOURCE_ENGINE],
            "owner_engine_sha256": PINS[OWNER_ENGINE],
            "atom_recognizer_sha256": PINS[ATOM_RECOGNIZER],
            **receipt,
            "replay": replay,
            "replay_sha256": sha256(canonical_bytes(replay)),
        }
        exact_fields(manifest, PARTITION_STREAM_MANIFEST_FIELDS,
                     "partition stream manifest")
        return manifest
    except BaseException:
        sink.abort()
        try:
            output.unlink()
        except FileNotFoundError:
            pass
        raise



def automorphism_actions(edges: tuple[tuple[int, int, int], ...]) -> tuple[tuple[int, ...], ...]:
    """Derive exact sparse-edge actions from weighted-graph automorphisms.

    Vertex candidates are partitioned by their weighted degree and sorted
    incident-multiplicity signature.  Exhausting permutations inside these
    invariant cells is complete, while avoiding any optional graph package.
    """
    matrix = [[0] * ORDER for _ in range(ORDER)]
    degree = [0] * ORDER
    for u, v, multiplicity in edges:
        matrix[u][v] = matrix[v][u] = multiplicity
        degree[u] += multiplicity
        degree[v] += multiplicity
    signatures = tuple((degree[vertex], tuple(sorted(matrix[vertex])))
                       for vertex in range(ORDER))
    cells = tuple(tuple(vertex for vertex, value in enumerate(signatures) if value == signature)
                  for signature in sorted(set(signatures)))
    sparse_index = {(u, v): index for index, (u, v, _) in enumerate(edges)}
    actions = []
    for images in itertools.product(*(itertools.permutations(cell) for cell in cells)):
        permutation = list(range(ORDER))
        for cell, image in zip(cells, images, strict=True):
            for source, target in zip(cell, image, strict=True):
                permutation[source] = target
        if all(matrix[u][v] == matrix[permutation[u]][permutation[v]]
               for u in range(ORDER) for v in range(u + 1, ORDER)):
            actions.append(tuple(sparse_index[tuple(sorted((permutation[u], permutation[v])))]
                                 for u, v, _ in edges))
    require(bool(actions) and len(set(actions)) == len(actions),
            "automorphism action derivation failed")
    return tuple(sorted(actions))


def action_cycles(action: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    unseen = set(range(len(action)))
    cycles = []
    while unseen:
        value = min(unseen)
        cycle = []
        while value in unseen:
            unseen.remove(value)
            cycle.append(value)
            value = action[value]
        cycles.append(tuple(cycle))
    return tuple(cycles)


def burnside_orbits(edges: tuple[tuple[int, int, int], ...],
                    actions: tuple[tuple[int, ...], ...]) -> int:
    fixed_sum = 0
    for action in actions:
        fixed = 1
        for cycle in action_cycles(action):
            multiplicities = {edges[index][2] for index in cycle}
            require(len(multiplicities) == 1,
                    "automorphism action changes edge multiplicity")
            fixed *= multiplicities.pop() + 1
        fixed_sum += fixed
    require(fixed_sum % len(actions) == 0, "nonintegral Burnside orbit count")
    return fixed_sum // len(actions)


def recompute_orbit(row: tuple[int, ...], edges: tuple[tuple[int, int, int], ...],
                    actions: tuple[tuple[int, ...], ...]) -> tuple[int, int]:
    """Return the minimum mixed-radix image code and exact orbit size."""
    strides = []
    stride = 1
    for _, _, multiplicity in edges:
        strides.append(stride)
        stride *= multiplicity + 1
    image_codes = {
        sum(row[image] * strides[index] for index, image in enumerate(action))
        for action in actions
    }
    stabilizer = sum(all(row[index] == row[image]
                         for index, image in enumerate(action))
                     for action in actions)
    require(stabilizer > 0 and len(actions) % stabilizer == 0 and
            len(image_codes) == len(actions) // stabilizer,
            "orbit image/stabilizer identity failed")
    return min(image_codes), len(image_codes)


def empty_census_reconstruction_ledger() -> dict[str, Json]:
    """Create an execution ledger; no requested count is pre-populated."""
    return {
        "producer_loads": 0,
        "generate_chunk_calls": 0,
        "chunks_reconstructed": 0,
        "kernels_reconstructed": 0,
        "residual_rows_reconstructed": 0,
        "totals": {key: 0 for key in CENSUS_TOTAL_FIELDS},
        "raw_chunk_sha256": [],
    }


def record_census_reconstruction(ledger: dict[str, Json], regenerated: Json,
                                 stored: dict[str, Json], expected_raw_sha256: str,
                                 label: str) -> None:
    """Validate one actual producer return before recording any success counters."""
    require(type(regenerated) is dict, f"{label}: producer did not return an object")
    raw = canonical_bytes(regenerated)
    require(sha256(raw) == expected_raw_sha256,
            f"{label}: reconstructed canonical raw digest differs")
    require(raw == canonical_bytes(stored),
            f"{label}: fresh census reconstruction differs")
    exact_fields(regenerated, CENSUS_CHUNK_FIELDS, f"{label} regenerated census")
    kernels = regenerated["kernels"]
    residuals = regenerated["residuals"]
    require(type(kernels) is list and type(residuals) is list,
            f"{label}: regenerated arrays malformed")
    for key in CENSUS_TOTAL_FIELDS:
        exact_int(regenerated[key], f"{label} regenerated.{key}", minimum=0)
    require(regenerated["kernel_total"] == len(kernels) and
            regenerated["coarse_residual_total"] == len(residuals),
            f"{label}: regenerated materialization counts differ")

    # These increments occur only after generate_chunk returned exact canonical
    # content.  They are therefore execution-derived, never request-derived.
    ledger["generate_chunk_calls"] += 1
    ledger["chunks_reconstructed"] += 1
    ledger["kernels_reconstructed"] += len(kernels)
    ledger["residual_rows_reconstructed"] += len(residuals)
    for key in CENSUS_TOTAL_FIELDS:
        ledger["totals"][key] += regenerated[key]
    ledger["raw_chunk_sha256"].append(sha256(raw))


class StdlibCensusProducer:
    """Pinned order-nine census producer implemented with Python's stdlib only.

    This mirrors the pinned vectorized producer's exact integer predicates but
    uses bounded batches of mixed-radix codes.  It exists specifically for the
    isolated ``-I -S`` child, where optional NumPy/networkx are unavailable.
    """

    CHUNK_SCHEMA = "rank-seven-orders9-12-exact-residual-census-chunk-v1"
    MANIFEST_SCHEMA = "rank-seven-orders9-12-exact-residual-census-manifest-v1"
    ORDER_KERNEL_TOTALS = {ORDER: KERNEL_TOTAL}
    SOURCE_SHA256 = PINS[KERNEL_FIXTURE]
    RANK = RANK
    BUDGET_SCALED = 180

    _COLOR_CACHE: dict[tuple[int, int], tuple[tuple[int, ...], ...]] = {}
    _ORDER_ITEMS: tuple[tuple[int, int, int,
                              tuple[tuple[int, int, int], ...]], ...] | None = None

    @classmethod
    def reset_cache(cls) -> None:
        cls._ORDER_ITEMS = None

    @classmethod
    def restricted_colorings(cls, order: int, limit: int = 4
                             ) -> tuple[tuple[int, ...], ...]:
        key = (order, limit)
        cached = cls._COLOR_CACHE.get(key)
        if cached is not None:
            return cached
        require(type(order) is int and order >= 1 and type(limit) is int and limit >= 1,
                "invalid stdlib restricted-coloring request")
        colors = [0] * order
        rows = []

        def visit(position: int, maximum: int) -> None:
            if position == order:
                rows.append(tuple(colors))
                return
            for color in range(min(maximum + 1, limit - 1) + 1):
                colors[position] = color
                visit(position + 1, max(maximum, color))

        visit(1, 0)
        result = tuple(rows)
        cls._COLOR_CACHE[key] = result
        return result

    @classmethod
    def coarse_sieve(cls, edges: tuple[tuple[int, int, int], ...]) -> list[int]:
        support_count = len(edges)
        infinity = 10 ** 9
        minimum = [infinity] * (1 << support_count)
        for colors in cls.restricted_colorings(ORDER):
            crossing = 0
            cost = 0
            for index, (u, v, multiplicity) in enumerate(edges):
                if colors[u] != colors[v]:
                    crossing |= 1 << index
                    cost += 18 * multiplicity
            if cost < minimum[crossing]:
                minimum[crossing] = cost
        for bit in range(support_count):
            flag = 1 << bit
            for mask in range(1 << support_count):
                if not mask & flag and minimum[mask | flag] < minimum[mask]:
                    minimum[mask] = minimum[mask | flag]
        return minimum

    @classmethod
    def residual_orbits(cls, edges: tuple[tuple[int, int, int], ...],
                        actions: tuple[tuple[int, ...], ...], minimum: list[int],
                        batch_size: int):
        # Preserve the vector producer's mixed-radix code order.  The batch
        # argument remains part of its pinned API; an order-nine kernel has at
        # most 32,768 physical rows, so this fallback keeps only one row and
        # its finite automorphism image set live at a time.
        require(type(batch_size) is int and batch_size >= 1,
                "invalid stdlib census batch size")
        radices = tuple(multiplicity + 1 for _, _, multiplicity in edges)
        strides = []
        physical_rows = 1
        for radix in radices:
            strides.append(physical_rows)
            physical_rows *= radix
        residuals = []
        residual_physical = 0
        orbit_mass = 0
        for code in range(physical_rows):
            row = tuple((code // stride) % radix
                        for stride, radix in zip(strides, radices, strict=True))
            support = 0
            odd_sum = 0
            for index, value in enumerate(row):
                if value:
                    support |= 1 << index
                    odd_sum += value
            threshold = cls.BUDGET_SCALED - 10 * support.bit_count() + 13 * odd_sum
            if minimum[support] <= threshold:
                continue
            residual_physical += 1
            image_codes = tuple(
                sum(row[image] * strides[index]
                    for index, image in enumerate(action))
                for action in actions
            )
            if code != min(image_codes):
                continue
            stabilizer = sum(image == code for image in image_codes)
            orbit_size = len(set(image_codes))
            require(stabilizer >= 1 and len(actions) % stabilizer == 0 and
                    orbit_size == len(actions) // stabilizer,
                    "stdlib producer orbit-stabilizer identity failed")
            residuals.append((list(row), orbit_size))
            orbit_mass += orbit_size
        require(orbit_mass == residual_physical,
                "stdlib producer residual orbits do not partition residual rows")
        return physical_rows, len(residuals), residual_physical, residuals

    @classmethod
    def generate_chunk(cls, order: int, start: int, stop: int,
                       batch_size: int, progress: bool = False) -> dict[str, Json]:
        require(order == ORDER and type(start) is int and type(stop) is int and
                0 <= start < stop <= KERNEL_TOTAL and type(batch_size) is int and
                batch_size >= 1 and progress is False,
                "invalid stdlib census producer request")
        engine = census_source_engine_adapter()
        if cls._ORDER_ITEMS is None:
            cls._ORDER_ITEMS = tuple(
                item for item in engine.source_kernels() if item[2] == order)
        items = cls._ORDER_ITEMS
        require(len(items) == KERNEL_TOTAL, "stdlib producer source count changed")
        kernels = []
        residual_records = []
        residual_digest = hashlib.sha256()
        for global_index, local_index, item_order, edges in items[start:stop]:
            actions = engine.automorphism_actions(item_order, edges)
            minimum = cls.coarse_sieve(edges)
            physical, residual_count, residual_physical, residuals = cls.residual_orbits(
                edges, actions, minimum, batch_size)
            parity_orbits = burnside_orbits(edges, actions)
            ledger = {
                "global_kernel": global_index,
                "order_kernel": local_index,
                "edges": [list(edge) for edge in edges],
                "support_edges": len(edges),
                "automorphisms": len(actions),
                "physical_rows": physical,
                "parity_orbits": parity_orbits,
                "coarse_certified_orbits": parity_orbits - residual_count,
                "coarse_residual_orbits": residual_count,
                "coarse_residual_physical_rows": residual_physical,
            }
            kernels.append(ledger)
            for row, orbit_size in residuals:
                record = {
                    "global_kernel": global_index,
                    "order_kernel": local_index,
                    "row": row,
                    "orbit_size": orbit_size,
                }
                residual_digest.update(canonical_bytes(record))
                residual_records.append(record)
        return {
            "schema": cls.CHUNK_SCHEMA,
            "status": "complete-exact-residual-orbit-chunk",
            "full_theorem": False,
            "rank": RANK,
            "order": order,
            "budget": [RANK - 1, 1],
            "path_count": PATH_COUNT,
            "frontiers_per_residual": FRONTIERS,
            "kernel_range": [start, stop],
            "source_sha256": cls.SOURCE_SHA256,
            "kernel_total": len(kernels),
            "physical_row_total": sum(row["physical_rows"] for row in kernels),
            "parity_orbit_total": sum(row["parity_orbits"] for row in kernels),
            "coarse_certified_total": sum(row["coarse_certified_orbits"] for row in kernels),
            "coarse_residual_total": len(residual_records),
            "coarse_residual_physical_total": sum(
                row["coarse_residual_physical_rows"] for row in kernels),
            "frontier_target_total": FRONTIERS * len(residual_records),
            "residual_stream_sha256": residual_digest.hexdigest(),
            "kernels": kernels,
            "residuals": residual_records,
        }


def validate_stdlib_producer_equivalence(vector_producer: Any,
                                           ranges: tuple[tuple[int, int], ...]
                                           ) -> dict[str, Json]:
    """Compare bounded stdlib chunks byte-for-byte with the pinned vector producer.

    This is a diagnostic/preflight helper for a site-enabled test process.  The
    isolated ``-I -S`` production child cannot import NumPy and never calls it.
    """
    require(type(ranges) is tuple and bool(ranges),
            "stdlib/vector equivalence ranges must be a nonempty tuple")
    require(sha256(CENSUS_PRODUCER.read_bytes()) == PINS[CENSUS_PRODUCER],
            "vector census producer changed before equivalence probe")
    adapter = census_source_engine_adapter()
    original_load_engine = vector_producer.load_engine
    vector_producer.load_engine = lambda: adapter
    receipts = []
    try:
        for position, interval in enumerate(ranges):
            require(type(interval) is tuple and len(interval) == 2 and
                    all(type(value) is int for value in interval),
                    f"stdlib/vector equivalence range {position} malformed")
            start, stop = interval
            require(0 <= start < stop <= KERNEL_TOTAL and stop - start <= 16,
                    f"stdlib/vector equivalence range {position} is not bounded")
            scalar = StdlibCensusProducer.generate_chunk(
                ORDER, start, stop, 257, progress=False)
            vector = vector_producer.generate_chunk(
                ORDER, start, stop, 257, progress=False)
            scalar_raw = canonical_bytes(scalar)
            vector_raw = canonical_bytes(vector)
            require(scalar_raw == vector_raw,
                    f"stdlib/vector census producer differs on [{start},{stop})")
            receipts.append({
                "kernel_range": [start, stop],
                "kernel_total": stop - start,
                "physical_row_total": scalar["physical_row_total"],
                "residual_orbit_total": scalar["coarse_residual_total"],
                "canonical_sha256": sha256(scalar_raw),
                "byte_identical": True,
            })
    finally:
        vector_producer.load_engine = original_load_engine
    return {
        "schema": "rank-seven-order-nine-stdlib-vector-equivalence-v1",
        "bounded_kernel_total": sum(stop - start for start, stop in ranges),
        "ranges": receipts,
        "byte_identical": True,
        "claim_boundary": "bounded preflight only; not full-census or theorem evidence",
    }


def load_census_producer() -> Any:
    """Load the pinned producer, falling back only on absent optional NumPy."""
    try:
        return load_module(CENSUS_PRODUCER, "rank7_order9_fresh_census_producer")
    except ModuleNotFoundError as error:
        require(error.name == "numpy", "unexpected missing census producer dependency")
        return StdlibCensusProducer


def census_source_engine_adapter() -> Any:
    """Return the pinned producer interface with a stdlib exact source engine.

    The historical pinned source module imports optional ``networkx``.  The
    adapter instead reads the already authenticated fixture and supplies the
    only two source-engine operations used by ``generate_chunk``.  Its
    automorphism implementation is this replayer's independently tested exact
    weighted-multigraph enumerator.
    """
    class Adapter:
        SOURCE_SHA256 = PINS[KERNEL_FIXTURE]

        @staticmethod
        def source_kernels() -> tuple[tuple[int, int, int,
                                            tuple[tuple[int, int, int], ...]], ...]:
            fixture = strict_json(read_pinned(KERNEL_FIXTURE, PINS[KERNEL_FIXTURE]),
                                  KERNEL_FIXTURE.name)
            local = {order: 0 for order in range(2, 13)}
            records = []
            for global_index, item in enumerate(fixture["kernels"], 1):
                order = exact_int(item["n"], "source adapter kernel order", minimum=2)
                local[order] += 1
                dense = item["code"]
                require(type(dense) is list and
                        len(dense) == order * (order - 1) // 2 and
                        all(type(value) is int and value >= 0 for value in dense),
                        "source adapter dense kernel malformed")
                edges = []
                cursor = 0
                for u in range(order):
                    for v in range(u + 1, order):
                        multiplicity = dense[cursor]
                        cursor += 1
                        if multiplicity:
                            edges.append((u, v, multiplicity))
                records.append((global_index, local[order], order, tuple(edges)))
            require(local[ORDER] == KERNEL_TOTAL, "source adapter order-nine count changed")
            return tuple(records)

        @staticmethod
        def automorphism_actions(order: int, edges: tuple[tuple[int, int, int], ...]
                                 ) -> tuple[tuple[int, ...], ...]:
            require(type(order) is int and order == ORDER,
                    "source adapter called outside order nine")
            return automorphism_actions(edges)

    return Adapter


def census_reconstruction_result(requested: bool, complete: bool,
                                 ledger: dict[str, Json],
                                 census_manifest: dict[str, Json]) -> dict[str, Json]:
    """Return and enforce the execution-derived fresh-census contract."""
    expected_hashes = [pin[0] for pin in CHUNK_SPECS]
    expected_totals = {key: census_manifest[key] for key in CENSUS_TOTAL_FIELDS}
    eligible = bool(
        requested and complete and
        ledger["producer_loads"] == 1 and
        ledger["generate_chunk_calls"] == len(CHUNK_SPECS) and
        ledger["chunks_reconstructed"] == len(CHUNK_SPECS) and
        ledger["kernels_reconstructed"] == KERNEL_TOTAL and
        ledger["residual_rows_reconstructed"] == RESIDUAL_TOTAL and
        ledger["totals"] == expected_totals and
        ledger["raw_chunk_sha256"] == expected_hashes
    )
    if requested and complete:
        require(eligible, "complete census reconstruction execution ledger differs")
    if not requested:
        require(ledger == empty_census_reconstruction_ledger(),
                "census reconstruction counters changed without execution")
    return {
        "census_reconstruction": requested,
        "census_reconstruction_requested": requested,
        "census_reconstruction_eligible": eligible,
        "census_producer_loads": ledger["producer_loads"],
        "census_generate_chunk_calls": ledger["generate_chunk_calls"],
        "census_reconstruction_generate_calls": ledger["generate_chunk_calls"],
        "census_chunks_reconstructed": ledger["chunks_reconstructed"],
        "census_reconstruction_chunks": ledger["chunks_reconstructed"],
        "census_kernels_reconstructed": ledger["kernels_reconstructed"],
        "census_reconstruction_kernel_total": ledger["kernels_reconstructed"],
        "census_residual_rows_reconstructed": ledger["residual_rows_reconstructed"],
        "census_reconstruction_residual_orbit_total":
            ledger["residual_rows_reconstructed"],
        "census_physical_row_total_reconstructed": ledger["totals"]["physical_row_total"],
        "census_parity_orbit_total_reconstructed": ledger["totals"]["parity_orbit_total"],
        "census_coarse_certified_total_reconstructed":
            ledger["totals"]["coarse_certified_total"],
        "census_coarse_residual_total_reconstructed":
            ledger["totals"]["coarse_residual_total"],
        "census_coarse_residual_physical_total_reconstructed":
            ledger["totals"]["coarse_residual_physical_total"],
        "census_reconstruction_residual_physical_total":
            ledger["totals"]["coarse_residual_physical_total"],
        "census_frontier_target_total_reconstructed":
            ledger["totals"]["frontier_target_total"],
        "census_reconstructed_raw_chunk_sha256": ledger["raw_chunk_sha256"],
        "census_reconstructed_raw_sha256": ledger["raw_chunk_sha256"],
        "census_producer_sha256": PINS[CENSUS_PRODUCER],
        "census_source_engine_sha256": PINS[SOURCE_ENGINE],
        "census_fixture_sha256": PINS[KERNEL_FIXTURE],
        "census_source_adapter":
            "pinned fixture order plus local exact weighted-automorphism actions",
    }


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
    # search followed by one independent exact replay of the returned witness.
    witness = owner.generalized_three_ray_witness(edges, row)
    cost = None if witness is None else owner.three_ray_witness_cost(edges, row, witness)
    accepted = cost is not None and cost <= 18 * (RANK - 1)
    return ["signed-three-ray"], accepted


def _load_common() -> tuple[dict[str, Json], dict[str, Json]]:
    audit_pins()
    census_manifest = strict_json(read_pinned(CENSUS_MANIFEST, PINS[CENSUS_MANIFEST]),
                                  CENSUS_MANIFEST.name)
    owner_manifest = strict_json(read_pinned(OWNER_MANIFEST, PINS[OWNER_MANIFEST]),
                                 OWNER_MANIFEST.name)
    exact_fields(census_manifest, CENSUS_MANIFEST_FIELDS, "census manifest")
    exact_fields(owner_manifest, OWNER_MANIFEST_FIELDS, "owner manifest")
    require(type(census_manifest["chunks"]) is list and
            all(type(item) is dict and set(item) == CENSUS_MANIFEST_CHUNK_FIELDS
                for item in census_manifest["chunks"]),
            "census manifest chunk exact schema changed")
    require(type(owner_manifest["chunks"]) is list and
            all(type(item) is dict and set(item) == OWNER_MANIFEST_CHUNK_FIELDS
                for item in owner_manifest["chunks"]),
            "owner manifest chunk exact schema changed")
    for key in ("rank", "order", "path_count", "frontiers_per_residual", "kernel_total",
                "parity_orbit_total", "coarse_certified_total", "coarse_residual_total",
                "coarse_residual_physical_total", "physical_row_total",
                "frontier_target_total"):
        exact_int(census_manifest[key], f"census manifest.{key}", minimum=0)
    exact_int_list(census_manifest["budget"], 2, "census manifest.budget", minimum=0)
    exact_bool(census_manifest["full_theorem"], "census manifest.full_theorem")
    for key in ("schema", "status", "source_sha256"):
        exact_str(census_manifest[key], f"census manifest.{key}")
    for key in ("rank", "order", "path_count", "frontiers_per_residual",
                "scanned_residual_total", "scanned_target_total",
                "payload_free_owned_orbit_total", "payload_free_owned_physical_total",
                "payload_free_owned_target_total", "remainder_orbit_total",
                "remainder_physical_total", "remainder_target_total"):
        exact_int(owner_manifest[key], f"owner manifest.{key}", minimum=0)
    exact_bool(owner_manifest["full_theorem"], "owner manifest.full_theorem")
    for key in ("schema", "status", "scope", "manifest_sha256", "owner_engine_sha256",
                "atom_recognizer_sha256", "classification_stream_sha256",
                "remainder_stream_sha256"):
        exact_str(owner_manifest[key], f"owner manifest.{key}")
    exact_str_int_map(owner_manifest["exclusive_owner_orbit_counts"], set(LANES),
                      "owner manifest.exclusive_owner_orbit_counts")
    exact_str_int_map(owner_manifest["exclusive_owner_physical_counts"], set(LANES),
                      "owner manifest.exclusive_owner_physical_counts")
    exact_str_int_map(owner_manifest["atom_profile_owner_counts"], set(EXPECTED_PROFILES),
                      "owner manifest.atom_profile_owner_counts")
    require(census_manifest.get("schema") ==
            "rank-seven-orders9-12-exact-residual-census-manifest-v1" and
            census_manifest.get("status") == "complete-exact-residual-orbit-decomposition" and
            census_manifest.get("full_theorem") is False and
            (census_manifest.get("rank"), census_manifest.get("order"),
             census_manifest.get("path_count"), census_manifest.get("frontiers_per_residual"),
             census_manifest.get("kernel_total")) ==
            (RANK, ORDER, PATH_COUNT, FRONTIERS, KERNEL_TOTAL) and
            census_manifest.get("budget") == [RANK - 1, 1] and
            census_manifest.get("source_sha256") == PINS[KERNEL_FIXTURE],
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
            (RANK, ORDER, PATH_COUNT, FRONTIERS) and
            owner_manifest.get("scope") == "sufficient structural owners only; no rational search" and
            owner_manifest.get("manifest_sha256") == PINS[CENSUS_MANIFEST] and
            owner_manifest.get("owner_engine_sha256") == PINS[OWNER_ENGINE] and
            owner_manifest.get("atom_recognizer_sha256") == PINS[ATOM_RECOGNIZER],
            "owner manifest scope changed")
    require(owner_manifest.get("scanned_residual_total") == RESIDUAL_TOTAL and
            owner_manifest.get("exclusive_owner_orbit_counts") == EXPECTED_OWNER_COUNTS and
            owner_manifest.get("exclusive_owner_physical_counts") == EXPECTED_OWNER_PHYSICAL and
            owner_manifest.get("atom_profile_owner_counts") == EXPECTED_PROFILES and
            owner_manifest.get("payload_free_owned_orbit_total") == OWNER_TOTAL and
            owner_manifest.get("payload_free_owned_physical_total") == OWNER_PHYSICAL_TOTAL and
            owner_manifest.get("remainder_orbit_total") == REMAINDER_TOTAL and
            owner_manifest.get("remainder_physical_total") == REMAINDER_PHYSICAL_TOTAL and
            owner_manifest.get("scanned_target_total") == RESIDUAL_TOTAL * FRONTIERS and
            owner_manifest.get("payload_free_owned_target_total") == OWNER_TOTAL * FRONTIERS and
            owner_manifest.get("remainder_target_total") == REMAINDER_TOTAL * FRONTIERS,
            "owner manifest exact ledger changed")
    return census_manifest, owner_manifest


def _verify(*, replay_predicates: bool, progress: bool = False,
            chunk_limit: int | None = None, key_sink: KeySink | None = None,
            reconstruct_census: bool = False) -> dict[str, Json]:
    census_manifest, owner_manifest = _load_common()
    census_records = census_manifest.get("chunks")
    owner_records = owner_manifest.get("chunks")
    require(type(census_records) is list and type(owner_records) is list and
            len(census_records) == len(owner_records) == len(CHUNK_SPECS),
            "eight-chunk ledger changed")
    require(chunk_limit is None or (type(chunk_limit) is int and
            1 <= chunk_limit <= len(CHUNK_SPECS)), "invalid test-only chunk limit")
    selected = len(CHUNK_SPECS) if chunk_limit is None else chunk_limit

    fixture = strict_json(read_pinned(KERNEL_FIXTURE, PINS[KERNEL_FIXTURE]),
                          KERNEL_FIXTURE.name)
    exact_fields(fixture, FIXTURE_FIELDS, "kernel fixture")
    for key in ("schema", "status", "generator", "encoding"):
        exact_str(fixture[key], f"kernel fixture.{key}")
    exact_int(fixture["beta"], "kernel fixture.beta", minimum=0)
    exact_int(fixture["minimum_degree"], "kernel fixture.minimum_degree", minimum=0)
    exact_int_list(fixture["orders"], 2, "kernel fixture.orders", minimum=0)
    exact_int_list(fixture["counts_by_order_n2_to_n12"], 11,
                   "kernel fixture.counts_by_order_n2_to_n12", minimum=0)
    require(fixture["schema"] == "rank-seven-loopless-no-cut-kernels-v2" and
            fixture["status"] == "complete-proved-removable-ear-exhaustion" and
            fixture["generator"] ==
            "proved-complete-one-open-ear-augmentation-of-exact-rank-six-census" and
            fixture["beta"] == RANK and fixture["minimum_degree"] == 3 and
            fixture["orders"] == [2, 12] and
            fixture["encoding"] == "lexicographic upper-triangle multiplicities" and
            fixture["counts_by_order_n2_to_n12"] ==
            [1, 6, 47, 233, 914, 2270, 4015, 4495, 3396, 1391, 365],
            "kernel fixture semantics changed")
    fixture_kernels = fixture["kernels"]
    require(type(fixture_kernels) is list and len(fixture_kernels) == 17133 and
            all(type(item) is dict and set(item) == FIXTURE_KERNEL_FIELDS
                for item in fixture_kernels),
            "kernel fixture record schema changed")
    order_nine_fixture = tuple((global_index, item) for global_index, item in
                               enumerate(fixture_kernels, 1) if item["n"] == ORDER)
    require(len(order_nine_fixture) == KERNEL_TOTAL,
            "kernel fixture order-nine slice changed")

    producer = None
    census_reconstruction = empty_census_reconstruction_ledger()
    if reconstruct_census:
        producer = load_census_producer()
        census_reconstruction["producer_loads"] += 1
        require(producer.CHUNK_SCHEMA ==
                "rank-seven-orders9-12-exact-residual-census-chunk-v1" and
                producer.MANIFEST_SCHEMA ==
                "rank-seven-orders9-12-exact-residual-census-manifest-v1" and
                producer.ORDER_KERNEL_TOTALS[ORDER] == KERNEL_TOTAL and
                producer.SOURCE_SHA256 == PINS[KERNEL_FIXTURE] and
                producer.RANK == RANK and producer.BUDGET_SCALED == 180,
                "census producer semantics changed")
        if producer is not StdlibCensusProducer:
            source_adapter = census_source_engine_adapter()
            original_load_engine = producer.load_engine

            def load_pinned_source_engine() -> Any:
                # The vectorized producer's source imports optional networkx.
                try:
                    engine = original_load_engine()
                except ModuleNotFoundError as error:
                    require(error.name == "networkx",
                            "unexpected missing census source dependency")
                    return source_adapter
                require(engine.SOURCE_SHA256 == PINS[KERNEL_FIXTURE],
                        "census source engine fixture pin changed")
                return engine

            producer.load_engine = load_pinned_source_engine

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
    universe_source_indices = hashlib.sha256()
    universe_keys = hashlib.sha256()
    owner_source_indices = hashlib.sha256()
    owner_keys = hashlib.sha256()
    remainder_source_indices = hashlib.sha256()
    remainder_keys = hashlib.sha256()
    source_cursor = 0
    orbit_recomputations = 0
    burnside_recomputations = 0
    remainder_count = remainder_mass = 0
    kernel_cursor = 0
    independent_totals = Counter()
    receipts = []

    for chunk_index in range(selected):
        pin = CHUNK_SPECS[chunk_index]
        census_spec = census_records[chunk_index]
        owner_spec = owner_records[chunk_index]
        exact_fields(census_spec, CENSUS_MANIFEST_CHUNK_FIELDS,
                     f"chunk {chunk_index} census manifest record")
        exact_fields(owner_spec, OWNER_MANIFEST_CHUNK_FIELDS,
                     f"chunk {chunk_index} owner manifest record")
        start, stop = exact_int_list(census_spec["kernel_range"], 2,
                                     f"chunk {chunk_index} census kernel_range", minimum=0)
        exact_int(census_spec["coarse_residual_total"],
                  f"chunk {chunk_index} census coarse_residual_total", minimum=0)
        for key in ("path", "raw_sha256", "artifact_sha256"):
            exact_str(census_spec[key], f"chunk {chunk_index} census {key}")
        exact_int_list(owner_spec["kernel_range"], 2,
                       f"chunk {chunk_index} owner kernel_range", minimum=0)
        exact_int(owner_spec["scanned_residual_total"],
                  f"chunk {chunk_index} owner scanned_residual_total", minimum=0)
        exact_int(owner_spec["remainder_orbit_total"],
                  f"chunk {chunk_index} owner remainder_orbit_total", minimum=0)
        exact_int(owner_spec["remainder_physical_total"],
                  f"chunk {chunk_index} owner remainder_physical_total", minimum=0)
        exact_str(owner_spec["path"], f"chunk {chunk_index} owner path")
        exact_str(owner_spec["artifact_sha256"],
                  f"chunk {chunk_index} owner artifact_sha256")
        exact_str_int_map(owner_spec["exclusive_owner_orbit_counts"], set(LANES),
                          f"chunk {chunk_index} owner orbit counts", allow_sparse=True)
        exact_str_int_map(owner_spec["exclusive_owner_physical_counts"], set(LANES),
                          f"chunk {chunk_index} owner physical counts", allow_sparse=True)
        expected_stop = min(KERNEL_TOTAL, (chunk_index + 1) * 562)
        require(start == kernel_cursor and stop == expected_stop and
                owner_spec["kernel_range"] == [start, stop],
                f"chunk {chunk_index}: kernel ranges gap, overlap, or disagree")
        kernel_cursor = stop
        census_path = (HERE / census_spec.get("path", "")).resolve()
        require(census_path.parent == HERE.resolve(),
                f"chunk {chunk_index}: census path escapes experiment directory")
        report_path = RESULTS / f"chunk-{chunk_index:02d}.json"
        report_raw = read_pinned(report_path, pin[2])
        report = strict_json(report_raw, report_path.name)
        exact_fields(report, CHUNK_REPORT_FIELDS, f"chunk {chunk_index} report")
        exact_fields(report["classification_stream"], STREAM_RECEIPT_FIELDS,
                     f"chunk {chunk_index} classification receipt")
        exact_fields(report["remainder_stream"], STREAM_RECEIPT_FIELDS,
                     f"chunk {chunk_index} remainder receipt")
        for receipt_name in ("classification_stream", "remainder_stream"):
            for key in STREAM_RECEIPT_FIELDS:
                exact_str(report[receipt_name][key],
                          f"chunk {chunk_index} {receipt_name}.{key}")
        for key in ("chunk_index", "scanned_residual_total", "remainder_orbit_total",
                    "remainder_physical_total"):
            exact_int(report[key], f"chunk {chunk_index} report.{key}", minimum=0)
        exact_int_list(report["kernel_range"], 2,
                       f"chunk {chunk_index} report.kernel_range", minimum=0)
        exact_int_list(report["source_range"], 2,
                       f"chunk {chunk_index} report.source_range", minimum=0)
        exact_bool(report["full_theorem"], f"chunk {chunk_index} report.full_theorem")
        for key in ("schema", "census_path", "census_artifact_sha256", "owner_engine_sha256",
                    "atom_recognizer_sha256", "manifest_sha256"):
            exact_str(report[key], f"chunk {chunk_index} report.{key}")
        exact_str_int_map(report["exclusive_owner_orbit_counts"], set(LANES),
                          f"chunk {chunk_index} report orbit counts")
        exact_str_int_map(report["exclusive_owner_physical_counts"], set(LANES),
                          f"chunk {chunk_index} report physical counts")
        exact_str_int_map(report["atom_profile_owner_counts"], set(EXPECTED_PROFILES),
                          f"chunk {chunk_index} report atom profiles", allow_sparse=True)
        require(report.get("schema") == "rank-seven-order-nine-structural-owner-chunk-v1" and
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
        exact_fields(census, CENSUS_CHUNK_FIELDS, f"chunk {chunk_index} census")
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
        for key in ("rank", "order", "path_count", "frontiers_per_residual", "kernel_total",
                    "physical_row_total", "parity_orbit_total", "coarse_certified_total",
                    "coarse_residual_total", "coarse_residual_physical_total",
                    "frontier_target_total"):
            exact_int(census[key], f"chunk {chunk_index} census.{key}", minimum=0)
        exact_int_list(census["budget"], 2, f"chunk {chunk_index} census.budget", minimum=0)
        exact_int_list(census["kernel_range"], 2,
                       f"chunk {chunk_index} census.kernel_range", minimum=0)
        exact_bool(census["full_theorem"], f"chunk {chunk_index} census.full_theorem")
        for key in ("schema", "status", "source_sha256", "residual_stream_sha256"):
            exact_str(census[key], f"chunk {chunk_index} census.{key}")
        require(census.get("schema") ==
                "rank-seven-orders9-12-exact-residual-census-chunk-v1" and
                census.get("full_theorem") is False and
                census.get("status") == "complete-exact-residual-orbit-chunk" and
                census.get("source_sha256") == PINS[KERNEL_FIXTURE] and
                census.get("budget") == [RANK - 1, 1] and
                (census.get("rank"), census.get("order"), census.get("path_count"),
                 census.get("frontiers_per_residual"), census.get("kernel_range")) ==
                (RANK, ORDER, PATH_COUNT, FRONTIERS, [start, stop]),
                f"chunk {chunk_index}: census scope changed")
        require(census.get("coarse_certified_total") + census.get("coarse_residual_total") ==
                census.get("parity_orbit_total"),
                f"chunk {chunk_index}: base partition identity changed")
        if reconstruct_census:
            regenerated = producer.generate_chunk(ORDER, start, stop, 262144, progress=False)
            record_census_reconstruction(
                census_reconstruction, regenerated, census, pin[0], f"chunk {chunk_index}")

        expected_fixture_kernels = {}
        for local_offset, (global_kernel, fixture_item) in enumerate(
                order_nine_fixture[start:stop], start + 1):
            dense = fixture_item["code"]
            require(type(dense) is list and len(dense) == ORDER * (ORDER - 1) // 2 and
                    all(type(value) is int and value >= 0 for value in dense),
                    f"chunk {chunk_index}: malformed fixture kernel")
            pair_cursor = 0
            edges = []
            for u in range(ORDER):
                for v in range(u + 1, ORDER):
                    multiplicity = dense[pair_cursor]
                    pair_cursor += 1
                    if multiplicity:
                        edges.append((u, v, multiplicity))
            require(sum(edge[2] for edge in edges) == PATH_COUNT,
                    f"chunk {chunk_index}: fixture path total changed")
            expected_fixture_kernels[local_offset] = (global_kernel, tuple(edges))

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
        kernel_physical = kernel_orbits = kernel_certified = 0
        kernel_residuals = kernel_residual_physical = 0
        for item in kernels_raw:
            exact_fields(item, KERNEL_FIELDS, f"chunk {chunk_index} kernel")
            for key in ("order_kernel", "global_kernel", "support_edges", "automorphisms",
                        "physical_rows", "parity_orbits", "coarse_certified_orbits",
                        "coarse_residual_orbits", "coarse_residual_physical_rows"):
                exact_int(item[key], f"chunk {chunk_index} kernel.{key}", minimum=0)
            require(type(item.get("order_kernel")) is int and
                    item["order_kernel"] == previous_kernel + 1 and
                    item["order_kernel"] not in kernels,
                    f"chunk {chunk_index}: malformed, duplicate, or unordered kernel")
            previous_kernel = item["order_kernel"]
            edges_raw = item.get("edges")
            require(type(edges_raw) is list, f"chunk {chunk_index}: malformed edges")
            edges = tuple(tuple(edge) for edge in edges_raw)
            require(all(len(edge) == 3 and all(type(value) is int for value in edge) and
                        0 <= edge[0] < edge[1] < ORDER and edge[2] > 0 for edge in edges) and
                    sum(edge[2] for edge in edges) == PATH_COUNT,
                    f"chunk {chunk_index}: nonphysical kernel edges")
            require(item["global_kernel"] >= 1 and
                    (item["global_kernel"], edges) ==
                    expected_fixture_kernels[item["order_kernel"]],
                    f"chunk {chunk_index}: kernel differs from canonical fixture order")
            require(type(item["automorphisms"]) is int and item["automorphisms"] >= 1 and
                    type(item["support_edges"]) is int and
                    item["support_edges"] == len(edges) and
                    all(type(item[key]) is int and item[key] >= 0 for key in (
                        "physical_rows", "parity_orbits", "coarse_certified_orbits",
                        "coarse_residual_orbits", "coarse_residual_physical_rows")) and
                    item["parity_orbits"] == item["coarse_certified_orbits"] +
                    item["coarse_residual_orbits"] and
                    item["physical_rows"] == math.prod(edge[2] + 1 for edge in edges),
                    f"chunk {chunk_index}: kernel ledger semantics changed")
            actions = automorphism_actions(edges)
            require(len(actions) == item["automorphisms"],
                    f"chunk {chunk_index}: fresh automorphism count differs")
            require(burnside_orbits(edges, actions) == item["parity_orbits"],
                    f"chunk {chunk_index}: fresh Burnside orbit total differs")
            burnside_recomputations += 1
            kernels[item["order_kernel"]] = {
                "global_kernel": item["global_kernel"],
                "edges": edges,
                "actions": actions,
                "expected_residual_orbits": item["coarse_residual_orbits"],
                "expected_residual_physical": item["coarse_residual_physical_rows"],
                "observed_residual_orbits": 0,
                "observed_residual_physical": 0,
            }
            kernel_physical += item["physical_rows"]
            kernel_orbits += item["parity_orbits"]
            kernel_certified += item["coarse_certified_orbits"]
            kernel_residuals += item["coarse_residual_orbits"]
            kernel_residual_physical += item["coarse_residual_physical_rows"]
        require(len(kernels) == stop - start and previous_kernel == stop and
                (kernel_physical, kernel_orbits, kernel_certified, kernel_residuals,
                 kernel_residual_physical) ==
                (census["physical_row_total"], census["parity_orbit_total"],
                 census["coarse_certified_total"], census["coarse_residual_total"],
                 census["coarse_residual_physical_total"]),
                f"chunk {chunk_index}: incomplete or inconsistent kernel ledger")

        local_counts = Counter({lane: 0 for lane in LANES})
        local_masses = Counter({lane: 0 for lane in LANES})
        local_profiles: Counter[str] = Counter()
        local_remainder_count = local_remainder_mass = 0
        local_source_mass = 0
        remainder_iterator = iter(remainders)
        next_remainder = next(remainder_iterator, None)
        previous_key = None
        census_digest = hashlib.sha256()
        local_classification = hashlib.sha256()
        local_remainder = hashlib.sha256()

        for local_index, (residual, classification) in enumerate(
                zip(residuals, classifications, strict=True)):
            source_index = source_cursor + local_index
            exact_fields(residual, RESIDUAL_FIELDS,
                         f"chunk {chunk_index} row {local_index} residual")
            local_kernel = residual["order_kernel"]
            require(type(local_kernel) is int and local_kernel in kernels and
                    type(residual["global_kernel"]) is int and
                    residual["global_kernel"] == kernels[local_kernel]["global_kernel"],
                    f"chunk {chunk_index} row {local_index}: bad kernel reference")
            edges = kernels[local_kernel]["edges"]
            actions = kernels[local_kernel]["actions"]
            row_raw = residual["row"]
            orbit_size = residual["orbit_size"]
            require(type(row_raw) is list and len(row_raw) == len(edges) and
                    all(type(value) is int and 0 <= value <= edge[2]
                        for value, edge in zip(row_raw, edges, strict=True)) and
                    type(orbit_size) is int and orbit_size >= 1,
                    f"chunk {chunk_index} row {local_index}: nonphysical row")
            row = tuple(row_raw)
            code = 0
            stride = 1
            for value, edge in zip(row_raw, edges, strict=True):
                code += value * stride
                stride *= edge[2] + 1
            minimum_image_code, fresh_orbit_size = recompute_orbit(row, edges, actions)
            require(code == minimum_image_code,
                    f"chunk {chunk_index} row {local_index}: noncanonical mixed-radix representative")
            require(fresh_orbit_size == orbit_size,
                    f"chunk {chunk_index} row {local_index}: fresh orbit size differs")
            orbit_recomputations += 1
            kernels[local_kernel]["observed_residual_orbits"] += 1
            kernels[local_kernel]["observed_residual_physical"] += orbit_size
            local_source_mass += orbit_size
            key = (local_kernel, code)
            require(previous_key is None or previous_key < key,
                    f"chunk {chunk_index} row {local_index}: census order/uniqueness changed")
            previous_key = key
            census_digest.update(canonical_bytes(residual))
            expected_key = [source_index, residual["global_kernel"], local_kernel,
                            row_raw, orbit_size]
            canonical_key = (source_index, residual["global_kernel"], local_kernel,
                             tuple(row_raw), orbit_size)
            update_index_digest(universe_source_indices, source_index)
            update_key_digest(universe_keys, canonical_key)
            require(type(classification) is list and len(classification) == 7 and
                    type(classification[0]) is int and classification[0] >= 0 and
                    type(classification[1]) is int and classification[1] >= 1 and
                    type(classification[2]) is int and classification[2] >= 1 and
                    type(classification[3]) is list and
                    all(type(value) is int and value >= 0 for value in classification[3]) and
                    type(classification[4]) is int and classification[4] >= 1 and
                    classification[:5] == expected_key,
                    f"chunk {chunk_index} row {local_index}: classification/census zip failed")
            lane, detail = classification[5:]
            require(lane is None or lane in LANES,
                    f"chunk {chunk_index} row {local_index}: unknown lane")
            encoded_classification = canonical_bytes(classification)
            local_classification.update(encoded_classification)
            global_classification.update(encoded_classification)
            if lane is None:
                require(type(next_remainder) is list and len(next_remainder) == 5 and
                        type(next_remainder[0]) is int and next_remainder[0] >= 0 and
                        type(next_remainder[1]) is int and next_remainder[1] >= 1 and
                        type(next_remainder[2]) is int and next_remainder[2] >= 1 and
                        type(next_remainder[3]) is list and
                        all(type(value) is int and value >= 0 for value in next_remainder[3]) and
                        type(next_remainder[4]) is int and next_remainder[4] >= 1 and
                        detail is None and next_remainder == expected_key,
                        f"chunk {chunk_index} row {local_index}: ordered complement mismatch")
                encoded_remainder = canonical_bytes(next_remainder)
                local_remainder.update(encoded_remainder)
                global_remainder.update(encoded_remainder)
                next_remainder = next(remainder_iterator, None)
                update_index_digest(remainder_source_indices, source_index)
                update_key_digest(remainder_keys, canonical_key)
                if key_sink is not None:
                    key_sink("remainder", canonical_key)
                local_remainder_count += 1
                local_remainder_mass += orbit_size
            else:
                update_index_digest(owner_source_indices, source_index)
                update_key_digest(owner_keys, canonical_key)
                if key_sink is not None:
                    key_sink("owner", canonical_key)
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
                    require(type(detail) is list and bool(detail),
                            f"chunk {chunk_index} row {local_index}: bad atom detail")
                    for profile in detail:
                        require(type(profile) is list and len(profile) == 2,
                                f"chunk {chunk_index} row {local_index}: bad atom profile")
                        mixed, widths = profile
                        require(type(mixed) is int and type(widths) is list and
                                all(type(width) is int for width in widths),
                                f"chunk {chunk_index} row {local_index}: bad atom profile")
                        local_profiles[f"mixed-{mixed}/simplex-"
                                       f"{'-'.join(map(str, widths)) or 'none'}"] += 1
                else:
                    require(detail == ["signed-three-ray"],
                            f"chunk {chunk_index} row {local_index}: bad generalized detail")

            if replay_predicates:
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

        require(next_remainder is None and
                local_source_mass == census["coarse_residual_physical_total"],
                f"chunk {chunk_index}: remainder tail or residual physical ledger differs")
        require(all(kernel["observed_residual_orbits"] == kernel["expected_residual_orbits"] and
                    kernel["observed_residual_physical"] == kernel["expected_residual_physical"]
                    for kernel in kernels.values()),
                f"chunk {chunk_index}: fresh per-kernel residual ledger differs")
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
            "source_range": [source_cursor - len(residuals), source_cursor],
            "rows": len(residuals),
            "census_raw_sha256": pin[0],
            "census_artifact_sha256": pin[1],
            "report_sha256": pin[2],
            "classification_sha256": pin[3],
            "classification_artifact_sha256": pin[4],
            "remainder_rows": local_remainder_count,
            "remainder_sha256": pin[5],
            "remainder_artifact_sha256": pin[6],
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
        observed_source_identity = {
            "universe_source_index_sha256": universe_source_indices.hexdigest(),
            "universe_key_sha256": universe_keys.hexdigest(),
            "owner_source_index_sha256": owner_source_indices.hexdigest(),
            "owner_key_sha256": owner_keys.hexdigest(),
            "remainder_source_index_sha256": remainder_source_indices.hexdigest(),
            "remainder_key_sha256": remainder_keys.hexdigest(),
        }
        require(observed_source_identity == EXPECTED_SOURCE_IDENTITY,
                "canonical source identity digests differ")
        if replay_predicates:
            # A None classification means every predicate failed; accepted lanes
            # alone therefore sum to OWNER_TOTAL, not the full residual universe.
            require(dict(predicate_passes) == EXPECTED_OWNER_COUNTS,
                    "fresh predicate pass ledger differs")
            require(dict(predicate_calls) == EXPECTED_PREDICATE_CALLS and
                    sum(predicate_calls.values()) == EXPECTED_PREDICATE_CALL_TOTAL,
                    "fresh predicate call ledger differs")

    reconstruction_result = census_reconstruction_result(
        reconstruct_census, complete, census_reconstruction, census_manifest)
    predicate_eligible = bool(
        replay_predicates and complete and source_cursor == RESIDUAL_TOTAL and
        dict(predicate_calls) == EXPECTED_PREDICATE_CALLS and
        dict(predicate_passes) == EXPECTED_OWNER_COUNTS
    )
    require(not replay_predicates or not complete or predicate_eligible,
            "complete predicate execution ledger is ineligible")
    combined_eligible = bool(
        complete and predicate_eligible and
        reconstruction_result["census_reconstruction_eligible"]
    )
    mode = {
        (False, False): "authenticated-stored-stream-zip",
        (False, True): "fresh-census-plus-authenticated-stored-stream-zip",
        (True, False): "authenticated-census-plus-fresh-full-predicate-replay",
        (True, True): "fresh-census-plus-fresh-full-predicate-replay",
    }[(replay_predicates, reconstruct_census)]
    trust_boundary = {
        (False, False):
            "stored census/classification/remainder rows are authenticated and zipped; "
            "census generation and ownership predicates are not replayed",
        (False, True):
            "the exact census is freshly reconstructed and matched chunk-for-chunk; stored "
            "classification/remainder rows are authenticated and zipped; ownership predicates "
            "are not replayed",
        (True, False):
            "stored census/classification/remainder rows are authenticated and zipped; every "
            "orbit, Burnside ledger, and precedence-ordered exact ownership predicate is freshly "
            "replayed; census generation is not replayed",
        (True, True):
            "the exact census is freshly reconstructed and matched chunk-for-chunk, then every "
            "orbit, Burnside ledger, and precedence-ordered exact ownership predicate is freshly "
            "replayed; stored generalized detail is not a witness",
    }[(replay_predicates, reconstruct_census)]
    return {
        "schema": SCHEMA,
        "status": "passed",
        "mode": mode,
        "full_theorem": False,
        "read_only": True,
        "writes": 0,
        "complete": complete,
        "trust_boundary": trust_boundary,
        **reconstruction_result,
        "combined_replay_eligible": combined_eligible,
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
        "orbit_recomputations": orbit_recomputations,
        "automorphism_recomputations": burnside_recomputations,
        "burnside_recomputations": burnside_recomputations,
        "mixed_radix_canonicality_validated": True,
        "per_kernel_residual_ledgers_validated": True,
        "source_identity": {
            "encoding": "sha256(concatenated canonical JSON [source_index,global_kernel,order_kernel,row,orbit_size] lines)",
            "source_index_encoding": "sha256(concatenated ASCII decimal source_index plus newline)",
            "source_index_range": [0, source_cursor],
            "universe_orbit_total": source_cursor,
            "universe_physical_total": independent_totals["coarse_residual_physical_total"],
            "universe_source_index_sha256": universe_source_indices.hexdigest(),
            "universe_key_sha256": universe_keys.hexdigest(),
            "owner_orbit_total": sum(counts.values()),
            "owner_physical_total": sum(masses.values()),
            "owner_source_index_sha256": owner_source_indices.hexdigest(),
            "owner_key_sha256": owner_keys.hexdigest(),
            "remainder_orbit_total": remainder_count,
            "remainder_physical_total": remainder_mass,
            "remainder_source_index_sha256": remainder_source_indices.hexdigest(),
            "remainder_key_sha256": remainder_keys.hexdigest(),
            "partition_validated": source_cursor == sum(counts.values()) + remainder_count,
        },
        "row_recognition_calls": source_cursor if replay_predicates else 0,
        "predicate_replay_eligible": predicate_eligible,
        "predicate_call_total": sum(predicate_calls.values()),
        "predicate_pass_total": sum(predicate_passes.values()),
        "predicate_unowned_rows": remainder_count if replay_predicates else 0,
        "recognition_calls": source_cursor if replay_predicates else 0,
        "recognition_calls_definition": "rows classified through the precedence chain; not total predicate invocations",
        "predicate_calls": dict(predicate_calls),
        "predicate_passes": dict(predicate_passes),
        "generalized_three_ray_calls": predicate_calls["generalized-ray"],
        "generalized_three_ray_passes": predicate_passes["generalized-ray"],
        "stored_generalized_witnesses": 0,
        "chunks": receipts,
    }


def verify_stored_semantic_zip(*, progress: bool = False,
                               key_sink: KeySink | None = None,
                               _chunk_limit: int | None = None) -> dict[str, Json]:
    """Authenticate and zip every stored row without claiming predicate replay.

    ``key_sink`` is called in canonical source order as ``(partition, key)``,
    where partition is ``"owner"`` or ``"remainder"`` and key is
    ``(source_index, global_kernel, order_kernel, row_tuple, orbit_size)``.
    The callback is observational only; this module never publishes lane state.
    """
    return _verify(replay_predicates=False, progress=progress, chunk_limit=_chunk_limit,
                   key_sink=key_sink, reconstruct_census=False)


def reconstruct_census(*, replay_predicates: bool = False, progress: bool = False,
                       key_sink: KeySink | None = None,
                       _chunk_limit: int | None = None) -> dict[str, Json]:
    """Freshly reconstruct the exact census, optionally replaying all predicates."""
    require(type(replay_predicates) is bool, "replay_predicates must be an exact boolean")
    return _verify(replay_predicates=replay_predicates, progress=progress,
                   chunk_limit=_chunk_limit, key_sink=key_sink, reconstruct_census=True)


def replay_all_predicates(*, progress: bool = False,
                          key_sink: KeySink | None = None,
                          reconstruct_fresh_census: bool = False,
                          _chunk_limit: int | None = None) -> dict[str, Json]:
    """Run fresh predicates over an authenticated or freshly reconstructed census."""
    require(type(reconstruct_fresh_census) is bool,
            "reconstruct_fresh_census must be an exact boolean")
    return _verify(replay_predicates=True, progress=progress, chunk_limit=_chunk_limit,
                   key_sink=key_sink, reconstruct_census=reconstruct_fresh_census)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full-rescan", action="store_true",
                        help="freshly rerun every precedence-ordered ownership predicate")
    parser.add_argument("--reconstruct-census", action="store_true",
                        help="freshly regenerate and compare every exact census chunk")
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--emit-partition-stream", action="store_true",
                        help="run the combined replay and emit a fixed-framing O/R stream")
    parser.add_argument("--partition-output")
    args = parser.parse_args(argv)
    try:
        if args.emit_partition_stream:
            require(args.full_rescan and args.reconstruct_census and not args.progress,
                    "partition stream requires --full-rescan --reconstruct-census without progress")
            result = emit_combined_partition_stream(args.partition_output)
        else:
            require(args.partition_output is None,
                    "partition output path requires --emit-partition-stream")
            result = _verify(replay_predicates=args.full_rescan,
                             reconstruct_census=args.reconstruct_census,
                             progress=args.progress)
        sys.stdout.buffer.write(canonical_bytes(result))
        return 0
    except (KeyError, OSError, RuntimeError, TypeError, ValueError,
            UnicodeError, lzma.LZMAError) as error:
        sys.stderr.write(f"rank-seven order-nine structural replay: FAIL CLOSED: {error}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
