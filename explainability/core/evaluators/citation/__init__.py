"""
Citation Evaluation Module - Answer assessment with citation verification.

Evaluates answer quality through citation-based metrics:
- Citation verification (entailment, source verification)
- Answer alignment with gold standard
- Support score and interpretability analysis
"""

from .evaluator import CitationEvaluator
from .parser import ResponseParser

__all__ = ["CitationEvaluator", "ResponseParser"]
