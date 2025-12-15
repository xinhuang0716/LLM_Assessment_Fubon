import itertools
import json
import os
from datetime import datetime

import numpy as np
import torch
from bert_score import score
from datasets import load_dataset
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed

set_seed(42)

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
OUTPUT_PATH = "outputs"

print(f"Loading model: {MODEL_ID}...")
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        dtype="auto",
        device_map="auto"
    )

    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id

    print("Model loaded successfully!")
except Exception as e:
    print(f"Failed to load model: {e}")
    exit()


def get_hf_responses(prompt: str, n: int = 5, temperature: float = 0.7):
    """Use HF model to generate N responses for the same prompt"""

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True)
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    with torch.no_grad():
        generated_ids = model.generate(
            model_inputs.input_ids,
            max_new_tokens=512,
            do_sample=True,
            temperature=temperature,
            top_p=0.9,
            num_return_sequences=n,
            pad_token_id=tokenizer.pad_token_id
        )

    input_len = model_inputs.input_ids.shape[1]
    responses = []
    for output_ids in generated_ids:
        generated_text = tokenizer.decode(
            output_ids[input_len:], skip_special_tokens=True)
        responses.append(generated_text)

    return responses


def calculate_bertscore(responses, lang="en"):
    if len(responses) < 2:
        return 0.0, 0.0

    pairs = list(itertools.combinations(responses, 2))
    cands = [p[0] for p in pairs]
    refs = [p[1] for p in pairs]

    P, R, F1 = score(cands, refs, lang=lang, verbose=True,
                     device=DEVICE)

    mean_score = float(np.mean(F1.cpu().numpy()))
    min_score = float(np.min(F1.cpu().numpy()))

    return mean_score, min_score


def load_mt_bench_data(categories=None, max_samples=None):
    """
    Load MT-Bench Prompts from Hugging Face
    categories: list, e.g. ['reasoning', 'writing']
    max_samples: limit the number of samples for testing
    """
    print("Loading MT-Bench dataset...")
    dataset = load_dataset("HuggingFaceH4/mt_bench_prompts", split="train")

    data_list = []
    for row in dataset:
        category = row['category']
        prompt = row['prompt'][0]  # Use the first prompt variant

        if categories and category not in categories:
            continue

        data_list.append({
            "id": row['prompt_id'],
            "category": category,
            "prompt": prompt
        })

    if max_samples:
        data_list = data_list[:max_samples]

    print(f"Loaded {len(data_list)} test prompts (source: MT-Bench)")
    return data_list


def run_evaluation():
    # --- Settings ---
    N_SAMPLES = 5       # Number of responses to generate per prompt
    TEMP = 0.7          # Temperature
    # Choose categories to test, set to None to test all
    # MT-Bench categories: coding, extraction, humanities, math, reasoning, roleplay, stem, writing
    TARGET_CATEGORIES = ['writing', 'reasoning', 'roleplay']
    MAX_TEST_SAMPLES = 3  # For testing, set to None for full run

    test_data = load_mt_bench_data(
        categories=TARGET_CATEGORIES, max_samples=MAX_TEST_SAMPLES)

    results = []
    category_stats = {}  # To accumulate scores per category

    print(
        f"\nStarting consistency evaluation (N={N_SAMPLES}, Temp={TEMP})...\n")

    for item in tqdm(test_data, desc="Evaluating"):
        prompt = item['prompt']
        category = item['category']

        # Generate N responses
        try:
            responses = get_hf_responses(prompt, n=N_SAMPLES, temperature=TEMP)

            # Calculate scores
            mean_score, min_score = calculate_bertscore(responses, lang="en")

            # Results
            result_entry = {
                "id": item['id'],
                "category": category,
                "prompt": prompt,
                "consistency_score": mean_score,
                "min_score": min_score,
                "responses": responses
            }
            results.append(result_entry)

            # Accumulate scores per category
            if category not in category_stats:
                category_stats[category] = []
            category_stats[category].append(mean_score)

        except Exception as e:
            print(f"\n[Error] ID {item['id']} failed: {e}")

    # Generate report
    overall_mean = np.mean([r['consistency_score'] for r in results])

    print("\n" + "="*40)
    print("LLM Consistency Evaluation Report")
    print("="*40)
    print(f"Model: {MODEL_ID}")
    print(f"Overall Mean Score: {overall_mean:.4f}")
    print("-" * 40)
    print("Category Breakdown:")

    # Output average scores per category
    summary_data = {}
    for cat, scores in category_stats.items():
        cat_mean = np.mean(scores)
        print(f"  - {cat.ljust(15)}: {cat_mean:.4f}")
        summary_data[cat] = cat_mean

    print("="*40)

    # Save detailed results to JSON
    output = {
        "meta": {
            "model": MODEL_ID,
            "n_samples": N_SAMPLES,
            "temperature": TEMP,
            "overall_score": overall_mean
        },
        "category_summary": summary_data,
        "details": results
    }

    os.makedirs(OUTPUT_PATH, exist_ok=True)
    with open(os.path.join(OUTPUT_PATH, f"reliability_consistency_results_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"), "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(
        f"\nDetailed results saved to reliability_consistency_results_{datetime.now().strftime('%Y%m%d%H%M%S')}.json")


if __name__ == "__main__":
    run_evaluation()
