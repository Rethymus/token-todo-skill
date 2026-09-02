#!/usr/bin/env python3
"""Validate Token Todo repository structure without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Optional
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
CHECKS = 0


def check(condition: bool, message: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        ERRORS.append(message)


def load_text(relative: str) -> str:
    path = ROOT / relative
    check(path.is_file(), f"Missing required file: {relative}")
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def load_json(relative: str) -> object:
    raw = load_text(relative)
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        ERRORS.append(f"Invalid JSON in {relative}: {exc}")
        return {}


def frontmatter_value(frontmatter: str, key: str) -> Optional[str]:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", frontmatter)
    if not match:
        return None
    return match.group(1).strip().strip("\"'")


def validate_manifest() -> None:
    manifest = load_json(".codex-plugin/plugin.json")
    if not isinstance(manifest, dict):
        return

    for key in ("name", "version", "description", "author", "skills", "interface"):
        check(key in manifest, f"Plugin manifest is missing {key!r}")
    check(manifest.get("name") == "token-todo", "Plugin name must be token-todo")
    check(
        isinstance(manifest.get("version"), str)
        and bool(re.fullmatch(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)", manifest["version"])),
        "Plugin version must use strict MAJOR.MINOR.PATCH semver",
    )
    check(manifest.get("version") == "0.2.0", "Plugin version must match the current skill release")
    check(manifest.get("license") == "MIT", "Plugin license must be MIT")
    check(manifest.get("skills") == "./skills/", "Plugin skills path must be ./skills/")
    author = manifest.get("author", {})
    check(isinstance(author, dict) and author.get("name") == "Rethymus", "Plugin author.name must be Rethymus")

    interface = manifest.get("interface", {})
    for key in (
        "displayName",
        "shortDescription",
        "longDescription",
        "developerName",
        "category",
        "capabilities",
        "defaultPrompt",
    ):
        check(key in interface, f"Plugin interface is missing {key!r}")
    check(interface.get("displayName") == "Token Todo", "Unexpected plugin displayName")
    check(interface.get("developerName") == "Rethymus", "Unexpected plugin developerName")
    prompts = interface.get("defaultPrompt")
    check(isinstance(prompts, (str, list)) and bool(prompts), "Plugin defaultPrompt must be non-empty")


def validate_marketplace() -> None:
    marketplace = load_json(".agents/plugins/marketplace.json")
    if not isinstance(marketplace, dict):
        return
    check(marketplace.get("name") == "token-todo", "Marketplace name must be token-todo")
    plugins = marketplace.get("plugins")
    check(isinstance(plugins, list) and len(plugins) == 1, "Marketplace must contain exactly one plugin")
    if not isinstance(plugins, list) or len(plugins) != 1:
        return
    plugin = plugins[0]
    check(isinstance(plugin, dict) and plugin.get("name") == "token-todo", "Marketplace plugin must be token-todo")
    if not isinstance(plugin, dict):
        return
    source = plugin.get("source", {})
    policy = plugin.get("policy", {})
    check(isinstance(source, dict) and source.get("source") == "local", "Marketplace source must be local")
    check(isinstance(source, dict) and source.get("path") == "./", "Marketplace source path must be ./")
    check(isinstance(policy, dict) and policy.get("installation") == "AVAILABLE", "Installation must be AVAILABLE")
    check(isinstance(policy, dict) and policy.get("authentication") == "ON_INSTALL", "Authentication must be ON_INSTALL")


def validate_skill() -> None:
    skills_root = ROOT / "skills"
    skill_dirs = (
        sorted(path for path in skills_root.iterdir() if path.is_dir() and (path / "SKILL.md").is_file())
        if skills_root.is_dir()
        else []
    )
    check(len(skill_dirs) == 1, "Repository must contain exactly one skill directory")
    if len(skill_dirs) != 1:
        return

    skill_dir = skill_dirs[0]
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
    check(match is not None, "SKILL.md must begin with YAML frontmatter")
    if not match:
        return
    frontmatter = match.group(1)
    name = frontmatter_value(frontmatter, "name")
    description = frontmatter_value(frontmatter, "description")
    license_name = frontmatter_value(frontmatter, "license")
    check(name == skill_dir.name == "token-todo", "Skill name must match its directory")
    check(
        bool(name) and len(name) <= 64 and bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name or "")),
        "Skill name must follow the Agent Skills naming constraint",
    )
    check(bool(description) and len(description or "") <= 1024, "Skill description must be 1-1024 characters")
    check(description is not None and description.startswith("Use only when "), "Description must begin with trigger conditions")
    check(license_name == "MIT", "Skill frontmatter license must be MIT")
    check("author: Rethymus" in frontmatter, "Skill metadata must identify Rethymus")
    check('version: "0.2.0"' in frontmatter, "Skill metadata version must be 0.2.0")
    check(len(text.splitlines()) <= 500, "SKILL.md must remain under 500 lines")
    for reference in (
        "operating-model.md",
        "scheduling-policy.md",
        "task-ledger.md",
        "safety-and-rollback.md",
        "goals-and-prompts.md",
    ):
        check((skill_dir / "references" / reference).is_file(), f"Missing skill reference: {reference}")

    agent_text = load_text("skills/token-todo/agents/openai.yaml")
    check('display_name: "Token Todo"' in agent_text, "openai.yaml needs the expected display_name")
    short_match = re.search(r'(?m)^\s*short_description:\s*"([^"]+)"\s*$', agent_text)
    check(short_match is not None and 25 <= len(short_match.group(1)) <= 64, "short_description must be 25-64 characters")
    check("$token-todo" in agent_text, "openai.yaml default_prompt must mention $token-todo")
    check("allow_implicit_invocation: false" in agent_text, "Token Todo must remain explicit-only")


def validate_readmes_and_links() -> None:
    english = load_text("README.md")
    chinese = load_text("README.zh-CN.md")
    for marker in ("README.zh-CN.md", "## Installation", "## Usage", "## Design provenance", "## License"):
        check(marker in english, f"English README is missing {marker!r}")
    for marker in ("README.md", "## 安装", "## 使用", "## 设计来源", "## 许可证"):
        check(marker in chinese, f"Chinese README is missing {marker!r}")

    markdown_files = [path for path in ROOT.rglob("*.md") if ".git" not in path.parts]
    link_pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    for path in markdown_files:
        content = path.read_text(encoding="utf-8")
        for target in link_pattern.findall(content):
            target = target.strip().strip("<>")
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            relative_target = unquote(target.split("#", 1)[0])
            resolved = (path.parent / relative_target).resolve()
            check(resolved.exists(), f"Broken local link in {path.relative_to(ROOT)}: {target}")


def validate_scenarios() -> int:
    scenarios = load_json("tests/scenarios.json")
    check(isinstance(scenarios, list) and len(scenarios) >= 16, "Scenario corpus must contain at least sixteen cases")
    if not isinstance(scenarios, list):
        return 0

    identifiers: list[str] = []
    trigger_values: list[bool] = []
    for index, scenario in enumerate(scenarios):
        prefix = f"Scenario {index + 1}"
        check(isinstance(scenario, dict), f"{prefix} must be an object")
        if not isinstance(scenario, dict):
            continue
        for key in ("id", "prompt", "should_trigger", "expected_decisions", "forbidden_decisions"):
            check(key in scenario, f"{prefix} is missing {key!r}")
        identifier = scenario.get("id")
        check(isinstance(identifier, str) and bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identifier)), f"{prefix} has an invalid id")
        if isinstance(identifier, str):
            identifiers.append(identifier)
        check(isinstance(scenario.get("prompt"), str) and bool(scenario.get("prompt", "").strip()), f"{prefix} needs a prompt")
        check(isinstance(scenario.get("should_trigger"), bool), f"{prefix} should_trigger must be boolean")
        if isinstance(scenario.get("should_trigger"), bool):
            trigger_values.append(scenario["should_trigger"])
        for key in ("expected_decisions", "forbidden_decisions"):
            value = scenario.get(key)
            check(
                isinstance(value, list)
                and bool(value)
                and all(isinstance(item, str) and item.strip() for item in value),
                f"{prefix} {key} must be a non-empty string list",
            )
    check(len(identifiers) == len(set(identifiers)), "Scenario ids must be unique")
    check(True in trigger_values and False in trigger_values, "Scenario corpus needs trigger and non-trigger cases")
    return len(scenarios)


def validate_repository_hygiene() -> None:
    license_text = load_text("LICENSE")
    check("MIT License" in license_text and "Rethymus" in license_text, "LICENSE must contain MIT grant and copyright holder")
    for relative in (
        "CONTRIBUTING.md",
        "SECURITY.md",
        "AGENTS.md",
        "CHANGELOG.md",
        ".github/workflows/validate.yml",
        ".github/pull_request_template.md",
        ".github/ISSUE_TEMPLATE/config.yml",
    ):
        load_text(relative)

    placeholders = ("TBD", "your-name", "YOUR_USERNAME", "REPLACE_ME")
    scanned = [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.resolve() != Path(__file__).resolve()
        and ".git" not in path.parts
        and path.suffix.lower() in {".md", ".json", ".yaml", ".yml", ".py"}
    ]
    for path in scanned:
        content = path.read_text(encoding="utf-8")
        for placeholder in placeholders:
            check(placeholder not in content, f"Placeholder {placeholder!r} remains in {path.relative_to(ROOT)}")


def main() -> int:
    validate_manifest()
    validate_marketplace()
    validate_skill()
    validate_readmes_and_links()
    scenario_count = validate_scenarios()
    validate_repository_hygiene()
    if ERRORS:
        print(f"Validation failed with {len(ERRORS)} error(s) across {CHECKS} checks:")
        for error in ERRORS:
            print(f"- {error}")
        return 1
    print(f"Validation passed: {CHECKS} checks, 1 skill, bilingual READMEs, {scenario_count} scenarios.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
