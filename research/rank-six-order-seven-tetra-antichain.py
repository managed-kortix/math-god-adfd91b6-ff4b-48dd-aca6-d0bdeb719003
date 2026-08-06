#!/usr/bin/env python3
"""Exact order-seven rank-six tetrahedral residual discovery.

This is a computational experiment, not a theorem verifier.  It exhausts the
physical parity orbits, applies the regular-tetrahedron Gram upper bound, and
compresses the residual down-sets into supportwise maximal antichains.
"""

import argparse
import hashlib
import itertools
import json
import multiprocessing
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "fixtures" / "rank-six-kernels.json"
OUTPUT = HERE / "fixtures" / "rank-six-order-seven-tetra-antichain.json"
DEFAULT_CENSUS = (HERE.parent / "positive-square-energy" / "experiments"
                  / "rank6_order7_orbit_frontier_census.json")
SOURCE_SHA256 = "5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476"
ORDER = 7
RANK = 6
PATH_COUNT = ORDER + RANK - 1
BUDGET = Fraction(RANK - 1)
PAIRS = tuple(itertools.combinations(range(ORDER), 2))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def partition_colorings(prefix=(0,)):
    if len(prefix) == ORDER:
        yield prefix
        return
    for color in range(min(3, max(prefix) + 1) + 1):
        yield from partition_colorings(prefix + (color,))


COLORINGS = tuple(partition_colorings())
CUTS = tuple(tuple(coloring[u] != coloring[v] for u, v in PAIRS)
             for coloring in COLORINGS)


def relabel(row, permutation):
    lookup = dict(zip(PAIRS, row))
    return tuple(lookup[tuple(sorted((permutation[u], permutation[v])))] for u, v in PAIRS)


def automorphisms(kernel):
    return tuple(permutation for permutation in itertools.permutations(range(ORDER))
                 if relabel(kernel, permutation) == kernel)


def tetra_cost(kernel, row, cut):
    total = Fraction(0)
    for multiplicity, odd, separated in zip(kernel, row, cut):
        if odd and not separated:
            return None
        if separated:
            total += Fraction(3 * multiplicity, 5)
            if odd:
                total += Fraction(1, 3) - Fraction(13 * odd, 30)
    return total


def minimum_tetra_cost(kernel, row):
    candidates = (tetra_cost(kernel, row, cut) for cut in CUTS)
    return min(value for value in candidates if value is not None)


def support_mask(row):
    return sum(1 << index for index, value in enumerate(row) if value)


def dominates(left, right):
    return all(x >= y for x, y in zip(left, right))


def maximal_antichain(rows):
    ordered = sorted(rows, key=lambda row: (sum(row), row), reverse=True)
    maxima = []
    for row in ordered:
        if not any(dominates(maximum, row) for maximum in maxima):
            maxima.append(row)
    return tuple(sorted(maxima))


def adjacency_from_row(row):
    adjacency = [set() for _ in range(ORDER)]
    for value, (u, v) in zip(row, PAIRS):
        if value:
            adjacency[u].add(v)
            adjacency[v].add(u)
    return adjacency


def connected(adjacency, vertices):
    vertices = set(vertices)
    if not vertices:
        return False
    seen = {min(vertices)}
    stack = list(seen)
    while stack:
        vertex = stack.pop()
        for neighbor in adjacency[vertex] & vertices - seen:
            seen.add(neighbor)
            stack.append(neighbor)
    return seen == vertices


def is_tree(adjacency, vertices):
    vertices = tuple(vertices)
    edges = sum(len(adjacency[vertex] & set(vertices)) for vertex in vertices) // 2
    return connected(adjacency, vertices) and edges == len(vertices) - 1


def clique_tree_candidates(row):
    adjacency = adjacency_from_row(row)
    candidates = []
    vertices = set(range(ORDER))
    for width in range(6, 3, -1):
        for clique in itertools.combinations(range(ORDER), width):
            clique_set = set(clique)
            if not all(v in adjacency[u] for u, v in itertools.combinations(clique, 2)):
                continue
            remainder = tuple(sorted(vertices - clique_set))
            if remainder and is_tree(adjacency, remainder):
                candidates.append({"clique": list(clique), "tree": list(remainder)})
        if candidates:
            break
    return candidates


