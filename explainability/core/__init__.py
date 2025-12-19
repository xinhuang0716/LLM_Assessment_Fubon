"""
XAI Core Module - Main package for explainability evaluation.

This package provides tools for evaluating model explainability through:
- CoT (Chain-of-Thought) evaluation
- Citation-based answer evaluation
- Score aggregation and result processing
"""

from . import evaluators
from . import common
from . import pipelines

__all__ = ["evaluators", "common", "pipelines"]
