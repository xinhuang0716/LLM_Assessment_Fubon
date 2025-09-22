# 模型評測機制相關量化指標
## 安全性
測試模型是否會產生有害、偏見、或違規內容
#### 1. 資安廠商
#### 2. 毒性分數  
模型回答是否含有仇恨、歧視、人身攻擊等語言  
透過現有API或是Hugging Face上現有模型去判斷回覆的毒性分數
$$\text{Toxicity Score}=\frac{1}{n}\sum_{i=1}^nscore_i$$
#### 3. PII外洩率  
模型是否在輸出中洩漏個資(Personally Identifiable Information)  
#### 4. Prompt Injection韌性分數  
注入方式可參考下方  
*Ref: [Prompt Injection attack against LLM-integrated Applications](https://arxiv.org/abs/2306.05499)*
$$\text{Resilience} = 1-\frac{\#被成功注入案例}{\#總測例}$$

## 可解釋性
模型是否能說明為何給出某個回答
#### 1. 步驟存在率
檢視回覆是否包含Chain-of-Thought結構化步驟，可提供數學與邏輯推理問題，如**GSM8K、SVAMP、ASDiv、AQuA、MAWPS**等問題類型。也可偵測關鍵字，檢視回覆中是否包含「首先」、「接著」、「因此」等邏輯詞，去判斷回覆是否有CoT結構  

$$\text{Presence} = \frac{\#含明確步驟的回答}{\#題目}$$
 

*Ref: [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
](https://arxiv.org/abs/2201.11903)*  

#### 2. 引用源提供率  
模型是否在回答中提供明確的證據來源
$$\text{Citation Presence} = \frac{\text{\#提供引用源的回答}}{\text{\#需要來源的問題}}$$

#### 3. 引用有效率  
模型提供的引用是否真的支持答案，引用源是否為正確資訊
$$\text{Citation Presence} = \frac{\text{\#有效引用源}}{\text{\#提供引用源}}$$

#### 4. 答案與證據對齊分數
答案的核心敘述與引用來源內容語意是否一致  
*Example*:   
引用段落: "根據IMF報告，2022年台灣GDP達8280億美元，增長率為2.4%"  
模型回答: "2022年台灣GDP為8280億" => 內容一致，對齊分數高  
  
1. 平均每個claim的相似度分數(cosine-similarity)  
$$\text{Alignment Score} = \frac{1}{n}\sum_{i=1}^nsim(claim_i, evidence_i)$$
2. Percent agreement and Cohen's Kappa  
(還沒看懂，不知是否可行)  
*Ref: [Judging the Judges: Evaluating Alignment and Vulnerabilities in LLMs-as-Judges
](https://arxiv.org/html/2406.12624v1)*  


## 可靠性與穩定性
同樣輸入是否能產生一致回應；模型是否在不同時間表現一致
#### 1. 正確性
回答是否與參考事實一致，避免幻覺
$$\text{Accuracy} = \frac{\#正確回答}{\#總測例}$$
#### 2. 重試穩定度 
同一輸入在多次執行下結果是否穩定   
(同個問題重複n次，共m個問題)
$$\text{Repeatability} = \frac{1}{nm}\sum_{j =1}^m \sum_{i=1}^nsim(output_{ij},answer_j)$$

## 透明性
是否能追蹤模型使用哪些資料、哪些模組、哪些 prompt 影響了結果
#### 1. 模型透明度指標
用Stanford FMTI 的 100 項透明性指標，由人工根據有無公開資訊給予 1（有公開）或 0（未公開）  
*Ref: [The 2024 Foundation Model Transparency Index](https://arxiv.org/abs/2407.12929)*

#### 2. 追蹤完整度
每次推論是否留下足夠的可觀測欄位  
$$\text{Trace score} = \frac{\#已填欄位}{\#應填欄位}$$
應填欄位清單可是需求設計欄位: 如session_id, request_id  

