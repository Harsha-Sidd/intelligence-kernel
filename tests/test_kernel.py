import tempfile
import unittest
from pathlib import Path

from core.engine import KernelEngine
from memory.memory_store import MemoryStore


class TestIntelligenceKernel(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.memory_file = Path(self.temp_dir.name) / "memory.json"
        self.memory = MemoryStore(self.memory_file)
        self.engine = KernelEngine(self.memory)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_memory_persists_after_reload(self):
        status, _, _ = self.engine.process("remember creator = Harsha")
        self.assertEqual(status, "OK")

        reloaded = MemoryStore(self.memory_file)
        self.assertEqual(reloaded.recall("creator")["value"], "Harsha")

    def test_unknown_key(self):
        status, _, _ = self.engine.process("recall missing_key")
        self.assertEqual(status, "NOT_FOUND")

    def test_invalid_remember_command(self):
        status, _, _ = self.engine.process("remember creator")
        self.assertEqual(status, "ERROR")

    def test_unknown_command(self):
        status, _, _ = self.engine.process("do something unknown")
        self.assertEqual(status, "UNKNOWN")

    def test_empty_key_rejected(self):
        status, _, _ = self.engine.process("remember = value")
        self.assertEqual(status, "ERROR")

    def test_list_memory_keys(self):
        self.engine.process("remember beta = 2")
        self.engine.process("remember alpha = 1")

        status, response, _ = self.engine.process("list")

        self.assertEqual(status, "OK")
        self.assertEqual(response, "alpha, beta")


if __name__ == "__main__":
    unittest.main()
