#!/usr/bin/env python3
"""Exhaustive V4-to-row-stabilizer bridge for the retained h=1 cover.

This checker imports only the separately retained independent row/CNF
reconstructor.  For each of 6,186 pre-V4 rows and each of the 120 unordered
pairs in T={0,...,15}, it checks every V4 element taking the row to its
canonical representative.  It then constructs an explicit permutation inside
the canonical row's sorted labelled realization, including the ordinary-A/B
type-sorting relabelling induced by C exchange.  It then constructs a
permutation inside the canonical row's full-incidence blocks carrying the moved
pair to the one retained representative of its orbit.  Ambiguous canonicalizing
V4 maps must land in the same row-stabilizer orbit.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter

import check_h1_selector_parent as independent

EXPECTED_CASES = 742_320
EXPECTED_CANONICAL_ROWS = 1_919
EXPECTED_PAIR_ORBITS = 61_696
EXPECTED_MULTI_MAP_CASES = 178_800
EXPECTED_MAPPING_WITNESSES = 921_120
EXPECTED_PAIR_ORBIT_DIGEST = (
    "922c184dcfaa6dc2fc2ae613b93b7e2b092a797faeeab9956f8865e44bdabb98"
)
EXPECTED_FULL_MAP_DIGEST = (
    "c8b8cc8696ac80cb89f6774cdf1a7ea1cd051c9516d3e0be809aa5fe4d37bcc2"
)
REGRESSION_PRE_ROW = 3
REGRESSION_PAIR = (0, 13)
REGRESSION_MOVED = (0, 14)
REGRESSION_TARGET = (0, 14)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def apply_row(name: str, row: independent.Row) -> independent.Row:
    if name == "e":
        return row
    if name == "c":
        return independent.c_swap(row)
    if name == "h":
        return independent.high_swap(row)
    if name == "ch":
        return independent.c_swap(independent.high_swap(row))
    raise RuntimeError(f"unknown V4 element {name!r}")


def expanded_profiles(row: independent.Row) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Return the complete C-incidence type at each labelled A and B vertex."""
    _, distinguished, ac, bc, _ = row
    ordinary = tuple(typ for typ, number in enumerate(ac) for _ in range(number))
    btypes = tuple(typ for typ, number in enumerate(bc) for _ in range(number))
    require(len(ordinary) == 6 and len(btypes) == 7, "expanded type width changed")
    return tuple(distinguished) + ordinary, btypes


def full_canonicalizing_permutation(
    name: str, row: independent.Row, canonical: independent.Row
) -> tuple[int, ...]:
    """Map ``row`` labels to the sorted labelled realization of ``canonical``.

    A C exchange transposes every two-coordinate C-incidence type.  The count
    row action alone therefore does not specify the label map: ordinary A and B
    vertices must also be re-sorted into the canonical type blocks.  We use the
    unique order-preserving bijection between equal transformed-type classes.
    Any other such bijection differs by the canonical row stabilizer and hence
    reaches the same retained pair orbit; that fact is checked below for every
    ambiguous V4 canonicalizer.
    """
    source_a, source_b = expanded_profiles(row)
    target_a, target_b = expanded_profiles(canonical)
    swap_c = "c" in name
    swap_h = "h" in name
    swap_a_type = (0, 2, 1, 3)

    def transform_a(typ: int) -> int:
        return swap_a_type[typ] if swap_c else typ

    def transform_b(typ: int) -> int:
        return 3 * (typ % 3) + typ // 3 if swap_c else typ

    image: list[int | None] = [None] * 16
    image[0] = 0
    for source in (1, 2):
        target = 3 - source if swap_h else source
        image[source] = target
        require(
            transform_a(source_a[source]) == target_a[target],
            "high label map does not preserve transformed complete C type",
        )

    for source_labels, target_labels, source_types, target_types, transform, offset in (
        (range(3, 9), range(3, 9), source_a, target_a, transform_a, 0),
        (range(9, 16), range(9, 16), source_b, target_b, transform_b, 9),
    ):
        sources_by_type: dict[int, list[int]] = {}
        targets_by_type: dict[int, list[int]] = {}
        for vertex in source_labels:
            sources_by_type.setdefault(transform(source_types[vertex - offset]), []).append(vertex)
        for vertex in target_labels:
            targets_by_type.setdefault(target_types[vertex - offset], []).append(vertex)
        require(
            sources_by_type.keys() == targets_by_type.keys(),
            "canonical type-block support changed under V4 action",
        )
        for typ in sources_by_type:
            sources = sources_by_type[typ]
            targets = targets_by_type[typ]
            require(len(sources) == len(targets), "canonical type-block multiplicity changed")
            for source, target in zip(sources, targets):
                image[source] = target

    require(all(vertex is not None for vertex in image), "incomplete canonicalizing label map")
    permutation = tuple(int(vertex) for vertex in image)
    require(sorted(permutation) == list(range(16)), "canonicalizing label map is not a permutation")
    return permutation


