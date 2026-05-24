# 08: Traceability to Release

## English

Evidence-Driven Delivery does not reject traditional requirement traceability.

Traditional traceability is useful because it connects requirements, design, and test cases:

```text
Requirement -> Design -> Test Case
```

However, this is not enough for many modern systems.

Systems that include cloud platforms, AI components, managed services, external APIs, and CI/CD pipelines need traceability that continues beyond test design. Requirements should be connected to CI/CD results, observability, evidence artifacts, and release decisions.

Evidence-Driven Delivery extends traditional traceability into executable delivery evidence:

```text
Requirement -> Risk -> Observability -> Test -> CI/CD Evidence -> Release Decision
```

In this demo, `requirements.yml`, `evidence/traceability-matrix.json`, test evidence, and `evidence/release-decision.json` show that connection as files produced by the delivery flow.

## 日本語

Evidence-Driven Delivery は、従来の要件トレーサビリティを否定するものではありません。

従来のトレーサビリティは、要件・設計・試験項目を接続する点で有効です。

```text
Requirement -> Design -> Test Case
```

しかし、現代のシステムではそれだけでは不十分です。

クラウド、AI、マネージドサービス、外部API、CI/CD を含むシステムでは、要件を試験項目で止めず、CI/CD結果、観測可能性、証跡、リリース判断まで接続する必要があります。

EDD型トレーサビリティは、次のように要件を実行可能なデリバリー証跡へ接続します。

```text
Requirement -> Risk -> Observability -> Test -> CI/CD Evidence -> Release Decision
```

EDDは、トレーサビリティをExcelから実行基盤へ拡張する思想である。

このデモでは、`requirements.yml`、`evidence/traceability-matrix.json`、テスト証跡、`evidence/release-decision.json` によって、その接続をファイルとCI成果物として確認できます。
