#!/usr/bin/env python3
"""Execute the frozen Cycle 273 ND270 P3 numerical lead."""

import argparse
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import tempfile
import time

THREAD_NAMES = (
    "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"
)
for _name in THREAD_NAMES:
    os.environ[_name] = "2"


class FrozenFailure(RuntimeError):
    pass


def canonical_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("ascii")


def atomic_write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=path.name + ".", delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(canonical_bytes(value))
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def fraction(value):
    return Fraction(str(value))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_durable_integrity(manifest_path):
    root = manifest_path.parent
    amendment_path = manifest_path.with_name("cycle273-nd270-p3-amendment.json")
    amendment = json.loads(amendment_path.read_text(encoding="ascii"))
    frozen = amendment["frozen_manifest"]
    checks = {
        "frozen_manifest": (
            frozen["file"] == manifest_path.name
            and digest(manifest_path) == frozen["sha256"]
        ),
    }
    actual_digests = {manifest_path.name: digest(manifest_path)}
    for section in ("frozen_dependencies", "recovered_frozen_objects", "superseding_objects"):
        for record in amendment[section]:
            path = root / record["file"]
            actual = digest(path) if path.is_file() else None
            actual_digests[record["file"]] = actual
            checks[f"{section}:{record['file']}"] = actual == record["sha256"]

    analytic = amendment["independent_analytic_rejection"]
    source_path = root / analytic["source"]
    source_actual = digest(source_path) if source_path.is_file() else None
    actual_digests[analytic["source"]] = source_actual
    checks[f"analytic_source:{analytic['source']}"] = source_actual == analytic["source_sha256"]

    manifest = json.loads(manifest_path.read_text(encoding="ascii"))
    recovered = amendment["recovered_frozen_objects"][0]
    checks["manifest_admission_pin_matches_recovery"] = (
        manifest["singleton"]["admission_certificate_sha256"] == recovered["sha256"]
    )
    dependency_digests = {row["file"]: row["sha256"] for row in amendment["frozen_dependencies"]}
    source_bindings = {
        "admission_audit_sha256": "cycle-272-p3-finite-support-admission-audit.md",
        "full_euler_interface_sha256": "cycle-265-genuine-3d-euler-pivot-architecture.md",
        "midpoint_picard_interface_sha256": "cycle-264-midpoint-tail-picard-interface.md",
    }
    for field, filename in source_bindings.items():
        checks[f"manifest_source_pin:{field}"] = (
            manifest["source_digests"][field] == dependency_digests[filename]
        )
    return amendment, manifest, {
        "checks": checks,
        "actual_sha256": actual_digests,
        "passed": all(checks.values()),
    }


def analytic_rejection(amendment, manifest, root):
    cap = amendment["independent_analytic_rejection"]
    source = json.loads((root / cap["source"]).read_text(encoding="ascii"))
    source_cap = source["factor_two_audit"]
    displacement = fraction(cap["L3_norm_displacement_at_T"])
    initial_lower = Fraction(cap["initial_L3_norm_lower_bound"])
    relative = fraction(cap["relative_displacement_bound"])
    log_bound = fraction(cap["absolute_log_ratio_upper_bound"])
    exact_gates = {
        "source_displacement": source_cap["L3_norm_displacement_at_T"] == cap["L3_norm_displacement_at_T"],
        "source_relative_bound": source_cap["relative_displacement_bound"] == cap["relative_displacement_bound"],
        "source_log_bound": source_cap["absolute_log_change_upper_bound"] == cap["absolute_log_ratio_upper_bound"],
        "relative_displacement_identity": displacement / initial_lower == relative,
        "log_ratio_below_two_thirds": log_bound < Fraction(2, 3),
        "source_excludes_factor_two": source_cap["factor_two_excluded_on_frozen_interval"] is True,
        "threshold_exceeds_two": fraction(manifest["promotion"]["threshold"]) > 2,
        "trajectory_disposition_reject": cap["disposition"] == "reject without trajectory",
    }
    return {"exact_gates": exact_gates, "passed": all(exact_gates.values())}