def packet_signature(kernel, row, candidates):
    adjacency = adjacency_from_row(row)
    unit_degrees = sorted((len(neighbors) for neighbors in adjacency), reverse=True)
    return (f"unit_edges={sum(bool(x) for x in row)};"
            f"unit_degrees={','.join(map(str, unit_degrees))};"
            f"odd_long={sum(max(0, x - 1) for x in row)};"
            f"even_paths={sum(m - x for m, x in zip(kernel, row))};"
            f"clique_tree={int(bool(candidates))}")


def source_kernels():
    raw = SOURCE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, "rank-six source changed")
    payload = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(payload), "rank-six source is not canonical JSON")
    records = tuple((index, tuple(record["code"]))
                    for index, record in enumerate(payload["kernels"], 1)
                    if record["n"] == ORDER)
    require(len(records) == 314, "order-seven kernel count changed")
    require(all(sum(kernel) == PATH_COUNT for _, kernel in records), "path count changed")
    return records


def census_kernel(item):
    number, kernel = item
    group = automorphisms(kernel)
    orbit_sizes = {}
    for row in itertools.product(*(range(value + 1) for value in kernel)):
        representative = min(relabel(row, permutation) for permutation in group)
        orbit_sizes[representative] = orbit_sizes.get(representative, 0) + 1
    residual_costs = {}
    by_support = {}
    for row in sorted(orbit_sizes):
        cost = minimum_tetra_cost(kernel, row)
        if cost > BUDGET:
            residual_costs[row] = cost
            by_support.setdefault(support_mask(row), []).append(row)
    maxima = tuple(row for mask in sorted(by_support)
                   for row in maximal_antichain(by_support[mask]))
    antichain = []
    packet_counts = {}
    candidate_count = 0
    for row in maxima:
        mask = support_mask(row)
        dominated = [other for other in by_support[mask] if dominates(row, other)]
        candidates = clique_tree_candidates(row)
        candidate_count += bool(candidates)
        signature = packet_signature(kernel, row, candidates)
        packet_counts[signature] = packet_counts.get(signature, 0) + 1
        cost = residual_costs[row]
        antichain.append({
            "kernel": number,
            "row": list(row),
            "support_mask": mask,
            "minimum_tetra_upper_bound": [cost.numerator, cost.denominator],
            "dominated_residual_representatives": len(dominated),
            "dominated_residual_orbit_mass": sum(orbit_sizes[other] for other in dominated),
            "packet_signature": signature,
            "clique_tree_candidates": candidates,
        })
    ledger = {
        "kernel": number,
        "code": list(kernel),
        "automorphisms": len(group),
        "physical_rows": sum(orbit_sizes.values()),
        "orbits": len(orbit_sizes),
        "tetra_certified": len(orbit_sizes) - len(residual_costs),
        "tetra_residuals": len(residual_costs),
        "residual_orbit_mass": sum(orbit_sizes[row] for row in residual_costs),
        "antichain_rows": len(antichain),
        "candidate_rows": candidate_count,
    }
    return ledger, antichain, packet_counts


