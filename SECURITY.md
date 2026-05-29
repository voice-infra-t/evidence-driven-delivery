# Security Policy

## Scope

This repository is a minimal reference implementation of Evidence-Driven
Delivery. It is not a production service template.

## Reporting a Vulnerability

1. Do not open a public issue for suspected security problems.
2. Contact the maintainers through the repository owner contact channel.
3. Include reproducible steps, affected files, and potential impact.

## Handling Sensitive Data

- Do not commit secrets, API keys, access tokens, private certificates, or credentials.
- If sensitive data is committed, rotate or revoke it immediately and remove it from history as needed.

## Security Baseline

- Keep dependencies reviewed and updated.
- Run lint, tests, evidence generation, and the release gate before release decisions.
- Use automated security tooling as a future hardening step.
