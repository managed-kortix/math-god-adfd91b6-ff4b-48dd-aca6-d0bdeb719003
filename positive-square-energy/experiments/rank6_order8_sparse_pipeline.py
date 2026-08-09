#!/usr/bin/env python3
"""Sparse order-eight/rank-six census and compact exact-Gram prototype.

The census never materializes dense 28-coordinate parity rows or a JSON target
ledger.  It uses support coordinates, degree-class automorphisms, mixed-radix
orbit traversal, and a superset-min transform for the tetrahedral sieve.

The optional search writes a binary XZ stream.  It stores a shared realization
when possible and otherwise a success bitmap plus exact per-target witnesses.
Symbolic signed-cycle rows have a payload-free template tag.  Costs, rows, path
lengths, and unchanged metadata are reconstructed, not stored.  This is an
experiment and is not a theorem fixture.
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
MAGIC = b"R8G2"
SCHEMA = "rank-six-order-eight-sparse-pipeline-experiment-v2"
MODE_UNRESOLVED = 0
MODE_SHARED = 1
MODE_TEMPLATE = 2
MODE_INDIVIDUAL = 3
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


def verify_signed_cycle_template(source):
    number, support, multiplicities, row, _, _, template = source
    require(template and signed_cycle_template(number, support, multiplicities, row),
            "bad signed-cycle template tag")
    singles, doubles = SIGNED_CYCLE_SUPPORTS[number]
    values = {f"{PAIRS[index][0]}{PAIRS[index][1]}": (multiplicity, odd)
              for index, multiplicity, odd in zip(support, multiplicities, row)}
    parent = list(range(ORDER))
    sign = [1] * ORDER
    for edge in sorted(singles):
        left, right = map(int, edge)
        require(parent[right] == right, "bad singleton forest orientation")
        parent[right] = parent[left]
        sign[right] = sign[left] * (-1 if values[edge][1] else 1)
    require(len(set(parent)) == 5, "wrong signed-cycle quotient width")
    gram = [[Fraction() for _ in range(ORDER)] for _ in range(ORDER)]
    for left in range(ORDER):
        for right in range(ORDER):
            if parent[left] == parent[right]:
                gram[left][right] = Fraction(sign[left] * sign[right])
    for edge in sorted(doubles):
        left, right = map(int, edge)
        value = Fraction(-sign[left] * sign[right], 2)
        for u in range(ORDER):
            if parent[u] != parent[left]:
                continue
            for v in range(ORDER):
                if parent[v] == parent[right]:
                    gram[u][v] = gram[v][u] = sign[u] * sign[v] * value

    def determinant(matrix):
        work = [list(values) for values in matrix]
        result = Fraction(1)
        for column in range(len(work)):
            pivot = next((index for index in range(column, len(work))
                          if work[index][column]), None)
            if pivot is None:
                return Fraction()
            if pivot != column:
                work[column], work[pivot] = work[pivot], work[column]
                result = -result
            value = work[column][column]
            result *= value
            for index in range(column + 1, len(work)):
                scale = work[index][column] / value
                for offset in range(column + 1, len(work)):
                    work[index][offset] -= scale * work[column][offset]
        return result

    require(all(gram[index][index] == 1 for index in range(ORDER)),
            "signed-cycle Gram diagonal changed")
    for width in range(1, ORDER + 1):
        for indices in itertools.combinations(range(ORDER), width):
            minor = [[gram[left][right] for right in indices] for left in indices]
            require(determinant(minor) >= 0, "signed-cycle Gram is not PSD")
    for edge in singles:
        left, right = map(int, edge)
        transformed = -gram[left][right] if values[edge][1] else gram[left][right]
        require(transformed == 1, "singleton symbolic cost changed")
    for edge in doubles:
        left, right = map(int, edge)
        require(gram[left][right] in (Fraction(-1, 2), Fraction(1, 2)),
                "doubled-bundle correlation changed")
    cost = sum((Fraction(1, 3) + Fraction(2, 3) for _ in doubles), Fraction())
    require(cost == BUDGET, "signed-cycle symbolic cost changed")
    for frontier in (None, *range(PATH_COUNT)):
        require(frontier is None or 0 <= frontier < PATH_COUNT, "bad template frontier")
        require(cost + (Fraction() if frontier is None else 2 * Fraction(1 - 1, 1 + 1))
                == BUDGET, "signed-cycle extension cost changed")


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


def individual_rationalize(engine, paths, vectors, denominators):
    vectors = engine.rotate_away_from_pole(vectors)
    for denominator in denominators:
        try:
            branch_parameters = tuple(engine.stereographic(row, denominator) for row in vectors)
            branches = tuple(engine.rational_unit(row) for row in branch_parameters)
            internals = []
            total = Fraction()
            for _, _, u, v, length in paths:
                endpoint = vectors[v] if length % 2 == 0 else tuple(-x for x in vectors[v])
                exact_endpoint = branches[v] if length % 2 == 0 else tuple(-x for x in branches[v])
                parameters = tuple(engine.stereographic(
                    engine.slerp(vectors[u], endpoint, step / length), denominator)
                                   for step in range(1, length))
                chain = [branches[u], *(engine.rational_unit(value) for value in parameters),
                         exact_endpoint]
                total += sum((engine.exact_step_cost(a, b) for a, b in zip(chain, chain[1:])),
                             Fraction())
                internals.append(parameters)
        except (RuntimeError, ZeroDivisionError):
            continue
        if total <= BUDGET:
            return denominator, branch_parameters, tuple(internals)
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


def put_parameters(output, denominator, rows):
    for row in rows:
        for value in row:
            put_svarint(output, scaled_numerator(value, denominator))


def encode_search(start, attempts, records):
    require(attempts == len(records), "search record count changed")
    output = bytearray(MAGIC)
    output.extend(bytes.fromhex(SOURCE_SHA256))
    put_uvarint(output, start)
    put_uvarint(output, attempts)
    for record in records:
        mode, payload = record
        require(mode in (MODE_UNRESOLVED, MODE_SHARED, MODE_TEMPLATE, MODE_INDIVIDUAL),
                "bad search record mode")
        output.append(mode)
        if mode in (MODE_UNRESOLVED, MODE_TEMPLATE):
            require(payload is None, "payload on payload-free record")
            continue
        if mode == MODE_SHARED:
            denominator, branches, canonical, extended = payload
            put_uvarint(output, denominator)
            put_parameters(output, denominator, branches)
            for family in (canonical, extended):
                for path in family:
                    put_parameters(output, denominator, path)
            continue
        bitmap = sum(1 << target for target, witness in enumerate(payload) if witness is not None)
        require(0 < bitmap < 1 << (PATH_COUNT + 1), "bad individual target bitmap")
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


def decode_search(raw, residual_rows):
    require(raw[:4] == MAGIC and raw[4:36] == bytes.fromhex(SOURCE_SHA256), "bad pack header")
    position = 36
    start, position = get_uvarint(raw, position)
    attempts, position = get_uvarint(raw, position)
    require(start + attempts <= len(residual_rows), "pack range exceeds census")
    records = []
    for local in range(attempts):
        require(position < len(raw) and raw[position] in
                (MODE_UNRESOLVED, MODE_SHARED, MODE_TEMPLATE, MODE_INDIVIDUAL),
                "bad witness tag")
        mode = raw[position]
        position += 1
        source = residual_rows[start + local]
        _, _, multiplicities, row, _, _, template = source
        lengths = canonical_path_lengths(multiplicities, row)
        if mode == MODE_UNRESOLVED:
            require(not template, "template encoded as unresolved")
            records.append((mode, None))
            continue
        if mode == MODE_TEMPLATE:
            require(template, "template tag on numerical row")
            records.append((mode, None))
            continue
        def vector(denominator):
            nonlocal position
            values = []
            for _ in range(ORDER - 1):
                value, position = get_svarint(raw, position)
                values.append(Fraction(value, denominator))
            return tuple(values)
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
        require(0 < bitmap < 1 << (PATH_COUNT + 1), "bad individual target bitmap")
        witnesses = []
        for target in range(PATH_COUNT + 1):
            if not bitmap & (1 << target):
                witnesses.append(None)
                continue
            denominator, position = get_uvarint(raw, position)
            require(denominator > 0, "zero individual denominator")
            target_lengths = list(lengths)
            if target:
                target_lengths[target - 1] += 2
            branches = tuple(vector(denominator) for _ in range(ORDER))
            internals = tuple(tuple(vector(denominator) for _ in range(length - 1))
                              for length in target_lengths)
            witnesses.append((denominator, branches, internals))
        records.append((mode, tuple(witnesses)))
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
    costs = []
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
        costs.append(total)
    return tuple(costs)


def verify_individual_witness(engine, source, target, witness):
    _, support, multiplicities, row, _, _, _ = source
    kernel = dense_kernel(support, multiplicities)
    parity = dense_row(support, row)
    frontier = None if target == 0 else target - 1
    paths = engine.path_ledger(kernel, parity, frontier)
    denominator, branch_parameters, internals = witness
    require(denominator > 0 and len(branch_parameters) == ORDER and
            len(internals) == PATH_COUNT, "bad individual witness")
    for parameters in branch_parameters:
        require(len(parameters) == ORDER - 1 and
                all(denominator % value.denominator == 0 for value in parameters),
                "individual branch denominator changed")
    branches = tuple(engine.rational_unit(value) for value in branch_parameters)
    total = Fraction()
    for (_, _, u, v, length), parameters in zip(paths, internals):
        require(len(parameters) == length - 1, "individual path width changed")
        for value in parameters:
            require(len(value) == ORDER - 1 and
                    all(denominator % coordinate.denominator == 0 for coordinate in value),
                    "individual internal denominator changed")
        endpoint = branches[v] if length % 2 == 0 else tuple(-x for x in branches[v])
        chain = [branches[u], *(engine.rational_unit(value) for value in parameters), endpoint]
        total += sum((engine.exact_step_cost(a, b) for a, b in zip(chain, chain[1:])),
                     Fraction())
    require(total <= BUDGET, "individual exact cost exceeds five")
    return total


def verify_record(engine, source, record):
    mode, payload = record
    if mode == MODE_TEMPLATE:
        require(payload is None, "payload on template record")
        verify_signed_cycle_template(source)
        return (BUDGET,) * (PATH_COUNT + 1)
    elif mode == MODE_SHARED:
        require(not source[-1], "template stored numerically")
        return verify_witness(engine, source, payload)
    elif mode == MODE_INDIVIDUAL:
        require(not source[-1] and type(payload) is tuple and
                len(payload) == PATH_COUNT + 1 and any(payload),
                "bad individual record")
        return tuple(None if witness is None else
                     verify_individual_witness(engine, source, target, witness)
                     for target, witness in enumerate(payload))
    else:
        require(mode == MODE_UNRESOLVED and payload is None and not source[-1],
                "bad unresolved record")
        return (None,) * (PATH_COUNT + 1)


def search(args, residual_rows):
    engine = load_engine()
    selected = residual_rows[args.start:args.start + args.search_count]
    denominators = tuple(int(value) for value in args.denominators.split(","))
    require(denominators and all(value > 0 for value in denominators), "bad denominators")
    records = []
    for local, source in enumerate(selected):
        _, support, multiplicities, row, _, _, template = source
        if template:
            records.append((MODE_TEMPLATE, None))
            continue
        paths = engine.path_ledger(dense_kernel(support, multiplicities), dense_row(support, row))
        value, vectors = engine.optimize(paths, args.seed + 1009 * (args.start + local),
                                         args.restarts, args.iterations)
        witness = shared_rationalize(engine, paths, vectors, denominators)
        individual = None
        if witness is None:
            individual = []
            for target in range(PATH_COUNT + 1):
                frontier = None if target == 0 else target - 1
                target_paths = paths if frontier is None else engine.path_ledger(
                    dense_kernel(support, multiplicities), dense_row(support, row), frontier)
                candidate = vectors
                exact = individual_rationalize(engine, target_paths, candidate, denominators)
                if exact is None and args.fallback_restarts:
                    _, candidate = engine.optimize(
                        target_paths, args.seed + 1009 * (args.start + local) + target + 1,
                        args.fallback_restarts, args.fallback_iterations, warm=(vectors,))
                    exact = individual_rationalize(engine, target_paths, candidate, denominators)
                individual.append(exact)
            mode = MODE_INDIVIDUAL if any(item is not None for item in individual) else MODE_UNRESOLVED
            records.append((mode, tuple(individual) if mode == MODE_INDIVIDUAL else None))
        else:
            records.append((MODE_SHARED, witness))
        if args.progress:
            fallback_exact = 0 if individual is None else sum(x is not None for x in individual)
            print(f"[{local + 1}/{len(selected)}] numerical={value:.9f} "
                  f"shared_exact={witness is not None} fallback_exact={fallback_exact}", flush=True)
    raw = encode_search(args.start, len(selected), records)
    stored = lzma.compress(raw, format=lzma.FORMAT_XZ, preset=6)
    for source, record in zip(selected, records):
        verify_record(engine, source, record)
    temporary = args.output.with_name(args.output.name + ".tmp")
    temporary.write_bytes(stored)
    temporary.replace(args.output)
    shared = sum(record[0] == MODE_SHARED for record in records)
    templates = sum(record[0] == MODE_TEMPLATE for record in records)
    fallback = sum(sum(witness is not None for witness in record[1])
                   for record in records if record[0] == MODE_INDIVIDUAL)
    unresolved = sum(PATH_COUNT + 1 for record in records if record[0] == MODE_UNRESOLVED)
    unresolved += sum(sum(witness is None for witness in record[1])
                      for record in records if record[0] == MODE_INDIVIDUAL)
    print(f"attempts={len(selected)} shared_exact={shared} templates={templates} "
          f"fallback_exact={fallback} unresolved_targets={unresolved} "
          f"raw_bytes={len(raw)} xz_bytes={len(stored)}")
    print(f"sha256={hashlib.sha256(stored).hexdigest()}")


def main():
    global CENSUS_CACHE
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--search-count", type=int, default=0)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--seed", type=int, default=86131)
    parser.add_argument("--restarts", type=int, default=2)
    parser.add_argument("--iterations", type=int, default=260)
    parser.add_argument("--fallback-restarts", type=int, default=2)
    parser.add_argument("--fallback-iterations", type=int, default=360)
    parser.add_argument("--denominators", default="256,1024,4096,16384,65536")
    parser.add_argument("--verify-pack", type=Path)
    parser.add_argument("--census-cache", type=Path)
    args = parser.parse_args()
    CENSUS_CACHE = args.census_cache
    require(CENSUS_CACHE is None or CENSUS_CACHE.parent.is_dir(),
            "census cache parent missing")
    require(args.start >= 0 and args.search_count >= 0, "bad selected range")
    need_rows = args.search_count > 0 or args.verify_pack is not None
    payload, residual_rows = census(need_rows, args.progress and not args.search_count)
    if args.verify_pack is not None:
        raw = lzma.decompress(args.verify_pack.read_bytes(), format=lzma.FORMAT_XZ)
        start, attempts, records = decode_search(raw, residual_rows)
        engine = load_engine()
        selected = residual_rows[start:start + attempts]
        for source, record in zip(selected, records):
            verify_record(engine, source, record)
        shared = sum(record[0] == MODE_SHARED for record in records)
        templates = sum(record[0] == MODE_TEMPLATE for record in records)
        fallback = sum(sum(witness is not None for witness in record[1])
                       for record in records if record[0] == MODE_INDIVIDUAL)
        print(f"attempts={attempts} shared_exact={shared} templates={templates} "
              f"fallback_exact={fallback} exact_audit=true")
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
