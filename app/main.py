from __future__ import annotations

from fastapi import FastAPI

from .decision import decide
from .models import DecisionRequest, DecisionResponse

app = FastAPI(
    title="Simple Decision API",
    description=(
        "A deliberately simple API used by the Evidence-Driven Delivery "
        "reference implementation."
    ),
)


@app.post(
    "/decide",
    response_model=DecisionResponse,
    summary="Make a decision",
    description=(
        "Input an id and value, then return approve, review, reject, or fallback."
    ),
)
def create_decision(request: DecisionRequest) -> DecisionResponse:
    return decide(request.id, request.value)

