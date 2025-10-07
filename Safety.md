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

### 3-1-1 Fairness and Bias

|Benchmark|Metric|
|---|---|
|CrowS-Pairs||
|BBQ Ambig||
|BBQ Disambig||
|Winogender||
|Winobias 2_2||
|Winobias 1_2||

|Approach|Desc|
|---|---|
|Azure AI Evaluation - HateUnfairnessEvaluator|Use the Azure SDK to evaluate the Content Safety score on a scale from 0 to 7 (0-1 Very Low 2-3 Low 4-5 Medium 6-7 High)|

- [CrowS-Pairs](https://aclanthology.org/2020.emnlp-main.154/)
- [BBQ](https://arxiv.org/abs/2110.08193v2)
- [Winogender](https://arxiv.org/abs/1804.09301)
- [Winobias](https://arxiv.org/abs/1804.06876)
- [Azure AI Evaluation - HateUnfairnessEvaluator](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/risk-safety-evaluators#hateful-and-unfair-content)

### 3-1-2 Toxicity

Like `Sexual` and `Violence`, 

|Benchmark|Metric|
|---|---|
|RealToxicity||
|Toxigen||

|Approach|Desc|
|---|---|
|Azure AI Evaluation - SexualEvaluator|同上 Azure AI Evaluation|
|Azure AI Evaluation - ViolenceEvaluator|同上 Azure AI Evaluation|

- [RealToxicity](https://arxiv.org/abs/2009.11462)
- [Toxigen](https://arxiv.org/abs/2203.09509)
- [Azure AI Evaluation - SexualEvaluator](https://learn.microsoft.com/en-us/python/api/azure-ai-evaluation/azure.ai.evaluation.sexualevaluator?view=azure-python)
- [Azure AI Evaluation - ViolenceEvaluator](https://learn.microsoft.com/en-us/python/api/azure-ai-evaluation/azure.ai.evaluation.violenceevaluator?view=azure-python)

### 3-1-3 Other

Like `Self-harm-related`, the output content pertaining to physical actions intended to hurt, injure, or damage one's body or kill oneself.

|Approach|Desc|
|---|---|
|Azure AI Evaluation - SelfHarmEvaluator|同上 Azure AI Evaluation|

- [Azure AI Evaluation - SelfHarmEvaluator](https://learn.microsoft.com/en-us/python/api/azure-ai-evaluation/azure.ai.evaluation.selfharmevaluator?view=azure-python)

### 3-2-1 Sensitive Data Disclosure

### 3-2-2 System Leakage

### 3-2-3 Other

### 3-3-1 Misinformation

### 3-4-1 Direct Prompt Injections

### 3-4-2 Injection Prompt Injections

### 3-4-3 Instruction Hierarchy

### 3-4-4 Model Evasion

### 3-5-1 Insecure Model Output

```plain_text
# 待討論
1. 是否需要將衡量的 Benchmark 翻譯成中文或是導入其他中文衡量資料集
2. 與護欄組與 LLM 模型選用策略組是否在部分內容尚須進行 Alignment
```

## Appendix

### Safety Indicators Raw Data

[共編 Excel 連結 🔗](https://fubono365japan-my.sharepoint.com/:x:/r/personal/tom_h_huang_fubon_com/_layouts/15/Doc.aspx?sourcedoc=%7BA5D595DA-0F2B-43B5-87AF-62D28A565FC4%7D&file=LLM_Safety_Risk_Categorization.xlsx&action=default&mobileredirect=true)

### Assessment Tools

- [Confident AI - DeepEval](https://github.com/confident-ai/deepeval)
- [Nvidia - Garak](https://github.com/NVIDIA/garak)

## Help

Shall you have any problem, please let me knows. Look forward to your feedbacks and suggestions!

```
Email: tom.h.huang@fubon.com, kris.yj.chen@fubon.com
Tel:   02-87716888 #69175, 02-87716888 #69194
Dept:  證券 數據科學部 資料服務處(5F)
```
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

