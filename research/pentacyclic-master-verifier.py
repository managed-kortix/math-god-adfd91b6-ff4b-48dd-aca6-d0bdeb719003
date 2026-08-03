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

SOURCES = (
    ("paper", PAPER,
     "37d8f872b52b780944287ccc4dd62cb791140cc4416de5f723e170944bbef9ca"),
    ("multiblock-sieve", ROOT / "positive-square-energy" / "pentacyclic-general"
     / "multiblock-induced-territory-theorem.md",
     "4fec6c4d8bef4ad4822d0979464fe149d5021b3975f89b17f8f7b4b413de0beb"),
    ("packet-reduction", ROOT / "positive-square-energy" / "pentacyclic-general"
     / "universal-block-tree-packet-reduction.md",
     "94f0333d2250a9c11d3a9e911b93762d95e053922c723a1870306301b5849645"),
    ("terminal-reduction", ROOT / "positive-square-energy" / "pentacyclic-general"
     / "four-residual-block-cut-terminal-reduction.md",
     "ba06aeaff3ab130ee1e46d0e8b3271b1b01790f2622d927bd72e2f5f7390b4e8"),
    ("owner-closure", ROOT / "positive-square-energy" / "pentacyclic-general"
     / "four-residual-owner-exact-closure.md",
     "8fdc10a3e0200e1bda471dff3c4f7d56e477cfd84b16ce97cef1fbdfd76d76fc"),
    ("doubled-triangle-gate", ROOT / "positive-square-energy" / "tricyclic-general"
     / "doubled-triangle-dnn-cover.md",
     "032c79461a8f36e54917a2349be87292b41d5a3bc07167862311e4db2f0cfd48"),
    ("doubled-c4-gate", ROOT / "positive-square-energy" / "tricyclic-general"
     / "doubled-c4-switching-sieve.md",
     "86a484208a0931aa20cf35d9ac875574be6fd51d240e9d71e4b48c7d9239815d"),
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

CANONICAL_GATES = (
    ("doubled-triangle-111", "doubled-triangle-gate",
     ("229/120<2", "31/20<2"), "noncanonical-dnn;canonical-owner-closure"),
    ("doubled-c4-111", "doubled-c4-gate",
     ("1862/1000<2", "1662/1000<2"), "noncanonical-dnn;canonical-owner-closure"),
)

FOUR_RESIDUALS = (
    ("D+T+T+P", "positive-route-or-bridge-free", "D+T-anchor-minus-at-most-two-trees"),
    ("doubled-triangle-111+T+T", "noncanonical-or-canonical", "dnn-gate-or-owner-anchor"),
    ("doubled-c4-111+T+T", "noncanonical-or-canonical", "dnn-gate-or-owner-anchor"),
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
EXPECTED_MANIFEST_SHA256 = "19926bb35e4989b4b18258dddb18659f5b6c38010f5df08a33dee5342fa03bd0"


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


def canonical_gate_ledger(entries=CANONICAL_GATES, source_entries=SOURCES):
    require(entries == CANONICAL_GATES, "canonical gate registry changed")
    source_names = {name for name, unused_path, unused_digest in source_entries}
    owner_text = (ROOT / "positive-square-energy" / "pentacyclic-general"
                  / "four-residual-owner-exact-closure.md").read_text(encoding="ascii")
    records = []
    for family, source, bounds, disposition in entries:
        require(source in source_names, f"canonical gate source is unlocked: {family}")
        source_path = next(path for name, path, unused_digest in source_entries if name == source)
        text = source_path.read_text(encoding="ascii")
        require(all(bound.split("<", 1)[0] in text and bound in owner_text for bound in bounds),
                f"canonical all-length gate changed: {family}")
        require(disposition == "noncanonical-dnn;canonical-owner-closure",
                f"canonical gate disposition changed: {family}")
        records.append({"family": family, "source": source, "bounds": list(bounds),
                        "disposition": disposition})
    require(len(records) == 2, "canonical gate count changed")
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


def audit(sources=SOURCES, partitions=BLOCK_PARTITIONS, gates=CANONICAL_GATES,
          residuals=FOUR_RESIDUALS, expected_digest=EXPECTED_MANIFEST_SHA256):
    require(expected_digest == EXPECTED_MANIFEST_SHA256, "manifest digest policy changed")
    manifest = {
        "schema": "pentacyclic-master-fail-closed-v1",
        "paper_sha256": SOURCES[0][2],
        "source_locks": source_locks(sources),
        "block_rank_partition": partition_ledger(partitions),
        "canonical_all_length_gates": canonical_gate_ledger(gates, sources),
        "four_residual_closure": residual_ledger(residuals),
        "paper_required_ledger": paper_gates(),
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
    changed_partitions = list(BLOCK_PARTITIONS)
    changed_partitions.pop(4)
    expect_rejected(lambda: partition_ledger(tuple(changed_partitions)), "partition omitted")
    mutations += 1
    changed_partitions = list(BLOCK_PARTITIONS)
    changed_partitions[-1] = ("5", "multiblock-sieve")
    expect_rejected(lambda: partition_ledger(tuple(changed_partitions)), "rank-five owner moved")
    mutations += 1
    changed_gates = list(deepcopy(CANONICAL_GATES))
    changed_gates[0] = (changed_gates[0][0], changed_gates[0][1], ("229/120<2",),
                        changed_gates[0][3])
    expect_rejected(lambda: canonical_gate_ledger(tuple(changed_gates)), "gate bound omitted")
    mutations += 1
    changed_residuals = FOUR_RESIDUALS[:-1]
    expect_rejected(lambda: residual_ledger(changed_residuals), "residual family omitted")
    mutations += 1
    expect_rejected(lambda: paper_gates(PAPER_REQUIRED[:-1]), "paper conclusion omitted")
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
        "canonical_gates: doubled-triangle 229/120,31/20; doubled-C4 1862/1000,1662/1000",
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
    require(mutations == 16, "hostile mutation count changed")
    output = report(digest, mutations)
    if not args.emit and sys.flags.optimize == 0:
        require(optimized_output() == output, "normal and python -O output differ")
    if args.print_manifest:
        sys.stdout.write(canonical_bytes(manifest).decode("ascii"))
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
