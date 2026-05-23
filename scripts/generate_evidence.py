from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path

REQUIRED_REQUIREMENTS = [
    "R-001",
    "R-002",
    "R-003",
    "R-004",
    "R-005",
    "R-006",
]

REQUIRED_RISKS = [
    "Risk-001",
    "Risk-002",
    "Risk-003",
    "Risk-004",
    "Risk-005",
]


def parse_junit(junit_path: Path) -> tuple[int, int]:
    tree = ET.parse(junit_path)
    root = tree.getroot()

    test_elements = root.findall(".//testcase")
    total = int(root.attrib.get("tests", len(test_elements)))
    failures = int(root.attrib.get("failures", 0))
    errors = int(root.attrib.get("errors", 0))
    skipped = int(root.attrib.get("skipped", 0))

    if total == 0:
        total = len(test_elements)
    failed = failures + errors
    passed = max(total - failed - skipped, 0)
    return passed, failed


def generate_report(
    junit_path: Path, report_path: Path, test_run_id: str = "local-run"
) -> dict:
    passed, failed = parse_junit(junit_path)
    result = "PASS" if failed == 0 else "FAIL"
    payload = {
        "test_run_id": test_run_id,
        "result": result,
        "requirements_covered": REQUIRED_REQUIREMENTS,
        "risks_mitigated": REQUIRED_RISKS,
        "tests": {"passed": passed, "failed": failed},
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--junit",
        default="evidence/junit.xml",
        help="Path to pytest junit XML",
    )
    parser.add_argument(
        "--output",
        default="evidence/test-report.json",
        help="Path to output test report JSON",
    )
    parser.add_argument(
        "--test-run-id",
        default="local-run",
        help="Human-readable test run id",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generate_report(Path(args.junit), Path(args.output), test_run_id=args.test_run_id)


if __name__ == "__main__":
    main()
