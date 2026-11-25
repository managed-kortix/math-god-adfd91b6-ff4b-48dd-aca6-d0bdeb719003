#!/usr/bin/env python3
"""Exact runtime contract shared by the Cycle 45 census programs."""

import hashlib
import json
from pathlib import Path
import platform
import sys

import flint

HERE = Path(__file__).resolve().parent
ENVIRONMENT_MANIFEST_PATH = HERE / "cycle45-dispersion-environment.json"
REQUIRED_RUNTIME = {
    "python": "3.12.13",
    "python_flint": "0.9.0",
    "flint": "3.6.0",
}


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_environment_manifest():
    try:
        manifest = json.loads(ENVIRONMENT_MANIFEST_PATH.read_text("ascii"))
    except Exception as exc:
        raise RuntimeError(("cannot read environment manifest",
                            str(ENVIRONMENT_MANIFEST_PATH))) from exc
    declared = {
        "python": manifest["python"]["version"],
        "python_flint": manifest["python_packages"]["python-flint"],
        "flint": manifest["native_libraries"]["FLINT"],
    }
    if declared != REQUIRED_RUNTIME:
        raise RuntimeError(("environment manifest/runtime contract mismatch",
                            declared, REQUIRED_RUNTIME))
    return manifest


def observed_runtime():
    return {
        "python": platform.python_version(),
        "python_flint": flint.__version__,
        "flint": flint.__FLINT_VERSION__,
    }


def require_exact_runtime():
    load_environment_manifest()
    observed = observed_runtime()
    if observed != REQUIRED_RUNTIME:
        raise RuntimeError(("wrong certified runtime", observed,
                            REQUIRED_RUNTIME))
    if sys.implementation.name != "cpython":
        raise RuntimeError(("wrong Python implementation",
                            sys.implementation.name, "cpython"))
    return observed
