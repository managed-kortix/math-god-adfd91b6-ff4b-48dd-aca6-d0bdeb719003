#!/usr/bin/env python3
"""Dependency-free hostile mutations for the pure IV--XII packet verifier.

These focused tests exercise fail-closed parsers and semantic checks without
rerunning the ten-minute complete artifact replay.  The full verifier is run
separately in both ordinary and optimized Python.
"""

from __future__ import annotations

import dataclasses
import importlib.util
import json
import lzma
import sys
import tempfile
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Callable

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
VERIFIER = EXPERIMENTS / "verify_rank7_order8_packet_chain.py"


def load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("pure_packet_chain_verifier", VERIFIER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load pure packet-chain verifier")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


v = load()


def rejected(label: str, action: Callable[[], object]) -> None:
    try:
        action()
    except (RuntimeError, ValueError, ZeroDivisionError, OSError, EOFError, KeyError):
        return
    raise RuntimeError(f"hostile mutation accepted: {label}")


# Strict JSON and exact scalar types.
rejected("duplicate JSON key", lambda: v.strict_json(b'{"x":1,"x":2}\n', "duplicate"))
rejected("NaN JSON constant", lambda: v.strict_json(b'{"x":NaN}\n', "nan"))
rejected("non-ASCII JSON", lambda: v.strict_json(b'"\xff"\n', "non-ascii"))
rejected("bool laundered as integer", lambda: v.exact_int(True, "integer"))
rejected("float laundered as integer", lambda: v.exact_int(1.0, "integer"))
rejected("unsafe artifact path", lambda: v.safe_path(EXPERIMENTS, "../x", "../x", "path"))

# Packet schema mutations.
zero = [0] * 7
synthetic = {
    "denominator": 256,
    "branches": [zero[:] for _ in range(8)],
    "canonical": [[zero[:]] for _ in range(14)],
    "extended": [[zero[:], zero[:], zero[:]] for _ in range(14)],
}
rejected("zero denominator", lambda: v.decode_witness({**synthetic, "denominator": 0}, "w"))
rejected("unapproved denominator", lambda: v.decode_witness({**synthetic, "denominator": 257}, "w"))
short_branch = json.loads(json.dumps(synthetic))
short_branch["branches"][0].pop()
rejected("short branch vector", lambda: v.decode_witness(short_branch, "w"))
missing_path = json.loads(json.dumps(synthetic))
missing_path["canonical"].pop()
rejected("missing canonical path", lambda: v.decode_witness(missing_path, "w"))
extra_field = {**synthetic, "payload": 1}
rejected("extra witness field", lambda: v.decode_witness(extra_field, "w"))
rejected("antipodal exact step", lambda: v.exact_step_cost(
    (Fraction(1),) + (Fraction(0),) * 7,
    (Fraction(-1),) + (Fraction(0),) * 7,
))

# Source schema and regenerated-census binding.
edges = [[0, 1, 2], [0, 2, 2], [0, 3, 2], [1, 4, 2],
         [2, 5, 2], [3, 6, 2], [4, 7, 2]]
odds = [0] * len(edges)
support = tuple(a * (2 * 8 - a - 1) // 2 + b - a - 1 for a, b, _ in edges)
residual = (9, 10, support, (2,) * len(edges), tuple(odds), 1)
record = [0, 10, 9, edges, odds, 1]
v.source_record(record, (residual,), "valid synthetic source")
mutated = json.loads(json.dumps(record))
mutated[3][0] = mutated[3][1]
rejected("duplicate support edge", lambda: v.source_record(mutated, (residual,), "source"))
mutated = json.loads(json.dumps(record))
mutated[4][0] = 3
rejected("odd count exceeds multiplicity", lambda: v.source_record(mutated, (residual,), "source"))
mutated = json.loads(json.dumps(record))
mutated[5] = True
rejected("boolean orbit size", lambda: v.source_record(mutated, (residual,), "source"))
mutated = json.loads(json.dumps(record))
mutated[2] += 1
rejected("source differs from regenerated residual", lambda: v.source_record(mutated, (residual,), "source"))

# Exact dominant-family and virtual-IV topology checks.
entry = v.StreamEntry(record, v.canonical_bytes(record), residual)
key = v.family(record)
spec = dataclasses.replace(v.LANES[1], target=key, owner_total=1,
                           target_physical=1, dominance_rank=1,
                           source_total=1, remainder_total=0)
report = {"dominant_families": [v.family_object(key, 1, 1)]}
v.exact_dominant_report(report, spec, (entry,))
report["dominant_families"][0]["orbit_total"] = 2
rejected("mutated dominant-family census",
         lambda: v.exact_dominant_report(report, spec, (entry,)))
virtual_spec = dataclasses.replace(v.LANES[1], virtual_closed_target=key,
                                   virtual_closed_total=1, source_total=0)
v.verify_fifth_virtual_topology(
    virtual_spec, {"closed_source_family_total": 1}, (entry,), ())
rejected("broken virtual-IV complement",
         lambda: v.verify_fifth_virtual_topology(
             virtual_spec, {"closed_source_family_total": 1}, (entry,), (entry,)))

# Stream authentication must reject a duplicate owner even when hostile metadata
# is self-consistently rewritten to its new count and hashes.
owner = {
    "global_kernel": 9,
    "numerical_canonical_cost": 0.0,
    "orbit_size": 1,
    "source_index": 10,
    "stream_index": 0,
    "witness": synthetic,
}
with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    name = "owners.jsonl.xz"
    raw = v.canonical_bytes(owner) * 2
    artifact = lzma.compress(raw, format=lzma.FORMAT_XZ)
    (root / name).write_bytes(artifact)
    owner_spec = dataclasses.replace(v.LANES[0], owner_stream_name=name,
                                     owner_total=2, target=key)
    info = {
        "path": name,
        "record_total": 2,
        "raw_sha256": __import__("hashlib").sha256(raw).hexdigest(),
        "artifact_sha256": __import__("hashlib").sha256(artifact).hexdigest(),
    }
    rejected("duplicated owner with rewritten digests",
             lambda: v.read_owner_stream(root, owner_spec, info, {0: entry}))

# Optimization mode must not erase any gate: inspect the AST, not a substring.
import ast
for checked in (VERIFIER, Path(__file__)):
    tree = ast.parse(checked.read_text("ascii"), filename=str(checked))
    if any(isinstance(node, ast.Assert) for node in ast.walk(tree)):
        raise RuntimeError("optimization-removable assertion found")

print("PASS: 20 hostile packet-chain mutations rejected")
