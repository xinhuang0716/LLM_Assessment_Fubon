import itertools
import json
import os
from datetime import datetime

import numpy as np
import torch
from bert_score import score
from datasets import load_dataset
from openai import AzureOpenAI, OpenAI
from tqdm import tqdm
from transformers import set_seed

set_seed(42)

# --- CONFIGURATION ---

# Backend selection: "ollama" or "azure"
BACKEND_TYPE = "ollama"

# --- OLLAMA SETTINGS ---
OLLAMA_CONFIG = {
    "base_url": "http://localhost:11434/v1",
    "api_key": "ollama",
    "model": "llama3.1:8b"
}

# --- AZURE OPENAI SETTINGS ---
AZURE_CONFIG = {
    "endpoint": "https://YOUR_RESOURCE.openai.azure.com/",
    "api_key": "YOUR_API_KEY",
    "api_version": "2024-02-15-preview",
    "deployment_name": "gpt-4o"
}

# Device for BERTScore (metric calculation)
DEVICE = "cuda" if torch.cuda.is_available(
) else "mps" if torch.backends.mps.is_available() else "cpu"
OUTPUT_PATH = "outputs"


def get_client_and_model():
    """
    Returns the appropriate OpenAI client and model name 
    based on the BACKEND_TYPE configuration.
    """
    if BACKEND_TYPE == "ollama":
        print(f"Initializing Ollama client at {OLLAMA_CONFIG['base_url']}...")
        client = OpenAI(
            base_url=OLLAMA_CONFIG["base_url"],
            api_key=OLLAMA_CONFIG["api_key"]
        )
        return client, OLLAMA_CONFIG["model"]

    elif BACKEND_TYPE == "azure":
        print(
            f"Initializing Azure OpenAI client at {AZURE_CONFIG['endpoint']}...")
        client = AzureOpenAI(
            api_key=AZURE_CONFIG["api_key"],
            api_version=AZURE_CONFIG["api_version"],
            azure_endpoint=AZURE_CONFIG["endpoint"]
        )
        return client, AZURE_CONFIG["deployment_name"]

    else:
        raise ValueError(f"Unsupported backend type: {BACKEND_TYPE}")


def generate_responses(client, model_name, prompt, n=3, temperature=0.7):
    """
    Generates N responses using the unified OpenAI-compatible client.
    """
    responses = []

    for i in range(n):
        try:
            completion = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                n=1
            )

            content = completion.choices[0].message.content
            if content:
                responses.append(content)

        except Exception as e:
            print(f"Generation error (attempt {i+1}/{n}): {e}")

    return responses


def calculate_bertscore(responses, lang="en"):
    """
    Calculates the pairwise BERTScore similarity for the generated responses.
    """
    # Filter empty responses
    responses = [r for r in responses if r]

    if len(responses) < 2:
        return 0.0, 0.0

    # Create all unique pairs
    pairs = list(itertools.combinations(responses, 2))
    cands = [p[0] for p in pairs]
    refs = [p[1] for p in pairs]

    try:
        # verbose=False to keep logs clean
        P, R, F1 = score(cands, refs, lang=lang, verbose=False, device=DEVICE)
        mean_score = float(np.mean(F1.cpu().numpy()))
        min_score = float(np.min(F1.cpu().numpy()))
        return mean_score, min_score
    except Exception as e:
        print(f"BERTScore calculation failed: {e}")
        return 0.0, 0.0


def load_mt_bench_data(categories=None, max_samples=None):
    print("Loading MT-Bench dataset from Hugging Face...")
    dataset = load_dataset("./mt_bench_prompts", split="train")

    data_list = []
    for row in dataset:
        category = row['category']
        prompt = row['prompt'][0]

        if categories and category not in categories:
            continue

        data_list.append({
            "id": row['prompt_id'],
            "category": category,
            "prompt": prompt
        })

    if max_samples:
        data_list = data_list[:max_samples]

    print(f"Loaded {len(data_list)} test prompts.")
    return data_list


def run_evaluation():
    # 1. Setup Client
    client, model_name = get_client_and_model()

    # 2. Evaluation Parameters
    N_SAMPLES = 5
    TEMP = 0.1
    TARGET_CATEGORIES = ['writing', 'reasoning', 'roleplay']
    MAX_TEST_SAMPLES = 3  # Set to None to run all

    # 3. Load Data
    test_data = load_mt_bench_data(
        categories=TARGET_CATEGORIES, max_samples=MAX_TEST_SAMPLES
    )

    results = []
    category_stats = {}

    print(
        f"\nStarting consistency evaluation (Backend={BACKEND_TYPE}, Model={model_name})...\n")

    for item in tqdm(test_data, desc="Evaluating"):
        prompt = item['prompt']
        category = item['category']

        # Generate
        responses = generate_responses(
            client, model_name, prompt, n=N_SAMPLES, temperature=TEMP)

        if not responses:
            continue

        # Score
        mean_score, min_score = calculate_bertscore(responses)

        # Record
        result_entry = {
            "id": item['id'],
            "category": category,
            "prompt": prompt,
            "consistency_score": mean_score,
            "min_score": min_score,
            "responses": responses
        }
        results.append(result_entry)

        if category not in category_stats:
            category_stats[category] = []
        category_stats[category].append(mean_score)

    # 4. Reporting
    if not results:
        print("No results generated.")
        return

    overall_mean = np.mean([r['consistency_score'] for r in results])

    print("\n" + "="*40)
    print("Consistency Evaluation Report")
    print("="*40)
    print(f"Backend: {BACKEND_TYPE}")
    print(f"Model: {model_name}")
    print(f"Overall Mean Score: {overall_mean:.4f}")
    print("-" * 40)
    print("Category Breakdown:")

    summary_data = {}
    for cat, scores in category_stats.items():
        cat_mean = np.mean(scores)
        print(f"  - {cat.ljust(15)}: {cat_mean:.4f}")
        summary_data[cat] = cat_mean

    print("="*40)

    # 5. Save output
    output = {
        "meta": {
            "backend": BACKEND_TYPE,
            "model": model_name,
            "n_samples": N_SAMPLES,
            "temperature": TEMP,
            "overall_score": overall_mean
        },
        "category_summary": summary_data,
        "details": results
    }

    os.makedirs(OUTPUT_PATH, exist_ok=True)
    filename = f"consistency_{BACKEND_TYPE}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"

    with open(os.path.join(OUTPUT_PATH, filename), "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nResults saved to {filename}")


if __name__ == "__main__":
    run_evaluation()
