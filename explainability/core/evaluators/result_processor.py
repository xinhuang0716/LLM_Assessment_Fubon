from typing import Dict, List, Tuple, Any

class ResultProcessor:    
    @staticmethod
    def process_reports(reports: List[Dict[str, Any]]) -> Tuple[Dict, Dict, List[float], List[float]]:
        """
        Process multiple evaluation reports and aggregate results into structured records and score lists.
        
        This method orchestrates the processing of reports from different evaluation tasks (CoT and Citation),
        routing each report to the appropriate processor based on the evaluator type. It consolidates successful
        results, failed results, and scores from both evaluation mechanisms into separate collections.
        
        Args:
            reports: A list of reports returned by run_all, where each report contains:
                metadata: Dictionary with 'evaluator' (task name) and 'start_time'
                successful_results: List of successful evaluation results
                failed_results: List of failed evaluation results 

        Returns:

            success_records: A dictionary of successful results keyed by 'task::question_id'
            failed_results: A dictionary of failed results keyed by 'task::question_id'
            cot_scores: A list of all scores from CoT evaluation
            citation_scores: A list of all scores from Citation evaluation
        """
        success_records = {}
        failed_results = {}
        
        cot_scores = []
        citation_scores = []
        
        for report in reports:
            task_name = report["metadata"]["evaluator"]
            start_time = report['metadata']['start_time']
            successful_results = report.get("successful_results", [])
            failed_results_list = report.get('failed_results', [])
            
            if task_name.lower() == "cot":
                ResultProcessor._process_cot_results(
                    successful_results=successful_results,
                    failed_results_list=failed_results_list,
                    task_name=task_name,
                    start_time=start_time,
                    success_records=success_records,
                    failed_results=failed_results,
                    scores=cot_scores,
                )
                
            elif task_name.lower() == "citation":
                ResultProcessor._process_citation_results(
                    successful_results=successful_results,
                    failed_results_list=failed_results_list,
                    task_name=task_name,
                    start_time=start_time,
                    success_records=success_records,
                    failed_results=failed_results,
                    scores=citation_scores,
                )
        
        return success_records, failed_results, cot_scores, citation_scores
    
    @staticmethod
    def _process_cot_results(successful_results: List[Dict], failed_results_list: List[Dict], task_name: str, start_time: str, success_records: Dict, failed_results: Dict, scores: List[float]) -> None:
        """
        Process Chain-of-Thought (CoT) evaluation results and extract structured records.
        
        This method handles both successful and failed CoT evaluation results, transforming them
        into standardized record formats with multi-level individual scores and collecting scores
        for aggregation. Each result is keyed by a combination of task name and question ID for 
        easy retrieval.
        
        Args:
            successful_results: List of successfully evaluated CoT results containing evaluation data.
            failed_results_list: List of failed CoT results with error information.
            task_name: Name identifier for the task (e.g., "CoT").
            start_time: Timestamp when the evaluation started.
            success_records: Dictionary to accumulate successful result records (modified in-place).
            failed_results: Dictionary to accumulate failed result records (modified in-place).
            scores: List to accumulate individual scores from successful results (modified in-place).
            
        Returns:
            None. This method modifies the input dictionaries and lists directly.
        """
        for result in successful_results:
            qid = result.get("question_id")
            cot_key = f"{task_name.lower()}::{qid}"
            evaluation = result.get("evaluation", {})
            
            record = {
                "task": task_name,
                "start_time": start_time,
                "question_id": result.get("question_id"),
                "question": evaluation.get("question"),
                "reference_answer": evaluation.get("reference_answer"),
                "model_answer": evaluation.get("model_answer"),
                "overall_score": evaluation.get("overall_score"),
                'indivual_score': {
                    'level 1': evaluation['individual_score']['level 1'],
                    'level 2': evaluation['individual_score']['level 2'],
                    'level 3': evaluation['individual_score']['level 3'],
                    'level 4': evaluation['individual_score']['level 4'],
                },
                'level_details': evaluation.get('level_details'),
                "pass_status": evaluation.get("pass_status"),
                "pass_reason": evaluation.get("pass_reason"),
            }
            success_records[cot_key] = record
            scores.append(evaluation.get("overall_score"))
        
        for result in failed_results_list:
            result_task_name = result.get('task', '')
            qid = result.get('question_id')
            cot_key = f"{result_task_name.lower()}::{qid}"
            
            record = {
                'task': result_task_name,
                "question_id": qid,
                'error': result['error']
            }
            failed_results[cot_key] = record
    
    @staticmethod
    def _process_citation_results(successful_results: List[Dict], failed_results_list: List[Dict], task_name: str, start_time: str, success_records: Dict, failed_results: Dict, scores: List[float]) -> None:
        """
        Process Citation evaluation results and extract structured records with detailed metrics.
        
        This method processes citation evaluation results from the judge model, extracting citation
        evaluations and detailed judgment information. Like _process_cot_results, it handles both
        successful and failed results, storing them in standardized record formats with richer nested
        judgment information (answer evaluation, overall assessment) specific to citation evaluation.
        
        Args:
            successful_results: List of successfully evaluated Citation results containing judge_json data.
            failed_results_list: List of failed Citation results with error information.
            task_name: Name identifier for the task (e.g., "Citation").
            start_time: Timestamp when the evaluation started.
            success_records: Dictionary to accumulate successful result records (modified in-place).
            failed_results: Dictionary to accumulate failed result records (modified in-place).
            scores: List to accumulate individual scores from successful results (modified in-place).
            
        Returns:
            None. This method modifies the input dictionaries and lists directly.
        """


        for result in successful_results:
            qid = result.get('question_id')
            citation_key = f"{task_name}::{qid}"
            evaluation = result.get('evaluation', {})
            
            record = {
                "task": task_name,
                "start_time": start_time,
                "question_id": result.get("question_id"),
                "question": evaluation.get("question"),
                "reference_answer": evaluation.get("reference_answer"),
                "model_answer": evaluation.get("model_answer"),
                "overall_score": evaluation['judge_json']['overall_assessment']['overall_score'],
                "citations": evaluation['judge_json']['citation_evaluations'],
                "indivual_score": evaluation.get("metrics"),
                "answer_judgement_details": evaluation['judge_json']['answer_evaluation'],
                "overall_judgement_details": evaluation['judge_json']['overall_assessment'],
                "pass_status": evaluation.get("pass_status"),
                "pass_reason": evaluation.get("pass_reason"),
            }
            success_records[citation_key] = record
            scores.append(evaluation['judge_json']['overall_assessment']['overall_score'])
        
        for result in failed_results_list:
            result_task_name = result.get('task', '')
            qid = result.get('question_id')
            citation_key = f"{result_task_name.lower()}::{qid}"
            
            record = {
                'task': result_task_name,
                "question_id": qid,
                'error': result['error']
            }
            failed_results[citation_key] = record
    
