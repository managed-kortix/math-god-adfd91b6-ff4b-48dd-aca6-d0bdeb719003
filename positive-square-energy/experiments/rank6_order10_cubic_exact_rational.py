#!/usr/bin/env python3
"""Chunked exact-rational search for order-ten cubic residual frontiers.

The binary R10G1/XZ format regenerates kernels, parity rows, path lengths, and
the K1133 signed-cycle templates. Numerical optimization only proposes points;
every stored shared or per-target fallback witness is audited with Fraction.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import lzma
import math
import random
import time
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
CENSUS_PATH = HERE / "rank6_order10_cubic_frontier_census.py"
MAGIC = b"R10G1"
ORDER = DIMENSION = 10
PATH_COUNT = 15
BUDGET = Fraction(5)
MODE_UNRESOLVED = 0
MODE_SHARED = 1
MODE_TEMPLATE = 2
MODE_FALLBACK = 3
CENSUS_CACHE_SCHEMA = "rank-six-order-ten-residual-cache-v1"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_census_module():
    spec = importlib.util.spec_from_file_location("rank6_order10_census", CENSUS_PATH)
    require(spec is not None and spec.loader is not None, "cannot load order-ten census")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def residual_rows(census, progress=False, cache_path=None):
    """Regenerate the canonical sparse residual stream without serializing it."""
    rows = census.source_rows(ORDER)
    if cache_path is not None and cache_path.is_file():
        cached = json.loads(lzma.decompress(cache_path.read_bytes()).decode("ascii"))
        require(cached.get("schema") == CENSUS_CACHE_SCHEMA and
                cached.get("source_sha256") == census.SOURCE_SHA256 and
                cached.get("residual_total") == 125457,
                "order-ten residual cache changed")
        result = []
        for kernel_index, row, orbit_size, cost, template in cached["residuals"]:
            number, code = rows[kernel_index]
            support, multiplicities = census.support_data(code)
            result.append((number, code, support, multiplicities, tuple(row),
                           orbit_size, cost, template))
        require(len(result) == 125457 and sum(row[-1] for row in result) == 8,
                "order-ten cached residual stream changed")
        expected = {record["kernel"]: record["residual_stream_sha256"]
                    for record in json.loads(census.OUTPUT.read_text("ascii"))["kernels"]}
        digests = {number: hashlib.sha256() for number, _ in rows}
        for number, _, _, _, row, orbit_size, cost, _ in result:
            raw = (json.dumps([number, list(row), orbit_size, cost],
                              sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")
            digests[number].update(raw)
        require(all(digests[number].hexdigest() == expected[number] for number in digests),
                "order-ten cached residual stream digest changed")
        return tuple(result)
    cycle = {number: census.five_cycle_support(ORDER, code)
             for number, code in rows if census.five_cycle_support(ORDER, code)}
    require(tuple(cycle) == census.EXPECTED_CYCLE_KERNELS[ORDER],
            "order-ten cycle candidates changed")
    result = []
    for position, (number, code) in enumerate(rows, 1):
        support, multiplicities = census.support_data(code)
        actions = census.support_actions(support, census.automorphisms(code))
        radices = tuple(value + 1 for value in multiplicities)
        physical = math.prod(radices)
        seen = bytearray(physical)
        crossing = census.superset_crossing_costs(
            multiplicities, census.crossing_masks(support))
        specification = cycle.get(number)
        before = len(result)
        for encoded in range(physical):
            if seen[encoded]:
                continue
            row = census.mixed_radix_decode(encoded, radices)
            orbit = {census.mixed_radix_encode(
                tuple(row[source] for source in action), radices) for action in actions}
            for image in orbit:
                seen[image] = 1
            representative = row
            cost = census.coarse_cost(representative, multiplicities, crossing)
            if cost > census.BUDGET_SCALED:
                template = specification is not None and census.candidate_row(
                    support, multiplicities, representative, specification)
                result.append((number, code, support, multiplicities, representative,
                               len(orbit), cost, template))
        if progress:
            print(f"[{position}/66] K{number} residuals={len(result) - before}", flush=True)
    require(len(result) == 125457, "order-ten residual count changed")
    require(sum(row[-1] for row in result) == 8, "K1133 template count changed")
    if cache_path is not None and not cache_path.exists():
        kernel_indices = {number: index for index, (number, _) in enumerate(rows)}
        cached = {
            "schema": CENSUS_CACHE_SCHEMA,
            "source_sha256": census.SOURCE_SHA256,
            "residual_total": len(result),
            "residuals": [[kernel_indices[row[0]], list(row[4]), row[5], row[6], bool(row[7])]
                          for row in result],
        }
        raw = (json.dumps(cached, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")
        temporary = cache_path.with_name(cache_path.name + ".tmp")
        temporary.write_bytes(lzma.compress(raw, format=lzma.FORMAT_XZ, preset=3))
        temporary.replace(cache_path)
    return tuple(result)


def canonical_lengths(multiplicity, odd):
    return (([1] + [3] * (odd - 1)) if odd else []) + [2] * (multiplicity - odd)


def path_ledger(census, source, frontier=None):
    _, _, support, multiplicities, row, _, _, _ = source
    paths = []
    for sparse, (dense, multiplicity, odd) in enumerate(zip(support, multiplicities, row)):
        u, v = census.PAIRS[dense]
        paths.extend((sparse, occurrence, u, v, length)
                     for occurrence, length in enumerate(canonical_lengths(multiplicity, odd)))
    require(len(paths) == PATH_COUNT, "path count changed")
    if frontier is not None:
        require(0 <= frontier < PATH_COUNT, "bad frontier")
        edge, occurrence, u, v, length = paths[frontier]
        paths[frontier] = edge, occurrence, u, v, length + 2
    return tuple(paths)


def dot(left, right):
    return sum(x * y for x, y in zip(left, right))


def normalized(vector):
    norm = math.sqrt(dot(vector, vector))
    require(norm > 1e-14, "cannot normalize zero vector")
    return tuple(value / norm for value in vector)


def path_cost_derivative(correlation, length):
    sign = -1.0 if length & 1 else 1.0
    transformed = max(-1.0 + 1e-14, min(1.0 - 1e-14, sign * correlation))
    angle = math.acos(transformed)
    tangent = math.tan(angle / (2.0 * length))
    derivative = (-sign * tangent * (1.0 + tangent * tangent)
                  / math.sqrt(max(1e-28, 1.0 - transformed * transformed)))
    return length * tangent * tangent, derivative


def objective_gradient(paths, vectors):
    total = 0.0
    gradient = [[0.0] * DIMENSION for _ in range(ORDER)]
    for _, _, u, v, length in paths:
        cost, derivative = path_cost_derivative(dot(vectors[u], vectors[v]), length)
        total += cost
        for coordinate in range(DIMENSION):
            gradient[u][coordinate] += derivative * vectors[v][coordinate]
            gradient[v][coordinate] += derivative * vectors[u][coordinate]
    for vertex in range(1, ORDER):
        radial = dot(gradient[vertex], vectors[vertex])
        gradient[vertex] = [value - radial * coordinate
                            for value, coordinate in zip(gradient[vertex], vectors[vertex])]
    gradient[0] = [0.0] * DIMENSION
    return total, gradient


def objective(paths, vectors):
    return sum(path_cost_derivative(dot(vectors[u], vectors[v]), length)[0]
               for _, _, u, v, length in paths)


def random_vectors(generator):
    return (((1.0,) + (0.0,) * (DIMENSION - 1)),) + tuple(
        normalized(tuple(generator.gauss(0.0, 1.0) for _ in range(DIMENSION)))
        for _ in range(ORDER - 1))


def descend(paths, initial, iterations):
    vectors = tuple(initial)
    step = 0.25
    for _ in range(iterations):
        value, gradient = objective_gradient(paths, vectors)
        norm = math.sqrt(sum(dot(row, row) for row in gradient))
        if norm < 1e-10:
            break
        trial_step = step
        for _ in range(18):
            candidate = [vectors[0]]
            for vertex in range(1, ORDER):
                candidate.append(normalized(tuple(
                    vectors[vertex][coordinate] - trial_step * gradient[vertex][coordinate]
                    for coordinate in range(DIMENSION))))
            candidate = tuple(candidate)
            if objective(paths, candidate) < value - 1e-5 * trial_step * norm * norm:
                vectors = candidate
                step = min(0.8, trial_step * 1.35)
                break
            trial_step *= 0.5
        else:
            step *= 0.25
            if step < 1e-11:
                break
    return objective(paths, vectors), vectors


def optimize(paths, seed, restarts, iterations, warm=()):
    generator = random.Random(seed)
    starts = list(warm) + [random_vectors(generator) for _ in range(restarts)]
    require(starts, "optimizer has no starts")
    return min((descend(paths, initial, iterations) for initial in starts), key=lambda row: row[0])


def rotate_away_from_pole(vectors):
    choices = [(min(1.0 + sign * row[coordinate] for row in vectors), coordinate, sign)
               for coordinate in range(DIMENSION) for sign in (-1.0, 1.0)]
    _, first, sign = max(choices)
    order = (first,) + tuple(index for index in range(DIMENSION) if index != first)
    return tuple(tuple((sign if position == 0 else 1.0) * row[coordinate]
                       for position, coordinate in enumerate(order)) for row in vectors)


def stereographic(vector, denominator):
    scale = 1.0 + vector[0]
    require(abs(scale) > 1e-10, "stereographic pole")
    return tuple(Fraction(round(value / scale * denominator), denominator) for value in vector[1:])


def rational_unit(parameters):
    square = dot(parameters, parameters)
    denominator = 1 + square
    return ((1 - square) / denominator,) + tuple(2 * value / denominator for value in parameters)


def slerp(left, right, fraction):
    correlation = max(-1.0, min(1.0, dot(left, right)))
    angle = math.acos(correlation)
    if angle < 1e-12:
        return left
    sine = math.sin(angle)
    return normalized(tuple((math.sin((1.0 - fraction) * angle) * x
                             + math.sin(fraction * angle) * y) / sine
                            for x, y in zip(left, right)))


def exact_step_cost(left, right):
    correlation = dot(left, right)
    require(correlation != -1, "antipodal rational step")
    return (1 - correlation) / (1 + correlation)


def exact_path(left, right, exact_left, exact_right, length, denominator):
    parameters = tuple(stereographic(slerp(left, right, step / length), denominator)
                       for step in range(1, length))
    chain = [exact_left, *(rational_unit(row) for row in parameters), exact_right]
    cost = sum((exact_step_cost(a, b) for a, b in zip(chain, chain[1:])), Fraction())
    return parameters, cost


def shared_rationalize(paths, vectors, denominators):
    vectors = rotate_away_from_pole(vectors)
    for denominator in denominators:
        try:
            branches_p = tuple(stereographic(row, denominator) for row in vectors)
            branches = tuple(rational_unit(row) for row in branches_p)
            canonical, extended, base_costs, extended_costs = [], [], [], []
            for _, _, u, v, length in paths:
                endpoint = vectors[v] if length % 2 == 0 else tuple(-x for x in vectors[v])
                exact_endpoint = branches[v] if length % 2 == 0 else tuple(-x for x in branches[v])
                inside, cost = exact_path(vectors[u], endpoint, branches[u], exact_endpoint,
                                          length, denominator)
                longer, longer_cost = exact_path(vectors[u], endpoint, branches[u], exact_endpoint,
                                                  length + 2, denominator)
                canonical.append(inside)
                extended.append(longer)
                base_costs.append(cost)
                extended_costs.append(longer_cost)
        except (RuntimeError, ZeroDivisionError):
            continue
        base = sum(base_costs, Fraction())
        if all(value <= BUDGET for value in
               (base, *(base - base_costs[i] + extended_costs[i] for i in range(PATH_COUNT)))):
            return denominator, branches_p, tuple(canonical), tuple(extended)
    return None


def individual_rationalize(paths, vectors, denominators):
    vectors = rotate_away_from_pole(vectors)
    for denominator in denominators:
        try:
            branches_p = tuple(stereographic(row, denominator) for row in vectors)
            branches = tuple(rational_unit(row) for row in branches_p)
            internals, total = [], Fraction()
            for _, _, u, v, length in paths:
                endpoint = vectors[v] if length % 2 == 0 else tuple(-x for x in vectors[v])
                exact_endpoint = branches[v] if length % 2 == 0 else tuple(-x for x in branches[v])
                inside, cost = exact_path(vectors[u], endpoint, branches[u], exact_endpoint,
                                          length, denominator)
                internals.append(inside)
                total += cost
        except (RuntimeError, ZeroDivisionError):
            continue
        if total <= BUDGET:
            return denominator, branches_p, tuple(internals)
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


def put_parameters(output, denominator, rows):
    for row in rows:
        for value in row:
            require(denominator % value.denominator == 0, "parameter denominator is not shared")
            put_svarint(output, value.numerator * (denominator // value.denominator))


def encode_pack(census, start, records):
    output = bytearray(MAGIC)
    output.extend(bytes.fromhex(census.SOURCE_SHA256))
    put_uvarint(output, start)
    put_uvarint(output, len(records))
    for mode, payload in records:
        require(mode in (MODE_UNRESOLVED, MODE_SHARED, MODE_TEMPLATE, MODE_FALLBACK), "bad mode")
        output.append(mode)
        if mode in (MODE_UNRESOLVED, MODE_TEMPLATE):
            require(payload is None, "payload on empty mode")
        elif mode == MODE_SHARED:
            denominator, branches, canonical, extended = payload
            put_uvarint(output, denominator)
            put_parameters(output, denominator, branches)
            for family in (canonical, extended):
                for path in family:
                    put_parameters(output, denominator, path)
        else:
            bitmap = sum(1 << target for target, witness in enumerate(payload) if witness is not None)
            require(0 < bitmap < 1 << (PATH_COUNT + 1), "bad fallback bitmap")
            put_uvarint(output, bitmap)
            for witness in payload:
                if witness is None:
                    continue
                denominator, branches, internals = witness
                put_uvarint(output, denominator)
                put_parameters(output, denominator, branches)
                for path in internals:
                    put_parameters(output, denominator, path)
    return bytes(output)


def decode_pack(census, raw, residuals):
    header = len(MAGIC)
    require(raw[:header] == MAGIC and raw[header:header + 32] ==
            bytes.fromhex(census.SOURCE_SHA256), "bad pack header")
    position = header + 32
    start, position = get_uvarint(raw, position)
    count, position = get_uvarint(raw, position)
    require(start + count <= len(residuals), "pack range exceeds residual stream")
    records = []

    def vector(denominator):
        nonlocal position
        values = []
        for _ in range(DIMENSION - 1):
            value, position = get_svarint(raw, position)
            values.append(Fraction(value, denominator))
        return tuple(values)

    for local in range(count):
        require(position < len(raw), "truncated mode")
        mode = raw[position]
        position += 1
        source = residuals[start + local]
        lengths = tuple(path[4] for path in path_ledger(census, source))
        if mode in (MODE_UNRESOLVED, MODE_TEMPLATE):
            records.append((mode, None))
            continue
        require(mode in (MODE_SHARED, MODE_FALLBACK), "bad witness mode")
        if mode == MODE_SHARED:
            denominator, position = get_uvarint(raw, position)
            require(denominator > 0, "zero shared denominator")
            branches = tuple(vector(denominator) for _ in range(ORDER))
            canonical = tuple(tuple(vector(denominator) for _ in range(length - 1))
                              for length in lengths)
            extended = tuple(tuple(vector(denominator) for _ in range(length + 1))
                             for length in lengths)
            records.append((mode, (denominator, branches, canonical, extended)))
            continue
        bitmap, position = get_uvarint(raw, position)
        require(0 < bitmap < 1 << (PATH_COUNT + 1), "bad fallback bitmap")
        witnesses = []
        for target in range(PATH_COUNT + 1):
            if not bitmap & (1 << target):
                witnesses.append(None)
                continue
            denominator, position = get_uvarint(raw, position)
            require(denominator > 0, "zero fallback denominator")
            branches = tuple(vector(denominator) for _ in range(ORDER))
            widths = list(lengths)
            if target:
                widths[target - 1] += 2
            internals = tuple(tuple(vector(denominator) for _ in range(length - 1))
                              for length in widths)
            witnesses.append((denominator, branches, internals))
        records.append((mode, tuple(witnesses)))
    require(position == len(raw), "trailing pack bytes")
    return start, tuple(records)


def audit_parameters(denominator, rows):
    for row in rows:
        require(len(row) == DIMENSION - 1 and
                all(value.denominator > 0 and denominator % value.denominator == 0
                    for value in row), "bad stereographic parameter")


def verify_individual(census, source, target, witness):
    denominator, branches_p, internals = witness
    paths = path_ledger(census, source, None if target == 0 else target - 1)
    require(denominator > 0 and len(branches_p) == ORDER and
            len(internals) == PATH_COUNT, "bad fallback witness")
    audit_parameters(denominator, branches_p)
    branches = tuple(rational_unit(row) for row in branches_p)
    total = Fraction()
    for (_, _, u, v, length), parameters in zip(paths, internals):
        require(len(parameters) == length - 1, "fallback path width changed")
        audit_parameters(denominator, parameters)
        endpoint = branches[v] if length % 2 == 0 else tuple(-x for x in branches[v])
        chain = [branches[u], *(rational_unit(row) for row in parameters), endpoint]
        total += sum((exact_step_cost(a, b) for a, b in zip(chain, chain[1:])), Fraction())
    require(total <= BUDGET, "fallback exact cost exceeds five")


def verify_shared(census, source, witness):
    denominator, branches_p, canonical, extended = witness
    paths = path_ledger(census, source)
    require(denominator > 0 and len(branches_p) == ORDER and
            len(canonical) == len(extended) == PATH_COUNT, "bad shared witness")
    audit_parameters(denominator, branches_p)
    branches = tuple(rational_unit(row) for row in branches_p)
    for frontier in (None, *range(PATH_COUNT)):
        total = Fraction()
        for index, ((_, _, u, v, length), base, longer) in enumerate(
                zip(paths, canonical, extended)):
            parameters = longer if index == frontier else base
            require(len(parameters) == length - 1 + (2 if index == frontier else 0),
                    "shared path width changed")
            audit_parameters(denominator, parameters)
            endpoint = branches[v] if length % 2 == 0 else tuple(-x for x in branches[v])
            chain = [branches[u], *(rational_unit(row) for row in parameters), endpoint]
            total += sum((exact_step_cost(a, b) for a, b in zip(chain, chain[1:])), Fraction())
        require(total <= BUDGET, "shared exact cost exceeds five")


def verify_template(census, source):
    number, code, support, multiplicities, row, _, _, template = source
    require(number == 1133 and template, "bad K1133 template tag")
    specification = census.five_cycle_support(ORDER, code)
    require(specification is not None and census.candidate_row(
        support, multiplicities, row, specification), "K1133 template row changed")
    singles, doubles = specification
    values = {census.PAIRS[index]: odd for index, odd in zip(support, row)}
    bits = tuple(values[edge] for edge in singles)
    gram = census.cycle_gram(ORDER, singles, doubles, bits)
    census.audit_psd(gram)
    for edge, odd in zip(singles, bits):
        transformed = -gram[edge[0]][edge[1]] if odd else gram[edge[0]][edge[1]]
        require(transformed == 1, "K1133 singleton cost changed")
    require(sum((Fraction(1, 3) + Fraction(2, 3) for _ in doubles), Fraction()) == BUDGET,
            "K1133 template cost changed")
    paths = path_ledger(census, source)
    require(len(paths) == PATH_COUNT, "K1133 frontier width changed")
    for frontier in range(PATH_COUNT):
        extended = path_ledger(census, source, frontier)
        require(extended[frontier][4] == paths[frontier][4] + 2,
                "K1133 zero-cost extension changed")


def verify_record(census, source, record):
    mode, payload = record
    if mode == MODE_TEMPLATE:
        require(payload is None, "template payload present")
        verify_template(census, source)
    elif mode == MODE_SHARED:
        require(not source[-1], "template stored numerically")
        verify_shared(census, source, payload)
    elif mode == MODE_FALLBACK:
        require(not source[-1] and len(payload) == PATH_COUNT + 1 and any(payload),
                "bad fallback record")
        for target, witness in enumerate(payload):
            if witness is not None:
                verify_individual(census, source, target, witness)
    else:
        require(mode == MODE_UNRESOLVED and payload is None and not source[-1],
                "bad unresolved record")


def search(args, census, residuals):
    selected = residuals[args.start:args.start + args.count]
    denominators = tuple(int(value) for value in args.denominators.split(","))
    require(denominators and all(value > 0 for value in denominators), "bad denominators")
    records = []
    started = time.perf_counter()
    for local, source in enumerate(selected):
        if source[-1]:
            records.append((MODE_TEMPLATE, None))
            continue
        paths = path_ledger(census, source)
        value, vectors = optimize(paths, args.seed + 1009 * (args.start + local),
                                  args.restarts, args.iterations)
        shared = shared_rationalize(paths, vectors, denominators)
        fallbacks = None
        if shared is None:
            fallbacks = []
            for target in range(PATH_COUNT + 1):
                frontier = None if target == 0 else target - 1
                target_paths = path_ledger(census, source, frontier)
                witness = individual_rationalize(target_paths, vectors, denominators)
                if witness is None and args.fallback_restarts:
                    _, candidate = optimize(
                        target_paths, args.seed + 1009 * (args.start + local) + target + 1,
                        args.fallback_restarts, args.fallback_iterations, warm=(vectors,))
                    witness = individual_rationalize(target_paths, candidate, denominators)
                fallbacks.append(witness)
            records.append((MODE_FALLBACK, tuple(fallbacks)) if any(fallbacks)
                           else (MODE_UNRESOLVED, None))
        else:
            records.append((MODE_SHARED, shared))
        if args.progress:
            exact = 0 if fallbacks is None else sum(item is not None for item in fallbacks)
            print(f"[{local + 1}/{len(selected)}] numerical={value:.9f} "
                  f"shared_exact={shared is not None} fallback_exact={exact}", flush=True)
    raw = encode_pack(census, args.start, records)
    stored = lzma.compress(raw, format=lzma.FORMAT_XZ, preset=6)
    decoded_start, decoded = decode_pack(census, lzma.decompress(stored), residuals)
    require(decoded_start == args.start, "round-trip start changed")
    for source, record in zip(selected, decoded):
        verify_record(census, source, record)
    temporary = args.output.with_name(args.output.name + ".tmp")
    temporary.write_bytes(stored)
    temporary.replace(args.output)
    shared_count = sum(mode == MODE_SHARED for mode, _ in records)
    templates = sum(mode == MODE_TEMPLATE for mode, _ in records)
    fallback = sum(sum(item is not None for item in payload)
                   for mode, payload in records if mode == MODE_FALLBACK)
    unresolved = sum(PATH_COUNT + 1 for mode, _ in records if mode == MODE_UNRESOLVED)
    unresolved += sum(sum(item is None for item in payload)
                      for mode, payload in records if mode == MODE_FALLBACK)
    print(f"attempts={len(records)} shared_exact={shared_count} templates={templates} "
          f"fallback_exact={fallback} unresolved_targets={unresolved}")
    print(f"raw_bytes={len(raw)} xz_bytes={len(stored)} "
          f"elapsed_seconds={time.perf_counter() - started:.6f}")
    print(f"sha256={hashlib.sha256(stored).hexdigest()}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--count", type=int, default=0)
    parser.add_argument("--seed", type=int, default=101133)
    parser.add_argument("--restarts", type=int, default=2)
    parser.add_argument("--iterations", type=int, default=300)
    parser.add_argument("--fallback-restarts", type=int, default=2)
    parser.add_argument("--fallback-iterations", type=int, default=420)
    parser.add_argument("--denominators", default="256,1024,4096,16384,65536")
    parser.add_argument("--verify-pack", type=Path)
    parser.add_argument("--census-cache", type=Path)
    parser.add_argument("--progress", action="store_true")
    args = parser.parse_args()
    require(args.start >= 0 and args.count >= 0, "bad selected range")
    require(args.count > 0 or args.verify_pack is not None,
            "specify --count or --verify-pack; a full run is intentionally not implicit")
    census = load_census_module()
    started = time.perf_counter()
    require(args.census_cache is None or args.census_cache.parent.is_dir(),
            "census cache parent missing")
    residuals = residual_rows(census, args.progress and args.count == 0,
                             args.census_cache)
    census_seconds = time.perf_counter() - started
    if args.verify_pack is not None:
        raw = lzma.decompress(args.verify_pack.read_bytes(), format=lzma.FORMAT_XZ)
        start, records = decode_pack(census, raw, residuals)
        for source, record in zip(residuals[start:start + len(records)], records):
            verify_record(census, source, record)
        shared = sum(mode == MODE_SHARED for mode, _ in records)
        templates = sum(mode == MODE_TEMPLATE for mode, _ in records)
        fallback = sum(sum(item is not None for item in payload)
                       for mode, payload in records if mode == MODE_FALLBACK)
        print(f"attempts={len(records)} shared_exact={shared} templates={templates} "
              f"fallback_exact={fallback} exact_audit=true census_seconds={census_seconds:.6f}")
        return
    require(args.start < len(residuals) and args.start + args.count <= len(residuals),
            "selected range exceeds residual stream")
    require(args.output is not None and args.output.parent.is_dir(), "output parent missing")
    search(args, census, residuals)


if __name__ == "__main__":
    main()
