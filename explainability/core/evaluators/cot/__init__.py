"""
CoT Evaluation Module - Chain-of-Thought reasoning assessment.

Evaluates mathematical problem-solving through step-by-step reasoning:
- Level 1: Final answer accuracy
- Level 2: Solution structure analysis
- Level 3: Steps similarity using operators, numbers, and keywords
- Level 4: Logic coherence and calculation validity
"""

from .evaluator import CoTEvaluator

__all__ = ["CoTEvaluator"]
