# Transparency

## Assessment Methodology

## Survey

### 1. Google

#### 1.1 Documentation

Offer thorough documentation, like Technical Reports or Model Card, on how the generative AI service or product works using understandable language.

#### 1.2 Google - Model Card

|Info Type||
|---|---|
|Model Summary|Architecture, Inputs and outputs, Terms and links, Model data|
|Model Usage and Limitations|Intended usage, Limitations|
|Implementation|Hardware, Software|
|Evaluation|Performance, Ethics and Safety, Dangerous Capability|

#### 1.3 Google - Model Card (Evaluation)

Refer to Gemma 3 model card and Gemma 2 model card

- Performance

    |Type|Benchmark|
    |---|---|
    |Reasoning and factuality|SocialIQA, IFEval, Natural Questions ...|
    |STEM and code|MMLU, Math, HumanEval ...|
    |Multilingual|MGSM, XQuAD, IndicGenBench ...|
    |Multimodal|MMMU, TextVQA, ChartQA ...|        

- Ethics and Safety

    ||Desc|
    |---|---|
    |Category|Child Safety, Content Safety, Representational Harms, Memorization, Large-scale Harms|
    |Benchmarks|RealToxicity, CrowS-Pairs, BBQ Ambig, BBQ Disambig, Winogender, TruthfulQA, Winobias 1_2, Winobias 2_2, Toxigen|


- Dangerous Capability

    |Capability|Evaluation|
    |---|---|
    |Offensive cybersecurity|InterCode-CTF, Internal CTF, Hack the Box|
    |Self-proliferation|Self-proliferation|
    |Persuasion|Charm offensive, Click Links, Find Info, Run Code, Money talks, Web of Lies|

#### 1.4 HuggingFace - Model Card

|Info Type||
|---|---|
|Model Details|Model Description, Model Sources|
|Uses|Direct Use, Downstream Use, Out-of-Scope Use|
|Bias, Risks, and Limitations||
|How to Get Started with the Model||
|Training Details|Training Data, Training Procedure|
|Evaluation|Testing Data, Factors & Metrics, Results|
|Model Examination||
|Environmental Impact|Hardware Type, Hours used, Cloud Provider, Compute Region, Carbon Emitted|
|Technical Specifications|Model Architecture and Objective, Compute Infrastructure|
|Other|Citation, Glossary ...|

#### Reference

