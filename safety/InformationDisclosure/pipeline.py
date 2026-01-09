import os, time, json, asyncio
from typing import Callable
from deepteam import red_team
from deepteam.vulnerabilities import PIILeakage, PromptLeakage
from deepeval.models.base_model import DeepEvalBaseLLM

import warnings
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
    vul_0 = PIILeakage(types=["direct_disclosure", "api_and_database_access", "session_leak", "social_manipulation"])
    vul_1 = PromptLeakage(types=["secrets_and_credentials", "instructions", "guard_exposure", "permissions_and_roles"])
    
    # Red teaming
    risk_assessment = red_team(
        model_callback=model_callback,
        vulnerabilities=[vul_0, vul_1],
        attacks_per_vulnerability_type=sample_size,
        simulator_model=simulator_model,
        evaluation_model=evaluation_model,
        ignore_errors=False
    )

    # Save results
    os.makedirs("./results", exist_ok=True)

    risk_assessment.save(to="./results")

    file_name = [i for i in os.listdir("./results") if i.startswith(time.strftime("%Y%m%d") + "_")][0]
    with open(f"./results/{file_name}", "r", encoding="utf-8") as f: result = json.load(f)
    os.remove(f"./results/{file_name}")

    file_name_log = f"./results/information_disclosure_log_{time.strftime('%Y%m%d')}.json"
    file_name_result = f"./results/information_disclosure_summary_{time.strftime('%Y%m%d')}.json"

    # Calculate overall statistics
    overview = result["overview"]
    total_passing = sum(item["passing"] for item in overview.get("vulnerability_type_results", []))
    total_failing = sum(item["failing"] for item in overview.get("vulnerability_type_results", []))
    total_errored = sum(item["errored"] for item in overview.get("vulnerability_type_results", []))
    total_tests = total_passing + total_failing + total_errored
    
    overall_pass_rate = total_passing / total_tests if total_tests > 0 else 0.0
    
    # Add overall statistics to overview
    overview["overall_pass_rate"] = overall_pass_rate
    overview["overall_passing"] = total_passing
    overview["overall_failing"] = total_failing
    overview["overall_errored"] = total_errored
    overview["overall_total"] = total_tests

    with open(file_name_log, "w", encoding="utf-8") as f: json.dump(result["test_cases"], f, ensure_ascii=False, indent=4)
    with open(file_name_result, "w", encoding="utf-8") as f: json.dump(overview, f, ensure_ascii=False, indent=4)

    #print(risk_assessment)