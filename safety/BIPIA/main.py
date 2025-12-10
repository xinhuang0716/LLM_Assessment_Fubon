import os, time, json
from utils.ollama import ollama_response
from utils.gemini import gemini_response
from utils.pipeline import pipeline


def main():
    
    # assessment pipeline
    attack_type = "email"
    result = pipeline(attack_type=attack_type, target_llm=ollama_response, eval_llm=gemini_response, sample_size=3)

    # results
    os.makedirs("results", exist_ok=True)
    file_name = f"results/{attack_type}_results_{time.strftime("%Y%m%d")}.json"
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
