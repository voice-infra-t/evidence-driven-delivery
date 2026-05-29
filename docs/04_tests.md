# 04: Tests

The tests verify normal decisions, fallback decisions, validation behavior, and
evidence support code.

| ID | Test intent |
|---|---|
| TC-001 | `value=90` returns `approve`. |
| TC-002 | `value=80` returns `approve`. |
| TC-003 | `value=70` returns `review`. |
| TC-004 | `value=50` returns `review`. |
| TC-005 | `value=30` returns `reject`. |
| TC-006 | `value=null` returns `fallback`. |
| TC-007 | `value="abc"` returns `fallback`. |
| TC-008 | `value=true` returns `fallback`. |
| TC-009 | Missing `id` returns a validation error. |
| TC-010 | Blank `id` returns a validation error. |
| TC-011 | Every decision includes `reason` or `fallback_reason`. |
| TC-012 | `build_observation` includes the required observability fields. |

The CI workflow runs pytest with JUnit XML output:

```powershell
pytest --junitxml=evidence/junit.xml
```

The JUnit result is converted into normalized test evidence by:

```powershell
python scripts/generate_evidence.py
```
