import argparse
import json
import os
import time

import lm_eval
from lm_eval.tasks import TaskManager


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--split", type=str, choices=[
                        "valid", "test"], default="valid", help="Choose to run on validation set or test set")
    parser.add_argument("--model", type=str, default="hf")
    parser.add_argument("--model_args", type=str,
                        default="pretrained=Qwen/Qwen2.5-0.5B-Instruct")
    parser.add_argument("--output_path", type=str, default="output")
    parser.add_argument("--log_samples", action="store_true",
                        help="Whether to log samples")
    args = parser.parse_args()

    task_manager = TaskManager(include_path="./custom_tasks")

    target_group = f"ceval-{args.split}"

    print(
        f"Running evaluation on C-Eval [{args.split} set] (Group: {target_group})...")

    results = lm_eval.simple_evaluate(
        model=args.model,
        model_args=args.model_args,
        tasks=[target_group],
        task_manager=task_manager,
        batch_size="1",
        device="cuda",
        log_samples=args.log_samples,
        num_fewshot=5,
    )

    if results is not None:
        print(results["results"])

        output_file = os.path.join(
            args.output_path, f"result_ceval_{args.split}__{time.strftime("%Y%m%d")}.json")
        os.makedirs(args.output_path, exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2, default=str, ensure_ascii=False)
            print(f"Results saved to {output_file}")


if __name__ == "__main__":
    main()
