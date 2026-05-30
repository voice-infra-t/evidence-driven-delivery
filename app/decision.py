from __future__ import annotations

from typing import Any

from .models import DecisionResult


def decide(case_id: str, value: Any) -> DecisionResult:
    """
    Make a deterministic decision with strict fallback handling for invalid values.
    """

    if isinstance(value, bool) or value is None or not isinstance(value, (int, float)):
        return DecisionResult(
            id=case_id,
            decision="fallback",
            reason=None,
            fallback_reason="missing_or_invalid_value",
        )

    if value >= 80:
        return DecisionResult(
            id=case_id,
            decision="approve",
            reason="value >= 80",
            fallback_reason=None,
        )

    if value >= 50:
        return DecisionResult(
            id=case_id,
            decision="review",
            reason="50 <= value < 80",
            fallback_reason=None,
        )

    return DecisionResult(
        id=case_id,
        decision="reject",
        reason="value < 50",
        fallback_reason=None,
    )

