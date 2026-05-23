from __future__ import annotations

from fastapi.testclient import TestClient

from app.decision import decide
from app.evidence import build_observation
from app.main import app
from app.models import DecisionResponse

client = TestClient(app)


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
    response = client.post("/decide", json={"value": 80})
    assert response.status_code == 422


def test_validation_error_when_id_empty():
    response = client.post("/decide", json={"id": "", "value": 80})
    assert response.status_code == 422


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
    response = DecisionResponse(
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
