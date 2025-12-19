from typing import Dict, List, Any
import numpy as np
from core.config import CoTConfig, CitationConfig, OverallConfig

class ScoreAggregator:    
    def __init__(self):
        """
        Initialize ScoreAggregator with configuration objects for each evaluation mechanism.
        
        Loads configuration settings for:
        - CoT evaluation thresholds and parameters
        - Citation evaluation thresholds and parameters
        - Overall aggregation weights and pass thresholds
        """
        self.cot_config = CoTConfig()
        self.citation_config = CitationConfig()
        self.overall_config = OverallConfig()
    
    def aggregate_scores(self, cot_scores: List[float], citation_scores: List[float], cot_model: str, citation_response_model: str, citation_judge_model: str) -> Dict[str, Any]:
        """
        Aggregate evaluation scores from CoT and Citation.
        
        This method computes individual averages for each evaluation mechanism, checks them against
        their respective thresholds, then combines them using configured weights to produce an overall
        score. The result includes detailed pass/fail status and threshold information for analysis
        and debugging.
        
        Args:
            cot_scores: List of numerical scores from Chain-of-Thought evaluation (0.0-1.0 or similar range).
            citation_scores: List of numerical scores from Citation evaluation (0.0-1.0 or similar range).
            
        Returns:
            containing:
                - XAI_overall_score: Weighted combined score (float)
                - overall_pass: Boolean indicating if overall score meets the threshold
                - overall_threshold: The overall pass threshold used (float)
                - cot: (Dict)
                    - avg_score: Average CoT score (float)
                    - count: Number of CoT samples (int)
                    - pass: Whether CoT average meets its threshold (bool)
                    - threshold: CoT threshold (float)
                - citation: (Dict)
                    - avg_score: Average Citation score (float)
                    - count: Number of Citation samples (int)
                    - pass: Whether Citation average meets its threshold (bool)
                    - threshold: Citation threshold (float)
                - weights: (Dict)
                    - weight_cot: Weight assigned to CoT in aggregation (float)
                    - weight_citation: Weight assigned to Citation in aggregation (float)
        """

        avg_cot = np.mean(cot_scores) if cot_scores else 0.0
        avg_citation = np.mean(citation_scores) if citation_scores else 0.0
        
        cot_pass = avg_cot >= self.cot_config.avg_overall_threshold
        citation_pass = avg_citation >= self.citation_config.avg_overall_threshold
        
        weighted_total = (
            avg_cot * self.overall_config.weight_cot +
            avg_citation * self.overall_config.weight_citation
        )
        
        overall_pass = weighted_total >= self.overall_config.xai_pass_threshold
        
        task_scores = {
            'XAI_overall_score': round(float(weighted_total),3),
            'overall_pass': bool(overall_pass),
            'overall_threshold': float(self.overall_config.xai_pass_threshold),
            'cot': {
                'model': cot_model,
                'avg_score': round(float(avg_cot),3),
                'count': len(cot_scores),
                'pass': bool(cot_pass),
                'threshold': float(self.cot_config.avg_overall_threshold),
            },
            'citation': {
                'response_model': citation_response_model,
                'judge_model': citation_judge_model,
                'avg_score': float(avg_citation),
                'count': len(citation_scores),
                'pass': bool(citation_pass),
                'threshold': float(self.citation_config.avg_overall_threshold),
            },
            'weights': {
                'weight_cot': float(self.overall_config.weight_cot),
                'weight_citation': float(self.overall_config.weight_citation),
            },
        }
        
        return task_scores
    
