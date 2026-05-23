from __future__ import annotations

from app.decision import decide


def test_decide_approve_90():
    resp = decide("case-001", 90)
    assert resp.decision == "approve"
    assert resp.reason == "value >= 80"
    assert resp.fallback_reason is None


def test_decide_approve_80():
    resp = decide("case-001", 80)
    assert resp.decision == "approve"
    assert resp.reason == "value >= 80"


def test_decide_review_70():
    resp = decide("case-001", 70)
    assert resp.decision == "review"
    assert resp.reason == "50 <= value < 80"


def test_decide_review_50():
    resp = decide("case-001", 50)
    assert resp.decision == "review"
    assert resp.reason == "50 <= value < 80"


def test_decide_reject_30():
    resp = decide("case-001", 30)
    assert resp.decision == "reject"
    assert resp.reason == "value < 50"

