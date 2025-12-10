import json, random, tqdm
from typing import Callable
from utils.prompt import Prompt

def pipeline(attack_type: str, target_llm: Callable, eval_llm: Callable, seed: int = 42, sample_size: int = 5) -> list[dict]:
    """Pipeline function to process attack types and evaluate responses.

    Args:
        attack_type (str): Must be `email`, `qa`, `abstract`, `table`, or `code`
        target_llm (Callable): A Callable function that takes a prompt string and returns a response string, e.g., ollama_response.
        eval_llm (Callable): A Callable function that takes a prompt string and returns a response string, e.g., gemini_response.
        seed (int, optional): Random seed for sampling. Defaults to `42`.
        sample_size (int, optional): Sample size for testing data. Defaults to `10`.

    Raises:
        ValueError: If the attack type is invalid.

    Returns:
        list[dict]: A list of dictionaries containing the results of the pipeline, including prompts, responses, and evaluations.
    """
            
    # check attack type validity
    if attack_type not in ("email", "qa", "abstract", "table", "code"):
        raise ValueError("Invalid attack type. Must be 'email', 'qa', 'abstract', 'table', or 'code'.")

    # Load testing data
    with open(f"./dataset/{attack_type}.json", "r") as file: testing_data = json.load(file)
    
    random.seed(seed)
    testing_indices: list[int] = random.sample(range(len(testing_data)), min(len(testing_data), sample_size))

    # Attack and Evaluation Loop
    results: list[dict] = []
    for idx in tqdm.tqdm(testing_indices, desc="Processing attacks"):

        # LLM Response
        testing_prompt = Prompt.construct(
            context=testing_data[idx]["context"],
            question=testing_data[idx]["question"],
            attack_type=attack_type
        )
        response = target_llm(testing_prompt)

        # LLM Evaluation
        attack_name, attack_idx = testing_data[idx]["attack_name"].split("-")
        #print("idx:", idx, "attack_name:", attack_name, "attack_idx:", attack_idx)
        judge_prompt = Prompt.judge_prompt(
            attack_type=attack_type,
            attack_name=attack_name,
            attack_idx=int(attack_idx),
            response=response
        )
        eval_response = eval_llm(judge_prompt)

        results.append({
            "idx": idx,
            "attack_type": attack_type,
            "attack_name": attack_name,
            "attack_idx": attack_idx,
            "testing_prompt": testing_prompt,
            "response": response,
            "eval_response": eval_response
        })

    return results