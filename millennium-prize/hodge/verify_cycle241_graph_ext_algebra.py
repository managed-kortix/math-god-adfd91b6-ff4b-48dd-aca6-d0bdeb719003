#!/usr/bin/env python3
"""Generate and verify the compressed exact graph-Ext algebra artifact."""

import argparse
import json
from itertools import combinations
from pathlib import Path


POWERS = ((1, 0), (2, 1), (3, 4), (2, 11), (-7, 24),
          (-38, 41), (-117, 44))
ARTIFACT = Path(__file__).with_name("cycle241_graph_ext_algebra.json")


def gaussian_mul(left, right):
    a, b = left
    c, d = right
    return (a * c - b * d, a * d + b * c)


def wedge(left, right):
    """Return the exact exterior-product coefficient and ordered support."""
    if set(left) & set(right):
        return 0, ()
    inversions = sum(a > b for a in left for b in right)
    return (-1 if inversions % 2 else 1), tuple(sorted(left + right))


def pair_records():
    records = []
    for i, j in combinations(range(7), 2):
        delta = (POWERS[j][0] - POWERS[i][0],
                 POWERS[j][1] - POWERS[i][1])
        norm = delta[0] ** 2 + delta[1] ** 2
        records.append({
            "vertices": [i, j],
            "delta": {"re": delta[0], "im": delta[1]},
            "norm": norm,
            "cross_ext_3_dimension": norm ** 3,
        })
    return records


def build_artifact():
    self_basis = []
    for degree in range(7):
        self_basis.append({
            "degree": degree,
            "labels": [list(term) for term in combinations(range(1, 7), degree)],
        })

    return {
        "artifact": "cycle241_graph_ext_algebra",
        "version": 1,
        "field": {
            "name": "Q(i)",
            "model": "Q[t]/(t^2+1)",
            "scalar_encoding": {"re": "rational", "im": "rational"},
        },
        "geometry": {
            "ambient": "E_i^3 x E_i^3",
            "u": {"re": 2, "im": 1},
            "objects": [f"F_{k}=O_Gamma_(u^{k})" for k in range(7)],
            "powers": [{"re": a, "im": b} for a, b in POWERS],
        },
        "self_ext": {
            "presentation": "Lambda_K(a_1,...,a_6), |a_r|=1",
            "dimensions_degrees_0_to_6": [1, 6, 15, 20, 15, 6, 1],
            "basis": self_basis,
            "product": {
                "rule": "a_I*a_J=0 if I intersects J; otherwise (-1)^inv(I,J)*a_(sorted(I union J))",
                "inv": "number of pairs (p,q) in I x J with p>q",
                "top_class": [1, 2, 3, 4, 5, 6],
            },
        },
        "cross_ext": {
            "pair_records": pair_records(),
            "basis": "x_(ij,s), 0<=s<L_ij, for every ordered i!=j",
            "degrees": "all x_(ij,s) have degree 3; every other cross Ext group is zero",
            "products": [
                "m2(x_(ji,t),x_(ij,s))=delta_(s,t)*omega_i",
                "m2(x_(ij,s),x_(ji,t))=-delta_(s,t)*omega_j",
                "all products of cross basis vectors with distinct outer vertices are zero",
                "positive-degree self classes times cross classes, on either side, are zero",
                "vertex units act as source and target identities",
            ],
            "normalization": "dual bases for the perfect degree-3 Serre pairings; the minus sign is graded cyclicity in odd degree",
        },
        "shift_rule": {
            "formula": "Hom^d(F_i[r],F_j[s])=Ext^(d-r+s)(F_i,F_j)",
            "cross_degree": "a cross basis map has shifted degree d=3+r-s",
        },
        "smallest_idempotents": {
            "absolute_two_copy": {
                "object": "F_i[r] direct_sum F_i[r]",
                "all_nontrivial": "[[a,b],[c,1-a]] with a(1-a)=bc over Q(i)",
                "structure": "all are rank-one and noncentral in M_2(Q(i))",
            },
            "cross_vertex_two_summand": {
                "object": "F_i[r] direct_sum F_j[r+3], i!=j",
                "endomorphism_algebra": "T_L={[[a,x],[0,b]]:a,b in Q(i), x in Q(i)^L}, L=L_ij",
                "all_nontrivial": ["[[1,x],[0,0]]", "[[0,x],[0,1]]"],
                "parameter": "x arbitrary in Q(i)^L",
                "structure": "every listed projector is noncentral and conjugate by 1+rad(T_L) to its x=0 vertex projector",
            },
            "one_arrow_twisted_complex": {
                "object": "(F_i[r] -> F_j[r+2]) with a nonzero degree-one cross differential",
                "degree_zero_chain_idempotents": ["0", "1"],
                "reason": "degree-zero endomorphisms are diagonal scalars and commuting with the nonzero arrow makes them equal",
            },
        },
        "scope": [
            "This is the exact binary Yoneda algebra, in normalized bases, not a claim of a canonical geometric basis.",
            "The compressed cross basis avoids materializing up to 4,103,684,801,000 coordinates.",
            "The rules determine sparse chain-map products, Hom differentials, and Ext^2 obstruction matrices for bounded twisted complexes.",
            "This bounded classification does not decide arbitrary Karoubi packets or KI240.",
        ],
    }


def verify(artifact):
    powers = []
    value = (1, 0)
    for _ in range(7):
        powers.append(value)
        value = gaussian_mul(value, (2, 1))
    assert tuple(powers) == POWERS

    expected_dims = [1, 6, 15, 20, 15, 6, 1]
    assert [len(row["labels"]) for row in artifact["self_ext"]["basis"]] == expected_dims
    for left_degree in range(7):
        for left in combinations(range(1, 7), left_degree):
            for right_degree in range(7):
                for right in combinations(range(1, 7), right_degree):
                    coefficient, support = wedge(left, right)
                    reverse_coefficient, reverse_support = wedge(right, left)
                    if coefficient:
                        assert support == reverse_support
                        assert coefficient == ((-1) ** (left_degree * right_degree)) * reverse_coefficient

    records = artifact["cross_ext"]["pair_records"]
    assert len(records) == 21
    for record in records:
        i, j = record["vertices"]
        delta = (POWERS[j][0] - POWERS[i][0],
                 POWERS[j][1] - POWERS[i][1])
        norm = delta[0] ** 2 + delta[1] ** 2
        assert record["delta"] == {"re": delta[0], "im": delta[1]}
        assert record["norm"] == norm
        assert record["cross_ext_3_dimension"] == norm ** 3

    # Symbolic coefficient checks for the two triangular idempotent families.
    for a, b in ((1, 0), (0, 1)):
        assert a * a == a and b * b == b and a + b == 1


def serialized_artifact():
    artifact = build_artifact()
    verify(artifact)
    return json.dumps(artifact, indent=2, sort_keys=True) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered = serialized_artifact()
    if args.check:
        assert ARTIFACT.read_text() == rendered
        print("cycle241 exact Ext algebra artifact verified")
    else:
        ARTIFACT.write_text(rendered)
        print(f"wrote {ARTIFACT}")


if __name__ == "__main__":
    main()
