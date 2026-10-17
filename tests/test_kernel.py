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

    def test_update_existing_memory(self):
        self.engine.process("remember project = Version 1")

        status, _, _ = self.engine.process("update project = Version 2")

        self.assertEqual(status, "OK")
        self.assertEqual(self.memory.recall("project")["value"], "Version 2")

    def test_update_missing_memory(self):
        status, _, _ = self.engine.process("update missing = value")
        self.assertEqual(status, "NOT_FOUND")

    def test_remember_rejects_duplicate_key(self):
        self.engine.process("remember project = Version 1")

        status, _, _ = self.engine.process("remember project = Version 2")

        self.assertEqual(status, "EXISTS")
        self.assertEqual(self.memory.recall("project")["value"], "Version 1")

    def test_forget_requires_confirmation(self):
        self.engine.process("remember project = Version 1")

        status, _, _ = self.engine.process("forget project")

        self.assertEqual(status, "CONFIRMATION_REQUIRED")
        self.assertIsNotNone(self.memory.recall("project"))

    def test_forget_cancel_preserves_memory(self):
        self.engine.process("remember project = Version 1")
        self.engine.process("forget project")

        status, _, _ = self.engine.process("cancel")

        self.assertEqual(status, "OK")
        self.assertIsNotNone(self.memory.recall("project"))

    def test_forget_confirm_deletes_memory(self):
        self.engine.process("remember project = Version 1")
        self.engine.process("forget project")

        status, _, _ = self.engine.process("confirm")

        self.assertEqual(status, "OK")
        self.assertIsNone(self.memory.recall("project"))

        reloaded = MemoryStore(self.memory_file)
        self.assertIsNone(reloaded.recall("project"))

    def test_search_matches_keys_and_values(self):
        self.engine.process("remember project = Intelligence Kernel")
        self.engine.process("remember hobby = Gardening")

        status, response, _ = self.engine.process("search intelligence")

        self.assertEqual(status, "OK")
        self.assertEqual(response, "project")

        status, response, _ = self.engine.process("search HOBBY")

        self.assertEqual(status, "OK")
        self.assertEqual(response, "hobby")

    def test_search_empty_query(self):
        status, _, _ = self.engine.process("search   ")
        self.assertEqual(status, "ERROR")

    def test_malformed_entry_is_ignored(self):
        self.memory_file.write_text(
            '{"valid": {"value": "hello", "updated_at": "now"}, '
            '"invalid": {"wrong_field": "bad"}}',
            encoding="utf-8",
        )

        reloaded = MemoryStore(self.memory_file)

        self.assertIsNotNone(reloaded.recall("valid"))
        self.assertIsNone(reloaded.recall("invalid"))


if __name__ == "__main__":
    unittest.main()
