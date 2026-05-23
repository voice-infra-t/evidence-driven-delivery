# 04: Tests

- TC-001: value=90 → approve
- TC-002: value=80 → approve
- TC-003: value=70 → review
- TC-004: value=50 → review
- TC-005: value=30 → reject
- TC-006: value=null → fallback
- TC-007: value="abc" → fallback
- TC-008: value=true → fallback
- TC-009: idなし → validation error
- TC-010: 空id → validation error
- TC-011: すべての判定に `reason` または `fallback_reason` が含まれる
- TC-012: `build_observation` が観測項目を含む
