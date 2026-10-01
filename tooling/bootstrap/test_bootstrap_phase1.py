#!/usr/bin/env python3
"""
Test Suite for AICF Phase 1 Bootstrap & Context Population.

Validates the 8 core acceptance criteria from AICF-004:
1. init creates the template when .aicf/ is absent.
2. init does not overwrite an existing .aicf/.
3. selected artifacts are populated.
4. unselected artifacts are not modified.
5. existing artifact content is preserved appropriately (conservative merge).
6. generated content does not contain machine-specific paths (e.g., D:\\, file:///).
7. generated content does not contain obvious secret values.
8. existing AICF context can be discovered/read for future work (governance & conflict check).
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add project root to sys.path so we can import tooling.bootstrap
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tooling.bootstrap.bootstrap_phase1 import (
    init,
    analyze,
    characterize,
    validate_characterization,
    propose,
    apply,
    read_context,
    check_rule_conflict,
    contains_machine_paths,
    contains_secrets,
    merge_markdown_sections,
    AICFBootstrapError,
    CANONICAL_PHASE1_FILES,
    SELECTABLE_ARTIFACTS,
)


class TestAICFPhase1Bootstrap(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def _characterization(self):
        return {
            "identity": "Sample service", "purpose": "Serves sample requests",
            "languages": ["Python"], "frameworks": ["Flask"], "runtimes": ["Python 3"],
            "package_manager": "pip", "important_dependencies": ["Flask"],
            "build_tooling": ["setuptools"], "testing_tooling": ["unittest"],
            "repository_structure": {"src/": "application code"},
            "development_workflow": ["Run python -m unittest"],
            "engineering_conventions": ["Use type hints"],
            "architectural_boundaries": ["Keep HTTP handlers in src/web.py"],
            "generated_vendor_files": ["Do not edit build/"],
            "agent_constraints": ["Never store credentials"],
            "proposed_artifacts": {
                "project.md": "# Project Context\n\n## Identity & Purpose\n\nSample service handles requests.\n\n## Technology Stack\n\nPython, Flask.\n",
                "rules.md": "# Project Rules\n\n## Coding Conventions\n\n- Use type hints.\n- Use Redux for client state.\n"
            },
            "evidence": [{"finding": "Python application and typed conventions", "paths": ["src/web.py"]}]
        }

    def test_13_characterization_validation_and_evidence_safety(self):
        (self.repo_path / "src").mkdir()
        (self.repo_path / "src" / "web.py").write_text("# handler", encoding="utf-8")
        result = self._characterization()
        validate_characterization(result, self.repo_path)
        for bad_path in ("D:\\repo\\src\\web.py", "file:///tmp/web.py", "/home/user/web.py", "../outside.py"):
            changed = self._characterization()
            changed["evidence"][0]["paths"] = [bad_path]
            with self.assertRaises(AICFBootstrapError, msg=bad_path):
                validate_characterization(changed, self.repo_path)
        missing = self._characterization()
        del missing["agent_constraints"]
        with self.assertRaises(AICFBootstrapError):
            validate_characterization(missing, self.repo_path)
        secret = self._characterization()
        secret["purpose"] = "api_key='abcdef1234567890abcdef'"
        with self.assertRaises(AICFBootstrapError):
            validate_characterization(secret, self.repo_path)

    def test_14_candidates_selection_preservation_and_conflict_surfacing(self):
        (self.repo_path / "src").mkdir()
        (self.repo_path / "src" / "web.py").write_text("# handler", encoding="utf-8")
        init(self.repo_path)
        rules_path = self.repo_path / ".aicf" / "rules.md"
        rules_path.write_text("# My Rules\n\n## Existing\n\n- Do not use Redux.\n", encoding="utf-8")
        result = characterize(self.repo_path, self._characterization())
        self.assertIn("Project Context", result["proposed"]["project.md"])
        self.assertIn("type hints", result["proposed"]["rules.md"])
        self.assertTrue(result["conflicts"])
        applied = apply(self.repo_path, ["project.md"], result["proposed"])
        self.assertEqual(applied["updated"], ["project.md"])
        self.assertEqual(rules_path.read_text(encoding="utf-8"), "# My Rules\n\n## Existing\n\n- Do not use Redux.\n")

    # 1. init creates the template when .aicf/ is absent
    def test_01_init_creates_template_when_aicf_absent(self):
        aicf_dir = self.repo_path / ".aicf"
        self.assertFalse(aicf_dir.exists())

        res = init(self.repo_path)
        self.assertEqual(res["status"], "created")
        self.assertTrue(aicf_dir.exists())
        self.assertTrue(aicf_dir.is_dir())

        for expected_file in CANONICAL_PHASE1_FILES:
            file_path = aicf_dir / expected_file
            self.assertTrue(file_path.is_file(), f"Expected {expected_file} to exist")
            content = file_path.read_text(encoding="utf-8")
            self.assertTrue(len(content.strip()) > 0, f"{expected_file} should not be empty")

    # 2. init does not overwrite an existing .aicf/
    def test_02_init_does_not_overwrite_existing_aicf(self):
        aicf_dir = self.repo_path / ".aicf"
        aicf_dir.mkdir(parents=True)
        custom_rules = aicf_dir / "rules.md"
        custom_rules.write_text("# Custom Existing Rules\n\n- Do not overwrite me!", encoding="utf-8")

        res = init(self.repo_path)
        self.assertEqual(res["status"], "skipped")
        self.assertEqual(res["created"], [])

        # Verify existing content is completely untouched
        content = custom_rules.read_text(encoding="utf-8")
        self.assertEqual(content, "# Custom Existing Rules\n\n- Do not overwrite me!")

    # 3. selected artifacts are populated & 4. unselected artifacts are not modified
    def test_03_and_04_selected_artifacts_populated_unselected_untouched(self):
        # Setup repo files
        (self.repo_path / "package.json").write_text(
            '{"name": "test-app", "scripts": {"build": "tsc", "test": "jest"}, "dependencies": {"react": "^18.0.0"}, "devDependencies": {"typescript": "^5.0.0", "jest": "^29.0.0"}}',
            encoding="utf-8",
        )
        (self.repo_path / "README.md").write_text("# Test App\n\nA modern web application for testing.", encoding="utf-8")

        # 1. Initialize
        init(self.repo_path)

        # Record initial content of unselected artifacts
        aicf_dir = self.repo_path / ".aicf"
        env_original = (aicf_dir / "environment.md").read_text(encoding="utf-8")
        state_original = (aicf_dir / "state.md").read_text(encoding="utf-8")
        readme_original = (aicf_dir / "README.md").read_text(encoding="utf-8")

        # 2. Analyze
        analysis = analyze(self.repo_path)
        proposed = propose(analysis)

        # 3. User selects ONLY rules.md and project.md
        selected = ["rules.md", "project.md"]
        res = apply(self.repo_path, selected, proposed)

        self.assertEqual(set(res["updated"]), {"rules.md", "project.md"})
        self.assertIn("environment.md", res["skipped"])
        self.assertIn("state.md", res["skipped"])

        # Check selected artifacts were populated with analysis content
        rules_content = (aicf_dir / "rules.md").read_text(encoding="utf-8")
        project_content = (aicf_dir / "project.md").read_text(encoding="utf-8")
        self.assertIn("test-app", project_content)
        self.assertIn("A modern web application for testing", project_content)
        self.assertIn("React", project_content)
        self.assertIn("TypeScript", rules_content)

        # Check unselected artifacts remain exactly untouched
        self.assertEqual((aicf_dir / "environment.md").read_text(encoding="utf-8"), env_original)
        self.assertEqual((aicf_dir / "state.md").read_text(encoding="utf-8"), state_original)
        self.assertEqual((aicf_dir / "README.md").read_text(encoding="utf-8"), readme_original)

    # 5. existing artifact content is preserved appropriately (conservative merge)
    def test_05_existing_artifact_content_preserved_conservatively(self):
        init(self.repo_path)
        aicf_dir = self.repo_path / ".aicf"

        # User writes custom rule in Coding Conventions
        custom_content = (
            "# Project Rules\n\n"
            "## Coding Conventions\n\n"
            "- Always use strict typing and never use any.\n"
            "- User custom invariant: never bypass lint.\n\n"
            "## AI Operating Invariants\n\n"
            "- Stop if uncertainty affects correctness.\n"
        )
        (aicf_dir / "rules.md").write_text(custom_content, encoding="utf-8")

        # Create some repo evidence
        (self.repo_path / "pom.xml").write_text(
            "<project><modelVersion>4.0.0</modelVersion><groupId>com.way</groupId><artifactId>service</artifactId></project>",
            encoding="utf-8",
        )

        analysis = analyze(self.repo_path)
        proposed = propose(analysis)

        # Apply without force_overwrite
        res = apply(self.repo_path, ["rules.md"], proposed, force_overwrite=False)
        self.assertIn("rules.md", res["preserved_customizations"])

        # Read back rules.md and verify user content is preserved
        updated_rules = (aicf_dir / "rules.md").read_text(encoding="utf-8")
        self.assertIn("Always use strict typing and never use any.", updated_rules)
        self.assertIn("User custom invariant: never bypass lint.", updated_rules)
        self.assertIn("Stop if uncertainty affects correctness.", updated_rules)

    # 6. generated content does not contain obvious machine-specific paths
    def test_06_generated_content_contains_no_machine_specific_paths(self):
        (self.repo_path / "README.md").write_text("# Local Service\nSample service.", encoding="utf-8")
        analysis = analyze(self.repo_path)
        proposed = propose(analysis)

        for art, text in proposed.items():
            self.assertFalse(
                contains_machine_paths(text),
                f"Artifact {art} must not contain machine paths like D:\\ or file:///: {text}",
            )

        # Directly test path detection utility
        self.assertTrue(contains_machine_paths("Reference path D:\\Work\\project\\src"))
        self.assertTrue(contains_machine_paths("file:///c:/Users/Test/file.txt"))
        self.assertTrue(contains_machine_paths("/home/user/work/repo"))
        self.assertFalse(contains_machine_paths("apps/web/src/components/button.tsx"))
        self.assertFalse(contains_machine_paths("package.json"))

    # 7. generated content does not contain obvious secret values
    def test_07_generated_content_contains_no_secret_values(self):
        (self.repo_path / "README.md").write_text("# Secure Service\nSample.", encoding="utf-8")
        analysis = analyze(self.repo_path)
        proposed = propose(analysis)

        for art, text in proposed.items():
            self.assertFalse(
                contains_secrets(text),
                f"Artifact {art} must not contain secrets: {text}",
            )

        # Directly test secret detection utility
        self.assertTrue(contains_secrets("api_key = 'abcdef1234567890abcdef'"))
        self.assertTrue(contains_secrets("password: \"supersecretpassword123\""))
        self.assertTrue(contains_secrets("-----BEGIN RSA PRIVATE KEY-----"))
        self.assertTrue(contains_secrets("ghp_123456789012345678901234567890123456"))
        self.assertFalse(contains_secrets("npm run build"))
        self.assertFalse(contains_secrets("API_KEY environment variable is required."))

    # 8. existing AICF context can be discovered/read for future work & rule conflicts detected
    def test_08_governance_context_reading_and_rule_conflict_detection(self):
        init(self.repo_path)
        aicf_dir = self.repo_path / ".aicf"

        (aicf_dir / "rules.md").write_text(
            "# Project Rules\n\n"
            "## Architecture Rules\n\n"
            "- Do not introduce new state-management libraries.\n"
            "- Never commit credentials or secrets.\n",
            encoding="utf-8",
        )
        (aicf_dir / "project.md").write_text(
            "# Project Context\n\n**Name:** Gateway Service\n",
            encoding="utf-8",
        )

        # Discover & read context
        context = read_context(self.repo_path)
        self.assertIn("README.md", context)
        self.assertIn("rules.md", context)
        self.assertIn("project.md", context)
        self.assertIn("Gateway Service", context["project.md"])

        # Check rule conflicts:
        # Scenario A: Task conflicts with state management prohibition
        conflicts = check_rule_conflict(self.repo_path, "Add Redux for client state caching")
        self.assertTrue(len(conflicts) > 0)
        self.assertTrue(any("state-management" in c or "state management" in c for c in conflicts))

        # Scenario B: Task conflicts with secret prohibition
        secret_conflicts = check_rule_conflict(self.repo_path, "Store password in code for quick testing")
        self.assertTrue(len(secret_conflicts) > 0)

        # Scenario C: Normal compliant task
        normal_conflicts = check_rule_conflict(self.repo_path, "Refactor button component to improve accessibility")
        self.assertEqual(len(normal_conflicts), 0)

    # 9. Invalid artifact selection raises AICFBootstrapError
    def test_09_invalid_artifact_selection_rejected(self):
        init(self.repo_path)
        analysis = analyze(self.repo_path)
        proposed = propose(analysis)

        # Attempting to select README.md (structural, not selectable) must raise AICFBootstrapError
        with self.assertRaises(AICFBootstrapError):
            apply(self.repo_path, ["README.md"], proposed)

        # Attempting to select random file must raise AICFBootstrapError
        with self.assertRaises(AICFBootstrapError):
            apply(self.repo_path, ["arbitrary.txt"], proposed)

    # 10. Safety rejections for injected machine paths or secrets
    def test_10_safety_rejections_for_machine_paths_and_secrets(self):
        init(self.repo_path)
        
        # Injected machine path
        unsafe_path_content = {"rules.md": "Reference path: D:\\Sensitive\\Path\\file.ts"}
        with self.assertRaises(AICFBootstrapError):
            apply(self.repo_path, ["rules.md"], unsafe_path_content)

        # Injected secret
        unsafe_secret_content = {"rules.md": "api_key = 'abcdef1234567890abcdef'"}
        with self.assertRaises(AICFBootstrapError):
            apply(self.repo_path, ["rules.md"], unsafe_secret_content)

    # 11. Multi-stack detection: Java Maven + Spring Boot
    def test_11_java_maven_stack_detection(self):
        (self.repo_path / "pom.xml").write_text(
            "<project><dependencies><dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-web</artifactId></dependency></dependencies></project>",
            encoding="utf-8",
        )
        (self.repo_path / "README.md").write_text("# Banking Service\nCore backend banking service.", encoding="utf-8")

        analysis = analyze(self.repo_path)
        summary = analysis["summary"]
        self.assertIn("Java", summary["languages"])
        self.assertIn("Spring Boot", summary["frameworks"])
        self.assertIn("Maven", summary["packageManagers"])

        proposed = propose(analysis)
        self.assertIn("Banking Service", proposed["project.md"])
        self.assertIn("mvn clean compile", proposed["environment.md"])

    # 12. Multi-stack detection: Angular + Nx Monorepo
    def test_12_angular_nx_detection(self):
        (self.repo_path / "package.json").write_text(
            '{"name": "portal-monorepo", "dependencies": {"@angular/core": "^17.0.0"}, "devDependencies": {"nx": "^17.0.0", "typescript": "^5.2.0"}}',
            encoding="utf-8",
        )
        (self.repo_path / "nx.json").write_text('{}', encoding="utf-8")
        (self.repo_path / "angular.json").write_text('{}', encoding="utf-8")

        analysis = analyze(self.repo_path)
        summary = analysis["summary"]
        self.assertIn("Angular", summary["frameworks"])
        self.assertIn("Nx", summary["frameworks"])
        self.assertIn("TypeScript", summary["languages"])


def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAICFPhase1Bootstrap)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
