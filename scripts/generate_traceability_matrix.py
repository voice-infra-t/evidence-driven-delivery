from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

LIST_FIELDS = {
    "acceptance_criteria",
    "risks",
    "tests",
    "observability_fields",
    "release_gate",
}


def parse_key_value(text: str) -> tuple[str, str]:
    key, value = text.split(":", 1)
    return key.strip(), value.strip()


def parse_requirements_yaml(text: str) -> list[dict[str, Any]]:
    # This intentionally supports only the simple requirements.yml shape used here.
    requirements: list[dict[str, Any]] = []
    current_requirement: dict[str, Any] | None = None
    current_list_key: str | None = None

    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.strip().startswith("#"):
            continue

        if raw_line == "requirements:":
            continue

        if raw_line.startswith("  - "):
            key, value = parse_key_value(raw_line[4:])
            current_requirement = {key: value}
            requirements.append(current_requirement)
            current_list_key = None
            continue

        if current_requirement is None:
            raise ValueError("Requirement entries must appear under the 'requirements' list.")

        if raw_line.startswith("    ") and not raw_line.startswith("      - "):
            key, value = parse_key_value(raw_line[4:])
            if key in LIST_FIELDS:
                current_requirement[key] = []
                current_list_key = key
            else:
                current_requirement[key] = value
                current_list_key = None
            continue

        if raw_line.startswith("      - "):
            if current_list_key is None:
                raise ValueError("List item found before a list field.")
            current_requirement[current_list_key].append(raw_line[8:].strip())
            continue

        raise ValueError(f"Unsupported requirements.yml line: {raw_line}")

    return requirements


def load_requirements(requirements_path: Path) -> list[dict[str, Any]]:
    requirements = parse_requirements_yaml(requirements_path.read_text(encoding="utf-8"))

    if not requirements:
        raise ValueError("requirements.yml must contain at least one requirement.")

    return requirements


def has_items(value: Any) -> bool:
    return isinstance(value, list) and len(value) > 0


def build_requirement_entry(requirement: dict[str, Any]) -> dict[str, Any]:
    tests = requirement.get("tests", [])
    observability_fields = requirement.get("observability_fields", [])
    release_gate = requirement.get("release_gate", [])

    coverage = {
        "has_tests": has_items(tests),
        "has_observability_fields": has_items(observability_fields),
        "has_release_gate": has_items(release_gate),
    }

    return {
        "requirement_id": requirement.get("id"),
        "title": requirement.get("title"),
        "tests": tests,
        "observability_fields": observability_fields,
        "release_gate": release_gate,
        "coverage": coverage,
    }


def build_traceability_matrix(requirements: list[dict[str, Any]]) -> dict[str, Any]:
    entries = [build_requirement_entry(requirement) for requirement in requirements]
    total = len(entries)
    requirements_with_tests = sum(1 for entry in entries if entry["coverage"]["has_tests"])
    requirements_with_observability = sum(
        1 for entry in entries if entry["coverage"]["has_observability_fields"]
    )
    requirements_with_release_gate = sum(
        1 for entry in entries if entry["coverage"]["has_release_gate"]
    )

    complete = (
        total > 0
        and requirements_with_tests == total
        and requirements_with_observability == total
        and requirements_with_release_gate == total
    )

    return {
        "summary": {
            "requirements_total": total,
            "requirements_with_tests": requirements_with_tests,
            "requirements_with_observability": requirements_with_observability,
            "requirements_with_release_gate": requirements_with_release_gate,
            "traceability_status": "complete" if complete else "incomplete",
        },
        "requirements": entries,
    }


def generate_traceability_matrix(requirements_path: Path, output_path: Path) -> dict[str, Any]:
    requirements = load_requirements(requirements_path)
    payload = build_traceability_matrix(requirements)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--requirements",
        default="requirements.yml",
        help="Path to requirements YAML",
    )
    parser.add_argument(
        "--output",
        default="evidence/traceability-matrix.json",
        help="Path to output traceability matrix JSON",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generate_traceability_matrix(Path(args.requirements), Path(args.output))


if __name__ == "__main__":
    main()
