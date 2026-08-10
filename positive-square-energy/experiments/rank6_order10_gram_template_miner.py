#!/usr/bin/env python3
"""Mine exact recurring branch-Gram templates from completed R10G1 packs.

The canonical form is invariant under simultaneous row/column permutations and
independent sign switches.  It uses exact Fraction arithmetic throughout.  A
cheap switching-invariant vertex partition normally makes canonicalization
linear; permutations are enumerated only inside genuinely tied cells.
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
STREAM_PATH = HERE / "rank6_order10_cubic_exact_rational.py"
DEFAULT_PACK_DIRECTORY = HERE / "rank6_order10_search_ckpt"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_stream():
    spec = importlib.util.spec_from_file_location("rank6_order10_gram_miner_stream", STREAM_PATH)
    require(spec is not None and spec.loader is not None, "cannot load R10 stream")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fraction_key(value):
    return value.numerator, value.denominator


def gram_from_parameters(stream, parameters):
    vectors = tuple(stream.rational_unit(row) for row in parameters)
    return tuple(tuple(stream.dot(left, right) for right in vectors) for left in vectors)


def vertex_fingerprint(gram, vertex):
    order = len(gram)
    incident = tuple(sorted(fraction_key(abs(gram[vertex][other]))
                            for other in range(order) if other != vertex))
    triangles = []
    others = [other for other in range(order) if other != vertex]
    for left, right in itertools.combinations(others, 2):
        incident_pair = sorted((fraction_key(abs(gram[vertex][left])),
                                fraction_key(abs(gram[vertex][right]))))
        triangles.append((incident_pair[0], incident_pair[1],
                          fraction_key(gram[vertex][left] * gram[left][right]
                                       * gram[right][vertex])))
    return incident, tuple(sorted(triangles))


def switched_flattening(gram, permutation):
    """Switch deterministically along the first nonzero edge of each component."""
    signs = [None] * len(permutation)
    for root in range(len(permutation)):
        if signs[root] is not None:
            continue
        signs[root] = 1
        queue = [root]
        for position in queue:
            for neighbor in range(len(permutation)):
                value = gram[permutation[position]][permutation[neighbor]]
                if neighbor != position and value and signs[neighbor] is None:
                    signs[neighbor] = signs[position] if value > 0 else -signs[position]
                    queue.append(neighbor)
    return tuple(fraction_key(Fraction(signs[i] * signs[j])
                              * gram[permutation[i]][permutation[j]])
                 for i in range(len(gram)) for j in range(i + 1, len(gram)))


def canonical_gram(gram):
    """Return the exact signed-permutation canonical upper triangle.

    Switching-invariant fingerprints split almost every numerical R10 Gram
    completely.  Enumerating permutations within equal cells is exact, not a
    hash heuristic.  Uniform balanced/antibalanced Grams are handled directly
    to avoid a pointless 10! symmetric enumeration.
    """
    order = len(gram)
    require(order and all(len(row) == order for row in gram), "nonsquare Gram")
    require(all(gram[i][i] == 1 for i in range(order)), "non-correlation Gram")
    require(all(gram[i][j] == gram[j][i] for i in range(order) for j in range(order)),
            "nonsymmetric Gram")
    nonzero_abs = {abs(gram[i][j]) for i in range(order) for j in range(i + 1, order)}
    triangle_signs = {0 if (product := gram[i][j] * gram[j][k] * gram[k][i]) == 0
                      else (1 if product > 0 else -1)
                      for i, j, k in itertools.combinations(range(order), 3)}
    if len(nonzero_abs) == 1 and 0 not in nonzero_abs and len(triangle_signs) == 1:
        value = next(iter(nonzero_abs))
        sign = next(iter(triangle_signs))
        canonical = tuple(fraction_key(value if sign > 0 or i == 0 else -value)
                          for i in range(order) for j in range(i + 1, order))
        return canonical

    cells = defaultdict(list)
    for vertex in range(order):
        cells[vertex_fingerprint(gram, vertex)].append(vertex)
    ordered_cells = tuple(tuple(cells[key]) for key in sorted(cells))
    best = None
    for blocks in itertools.product(*(itertools.permutations(cell) for cell in ordered_cells)):
        permutation = tuple(itertools.chain.from_iterable(blocks))
        candidate = switched_flattening(gram, permutation)
        if best is None or candidate < best:
            best = candidate
    require(best is not None, "empty canonicalization orbit")
    return best


def canonical_digest(canonical):
    raw = json.dumps(canonical, separators=(",", ":")).encode("ascii")
    return hashlib.sha256(raw).hexdigest()


def discover_packs(directory):
    candidates = list(directory.glob("chunk-*.r10g.xz"))
    candidates.extend(directory.glob("chunk-*.r10g.xz.fragments/fragment-*.r10g.xz"))
    return tuple(sorted(candidates))


def load_records(stream, census, residuals, paths):
    intervals = []
    for path in paths:
        raw = lzma.decompress(path.read_bytes(), format=lzma.FORMAT_XZ)
        start, records = stream.decode_pack(census, raw, residuals)
        intervals.append((start, start + len(records), path, records))
    intervals.sort(key=lambda item: (item[0], -(item[1] - item[0]), str(item[2])))
    accepted = []
    occupied = set()
    for start, stop, path, records in intervals:
        if any(index in occupied for index in range(start, stop)):
            continue
        occupied.update(range(start, stop))
        accepted.append((start, stop, path, records))
    return tuple(accepted)


def mine(stream, census, residuals, intervals, minimum_occurrences):
    classes = defaultdict(list)
    mode_counts = Counter()
    for start, _, _, records in intervals:
        for local, (mode, payload) in enumerate(records):
            mode_counts[mode] += 1
            if mode != stream.MODE_SHARED:
                continue
            gram = gram_from_parameters(stream, payload[1])
            canonical = canonical_gram(gram)
            classes[canonical].append(start + local)
    recurring = {key: indices for key, indices in classes.items()
                 if len(indices) >= minimum_occurrences}
    recognized = sum(len(indices) for indices in recurring.values())
    future_hits = sum(len(indices) - 1 for indices in recurring.values())
    templates = []
    for canonical, indices in sorted(recurring.items(), key=lambda item: (-len(item[1]), item[1][0])):
        sources = [residuals[index] for index in indices]
        templates.append({
            "digest": canonical_digest(canonical),
            "occurrences": len(indices),
            "first_source_index": indices[0],
            "source_indices": indices,
            "kernels": sorted({source[0] for source in sources}),
        })
    covered = sum(stop - start for start, stop, _, _ in intervals)
    shared = mode_counts[stream.MODE_SHARED]
    return {
        "schema": "rank-six-order-ten-exact-gram-template-mining-v1",
        "equivalence": "exact rational branch Grams modulo vertex permutations and sign switches",
        "pack_intervals": [[start, stop, path.name] for start, stop, path, _ in intervals],
        "covered_residual_total": covered,
        "shared_witness_total": shared,
        "unique_canonical_gram_total": len(classes),
        "minimum_template_occurrences": minimum_occurrences,
        "recurring_template_total": len(recurring),
        "recurring_witness_total": recognized,
        "future_recognizer_hit_total": future_hits,
        "future_recognizer_hit_rate_of_shared": [future_hits, shared],
        "templates": templates,
    }


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("packs", nargs="*", type=Path)
    parser.add_argument("--pack-directory", type=Path, default=DEFAULT_PACK_DIRECTORY)
    parser.add_argument("--census-cache", type=Path)
    parser.add_argument("--minimum-occurrences", type=int, default=2)
    parser.add_argument("--require-covered", type=int, default=0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    require(args.minimum_occurrences >= 2, "minimum occurrence count must be at least two")
    stream = load_stream()
    census = stream.load_census_module()
    residuals = stream.residual_rows(census, cache_path=args.census_cache)
    paths = tuple(args.packs) if args.packs else discover_packs(args.pack_directory)
    require(paths, "no R10G1 packs found")
    intervals = load_records(stream, census, residuals, paths)
    payload = mine(stream, census, residuals, intervals, args.minimum_occurrences)
    require(payload["covered_residual_total"] >= args.require_covered,
            "completed pack coverage is below the requested threshold")
    raw = canonical_bytes(payload)
    if args.output is not None:
        require(args.output.parent.is_dir(), "output parent does not exist")
        args.output.write_bytes(raw)
    print(raw.decode("ascii"), end="")
    print(f"sha256={hashlib.sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()
