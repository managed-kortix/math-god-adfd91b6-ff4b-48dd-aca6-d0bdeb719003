#!/usr/bin/env python3
"""Fail-closed exact replay of the rank-seven/order-eight direct packs.

This child does not trust scheduler ``exact_audit`` flags.  It pins every
runtime source and input artifact, strictly decodes the authenticated residual
cache and owner ledgers, requires canonical R7O8G1 re-encoding, and replays all
shared witnesses with ``fractions.Fraction``.  The deterministic receipt binds
each selected owner position to the complete source-row identity and decoded
record.  It contains no clocks, host data, or other runtime-dependent fields.
"""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import importlib.util
import json
import lzma
import sys
from pathlib import Path
from typing import Any, NoReturn

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SCHEDULER_RESULTS = HERE / "rank7_order8_scheduler" / "results"
ENGINE_PATH = HERE / "rank7_order8_exact_rational.py"
BASE_PATH = HERE / "rank6_order10_cubic_exact_rational.py"
LANES_PATH = HERE / "rank7_order8_payload_free_lanes.py"
ATOM_PATH = HERE / "rank7_order7_symbolic_atom_recognizer.py"
MANIFEST_PATH = HERE / "rank7_order8_exact_residual_census_manifest.json"
SEARCH_INDICES_PATH = HERE / "rank7_order8_rational_search_indices.json"
CACHE_PATH = HERE / "rank7_order8_rational_search_cache.r7o8c.xz"
LEDGER_PATH = HERE / "rank7_order8_combined_owner_ledger.json"
OWNER_INDICES_PATH = HERE / "rank7_order8_combined_owner_indices.json.xz"
UNION_REPORT_PATH = HERE / "rank7_order8_lane_union.json.xz"
SCHEMA = "rank-seven-order-eight-direct-pack-exact-replay-v1"
OWNER_SCHEMA = "rank-seven-order-eight-combined-owner-indices-v1"
UNION_SCHEMA = "rank-seven-order-eight-lane-union-v1"
LEDGER_SCHEMA = "rank-seven-order-eight-combined-owner-ledger-v1"
EXPECTED_ROWS = 29000
EXPECTED_TARGETS = 435000
EXPECTED_STREAM_ROWS = 492812
EXPECTED_SOURCE_STREAM = "53c64c930846c92d8a4f35e5c228c60afb4c56c1a35009cfec60eaf2ffba6ee3"

