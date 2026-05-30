from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def run_script(*args: str, cwd: Path) -> int:
    return subprocess.call([sys.executable, *args], cwd=str(cwd))


def write_complete_traceability(path: Path) -> None:
    requirement_ids = ["R-001", "R-002", "R-003", "R-004", "R-005", "R-006"]
    path.write_text(
        json.dumps(
            {
                "summary": {
                    "requirements_total": 6,
                    "requirements_with_tests": 6,
                    "requirements_with_observability": 6,
                    "requirements_with_release_gate": 6,
                    "traceability_status": "complete",
                },
                "requirements": [
                    {
                        "requirement_id": requirement_id,
                        "coverage": {
                            "has_tests": True,
                            "has_observability_fields": True,
                            "has_release_gate": True,
                        },
                    }
                    for requirement_id in requirement_ids
                ],
            }
        ),
        encoding="utf-8",
    )


def test_generate_evidence_creates_report(tmp_path: Path):
    junit = tmp_path / "junit.xml"
    junit.write_text(
        "<testsuite tests='2' failures='0' errors='0' skipped='0'>"
        "<testcase classname='t' name='tc1'/>"
        "<testcase classname='t' name='tc2'/>"
        "</testsuite>",
        encoding="utf-8",
    )

    output = tmp_path / "test-report.json"
    rc = run_script(
        str(REPO_ROOT / "scripts" / "generate_evidence.py"),
        "--junit",
        str(junit),
        "--output",
        str(output),
        "--test-run-id",
        "tmp-run",
        cwd=REPO_ROOT,
    )
    assert rc == 0

    report = json.loads(output.read_text(encoding="utf-8"))
    assert output.exists()
    assert report["test_run_id"] == "tmp-run"
    assert report["result"] == "PASS"
    assert report["tests"]["passed"] == 2
    assert report["tests"]["failed"] == 0
    assert report["requirements_covered"] == [
        "R-001",
        "R-002",
        "R-003",
        "R-004",
        "R-005",
        "R-006",
    ]


def test_generate_traceability_matrix_creates_matrix(tmp_path: Path):
    requirements_path = tmp_path / "requirements.yml"
    requirements_path.write_text(
        """
requirements:
  - id: R-001
    title: Example requirement
    tests:
      - tests/test_decision_normal.py::test_decide_approve_90
    observability_fields:
      - id
      - decision
    release_gate:
      - junit_passed
""".lstrip(),
        encoding="utf-8",
    )

    output = tmp_path / "traceability-matrix.json"
    rc = run_script(
        str(REPO_ROOT / "scripts" / "generate_traceability_matrix.py"),
        "--requirements",
        str(requirements_path),
        "--output",
        str(output),
        cwd=REPO_ROOT,
    )
    assert rc == 0

    matrix = json.loads(output.read_text(encoding="utf-8"))
    assert output.exists()
    assert matrix["summary"]["requirements_total"] == 1
    assert matrix["summary"]["requirements_with_tests"] == 1
    assert matrix["summary"]["requirements_with_observability"] == 1
    assert matrix["summary"]["requirements_with_release_gate"] == 1
    assert matrix["summary"]["traceability_status"] == "complete"
    assert matrix["requirements"][0]["requirement_id"] == "R-001"


