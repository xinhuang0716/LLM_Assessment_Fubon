import json, random, tqdm
from typing import Callable

from BIPIA.prompt import Prompt


def eval(target_llm: Callable, eval_llm: Callable, seed: int = 42, sample_size: int = 30) -> list[dict]:
    """Pipeline function to process attack types and evaluate responses.

    Args:
        target_llm (Callable): A Callable function that takes a prompt string and returns a response string, e.g., OllamaLLM.
        eval_llm (Callable): A Callable function that takes a prompt string and returns a response string, e.g., AOAILLM.
        seed (int, optional): Random seed for sampling. Defaults to `42`.
        sample_size (int, optional): Sample size for testing data. Defaults to `30`.

    Returns:
        list[dict]: A list of dictionaries containing the results of the pipeline, including `idx`, `attack_type`, `attack_name`, `attack_idx`, `testing_prompt`, `response`, and `eval_response`.
    """

    random.seed(seed)
    testing_results: list[dict] = []

    for attack_type in ("email", "table", "code"):

        # Load testing data
        with open(f"./BIPIA/dataset/{attack_type}.json", "r", encoding="utf-8") as file: testing_data = json.load(file)
        testing_indices: list[int] = random.sample(range(len(testing_data)), min(len(testing_data), sample_size))

        # Attack and Evaluation Loop
        for idx in tqdm.tqdm(testing_indices, desc=f"Processing {attack_type.capitalize()}"):

            # LLM Response
            if attack_type == "code":
                testing_prompt = Prompt.construct(
                    attack_type=attack_type,
                    context=testing_data[idx]["context"],
                    question=None,
                    code=testing_data[idx]["code"],
                    error=testing_data[idx]["error"],
                )

            else:
                testing_prompt = Prompt.construct(
                    attack_type=attack_type,
                    context=testing_data[idx]["context"],
                    question=testing_data[idx]["question"],
                    code=None,
                    error=None,
                )

            response = target_llm(testing_prompt)

            # LLM Evaluation
            attack_name, attack_idx = testing_data[idx]["attack_name"].split("-")
            judging_prompt = Prompt.judging_prompt(
                attack_type=attack_type,
                attack_name=attack_name,
                attack_idx=int(attack_idx),
                response=response,
            )
            eval_response = eval_llm(judging_prompt)

            # Store Results
            testing_results.append(
                {
                    "idx": idx,
                    "attack_type": attack_type,
                    "attack_name": attack_name + "-" + str(attack_idx),
                    "context": testing_data[idx]["context"],
                    **(
                        {
                            "code": testing_data[idx]["code"],
                            "error": testing_data[idx]["error"],
                        }
                        if attack_type == "code"
                        else {"question": testing_data[idx]["question"]}
                    ),
                    "response": response,
                    "eval_response": eval_response,
                }
            )

    return testing_results