- [Responsible Generative AI Toolkit - Responsible Generative AI Toolkit](https://ai.google.dev/responsible/docs/design?hl=zh-tw#transparency-artifacts)
- [Model Cards - Explore a model card](https://modelcards.withgoogle.com/explore-a-model-card)
- [Gemma 3 model card](https://ai.google.dev/gemma/docs/core/model_card_3)
- [DeepMind - Evaluating Frontier Models for Dangerous Capabilities](https://arxiv.org/pdf/2403.13793)
- [DeepMind - Gemma 2: Improving Open Language Models at a Practical Size](https://storage.googleapis.com/deepmind-media/gemma/gemma-2-report.pdf)

### 2. Microsoft

#### 2.1 The CLeAR Documentation Framework for AI Transparency: Recommendations for Practitioners & Context for Policymakers

CLeAR (Comparable, Legible, Actionable, and Robust), a Documentation Framework which aims to offer guiding principles for AI documentation, and support responsible development and use, as well as mitigation of downstream harms, by providing transparency into the design, attributes, intended use, and shortcomings of datasets, models, and AI systems.

The Key Themes and Considerations of Documentation Practices

||
|---|
|Importance of documenting datasets, models, and AI systems|
|Documentation should occur throughout the lifecycle|
|Expanding the focus of documentation to be context-aware|
|Risk and impact assessments in the context of documentation|
|The opportunity to drive behavior through documentation requirements|
|Documentation requires robust organizational support|

#### 2.2 Microsoft's Transparency Notes

Microsoft's Transparency Notes are intended to help you understand how our AI technology works, the choices system owners can make that influence system performance and behavior, and the importance of thinking about the whole system, including the technology, the people, and the environment.

- Transparency Note for Azure OpenAI Service

    |Topic|Subtopic|
    |---|---|
    |The basics of the Azure OpenAI Models|Introduction, Key terms|
    |Capabilities|Text, code, and fine-tuned models, Vision models, Audio / speech models, Model Card|
    |Use cases|Intended uses, Fine-tuned use cases, Reasoning model use cases, Deep research use cases, Azure OpenAI evaluation use cases ...|
    |Limitations|Technical limitations, operational factors, and ranges, Risks and limitations of fine-tuning ...|
    |System performance|Best practices for improving system performance ...|
    |Other|Evaluating and integrating Azure OpenAI natural language and vision models for your use|

- Transparency Note for Microsoft 365 Copilot

    |Topic|Subtopic|
    |---|---|
    |The basics of the Azure OpenAI Models|Introduction, Key terms|
    |Capabilities|Features|
    |System Behavior|Explanation of how Microsoft 365 Copilot works, How generates responses without web content or organizational data|
    |Extensibility & customization||
    |Use Cases|Considerations when choosing a use case|
    |Limitations|Specific Limitations of Microsoft 365 Copilot|
    |Microsoft 365 Copilot performance|Best practices|
    |Mapping, measuring, and managing risks|Map, Measure, Manage|
    |Other|Evaluating and integrating Microsoft 365 Copilot for your organization|

- Greater transparency and control for web search queries in Microsoft 365 Copilot
    - Bing web search query citations for users
    - Audit logging and eDiscovery for Bing web search queries
    - Expanded controls for managing web searches in Copilot
    
- OpenAI o3 and o4-mini System Card

    |Chapter|Content|
    |---|---|
    |Model Data and Training||
    |Observed Safety Challenges and Evaluations|Disallowed Content, Jailbreaks, Hallucinations, Multimodal refusals, Person Identification and Ungrounded Inference Evaluations, Fairness and Bias, Jailbreaks through Custom Developer Messages, Image Generation, Third Party Assessments|
    | Preparedness| Capabilities Assessment, Biological and Chemical, Cybersecurity, AI Self-improvement, Safeguards|
    |Multilingual Performance||

#### Reference

- [2025 Responsible AI Transparency Report](https://www.microsoft.com/zh-tw/ai/responsible-ai#Our-commitment)
- [The CLeAR Documentation Framework for AI Transparency: Recommendations for Practitioners & Context for Policymakers](https://shorensteincenter.org/clear-documentation-framework-ai-transparency-recommendations-practitioners-context-policymakers/)
- [Transparency Note for Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/ai-foundry/responsible-ai/openai/transparency-note?tabs=text#what-is-a-transparency-note)
- [Transparency Note for Microsoft 365 Copilot](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-transparency-note)
- [OpenAI o3 and o4-mini System Card](https://cdn.openai.com/pdf/2221c875-02dc-4789-800b-e7758f3722c1/o3-and-o4-mini-system-card.pdf)
- [Introducing greater transparency and control for web search queries in Microsoft 365 Copilot and Microsoft 365 Copilot Chat](https://techcommunity.microsoft.com/blog/microsoft365copilotblog/introducing-greater-transparency-and-control-for-web-search-queries-in-microsoft/4253080)

### 3. Standard

#### 3.1 The Foundation Model Transparency Index

- 100 fine-grained transparency indicators across three main domains: Upstream, Model, and Downstream
- Binary scoring (0/1) for each indicator (publicly available or not), with independent double review and company feedback

||Indicators Cat|
|---|---|
|Upstream|Data, Data Labor, Data Access, Compute, Methods and Data Mitigations|
|Model|Model Basics, Model Access, Capabilities, Limitations, Risks, Model Mitigations, Trustworthiness and Inference|
|Downstream|Distribution, Usage Policy, Model Behavior Policy, User Interface, User Data Protection, Model Updates, Feedback, Impact and Downstream Documentation|

#### Reference

- [The Foundation Model Transparency Index, 2023, Bommasani, Rishi, et al.](https://arxiv.org/abs/2310.12941)
- [Human-Centered Artificial Intelligence - The 2025 AI Index Report](https://hai.stanford.edu/ai-index/2025-ai-index-report)

### 4. EY 安永

#### 4.1 利害關係人資訊揭露與權益影響
- 應明確告知利害關係人其互動對象是否為 AI 系統
- 說明 AI 系統可能影響的範疇（如信用評分、投資建議、客戶分群等），並評估影響程度
- 揭露 AI 所使用的資料來源、模型邏輯與預測或決策流程
- 若 AI 系統出現錯誤，應有明確的責任歸屬機制與處理流程
- 提供利害關係人申訴或異議的方式與聯絡窗口

#### 4.2 透明性揭露以彌補解釋性不足

#### 4.3 AI 系統透明性與通知機制

- 若使用 AI 輔助決策，應主動以簡明語言通知客戶 AI 的參與與影響
- 用語淺白易懂說明 AI 如何影響建議生成，幫助客戶理解來源
- 多元揭露管道即時說明

#### 4.4 AI 系統訓練與資料管理

- 書面化紀錄資料來源、收集時間、消費者同意方式（如電子簽署）、資料字典等
- 資料字典內容(包含變數名稱、來源、單位、計算方式、使用目的等)儲存於中央資料庫並定期更新。

#### Reference

- [富邦金控-落實人工智慧系統生命週期控管_20250916]()

## Help

Shall you have any problem, please let me knows. Look forward to your feedbacks and suggestions!

```
Email: tom.h.huang@fubon.com
Tel:   02-87716888 #69175
Dept:  證券 數據科學部 資料服務處(5F)
```
