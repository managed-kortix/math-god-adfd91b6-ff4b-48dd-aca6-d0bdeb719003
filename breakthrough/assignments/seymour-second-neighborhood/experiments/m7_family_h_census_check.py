#!/usr/bin/env python3
"""Independent exact census and symmetry audit for order-18 family H.

This module does not import a CNF producer or any family-H row generator.  It
reconstructs the q-incidence universe directly.  A row records, for every
vertex other than q, whether its unordered pair with q has status

    O : q -> x,  I : x -> q,  H : q--x is a hole.

Family H fixes v-q as I and q-r as O.  The two root-location cases have
uniform block sizes (6,7,2) and (7,6,2); C admits only I/H.  Permuting labels
inside those three blocks is S_G1 x S_G2 x S_C.
"""
from itertools import permutations, product
from math import comb, factorial

STATUSES = ("O", "I", "H")
ORDER = {status: index for index, status in enumerate(STATUSES)}
CASES = {
    "A": (tuple(range(3, 9)), tuple(range(9, 16)), (16, 17)),
    "B": (tuple(range(2, 9)), tuple(range(10, 16)), (16, 17)),
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def multinomial3(size, counts):
    o_count, i_count, h_count = counts
    require(o_count + i_count + h_count == size, "bad multinomial margin")
    return factorial(size) // (
        factorial(o_count) * factorial(i_count) * factorial(h_count)
    )


def integer_rows(size1, size2):
    """Return exact sorted-status orbit keys for one location case."""
    result = []
    for o1 in range(size1 + 1):
        for i1 in range(size1 - o1 + 1):
            h1 = size1 - o1 - i1
            for o2 in range(size2 + 1):
                for i2 in range(size2 - o2 + 1):
                    h2 = size2 - o2 - i2
                    for h_c in range(3):
                        # q has nine outarcs: q->r plus eight in G1 union G2.
                        # At most all seven graph holes may be incident with q.
                        if o1 + o2 == 8 and h1 + h2 + h_c <= 7:
                            result.append(((o1, i1, h1), (o2, i2, h2), h_c))
    return tuple(result)


def labelled_multiplicity(row, size1, size2):
    counts1, counts2, h_c = row
    return (
        multinomial3(size1, counts1)
        * multinomial3(size2, counts2)
        * comb(2, h_c)
    )


def status_counts(word):
    return tuple(word.count(status) for status in STATUSES)


def orbit_key(word1, word2, word_c):
    return status_counts(word1), status_counts(word2), word_c.count("H")


def valid_labelled(word1, word2, word_c):
    require(all(status in STATUSES for status in word1 + word2 + word_c),
            "unknown status")
    return (
        "O" not in word_c
        and word1.count("O") + word2.count("O") == 8
        and word1.count("H") + word2.count("H") + word_c.count("H") <= 7
    )


def sorted_word(word):
    return tuple(sorted(word, key=ORDER.__getitem__))


def sorting_clause_pair(status_left, status_right):
    """Evaluate the two adjacent CNF clauses on a q-status pair.

    Literals are interpreted from status alone:
      (-a_qw or a_qu),
      (-a_wq or a_qu or a_uq).
    """
    a_qu = status_left == "O"
    a_uq = status_left == "I"
    a_qw = status_right == "O"
    a_wq = status_right == "I"
    return ((not a_qw) or a_qu) and ((not a_wq) or a_qu or a_uq)


def audit_sorting_clauses():
    accepted = set()
    for left, right in product(STATUSES, repeat=2):
        if sorting_clause_pair(left, right):
            accepted.add((left, right))
    expected = {
        (left, right)
        for left, right in product(STATUSES, repeat=2)
        if ORDER[left] <= ORDER[right]
    }
    require(accepted == expected,
            f"sorting clauses accept {accepted}, expected {expected}")


def apply_permutation(word, permutation):
    require(sorted(permutation) == list(range(len(word))), "not a permutation")
    return tuple(word[index] for index in permutation)


def audit_group_canonicalization(case):
    """Exhaust the labelled q rows and prove sorting is an orbit transversal.

    We do not enumerate all |G1|!|G2|!2! group elements.  For each labelled
    row, the unique sorted word with the same three block-margins is obtained by
    an explicit within-block permutation.  Conversely, permutations preserve
    those margins.  Exhausting all 3^13*2^2 candidate words checks both claims
    over the complete family-H q-incidence universe.
    """
    g1, g2, c_block = CASES[case]
    size1, size2 = len(g1), len(g2)
    expected_keys = set(integer_rows(size1, size2))
    seen_keys = set()
    labelled = 0
    representatives = set()

    def canonicalizing_permutation(word):
        # Stable sorting exposes a concrete member of the full symmetric group.
        return tuple(sorted(range(len(word)), key=lambda index: ORDER[word[index]]))

    for word1 in product(STATUSES, repeat=size1):
        for word2 in product(STATUSES, repeat=size2):
            if word1.count("O") + word2.count("O") != 8:
                continue
            for word_c in product(("I", "H"), repeat=2):
                if not valid_labelled(word1, word2, word_c):
                    continue
                labelled += 1
                key = orbit_key(word1, word2, word_c)
                seen_keys.add(key)
                p1 = canonicalizing_permutation(word1)
                p2 = canonicalizing_permutation(word2)
                pc = canonicalizing_permutation(word_c)
                canonical = (
                    apply_permutation(word1, p1),
                    apply_permutation(word2, p2),
                    apply_permutation(word_c, pc),
                )
                require(all(sorting_clause_pair(x, y)
                            for word in canonical
                            for x, y in zip(word, word[1:])),
                        "explicit canonicalizer did not satisfy sorting clauses")
                require(orbit_key(*canonical) == key,
                        "within-block canonicalizer changed orbit key")
                representatives.add(canonical)

    require(seen_keys == expected_keys, "labelled universe and integer rows differ")
    require(len(representatives) == len(expected_keys),
            "sorting is not one representative per status orbit")
    require(labelled == sum(labelled_multiplicity(row, size1, size2)
                            for row in integer_rows(size1, size2)),
            "direct labelled count and multinomial count differ")
    return len(expected_keys), labelled


def main():
    audit_sorting_clauses()
    results = {}
    for case, blocks in CASES.items():
        size1, size2 = len(blocks[0]), len(blocks[1])
        rows = integer_rows(size1, size2)
        multiplicity = sum(labelled_multiplicity(row, size1, size2) for row in rows)
        direct_orbits, direct_labelled = audit_group_canonicalization(case)
        require(len(rows) == direct_orbits == 168, f"case {case}: orbit count")
        require(multiplicity == direct_labelled == 164736,
                f"case {case}: labelled count")
        results[case] = (len(rows), multiplicity)
        print(f"PASS family-H case={case} q_status_orbits={len(rows)} "
              f"labelled_rows={multiplicity}")
    require(results["A"] == results["B"], "location cases disagree")
    print("PASS q-status sorting canonicalization under S_G1 x S_G2 x S_C")


if __name__ == "__main__":
    main()