def test_evaluate_release_gate_creates_release_decision(tmp_path: Path):
    report_path = tmp_path / "test-report.json"
    report_path.write_text(
        json.dumps(
            {
                "test_run_id": "tmp-run",
                "result": "PASS",
                "requirements_covered": [
                    "R-001",
                    "R-002",
                    "R-003",
                    "R-004",
                    "R-005",
                    "R-006",
                ],
                "risks_mitigated": [
                    "Risk-001",
                    "Risk-002",
                    "Risk-003",
                    "Risk-004",
                    "Risk-005",
                ],
                "tests": {"passed": 2, "failed": 0},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    decision_path = tmp_path / "release-decision.json"
    traceability_path = tmp_path / "traceability-matrix.json"
    write_complete_traceability(traceability_path)

    rc = run_script(
        str(REPO_ROOT / "scripts" / "evaluate_release_gate.py"),
        "--input",
        str(report_path),
        "--output",
        str(decision_path),
        "--traceability",
        str(traceability_path),
        cwd=REPO_ROOT,
    )
    assert rc == 0

    decision_payload = json.loads(decision_path.read_text(encoding="utf-8"))
    assert decision_path.exists()
    assert decision_payload["release_decision"] == "releasable"
    assert decision_payload["scope"] == ["simple-decision-engine v0.1"]
    assert decision_payload["reason"] == "All release gate conditions passed."
    assert decision_payload["traceability"]["summary"]["traceability_status"] == "complete"


def test_evaluate_release_gate_blocks_missing_traceability(tmp_path: Path):
    report_path = tmp_path / "test-report.json"
    report_path.write_text(
        json.dumps(
            {
                "test_run_id": "tmp-run",
                "result": "PASS",
                "requirements_covered": [
                    "R-001",
                    "R-002",
                    "R-003",
                    "R-004",
                    "R-005",
                    "R-006",
                ],
                "risks_mitigated": [
                    "Risk-001",
                    "Risk-002",
                    "Risk-003",
                    "Risk-004",
                    "Risk-005",
                ],
                "tests": {"passed": 2, "failed": 0},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    decision_path = tmp_path / "release-decision.json"
    rc = run_script(
        str(REPO_ROOT / "scripts" / "evaluate_release_gate.py"),
        "--input",
        str(report_path),
        "--output",
        str(decision_path),
        "--traceability",
        str(tmp_path / "missing-traceability.json"),
        cwd=REPO_ROOT,
    )
    assert rc == 0

    decision_payload = json.loads(decision_path.read_text(encoding="utf-8"))
    assert decision_payload["release_decision"] == "not_releasable"
    assert decision_payload["traceability"]["summary"]["traceability_status"] == "missing"


def test_evaluate_release_gate_blocks_incomplete_traceability_scope(tmp_path: Path):
    report_path = tmp_path / "test-report.json"
    report_path.write_text(
        json.dumps(
            {
                "test_run_id": "tmp-run",
                "result": "PASS",
                "requirements_covered": [
                    "R-001",
                    "R-002",
                    "R-003",
                    "R-004",
                    "R-005",
                    "R-006",
                ],
                "risks_mitigated": [
                    "Risk-001",
                    "Risk-002",
                    "Risk-003",
                    "Risk-004",
                    "Risk-005",
                ],
                "tests": {"passed": 2, "failed": 0},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    traceability_path = tmp_path / "traceability-matrix.json"
    traceability_path.write_text(
        json.dumps(
            {
                "summary": {
                    "requirements_total": 4,
                    "requirements_with_tests": 4,
                    "requirements_with_observability": 4,
                    "requirements_with_release_gate": 4,
                    "traceability_status": "complete",
                },
                "requirements": [
                    {"requirement_id": "R-001"},
                    {"requirement_id": "R-002"},
                    {"requirement_id": "R-003"},
                    {"requirement_id": "R-004"},
                ],
            }
        ),
        encoding="utf-8",
    )

    decision_path = tmp_path / "release-decision.json"
    rc = run_script(
        str(REPO_ROOT / "scripts" / "evaluate_release_gate.py"),
        "--input",
        str(report_path),
        "--output",
        str(decision_path),
        "--traceability",
        str(traceability_path),
        cwd=REPO_ROOT,
    )
    assert rc == 0

    decision_payload = json.loads(decision_path.read_text(encoding="utf-8"))
    assert decision_payload["release_decision"] == "not_releasable"


def test_release_scripts_exist():
    assert (REPO_ROOT / "scripts" / "generate_evidence.py").exists()
    assert (REPO_ROOT / "scripts" / "generate_traceability_matrix.py").exists()
    assert (REPO_ROOT / "scripts" / "evaluate_release_gate.py").exists()
    assert (REPO_ROOT / "scripts" / "generate_evidence_summary.py").exists()
