import os, time, json
from utils.ollama import ollama_response
from utils.pipeline import pipeline
from utils.score import score
from utils.display import display_scores_table, display_overall_scores


def main():
    # Assessment pipeline
    result = pipeline(target_llm=ollama_response, sample_size=30)

    # Save results
    os.makedirs("results", exist_ok=True)
    file_name = f"results/results_{time.strftime("%Y%m%d")}.json"
    with open(file_name, "w", encoding="utf-8") as f: json.dump(result, f, ensure_ascii=False, indent=4)

    # Calculate scores for each bias type   
    scores = {}
    for bias_type in ["Age", "Disability_status", "Gender_identity", "Nationality", "Physical_appearance", "Race_ethnicity", "Religion", "SES", "Sexual_orientation"]:
        responses = [i["response"] for i in result if i["bias_type"] == bias_type]
        ground_truths = [i["correct_answer"] for i in result if i["bias_type"] == bias_type]
        scores[bias_type] = score(responses, ground_truths)

    # Calculate overall scores
    responses = [i["response"] for i in result]
    ground_truths = [i["correct_answer"] for i in result]
    overall_score = score(responses, ground_truths)

    # Display results
    display_scores_table(scores)
    display_overall_scores(overall_score)


if __name__ == "__main__":
    main()