def available_memory_mib():
    for line in Path("/proc/meminfo").read_text(encoding="ascii").splitlines():
        if line.startswith("MemAvailable:"):
            return int(line.split()[1]) // 1024
    raise FrozenFailure("cannot determine available memory")


def preflight(manifest, root):
    resources = manifest["resources"]
    singleton = manifest["singleton"]
    datum_digest = digest(root / singleton["file"])
    certificate_digest = digest(root / singleton["admission_certificate"])
    q0 = fraction(manifest["analytic_tail"]["q0"])
    mass = fraction(manifest["analytic_tail"]["initial_Aq_upper"])
    bound = Fraction(manifest["analytic_tail"]["M"])
    alpha = Fraction(manifest["analytic_tail"]["alpha"])
    final_time = fraction(manifest["time"]["T"])
    q_final = q0 * (1 - alpha * final_time)
    result = {
        "logical_cores": os.cpu_count() or 0,
        "available_memory_mib": available_memory_mib(),
        "thread_environment": {name: os.environ.get(name) for name in THREAD_NAMES},
        "datum_sha256": datum_digest,
        "admission_certificate_sha256": certificate_digest,
        "analytic_tail_gates": {
            "initial_Aq": mass <= fraction("91652781/163840") < bound,
            "alpha": alpha >= bound,
            "q_T": q_final == fraction(manifest["analytic_tail"]["q_T"]) and q_final > 1,
        },
    }
    result["logical_cores_pass"] = result["logical_cores"] >= resources["maximum_cores"]
    result["available_memory_pass"] = (
        result["available_memory_mib"] >= resources["maximum_resident_memory_mib"]
    )
    result["thread_environment_pass"] = all(value == "2" for value in result["thread_environment"].values())
    result["datum_digest_pass"] = datum_digest == singleton["sha256"]
    result["admission_certificate_digest_pass"] = (
        certificate_digest == singleton["admission_certificate_sha256"]
    )
    result["passed"] = all((
        result["logical_cores_pass"], result["available_memory_pass"],
        result["thread_environment_pass"], result["datum_digest_pass"],
        result["admission_certificate_digest_pass"],
        all(result["analytic_tail_gates"].values()),
    ))
    return result


def datum_state(solver, datum):
    state = np.zeros((3, solver.width, solver.width, solver.width), dtype=np.complex128)
    for row in datum["modes"]:
        wave = tuple(row["k"])
        amplitude = np.array([float(fraction(value)) for value in row["amplitude"]])
        positive = amplitude / 2 if row["kind"] == "cos" else -0.5j * amplitude
        positive_index = tuple(value + solver.cutoff for value in wave)
        negative_index = tuple(-value + solver.cutoff for value in wave)
        state[(slice(None),) + positive_index] += positive
        state[(slice(None),) + negative_index] += np.conj(positive)
    return state


def rationalize_node(state):
    # Every binary64 value already has denominator dividing 2^80 at this scale.
    return np.ldexp(np.rint(np.ldexp(state.real, 80)), -80) + 1j * np.ldexp(
        np.rint(np.ldexp(state.imag, 80)), -80
    )


