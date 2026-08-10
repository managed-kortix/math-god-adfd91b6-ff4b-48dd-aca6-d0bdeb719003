#!/usr/bin/env python3
"""Exact certificate sieve for the 444 proper odd-support rank candidates."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import random
from collections import Counter
from fractions import Fraction
from pathlib import Path

import networkx as nx
import sympy as sp


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "rank6_orders9_10_proper_odd_support_census.json"
SOURCE_SHA256 = "fe0078654df18ecf31efa688e021ed8cf9c3ddc455978d302584b9354e31232d"
OUTPUT = HERE / "rank6_orders9_10_extremality_feasibility.json"
SCHEMA = "rank6-orders9-10-extremality-feasibility-v1"
SEED = 44420260809
TRIALS = 64
RANK_PRIMES = (2_147_483_647, 2_147_483_629, 2_147_483_587)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def source_payload():
    raw = SOURCE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, "support census changed")
    return json.loads(raw.decode("ascii"))


def primitive(vector):
    values = [Fraction(int(value.p), int(value.q)) if isinstance(value, sp.Rational)
              else Fraction(value) for value in vector]
    denominator = math.lcm(*(value.denominator for value in values))
    integers = [value.numerator * (denominator // value.denominator)
                for value in values]
    divisor = math.gcd(*integers)
    if divisor:
        integers = [value // divisor for value in integers]
    first = next((value for value in integers if value), 0)
    if first < 0:
        integers = [-value for value in integers]
    return tuple(integers)


def constraint_row(left, right):
    rank = len(left)
    return tuple(
        left[i] * right[j] + (left[j] * right[i] if i != j else 0)
        for i in range(rank) for j in range(i, rank)
    )


def rank_modulo(rows, columns, prime):
    """Compute matrix rank over a prime field using compact Python integers."""
    matrix = [[value % prime for value in row] for row in rows]
    rank = 0
    for column in range(columns):
        pivot = next((index for index in range(rank, len(matrix))
                      if matrix[index][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_row = matrix[rank]
        inverse = pow(pivot_row[column], prime - 2, prime)
        pivot_row[column:] = [(value * inverse) % prime
                              for value in pivot_row[column:]]
        for index in range(rank + 1, len(matrix)):
            row = matrix[index]
            factor = row[column]
            if factor:
                row[column:] = [(left - factor * right) % prime
                                for left, right in zip(row[column:],
                                                       pivot_row[column:])]
        rank += 1
        if rank == min(len(matrix), columns):
            break
    return rank


def certified_rank(rows, columns, target):
    """Prove the requested rational rank via a nonzero modular minor."""
    if len(rows) < target or columns < target:
        return False
    return any(rank_modulo(rows, columns, prime) >= target
               for prime in RANK_PRIMES)


def exact_witness(graph, rank, rng):
    """Seek a rational point by exact sequential orthogonal construction."""
    complement = nx.complement(graph)
    order = list(graph)
    rng.shuffle(order)
    vectors = {}
    for vertex in order:
        earlier = [vectors[neighbor] for neighbor in complement[vertex]
                   if neighbor in vectors]
        matrix = sp.Matrix(earlier) if earlier else sp.zeros(0, rank)
        nullspace = matrix.nullspace()
        if not nullspace:
            return None
        coefficients = [rng.choice((-5, -4, -3, -2, -1, 1, 2, 3, 4, 5))
                        for _ in nullspace]
        vector = sp.zeros(rank, 1)
        for coefficient, basis_vector in zip(coefficients, nullspace):
            vector += coefficient * basis_vector
        vectors[vertex] = primitive(vector)

    rows = [vectors[vertex] for vertex in sorted(graph)]
    if not certified_rank(rows, rank, rank):
        return None
    constraints = [constraint_row(rows[left], rows[right])
                   for left, right in nx.non_edges(graph)]
    target = math.comb(rank + 1, 2) - 1
    # Every constraint annihilates the identity because its endpoint vectors
    # are orthogonal. Thus target is an a priori upper bound; a modular minor
    # of that order proves equality over Q without costly rational elimination.
    if not certified_rank(constraints, math.comb(rank + 1, 2), target):
        return None
    return rows


def independence_certificate(graph):
    complement = nx.complement(graph)
    clique = max(nx.find_cliques(complement), key=len)
    return sorted(clique)


def derive():
    source = source_payload()
    rng = random.Random(SEED)
    records = []
    for support in source["supports"]:
        graph = nx.from_graph6_bytes(support["graph6"].encode("ascii"))
        independent_set = independence_certificate(graph)
        for rank in support["extreme_dnn_rank_candidates"]:
            base = {"support_id": support["id"], "rank": rank}
            if len(independent_set) > rank:
                record = {
                    **base,
                    "status": "infeasible",
                    "certificate": {
                        "kind": "independent-set-orthogonality",
                        "vertices": independent_set[:rank + 1],
                    },
                }
            else:
                witness = None
                for _ in range(TRIALS):
                    witness = exact_witness(graph, rank, rng)
                    if witness is not None:
                        break
                if witness is None:
                    record = {
                        **base,
                        "status": "unresolved",
                        "certificate": {
                            "kind": "bounded-exact-search",
                            "trials": TRIALS,
                        },
                    }
                else:
                    record = {
                        **base,
                        "status": "feasible",
                        "certificate": {
                            "kind": "integer-orthogonal-representation",
                            "vectors": [list(vector) for vector in witness],
                        },
                    }
            records.append(record)

    counts = Counter(record["status"] for record in records)
    by_rank = {}
    for rank in range(3, 8):
        rank_counts = Counter(record["status"] for record in records
                              if record["rank"] == rank)
        if rank_counts:
            by_rank[str(rank)] = {key: rank_counts[key]
                                  for key in ("feasible", "infeasible", "unresolved")}
    surviving = {
        record["support_id"] for record in records if record["status"] != "infeasible"
    }
    return {
        "schema": SCHEMA,
        "source_sha256": SOURCE_SHA256,
        "semantics": {
            "feasible": "displayed spanning rational vectors annihilate every nonedge tensor and give tensor rank binom(r+1,2)-1",
            "infeasible": "displayed independent set has r+1 vertices, forcing r+1 nonzero mutually orthogonal vectors in Q^r or R^r",
            "unresolved": "neither conclusion; bounded exact witness search is not an infeasibility certificate",
            "scope_excludes": "edge positivity and path-derivative KKT compatibility",
        },
        "search": {"seed": SEED, "trials_per_nonexcluded_pair": TRIALS},
        "counts": {
            "candidate_pairs": len(records),
            "feasible": counts["feasible"],
            "infeasible": counts["infeasible"],
            "unresolved": counts["unresolved"],
            "supports_not_eliminated": len(surviving),
            "by_rank": by_rank,
        },
        "records": records,
    }


def verify(payload, expected):
    require(payload == expected, "stored extremality feasibility artifact changed")
    source = source_payload()
    supports = {row["id"]: row for row in source["supports"]}
    expected_pairs = {(row["id"], rank) for row in source["supports"]
                      for rank in row["extreme_dnn_rank_candidates"]}
    actual_pairs = {(row["support_id"], row["rank"]) for row in payload["records"]}
    require(actual_pairs == expected_pairs and len(actual_pairs) == len(payload["records"]),
            "candidate-pair coverage changed")
    for record in payload["records"]:
        support = supports[record["support_id"]]
        graph = nx.from_graph6_bytes(support["graph6"].encode("ascii"))
        rank = record["rank"]
        certificate = record["certificate"]
        if record["status"] == "infeasible":
            vertices = certificate["vertices"]
            require(len(vertices) == rank + 1 and
                    all(not graph.has_edge(left, right)
                        for left, right in itertools.combinations(vertices, 2)),
                    "bad independent-set certificate")
        elif record["status"] == "feasible":
            vectors = certificate["vectors"]
            require(len(vectors) == len(graph) and
                    all(len(vector) == rank and any(vector) for vector in vectors),
                    "bad witness dimensions")
            require(certified_rank(vectors, rank, rank), "witness does not span")
            constraints = [constraint_row(vectors[left], vectors[right])
                           for left, right in nx.non_edges(graph)]
            require(all(sum(vectors[left][index] * vectors[right][index]
                            for index in range(rank)) == 0
                        for left, right in nx.non_edges(graph)),
                    "witness violates a nonedge equation")
            require(certified_rank(constraints, math.comb(rank + 1, 2),
                                   math.comb(rank + 1, 2) - 1),
                    "nonedge tensors have wrong rank")
        else:
            require(record["status"] == "unresolved" and
                    certificate == {"kind": "bounded-exact-search", "trials": TRIALS},
                    "bad unresolved record")


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    payload = derive()
    if args.verify:
        verify(json.loads(args.verify.read_text(encoding="ascii")), payload)
        print("rank-six orders 9-10 extremality feasibility: exact audit passed")
        print(json.dumps(payload["counts"], sort_keys=True))
    elif args.write:
        OUTPUT.write_bytes(canonical_bytes(payload))
        print(OUTPUT)
        print(json.dumps(payload["counts"], sort_keys=True))
    else:
        print(canonical_bytes(payload).decode("ascii"), end="")


if __name__ == "__main__":
    main()
