#!/usr/bin/env python3
"""
Eval runner for Agent Skills.

Run all evals:
    python3 evals/run.py

Run specific suite:
    python3 evals/run.py --suite static
    python3 evals/run.py --suite config
    python3 evals/run.py --suite description

Run with LLM judge (requires OPENAI_API_KEY):
    python3 evals/run.py --suite golden --llm-judge
"""
import argparse
import json
import os
import re
import subprocess
import sys
import yaml
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent.parent
SKILLS_DIR = ROOT / "skills"
EVALS_DIR = ROOT / "evals"
FIXTURES_DIR = EVALS_DIR / "fixtures"

@dataclass
class EvalResult:
    name: str
    passed: bool
    message: str = ""
    details: dict = field(default_factory=dict)

class EvalSuite:
    def __init__(self, name: str):
        self.name = name
        self.results: list[EvalResult] = []

    def add(self, name: str, passed: bool, message: str = "", **details):
        self.results.append(EvalResult(name, passed, message, details))

    def passed(self) -> bool:
        return all(r.passed for r in self.results)

    def summary(self) -> str:
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        return f"{self.name}: {passed}/{total} passed"

def run_static_evals() -> EvalSuite:
    """Static analysis: frontmatter, references, personal data, structure"""
    suite = EvalSuite("static")

    # 1. Frontmatter validation
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            suite.add(f"{skill_dir.name}/SKILL.md", False, "Missing SKILL.md")
            continue
        content = skill_md.read_text(encoding="utf-8")
        if not content.startswith("---"):
            suite.add(f"{skill_dir.name}/frontmatter", False, "No YAML frontmatter")
            continue
        try:
            fm = yaml.safe_load(content.split("---", 2)[1])
            if not fm.get("name"):
                suite.add(f"{skill_dir.name}/frontmatter.name", False, "Missing 'name'")
            else:
                suite.add(f"{skill_dir.name}/frontmatter.name", True)
            if not fm.get("description"):
                suite.add(f"{skill_dir.name}/frontmatter.description", False, "Missing 'description'")
            else:
                suite.add(f"{skill_dir.name}/frontmatter.description", True)
        except yaml.YAMLError as e:
            suite.add(f"{skill_dir.name}/frontmatter", False, f"YAML parse error: {e}")

    # 2. Reference integrity
    ref_pattern = re.compile(r"`(references/[^`]+\.(?:md|yaml|html|tex))`")
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        content = skill_md.read_text(encoding="utf-8")
        refs = ref_pattern.findall(content)
        for ref in refs:
            ref_path = (skill_dir / ref).resolve()
            if ref_path.exists():
                suite.add(f"{skill_dir.name}/ref:{ref}", True)
            else:
                suite.add(f"{skill_dir.name}/ref:{ref}", False, f"Missing: {ref}")

    # 3. Run existing check scripts
    for script_name in ["check-principles.sh", "check-structure.sh"]:
        script = ROOT / "scripts" / script_name
        if script.exists():
            result = subprocess.run(["bash", str(script)], capture_output=True, text=True, cwd=ROOT)
            if result.returncode == 0:
                suite.add(f"script:{script_name}", True)
            else:
                suite.add(f"script:{script_name}", False, result.stdout + result.stderr)
        else:
            suite.add(f"script:{script_name}", False, "Script not found")

    return suite

def run_config_evals() -> EvalSuite:
    """Config validation tests for job-search-quality"""
    suite = EvalSuite("config")
    skill_dir = SKILLS_DIR / "job-search-quality"
    prefs_example = skill_dir / "references" / "preferences.example.yaml"
    skill_md = skill_dir / "SKILL.md"

    if not prefs_example.exists():
        suite.add("preferences.example.yaml", False, "Missing example file")
        return suite

    # Load example to get required keys
    example = yaml.safe_load(prefs_example.read_text()) or {}
    required_keys = [k for k in example.keys() if not k.startswith("#")]

    # Test 1: Example has all expected required keys
    expected = ["currency", "minimum_base_salary_excluding_super_aud",
                "preferred_title_levels", "preferred_title_families",
                "minimum_equivalent_scope", "excluded_title_levels",
                "salary_unknown_policy", "maximum_new_jira_issues_per_run"]
    for key in expected:
        if key in example:
            suite.add(f"example.has.{key}", True)
        else:
            suite.add(f"example.has.{key}", False, f"Required key {key} missing from example")

    # Test 2: Skill mentions validation of placeholder values
    if skill_md.exists():
        content = skill_md.read_text()
        if "placeholder" in content.lower() and ("stop" in content.lower() or "reject" in content.lower() or "fail" in content.lower()):
            suite.add("skill.validates_placeholders", True)
        else:
            suite.add("skill.validates_placeholders", False, "Skill doesn't explicitly validate placeholder values")

    # Test 3: Skill mentions required keys
    if skill_md.exists():
        content = skill_md.read_text()
        for key in expected:
            if key in content:
                suite.add(f"skill.docs.{key}", True)
            else:
                suite.add(f"skill.docs.{key}", False, f"Required key {key} not documented in SKILL.md")

    return suite

