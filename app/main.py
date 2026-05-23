from __future__ import annotations

from fastapi import FastAPI

from .decision import decide
from .models import DecisionRequest, DecisionResponse

app = FastAPI(
    title="Simple Decision API / シンプル判定 API",
    description=(
        "A minimal API to demonstrate deterministic decision behavior.\n\n"
        "証跡駆動デリバリーを説明するための最小判定 API です。"
    ),
)


@app.post(
    "/decide",
    response_model=DecisionResponse,
    summary="Make a decision / 判定を実行する",
    description=(
        "Input an id and value, then return approve/review/reject/fallback.\n\n"
        "id と value を入力し、approve/review/reject/fallback を返します。"
    ),
)
def create_decision(request: DecisionRequest) -> DecisionResponse:
    return decide(request.id, request.value)

