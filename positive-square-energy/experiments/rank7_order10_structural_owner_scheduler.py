#!/usr/bin/env python3
"""Order-ten configuration of the durable per-census-chunk scheduler."""

from __future__ import annotations

import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
CORE_PATH = HERE / "rank7_order9_structural_owner_scheduler.py"


def load_core():
    spec = importlib.util.spec_from_file_location("rank7_order10_owner_scheduler_core",
                                                  CORE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load structural owner scheduler core")
    core = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(core)
    # Workers must re-enter this wrapper so its order-ten configuration survives
    # the subprocess boundary.
    core.__file__ = str(Path(__file__).resolve())
    core.ENGINE = HERE / "rank7_order10_structural_owners.py"
    core.DEFAULT_MANIFEST = HERE / "rank7_order10_exact_residual_census_manifest.json"
    core.DEFAULT_OUTPUT = HERE / "rank7_order10_structural_owner_manifest.json"
    core.RUN_DIRECTORY = HERE / "rank7_order10_structural_owner_scheduler"
    return core


if __name__ == "__main__":
    scheduler = load_core()
    raise SystemExit(scheduler.main())
