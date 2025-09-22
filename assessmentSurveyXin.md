# 模型評測機制 - Survey

## 1. 安全性

### 1-1. Google - Secure AI Framework

https://saif.google/secure-ai-framework/risks

|Risks|
|-|
|Data Poisoning|
|Unauthorized Training Data|
|Model Source Tampering|
|Excessive Data Handling|
|Model Exfiltration|
|Model Deployment Tampering|
|Denial of ML Service|
|Model Reverse Engineering|
|Insecure Integrated Component|
|Prompt Injection|
|Model Evasion|
|Sensitive Data Disclosure| 
|Inferred Sensitive Data|
|Insecure Model Output|
|Rogue Actions|

### 1-2. Microsoft - The basics of Azure AI Foundry risk and safety evaluations

https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/safety-evaluations-transparency-note

|security vulnerabilities|
|-|
|Hateful, Unfair, Sexual, Violent and Self-harm-related content|
|Protected material content|
|Jailbreak|

## 1-3. Nvidia - Garak / Safeguard Agentic AI Systems with the NVIDIA Safety Recipe

https://github.com/NVIDIA/garak

https://developer.nvidia.com/blog/safeguard-agentic-ai-systems-with-the-nvidia-safety-recipe/

|Probe|Description|
|-|-|
|blank|最簡單的測試，送出空白提示，觀察模型的反應。|
|atkgen|自動化攻擊生成，模擬紅隊測試，嘗試誘導模型產生有害內容。使用經微調的 GPT-2 模型。|
|av_spam_scanning|嘗試讓模型輸出惡意內容的特徵碼，類似病毒掃描測試。|
|continuation|測試模型是否會延續不當或敏感詞語。|
|dan|模擬 DAN（Do Anything Now）攻擊，試圖繞過模型的安全限制。|
|donotanswer|測試模型是否會回答本不該回答的問題。|
|encoding|利用文字編碼進行提示注入，測試模型是否能被操控。|
|gcg|透過加入對抗性後綴來破壞系統提示，測試模型的穩定性。|
|glitch|利用特殊字元或錯誤編碼測試模型是否出現異常行為。|
|grandma|以「請你像奶奶一樣提醒我」的方式，測試模型是否會放鬆限制。|
|goodside|實作 Riley Goodside 的提示攻擊技術，測試模型的防禦能力。|
|leakreplay|測試模型是否會重播訓練資料，檢查資料洩漏風險。|
|lmrc|使用語言模型風險卡（LM Risk Cards）中的部分測試項目。|
|malwaregen|嘗試讓模型生成惡意程式碼，如病毒或木馬。|
|misleading|測試模型是否會支持錯誤或誤導性的說法。|
|packagehallucination|嘗試讓模型生成不存在的程式套件名稱，測試其安全性與真實性。|
|promptinject|實作 PromptInject 專案的提示注入技術，測試模型是否能被操控。|
|realtoxicityprompts|使用 RealToxicityPrompts 資料集的一部分，測試模型對有毒內容的反應。|
|snowball|利用複雜問題誘導模型產生錯誤答案，模擬「滾雪球式幻覺」。|
|xss|測試模型是否會產生跨站攻擊（XSS）相關的漏洞或程式碼。|

### 1-4. OWASP Top 10 for LLM Applications 2025

https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/

||
|-|
|Prompt Injection|
|Sensitive Information Disclosure|
|Supply Chain|
|Data and Model Poisoning|
|Improper Output Handling|
| Excessive Agency|
|System Prompt Leakage|
|Vector and Embedding Weaknesses|
|Misinformation|
|Unbounded Consumption|

### 1-5. Elastic Security Lab

https://www.cit-sys.co.uk/wp-content/uploads/2024/11/elastic-security-labs-llm-safety-assessment-2024-1.pdf

||
|-|
|Prompt injection|
|Insecure output handling|
|Training data poisoning|
|Model Denial of Service|
|Supply chain vulnerability|
|Sensitive information disclosure|
|Insecure plugin design|
|Excessive agency|
|Overreliance|
|Model theft|

### 1-6. HuggingFace Safety Leaderboard (from UIUC - AI Secure)

https://huggingface.co/spaces/AI-Secure/llm-trustworthy-leaderboard

||
|-|
|Toxicity|
|Stereotype and bias|
|Adversarial robustness|
|Out-of-Distribution Robustness|
|Robustness to Adversarial Demonstrations|
|Privacy|
|Machine Ethics|
|Fairness|

### 1-7. Confident AI

https://github.com/confident-ai/deepeval

