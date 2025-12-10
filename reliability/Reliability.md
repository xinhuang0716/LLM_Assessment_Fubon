

## 可靠性 (穩定性)

> https://arxiv.org/pdf/2402.06196

> https://cdn.openai.com/gpt-5-system-card.pdf

> https://storage.googleapis.com/deepmind-media/gemini/gemini_v2_5_report.pdf

> https://www-cdn.anthropic.com/de8ba9b01c9ab7cbabf5c33b80b7bbc618857627/Model_Card_Claude_3.pdf

### 正確性 (Knowledge accuracy)

1. 核心能力與知識基準
	- MMLU (Massive Multitask Language Understanding): 評估模型在 STEM、人文、社會科學等 57 個領域的多任務理解和一般知識
	- C-Eval: 評估模型在中文環境下的進階知識和推理能力，包含 52 個學科的考試
	- BIG-bench / BIG-Bench-Hard: 衡量 LLM 的能力和限制，更具挑戰性的任務
	- GPQA (Diamond): 測試專家級別、難以透過 Google 搜尋找到答案的問答（生物、物理、化學）
	- Humanity’s Last Exam (HLE): 測試模型在多學科上的挑戰性問題，涵蓋多學科專業知識
	- SimpleQA, TruthfulQA, TriviaQA, Natural Questions: 衡量模型在事實問答上的準確性
2. 推理、數學與程式設計
	- MATH, GSM8K, AIME 2025: 評估模型解決數學問題、代數操作等能力
	- HumanEval, APPS, MBPP: 衡量模型根據自然語言指令生成程式碼（Python）的能力
	- SWE-bench Verified: 評估模型解決真實軟體工程問題的能力，如修改程式碼庫中的錯誤
3. 多模態、長上下文與效率
	- MMMU (Massive Multi-discipline Multimodal Understanding): 評估模型在大學級別多學科多模態圖像理解和推理的能力
	- Vibe-Eval, ZeroBench: 具有挑戰性的圖像理解評估，需要多步驟推理
	- Needle In A Haystack (NIAH): 測試模型在極長文件（例如 200K Tokens）中間檢索和回憶特定資訊的準確性
	- LOFT, MRCR-V2: 評估模型在 1M 或更長上下文中的困難檢索任務和多針檢索能力

模型選用組選擇評測資料:

|Type|Benchmark|Desc|Dataset|Evaluation script|
|---|---|---|---|---|
|通用知識與語言理解|[MMLU](https://arxiv.org/abs/2009.03300)|評估模型在多任務環境下的語言理解與問題解決能力|[huggingface](https://huggingface.co/datasets/cais/mmlu) [github](https://github.com/hendrycks/test)|同左|
|通用知識與語言理解|[MMLU-Pro](https://arxiv.org/abs/2406.01574)|評估模型在多任務環境下的語言理解與問題解決能力|[huggingface](https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro)|同左|
|通用知識與語言理解|[Humanity’s Last Exam](https://arxiv.org/abs/2501.14249)|旨在評估模型在人類知識前沿的能力。|[huggingface](https://huggingface.co/datasets/cais/hle)|[github](https://github.com/centerforaisafety/hle)|
|通用知識與語言理解|AA-LCR (Artificial Analysis Long Context Reasoning)|衡量模型長上下文處理實用性的重要指標|[huggingface](https://huggingface.co/datasets/ArtificialAnalysis/AA-LCR) |沒找到|
|數學與邏輯推理|AIME|具挑戰性的競賽級數學問題基準 。它們要求模型具備深度邏輯、抽象思維和複雜的符號操作能力，能有效檢驗模型的推理上限 。|||
|數學與邏輯推理|MATH-500|具挑戰性的競賽級數學問題基準 。它們要求模型具備深度邏輯、抽象思維和複雜的符號操作能力，能有效檢驗模型的推理上限 。|[huggingface](https://huggingface.co/datasets/HuggingFaceH4/MATH-500)||
|程式碼生成|HumanEval|用於評估模型的程式碼生成能力。|[huggingface](https://huggingface.co/datasets/openai/openai_humaneval)||
|程式碼生成|[SWE-bench](https://arxiv.org/abs/2310.06770)|這個基準超越了單一函式的生成，要求模型解決來自真實 GitHub 開源專案的問題 (issues) |[huggingface](https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified)|[github](https://github.com/SWE-bench/SWE-bench)|
|對話與指令遵循|MT-Bench|專為評估模型在多輪對話中的能力(but現行資料不好找到現成指標)|
|對話與指令遵循|Chatbot Arena|透過讓真人使用者對兩個匿名模型的回答進行投票，來產生一個類似於棋類比賽的 Elo 評分 。這個分數被廣泛認為是衡量模型在真實世界對話中的實用性與人類偏好的黃金標準|

欲新增評測資料:

|Type|Benchmark|Desc|Dataset|Evaluation script|
|---|---|---|---|---|
|通用知識與語言理解|[C-Eval](https://arxiv.org/abs/2305.08322)|評估模型在中文環境下的進階知識和推理能力，包含 52 個學科的考試|[github](https://github.com/hkust-nlp/ceval) [huggingface](https://huggingface.co/datasets/ceval/ceval-exam)|[github](https://github.com/hkust-nlp/ceval)|
|通用知識與語言理解|MMMLU|OpenAI將MMLU翻譯成多國語言|[huggingface](https://huggingface.co/datasets/openai/MMMLU)|同MMLU|
|指令遵循|[Multi-IF](https://arxiv.org/abs/2410.15553)|MetaAI提出，針對8種語言測試多輪對話指令遵循能力，[Qwen3](https://arxiv.org/abs/2505.09388) paper中評測項目|[huggingface](https://huggingface.co/datasets/facebook/Multi-IF)|[github](https://github.com/facebookresearch/Multi-IF)|

### 一致性 (Consistency)

- 將相同的 Prompt 輸入給模型 N 次（例如 5 次），比較這 N 次輸出的語意相似度。
- 指標: 可以使用 BERTScore 或 ROUGE-L 等指標來計算輸出之間的平均相似度分數。分數越高，代表模型輸出越穩定。

### Hallucination

> https://github.com/RUCAIBox/HaluEval

HaluEval: 幻覺率評測資料
