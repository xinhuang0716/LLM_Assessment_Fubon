---
license: apache-2.0
task_categories:
- question-answering
- conversational
language:
- en
tags:
- evaluation
pretty_name: MT Bench
size_categories:
- n<1K
---

# MT Bench by LMSYS
This set of evaluation prompts is created by the [LMSYS org](https://huggingface.co/lmsys) for better evaluation of chat models.
For more information, see the [paper](https://arxiv.org/abs/2306.05685).


### Dataset loading
To load this dataset, use 🤗 datasets:
```python
from datasets import load_dataset
data = load_dataset(HuggingFaceH4/mt_bench_prompts, split="train")
```
### Dataset creation
To create the dataset, we do the following for our internal tooling. 
* rename `turns` to `prompts`,
* add empty `reference` to remaining prompts (for HF Datasets),
* Use the following code to load and save as a dataset
```python
from datasets import load_dataset
import hashlib

data = load_dataset("json", data_files="https://huggingface.co/datasets/HuggingFaceH4/mt_bench_prompts/raw/main/raw/question.jsonl", split="train")

# %% create_dataset.ipynb 11
def format_example(example):
    return {
        "prompt": example["prompt"],
        "prompt_id": int(hashlib.sha256(''.join(example["prompt"]).encode("utf-8")).hexdigest(), 16) % (10 ** 8),
        "category": example["category"],
        "reference": example["reference"],
    }

formatted_ds = data.map(format_example, num_proc=6, remove_columns=data.column_names)

# 
formatted_ds.push_to_hub("HuggingFaceH4/mt_bench_prompts", split="train")
```