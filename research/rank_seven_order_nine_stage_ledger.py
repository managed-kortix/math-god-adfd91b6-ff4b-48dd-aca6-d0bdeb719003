#!/usr/bin/env python3
"""Fail-closed finite-key accounting for rank seven, order nine.

:class:`StageLedger` checks only exact identities between an ordered row
universe and successive owner/remainder boundaries.  It also defines one
versioned target wire encoding:

``[source_index,global_kernel,order_kernel,row,orbit_size,coordinate]\n``

Each target is one compact canonical ASCII JSON line, rows are in source order,
and ``coordinate`` runs through ``0..15`` in increasing order for every row.
Every external wire container, including ``target_indices``, is a JSON list.

This module deliberately separates three things which must not be conflated:

* a boundary receipt says that one supplied source is the exact ordered,
  disjoint union of supplied owner and remainder streams;
* a target *identity* is deterministically generated from authenticated row
  identities and is not evidence that any child emitted those targets;
* an observed-target receipt is created only after an explicit supplied target
  stream has been consumed and exact-matched record by record.

Every state-advancing boundary call and every target-observation call requires
an exact expected semantic receipt.  Generated identities are exposed through
separately named, non-observational methods.  Stored observations are
idempotent and cannot be replaced by generated identities or by a different
observation.

The ledger has no implication/dependency authentication constructor and never
emits a bounded-premise, theorem-eligibility, or global-claim verdict.  It also
does not authenticate the committed 2,835,895-row order-nine universe root;
a release master must exact-match that independently reviewed root and exact
child process receipts before interpreting this generic accounting layer.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any, Iterable, Iterator, Mapping, NamedTuple, Sequence

Json = Any
RowKey = tuple[int, int, int, tuple[int, ...], int]
TargetKey = tuple[int, int, int, tuple[int, ...], int, int]

TARGET_INDICES = tuple(range(16))
TARGET_ENCODING = "rank-seven-order-nine-flat-six-field-target-jsonl-v1"
UNIVERSE_SCOPE = "ledger-universe"
BOUNDARY_SCHEMA = "rank-seven-order-nine-stage-boundary-v2"
TARGET_IDENTITY_SCHEMA = "rank-seven-order-nine-target-identity-v2"
TARGET_OBSERVATION_SCHEMA = "rank-seven-order-nine-target-observation-v1"
ACCOUNTING_SCHEMA = "rank-seven-order-nine-finite-key-accounting-v2"

BOUNDARY_FIELDS = frozenset({
    "schema", "stage", "source_row_total", "source_physical_total",
    "source_key_sha256", "source_index_sha256", "owner_row_total",
    "owner_physical_total", "owner_key_sha256", "owner_index_sha256",
    "owner_target_total", "remainder_row_total", "remainder_physical_total",
    "remainder_key_sha256", "remainder_index_sha256", "ordered_subsequences",
    "exact_disjoint_union", "analytic_ownership_established",
})
TARGET_IDENTITY_FIELDS = frozenset({
    "schema", "scope", "row_total", "row_key_sha256", "target_indices",
    "per_row_target_cardinality", "target_total", "target_key_sha256",
    "encoding", "identity_kind", "observed_target_stream_validated",
    "analytic_ownership_established",
})
TARGET_OBSERVATION_FIELDS = frozenset({
    "schema", "scope", "target_identity_sha256", "row_total",
    "row_key_sha256", "target_indices", "per_row_target_cardinality",
    "target_total", "observed_target_key_sha256", "encoding",
    "evidence_kind", "observed_target_stream_validated",
    "analytic_ownership_established",
})


def require(condition: bool, message: str) -> None:
    """Raise a fail-closed error without relying on optimizable assertions."""
    if not condition:
        raise RuntimeError(message)


def exact_int(value: object, label: str, *, minimum: int = 0) -> int:
    """Return an exact integer, rejecting booleans and numeric lookalikes."""
    require(type(value) is int and value >= minimum, f"{label}: invalid exact integer")
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
    """Encode one compact canonical ASCII JSON line.

    Floats, non-JSON values, non-string object keys, and non-ASCII output are
    rejected.  Tuples are accepted internally but encode as JSON arrays.
    """
    _validate_json(value, "canonical value")
    try:
        encoded = json.dumps(value, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=True, allow_nan=False)
        return (encoded + "\n").encode("ascii")
    except (TypeError, ValueError, UnicodeError) as error:
        raise RuntimeError("cannot encode canonical JSON") from error


def _decode_receipt(data: object, fields: frozenset[str], label: str) -> dict[str, Json]:
    """Decode an internally stored canonical receipt and reject byte drift."""
    require(type(data) is bytes, f"{label}: stored receipt is not immutable bytes")
    try:
        value = json.loads(data.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"{label}: stored receipt is not canonical JSON") from error
    require(type(value) is dict and set(value) == fields,
            f"{label}: stored receipt schema changed")
    require(canonical_bytes(value) == data,
            f"{label}: stored receipt bytes are not canonical")
    return value


def _row_json(key: RowKey) -> list[Json]:
    return [key[0], key[1], key[2], list(key[3]), key[4]]


def canonical_row_key(value: object, label: str = "row key") -> RowKey:
    """Validate and normalize a full five-field row identity."""
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
    # under fabricated indices.  The canonical producer must make this tuple
    # injective; StageLedger checks that invariant rather than assuming it.
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
    return sum(row[4] for row in rows)


def _validate_stage_name(stage: object) -> str:
    require(type(stage) is str and bool(stage) and stage.isascii(),
            "stage must be a nonempty ASCII string")
    require(stage != UNIVERSE_SCOPE, "stage uses reserved universe scope")
    return stage


def _boundary_receipt(stage: str, source_values: Iterable[object],
                      owner_values: Iterable[object],
                      remainder_values: Iterable[object]) -> tuple[
                          dict[str, Json], tuple[RowKey, ...], tuple[RowKey, ...],
                          tuple[RowKey, ...]]:
    """Revalidate a partition and derive its stable semantic receipt."""
    _validate_stage_name(stage)
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


def _target_json(row: RowKey, coordinate: int) -> list[Json]:
    """Return the sole canonical six-field target representation."""
    return [row[0], row[1], row[2], list(row[3]), row[4], coordinate]


def iter_target_keys(rows: Iterable[object]) -> Iterator[TargetKey]:
    """Yield normalized flat six-field targets in canonical row-major order."""
    frozen = _freeze_rows(rows, "target source rows")
    for row in frozen:
        for coordinate in TARGET_INDICES:
            yield row[0], row[1], row[2], row[3], row[4], coordinate


def _canonical_target(value: object, label: str) -> TargetKey:
    require(type(value) in (list, tuple) and len(value) == 6,
            f"{label}: expected a flat six-field target key")
    row = canonical_row_key(value[:5], f"{label}.row_key")
    coordinate = exact_int(value[5], f"{label}.coordinate")
    require(coordinate in TARGET_INDICES, f"{label}: coordinate outside 0..15")
    return row[0], row[1], row[2], row[3], row[4], coordinate


def canonical_target_bytes(value: object, label: str = "target") -> bytes:
    """Validate one target and return its versioned canonical JSONL bytes."""
    target = _canonical_target(value, label)
    row: RowKey = target[0], target[1], target[2], target[3], target[4]
    return canonical_bytes(_target_json(row, target[5]))


def iter_target_jsonl(rows: Iterable[object]) -> Iterator[bytes]:
    """Yield the exact bytes hashed by target identity receipts."""
    for target in iter_target_keys(rows):
        yield canonical_target_bytes(target)


def _target_identity(rows: Sequence[RowKey], scope: str) -> dict[str, Json]:
    require(type(scope) is str and bool(scope) and scope.isascii(),
            "target scope must be a nonempty ASCII string")
    digest = hashlib.sha256()
    target_total = 0
    for line in iter_target_jsonl(rows):
        digest.update(line)
        target_total += 1
    require(target_total == len(rows) * len(TARGET_INDICES),
            f"{scope}: aggregate target cardinality changed")
    receipt = {
        "schema": TARGET_IDENTITY_SCHEMA,
        "scope": scope,
        "row_total": len(rows),
        "row_key_sha256": _row_digest(rows),
        "target_indices": list(TARGET_INDICES),
        "per_row_target_cardinality": len(TARGET_INDICES),
        "target_total": target_total,
        "target_key_sha256": digest.hexdigest(),
        "encoding": TARGET_ENCODING,
        "identity_kind": "generated-deterministic-row-times-coordinate",
        "observed_target_stream_validated": False,
        "analytic_ownership_established": False,
    }
    require(set(receipt) == TARGET_IDENTITY_FIELDS,
            "internal target identity schema changed")
    return receipt


def _observation_from_identity(identity: Mapping[str, Json]) -> dict[str, Json]:
    require(type(identity) is dict and set(identity) == TARGET_IDENTITY_FIELDS,
            "target identity schema changed before observation")
    receipt = {
        "schema": TARGET_OBSERVATION_SCHEMA,
        "scope": identity["scope"],
        "target_identity_sha256": hashlib.sha256(
            canonical_bytes(identity)).hexdigest(),
        "row_total": identity["row_total"],
        "row_key_sha256": identity["row_key_sha256"],
        "target_indices": list(TARGET_INDICES),
        "per_row_target_cardinality": identity["per_row_target_cardinality"],
        "target_total": identity["target_total"],
        "observed_target_key_sha256": identity["target_key_sha256"],
        "encoding": TARGET_ENCODING,
        "evidence_kind": "observed-exact-target-stream",
        "observed_target_stream_validated": True,
        "analytic_ownership_established": False,
    }
    require(set(receipt) == TARGET_OBSERVATION_FIELDS,
            "internal target observation schema changed")
    return receipt


def _observe_target_stream(rows: Sequence[RowKey], scope: str,
                           targets: Iterable[object]) -> dict[str, Json]:
    """Consume and exact-match an externally supplied target stream."""
    identity = _target_identity(rows, scope)
    try:
        supplied = iter(targets)
    except TypeError as error:
        raise RuntimeError(f"{scope}: target stream is not iterable") from error
    observed_digest = hashlib.sha256()
    target_total = 0
    for row_position, row in enumerate(rows):
        for coordinate in TARGET_INDICES:
            expected_target: TargetKey = (
                row[0], row[1], row[2], row[3], row[4], coordinate
            )
            try:
                observed = _canonical_target(
                    next(supplied), f"{scope}.target[{target_total}]"
                )
            except StopIteration as error:
                raise RuntimeError(f"{scope}: target stream ended early") from error
            require(observed == expected_target,
                    f"{scope}: target duplicate, omission, or order change at "
                    f"row {row_position} coordinate {coordinate}")
            observed_digest.update(canonical_target_bytes(observed))
            target_total += 1
    try:
        next(supplied)
    except StopIteration:
        pass
    else:
        raise RuntimeError(f"{scope}: target stream has a surplus record")
    require(target_total == identity["target_total"] and
            observed_digest.hexdigest() == identity["target_key_sha256"],
            f"{scope}: observed target digest changed")
    return _observation_from_identity(identity)


def _validate_expected(receipt: dict[str, Json], expected: Mapping[str, Json] | None,
                       fields: frozenset[str], label: str) -> None:
    """Require an exact external semantic pin; absence never self-blesses."""
    require(expected is not None, f"{label}: immutable expected receipt is required")
    require(type(expected) is dict and set(expected) == fields,
            f"{label}: expected receipt schema changed")
    if "target_indices" in fields:
        require(type(expected["target_indices"]) is list,
                f"{label}: target_indices wire type must be a JSON list")
    # Canonical bytes, rather than Python equality, reject True/1 laundering.
    require(canonical_bytes(expected) == canonical_bytes(receipt),
            f"{label}: exact receipt changed")


def _require_stored_receipt(data: object, recomputed: dict[str, Json],
                            fields: frozenset[str], label: str) -> dict[str, Json]:
    stored = _decode_receipt(data, fields, label)
    require(canonical_bytes(stored) == canonical_bytes(recomputed),
            f"{label}: stored receipt integrity changed")
    return stored


class _StageState(NamedTuple):
    boundary_bytes: bytes
    owners: tuple[RowKey, ...]
    remainder: tuple[RowKey, ...]


class StageLedger:
    """Compose exact ordered owner/remainder boundaries over full row keys."""

    def __init__(self, source_rows: Iterable[object]):
        self._universe = _freeze_rows(source_rows, "source")
        require(bool(self._universe), "source: empty row universe")
        self._current = self._universe
        self._stages: dict[str, _StageState] = {}
        # Values are immutable canonical receipt bytes.  Presence means an
        # explicit stream was consumed; generated identities never write here.
        self._observed_target_receipts: dict[str, bytes] = {}
        self._observed_universe_target_receipt: bytes | None = None

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
        return deepcopy(_decode_receipt(
            self._stages[stage].boundary_bytes, BOUNDARY_FIELDS,
            f"{stage} boundary",
        ))

    def owner_rows(self, stage: str) -> tuple[RowKey, ...]:
        require(type(stage) is str and stage in self._stages, "unknown stage")
        return self._stages[stage].owners

    def advance(self, stage: str, owners: Iterable[object], remainder: Iterable[object],
                *, expected: Mapping[str, Json] | None = None) -> dict[str, Json]:
        """Advance one pinned exact source = owners disjoint-union remainder stage.

        ``expected`` is mandatory.  It must be an independently reviewed stable
        semantic receipt; omitting it is a hard failure.  State changes only
        after both the partition and pin have been checked exactly.
        """
        _validate_stage_name(stage)
        require(stage not in self._stages, f"duplicate stage: {stage}")
        receipt, source_rows, owner_rows, remainder_rows = _boundary_receipt(
            stage, self._current, owners, remainder)
        require(source_rows == self._current,
                f"{stage}: current source rows are not canonical")
        _validate_expected(receipt, expected, BOUNDARY_FIELDS, f"{stage} boundary")

        self._stages[stage] = _StageState(
            canonical_bytes(receipt), owner_rows, remainder_rows
        )
        self._current = remainder_rows
        return deepcopy(receipt)

    def stage_target_identity(self, stage: str) -> dict[str, Json]:
        """Return a generated identity, explicitly not observational evidence.

        In particular, this identity cannot discharge an ``explicit-frontier``
        implication.  Such a lane must present an independently authenticated
        observed target receipt to a release master.  A
        ``uniform-all-descendant`` proof may bind this deterministic digest, but
        only after that separate proof and its isolated execution are
        authenticated outside StageLedger.
        """
        require(type(stage) is str and stage in self._stages, "unknown target stage")
        return _target_identity(self._stages[stage].owners, stage)

    def universe_target_identity(self) -> dict[str, Json]:
        """Return the generated generic ledger-universe target identity."""
        return _target_identity(self._universe, UNIVERSE_SCOPE)

    def observe_stage_targets(
            self, stage: str, targets: Iterable[object], *,
            expected: Mapping[str, Json] | None = None,
    ) -> dict[str, Json]:
        """Consume, pin, and remember one exact stage-owner target stream.

        Replaying the same observation is idempotent.  Any attempt to replace a
        stored observation with different receipt bytes fails before mutation.
        """
        require(type(stage) is str and stage in self._stages, "unknown target stage")
        receipt = _observe_target_stream(self._stages[stage].owners, stage, targets)
        _validate_expected(receipt, expected, TARGET_OBSERVATION_FIELDS,
                           f"{stage} target observation")
        receipt_bytes = canonical_bytes(receipt)
        if stage in self._observed_target_receipts:
            require(self._observed_target_receipts[stage] == receipt_bytes,
                    f"{stage}: observed target receipt cannot be overwritten")
            return deepcopy(receipt)
        self._observed_target_receipts[stage] = receipt_bytes
        return deepcopy(receipt)

    def observe_universe_targets(
            self, targets: Iterable[object], *,
            expected: Mapping[str, Json] | None = None,
    ) -> dict[str, Json]:
        """Consume, pin, and remember the exact generic-universe target stream."""
        receipt = _observe_target_stream(self._universe, UNIVERSE_SCOPE, targets)
        _validate_expected(receipt, expected, TARGET_OBSERVATION_FIELDS,
                           "ledger-universe target observation")
        receipt_bytes = canonical_bytes(receipt)
        if self._observed_universe_target_receipt is not None:
            require(self._observed_universe_target_receipt == receipt_bytes,
                    "ledger-universe observed target receipt cannot be overwritten")
            return deepcopy(receipt)
        self._observed_universe_target_receipt = receipt_bytes
        return deepcopy(receipt)

    def observed_stage_target_receipt(self, stage: str) -> dict[str, Json] | None:
        """Return an existing observation without manufacturing one."""
        require(type(stage) is str and stage in self._stages, "unknown target stage")
        data = self._observed_target_receipts.get(stage)
        if data is None:
            return None
        identity = self.stage_target_identity(stage)
        return deepcopy(_require_stored_receipt(
            data, _observation_from_identity(identity), TARGET_OBSERVATION_FIELDS,
            f"{stage} target observation",
        ))

    def observed_universe_target_receipt(self) -> dict[str, Json] | None:
        """Return an existing universe observation without manufacturing one."""
        if self._observed_universe_target_receipt is None:
            return None
        identity = self.universe_target_identity()
        return deepcopy(_require_stored_receipt(
            self._observed_universe_target_receipt,
            _observation_from_identity(identity), TARGET_OBSERVATION_FIELDS,
            "ledger-universe target observation",
        ))

    def _recompute_and_validate_receipts(self) -> tuple[
            list[dict[str, Json]], dict[str, dict[str, Json]],
            dict[str, dict[str, Json]], dict[str, Json], dict[str, Json] | None]:
        """Recompute identities while preserving and checking observations."""
        require(type(self._stages) is dict, "stored stage registry type changed")
        require(type(self._observed_target_receipts) is dict,
                "stored target-observation registry type changed")
        universe = _freeze_rows(self._universe, "stored source")
        require(type(self._universe) is tuple and universe == self._universe,
                "stored source rows are not canonical")
        require(set(self._observed_target_receipts).issubset(set(self._stages)),
                "stored target observation exists for an unknown stage")

        source = universe
        boundaries: list[dict[str, Json]] = []
        identities: dict[str, dict[str, Json]] = {}
        observations: dict[str, dict[str, Json]] = {}
        for stage, state in self._stages.items():
            require(type(state) is _StageState, f"{stage}: stored stage type changed")
            recomputed, recomputed_source, owners, remainder = _boundary_receipt(
                stage, source, state.owners, state.remainder)
            require(recomputed_source == source,
                    f"{stage}: stored boundary source changed")
            require(type(state.owners) is tuple and owners == state.owners and
                    type(state.remainder) is tuple and remainder == state.remainder,
                    f"{stage}: stored owner/remainder rows are not canonical")
            _require_stored_receipt(state.boundary_bytes, recomputed,
                                    BOUNDARY_FIELDS, f"{stage} boundary")
            boundaries.append(recomputed)

            identity = _target_identity(owners, stage)
            identities[stage] = identity
            if stage in self._observed_target_receipts:
                observations[stage] = _require_stored_receipt(
                    self._observed_target_receipts[stage],
                    _observation_from_identity(identity),
                    TARGET_OBSERVATION_FIELDS,
                    f"{stage} target observation",
                )
            source = remainder

        current = _freeze_rows(self._current, "stored current remainder")
        require(type(self._current) is tuple and current == self._current,
                "stored current remainder rows are not canonical")
        require(current == source,
                "stored current remainder does not match the stage chain")

        universe_identity = _target_identity(universe, UNIVERSE_SCOPE)
        universe_observation = None
        if self._observed_universe_target_receipt is not None:
            universe_observation = _require_stored_receipt(
                self._observed_universe_target_receipt,
                _observation_from_identity(universe_identity),
                TARGET_OBSERVATION_FIELDS,
                "ledger-universe target observation",
            )
        return (boundaries, identities, observations, universe_identity,
                universe_observation)

    def finite_key_accounting(self, *, require_complete: bool = True) -> dict[str, Json]:
        """Return generic finite accounting with no theorem/premise semantics."""
        (boundaries, identities, observations, universe_identity,
         universe_observation) = self._recompute_and_validate_receipts()
        if require_complete:
            require(not self._current,
                    "finite-key accounting has an unowned final remainder")
        complete = (
            not self._current and
            len(identities) == len(self._stages) and
            sum(boundary["owner_row_total"] for boundary in boundaries) ==
            len(self._universe)
        )
        accounting = {
            "schema": ACCOUNTING_SCHEMA,
            "scope": "generic finite-key accounting; order-nine root not authenticated",
            "source_row_total": len(self._universe),
            "source_physical_total": _physical_mass(self._universe),
            "source_key_sha256": _row_digest(self._universe),
            "source_index_sha256": _index_digest(self._universe),
            "stage_order": list(self._stages),
            "stage_boundaries": deepcopy(boundaries),
            "lane_target_identities": deepcopy(identities),
            "observed_lane_target_receipts": deepcopy(observations),
            "universe_target_identity": deepcopy(universe_identity),
            "observed_universe_target_receipt": deepcopy(universe_observation),
            "final_remainder_row_total": len(self._current),
            "final_remainder_physical_total": _physical_mass(self._current),
            "finite_key_accounting_complete": complete,
            "all_stage_target_streams_observed": (
                set(observations) == set(self._stages)
            ),
            "universe_target_stream_observed": universe_observation is not None,
            "order_nine_universe_root_authenticated": False,
            "analytic_lane_ownership_established": False,
            "bounded_order_nine_finite_premise_discharged": False,
            "claim_boundary": (
                "exact generic row/target identities and in-process stream observations "
                "only; no child-process authentication, lane implication, committed "
                "order-nine scope root, analytic dependency, theorem eligibility, or "
                "global claim is established"
            ),
        }
        if require_complete:
            require(complete, "finite-key accounting is incomplete")
        return accounting

    # Intentionally absent: implication_record, dependency authentication, and
    # derive_bounded_premise.  Those verdicts can only be constructed by a
    # release master from exact lane registries and pinned isolated executions.
