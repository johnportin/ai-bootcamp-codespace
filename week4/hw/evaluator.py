from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

CriterionInput = Mapping[str, Any]


@dataclass
class CriterionResult:
    name: str
    passed: bool
    details: str


def load_log_entry(path: Path) -> CriterionInput:
    with path.open("r", encoding="utf-8") as f_in:
        return json.load(f_in)


def get_user_prompt(entry: CriterionInput) -> str:
    for message in entry.get("messages", []):
        for part in message.get("parts", []):
            if part.get("part_kind") == "user-prompt":
                return part.get("content", "")
    return ""


def follows_direction(entry: CriterionInput) -> CriterionResult:
    messages: Iterable[Mapping[str, Any]] = entry.get("messages", [])
    output: str = entry.get("output", "") or ""

    used_tools = entry_made_tool_calls(entry)
    has_url = bool(re.search(r"https?://\S+", output))

    passed = used_tools and has_url
    missing = []
    if not used_tools:
        missing.append("no tool calls were recorded")
    if not has_url:
        missing.append("no citation/url found in output")

    details = (
        "Directions followed: used tools and cited a URL."
        if passed
        else "Directions missed: " + "; ".join(missing)
    )

    return CriterionResult(
        name="follows direction",
        passed=passed,
        details=details,
    )


def answer_is_relevant(entry: CriterionInput) -> CriterionResult:
    prompt = get_user_prompt(entry).lower()
    output = (entry.get("output", "") or "").lower()

    prompt_terms = {
        term
        for term in re.findall(r"[a-z]+", prompt)
        if len(term) > 3
    }

    overlapping_terms = {term for term in prompt_terms if term in output}
    coverage = (len(overlapping_terms) / len(prompt_terms)) if prompt_terms else 0

    passed = bool(overlapping_terms) and coverage >= 0.25

    if not prompt_terms:
        details = "No user prompt detected; cannot evaluate relevance."
    elif not output.strip():
        details = "No output to evaluate."
    elif passed:
        details = f"Output references prompt terms: {', '.join(sorted(overlapping_terms))}."
    else:
        details = "Output lacks sufficient overlap with important prompt terms."

    return CriterionResult(
        name="answer is relevant",
        passed=passed,
        details=details,
    )


def entry_made_tool_calls(entry: CriterionInput) -> bool:
    messages: Iterable[Mapping[str, Any]] = entry.get("messages", [])
    return any(
        part.get("part_kind") == "tool-call"
        for message in messages
        for part in message.get("parts", [])
    )


def used_tools(entry: CriterionInput) -> CriterionResult:
    used = entry_made_tool_calls(entry)
    details = (
        "Tool calls detected in log."
        if used
        else "No tool calls detected."
    )
    return CriterionResult(
        name="tool usage",
        passed=used,
        details=details,
    )


def evaluate_log(path: Path) -> list[CriterionResult]:
    entry = load_log_entry(path)
    return [
        used_tools(entry),
        follows_direction(entry),
        answer_is_relevant(entry),
    ]


def iter_log_files(logs_dir: Path) -> Iterable[Path]:
    if not logs_dir.exists():
        return []
    return sorted(
        p for p in logs_dir.iterdir()
        if p.suffix == ".json" and p.is_file()
    )


def main() -> None:
    logs_dir = Path("logs")
    log_files = list(iter_log_files(logs_dir))

    if not log_files:
        print("No log files found in ./logs")
        return

    for log_path in log_files:
        print(f"\nEvaluating {log_path.name}")
        for result in evaluate_log(log_path):
            status = "PASS" if result.passed else "FAIL"
            print(f"  [{status}] {result.name}: {result.details}")


if __name__ == "__main__":
    main()
