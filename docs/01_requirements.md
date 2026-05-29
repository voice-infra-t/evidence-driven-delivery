# 01: Requirements

The Simple Decision API has six requirements.

| ID | Requirement |
|---|---|
| R-001 | A numeric value greater than or equal to 80 returns `approve`. |
| R-002 | A numeric value from 50 through 79 returns `review`. |
| R-003 | A numeric value less than 50 returns `reject`. |
| R-004 | A missing, boolean, or non-numeric value returns `fallback`. |
| R-005 | A missing or blank `id` is rejected by validation before decision logic runs. |
| R-006 | Every decision response includes either `reason` or `fallback_reason`. |

The detailed executable requirement map is maintained in
[`requirements.yml`](../requirements.yml). That file connects each requirement
to risks, tests, observability fields, and release gate criteria.
