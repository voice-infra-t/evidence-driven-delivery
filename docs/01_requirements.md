# 01: Requirements

- R-001: value が 80 以上なら `approve` を返す
- R-002: value が 50 以上 80 未満なら `review` を返す
- R-003: value が 50 未満なら `reject` を返す
- R-004: value が欠損または不正な場合は `fallback` を返す
- R-005: id が欠損または空の場合は validation error とする
- R-006: すべての判定結果に `reason` または `fallback_reason` を含める
