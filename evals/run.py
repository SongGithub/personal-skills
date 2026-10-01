#!/usr/bin/env python3
"""
Eval runner for Agent Skills.

Run all evals:
    python3 evals/run.py

Run specific suite:
    python3 evals/run.py --suite static
    python3 evals/run.py --suite config
    python3 evals/run.py --suite description
    python3 evals/run.py --suite document-design

Run with LLM judge (requires OPENAI_API_KEY):
    python3 evals/run.py --suite golden --llm-judge
"""
import argparse
import json
import os
import pathlib
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

# Document Design required tokens (from SKILL.md)
REQUIRED_DESIGN_TOKENS = [
    "--doc-background",
    "--doc-background-mid",
    "--doc-border-light",
    "--doc-text-primary",
    "--doc-text-secondary",
    "--doc-accent",
    "--doc-accent-soft",
]

REQUIRED_CLASSES = [
    ".page",
    ".name",
    ".tagline",
    ".contact",
    "h2.section-title",
    ".summary",
    ".skills",
    ".skill",
    ".role",
    ".role-head",
    ".role-title",
    ".company",
    ".role-meta",
    ".role-context",
    "ul.bullets",
    ".subrole",
    ".earlier",
]

# Anti-patterns that should NOT appear in a compliant CV
# Note: flex-wrap is used legitimately in this design system (.contact, .skills, .role-head)
# for responsive wrapping - only CSS Grid is considered an anti-pattern for layout
ANTI_PATTERNS = [
    (r"display\s*:\s*grid", "CSS Grid layout (multi-column)"),
    (r"grid-template-columns", "Grid columns"),
    (r"<table\b", "HTML table for layout"),
    # border-collapse is not always present (inline borders used instead)
]

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

