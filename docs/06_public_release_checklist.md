# 06: Public Release Checklist

Use this checklist before publishing artifacts from the private working
repository to the public repository.

## Content Scope

- README and docs are English-first.
- The repository is positioned as a minimal reference implementation.
- The Simple Decision Engine remains intentionally simple.
- No LLM integration, database persistence, external API integration, custom UI,
  HTTP API, or business-domain-specific workflow is added.

## Evidence Scope

- `evidence/junit.xml` contains only test result data.
- `evidence/test-report.json` contains no local paths or sensitive values.
- `evidence/traceability-matrix.json` contains only repository-relative test references.
- `evidence/release-decision.json` contains no local paths or sensitive values.

## Repository Safety

- Public files are synced from an allow list only.
- `.git` directories are never copied.
- Private Git history is not pushed to the public repository.
- CI badges and repository links point to the public repository.
- Markdown files remain UTF-8 with LF line endings.

## Security And Quality

- Dependabot alerts are enabled.
- Dependabot security updates are enabled.
- Dependabot version updates are configured for Python dependencies and GitHub Actions.
- CodeQL code scanning is enabled for pull requests and the default branch.
- Secret scanning and push protection are enabled where available.
- Private vulnerability reporting is enabled.

## Search Checks

Before publication, search for:

- private repository names
- local absolute paths
- user profile paths
- API keys
- access tokens
- passwords
- private keys
- internal-only URLs or names

Any uncertain file stays private until it has been reviewed.
