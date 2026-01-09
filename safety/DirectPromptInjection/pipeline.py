import os, time, json, asyncio
from typing import Callable
from deepteam import red_team
from deepteam.vulnerabilities import Bias, Toxicity, IllegalActivity, PersonalSafety, ChildProtection, Ethics, Fairness, BFLA, BOLA, RBAC, ShellInjection, SQLInjection, IntellectualProperty,Misinformation,PIILeakage,PromptLeakage
from deepeval.models.base_model import DeepEvalBaseLLM
from deepteam.attacks.single_turn import PromptInjection

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
    vul_0 = Toxicity(types=["profanity", "insults", "threats", "mockery"])
    # vul_1 = IllegalActivity(types=["weapons", "illegal_drugs", "violent_crimes", "non_violent_crimes", "sex_crimes", "cybercrime", "child_exploitation"])
    # vul_2 = PersonalSafety(types=["bullying", "self_harm", "unsafe_practices", "dangerous_challenges", "stalking"])
    vul_3 = Bias(types=["race", "gender", "religion", "politics"])
    vul_4 = ChildProtection(types=["data_privacy", "age_verification","exposure_interaction"])
    vul_5 = Misinformation(types=["factual_errors", "unsupported_claims","expertize_misrepresentation"])
    vul_6 = Ethics(types=["harm_prevention", "moral_integrity", "responsible_transparency"])
    vul_7 = Fairness(types=["equality_consistency", "procedural_opportunity", "temporal_outcome"])
    vul_8 = BFLA(types=["privilege_escalation", "function_bypass", "authorization_bypass"])
    vul_9 = BOLA(types=["object_access_bypass", "cross_customer_access","unauthorized_object_manipulation"])
    vul_10 = RBAC(types=["role_bypass", "privilege_escalation","unauthorized_role_assumption"])
    vul_11 = ShellInjection(types=["command_injection", "shell_escape_sequences","system_command_execution"])
    vul_12 = SQLInjection(types=["blind_sql_injection", "union_based_injection","error_based_injection"])
    vul_13 = IntellectualProperty(types=["imitation", "copyright_violations","trademark_infringement","patent_disclosure"])
    vul_14 = PIILeakage(types=["direct_disclosure", "social_manipulation", "session_leak", "api_and_database_access"])
    vul_15 = PromptLeakage(types=["secrets_and_credentials", "guard_exposure","instructions","permissions_and_roles"])

    # Red teaming
    risk_assessment = red_team(
        model_callback=model_callback,
        vulnerabilities=[vul_0,vul_3,vul_4,vul_5,vul_6,vul_7,vul_8,vul_9,vul_10,vul_11,vul_12,vul_13,vul_14,vul_15],
        attacks_per_vulnerability_type=sample_size,
        attacks=[PromptInjection()], 
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

    file_name_log = f"./results/directpromptinjection_log_{time.strftime('%Y%m%d')}.json"
    file_name_result = f"./results/directpromptinjection_summary_{time.strftime('%Y%m%d')}.json"

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