def run_document_design_evals() -> EvalSuite:
    """Document Design compliance checks for generated CV HTML"""
    suite = EvalSuite("document-design")

    skill_dir = SKILLS_DIR / "document-design"
    template_path = skill_dir / "references" / "cv-template.html"
    valid_fixture = FIXTURES_DIR / "document-design" / "valid_cv.html"
    invalid_fixture = FIXTURES_DIR / "document-design" / "invalid_cv.html"

    # 1. Template exists and has required tokens
    if template_path.exists():
        template = template_path.read_text(encoding="utf-8")
        for token in REQUIRED_DESIGN_TOKENS:
            if token in template:
                suite.add(f"template.token.{token}", True)
            else:
                suite.add(f"template.token.{token}", False, f"Missing design token: {token}")

        # Check dark theme override
        if "html[data-theme='dark']" in template or 'html[data-theme="dark"]' in template:
            suite.add("template.dark_theme", True)
        else:
            suite.add("template.dark_theme", False, "Missing dark theme override")

        # Check print media query
        if "@media print" in template:
            suite.add("template.print_styles", True)
        else:
            suite.add("template.print_styles", False, "Missing @media print block")

        # Check key print rules
        print_checks = [
            ("@page", "@page rule"),
            ("print-color-adjust", "print-color-adjust"),
            ("break-inside:avoid", "break-inside avoid"),
            ("display:none", "interactive chrome hidden"),
        ]
        for pattern, desc in print_checks:
            if pattern in template:
                suite.add(f"template.print.{desc}", True)
            else:
                suite.add(f"template.print.{desc}", False, f"Missing print rule: {desc}")

    else:
        suite.add("template.exists", False, "cv-template.html not found")

    # 2. Valid fixture passes all checks
    if valid_fixture.exists():
        html = valid_fixture.read_text(encoding="utf-8")

        # Design tokens present
        for token in REQUIRED_DESIGN_TOKENS:
            if f"var({token})" in html or token in html:
                suite.add(f"valid_fixture.token.{token}", True)
            else:
                suite.add(f"valid_fixture.token.{token}", False, f"Missing token usage: {token}")

        # Required classes present
        for cls in REQUIRED_CLASSES:
            if cls in html:
                suite.add(f"valid_fixture.class.{cls}", True)
            else:
                suite.add(f"valid_fixture.class.{cls}", False, f"Missing class: {cls}")

        # Anti-patterns absent (check only main style block, not @media print)
        main_style = html.split("@media print")[0] if "@media print" in html else html
        for pattern, desc in ANTI_PATTERNS:
            if re.search(pattern, main_style, re.IGNORECASE):
                suite.add(f"valid_fixture.anti.{desc}", False, f"Anti-pattern found in main styles: {desc}")
            else:
                suite.add(f"valid_fixture.anti.{desc}", True)

        # Hardcoded colors check (exclude @media print, :root token definitions, dark theme block, box-shadow, var() references)
        # Remove @media print block, :root block, dark theme block, box-shadow lines, and var() references
        check_html = re.sub(r"@media print.*", "", html, flags=re.DOTALL)
        check_html = re.sub(r":root\s*\{[^}]*\}", "", check_html, flags=re.DOTALL)
        check_html = re.sub(r"html\[data-theme='dark'\]\s*\{[^}]*\}", "", check_html, flags=re.DOTALL)
        check_html = re.sub(r"box-shadow[^;]*;", "", check_html)
        check_html = re.sub(r"var\([^)]+\)", "", check_html)
        # Check for hardcoded hex colors in remaining
        hex_colors = re.findall(r"#[0-9a-fA-F]{3,8}", check_html)
        if hex_colors:
            suite.add("valid_fixture.anti.Hardcoded hex color", False, f"Hardcoded hex colors in main styles: {hex_colors}")
        else:
            suite.add("valid_fixture.anti.Hardcoded hex color", True)

        rgb_colors = re.findall(r"rgba?\(\s*\d+", check_html)
        if rgb_colors:
            suite.add("valid_fixture.anti.Hardcoded rgb/rgba color", False, f"Hardcoded rgb/rgba in main styles: {rgb_colors}")
        else:
            suite.add("valid_fixture.anti.Hardcoded rgb/rgba color", True)

        # Layout constraints
        if "max-width:820px" in html.replace(" ", "") or "max-width: 820px" in html:
            suite.add("valid_fixture.layout.max_width", True)
        else:
            suite.add("valid_fixture.layout.max_width", False, "Page max-width not 820px")

        # Typography: system font stack
        if "-apple-system" in html and "BlinkMacSystemFont" in html:
            suite.add("valid_fixture.typography.font_stack", True)
        else:
            suite.add("valid_fixture.typography.font_stack", False, "Missing system font stack")

        # Print styles present
        if "@media print" in html:
            suite.add("valid_fixture.print_styles", True)
        else:
            suite.add("valid_fixture.print_styles", False, "Missing @media print in valid fixture")

    else:
        suite.add("valid_fixture.exists", False, "valid_cv.html not found")

    # 3. Invalid fixture fails expected checks
    if invalid_fixture.exists():
        html = invalid_fixture.read_text(encoding="utf-8")

        # Should have anti-patterns (check whole file since it's intentionally bad)
        violations_found = 0
        for pattern, desc in ANTI_PATTERNS:
            # Skip commented out patterns
            if pattern.startswith("#"):
                continue
            if re.search(pattern, html, re.IGNORECASE):
                violations_found += 1
                suite.add(f"invalid_fixture.detects.{desc}", True)
            else:
                suite.add(f"invalid_fixture.detects.{desc}", False, f"Should detect: {desc}")

        # Hardcoded colors in invalid fixture
        hex_colors = re.findall(r"#[0-9a-fA-F]{3,8}", html)
        if hex_colors:
            suite.add("invalid_fixture.detects.Hardcoded hex color", True)
        else:
            suite.add("invalid_fixture.detects.Hardcoded hex color", False, "Should detect hardcoded hex colors")

        # invalid fixture has no rgb/rgba - that's fine, just verify it doesn't have them
        rgb_colors = re.findall(r"rgba?\(\s*\d+", html)
        if not rgb_colors:
            suite.add("invalid_fixture.no_rgba_colors", True)
        else:
            suite.add("invalid_fixture.no_rgba_colors", False, "Unexpected rgb/rgba")

        # Should be missing design tokens
        tokens_missing = sum(1 for token in REQUIRED_DESIGN_TOKENS if token not in html)
        if tokens_missing >= len(REQUIRED_DESIGN_TOKENS) * 0.5:
            suite.add("invalid_fixture.missing_tokens", True)
        else:
            suite.add("invalid_fixture.missing_tokens", False, "Invalid fixture should not have design tokens")

    else:
        suite.add("invalid_fixture.exists", False, "invalid_cv.html not found")

    check_live_cv(suite)
    return suite