|LLM Risk Category|	Vulnerabilities|	Description|
|-|-|-|
|Data Privacy|	PIILeakage, PromptLeakage|	Involves exposure of personal or sensitive information through LLM outputs, leading to privacy breaches or regulatory violations.|
|Responsible AI|	Bias, Toxicity	|Ensures ethical and non-harmful behavior of models. Risks include offensive, discriminatory, or unfair content.|
|Security|	BFLA, BOLA, RBAC, DebugAccess, ShellInjection, SQLInjection, SSRF|	Concerns related to system-level attacks or misuse, such as bypassing controls, code injection, or unauthorized access to internal systems.|
|Safety	|IllegalActivity, GraphicContent, PersonalSafety	|Covers risks where the model may generate or encourage illegal, violent, or harmful behaviors affecting people or public safety.|
|Business	|Misinformation, IntellectualProperty, Competition	|Threats to organizational integrity, reputation, legal standing, and competitive positioning. Includes IP leakage, false information, and competitive data exposure.|
|Agentic|	GoalTheft, RecursiveHijacking, ExcessiveAgency, Robustness	|Emergent behaviors and control issues when LLMs or agents act autonomously. Includes risks of agents acting outside of their intended scope or being hijacked through indirect prompt manipulation.|

### 1-8. 安永

- 除了模型的準確性和效能，還應選擇已「對抗性訓練」(adversarial training)的模型，以避免外部威脅造成的錯誤判斷。如一些模型會自帶防止對抗性樣本攻擊的功能，減少不當輸入對模型預測的影響、強化資料管控降低資料外洩

- 可針對敏感資料進行加密(如使用AES 或 RSA技術)，並設置分層存取權限控制，確保只有特定的授權人員可以檢視和操作敏感資料，同時進行資料存取記錄。

### 1-9. Other References

