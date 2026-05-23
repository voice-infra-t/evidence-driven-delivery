# 07: Positioning

## Evidence-Driven Delivery is not a replacement

Evidence-Driven Delivery does not replace Agile, TDD, ODD, DevOps, CI/CD, SRE, DevSecOps, Quality Gates, or Assurance Cases.

It treats the outputs of those practices as release decision evidence.

## Relationship to existing practices

| Practice | Produces | Used by Evidence-Driven Delivery as |
|---|---|---|
| Agile | prioritized requirements and feedback | requirement context |
| TDD | executable tests | behavior evidence |
| ODD | observable runtime fields | observability evidence |
| CI | build and test results | verification evidence |
| CD | deployable artifacts and deployment records | delivery evidence |
| DevSecOps | security and supply-chain checks | security evidence |
| SRE | SLOs, incidents, operational signals | reliability evidence |
| Quality Gate | pass/fail criteria | gate evidence |
| Assurance Case | structured argument and supporting evidence | assurance evidence |

## What is new here

The novelty is not each individual practice.

The novelty is the explicit connection:

Requirement -> Risk -> Observability -> Test -> Evidence -> Release Gate

Evidence-Driven Delivery connects signals from existing practices to a release decision.

## Release decision as a first-class artifact

This demo treats `evidence/release-decision.json` as a first-class artifact.

It describes:

- what is releasable
- why it is releasable
- what is not in scope

The release decision is not just an implicit human judgment. It is represented as a machine-readable artifact.