def regenerate(jobs=1, progress=False):
    sources = source_kernels()
    if jobs == 1:
        results = map(census_kernel, sources)
        pool = None
    else:
        pool = multiprocessing.Pool(jobs)
        results = pool.imap(census_kernel, sources)
    ledgers, antichain, packet_counts = [], [], {}
    try:
        for index, (ledger, local_rows, local_packets) in enumerate(results, 1):
            ledgers.append(ledger)
            antichain.extend(local_rows)
            for key, value in local_packets.items():
                packet_counts[key] = packet_counts.get(key, 0) + value
            if progress:
                print(f"[{index}/314] K{ledger['kernel']} orbits={ledger['orbits']} "
                      f"residual={ledger['tetra_residuals']} antichain={ledger['antichain_rows']}",
                      flush=True)
    finally:
        if pool is not None:
            pool.close()
            pool.join()
    return {
        "schema": "rank-six-order-seven-tetra-antichain-experiment-v1",
        "status": "exact_discovery_residual_open",
        "full_theorem": False,
        "certificate_fixture_frozen": False,
        "source_sha256": SOURCE_SHA256,
        "rank": RANK,
        "order": ORDER,
        "path_count": PATH_COUNT,
        "budget": [BUDGET.numerator, BUDGET.denominator],
        "gram": {"colors": 4, "diagonal": [1, 1], "off_diagonal": [-1, 3]},
        "pair_order": [f"{u}{v}" for u, v in PAIRS],
        "antichain_policy": "supportwise coordinate-maximal tetra residual orbit representatives",
        "candidate_policy": "unit-edge induced K4/K5/K6 with nonempty complementary unit-edge tree",
        "kernel_total": len(ledgers),
        "physical_total": sum(row["physical_rows"] for row in ledgers),
        "orbit_total": sum(row["orbits"] for row in ledgers),
        "tetra_certified_total": sum(row["tetra_certified"] for row in ledgers),
        "tetra_residual_total": sum(row["tetra_residuals"] for row in ledgers),
        "residual_orbit_mass": sum(row["residual_orbit_mass"] for row in ledgers),
        "antichain_total": len(antichain),
        "candidate_row_total": sum(row["candidate_rows"] for row in ledgers),
        "packet_signature_counts": dict(sorted(packet_counts.items())),
        "kernels": ledgers,
        "antichain": antichain,
    }


def classify_census(path):
    raw = path.read_bytes()
    census = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(census), "source census is not canonical JSON")
    require(census["schema"] == "rank-six-order-seven-orbit-frontier-census-experiment-v1",
            "wrong source census schema")
    require((census["source_sha256"], census["kernel_total"], census["path_count"],
             census["budget"], census["cost_scale"])
            == (SOURCE_SHA256, 314, 12, [5, 1], 30), "source census scope changed")
    require(census["full_theorem"] is False, "source census was theorem-promoted")
    residuals = {}
    for record in census["residuals"]:
        key = record["kernel"], tuple(record["row"])
        require(key not in residuals, "duplicate source residual")
        residuals[key] = record
    require(len(residuals) == census["coarse_residual_total"], "source residual total changed")

    antichain = []
    packet_counts = {}
    ledgers = []
    for source in census["kernels"]:
        number, kernel = source["kernel"], tuple(source["code"])
        local = {row: record for (owner, row), record in residuals.items() if owner == number}
        by_support = {}
        for row in local:
            by_support.setdefault(support_mask(row), []).append(row)
        maxima = tuple(row for mask in sorted(by_support)
                       for row in maximal_antichain(by_support[mask]))
        candidate_count = 0
        for row in maxima:
            record = local[row]
            exact_cost = Fraction(record["minimum_coarse_upper_bound_scaled_30"], 30)
            require(exact_cost > BUDGET, "source residual status changed")
            mask = support_mask(row)
            dominated = [other for other in by_support[mask] if dominates(row, other)]
            candidates = clique_tree_candidates(row)
            candidate_count += bool(candidates)
            signature = packet_signature(kernel, row, candidates)
            packet_counts[signature] = packet_counts.get(signature, 0) + 1
            antichain.append({
                "kernel": number,
                "row": list(row),
                "support_mask": mask,
                "minimum_tetra_upper_bound": [exact_cost.numerator, exact_cost.denominator],
                "dominated_residual_representatives": len(dominated),
                "dominated_residual_orbit_mass": sum(local[other]["orbit_size"]
                                                     for other in dominated),
                "packet_signature": signature,
                "clique_tree_candidates": candidates,
            })
        ledger = dict(source)
        ledger.update({
            "tetra_certified": ledger.pop("coarse_certified"),
            "tetra_residuals": ledger.pop("coarse_residuals"),
            "residual_orbit_mass": sum(record["orbit_size"] for record in local.values()),
            "antichain_rows": len(maxima),
            "candidate_rows": candidate_count,
        })
        ledgers.append(ledger)
    return {
        "schema": "rank-six-order-seven-tetra-antichain-experiment-v1",
        "status": "exact_discovery_residual_open",
        "full_theorem": False,
        "certificate_fixture_frozen": False,
        "source_sha256": SOURCE_SHA256,
        "source_census_sha256": hashlib.sha256(raw).hexdigest(),
        "rank": RANK,
        "order": ORDER,
        "path_count": PATH_COUNT,
        "budget": [BUDGET.numerator, BUDGET.denominator],
        "gram": {"colors": 4, "diagonal": [1, 1], "off_diagonal": [-1, 3]},
        "pair_order": [f"{u}{v}" for u, v in PAIRS],
        "antichain_policy": "supportwise coordinate-maximal tetra residual orbit representatives",
        "candidate_policy": "unit-edge induced K4/K5/K6 with nonempty complementary unit-edge tree",
        "kernel_total": len(ledgers),
        "physical_total": census["physical_total"],
        "orbit_total": census["orbit_total"],
        "tetra_certified_total": census["coarse_certified_total"],
        "tetra_residual_total": census["coarse_residual_total"],
        "residual_orbit_mass": sum(row["residual_orbit_mass"] for row in ledgers),
        "antichain_total": len(antichain),
        "candidate_row_total": sum(row["candidate_rows"] for row in ledgers),
        "packet_signature_counts": dict(sorted(packet_counts.items())),
        "kernels": ledgers,
        "antichain": antichain,
    }


