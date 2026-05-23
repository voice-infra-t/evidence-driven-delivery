# 00: コンセプト

このリポジトリは、**Evidence-Driven Delivery（証跡駆動デリバリー）**の最小デモです。

このデモの対象はあえて簡単な**Simple Decision API**です。  
複雑なドメインルールではなく、判断ロジックとその証跡がどうリリース品質を支えるかを見せることに集中しています。

重要なのは実装内容そのものではなく、次の流れを実装として残すことです。

```
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

この流れにより「実装が完成したからリリース」ではなく、「**出してよい証跡が揃ったからリリース**」にします。

## ODDとの関係

CIでは**Observability-Driven Development（ODD）**の考えで、判断ごとに観測可能な情報を記録します。  
判断が再現可能で説明可能であることが、後工程の判断材料になります。

## CDとの関係

CDでは生成された観測データとテスト実行結果をもとに、  
`release_decsion` を切り分けます。  
このデモでは `evidence/test-report.json` と `evidence/release-decision.json` が
`Release Gate` に該当します。

## 中心メッセージ

**「コードが完成したからリリースするのではなく、出してよい証跡が揃ったものをリリースする」**
