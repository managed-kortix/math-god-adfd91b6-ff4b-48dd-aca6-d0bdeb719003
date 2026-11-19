#!/usr/bin/env python3
"""Exhaustive reconstruction and hostile mutations for clean-sink streams."""

import tempfile
from pathlib import Path

import check_m6_clean_sink_manifest as checker
import m6_clean_sink_manifest as producer

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "m6-clean-sink-manifest.tsv"
ELIMINATED = HERE / "m6-clean-sink-eliminated.tsv"
REMAINING = HERE / "m6-clean-sink-remaining.tsv"
COVER = HERE / "m6-placement-cover.txt"
FILTER = HERE / "m6-placement-filter.txt"


def reject(action, label):
    try:
        action()
    except (RuntimeError, UnicodeError, ValueError):
        return
    raise RuntimeError(f"hostile mutation accepted: {label}")


rows = checker.read_cover(COVER)
statuses = checker.read_acceptance(FILTER)
independent = checker.derive(rows, statuses)
produced = producer.partition(producer.residual.load_partition(COVER, FILTER))
for name in ("eliminated", "remaining"):
    if produced[name] != independent[name]:
        raise RuntimeError(f"producer and independent {name} streams differ")

summary = checker.counts(independent)
if summary[0] != ("ALL", 34810, 46164, 80974, 17084, 18862, 35946,
                  17084, 18862, 0):
    raise RuntimeError(f"membership/parent summary changed: {summary[0]}")
if summary[1][1:4] != (11072, 8839, 19911) or summary[2][1:4] != (23738, 37325, 61063):
    raise RuntimeError("branch membership subtotals changed")
print("PASS exhaustive 80974-membership reconstruction; memberships remain distinct from parents")

checker.check(MANIFEST, ELIMINATED, REMAINING, COVER, FILTER)

with tempfile.TemporaryDirectory(prefix="m6-clean-sink-", dir=HERE) as directory:
    directory = Path(directory)

    generated_manifest = directory / MANIFEST.name
    generated_eliminated = directory / ELIMINATED.name
    generated_remaining = directory / REMAINING.name
    old = (producer.MANIFEST_IDENTITY, producer.ELIMINATED_IDENTITY, producer.REMAINING_IDENTITY)
    producer.main  # Keep the public entry point import-covered.
    groups = producer.residual.load_partition(COVER, FILTER)
    streams = producer.partition(groups)
    payloads = {name: producer.stream_payload(name, records) for name, records in streams.items()}
    generated_manifest.write_bytes(producer.manifest_payload(streams, payloads))
    generated_eliminated.write_bytes(payloads["eliminated"])
    generated_remaining.write_bytes(payloads["remaining"])
    if (generated_manifest.read_bytes(), generated_eliminated.read_bytes(), generated_remaining.read_bytes()) != (
            MANIFEST.read_bytes(), ELIMINATED.read_bytes(), REMAINING.read_bytes()):
        raise RuntimeError("producer regeneration differs from frozen files")

    def mutate(source, name, transform):
        target = directory / name
        target.write_bytes(transform(source.read_bytes()))
        return target

    bad_manifest = mutate(MANIFEST, "bad-manifest.tsv", lambda data: data.replace(
        b"count\tALL\t34810", b"count\tALL\t34811", 1))
    reject(lambda: checker.check(bad_manifest, ELIMINATED, REMAINING, COVER, FILTER),
           "manifest count")

    bad_eliminated = mutate(ELIMINATED, "bad-eliminated.tsv", lambda data: data.replace(
        b"\teliminated\n", b"\tremaining\n", 1))
    reject(lambda: checker.check(MANIFEST, bad_eliminated, REMAINING, COVER, FILTER),
           "eliminated stream header")

    bad_remaining = mutate(REMAINING, "bad-remaining.tsv", lambda data: data[:-1])
    reject(lambda: checker.check(MANIFEST, ELIMINATED, bad_remaining, COVER, FILTER),
           "truncated remaining stream")

    moved = mutate(ELIMINATED, "moved-membership.tsv", lambda data: data.replace(
        b"B6-l4-r0-t2", b"B6-l4-r1-t3", 1))
    reject(lambda: checker.check(MANIFEST, moved, REMAINING, COVER, FILTER),
           "membership moved between groups")

    duplicate = mutate(ELIMINATED, "duplicate-membership.tsv", lambda data: data + data.splitlines(True)[3])
    reject(lambda: checker.check(MANIFEST, duplicate, REMAINING, COVER, FILTER),
           "duplicate eliminated membership")

    old_source = checker.SOURCE
    checker.SOURCE = mutate(old_source, "bad-source.tsv", lambda data: data + b"\n")
    reject(lambda: checker.check(MANIFEST, ELIMINATED, REMAINING, COVER, FILTER),
           "23-group source identity")
    checker.SOURCE = old_source

    old_theorem = checker.THEOREM
    checker.THEOREM = mutate(old_theorem, "bad-theorem.md", lambda data: data + b"\n")
    reject(lambda: checker.check(MANIFEST, ELIMINATED, REMAINING, COVER, FILTER),
           "theorem identity")
    checker.THEOREM = old_theorem

print("PASS manifest/stream/group/duplicate/source/theorem hostile mutations")
print("PASS m6 rooted clean-sink manifest tests")
clean = ((0, 1, 0),)
unclean = ((1, 1, 0),)
assert producer.universally_clean((clean,))
assert not producer.universally_clean((clean, unclean))
assert not producer.universally_clean((unclean,))
print("PASS universal clean-sink quantifier rejects mixed realizations")
