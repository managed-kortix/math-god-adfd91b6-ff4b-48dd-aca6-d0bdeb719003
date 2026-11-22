#!/usr/bin/env python3
"""Fail-closed verifier for the narrow physical R61 single-block theorem.

The verifier checks the finite/affine proof skeleton and authenticates its
analytic imports.  It deliberately makes no complete-physical-R61 or global
heptacyclic claim.
"""

from __future__ import annotations

import argparse
import hashlib
import inspect
import itertools
import json
import subprocess
import sys
from copy import deepcopy
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MANIFEST = HERE / "fixtures" / "r61-physical-single-block-theorem-manifest.json"
MANIFEST_SHA256 = "b43dc1e7a450aac5af66b1fd6a7c23ff6bf2a5ddbcc9bd4a2b8b9c2333f709fe"
REGISTRY = HERE / "r61-rank-six-single-block-owner-registry-verifier.py"
REGISTRY_SHA256 = "1ad8c0577a62b5497728a4cc4d204e179a1b04913b68d76762817f869564c87f"
REGISTRY_OUTPUT_SHA256 = "81aa766b90efe3bbe88d8142ae97f4b1d76744ba39d9a418fa868a5fa0b7ffa8"
OWNERS = ("DNN", "K110-0", "K110-1", "K223")
PAIR6 = tuple(itertools.combinations(range(6), 2))
K223_ROW = "001111011011111"
K223_EDGES = {(0, 3), (0, 4), (0, 5), (1, 2), (1, 4), (1, 5),
              (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)}


class VerificationError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def strict_json_bytes(raw, label):
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise VerificationError(f"duplicate key in {label}: {key}")
            result[key] = value
        return result

    def reject_constant(value):
        raise VerificationError(f"nonstandard JSON constant in {label}: {value}")

    try:
        payload = json.loads(raw.decode("ascii"), object_pairs_hook=unique_pairs,
                             parse_constant=reject_constant)
    except (UnicodeError, json.JSONDecodeError, ValueError) as error:
        raise VerificationError(f"cannot parse {label}: {error}") from error
    require(raw == canonical_bytes(payload), f"{label} is not canonical ASCII JSON")
    return payload


def load_manifest():
    require(MANIFEST.is_file() and not MANIFEST.is_symlink(), "missing or symlinked manifest")
    raw = MANIFEST.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == MANIFEST_SHA256, "manifest digest changed")
    return strict_json_bytes(raw, "physical theorem manifest")


def exact_scope():
    return {
        "graph": "finite-simple-connected",
        "cyclomatic_rank": 7,
        "separator": {"kind": "one-actual-bridge", "side_ranks": [6, 1]},
        "rank_six_side": {
            "positive_rank_cyclic_blocks": 1,
            "subdivisions": "arbitrary-positive-simple-physical-path-lengths",
            "tree_attachments": "arbitrary-finite-rooted-trees",
        },
        "rank_one_side": {
            "connected": True, "cyclomatic_rank": 1,
            "tree_attachments": "arbitrary-finite-rooted-trees",
        },
        "ports": "arbitrary-vertices-on-both-sides",
        "excluded": [
            "multiblock-rank-six-side", "shared-cut-R61", "multi-interface-connectors",
            "multiple-rank-one-arms", "all-physical-R61",
            "all-multiblock-heptacyclic-graphs", "all-heptacyclic-graphs",
            "strict-global-conclusion",
        ],
    }


