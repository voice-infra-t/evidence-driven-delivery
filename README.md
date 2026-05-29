# Evidence-Driven Delivery

[![CI](https://github.com/voice-infra-t/evidence-driven-delivery/actions/workflows/ci.yml/badge.svg)](https://github.com/voice-infra-t/evidence-driven-delivery/actions/workflows/ci.yml)

Release decisions as executable evidence.

Evidence-Driven Delivery is a delivery approach that connects requirements,
risks, tests, observability, CI/CD results, and release criteria into
machine-readable release decision evidence.

Core message:

> Do not release because the code is finished.
> Release because the evidence is complete.

## Purpose

This repository is a minimal reference implementation of Evidence-Driven
Delivery. It keeps the application deliberately simple so the evidence flow is
easy to inspect and repeat.

The reference application is the Simple Decision API. It exists to show how a
small deterministic behavior can be connected to requirements, risks,
observability fields, tests, generated evidence artifacts, and a release gate.

```text
Requirement -> Risk -> Observability -> Test -> Evidence -> Release Gate
```

## Scope

Included:

- A small FastAPI service with one decision endpoint.
- Requirements and risks captured as repository files.
- Tests that verify normal, fallback, and validation behavior.
- Evidence generation scripts.
- A traceability matrix from requirements to tests and release criteria.
- A release gate evaluator that writes a machine-readable release decision.
- A GitHub Actions workflow that runs lint, tests, evidence generation, and the release gate.

Deliberately not included:

- LLM integration.
- Database persistence.
- External API integration.
- A custom UI.
- Authentication or authorization.
- Business-domain-specific workflow.
- Production deployment orchestration.

This is a reference implementation for the delivery method, not a production
service template.

## Simple Decision API

Endpoint: `POST /decide`

Request fields:

- `id`: required non-empty string.
- `value`: optional value used by the decision logic.

Response fields:

- `decision`: one of `approve`, `review`, `reject`, or `fallback`.
- `reason`: present for normal decisions.
- `fallback_reason`: present for fallback decisions.

Decision rules:

| Input | Decision | Evidence reason |
|---|---|---|
| `value >= 80` | `approve` | `value >= 80` |
| `50 <= value < 80` | `review` | `50 <= value < 80` |
| `value < 50` | `reject` | `value < 50` |
| missing, boolean, or non-numeric `value` | `fallback` | `missing_or_invalid_value` |
| missing or blank `id` | validation error | rejected before decision logic |

## Evidence Artifacts

The repository treats release readiness as an artifact that can be generated and
reviewed.

- `requirements.yml`: requirements, risks, tests, observability fields, and release gate criteria.
- `evidence/junit.xml`: test execution result from pytest.
- `evidence/test-report.json`: normalized test evidence generated from JUnit XML.
- `evidence/traceability-matrix.json`: requirement-to-test-to-release-gate traceability.
- `evidence/release-decision.json`: release gate output.

`evidence/release-decision.json` is the release decision evidence. It states
whether the current artifact is releasable, why, and what is out of scope.

## Local Setup

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Bash:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

## Verification

Run the same checks locally that the CI workflow runs:

```powershell
ruff check .
pytest --junitxml=evidence/junit.xml
python scripts/generate_evidence.py
python scripts/generate_traceability_matrix.py
python scripts/evaluate_release_gate.py
```

The expected release decision is written to:

```text
evidence/release-decision.json
```

## Example Request

```json
{
  "id": "case-001",
  "value": 85
}
```

Expected response:

```json
{
  "id": "case-001",
  "decision": "approve",
  "reason": "value >= 80",
  "fallback_reason": null
}
```

Fallback example:

```json
{
  "id": "case-002",
  "value": "abc"
}
```

Expected response:

```json
{
  "id": "case-002",
  "decision": "fallback",
  "reason": null,
  "fallback_reason": "missing_or_invalid_value"
}
```

## Documentation

- [docs/00_concept.md](docs/00_concept.md): core concept.
- [docs/01_requirements.md](docs/01_requirements.md): requirements.
- [docs/02_risks.md](docs/02_risks.md): risks.
- [docs/03_observability.md](docs/03_observability.md): observability evidence.
- [docs/04_tests.md](docs/04_tests.md): test coverage.
- [docs/05_release_gate.md](docs/05_release_gate.md): release gate criteria.
- [docs/06_public_release_checklist.md](docs/06_public_release_checklist.md): public release checks.
- [docs/07_positioning.md](docs/07_positioning.md): relationship to existing practices.
- [docs/08_traceability_to_release.md](docs/08_traceability_to_release.md): traceability to release decision evidence.

## Security

Security reporting guidance is documented in [SECURITY.md](SECURITY.md).

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for full
terms.
