#!/usr/bin/env python3
"""
AICF Phase 1 Bootstrap & Context Population Tooling.

Implements the normative workflow from AICF-004:
    init -> analyze -> select -> populate (apply) -> govern

Canonical Phase 1 Template:
.aicf/
├── README.md
├── rules.md
├── project.md
├── environment.md
└── state.md
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

CANONICAL_PHASE1_FILES = [
    "README.md",
    "rules.md",
    "project.md",
    "environment.md",
    "state.md",
]

SELECTABLE_ARTIFACTS = [
    "rules.md",
    "project.md",
    "environment.md",
    "state.md",
]

# Patterns representing machine-specific paths (Windows drive letters, file URIs, Unix home roots)
MACHINE_PATH_PATTERNS = [
    re.compile(r"[a-zA-Z]:[\\/][^\s\)\`\'\"]+"),  # D:\..., C:/...
    re.compile(r"file:///[^\s\)\`\'\"]+"),         # file:///...
    re.compile(r"/(?:Users|home)/[^\s\)\`\'\"]+"),  # /Users/... or /home/...
]

# Patterns for sensitive credentials / secrets
SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|password|bearer|auth[_-]?token|private[_-]?key)\s*[:=]\s*['\"]?[a-zA-Z0-9_\-\.]{12,}['\"]?"),
    re.compile(r"(?i)-----BEGIN (?:RSA|OPENSSH|EC|PGP)? PRIVATE KEY-----"),
    re.compile(r"(?i)ghp_[a-zA-Z0-9]{36}"),
]

class AICFBootstrapError(Exception):
    """Base exception for AICF bootstrap operations."""
    pass


def find_phase1_template_dir() -> Optional[Path]:
    """Finds the templates/phase1/.aicf directory if available relative to this script."""
    current = Path(__file__).resolve().parent
    # Check ../../templates/phase1/.aicf
    candidate = current.parent.parent / "templates" / "phase1" / ".aicf"
    if candidate.exists() and candidate.is_dir():
        return candidate
    return None


def get_default_template_content(filename: str) -> str:
    """Returns canonical template content, loading from template dir or built-in fallback."""
    tmpl_dir = find_phase1_template_dir()
    if tmpl_dir:
        target = tmpl_dir / filename
        if target.exists():
            return target.read_text(encoding="utf-8")

    fallbacks = {
        "README.md": (
            "# AICF Local Context\n\n"
            "This `.aicf/` directory provides repository-local engineering context for\n"
            "human developers and AI coding companions.\n\n"
            "## Purpose\n\n"
            "AICF (AI Coding Framework) context files establish shared architectural\n"
            "understanding, engineering rules, and operating environment constraints.\n\n"
            "## Canonical Phase 1 Artifacts\n\n"
            "- `rules.md` — Repository-specific engineering constraints and coding conventions.\n"
            "- `project.md` — Project purpose, architecture, tech stack, and structure.\n"
            "- `environment.md` — Development, build, test, and runtime environment specifications.\n"
            "- `state.md` — Current milestone, active objectives, and known constraints.\n\n"
            "## Governance Principles\n\n"
            "1. Read `rules.md` and `project.md` before planning or modifying code.\n"
            "2. Always follow rules defined in `rules.md`; surface conflicts explicitly.\n"
            "3. Keep context files accurate, concise, and evidence-based.\n"
            "4. Never store credentials, tokens, or workstation-specific paths here.\n"
        ),
        "rules.md": (
            "# Project Rules\n\n"
            "Repository-specific engineering rules and constraints governing human and\n"
            "AI-assisted development.\n\n"
            "## Core Principles\n\n"
            "- Adhere to existing patterns and conventions found in this repository.\n"
            "- Avoid introducing speculative dependencies or unapproved architecture.\n"
            "- Keep modifications minimal, reviewable, and focused on the requested task.\n"
            "- Treat unknown requirements or ambiguous designs explicitly rather than guessing.\n\n"
            "## Coding Conventions\n\n"
            "<!-- Observable coding conventions, style rules, and language standards. -->\n\n"
            "## Architecture & Boundaries\n\n"
            "<!-- Module boundaries, dependency flow rules, and forbidden patterns. -->\n\n"
            "## Testing Expectations\n\n"
            "<!-- Test frameworks used, coverage or test-writing rules, and required checks. -->\n\n"
            "## Security & Privacy Rules\n\n"
            "<!-- Sensitive areas, secret handling rules, input validation requirements. -->\n\n"
            "## AI Operating Invariants\n\n"
            "- Inspect relevant `.aicf/` context files (`rules.md`, `project.md`) before planning.\n"
            "- If a requested task conflicts with any rule in this document, surface the conflict.\n"
            "- Do not commit changes automatically without human review.\n"
            "- Never write credentials, tokens, or absolute workstation paths into this repository.\n"
        ),
        "project.md": (
            "# Project Context\n\n"
            "High-level context describing repository purpose, architecture, and technology.\n\n"
            "## Identity & Purpose\n\n"
            "<!-- Brief description of what this project or system does and who uses it. -->\n\n"
            "## Technology Stack\n\n"
            "<!-- Languages, frameworks, runtimes, package managers, and major libraries. -->\n\n"
            "## Repository Structure\n\n"
            "<!-- Key directories and their architectural roles. All paths must be relative. -->\n\n"
            "## Major Subsystems / Applications\n\n"
            "<!-- Primary application areas, modules, or services within the repository. -->\n\n"
            "## Development & Build Conventions\n\n"
            "<!-- Standard workflows, code generation steps, or workspace configurations. -->\n"
        ),
        "environment.md": (
            "# Environment & Tooling\n\n"
            "Development, build, test, and runtime environment specifications.\n\n"
            "## Runtime & Tooling\n\n"
            "<!-- Language runtimes, SDK versions, package managers, and CLI utilities required. -->\n\n"
            "## Common Commands\n\n"
            "<!-- Frequently used development, build, test, and lint commands. -->\n\n"
            "## Local Services & Prerequisites\n\n"
            "<!-- Local databases, emulators, or required background services (if any). -->\n\n"
            "## Configuration & Environment Variables\n\n"
            "<!-- Required configuration variables, schemas, or profile names.\n"
            "IMPORTANT: Never record actual secrets, API keys, passwords, or tokens here.\n"
            "Only document variable names and their non-sensitive purpose. -->\n\n"
            "## Known Environment Assumptions\n\n"
            "<!-- Operating system assumptions, path requirements, or platform notes. -->\n"
        ),
        "state.md": (
            "# Current State\n\n"
            "High-level status of the repository and ongoing engineering objectives.\n\n"
            "## Current Milestone / Phase\n\n"
            "<!-- Current milestone, phase, or active release cycle. -->\n\n"
            "## Active Work & Focus Areas\n\n"
            "<!-- Current active initiatives or short-term work items. -->\n\n"
            "## Known Constraints & Blockers\n\n"
            "<!-- Active constraints, temporary limitations, or unresolved design questions. -->\n\n"
            "## Recent Key Changes\n\n"
            "<!-- Concise record of recent significant architectural or structural updates. -->\n"
        ),
    }

    if filename not in fallbacks:
        raise AICFBootstrapError(f"Unknown template filename: {filename}")
    return fallbacks[filename]


def sanitize_text(text: str) -> str:
    """Removes or flags machine-specific paths and secrets from generated text."""
    cleaned = text
    for pattern in MACHINE_PATH_PATTERNS:
        cleaned = pattern.sub("<redacted-machine-path>", cleaned)
    for pattern in SECRET_PATTERNS:
        cleaned = pattern.sub("<redacted-secret>", cleaned)
    return cleaned


def contains_machine_paths(text: str) -> bool:
    """Checks whether the text contains absolute workstation/machine paths."""
    for pattern in MACHINE_PATH_PATTERNS:
        if pattern.search(text):
            return True
    return False


def contains_secrets(text: str) -> bool:
    """Checks whether the text contains obvious secret patterns."""
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            return True
    return False


def init(repo_path: Union[str, Path], template_dir: Optional[Path] = None) -> Dict[str, Any]:
    """
    Initializes standard AICF Phase 1 template in repo_path if .aicf does not exist.
    Will NOT overwrite existing .aicf/.
    """
    target_repo = Path(repo_path).resolve()
    aicf_dir = target_repo / ".aicf"

    if aicf_dir.exists():
        return {
            "status": "skipped",
            "message": f"Initialization skipped: .aicf already exists at {aicf_dir.name}",
            "created": [],
            "path": str(aicf_dir.relative_to(target_repo) if aicf_dir == target_repo / ".aicf" else ".aicf"),
        }

    aicf_dir.mkdir(parents=True, exist_ok=False)
    created_files = []

    for filename in CANONICAL_PHASE1_FILES:
        file_path = aicf_dir / filename
        content = get_default_template_content(filename)
        file_path.write_text(content, encoding="utf-8")
        created_files.append(filename)

    return {
        "status": "created",
        "message": "Initialized canonical Phase 1 AICF template.",
        "created": created_files,
        "path": ".aicf",
    }


def analyze(repo_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Passively inspects repository files to extract stack, conventions, and architecture.
    Returns evidence, summary, and proposed content for selectable artifacts.
    """
    target_repo = Path(repo_path).resolve()
    evidence: List[Dict[str, Any]] = []

    # Detection buckets
    languages: Set[str] = set()
    frameworks: Set[str] = set()
    package_managers: Set[str] = set()
    build_commands: List[str] = []
    test_commands: List[str] = []
    lint_commands: List[str] = []
    dev_commands: List[str] = []
    major_areas: List[str] = []
    coding_rules: List[str] = []
    testing_rules: List[str] = []

    project_name = target_repo.name
    project_description = ""

    # 1. Inspect package.json
    pkg_path = target_repo / "package.json"
    if pkg_path.is_file():
        try:
            with open(pkg_path, "r", encoding="utf-8") as f:
                pkg = json.load(f)
            evidence.append({"source": "package.json", "detail": "Node.js manifest present"})
            languages.add("JavaScript")
            
            if "name" in pkg and isinstance(pkg["name"], str):
                project_name = pkg["name"]
            if "description" in pkg and isinstance(pkg["description"], str):
                project_description = pkg["description"]

            # Package manager / engines
            if "packageManager" in pkg:
                pm = str(pkg["packageManager"]).split("@")[0]
                package_managers.add(pm)
                evidence.append({"source": "package.json", "detail": f"packageManager: {pm}"})
            else:
                # Infer from lockfiles
                if (target_repo / "package-lock.json").exists():
                    package_managers.add("npm")
                elif (target_repo / "yarn.lock").exists():
                    package_managers.add("yarn")
                elif (target_repo / "pnpm-lock.yaml").exists():
                    package_managers.add("pnpm")

            # Scripts
            scripts = pkg.get("scripts", {})
            if isinstance(scripts, dict):
                if "build" in scripts:
                    build_commands.append(f"npm run build ({scripts['build']})")
                if "test" in scripts:
                    test_commands.append(f"npm test ({scripts['test']})")
                if "lint" in scripts:
                    lint_commands.append(f"npm run lint ({scripts['lint']})")
                if "start" in scripts or "dev" in scripts:
                    dev_cmd = scripts.get("dev") or scripts.get("start")
                    dev_commands.append(f"npm run dev / start ({dev_cmd})")

            # Dependencies & Frameworks
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            if "typescript" in deps:
                languages.add("TypeScript")
                coding_rules.append("Use TypeScript with strict typing.")
                evidence.append({"source": "package.json", "detail": "TypeScript dependency"})
            if "react" in deps:
                frameworks.add("React")
                evidence.append({"source": "package.json", "detail": "React dependency"})
            if "@angular/core" in deps:
                frameworks.add("Angular")
                evidence.append({"source": "package.json", "detail": "Angular dependency"})
            if "vue" in deps:
                frameworks.add("Vue")
                evidence.append({"source": "package.json", "detail": "Vue dependency"})
            if "next" in deps:
                frameworks.add("Next.js")
                evidence.append({"source": "package.json", "detail": "Next.js dependency"})
            if "jest" in deps or "@types/jest" in deps:
                frameworks.add("Jest")
                testing_rules.append("Write unit tests using Jest.")
                evidence.append({"source": "package.json", "detail": "Jest test framework"})
            if "vitest" in deps:
                frameworks.add("Vitest")
                testing_rules.append("Write unit tests using Vitest.")
                evidence.append({"source": "package.json", "detail": "Vitest test framework"})
            if "eslint" in deps:
                coding_rules.append("Adhere to repository ESLint rules.")
                evidence.append({"source": "package.json", "detail": "ESLint linter"})
        except Exception as e:
            evidence.append({"source": "package.json", "error": str(e)})

    # 2. Inspect tsconfig.json
    tsconfig_path = target_repo / "tsconfig.json"
    if tsconfig_path.is_file():
        languages.add("TypeScript")
        evidence.append({"source": "tsconfig.json", "detail": "TypeScript configuration found"})

    # 3. Inspect angular.json / nx.json
    if (target_repo / "angular.json").is_file():
        frameworks.add("Angular")
        evidence.append({"source": "angular.json", "detail": "Angular workspace CLI"})
    if (target_repo / "nx.json").is_file():
        frameworks.add("Nx")
        evidence.append({"source": "nx.json", "detail": "Nx monorepo workspace"})

    # 4. Inspect pom.xml (Java / Maven)
    pom_path = target_repo / "pom.xml"
    if pom_path.is_file():
        languages.add("Java")
        package_managers.add("Maven")
        build_commands.append("mvn clean compile")
        test_commands.append("mvn test")
        testing_rules.append("Write tests using JUnit.")
        evidence.append({"source": "pom.xml", "detail": "Maven build file found"})
        try:
            content = pom_path.read_text(encoding="utf-8", errors="ignore")
            if "spring-boot" in content:
                frameworks.add("Spring Boot")
                evidence.append({"source": "pom.xml", "detail": "Spring Boot dependency"})
        except Exception:
            pass

    # 5. Inspect build.gradle / build.gradle.kts
    gradle_path = target_repo / "build.gradle"
    gradle_kts = target_repo / "build.gradle.kts"
    if gradle_path.is_file() or gradle_kts.is_file():
        languages.add("Java")
        package_managers.add("Gradle")
        build_commands.append("./gradlew build")
        test_commands.append("./gradlew test")
        evidence.append({"source": "build.gradle", "detail": "Gradle build file found"})

    # 6. Inspect Python (pyproject.toml / requirements.txt / setup.py / Python scripts)
    pyproject = target_repo / "pyproject.toml"
    reqs = target_repo / "requirements.txt"
    setup_py = target_repo / "setup.py"
    py_files = list(target_repo.glob("*.py")) + list((target_repo / "schemas").glob("**/*.py")) + list((target_repo / "tooling").glob("**/*.py"))
    workflows_with_python = False
    wf_dir = target_repo / ".github" / "workflows"
    if wf_dir.is_dir():
        for wf in wf_dir.glob("*.yml"):
            try:
                if "python" in wf.read_text(encoding="utf-8", errors="ignore").lower():
                    workflows_with_python = True
                    break
            except Exception:
                pass

    if pyproject.is_file() or reqs.is_file() or setup_py.is_file() or py_files or workflows_with_python:
        languages.add("Python")
        if reqs.is_file():
            evidence.append({"source": "requirements.txt", "detail": "Python requirements found"})
        if pyproject.is_file():
            evidence.append({"source": "pyproject.toml", "detail": "pyproject.toml found"})
        if py_files:
            evidence.append({"source": "repository", "detail": f"Python files detected ({len(py_files)} files)"})
            test_commands.append("python -m unittest / pytest")
            testing_rules.append("Write tests using standard unittest or pytest.")
        if workflows_with_python:
            evidence.append({"source": ".github/workflows", "detail": "Python CI workflow configuration"})


    # 7. Inspect Rust (Cargo.toml)
    cargo_path = target_repo / "Cargo.toml"
    if cargo_path.is_file():
        languages.add("Rust")
        package_managers.add("Cargo")
        build_commands.append("cargo build")
        test_commands.append("cargo test")
        evidence.append({"source": "Cargo.toml", "detail": "Rust Cargo manifest found"})

    # 8. Inspect Go (go.mod)
    go_mod = target_repo / "go.mod"
    if go_mod.is_file():
        languages.add("Go")
        build_commands.append("go build ./...")
        test_commands.append("go test ./...")
        evidence.append({"source": "go.mod", "detail": "Go module definition found"})

    # 9. Inspect README.md for project overview
    readme_path = target_repo / "README.md"
    if readme_path.is_file():
        try:
            content = readme_path.read_text(encoding="utf-8", errors="ignore")
            # Extract first non-empty markdown title
            m = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
            if m:
                extracted_title = m.group(1).strip()
                if not project_name or project_name == target_repo.name:
                    project_name = extracted_title
            # Extract short paragraph following title
            paras = [p.strip() for p in content.split("\n\n") if p.strip() and not p.strip().startswith("#")]
            if paras and not project_description:
                project_description = paras[0].replace("\n", " ")[:240]
            evidence.append({"source": "README.md", "detail": "Project overview extracted"})
        except Exception:
            pass

    # 10. Inspect repository directory structure (relative paths only!)
    structural_dirs = []
    common_roots = [
        "src", "apps", "libs", "packages", "docs", "schemas",
        "templates", "tooling", "adapters", "pilots", "tests", "test"
    ]
    for d in common_roots:
        p = target_repo / d
        if p.is_dir():
            structural_dirs.append(f"`{d}/`")
            major_areas.append(f"{d} module / directory")

    # Construct synthesized proposed content for selectable artifacts
    lang_str = ", ".join(sorted(languages)) if languages else "Polyglot / Unspecified"
    fw_str = ", ".join(sorted(frameworks)) if frameworks else "Standard libraries"
    pm_str = ", ".join(sorted(package_managers)) if package_managers else "Standard tooling"
    dirs_str = ", ".join(structural_dirs) if structural_dirs else "Root workspace"

    # Synthesize rules.md
    coding_rules_md = "\n".join(f"- {r}" for r in coding_rules) if coding_rules else "- Follow existing file conventions and style in this repository."
    testing_rules_md = "\n".join(f"- {r}" for r in testing_rules) if testing_rules else "- Maintain and execute tests before completing tasks."

    proposed_rules = (
        "# Project Rules\n\n"
        f"Engineering rules and constraints for `{project_name}`.\n\n"
        "## Core Principles\n\n"
        "- Adhere to existing patterns and conventions found in this repository.\n"
        "- Avoid introducing speculative dependencies or unapproved architecture.\n"
        "- Keep modifications minimal, reviewable, and focused on the requested task.\n"
        "- Treat unknown requirements or ambiguous designs explicitly rather than guessing.\n\n"
        "## Coding Conventions\n\n"
        f"{coding_rules_md}\n"
        "- Do not use absolute workstation paths in code, comments, or configurations.\n\n"
        "## Architecture & Boundaries\n\n"
        f"- Respect modular structure across {dirs_str}.\n"
        "- Do not introduce external libraries without explicit necessity.\n\n"
        "## Testing Expectations\n\n"
        f"{testing_rules_md}\n\n"
        "## Security & Privacy Rules\n\n"
        "- Never commit or expose API keys, tokens, passwords, private keys, or secrets.\n"
        "- Sanitize all inputs at system boundaries.\n\n"
        "## AI Operating Invariants\n\n"
        "- Inspect `.aicf/rules.md` and `.aicf/project.md` before planning any changes.\n"
        "- If a user task conflicts with these rules, explicitly surface the conflict.\n"
        "- Do not commit changes automatically without user review.\n"
    )

    # Synthesize project.md
    desc_str = project_description if project_description else "Engineering project managed with AICF context."
    proposed_project = (
        "# Project Context\n\n"
        "## Identity & Purpose\n\n"
        f"**Name:** {project_name}\n"
        f"**Description:** {desc_str}\n\n"
        "## Technology Stack\n\n"
        f"- **Languages:** {lang_str}\n"
        f"- **Frameworks / Libraries:** {fw_str}\n"
        f"- **Package Manager:** {pm_str}\n\n"
        "## Repository Structure\n\n"
        f"Active primary directories: {dirs_str}.\n\n"
        "## Major Subsystems / Applications\n\n"
        + ("\n".join(f"- {area}" for area in major_areas) if major_areas else "- Main application workspace") + "\n\n"
        "## Development & Build Conventions\n\n"
        "- Keep changes localized and verify with project tests.\n"
    )

    # Synthesize environment.md
    cmd_build = "\n".join(f"- Build: `{c}`" for c in build_commands) if build_commands else "- Build: (None detected or not applicable)"
    cmd_test = "\n".join(f"- Test: `{c}`" for c in test_commands) if test_commands else "- Test: (None detected)"
    cmd_lint = "\n".join(f"- Lint: `{c}`" for c in lint_commands) if lint_commands else "- Lint: (None detected)"
    cmd_dev = "\n".join(f"- Dev: `{c}`" for c in dev_commands) if dev_commands else "- Dev: (None detected)"

    proposed_environment = (
        "# Environment & Tooling\n\n"
        "## Runtime & Tooling\n\n"
        f"- **Runtimes / Languages:** {lang_str}\n"
        f"- **Package Manager:** {pm_str}\n\n"
        "## Common Commands\n\n"
        f"{cmd_build}\n"
        f"{cmd_test}\n"
        f"{cmd_lint}\n"
        f"{cmd_dev}\n\n"
        "## Local Services & Prerequisites\n\n"
        "- Local development dependencies managed via the detected package manager.\n\n"
        "## Configuration & Environment Variables\n\n"
        "<!-- Document required environment variable names here. -->\n"
        "<!-- NEVER record actual secret values, tokens, or credentials. -->\n\n"
        "## Known Environment Assumptions\n\n"
        "- Cross-platform compatibility expected.\n"
        "- Relative repository paths only.\n"
    )

    # Synthesize state.md (conservative Phase 1 state)
    proposed_state = (
        "# Current State\n\n"
        "## Current Milestone / Phase\n\n"
        "- Initial AICF Bootstrap & Context Grounding (Phase 1).\n\n"
        "## Active Work & Focus Areas\n\n"
        "- Repository characterization and context population.\n\n"
        "## Known Constraints & Blockers\n\n"
        "- None recorded.\n\n"
        "## Recent Key Changes\n\n"
        "- Initialized `.aicf/` context files.\n"
    )

    # Safety validation
    raw_proposed = {
        "rules.md": sanitize_text(proposed_rules),
        "project.md": sanitize_text(proposed_project),
        "environment.md": sanitize_text(proposed_environment),
        "state.md": sanitize_text(proposed_state),
    }

    # Verify no machine paths or secrets exist in generated markdown
    for art, text in raw_proposed.items():
        if contains_machine_paths(text):
            raise AICFBootstrapError(f"Safety violation: Machine path detected in generated {art}")
        if contains_secrets(text):
            raise AICFBootstrapError(f"Safety violation: Secret detected in generated {art}")

    summary = {
        "projectName": project_name,
        "languages": sorted(list(languages)),
        "frameworks": sorted(list(frameworks)),
        "packageManagers": sorted(list(package_managers)),
        "keyDirectories": structural_dirs,
    }

    return {
        "evidence": evidence,
        "summary": summary,
        "proposed": raw_proposed,
    }


