# 06: Public Release Checklist

This checklist is for preparing this repository for public visibility.

## Checklist

- Secrets and sensitive data:
  - No API keys, tokens, credentials, certificates, or private data in repository files, commits, or artifacts.
- License:
  - `LICENSE` file exists and is consistent with `README.md` license section.
- Non-production use statement:
  - README clearly states educational/demo only and not for production use.
- Dependency hygiene:
  - Dependencies are reviewed, version constraints are intentional, and unnecessary packages are removed.
- Evidence file handling:
  - Keep only safe, non-sensitive sample/generated evidence.
  - Validate that evidence files do not contain secrets or private operational information.

## Future Work

- Add `pip-audit` to CI for dependency vulnerability checks.
- Add `gitleaks` to CI for secret detection.
- Enable `Dependabot` for dependency update PRs.
- Enable repository-level secret scanning.
