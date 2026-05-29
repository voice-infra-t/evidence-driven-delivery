# 05: Release Gate

The release gate evaluates whether the evidence is complete enough to publish a
release decision.

Release Gate v0.1 returns `releasable` only when all criteria pass:

1. All tests pass.
2. Fallback behavior is verified.
3. Missing `id` values are rejected by validation.
4. Invalid `value` inputs return `fallback`.
5. Boolean `value` inputs return `fallback`.
6. Every decision includes `reason` or `fallback_reason`.
7. `evidence/test-report.json` exists and reports `PASS`.
8. `evidence/traceability-matrix.json` exists.
9. The traceability matrix includes all required requirement IDs.
10. `evidence/release-decision.json` is generated with `release_decision` set to `releasable`.

The evaluator is:

```powershell
python scripts/evaluate_release_gate.py
```

The release gate does not prove the application is production-ready. It proves
that the reference implementation has the evidence required by this repository's
release criteria.
