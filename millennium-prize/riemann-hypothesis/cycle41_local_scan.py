#!/usr/bin/env python3
"""Parallel exact-Arb scan of local H_n/kappa_n with compact certificates."""

import argparse
import gzip
import hashlib
import json
import multiprocessing as mp
import time
from pathlib import Path

from flint import arb, arb_mat, ctx

from certify_complete_gram import RestrictedGram, mobius_sieve


def contraction_row(task):
    """Compute one new-row Gram contraction using Arb matrix dot products."""
    n, bits, active, u_coeff_text, d_coeff_text = task
    ctx.prec = bits
    gram = RestrictedGram()
    entries = [gram.entry(a, n) for a in active]
    row = arb_mat(1, len(active), entries)
    u_coeff = arb_mat(len(active), 1, [arb(value) for value in u_coeff_text])
    d_coeff = arb_mat(len(active), 1, [arb(value) for value in d_coeff_text])
    row_u = gram.chi_cross(n) + (row * u_coeff)[0, 0]
    row_d = (row * d_coeff)[0, 0]
    return n, row_u.str(80), row_d.str(80), gram.entry(n, n).str(80)


def parallel_contractions(limit, bits, jobs, chunk_size, start=2):
    """Return independent Gram rows, parallelized and ordered by index."""
    mu = mobius_sieve(limit)
    logs = [arb(0)] + [arb(n).log() for n in range(1, limit + 2)]
    targets = [n for n in range(start, limit + 1) if mu[n]]
    tasks = []
    for n in targets:
        active = tuple(a for a in range(1, n) if mu[a])
        tasks.append((
            n,
            bits,
            active,
            tuple(str(mu[a]) for a in active),
            tuple((mu[a] * logs[a]).str(80) for a in active),
        ))
    if jobs == 1:
        results = map(contraction_row, tasks)
    else:
        with mp.Pool(jobs) as pool:
            results = pool.imap_unordered(contraction_row, tasks, chunksize=chunk_size)
            results = list(results)
    rows = {}
    for n, row_u, row_d, diagonal in results:
        rows[n] = (arb(row_u), arb(row_d), arb(diagonal))
    return mu, logs, rows


def load_checkpoint(path, bits):
    if path is None or not path.exists():
        return None
    with path.open(encoding="ascii") as handle:
        data = json.load(handle)
    if data["arb_precision_bits"] != bits:
        raise ValueError("checkpoint precision does not match --bits")
    return {
        "n": data["n"],
        "u2": arb(data["u2"]),
        "ud": arb(data["ud"]),
        "d2": arb(data["d2"]),
        "energy_n": arb(data["energy_n"]),
    }


def write_checkpoint(path, bits, n, u2, ud, d2, energy_n):
    if path is None:
        return
    data = {
        "arb_precision_bits": bits,
        "n": n,
        "u2": u2.str(80),
        "ud": ud.str(80),
        "d2": d2.str(80),
        "energy_n": energy_n.str(80),
    }
    with path.open("w", encoding="ascii") as handle:
        json.dump(data, handle, separators=(",", ":"))
        handle.write("\n")


def scan_values(limit, bits=192, jobs=1, chunk_size=128, checkpoint_path=None):
    """Compute rigorous P_N, H_n, kappa_n, and half-surplus balls."""
    if limit < 3:
        raise ValueError("limit must be at least 3")
    ctx.prec = bits
    mu, logs, rows = parallel_contractions(limit, bits, jobs, chunk_size)
    gram = RestrictedGram()
    u2 = arb(1) + 2 * gram.chi_cross(1) + gram.entry(1, 1)
    ud = arb(0)
    d2 = arb(0)
    energies = {}
    h_values = {}
    for n in range(2, limit + 1):
        log_n = logs[n]
        energies[n] = u2 - 2 * ud / log_n + d2 / log_n ** 2
        if mu[n]:
            row_u, row_d, diagonal = rows[n]
            m = mu[n]
            old_u2, old_ud, old_d2 = u2, ud, d2
            u2 = old_u2 + 2 * m * row_u + diagonal
            ud = (old_ud + m * row_d + m * log_n * row_u
                  + log_n * diagonal)
            d2 = old_d2 + 2 * m * log_n * row_d + log_n ** 2 * diagonal
        h_values[n] = d2 - log_n * logs[n + 1] * u2

    write_checkpoint(checkpoint_path, bits, limit, u2, ud, d2, energies[limit])

    local = []
    prefix = {2: arb(0)}
    total = arb(0)
    for n in range(2, limit):
        weight = 1 - logs[n] / logs[n + 1]
        decrement = energies[n] - energies[n + 1]
        surplus = decrement - weight * energies[n]
        kappa = decrement / (2 * weight * energies[n])
        local.append((n, h_values[n], kappa, surplus))
        total += surplus
        prefix[n + 1] = total
    return energies, local, prefix


