# BBQ Bias Benchmark Evaluation

> A Python-based framework for evaluating LLM bias across multiple social dimensions using the Bias Benchmark for QA (BBQ) dataset.

<img width="700" height="450" alt="image" src="https://github.com/user-attachments/assets/fb2c0a58-8174-4f08-949c-cb0f7786b163" />

## Overview

This tool assesses how language models handle questions that could reveal social biases. It measures model tendency to rely on stereotypes versus providing unbiased answers across nine bias categories including age, gender, race, religion, and more.

## Features

- **9 Bias Categories**: Age, disability status, gender identity, nationality, physical appearance, race/ethnicity, religion, socioeconomic status, sexual orientation
- **Flexible LLM Integration**: Support for any LLM via callable functions (Ollama included)
- **Automated Scoring**: Multiple-choice answer evaluation with format validation
- **Rich Visualizations**: Color-coded results table with per-category accuracy metrics

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
result = pipeline(
    target_llm=ollama_response,  # Model under test
    sample_size=30,              # Questions per bias type
    seed=42                      # Random seed
)
```

### Custom LLM Integration

Implement any LLM by creating a function with signature `(prompt: str) -> str`:

```python
def custom_llm(prompt: str) -> str:
    # Your LLM API call here
    return response_text

result = pipeline(target_llm=custom_llm)
```

### Bias Categories

- **Age**: Stereotypes about older/younger individuals
- **Disability_status**: Biases regarding people with disabilities
- **Gender_identity**: Gender-based assumptions
- **Nationality**: National origin stereotypes
- **Physical_appearance**: Appearance-based biases
- **Race_ethnicity**: Racial and ethnic stereotypes
- **Religion**: Religious affiliation biases
- **SES**: Socioeconomic status assumptions
- **Sexual_orientation**: LGBTQ+ related biases

### Running Assessments

```bash
python main.py
```

Results are saved to `results/results_{date}.json`

## Project Structure

```
BBQ/
├── main.py              # Entry point and workflow orchestration
├── requirements.txt     # Dependencies
├── dataset/            # Bias benchmark datasets
│   ├── Age.json
│   ├── Disability_status.json
│   ├── Gender_identity.json
│   └── ...
├── utils/              # Core modules
│   ├── pipeline.py     # Assessment pipeline
│   ├── prompt.py       # Prompt templates
│   ├── score.py        # Scoring calculation logic
│   ├── display.py      # Rich console visualization
│   └── ollama.py       # Ollama integration
└── results/            # Output directory
```

## Architecture

The project follows a clean separation of concerns:

- **`main.py`**: Orchestrates the workflow (pipeline → scoring → display)
- **`pipeline.py`**: Handles data loading and LLM response collection
- **`score.py`**: Pure calculation logic for evaluation metrics
- **`display.py`**: Rich console formatting and visualization
- **`ollama.py`**: LLM integration interface

## Output Format

Each result contains:

```json
{
  "bias_type": "Age",
  "idx": 0,
  "context": "...",
  "question": "...",
  "answers_choice": ["Option 0", "Option 1", "Option 2"],
  "correct_answer": 2,
  "response": "..."
}
```

## Scoring Metrics

- **Total**: Number of questions tested
- **Correct**: Unbiased answers matching ground truth
- **Incorrect**: Wrong answer choices
- **Failed Format**: Responses not following expected format
- **Accuracy**: Percentage of correct answers

