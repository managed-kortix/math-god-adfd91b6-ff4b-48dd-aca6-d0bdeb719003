#!/usr/bin/env python3
"""Fail-closed census of loopless 2-connected rank-four multigraph kernels.

Only the Python standard library is used.  The generator independently visits
every weak composition of n+3 among the unordered vertex pairs for 2 <= n <= 6,
then tests degree, connectedness after every vertex deletion, and isomorphism.
"""

from copy import deepcopy
from functools import lru_cache
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations


EXPECTED_DIGEST = "d89e6e60c66e480ba89e662ab90b5ace211cbcff7292f92ad1614bb0937eb8e9"
EXPECTED_COUNTS = (1, 2, 5, 4, 5)
EXPECTED_LABELLED_COUNTS = (1, 7, 54, 255, 550)
EXPECTED_AUTOMORPHISM_ORDERS = (2, 1, 6, 2, 2, 2, 2, 4, 2, 2, 1, 8, 4, 6, 4, 72, 12)
EXPECTED_SIMPLICITY_COSTS = (4, 3, 3, 2, 2, 3, 3, 1, 3, 1, 2, 0, 2, 3, 1, 0, 0)
EXPECTED_KERNELS = (
    (2, (5,)),
    (3, (1, 2, 3)),
    (3, (2, 2, 2)),
    (4, (0, 1, 2, 1, 2, 1)),
    (4, (0, 1, 2, 2, 1, 1)),
    (4, (0, 1, 2, 2, 2, 0)),
    (4, (0, 1, 2, 3, 1, 0)),
    (4, (1, 1, 1, 1, 1, 2)),
    (5, (0, 0, 1, 2, 1, 0, 2, 2, 0, 0)),
    (5, (0, 0, 1, 2, 1, 1, 1, 1, 1, 0)),
    (5, (0, 0, 1, 2, 1, 1, 1, 2, 0, 0)),
    (5, (0, 1, 1, 1, 1, 1, 1, 0, 1, 1)),
    (6, (0, 0, 0, 1, 2, 0, 1, 1, 1, 2, 1, 0, 0, 0, 0)),
    (6, (0, 0, 0, 1, 2, 0, 1, 2, 0, 2, 0, 1, 0, 0, 0)),
    (6, (0, 0, 0, 1, 2, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0)),
    (6, (0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0)),
    (6, (0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0)),
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pairs(n):
    return tuple(combinations(range(n), 2))


def weak_compositions(total, slots, prefix=()):
    require(isinstance(total, int) and total >= 0, "invalid composition total")
    require(isinstance(slots, int) and slots >= 1, "invalid composition width")
    if slots == 1:
        yield prefix + (total,)
        return
    for first in range(total + 1):
        yield from weak_compositions(total - first, slots - 1, prefix + (first,))


def degrees(n, code):
    edge_pairs = pairs(n)
    require(len(code) == len(edge_pairs), "multiplicity code has wrong length")
    result = [0] * n
    for multiplicity, (u, v) in zip(code, edge_pairs):
        require(isinstance(multiplicity, int) and multiplicity >= 0,
                "multiplicity is not a nonnegative integer")
        result[u] += multiplicity
        result[v] += multiplicity
    return tuple(result)


def connected_after_deleting(n, code, deleted):
    remaining = tuple(v for v in range(n) if v != deleted)
    if len(remaining) <= 1:
        return True
    adjacency = [set() for _ in range(n)]
    for multiplicity, (u, v) in zip(code, pairs(n)):
        if multiplicity and u != deleted and v != deleted:
            adjacency[u].add(v)
            adjacency[v].add(u)
    seen = {remaining[0]}
    stack = [remaining[0]]
    while stack:
        vertex = stack.pop()
        for neighbor in adjacency[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return len(seen) == len(remaining)


def is_kernel(n, code, min_degree=3, edge_offset=3):
    if not isinstance(n, int) or n < 2:
        return False
    if len(code) != n * (n - 1) // 2:
        return False
    if any(not isinstance(value, int) or value < 0 for value in code):
        return False
    if sum(code) != n + edge_offset:
        return False
    if min(degrees(n, code)) < min_degree:
        return False
    return all(connected_after_deleting(n, code, deleted)
               for deleted in (None,) + tuple(range(n)))


def relabel(n, code, permutation):
    require(tuple(sorted(permutation)) == tuple(range(n)), "invalid vertex permutation")
    lookup = dict(zip(pairs(n), code))
    return tuple(lookup[tuple(sorted((permutation[u], permutation[v])))]
                 for u, v in pairs(n))


def canonical_code(n, code):
    require(len(code) == n * (n - 1) // 2, "cannot canonicalize malformed code")
    return min(relabel(n, code, permutation) for permutation in permutations(range(n)))


def degree_ordered_code(n, code):
    """Published representative: nondecreasing degrees, then least code."""
    candidates = []
    for permutation in permutations(range(n)):
        candidate = relabel(n, code, permutation)
        if degrees(n, candidate) == tuple(sorted(degrees(n, candidate))):
            candidates.append(candidate)
    require(candidates, "no degree-ordered labelling exists")
    return min(candidates)


def simplicity_cost(code):
    """Minimum subdivisions needed so every parallel class becomes simple."""
    return sum(max(0, multiplicity - 1) for multiplicity in code)


def automorphisms(n, code):
    """Vertex permutations preserving every edge multiplicity."""
    return tuple(permutation for permutation in permutations(range(n))
                 if relabel(n, code, permutation) == code)


def incidence_automorphism_order(n, code):
    """Order when parallel edge copies are also regarded as distinguishable flags."""
    from math import factorial
    return len(automorphisms(n, code)) * prod(factorial(value) for value in code)


def prod(values):
    result = 1
    for value in values:
        result *= value
    return result


def is_simple_subdivision_lengths(code, bundle_lengths):
    """Check exactly when replacing edge copies by paths produces a simple graph."""
    if not isinstance(bundle_lengths, tuple) or len(bundle_lengths) != len(code):
        return False
    for multiplicity, lengths in zip(code, bundle_lengths):
        if not isinstance(lengths, tuple) or len(lengths) != multiplicity:
            return False
        if any(not isinstance(length, int) or length < 1 for length in lengths):
            return False
        if sum(length == 1 for length in lengths) > 1:
            return False
    return True


def minimum_simple_lengths(code):
    """A canonical simple-subdivision witness attaining simplicity_cost(code)."""
    return tuple((1,) + (2,) * (multiplicity - 1) if multiplicity else ()
                 for multiplicity in code)


@lru_cache(maxsize=None)
def census(min_degree=3, edge_offset=3, require_no_cut=True):
    classes = []
    labelled_counts = []
    for n in range(2, 7):
        canonical = set()
        labelled = 0
        for code in weak_compositions(n + edge_offset, len(pairs(n))):
            if min(degrees(n, code)) < min_degree:
                continue
            if require_no_cut and not all(
                    connected_after_deleting(n, code, deleted)
                    for deleted in (None,) + tuple(range(n))):
                continue
            labelled += 1
            canonical.add(canonical_code(n, code))
        labelled_counts.append(labelled)
        classes.extend((n, code) for code in sorted(canonical))
    return tuple(classes), tuple(labelled_counts)


def canonical_payload(kernels):
    """Stable published payload using one-based edge names and exponents."""
    lines = []
    published_kernels = sorted((n, degree_ordered_code(n, code)) for n, code in kernels)
    for n, published in published_kernels:
        edge_terms = []
        for multiplicity, (u, v) in zip(published, pairs(n)):
            if multiplicity:
                term = f"{u + 1}{v + 1}"
                if multiplicity > 1:
                    term += f"^{multiplicity}"
                edge_terms.append(term)
        degree_text = ", ".join(map(str, sorted(degrees(n, published), reverse=True)))
        lines.append(f"n={n}; deg=({degree_text}); edges={','.join(edge_terms)}")
    return "\n".join(lines) + "\n"


def census_digest(kernels):
    generated = sha256(canonical_payload(kernels).encode("ascii")).hexdigest()
    require(generated == EXPECTED_DIGEST, "published canonical-list digest changed")
    return generated


def audit(expected=EXPECTED_KERNELS, expected_counts=EXPECTED_COUNTS,
          expected_automorphisms=EXPECTED_AUTOMORPHISM_ORDERS,
          expected_costs=EXPECTED_SIMPLICITY_COSTS,
          min_degree=3, edge_offset=3, require_no_cut=True):
    require(min_degree == 3, "minimum-degree policy changed")
    require(edge_offset == 3, "rank-four edge count changed")
    require(require_no_cut is True, "cut-vertex policy changed")
    require(expected_counts == EXPECTED_COUNTS, "expected count ledger changed")
    require(expected_automorphisms == EXPECTED_AUTOMORPHISM_ORDERS,
            "automorphism-order ledger changed")
    require(expected_costs == EXPECTED_SIMPLICITY_COSTS,
            "simplicity-cost ledger changed")
    require(isinstance(expected, tuple), "canonical fixture is not immutable")
    require(len(expected) == 17, "canonical fixture does not contain 17 kernels")
    require(len(set(expected)) == len(expected), "canonical fixture has duplicates")
    require(expected == tuple(sorted(expected)), "canonical fixture is not sorted")
    for n, code in expected:
        require(is_kernel(n, code), "fixture contains a non-kernel")
        require(canonical_code(n, code) == code, "fixture contains a noncanonical code")
    generated, labelled_counts = census(min_degree, edge_offset, require_no_cut)
    counts = tuple(sum(n == order for n, _ in generated) for order in range(2, 7))
    require(counts == expected_counts, "unlabelled counts by order changed")
    require(labelled_counts == EXPECTED_LABELLED_COUNTS, "labelled counts by order changed")
    require(generated == expected, "independently regenerated canonical list changed")
    generated_automorphisms = tuple(len(automorphisms(n, code)) for n, code in generated)
    generated_costs = tuple(simplicity_cost(code) for _, code in generated)
    require(generated_automorphisms == expected_automorphisms,
            "automorphism orders changed")
    require(generated_costs == expected_costs, "simplicity costs changed")
    for n, code in generated:
        require(is_kernel(n, code), "listed object is not a rank-four kernel")
        require(canonical_code(n, code) == code, "listed code is not canonical")
        require(sum(degrees(n, code)) == 2 * (n + 3), "handshake identity failed")
        require(sum(degree - 2 for degree in degrees(n, code)) == 6,
                "degree-excess identity failed")
        require(simplicity_cost(code) == sum(code) - sum(value > 0 for value in code),
                "simplicity cost identity failed")
        witness = minimum_simple_lengths(code)
        require(is_simple_subdivision_lengths(code, witness),
                "minimum simple-subdivision witness rejected")
        require(sum(sum(length - 1 for length in lengths) for lengths in witness)
                == simplicity_cost(code), "minimum subdivision witness has wrong cost")
        for bundle, multiplicity in enumerate(code):
            if multiplicity > 1:
                hostile = list(witness)
                hostile[bundle] = (1,) * multiplicity
                require(not is_simple_subdivision_lengths(code, tuple(hostile)),
                        "parallel direct edges accepted as a simple subdivision")
    return generated, labelled_counts, generated_costs


def expect_rejected(action, label):
    try:
        action()
    except (RuntimeError, TypeError, ValueError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_self_checks():
    mutations = []

    def add(label, mutator, **audit_changes):
        fixture = [[n, list(code)] for n, code in deepcopy(EXPECTED_KERNELS)]
        mutator(fixture)
        candidate = tuple((n, tuple(code)) for n, code in fixture)
        mutations.append((label, candidate, audit_changes))

    add("deleted kernel", lambda rows: rows.pop())
    add("duplicated kernel", lambda rows: rows.append(deepcopy(rows[-1])))
    add("changed multiplicity", lambda rows: rows[1][1].__setitem__(0, 2))
    add("noncanonical relabelling", lambda rows: rows[3].__setitem__(1, [1, 0, 2, 1, 1, 2]))
    add("wrong order", lambda rows: rows[0].__setitem__(0, 3))
    add("degree threshold weakened", lambda rows: None, min_degree=2)
    add("rank changed", lambda rows: None, edge_offset=2)
    add("cut-vertex test disabled", lambda rows: None, require_no_cut=False)
    add("count ledger changed", lambda rows: None, expected_counts=(1, 2, 5, 5, 4))
    add("automorphism ledger changed", lambda rows: None,
        expected_automorphisms=EXPECTED_AUTOMORPHISM_ORDERS[:-1] + (11,))
    add("simplicity ledger changed", lambda rows: None,
        expected_costs=EXPECTED_SIMPLICITY_COSTS[:-1] + (1,))
    add("boolean multiplicity", lambda rows: rows[0][1].__setitem__(0, True))
    add("floating multiplicity", lambda rows: rows[0][1].__setitem__(0, 5.0))
    add("nonintegral multiplicity", lambda rows: rows[0][1].__setitem__(0, Fraction(5, 2)))

    for label, candidate, changes in mutations:
        expect_rejected(lambda candidate=candidate, changes=changes:
                        audit(expected=candidate, **changes), label)
    return len(mutations)


def main():
    kernels, labelled_counts, costs = audit()
    digest = census_digest(kernels)
    mutations = hostile_self_checks()
    require(mutations == 14, "hostile mutation count changed")
    counts = tuple(sum(n == order for n, _ in kernels) for order in range(2, 7))
    print("rank-four kernel census: exact audit passed")
    print(f"canonical_counts_n2_to_n6: {','.join(map(str, counts))} (total {len(kernels)})")
    print(f"labelled_counts_n2_to_n6: {','.join(map(str, labelled_counts))}")
    print(f"canonical_list_sha256: {digest}")
    print(f"simplicity_costs: {','.join(map(str, costs))}")
    print("kernel_listing: id;n;degrees;code;aut_vertices;aut_incidence;simplicity_cost")
    for identifier, (n, code) in enumerate(kernels, 1):
        degree_text = ",".join(map(str, sorted(degrees(n, code), reverse=True)))
        code_text = ",".join(map(str, code))
        print(f"kernel: {identifier};{n};{degree_text};{code_text};"
              f"{len(automorphisms(n, code))};{incidence_automorphism_order(n, code)};"
              f"{simplicity_cost(code)}")
    print(f"rejected_hostile_mutations: {mutations}")


if __name__ == "__main__":
    main()
