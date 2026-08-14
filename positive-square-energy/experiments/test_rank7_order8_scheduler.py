#!/usr/bin/env python3

import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path


PATH = Path(__file__).with_name("rank7_order8_scheduler.py")


def load_scheduler():
    spec = importlib.util.spec_from_file_location("rank7_order8_scheduler_test", PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SchedulerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scheduler = load_scheduler()

    def test_claim_rejects_active_and_reclaims_stale_lock(self):
        with tempfile.TemporaryDirectory() as temporary:
            lock = Path(temporary) / "shard.lock"
            lock.write_text(json.dumps({"pid": os.getpid()}) + "\n", encoding="ascii")
            self.assertFalse(self.scheduler.claim(lock, 5000, 6000))
            lock.write_text(json.dumps({"pid": 999999999}) + "\n", encoding="ascii")
            self.assertTrue(self.scheduler.claim(lock, 5000, 6000))

    def test_reserved_lock_transfers_to_worker_token(self):
        with tempfile.TemporaryDirectory() as temporary:
            lock = Path(temporary) / "shard.lock"
            lock.write_text(json.dumps({"pid": os.getpid(), "status": "reserved",
                                        "token": "token"}) + "\n", encoding="ascii")
            self.assertTrue(self.scheduler.claim(lock, 5000, 6000, "token"))
            payload = json.loads(lock.read_text(encoding="ascii"))
            self.assertEqual(payload["status"], "running")
            self.assertEqual(payload["range"], [5000, 6000])

    def test_shard_paths_are_private_and_persistent(self):
        run_directory = Path("run")
        first = self.scheduler.shard_paths(run_directory, 5000, 6000)
        second = self.scheduler.shard_paths(run_directory, 6000, 7000)
        self.assertNotEqual(first["fragments"], second["fragments"])
        self.assertEqual(first["result"], run_directory / "results" /
                         "shard-005000_006000.json")


if __name__ == "__main__":
    unittest.main()