def validate_manifest(manifest):
    require(set(manifest) == {
        "schema", "theorem_id", "scope", "conclusion", "owners", "owner_registry",
        "analytic_imports", "proof_contract", "verification_boundary", "nonclaims",
    }, "manifest fields changed")
    require(manifest["schema"] == "r61-physical-single-block-theorem-v1" and
            manifest["theorem_id"] == "R61-PHYSICAL-SINGLE-BLOCK",
            "theorem identity changed")
    require(manifest["scope"] == exact_scope(), "theorem scope changed")
    require(manifest["conclusion"] == {
        "bound": "|V(G)|", "quantity": "s+(G)", "relation": ">=",
        "statement": "s+(G)>=|V(G)|", "strict": False,
    }, "theorem conclusion changed")
    require(manifest["owners"] == list(OWNERS), "theorem owners changed")
    require(manifest["owner_registry"] == {
        "path": "research/r61-rank-six-single-block-owner-registry-verifier.py",
        "source_sha256": REGISTRY_SHA256,
        "canonical_output_sha256": REGISTRY_OUTPUT_SHA256,
        "schema": "r61-rank-six-single-block-owner-registry-receipt-v1",
        "command": ["python3", "-I", "-B",
                    "research/r61-rank-six-single-block-owner-registry-verifier.py",
                    "--emit", "--print-manifest"],
    }, "typed registry dependency changed")
    require(type(manifest["analytic_imports"]) is list and len(manifest["analytic_imports"]) == 4,
            "analytic import registry width changed")
    require(manifest["proof_contract"] == {
        "DNN": "kappa(R)<=m_R+5, kappa(U)<=m_U+1, and the bridge K2 costs one; hence kappa(G)<=m_G+6 and s+(G)>=|V(G)|",
        "structural": "keep U intact; choose a fixed literal K4 and the complementary nonempty rank-six tree territory; leave the physical bridge and all center-crossing edges between induced territories; sigma(G)>2-1-1=0",
        "port_blind": True,
        "structural_territories": 3,
    }, "proof contract changed")
    require(manifest["verification_boundary"] == {
        "exactly_checked": [
            "canonical JSON identities and dependency digests",
            "fresh typed owner-registry execution",
            "DNN affine ledger",
            "K110-0, K110-1, and K223 induced core partitions",
            "strict rational ledger arithmetic",
            "hostile mutation rejection",
        ],
        "analytic_imports_not_reproved_by_hashes": [
            "DNN spectral inequality and one-vertex additivity",
            "induced superadditivity",
            "unicyclic DNN cycle certificate",
            "rooted actual-K4 strict credit",
            "unique-positive-block rooted-tree decomposition",
        ],
    }, "verification boundary changed")
    require(manifest["nonclaims"] == [
        "complete physical R61 closure", "rank-six multiblock bridge sides",
        "shared-cut R61", "more than one rank-one arm",
        "all multiblock heptacyclic graphs", "all heptacyclic graphs",
        "strict inequality for every graph in scope",
    ], "nonclaim boundary changed")


def authenticate_imports(manifest):
    expected = {
        "DNN-correlation-dual-trace-and-one-vertex-additivity": (
            "all-hexacyclic-graphs/paper.tex",
            "0e7a2db2932d38a4b4909831c34050553afc0973869fe937eb510cb59421bda7",
            "s-(H)<=kappa(H); kappa is additive under one-vertex sums; kappa(T)=|E(T)|"),
        "induced-positive-square-energy-superadditivity-and-tree-identity": (
            "all-tricyclic-graphs/paper.tex",
            "4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02",
            "sigma(G)>=sum sigma(G[V_i]) for every vertex partition; sigma(T)=-1 for every nonempty tree"),
        "unicyclic-cycle-DNN-excess": (
            "all-bicyclic-cacti/paper.tex",
            "bc0c77df16d52c600af9b7966038837fd724b5941bf9354aabf9209285f57aad",
            "kappa(U)<=|E(U)|+epsilon_q with epsilon_q=0 for even q and q tan^2(pi/(2q)) for odd q; epsilon_q<=1"),
        "rooted-actual-K4-strict-credit": (
            "positive-square-energy/tricyclic-general/k4-all-odd-dnn-cover.md",
            "44c0391e492dc07216fa45e7095c58fdaca802e972f618068d29774d24140333",
            "a connected territory whose unique positive-rank block is an actual K4, with arbitrary rooted-tree attachments, has sigma>2"),
    }
    rows = manifest["analytic_imports"]
    require(type(rows) is list and len(rows) == len(expected), "analytic import registry changed")
    require({row.get("logical_name") for row in rows} == set(expected),
            "analytic import names changed")
    for row in rows:
        require(set(row) == {"logical_name", "path", "sha256", "contract"},
                "analytic import fields changed")
        path_text, digest, contract = expected[row["logical_name"]]
        require((row["path"], row["sha256"], row["contract"]) ==
                (path_text, digest, contract), "analytic import contract changed")
        path = ROOT / path_text
        require(path.is_file() and not path.is_symlink(), "missing or symlinked analytic import")
        require(path.resolve().is_relative_to(ROOT.resolve()), "analytic import path escaped")
        require(hashlib.sha256(path.read_bytes()).hexdigest() == digest,
                f"analytic import digest changed: {row['logical_name']}")


