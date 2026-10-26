"""Workflow gates, private storage, resumability, and CLI boundaries."""

import copy
import fcntl
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "skills/stock-analysis/scripts/workflow.py"
spec = importlib.util.spec_from_file_location("workflow", SCRIPT)
workflow = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workflow)


def result(stage="research"):
    today = date.today().isoformat()
    return {
        "stage": stage, "status": "complete", "summary": "Synthetic test result.",
        "sources": [
            {"id": "filing", "url": "https://www.sec.gov/edgar/search/",
             "title": "Synthetic filing fixture", "published_on": today,
             "accessed_on": today, "primary": True},
            {"id": "exchange", "url": "https://www.asx.com.au/",
             "title": "Synthetic exchange fixture", "published_on": today,
             "accessed_on": today, "primary": True},
        ],
        "claims": [{"statement": "Synthetic assertion, not investment evidence.",
                    "kind": "fact", "source_ids": ["filing"]}],
        "options": [], "plan": [], "risks": [], "missing": [],
    }


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.run = Path(self.tmp.name) / "run"
        workflow.create_run(self.run, "TEST", "ASX", "AUD")

    def accept(self, data):
        workflow.accept_result(self.run, data)

    def test_research_can_start_without_risk_profile(self):
        self.assertEqual(workflow.next_stage(workflow.load_state(self.run)), "research")
        self.accept(result())
        with self.assertRaisesRegex(ValueError, "risk.*horizon"):
            workflow.next_stage(workflow.load_state(self.run))

    def test_rejects_skipping_a_stage_without_changing_checkpoint(self):
        before = (self.run / "state.json").read_bytes()
        with self.assertRaisesRegex(ValueError, "Expected research"):
            self.accept(result("risk"))
        self.assertEqual((self.run / "state.json").read_bytes(), before)

    def test_stale_or_unsourced_research_does_not_advance(self):
        for mutation in ["unsourced", "stale", "secondary", "future", "no_date"]:
            data = result()
            if mutation == "unsourced":
                data["claims"][0]["source_ids"] = []
            elif mutation == "secondary":
                for s in data["sources"]:
                    s["primary"] = False
            elif mutation == "future":
                data["sources"][0]["published_on"] = "2999-01-01"
            elif mutation == "no_date":
                data["sources"][0]["accessed_on"] = ""
            else:
                for s in data["sources"]:
                    s["published_on"] = "2000-01-01"
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                self.accept(data)
            self.assertEqual(workflow.load_state(self.run)["completed"], [])

    def test_blocked_response_is_saved_but_does_not_advance(self):
        data = result()
        data.update(status="blocked", missing=["Issuer cannot be identified."])
        self.accept(data)
        state = workflow.load_state(self.run)
        self.assertEqual(state["completed"], [])
        self.assertEqual(state["blocked"]["missing"], data["missing"])

    def test_profile_and_user_selection_gate_execution(self):
        self.accept(result())
        workflow.update_profile(self.run, risk="moderate", horizon="five years")
        data = result("strategies")
        data["options"] = [
            {"id": "no_action", "description": "Wait", "tradeoffs": "Opportunity cost"},
            {"id": "staged", "description": "Stage entry", "tradeoffs": "Market exposure"},
        ]
        self.accept(data)
        with self.assertRaisesRegex(ValueError, "Select an option"):
            workflow.next_stage(workflow.load_state(self.run))
        with self.assertRaisesRegex(ValueError, "Unknown option"):
            workflow.update_profile(self.run, option="invented")
        workflow.update_profile(self.run, option="no_action")
        self.assertEqual(workflow.next_stage(workflow.load_state(self.run)), "execution")

    def test_full_run_survives_reload_and_report_retains_citations(self):
        self.accept(result())
        workflow.update_profile(self.run, risk="moderate", horizon="five years")
        strategies = result("strategies")
        strategies["options"] = [
            {"id": "no_action", "description": "Wait", "tradeoffs": "Opportunity cost"},
            {"id": "staged", "description": "Stage entry", "tradeoffs": "Market exposure"},
        ]
        self.accept(strategies)
        workflow.update_profile(self.run, option="no_action")
        execution = result("execution")
        execution["plan"] = ["Reassess after the next verified issuer filing."]
        self.accept(execution)
        risk = result("risk")
        risk["risks"] = ["Stale evidence; refresh before acting; residual uncertainty remains."]
        self.accept(risk)
        self.assertIsNone(workflow.next_stage(workflow.load_state(self.run)))
        report = workflow.render_report(workflow.load_state(self.run))
        self.assertIn("https://www.sec.gov", report)
        self.assertIn("no_action", report)
        self.assertIn("Reassess", report)
        self.assertIn("residual", report)

    def test_profile_cannot_silently_invalidate_completed_stages(self):
        self.accept(result())
        workflow.update_profile(self.run, risk="moderate", horizon="five years")
        data = result("strategies")
        data["options"] = [
            {"id": "no_action", "description": "Wait", "tradeoffs": "Opportunity cost"},
            {"id": "staged", "description": "Stage entry", "tradeoffs": "Market exposure"},
        ]
        self.accept(data)
        with self.assertRaisesRegex(ValueError, "new run"):
            workflow.update_profile(self.run, risk="aggressive")

    def test_private_state_and_no_overwrite(self):
        self.assertEqual((self.run / "state.json").stat().st_mode & 0o777, 0o600)
        with self.assertRaises(FileExistsError):
            workflow.create_run(self.run, "OTHER", "ASX", "AUD")
        self.assertEqual(workflow.load_state(self.run)["request"]["ticker"], "TEST")

    def test_codex_command_does_not_interpolate_ticker_or_enable_writes(self):
        cmd = workflow.codex_command(self.run, self.run / "result.json", None, True)
        self.assertIn("read-only", cmd)
        self.assertIn("--ignore-user-config", cmd)
        self.assertIn("--output-schema", cmd)
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", cmd)

    def test_result_schema_and_validator_reject_wrong_types(self):
        for key, bad in [("sources", "fake"), ("claims", [{}]), ("summary", 3)]:
            data = copy.deepcopy(result())
            data[key] = bad
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.accept(data)

    def fake_codex(self, payload, mode="ok"):
        """A real subprocess boundary without network, model charges or credentials."""
        binary = Path(self.tmp.name) / "codex"
        binary.write_text(
            f"#!{sys.executable}\n"
            "import json, os, sys\n"
            "from pathlib import Path\n"
            "if sys.argv[1:3] == ['login', 'status']:\n"
            " print('Logged in using ' + ('API key' if os.environ['FAKE_MODE'] == 'api' else 'ChatGPT'))\n"
            " sys.exit(0)\n"
            "assert 'OPENAI_API_KEY' not in os.environ\n"
            "assert 'CODEX_API_KEY' not in os.environ\n"
            "prompt = sys.stdin.read()\n"
            "schema = json.loads(prompt.split('RESULT JSON SCHEMA:\\n')[1].split('\\n\\nRUN DATA')[0])\n"
            "assert 'stage' in schema['required']\n"
            "mode = os.environ['FAKE_MODE']\n"
            "if mode == 'fail': sys.exit(2)\n"
            "output = Path(sys.argv[sys.argv.index('--output-last-message') + 1])\n"
            "output.write_text('invalid json' if mode == 'malformed' else os.environ['FAKE_RESULT'])\n"
        )
        binary.chmod(0o700)
        return patch.dict(os.environ, {
            "PATH": str(binary.parent) + os.pathsep + os.environ['PATH'],
            "FAKE_MODE": mode, "FAKE_RESULT": json.dumps(payload),
            "OPENAI_API_KEY": "synthetic-should-not-be-inherited",
            "CODEX_API_KEY": "synthetic-should-not-be-inherited",
        })

    def test_codex_adapter_accepts_structured_result_through_real_subprocess(self):
        with self.fake_codex(result()):
            workflow.run_codex(self.run, timeout=10)
        self.assertEqual(workflow.load_state(self.run)["completed"], ["research"])

    def test_codex_failures_never_reuse_stale_candidate_or_advance(self):
        (self.run / "research-candidate.json").write_text(json.dumps(result()))
        for mode in ["api", "fail", "malformed"]:
            with self.subTest(mode=mode), self.fake_codex(result(), mode):
                with self.assertRaises(ValueError):
                    workflow.run_codex(self.run, timeout=10)
            self.assertEqual(workflow.load_state(self.run)["completed"], [])

    def test_status_and_next_can_read_checkpoint_while_a_writer_is_running(self):
        with (self.run / ".lock").open("w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            for command in ["status", "next"]:
                proc = subprocess.run(
                    [sys.executable, str(SCRIPT), "--run", str(self.run), command],
                    capture_output=True, text=True, timeout=5,
                )
                self.assertEqual(proc.returncode, 0, proc.stderr)


if __name__ == "__main__":
    unittest.main()
