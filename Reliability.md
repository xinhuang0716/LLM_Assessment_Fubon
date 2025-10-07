

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

### 一致性 (Consistency)

- 將相同的 Prompt 輸入給模型 N 次（例如 5 次），比較這 N 次輸出的語意相似度。
- 指標: 可以使用 BERTScore 或 ROUGE-L 等指標來計算輸出之間的平均相似度分數。分數越高，代表模型輸出越穩定。

### Hallucination

> https://github.com/RUCAIBox/HaluEval

HaluEval: 幻覺率評測資料
