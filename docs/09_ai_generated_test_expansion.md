# 09: AI-Generated Test Expansion

## English

AI makes it realistic to generate a broad set of test perspectives and test cases.

However, AI-generated tests are not a release decision by themselves. They are useful inputs to verification, but the release decision still needs executable evidence.

Evidence-Driven Delivery connects AI-expanded test perspectives, CI/CD execution results, runtime observability, and release judgment:

```text
AI test expansion -> CI/CD execution -> Observability evidence -> Release Decision
```

Modern systems still contain black boxes: managed services, external APIs, networks, runtime conditions, and AI models. These cannot always be fully verified by generated test cases alone.

For that reason, AI-assisted test expansion and runtime observability are complementary. AI can broaden what is checked before release. Observability can show what actually happened during execution.

## 日本語

AIにより、試験観点やテストケースを広範に生成することが現実的になっています。

ただし、AIが生成したテストは、それだけではリリース判断ではありません。AIによる試験観点展開は有効な入力ですが、リリース判断には実行された証跡が必要です。

EDDは、AIによる試験観点展開、CI/CDでの実行結果、オブザーバビリティによる実行時証跡を、リリース判断へ接続します。

```text
AI test expansion -> CI/CD execution -> Observability evidence -> Release Decision
```

現代システムには、マネージドサービス、外部API、ネットワーク、実行時条件、AIモデルなどのブラックボックスが残ります。これらを、AIが生成したテストケースだけで完全に説明することはできません。

そのため、AIによる全量試験と、オブザーバビリティによる実行時観測は補完関係にあります。
