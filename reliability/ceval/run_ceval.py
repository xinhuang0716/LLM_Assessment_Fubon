import json
import re
from datetime import datetime

from datasets import get_dataset_config_names, load_dataset
from openai import AzureOpenAI, OpenAI
from tqdm import tqdm

# ================= CONFIGURATION =================

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
    "api_version": "2025-01-01",
    "deployment_name": "gpt-4o"
}

# --- EVALUATION SCOPE ---
# Set to True to evaluate all 52 C-Eval subjects.
RUN_ALL_SUBJECTS = True

# Specific subjects to test if RUN_ALL_SUBJECTS is False
TEST_SUBJECTS = ["computer_network", "operating_system"]

# Number of questions to test per subject (Set to None for all)
TEST_COUNT_PER_SUBJECT = 5

# =================================================


def get_client():
    """Initialize the API client based on the selected backend."""
    if BACKEND_TYPE == "azure":
        return AzureOpenAI(
            azure_endpoint=AZURE_CONFIG["endpoint"],
            api_key=AZURE_CONFIG["api_key"],
            api_version=AZURE_CONFIG["api_version"]
        )
    else:
        return OpenAI(
            base_url=OLLAMA_CONFIG["base_url"],
            api_key=OLLAMA_CONFIG["api_key"]
        )


def get_model_name():
    """Retrieve the model identifier based on the selected backend."""
    return AZURE_CONFIG["deployment_name"] if BACKEND_TYPE == "azure" else OLLAMA_CONFIG["model"]


def get_response(client, prompt):
    """Send request to LLM and retrieve the generated text."""
    try:
        response = client.chat.completions.create(
            model=get_model_name(),
            messages=[
                {
                    "role": "system",
                    "content": "You are an exam assistant. Please answer with the correct option letter (A, B, C, or D) only. Do not provide explanations."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=5
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"  [Error] API Request failed: {e}")
        return ""


def extract_answer(text):
    """Parse the response to extract the first occurrence of A, B, C, or D."""
    match = re.search(r"([A-D])", text.upper())
    return match.group(1) if match else "UNKNOWN"


def main():
    # Retrieve subject list
    print("--- Initializing Subject List ---")
    if RUN_ALL_SUBJECTS:
        try:
            subjects = get_dataset_config_names("./ceval-exam-zhtw")
            print(f"Loaded all {len(subjects)} subjects.")
        except Exception as e:
            print(f"[Error] Failed to fetch subject list: {e}")
            return
    else:
        subjects = TEST_SUBJECTS
        print(f"Using manual subject list: {subjects}")

    # Initialize report structure
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"ceval_full_report_{timestamp}.json"

    final_report = {
        "meta": {
            "timestamp": timestamp,
            "backend": BACKEND_TYPE,
            "model": get_model_name()
        },
        "summary": {
            "total_questions": 0,
            "total_correct": 0,
            "overall_accuracy": 0.0
        },
        "subject_breakdown": {},
        "details": []
    }

    client = get_client()

    # Execution Loop
    total_q = 0
    total_c = 0

    for idx, subject in enumerate(subjects):
        print(f"\n[{idx+1}/{len(subjects)}] Evaluating: {subject}")

        try:
            dataset = load_dataset(
                "./ceval-exam-zhtw", subject, split="val")
        except Exception as e:
            print(f"  [Skipped] Failed to load dataset for {subject}: {e}")
            final_report["subject_breakdown"][subject] = {"error": str(e)}
            continue

        limit = TEST_COUNT_PER_SUBJECT if TEST_COUNT_PER_SUBJECT else len(
            dataset)
        sub_correct = 0
        sub_total = 0

        for i, item in tqdm(enumerate(dataset), desc="Progress", unit="q", leave=False, total=limit):
            if i >= limit:
                break

            # Format prompt
            options_text = f"A. {item['A']}\nB. {item['B']}\nC. {item['C']}\nD. {item['D']}"
            prompt = f"{item['question']}\n{options_text}\n\nAnswer:"

            # Inference
            raw_out = get_response(client, prompt)
            pred = extract_answer(raw_out)
            truth = item['answer']
            is_correct = (pred == truth)

            # Update counters
            if is_correct:
                sub_correct += 1
            sub_total += 1

            # Log details (Updated to include options)
            final_report["details"].append({
                "subject": subject,
                "id": i,
                "question": item['question'],
                "options": {
                    "A": item['A'],
                    "B": item['B'],
                    "C": item['C'],
                    "D": item['D']
                },
                "prediction": pred,
                "ground_truth": truth,
                "is_correct": is_correct,
                "raw_output": raw_out
            })

        # Calculate subject-level accuracy
        sub_acc = (sub_correct / sub_total * 100) if sub_total > 0 else 0
        print(f"  -> Result: {sub_acc:.1f}% ({sub_correct}/{sub_total})")

        # Update global counters
        total_q += sub_total
        total_c += sub_correct

        # Record breakdown
        final_report["subject_breakdown"][subject] = {
            "accuracy": sub_acc,
            "correct": sub_correct,
            "total": sub_total
        }

    # Save
    if total_q > 0:
        final_report["summary"]["total_questions"] = total_q
        final_report["summary"]["total_correct"] = total_c
        final_report["summary"]["overall_accuracy"] = (total_c / total_q) * 100

    print(f"\n========================================")
    print(
        f"Evaluation Complete. Overall Accuracy: {final_report['summary']['overall_accuracy']:.2f}%")
    print(f"Saving report to: {output_filename}")

    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(final_report, f, indent=2, ensure_ascii=False)

    print("Done.")


if __name__ == "__main__":
    main()
