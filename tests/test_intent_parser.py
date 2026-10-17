
import unittest

from core.intent_parser import IntentParser


class TestIntentParser(unittest.TestCase):
    def setUp(self):
        self.parser = IntentParser()

    def test_parse_remember(self):
        intent = self.parser.parse("remember project = Intelligence Kernel")

        self.assertEqual(intent.name, "remember")
        self.assertEqual(
            intent.arguments,
            ("project", "Intelligence Kernel"),
        )
        self.assertIsNone(intent.error)

    def test_parse_update(self):
        intent = self.parser.parse("update project = Version 2")

        self.assertEqual(intent.name, "update")
        self.assertEqual(intent.arguments, ("project", "Version 2"))

    def test_parse_search_preserves_phrase(self):
        intent = self.parser.parse("search Intelligence Kernel")

        self.assertEqual(intent.name, "search")
        self.assertEqual(intent.arguments, ("Intelligence Kernel",))

    def test_command_name_is_case_insensitive(self):
        intent = self.parser.parse("ReCaLl project")

        self.assertEqual(intent.name, "recall")
        self.assertEqual(intent.arguments, ("project",))

    def test_empty_command(self):
        intent = self.parser.parse("   ")

        self.assertEqual(intent.name, "invalid")
        self.assertIsNotNone(intent.error)

    def test_unknown_command(self):
        intent = self.parser.parse("launch rocket")

        self.assertEqual(intent.name, "unknown")

    def test_missing_remember_separator(self):
        intent = self.parser.parse("remember project")

        self.assertEqual(intent.name, "remember")
        self.assertIsNotNone(intent.error)

    def test_empty_key_rejected(self):
        intent = self.parser.parse("remember = value")

        self.assertIsNotNone(intent.error)

    def test_empty_value_rejected(self):
        intent = self.parser.parse("remember project = ")

        self.assertIsNotNone(intent.error)

    def test_argument_rejected_for_list(self):
        intent = self.parser.parse("list extra")

        self.assertEqual(intent.name, "invalid")

    def test_empty_search_rejected(self):
        intent = self.parser.parse("search   ")

        self.assertEqual(intent.name, "search")
        self.assertIsNotNone(intent.error)


if __name__ == "__main__":
    unittest.main()

