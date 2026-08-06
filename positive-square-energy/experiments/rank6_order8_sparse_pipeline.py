#!/usr/bin/env python3
"""Sparse order-eight/rank-six census and compact exact-Gram prototype.

The census never materializes dense 28-coordinate parity rows or a JSON target
ledger.  It uses support coordinates, degree-class automorphisms, mixed-radix
orbit traversal, and a superset-min transform for the tetrahedral sieve.

The optional search writes a binary XZ stream.  A successful source row stores
one common-denominator stereographic realization for all fourteen targets;
costs, rows, path lengths, and unchanged metadata are reconstructed, not stored.
This is an experiment and is not a theorem fixture.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import lzma
import math
import time
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "research" / "fixtures" / "rank-six-kernels.json"
ENGINE_PATH = ROOT / "pentacyclic" / "research" / "order8-dim8-rational-canonical-frontiers-experiment.py"
SOURCE_SHA256 = "5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476"
ORDER = 8
RANK = 6
PATH_COUNT = ORDER + RANK - 1
BUDGET = Fraction(RANK - 1)
BUDGET_SCALED = 30 * (RANK - 1)
PAIRS = tuple(itertools.combinations(range(ORDER), 2))
PAIR_INDEX = {edge: index for index, edge in enumerate(PAIRS)}
MAGIC = b"R8G1"
SCHEMA = "rank-six-order-eight-sparse-pipeline-experiment-v1"
SIGNED_CYCLE_SUPPORTS = {
    744: ({"05", "14", "23"}, {"07", "16", "27", "36", "45"}),
    756: ({"05", "14", "23"}, {"07", "16", "25", "34", "67"}),
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def source_kernels():
    raw = SOURCE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, "rank-six fixture changed")
    payload = json.loads(raw.decode("ascii"))
    rows = []
    for number, record in enumerate(payload["kernels"], 1):
        if record["n"] != ORDER:
            continue
        dense = tuple(record["code"])
        support = tuple(index for index, value in enumerate(dense) if value)
        multiplicities = tuple(dense[index] for index in support)
        require(sum(multiplicities) == PATH_COUNT, "path count changed")
        degrees = [0] * ORDER
        for index, value in zip(support, multiplicities):
            u, v = PAIRS[index]
            degrees[u] += value
            degrees[v] += value
        require(sorted(degrees, reverse=True) in ([5] + [3] * 7, [4, 4] + [3] * 6),
                "degree excess is not two")
        rows.append((number, dense, support, multiplicities, tuple(degrees)))
    require(len(rows) == 325 and rows[0][0] == 646 and rows[-1][0] == 970,
            "order-eight kernel interval changed")
    return tuple(rows)


def degree_class_permutations(degrees):
    classes = []
    for degree in sorted(set(degrees), reverse=True):
        classes.append(tuple(index for index, value in enumerate(degrees) if value == degree))
    for local in itertools.product(*(itertools.permutations(block) for block in classes)):
        permutation = list(range(ORDER))
        for block, image in zip(classes, local):
            for source, target in zip(block, image):
                permutation[source] = target
        yield tuple(permutation)


def automorphism_actions(dense, support, degrees):
    sparse_index = {dense_index: index for index, dense_index in enumerate(support)}
    actions = []
    for permutation in degree_class_permutations(degrees):
        action = tuple(PAIR_INDEX[tuple(sorted((permutation[u], permutation[v])))]
                       for u, v in PAIRS)
        if tuple(dense[index] for index in action) != dense:
            continue
        actions.append(tuple(sparse_index[action[index]] for index in support))
    require(actions, "missing identity automorphism")
    return tuple(actions)


def restricted_growth_strings(prefix=(0,)):
    if len(prefix) == ORDER:
        yield prefix
        return
    for color in range(min(3, max(prefix) + 1) + 1):
        yield from restricted_growth_strings(prefix + (color,))


COLORINGS = tuple(restricted_growth_strings())


def crossing_masks(support):
    result = set()
    edges = tuple(PAIRS[index] for index in support)
    for colors in COLORINGS:
        mask = 0
        for bit, (u, v) in enumerate(edges):
            if colors[u] != colors[v]:
                mask |= 1 << bit
        result.add(mask)
    return result


def superset_crossing_costs(multiplicities, masks):
    width = len(multiplicities)
    infinity = 10 ** 9
    best = [infinity] * (1 << width)
    weights = [18 * value for value in multiplicities]
    for mask in masks:
        best[mask] = min(best[mask], sum(weight for bit, weight in enumerate(weights)
                                         if mask & (1 << bit)))
    for bit in range(width):
        flag = 1 << bit
        for mask in range(1 << width):
            if not mask & flag and best[mask | flag] < best[mask]:
                best[mask] = best[mask | flag]
    require(best[0] == 0, "constant coloring disappeared")
    return tuple(best)


def mixed_radix_decode(code, radices):
    row = []
    for radix in radices:
        row.append(code % radix)
        code //= radix
    return tuple(row)


def mixed_radix_encode(row, radices):
    code = 0
    scale = 1
    for value, radix in zip(row, radices):
        code += scale * value
        scale *= radix
    return code


def coarse_cost(row, multiplicities, best_crossing):
    mandatory = 0
    adjustment = 0
    for bit, odd in enumerate(row):
        if odd:
            mandatory |= 1 << bit
            adjustment += 10 - 13 * odd
    return best_crossing[mandatory] + adjustment


def signed_cycle_template(kernel_number, support, multiplicities, row):
    specification = SIGNED_CYCLE_SUPPORTS.get(kernel_number)
    if specification is None:
        return False
    singles, doubles = specification
    values = {f"{PAIRS[index][0]}{PAIRS[index][1]}": (multiplicity, odd)
              for index, multiplicity, odd in zip(support, multiplicities, row)}
    return (set(values) == singles | doubles
            and all(values[edge][0] == 1 for edge in singles)
            and all(values[edge] == (2, 1) for edge in doubles))


def kernel_census(source, collect_residuals=False):
    number, dense, support, multiplicities, degrees = source
    actions = automorphism_actions(dense, support, degrees)
    masks = crossing_masks(support)
    best_crossing = superset_crossing_costs(multiplicities, masks)
    radices = tuple(value + 1 for value in multiplicities)
    physical = math.prod(radices)
    seen = bytearray(physical)
    orbits = residuals = template_orbits = 0
    residual_rows = []
    orbit_histogram = {}
    for code in range(physical):
        if seen[code]:
            continue
        row = mixed_radix_decode(code, radices)
        orbit = {mixed_radix_encode(tuple(row[index] for index in action), radices)
                 for action in actions}
        for image in orbit:
            seen[image] = 1
        orbits += 1
        orbit_histogram[len(orbit)] = orbit_histogram.get(len(orbit), 0) + 1
        cost = coarse_cost(row, multiplicities, best_crossing)
        if cost > BUDGET_SCALED:
            residuals += 1
            template = signed_cycle_template(number, support, multiplicities, row)
            template_orbits += template
            if collect_residuals:
                residual_rows.append((number, support, multiplicities, row, len(orbit), cost,
                                      template))
    return ({
        "kernel": number,
        "degree_partition": sorted(degrees, reverse=True),
        "support_edges": len(support),
        "parallel_excess": PATH_COUNT - len(support),
        "automorphisms": len(actions),
        "physical_rows": physical,
        "parity_orbits": orbits,
        "coarse_certified": orbits - residuals,
        "coarse_residuals": residuals,
        "signed_cycle_template_orbits": template_orbits,
        "crossing_masks": len(masks),
        "orbit_size_histogram": {str(key): orbit_histogram[key] for key in sorted(orbit_histogram)},
    }, residual_rows)


def census(collect_residuals=False, progress=False):
    started = time.perf_counter()
    ledgers = []
    residual_rows = []
    for index, source in enumerate(source_kernels(), 1):
        ledger, local = kernel_census(source, collect_residuals)
        ledgers.append(ledger)
        residual_rows.extend(local)
        if progress:
            print(f"[{index}/325] K{ledger['kernel']} orbits={ledger['parity_orbits']} "
                  f"residuals={ledger['coarse_residuals']}", flush=True)
    residual_total = sum(row["coarse_residuals"] for row in ledgers)
    template_total = sum(row["signed_cycle_template_orbits"] for row in ledgers)
    payload = {
        "schema": SCHEMA,
        "status": "census_complete_certificates_open",
        "full_theorem": False,
        "source_sha256": SOURCE_SHA256,
        "rank": RANK,
        "order": ORDER,
        "kernel_interval": [646, 970],
        "kernel_total": len(ledgers),
        "path_count": PATH_COUNT,
        "frontiers_per_residual": PATH_COUNT + 1,
        "physical_total": sum(row["physical_rows"] for row in ledgers),
        "parity_orbit_total": sum(row["parity_orbits"] for row in ledgers),
        "coarse_certified_total": sum(row["coarse_certified"] for row in ledgers),
        "coarse_residual_total": residual_total,
        "frontier_target_total": (PATH_COUNT + 1) * residual_total,
        "signed_cycle_template_orbit_total": template_total,
        "signed_cycle_template_target_total": (PATH_COUNT + 1) * template_total,
        "search_target_after_templates": (PATH_COUNT + 1) * (residual_total - template_total),
        "representation": "support rows regenerated from source; no residual or target JSON",
        "elapsed_seconds": float(f"{time.perf_counter() - started:.6f}"),
        "kernels": ledgers,
    }
    return payload, residual_rows


def load_engine():
    spec = importlib.util.spec_from_file_location("rank6_order8_vector_engine", ENGINE_PATH)
    require(spec is not None and spec.loader is not None, "cannot load vector engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.BUDGET = BUDGET
    module.PATHS_PER_KERNEL = PATH_COUNT
    return module


def dense_row(support, row):
    result = [0] * len(PAIRS)
    for index, value in zip(support, row):
        result[index] = value
    return tuple(result)


def dense_kernel(support, multiplicities):
    result = [0] * len(PAIRS)
    for index, value in zip(support, multiplicities):
        result[index] = value
    return tuple(result)


def canonical_path_lengths(multiplicities, row):
    lengths = []
    for multiplicity, odd in zip(multiplicities, row):
        if odd:
            lengths.extend((1, *(3 for _ in range(odd - 1))))
        lengths.extend(2 for _ in range(multiplicity - odd))
    require(len(lengths) == PATH_COUNT, "canonical path count changed")
    return tuple(lengths)


def shared_rationalize(engine, paths, vectors, denominators):
    vectors = engine.rotate_away_from_pole(vectors)
    for denominator in denominators:
        try:
            branch_parameters = tuple(engine.stereographic(row, denominator) for row in vectors)
            branches = tuple(engine.rational_unit(row) for row in branch_parameters)
            canonical = []
            extended = []
            base_costs = []
            extended_costs = []
            for _, _, u, v, length in paths:
                endpoint = vectors[v] if length % 2 == 0 else tuple(-x for x in vectors[v])
                exact_endpoint = branches[v] if length % 2 == 0 else tuple(-x for x in branches[v])
                local = []
                longer = []
                for target, width in ((local, length), (longer, length + 2)):
                    target.extend(engine.stereographic(
                        engine.slerp(vectors[u], endpoint, step / width), denominator)
                                  for step in range(1, width))
                def path_cost(parameters):
                    chain = [branches[u], *(engine.rational_unit(value) for value in parameters),
                             exact_endpoint]
                    return sum((engine.exact_step_cost(a, b) for a, b in zip(chain, chain[1:])),
                               Fraction())
                canonical.append(tuple(local))
                extended.append(tuple(longer))
                base_costs.append(path_cost(local))
                extended_costs.append(path_cost(longer))
        except (RuntimeError, ZeroDivisionError):
            continue
        base = sum(base_costs, Fraction())
        costs = (base, *(base - base_costs[i] + extended_costs[i]
                         for i in range(PATH_COUNT)))
        if all(value <= BUDGET for value in costs):
            return denominator, branch_parameters, tuple(canonical), tuple(extended)
    return None


def put_uvarint(output, value):
    require(type(value) is int and value >= 0, "bad unsigned varint")
    while value >= 0x80:
        output.append((value & 0x7f) | 0x80)
        value >>= 7
    output.append(value)


def put_svarint(output, value):
    put_uvarint(output, 2 * value if value >= 0 else -2 * value - 1)


def get_uvarint(raw, position):
    value = shift = 0
    while True:
        require(position < len(raw) and shift <= 4096, "truncated or excessive varint")
        byte = raw[position]
        position += 1
        value |= (byte & 0x7f) << shift
        if not byte & 0x80:
            return value, position
        shift += 7


def get_svarint(raw, position):
    value, position = get_uvarint(raw, position)
    return (value // 2 if value % 2 == 0 else -(value // 2) - 1), position


def scaled_numerator(value, denominator):
    require(denominator % value.denominator == 0, "parameter denominator is not shared")
    return value.numerator * (denominator // value.denominator)


def encode_search(start, attempts, witnesses):
    output = bytearray(MAGIC)
    output.extend(bytes.fromhex(SOURCE_SHA256))
    put_uvarint(output, start)
    put_uvarint(output, attempts)
    for witness in witnesses:
        output.append(witness is not None)
        if witness is None:
            continue
        denominator, branches, canonical, extended = witness
        put_uvarint(output, denominator)
        for row in branches:
            for value in row:
                put_svarint(output, scaled_numerator(value, denominator))
        for family in (canonical, extended):
            for path in family:
                for row in path:
                    for value in row:
                        put_svarint(output, scaled_numerator(value, denominator))
    return bytes(output)


def decode_search(raw, residual_rows):
    require(raw[:4] == MAGIC and raw[4:36] == bytes.fromhex(SOURCE_SHA256), "bad pack header")
    position = 36
    start, position = get_uvarint(raw, position)
    attempts, position = get_uvarint(raw, position)
    require(start + attempts <= len(residual_rows), "pack range exceeds census")
    records = []
    for local in range(attempts):
        require(position < len(raw) and raw[position] in (0, 1), "bad witness tag")
        success = bool(raw[position])
        position += 1
        if not success:
            records.append(None)
            continue
        denominator, position = get_uvarint(raw, position)
        require(denominator > 0, "zero shared denominator")
        _, _, multiplicities, row, _, _, _ = residual_rows[start + local]
        lengths = canonical_path_lengths(multiplicities, row)
        def vector():
            nonlocal position
            values = []
            for _ in range(ORDER - 1):
                value, position = get_svarint(raw, position)
                values.append(Fraction(value, denominator))
            return tuple(values)
        branches = tuple(vector() for _ in range(ORDER))
        canonical = tuple(tuple(vector() for _ in range(length - 1)) for length in lengths)
        extended = tuple(tuple(vector() for _ in range(length + 1)) for length in lengths)
        records.append((denominator, branches, canonical, extended))
    require(position == len(raw), "trailing pack bytes")
    return start, attempts, records


def verify_witness(engine, source, witness):
    _, support, multiplicities, row, _, _, _ = source
    kernel = dense_kernel(support, multiplicities)
    parity = dense_row(support, row)
    paths = engine.path_ledger(kernel, parity)
    denominator, branch_parameters, canonical, extended = witness
    require(denominator > 0 and len(branch_parameters) == ORDER, "bad compact witness")
    for family in (branch_parameters, *canonical, *extended):
        for parameters in family:
            require(len(parameters) == ORDER - 1, "stereographic dimension changed")
            require(all(value.denominator > 0 and denominator % value.denominator == 0
                        for value in parameters), "parameter denominator changed")
    branches = tuple(engine.rational_unit(value) for value in branch_parameters)
    require(all(len(value) == ORDER for value in branches), "branch dimension changed")
    for frontier in (None, *range(PATH_COUNT)):
        total = Fraction()
        for index, ((_, _, u, v, length), base, longer) in enumerate(
                zip(paths, canonical, extended)):
            parameters = longer if index == frontier else base
            expected_length = length + (2 if index == frontier else 0)
            require(len(parameters) == expected_length - 1, "path width changed")
            endpoint = branches[v] if length % 2 == 0 else tuple(-x for x in branches[v])
            chain = [branches[u], *(engine.rational_unit(value) for value in parameters), endpoint]
            total += sum((engine.exact_step_cost(a, b) for a, b in zip(chain, chain[1:])),
                         Fraction())
        require(total <= BUDGET, "compact exact cost exceeds five")


def search(args, residual_rows):
    engine = load_engine()
    selected = residual_rows[args.start:args.start + args.search_count]
    denominators = tuple(int(value) for value in args.denominators.split(","))
    require(denominators and all(value > 0 for value in denominators), "bad denominators")
    witnesses = []
    for local, source in enumerate(selected):
        _, support, multiplicities, row, _, _, template = source
        if template:
            witnesses.append(None)
            continue
        paths = engine.path_ledger(dense_kernel(support, multiplicities), dense_row(support, row))
        value, vectors = engine.optimize(paths, args.seed + 1009 * (args.start + local),
                                         args.restarts, args.iterations)
        witness = shared_rationalize(engine, paths, vectors, denominators)
        witnesses.append(witness)
        if args.progress:
            print(f"[{local + 1}/{len(selected)}] numerical={value:.9f} "
                  f"shared_exact={witness is not None}", flush=True)
    raw = encode_search(args.start, len(selected), witnesses)
    stored = lzma.compress(raw, format=lzma.FORMAT_XZ, preset=6)
    args.output.write_bytes(stored)
    for source, witness in zip(selected, witnesses):
        if witness is not None:
            verify_witness(engine, source, witness)
    print(f"attempts={len(selected)} shared_exact={sum(x is not None for x in witnesses)} "
          f"raw_bytes={len(raw)} xz_bytes={len(stored)}")
    print(f"sha256={hashlib.sha256(stored).hexdigest()}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--search-count", type=int, default=0)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--seed", type=int, default=86131)
    parser.add_argument("--restarts", type=int, default=2)
    parser.add_argument("--iterations", type=int, default=260)
    parser.add_argument("--denominators", default="256,1024,4096,16384,65536")
    parser.add_argument("--verify-pack", type=Path)
    args = parser.parse_args()
    require(args.start >= 0 and args.search_count >= 0, "bad selected range")
    need_rows = args.search_count > 0 or args.verify_pack is not None
    payload, residual_rows = census(need_rows, args.progress and not args.search_count)
    if args.verify_pack is not None:
        raw = lzma.decompress(args.verify_pack.read_bytes(), format=lzma.FORMAT_XZ)
        start, attempts, records = decode_search(raw, residual_rows)
        engine = load_engine()
        for source, witness in zip(residual_rows[start:start + attempts], records):
            if witness is not None:
                verify_witness(engine, source, witness)
        print(f"attempts={attempts} shared_exact={sum(x is not None for x in records)} exact_audit=true")
        return
    if args.search_count:
        require(args.output is not None and args.output.parent.is_dir(), "search output parent missing")
        search(args, residual_rows)
        return
    raw = canonical_bytes(payload)
    if args.output is not None:
        require(args.output.parent.is_dir(), "census output parent missing")
        args.output.write_bytes(raw)
    print(f"kernels={payload['kernel_total']} physical={payload['physical_total']} "
          f"orbits={payload['parity_orbit_total']}")
    print(f"coarse_certified={payload['coarse_certified_total']} "
          f"residuals={payload['coarse_residual_total']} "
          f"frontier_targets={payload['frontier_target_total']}")
    print(f"signed_cycle_templates={payload['signed_cycle_template_orbit_total']} "
          f"search_targets={payload['search_target_after_templates']}")
    print(f"summary_bytes={len(raw)} elapsed_seconds={payload['elapsed_seconds']:.6f} full_theorem=false")


if __name__ == "__main__":
    main()
