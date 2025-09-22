# 模型評測機制 - Survey

## 安全性

### Google - Secure AI Framework

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

### Microsoft - The basics of Azure AI Foundry risk and safety evaluations

https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/safety-evaluations-transparency-note

|security vulnerabilities|
|-|
|Hateful, Unfair, Sexual, Violent and Self-harm-related content|
|Protected material content|
|Jailbreak|

## Nvidia - Garak / Safeguard Agentic AI Systems with the NVIDIA Safety Recipe

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

### OWASP Top 10 for LLM Applications 2025

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

### Elastic Security Lab

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

### HuggingFace Safety Leaderboard (from UIUC - AI Secure)

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

### Confident AI

https://github.com/confident-ai/deepeval

|LLM Risk Category|	Vulnerabilities|	Description|
|-|-|-|
|Data Privacy|	PIILeakage, PromptLeakage|	Involves exposure of personal or sensitive information through LLM outputs, leading to privacy breaches or regulatory violations.|
|Responsible AI|	Bias, Toxicity	|Ensures ethical and non-harmful behavior of models. Risks include offensive, discriminatory, or unfair content.|
|Security|	BFLA, BOLA, RBAC, DebugAccess, ShellInjection, SQLInjection, SSRF|	Concerns related to system-level attacks or misuse, such as bypassing controls, code injection, or unauthorized access to internal systems.|
|Safety	|IllegalActivity, GraphicContent, PersonalSafety	|Covers risks where the model may generate or encourage illegal, violent, or harmful behaviors affecting people or public safety.|
|Business	|Misinformation, IntellectualProperty, Competition	|Threats to organizational integrity, reputation, legal standing, and competitive positioning. Includes IP leakage, false information, and competitive data exposure.|
|Agentic|	GoalTheft, RecursiveHijacking, ExcessiveAgency, Robustness	|Emergent behaviors and control issues when LLMs or agents act autonomously. Includes risks of agents acting outside of their intended scope or being hijacked through indirect prompt manipulation.|

### 安永

- 除了模型的準確性和效能，還應選擇已「對抗性訓練」(adversarial training)的模型，以避免外部威脅造成的錯誤判斷。如一些模型會自帶防止對抗性樣本攻擊的功能，減少不當輸入對模型預測的影響、強化資料管控降低資料外洩

- 可針對敏感資料進行加密(如使用AES 或 RSA技術)，並設置分層存取權限控制，確保只有特定的授權人員可以檢視和操作敏感資料，同時進行資料存取記錄。

### Other References

- [ACL 2025 Tutorial - Guardrails and Security for LLMs:
Safe, Secure, and Controllable Steering of LLM Applications](https://llm-guardrails-security.github.io/)
- [知乎 - 大模型安全评估——LLMs Evaluation in Safety](https://zhuanlan.zhihu.com/p/2534134145)
- [LLM Safety 最新论文推介 - 2025.7.30(2)](https://zhuanlan.zhihu.com/p/1933792417364022202)
- [Apollo Research and OpenAI - Anti-Scheming](https://www.antischeming.ai/)

## 可靠性(穩定性)

## 可解釋性

### 安永
- 應該準備詳細的技術報告，包含模型架構、訓練資料的來源與資料處理方法等文件

### Other References

- [LLM 可解釋性](https://blog.csdn.net/Nifc666/article/details/141927514)

## 透明性

### 安永 
- 透過透明性來補償可解釋性不足時可能產生的風險 (Model Card)
主動通知客戶該審核過程中包含AI的參與、標示標示「此建議由人工智慧分析提供」、以易於理解的方式呈現
- 如紀錄消費者的行為資料時，應明確紀錄資訊的取得時間（例如，資料收集的日期）、來源（例如內部交易資料或外部第三方資料供應商）等，並確保每筆資料已獲得消費者的授權同意（如透過電子簽署或書面同意）。
- 資料字典(用以詳細描述資料集中所有變數的含義和用途)應包括變數名稱、來源、單位、計算方式（若為衍生變數）、使用目的等內容，並儲存於中央資料庫中，便於相關人員查閱。透過定期審核和更新資料字典，可確保所有人員對AI 模型所使用資料的理解一致。

![alt text](image.png)

## Ref

- [Googel - Model Cards Explained](https://modelcards.withgoogle.com/)
- [2023 - The Foundation Model Transparency Index](https://arxiv.org/abs/2310.12941)
- [AI Transparency in the Age of LLMs: A Human-Centered Research Roadmap](https://hdsr.mitpress.mit.edu/pub/aelql9qy/release/2)
- [A Comprehensive Survey on Trustworthiness in Reasoning with Large Language Models - Hullucination, Truthfulness, Safety, Robustness, Fairness and Privacy](https://arxiv.org/pdf/2509.03871)

## Help

Shall you have any problem, please let me knows. Look forward to your feedbacks and suggestions!

```
Email: tom.h.huang@fubon.com
Tel:   02-87716888 #69175
Dept:  證券 數據科學部 資料服務處(5F)
```