def move_t_pair(
    name: str,
    row: independent.Row,
    canonical: independent.Row,
    pair: tuple[int, int],
) -> tuple[tuple[int, int], tuple[int, ...]]:
    permutation = full_canonicalizing_permutation(name, row, canonical)
    moved = tuple(sorted((permutation[pair[0]], permutation[pair[1]])))
    return moved, permutation


def retained_representative(
    blocks: tuple[tuple[int, ...], ...], pair: tuple[int, int]
) -> tuple[int, int]:
    owner = {vertex: index for index, block in enumerate(blocks) for vertex in block}
    left, right = owner[pair[0]], owner[pair[1]]
    if left == right:
        require(len(blocks[left]) >= 2, "internal pair lies in a singleton block")
        return tuple(sorted((blocks[left][0], blocks[left][1])))
    if left > right:
        left, right = right, left
    return tuple(sorted((blocks[left][0], blocks[right][0])))


def explicit_block_permutation(
    blocks: tuple[tuple[int, ...], ...],
    source: tuple[int, int],
    target: tuple[int, int],
) -> tuple[int, ...]:
    """Extend the endpoint map source->target inside each exact type block."""
    owner = {vertex: block for block in blocks for vertex in block}
    partial: dict[int, int] = {}
    for block in blocks:
        sources = [vertex for vertex in source if owner[vertex] == block]
        targets = [vertex for vertex in target if owner[vertex] == block]
        require(len(sources) == len(targets), "pair endpoints have different block profiles")
        partial.update(zip(sources, targets))

    image = list(range(16))
    for block in blocks:
        fixed_sources = [vertex for vertex in block if vertex in partial]
        used_targets = {partial[vertex] for vertex in fixed_sources}
        require(len(used_targets) == len(fixed_sources), "endpoint map is not injective")
        require(used_targets <= set(block), "endpoint map leaves its exact type block")
        remaining_sources = [vertex for vertex in block if vertex not in partial]
        remaining_targets = [vertex for vertex in block if vertex not in used_targets]
        for vertex in fixed_sources:
            image[vertex] = partial[vertex]
        for vertex, target_vertex in zip(remaining_sources, remaining_targets):
            image[vertex] = target_vertex

    permutation = tuple(image)
    require(sorted(permutation) == list(range(16)), "block witness is not a permutation")
    require(
        tuple(sorted((permutation[source[0]], permutation[source[1]]))) == target,
        "block witness does not carry source pair to target",
    )
    require(
        all(owner[vertex] == owner[permutation[vertex]] for vertex in range(16)),
        "block witness does not preserve full C-incidence types",
    )
    return permutation


