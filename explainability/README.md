# 可解釋性評測機制

本機制旨在檢驗大型語言模型在回答問題時，是否能清楚呈現其**推理過程**與**決策依據**，以確保模型輸出的透明度與可信度，也是提升使用者信任與滿足合規要求的重要環節。

1. **思維鍊的邏輯推理合理性**  
   - 檢查模型的推理過程是否具備合理性與一致性，避免出現跳躍、矛盾或無依據的推論。

2. **引用來源的可信度**  
   - 評估模型提供的資料來源是否真實、可靠，並能支持其最終結論，避免虛構或不準確的引用。  
  

## 評測指標：思維鍊邏輯推理合理性

本指標採用 OpenAI 提供的 **`GSM8K` 資料集**，該資料集包含小學數學題目，專門用於數學推理與步驟解釋，適合檢視語言模型的 **思維鍊品質**。

- [OpenAI - GM8SK](https://github.com/openai/grade-school-math)

本指標旨在檢查語言模型在回答問題時，推理過程是否合理且具備邏輯性，並分為四個層級：

---
### **Level 1: Final Answer Accuracy（最終答案正確性）**
- **目的**：檢查最終答案是否正確  
- **方法**：直接比較 `reference['final_answer']` 與 `response['final_answer']`  
- **評分**：二元制（`1.0` 或 `0.0`）  
- **意義**：最基本的評測，只看結果是否正確  

---

### **Level 2: Steps Ratio（步驟結構完整性）**
- **目的**：檢查回答的步驟數量是否合理  
- **方法**：計算 `response步驟數 ÷ reference步驟數` 的比例  
- **評分邏輯**：  
  - `0.8 ≤ ratio ≤ 1.2` → **1.0 分**（步驟數合理）  
  - `ratio < 0.8` → 步驟過少，按比例扣分（最低 **0.2**）  
  - `ratio > 1.2` → 步驟過多，按比例扣分（最低 **0.5**）  
- **意義**：確保模型不會跳步或過度冗長  

---

### **Level 3: Steps Similarity（推理過程相似度）**
- **目的**：檢查推理過程與參考答案的相似程度  
- **方法**：使用 **Jaccard Similarity** 比較三個維度：  
  - **Operators（運算子）**：`+`, `-`, `*`, `/` 的使用情況  
  - **Numbers（數字）**：運算式中出現的數字  
  - **Words（關鍵詞）**：推理文字中的英文詞彙  
- **評分**：加權平均（Operators: 40%，Numbers: 40%，Words: 20%）  
- **意義**：評估模型的推理路徑是否與標準答案一致  

---

### **Level 4: Coherence（邏輯連貫性）**
- **目的**：檢查推理的正確性與連貫性  
- **方法**：檢查兩個面向：  
  1. **Accuracy（運算正確性）**：每個算式的計算結果是否正確  
  2. **Coherence（邏輯連貫性）**：算式中的數字來源是否有跡可循  
     - Step 1：數字必須來自 `given_numbers`  
     - Step 2+：數字必須來自 `given_numbers` 或前面步驟的結果  
- **評分**：加權平均（Accuracy: 75%，Coherence: 25%）  
- **意義**：確保推理過程不僅結構相似，且邏輯嚴謹  

---

#### Example:
```
Question:
"Farmer Red has three milk cows: Bess, Brownie, and Daisy. Bess, the smallest cow, gives him two pails of milk every day. Brownie, the largest cow, produces three times that amount. Then Daisy makes one pail more than Bess. How many pails of milk does Farmer Red get from them each week?"

Reference Answer:
Bess produces 2 pails every day.
Brownie produces 3 times as much * 2 = <<3*2=6>>6 pails every day.
Daisy produces 2 + 1 more pail than Bess = <<2+1=3>>3 pails every day.
Bess, Brownie, and Daisy together produce 2 + 6 + 3 = <<2+6+3=11>>11 pails every day.
A week is 7 days, so Farmer Red gets 11 * 7 = <<11*7=77>>77 pails each week.
#### 77

Model Answer:
Bess gives 2 pails of milk every day because <<2=2>>2.  
Brownie gives three times Bess's daily amount because <<2*3=6>>6.  
Daisy gives one pail more than Bess because <<2+1=3>>3.  
Total daily milk from all cows is <<2+6+3=11>>11.  
A week has 7 days because <<7=7>>7.  
Total weekly milk is <<11*7=77>>77.  
#### 77
```
#### Evaluation:
```
# Level 1:
模型回覆的最終答案與資料提供之參考答案相同 -> 正確 (Score: 1.0)

# Level 2:
模型回覆的總步數為 6，參考答案的總步數為 5 -> Step Ratio為 1.2 (Score: 1.0)

# Level 3:
拆解運算式與回覆內容後，模型回覆與參考答案使用的運算子與數字吻合，文字上敘述稍有不同 -> 經加權後，Step Similiarity為 (Score: 0.853)

# Level 4:
模型回覆中的運算式皆正確，然而，在一致性的表現上，因為些許步驟的說明較冗贅(如第 5 步)，可能導致一致性判斷上有偏誤，經加權後，Coherence為 (Score: 0.917)

最終加權分數為 0.95 -> 通過!
```



## 評測指標：引用來源的可信度

本指標採用 Google 推出的 **`Natural Questions`** 資料集，用於檢驗語言模型回答問題時，引用來源是否真實且能支持結論，以提升透明度並降低「幻覺」風險，該資料集包含真實搜尋問題及 Wikipedia 標準答案，適合檢視引用來源的可信度。

- [Google - Natural Questions](https://ai.google.com/research/NaturalQuestions)

本指標旨在檢查語言模型在回答問題時，引用來源是否正確且支持回覆時，分為幾個面向：
本

---
### **Citation Support（引用來源支持度）**
- **目的**：檢查模型提供的引用來源敘述是否支持其回覆  
- **方法**：透過LLM 比較 `citation['claim']` 與 `response['model_answer']`，判斷兩者語意關係  
- **評分**：
  - **`ENTAILMENT`** -> 引用完全支持回答 -> **Score: 1.0**
  - **`NEUTRAL`** -> 引用內容與回答支持度不顯著 -> **Score: 0.5**
  - **`CONTRADICTION`** -> 引用內容與回答相矛盾 -> **Score: 0.0**  

- **意義**：確認引用內容支持模型回覆之答案  
---
### **Source Verification（引用來源驗證）**
- **目的**：檢查模型引用的內容是否真實來自所提供的來源（URL 或參考資料）。
- **方法**：驗證引用內容與來源的一致性，包括 URL 有效性、頁面內容與敘述內容是否相符 
- **評分**： 
    - **`VERIFIED`** -> 來源有效且可訪，引用內容來自所述來源 
    - **`UNCERTAIN`** -> 無法確定引用內容來自所述來源  
    - **`LIKELY_FABRICATED`** -> 來源無效，可能為虛構內容
- **意義**： 確保引用來源真實，避免模型虛構資訊，提升可信度

---

### **Interpretability Score(引用來源解釋性)**
- **目的**：以`Citation Support`與`Source Verification`之判斷給予一個整體分數
- **評分**： `0.0` - `1.0`
---
### **Answer Correctness（答案正確性）**
- **目的**：檢查模型的最終回答是否與標準答案（gold standard）一致。
- **方法**：比較 LLM 回答中的主要論點與標準答案，評估整體正確性（以答案層級為單位，而非逐一引用）。
評分標準：
**`CORRECT`** → 回答與標準答案高度一致  
**`PARTIALLY_CORRECT`** → 回答部分正確，但有遺漏或輕微錯誤  
**`INCORRECT`** → 回答與標準答案不一致或錯誤  

- **意義**：確保模型在整體層面提供準確答案，而非僅依靠引用或片段資訊。

---
#### Example
```
Quesion:
When did the titanic sank how many died.

Reference Answer:
"Sinking of the RMS Titanic The number of casualties of the sinking is unclear, due to a number of factors, including confusion over the passenger list, which included some names of people who cancelled their trip at the last minute, and the fact that several passengers travelled under aliases for various reasons and were double-counted on the casualty lists.[228] The death toll has been put at between 1,490 and 1,635 people.[229] The figures below are from the British Board of Trade report on the disaster.[230]"

Model Answer:
"The RMS Titanic sank on April 15, 1912 [1]. It is estimated that more than 1,500 people lost their lives in the disaster [2], although some sources put the death toll as high as 1,635 [3]."

Citation Claims:
[1] "The RMS Titanic sank on April 15, 1912"
[2] "It is estimated that more than 1,500 people lost their lives in the disaster"
[3] "The death toll could be as high as 1,635"
```

#### Evaluation:
```
# Citation Support:
[1] ENTAILMENT | 1.0
引用的 Wikipedia 內容明確指出鐵達尼號在 1912 年 4 月 15 日沉沒，這直接支持該主張

[2] ENTAILMENT | 1.0
引用的 National Geographic 內容明確指出，在鐵達尼號災難中有超過 1,500 人喪生，這直接支持該主張

[3] ENTAILMENT | 1.0
引用的《大英百科全書》內容明確指出，估計的死亡人數範圍在 1,495 至 1,635 之間，這直接支持該主張

# Source Verification:
[1] VERIFIED 
提供的 URL 有效且可訪問，內容與主張一致。來源具有可信度（Wikipedia），且資訊與預期內容相符

[2] VERIFIED 
提供的 URL 有效，內容與主張一致。National Geographic 是可信來源，且資訊與主題及預期內容相符

[3] VERIFIED 
《大英百科全書》是可信來源，且資訊與主題及預期內容相符

整體引用來源分數 Interpretability Score -> 1.0

# Answer Correctness
模型回覆答案語意與資料提供之標準答案相符 -> CORRECT

最終加權分數為 1.0 -> 通過!
```

## **可解釋性通過標準**
以兩維度的最終分數為依據，計算加權總分，並與預設門檻值（Threshold）比較（相關權重與門檻值設定可參考 `config.py`）
- 判定規則：
  - 若加權總分 ≥ Threshold → 標註為「通過」 
  - 若加權總分 < Threshold → 標註為「未通過」 

## Reference

[1] Liu, X., Zhang, Z., Hou, Y., Wang, X., & Liu, Q. (2023). *Explainability for large language models: A survey.* arXiv. https://doi.org/10.48550/arXiv.2309.01029

[2] Chang, Y., Wang, X., Wang, J., Wu, Y., Yang, L., Zhu, K., Chen, H., Yi, X., Wang, C., Wang, Y., Ye, W., Zhang, Y., Chang, Y., Yu, P. S., Yang, Q., & Xie, X. (2023). *A survey on evaluation of large language models.* arXiv. https://doi.org/10.48550/arXiv.2307.03109

[3]  Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H., Kaiser, L., Plappert, M., Tworek, J., Hilton, J., Nakano, R., Hesse, C., & Schulman, J. (2021). *Training verifiers to solve math word problems.* arXiv. https://doi.org/10.48550/arXiv.2110.14168

[4] Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E. H., Le, Q. V., & Zhou, D. (2022). *Chain‑of‑Thought Prompting Elicits Reasoning in Large Language Models.* In Advances in Neural Information Processing Systems (NeurIPS 2022). arXiv. https://doi.org/10.48550/arXiv.2201.11903

[5]  Gao, T., Yen, H., Yu, J., & Chen, D. (2023). *Enabling large language models to generate text with citations.* In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing (pp. 6465–6488). Association for Computational Linguistics. https://doi.org/10.48550/arXiv.2305.14627

[6] Zheng, L., Chiang, W.-L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E. P., Zhang, H., Gonzalez, J. E., & Stoica, I. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.* arXiv. https://doi.org/10.48550/arXiv.2306.05685

## Structure
```

XAIEvaluator
├─ core
│  ├─ common
│  │  ├─ __init__.py
│  │  ├─ paths.py
│  │  ├─ clients
│  │  │  ├─ __init__.py
│  │  │  ├─ client_protocol.py
│  │  │  ├─ azure_oai.py
│  │  │  ├─ gemini.py
│  │  │  └─ llama3.py
│  │  └─ batch
│  │     ├─ __init__.py
│  │     └─ async_batch_runner.py
│  ├─ evaluators
│  │  ├─ __init__.py
│  │  ├─ result_processor.py
│  │  ├─ score_aggregator.py
│  │  ├─ cot
│  │  │  ├─ __init__.py
│  │  │  └─ evaluator.py
│  │  └─ citation
│  │     ├─ __init__.py
│  │     ├─ parser.py
│  │     └─ evaluator.py
│  └─ pipelines
│     ├─ __init__.py
│     └─ run_all.py
├─ prompt
│  ├─ cot_prompt.txt
│  ├─ citation_judge_prompt.txt
│  └─ citation_response_prompt.txt
├─ data
│  ├─ gsm8k.parquet
│  └─ nq.parquet
└─ main.py
```

## Installation
Python Version: `3.11+`
```
pip install -r requirements.txt
```

## Usage
```
python main.py
```


## Configuration
可在 `main.py` 中設定，手動設定LLM相對應之`API_KEY`、`endpoint`、`temperature`等相關參數。於`run_all()`驅動流程，可調整各指標**抽樣的題數**、**抽樣方式**、**與RANDOM模式的seed**等。
```
# 下方示例
cot_answer_llm = AsyncLlamaClient(
      model='llama3.1:8b',
      temperature=0.3,
)

cite_answer_llm = AsyncLlamaClient(
      model='llama3.1:8b',
      temperature=0.3,
)

cite_judge_llm = AsyncAzureOAIClient(
    api_key="AOAI_API_KEY",
    azure_endpoint=azure_endpoint,
    api_version=api_version,
    model="gpt-4o"
)

reports = await run_all(
    gsm8k_path=str(data_dir() / "gsm8k.parquet"),
    nq_path=str(data_dir() / "nq.parquet"),
    cot_answer_llm=cot_answer_llm,
    cite_answer_llm=cite_answer_llm,
    cite_judge_llm=cite_judge_llm,
    cot_sample_method="random",
    cot_n_samples=30,
    cot_random_state= 50,
    citation_sample_method="random",
    citation_n_samples=5,
    citation_random_state = 50,
    )
```




## Output Format
相關結果可參考輸出後的 `output/FINAL_RESULTS_YYYYMMDD.json`檔案
```
{
  "XAI_overall_score": 0.823,
  "overall_pass": true,
  "overall_threshold": 0.8,
  "cot": {
    "model": "llama3.1:8b",
    "avg_score": 0.808,
    "count": 30,
    "pass": true,
    "threshold": 0.8
  },
  "citation": {
    "response_model": "llama3.1:8b",
    "judge_model": "gpt-4o",
    "avg_score": 0.8375,
    "count": 5,
    "pass": true,
    "threshold": 0.8
  },
  "weights": {
    "weight_cot": 0.5,
    "weight_citation": 0.5
  }
}
```

