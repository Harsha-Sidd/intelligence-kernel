
import json
import tempfile
import unittest
from pathlib import Path

from memory.memory_store import MemoryLoadError, MemoryStore


class TestMemoryRecovery(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.path = Path(self.temp_dir.name) / "memory.json"

    def test_missing_file_starts_with_empty_memory(self):
        store = MemoryStore(self.path)

        self.assertEqual(store.list_keys(), [])
        self.assertFalse(self.path.exists())

    def test_corrupt_json_is_not_silently_replaced(self):
        original = '{"broken": '
        self.path.write_text(original, encoding="utf-8")

        with self.assertRaises(MemoryLoadError):
            MemoryStore(self.path)

        self.assertEqual(
            self.path.read_text(encoding="utf-8"),
            original,
        )

    def test_invalid_top_level_format_is_rejected(self):
        original = json.dumps(["not", "a", "dictionary"])
        self.path.write_text(original, encoding="utf-8")

        with self.assertRaises(MemoryLoadError):
            MemoryStore(self.path)

        self.assertEqual(
            self.path.read_text(encoding="utf-8"),
            original,
        )

    def test_save_creates_backup_of_previous_memory(self):
        store = MemoryStore(self.path)
        store.remember("project", "v0.9")

        previous = self.path.read_bytes()
        store.remember("status", "active")

        backup = self.path.with_suffix(".bak")

        self.assertTrue(backup.exists())
        self.assertEqual(backup.read_bytes(), previous)

        saved = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertIn("project", saved)
        self.assertIn("status", saved)

    def test_malformed_existing_file_is_not_overwritten(self):
        store = MemoryStore(self.path)
        store.remember("project", "original")

        damaged = '{"broken": '
        self.path.write_text(damaged, encoding="utf-8")

        with self.assertRaises(MemoryLoadError):
            store.remember("new_key", "new value")

        self.assertEqual(
            self.path.read_text(encoding="utf-8"),
            damaged,
        )
        self.assertNotIn("new_key", store.data)

    def test_failed_forget_restores_in_memory_entry(self):
        store = MemoryStore(self.path)
        store.remember("project", "original")

        self.path.write_text('{"broken": ', encoding="utf-8")

        with self.assertRaises(MemoryLoadError):
            store.forget("project")

        self.assertEqual(store.recall("project")["value"], "original")

    def test_saved_memory_survives_reload(self):
        store = MemoryStore(self.path)
        store.remember("project", "Intelligence Kernel")

        reloaded = MemoryStore(self.path)

        self.assertEqual(
            reloaded.recall("project")["value"],
            "Intelligence Kernel",
        )


if __name__ == "__main__":
    unittest.main()

