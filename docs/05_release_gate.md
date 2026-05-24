# 05: Release Gate

Release Gate v0.1

以下を満たす場合のみ `releasable` とする。

1. 正常系テストがすべて PASS
2. fallback系テストがすべて PASS
3. id 欠損時は validation error になる
4. 不正 value は fallback になる
5. bool value は fallback になる
6. すべての判定に `reason` または `fallback_reason` が含まれる
7. `evidence/test-report.json` が生成される
8. `evidence/traceability-matrix.json` が生成され、必要な要件IDをすべて含む
9. `evidence/release-decision.json` が生成され、`release_decision` が `"releasable"` である
