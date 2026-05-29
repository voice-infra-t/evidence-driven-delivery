# 07: Positioning

Evidence-Driven Delivery does not replace Agile, TDD, Observability-Driven
Development, DevOps, CI/CD, SRE, DevSecOps, Quality Gates, or Assurance Cases.

It treats the outputs of those practices as release decision evidence.

| Practice | Produces | Used by Evidence-Driven Delivery as |
|---|---|---|
| Agile | prioritized requirements and feedback | requirement context |
| TDD | executable tests | behavior evidence |
| Observability-Driven Development | observable runtime fields | observability evidence |
| CI/CD | build, test, and delivery results | verification and delivery evidence |
| DevSecOps | security and supply-chain checks | security evidence |
| SRE | reliability signals and operational criteria | reliability evidence |
| Quality Gate | pass/fail criteria | release gate evidence |
| Assurance Case | structured argument and supporting evidence | assurance evidence |

## What This Reference Adds

The point is not a new application architecture. The point is the explicit
connection:

```text
Requirement -> Risk -> Observability -> Test -> Evidence -> Release Gate
```

Existing practices produce signals. Evidence-Driven Delivery turns those
signals into a release decision.

## Release Decision as a First-Class Artifact

This reference implementation treats
`evidence/release-decision.json` as a first-class artifact.

It describes:

- what is releasable
- why it is releasable
- what is out of scope

The release decision is not only an implicit human judgment. It is represented
as machine-readable release decision evidence.
