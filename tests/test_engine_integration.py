
import unittest

from core.engine import KernelEngine


class FakeMemory:
    """In-memory test double; does not touch the real memory file."""

    def __init__(self):
        self.data = {}

    def remember(self, key, value):
        self.data[key] = value

    def recall(self, key):
        if key not in self.data:
            return None
        return {"value": self.data[key]}

    def update(self, key, value):
        if key not in self.data:
            return False
        self.data[key] = value
        return True

    def forget(self, key):
        return self.data.pop(key, None) is not None

    def search(self, query):
        query = query.casefold()
        return [
            key
            for key, value in self.data.items()
            if query in key.casefold() or query in value.casefold()
        ]

    def list_keys(self):
        return list(self.data.keys())


class TestEngineIntegration(unittest.TestCase):
    def setUp(self):
        self.memory = FakeMemory()
        self.engine = KernelEngine(self.memory)

    def test_unknown_command_returns_unknown(self):
        status, _, _ = self.engine.process("dance")

        self.assertEqual(status, "UNKNOWN")

    def test_invalid_command_does_not_change_memory(self):
        self.memory.remember("city", "Hyderabad")

        status, _, _ = self.engine.process("remember city")

        self.assertEqual(status, "ERROR")
        self.assertEqual(self.memory.recall("city")["value"], "Hyderabad")
        self.assertEqual(len(self.memory.data), 1)

    def test_pending_deletion_blocks_unrelated_command(self):
        self.memory.remember("temporary", "value")

        status, _, _ = self.engine.process("forget temporary")
        self.assertEqual(status, "CONFIRMATION_REQUIRED")

        status, _, _ = self.engine.process("remember another = value")

        self.assertEqual(status, "CONFIRMATION_REQUIRED")
        self.assertIsNone(self.memory.recall("another"))
        self.assertIsNotNone(self.memory.recall("temporary"))

    def test_cancelled_deletion_preserves_memory(self):
        self.memory.remember("temporary", "value")
        self.engine.process("forget temporary")

        status, _, _ = self.engine.process("cancel")

        self.assertEqual(status, "OK")
        self.assertIsNotNone(self.memory.recall("temporary"))
        self.assertIsNone(self.engine.pending_forget)

    def test_confirmed_deletion_removes_memory(self):
        self.memory.remember("temporary", "value")
        self.engine.process("forget temporary")

        status, _, _ = self.engine.process("confirm")

        self.assertEqual(status, "OK")
        self.assertIsNone(self.memory.recall("temporary"))
        self.assertIsNone(self.engine.pending_forget)


if __name__ == "__main__":
    unittest.main()

