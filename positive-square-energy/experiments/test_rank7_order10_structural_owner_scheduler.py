#!/usr/bin/env python3

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


PATH = Path(__file__).with_name("rank7_order10_structural_owner_scheduler.py")


def load_scheduler():
    spec = importlib.util.spec_from_file_location("rank7_order10_scheduler_test", PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.load_core()


class StructuralOwnerSchedulerTest(unittest.TestCase):
    def test_launch_dispatches_worker_through_order_ten_wrapper(self):
        scheduler = load_scheduler()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            manifest = root / "manifest.json"
            run_directory = root / "run"
            manifest.write_text(json.dumps({"chunks": [{}]}) + "\n", encoding="ascii")
            args = mock.Mock(manifest=manifest, run_directory=run_directory)

            with mock.patch.object(scheduler.subprocess, "Popen") as popen:
                popen.return_value.pid = 12345
                self.assertEqual(scheduler.launch(args), 0)

            command = popen.call_args.args[0]
            self.assertEqual(Path(command[2]), PATH.resolve())
            self.assertEqual(command[3], "worker")
            self.assertEqual(scheduler.ENGINE,
                             PATH.with_name("rank7_order10_structural_owners.py"))

    def test_worker_dispatches_order_ten_engine(self):
        scheduler = load_scheduler()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_directory = root / "run"
            scheduler.prepare(run_directory)
            token = scheduler.reserve(scheduler.paths(run_directory, 0)["lock"], 0)
            args = mock.Mock(manifest=root / "manifest.json",
                             run_directory=run_directory, chunk_index=0, token=token)

            def complete(command, **_kwargs):
                output = Path(command[command.index("--output") + 1])
                output.write_text(json.dumps({
                    "chunk_index": 0,
                    "scanned_residual_total": 1,
                    "remainder_orbit_total": 0,
                }) + "\n", encoding="ascii")
                return mock.Mock(returncode=0)

            with mock.patch.object(scheduler.subprocess, "run",
                                   side_effect=complete) as run:
                self.assertEqual(scheduler.worker(args), 0)

            command = run.call_args.args[0]
            self.assertEqual(Path(command[2]),
                             PATH.with_name("rank7_order10_structural_owners.py"))
            self.assertEqual(command[3], "chunk")


if __name__ == "__main__":
    unittest.main()