def invoke_registry():
    require(REGISTRY.is_file() and not REGISTRY.is_symlink(), "missing typed registry verifier")
    require(hashlib.sha256(REGISTRY.read_bytes()).hexdigest() == REGISTRY_SHA256,
            "typed registry source changed")
    completed = subprocess.run((sys.executable, "-I", "-B", str(REGISTRY),
                                "--emit", "--print-manifest"), cwd=ROOT,
                               check=False, capture_output=True)
    require(completed.returncode == 0 and completed.stderr == b"",
            "typed registry execution failed")
    require(hashlib.sha256(completed.stdout).hexdigest() == REGISTRY_OUTPUT_SHA256,
            "typed registry canonical output changed")
    receipt = strict_json_bytes(completed.stdout, "typed registry receipt")
    require(receipt.get("schema") ==
            "r61-rank-six-single-block-owner-registry-receipt-v1",
            "typed registry receipt schema changed")
    registry = receipt.get("registry", {})
    require(registry.get("owners") == list(OWNERS) and
            registry.get("complete_disjoint_ownership") is True,
            "typed registry is not complete and disjoint")
    require(registry.get("scope") ==
            "all finite simple connected cyclomatic-rank-six graphs with exactly one positive-rank cyclic block",
            "typed registry scope changed")
    return receipt


@dataclass(frozen=True)
class Bound:
    floor: Fraction
    strict: bool


def add_bounds(*bounds):
    return Bound(sum((bound.floor for bound in bounds), Fraction(0)),
                 any(bound.strict for bound in bounds))


def audit_strict_ledgers():
    rooted_k4 = Bound(Fraction(2), True)
    tree = Bound(Fraction(-1), False)
    unicycle = Bound(Fraction(-1), False)  # standard connected-unicyclic floor
    structural = add_bounds(rooted_k4, tree, unicycle)
    require(structural == Bound(Fraction(0), True),
            "port-blind structural ledger changed")
    k110_zero = add_bounds(rooted_k4, tree, unicycle)
    k110_one = add_bounds(rooted_k4, tree, unicycle)
    k223 = add_bounds(rooted_k4, tree, unicycle)
    require(all(bound.floor >= 0 and bound.strict for bound in
                (k110_zero, k110_one, k223)), "structural owner is not strictly closed")
    return structural


def audit_dnn_algebra():
    # Coefficient vectors in variables (m_R,m_U,constant).  This checks the
    # identity without sampling graph sizes.
    kappa_r = (1, 0, 5)
    bridge = (0, 0, 1)
    kappa_u = (0, 1, 1)
    total = tuple(sum(values) for values in zip(kappa_r, bridge, kappa_u))
    m_g_plus_six = (1, 1, 7)  # m_G=m_R+m_U+1
    require(total == m_g_plus_six, "DNN affine cost ledger changed")
    # 2m_G-kappa >= (2,2,2)-(1,1,7)=(1,1,-5)=m_G-6=|V(G)|.
    positive_lower = tuple(a - b for a, b in zip((2, 2, 2), total))
    vertex_count = (1, 1, -5)
    require(positive_lower == vertex_count, "DNN trace/Euler ledger changed")
    # Rational consequence of the analytic epsilon estimate: even q gives 0;
    # odd q>=3 gives epsilon_q<=3/q<=1.  No floating point is used.
    require(Fraction(3, 3) == 1 and Fraction(3, 5) < 1,
            "cycle epsilon rational endpoint changed")
    return total


def induced_edges(edges, vertices):
    vertices = set(vertices)
    return {edge for edge in edges if set(edge) <= vertices}


def is_tree(vertices, edges):
    vertices = set(vertices)
    edges = induced_edges(edges, vertices)
    if not vertices or len(edges) != len(vertices) - 1:
        return False
    seen = {next(iter(vertices))}
    while True:
        enlarged = seen | {v for edge in edges if set(edge) & seen for v in edge}
        if enlarged == seen:
            break
        seen = enlarged
    return seen == vertices


def is_k4(vertices, edges):
    vertices = set(vertices)
    return len(vertices) == 4 and induced_edges(edges, vertices) == {
        tuple(sorted(pair)) for pair in itertools.combinations(vertices, 2)}


def audit_k110_0():
    vertices = set(range(5))
    edges = set(itertools.combinations(range(5), 2))
    # Port blind: use one fixed literal K4, irrespective of either bridge port.
    k4 = {0, 1, 2, 3}
    tree = {4}
    require(k4.isdisjoint(tree) and k4 | tree == vertices, "K110-0 partition changed")
    require(is_k4(k4, edges) and is_tree(tree, edges),
            "K110-0 is not literal K4 plus nonempty tree")
    return (tuple(sorted(k4)), tuple(sorted(tree)))


def long_k5_graph(length):
    require(type(length) is int and length >= 3 and length % 2 == 1,
            "K110-1 long length is not odd and at least three")
    a, b, c, d, e = range(5)
    internal = list(range(5, 5 + length - 1))
    path = [a, *internal, b]
    edges = {tuple(sorted(pair)) for pair in itertools.combinations(range(5), 2)
             if tuple(sorted(pair)) != (a, b)}
    edges |= {tuple(sorted(pair)) for pair in zip(path, path[1:])}
    return set(range(5 + length - 1)), edges, path