SOURCE_PINS = {
    "exact_rational_engine": (ENGINE_PATH, "0577103afb8be3f9f90d0635a37266281c9496a5b5d1d3349cb0c74ccdc1b8e5"),
    "exact_rational_base": (BASE_PATH, "fb419856225aeb513285ae5467233b1cccc096b9632170c6bbfac905abf08827"),
    "payload_free_lanes": (LANES_PATH, "278884b76bf490dc55f92a3c775565a74c3a94f67cf62178378af8899eff239c"),
    "atom_recognizer": (ATOM_PATH, "10de4fb714c15756341a7dbddb5a4da9f8ce5e0393aacc9e9434d619ebce9734"),
}
ARTIFACT_PINS = {
    "residual_manifest": (MANIFEST_PATH, "5d41e78a2f688f4c3064cb88f1d6d475008d36c84f892edc4cba28ade424fe98"),
    "rational_search_indices": (SEARCH_INDICES_PATH, "245cceaab164ba9c2a604d0db8b09a65598fd52084b1df2363911c6d1d4d3a59"),
    "residual_cache": (CACHE_PATH, "0e31fb87d7bfa8e01d8cf168240cb2cc164673628f2c22b9e14347186cea7502"),
    "combined_owner_ledger": (LEDGER_PATH, "5700803dd3989853440291423a6cae736978125cbcf3a13ffa89281e7b5ea84e"),
    "combined_owner_indices": (OWNER_INDICES_PATH, "1dacaf02fc546c634ba879bdd1af49774040d963e09a40331bba77bdff50c6d5"),
    "lane_union_report": (UNION_REPORT_PATH, "ca60c847f59d0d0c52fe411944852f3134debc39384f88daae95be67d84b32a9"),
}
EXPECTED_PACKS = (('rank7_order8_chunk_000000_005000.r7o8g.xz', (0, 5000), '22e7b473ab295f75470587a00319f0624bfee3882ba6621d737b86b81e3f52aa', '2f3773dc99c930f9aeacff1e3566e037eb6d7d106d866e81a829c1b53797a2ee', None, None), ('rank7_order8_chunk_005000_006000.r7o8g.xz', (5000, 6000), '06e5d982fb54bb4ca946b36ea6d58d9d9cd96b5b2a6131bd534de185412e4213', 'ebb98d15ce6917d958357646ce202333171c181954edff08d8ef23c1bae757dc', 'shard-005000_006000.json', 'fd2682b2885eac94e8b364a08fd72b4b29f23291be9541d9b4be5f98fc31bc1f'), ('rank7_order8_chunk_006000_007000.r7o8g.xz', (6000, 7000), '2c32100325826a14082cf7549622f0577e6f7a5ebe957c53e3b5d3c8806fd800', '0f07f2a9876c7cd13e84afd6a89ac59470dcf17653d509e5233cc17504b50b40', 'shard-006000_007000.json', 'ea79f4a49d1908f1ad10d2233bf3fbf00444b1cf2af05942f9ccf78fc816feea'), ('rank7_order8_chunk_007000_008000.r7o8g.xz', (7000, 8000), '2488b01ee7d0c192f58176ef1833771a1a5b505d2a7bca190fb7e0dc168fecef', 'aadc313e0062984998f42cef6b9c0e05ea222ee5b4d14676befd1782c9eeb562', 'shard-007000_008000.json', '2e0b6a6be8ee9443b7ade05f640e11321ae93bb07c7dab15426319979a6684aa'), ('rank7_order8_chunk_008000_009000.r7o8g.xz', (8000, 9000), '2a6bae92d56b2b0067b20d4b2e4d0557740a5fc85f77c7fa54f28f867288e60e', '4ff35e6fe5cc00e6ce0b9bd9172d1c743eaca449619a6f3fbf6b40214dd122aa', 'shard-008000_009000.json', 'c37ec3a7a9b2c875030b355452a4059ae42e01857f037b2ee971f28f4132db98'), ('rank7_order8_chunk_009000_010000.r7o8g.xz', (9000, 10000), 'f80798728e73610fcaf54e3d31ce8fb6db8019498b07a61bffc23f93aab3e683', 'b8caa832fd10d1a1daad1e2e08a56173f480034e32d3220ce893d857af3c66b4', 'shard-009000_010000.json', '9e69bad3a7bed7728575698917342d93ff8a32c5959af7e2d61a9f2cb38d8938'), ('rank7_order8_chunk_010000_011000.r7o8g.xz', (10000, 11000), 'eb97ec5b43595fd390a43c02f71286bddfe99ef353fd1a72ca8be7871adbe356', 'a0b4dcb3a419c5d253a6f956b4e88f30691f08eb15098a83ffbe4e59a3f222e5', 'shard-010000_011000.json', '4be02c4cf0e7997bd183af2029ddeb53eab233cd9452a762727fc4c423e760f1'), ('rank7_order8_chunk_011000_012000.r7o8g.xz', (11000, 12000), '6944cf622f8a9641c1d9f9cb67569a0789cde31ae81dd2c86a2865caefa764e9', '1e9687fde846d8c7a0e4cffc494e19797e81828c4b9d33459ee5d0049f0e9960', 'shard-011000_012000.json', 'd36d223df8c9ecee0f63e92b3e0080dfb1859c6b863017e562a00d65fbabd089'), ('rank7_order8_chunk_012000_013000.r7o8g.xz', (12000, 13000), '8e5d7f56a8763c28c7b200f1305e7500ca07f5be10cf4d189ce8789e56037e4a', '059422c9d307b73ef9212a41bc86a8b3f4090bab91166effceb77d0d97631da0', 'shard-012000_013000.json', '2402db3cf362937eef01634dfdd115a192608076ee04a51a7a8d12c460235431'), ('rank7_order8_chunk_013000_014000.r7o8g.xz', (13000, 14000), 'f9d80a6a54bdfb995acb66483ca01cecc02ac13687f45e5dae6e9df5b93b2e6a', '737338245bc3905400de0fcff05b60fed5efce5f0fb49661d3b7ff05d2a6cdef', 'shard-013000_014000.json', 'f14e5355b7919f8a1ae84cee9ca13f38c419fab76db1da2a58b5411db4095e10'), ('rank7_order8_chunk_014000_015000.r7o8g.xz', (14000, 15000), '7018e6e1e1e73cdaacba1ae18f83cfb8bfb3a72272b92f7e2a7f5447218b18c3', '7ef49463417ed18d0cc8a2d33c08f97cdeae2669decd0d4d6a094fc5f7e56828', 'shard-014000_015000.json', 'd403397e89c77b9c10131ee5b67e51676976d075611db307f23592cb77865dc9'), ('rank7_order8_chunk_015000_016000.r7o8g.xz', (15000, 16000), 'a59712d44123c764c03296990992dd983ee53adffaa6d7782b96a05374a6c5bf', '5ffa9b2cd1b9338e76896a2bf3ed2aa28f194e4ebfa44ec7841da17a55573dba', 'shard-015000_016000.json', '414cc1dee32caa2b84a122b7390ee351564d21b6522eebf662009733213370af'), ('rank7_order8_chunk_016000_017000.r7o8g.xz', (16000, 17000), '69f8b06378543de3b78d7c7fc682cceb9fcffac0f951588421962d5778dfa2c3', 'a1d84b9c1b3fba1ffe03e79ade40799c6fa9621ce6d2a0ffb01de8f63d6a600b', 'shard-016000_017000.json', '06013d557c1c421db3ca71dc140ec19e21d29164c294faade01bd6c18cfff349'), ('rank7_order8_chunk_017000_018000.r7o8g.xz', (17000, 18000), '794af16328bc03a69fc6c6d9939ce2866dbd67fc4633d74312a702e22039b5e2', 'e0f42c942e4fc3bc6ec2e9d7306bfb3a20c4bf131cdc92334c41b8cbd25f0c0d', 'shard-017000_018000.json', 'fee40d8e09c3c2ec260f8608495e23e651e0e5bac525d843aa77a0be83402b90'), ('rank7_order8_chunk_018000_019000.r7o8g.xz', (18000, 19000), 'a234c14c9e943df40369f569666abc30235da58793580e9d23cf6d682a342707', 'c5b5f2a32198eacc881283d643fc2dc8a49a2dab1f64adfdde34485678e441f7', 'shard-018000_019000.json', 'f417ed88bd4c0f695dbb2cbfaecd1604a77512add77aaede411ab58033d4f0f1'), ('rank7_order8_chunk_019000_020000.r7o8g.xz', (19000, 20000), '9f9ae2229b470a0b9090fc9818f42313a1524b7dd1ba222e9221206d7e8fa723', 'c23d03512d211611aa74d926f21fdbf5c18fcc10a746bd15be4684ea030b36d7', 'shard-019000_020000.json', 'a64249fdde27885439a021c774c7c1c3397e19b87368db021a382ed38c7a2796'), ('rank7_order8_chunk_020000_021000.r7o8g.xz', (20000, 21000), '21bed48a35fd2390d69b45ebaa2d3d3f190779c319ce234e13222f6b8212ad8d', '5b38b8459ffa703afa36f0ab16e3b3f694aab42fc85f72c87898c90ca230ea4f', 'shard-020000_021000.json', '62ef51875ccaa0bae38491de3e9eff1de30175ead6618e0c112d9fca17b1abfa'), ('rank7_order8_chunk_021000_022000.r7o8g.xz', (21000, 22000), '4b3f76c6f429a194b08b4399588fc11906933d4ae8bb2b59915e0ea8c7fbbb68', '66e7b42ad106c52b378bf5f7386e49ac1127d57c3110ac2a1d7a4d0232d5e13d', 'shard-021000_022000.json', '45ce54a040e848b0c481f5a74ad1dcdc84c01f42e00e783fa26d4134e06e06d6'), ('rank7_order8_chunk_022000_023000.r7o8g.xz', (22000, 23000), 'ce4f1c9b56e32be075f3c5a571856fbfd50d23b9e258258228957a9899e81c7b', '11d9d2e476809c093189f1d318d277e111ec75adbf04cbc907a345d0463273f1', 'shard-022000_023000.json', '1ddb918a361cd74b0ddf386d84a1095177a0bc4b4da7318023f74b4eb1f452e2'), ('rank7_order8_chunk_023000_024000.r7o8g.xz', (23000, 24000), '8284f60f41dc7766cca969f8a552410002f5ed80e3123413b41d6be6aac9e806', '8770ac2bcaf5525c27ded483173fc55aa3be10a9b850f5eebe525def5e8bc77c', 'shard-023000_024000.json', '8967f820aa920a9a4eb83ba965002405dd10dddd2cd7c6998a6256d00b33e67f'), ('rank7_order8_chunk_024000_025000.r7o8g.xz', (24000, 25000), 'dbbce85adc822f45349eba3af3bca04611810c38f9eadb7c59f62aee53204f6d', '607f24f2e3a0c24aca83167e9a893946374b0986d89fa200def1106a090fa229', 'shard-024000_025000.json', '3395e94cf28594d7550610f71bce67c1ccfaa9c1e8ca32ea83afedd0647b2651'), ('rank7_order8_chunk_025000_026000.r7o8g.xz', (25000, 26000), '0d84790e08a15b63c76581784cdabce574496e641e9c273a0f344c05f90129cd', 'c1c50956629e5ede0bd55e228d9b8ae962ff999ca1a74c75e4125710b6eaf3bb', 'shard-025000_026000.json', '1fe9dc4e3efe06ed567a64f221e11e2eb907b012e7bb63f8b484bb5f5c97a5f2'), ('rank7_order8_chunk_026000_027000.r7o8g.xz', (26000, 27000), '54ecfdbbd40782e65c90ab4e77ca0738d15a6436c87e71176d4ade7e881db935', '556662b76d1123952e32a718e663f7345d390328e8282b9d9024f3ad1882f575', 'shard-026000_027000.json', '442283afedb3482e066460754366034c4f40795e4404efb0261e9a464805d5dd'), ('rank7_order8_chunk_027000_028000.r7o8g.xz', (27000, 28000), 'c17a1b88ad02da30037915d457bc61c647760b5a7f37c425841335f2a1e1ac2f', '76101b7c09055daeb70e5927d4b635c8696218a618f318d968a3633c74edadfa', 'shard-027000_028000.json', '5d6583d1a71bb8a34ce65c4454552f533a60063ed84b368c78f963eba60034e0'), ('rank7_order8_chunk_028000_029000.r7o8g.xz', (28000, 29000), 'b9acd50788a0910062acfadc96ca7b6a26d37f42dbad7f0510745022e2ed11fa', 'fda5797f94a5fbb7edc965ab46d009556e46ea8427430b34bc6291e81fe6a1fd', 'shard-028000_029000.json', '4c8c7e7f28f6d1fce2cbba15a97af7d609cd62f241b3418c7f2843972392081e'))


