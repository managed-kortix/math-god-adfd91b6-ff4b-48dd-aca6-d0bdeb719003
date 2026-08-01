#!/usr/bin/env python3
import json
from pathlib import Path


def main():
    path = Path(__file__).with_name("cycle218_frozen_chow_secant.json")
    data = json.loads(path.read_text())

    coefficients = data["coefficients"]
    graph_degrees = data["graph_degrees"]
    positive_degree = sum(max(c, 0) * d for c, d in zip(coefficients, graph_degrees))
    negative_degree = sum(max(-c, 0) * d for c, d in zip(coefficients, graph_degrees))

    assert positive_degree == data["d_plus"]
    assert negative_degree == data["d_minus"]
    assert positive_degree + negative_degree == data["common_degree"]
    assert data["incidence"] == {
        "auxiliary_degree_e": 0,
        "chain_length_n": 1,
        "map_degrees_h": [1],
        "map": "[s:t] -> [s*a(Y)+t*b(Y)]",
    }
    n = data["pel_tangent_dimension"]
    assert n * (n + 1) // 2 == data["second_order_pairs"]
    assert data["status"] == "frozen_candidate_not_certificate"

    print("PASS Cycle 218 frozen Chow-secant candidate data")


if __name__ == "__main__":
    main()
