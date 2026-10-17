
import unittest

from core.response import KernelResponse
from core.engine import KernelEngine


class TestKernelResponse(unittest.TestCase):
    def test_create_response_from_tuple(self):
        result = KernelResponse.from_tuple(
            ("OK", "Stored: project", "Memory saved.")
        )

        self.assertEqual(result.status, "OK")
        self.assertEqual(result.message, "Stored: project")
        self.assertEqual(result.explanation, "Memory saved.")

    def test_response_converts_back_to_tuple(self):
        result = KernelResponse(
            "OK",
            "Ready",
            "Command completed.",
        )

        self.assertEqual(
            result.to_tuple(),
            ("OK", "Ready", "Command completed."),
        )

    def test_response_converts_to_dictionary(self):
        result = KernelResponse(
            "ERROR",
            "Invalid command",
            "Validation failed.",
        )

        self.assertEqual(
            result.to_dict(),
            {
                "status": "ERROR",
                "message": "Invalid command",
                "explanation": "Validation failed.",
            },
        )

    def test_successful_property(self):
        self.assertTrue(
            KernelResponse("OK", "Done", "Complete").successful
        )
        self.assertFalse(
            KernelResponse("ERROR", "Failed", "Invalid").successful
        )

    def test_invalid_tuple_rejected(self):
        with self.assertRaises(ValueError):
            KernelResponse.from_tuple(("OK", "Missing explanation"))

    def test_non_string_fields_rejected(self):
        with self.assertRaises(TypeError):
            KernelResponse.from_tuple(("OK", 123, "Explanation"))

    def test_engine_returns_structured_response(self):
        class FakeMemory:
            def list_keys(self):
                return []

        engine = KernelEngine(FakeMemory())
        result = engine.process_structured("list")

        self.assertIsInstance(result, KernelResponse)
        self.assertEqual(result.status, "OK")
        self.assertEqual(result.message, "Memory is empty.")


if __name__ == "__main__":
    unittest.main()

