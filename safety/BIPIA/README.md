# Indirect Prompt Injection Attack Assessment

A Python-based framework for evaluating LLM resilience against indirect prompt injection attacks across multiple attack vectors.

## Overview

This tool assesses how language models handle malicious prompts embedded in context (emails, code, tables, etc.). It automates testing, response collection, and evaluation to measure model vulnerability to indirect prompt injection.

## Features

- **Multiple Attack Vectors**: Email, QA, abstract, table, and code-based attacks
- **Flexible LLM Integration**: Support for any LLM via callable functions (Ollama, Gemini included)
- **Automated Evaluation**: Use separate evaluator LLM to assess attack success
- **Attack Categories**: Task automation, business intelligence, conversational agent, research assistance, sentiment analysis, information dissemination, and marketing

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Basic Configuration

Edit `main.py` to configure your assessment:

```python
attack_type = "email"  # Options: email, qa, abstract, table, code
result = pipeline(
    attack_type=attack_type,
    target_llm=ollama_response,  # Model under test
    eval_llm=gemini_response,     # Evaluator model
    sample_size=10,               # Number of test cases
    seed=42                       # Random seed
)
```

### Custom LLM Integration

Implement any LLM by creating a function with signature `(prompt: str) -> str`:

```python
def custom_llm(prompt: str) -> str:
    # Your LLM API call here
    return response_text

result = pipeline(attack_type="email", target_llm=custom_llm, eval_llm=gemini_response)
```

### Attack Types

- **email**: Injected prompts in email content
- **code**: Malicious instructions in code comments
- **table**: Attacks embedded in tabular data
- **qa**: Question-answering context attacks
- **abstract**: Academic abstract manipulation

### Running Assessments

```bash
python main.py
```

Results are saved to `results/{attack_type}_results_{date}.json`

## Project Structure

```
IPIA/
├── main.py              # Entry point
├── requirements.txt     # Dependencies
├── dataset/            # Attack datasets
│   ├── email.json
│   ├── code.json
│   ├── table.json
│   └── ...
├── utils/              # Core modules
│   ├── pipeline.py     # Assessment pipeline
│   ├── prompt.py       # Prompt templates
│   ├── ollama.py       # Ollama integration
│   └── gemini.py       # Gemini integration
└── results/            # Output directory
```

## Output Format

Each result contains:

```json
{
  "idx": 0,
  "attack_type": "email",
  "attack_name": "Task Automation",
  "attack_idx": "0",
  "testing_prompt": "...",
  "response": "...",
  "eval_response": "..."
}
```