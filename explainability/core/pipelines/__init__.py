"""
Pipelines Module - Orchestration of evaluation workflows.

Provides main execution pipelines:
- run_all: Orchestrates CoT and Citation evaluation with configurable sampling
"""

from .run_all import run_all

__all__ = ["run_all"]
