# 02: Risks

The release gate is designed around risks that would make a release decision
untrustworthy.

| ID | Risk |
|---|---|
| Risk-001 | Missing or invalid values are processed as normal business decisions. |
| Risk-002 | Values that require review are incorrectly approved. |
| Risk-003 | Missing case identifiers make later traceability impossible. |
| Risk-004 | Decision reasons are not recorded. |
| Risk-005 | The service is released without test evidence. |

Each risk is mapped to one or more requirements in
[`requirements.yml`](../requirements.yml). The generated traceability matrix
keeps that mapping visible to the release gate.
