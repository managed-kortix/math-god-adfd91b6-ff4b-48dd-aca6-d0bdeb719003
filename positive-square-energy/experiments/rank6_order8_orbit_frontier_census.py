#!/usr/bin/env python3
"""Exact order-eight rank-six orbit and canonical/coordinate frontier census.

This is a finite experimental census, not a theorem artifact.  The tetrahedral
DNN sieve uses integer arithmetic scaled by 30.  Digests commit to ordered
kernel, orbit, residual, and frontier-key streams without materializing the
much larger frontier stream in the JSON payload.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import multiprocessing
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "research" / "fixtures" / "rank-six-kernels.json"
OUTPUT = HERE / "rank6_order8_orbit_frontier_census.json"
SOURCE_SHA256 = "5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476"
SCHEMA = "rank-six-order-eight-orbit-coordinate-frontier-census-experiment-v1"
ORDER = 8
RANK = 6
PATH_COUNT = ORDER + RANK - 1
BUDGET_SCALED = 30 * (RANK - 1)
PAIRS = tuple(itertools.combinations(range(ORDER), 2))
PAIR_INDEX = {edge: index for index, edge in enumerate(PAIRS)}
FRONTIERS = (None, *range(PATH_COUNT))
EXPECTED_TOTALS = (1598512, 1045292, 942304, 102988, 1441832)
EXPECTED_DIGESTS = {
    "kernel_stream_sha256": "37646f53c89bd904c7e04c687ce90e52be3aea414810499e749ce95493aab0ea",
    "orbit_manifest_sha256": "40ce2900c0e2f9887d46f9bf1dfe4eb21ad8b0cc1c4e71179a56d49b34220b3e",
    "residual_stream_sha256": "b451837e04a30e5b71eba5fe631841eee73bbb8f3722a0b6bd25b666ad4fe900",
    "frontier_key_stream_sha256": "52439257eaa2b5a6bc2976f5c4199a5a06e3e3b6ab8afc61b2ad7c734876e97d",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def stream_line(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":"),
                      allow_nan=False).encode("ascii") + b"\n"


def reject_constant(value):
    raise ValueError(f"nonstandard JSON constant: {value}")


def load_json(raw):
    return json.loads(raw.decode("ascii"), parse_constant=reject_constant)


def relabel_action(permutation):
    return tuple(PAIR_INDEX[tuple(sorted((permutation[u], permutation[v])))] for u, v in PAIRS)


def apply_action(row, action):
    return tuple(row[index] for index in action)


def vertex_signature(kernel, vertex):
    incident = [kernel[PAIR_INDEX[tuple(sorted((vertex, other)))]]
                for other in range(ORDER) if other != vertex]
    return sum(incident), tuple(sorted(incident))


def automorphism_actions(kernel):
    cells = {}
    for vertex in range(ORDER):
        cells.setdefault(vertex_signature(kernel, vertex), []).append(vertex)
    ordered_cells = tuple(tuple(cell) for _, cell in sorted(cells.items()))
    actions = []
    for images in itertools.product(*(itertools.permutations(cell) for cell in ordered_cells)):
        permutation = list(range(ORDER))
        for cell, image in zip(ordered_cells, images):
            for source, target in zip(cell, image):
                permutation[source] = target
        action = relabel_action(permutation)
        if apply_action(kernel, action) == kernel:
            actions.append(action)
    require(actions, "kernel has no identity automorphism")
    return tuple(actions)


def color_patterns(prefix=(0,)):
    if len(prefix) == ORDER:
        yield prefix
        return
    for color in range(min(3, max(prefix) + 1) + 1):
        yield from color_patterns(prefix + (color,))


def difference_bits(coloring):
    result = 0
    for index, (u, v) in enumerate(PAIRS):
        if coloring[u] != coloring[v]:
            result |= 1 << index
    return result


COLOR_MASKS = tuple(dict.fromkeys(difference_bits(coloring) for coloring in color_patterns()))


def minimum_tetrahedral_cost_scaled(kernel, row):
    odd_bits = 0
    weights = []
    for index, (multiplicity, odd) in enumerate(zip(kernel, row)):
        if odd:
            odd_bits |= 1 << index
        weights.append(18 * multiplicity + (10 - 13 * odd if odd else 0))
    best = None
    for mask in COLOR_MASKS:
        if odd_bits & ~mask:
            continue
        value = 0
        bits = mask
        while bits:
            low = bits & -bits
            value += weights[low.bit_length() - 1]
            if best is not None and value >= best:
                break
            bits ^= low
        if bits == 0 and (best is None or value < best):
            best = value
            if best <= BUDGET_SCALED:
                return best
    require(best is not None, "physical parity row has no tetrahedral coloring")
    return best


def source_kernels():
    raw = SOURCE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, "rank-six fixture changed")
    payload = load_json(raw)
    records = tuple((index, tuple(record["code"]))
                    for index, record in enumerate(payload["kernels"], 1)
                    if record["n"] == ORDER)
    require(len(records) == 325, "order-eight rank-six kernel count changed")
    require(records[0][0] == 646 and records[-1][0] == 970, "kernel interval changed")
    require(all(len(kernel) == len(PAIRS) and sum(kernel) == PATH_COUNT
                for _, kernel in records), "kernel encoding changed")
    return records


def census_kernel(item):
    kernel_number, kernel = item
    group = automorphism_actions(kernel)
    orbit_sizes = {}
    for row in itertools.product(*(range(value + 1) for value in kernel)):
        representative = min(apply_action(row, action) for action in group)
        orbit_sizes[representative] = orbit_sizes.get(representative, 0) + 1
    residuals = []
    orbit_digest = hashlib.sha256()
    for row in sorted(orbit_sizes):
        orbit_digest.update(stream_line([kernel_number, list(row), orbit_sizes[row]]))
        cost = minimum_tetrahedral_cost_scaled(kernel, row)
        if cost > BUDGET_SCALED:
            residuals.append({
                "kernel": kernel_number,
                "row": list(row),
                "orbit_size": orbit_sizes[row],
                "minimum_tetrahedral_cost_scaled_30": cost,
            })
    ledger = {
        "kernel": kernel_number,
        "code": list(kernel),
        "physical_rows": sum(orbit_sizes.values()),
        "automorphisms": len(group),
        "orbits": len(orbit_sizes),
        "tetrahedral_certified": len(orbit_sizes) - len(residuals),
        "tetrahedral_residuals": len(residuals),
        "orbit_stream_sha256": orbit_digest.hexdigest(),
    }
    return ledger, residuals


def digest_payload(ledgers, residuals):
    kernel_digest = hashlib.sha256()
    orbit_manifest = hashlib.sha256()
    residual_digest = hashlib.sha256()
    frontier_digest = hashlib.sha256()
    for ledger in ledgers:
        kernel_digest.update(stream_line([ledger["kernel"], ledger["code"]]))
        orbit_manifest.update((ledger["orbit_stream_sha256"] + "\n").encode("ascii"))
    for source_index, residual in enumerate(residuals):
        residual_digest.update(stream_line(residual))
        for frontier in FRONTIERS:
            frontier_digest.update(stream_line(
                [source_index, residual["kernel"], residual["row"], frontier]))
    return {
        "kernel_stream_sha256": kernel_digest.hexdigest(),
        "orbit_manifest_sha256": orbit_manifest.hexdigest(),
        "residual_stream_sha256": residual_digest.hexdigest(),
        "frontier_key_stream_sha256": frontier_digest.hexdigest(),
    }


def regenerate(jobs=1, progress=False):
    sources = source_kernels()
    pool = None
    if jobs == 1:
        results = map(census_kernel, sources)
    else:
        pool = multiprocessing.Pool(jobs)
        results = pool.imap(census_kernel, sources, chunksize=1)
    ledgers, residuals = [], []
    try:
        for index, (ledger, local) in enumerate(results, 1):
            ledgers.append(ledger)
            residuals.extend(local)
            if progress:
                print(f"[{index}/325] K{ledger['kernel']} orbits={ledger['orbits']} "
                      f"residuals={len(local)}", flush=True)
    finally:
        if pool is not None:
            pool.close()
            pool.join()
    return {
        "schema": SCHEMA,
        "status": "census_complete_certificates_open",
        "full_theorem": False,
        "certificate_fixture_frozen": False,
        "rank": RANK,
        "order": ORDER,
        "budget": [RANK - 1, 1],
        "cost_scale": 30,
        "source_sha256": SOURCE_SHA256,
        "pair_order": [f"{u}{v}" for u, v in PAIRS],
        "kernel_interval": [646, 970],
        "kernel_total": len(ledgers),
        "path_count": PATH_COUNT,
        "physical_total": sum(row["physical_rows"] for row in ledgers),
        "orbit_total": sum(row["orbits"] for row in ledgers),
        "tetrahedral_certified_total": sum(row["tetrahedral_certified"] for row in ledgers),
        "tetrahedral_residual_total": len(residuals),
        "frontiers_per_residual": len(FRONTIERS),
        "frontier_target_total": len(residuals) * len(FRONTIERS),
        "frontier_policy": "canonical plus every one-coordinate length-plus-two target",
        "digests": digest_payload(ledgers, residuals),
        "kernels": ledgers,
        "residuals": residuals,
    }


def exact_int(value, label, minimum=None):
    require(type(value) is int and (minimum is None or value >= minimum), f"bad {label}")


def verify(payload):
    require(type(payload) is dict, "payload is not an object")
    require(payload["schema"] == SCHEMA, "schema changed")
    require(payload["status"] == "census_complete_certificates_open", "status changed")
    require(payload["full_theorem"] is False and payload["certificate_fixture_frozen"] is False,
            "open census was promoted")
    require((payload["rank"], payload["order"], payload["kernel_interval"],
             payload["kernel_total"], payload["path_count"], payload["budget"],
             payload["cost_scale"]) == (6, 8, [646, 970], 325, 13, [5, 1], 30),
            "scope changed")
    require(payload["source_sha256"] == SOURCE_SHA256, "source digest changed")
    require(payload["pair_order"] == [f"{u}{v}" for u, v in PAIRS], "pair order changed")
    require(payload["frontier_policy"] ==
            "canonical plus every one-coordinate length-plus-two target", "policy changed")
    exact_int(payload["physical_total"], "physical total", 0)
    exact_int(payload["orbit_total"], "orbit total", 0)
    exact_int(payload["tetrahedral_certified_total"], "certified total", 0)
    exact_int(payload["tetrahedral_residual_total"], "residual total", 0)
    require(payload["frontiers_per_residual"] == 14, "frontier width changed")
    require(payload["tetrahedral_certified_total"] + payload["tetrahedral_residual_total"]
            == payload["orbit_total"], "tetrahedral partition changed")
    require(payload["frontier_target_total"] == 14 * payload["tetrahedral_residual_total"],
            "frontier total changed")
    require((payload["physical_total"], payload["orbit_total"],
             payload["tetrahedral_certified_total"], payload["tetrahedral_residual_total"],
             payload["frontier_target_total"]) == EXPECTED_TOTALS, "exact totals changed")
    require(type(payload["kernels"]) is list and len(payload["kernels"]) == 325,
            "kernel ledger width changed")
    require(type(payload["residuals"]) is list and
            len(payload["residuals"]) == payload["tetrahedral_residual_total"],
            "residual ledger width changed")
    require(tuple((row["kernel"], tuple(row["code"])) for row in payload["kernels"])
            == source_kernels(), "kernel selection changed")
    require(sum(row["physical_rows"] for row in payload["kernels"])
            == payload["physical_total"], "physical ledger sum changed")
    require(sum(row["orbits"] for row in payload["kernels"])
            == payload["orbit_total"], "orbit ledger sum changed")
    require(sum(row["tetrahedral_certified"] for row in payload["kernels"])
            == payload["tetrahedral_certified_total"], "certified ledger sum changed")
    require(sum(row["tetrahedral_residuals"] for row in payload["kernels"])
            == payload["tetrahedral_residual_total"], "residual ledger sum changed")
    require(payload["digests"] == digest_payload(payload["kernels"], payload["residuals"]),
            "ordered census digest changed")
    require(payload["digests"] == EXPECTED_DIGESTS, "pinned census digest changed")
    previous = None
    kernels = {number: code for number, code in source_kernels()}
    for residual in payload["residuals"]:
        require(type(residual) is dict and set(residual) ==
                {"kernel", "row", "orbit_size", "minimum_tetrahedral_cost_scaled_30"},
                "residual envelope changed")
        key = residual["kernel"], tuple(residual["row"])
        require(previous is None or previous < key, "residual stream is not strictly ordered")
        previous = key
        require(residual["kernel"] in kernels and len(residual["row"]) == len(PAIRS),
                "bad residual key")
        require(all(type(value) is int and 0 <= value <= multiplicity
                    for value, multiplicity in zip(residual["row"], kernels[residual["kernel"]])),
                "nonphysical residual row")
        exact_int(residual["orbit_size"], "orbit size", 1)
        exact_int(residual["minimum_tetrahedral_cost_scaled_30"], "tetrahedral cost", 151)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    require(args.jobs >= 1, "jobs must be positive")
    if args.verify is None:
        payload = regenerate(args.jobs, args.progress)
        verify(payload)
        require(args.output.parent.is_dir(), "output parent is missing")
        raw = canonical_bytes(payload)
        temporary = args.output.with_name(args.output.name + ".tmp")
        temporary.write_bytes(raw)
        temporary.replace(args.output)
    else:
        raw = args.verify.read_bytes()
        payload = load_json(raw)
        require(raw == canonical_bytes(payload), "census JSON is not canonical")
        verify(payload)
    print(f"kernels={payload['kernel_total']} physical={payload['physical_total']} "
          f"orbits={payload['orbit_total']}")
    print(f"tetrahedral_certified={payload['tetrahedral_certified_total']} "
          f"residuals={payload['tetrahedral_residual_total']} "
          f"frontier_targets={payload['frontier_target_total']}")
    print(f"json_sha256={hashlib.sha256(raw).hexdigest()}")
    for name, digest in sorted(payload["digests"].items()):
        print(f"{name}={digest}")
    print("census_complete=true full_theorem=false")


if __name__ == "__main__":
    try:
        main()
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as error:
        raise RuntimeError(f"fail-closed malformed input: {error}") from error
