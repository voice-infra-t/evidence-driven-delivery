# Evidence-Driven Delivery Demo

**English**  
This repository is a minimal demo of Evidence-Driven Delivery.  
Core message: **Do not release because code is finished; release because evidence is complete.**

**日本語**  
このリポジトリは Evidence-Driven Delivery（証跡駆動デリバリー）の最小デモです。  
中心メッセージ: **コードが完成したからリリースするのではなく、出してよい証跡が揃ったものをリリースする。**

## Purpose / 目的

**English**  
This demo uses a deliberately simple Simple Decision API to show a practical release-quality flow:
`Requirement -> Risk -> Observability -> Test -> Evidence -> Release Gate`.

**日本語**  
このデモは意図的に単純な Simple Decision API を使い、実務で使える品質判断フロー
`Requirement -> Risk -> Observability -> Test -> Evidence -> Release Gate`
を示します。

## Educational Demo Only / 教育・デモ用途のみ

**English**

- Educational/demo only.
- Not for production use.
- This repository is for educational and demonstration purposes only.
- It is not intended for production use.
- Before any production-like use, implement additional security controls, operational design, and compliance review.

**日本語**

- このリポジトリは教育・デモ用途のみを目的としています。
- 本番利用を目的とした実装ではありません。
- 本番相当の利用を行う場合は、追加のセキュリティ対策、運用設計、コンプライアンス確認が必要です。

## Simple Decision API / シンプル判定API

**English**

- Endpoint: `POST /decide`
- Request:
  - `id`: required non-empty string
  - `value`: optional; invalid type is handled as fallback in decision logic
- Response:
  - `decision`: `approve` / `review` / `reject` / `fallback`
  - always includes either `reason` or `fallback_reason`

Decision rules:

- `value >= 80` -> `approve`, `reason = "value >= 80"`
- `50 <= value < 80` -> `review`, `reason = "50 <= value < 80"`
- `value < 50` -> `reject`, `reason = "value < 50"`
- invalid `value` (`null`, `bool`, non-numeric) -> `fallback`, `fallback_reason = "missing_or_invalid_value"`
- missing/empty `id` -> FastAPI/Pydantic validation error

**日本語**

- エンドポイント: `POST /decide`
- 入力:
  - `id`: 必須、空文字不可
  - `value`: 任意。不正型は判定ロジックで fallback 扱い
- 出力:
  - `decision`: `approve` / `review` / `reject` / `fallback`
  - 常に `reason` または `fallback_reason` のどちらかを含む

判定ルール:

- `value >= 80` -> `approve`, `reason = "value >= 80"`
- `50 <= value < 80` -> `review`, `reason = "50 <= value < 80"`
- `value < 50` -> `reject`, `reason = "value < 50"`
- 不正 `value`（`null`、`bool`、数値以外）-> `fallback`, `fallback_reason = "missing_or_invalid_value"`
- `id` 欠損/空文字 -> FastAPI/Pydantic の validation error

## Why Intentionally Simple / なぜ意図的に単純なのか

**English**  
The objective is not domain complexity. The objective is to make evidence and release judgment explicit and repeatable.

**日本語**  
目的はドメインの複雑化ではありません。証跡とリリース判断を明示的かつ再現可能にすることです。

## Evidence-Driven Delivery / 証跡駆動デリバリー

**English**

- Treat runtime/test data as release decision material, not just logs.
- Connect tests, observability, and release criteria end-to-end.
- Make release decisions from evidence state, not implementation confidence.

**日本語**

- 実行データやテスト結果を単なるログではなくリリース判断材料として扱う。
- テスト、観測、リリース条件を一気通貫でつなぐ。
- 実装の感触ではなく証跡の状態でリリース判断を行う。

## ODD Relationship / ODDとの関係

**English**  
This demo follows Observability-Driven Development (ODD): every decision is observable with
`id`, `input_value`, `decision`, `reason`, `fallback_reason`, and `timestamp`.

**日本語**  
このデモは ODD（Observability-Driven Development）に従い、すべての判定を
`id`、`input_value`、`decision`、`reason`、`fallback_reason`、`timestamp`
で観測可能にします。

## CI/CD Flow / CI/CDフロー

```text
Requirement
↓
Risk
↓
Observability
↓
Test
↓
Evidence
↓
Release Gate
```

**English**

- CI:
  - `ruff check .`
  - `pytest --junitxml=evidence/junit.xml`
  - `python scripts/generate_evidence.py`
- CD-like decision step:
  - `python scripts/evaluate_release_gate.py`
  - output: `evidence/release-decision.json`

**日本語**

- CI:
  - `ruff check .`
  - `pytest --junitxml=evidence/junit.xml`
  - `python scripts/generate_evidence.py`
- CD相当の判定ステップ:
  - `python scripts/evaluate_release_gate.py`
  - 出力: `evidence/release-decision.json`