def midpoint_step(solver, initial, step_size, residual_gate, maximum_iterations):
    endpoint = initial + step_size * solver.rhs(initial)
    history = []
    for iteration in range(1, maximum_iterations + 1):
        midpoint = (initial + endpoint) / 2
        tangent = solver.rhs(midpoint)
        residual = endpoint - initial - step_size * tangent
        scale = 1 + np.linalg.norm(initial) + step_size * np.linalg.norm(tangent)
        ratio = float(np.linalg.norm(residual) / scale)
        if ratio <= residual_gate:
            endpoint = rationalize_node(endpoint)
            midpoint = (initial + endpoint) / 2
            tangent = solver.rhs(midpoint)
            residual = endpoint - initial - step_size * tangent
            ratio = float(np.linalg.norm(residual) / (
                1 + np.linalg.norm(initial) + step_size * np.linalg.norm(tangent)
            ))
            if ratio > residual_gate:
                raise FrozenFailure("rationalized node fails residual gate")
            energy_change = solver.energy(endpoint) - solver.energy(initial)
            energy_terms = step_size * float(np.real(np.vdot(midpoint, tangent))) + float(
                np.real(np.vdot(midpoint, residual))
            )
            helicity_change = solver.helicity(endpoint) - solver.helicity(initial)
            helicity_terms = step_size * float(np.real(np.vdot(solver.curl(midpoint), tangent)))
            helicity_terms += 0.5 * float(np.real(np.vdot(
                solver.curl(initial) + solver.curl(endpoint), residual
            )))
            return endpoint, {
                "iterations": iteration,
                "residual_ratio": ratio,
                "energy_identity_closure": abs(energy_change - energy_terms),
                "helicity_identity_closure": abs(helicity_change - helicity_terms),
            }
        image = initial + step_size * tangent
        history.append((image.copy(), (image - endpoint).copy()))
        history = history[-4:]
        if len(history) == 1:
            endpoint = image
            continue
        count = len(history)
        gram = np.array([[np.real(np.vdot(a[1], b[1])) for b in history] for a in history])
        system = np.block([[gram, np.ones((count, 1))], [np.ones((1, count)), np.zeros((1, 1))]])
        target = np.zeros(count + 1)
        target[-1] = 1
        try:
            weights = np.linalg.solve(system, target)[:-1]
            endpoint = sum(weight * row[0] for weight, row in zip(weights, history))
        except np.linalg.LinAlgError:
            endpoint = image
    raise FrozenFailure("implicit midpoint solve did not meet residual gate")


def cube_integral(solver, state, grid):
    velocity = solver.physical(state, grid)
    return float(np.mean(np.sum(velocity * velocity, axis=0) ** 1.5))


def endpoint_record(solver, state, initial_cubes, grids):
    cubes = {str(grid): cube_integral(solver, state, grid) for grid in grids}
    ratios = {
        str(grid): float((cubes[str(grid)] / initial_cubes[str(grid)]) ** (1 / 3))
        for grid in grids
    }
    lower_bounds = {
        str(grid): float(np.nextafter((
            np.nextafter(cubes[str(grid)], -np.inf)
            / np.nextafter(initial_cubes[str(grid)], np.inf)
        ) ** (1 / 3), -np.inf))
        for grid in grids
    }
    return {
        "complete_field_l3_cubes": cubes,
        "ratios": ratios,
        "outward_ratio_lower_bounds": lower_bounds,
        "doubled_cubature_ratio_difference": abs(ratios[str(grids[1])] - ratios[str(grids[0])]),
    }


def update_maxima(maxima, diagnostics):
    maxima["iterations_max"] = max(maxima["iterations_max"], diagnostics["iterations"])
    for name, value in diagnostics.items():
        if name != "iterations":
            key = name + "_max"
            maxima[key] = max(maxima.get(key, 0.0), value)


