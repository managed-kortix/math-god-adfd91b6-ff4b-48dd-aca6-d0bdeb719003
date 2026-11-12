#!/usr/bin/env python3
"""Exact verifier for the 80 order-nine favorable-cycle residual Grams.

The certificate fixture is trust-complete: this verifier uses only the Python
standard library and exact :class:`fractions.Fraction` arithmetic.  Numerical
SDP output was used only to propose matrices and is neither loaded nor trusted.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RESIDUAL = HERE / "rank-seven-order-nine-favorable-cycle-residual.json"
CERTIFICATES = HERE / "rank-seven-order-nine-favorable-cycle-residual-direct-grams.json"
KERNELS = HERE / "fixtures/rank-seven-kernel-frontier-census.json"
EXPECTED = {
    "residual": "8a5073c977f7f7b3ca457dee056301e8bdc83e6e0b9974bf171d39b20cdaaac2",
    "kernels": "a241139ab54ce4cce1ab3812887359edb241c0abfb1018e804b4a5f86762cfd5",
    "certificate": "011aa5da23af851525ce3d6c0df13f3697b1464025c96748d0a9d111a45e7697",
}
ORDER = 9
PATH_COUNT = 15
BUDGET = Fraction(6)
F = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def strict_json(path: Path, expected_sha256: str):
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == expected_sha256,
            f"{path.name} bytes changed")

    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, f"duplicate key in {path.name}: {key}")
            result[key] = value
        return result

    try:
        value = json.loads(
            raw.decode("ascii"), object_pairs_hook=pairs,
            parse_constant=lambda item: (_ for _ in ()).throw(
                RuntimeError(f"nonstandard JSON constant in {path.name}: {item}")),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"cannot parse {path.name}") from error
    require(raw == canonical_bytes(value), f"noncanonical JSON: {path.name}")
    return value


def rational(raw, label: str) -> F:
    require(isinstance(raw, list) and len(raw) == 2 and
            all(type(value) is int for value in raw),
            f"malformed rational pair: {label}")
    numerator, denominator = raw
    require(denominator > 0, f"nonpositive rational denominator: {label}")
    value = F(numerator, denominator)
    require([value.numerator, value.denominator] == raw,
            f"noncanonical rational pair: {label}")
    return value


def load_kernels():
    fixture = strict_json(KERNELS, EXPECTED["kernels"])
    kernels = {}
    local = 0
    for global_index, record in enumerate(fixture["kernels"], 1):
        if record["n"] != ORDER:
            continue
        local += 1
        edges = tuple(
            (u, v, multiplicity)
            for (u, v), multiplicity in zip(
                itertools.combinations(range(ORDER), 2), record["code"], strict=True
            )
            if multiplicity
        )
        kernels[local] = (global_index, edges)
    require(len(kernels) == 4495, "order-nine kernel count changed")
    return kernels


def canonical_paths(edges, row):
    paths = []
    for support, ((u, v, multiplicity), odd_total) in enumerate(
            zip(edges, row, strict=True)):
        lengths = (([1] + [3] * (odd_total - 1)) if odd_total else [])
        lengths += [2] * (multiplicity - odd_total)
        paths.extend((support, occurrence, u, v, length)
                     for occurrence, length in enumerate(lengths))
    require(len(paths) == PATH_COUNT, "physical path count changed")
    return tuple(paths)


def exact_ldl(matrix):
    """Return exact unit-lower L and diagonal D, failing on a bad zero pivot."""
    size = len(matrix)
    lower = [[F(i == j) for j in range(size)] for i in range(size)]
    diagonal = []
    for column in range(size):
        pivot = matrix[column][column] - sum(
            lower[column][k] * lower[column][k] * diagonal[k]
            for k in range(column)
        )
        diagonal.append(pivot)
        if pivot:
            for row in range(column + 1, size):
                lower[row][column] = (
                    matrix[row][column] - sum(
                        lower[row][k] * lower[column][k] * diagonal[k]
                        for k in range(column)
                    )
                ) / pivot
        else:
            require(all(
                matrix[row][column] == sum(
                    lower[row][k] * lower[column][k] * diagonal[k]
                    for k in range(column)
                ) for row in range(column + 1, size)
            ), "nonzero Schur entry below a zero LDL pivot")
    return lower, diagonal


def verify():
    residual = strict_json(RESIDUAL, EXPECTED["residual"])
    fixture = strict_json(CERTIFICATES, EXPECTED["certificate"])
    kernels = load_kernels()
    failures = residual["failures"]
    certificates = fixture["certificates"]

    require(residual["residual_targets"] == 80 and len(failures) == 80,
            "residual population changed")
    require(fixture["schema"] ==
            "rank-seven-order-nine-favorable-cycle-residual-direct-gram-v1" and
            fixture["full_theorem"] is False and
            fixture["certificate_total"] == 80 and len(certificates) == 80,
            "certificate fixture header changed")
    require(fixture["source_residual"] == {
                "path": RESIDUAL.name,
                "record_total": 80,
                "sha256": EXPECTED["residual"],
            }, "certificate source identity changed")
    require(fixture["proposal_provenance"]["trusted"] is False and
            "exact verifier" in fixture["proposal_provenance"]["role"] and
            "Fraction" in fixture["proposal_provenance"]["acceptance"],
            "proposal/trust boundary changed")

    minimum_pivot = None
    maximum_cost = F()
    seen = set()
    for index, (failure, certificate) in enumerate(
            zip(failures, certificates, strict=True)):
        key = canonical_bytes(certificate["key"])
        require(certificate["key"] == failure["key"] and key not in seen,
                f"certificate key mismatch or duplicate at {index}")
        seen.add(key)

        local_kernel = failure["order9_kernel"]
        expected_global, edges = kernels[local_kernel]
        require(expected_global == failure["global_kernel"],
                f"kernel reference changed at {index}")
        paths = canonical_paths(edges, failure["row"])
        target_lengths = failure["target_length_vector"]
        require(isinstance(target_lengths, list) and len(target_lengths) == PATH_COUNT and
                all(type(length) is int and length > 0 for length in target_lengths),
                f"bad target length vector at {index}")
        require(all((target - base) % 2 == 0 and target >= base
                    for target, (*_, base) in zip(target_lengths, paths, strict=True)),
                f"target is not a same-parity descendant at {index}")
        frontier = failure["frontier_path_index"]
        require(type(frontier) is int and 0 <= frontier < PATH_COUNT and
                target_lengths[frontier] == paths[frontier][4] + 2 and
                sum(target != path[4]
                    for target, path in zip(target_lengths, paths, strict=True)) == 1,
                f"target vector is not the recorded single-coordinate frontier at {index}")
        require(failure["physical_occurrence_key"] == list(paths[frontier][:2]),
                f"physical occurrence identity changed at {index}")

        raw_matrix = certificate["matrix"]
        require(isinstance(raw_matrix, list) and len(raw_matrix) == ORDER and
                all(isinstance(row, list) and len(row) == ORDER
                    for row in raw_matrix), f"bad matrix shape at {index}")
        matrix = tuple(tuple(rational(value, f"matrix[{index}][{u}][{v}]")
                             for v, value in enumerate(row))
                       for u, row in enumerate(raw_matrix))
        require(all(matrix[u][v] == matrix[v][u]
                    for u in range(ORDER) for v in range(ORDER)),
                f"nonsymmetric matrix at {index}")
        require(all(matrix[u][u] == 1 for u in range(ORDER)),
                f"non-unit diagonal at {index}")
        lower, pivots = exact_ldl(matrix)
        require(all(pivot > 0 for pivot in pivots),
                f"matrix is not positive definite at {index}")
        # Reconstruct every entry.  This turns LDL into an explicit exact Gram
        # decomposition: G = sum_i d_i L[:,i] L[:,i]^T, with d_i > 0.
        require(all(matrix[u][v] == sum(
                    pivots[k] * lower[u][k] * lower[v][k]
                    for k in range(ORDER))
                    for u in range(ORDER) for v in range(ORDER)),
                f"LDL reconstruction failed at {index}")
        local_minimum = min(pivots)
        minimum_pivot = (local_minimum if minimum_pivot is None else
                         min(minimum_pivot, local_minimum))

        cost = F()
        for path, length in zip(paths, target_lengths, strict=True):
            _, _, u, v, _ = path
            transformed = (-1 if length & 1 else 1) * matrix[u][v]
            require(-1 <= transformed <= 1,
                    f"correlation escaped [-1,1] at {index}")
            require(transformed != -1,
                    f"infinite path summand at {index}")
            cost += (1 - transformed) / (length * (1 + transformed))
        stored_cost = rational(certificate["cost"], f"cost[{index}]")
        require(cost == stored_cost and cost <= BUDGET,
                f"exact cost mismatch or budget failure at {index}")
        maximum_cost = max(maximum_cost, cost)

    require(len(seen) == 80 and minimum_pivot is not None,
            "certificate accounting failed")
    return {
        "certificate_total": len(seen),
        "maximum_exact_cost": [maximum_cost.numerator, maximum_cost.denominator],
        "minimum_positive_ldl_pivot": [minimum_pivot.numerator,
                                        minimum_pivot.denominator],
        "descendant_lift": (
            "for any coordinatewise same-parity length increase, every "
            "transformed correlation is unchanged and each nonnegative path "
            "summand weakly decreases"
        ),
        "full_theorem": False,
    }


def main() -> None:
    result = verify()
    print(canonical_bytes(result).decode("ascii"), end="")


if __name__ == "__main__":
    main()
