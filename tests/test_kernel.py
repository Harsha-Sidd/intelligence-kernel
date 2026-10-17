import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import main


class TestIntelligenceKernel(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.memory_file = Path(self.temp_dir.name) / "memory.json"
        self.patcher = patch.object(main, "MEMORY_FILE", self.memory_file)
        self.patcher.start()
        self.memory = {}

    def tearDown(self):
        self.patcher.stop()
        self.temp_dir.cleanup()

    def test_memory_persists_after_reload(self):
        status, response, explanation = main.process(
            "remember creator = Harsha", self.memory
        )
        self.assertEqual(status, "OK")

        reloaded_memory = main.load_memory()
        self.assertEqual(reloaded_memory["creator"]["value"], "Harsha")

    def test_unknown_key(self):
        status, response, explanation = main.process(
            "recall missing_key", self.memory
        )
        self.assertEqual(status, "NOT_FOUND")

    def test_invalid_remember_command(self):
        status, response, explanation = main.process(
            "remember creator", self.memory
        )
        self.assertEqual(status, "ERROR")

    def test_unknown_command(self):
        status, response, explanation = main.process(
            "do something unknown", self.memory
        )
        self.assertEqual(status, "UNKNOWN")

    def test_empty_key_rejected(self):
        status, response, explanation = main.process(
            "remember = value", self.memory
        )
        self.assertEqual(status, "ERROR")


if __name__ == "__main__":
    unittest.main()