def run_level(level, manifest, datum, started, output, report):
    solver = Galerkin3D(level["cubic_cutoff"])
    state = datum_state(solver, datum)
    grids = level["endpoint_cubature_grids"]
    initial_cubes = {str(grid): cube_integral(solver, state, grid) for grid in grids}
    energy0 = solver.energy(state)
    helicity0 = solver.helicity(state)
    step_size = float(fraction(level["step_size"]))
    residual_gate = float(fraction(manifest["implicit_midpoint"]["residual_ratio_max"]))
    checkpoints = {
        int(fraction(value) / fraction(level["step_size"])): value
        for value in manifest["time"]["checkpoints"]
    }
    maxima = {"iterations_max": 0}
    endpoints = {
        "0": endpoint_record(solver, state, initial_cubes, grids)
    }
    for step in range(1, level["steps"] + 1):
        if time.monotonic() - started > manifest["resources"]["maximum_wall_seconds"]:
            raise FrozenFailure("wall-time limit reached")
        if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 > manifest["resources"]["maximum_resident_memory_mib"]:
            raise FrozenFailure("resident-memory limit reached")
        state, diagnostics = midpoint_step(
            solver, state, step_size, residual_gate,
            manifest["implicit_midpoint"]["maximum_iterations_per_step"],
        )
        update_maxima(maxima, diagnostics)
        if step in checkpoints:
            endpoints[checkpoints[step]] = endpoint_record(solver, state, initial_cubes, grids)
            report["levels"][level["name"]] = {
                "status": "IN_PROGRESS", "completed_steps": step, "endpoints": endpoints
            }
            atomic_write(output, report)
    energy1 = solver.energy(state)
    helicity1 = solver.helicity(state)
    defects = solver.defects(state)
    maxima.update({
        "relative_energy_drift": abs(energy1 / energy0 - 1),
        "energy_scaled_helicity_drift": abs(helicity1 - helicity0) / energy0,
        "divergence_defect": defects["divergence"],
        "reality_defect": defects["reality"],
    })
    gates = manifest["implicit_midpoint"]["gates"]
    local_pass = all((
        maxima["residual_ratio_max"] <= residual_gate,
        maxima["relative_energy_drift"] <= float(fraction(gates["relative_energy_drift_max"])),
        maxima["energy_scaled_helicity_drift"] <= float(fraction(gates["energy_scaled_helicity_drift_max"])),
        maxima["divergence_defect"] <= float(fraction(gates["divergence_defect_max"])),
        maxima["reality_defect"] <= float(fraction(gates["reality_defect_max"])),
        np.isfinite(maxima["energy_identity_closure_max"]),
        np.isfinite(maxima["helicity_identity_closure_max"]),
        all(row["doubled_cubature_ratio_difference"] <= float(
            fraction(gates["doubled_cubature_ratio_difference_max"])
        ) for row in endpoints.values()),
    ))
    return {
        "status": "COMPLETE",
        "cutoff": level["cubic_cutoff"],
        "dealiased_fft_side": solver.side,
        "step_size": level["step_size"],
        "steps": level["steps"],
        "initial_energy": energy0,
        "initial_helicity": helicity0,
        "initial_complete_field_l3_cubes": initial_cubes,
        "maxima": maxima,
        "endpoints": endpoints,
        "all_local_gates_pass": local_pass,
    }


def attempt_full_certificate(manifest_path, numerical_output, report):
    artifact = numerical_output.with_name("cycle273-nd270-p3-full-euler-certificate.json")
    builder = manifest_path.with_name("build_cycle273_full_euler_certificate.py")
    attempt = {
        "format": "ND270-P3-full-euler-certificate-failure-v1",
        "attempt": 1,
        "maximum_attempts": 1,
        "status": "FAILED",
    }
    if not builder.exists():
        attempt["failed_interface"] = "metadata"
        attempt["reason"] = "frozen full-Euler certificate builder is unavailable"
        atomic_write(artifact, attempt)
        return attempt
    completed = subprocess.run(
        [str(builder), "--manifest", str(manifest_path), "--numerical", str(numerical_output),
         "--output", str(artifact)],
        cwd=manifest_path.parent, check=False, timeout=21600,
    )
    attempt["returncode"] = completed.returncode
    attempt["artifact"] = artifact.name
    attempt["status"] = "COMPLETE" if completed.returncode == 0 else "FAILED"
    if completed.returncode != 0:
        attempt["failed_interface"] = "builder"
        attempt["reason"] = "sole certificate process failed"
        if not artifact.exists():
            atomic_write(artifact, attempt)
    return attempt