## Local Run (PowerShell) / ローカル実行（PowerShell）

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

## Local Run (bash) / ローカル実行（bash）

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

## Test and Evidence Commands / テストと証跡コマンド

```powershell
ruff check .
pytest --junitxml=evidence/junit.xml
python scripts/generate_evidence.py
python scripts/evaluate_release_gate.py
```

## Try it in your browser / ブラウザで試す

**English**

Because this demo uses FastAPI, you can test the API from the auto-generated Swagger UI.

Start the server:

```powershell
uvicorn app.main:app --reload
```

You should see startup logs similar to:

```text
Uvicorn running on http://127.0.0.1:8000
```

Open:

```text
http://127.0.0.1:8000/docs
```

In Swagger UI:

1. Open `POST /decide`.
2. Click `Try it out`.
3. Edit the request body.
4. Click `Execute`.
5. Check the response body.

Approve example:

Request:

```json
{
  "id": "case-001",
  "value": 85
}
```

Expected response:

```json
{
  "id": "case-001",
  "decision": "approve",
  "reason": "value >= 80",
  "fallback_reason": null
}
```

Fallback example:

Request:

```json
{
  "id": "case-002",
  "value": "abc"
}
```

Expected response:

```json
{
  "id": "case-002",
  "decision": "fallback",
  "reason": null,
  "fallback_reason": "missing_or_invalid_value"
}
```

Validation error example:

Request:

```json
{
  "value": 85
}
```

Expected result:

```text
HTTP 422 validation error
```

`id` is required, so missing `id` triggers FastAPI/Pydantic validation before decision logic runs.

How this browser demo relates to Evidence-Driven Delivery:

- `/decide` shows runtime decision behavior.
- `pytest --junitxml=evidence/junit.xml` verifies the behavior.
- `scripts/generate_evidence.py` converts test output into evidence.
- `scripts/evaluate_release_gate.py` creates release decision from evidence.
- Browser checks confirm behavior; release readiness is decided by evidence and release gate.

**日本語**

このデモは FastAPI を使っているため、自動生成される Swagger UI から API を試せます。

サーバ起動:

```powershell
uvicorn app.main:app --reload
```

起動後の表示例:

```text
Uvicorn running on http://127.0.0.1:8000
```

ブラウザで開くURL:

```text
http://127.0.0.1:8000/docs
```

Swagger UIでの操作:

1. `POST /decide` を開く
2. `Try it out` を押す
3. request body を編集する
4. `Execute` を押す
5. response body を確認する

approve の例:

リクエスト:

```json
{
  "id": "case-001",
  "value": 85
}
```

期待されるレスポンス:

```json
{
  "id": "case-001",
  "decision": "approve",
  "reason": "value >= 80",
  "fallback_reason": null
}
```

fallback の例:

リクエスト:

```json
{
  "id": "case-002",
  "value": "abc"
}
```

期待されるレスポンス:

```json
{
  "id": "case-002",
  "decision": "fallback",
  "reason": null,
  "fallback_reason": "missing_or_invalid_value"
}
```

validation error の例:

リクエスト:

```json
{
  "value": 85
}
```

期待結果:

```text
HTTP 422 validation error
```

`id` は必須なので、`id` 欠損時は判定ロジック実行前に FastAPI/Pydantic の validation error になります。

このブラウザデモと Evidence-Driven Delivery の関係:

- `/decide` は runtime decision behavior を示す
- `pytest --junitxml=evidence/junit.xml` は挙動を検証する
- `scripts/generate_evidence.py` はテスト結果を evidence に変換する
- `scripts/evaluate_release_gate.py` は evidence から release decision を生成する
- ブラウザデモは動作確認であり、release readiness は evidence と release gate で判断する

## Out of Scope / このデモで扱わないこと

**English**

- external API integration
- AI/LLM-based decision
- database persistence
- production deployment orchestration
- organization-specific business workflow

**日本語**

- 外部API連携
- AI/LLMによる判定
- データベース永続化
- 本番デプロイ運用
- 組織固有の業務ワークフロー

## Public Release Checklist / 公開前チェックリスト

**English**  
See [docs/06_public_release_checklist.md](docs/06_public_release_checklist.md) for public-release checks.

**日本語**  
公開前チェック項目は [docs/06_public_release_checklist.md](docs/06_public_release_checklist.md) を参照してください。

## Security / セキュリティ

**English**  
Security reporting guidance is documented in [SECURITY.md](SECURITY.md).

**日本語**  
セキュリティ報告手順は [SECURITY.md](SECURITY.md) を参照してください。

## License / ライセンス

**English**

- This project is licensed under the MIT License.
- See [LICENSE](LICENSE) for full terms.

**日本語**

- このプロジェクトは MIT License のもとで提供されます。
- 詳細は [LICENSE](LICENSE) を参照してください。
