"""Tests for the Q-lang command-line entry point."""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import q_cli


class CliTests(unittest.TestCase):
    def test_main_prints_each_runtime_result(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "program.q"
            source.write_text("let answer = 42", encoding="utf-8")
            output = io.StringIO()

            with patch("q_cli.run_file", return_value=[42, "done"]) as run_file:
                with contextlib.redirect_stdout(output):
                    exit_code = q_cli.main([str(source)])

        self.assertEqual(exit_code, 0)
        self.assertEqual(output.getvalue(), "42\ndone\n")
        run_file.assert_called_once_with(source)

    def test_main_reports_runtime_error(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "program.q"
            source.write_text("invalid", encoding="utf-8")
            errors = io.StringIO()

            with patch("q_cli.run_file", side_effect=RuntimeError("execution failed")):
                with contextlib.redirect_stderr(errors):
                    exit_code = q_cli.main([str(source)])

        self.assertEqual(exit_code, 1)
        self.assertIn("Q-lang error: execution failed", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
