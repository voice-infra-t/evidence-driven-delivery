from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def run_script(*args: str, cwd: Path) -> int:
    return subprocess.call([sys.executable, *args], cwd=str(cwd))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_generate_evidence_summary_creates_human_readable_reports(tmp_path: Path):
    release_decision_path = tmp_path / "release-decision.json"
    test_report_path = tmp_path / "test-report.json"
    traceability_matrix_path = tmp_path / "traceability-matrix.json"
    evidence_summary_path = tmp_path / "evidence-summary.md"
    traceability_report_path = tmp_path / "traceability-report.md"

    write_json(
        release_decision_path,
        {
            "release_decision": "releasable",
            "scope": ["simple-decision-service v0.1"],
            "reason": "All release gate conditions passed.",
            "not_in_scope": [
                "external API integration",
                "AI/LLM decision",
                "database persistence",
                "production deployment",
            ],
            "traceability": {
                "summary": {
                    "requirements_total": 1,
                    "requirements_with_tests": 1,
                    "requirements_with_observability": 1,
                    "requirements_with_release_gate": 1,
                    "traceability_status": "complete",
                }
            },
        },
    )
    write_json(
        test_report_path,
        {
            "test_run_id": "tmp-run",
            "result": "PASS",
            "requirements_covered": ["R-001"],
            "risks_mitigated": ["Risk-001"],
            "tests": {"passed": 2, "failed": 0},
        },
    )
    write_json(
        traceability_matrix_path,
        {
            "summary": {
                "requirements_total": 1,
                "requirements_with_tests": 1,
                "requirements_with_observability": 1,
                "requirements_with_release_gate": 1,
                "traceability_status": "complete",
            },
            "requirements": [
                {
                    "requirement_id": "R-001",
                    "title": "Approve high numeric value",
                    "tests": [
                        "tests/test_decision_normal.py::test_decide_approve_90",
                        "tests/test_decision_normal.py::test_decide_approve_80",
                    ],
                    "observability_fields": ["id", "decision"],
                    "release_gate": ["junit_passed"],
                    "coverage": {
                        "has_tests": True,
                        "has_observability_fields": True,
                        "has_release_gate": True,
                    },
                }
            ],
        },
    )

    rc = run_script(
        str(REPO_ROOT / "scripts" / "generate_evidence_summary.py"),
        "--release-decision",
        str(release_decision_path),
        "--test-report",
        str(test_report_path),
        "--traceability-matrix",
        str(traceability_matrix_path),
        "--evidence-summary",
        str(evidence_summary_path),
        "--traceability-report",
        str(traceability_report_path),
        cwd=REPO_ROOT,
    )
    assert rc == 0

    assert evidence_summary_path.exists()
    assert traceability_report_path.exists()

    evidence_summary = evidence_summary_path.read_text(encoding="utf-8")
    traceability_report = traceability_report_path.read_text(encoding="utf-8")

    assert "| Decision | releasable |" in evidence_summary
    assert "| Result | PASS |" in evidence_summary
    assert "| Passed | 2 |" in evidence_summary
    assert "| Traceability | complete |" in evidence_summary

    assert "| Requirements total | 1 |" in traceability_report
    assert "| Status | complete |" in traceability_report
    assert "| R-001 | Approve high numeric value | 2 | yes | yes | complete |" in (
        traceability_report
    )
