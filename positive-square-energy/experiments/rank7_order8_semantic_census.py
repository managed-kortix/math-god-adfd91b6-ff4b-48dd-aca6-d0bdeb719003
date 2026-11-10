#!/usr/bin/env python3
"""Read-only exact comparison of committed residual census against regeneration.

No stored census ledger, digest or residual list is an input to regeneration.
A bounded --start/--stop run is diagnostic only, never a full theorem gate.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent


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


def compare(manifest_path, start=0, stop=4015):
    c = load_census()
    require(type(start) is int and type(stop) is int and 0 <= start < stop <= c.KERNEL_TOTAL,
            'invalid semantic comparison range')
    manifest, _, _ = c.read_payload(manifest_path)
    c.verify_manifest(manifest, manifest_path)
    engine = c.load_engine()
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
