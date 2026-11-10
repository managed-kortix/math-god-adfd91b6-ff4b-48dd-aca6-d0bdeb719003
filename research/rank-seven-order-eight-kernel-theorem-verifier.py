#!/usr/bin/env python3
"""Fail-closed gate for the rank-seven/order-eight single-block theorem.

The gate composes four independently pinned read-only exact certificate replays
with the rank-seven analytic reduction and the final induced-territory proof.
Its base-owner bridge intentionally treats four historical producer artifacts
as immutable trust roots; this is not a fresh semantic rerun of those searches.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import lzma
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, NoReturn

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = ROOT / "positive-square-energy" / "experiments"
HEPTACYCLIC = ROOT / "positive-square-energy" / "heptacyclic-general"
SELF = Path(__file__).resolve()

BASE = EXPERIMENTS / "rank7_order8_typed_precedence_bridge.py"
STRUCTURAL = EXPERIMENTS / "rank7_order8_structural_exact_verifier.py"
PACKETS = EXPERIMENTS / "verify_rank7_order8_packet_chain.py"
POST_XII = EXPERIMENTS / "rank7_order8_post_xii_shared_packet_lane.py"
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
FINITE = ROOT / "research" / "tricyclic-finite-rational-certificates-verifier.py"
K4 = EXPERIMENTS / "k4_all_odd_exact_verify.py"
DOUBLED_TRIANGLE = ROOT / "research" / "doubled-triangle-all-length-certificate.py"
GRAM = ROOT / "research" / "tricyclic-gram-obstruction-verifier.py"

# Every executed verifier and every mathematical source is bound to exact bytes.
SOURCE_SHA256 = {
    "base_verifier": "f99c94d3781539fba444f91bedf6c6bba14ba96f0541e51d8c8d0877220eba03",
    "structural_verifier": "46851a4aa58d0b0ed0a3f63d0b0839755c057c0c4c671acf204011bd312b9415",
    "packet_verifier": "4410a45fb514831a0828e9064d091f0c6ee1ff17d037ee4cf611af0e4f3f7a87",
    "post_xii_verifier": "a8903c69287a531d5a4aa62fa514318daad0583c3690a7dcb20d62384ac60fd1",
    "rank_seven_reduction": "f1daf9109f4843aa2db149c974fb21c847bb6f8144275201aebabed7fe4ea516",
    "singleton_territory": "9d7385473e5a2f32700f44aed86e7a06039012932b75f6812c28717c04b25238",
    "tricyclic_tex": "13f8f8c7996c0f58f764c52b4a5b915132038e2ce38d3e56285f1bf952990fc1",
    "tricyclic_pdf": "57c876516e891cd74b016da495ed26200a137cd073296961b3170c95e84a76cc",
    "tricyclic_audit": "6e5bee956c412454fd9dc59e020b5dfe35205c336a6c0e740aea96f0f90fa92f",
    "tricyclic_readme": "4de20b0a78f7598dc8172a118eaf178272494a9ee13cfbabc3fbabfa688a3f15",
    "finite_verifier": "fe272e94ee5d1ad549fe29b498f785df9fc298352ccfb3e67a1e4967461fde16",
    "k4_verifier": "0e4ef323a076c807a5aba0c80f0e385e5c3cee18ebd4d7e249928b345e6745a4",
    "doubled_triangle_verifier": "a27981b5bf6381edf6a8760477e6c99828bc9934d1d135d488670c35493b199d",
    "gram_verifier": "aeec6f4471a0a78b6807275217ee22e9909f07a8e356d8126c03ea175d9a8126",
}
SOURCE_PATHS = {
    "base_verifier": BASE,
    "structural_verifier": STRUCTURAL,
    "packet_verifier": PACKETS,
    "post_xii_verifier": POST_XII,
    "rank_seven_reduction": REDUCTION,
    "singleton_territory": TERRITORY,
    "tricyclic_tex": TRICYCLIC_TEX,
    "tricyclic_pdf": TRICYCLIC_PDF,
    "tricyclic_audit": TRICYCLIC_AUDIT,
    "tricyclic_readme": TRICYCLIC_README,
    "finite_verifier": FINITE,
    "k4_verifier": K4,
    "doubled_triangle_verifier": DOUBLED_TRIANGLE,
    "gram_verifier": GRAM,
}

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
    "29,000 direct-rational witness packs",
)
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


def audit_source_pins() -> None:
    require(set(SOURCE_PATHS) == set(SOURCE_SHA256), "source registry changed")
    for name, path in SOURCE_PATHS.items():
        require(path.is_file(), f"missing dependency: {name}")
        require(digest(path) == SOURCE_SHA256[name], f"dependency bytes changed: {name}")


def audit_no_asserts() -> int:
    checked = [SELF, BASE, STRUCTURAL, PACKETS, POST_XII, FINITE, K4,
               DOUBLED_TRIANGLE, GRAM]
    for path in checked:
        try:
            tree = ast.parse(path.read_text("ascii"), filename=str(path))
        except (OSError, UnicodeError, SyntaxError) as error:
            raise RuntimeError(f"cannot parse proof-critical source: {path.name}") from error
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
            tuple(payload.get("digest_pinned_not_recomputed", ())) == BASE_TRUST_ROOTS,
            "base bridge receipt changed")


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
    if not full:
        # Quick mode is a true integration gate: source bytes, artifacts, schemas,
        # ASTs, and proof text were checked above.  These exact output digests are
        # receipts from prior independent normal/-O executions; no expensive
        # semantic child is rerun here.
        require(CHILD_OUTPUT_SHA256 == {
            "base": "fd5a5bc5434af1e8c1f82da7f69b5c71e6b8234826d73bdc4c08e3c7cfd874fa",
            "structural": "412fbe20b7435c19897363cd3263f7b4080b79886e5cd811a4ecdbb6a147ad57",
            "packets": "0d15bd6d6addc534b160ae624555620e37a76a3e023d2c2f04e9696d23f3dd78",
            "finite": "86f4ad87b1cc5a84817d630f2fb448045ce207d345c185c7b96bf38895c4a617",
            "k4": "cb5434669fd3aacea9ca07e7a4d75f076a63a19f718806b394234996f52b95f7",
            "doubled_triangle": "a0b9311d8173972c4ac529c326366391ae5df9928079824ff5c0a6c601848222",
        }, "quick-mode child output receipt registry changed")
        return 0, 0

    children = (
        ("base", BASE, ("--hostile",), CHILD_OUTPUT_SHA256["base"], validate_base),
        ("structural", STRUCTURAL, (), CHILD_OUTPUT_SHA256["structural"], None),
        ("packets", PACKETS, (), CHILD_OUTPUT_SHA256["packets"], None),
        ("finite", FINITE, (), CHILD_OUTPUT_SHA256["finite"], None),
        ("k4", K4, (), CHILD_OUTPUT_SHA256["k4"], None),
        ("doubled_triangle", DOUBLED_TRIANGLE, (),
         CHILD_OUTPUT_SHA256["doubled_triangle"], None),
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
        "verification_mode": "full-read-only-replay" if full else "quick-pinned-artifact-gate",
        "child_receipt_sha256": CHILD_OUTPUT_SHA256,
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
            "fresh semantic recomputation of the four pinned base producer artifacts",
        ],
        "source_sha256": SOURCE_SHA256,
        "artifact_sha256": ARTIFACT_SHA256,
        "certificate_sha256": CERTIFICATE_SHA256,
    }


def audit(full: bool) -> dict[str, Json]:
    audit_source_pins()
    ast_sources = audit_no_asserts()
    report = audit_post_artifacts()
    audit_math_sources()
    audit_accounting(report)
    child_count, executions = run_children(full)
    return manifest(full, child_count, executions, ast_sources)


def expect_rejection(action: Any, label: str) -> None:
    try:
        action()
    except (KeyError, OSError, RuntimeError, TypeError, ValueError,
            UnicodeError, lzma.LZMAError):
        return
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
        "trust_boundary=four pinned base producer artifacts; not fresh producer recomputation",
        "conclusion=s+(G)>=|V(G)| for rank-seven kernel order eight only",
        "nonclaim=no orders 9-12, no multiblock, no all-heptacyclic conclusion",
        f"hostile_mutations_rejected={rejected}",
        f"child_manifest_sha256={manifest_digest}",
    )) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true",
                        help="also replay all 54,597 post-XII packets in normal and -O")
    parser.add_argument("--print-manifest", action="store_true")
    parser.add_argument("--optimized-master-child", action="store_true",
                        help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        result = audit(args.full)
        rejected = hostile_self_checks()
        require(rejected == 12, "hostile mutation count changed")
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
