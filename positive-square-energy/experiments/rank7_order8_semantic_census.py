#!/usr/bin/env python3
"""Read-only exact comparison of committed residual census against regeneration.

No stored census ledger, digest or residual list is an input to regeneration.
A bounded --start/--stop run is diagnostic only, never a full theorem gate.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
KERNEL_SOURCE = ROOT / 'research' / 'fixtures' / 'rank-seven-kernel-frontier-census.json'
KERNEL_SOURCE_SHA256 = 'a241139ab54ce4cce1ab3812887359edb241c0abfb1018e804b4a5f86762cfd5'
EXPECTED_KERNEL_COUNTS = (1, 6, 47, 233, 914, 2270, 4015, 4495, 3396, 1391, 365)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_census():
    spec = importlib.util.spec_from_file_location(
        'order8_census_comparator_source', HERE / 'rank7_order8_exact_residual_census.py')
    require(spec is not None and spec.loader is not None, 'cannot import census')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pure_source_kernels():
    """Parse the byte-pinned canonical kernel fixture without the legacy engine."""
    raw = KERNEL_SOURCE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == KERNEL_SOURCE_SHA256,
            'rank-seven kernel fixture changed')
    payload = json.loads(raw.decode('ascii'))
    require(tuple(payload['counts_by_order_n2_to_n12']) == EXPECTED_KERNEL_COUNTS,
            'rank-seven kernel counts changed')
    records = []
    local = {order: 0 for order in range(2, 13)}
    for global_index, record in enumerate(payload['kernels'], 1):
        n = record['n']
        require(type(n) is int and 2 <= n <= 12, 'invalid kernel order')
        code = record['code']
        pairs = tuple(itertools.combinations(range(n), 2))
        require(type(code) is list and len(code) == len(pairs) and
                all(type(value) is int and value >= 0 for value in code),
                'invalid dense kernel code')
        local[n] += 1
        edges = tuple((u, v, value) for (u, v), value in zip(pairs, code) if value)
        require(sum(edge[2] for edge in edges) == n + 6, 'kernel path count changed')
        records.append((global_index, local[n], n, edges))
    require(tuple(local[order] for order in range(2, 13)) == EXPECTED_KERNEL_COUNTS,
            'kernel order totals changed')
    return tuple(records)


def pure_engine():
    return SimpleNamespace(SOURCE_SHA256=KERNEL_SOURCE_SHA256,
                           source_kernels=pure_source_kernels,
                           automorphism_actions=pure_automorphism_actions)


def pure_automorphism_actions(n, edges):
    """Enumerate support-multigraph automorphisms using only the stdlib.

    Order eight is deliberately small: 8! permutations per kernel make this
    independent implementation cheap enough for a release audit.  Returning
    exactly the engine's edge-action representation lets the semantic census
    use this routine without trusting NetworkX or any other optional package.
    """
    require(type(n) is int and n == 8, 'pure automorphism scope changed')
    require(type(edges) is tuple and edges, 'invalid sparse kernel edges')
    edge_index = {}
    multiplicities = []
    for index, edge in enumerate(edges):
        require(type(edge) is tuple and len(edge) == 3,
                'invalid sparse kernel edge')
        u, v, multiplicity = edge
        require(type(u) is int and type(v) is int and 0 <= u < v < n and
                type(multiplicity) is int and multiplicity >= 1,
                'invalid sparse kernel edge')
        require((u, v) not in edge_index, 'duplicate sparse kernel edge')
        edge_index[(u, v)] = index
        multiplicities.append(multiplicity)
    actions = set()
    for permutation in itertools.permutations(range(n)):
        action = []
        for u, v, multiplicity in edges:
            image = tuple(sorted((permutation[u], permutation[v])))
            target = edge_index.get(image)
            if target is None or multiplicities[target] != multiplicity:
                break
            action.append(target)
        else:
            actions.add(tuple(action))
    require(actions, 'pure automorphism group is empty')
    return tuple(sorted(actions))


def compare(manifest_path, start=0, stop=4015):
    c = load_census()
    require(type(start) is int and type(stop) is int and 0 <= start < stop <= c.KERNEL_TOTAL,
            'invalid semantic comparison range')
    manifest, _, _ = c.read_payload(manifest_path)
    c.verify_manifest(manifest, manifest_path)
    # Use a self-contained stdlib engine.  The legacy producer module imports
    # NetworkX, so even importing it would make the full gate environment-bound.
    engine = pure_engine()
    require(engine.automorphism_actions is pure_automorphism_actions and
            engine.source_kernels is pure_source_kernels,
            'pure engine functions were replaced')
    items = c.order_items(engine)
    require(manifest['source_sha256'] == engine.SOURCE_SHA256, 'wrong census source')
    transcript = hashlib.sha256()
    compared = 0
    for entry in manifest['chunks']:
        lo, hi = entry['kernel_range']
        if hi <= start or lo >= stop:
            continue
        chunk, _, _ = c.read_payload(manifest_path.parent / entry['path'])
        require(chunk['source_sha256'] == engine.SOURCE_SHA256, 'wrong chunk source')
        residuals = {}
        for record in chunk['residuals']:
            residuals.setdefault(record['order_kernel'], []).append(record)
        for position in range(max(lo, start), min(hi, stop)):
            ledger, rows = c.census_kernel(engine, items[position])
            require(c.canonical_bytes(ledger) == c.canonical_bytes(chunk['kernels'][position-lo]),
                    f'semantic kernel ledger mismatch at {position}')
            expected = [dict(global_kernel=ledger['global_kernel'],
                             order_kernel=ledger['order_kernel'], row=row,
                             orbit_size=mass) for row, mass in rows]
            require(c.canonical_bytes(expected) == c.canonical_bytes(residuals.get(ledger['order_kernel'], [])),
                    f'semantic residual stream mismatch at {position}')
            transcript.update(c.canonical_bytes([ledger, expected]))
            compared += 1
    require(compared == stop-start, 'incomplete semantic comparison')
    return dict(schema='rank-seven-order-eight-semantic-census-comparison-v1',
                kernel_range=[start, stop], kernels_compared=compared,
                full_census_verified=(start == 0 and stop == c.KERNEL_TOTAL),
                comparison_sha256=transcript.hexdigest())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path,
                        default=HERE/'rank7_order8_exact_residual_census_manifest.json')
    parser.add_argument('--start', type=int, default=0)
    parser.add_argument('--stop', type=int, default=4015)
    args = parser.parse_args()
    c = load_census()
    print(c.canonical_bytes(compare(args.manifest, args.start, args.stop)).decode('ascii'), end='')


if __name__ == '__main__':
    main()
