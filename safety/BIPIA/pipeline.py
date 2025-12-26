import time, json, os
from typing import Callable

from BIPIA.evaluation import eval
from BIPIA.score import ASR


def runEvaluation(target_llm: Callable, eval_llm: Callable, sample_size: int):
    
    # Assessment
    result = eval(target_llm=target_llm, eval_llm=eval_llm, sample_size=sample_size)

    # Calculate overall scores
    scores: dict = {}
    responses = [i["eval_response"] for i in result]
    scores["overall"] = ASR(responses)

    # Calculate scores for each bias type   
    for attack_type in ["email", "table", "code"]:
        responses = [i["eval_response"] for i in result if i["attack_type"] == attack_type]
        scores[attack_type] = ASR(responses)

    # Save results
    os.makedirs("./results", exist_ok=True)

    file_name_log = f"./results/bipia_log_{time.strftime("%Y%m%d")}.json"
    file_name_result = f"./results/bipia_summary_{time.strftime("%Y%m%d")}.json"

    with open(file_name_log, "w", encoding="utf-8") as f: json.dump(result, f, ensure_ascii=False, indent=4)
    with open(file_name_result, "w", encoding="utf-8") as f: json.dump(scores, f, ensure_ascii=False, indent=4)

