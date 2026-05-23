from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .models import DecisionResponse


def build_observation(response: DecisionResponse, input_value: Any) -> dict:
    return {
        "id": response.id,
        "input_value": input_value,
        "decision": response.decision,
        "reason": response.reason,
        "fallback_reason": response.fallback_reason,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