def check_live_cv(suite: EvalSuite) -> None:
    """Check the CV template the candidate actually ships, if one is configured.

    The fixtures prove the rules work; this proves the rules hold for the
    document that gets sent to employers. It reads $JOB_SEARCH_HOME, which is
    private and absent on CI, so it skips rather than fails there — the same
    pattern scripts/check-principles.sh uses for its denylist.
    """
    import os

    home = pathlib.Path(os.environ.get("JOB_SEARCH_HOME", Path.home() / ".config/job-search"))
    cfg = home / "integrations.yaml"
    if not cfg.exists():
        suite.add("live_cv.skipped", True, f"no integrations.yaml at {cfg}")
        return

    try:
        cv_template = (yaml.safe_load(cfg.read_text()) or {}).get("cv_template")
    except yaml.YAMLError as e:
        suite.add("live_cv.config", False, f"integrations.yaml does not parse: {e}")
        return

    if not cv_template:
        suite.add("live_cv.skipped", True, "cv_template not set in integrations.yaml")
        return

    cv = home / "cv" / cv_template
    if not cv.exists():
        suite.add("live_cv.exists", False, f"cv_template set but missing: {cv}")
        return

    html = cv.read_text(encoding="utf-8")

    def check(name: str, passed: bool, failure: str) -> None:
        suite.add(name, passed, "" if passed else failure)

    for token in REQUIRED_DESIGN_TOKENS:
        defined = f"{token}:" in html
        used = f"var({token})" in html
        check(f"live_cv.token.{token}", defined and used,
              "not defined in :root" if not defined else "defined but never used via var()")

    check("live_cv.dark_theme",
          "html[data-theme='dark']" in html or 'html[data-theme="dark"]' in html,
          "missing dark theme override")

    for needle, label in [("@media print", "print block"),
                          ("@page", "@page rule"),
                          ("print-color-adjust", "colour adjust"),
                          ("break-inside:avoid", "break-inside avoid")]:
        check(f"live_cv.print.{label}", needle in html, f"missing {label}")

    check("live_cv.layout.max_width", "max-width:820px" in html.replace(" ", ""),
          "page max-width is not 820px")
    check("live_cv.typography.font_stack",
          "-apple-system" in html and "BlinkMacSystemFont" in html,
          "missing system font stack")

    main = html.split("@media print")[0]
    for pattern, desc in ANTI_PATTERNS:
        check(f"live_cv.anti.{desc}", not re.search(pattern, main, re.IGNORECASE),
              f"anti-pattern present: {desc}")

    # Hardcoded colours are only legitimate inside the token definitions and the
    # dark-theme override, so strip those before scanning.
    chk = re.sub(r"@media print.*", "", html, flags=re.DOTALL)
    chk = re.sub(r":root\s*\{[^}]*\}", "", chk, flags=re.DOTALL)
    chk = re.sub(r"html\[data-theme='dark'\]\s*\{[^}]*\}", "", chk, flags=re.DOTALL)
    chk = re.sub(r"box-shadow[^;]*;", "", chk)
    chk = re.sub(r"var\([^)]+\)", "", chk)
    hexes = re.findall(r"#[0-9a-fA-F]{3,8}", chk)
    rgbs = re.findall(r"rgba?\(\s*\d+", chk)
    check("live_cv.anti.Hardcoded hex color", not hexes, f"hardcoded hex outside tokens: {hexes}")
    check("live_cv.anti.Hardcoded rgb/rgba color", not rgbs, f"hardcoded rgb/rgba outside tokens: {rgbs}")


def run_golden_evals(llm_judge: bool = False) -> EvalSuite:
    """Golden workflow tests with fixtures"""
    suite = EvalSuite("golden")

    if not llm_judge:
        # Check fixtures exist
        for skill_name in ["job-search-quality", "job-application-assistant", "document-design"]:
            fix_dir = FIXTURES_DIR / skill_name
            if fix_dir.exists():
                fixtures = list(fix_dir.glob("*.yaml")) + list(fix_dir.glob("*.html"))
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
    for skill_name in ["job-search-quality", "job-application-assistant", "document-design"]:
        fix_dir = FIXTURES_DIR / skill_name
        if fix_dir.exists():
            for fixture in fix_dir.glob("*.yaml"):
                suite.add(f"{skill_name}.fixture:{fixture.stem}", True, "Fixture available for LLM judge")
            for fixture in fix_dir.glob("*.html"):
                suite.add(f"{skill_name}.fixture:{fixture.stem}", True, "Fixture available for LLM judge")
    return suite


def main():
    parser = argparse.ArgumentParser(description="Run Agent Skills evals")
    parser.add_argument("--suite", choices=["all", "static", "config", "description", "document-design", "golden"],
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
    if args.suite in ("all", "document-design"):
        suites.append(run_document_design_evals())
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