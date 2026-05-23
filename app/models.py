from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class DecisionRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"id": "case-001", "value": 85},
                {"id": "case-002", "value": "abc"},
            ]
        }
    )

    id: str = Field(
        ...,
        description="Unique case id. Must not be blank. / 一意なID。空文字は不可。",
    )
    value: Any | None = Field(
        default=None,
        description=(
            "Decision input value. Invalid types are handled as fallback "
            "in decision logic. / 判定入力値。不正型は判定ロジックで fallback 扱い。"
        ),
    )

    @field_validator("id")
    @classmethod
    def id_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("id must be a non-empty string")
        return v


class DecisionResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "case-001",
                    "decision": "approve",
                    "reason": "value >= 80",
                    "fallback_reason": None,
                },
                {
                    "id": "case-002",
                    "decision": "fallback",
                    "reason": None,
                    "fallback_reason": "missing_or_invalid_value",
                },
            ]
        }
    )

    id: str = Field(..., description="Case id. / 判定対象ID。")
    decision: Literal["approve", "review", "reject", "fallback"] = Field(
        ...,
        description="Decision result. / 判定結果。",
    )
    reason: str | None = Field(
        default=None,
        description="Reason for approve/review/reject. / 通常判定時の理由。",
    )
    fallback_reason: str | None = Field(
        default=None,
        description="Reason for fallback. / fallback時の理由。",
    )
