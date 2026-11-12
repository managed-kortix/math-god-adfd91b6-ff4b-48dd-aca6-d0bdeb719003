#!/usr/bin/env python3
"""Exact reusable row/target composition ledger for rank seven, order nine.

This module has a deliberately narrow claim boundary.  :class:`StageLedger`
checks identities between an ordered row universe and successive owner/remainder
boundaries.  It also hashes the canonical target contract
``[full_row_key, target_index]`` for every target index in ``0..15``.

Those checks are *finite-key accounting only*.  A partition does not prove that
a lane's certificate owns any row.  ``derive_bounded_premise`` therefore also
requires an exact lane-implication registry and a separately authenticated
analytic-dependency registry.  It derives only the bounded order-nine finite
premise; it never emits theorem eligibility or a global analytic claim.

A canonical artifact row identity is the full five-field tuple
``(source_index, global_kernel, order_kernel, row_tuple, orbit_size)``; no
proper subset is treated as the identity.  The ``source_index`` field is also
checked separately as unique, strictly source-ordered metadata, but it need
not be consecutive.

Target receipts have two explicitly different meanings.  With a supplied
target stream they authenticate that observed stream.  Without one they are
generated row-times-``0..15`` contracts; they must not be represented as
observed child evidence.  In either case this module remains an accounting
primitive: digest strings and Boolean verdicts passed to
``derive_bounded_premise`` are not made trustworthy merely by their shape.  A
release master must compare them with its own pinned proof/verifier/output
bytes and expected receipts before calling the composer.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any, Iterable, Iterator, Mapping, NamedTuple, Sequence

Json = Any
RowKey = tuple[int, int, int, tuple[int, ...], int]
TargetKey = tuple[RowKey, int]

TARGET_INDICES = tuple(range(16))
IMPLICATION_KINDS = frozenset({"uniform-all-descendant", "explicit-frontier"})
BOUNDARY_SCHEMA = "rank-seven-order-nine-stage-boundary-v1"
TARGET_SCHEMA = "rank-seven-order-nine-row-target-contract-v1"
ACCOUNTING_SCHEMA = "rank-seven-order-nine-finite-key-accounting-v1"
PREMISE_SCHEMA = "rank-seven-order-nine-bounded-premise-composition-v1"

BOUNDARY_FIELDS = frozenset({
    "schema", "stage", "source_row_total", "source_physical_total",
    "source_key_sha256", "source_index_sha256", "owner_row_total",
    "owner_physical_total", "owner_key_sha256", "owner_index_sha256",
    "owner_target_total", "remainder_row_total", "remainder_physical_total",
    "remainder_key_sha256", "remainder_index_sha256", "ordered_subsequences",
    "exact_disjoint_union", "analytic_ownership_established",
})
TARGET_FIELDS = frozenset({
    "schema", "scope", "row_total", "row_key_sha256", "target_indices",
    "per_row_target_cardinality", "per_row_cardinality_validated",
    "target_total", "target_key_sha256", "encoding", "evidence_kind",
    "observed_target_stream_validated", "analytic_ownership_established",
})
IMPLICATION_FIELDS = frozenset({
    "lane", "implication_kind", "row_total", "row_key_sha256", "target_indices",
    "target_total", "target_key_sha256", "proof_contract_sha256",
    "verifier_sha256", "verification_output_sha256", "authenticated",
    "lane_implication_verified",
})
DEPENDENCY_FIELDS = frozenset({"authenticated", "dependency_sha256"})


def require(condition: bool, message: str) -> None:
    """Raise a fail-closed error without relying on optimizable assertions."""
    if not condition:
        raise RuntimeError(message)


def exact_int(value: object, label: str, *, minimum: int = 0) -> int:
    """Return an exact integer, rejecting booleans and numeric lookalikes."""
    require(type(value) is int and value >= minimum, f"{label}: invalid exact integer")
    return value


def exact_bool(value: object, label: str) -> bool:
    require(type(value) is bool, f"{label}: invalid exact boolean")
    return value


def _validate_json(value: object, label: str) -> None:
    value_type = type(value)
    if value is None or value_type in (str, bool, int):
        return
    if value_type in (list, tuple):
        for index, item in enumerate(value):
            _validate_json(item, f"{label}[{index}]")
        return
    if value_type is dict:
        for key, item in value.items():
            require(type(key) is str, f"{label}: non-string JSON key")
            _validate_json(item, f"{label}.{key}")
        return
    raise RuntimeError(f"{label}: non-integral JSON value")


def canonical_bytes(value: Json) -> bytes:
    """Canonical ASCII JSON line, with floats and non-JSON values rejected."""
    _validate_json(value, "canonical value")
    try:
        encoded = json.dumps(value, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=True, allow_nan=False)
        return (encoded + "\n").encode("ascii")
    except (TypeError, ValueError, UnicodeError) as error:
        raise RuntimeError("cannot encode canonical JSON") from error


def _row_json(key: RowKey) -> list[Json]:
    return [key[0], key[1], key[2], list(key[3]), key[4]]


def canonical_row_key(value: object, label: str = "row key") -> RowKey:
    """Validate and normalize a full five-field row identity.

    Lists are accepted at artifact boundaries, but the returned identity is
    always a tuple whose fourth field is itself a tuple.
    """
    require(type(value) in (list, tuple) and len(value) == 5,
            f"{label}: expected a five-field row key")
    source_index = exact_int(value[0], f"{label}.source_index")
    global_kernel = exact_int(value[1], f"{label}.global_kernel", minimum=1)
    order_kernel = exact_int(value[2], f"{label}.order_kernel", minimum=1)
    raw_row = value[3]
    require(type(raw_row) in (list, tuple) and len(raw_row) > 0,
            f"{label}.row: expected a nonempty integer vector")
    row = tuple(exact_int(item, f"{label}.row[{index}]")
                for index, item in enumerate(raw_row))
    orbit_size = exact_int(value[4], f"{label}.orbit_size", minimum=1)
    return source_index, global_kernel, order_kernel, row, orbit_size


def _freeze_rows(values: Iterable[object], label: str) -> tuple[RowKey, ...]:
    try:
        rows = tuple(canonical_row_key(value, f"{label}[{index}]")
                     for index, value in enumerate(values))
    except TypeError as error:
        raise RuntimeError(f"{label}: row sequence is not iterable") from error
    seen_rows: set[RowKey] = set()
    seen_indices: set[int] = set()
    # Excluding source_index prevents one semantic row from being counted twice
    # under two fabricated indices.  The canonical census producer is expected
    # to make this tuple injective; StageLedger enforces that expectation.
    seen_semantic_rows: set[tuple[int, int, tuple[int, ...], int]] = set()
    previous_index: int | None = None
    for position, row in enumerate(rows):
        source_index = row[0]
        semantic_row = row[1:]
        require(row not in seen_rows, f"{label}[{position}]: duplicate full row key")
        require(source_index not in seen_indices,
                f"{label}[{position}]: duplicate source-index metadata")
        require(semantic_row not in seen_semantic_rows,
                f"{label}[{position}]: duplicate semantic row under distinct source indices")
        require(previous_index is None or previous_index < source_index,
                f"{label}[{position}]: source-index order changed")
        seen_rows.add(row)
        seen_indices.add(source_index)
        seen_semantic_rows.add(semantic_row)
        previous_index = source_index
    return rows


def _row_digest(rows: Sequence[RowKey]) -> str:
    digest = hashlib.sha256()
    for row in rows:
        digest.update(canonical_bytes(_row_json(row)))
    return digest.hexdigest()


def _index_digest(rows: Sequence[RowKey]) -> str:
    digest = hashlib.sha256()
    for row in rows:
        digest.update(f"{row[0]}\n".encode("ascii"))
    return digest.hexdigest()


def _physical_mass(rows: Sequence[RowKey]) -> int:
    # The mass is derived only from the authenticated full key's fifth field.
    return sum(row[4] for row in rows)


def _is_sha256(value: object) -> bool:
    return (type(value) is str and len(value) == 64 and
            all(character in "0123456789abcdef" for character in value))


def _boundary_receipt(stage: str, source_values: Iterable[object],
                      owner_values: Iterable[object],
                      remainder_values: Iterable[object]) -> tuple[
                          dict[str, Json], tuple[RowKey, ...], tuple[RowKey, ...],
                          tuple[RowKey, ...]]:
    """Revalidate a partition and derive its receipt only from canonical rows."""
    require(type(stage) is str and bool(stage) and stage.isascii(),
            "stage must be a nonempty ASCII string")
    source_rows = _freeze_rows(source_values, f"{stage}.source")
    owner_rows = _freeze_rows(owner_values, f"{stage}.owners")
    remainder_rows = _freeze_rows(remainder_values, f"{stage}.remainder")

    source_by_index = {row[0]: row for row in source_rows}
    for partition, rows in (("owner", owner_rows), ("remainder", remainder_rows)):
        for position, row in enumerate(rows):
            require(source_by_index.get(row[0]) == row,
                    f"{stage}.{partition}[{position}]: full row key is not in source")

    owner_set = set(owner_rows)
    remainder_set = set(remainder_rows)
    require(owner_set.isdisjoint(remainder_set),
            f"{stage}: owner/remainder overlap")

    owner_position = remainder_position = 0
    for source_position, source_row in enumerate(source_rows):
        if (owner_position < len(owner_rows) and
                owner_rows[owner_position] == source_row):
            owner_position += 1
        elif (remainder_position < len(remainder_rows) and
              remainder_rows[remainder_position] == source_row):
            remainder_position += 1
        else:
            raise RuntimeError(
                f"{stage}: owner/remainder merge omits or changes source row "
                f"{source_position}"
            )
    require(owner_position == len(owner_rows) and
            remainder_position == len(remainder_rows),
            f"{stage}: owner/remainder streams contain surplus rows")
    require(len(owner_rows) + len(remainder_rows) == len(source_rows),
            f"{stage}: owner/remainder cardinality changed")
    require(_physical_mass(owner_rows) + _physical_mass(remainder_rows) ==
            _physical_mass(source_rows),
            f"{stage}: owner/remainder physical mass changed")

    receipt = {
        "schema": BOUNDARY_SCHEMA,
        "stage": stage,
        "source_row_total": len(source_rows),
        "source_physical_total": _physical_mass(source_rows),
        "source_key_sha256": _row_digest(source_rows),
        "source_index_sha256": _index_digest(source_rows),
        "owner_row_total": len(owner_rows),
        "owner_physical_total": _physical_mass(owner_rows),
        "owner_key_sha256": _row_digest(owner_rows),
        "owner_index_sha256": _index_digest(owner_rows),
        "owner_target_total": len(owner_rows) * len(TARGET_INDICES),
        "remainder_row_total": len(remainder_rows),
        "remainder_physical_total": _physical_mass(remainder_rows),
        "remainder_key_sha256": _row_digest(remainder_rows),
        "remainder_index_sha256": _index_digest(remainder_rows),
        "ordered_subsequences": True,
        "exact_disjoint_union": True,
        "analytic_ownership_established": False,
    }
    require(set(receipt) == BOUNDARY_FIELDS,
            "internal boundary receipt schema changed")
    return receipt, source_rows, owner_rows, remainder_rows


def _require_stored_receipt(stored: object, recomputed: dict[str, Json],
                            fields: frozenset[str], label: str) -> None:
    require(type(stored) is dict and set(stored) == fields,
            f"{label}: stored receipt schema changed")
    require(canonical_bytes(stored) == canonical_bytes(recomputed),
            f"{label}: stored receipt integrity changed")


def iter_target_keys(rows: Iterable[object]) -> Iterator[TargetKey]:
    """Yield the exact row-major target universe for indices ``0..15``."""
    frozen = _freeze_rows(rows, "target source rows")
    for row in frozen:
        for target_index in TARGET_INDICES:
            yield row, target_index


def _canonical_target(value: object, label: str) -> TargetKey:
    require(type(value) in (list, tuple) and len(value) == 2,
            f"{label}: expected [full_row_key,target_index]")
    row = canonical_row_key(value[0], f"{label}.row_key")
    target_index = exact_int(value[1], f"{label}.target_index")
    require(target_index in TARGET_INDICES, f"{label}: target index outside 0..15")
    return row, target_index


def _validate_expected(receipt: dict[str, Json], expected: Mapping[str, Json] | None,
                       fields: frozenset[str], label: str) -> None:
    if expected is None:
        return
    require(type(expected) is dict and set(expected) == fields,
            f"{label}: expected receipt schema changed")
    # Canonical bytes, rather than Python equality, reject True/1 laundering.
    require(canonical_bytes(expected) == canonical_bytes(receipt),
            f"{label}: exact receipt changed")


def _target_receipt(rows: Sequence[RowKey], scope: str,
                    targets: Iterable[object] | None = None) -> dict[str, Json]:
    require(type(scope) is str and bool(scope) and scope.isascii(),
            "target scope must be a nonempty ASCII string")
    target_digest = hashlib.sha256()
    target_total = 0
    observed_stream = targets is not None
    supplied = iter(targets) if observed_stream else None
    for row_position, row in enumerate(rows):
        row_target_total = 0
        for target_index in TARGET_INDICES:
            expected_target = (row, target_index)
            if supplied is not None:
                try:
                    observed = _canonical_target(
                        next(supplied),
                        f"{scope}.target[{target_total}]",
                    )
                except StopIteration as error:
                    raise RuntimeError(f"{scope}: target stream ended early") from error
                require(observed == expected_target,
                        f"{scope}: target duplicate, omission, or order change at "
                        f"row {row_position} index {target_index}")
            target_digest.update(canonical_bytes([_row_json(row), target_index]))
            target_total += 1
            row_target_total += 1
        require(row_target_total == len(TARGET_INDICES),
                f"{scope}: per-row target cardinality changed")
    if supplied is not None:
        try:
            next(supplied)
        except StopIteration:
            pass
        else:
            raise RuntimeError(f"{scope}: target stream has a surplus record")
    require(target_total == len(rows) * len(TARGET_INDICES),
            f"{scope}: aggregate target cardinality changed")
    return {
        "schema": TARGET_SCHEMA,
        "scope": scope,
        "row_total": len(rows),
        "row_key_sha256": _row_digest(rows),
        "target_indices": list(TARGET_INDICES),
        "per_row_target_cardinality": len(TARGET_INDICES),
        "per_row_cardinality_validated": True,
        "target_total": target_total,
        "target_key_sha256": target_digest.hexdigest(),
        "encoding": (
            "sha256(concatenated canonical ASCII JSON lines "
            "[full_five_field_row_key,target_index] in row-major order)"
        ),
        "evidence_kind": ("observed-exact-target-stream" if observed_stream else
                          "generated-row-times-target-index-contract"),
        "observed_target_stream_validated": observed_stream,
        "analytic_ownership_established": False,
    }


class _StageState(NamedTuple):
    boundary: dict[str, Json]
    owners: tuple[RowKey, ...]
    remainder: tuple[RowKey, ...]


class StageLedger:
    """Compose exact ordered owner/remainder boundaries over full row keys."""

    def __init__(self, source_rows: Iterable[object]):
        self._universe = _freeze_rows(source_rows, "source")
        require(bool(self._universe), "source: empty row universe")
        self._current = self._universe
        self._stages: dict[str, _StageState] = {}
        self._target_receipts: dict[str, dict[str, Json]] = {}
        self._universe_target_receipt: dict[str, Json] | None = None

    @property
    def source_rows(self) -> tuple[RowKey, ...]:
        return self._universe

    @property
    def remaining_rows(self) -> tuple[RowKey, ...]:
        return self._current

    @property
    def stage_names(self) -> tuple[str, ...]:
        return tuple(self._stages)

    def boundary(self, stage: str) -> dict[str, Json]:
        require(type(stage) is str and stage in self._stages, "unknown stage")
        return deepcopy(self._stages[stage].boundary)

    def owner_rows(self, stage: str) -> tuple[RowKey, ...]:
        require(type(stage) is str and stage in self._stages, "unknown stage")
        return self._stages[stage].owners

    def advance(self, stage: str, owners: Iterable[object], remainder: Iterable[object],
                *, expected: Mapping[str, Json] | None = None) -> dict[str, Json]:
        """Validate one exact source = owners disjoint-union remainder boundary.

        Owner and remainder streams must each be source-ordered subsequences.
        Their row-by-row merge must reproduce the current source exactly.  An
        optional exact receipt pin detects count/mass-preserving lane swaps.
        State advances only after every check (including the pin) succeeds.
        """
        require(type(stage) is str and bool(stage) and stage.isascii(),
                "stage must be a nonempty ASCII string")
        require(stage not in self._stages, f"duplicate stage: {stage}")
        receipt, source_rows, owner_rows, remainder_rows = _boundary_receipt(
            stage, self._current, owners, remainder)
        require(source_rows == self._current,
                f"{stage}: current source rows are not canonical")
        _validate_expected(receipt, expected, BOUNDARY_FIELDS, f"{stage} boundary")

        self._stages[stage] = _StageState(deepcopy(receipt), owner_rows, remainder_rows)
        self._current = remainder_rows
        return deepcopy(receipt)

    def stage_target_contract(self, stage: str, *, targets: Iterable[object] | None = None,
                              expected: Mapping[str, Json] | None = None) -> dict[str, Json]:
        """Observe or generate ``owners(stage) x tuple(range(16))`` exactly."""
        require(type(stage) is str and stage in self._stages, "unknown target stage")
        receipt = _target_receipt(self._stages[stage].owners, stage, targets)
        require(set(receipt) == TARGET_FIELDS, "internal target receipt schema changed")
        _validate_expected(receipt, expected, TARGET_FIELDS, f"{stage} target contract")
        self._target_receipts[stage] = deepcopy(receipt)
        return deepcopy(receipt)

    def universe_target_contract(self, *, targets: Iterable[object] | None = None,
                                 expected: Mapping[str, Json] | None = None) -> dict[str, Json]:
        """Observe or generate the residual universe times ``0..15`` exactly."""
        receipt = _target_receipt(self._universe, "residual-universe", targets)
        require(set(receipt) == TARGET_FIELDS, "internal universe target schema changed")
        _validate_expected(receipt, expected, TARGET_FIELDS,
                           "residual-universe target contract")
        self._universe_target_receipt = deepcopy(receipt)
        return deepcopy(receipt)

    def _recompute_and_validate_receipts(self) -> tuple[
            list[dict[str, Json]], dict[str, dict[str, Json]], dict[str, Json]]:
        """Recompute every receipt from rows and reject mutable-state drift."""
        require(type(self._stages) is dict, "stored stage registry type changed")
        require(type(self._target_receipts) is dict,
                "stored target receipt registry type changed")
        universe = _freeze_rows(self._universe, "stored source")
        require(type(self._universe) is tuple and universe == self._universe,
                "stored source rows are not canonical")
        require(set(self._target_receipts).issubset(set(self._stages)),
                "stored target receipt exists for an unknown stage")

        source = universe
        boundaries: list[dict[str, Json]] = []
        target_receipts: dict[str, dict[str, Json]] = {}
        for stage, state in self._stages.items():
            require(type(state) is _StageState, f"{stage}: stored stage type changed")
            recomputed, recomputed_source, owners, remainder = _boundary_receipt(
                stage, source, state.owners, state.remainder)
            require(recomputed_source == source,
                    f"{stage}: stored boundary source changed")
            require(type(state.owners) is tuple and owners == state.owners and
                    type(state.remainder) is tuple and remainder == state.remainder,
                    f"{stage}: stored owner/remainder rows are not canonical")
            _require_stored_receipt(state.boundary, recomputed, BOUNDARY_FIELDS,
                                    f"{stage} boundary")
            boundaries.append(recomputed)

            target = _target_receipt(owners, stage)
            if stage in self._target_receipts:
                _require_stored_receipt(self._target_receipts[stage], target,
                                        TARGET_FIELDS, f"{stage} target")
            target_receipts[stage] = target
            source = remainder

        current = _freeze_rows(self._current, "stored current remainder")
        require(type(self._current) is tuple and current == self._current,
                "stored current remainder rows are not canonical")
        require(current == source,
                "stored current remainder does not match the stage chain")

        universe_target = _target_receipt(universe, "residual-universe")
        if self._universe_target_receipt is not None:
            _require_stored_receipt(self._universe_target_receipt, universe_target,
                                    TARGET_FIELDS, "residual-universe target")
        return boundaries, target_receipts, universe_target

    def finite_key_accounting(self, *, require_complete: bool = True) -> dict[str, Json]:
        """Return finite accounting, explicitly making no analytic owner claim."""
        boundaries, target_receipts, universe_target = \
            self._recompute_and_validate_receipts()
        if require_complete:
            require(not self._current,
                    "finite-key accounting has an unowned final remainder")
        complete = (not self._current and
                    len(target_receipts) == len(self._stages) and
                    sum(boundary["owner_row_total"] for boundary in boundaries) ==
                    len(self._universe))
        # Cache only exact recomputations, and only after all pre-existing
        # mutable receipts have survived exact comparison.
        self._target_receipts = deepcopy(target_receipts)
        self._universe_target_receipt = deepcopy(universe_target)
        accounting = {
            "schema": ACCOUNTING_SCHEMA,
            "source_row_total": len(self._universe),
            "source_physical_total": _physical_mass(self._universe),
            "source_key_sha256": _row_digest(self._universe),
            "source_index_sha256": _index_digest(self._universe),
            "stage_order": list(self._stages),
            "stage_boundaries": deepcopy(boundaries),
            "lane_target_contracts": deepcopy(target_receipts),
            "universe_target_contract": deepcopy(universe_target),
            "final_remainder_row_total": len(self._current),
            "final_remainder_physical_total": _physical_mass(self._current),
            "finite_key_accounting_complete": complete,
            "analytic_lane_ownership_established": False,
            "bounded_order_nine_finite_premise_discharged": False,
            "claim_boundary": (
                "exact finite row/target identities only; lane implications and analytic "
                "dependencies are not established by StageLedger"
            ),
        }
        if require_complete:
            require(complete, "finite-key accounting is incomplete")
        return accounting

    def derive_bounded_premise(
            self,
            lane_implications: Mapping[str, Mapping[str, Json]],
            analytic_dependencies: Mapping[str, Mapping[str, Json]],
            *,
            global_analytic_child_claim: bool = False,
    ) -> dict[str, Json]:
        """Derive the bounded finite premise from keys *and* analytic contracts.

        A well-formed registry may carry a false verification/authentication bit;
        the result is then false rather than laundered into success.  Missing,
        extra, malformed, or unbound registry entries fail closed.
        """
        exact_bool(global_analytic_child_claim, "global analytic child claim")
        require(global_analytic_child_claim is False,
                "this bounded composer requires the global analytic child to remain false")
        accounting = self.finite_key_accounting(require_complete=True)
        stage_names = tuple(accounting["stage_order"])
        boundary_by_stage = {
            boundary["stage"]: boundary
            for boundary in accounting["stage_boundaries"]
        }
        target_by_stage = accounting["lane_target_contracts"]
        require(set(boundary_by_stage) == set(stage_names) and
                set(target_by_stage) == set(stage_names),
                "recomputed accounting registry is not exact")
        require(type(lane_implications) is dict and
                set(lane_implications) == set(stage_names),
                "lane implication registry is not exact")
        require(type(analytic_dependencies) is dict and
                set(analytic_dependencies) == set(stage_names),
                "analytic dependency registry is not exact")

        implication_authentication_flags: list[bool] = []
        implication_flags: list[bool] = []
        dependency_flags: list[bool] = []
        lane_kinds: dict[str, str] = {}
        for stage in stage_names:
            target = target_by_stage[stage]
            boundary = boundary_by_stage[stage]
            implication = lane_implications[stage]
            require(type(implication) is dict and set(implication) == IMPLICATION_FIELDS,
                    f"{stage}: lane implication schema changed")
            require(implication["lane"] == stage and type(implication["lane"]) is str,
                    f"{stage}: implication lane identity changed")
            kind = implication["implication_kind"]
            require(type(kind) is str and kind in IMPLICATION_KINDS,
                    f"{stage}: unknown lane implication kind")
            exact_int(implication["row_total"], f"{stage}.implication.row_total")
            exact_int(implication["target_total"], f"{stage}.implication.target_total")
            require(_is_sha256(implication["row_key_sha256"]) and
                    _is_sha256(implication["target_key_sha256"]),
                    f"{stage}: malformed implication digest")
            require(type(implication["target_indices"]) is tuple and
                    implication["target_indices"] == TARGET_INDICES,
                    f"{stage}: implication target-index contract changed")
            require(all(_is_sha256(implication[field]) for field in
                        ("proof_contract_sha256", "verifier_sha256",
                         "verification_output_sha256")),
                    f"{stage}: malformed implication authentication digest")
            authenticated = exact_bool(implication["authenticated"],
                                       f"{stage}.implication.authenticated")
            verified = exact_bool(implication["lane_implication_verified"],
                                  f"{stage}.lane_implication_verified")
            require(implication["row_total"] == boundary["owner_row_total"] and
                    implication["row_key_sha256"] == boundary["owner_key_sha256"] and
                    implication["row_total"] == target["row_total"] and
                    implication["row_key_sha256"] == target["row_key_sha256"] and
                    implication["target_total"] == target["target_total"] and
                    implication["target_key_sha256"] == target["target_key_sha256"],
                    f"{stage}: implication is not bound to exact owner rows/targets")
            implication_authentication_flags.append(authenticated)
            implication_flags.append(verified)
            lane_kinds[stage] = kind

            dependency = analytic_dependencies[stage]
            require(type(dependency) is dict and set(dependency) == DEPENDENCY_FIELDS,
                    f"{stage}: analytic dependency schema changed")
            authenticated = exact_bool(dependency["authenticated"],
                                       f"{stage}.dependency.authenticated")
            digests = dependency["dependency_sha256"]
            require(type(digests) is tuple and bool(digests) and
                    len(set(digests)) == len(digests) and
                    all(_is_sha256(digest) for digest in digests),
                    f"{stage}: malformed analytic dependency digest tuple")
            dependency_flags.append(authenticated)

        implication_contracts_authenticated = all(implication_authentication_flags)
        implications_verified = all(implication_flags)
        dependencies_authenticated = all(dependency_flags)
        bounded = (accounting["finite_key_accounting_complete"] is True and
                   implication_contracts_authenticated and implications_verified and
                   dependencies_authenticated)
        return {
            "schema": PREMISE_SCHEMA,
            "scope": "rank-seven order-nine bounded finite-key premise only",
            "finite_key_accounting_sha256": hashlib.sha256(
                canonical_bytes(accounting)).hexdigest(),
            "universe_row_key_sha256": accounting["source_key_sha256"],
            "universe_target_key_sha256":
                accounting["universe_target_contract"]["target_key_sha256"],
            "target_indices": list(TARGET_INDICES),
            "lane_implication_kinds": lane_kinds,
            "lane_implication_registry_sha256": hashlib.sha256(
                canonical_bytes(lane_implications)).hexdigest(),
            "analytic_dependency_registry_sha256": hashlib.sha256(
                canonical_bytes(analytic_dependencies)).hexdigest(),
            "finite_key_accounting_complete":
                accounting["finite_key_accounting_complete"],
            "lane_implication_contracts_authenticated":
                implication_contracts_authenticated,
            "lane_implications_verified": implications_verified,
            "analytic_dependencies_authenticated": dependencies_authenticated,
            "bounded_order_nine_finite_premise_discharged": bounded,
            "global_analytic_child_claim": False,
            "claim_boundary": (
                "does not establish theorem eligibility or any kernel order outside nine"
            ),
        }


def implication_record(
        ledger: StageLedger,
        stage: str,
        implication_kind: str,
        *,
        proof_contract_sha256: str,
        verifier_sha256: str,
        verification_output_sha256: str,
        authenticated: bool,
        verified: bool,
) -> dict[str, Json]:
    """Build a row/target-bound lane implication authentication record.

    Digests identify the lane-specific mathematical contract, executable
    verifier, and exact verification output.  This helper does not manufacture
    their truth: callers must independently authenticate those bytes and pass
    both exact boolean verdicts.
    """
    require(type(implication_kind) is str and implication_kind in IMPLICATION_KINDS,
            "unknown implication kind")
    require(all(_is_sha256(digest) for digest in
                (proof_contract_sha256, verifier_sha256,
                 verification_output_sha256)),
            "malformed implication authentication digest")
    exact_bool(authenticated, "lane implication authentication verdict")
    exact_bool(verified, "lane implication verification verdict")
    boundary = ledger.boundary(stage)
    target = ledger.stage_target_contract(stage)
    return {
        "lane": stage,
        "implication_kind": implication_kind,
        "row_total": boundary["owner_row_total"],
        "row_key_sha256": boundary["owner_key_sha256"],
        "target_indices": TARGET_INDICES,
        "target_total": target["target_total"],
        "target_key_sha256": target["target_key_sha256"],
        "proof_contract_sha256": proof_contract_sha256,
        "verifier_sha256": verifier_sha256,
        "verification_output_sha256": verification_output_sha256,
        "authenticated": authenticated,
        "lane_implication_verified": verified,
    }
