from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.decision import decide
from app.evidence import build_observation
from app.main import make_decision
from app.models import DecisionInput, DecisionResult

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_decide_fallback_none():
    resp = decide("case-001", None)
    assert resp.decision == "fallback"
    assert resp.fallback_reason == "missing_or_invalid_value"
    assert resp.reason is None


def test_decide_fallback_string():
    resp = decide("case-001", "abc")
    assert resp.decision == "fallback"
    assert resp.fallback_reason == "missing_or_invalid_value"


def test_decide_fallback_bool():
    resp = decide("case-001", True)
    assert resp.decision == "fallback"
    assert resp.fallback_reason == "missing_or_invalid_value"


def test_validation_error_when_id_missing():
    with pytest.raises(ValidationError):
        DecisionInput.model_validate({"value": 80})


def test_validation_error_when_id_empty():
    with pytest.raises(ValidationError):
        DecisionInput.model_validate({"id": "", "value": 80})


def test_make_decision_validates_and_returns_result():
    result = make_decision({"id": "case-001", "value": 80})
    assert result.decision == "approve"
    assert result.reason == "value >= 80"


def test_cli_reads_json_and_writes_decision():
    result = subprocess.run(
        [sys.executable, "-m", "app.main", "--id", "case-001", "--value", "85"],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["id"] == "case-001"
    assert payload["decision"] == "approve"


def test_decision_and_fallback_reason_presence():
    responses = [
        decide("case-001", 90),
        decide("case-002", 70),
        decide("case-003", 30),
        decide("case-004", None),
    ]
    for response in responses:
        has_reason = response.reason is not None or response.fallback_reason is not None
        assert has_reason


def test_observation_contains_required_fields():
    response = DecisionResult(
        id="case-001",
        decision="approve",
        reason="value >= 80",
    )
    obs = build_observation(response, 85)
    assert set(obs.keys()) == {"id", "input_value", "decision", "reason", "fallback_reason", "timestamp"}
    assert obs["id"] == "case-001"
    assert obs["input_value"] == 85
    assert obs["decision"] == "approve"
    assert obs["reason"] == "value >= 80"
    assert obs["fallback_reason"] is None
    assert isinstance(obs["timestamp"], str)
