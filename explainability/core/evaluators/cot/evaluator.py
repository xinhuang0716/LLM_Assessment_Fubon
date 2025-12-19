import re
from typing import Dict, List, Union, Any
from collections import Counter
from core.common.paths import prompt_dir
from core.config import CoTConfig

class CoTEvaluator:
    """
    Evaluates Chain-of-Thought reasoning quality by analyzing mathematical problem solving steps.
    
    This evaluator assesses CoT responses across four levels:
    - Level 1: Final answer accuracy
    - Level 2: Solution structure (step count ratio)
    - Level 3: Steps similarity (operations, numbers, keywords)
    - Level 4: Logic coherence and calculation validity
    """
    name = "cot"

    def __init__(self, answer_llm, config: CoTConfig):
        """
        Initialize CoTEvaluator with an LLM client and configuration.
        
        Args:
            answer_llm: LLM client for generating CoT answers to math problems.
            config: CoTConfig object containing evaluation thresholds and weights.
        """
        self.answer_llm = answer_llm
        self.cfg = config

    def parse(self, question: str, answer: str, index: int = None) -> Dict[str, Union[str, List[str]]]:
        """
        Parse a CoT answer into structured components for evaluation.
        
        This method extracts the final answer, intermediate steps, operations (marked with <<>>),
        and given numbers from the raw answer text. The expected format is steps followed by
        #### and the final answer.
        
        Args:
            question: The original math problem question.
            answer: The raw CoT answer containing steps and final answer (separated by ####).
            index: Optional index/ID for tracking the question.
            
        Returns:
            containing:
                - index: Question index
                - question: Original question
                - raw_answer: Complete answer text
                - final_answer: The answer after ####
                - process: List of cleaned process steps
                - operation: List of operations marked with <<>>
                - given_number: List of numbers extracted from the question
        """
        final_answer = answer.split("####")[-1].strip()
        steps = answer.split("####")[0].strip().split("\n")
        cleaned_question = re.sub(r"[\$,]", "", question)
        given_numbers = re.findall(r"(\d+(?:\.\d+)?)", cleaned_question)

        operation, process = [], []
        for step in steps:
            step = step.strip()
            ops = re.findall(r"<<([^>]+)>>", step)
            operation.extend(ops)
            cleaned_step = re.sub(r"<<([^>]+)>>", "", step)
            process.append(cleaned_step.strip())

        return {
            "index": index,
            "question": question.strip(),
            "raw_answer": answer.strip(),
            "final_answer": final_answer,
            "process": process,
            "operation": operation,
            "given_number": given_numbers
        }

    def compare_final_answer(self, reference: dict, response: dict) -> Dict[str, Any]:
        """
        Compare final answers at Level 1 (Final Answer Accuracy).
        
        Converts both reference and response final answers to floats and compares them.
        Returns 1.0 if they match exactly, 0.0 otherwise. Non-numeric answers receive 0.0.
        
        Args:
            reference: Parsed reference answer dictionary.
            response: Parsed model response dictionary.
            
        Returns:
            Dictionary with level, metric name, and score (0.0 or 1.0).
        """
        try:
            ref_num = float(reference["final_answer"])
            resp_num = float(response["final_answer"])
            return {"level": 1, "metric": "final_answer_accuracy", "score": 1.0 if ref_num == resp_num else 0.0}
        except Exception:
            return {"level": 1, "metric": "final_answer_accuracy", "score": 0.0}

    def evaluate_structure(self, reference: dict, response: dict) -> Dict[str, Any]:
        """
        Evaluate solution structure at Level 2 (Steps Ratio).
        
        Compares the number of steps in the response to the reference. Scores are higher when
        the ratio falls within acceptable bounds, with penalties for too few or too many steps.
        
        Args:
            reference: Parsed reference answer dictionary.
            response: Parsed model response dictionary.
            
        Returns:
            Dictionary with level, metric name, and score (0.2-1.0).
        """
        ratio = len(response["process"]) / max(1, len(reference["process"]))
        if self.cfg.step_ratio_lb <= ratio <= self.cfg.step_ratio_ub:
            score = 1.0
        elif ratio < self.cfg.step_ratio_lb:
            score = max(0.2, ratio / self.cfg.step_ratio_lb)
        else:
            score = max(0.5, self.cfg.step_ratio_ub / ratio)
        return {"level": 2, "metric": "steps_ratio", "score": float(round(score, 3))}

    def _parse_operation(self, ops: list) -> List[str]:
        """
        Extract mathematical operators from operation expressions.
        
        Uses regex to find operators (+, -, /, *) that appear between digits.
        
        Args:
            ops: List of operation expressions as strings.
            
        Returns:
            List of extracted operators.
        """
        PATTERN = r"(?<=\d)\s*([+\-/*])\s*(?=\d)"
        return [op for expr in ops for op in re.findall(PATTERN, expr)]

    def _parse_numbers(self, ops: list) -> List[str]:
        """
        Extract numerical values from operation expressions.
        
        Finds all integers and floating-point numbers in the expressions.
        
        Args:
            ops: List of operation expressions as strings.
            
        Returns:
            List of extracted numbers as strings.
        """
        PATTERN = r"\d+(?:\.\d+)?"
        return [n for expr in ops for n in re.findall(PATTERN, expr)]

    def _parse_words(self, process: list) -> List[str]:
        """
        Extract meaningful words from process steps.
        
        Finds words with 3 or more characters and converts them to lowercase.
        Used to compare semantic content between reference and response steps.
        
        Args:
            process: List of process step strings.
            
        Returns:
            List of extracted lowercase words.
        """
        PATTERN = r"[A-Za-z]{3,}"
        return [w.lower() for expr in process for w in re.findall(PATTERN, expr)]

    def evaluate_steps_similarity(self, reference: dict, response: dict) -> Dict[str, Any]:
        """
        Evaluate reasoning steps similarity at Level 3 (Steps Similarity).
        
        Compares reference and response steps using Jaccard similarity across three dimensions:
        - Operators: Mathematical operators used
        - Numbers: Numerical values involved
        - Words: Semantic keywords in explanations
        
        Combines these scores using configured weights to produce an overall similarity score.
        
        Args:
            reference: Parsed reference answer dictionary.
            response: Parsed model response dictionary.
            
        Returns:
            Dictionary with level, metric, overall score, individual scores for each dimension,
            and their respective weights.
        """
        ref_ops = self._parse_operation(reference["operation"])
        resp_ops = self._parse_operation(response["operation"])
        refc, respc = Counter(ref_ops), Counter(resp_ops)
        keys = set(ref_ops) | set(resp_ops)
        inter = sum(min(refc[k], respc[k]) for k in keys)
        union = sum(max(refc[k], respc[k]) for k in keys)
        ops_score = inter / union if union else 0.0

        ref_nums = self._parse_numbers(reference["operation"])
        resp_nums = self._parse_numbers(response["operation"])
        refn, respn = Counter(ref_nums), Counter(resp_nums)
        keys = set(ref_nums) | set(resp_nums)
        inter = sum(min(refn[k], respn[k]) for k in keys)
        union = sum(max(refn[k], respn[k]) for k in keys)
        num_score = inter / union if union else 0.0

        ref_words = self._parse_words(reference["process"])
        resp_words = self._parse_words(response["process"])
        keys = set(ref_words) | set(resp_words)
        word_score = (len(set(resp_words)) / len(keys)) if keys else 0.0

        similarity = self.cfg.weight_ops * ops_score + self.cfg.weight_num * num_score + self.cfg.weight_words * word_score
        return {
            "level": 3,
            "metric": "steps_similarity",
            "score": float(round(similarity, 3)),
            "individual_score": {"operators": ops_score, "number": num_score, "words": word_score},
            "weights": {"operators": self.cfg.weight_ops, "number": self.cfg.weight_num, "words": self.cfg.weight_words},
        }

    def evaluate_coherence(self, response: dict) -> Dict[str, Any]:
        """
        Evaluate logic coherence and calculation validity at Level 4 (Coherence).
        
        Validates that each operation in the response:
        - Executes correctly (calculated result matches claimed result)
        - Uses coherent inputs (values come from given numbers or previous steps)
        
        Returns scores for accuracy and coherence, with details of calculation errors.
        
        Args:
            response: Parsed model response dictionary.
            
        Returns:
            Dictionary with level, metric, combined score, individual accuracy/coherence scores,
            weights, and detailed error information.
        """
        ops = response["operation"]
        given = [float(n) for n in response["given_number"]]

        if not ops:
            return {"level": 4, "metric": "coherence", "score": 0.0, "detail": {"reason": "no operations"}}

        correct, coherent = 0, 0
        prev_results = []
        detail_errors = []

        for i, op in enumerate(ops):
            if "=" not in op:
                continue
            left, right = op.split("=")
            try:
                calculated = eval(left.strip())
                claimed = float(right.strip())
            except Exception as e:
                detail_errors.append({"step": i + 1, "operation": op, "error": str(e)})
                continue

            if calculated == claimed:
                correct += 1

            left_nums = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", left)]
            sources = set(given) | set(prev_results)
            if any(n in sources for n in left_nums):
                coherent += 1

            prev_results.append(claimed)

        denom = max(1, len([op for op in ops if "=" in op]))
        acc = correct / denom
        coh = coherent / denom
        score = self.cfg.weight_accuray * acc + self.cfg.weight_coherence * coh
        return {
            "level": 4, "metric": "coherence", "score": float(round(score, 3)),
            "individual_score": {"accuracy": acc, "coherence": coh},
            "weights": {"accuracy": self.cfg.weight_accuray, "coherence": self.cfg.weight_coherence},
            "detail": {"errors": detail_errors}
        }

    def evaluate(self, reference: dict, response: dict) -> Dict[str, Any]:
        """
        Perform comprehensive evaluation of a CoT response against reference answer.
        
        Evaluates across all four levels using configured weights, then applies decision rules:
        - Fail if Level 1 (final answer) is incorrect
        - Fail if Level 4 (coherence) falls below threshold
        - Pass if overall weighted score meets overall threshold
        - Otherwise Fail with overall score reason
        
        Args:
            reference: Parsed reference answer dictionary.
            response: Parsed model response dictionary.
            
        Returns:
            Dictionary containing overall score, pass/fail status, reason, individual scores
            for each level, detailed information for each level, and original answers.
        """
        weights = {
            'level 1': self.cfg.weight_l1,
            'level 2': self.cfg.weight_l2,
            'level 3': self.cfg.weight_l3,
            'level 4': self.cfg.weight_l4
        }
        l1 = self.compare_final_answer(reference, response)
        l2 = self.evaluate_structure(reference, response)
        l3 = self.evaluate_steps_similarity(reference, response)
        l4 = self.evaluate_coherence(response)

        scores = {"level 1": l1["score"], "level 2": l2["score"], "level 3": l3["score"], "level 4": l4["score"]}
        overall = sum(weights[k] * scores[k] for k in weights)

        # pass rule
        if scores["level 1"] < 1.0:
            status, reason = "Fail", "Final answer incorrect"
        elif scores["level 4"] < self.cfg.coherence_threshold:
            status, reason = "Fail", "Logic coherence too low"
        elif overall >= self.cfg.overall_threshold:
            status, reason = "Pass", "Excellent"
        else:
            status, reason = "Fail", f"Overall score too low ({overall:.2f})"

        return {
            "task": "cot",
            "question_id": response["index"],
            "question": response["question"],
            "overall_score": round(float(overall), 3),
            "pass_status": status,
            "pass_reason": reason,
            "individual_scores": scores,
            "level_details": {"l1": l1, "l2": l2, "l3": l3, "l4": l4},
            "reference_answer": reference["raw_answer"],
            "model_answer": response["raw_answer"],
        }

    async def run_one(self, qid: int, row) -> Dict[str, Any]:
        """
        Evaluate a single question-answer pair asynchronously.
        
        This is the main entry point for evaluating one sample. It:
        1. Loads the CoT prompt template
        2. Generates a model response using the LLM
        3. Parses both reference and model answers
        4. Runs comprehensive evaluation
        5. Returns results or error information
        
        Args:
            qid: Unique question ID.
            row: Data row containing 'question' and 'answer' fields.
            
        Returns:
            Dictionary with 'success' flag. If successful, includes question_id, task, and
            evaluation results. If failed, includes error message and task name.
        """
        question = row["question"]
        ref = row["answer"]

        cot_prompt_path = prompt_dir() / "cot_prompt.txt"
        prompt = cot_prompt_path.read_text(encoding="utf-8")
        full_prompt = f"{prompt}\n\n{question}"

        llm = await self.answer_llm.generate(
            prompt=full_prompt,
            system="You are a helpful assistant that solves math problems step by step."
        )
        if not llm["success"]:
            return {"success": False, "question_id": qid, "error": llm["error"], "task": "cot"}

        reference = self.parse(question, ref, index=qid)
        response = self.parse(question, llm["text"], index=qid)
        evaluation = self.evaluate(reference, response)

        return {"success": True, "question_id": qid, "task": "cot", "evaluation": evaluation}