def main() -> None:
    pre_rows = independent.independent_pre_rows()
    require(len(pre_rows) == len(set(pre_rows)) == 6_186, "pre-V4 universe changed")
    pre_set = set(pre_rows)
    require(
        all(
            apply_row(name, row) in pre_set
            for row in pre_rows
            for name in ("e", "c", "h", "ch")
        ),
        "V4 action leaves the independently reconstructed h=1 universe",
    )

    canonical_rows = independent.independent_rows()
    require(len(canonical_rows) == EXPECTED_CANONICAL_ROWS, "canonical row count changed")
    canonical_set = set(canonical_rows)

    pair_digest = hashlib.sha256()
    pair_orbits = 0
    for row in canonical_rows:
        representatives = independent.canonical_hole_pairs(row)
        pair_orbits += len(representatives)
        pair_digest.update(
            (
                independent.row_json(row)
                + "\t"
                + json.dumps(sorted(representatives), separators=(",", ":"))
                + "\n"
            ).encode("ascii")
        )
    require(pair_orbits == EXPECTED_PAIR_ORBITS, "canonical pair-orbit total changed")
    require(
        pair_digest.hexdigest() == EXPECTED_PAIR_ORBIT_DIGEST,
        "canonical pair-orbit digest changed",
    )

    cases = 0
    multi_map_cases = 0
    mapping_witnesses = 0
    full_map_digest = hashlib.sha256()
    regression_seen = False
    canonicalizer_distribution: Counter[int] = Counter()
    all_pairs = tuple(itertools.combinations(range(16), 2))

    for row_index, row in enumerate(pre_rows):
        canonical = min(apply_row(name, row) for name in ("e", "c", "h", "ch"))
        require(canonical in canonical_set, "canonical image is absent from retained universe")
        canonicalizers = tuple(
            name for name in ("e", "c", "h", "ch") if apply_row(name, row) == canonical
        )
        require(canonicalizers, "row has no canonicalizing V4 element")
        canonicalizer_distribution[len(canonicalizers)] += 1
        blocks = independent.stabilizer_blocks(canonical)
        representatives = independent.canonical_hole_pairs(canonical)

        for pair in all_pairs:
            targets = set()
            for name in canonicalizers:
                moved, canonicalizing_permutation = move_t_pair(name, row, canonical, pair)
                target = retained_representative(blocks, moved)
                require(target in representatives, "composite image has no retained pair")
                explicit_block_permutation(blocks, moved, target)
                full_map_digest.update(
                    (
                        f"{row_index}\t{name}\t{pair[0]},{pair[1]}\t"
                        + ",".join(map(str, canonicalizing_permutation))
                        + f"\t{moved[0]},{moved[1]}\t{target[0]},{target[1]}\n"
                    ).encode("ascii")
                )
                if (
                    row_index == REGRESSION_PRE_ROW
                    and name == "c"
                    and pair == REGRESSION_PAIR
                ):
                    require(moved == REGRESSION_MOVED, "C-swap sorting regression moved pair changed")
                    require(target == REGRESSION_TARGET, "C-swap sorting regression target changed")
                    regression_seen = True
                targets.add(target)
                mapping_witnesses += 1
            require(
                len(targets) == 1,
                "different canonicalizing V4 maps reach different row-stabilizer orbits",
            )
            if len(canonicalizers) > 1:
                multi_map_cases += 1
            cases += 1

    require(cases == EXPECTED_CASES, f"composite case total changed: {cases}")
    require(
        multi_map_cases == EXPECTED_MULTI_MAP_CASES,
        f"ambiguous-canonicalizer case total changed: {multi_map_cases}",
    )
    require(
        mapping_witnesses == EXPECTED_MAPPING_WITNESSES,
        f"mapping witness total changed: {mapping_witnesses}",
    )
    require(
        canonicalizer_distribution == Counter({1: 4_696, 2: 1_490}),
        f"canonicalizer distribution changed: {canonicalizer_distribution}",
    )
    require(regression_seen, "C-swap type-sorting regression was not exercised")
    require(
        full_map_digest.hexdigest() == EXPECTED_FULL_MAP_DIGEST,
        "full canonicalizing-map digest changed",
    )

    print(
        "PASS composite V4-to-row-stabilizer bridge "
        f"pre_rows={len(pre_rows)} cases={cases} multi_map_cases={multi_map_cases}"
    )
    print(
        "PASS explicit composite mapping witnesses="
        f"{mapping_witnesses} canonical_pair_orbits={pair_orbits}"
    )
    print(
        "PASS full type-sorting canonicalizing maps "
        f"digest={full_map_digest.hexdigest()} regression=row3-c-0,13-to-0,14"
    )
    print(f"PASS pair_orbit_digest={pair_digest.hexdigest()}")


if __name__ == "__main__":
    main()