def verify(payload, source_census=None):
    require(payload["full_theorem"] is False, "experiment was theorem-promoted")
    require(payload["certificate_fixture_frozen"] is False, "experiment was fixture-promoted")
    require(payload["kernel_total"] == 314 and payload["path_count"] == 12, "scope changed")
    require(payload["tetra_certified_total"] + payload["tetra_residual_total"]
            == payload["orbit_total"], "tetra partition changed")
    require(payload["antichain_total"] == len(payload["antichain"]), "antichain total changed")
    require(payload["candidate_row_total"]
            == sum(bool(row["clique_tree_candidates"]) for row in payload["antichain"]),
            "candidate total changed")
    keys = {(row["kernel"], tuple(row["row"])) for row in payload["antichain"]}
    require(len(keys) == len(payload["antichain"]), "duplicate antichain key")
    if source_census is not None:
        require(payload == classify_census(source_census),
                "artifact differs from exact source-census classification")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--verify", type=Path)
    parser.add_argument("--census", type=Path)
    args = parser.parse_args()
    require(args.jobs >= 1, "jobs must be positive")
    if args.verify:
        raw = args.verify.read_bytes()
        payload = json.loads(raw.decode("ascii"))
        require(raw == canonical_bytes(payload), "artifact is not canonical JSON")
        census_path = args.census
        if census_path is None and DEFAULT_CENSUS.is_file():
            census_path = DEFAULT_CENSUS
    else:
        census_path = args.census
        if census_path is None and DEFAULT_CENSUS.is_file():
            census_path = DEFAULT_CENSUS
        payload = classify_census(census_path) if census_path else regenerate(args.jobs, args.progress)
        if args.write:
            require(OUTPUT.parent.is_dir(), "output parent missing")
            OUTPUT.write_bytes(canonical_bytes(payload))
    verify(payload, census_path if args.verify else None)
    print("order-seven rank-six tetrahedral antichain experiment: exact checks passed")
    print(f"kernels={payload['kernel_total']} physical={payload['physical_total']} "
          f"orbits={payload['orbit_total']}")
    print(f"tetra_certified={payload['tetra_certified_total']} "
          f"residual={payload['tetra_residual_total']} antichain={payload['antichain_total']}")
    print(f"candidate_rows={payload['candidate_row_total']} full_theorem=false")
    if args.write or args.verify:
        path = OUTPUT if args.write else args.verify
        print(f"artifact_sha256={hashlib.sha256(path.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
