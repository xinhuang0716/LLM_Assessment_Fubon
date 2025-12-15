from deepteam import red_team
from deepteam.vulnerabilities import ChildProtection, Toxicity, IllegalActivity, PersonalSafety
import warnings

warnings.filterwarnings("ignore")

from utils.ollama import ollama_response
from utils.customLLM import GeminiRequestsLLM


def main():
    # callback model for red teaming assessment
    async def model_callback(input: str) -> str:
        return ollama_response(prompt=input + "\nPlease DO NOT reply over `50` words.")

    # simulator and evaluation model
    customLLM = GeminiRequestsLLM(api_key="")

    # vulnerabilities
    vul_0 = ChildProtection(types=["exposure_interaction"])
    vul_1 = Toxicity(types=["profanity", "insults", "threats", "mockery"])
    vul_2 = IllegalActivity(types=["weapons", "illegal_drugs", "violent_crimes", "non_violent_crimes", "sex_crimes", "cybercrime", "child_exploitation"])
    vul_3 = PersonalSafety(types=["bullying", "self_harm", "unsafe_practices", "dangerous_challenges", "stalking"])


    # run red teaming
    risk_assessment = red_team(
        model_callback=model_callback,
        vulnerabilities=[vul_0, vul_1, vul_2, vul_3],
        attacks_per_vulnerability_type=1,
        simulator_model=customLLM,
        evaluation_model=customLLM,
    )

    # save testing records
    risk_assessment.save(to="./result")
    print(risk_assessment)


if __name__ == "__main__":
    main()
