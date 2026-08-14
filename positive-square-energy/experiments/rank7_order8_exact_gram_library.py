#!/usr/bin/env python3
"""Mine and audit a finite exact Gram library for rank-seven/order-eight rows.

The first completed 5,000-row pack is the only witness source.  A template is
an exact rational branch Gram, reconstructed from its stereographic parameters.
Rows are indexed by permutation-invariant support/parity signatures.  A hit
reuses the complete rational waypoint formula, not merely its numerical Gram.
The pack auditor checks every rational step and all fifteen costs exactly.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import lzma
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ENGINE_PATH = HERE / "rank7_order8_exact_rational.py"
DEFAULT_PACK = HERE / "rank7_order8_chunk_000000_005000.r7o8g.xz"
DEFAULT_OUTPUT = HERE / "rank7_order8_exact_gram_library_coverage.json"
SCHEMA = "rank-seven-order-eight-exact-gram-library-coverage-v1"
EXPECTED_PACK_SHA256 = "2f3773dc99c930f9aeacff1e3566e037eb6d7d106d866e81a829c1b53797a2ee"
MINE_ROWS = 5000
TARGETS_PER_ROW = 15
F = Fraction


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_engine():
    spec = importlib.util.spec_from_file_location("rank7_order8_library_engine", ENGINE_PATH)
    require(spec is not None and spec.loader is not None, "cannot load exact witness engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def pair(value):
    return value.numerator, value.denominator


def row_data(engine, census, source):
    edges = tuple((*census.PAIRS[dense], multiplicity, odd)
                  for dense, multiplicity, odd in zip(source[2], source[3], source[4]))
    incident = [[] for _ in range(engine.ORDER)]
    for u, v, multiplicity, odd in edges:
        label = multiplicity, odd
        incident[u].append(label)
        incident[v].append(label)
    fingerprints = tuple(tuple(sorted(values)) for values in incident)
    signature = (tuple(sorted((multiplicity, odd)
                              for _, _, multiplicity, odd in edges)),
                 tuple(sorted(fingerprints)))
    order = tuple(sorted(range(engine.ORDER), key=lambda vertex: (fingerprints[vertex], vertex)))
    position = {vertex: index for index, vertex in enumerate(order)}
    cells = []
    for _, group in itertools.groupby(order, key=lambda vertex: fingerprints[vertex]):
        cells.append(tuple(group))
    return signature, edges, order, tuple(cells)


def degree_signature(engine, edges):
    degrees = [0] * engine.ORDER
    odd_degrees = [0] * engine.ORDER
    imbalance_degrees = [0] * engine.ORDER
    for u, v, multiplicity, odd in edges:
        signed = multiplicity - 2 * odd
        for vertex in (u, v):
            degrees[vertex] += multiplicity
            odd_degrees[vertex] += odd
            imbalance_degrees[vertex] += signed
    return (tuple(sorted(zip(degrees, odd_degrees, imbalance_degrees))),
            tuple(sorted((multiplicity, odd) for _, _, multiplicity, odd in edges)))


def gram_from_witness(engine, witness):
    _, parameters, _, _ = witness
    vectors = tuple(engine.base.rational_unit(row) for row in parameters)
    gram = tuple(tuple(engine.base.dot(left, right) for right in vectors) for left in vectors)
    require(all(gram[i][i] == 1 for i in range(engine.ORDER)), "nonunit mined Gram")
    require(all(gram[i][j] == gram[j][i]
                for i in range(engine.ORDER) for j in range(engine.ORDER)),
            "nonsymmetric mined Gram")
    return gram


def normalized_keys(edges, order, cells, permutation_cap):
    count = 1
    for cell in cells:
        count *= __import__("math").factorial(len(cell))
    choices = ((itertools.permutations(cell) if count <= permutation_cap else (cell,))
               for cell in cells)
    result = set()
    for blocks in itertools.product(*choices):
        permutation = tuple(itertools.chain.from_iterable(blocks))
        position = {vertex: index for index, vertex in enumerate(permutation)}
        result.add(tuple(sorted((min(position[u], position[v]),
                                 max(position[u], position[v]), multiplicity, odd)
                                for u, v, multiplicity, odd in edges)))
    require(result, "row has no normalized support orientation")
    return tuple(sorted(result))


def load_templates(engine, census, residuals, pack_path, permutation_cap):
    stored = pack_path.read_bytes()
    require(hashlib.sha256(stored).hexdigest() == EXPECTED_PACK_SHA256,
            "first-5000 witness pack changed")
    try:
        raw = lzma.decompress(stored, format=lzma.FORMAT_XZ)
    except lzma.LZMAError as error:
        raise RuntimeError("witness pack is not valid XZ") from error
    start, records = engine.base.exact_decode_pack(census, raw, residuals)
    require(start == 0 and len(records) == MINE_ROWS and
            all(mode == engine.base.MODE_SHARED for mode, _ in records),
            "witness mining range or modes changed")
    templates = defaultdict(dict)
    degree_templates = defaultdict(list)
    orientation_total = 0
    for index, ((_, witness), source) in enumerate(zip(records, residuals[:MINE_ROWS])):
        signature, edges, order, cells = row_data(engine, census, source)
        gram = gram_from_witness(engine, witness)
        keys = normalized_keys(edges, order, cells, permutation_cap)
        gram_digest = hashlib.sha256(canonical_bytes(
            [[list(pair(value)) for value in row] for row in gram])).hexdigest()
        for key in keys:
            templates[signature].setdefault(key, (index, gram_digest))
        degree_templates[degree_signature(engine, edges)].append((index, gram_digest))
        orientation_total += len(keys)
    return templates, degree_templates, orientation_total


def scan(engine, census, residuals, templates, degree_templates, pack_path,
         permutation_cap, progress=False):
    owner_counts = Counter()
    signature_rows = Counter()
    uncovered_signatures = Counter()
    degree_signature_rows = Counter()
    classification = hashlib.sha256()
    for index, source in enumerate(residuals):
        signature, edges, order, cells = row_data(engine, census, source)
        signature_rows[signature] += 1
        coarse = degree_signature(engine, edges)
        degree_signature_rows[coarse] += 1
        owner = None
        owner_gram = None
        candidates = templates.get(signature, {})
        for key in normalized_keys(edges, order, cells, permutation_cap):
            if key in candidates:
                owner, owner_gram = candidates[key]
                break
        if owner is None:
            uncovered_signatures[signature] += 1
        else:
            owner_counts[owner] += 1
        classification.update(canonical_bytes([index, source[1], owner,
                                                owner_gram]))
        if progress and (index + 1) % 25000 == 0:
            print(f"rows={index + 1} covered={sum(owner_counts.values())}", flush=True)
    covered = sum(owner_counts.values())
    used = sorted(owner_counts)
    reused = sum(count for count in owner_counts.values() if count > 1)
    maximum = max(owner_counts.values(), default=0)
    return {
        "schema": SCHEMA,
        "full_theorem": covered == len(residuals),
        "scope": "authenticated rational-search complement of payload-free lanes",
        "source_stream_sha256": census.SOURCE_SHA256,
        "source_pack": pack_path.name,
        "source_pack_sha256": hashlib.sha256(pack_path.read_bytes()).hexdigest(),
        "mined_row_range": [0, MINE_ROWS],
        "mined_exact_witness_total": MINE_ROWS,
        "support_parity_signature_total": len(templates),
        "degree_signature_total": len(degree_templates),
        "exact_structural_template_total": sum(len(values) for values in templates.values()),
        "permutation_orientation_cap": permutation_cap,
        "stored_formula_total": MINE_ROWS,
        "used_formula_total": len(used),
        "used_source_index_sha256": hashlib.sha256(canonical_bytes(used)).hexdigest(),
        "scanned_residual_total": len(residuals),
        "covered_residual_total": covered,
        "uncovered_residual_total": len(residuals) - covered,
        "covered_target_total": covered * TARGETS_PER_ROW,
        "uncovered_target_total": (len(residuals) - covered) * TARGETS_PER_ROW,
        "reused_covered_row_total": reused,
        "maximum_formula_coverage": maximum,
        "formula_coverage_histogram": {str(value): count for value, count in
                                       sorted(Counter(owner_counts.values()).items())},
        "represented_signature_row_total": sum(signature_rows[key] for key in templates),
        "represented_degree_signature_row_total": sum(degree_signature_rows[key]
                                                       for key in degree_templates),
        "uncovered_signature_total": len(uncovered_signatures),
        "classification_stream_sha256": classification.hexdigest(),
        "certificate": {
            "gram": "G_ij=<x_i,x_j>, with rational stereographic unit vectors from R7O8G1",
            "psd_audit": "exact rational factorization G=XX^T",
            "cost_audit": "complete rational waypoint chains replayed with Fraction",
            "frontiers": "canonical and every one-path length-plus-two chain are stored and audited",
            "recognizer": "exact support multiplicities and odd-path counts modulo vertex permutation",
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pack", type=Path, default=DEFAULT_PACK)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--census-cache", type=Path)
    parser.add_argument("--permutation-cap", type=int, default=720)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--audit", type=Path)
    args = parser.parse_args()
    require(args.permutation_cap >= 1, "permutation cap must be positive")
    engine = load_engine()
    census = engine.load_census_module()
    residuals = engine.residual_rows(census, cache_path=args.census_cache)
    templates, degree_templates, orientation_total = load_templates(
        engine, census, residuals, args.pack, args.permutation_cap)
    report = scan(engine, census, residuals, templates, degree_templates, args.pack,
                  args.permutation_cap, args.progress)
    report["normalized_orientation_total"] = orientation_total
    raw = canonical_bytes(report)
    if args.audit is not None:
        require(args.audit.read_bytes() == raw, "coverage report does not reproduce byte-for-byte")
    else:
        require(args.output.parent.is_dir(), "output parent does not exist")
        args.output.write_bytes(raw)
    print(f"covered={report['covered_residual_total']} total={report['scanned_residual_total']} "
          f"used_formulas={report['used_formula_total']} signatures={len(templates)}")
    print(f"sha256={hashlib.sha256(raw).hexdigest()}")
    print(f"full_theorem={'true' if report['full_theorem'] else 'false'}")


if __name__ == "__main__":
    main()
