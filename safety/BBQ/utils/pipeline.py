import json, random, tqdm
from typing import Callable
from utils.prompt import Prompt


def pipeline(target_llm: Callable, seed: int = 42, sample_size: int = 10) -> list[dict]:
    """Assessment pipeline for BBQ dataset.
    
    Args:
        target_llm (Callable): A Callable function that takes a prompt string and returns a response string, e.g., ollama_response.
        seed (int, optional): Random seed for sampling. Defaults to `42`.
        sample_size (int, optional): Sample size for testing data. Defaults to `10`.

    Returns:
        list[dict]: A list of dictionaries containing the results of the pipeline, including `idx`, `context`, `question`, `answers_choice`, `correct_answer`, and `response`.
    """

    random.seed(seed)
    results: list[dict] = []

    for bias_type in ["Age", "Disability_status", "Gender_identity", "Nationality", "Physical_appearance", "Race_ethnicity", "Religion", "SES", "Sexual_orientation"]:

        # Load testing data
        with open(f"./dataset/{bias_type}.json", "r", encoding="utf-8") as file: testing_data = json.load(file)
        testing_indices: list[int] = random.sample(range(len(testing_data)), min(len(testing_data), sample_size))

        # Attack and Evaluation Loop
        for idx in tqdm.tqdm(testing_indices, desc=f"Processing {bias_type}"):

            # LLM Response
            testing_prompt = Prompt.construct(
                context := testing_data[idx]["context"],
                question := testing_data[idx]["question"],
                ans0 := testing_data[idx]["ans0"],
                ans1 := testing_data[idx]["ans1"],
                ans2 := testing_data[idx]["ans2"],
            )
            response = target_llm(testing_prompt)

            results.append(
                {
                    "bias_type": bias_type,
                    "idx": testing_data[idx]["example_id"],
                    "context": context,
                    "question": question,
                    "answers_choice": [ans0, ans1, ans2],
                    "correct_answer": testing_data[idx]["label"],
                    "response": response,
                }
            )

    return results