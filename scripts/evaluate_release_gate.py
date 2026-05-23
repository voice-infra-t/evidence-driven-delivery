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


def is_releasable(report: dict) -> bool:
    tests = report.get("tests", {})
    if report.get("result") != "PASS":
        return False
    if tests.get("failed") != 0:
        return False

    requirements = set(report.get("requirements_covered", []))
    return all(req in requirements for req in REQUIRED_REQUIREMENTS)


def evaluate_release_gate(report_path: Path, output_path: Path) -> dict:
    report = load_report(report_path)
    releasable = is_releasable(report)

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
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    evaluate_release_gate(Path(args.input), Path(args.output))


if __name__ == "__main__":
    main()

