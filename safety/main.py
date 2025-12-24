import json
from utils.ollama import OllamaLLM
from utils.aoai import AOAILLM

import warnings
warnings.filterwarnings("ignore")

from BBQ.pipeline import runEvaluation as runBBQEvaluation
from BIPIA.pipeline import runEvaluation as runBIPIAEvaluation
from Toxicity.pipeline import runEvaluation as runToxicityEvaluation
from Toxicity.customLLM import AzureOpenAI, OllamaDeepEval


def main():
    # Load configurations
    with open("./config.json", "r", encoding="utf-8") as f: config = json.load(f)
    
    # Initialize LLMs with configurations
    ollama_llm = OllamaLLM(
        endpoint=config["ollama"]["endpoint"],
        model=config["ollama"]["model"]
    )
    
    aoai_llm = AOAILLM(
        endpoint=config["aoai"]["endpoint"],
        api_key=config["aoai"]["openai_api_key"]
    )
    
    simulator_llm = OllamaDeepEval(
        endpoint=config["ollama"]["endpoint"],
        model=config["ollama"]["model"]
    )
    
    evaluator_llm = AzureOpenAI(
        openai_api_version=config["aoai"]["openai_api_version"],
        azure_deployment=config["aoai"]["model"],
        azure_endpoint=config["aoai"]["azure_endpoint"],
        openai_api_key=config["aoai"]["openai_api_key"]
    )

    
    # Run Evaluation Pipeline - BBQ
    if config["assessment"].get("run_BBQ"):

        try:
            print("Starting BBQ Evaluation...")
            runBBQEvaluation(
                target_llm=ollama_llm,
                sample_size=config["assessment"]["sample_size"]
            )
            print("BBQ Evaluation completed!")

        except Exception as e:
            print(f"Error during BBQ Evaluation: {e}")

        print("\n" + "---"*20 + "\n")


    # Run Evaluation Pipeline - BIPIA
    if config["assessment"].get("run_BIPIA"):

        try:
            print("Starting BIPIA Evaluation...")
            runBIPIAEvaluation(
                target_llm=ollama_llm,
                eval_llm=aoai_llm,
                sample_size=config["assessment"]["sample_size"]
            )
            print("BIPIA Evaluation completed!")

        except Exception as e:
            print(f"Error during BIPIA Evaluation: {e}")

        print("\n" + "---"*20 + "\n")


    # Run Evaluation Pipeline - Toxicity
    if config["assessment"].get("run_Toxicity"):

        try:
            print("Starting Toxicity Evaluation...")
            runToxicityEvaluation(
                target_llm=ollama_llm, 
                sample_size=config["assessment"]["sample_size"],
                simulator_model=simulator_llm,
                evaluation_model=evaluator_llm
            )
            print("Toxicity Evaluation completed!")

        except Exception as e:
            print(f"Error during Toxicity Evaluation: {e}")


if __name__ == "__main__":
    main()
