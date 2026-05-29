# 00: Concept

Evidence-Driven Delivery connects delivery signals to a release decision that
can be inspected as an artifact.

The core flow is:

```text
Requirement -> Risk -> Observability -> Test -> Evidence -> Release Gate
```

The Simple Decision API is intentionally small. Its purpose is not domain
complexity. Its purpose is to make the release evidence path explicit:

- Requirements define expected behavior.
- Risks identify what could make the behavior unsafe or untrustworthy.
- Observability fields explain how runtime decisions can be inspected.
- Tests verify the behavior.
- Evidence artifacts record the result.
- The release gate evaluates whether the evidence is complete.

Core message:

> Do not release because the code is finished.
> Release because the evidence is complete.

## Release Decision Evidence

This repository treats the release decision itself as a generated artifact.

The release gate reads test evidence and traceability evidence, then writes:

```text
evidence/release-decision.json
```

That file is the machine-readable release decision evidence for this reference
implementation.
