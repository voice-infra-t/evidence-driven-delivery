# Security Policy

## Scope

**English**

- This repository is an educational/demo project.
- It is not intended for production use.

**日本語**

- このリポジトリは教育・デモ用途のプロジェクトです。
- 本番用途は想定していません。

## Reporting a Vulnerability

**English**

1. Do not open a public issue for suspected security problems.
2. Contact the maintainers privately through the repository owner contact channel.
3. Include reproducible steps, affected files, and potential impact.

**日本語**

1. セキュリティ問題の疑いがある場合は、公開Issueを作成しないでください。
2. リポジトリ所有者の連絡手段で、メンテナへ非公開で連絡してください。
3. 再現手順、影響ファイル、想定される影響範囲を共有してください。

## Handling Secrets

**English**

- Do not commit secrets, API keys, tokens, private certificates, or credentials.
- If a secret is committed, rotate/revoke it immediately and remove it from history as needed.

**日本語**

- 秘密情報（APIキー、トークン、証明書、認証情報など）をコミットしないでください。
- 秘密情報が混入した場合は、即時に失効・ローテーションし、必要に応じて履歴から削除してください。

## Security Baseline

**English**

- Keep dependencies updated and pinned appropriately.
- Run tests and evidence generation before release decisions.
- Use automated security tooling as future hardening steps.

**日本語**

- 依存関係は更新状況を管理し、必要に応じてバージョンを固定してください。
- リリース判断前にテストと証跡生成を実行してください。
- 自動セキュリティツールの導入を今後の強化項目として扱ってください。
