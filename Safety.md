# Safety Survey

## How to Assessment

### 1. Main Reference Sources

在檢視各種安全性評估參考資料後，我們最終選擇了以下五份來源作為安全性指標參考之規劃

1. [Google - Secure AI Framework](https://saif.google/secure-ai-framework/risks)
2. [Azure AI Foundry - Risk and safety evaluators](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/risk-safety-evaluators)
3. [Model Card - Google Gemma 2](https://ai.google.dev/gemma/docs/core/model_card_2)
4. [Model Card - OpenAI GPT-OSS](https://arxiv.org/pdf/2508.10925)
5. [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/)

### 2. Safety Indicators

後續我們對該五份來源的安全性衡量面向進行，篩選與彙整，得出以下的安全性評估指標

|Type|Subtype|Ref|
|---|---|---|
|1. Content Safety|Fairness and Bias|2, 3, 4|
|1. Content Safety|Toxicity|2, 3, 4|
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

Stereotypes such as those related to `Race`, `Religion`, `Age`, `Occupation`, and so on.

|Benchmark|Metric|
|---|---|
|CrowS-Pairs|Bias Score = % of examples where stereotype sentence is preferred|
|BBQ|Accuracy (Ambig/Disambig)|
|Winogender|Gender Consistency Score (she/he/they)|
|Winobias|Stereotype Gap = Accuracy(pro) - Accuracy(anti)|

|Approach|Desc|
|---|---|
|Azure AI Evaluation - HateUnfairnessEvaluator|Use the Azure SDK to evaluate the Content Safety score on a scale from 0 to 7 (0-1 Very Low 2-3 Low 4-5 Medium 6-7 High)|

- [CrowS-Pairs](https://aclanthology.org/2020.emnlp-main.154/)
- [BBQ](https://arxiv.org/abs/2110.08193v2)
- [Winogender](https://arxiv.org/abs/1804.09301)
- [Winobias](https://arxiv.org/abs/1804.06876)
- [Azure AI Evaluation - HateUnfairnessEvaluator](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/risk-safety-evaluators#hateful-and-unfair-content)

### 3-1-2 Toxicity

Like `Sexual`, `Violence`, `Self-harm-related`, `illicit` and so on.

|Benchmark|Metric|
|---|---|
|RealToxicity|Maximum Toxicity, Empirical Toxicity Probability(>= 0.5)，使用 PERSPECTIVE API|
|Toxigen|Toxigen Score (%)，使用 toxigen_roberta 或 HateBERT 判斷|
|OpenAI - Standard Disallowed Content Evaluations|拒答率(not_unsafe, not_overrefuse)|
|OpenAI - Production Benchmarks|拒答率(not_unsafe, not_overrefuse)|

P.S. OpenAI 的兩個 Benchmark 似乎無提供公開的衡量資料集

|Approach|Desc|
|---|---|
|ConversationAI - PERSPECTIVE API|This API provides scores indicating whether the content contains toxicity, threats, insults, and similar harmful elements. The scores range from 0 to 1.|
|Azure AI Evaluation - SexualEvaluator|同上 Azure AI Evaluation|
|Azure AI Evaluation - ViolenceEvaluator|同上 Azure AI Evaluation|
|Azure AI Evaluation - SelfHarmEvaluator|同上 Azure AI Evaluation|

- [RealToxicity](https://arxiv.org/abs/2009.11462)
- [Toxigen](https://github.com/microsoft/TOXIGEN)
- [OpenAI - Safety Evaluations Hub](https://openai.com/zh-Hant/safety/evaluations-hub/)
- [ConversationAI - PERSPECTIVE API](https://github.com/conversationai/perspectiveapi)
- [Azure AI Evaluation - SexualEvaluator](https://learn.microsoft.com/en-us/python/api/azure-ai-evaluation/azure.ai.evaluation.sexualevaluator?view=azure-python)
- [Azure AI Evaluation - ViolenceEvaluator](https://learn.microsoft.com/en-us/python/api/azure-ai-evaluation/azure.ai.evaluation.violenceevaluator?view=azure-python)
- [Azure AI Evaluation - SelfHarmEvaluator](https://learn.microsoft.com/en-us/python/api/azure-ai-evaluation/azure.ai.evaluation.selfharmevaluator?view=azure-python)
- [Google AI for Developer - Academic benchmarks to evaluate responsibility metrics](https://ai.google.dev/responsible/docs/evaluation?hl=zh-tw)

### 3-2-1 Sensitive Data Disclosure

### 3-2-2 System Leakage

### 3-2-3 Other

### 3-3-1 Misinformation

### 3-4-1 Direct Prompt Injections

### 3-4-2 Injection Prompt Injections

### 3-4-3 Instruction Hierarchy

Instruction Hierarchy refers to a structured system of prioritizing different types of instructions that a language model receives during inference. It ensures that the model behaves safely and predictably, especially when multiple parties (like system providers, developers, and end users) are involved.

|Benchmark|Metric|
|---|---|
|StrongREJECT|score = (1 − refused) × (specific + convincing) / 2, refused = 0|1, specific = 0~1, convincing = 0~1|

GPT-OSS 主要用該 Benchmark 資料集衡量以下兩面向:
`System <> User message conflict`, ` Phrase and Password Protection`

- [StrongREJECT](https://arxiv.org/pdf/2402.10260)

### 3-4-4 Model Evasion

Model Evasion refers to slightly perturbing the prompt input to cause a model to generate incorrect or misleading outputs. Such attacks can result in reputational damage, legal liabilities, and downstream risks, including breaches in security and privacy systems.

### 3-5-1 Insecure Model Output

Model output that is not appropriately validated, rewritten, or formatted before being passed to downstream systems or the user. For example, an Email containing malicious links or attachments, or code that is vulnerable to injection attacks.

|Approach|Desc|
|---|---|
|Azure AI Evaluation - CodeVulnerabilityEvaluator|The output includes whether the input contains a code vulnerability issue, a description of the issue, and the likely category of the vulnerability.|

- [Azure AI Evaluation - CodeVulnerabilityEvaluator](https://learn.microsoft.com/en-us/python/api/azure-ai-evaluation/azure.ai.evaluation.codevulnerabilityevaluator?view=azure-python)

```plain_text
# 待討論
1. 是否需要將衡量的 Benchmark 翻譯成中文或是導入其他中文衡量資料集
2. 與護欄組與 LLM 模型選用策略組是否在部分內容尚須進行 Alignment
```

## Appendix

### Safety Indicators Raw Data

[共編 Excel 連結 🔗](https://fubono365japan-my.sharepoint.com/:x:/r/personal/tom_h_huang_fubon_com/_layouts/15/Doc.aspx?sourcedoc=%7BA5D595DA-0F2B-43B5-87AF-62D28A565FC4%7D&file=LLM_Safety_Risk_Categorization.xlsx&action=default&mobileredirect=true)

### Other Reference Sources
- [Elastic Security Lab - 2024 LLM Safety Assessment The Definitive Guide on Avoiding Risk and Abuses](https://www.cit-sys.co.uk/wp-content/uploads/2024/11/elastic-security-labs-llm-safety-assessment-2024-1.pdf)
- [UIUC - AI Secure](https://huggingface.co/spaces/AI-Secure/llm-trustworthy-leaderboard)
- [知乎 - 大模型安全评估——LLMs Evaluation in Safety](https://zhuanlan.zhihu.com/p/2534134145)
- [LLM Safety 最新论文推介 - 2025.7.30(2)](https://zhuanlan.zhihu.com/p/1933792417364022202)
- [Apollo Research and OpenAI - Anti-Scheming](https://www.antischeming.ai/)

- 安永
    ```
    除了模型的準確性和效能，還應選擇已「對抗性訓練」(adversarial training)的模型，以避免外部威脅造成的錯誤判斷。如一些模型會自帶防止對抗性樣本攻擊的功能，減少不當輸入對模型預測的影響、強化資料管控降低資料外洩
    ```

### Assessment Tools

- [Confident AI - DeepEval](https://github.com/confident-ai/deepeval)
- [Nvidia - Garak](https://github.com/NVIDIA/garak)
- [Lasso](https://www.lasso.security/)

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

