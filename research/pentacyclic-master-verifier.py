#!/usr/bin/env python3
"""Fail-closed dependency audit for the complete pentacyclic theorem."""

import argparse
import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PAPER = ROOT / "all-pentacyclic-graphs" / "paper.tex"
RANK5_MASTER = HERE / "rank-five-order2-8-master-verifier.py"
OWNER_TRANSPORT = HERE / "doubled-c4-exceptional-owner-transport-verifier.py"

SOURCES = (
    ("paper", PAPER,
     "acc9c55a16c9d70f6d2a0ba3ea44cf76e0458cb6c76485f7d064bcb6ea4b0a93"),
    ("multiblock-sieve", ROOT / "positive-square-energy" / "pentacyclic-general"
     / "multiblock-induced-territory-theorem.md",
     "45be1db908392dfc046955f8649be09cb90a3e79ae309dfe8e1c36ccac4a4b84"),
    ("packet-reduction", ROOT / "positive-square-energy" / "pentacyclic-general"
     / "universal-block-tree-packet-reduction.md",
     "a338978a8c2c6480a1e28cfbbcec0211e9cb5764feac2e596df477031da15e98"),
    ("terminal-reduction", ROOT / "positive-square-energy" / "pentacyclic-general"
     / "four-residual-block-cut-terminal-reduction.md",
     "08c4d9b151a93ddeeb19e6e2e7239317342e72171a555158b22b2f2977986edc"),
    ("owner-closure", ROOT / "positive-square-energy" / "pentacyclic-general"
     / "four-residual-owner-exact-closure.md",
     "ede45392d454f37643dd1cd4ecfe421374a2dfa0ba74667cde64b4cbbde0f8fc"),
    ("doubled-c4-retained-packet", ROOT / "positive-square-energy"
     / "pentacyclic-general"
     / "doubled-c4-111-two-triangles-retained-packet.md",
     "ee760d3de23902bcabd2fb7844bce971a30c4aed04034fbf842f44268772ecf4"),
    ("doubled-triangle-gate", ROOT / "positive-square-energy" / "tricyclic-general"
     / "doubled-triangle-dnn-cover.md",
     "d2aa1f7ae2a2abc825cef0f7da82af15523e66c5bec9b4cc4fe8e3a042ee91dc"),
    ("doubled-c4-gate", ROOT / "positive-square-energy" / "tricyclic-general"
     / "doubled-c4-switching-sieve.md",
     "7d2b77857c9f90514ceda84e6acb01d4c752a7aecf39a1f553601b5376164d84"),
)

BLOCK_PARTITIONS = (
    ("1^5", "pentacyclic-cactus"),
    ("2+1^3", "multiblock-sieve+owner-closure"),
    ("2+2+1", "multiblock-sieve"),
    ("3+1+1", "multiblock-sieve+owner-closure"),
    ("3+2", "multiblock-sieve"),
    ("4+1", "multiblock-sieve"),
    ("5", "rank-five-master"),
)

ALL_LENGTH_GATES = (
    ("doubled-triangle-111", "doubled-triangle-gate", None,
     ("229/120<2", "31/20<2"),
     "longer-doubled-member-dnn;first-simple-owner-closure"),
    ("doubled-c4-exceptional-orbit", "doubled-c4-gate",
     "doubled-c4-retained-packet", ("1862/1000<2", "1662/1000<2"),
     "longer-doubled-member-dnn;first-simple-owner-isomorphism-closure"),
)

FOUR_RESIDUALS = (
    ("D+T+T+P", "positive-route-or-bridge-free", "D+T-anchor-minus-at-most-two-trees"),
    ("doubled-triangle-111+T+T", "longer-or-first-simple", "dnn-gate-or-owner-anchor"),
    ("doubled-c4-exceptional-orbit+T+T", "longer-or-first-simple",
     "dnn-gate-or-owner-isomorphism-anchor"),
    ("one-long-all-odd-K4+T+T", "positive-route-or-bridge-free", "owner-anchor-minus-two-trees"),
)

PAPER_REQUIRED = (
    r"1^5,\quad2+1^3,\quad2+2+1,\quad3+1+1,\quad3+2,\quad4+1,\quad5.",
    r"D+C_3+C_3+C_5,",
    r"B_{\rm DT}+C_3+C_3,",
    r"B_{\rm DC4}+C_3+C_3,",
    r"B_{K_4}+C_3+C_3.",
    "229/120<2", "31/20<2", "1862/1000<2", "1662/1000<2",
    "1&3&13&24&38&23&16&118",
    r"\boxed{\spn(G)\ge n}",
)