def scan_extension(limit, checkpoint, bits=192, jobs=1, chunk_size=1,
                   checkpoint_path=None):
    """Continue a certified local scan from a saved post-update state."""
    start = checkpoint["n"]
    if limit <= start:
        raise ValueError("extension limit must exceed checkpoint n")
    ctx.prec = bits
    mu, logs, rows = parallel_contractions(
        limit, bits, jobs, chunk_size, start=start + 1
    )
    u2, ud, d2 = checkpoint["u2"], checkpoint["ud"], checkpoint["d2"]
    energies = {start: checkpoint["energy_n"]}
    h_values = {start: d2 - logs[start] * logs[start + 1] * u2}
    for n in range(start + 1, limit + 1):
        log_n = logs[n]
        energies[n] = u2 - 2 * ud / log_n + d2 / log_n ** 2
        if mu[n]:
            row_u, row_d, diagonal = rows[n]
            m = mu[n]
            old_u2, old_ud, old_d2 = u2, ud, d2
            u2 = old_u2 + 2 * m * row_u + diagonal
            ud = (old_ud + m * row_d + m * log_n * row_u
                  + log_n * diagonal)
            d2 = old_d2 + 2 * m * log_n * row_d + log_n ** 2 * diagonal
        h_values[n] = d2 - log_n * logs[n + 1] * u2
    write_checkpoint(checkpoint_path, bits, limit, u2, ud, d2, energies[limit])

    local = []
    for n in range(start, limit):
        weight = 1 - logs[n] / logs[n + 1]
        decrement = energies[n] - energies[n + 1]
        surplus = decrement - weight * energies[n]
        kappa = decrement / (2 * weight * energies[n])
        local.append((n, h_values[n], kappa, surplus))
    return energies, local


def consecutive_runs(indices):
    runs = []
    for value in indices:
        if not runs or value != runs[-1][1] + 1:
            runs.append([value, value])
        else:
            runs[-1][1] = value
    return runs


def certified_witness(rows, field, mode="min"):
    index = {"h": 1, "kappa": 2, "surplus": 3}[field]
    ordered = sorted(rows, key=lambda row: float(row[index].mid()),
                     reverse=(mode == "max"))
    candidate = ordered[0]
    if mode == "min":
        valid = all(candidate[index].upper() < row[index].lower()
                    for row in ordered[1:])
    else:
        valid = all(candidate[index].lower() > row[index].upper()
                    for row in ordered[1:])
    if not valid:
        raise RuntimeError(f"no unique certified {mode}imum for {field}")
    return candidate


def cumulative_scan(local):
    """Linear-time prefix-minimum scan for all cumulative negative starts."""
    limit = local[-1][0] + 1
    prefixes = [arb(0)] * (limit + 1)
    for n, _, _, surplus in local:
        prefixes[n + 1] = prefixes[n] + surplus
    suffix_min = [None] * (limit + 1)
    suffix_stop = [None] * (limit + 1)
    best = prefixes[limit]
    stop = limit
    for b in range(limit, 2, -1):
        if prefixes[b].upper() < best.lower():
            best, stop = prefixes[b], b
        suffix_min[b - 1] = best
        suffix_stop[b - 1] = stop
    rows = []
    for a in range(2, limit):
        rows.append((a, suffix_stop[a], suffix_min[a] - prefixes[a]))
    return rows


def ball_text(value):
    return value.str(50)


def certificate_records(local):
    for n, h_value, kappa, surplus in local:
        yield json.dumps({
            "n": n,
            "H_n": ball_text(h_value),
            "kappa_n": ball_text(kappa),
            "half_surplus": ball_text(surplus),
        }, separators=(",", ":")) + "\n"


def write_certificate(path, local):
    digest = hashlib.sha256()
    with gzip.open(path, "wt", encoding="ascii", newline="") as handle:
        for record in certificate_records(local):
            digest.update(record.encode("ascii"))
            handle.write(record)
    return digest.hexdigest()


def first_recoveries(local, cumulative):
    candidate_starts = {row[0] for row in cumulative if row[2] < 0}
    longest = (0, None, None)
    failures = []
    for start_index, (a, _, _, _) in enumerate(local):
        if a not in candidate_starts:
            continue
        total = arb(0)
        recovery = None
        for n, _, _, surplus in local[start_index:]:
            total += surplus
            if total >= 0:
                recovery = n + 1
                break
        if recovery is None:
            failures.append(a)
        elif recovery - a > longest[0]:
            longest = (recovery - a, a, recovery)
    return longest, failures


