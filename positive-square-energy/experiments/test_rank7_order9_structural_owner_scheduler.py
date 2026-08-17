#!/usr/bin/env python3

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


PATH = Path(__file__).with_name("rank7_order9_structural_owner_scheduler.py")


def load_scheduler():
    spec = importlib.util.spec_from_file_location("rank7_order9_scheduler_test", PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class StructuralOwnerSchedulerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scheduler = load_scheduler()

    def test_stale_lock_is_removed(self):
        with tempfile.TemporaryDirectory() as temporary:
            lock = Path(temporary) / "chunk.lock"
            lock.write_text('{"pid":999999999}\n', encoding="ascii")
            self.assertFalse(self.scheduler.active_lock(lock))
            self.assertFalse(lock.exists())

    def test_reservation_requires_matching_token(self):
        with tempfile.TemporaryDirectory() as temporary:
            lock = Path(temporary) / "chunk.lock"
            token = self.scheduler.reserve(lock, 3)
            self.assertIsNotNone(token)
            self.assertFalse(self.scheduler.claim(lock, 3, "wrong"))
            self.assertTrue(self.scheduler.claim(lock, 3, token))
            payload = json.loads(lock.read_text(encoding="ascii"))
            self.assertEqual(payload["status"], "running")
            self.assertEqual(payload["chunk_index"], 3)

    def test_chunk_paths_are_independent(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_directory = Path(temporary)
            first = self.scheduler.paths(run_directory, 0)
            second = self.scheduler.paths(run_directory, 1)
            self.assertNotEqual(first["result"], second["result"])
            self.assertEqual(first["name"], "chunk-00")
            self.assertEqual(second["name"], "chunk-01")


if __name__ == "__main__":
    unittest.main()
