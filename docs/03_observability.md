# 03: Observability

Evidence-Driven Delivery uses observability evidence to make runtime decisions
explainable.

For every Simple Decision API result, the reference implementation can record:

- `id`
- `input_value`
- `decision`
- `reason`
- `fallback_reason`
- `timestamp`

The implementation is intentionally small:

```text
app.evidence.build_observation
```

The point is the release evidence contract. A release decision is stronger when
the system can explain which input led to which decision and why that decision
was returned.
