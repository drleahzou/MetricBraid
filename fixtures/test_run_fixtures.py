"""Offline regressions for evaluation contracts and report preservation."""

import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import check_fixtures
import run_fixtures


class ReportTests(unittest.TestCase):
    def test_missing_parents_are_created(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / "missing" / "nested" / "report.json"
            payload = {"model": None, "runs": []}
            run_fixtures.prepare_report(str(dest), payload)
            self.assertEqual(json.loads(dest.read_text()), payload)

    def test_existing_report_is_preserved_without_model_calls(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / "report.json"
            dest.write_text("existing results\n")
            with patch.object(sys, "argv", ["run_fixtures.py", "--json", str(dest)]), \
                    patch.object(run_fixtures, "run_claude") as call, \
                    contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as error:
                    run_fixtures.main()
                self.assertEqual(error.exception.code, 2)
                call.assert_not_called()
            self.assertEqual(dest.read_text(), "existing results\n")

    def test_unwritable_report_fails_before_model_calls(self):
        with patch.object(sys, "argv", ["run_fixtures.py", "--json", "blocked.json"]), \
                patch.object(run_fixtures, "prepare_report", side_effect=PermissionError), \
                patch.object(run_fixtures, "run_claude") as call, \
                contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                run_fixtures.main()
            self.assertEqual(error.exception.code, 2)
            call.assert_not_called()

    def test_answers_and_failures_are_saved(self):
        answer = {"observations": [], "deduplication": "none",
                  "abstains": True, "competing_preserved": []}
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / "report.json"
            argv = ["run_fixtures.py", "--case", "single-device-setup", "--json", str(dest)]
            with patch.object(sys, "argv", argv), \
                    patch.object(run_fixtures, "run_claude", return_value=(answer, "", 0.1)), \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(run_fixtures.main(), 1)
            row = json.loads(dest.read_text())["runs"][0]["cases"][0]
            self.assertEqual(row["answer"], answer)
            self.assertTrue(any(not a["ok"] for a in row["assertions"]))

    def test_first_spec_survives_later_interruption(self):
        def fake_call(prompt, spec_file, schema, model, timeout):
            if spec_file == run_fixtures.SPEC_SOURCES["plugin"]:
                raise RuntimeError("simulated interruption")
            return None, "simulated CLI error", 0.0

        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / "report.json"
            argv = ["run_fixtures.py", "--spec", "both", "--case",
                    "single-device-setup", "--json", str(dest)]
            with patch.object(sys, "argv", argv), \
                    patch.object(run_fixtures, "run_claude", side_effect=fake_call), \
                    contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaisesRegex(RuntimeError, "simulated interruption"):
                    run_fixtures.main()
            runs = json.loads(dest.read_text())["runs"]
            self.assertEqual(len(runs), 1)
            self.assertEqual(runs[0]["spec"], "repo")
            self.assertEqual(runs[0]["cases"][0]["error"], "simulated CLI error")


class ContractTests(unittest.TestCase):
    def check_mutation(self, directory, change):
        payload = json.loads(run_fixtures.FIXTURES.read_text())
        change(payload["cases"][0]["expect"])
        dest = Path(directory) / "cases.json"
        dest.write_text(json.dumps(payload))
        with patch.object(check_fixtures, "FIXTURES", dest), \
                patch.object(check_fixtures, "errors", []):
            check_fixtures.check_fixtures(check_fixtures.load_enums())
            return list(check_fixtures.errors)

    def test_abstention_must_match_routing_status(self):
        with tempfile.TemporaryDirectory() as directory:
            errors = self.check_mutation(directory, lambda e: e.update(abstains=True))
        self.assertTrue(any("abstains must" in e for e in errors))

    def test_merges_cannot_be_hidden_as_no_collapse(self):
        with tempfile.TemporaryDirectory() as directory:
            errors = self.check_mutation(directory, lambda e: e.update(deduplication="none"))
        self.assertTrue(any("collapse must" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