RANK5_FILE_SHA256 = "00f86cda32a7eb5a8a3863466d2ddcd5296a521ab7d3dcbd9c7633c3c911c669"
RANK5_REQUIRED = (
    "rank-five order-2-8 master verifier: all exact audits passed",
    "kernel_census: counts=1+3+13+24+38+23+16=118",
    "conclusion: s+(G)>=|V(G)| for every selected single-block family",
    "exact_dependency_manifest_sha256: c3203c8f300ee995e55a09f8b1b32b2f973f0475ff54e560738b7e8caac09d0c",
    "rejected_hostile_mutations: 9",
)
OWNER_TRANSPORT_FILE_SHA256 = "15288382816208fd46c7e85eb3171f724739ba794b98c3b618e7fed7154fbe54"
OWNER_TRANSPORT_OUTPUT_SHA256 = "2b11fb34c05eace618796558f1220cd3e17d1aaac4c173609a04f7b18a6ce2b0"
OWNER_TRANSPORT_MANIFEST_SHA256 = "ba504e0ead31921b7c5b9c2c220b423fc92c100cd54b53da7f236038d504f073"
OWNER_TRANSPORT_REQUIRED = (
    "doubled-C4 exceptional owner-transport verifier: all exact audits passed",
    "orbit: 8 anchors under 16 genuine incidence automorphisms",
    "switching_split: class 110=4; class 111=4",
    "connector_scope: arbitrary same-parity lengths; no switching operation",
    "canonical_transport_manifest_sha256: " + OWNER_TRANSPORT_MANIFEST_SHA256,
    "rejected_hostile_mutations: 5",
)
EXPECTED_MANIFEST_SHA256 = "1a35403e979a504776cf2aed6826f20e094173d1081ce3ce45a00ccbf24cfc56"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def source_locks(entries=SOURCES):
    require(entries == SOURCES, "multiblock source registry changed")
    records = []
    for name, path, digest in entries:
        require(path.is_file(), f"missing locked source: {name}")
        raw = path.read_bytes()
        require(hashlib.sha256(raw).hexdigest() == digest, f"locked source changed: {name}")
        records.append({"name": name, "path": str(path.relative_to(ROOT)), "sha256": digest})
    return records


def partition_ledger(entries=BLOCK_PARTITIONS):
    require(entries == BLOCK_PARTITIONS, "block-rank partition ledger changed")
    labels = tuple(label for label, unused_owner in entries)
    require(labels == ("1^5", "2+1^3", "2+2+1", "3+1+1", "3+2", "4+1", "5"),
            "block-rank partition is not exhaustive")
    require(len(labels) == len(set(labels)), "block-rank partition overlaps")
    require(entries[-1] == ("5", "rank-five-master"), "single-block owner changed")
    require(all("multiblock" in owner or owner == "pentacyclic-cactus"
                for unused_label, owner in entries[:-1]), "multiblock owner gap")
    return {label: owner for label, owner in entries}


def all_length_gate_ledger(entries=ALL_LENGTH_GATES, source_entries=SOURCES):
    require(entries == ALL_LENGTH_GATES, "all-length gate registry changed")
    source_names = {name for name, unused_path, unused_digest in source_entries}
    owner_text = (ROOT / "positive-square-energy" / "pentacyclic-general"
                  / "four-residual-owner-exact-closure.md").read_text(encoding="ascii")
    records = []
    for family, source, retained_packet, bounds, disposition in entries:
        require(source in source_names, f"all-length gate source is unlocked: {family}")
        source_path = next(path for name, path, unused_digest in source_entries if name == source)
        text = source_path.read_text(encoding="ascii")
        require(all(bound.split("<", 1)[0] in text and bound in owner_text for bound in bounds),
                f"all-length gate changed: {family}")
        if family == "doubled-c4-exceptional-orbit":
            require(retained_packet in source_names,
                    "doubled-C4 retained packet is not directly source-locked")
            packet_path = next(path for name, path, unused_digest in source_entries
                               if name == retained_packet)
            packet = packet_path.read_text(encoding="ascii")
            required = ("010011", "010101", "011010", "011100", "100011",
                        "100101", "101010", "101100", "class `110`",
                        "class `111`", "physical graph-isomorphism transport",
                        "Arbitrary connector-only lengthening")
            require(all(token in packet for token in required),
                    "doubled-C4 retained-packet transport ledger changed")
        require(disposition in {
            "longer-doubled-member-dnn;first-simple-owner-closure",
            "longer-doubled-member-dnn;first-simple-owner-isomorphism-closure",
        }, f"all-length gate disposition changed: {family}")
        records.append({"family": family, "source": source,
                        "retained_packet": retained_packet, "bounds": list(bounds),
                        "disposition": disposition})
    require(len(records) == 2, "all-length gate count changed")
    return records


