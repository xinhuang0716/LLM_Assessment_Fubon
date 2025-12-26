# C-Eval

使用 C-Eval 評測 LLM 的可靠性，Model backend 支援 Ollama, AOAI。

## Installation

Python version: 3.12

```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


## Usage

```shell
python run_ceval.py
```


### Configuration
Open run_ceval.py and modify the configuration section at the top:

1. Select Backend

```python
# Set to "ollama" or "azure"
BACKEND_TYPE = "ollama"
```

2. Configure Credentials

For Ollama:

```python
OLLAMA_CONFIG = {
    "base_url": "http://localhost:11434/v1",
    "model": "llama3.1:8b"
}
```

For Azure OpenAI:

```python
AZURE_CONFIG = {
    "endpoint": "https://YOUR_RESOURCE.openai.azure.com/",
    "api_key": "YOUR_API_KEY",
    "api_version": "2025-01-01",
    "deployment_name": "gpt-4o"
}
```

3. Test Scope

```python
# True = Run all 52 subjects; False = Run specific list
RUN_ALL_SUBJECTS = True 

# Number of questions per subject (None = Run all questions)
TEST_COUNT_PER_SUBJECT = 5
```


The script generates a JSON file (e.g., ceval_full_report_20251226_120000.json) with the following structure:

```json
{
    "summary": {
        "overall_accuracy": 65.5,
        "total_questions": 100,
        "total_correct": 65
    },
    "subject_breakdown": {
        "computer_network": { "accuracy": 80.0, "correct": 4, "total": 5 }
    },
    "details": [
        {
            "subject": "computer_network",
            "question": "TCP protocol belongs to...",
            "options": {
                "A": "Application Layer",
                "B": "Transport Layer",
                "C": "Network Layer",
                "D": "Link Layer"
            },
            "prediction": "B",
            "ground_truth": "B",
            "is_correct": true,
            "raw_output": "The answer is B"
        }
    ]
}
```
