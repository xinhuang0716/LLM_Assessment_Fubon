from typing import Dict, Any
from core.common.paths import prompt_dir
from .parser import ResponseParser
from core.config import CitationConfig

class CitationEvaluator:
    """
    Evaluates the quality of answers with citations using a two-stage pipeline.
    
    This evaluator uses two LLM calls:
    1. Answer LLM: Generates a structured answer with citations for a given question
    2. Judge LLM: Evaluates the generated answer against a gold standard reference
    
    Produces detailed metrics including citation verification, answer alignment,
    and overall quality scores.
    """
    name = "citation"

    def __init__(self, answer_llm, judge_llm, config: CitationConfig):
        """
        Initialize CitationEvaluator with LLM clients and configuration.
        
        Args:
            answer_llm: LLM client for generating cited answers.
            judge_llm: LLM client for evaluating answer quality and citation validity.
            config: CitationConfig object containing evaluation thresholds and parameters.
        """
        self.answer_llm = answer_llm
        self.judge_llm = judge_llm
        self.cfg = config
        self.parser = ResponseParser()

    async def run_one(self, qid: int, row) -> Dict[str, Any]:
        """
        Evaluate a single question-answer pair with citation assessment asynchronously.
        
        Executes the citation evaluation pipeline in two stages:
        
        Stage 1 - Answer Generation:
        - Loads citation response prompt template
        - Generates a structured answer with citations using answer_llm
        - Parses the response to extract question, answer, and citation items
        
        Stage 2 - Answer Judgment:
        - Loads citation judge prompt template
        - Constructs judge prompt with generated answer and gold standard reference
        - Judge LLM evaluates citations, answer alignment, and correctness
        - Parses judge JSON output and summarizes metrics
        
        Final decision: Pass if overall_score >= pass_threshold, else Fail.
        
        Args:
            qid: Unique question ID.
            row: Data row containing 'query' (question) and 'answer' (gold standard) fields.
            
        Returns:
            Dictionary with 'success' flag. If successful, includes:
                - question_id: The question ID
                - task: "citation"
                - evaluation: Dictionary containing:
                    - overall_score: Final evaluation score (float)
                    - pass_status: "Pass" or "Fail"
                    - pass_reason: Explanation of result
                    - metrics: Aggregated evaluation metrics
                    - judge_json: Full judge model output
                    - model_answer: Generated answer
                    - reference_answer: Gold standard answer
            
            If failed, includes error message and optionally raw outputs for debugging.
        """
        question = row["query"]
        gold = row["answer"]

        p1 = (prompt_dir() / "citation_response_prompt.txt").read_text(encoding="utf-8")
        answer_prompt = f"{p1}\n\nQuestion:\n{question}\n"
        ans = await self.answer_llm.generate(prompt=answer_prompt, system="You are a helpful assistant that solves problems.")
        if not ans["success"]:
            return {"success": False, "question_id": qid, "task": "citation", "error": ans["error"]}

        try:
            parsed = self.parser.parse_response(ans["text"])
        except Exception as e:
            return {"success": False, "question_id": qid, "task": "citation", "error": f"Answer parsing error: {e}", "raw_answer": ans["text"]}

        p2 = (prompt_dir() / "citation_judge_prompt.txt").read_text(encoding="utf-8")
        judge_prompt = f"""
                ## Input
                **Question**:
                {parsed['question']}

                **Gold Standard Answer** (from dataset):
                {gold}

                **AI Generated Answer** (with citation markers):
                {parsed['answer']}

                **Citation Details**:
                {parsed['citations_raw']}

                {p2}
                """.strip()

        j = await self.judge_llm.generate(prompt = judge_prompt, system = "You are a judgement assistant")
        if not j["success"]:
            return {"success": False, "question_id": qid, "task": "citation", "error": j["error"]}

        try:
            judge_json = self.parser.parse_judge_json(j["text"])
            metrics = self.parser.summarize_metrics(judge_json)
        except Exception as e:
            return {"success": False, "question_id": qid, "task": "citation", "error": f"Judge parsing error: {e}", "raw_judge": j["text"]}
        
        status = "Pass" if metrics["overall_score"] >= self.cfg.pass_threshold else "Fail"

        evaluation = {
            "task": "citation",
            "question_id": qid,
            "question": question,
            "overall_score": float(metrics["overall_score"]),
            "pass_status": status,
            "pass_reason": "OK" if status == "Pass" else f"Overall score < {self.cfg.pass_threshold}",
            "metrics": metrics,
            "judge_json": judge_json,
            "reference_answer": gold,
            "model_answer": parsed["answer"],
        }

        return {"success": True, "question_id": qid, "task": "citation", "evaluation": evaluation}
