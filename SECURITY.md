# Security Policy

## Scope

This repository is a minimal reference implementation of Evidence-Driven
Delivery. It is not a production service template.

## Reporting a Vulnerability

1. Do not open a public issue for suspected security problems.
2. Use GitHub private vulnerability reporting when available.
3. Otherwise, contact the maintainers through the repository owner contact channel.
4. Include reproducible steps, affected files, and potential impact.

## Handling Sensitive Data

- Do not commit secrets, API keys, access tokens, private certificates, or credentials.
- If sensitive data is committed, rotate or revoke it immediately and remove it from history as needed.

## Security Baseline

- Keep dependencies reviewed and updated.
- Run lint, tests, evidence generation, and the release gate before release decisions.
- Keep Dependabot updates enabled for Python dependencies and GitHub Actions.
- Keep CodeQL code scanning enabled for pull requests and the default branch.
- Keep repository secret scanning and push protection enabled where available.
- Keep private vulnerability reporting enabled for coordinated disclosure.
