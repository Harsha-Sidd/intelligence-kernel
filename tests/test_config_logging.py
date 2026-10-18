
import logging
import tempfile
import unittest
from pathlib import Path

from core.config import APP_NAME, VERSION, ROOT, MEMORY_FILE
from core.logging_setup import configure_logging


class TestConfiguration(unittest.TestCase):
    def test_application_name_is_defined(self):
        self.assertEqual(APP_NAME, "Intelligence Kernel")

    def test_version_is_defined(self):
        self.assertEqual(VERSION, "0.8.0")

    def test_memory_path_is_inside_project(self):
        self.assertEqual(MEMORY_FILE.parent, ROOT / "memory")


class TestLogging(unittest.TestCase):
    def test_logging_creates_file_and_records_event(self):
        with tempfile.TemporaryDirectory() as directory:
            log_file = Path(directory) / "test.log"

            logger = configure_logging(log_file, "INFO")
            try:
                logger.info("Test event")
                for handler in logger.handlers:
                    handler.flush()

                self.assertTrue(log_file.exists())
                content = log_file.read_text(encoding="utf-8")
                self.assertIn("INFO", content)
                self.assertIn("Test event", content)
            finally:
                for handler in logger.handlers[:]:
                    logger.removeHandler(handler)
                    handler.close()

    def test_logging_does_not_duplicate_handlers(self):
        with tempfile.TemporaryDirectory() as directory:
            log_file = Path(directory) / "test.log"

            logger = configure_logging(log_file)
            first_handler_count = len(logger.handlers)

            try:
                configure_logging(log_file)
                self.assertEqual(
                    len(logger.handlers),
                    first_handler_count,
                )
            finally:
                for handler in logger.handlers[:]:
                    logger.removeHandler(handler)
                    handler.close()

    def test_invalid_log_level_falls_back_to_info(self):
        with tempfile.TemporaryDirectory() as directory:
            log_file = Path(directory) / "test.log"

            logger = configure_logging(log_file, "INVALID_LEVEL")
            try:
                self.assertEqual(logger.level, logging.INFO)
            finally:
                for handler in logger.handlers[:]:
                    logger.removeHandler(handler)
                    handler.close()


if __name__ == "__main__":
    unittest.main()

