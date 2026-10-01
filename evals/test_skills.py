#!/usr/bin/env python3
"""
Pytest-compatible test file for CI integration.
Run with: pytest evals/test_skills.py -v
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

def run_eval_suite(suite: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "evals/run.py", f"--suite={suite}"],
        cwd=ROOT,
        capture_output=True,
        text=True
    )

def test_static_evals():
    result = run_eval_suite("static")
    assert result.returncode == 0, f"Static evals failed:\n{result.stdout}\n{result.stderr}"

def test_config_evals():
    result = run_eval_suite("config")
    assert result.returncode == 0, f"Config evals failed:\n{result.stdout}\n{result.stderr}"

def test_description_evals():
    result = run_eval_suite("description")
    assert result.returncode == 0, f"Description evals failed:\n{result.stdout}\n{result.stderr}"

def test_golden_fixtures_exist():
    result = run_eval_suite("golden")
    assert result.returncode == 0, f"Golden fixture check failed:\n{result.stdout}\n{result.stderr}"

if __name__ == "__main__":
    # Allow running directly
    test_static_evals()
    test_config_evals()
    test_description_evals()
    test_golden_fixtures_exist()
    print("All eval tests passed!")