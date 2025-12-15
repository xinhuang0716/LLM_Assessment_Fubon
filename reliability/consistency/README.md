# Consistency

透過將 Prompt 重複輸入 LLM，將 LLM 輸出結果用 Bert Score 計算語意相似度，得出模型一致性分數。

Prompt 來源：[MT-Bench first prompt](https://huggingface.co/datasets/HuggingFaceH4/mt_bench_prompts)

## Installation

Python version: 3.12

```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```shell
python main.py
```

### Configuration

Edit in `main.py`

```python
MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct" # Huggingface Model
OUTPUT_PATH = "outputs" # Output path

...

def run_evaluation():
    # --- Settings ---
    N_SAMPLES = 5       # Number of responses to generate per prompt
    TEMP = 0.7          # Temperature
    # Choose categories to test, set to None to test all
    # MT-Bench categories: coding, extraction, humanities, math, reasoning, roleplay, stem, writing
    TARGET_CATEGORIES = ['writing', 'reasoning', 'roleplay']
    MAX_TEST_SAMPLES = 3  # For testing, set to None for full run

```


## Output format

```json
{
  "meta": {
    "model": "Qwen/Qwen2.5-0.5B-Instruct",
    "n_samples": 5,
    "temperature": 0.7,
    "overall_score": 0.8753269056479136
  },
  "category_summary": {
    "writing": 0.8801201045513153,
    "roleplay": 0.8613503515720368,
    "reasoning": 0.8845102608203887
  },
  "details": [
    {
      "id": 44067482,
      "category": "writing",
      "prompt": "Compose an engaging travel blog post about a recent trip to Hawaii, highlighting cultural experiences and must-see attractions.",
      "consistency_score": 0.8632161021232605,
      "min_score": 0.8511378765106201,
      "responses": [
        "As the sun sets over the beautiful island of Maui, I'm reminded of my latest adventure - a 10-day trip to Hawaii. ... So pack your bags, grab your camera, and let's embark on another unforgettable journey to one of the most magical places in the world!",
        "Hey everyone! Today I want to share my latest adventure to Hawaii. ... I learned so much about Hawaiian culture while having such a",
        "As I sit down at the airport in Honolulu, my heart races with excitement as I board my plane for my next adventure around the world. ... I can't wait",
        "As the sun sets on our last day in Hawaii, we couldn't help but feel a sense of awe at the beauty of this magical island. ... We couldn't wait to return and explore more of this beautiful island paradise.",
        "Hi there! 🌟\n\nAs we conclude this year's adventure in the Hawaiian Islands, I can't help but reflect on how much of a unique experience it has been for me. ... So, what did you"
      ]
    },
    ...
  ]
}
```