def residual_ledger(entries=FOUR_RESIDUALS):
    require(entries == FOUR_RESIDUALS, "four-residual closure ledger changed")
    require(len(entries) == 4 and len({entry[0] for entry in entries}) == 4,
            "four-residual closure is not exact")
    closure = (ROOT / "positive-square-energy" / "pentacyclic-general"
               / "four-residual-owner-exact-closure.md").read_text(encoding="ascii")
    required = ("multiblock residual is empty", "direct/direct", "direct/nested",
                "positive route", "interior-owner orbit")
    require(all(token in closure for token in required), "owner-exact closure ledger changed")
    return [{"family": family, "split": split, "closure": owner}
            for family, split, owner in entries]


def paper_gates(required=PAPER_REQUIRED):
    require(required == PAPER_REQUIRED, "paper theorem gate registry changed")
    text = PAPER.read_text(encoding="ascii")
    require(all(token in text for token in required), "paper theorem ledger changed")
    return list(required)


def invoke_owner_transport(path=OWNER_TRANSPORT, digest=OWNER_TRANSPORT_FILE_SHA256,
                           output_digest=OWNER_TRANSPORT_OUTPUT_SHA256,
                           required=OWNER_TRANSPORT_REQUIRED):
    require(path == OWNER_TRANSPORT, "owner-transport verifier path changed")
    require(digest == OWNER_TRANSPORT_FILE_SHA256,
            "owner-transport verifier digest policy changed")
    require(output_digest == OWNER_TRANSPORT_OUTPUT_SHA256,
            "owner-transport output digest policy changed")
    require(required == OWNER_TRANSPORT_REQUIRED,
            "owner-transport acceptance ledger changed")
    require(path.is_file(), "missing owner-transport verifier")
    require(hashlib.sha256(path.read_bytes()).hexdigest() == digest,
            "owner-transport verifier changed")
    optimize = ("-O",) if sys.flags.optimize else ()
    completed = subprocess.run((sys.executable, *optimize, str(path), "--emit"),
                               check=False, capture_output=True, text=True)
    require(completed.returncode == 0, "owner-transport verifier failed")
    require(completed.stderr == "", "owner-transport verifier wrote stderr")
    require(hashlib.sha256(completed.stdout.encode("ascii")).hexdigest() == output_digest,
            "owner-transport canonical output changed")
    require(all(line in completed.stdout for line in required),
            "owner-transport acceptance ledger changed")
    return {"file_sha256": digest, "output_sha256": output_digest,
            "manifest_sha256": OWNER_TRANSPORT_MANIFEST_SHA256,
            "required_lines": list(required)}


def invoke_rank5(path=RANK5_MASTER, digest=RANK5_FILE_SHA256,
                 required=RANK5_REQUIRED):
    require(path == RANK5_MASTER, "rank-five master path changed")
    require(digest == RANK5_FILE_SHA256, "rank-five master digest policy changed")
    require(required == RANK5_REQUIRED, "rank-five acceptance ledger changed")
    require(path.is_file(), "missing rank-five master verifier")
    require(hashlib.sha256(path.read_bytes()).hexdigest() == digest,
            "rank-five master verifier changed")
    optimize = ("-O",) if sys.flags.optimize else ()
    completed = subprocess.run((sys.executable, *optimize, str(path), "--emit"),
                               check=False, capture_output=True, text=True)
    require(completed.returncode == 0, "rank-five master verifier failed")
    require(completed.stderr == "", "rank-five master verifier wrote stderr")
    require(all(line in completed.stdout for line in required),
            "rank-five master acceptance ledger changed")
    return {"file_sha256": digest,
            "output_sha256": hashlib.sha256(completed.stdout.encode("ascii")).hexdigest(),
            "required_lines": list(required)}


def audit(sources=SOURCES, partitions=BLOCK_PARTITIONS, gates=ALL_LENGTH_GATES,
          residuals=FOUR_RESIDUALS, expected_digest=EXPECTED_MANIFEST_SHA256):
    require(expected_digest == EXPECTED_MANIFEST_SHA256, "manifest digest policy changed")
    manifest = {
        "schema": "pentacyclic-master-fail-closed-v1",
        "paper_sha256": SOURCES[0][2],
        "source_locks": source_locks(sources),
        "block_rank_partition": partition_ledger(partitions),
        "all_length_gates": all_length_gate_ledger(gates, sources),
        "four_residual_closure": residual_ledger(residuals),
        "paper_required_ledger": paper_gates(),
        "doubled_c4_owner_transport": invoke_owner_transport(),
        "rank_five_master": invoke_rank5(),
        "scope": "every finite simple connected graph with |E|=|V|+4",
        "conclusion": "s+(G)>=|V(G)|",
    }
    digest = hashlib.sha256(canonical_bytes(manifest)).hexdigest()
    require(digest == expected_digest, "exact dependency manifest digest changed")
    return manifest, digest


