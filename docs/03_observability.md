# 03: Observability

このデモでは、すべての判定で以下を観測します。

- id
- input_value
- decision
- reason
- fallback_reason
- timestamp

この記録を `app.evidence.build_observation` として実装し、  
判断結果がどの入力からどのように導出されたかを追跡可能にします。

観測がなければ、判断の説明責任が成立しません。  
また、判断が説明できない状態では、リリースゲートに必要な証跡を扱えません。  
これが ODD / Observability-Driven Development の最小例です。
