import io
import logging
import sys
import unittest

from main.core.infrastructure.logging.python_logger_adapter import PythonLoggerAdapter


class TestPythonLoggerAdapter(unittest.TestCase):
    def setUp(self):
        # Le logger est global : on repart d'un état propre pour que l'ordre des tests ne compte pas
        logging.getLogger("app_logger").handlers.clear()

    def tearDown(self):
        logging.getLogger("app_logger").handlers.clear()

    def test_logs_to_both_a_file_and_stdout(self):
        PythonLoggerAdapter()
        handlers = logging.getLogger("app_logger").handlers

        self.assertTrue(any(isinstance(h, logging.FileHandler) for h in handlers))
        stdout_handlers = [
            h for h in handlers
            if isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler)
        ]
        self.assertEqual(1, len(stdout_handlers))
        self.assertIs(sys.stdout, stdout_handlers[0].stream)

    def test_message_reaches_the_stream(self):
        adapter = PythonLoggerAdapter()
        captured = io.StringIO()
        for handler in logging.getLogger("app_logger").handlers:
            if isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler):
                handler.stream = captured

        adapter.error("Quota exceeded", isbn=9782754801096)

        written = captured.getvalue()
        self.assertIn("Quota exceeded", written)
        self.assertIn("9782754801096", written)
        self.assertIn("ERROR", written)

    def test_no_duplicate_handlers_when_instantiated_twice(self):
        PythonLoggerAdapter()
        count = len(logging.getLogger("app_logger").handlers)
        PythonLoggerAdapter()

        self.assertEqual(count, len(logging.getLogger("app_logger").handlers))


if __name__ == "__main__":
    unittest.main()
