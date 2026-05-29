from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def markdown_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    return str(value)


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def complete_missing(value: bool) -> str:
    return "complete" if value else "missing"


def write_markdown(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")


def build_evidence_summary(release_decision: dict[str, Any], test_report: dict[str, Any]) -> str:
    traceability_summary = release_decision.get("traceability", {}).get("summary", {})
    tests = test_report.get("tests", {})

    not_in_scope = release_decision.get("not_in_scope", [])
    not_in_scope_lines = "\n".join(f"- {item}" for item in not_in_scope)

    return f"""# Evidence Summary

## Release Decision

| Field | Value |
|---|---|
| Decision | {markdown_value(release_decision.get("release_decision"))} |
| Scope | {markdown_value(release_decision.get("scope", []))} |
| Reason | {markdown_value(release_decision.get("reason"))} |
| Traceability | {markdown_value(traceability_summary.get("traceability_status"))} |

## Test Summary

| Field | Value |
|---|---:|
| Result | {markdown_value(test_report.get("result"))} |
| Passed | {markdown_value(tests.get("passed", 0))} |
| Failed | {markdown_value(tests.get("failed", 0))} |
| Requirements covered | {len(test_report.get("requirements_covered", []))} |
| Risks mitigated | {len(test_report.get("risks_mitigated", []))} |

## Not in Scope

{not_in_scope_lines}

## Evidence Artifacts

| Artifact | Purpose |
|---|---|
| [release-decision.json](release-decision.json) | Machine-readable release decision |
| [test-report.json](test-report.json) | Normalized test execution evidence |
| [traceability-matrix.json](traceability-matrix.json) | Machine-readable traceability matrix |
| [traceability-report.md](traceability-report.md) | Human-readable traceability report |
| [junit.xml](junit.xml) | Raw pytest JUnit result |
"""


def requirement_status(requirement: dict[str, Any]) -> str:
    coverage = requirement.get("coverage", {})
    is_complete = (
        bool(coverage.get("has_tests"))
        and bool(coverage.get("has_observability_fields"))
        and bool(coverage.get("has_release_gate"))
    )
    return complete_missing(is_complete)


def build_traceability_report(traceability: dict[str, Any]) -> str:
    summary = traceability.get("summary", {})
    requirements = traceability.get("requirements", [])

    rows = []
    details = []
    for requirement in requirements:
        coverage = requirement.get("coverage", {})
        tests = requirement.get("tests", [])
        has_observability = bool(coverage.get("has_observability_fields"))
        has_release_gate = bool(coverage.get("has_release_gate"))
        requirement_id = markdown_value(requirement.get("requirement_id"))
        title = markdown_value(requirement.get("title"))
        status = requirement_status(requirement)

        rows.append(
            "| "
            f"{requirement_id} | "
            f"{title} | "
            f"{len(tests)} | "
            f"{yes_no(has_observability)} | "
            f"{yes_no(has_release_gate)} | "
            f"{status} |"
        )

        detail_lines = "\n".join(f"- `{test}`" for test in tests) or "- No tests mapped."
        details.append(f"### {requirement_id}: {title}\n\n{detail_lines}")

    requirement_rows = "\n".join(rows)
    detail_sections = "\n\n".join(details)

    return f"""# Traceability Report

## Summary

| Metric | Value |
|---|---:|
| Requirements total | {markdown_value(summary.get("requirements_total", 0))} |
| With tests | {markdown_value(summary.get("requirements_with_tests", 0))} |
| With observability | {markdown_value(summary.get("requirements_with_observability", 0))} |
| With release gate | {markdown_value(summary.get("requirements_with_release_gate", 0))} |
| Status | {markdown_value(summary.get("traceability_status"))} |

## Requirement Coverage

| Requirement | Title | Tests | Observability | Release Gate | Status |
|---|---|---:|---|---|---|
{requirement_rows}

## Test Mapping Details

{detail_sections}
"""


def generate_evidence_summary(
    release_decision_path: Path,
    test_report_path: Path,
    traceability_matrix_path: Path,
    evidence_summary_path: Path,
    traceability_report_path: Path,
) -> None:
    release_decision = load_json(release_decision_path)
    test_report = load_json(test_report_path)
    traceability = load_json(traceability_matrix_path)

    write_markdown(evidence_summary_path, build_evidence_summary(release_decision, test_report))
    write_markdown(traceability_report_path, build_traceability_report(traceability))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--release-decision",
        default="evidence/release-decision.json",
        help="Path to release decision JSON",
    )
    parser.add_argument(
        "--test-report",
        default="evidence/test-report.json",
        help="Path to normalized test report JSON",
    )
    parser.add_argument(
        "--traceability-matrix",
        default="evidence/traceability-matrix.json",
        help="Path to traceability matrix JSON",
    )
    parser.add_argument(
        "--evidence-summary",
        default="evidence/evidence-summary.md",
        help="Path to human-readable evidence summary Markdown",
    )
    parser.add_argument(
        "--traceability-report",
        default="evidence/traceability-report.md",
        help="Path to human-readable traceability report Markdown",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generate_evidence_summary(
        Path(args.release_decision),
        Path(args.test_report),
        Path(args.traceability_matrix),
        Path(args.evidence_summary),
        Path(args.traceability_report),
    )


if __name__ == "__main__":
    main()
