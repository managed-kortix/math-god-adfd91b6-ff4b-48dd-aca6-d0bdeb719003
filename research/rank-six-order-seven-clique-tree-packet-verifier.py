#!/usr/bin/env python3
"""Audit the 37 historical clique/tree candidates as redundant DNN rows.

This is deliberately not a structural packet verifier.  In particular, the
old discovery idea did not prove that its K4 packet survives lengthening a K4
edge.  The order-seven theorem does not need that claim: the source-locked
batched certificates and equality templates give exact DNN coverage of every
target on all 37 rows.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "fixtures" / "rank-six-order-seven-tetra-antichain.json"
SOURCE_SHA256 = "4ccdb97c3eeace00d64b0ccc25cdff25f548226cdaa61e19c5a9305fa56f7099"
EQUALITY_PATH = HERE / "rank-six-order-seven-equality-frontier-verifier.py"
EXPECTED_EXCEPTION = (511, 14191, (None, 2, 5))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def locked_candidates():
    raw = SOURCE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, "antichain source digest changed")
    payload = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(payload), "antichain source is not canonical JSON")
    require(payload["full_theorem"] is False and payload["candidate_row_total"] == 37,
            "candidate source scope changed")
    candidates = [(row["kernel"], tuple(row["row"])) for row in payload["antichain"]
                  if row["clique_tree_candidates"]]
    require(len(candidates) == len(set(candidates)) == 37, "candidate extraction changed")
    return set(candidates)


def audit():
    candidates = locked_candidates()
    equality = load_module(EQUALITY_PATH, "rank6_order7_candidate_redundancy")
    artifact = load_module(equality.BATCHED_ENGINE, "rank6_order7_candidate_artifact")

    # This rechecks all six digest-locked chunks, every rational witness, the
    # complete 319202-target key set, and all 39 exact equality templates.
    equality.audit()

    records = {}
    for name, stored_digest, _ in equality.CHUNKS:
        raw = artifact.artifact_bytes(equality.CHUNK_DIR / name, stored_digest)
        payload = json.loads(raw.decode("ascii"))
        for record in payload["records"]:
            key = record["kernel"], tuple(record["row"])
            if key in candidates:
                require(key not in records, "candidate appears in two chunks")
                records[key] = record
    require(set(records) == candidates, "batched manifest does not contain all candidates")

    closures = {}
    raw = equality.FIXTURE.read_bytes()
    fixture = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(fixture), "equality fixture is not canonical JSON")
    for closure in fixture["records"]:
        closures[closure["source_index"]] = tuple(closure["frontiers"])

    shared_rows = equality_rows = batched_targets = equality_targets = 0
    exception = None
    for record in records.values():
        require(type(record["source_index"]) is int, "noninteger source index")
        require(type(record["exact_target_total"]) is int, "noninteger exact subtotal")
        if record["exact_target_total"] == 13:
            require(record["shared_witness"] is not None
                    and record["individual_witnesses"] is None,
                    "fully covered candidate is not in shared-witness mode")
            shared_rows += 1
            batched_targets += 13
            continue
        require(record["shared_witness"] is None, "partial candidate has a shared witness")
        individual = record["individual_witnesses"]
        require(type(individual) is list and len(individual) == 13,
                "partial candidate frontier width changed")
        frontiers = (None, *range(12))
        missing = tuple(frontier for frontier, witness in zip(frontiers, individual)
                        if witness is None)
        observed = record["kernel"], record["source_index"], missing
        require(observed == EXPECTED_EXCEPTION, "candidate DNN exception changed")
        require(closures.get(record["source_index"]) == missing,
                "equality fixture does not close the candidate exception")
        exception = observed
        equality_rows += 1
        batched_targets += record["exact_target_total"]
        equality_targets += len(missing)

    require((shared_rows, equality_rows, batched_targets, equality_targets)
            == (36, 1, 478, 3), "candidate coverage partition changed")
    require(exception == EXPECTED_EXCEPTION, "expected equality row is absent")
    return shared_rows, equality_rows, batched_targets, equality_targets


def report(result):
    shared_rows, equality_rows, batched_targets, equality_targets = result
    return ("rank-six order-seven clique/tree candidate redundancy audit passed\n"
            f"candidate_rows=37 shared_exact_rows={shared_rows} equality_rows={equality_rows}\n"
            f"candidate_targets=481 batched_exact={batched_targets} equality_exact={equality_targets}\n"
            "structural_packet_dependency=false theorem_dependency=false\n")


def main():
    output = report(audit())
    if sys.flags.optimize == 0 and "--emit" not in sys.argv:
        completed = subprocess.run([sys.executable, "-O", __file__, "--emit"], check=False,
                                   capture_output=True, text=True)
        require(completed.returncode == 0 and completed.stderr == "", "optimized audit failed")
        require(completed.stdout == output, "normal and optimized outputs differ")
    sys.stdout.write(output)


if __name__ == "__main__":
    try:
        main()
    except (IndexError, KeyError, TypeError, ValueError, ZeroDivisionError) as error:
        raise RuntimeError(f"fail-closed malformed input: {error}") from error
