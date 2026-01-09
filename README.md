## Task

- Design evaluation target: Safety, Reliability (Stability), Interpretability, and Transparency.
- Build test datasets and scenario simulations.
- Develop automated testing tools (using Python, LangChain, pytest, etc.).
- Establish a reporting mechanism to automatically generate reports after each test.

📌 The scope is limited to the LLM model itself and does not extend to other LLM services or applications.

## Project Structure

```
LLM_Assessment_Fubon/
├── 📄 README.md
│
├── 🛡️ safety/
│   ├── 🔍 BBQ/                             # Bias benchmark
│   ├── 🧩 BIPIA/                           # Indirect prompt injection benchmark
│   ├── 🛠️ DirectPromptInjection/           # Direct prompt injection tests
│   ├── 🔐 InformationDisclosure/           # Information leakage tests
│   ├── ❗ Misinformation/                  # Misinformation detection
│   └── ☣️ Toxicity/                        # Toxicity evaluation
│
├── ✅ reliability/
│   ├── 📚 ceval/                           # C-Eval benchmark
│   └── 🔄 consistency/                     # Consistency checks
│
├── 🔍 explainability/
│   ├── 🧠 cot/                             # Chain-of-Thought evaluation
│   └── 📖 citation/                        # Citation validation
│
└── 🔎 transparency/
```

## Evaluation Results

|      Type      |          Subtype          |  Metric   | GPT-4o | Llama3.1:8B | Gemma3:12B | GPT-OSS:20B |
| :------------: | :-----------------------: | :-------: | :----: | :---------: | :--------: | :---------: |
|     Safety     |     Fairness and Bias     | Accuracy  |  94%   |     41%     |    77%     |     84%     |
|     Safety     |         Toxicity          | Pass Rate |   -    |     92%     |    96%     |     92%     |
|     Safety     |  Information Disclosure   | Pass Rate |  96%   |     89%     |    86%     |     87%     |
|     Safety     |      Misinformation       | Pass Rate |  99%   |     90%     |            |             |
|     Safety     |  Direct Prompt Injection  | Pass Rate |  94%   |     79%     |    63%     |     92%     |
|     Safety     | Indirect Prompt Injection |    ASR    |  70%   |     70%     |    73%     |     55%     |
|  Reliability   |Knowledge Accuracy (C-Eval)|  Accuracy |  74%   |     48%     |            |             |
|  Reliability   |        Consistency        | Bert Score|  94%   |     92%     |            |             |
| Explainability |   Chain-of-Thoughts(CoT)  | Pass Rate |        |             |            |             |
| Explainability |   Citation validation     | Pass Rate |        |             |            |             |

- GPT-4o can't complete Toxicity tests due to Azure OpenAI Service content policy restrictions.
- Each subtype conduct 30 test cases, and the metrics are calculated based on the average performance across all cases.
- For Direct Prompt Injection, since there are several subtypes, we will conduct 10 test cases for each subtype.
- To see more details, please refer to the respective `results` folders under each evaluation target.

## TO-DO

- [x] Design Evaluation Framework
- [x] Build Test Dataset and Testing Python Script
- [ ] Refactoring Testing Framework
- [ ] Output Test Report in more structured and visualized way
- [ ] Packaging the Testing Framework as a Python Library or some alternatives