def expect_rejected(action, label):
    try:
        action()
    except (IndexError, KeyError, OSError, RuntimeError, StopIteration, TypeError, ValueError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_self_checks():
    mutations = 0
    for index, entry in enumerate(SOURCES):
        candidate = SOURCES[:index] + SOURCES[index + 1:]
        expect_rejected(lambda candidate=candidate: source_locks(candidate),
                        f"source omitted: {entry[0]}")
        mutations += 1
    changed = list(deepcopy(SOURCES))
    changed[4] = (changed[4][0], changed[4][1], "0" * 64)
    expect_rejected(lambda: source_locks(tuple(changed)), "owner closure digest changed")
    mutations += 1
    changed = list(deepcopy(SOURCES))
    changed[5] = (changed[5][0], changed[5][1], "0" * 64)
    expect_rejected(lambda: source_locks(tuple(changed)), "retained packet digest changed")
    mutations += 1
    changed_partitions = list(BLOCK_PARTITIONS)
    changed_partitions.pop(4)
    expect_rejected(lambda: partition_ledger(tuple(changed_partitions)), "partition omitted")
    mutations += 1
    changed_partitions = list(BLOCK_PARTITIONS)
    changed_partitions[-1] = ("5", "multiblock-sieve")
    expect_rejected(lambda: partition_ledger(tuple(changed_partitions)), "rank-five owner moved")
    mutations += 1
    changed_gates = list(deepcopy(ALL_LENGTH_GATES))
    changed_gates[0] = (changed_gates[0][0], changed_gates[0][1], changed_gates[0][2],
                        ("229/120<2",), changed_gates[0][4])
    expect_rejected(lambda: all_length_gate_ledger(tuple(changed_gates)),
                    "gate bound omitted")
    mutations += 1
    changed_residuals = FOUR_RESIDUALS[:-1]
    expect_rejected(lambda: residual_ledger(changed_residuals), "residual family omitted")
    mutations += 1
    expect_rejected(lambda: paper_gates(PAPER_REQUIRED[:-1]), "paper conclusion omitted")
    mutations += 1
    expect_rejected(lambda: invoke_owner_transport(digest="0" * 64),
                    "owner-transport digest changed")
    mutations += 1
    expect_rejected(lambda: invoke_owner_transport(required=OWNER_TRANSPORT_REQUIRED[:-1]),
                    "owner-transport acceptance line omitted")
    mutations += 1
    expect_rejected(lambda: invoke_rank5(digest="0" * 64), "rank-five digest changed")
    mutations += 1
    expect_rejected(lambda: invoke_rank5(required=RANK5_REQUIRED[:-1]),
                    "rank-five acceptance line omitted")
    mutations += 1
    expect_rejected(lambda: audit(expected_digest="0" * 64), "manifest digest changed")
    mutations += 1
    return mutations


def report(digest, mutations):
    return "\n".join((
        "pentacyclic master verifier: all fail-closed dependency audits passed",
        "paper_lock: all-pentacyclic-graphs/paper.tex",
        "block_partition: 1^5 | 2+1^3 | 2+2+1 | 3+1+1 | 3+2 | 4+1 | 5",
        "multiblock_sources: sieve -> packet reduction -> terminal reduction -> owner-exact closure",
        "all_length_gates: doubled-triangle 229/120,31/20; doubled-C4 exceptional orbit 1862/1000,1662/1000",
        "retained_packet: eight doubled-C4 anchors locked; owner-isomorphism transport checked",
        "four_residuals: exact ledger closed; multiblock residual empty",
        "rank_five_master: 1+3+13+24+38+23+16=118 kernels accepted",
        "global_scope: every finite simple connected graph with |E|=|V|+4",
        "conclusion: s+(G)>=|V(G)|",
        f"exact_dependency_manifest_sha256: {digest}",
        f"rejected_hostile_mutations: {mutations}",
    )) + "\n"


def optimized_output():
    completed = subprocess.run((sys.executable, "-O", str(Path(__file__).resolve()), "--emit"),
                               check=False, capture_output=True, text=True)
    require(completed.returncode == 0, "python -O pentacyclic master failed")
    require(completed.stderr == "", "python -O pentacyclic master wrote stderr")
    return completed.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--print-manifest", action="store_true")
    args = parser.parse_args()
    manifest, digest = audit()
    mutations = hostile_self_checks()
    require(mutations == 20, "hostile mutation count changed")
    output = report(digest, mutations)
    if not args.emit and sys.flags.optimize == 0:
        require(optimized_output() == output, "normal and python -O output differ")
    if args.print_manifest:
        sys.stdout.write(canonical_bytes(manifest).decode("ascii"))
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
