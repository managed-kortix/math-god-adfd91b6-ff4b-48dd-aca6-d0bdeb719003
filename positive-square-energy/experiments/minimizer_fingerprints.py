#!/usr/bin/env python3
"""Reproduce basic structural fingerprints of the n=10 slice minimizers."""

from __future__ import annotations

import itertools

import networkx as nx
import numpy as np

from search_geng import graph6_adjacency


MINIMIZERS = {
    11: "I?`D@POd?", 12: "I?`DA_wIO", 13: "I?`DA`gJO",
    14: "I?`acgwg_", 15: "ICOf@pSb?", 16: "I?`DF`YN?",
    17: "I?`FBqsF_", 18: "I?q`qjo{?", 19: "I?bF`xw{?",
    20: "I?rFf_{N?",
}


def induced_claw_at(g: nx.Graph, v: int) -> bool:
    return any(all(not g.has_edge(a, b) for a, b in itertools.combinations(ns, 2))
               for ns in itertools.combinations(g.neighbors(v), 3))


for m, g6 in MINIMIZERS.items():
    a = graph6_adjacency(g6.encode()).astype(int)
    g = nx.from_numpy_array(a)
    eig = np.linalg.eigvalsh(a)
    inertia = (int(sum(eig > 1e-8)), int(sum(abs(eig) <= 1e-8)),
               int(sum(eig < -1e-8)))
    print(m, g6, "degrees", sorted(dict(g.degree()).values(), reverse=True),
          "diameter", nx.diameter(g), "girth", nx.girth(g),
          "bridges", len(list(nx.bridges(g))),
          "blocks", sorted(map(len, nx.biconnected_components(g)), reverse=True),
          "inertia", inertia, "triangles", sum(nx.triangles(g).values()) // 3,
          "claw_free", not any(induced_claw_at(g, v) for v in g))
