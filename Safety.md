# Safety Survey

## How to Assessment

### 1. Main Reference Sources

在檢視各種安全性評估參考資料後，我們最終選擇了以下五份來源作為安全性指標參考之規劃

1. [Google - Secure AI Framework](https://saif.google/secure-ai-framework/risks)
2. [Azure AI Foundry - Risk and safety evaluators](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/risk-safety-evaluators)
3. [Model Card - Google Gemma 2](https://ai.google.dev/gemma/docs/core/model_card_2)
4. [Model Card - OpenAI GPT-OSS](https://arxiv.org/pdf/2508.10925)
5. [OWASP Top 10 for LLM Applications 2025](https://saif.google/secure-ai-framework/risks)

### 2. Safety Indicators

後續我們對該五份來源的安全性衡量面向進行，篩選與彙整，得出以下的安全性評估指標

|Type|Subtype|Ref|
|---|---|---|
|1. Content Safety|Fairness and Bias|2, 3, 4|
|1. Content Safety|Toxicity|2, 3, 4|
|1. Content Safety|Other|2|
|2. Information Disclosure|Sensitive Data Disclosure|1, 2, 5|
|2. Information Disclosure|System Leakage|5|
|2. Information Disclosure|Other|1|
|3. Misinformation|Misinformation|2, 3, 4, 5|
|4. Prompt Injection|Direct Prompt Injections|1, 2, 4, 5|
|4. Prompt Injection|Indirect Prompt Injections|1, 2, 5|
|4. Prompt Injection|Instruction Hierarchy|4|
|4. Prompt Injection|Model Evasion|1|
|5. Insecure Model Output|Insecure Model Output|1, 2, 5|

```plain_text
# 待討論
以下五大面向之細項指標是否納入安全性衡量標準有待商榷
1. Dangerous Capability - Offensive cybersecurity
2. Dangerous Capability - Self-proliferation
3. Dangerous Capability - Persuasion
4. Supply Chain
5. Vector and Embedding Weaknesses
```

### 3. Assessment Methodology

#### 3-4-1 Direct Prompt Injections

#### 3-4-2 Injection Prompt Injections

#### 3-4-3 Instruction Hierarchy

#### 3-4-4 Model Evasion

#### 3-5-1 Insecure Model Output

desc

|Benchmark|Metric|
|---|---|
|A||

|Approach|Desc|
|---|---|
|A||

```plain_text
# 待討論
1. 是否需要將衡量的 Benchmark 翻譯成中文或是導入其他中文衡量資料集
2. 與護欄組與 LLM 模型選用策略組是否在部分內容尚須進行 Alignment
```

## Appendix

## Help

Shall you have any problem, please let me knows. Look forward to your feedbacks and suggestions!

```
Email: tom.h.huang@fubon.com, kris.yj.chen@fubon.com
Tel:   02-87716888 #69175, 02-87716888 #69194
Dept:  證券 數據科學部 資料服務處(5F)
```
