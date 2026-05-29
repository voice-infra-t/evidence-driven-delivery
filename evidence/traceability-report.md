# Traceability Report

## Summary

| Metric | Value |
|---|---:|
| Requirements total | 6 |
| With tests | 6 |
| With observability | 6 |
| With release gate | 6 |
| Status | complete |

## Requirement Coverage

| Requirement | Title | Tests | Observability | Release Gate | Status |
|---|---|---:|---|---|---|
| R-001 | Approve high numeric value | 2 | yes | yes | complete |
| R-002 | Review middle numeric value | 2 | yes | yes | complete |
| R-003 | Reject low numeric value | 1 | yes | yes | complete |
| R-004 | Fallback invalid input | 3 | yes | yes | complete |
| R-005 | Validate required id | 2 | yes | yes | complete |
| R-006 | Preserve decision reason | 2 | yes | yes | complete |

## Test Mapping Details

### R-001: Approve high numeric value

- `tests/test_decision_normal.py::test_decide_approve_90`
- `tests/test_decision_normal.py::test_decide_approve_80`

### R-002: Review middle numeric value

- `tests/test_decision_normal.py::test_decide_review_70`
- `tests/test_decision_normal.py::test_decide_review_50`

### R-003: Reject low numeric value

- `tests/test_decision_normal.py::test_decide_reject_30`

### R-004: Fallback invalid input

- `tests/test_decision_fallback.py::test_decide_fallback_none`
- `tests/test_decision_fallback.py::test_decide_fallback_string`
- `tests/test_decision_fallback.py::test_decide_fallback_bool`

### R-005: Validate required id

- `tests/test_decision_fallback.py::test_validation_error_when_id_missing`
- `tests/test_decision_fallback.py::test_validation_error_when_id_empty`

### R-006: Preserve decision reason

- `tests/test_decision_fallback.py::test_decision_and_fallback_reason_presence`
- `tests/test_decision_fallback.py::test_observation_contains_required_fields`