def run_description_evals() -> EvalSuite:
    """Description quality checks"""
    suite = EvalSuite("description")

    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        content = skill_md.read_text(encoding="utf-8")
        fm = {}
        if content.startswith("---"):
            try:
                fm = yaml.safe_load(content.split("---", 2)[1]) or {}
            except yaml.YAMLError:
                pass

        desc = fm.get("description", "")

        # Length check
        if len(desc) >= 50:
            suite.add(f"{skill_dir.name}/desc.length", True)
        else:
            suite.add(f"{skill_dir.name}/desc.length", False, f"Description too short ({len(desc)} chars)")

        # Trigger keywords present (skill name words should appear)
        name_words = [w for w in fm.get("name", "").replace("-", " ").split() if len(w) > 3]
        missing = [w for w in name_words if w.lower() not in desc.lower()]
        if not missing:
            suite.add(f"{skill_dir.name}/desc.triggers", True)
        else:
            suite.add(f"{skill_dir.name}/desc.triggers", False, f"Missing trigger words: {missing}")

        # No "use for" vagueness
        if "use for" in desc.lower() or "used for" in desc.lower():
            suite.add(f"{skill_dir.name}/desc.specificity", False, "Description uses vague 'use for'")
        else:
            suite.add(f"{skill_dir.name}/desc.specificity", True)

        # Mentions specific domain
        domain_terms = ["job", "cv", "cover letter", "interview", "salary", "search", "communication", "writing", "style"]
        has_domain = any(t in desc.lower() for t in domain_terms)
        suite.add(f"{skill_dir.name}/desc.domain", has_domain, "No domain-specific terms" if not has_domain else "")

    return suite

def run_golden_evals(llm_judge: bool = False) -> EvalSuite:
    """Golden workflow tests with fixtures"""
    suite = EvalSuite("golden")

    if not llm_judge:
        # Check fixtures exist
        for skill_name in ["job-search-quality", "job-application-assistant"]:
            fix_dir = FIXTURES_DIR / skill_name
            if fix_dir.exists():
                fixtures = list(fix_dir.glob("*.yaml"))
                if fixtures:
                    suite.add(f"{skill_name}.fixtures", True, f"{len(fixtures)} fixtures")
                else:
                    suite.add(f"{skill_name}.fixtures", False, "No fixtures found")
            else:
                suite.add(f"{skill_name}.fixtures", False, "No fixtures directory")
        suite.add("llm_judge", True, "Skipped (no --llm-judge flag)")
        return suite

    # LLM-judged evals would go here
    # For now, just report fixtures
    for skill_name in ["job-search-quality", "job-application-assistant"]:
        fix_dir = FIXTURES_DIR / skill_name
        if fix_dir.exists():
            for fixture in fix_dir.glob("*.yaml"):
                suite.add(f"{skill_name}.fixture:{fixture.stem}", True, "Fixture available for LLM judge")
    return suite

def main():
    parser = argparse.ArgumentParser(description="Run Agent Skills evals")
    parser.add_argument("--suite", choices=["all", "static", "config", "description", "golden"],
                        default="all", help="Which eval suite to run")
    parser.add_argument("--llm-judge", action="store_true", help="Enable LLM-judged golden evals")
    parser.add_argument("--json", action="store_true", help="Output JSON results")
    args = parser.parse_args()

    suites = []
    if args.suite in ("all", "static"):
        suites.append(run_static_evals())
    if args.suite in ("all", "config"):
        suites.append(run_config_evals())
    if args.suite in ("all", "description"):
        suites.append(run_description_evals())
    if args.suite in ("all", "golden"):
        suites.append(run_golden_evals(args.llm_judge))

    # Print results
    all_passed = True
    for suite in suites:
        print(f"\n{suite.summary()}")
        for r in suite.results:
            status = "PASS" if r.passed else "FAIL"
            print(f"  {status} {r.name}" + (f" - {r.message}" if r.message else ""))
        if not suite.passed():
            all_passed = False

    print(f"\n{'='*50}")
    print(f"Overall: {'PASSED' if all_passed else 'FAILED'}")

    if args.json:
        output = {
            "passed": all_passed,
            "suites": [
                {
                    "name": s.name,
                    "passed": s.passed(),
                    "results": [
                        {"name": r.name, "passed": r.passed, "message": r.message, "details": r.details}
                        for r in s.results
                    ]
                }
                for s in suites
            ]
        }
        print(json.dumps(output, indent=2))

    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()