# Safety Evaluation Pipeline for Large Language Models

A comprehensive Python-based framework for evaluating the safety and robustness of large language models (LLMs) across three critical dimensions: **Bias**, **Prompt Injection**, and **Toxicity**.

## Overview

This project provides automated evaluation pipelines to assess LLM safety through:

- **BBQ (Bias Benchmark for QA)**: Evaluates social biases across 9 demographic categories
- **BIPIA (Indirect Prompt Injection Attack)**: Tests resilience against prompt injection attacks
- **Toxicity Red Teaming**: Assesses safety vulnerabilities using adversarial testing

## Project Structure

```
Safety/
├── main.py                 # Entry point for running evaluations
├── config.json             # Configuration for LLMs and assessments
├── pyproject.toml          # Project dependencies
├── BBQ/                    # Bias evaluation module
│   └── ...                 
├── BIPIA/                  # Prompt injection evaluation module
│   └── ...                 
├── Toxicity/               # Toxicity evaluation module
│   └── ...                 
├── utils/                  # LLM interface utilities
│   ├── ollama.py           # Ollama LLM interface
│   └── aoai.py             # Azure OpenAI LLM interface
└── results/                # Evaluation outputs (automatically generated)
```


## Configuration

Edit `config.json` to configure your evaluation setup:

```json
{
  "ollama": {
    "model": "llama3.1:8b",
    "endpoint": "http://localhost:11434/api/generate"
  },
  "aoai": {
    "model": "gpt-4o",
    "endpoint": "<your-azure-openai-endpoint>",
    "openai_api_version": "2024-12-01-preview",
    "azure_endpoint": "<your-azure-endpoint>",
    "openai_api_key": "<your-api-key>"
  },
  "assessment": {
    "sample_size": 100,
    "run_BBQ": true,
    "run_BIPIA": true,
    "run_Toxicity": true
  }
}
```

### Configuration Parameters

- **ollama**: Target LLM configuration (model under test)
  - `model`: Ollama model name
  - `endpoint`: Ollama API endpoint
  
- **aoai**: Evaluator/Simulator LLM configuration (Azure OpenAI)
  - `model`: Azure OpenAI deployment name
  - `endpoint`: Full Azure OpenAI endpoint URL
  - `openai_api_key`: Azure OpenAI API key
  
- **assessment**: Evaluation settings
  - `sample_size`: Number of test cases per evaluation
  - `run_BBQ`: Enable/disable bias evaluation
  - `run_BIPIA`: Enable/disable prompt injection evaluation
  - `run_Toxicity`: Enable/disable toxicity evaluation

## Usage

Run all enabled evaluations:

(the virtual environment and dependencies will be automatically handled)

```bash
uv run main.py
```

The pipeline will execute the selected evaluations sequentially and save results to the `results/` directory.

## Evaluation Modules

### 1. BBQ (Bias Benchmark)

Evaluates model biases across 9 social dimensions:
- Age
- Disability Status
- Gender Identity
- Nationality
- Physical Appearance
- Race/Ethnicity
- Religion
- Socioeconomic Status (SES)
- Sexual Orientation

**Output**: Bias scores and detailed logs in `results/bbq_*`

See [BBQ/README.md](BBQ/README.md) for detailed documentation.

### 2. BIPIA (Indirect Prompt Injection)

Tests resilience against prompt injection attacks in:
- Email content
- Code snippets
- Data tables

**Output**: Security vulnerability scores in `results/bipia_*`

See [BIPIA/README.md](BIPIA/README.md) for detailed documentation.

### 3. Toxicity Red Teaming

Uses adversarial testing to identify safety vulnerabilities across multiple toxicity categories using DeepTeam framework.

**Output**: Toxicity scores and vulnerability reports in `results/toxicity_*`

See [Toxicity/README.md](Toxicity/README.md) for detailed documentation.


## LLM Roles

- **Target LLM** (Ollama): The model being evaluated for safety
- **Evaluator LLM** (Azure OpenAI): Judges responses for bias/toxicity/safety
- **Simulator LLM** (Ollama/Azure OpenAI): Generates adversarial test cases
