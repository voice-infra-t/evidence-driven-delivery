from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from typing import Any, TextIO

from pydantic import ValidationError

from .decision import decide
from .models import DecisionInput, DecisionResult


def load_payload(text: str) -> dict[str, Any]:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON input: {exc.msg}") from exc

    if not isinstance(payload, dict):
        raise ValueError("decision input must be a JSON object")

    return payload


def parse_value(text: str) -> Any:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def make_decision(payload: dict[str, Any]) -> DecisionResult:
    decision_input = DecisionInput.model_validate(payload)
    return decide(decision_input.id, decision_input.value)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the local Simple Decision Engine with a JSON input object."
    )
    parser.add_argument(
        "payload",
        nargs="?",
        help='JSON input, for example: {"id":"case-001","value":85}. Reads stdin when omitted.',
    )
    parser.add_argument("--id", dest="case_id", help="Case id. Must not be blank.")
    parser.add_argument(
        "--value",
        help="Decision value. Parsed as JSON when possible, otherwise treated as a string.",
    )
    return parser.parse_args(argv)


def main(
    argv: Sequence[str] | None = None,
    stdin: TextIO = sys.stdin,
    stdout: TextIO = sys.stdout,
    stderr: TextIO = sys.stderr,
) -> int:
    args = parse_args(argv)

    try:
        if args.case_id is not None:
            if args.payload is not None:
                raise ValueError("provide either JSON input or --id/--value arguments, not both")
            payload: dict[str, Any] = {"id": args.case_id}
            if args.value is not None:
                payload["value"] = parse_value(args.value)
        else:
            input_text = args.payload if args.payload is not None else stdin.read()
            payload = load_payload(input_text)

        response = make_decision(payload)
    except (ValueError, ValidationError) as exc:
        print(f"error: {exc}", file=stderr)
        return 2

    stdout.write(response.model_dump_json(indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
