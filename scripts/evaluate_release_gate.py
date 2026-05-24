from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_REQUIREMENTS = [
    "R-001",
    "R-002",
    "R-003",
    "R-004",
    "R-005",
    "R-006",
]


def load_report(report_path: Path) -> dict:
    return json.loads(report_path.read_text(encoding="utf-8"))


def missing_traceability() -> dict:
    return {
        "summary": {
            "requirements_total": 0,
            "requirements_with_tests": 0,
            "requirements_with_observability": 0,
            "requirements_with_release_gate": 0,
            "traceability_status": "missing",
        },
        "requirements": [],
    }


def load_traceability(traceability_path: Path) -> dict:
    if not traceability_path.exists():
        return missing_traceability()

    return json.loads(traceability_path.read_text(encoding="utf-8"))


def traceability_covers_required_requirements(traceability: dict) -> bool:
    traced_requirements = {
        requirement.get("requirement_id") for requirement in traceability.get("requirements", [])
    }
    return all(req in traced_requirements for req in REQUIRED_REQUIREMENTS)


def is_releasable(report: dict, traceability: dict) -> bool:
    tests = report.get("tests", {})
    if report.get("result") != "PASS":
        return False
    if tests.get("failed") != 0:
        return False

    requirements = set(report.get("requirements_covered", []))
    if not all(req in requirements for req in REQUIRED_REQUIREMENTS):
        return False

    traceability_summary = traceability.get("summary", {})
    if traceability_summary.get("traceability_status") != "complete":
        return False

    if not traceability_covers_required_requirements(traceability):
        return False

    return True


def evaluate_release_gate(report_path: Path, output_path: Path, traceability_path: Path) -> dict:
    report = load_report(report_path)
    traceability = load_traceability(traceability_path)
    traceability_summary = traceability.get("summary", {})
    releasable = is_releasable(report, traceability)

    payload = {
        "release_decision": "releasable" if releasable else "not_releasable",
        "scope": [
            "simple-decision-service v0.1",
        ],
        "reason": (
            "All release gate conditions passed."
            if releasable
            else "Release gate conditions not met."
        ),
        "not_in_scope": [
            "external API integration",
            "AI/LLM decision",
            "database persistence",
            "production deployment",
        ],
        "traceability": {
            "summary": traceability_summary,
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="evidence/test-report.json",
        help="Path to test evidence report JSON",
    )
    parser.add_argument(
        "--output",
        default="evidence/release-decision.json",
        help="Path to release gate output",
    )
    parser.add_argument(
        "--traceability",
        default="evidence/traceability-matrix.json",
        help="Path to traceability matrix JSON",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    evaluate_release_gate(Path(args.input), Path(args.output), Path(args.traceability))


if __name__ == "__main__":
    main()

