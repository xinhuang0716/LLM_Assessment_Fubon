import asyncio
import json
import os
import time
import warnings
from typing import Callable

from deepeval.models.base_model import DeepEvalBaseLLM
from deepteam import red_team
from deepteam.vulnerabilities import Misinformation

warnings.filterwarnings("ignore")


def runEvaluation(target_llm: Callable, simulator_model: DeepEvalBaseLLM, evaluation_model: DeepEvalBaseLLM, sample_size: int):

    # Callback model for red teaming assessment
    async def model_callback(input: str) -> str:
        try:
            loop = asyncio.get_event_loop()
            prompt = input + "\nPlease DO NOT reply over `50` words."
            result = await loop.run_in_executor(None, lambda: target_llm(prompt))
            return result
        except Exception as e:
            print(f"Error in model_callback: {e}")
            raise

    # Vulnerabilities
    vul_0 = Misinformation(
        types=["factual_errors", "unsupported_claims", "expertize_misrepresentation"])

    # Red teaming
    risk_assessment = red_team(
        model_callback=model_callback,
        vulnerabilities=[vul_0],
        attacks_per_vulnerability_type=sample_size,
        simulator_model=simulator_model,
        evaluation_model=evaluation_model,
        ignore_errors=False
    )

    # Save results
    os.makedirs("./results", exist_ok=True)

    risk_assessment.save(to="./results")

    file_name = [i for i in os.listdir(
        "./results") if i.startswith(time.strftime("%Y%m%d") + "_")][0]
    with open(f"./results/{file_name}", "r", encoding="utf-8") as f:
        result = json.load(f)
    os.remove(f"./results/{file_name}")

    file_name_log = f"./results/misinformation_log_{time.strftime("%Y%m%d")}.json"
    file_name_result = f"./results/misinformation_summary_{time.strftime("%Y%m%d")}.json"

    with open(file_name_log, "w", encoding="utf-8") as f:
        json.dump(result["test_cases"], f, ensure_ascii=False, indent=4)
    with open(file_name_result, "w", encoding="utf-8") as f:
        json.dump(result["overview"], f, ensure_ascii=False, indent=4)

    # print(risk_assessment)