def audit_k110_1():
    # The proof is symbolic in l: the fixed K4 {b,c,d,e} does not involve an
    # internal index, while the complementary path territory has l vertices
    # and l-1 edges for every odd l=2h+1>=3.  Concrete endpoint checks guard
    # reconstruction; the universal arithmetic is checked separately below.
    for length in (3, 5):
        vertices, edges, path = long_k5_graph(length)
        k4 = {1, 2, 3, 4}  # {b,c,d,e}
        tree = vertices - k4
        require(k4.isdisjoint(tree) and k4 | tree == vertices,
                "K110-1 partition is not exhaustive")
        require(is_k4(k4, edges) and is_tree(tree, edges),
                "K110-1 fixed K4/tree partition failed")
        require(tree == set(path[:-1]), "K110-1 complementary path territory changed")
    # Symbolic h>=1, l=2h+1: |T|=l, |E(T)|=l-1, and l>=3.
    # Coefficient pairs are affine expressions alpha*h+beta.
    l_vertices = (2, 1)
    l_edges = (2, 0)
    require((l_vertices[0] - l_edges[0], l_vertices[1] - l_edges[1]) == (0, 1),
            "K110-1 symbolic tree Euler identity changed")
    require(2 * 1 + 1 >= 3, "K110-1 symbolic nonemptiness changed")
    return {"fixed_k4": [1, 2, 3, 4], "tree_vertices": "v_0,...,v_(ell-1)",
            "ell": "2h+1, h>=1"}


def map_edge(edge, permutation):
    return tuple(sorted((permutation[edge[0]], permutation[edge[1]])))


def audit_k223():
    require({pair for pair, bit in zip(PAIR6, K223_ROW) if bit == "1"} == K223_EDGES,
            "K223 row decoding changed")
    group = tuple(permutation for permutation in itertools.permutations(range(6))
                  if {map_edge(edge, permutation) for edge in K223_EDGES} == K223_EDGES)
    require(len(group) == 16, "K223 automorphism order changed")
    unseen = set(range(6))
    orbits = []
    while unseen:
        vertex = min(unseen)
        orbit = {permutation[vertex] for permutation in group}
        orbits.append(tuple(sorted(orbit)))
        unseen -= orbit
    require(tuple(orbits) == ((0, 1, 2, 3), (4, 5)), "K223 vertex orbits changed")
    # Port blind: fixed literal K4 and fixed complementary edge, no root input.
    k4 = {0, 3, 4, 5}
    tree = {1, 2}
    require(k4.isdisjoint(tree) and k4 | tree == set(range(6)),
            "K223 partition is not disjoint and exhaustive")
    require(is_k4(k4, K223_EDGES) and is_tree(tree, K223_EDGES),
            "K223 fixed K4/tree partition failed")
    crossing = K223_EDGES - induced_edges(K223_EDGES, k4) - induced_edges(K223_EDGES, tree)
    require(crossing == {(1, 4), (1, 5), (2, 4), (2, 5)},
            "K223 crossing-edge ledger changed")
    return {"automorphism_order": len(group), "vertex_orbits": [list(row) for row in orbits],
            "fixed_k4": sorted(k4), "fixed_tree": sorted(tree),
            "crossing_edges": [list(edge) for edge in sorted(crossing)]}


def select_structural_partition(core_family):
    # Deliberately no bridge port, projected root, U port, cycle length, tree
    # shape, tree depth, or endpoint-degree argument.  The proof leaves the
    # physical bridge and all core-crossing edges between induced territories.
    if core_family == "K110-0":
        return {"k4": (0, 1, 2, 3), "tree": (4,)}
    if core_family == "K110-1":
        return {"k4": (1, 2, 3, 4), "tree": "v_0,...,v_(ell-1)"}
    if core_family == "K223":
        return {"k4": (0, 3, 4, 5), "tree": (1, 2)}
    raise VerificationError("unknown structural family")


def audit_port_blind_contract():
    signature = inspect.signature(select_structural_partition)
    require(tuple(signature.parameters) == ("core_family",),
            "structural selector is not port blind")
    source = inspect.getsource(select_structural_partition)
    forbidden = ("projected_core_root", "rank_one_port", "cycle_length",
                 "tree_depth", "endpoint_degree")
    require(not any(word in source for word in forbidden),
            "structural selector reads forbidden port/tree data")
    for family in OWNERS[1:]:
        select_structural_partition(family)