- [ACL 2025 Tutorial - Guardrails and Security for LLMs:
Safe, Secure, and Controllable Steering of LLM Applications](https://llm-guardrails-security.github.io/)
- [知乎 - 大模型安全评估——LLMs Evaluation in Safety](https://zhuanlan.zhihu.com/p/2534134145)
- [LLM Safety 最新论文推介 - 2025.7.30(2)](https://zhuanlan.zhihu.com/p/1933792417364022202)
- [Apollo Research and OpenAI - Anti-Scheming](https://www.antischeming.ai/)

## 可靠性(穩定性)

### OpenAI - Why Language Models Hallucinate

https://openai.com/zh-Hant/index/why-language-models-hallucinate/

- Factual Hallucinations
- Faithfulness Hallucinations

Detecting LLM Hallucinations: Strategies and Overview

https://medium.com/@techsachin/detecting-llm-hallucinations-strategies-and-overview-57eea69e6a07

- 語言模型內在指標（Intrinsic Metrics）
    - Perplexity：衡量模型對語言的掌握程度，越低代表越流暢。
    - Log-likelihood：用於比較不同模型對同一輸入的預測信心。
- 輸出品質指標
    - Correctness / Factuality：是否符合事實。
    - Hallucination Detection：是否生成虛構或錯誤資訊。
    - Answer Relevance / Contextual Relevance：是否與問題或上下文相關。
- 一致性與可重現性
    - Prompt Sensitivity：同一問題不同表述是否導致結果劇烈變化。
    - Ranking Stability：模型在不同語境下的相對表現是否穩定。

## 可解釋性

### OpenAI - Language models can explain neurons in language models

https://openai.com/index/language-models-can-explain-neurons-in-language-models/

### Anthropic - Tracing the thoughts of a large language model

https://transformer-circuits.pub/2025/attribution-graphs/biology.html

### Measuring the Interpretability and Explainability of Model Decisions of Five Large Language Models

https://scispace.com/pdf/measuring-the-interpretability-and-explainability-of-model-m3yynfj1hd.pdf

|Evaluation Criteria||
|--|--|
|Transparency of Reasoning|The extent to which a model’s decision-making process can be understood and traced by humans.|
|Accuracy of Explanations|The relevance and correctness of the models’ explanations for their outputs, assessed through comparison with expert judgments|
|Consistency Across Contexts|Evaluation of whether the models maintain a consistent level of interpretability and explainability across different types of input and contexts.|
|Adaptability to Feedback|The ability of the models to incorporate feedback and improve their explanations and decision-making rocesses over time.|
|Quantitative Metrics|Use of established quantitative metrics, such as fidelity, comprehensiveness, and sufficiency, to measure|

### LLMs for Explainable AI: A Comprehensive Survey

https://arxiv.org/html/2504.00125v1

|Eval Dataset||
|-|-|
|e-SNLI|自然語言推理，含人類撰寫解釋|
|CoS-E|常識推理多選題，含步驟解釋|
|ECQA|常識問答，含正反理由解釋|
|WorldTree|科學推理，結構化解釋圖|
|OpenBookQA|科學知識問答，含知識型解釋|
|XplainLLM|知識圖譜三元組，強化解釋透明度|
|RAGBench|檢索增強生成，強調證據透明|
|HateXplain|仇恨言論偵測，含偏見標註與解釋|

### 安永
- 應該準備詳細的技術報告，包含模型架構、訓練資料的來源與資料處理方法等文件

### Other References

- [CSDN - 深入解析大语言模型可解释性研究：工具、论文与前沿进展](https://blog.csdn.net/Nifc666/article/details/141927514)
- [iKala -  AI 學會說謊：Anthropic 可解釋性研究的警示與啟發](https://ikala.ai/zh-tw/blog/ceo-insight/when-ai-lies-anthropic-interpretability-research-warnings-and-implications/)
- [Explainability for Large Language Models: A Survey, 2024](https://arxiv.org/abs/2309.01029)

## 透明性

### Stanford CRFM - Foundation Model Transparency Index Scores & Artificial Intelligence Index Report 2025

https://arxiv.org/abs/2310.12941

https://hai.stanford.edu/ai-index/2025-ai-index-report

- Major Dimensions of Transparency
    - Upstream,  Model,  Downstream
    - Impact, Feedback, Usage Policy, Distribution, Mitigations,
    Risks, Capabilities, Model Access, Model Basics, Methods, Compute, Labor, Data

### Google - Model Cards Explained

https://modelcards.withgoogle.com/explore-a-model-card

By making this information easy to access, model cards support responsible AI development and the adoption of robust, industry-wide standards for broad transparency and evaluation practices.

### Google - Responsible Generative AI Toolkit - Transparency artifacts

https://ai.google.dev/responsible/docs/design?hl=zh-tw#transparency-artifacts

說明文件是實現資訊公開的關鍵方法 政府機關、政策執行者和使用者。包括 提供詳細的技術報表或模型、資料和系統資訊卡 根據安全及其他模型 以及評估結果透明度構件不只是通訊工具，他們 也為 AI 研究人員、部署人員和下游開發人員提供指引 如何負責任地使用模型這些資訊對於 也想深入瞭解型號

以下列舉幾項資訊公開指南，請多加留意：

- 向使用者明確告知正在參與實驗 並著重在突顯非預期模型的可能性行為
- 提供詳盡的說明文件，說明生成式 AI 服務或產品的方式 就是使用容易理解的語言考慮採用結構化發布方式透明度構件，例如模型資訊卡這些資訊卡提供並總結先前採用的評估作業 都會在整個模型開發期間執行
- 向觀眾說明他們可以如何提供意見，以及如何掌控一切，例如： 為：
    - 提供機制，協助使用者確認事實問題
    - 按讚/倒讚圖示，用來收集使用者意見
    - 回報問題和支援快速回應連結 使用者意見回饋
    - 儲存或刪除使用者活動的使用者控制項

### 安永 
- 透過透明性來補償可解釋性不足時可能產生的風險 (Model Card)
主動通知客戶該審核過程中包含AI的參與、標示標示「此建議由人工智慧分析提供」、以易於理解的方式呈現
- 如紀錄消費者的行為資料時，應明確紀錄資訊的取得時間（例如，資料收集的日期）、來源（例如內部交易資料或外部第三方資料供應商）等，並確保每筆資料已獲得消費者的授權同意（如透過電子簽署或書面同意）。
- 資料字典(用以詳細描述資料集中所有變數的含義和用途)應包括變數名稱、來源、單位、計算方式（若為衍生變數）、使用目的等內容，並儲存於中央資料庫中，便於相關人員查閱。透過定期審核和更新資料字典，可確保所有人員對AI 模型所使用資料的理解一致。

![alt text](image.png)

## Ref

- [A Comprehensive Survey on Trustworthiness in Reasoning with Large Language Models - Hullucination, Truthfulness, Safety, Robustness, Fairness and Privacy](https://arxiv.org/pdf/2509.03871)
- [Top 15 LLM Evaluation Metrics to Explore in 2025](https://www.analyticsvidhya.com/blog/2025/03/llm-evaluation-metrics/)
- [如何评估大语言模型（LLM）的质量——框架、方法、指标和基准](https://www.51cto.com/article/785983.html)

## Help

Shall you have any problem, please let me knows. Look forward to your feedbacks and suggestions!

```
Email: tom.h.huang@fubon.com
Tel:   02-87716888 #69175
Dept:  證券 數據科學部 資料服務處(5F)
```