def execute(manifest_path, output):
    amendment, manifest, integrity = verify_durable_integrity(manifest_path)
    raw = manifest_path.read_bytes()
    root = manifest_path.parent
    report = {
        "format": "ND270-P3-numerical-outcome-v1",
        "manifest_sha256": hashlib.sha256(raw).hexdigest(),
        "amendment_sha256": digest(manifest_path.with_name("cycle273-nd270-p3-amendment.json")),
        "durable_integrity": integrity,
        "levels": {},
        "full_pde_attempted": False,
        "claim": "Bounded manifest execution only; no Euler, Navier-Stokes, or Millennium result.",
    }
    if not integrity["passed"]:
        report.update({
            "status": "BOUNDED_NEGATIVE_PREFLIGHT_INTEGRITY_FAILURE",
            "trajectory_generated": False,
            "numerical_promotion": False,
        })
        atomic_write(output, report)
        return report
    if amendment["record_status"] == "INVALIDATES_COMPUTE_AUTHORIZATION":
        report["analytic_precheck"] = analytic_rejection(amendment, manifest, root)
        report.update({
            "status": (
                "BOUNDED_NEGATIVE_ANALYTIC_CAP"
                if report["analytic_precheck"]["passed"]
                else "BOUNDED_NEGATIVE_PREFLIGHT_INTEGRITY_FAILURE"
            ),
            "trajectory_generated": False,
            "numerical_promotion": False,
        })
        atomic_write(output, report)
        return report
    if manifest["status"] != "FROZEN_BEFORE_TRAJECTORY_COMPUTE":
        raise FrozenFailure("manifest is not frozen")
    report["preflight"] = preflight(manifest, root)
    if not report["preflight"]["passed"]:
        resource_failure = not (
            report["preflight"]["logical_cores_pass"]
            and report["preflight"]["available_memory_pass"]
        )
        report["status"] = (
            "ND270-RESOURCE-WALL" if resource_failure
            else "BOUNDED_NEGATIVE_PREFLIGHT_INTEGRITY_FAILURE"
        )
        atomic_write(output, report)
        return report
    global np, Galerkin3D
    import numpy as np
    from scout_cycle265_3d_alignment import Galerkin3D
    datum = json.loads((root / manifest["singleton"]["file"]).read_text(encoding="ascii"))
    report["status"] = "NUMERICAL_IN_PROGRESS"
    atomic_write(output, report)
    started = time.monotonic()
    try:
        for level in manifest["retained_levels"]:
            report["levels"][level["name"]] = run_level(
                level, manifest, datum, started, output, report
            )
            atomic_write(output, report)
    except FrozenFailure as error:
        report["status"] = "BOUNDED_NEGATIVE_NUMERICAL_FAILURE"
        report["failure"] = str(error)
        atomic_write(output, report)
        return report
    endpoint = manifest["time"]["T"]
    coarse, fine = (level["name"] for level in manifest["retained_levels"])
    coarse_grid = str(manifest["retained_levels"][0]["endpoint_cubature_grids"][0])
    fine_grid = str(manifest["retained_levels"][1]["endpoint_cubature_grids"][0])
    coarse_ratio = report["levels"][coarse]["endpoints"][endpoint]["ratios"][coarse_grid]
    fine_ratio = report["levels"][fine]["endpoints"][endpoint]["ratios"][fine_grid]
    difference = abs(coarse_ratio - fine_ratio)
    cross_pass = difference <= float(fraction(
        manifest["implicit_midpoint"]["gates"]["cross_cutoff_ratio_difference_max"]
    ))
    threshold = float(fraction(manifest["promotion"]["threshold"]))
    promotion = all((
        cross_pass,
        report["levels"][coarse]["all_local_gates_pass"],
        report["levels"][fine]["all_local_gates_pass"],
        report["levels"][coarse]["endpoints"][endpoint]["outward_ratio_lower_bounds"][coarse_grid] > threshold,
        report["levels"][fine]["endpoints"][endpoint]["outward_ratio_lower_bounds"][fine_grid] > threshold,
    ))
    report["cross_cutoff"] = {
        "K4_ratio": coarse_ratio, "K6_ratio": fine_ratio,
        "absolute_difference": difference, "gate_pass": cross_pass,
    }
    report["numerical_promotion"] = promotion
    report["status"] = "NUMERICAL_PROMOTION" if promotion else "BOUNDED_NEGATIVE_NO_PROMOTION"
    atomic_write(output, report)
    if promotion:
        report["full_pde_attempted"] = True
        report["full_pde_attempt"] = attempt_full_certificate(manifest_path, output, report)
        report["status"] = (
            "FULL_PDE_CERTIFICATE_COMPLETE"
            if report["full_pde_attempt"]["status"] == "COMPLETE"
            else "BOUNDED_NEGATIVE_CERTIFICATE_FAILURE"
        )
        atomic_write(output, report)
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = execute(args.manifest, args.output)
    if report["status"] in {
        "ND270-RESOURCE-WALL", "BOUNDED_NEGATIVE_PREFLIGHT_INTEGRITY_FAILURE",
        "BOUNDED_NEGATIVE_NUMERICAL_FAILURE", "BOUNDED_NEGATIVE_CERTIFICATE_FAILURE",
    }:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
