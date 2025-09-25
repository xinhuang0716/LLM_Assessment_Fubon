# 可解釋性
模型是否能說明為何給出某個回答  

#### 1. 步驟存在率
檢視回覆是否包含Chain-of-Thought結構化步驟，可提供數學與邏輯推理問題，如**GSM8K、SVAMP、ASDiv、AQuA、MAWPS**等問題類型。也可偵測關鍵字，檢視回覆中是否包含「首先」、「接著」、「因此」等邏輯詞，去判斷回覆是否有CoT結構  

$$\text{Presence} = \frac{\#含明確步驟的回答}{\#題目}$$
 

*Ref: [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
](https://arxiv.org/abs/2201.11903)*(2023)  

#### 2. 引用源提供率  
模型是否在回答中提供明確的證據來源

$$\text{Citation Presence} = \frac{\text{\#提供引用源的回答}}{\text{\#需要來源的問題}}$$

#### 3. 引用有效率  
模型提供的引用是否真的支持答案，引用源是否為正確資訊

$$\text{Citation Validity} = \frac{\text{\#有效引用源}}{\text{\#提供引用源}}$$

#### 4. 答案與證據對齊分數
答案的核心敘述與引用進行語意相似度辨識  

*Example*:   
```
引用段落: "根據IMF報告，2022年台灣GDP達8280億美元，增長率為2.4%"  
模型回答: "2022年台灣GDP為8280億" => 內容一致，對齊分數高  
``` 
平均每個claim的相似度分數(cosine-similarity, BERTScore)  

$$\text{Alignment Score} = \frac{1}{n}\sum_{i=1}^nsim(claim_i, evidence_i)$$

#### 5. 可模擬性（Simulatability）評估
可模擬性定義: 人類能否根據模型提供的解釋，準確預測模型在其他類似情境下的行為  
論文提出**精確度(Precision)** 指標去評估模型的可模擬性，人類根據模型的解釋，對「類似但不同的問題（反事實輸入）」所做的預測，跟模型實際的回答有多一致。  
$$\text{Precision} = \frac{1}{|C^*|} \sum_{x' \in C^*} \mathbf{1}[h_{\text{ex}}(x') = o_{x'}]$$

其中 $C^*$為反事實輸入集合，$x'$為反事實輸入，$h_{\text{ex}}(x')$代表人類根據模型的解釋對$x'$所做的預測，$o_{x'}$為模型對$x'$的實際輸出


*Example:* 
``` 
問題：「老鷹會飛嗎？」  
模型回答：「會」  
模型解釋：「因為所有鳥都會飛」

根據原始問題，產生一些類似但不同的問題(由LLM生成)，例如：
「企鵝會飛嗎？」
「鴕鳥會飛嗎？」
「麻雀會飛嗎？」
「蝙蝠會飛嗎？」

人類看到「所有鳥都會飛」這個解釋，可能會這樣預測：
「企鵝會飛」→ 預測：會
「鴕鳥會飛」→ 預測：會
「麻雀會飛」→ 預測：會
「蝙蝠會飛」→ 預測：不會

模型可能這樣回答：
「企鵝會飛」→ 不會
「鴕鳥會飛」→ 不會
「麻雀會飛」→ 會
「蝙蝠會飛」→ 會
```

疑慮: 人類預測可能沒有辦法自動化(?)  
*Ref: [Do Models Explain Themselves? Counterfactual Simulatability of Natural Language Explanations](https://arxiv.org/abs/2307.08678)* (2023)





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