import re, json
from typing import Dict, Any
import numpy as np

class ResponseParser:
    """
    Parses citation evaluation responses and judge JSON outputs.
    
    Handles extraction of structured information from model responses including questions,
    answers, citation items with their claims and sources, and detailed evaluation metrics
    from judge model outputs.
    """
    
    def parse_response(self, response: str) -> Dict[str, Any]:
        """
        Parse structured response containing question, answer, and citations.
        
        Extracts sections marked with ## headers (Question, Answer, Sources) and parses
        individual citation items from the Sources section. Citation items are identified
        by ### [N] markers and contain fields for claim, source type, name, URL, and content.
        
        Args:
            response: String response from the model in expected markdown format with sections
                     separated by ## and citation items separated by ### [N].
                     
        Returns:
            containing:
                - question: Extracted question text
                - answer: Extracted answer text
                - citations_raw: Raw citation block text
                - citation_items: List of parsed citation dictionaries, each with:
                    - index: Citation number (int)
                    - claim: The cited claim (str)
                    - source_type: Type of source (str)
                    - source_name: Name of the source (str)
                    - url: URL or reference (str)
                    - content: Source content (str)
        """
        m_q = re.search(r"##\s*Question:\s*(.*?)\n\s*##", response, flags=re.S)
        question = m_q.group(1).strip() if m_q else None

        m_a = re.search(r"##\s*Answer:\s*(.*?)\n\s*##", response, flags=re.S)
        answer = m_a.group(1).strip() if m_a else None

        m_c = re.search(r"##\s*Sources:\s*(.*)$", response, flags=re.S)
        citation_block = m_c.group(1).strip() if m_c else ""

        items = re.findall(r"###\s*\[(\d+)\]\s*(.*?)(?=\n###\s*\[\d+\]|\Z)", citation_block, flags=re.S)

        citation_items = []
        for idx, block in items:
            def grab(label):
                m = re.search(rf"-\s*\*\*{label}\*\*:\s*(.*?)(?=\n-\s*\*\*|\Z)", block, flags=re.S)
                return m.group(1).strip() if m else None

            content = grab("Content")
            if content:
                content = re.sub(r"^\s*>\s*", "", content, flags=re.M).strip()

            citation_items.append({
                "index": int(idx),
                "claim": grab("Claim"),
                "source_type": grab("Source Type"),
                "source_name": grab("Source Name"),
                "url": grab("URL/Reference"),
                "content": content,
            })

        return {
            "question": question,
            "answer": answer,
            "citations_raw": citation_block,
            "citation_items": citation_items
        }

    def parse_judge_json(self, response: str) -> Dict[str, Any]:
        """
        Parse JSON output from the judge model evaluating citation quality.
        
        Attempts to extract JSON from the response in multiple ways:
        1. First looks for JSON within ```json``` code fences
        2. Falls back to parsing the entire response as JSON
        3. As a last resort, searches for any JSON object pattern within the response
        
        Args:
            response: String response from the judge model, may contain JSON in various formats.
            
        Returns:
            Parsed JSON dictionary containing judge evaluation results including
            citation_evaluations, answer_evaluation, and overall_assessment sections.
            
        Raises:
            ValueError: If no valid JSON can be extracted from the response.
        """
        response = response.lstrip("\ufeff").strip()
        fenced = re.findall(r"```json\s*(.*?)\s*```", response, flags=re.DOTALL | re.IGNORECASE)
        if fenced:
            return json.loads(fenced[0].strip())

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            m = re.search(r"\{.*\}", response, re.DOTALL)
            if m:
                return json.loads(m.group(0))
            raise ValueError("Could not parse JSON from judge response.")

    def summarize_metrics(self, judge_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Summarize and aggregate citation evaluation metrics from judge JSON output.
        
        Calculates aggregated statistics from individual citation evaluations:
        - Average support score across all citations
        - Entailment rate (percentage of citations with ENTAILMENT judgment)
        - Verification rate (percentage of citations with VERIFIED judgment)
        - Average interpretability score
        
        Also includes overall answer correctness and final overall score.
        Returns default values (zeros) if no citations exist.
        
        Args:
            judge_json: Parsed judge evaluation output dictionary containing:
                - citation_evaluations: List of individual citation evaluations
                - answer_evaluation: Contains alignment_judgement and correctness_score
                - overall_assessment: Contains final overall_score
                
        Returns:
            containing:
                - total_citations: Number of citations (int)
                - avg_support_score: Average support score (float, 0-1)
                - entailment_rate: Proportion of entailed citations (float, 0-1)
                - verified_rate: Proportion of verified citations (float, 0-1)
                - interpretability_score: Average interpretability (float, 0-1)
                - correctness: String judgment of answer correctness
                - correctness_score: Score of answer correctness (float)
                - overall_score: Final aggregated evaluation score (float)
        """
        citations = judge_json.get("citation_evaluations", [])
        if not citations:
            return {
                "total_citations": 0,
                "avg_support_score": 0.0,
                "entailment_rate": 0.0,
                "verified_rate": 0.0,
                "interpretability_score": 0.0,
                "correctness": judge_json.get("answer_evaluation", {}).get("alignment_judgement"),
                "correctness_score": judge_json.get("answer_evaluation", {}).get("correctness_score", 0.0),
                "overall_score": judge_json.get("overall_assessment", {}).get("overall_score", 0.0),
            }

        entail = sum(1 for c in citations if c.get("citation_support", {}).get("judgement") == "ENTAILMENT")
        verified = sum(1 for c in citations if c.get("source_verification", {}).get("judgement") == "VERIFIED")
        support_scores = [c.get("citation_support", {}).get("support_score", 0.0) for c in citations]
        interp_scores = [c.get("interpretability_score", 0.0) for c in citations]

        return {
            "total_citations": len(citations),
            "avg_support_score": float(np.mean(support_scores)),
            "entailment_rate": entail / len(citations),
            "verified_rate": verified / len(citations),
            "interpretability_score": float(np.mean(interp_scores)),
            "correctness": judge_json["answer_evaluation"]["alignment_judgement"],
            "correctness_score": judge_json["answer_evaluation"]["correctness_score"],
            "overall_score": judge_json["overall_assessment"]["overall_score"],
        }
