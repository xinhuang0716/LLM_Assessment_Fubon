import time, json, os
from typing import Callable

from BBQ.evaluation import eval
from BBQ.score import accuracy


def runEvaluation(target_llm: Callable, sample_size: int):

    # Assessment
    result = eval(target_llm=target_llm, sample_size=sample_size)

    # Calculate overall scores
    scores: dict = {}
    responses = [i["response"] for i in result]
    ground_truths = [i["correct_answer"] for i in result]
    scores["overall"] = accuracy(responses, ground_truths)

    # Calculate scores for each bias type   
    for bias_type in ["Age", "Disability_status", "Gender_identity", "Nationality", "Physical_appearance", "Race_ethnicity", "Religion", "SES", "Sexual_orientation"]:
        responses = [i["response"] for i in result if i["bias_type"] == bias_type]
        ground_truths = [i["correct_answer"] for i in result if i["bias_type"] == bias_type]
        scores[bias_type] = accuracy(responses, ground_truths)

    # Save results
    os.makedirs("./results", exist_ok=True)

    file_name_log = f"./results/bbq_log_{time.strftime("%Y%m%d")}.json"
    file_name_result = f"./results/bbq_summary_{time.strftime("%Y%m%d")}.json"

    with open(file_name_log, "w", encoding="utf-8") as f: json.dump(result, f, ensure_ascii=False, indent=4)
    with open(file_name_result, "w", encoding="utf-8") as f: json.dump(scores, f, ensure_ascii=False, indent=4)

