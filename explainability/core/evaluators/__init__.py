"""
Evaluators Module - Assessment tools for different evaluation mechanisms.

Provides evaluators and utilities for:
- CoT (Chain-of-Thought) evaluation
- Citation-based answer assessment
- Result processing and score aggregation
"""

from . import cot
from . import citation
from .result_processor import ResultProcessor
from .score_aggregator import ScoreAggregator

__all__ = ["cot", "citation", "ResultProcessor", "ScoreAggregator"]