def propose(analysis_result: Dict[str, Any]) -> Dict[str, str]:
    """Returns the proposed content dictionary from an analysis result."""
    if "proposed" not in analysis_result:
        raise AICFBootstrapError("Analysis result does not contain 'proposed' content")
    return analysis_result["proposed"]


CHARACTERIZATION_FIELDS = (
    "identity", "purpose", "languages", "frameworks", "runtimes",
    "package_manager", "important_dependencies", "build_tooling",
    "testing_tooling", "repository_structure", "development_workflow",
    "engineering_conventions", "architectural_boundaries",
    "generated_vendor_files", "agent_constraints",
)


def _walk_strings(value: Any) -> List[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [s for item in value.values() for s in _walk_strings(item)]
    if isinstance(value, list):
        return [s for item in value for s in _walk_strings(item)]
    return []


def validate_characterization(result: Dict[str, Any], repo_path: Union[str, Path]) -> None:
    """Validate the portable agent handoff and its repository-relative evidence."""
    if not isinstance(result, dict):
        raise AICFBootstrapError("Characterization must be a JSON object")
    allowed = set(CHARACTERIZATION_FIELDS) | {"proposed_artifacts", "evidence"}
    unknown = sorted(set(result) - allowed)
    if unknown:
        raise AICFBootstrapError(f"Characterization contains unsupported fields: {', '.join(unknown)}")
    missing = [field for field in CHARACTERIZATION_FIELDS if field not in result]
    if missing:
        raise AICFBootstrapError(f"Characterization is missing fields: {', '.join(missing)}")
    for field in CHARACTERIZATION_FIELDS:
        value = result[field]
        if isinstance(value, str):
            continue
        if isinstance(value, list) and all(isinstance(item, str) for item in value):
            continue
        if field == "repository_structure" and isinstance(value, dict):
            continue
        raise AICFBootstrapError(f"Characterization field '{field}' must be text, a list of text, or a structure object")
    artifacts = result.get("proposed_artifacts")
    if not isinstance(artifacts, dict) or not all(isinstance(artifacts.get(name), str) for name in ("project.md", "rules.md")):
        raise AICFBootstrapError("Characterization must include proposed_artifacts.project.md and proposed_artifacts.rules.md text")
    evidence = result.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        raise AICFBootstrapError("Characterization must include repository-relative evidence")
    root = Path(repo_path).resolve()
    for item in evidence:
        if not isinstance(item, dict) or set(item) != {"finding", "paths"} or not isinstance(item.get("finding"), str):
            raise AICFBootstrapError("Each evidence item must include a finding and paths")
        paths = item.get("paths")
        if not isinstance(paths, list) or not paths:
            raise AICFBootstrapError(f"Evidence for '{item['finding']}' must include one or more paths")
        for raw_path in paths:
            if not isinstance(raw_path, str) or not raw_path or raw_path.startswith(("/", "\\")) or re.match(r"^[a-zA-Z]:", raw_path) or raw_path.lower().startswith("file:"):
                raise AICFBootstrapError(f"Evidence path must be repository-relative: {raw_path!r}")
            candidate = (root / raw_path).resolve()
            try:
                candidate.relative_to(root)
            except ValueError:
                raise AICFBootstrapError(f"Evidence path escapes repository: {raw_path!r}")
            if not candidate.exists():
                raise AICFBootstrapError(f"Evidence path does not exist in repository: {raw_path!r}")
    all_text = _walk_strings(result)
    for value in all_text:
        if (contains_machine_paths(value) or re.search(r"(?i)file://", value)
                or re.search(r"(?:^|[\s('\"=:])/(?!/)[^\s)`'\",;]+", value)):
            raise AICFBootstrapError("Characterization contains an absolute or file:// path")
        if contains_secrets(value):
            raise AICFBootstrapError("Characterization contains a credential or secret")


def _as_lines(value: Any) -> List[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, dict):
        return [f"- {key}: {item}" for key, item in value.items()]
    return [str(value)] if value else []


def characterize(repo_path: Union[str, Path], result: Dict[str, Any]) -> Dict[str, Any]:
    """Validate agent output and return reviewable candidates plus context warnings."""
    validate_characterization(result, repo_path)
    proposed = dict(result["proposed_artifacts"])
    evidence_lines = [
        f"- {item['finding']}: {', '.join(f'`{path}`' for path in item['paths'])}"
        for item in result["evidence"]
    ]
    evidence_section = "\n\n## Characterization Evidence\n\n" + "\n".join(evidence_lines) + "\n"
    for name in ("project.md", "rules.md"):
        if "## Characterization Evidence" not in proposed[name]:
            proposed[name] = proposed[name].rstrip() + evidence_section
        if contains_machine_paths(proposed[name]) or re.search(r"(?i)file://", proposed[name]):
            raise AICFBootstrapError(f"Safety violation: unsafe path in proposed {name}")
        if contains_secrets(proposed[name]):
            raise AICFBootstrapError(f"Safety violation: secret in proposed {name}")
    existing = read_context(repo_path, ["rules.md"]).get("rules.md", "")
    conflicts = detect_context_conflicts(existing, proposed["rules.md"])
    return {"characterization": result, "proposed": proposed, "conflicts": conflicts}


def detect_context_conflicts(existing_rules: str, proposed_rules: str) -> List[str]:
    """Flag same-topic opposite-polarity rule bullets for user review."""
    conflicts = []
    bullets = lambda text: [line.strip().lstrip("-* ").strip() for line in text.splitlines() if line.strip().startswith(("-", "*"))]
    neg = re.compile(r"\b(do not|don't|never|avoid|prohibit|forbidden|must not)\b", re.I)
    for old in bullets(existing_rules):
        for new in bullets(proposed_rules):
            old_terms = set(re.findall(r"[a-z0-9]+", old.lower())) - {"do", "not", "never", "avoid", "must", "use", "with", "the", "a", "an", "to", "and", "or"}
            new_terms = set(re.findall(r"[a-z0-9]+", new.lower())) - {"do", "not", "never", "avoid", "must", "use", "with", "the", "a", "an", "to", "and", "or"}
            shared = old_terms & new_terms
            if shared and bool(neg.search(old)) != bool(neg.search(new)):
                conflicts.append(f"Possible rules conflict: existing '{old}' vs proposed '{new}'")
    return conflicts


def merge_markdown_sections(existing: str, proposed: str) -> str:
    """
    Conservatively merges proposed markdown content into existing markdown.
    Preserves user modifications under existing headers.
    If a section only has default HTML comments/placeholders, proposed content fills it.
    """
    # If existing is completely blank or matches default placeholder pattern, use proposed
    if not existing.strip():
        return proposed

    # Split into sections by H2 headers
    header_regex = re.compile(r"^(##\s+[^\n]+)$", re.MULTILINE)
    
    def parse_sections(doc: str) -> Tuple[str, Dict[str, str]]:
        parts = header_regex.split(doc)
        lead = parts[0]
        secs = {}
        for i in range(1, len(parts), 2):
            h = parts[i].strip()
            body = parts[i+1] if i+1 < len(parts) else ""
            secs[h] = body
        return lead, secs

    ex_lead, ex_secs = parse_sections(existing)
    pr_lead, pr_secs = parse_sections(proposed)

    merged_sections: Dict[str, str] = dict(ex_secs)

    for h, pr_body in pr_secs.items():
        if h not in merged_sections:
            # New section from proposed: add it
            merged_sections[h] = pr_body
        else:
            cur_body = merged_sections[h]
            # Check if current section body is merely empty or contains only comments <!-- ... -->
            body_without_comments = re.sub(r"<!--[\s\S]*?-->", "", cur_body).strip()
            if not body_without_comments:
                # Replace placeholder with proposed content
                merged_sections[h] = pr_body
            else:
                # User has customized this section! Preserve existing content.
                # If proposed adds bullet items not already present, we can append them cleanly
                # without destroying user's existing text.
                pass

    # Reconstruct document
    out = [ex_lead.rstrip()]
    for h, body in merged_sections.items():
        out.append(f"\n\n{h}\n{body.strip()}\n")

    return "".join(out).strip() + "\n"


def apply(
    repo_path: Union[str, Path],
    selected_artifacts: List[str],
    proposed_content: Dict[str, str],
    force_overwrite: bool = False,
) -> Dict[str, Any]:
    """
    Applies proposed content ONLY to the selected artifacts.
    Non-destructive by default: preserves valid user modifications in existing files.
    """
    target_repo = Path(repo_path).resolve()
    aicf_dir = target_repo / ".aicf"

    if not aicf_dir.exists():
        raise AICFBootstrapError(f"Cannot apply context: .aicf directory does not exist at {aicf_dir}")

    # Validate selected artifacts
    invalid_selections = [a for a in selected_artifacts if a not in SELECTABLE_ARTIFACTS]
    if invalid_selections:
        raise AICFBootstrapError(
            f"Invalid artifact selection: {invalid_selections}. Only {SELECTABLE_ARTIFACTS} are selectable."
        )

    updated: List[str] = []
    skipped: List[str] = []
    preserved_user_content: List[str] = []

    for artifact in SELECTABLE_ARTIFACTS:
        target_file = aicf_dir / artifact
        if artifact not in selected_artifacts:
            skipped.append(artifact)
            continue

        if artifact not in proposed_content:
            skipped.append(artifact)
            continue

        content_to_apply = proposed_content[artifact]

        # Guard against machine paths and secrets
        if contains_machine_paths(content_to_apply):
            raise AICFBootstrapError(f"Safety violation: Machine-specific path detected in content for {artifact}")
        if contains_secrets(content_to_apply):
            raise AICFBootstrapError(f"Safety violation: Secret detected in content for {artifact}")

        if target_file.exists() and not force_overwrite:
            existing_content = target_file.read_text(encoding="utf-8")
            merged_content = merge_markdown_sections(existing_content, content_to_apply)
            # Check if user content was preserved
            if merged_content != content_to_apply and existing_content.strip() != "":
                preserved_user_content.append(artifact)
            target_file.write_text(merged_content, encoding="utf-8")
        else:
            target_file.write_text(content_to_apply, encoding="utf-8")

        updated.append(artifact)

    return {
        "status": "applied",
        "updated": updated,
        "skipped": skipped,
        "preserved_customizations": preserved_user_content,
    }


def read_context(
    repo_path: Union[str, Path],
    artifacts: Optional[List[str]] = None,
) -> Dict[str, str]:
    """
    Discovers .aicf/ and reads the specified (or core governance) artifacts.
    Default core artifacts: README.md, rules.md, project.md.
    """
    target_repo = Path(repo_path).resolve()
    aicf_dir = target_repo / ".aicf"

    if not aicf_dir.exists() or not aicf_dir.is_dir():
        raise AICFBootstrapError(f".aicf directory not found in repository at {target_repo}")

    if artifacts is None:
        # Default governance artifacts
        artifacts_to_read = ["README.md", "rules.md", "project.md"]
    else:
        artifacts_to_read = artifacts

    context_data: Dict[str, str] = {}
    for art in artifacts_to_read:
        file_path = aicf_dir / art
        if file_path.is_file():
            context_data[art] = file_path.read_text(encoding="utf-8")
        else:
            context_data[art] = f"<!-- {art} not present in .aicf/ -->"

    return context_data


def check_rule_conflict(
    repo_path: Union[str, Path],
    task_description: str,
) -> List[str]:
    """
    Evaluates a proposed development task against repository rules in .aicf/rules.md.
    Returns a list of conflict warning messages if violations are suspected.
    """
    target_repo = Path(repo_path).resolve()
    rules_path = target_repo / ".aicf" / "rules.md"

    if not rules_path.is_file():
        return []

    rules_content = rules_path.read_text(encoding="utf-8")
    conflicts: List[str] = []

    # Prohibitive rules extraction (e.g., "Do not...", "Never...", "Avoid...", "Prohibit...")
    rule_lines = [line.strip() for line in rules_content.splitlines() if line.strip().startswith("-")]

    task_lower = task_description.lower()

    for line in rule_lines:
        line_clean = line.lstrip("- *").strip()
        line_lower = line_clean.lower()

        # Check for explicit prohibitions
        if any(term in line_lower for term in ["do not", "never", "avoid", "prohibit", "forbidden"]):
            # Check for conflict scenarios:
            # 1. Redux or state-management prohibition
            if "state-management" in line_lower or "redux" in line_lower:
                if any(k in task_lower for k in ["redux", "mobx", "zustand", "state management library"]):
                    conflicts.append(f"Rule Conflict: '{line_clean}' conflicts with requested task mentioning state management.")

            # 2. Hardcoded secrets / credentials
            if "secret" in line_lower or "credential" in line_lower or "api key" in line_lower:
                if any(k in task_lower for k in ["hardcode api key", "store password in code", "commit credentials"]):
                    conflicts.append(f"Rule Conflict: '{line_clean}' conflicts with requested credential handling.")

            # 3. Absolute paths
            if "absolute" in line_lower and "path" in line_lower:
                if any(k in task_lower for k in ["absolute path", "hardcoded path"]):
                    conflicts.append(f"Rule Conflict: '{line_clean}' conflicts with requested path handling.")

            # 4. Direct keyword match between task and forbidden phrase
            forbidden_matches = re.findall(r"(?:do not|never|avoid|prohibit)\s+([a-zA-Z0-9\s\-]+?)(?:\.|$|,|;)", line_lower)
            for fm in forbidden_matches:
                fm_clean = fm.strip()
                if len(fm_clean) > 4 and fm_clean in task_lower:
                    conflicts.append(f"Rule Conflict: Prohibited action '{fm_clean}' (from rule: '{line_clean}') is referenced in task.")

    return conflicts


def main():
    parser = argparse.ArgumentParser(description="AICF Phase 1 Bootstrap & Context Population Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Init
    init_parser = subparsers.add_parser("init", help="Initialize .aicf/ Phase 1 template")
    init_parser.add_argument("--path", default=".", help="Target repository path")

    # Analyze
    analyze_parser = subparsers.add_parser("analyze", help="Analyze repository and propose context")
    analyze_parser.add_argument("--path", default=".", help="Target repository path")
    analyze_parser.add_argument("--json", action="store_true", help="Output raw JSON analysis")

    # Apply
    apply_parser = subparsers.add_parser("apply", help="Apply proposed context to selected artifacts")
    apply_parser.add_argument("--path", default=".", help="Target repository path")
    apply_parser.add_argument("--select", default="rules.md,project.md", help="Comma-separated list of artifacts to populate")
    apply_parser.add_argument("--all", action="store_true", help="Select all 4 selectable artifacts")
    apply_parser.add_argument("--force", action="store_true", help="Force overwrite existing customizations")
    apply_parser.add_argument("--proposal-file", help="JSON proposal produced by characterize")

    # Agent handoff: validate a portable characterization and write a reviewable proposal.
    characterize_parser = subparsers.add_parser("characterize", help="Validate agent characterization and create candidate artifacts")
    characterize_parser.add_argument("--path", default=".", help="Target repository path")
    characterize_parser.add_argument("--input", required=True, help="JSON file containing the characterization contract")
    characterize_parser.add_argument("--output", help="Write candidate proposal JSON to this file (otherwise stdout)")

    # Govern
    govern_parser = subparsers.add_parser("govern", help="Read AICF context and check rule conflicts")
    govern_parser.add_argument("--path", default=".", help="Target repository path")
    govern_parser.add_argument("--check-task", default=None, help="Check a proposed development task for rule conflicts")

    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    args = parser.parse_args()
    target_path = Path(args.path).resolve()

    try:
        if args.command == "init":
            res = init(target_path)
            print(f"[{res['status'].upper()}] {res['message']}")
            if res["created"]:
                print("Created artifacts:")
                for f in res["created"]:
                    print(f"  + .aicf/{f}")

        elif args.command == "analyze":
            analysis = analyze(target_path)
            if args.json:
                print(json.dumps(analysis, indent=2))
            else:
                print(f"=== AICF Repository Analysis: {analysis['summary']['projectName']} ===")
                print(f"Languages:       {', '.join(analysis['summary']['languages']) or 'None'}")
                print(f"Frameworks:      {', '.join(analysis['summary']['frameworks']) or 'None'}")
                print(f"Package Manager: {', '.join(analysis['summary']['packageManagers']) or 'None'}")
                print(f"Key Directories: {', '.join(analysis['summary']['keyDirectories']) or 'None'}")
                print("\nEvidence Items:")
                for ev in analysis["evidence"]:
                    detail = ev.get("detail", ev.get("error", "detected"))
                    print(f"  * [{ev['source']}] {detail}")
                print("\nProposed Artifacts ready for selection:")
                for art in SELECTABLE_ARTIFACTS:
                    print(f"  [ ] {art}")

        elif args.command == "apply":
            if args.proposal_file:
                try:
                    proposal_data = json.loads(Path(args.proposal_file).read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError) as err:
                    raise AICFBootstrapError(f"Cannot read proposal file: {err}")
                proposed = proposal_data.get("proposed")
                if not isinstance(proposed, dict):
                    raise AICFBootstrapError("Proposal file must contain a 'proposed' artifact object")
            else:
                analysis = analyze(target_path)
                proposed = propose(analysis)
            if args.all:
                selections = SELECTABLE_ARTIFACTS
            else:
                selections = [s.strip() for s in args.select.split(",") if s.strip()]

            res = apply(target_path, selections, proposed, force_overwrite=args.force)
            print(f"[{res['status'].upper()}] Context population completed.")
            print(f"Updated artifacts:   {res['updated']}")
            print(f"Skipped artifacts:   {res['skipped']}")
            if res["preserved_customizations"]:
                print(f"Preserved user work: {res['preserved_customizations']}")

        elif args.command == "characterize":
            try:
                agent_result = json.loads(Path(args.input).read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as err:
                raise AICFBootstrapError(f"Cannot read characterization input: {err}")
            candidate = characterize(target_path, agent_result)
            candidate["deterministic_evidence"] = analyze(target_path)
            serialized = json.dumps(candidate, indent=2, ensure_ascii=False)
            if args.output:
                output_path = Path(args.output)
                if output_path.exists() or output_path.is_symlink():
                    raise AICFBootstrapError(f"Refusing to overwrite existing proposal output: {output_path}")
                output_path.write_text(serialized + "\n", encoding="utf-8")
                print(f"Candidate proposal written to {args.output}")
                if candidate["conflicts"]:
                    print("Review conflicts:")
                    for conflict in candidate["conflicts"]:
                        print(f"  - {conflict}")
            else:
                print(serialized)

        elif args.command == "govern":
            context = read_context(target_path)
            print("=== AICF Local Governance Context ===")
            for art, content in context.items():
                print(f"\n--- .aicf/{art} ---")
                lines = content.splitlines()[:6]
                print("\n".join(lines))
                if len(content.splitlines()) > 6:
                    print(f"... ({len(content.splitlines()) - 6} more lines)")

            if args.check_task:
                print(f"\nEvaluating task: '{args.check_task}'")
                conflicts = check_rule_conflict(target_path, args.check_task)
                if conflicts:
                    print("\n[!] Rule conflicts detected:")
                    for c in conflicts:
                        print(f"  - {c}")
                    sys.exit(2)
                else:
                    print("\n[OK] No rule conflicts detected. Task conforms to .aicf/rules.md.")

    except AICFBootstrapError as err:
        print(f"AICF Error: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