def fail(message: str) -> NoReturn:
    raise RuntimeError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")


def stream_line(value: Any) -> bytes:
    return canonical_bytes(value)


def strict_json(raw: bytes, label: str, canonical: bool = True) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            require(type(key) is str and key not in result,
                    f"{label}: duplicate or non-string key")
            result[key] = value
        return result
    try:
        value = json.loads(raw.decode("ascii"), object_pairs_hook=pairs,
                           parse_constant=lambda token: fail(
                               f"{label}: non-finite token {token}"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"{label}: invalid strict ASCII JSON") from error
    if canonical:
        require(raw == canonical_bytes(value), f"{label}: noncanonical JSON")
    return value


def decompressed(path: Path, label: str) -> tuple[bytes, bytes]:
    stored = path.read_bytes()
    try:
        raw = lzma.decompress(stored, format=lzma.FORMAT_XZ)
    except lzma.LZMAError as error:
        raise RuntimeError(f"{label}: invalid XZ stream") from error
    return stored, raw


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_inputs() -> dict[str, str]:
    result = {}
    for name, (path, expected) in {**SOURCE_PINS, **ARTIFACT_PINS}.items():
        require(path.is_file(), f"missing pinned input: {path.name}")
        actual = sha256(path.read_bytes())
        require(actual == expected, f"pinned input changed: {path.name}")
        result[name] = actual
    return result


def audit_assert_free() -> dict[str, str]:
    result = {}
    for name, (path, expected) in SOURCE_PINS.items():
        raw = path.read_bytes()
        require(sha256(raw) == expected, f"proof source changed: {path.name}")
        try:
            tree = ast.parse(raw.decode("utf-8"), str(path))
        except (UnicodeDecodeError, SyntaxError) as error:
            raise RuntimeError(f"cannot parse proof source: {path.name}") from error
        assertions = [node.lineno for node in ast.walk(tree) if isinstance(node, ast.Assert)]
        require(not assertions, f"optimization-sensitive assert in {path.name}: {assertions}")
        result[name] = expected
    return result


def load_ledgers() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    ledger_raw = LEDGER_PATH.read_bytes()
    ledger = strict_json(ledger_raw, LEDGER_PATH.name)
    owner_stored, owner_raw = decompressed(OWNER_INDICES_PATH, OWNER_INDICES_PATH.name)
    union_stored, union_raw = decompressed(UNION_REPORT_PATH, UNION_REPORT_PATH.name)
    require(sha256(owner_stored) == ARTIFACT_PINS["combined_owner_indices"][1] and
            sha256(owner_raw) == ledger["combined_indices"]["raw_sha256"],
            "owner-index stored/raw identity changed")
    require(sha256(union_stored) == ARTIFACT_PINS["lane_union_report"][1] and
            sha256(union_raw) == ledger["union_report"]["raw_sha256"],
            "union-report stored/raw identity changed")
    owners = strict_json(owner_raw, OWNER_INDICES_PATH.name)
    union = strict_json(union_raw, UNION_REPORT_PATH.name)
    require(ledger.get("schema") == LEDGER_SCHEMA and ledger.get("full_theorem") is False and
            ledger.get("source_stream_sha256") == EXPECTED_SOURCE_STREAM and
            ledger.get("targets_per_residual") == 15 and
            ledger.get("exclusive_owner_row_counts", {}).get("direct-rational") == EXPECTED_ROWS and
            ledger.get("exclusive_owner_target_counts", {}).get("direct-rational") == EXPECTED_TARGETS,
            "combined owner ledger scope changed")
    require(owners.get("schema") == OWNER_SCHEMA and
            owners.get("source_stream_sha256") == EXPECTED_SOURCE_STREAM and
            owners.get("stream_index_scope") ==
            "authenticated 492812-row payload-free complement",
            "combined owner indices scope changed")
    require(union.get("schema") == UNION_SCHEMA and
            union.get("source_stream_sha256") == EXPECTED_SOURCE_STREAM and
            union.get("universe", {}).get("rational_search_total") == EXPECTED_STREAM_ROWS,
            "lane union scope changed")
    expected_records = []
    for name, interval, raw_digest, stored_digest, manifest, manifest_digest in EXPECTED_PACKS:
        authentication = ({"kind": "pinned-baseline-sha256"} if manifest is None else
                          {"kind": "scheduler-result", "path": manifest,
                           "sha256": manifest_digest})
        expected_records.append({"authentication": authentication, "path": name,
                                 "raw_sha256": raw_digest, "row_range": list(interval),
                                 "xz_sha256": stored_digest})
    require(ledger.get("direct_rational_artifacts") == expected_records and
            union.get("direct_rational_artifacts") == expected_records,
            "direct-pack ledger changed")
    direct = owners.get("exclusive_stream_indices", {}).get("direct-rational")
    require(type(direct) is list and direct == list(range(EXPECTED_ROWS)),
            "selected direct owner stream is not exactly [0,29000)")
    return ledger, owners, union


def audit_scheduler_manifests() -> list[dict[str, Any]]:
    receipts = []
    for name, interval, _raw_digest, stored_digest, manifest, manifest_digest in EXPECTED_PACKS:
        if manifest is None:
            continue
        path = SCHEDULER_RESULTS / manifest
        raw = path.read_bytes()
        require(sha256(raw) == manifest_digest, f"scheduler manifest changed: {manifest}")
        payload = strict_json(raw, manifest, canonical=False)
        require(type(payload) is dict and set(payload) == {
                    "completed_at", "exact_audit", "output", "output_sha256",
                    "range", "rows", "schema", "status"} and
                payload["schema"] == "rank-seven-order-eight-shard-result-v1" and
                payload["status"] == "completed" and payload["exact_audit"] is True and
                payload["output"] == name and payload["output_sha256"] == stored_digest and
                payload["range"] == list(interval) and
                payload["rows"] == interval[1] - interval[0],
                f"scheduler manifest semantics changed: {manifest}")
        receipts.append({"path": manifest, "sha256": manifest_digest})
    require(len(receipts) == 24, "scheduler manifest total changed")
    return receipts


def cache_get_uvarint(raw: bytes, position: int) -> tuple[int, int]:
    start = position
    value = shift = 0
    while True:
        require(position < len(raw) and shift <= 4096,
                "cache: truncated or excessive varint")
        byte = raw[position]
        position += 1
        value |= (byte & 0x7f) << shift
        if not byte & 0x80:
            require(position - start == 1 or byte != 0,
                    "cache: nonminimal unsigned varint")
            return value, position
        shift += 7


def strict_decode_cache(engine: Any, census: Any) -> tuple[tuple[Any, ...], str]:
    stored, raw = decompressed(CACHE_PATH, CACHE_PATH.name)
    require(sha256(stored) == ARTIFACT_PINS["residual_cache"][1], "cache XZ changed")
    magic = engine.CACHE_MAGIC
    header = len(magic)
    require(raw[:header] == magic and raw[header:header + 32] ==
            bytes.fromhex(census.SOURCE_SHA256), "cache header changed")
    digest_start, payload_start = header + 32, header + 64
    require(raw[digest_start:payload_start] == hashlib.sha256(raw[payload_start:]).digest(),
            "cache payload digest changed")
    position = payload_start
    count, position = cache_get_uvarint(raw, position)
    require(count == EXPECTED_STREAM_ROWS, "cache row count changed")
    rows = []
    previous_source = -1
    for _ in range(count):
        global_kernel, position = cache_get_uvarint(raw, position)
        source_index, position = cache_get_uvarint(raw, position)
        width, position = cache_get_uvarint(raw, position)
        require(0 < width <= len(census.PAIRS), "cache support width changed")
        support, multiplicities, parity = [], [], []
        for _ in range(width):
            dense, position = cache_get_uvarint(raw, position)
            multiplicity, position = cache_get_uvarint(raw, position)
            odd, position = cache_get_uvarint(raw, position)
            require(dense < len(census.PAIRS) and multiplicity > 0 and odd <= multiplicity,
                    "cache contains nonphysical source row")
            support.append(dense); multiplicities.append(multiplicity); parity.append(odd)
        orbit_size, position = cache_get_uvarint(raw, position)
        require(source_index > previous_source and orbit_size > 0 and
                all(left < right for left, right in zip(support, support[1:])),
                "cache source stream is noncanonical")
        previous_source = source_index
        rows.append((global_kernel, source_index, tuple(support), tuple(multiplicities),
                     tuple(parity), orbit_size, None, False))
    require(position == len(raw), "cache has trailing bytes")
    rows_tuple = tuple(rows)
    require(engine.cache_bytes(census, rows_tuple) == raw,
            "strict cache canonical re-encoding changed")
    return rows_tuple, sha256(raw)


def source_identity(stream_index: int, source: tuple[Any, ...]) -> dict[str, Any]:
    return {"global_kernel": source[0], "multiplicities": list(source[3]),
            "orbit_size": source[5], "parity_row": list(source[4]),
            "source_index": source[1], "stream_index": stream_index,
            "support": list(source[2])}


def witness_identity(mode: int, witness: tuple[Any, ...]) -> dict[str, Any]:
    denominator, branches, canonical, extended = witness
    def integers(rows: Any) -> Any:
        return [[value.numerator * (denominator // value.denominator) for value in row]
                for row in rows]
    return {"branches": integers(branches),
            "canonical": [integers(path) for path in canonical],
            "denominator": denominator,
            "extended": [integers(path) for path in extended],
            "mode": mode}


def row_binding(stream_index: int, source: tuple[Any, ...], record: tuple[Any, ...]) -> dict[str, Any]:
    mode, witness = record
    return {"owner": source_identity(stream_index, source),
            "record": witness_identity(mode, witness)}


def replay() -> dict[str, Any]:
    pins = pin_inputs()
    assert_free = audit_assert_free()
    _ledger, owners, _union = load_ledgers()
    scheduler = audit_scheduler_manifests()
    engine = load_module("rank7_order8_direct_pack_engine", ENGINE_PATH)
    require(Path(engine.BASE_PATH).resolve() == BASE_PATH.resolve() and
            Path(engine.LANES_PATH).resolve() == LANES_PATH.resolve() and
            engine.ORDER == engine.DIMENSION == 8 and engine.PATH_COUNT == 14 and
            engine.BUDGET.numerator == 6 and engine.BUDGET.denominator == 1,
            "engine constants or linkage changed")
    require(engine.base.MODE_SHARED == 1 and engine.base.PATH_COUNT == 14 and
            engine.base.BUDGET == engine.BUDGET,
            "base exact-verifier constants changed")
    census = engine.load_census_module()
    residuals, cache_raw_sha = strict_decode_cache(engine, census)
    require(len(residuals) == EXPECTED_STREAM_ROWS and
            census.SOURCE_SHA256 == EXPECTED_SOURCE_STREAM,
            "authenticated residual stream changed")
    direct = owners["exclusive_stream_indices"]["direct-rational"]
    cursor = 0
    global_owner_digest = hashlib.sha256()
    global_replay_digest = hashlib.sha256()
    pack_receipts = []
    mode_total = target_total = 0
    for name, interval, expected_raw, expected_stored, manifest, manifest_digest in EXPECTED_PACKS:
        require(interval[0] == cursor and interval[1] > cursor,
                f"pack interval gap/overlap: {name}")
        path = HERE / name
        stored, raw = decompressed(path, name)
        require(sha256(stored) == expected_stored and sha256(raw) == expected_raw,
                f"pack bytes changed: {name}")
        start, records = engine.base.decode_pack(census, raw, residuals)
        require(start == interval[0] and start + len(records) == interval[1],
                f"embedded pack interval changed: {name}")
        require(raw == engine.base.encode_pack(census, start, records),
                f"pack is not canonical: {name}")
        owner_digest = hashlib.sha256()
        replay_digest = hashlib.sha256()
        record_digest = hashlib.sha256()
        for local, record in enumerate(records):
            index = start + local
            require(direct[index] == index, "owner position does not select replayed row")
            source = residuals[index]
            mode, witness = record
            require(mode == engine.base.MODE_SHARED and witness is not None,
                    f"non-shared direct record at stream index {index}")
            # This is the expensive theorem-evidence step: reconstruct every
            # rational unit vector and every one of 15 exact frontier costs.
            engine.base.verify_record(census, source, record)
            owner_raw = stream_line(source_identity(direct[index], residuals[direct[index]]))
            replay_owner_raw = stream_line(source_identity(index, source))
            require(owner_raw == replay_owner_raw,
                    f"owner/source field mismatch at stream index {index}")
            binding_raw = stream_line(row_binding(index, source, record))
            owner_digest.update(owner_raw); replay_digest.update(replay_owner_raw)
            global_owner_digest.update(owner_raw); global_replay_digest.update(replay_owner_raw)
            record_digest.update(binding_raw)
            mode_total += 1; target_total += 15
        require(owner_digest.digest() == replay_digest.digest(),
                f"pack owner/replay row digest mismatch: {name}")
        pack_receipts.append({
            "authentication": ({"kind": "pinned-baseline-sha256"} if manifest is None else
                               {"kind": "scheduler-result", "path": manifest,
                                "sha256": manifest_digest}),
            "owner_row_stream_sha256": owner_digest.hexdigest(),
            "path": name, "raw_sha256": expected_raw,
            "record_binding_stream_sha256": record_digest.hexdigest(),
            "replay_row_stream_sha256": replay_digest.hexdigest(),
            "row_range": list(interval), "rows": len(records),
            "shared_rows": len(records), "targets": len(records) * 15,
            "xz_sha256": expected_stored})
        cursor = interval[1]
    require(cursor == EXPECTED_ROWS and mode_total == EXPECTED_ROWS and
            target_total == EXPECTED_TARGETS,
            "direct-pack aggregate coverage changed")
    require(global_owner_digest.digest() == global_replay_digest.digest(),
            "aggregate selected-owner/replay linkage changed")
    return {
        "assert_free_source_sha256": assert_free,
        "coverage": {"gap_free_row_range": [0, EXPECTED_ROWS],
                     "mode_shared_rows": mode_total, "packs": len(pack_receipts),
                     "scheduler_manifests": len(scheduler), "targets": target_total},
        "execution_semantics": "fresh_canonical_decode_and_exact_fraction_replay",
        "input_sha256": pins,
        "owner_linkage": {
            "field_set": ["stream_index", "source_index", "global_kernel", "support",
                          "multiplicities", "parity_row", "orbit_size"],
            "owner_row_stream_sha256": global_owner_digest.hexdigest(),
            "replay_row_stream_sha256": global_replay_digest.hexdigest(),
            "selected_owner_indices": "exactly_list(range(29000))",
            "status": "field-for-field-identical"},
        "pack_receipts": pack_receipts,
        "residual_cache_raw_sha256": cache_raw_sha,
        "schema": SCHEMA,
        "status": "passed",
    }


def expect_rejected(action: Any, label: str) -> None:
    try:
        action()
    except (RuntimeError, TypeError, ValueError, lzma.LZMAError):
        return
    fail(f"hostile mutation accepted: {label}")


def self_test() -> dict[str, Any]:
    pin_inputs()
    audit_assert_free()
    engine = load_module("rank7_order8_direct_pack_selftest", ENGINE_PATH)
    census = engine.load_census_module()
    residuals, _ = strict_decode_cache(engine, census)
    name, interval, expected_raw, expected_stored, _manifest, _digest = EXPECTED_PACKS[-1]
    stored, raw = decompressed(HERE / name, name)
    require(sha256(stored) == expected_stored and sha256(raw) == expected_raw,
            "self-test seed changed")
    start, records = engine.base.decode_pack(census, raw, residuals)
    require((start, start + len(records)) == interval, "self-test seed range changed")
    # A semantically unchanged but nonminimal start varint must be rejected by
    # canonical re-encoding; a witness mutation must fail exact Fraction replay.
    header = len(engine.MAGIC) + 32
    old_start, after_start = engine.base.get_uvarint(raw, header)
    encoded_start = bytearray()
    engine.base.put_uvarint(encoded_start, old_start)
    require(raw[header:after_start] == bytes(encoded_start), "seed start varint changed")
    # Add a redundant zero continuation group to the canonical varint.
    noncanonical_start = bytes(encoded_start[:-1]) + bytes([encoded_start[-1] | 128, 0])
    noncanonical = raw[:header] + noncanonical_start + raw[after_start:]
    mutated_start, mutated_records = engine.base.decode_pack(census, noncanonical, residuals)
    require((mutated_start, mutated_records) == (start, records),
            "noncanonical mutation changed semantics")
    expect_rejected(lambda: require(noncanonical == engine.base.encode_pack(
        census, mutated_start, mutated_records), "noncanonical pack"),
        "nonminimal pack varint")
    mode, witness = records[0]
    denominator, branches, canonical, extended = witness
    # Force an antipodal first step on the first path.  exact_step_cost must
    # reject it before any budget comparison.
    paths = engine.base.path_ledger(census, residuals[start])
    path_index = next(index for index, values in enumerate(canonical) if values)
    first_u = paths[path_index][2]
    first_branch = engine.base.rational_unit(branches[first_u])
    antipode = tuple(-value for value in first_branch)
    antipode_parameters = tuple(value / (1 + antipode[0]) for value in antipode[1:])
    changed_canonical = list(canonical)
    changed_path = list(changed_canonical[path_index])
    changed_path[0] = antipode_parameters
    changed_canonical[path_index] = tuple(changed_path)
    changed = (mode, (denominator, branches, tuple(changed_canonical), extended))
    expect_rejected(lambda: engine.base.verify_record(census, residuals[start], changed),
                    "changed exact witness")
    expect_rejected(lambda: strict_json(b'{"a":1,"a":2}\n', "duplicate"),
                    "duplicate JSON key")
    require(row_binding(start, residuals[start], records[0]) !=
            row_binding(start + 1, residuals[start], records[0]),
            "row binding ignores stream position")
    return {"assert_free_sources": len(SOURCE_PINS), "hostile_mutations_rejected": 4,
            "schema": "rank-seven-order-eight-direct-pack-self-test-v1",
            "status": "passed"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    payload = self_test() if args.self_test else replay()
    sys.stdout.buffer.write(canonical_bytes(payload))


if __name__ == "__main__":
    try:
        main()
    except (KeyError, IndexError, TypeError, ValueError, ZeroDivisionError) as error:
        raise RuntimeError(f"fail-closed malformed input: {error}") from error
