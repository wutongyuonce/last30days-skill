"""Documentation contract for Python CLI and wrapper-only flags."""

from __future__ import annotations

from pathlib import Path

import last30days as cli

ROOT = Path(__file__).resolve().parents[1]
CONFIGURATION = ROOT / "CONFIGURATION.md"
SKILL_MD = ROOT / "skills" / "last30days" / "SKILL.md"


def _parser_flags() -> set[str]:
    parser = cli.build_parser()
    flags: set[str] = set()
    for action in parser._actions:
        flags.update(action.option_strings)
    return flags


def test_configuration_documents_new_safety_flags():
    text = CONFIGURATION.read_text(encoding="utf-8")
    flags = _parser_flags()
    assert "--no-browser-cookies" in flags
    assert "--no-browser-cookies" in text
    assert "--save-dir" in text
    assert "--output" in text


def test_save_is_not_documented_as_python_cli_flag():
    text = CONFIGURATION.read_text(encoding="utf-8")
    assert "--save-dir <path>" in text
    assert "--save " not in text
    assert "`--save`" not in text


def test_agent_is_documented_as_skill_argument_not_python_flag():
    text = SKILL_MD.read_text(encoding="utf-8")
    start = text.index("## Agent Mode (--agent flag)")
    agent_section = text[start:start + 2000]
    assert "If `--agent` appears in ARGUMENTS" in agent_section
    assert "Skill tool" in text


def test_comparison_artifact_contract_documents_actual_paths():
    text = SKILL_MD.read_text(encoding="utf-8")
    comparison_start = text.index("\n## If QUERY_TYPE = COMPARISON\n")
    comparison_section = text[comparison_start:comparison_start + 5000]
    assert "there is no separate merged Markdown raw file" in comparison_section
    assert "[last30days] Comparison artifact set: main={path}; peers={path, ...}" in comparison_section
    assert "Treat that log line as authoritative" in comparison_section

    step_start = text.index("## Step 2.5: Append WebSearch Results to Saved Raw File")
    step_section = text[step_start:step_start + 3500]
    assert "append the same `## WebSearch Supplemental Results` section to every listed per-entity Markdown raw file" in step_section
    assert "do not append Markdown text to `.html` or `.json`" in step_section