def build_summary(limit, bits, jobs, local, cumulative, certificate, sha256):
    negative_h = [row[0] for row in local if row[1] < 0]
    negative_units = [row[0] for row in local if row[3] < 0]
    unresolved_h = [row[0] for row in local if not (row[1] < 0 or row[1] > 0)]
    unresolved_units = [row[0] for row in local if not (row[3] < 0 or row[3] > 0)]
    weakest = certified_witness(local, "kappa")
    strongest = certified_witness(local, "kappa", "max")
    closest = min(local, key=lambda row: abs(float((row[2] - arb(1) / 2).mid())))
    negative_cumulative = [row for row in cumulative if row[2] < 0]
    deepest = min(cumulative, key=lambda row: float(row[2].mid()))
    longest, failures = first_recoveries(local, cumulative)
    last_negative = max(negative_units) if negative_units else None
    tail = [row for row in local if last_negative is None or row[0] > last_negative]
    weakest_tail = certified_witness(tail, "kappa")
    return {
        "scope": "certified finite diagnostic only; no asymptotic theorem or RH claim",
        "max_N": limit,
        "arb_precision_bits": bits,
        "parallel_jobs": jobs,
        "unit_count": len(local),
        "certified_negative_H_count": len(negative_h),
        "certified_negative_H_runs": consecutive_runs(negative_h),
        "H_sign_unresolved_count": len(unresolved_h),
        "certified_negative_unit_count": len(negative_units),
        "certified_negative_unit_runs": consecutive_runs(negative_units),
        "unit_sign_unresolved_count": len(unresolved_units),
        "weakest_local_kappa": {"n": weakest[0], "interval": ball_text(weakest[2])},
        "strongest_local_kappa": {"n": strongest[0], "interval": ball_text(strongest[2])},
        "closest_local_kappa_to_half": {"n": closest[0], "interval": ball_text(closest[2])},
        "last_negative_unit": last_negative,
        "weakest_kappa_after_last_negative": {
            "n": weakest_tail[0], "interval": ball_text(weakest_tail[2])
        },
        "negative_cumulative_start_runs": consecutive_runs(
            [row[0] for row in negative_cumulative]
        ),
        "deepest_cumulative_excursion": {
            "start": deepest[0], "stop": deepest[1], "interval": ball_text(deepest[2])
        },
        "longest_first_recovery": {"length": longest[0], "start": longest[1], "stop": longest[2]},
        "starts_without_recovery_by_boundary": failures,
        "certificate": {
            "path": certificate.name,
            "format": "gzip JSON Lines; one Arb interval row per n",
            "uncompressed_sha256": sha256,
        },
    }


def build_extension_summary(start, limit, bits, jobs, local, certificate, sha256):
    negative_h = [row[0] for row in local if row[1] < 0]
    negative_units = [row[0] for row in local if row[3] < 0]
    unresolved_h = [row[0] for row in local if not (row[1] < 0 or row[1] > 0)]
    unresolved_units = [row[0] for row in local if not (row[3] < 0 or row[3] > 0)]
    weakest = certified_witness(local, "kappa")
    closest = min(local, key=lambda row: abs(float((row[2] - arb(1) / 2).mid())))
    return {
        "scope": "certified finite extension only; no asymptotic theorem or RH claim",
        "local_range": [start, limit - 1],
        "arb_precision_bits": bits,
        "parallel_jobs": jobs,
        "unit_count": len(local),
        "certified_negative_H_count": len(negative_h),
        "certified_negative_H_runs": consecutive_runs(negative_h),
        "H_sign_unresolved_count": len(unresolved_h),
        "certified_negative_unit_count": len(negative_units),
        "certified_negative_unit_runs": consecutive_runs(negative_units),
        "unit_sign_unresolved_count": len(unresolved_units),
        "first_failure_of_local_half_positivity": (
            negative_units[0] if negative_units else None
        ),
        "weakest_local_kappa": {
            "n": weakest[0], "interval": ball_text(weakest[2])
        },
        "closest_local_kappa_to_half": {
            "n": closest[0], "interval": ball_text(closest[2])
        },
        "certificate": {
            "path": certificate.name,
            "format": "gzip JSON Lines; one Arb interval row per n",
            "uncompressed_sha256": sha256,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-N", type=int, default=8192)
    parser.add_argument("--bits", type=int, default=192)
    parser.add_argument("--jobs", type=int, default=max(1, mp.cpu_count() // 2))
    parser.add_argument("--chunk-size", type=int, default=128)
    parser.add_argument("--output-dir", type=Path, default=Path("cycle41-data"))
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--resume-from", type=Path)
    args = parser.parse_args()
    ctx.prec = args.bits
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.resume_from:
        checkpoint = load_checkpoint(args.resume_from, args.bits)
        if checkpoint is None:
            raise FileNotFoundError(args.resume_from)
        _, local = scan_extension(
            args.max_N, checkpoint, args.bits, args.jobs, args.chunk_size,
            args.checkpoint,
        )
    else:
        _, local, _ = scan_values(
            args.max_N, args.bits, args.jobs, args.chunk_size, args.checkpoint
        )
    certificate = args.output_dir / "local-arb-certificate.jsonl.gz"
    sha256 = write_certificate(certificate, local)
    if args.resume_from:
        summary = build_extension_summary(
            checkpoint["n"], args.max_N, args.bits, args.jobs, local,
            certificate, sha256,
        )
    else:
        cumulative = cumulative_scan(local)
        summary = build_summary(
            args.max_N, args.bits, args.jobs, local, cumulative, certificate, sha256
        )
    with (args.output_dir / "summary.json").open("w", encoding="ascii") as handle:
        json.dump(summary, handle, indent=2)
        handle.write("\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