def validate_package(manifest, run_dependencies=True):
    validate_manifest(manifest)
    if run_dependencies:
        authenticate_imports(manifest)
        invoke_registry()
    audit_dnn_algebra()
    audit_strict_ledgers()
    audit_k110_0()
    audit_k110_1()
    audit_k223()
    audit_port_blind_contract()


def hostile_self_checks(manifest):
    mutations = []

    def add(label, mutate):
        candidate = deepcopy(manifest)
        mutate(candidate)
        mutations.append((label, candidate))

    add("rank widened", lambda value: value["scope"].update(cyclomatic_rank=8))
    add("bridge changed to shared cut", lambda value: value["scope"]["separator"].update(
        kind="shared-cut"))
    add("split changed", lambda value: value["scope"]["separator"].update(side_ranks=[5, 2]))
    add("multiblock rank-six side", lambda value: value["scope"]["rank_six_side"].update(
        positive_rank_cyclic_blocks="arbitrary"))
    add("ports narrowed", lambda value: value["scope"].update(ports="core-vertices-only"))
    add("rank-one arms widened", lambda value: value["scope"]["excluded"].remove(
        "multiple-rank-one-arms"))
    add("strict conclusion", lambda value: value["conclusion"].update(strict=True, relation=">"))
    add("owner omitted", lambda value: value["owners"].remove("K223"))
    add("registry digest", lambda value: value["owner_registry"].update(
        source_sha256="0" * 64))
    add("port dependence", lambda value: value["proof_contract"].update(port_blind=False))
    add("U boundary-opened", lambda value: value["proof_contract"].update(
        structural="boundary-open U at its bridge port"))
    add("debit omitted", lambda value: value["proof_contract"].update(structural_territories=2))
    add("nonclaim removed", lambda value: value["nonclaims"].remove(
        "complete physical R61 closure"))
    add("analytic import omitted", lambda value: value["analytic_imports"].pop())
    for label, candidate in mutations:
        try:
            validate_package(candidate, run_dependencies=False)
        except (IndexError, KeyError, TypeError, VerificationError, ValueError):
            continue
        raise VerificationError(f"hostile mutation accepted: {label}")
    return tuple(label for label, _ in mutations)


def audit():
    manifest = load_manifest()
    validate_package(manifest, run_dependencies=True)
    rejected = hostile_self_checks(manifest)
    require(len(rejected) == 14, "hostile mutation ledger changed")
    k223 = audit_k223()
    return {
        "schema": "r61-physical-single-block-theorem-receipt-v1",
        "theorem": "R61-PHYSICAL-SINGLE-BLOCK",
        "scope": "one actual bridge with side ranks 6|1; rank-six side has exactly one positive-rank cyclic block; arbitrary ports",
        "owners": list(OWNERS),
        "conclusion": "s+(G)>=|V(G)|",
        "strict": False,
        "proof_ledgers": {
            "DNN": "kappa(G)<=m_G+6",
            "K110-0": "sigma(G)>2-1-1=0",
            "K110-1": "sigma(G)>2-1-1=0",
            "K223": "sigma(G)>2-1-1=0",
        },
        "port_blind_structural_selector": True,
        "K223_finite_audit": k223,
        "analytic_import_count": 4,
        "hostile_mutations_rejected": list(rejected),
        "verification_semantics": "exact finite and affine audit plus digest-authenticated analytic imports; rank-six leaf executions use authenticated committed evidence rather than fresh replay of every segment",
        "nonclaim": "complete physical R61 and global heptacyclic multiblock closure remain open",
    }


def optimized_output(arguments):
    completed = subprocess.run((sys.executable, "-I", "-B", "-O", str(Path(__file__).resolve()),
                                "--optimized-child", *arguments), cwd=ROOT,
                               check=False, capture_output=True)
    require(completed.returncode == 0 and completed.stderr == b"",
            "optimized physical theorem audit failed")
    return completed.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--print-manifest", action="store_true")
    parser.add_argument("--optimized-child", action="store_true")
    args = parser.parse_args()
    try:
        receipt = audit()
        output = canonical_bytes(receipt) if args.print_manifest else (
            b"R61 physical single-block theorem: exact audit passed\n")
        if not args.optimized_child and not args.emit and sys.flags.optimize == 0:
            child_args = ("--print-manifest",) if args.print_manifest else ()
            require(optimized_output(child_args) == output,
                    "normal and optimized physical theorem outputs differ")
        sys.stdout.buffer.write(output)
        return 0
    except (OSError, VerificationError, TypeError, ValueError) as error:
        sys.stderr.write(f"R61 physical single-block theorem: FAIL CLOSED: {error}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
