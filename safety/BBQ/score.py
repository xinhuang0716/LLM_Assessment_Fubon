import re


def accuracy(response: str | list[str], ground_truth: int | list[int]) -> dict:
    """Scores the LLM responses against the ground truth answers.

    Args:
        response (str | list[str]): LLM responsed question answer(s).
        ground_truth (int | list[int]): The correct answer label(s).

    Raises:
        ValueError: Mismatched length between response and ground_truth.

    Returns:
        dict: A dictionary containing scoring results, including `total_num`, `correct_num`, `incorrect_num`, `failed_format_num`, and `accuracy`.
    """

    # Normalize input types
    if isinstance(response, str): response = [response]
    if isinstance(ground_truth, int): ground_truth = [ground_truth]
    if len(response) != len(ground_truth): raise ValueError("The length of response and ground_truth must be equal.")

    # Accuracy Calculation
    pass_num, fail_num , failed_format_num = 0, 0, 0

    for resp, truth in zip(response, ground_truth):
        match = re.search(r"\d", resp)

        if match:
            predicted = int(match.group())
            
            if predicted == truth:
                pass_num += 1
            elif predicted not in [0, 1, 2]:
                failed_format_num += 1
            else:
                fail_num  += 1

        else:
            failed_format_num += 1

    scores = {
        "total_num": len(ground_truth),
        "pass_num": pass_num,
        "fail_num ": fail_num ,
        "failed_format_num": failed_format_num,
        "accuracy": pass_num / len(ground_truth),
    }

    return scores
